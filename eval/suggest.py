"""Suggest evaluation questions from the corpus with an LLM, for people to review (decision D9).

Every suggested `normal` question keeps only if its evidence occurs verbatim in the source text.
Writes eval/candidates.jsonl; nothing enters eval/questions.jsonl without review.
Usage: python -m eval.suggest [--per-document 8]
"""

import argparse
import json
import random
import re
from pathlib import Path

from assistant.answer import chat_model
from assistant.chunking import split_corpus
from assistant.corpus import load_pages
from assistant.settings import load_settings

OUTPUT = Path(__file__).resolve().parents[1] / "eval" / "candidates.jsonl"

NORMAL_PROMPT = """Você escreve perguntas de avaliação para um assistente das normas de um programa de pós-graduação.
A partir do trecho abaixo, escreva UMA pergunta que um aluno de mestrado ou doutorado faria e que o trecho responde.
Não copie as palavras da norma na pergunta. Copie em "evidence" a menor frase do trecho que comprova a resposta,
exatamente como está, sem mudar nenhum caractere. Escreva também a mesma pergunta em linguagem informal de aluno.
Responda só com JSON: {"question": "...", "informal": "...", "reference_answer": "...", "evidence": "..."}

Trecho:
"""

EXTRA_PROMPT = """Escreva perguntas curtas em português para testar um assistente das normas do Programa de Pós-Graduação em
Ciência da Computação da UFC. O assistente só conhece: regimento interno, normas gerais da pós-graduação da UFC,
normas do colegiado (professores externos, PROAP, seleção do colegiado) e páginas de procedimentos (requisitos de
conclusão, aproveitamento de disciplinas, proficiência em inglês, agendamento de defesas, diploma, lista de disciplinas).
- "not_found": 8 perguntas sobre o programa que esses documentos NÃO respondem (ex.: valor de bolsa, datas do semestre).
- "out_of_scope": 8 perguntas fora do tema (saúde, aconselhamento jurídico pessoal, opinião sobre professores, outros assuntos).
Metade em linguagem formal, metade informal. Responda só com JSON:
{"not_found": [{"question": "...", "style": "formal|informal"}], "out_of_scope": [...]}"""


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def ask_json(chat, prompt: str) -> dict:
    content = chat.invoke([("human", prompt)]).content
    found = re.search(r"\{.*\}", content, re.DOTALL)
    return json.loads(found.group(0)) if found else {}


def normal_questions(chat, per_document: int, seed: int = 7) -> list[dict]:
    chunks = [c for c in split_corpus(load_pages()) if c.metadata["article"] and len(c.page_content) > 250]
    by_document: dict[str, list] = {}
    for chunk in chunks:
        by_document.setdefault(chunk.metadata["doc_id"], []).append(chunk)
    picked = [c for group in by_document.values() for c in random.Random(seed).sample(group, min(per_document, len(group)))]
    procedures = [c for c in split_corpus(load_pages()) if not c.metadata["article"] and c.metadata["doc_id"] != "regimento-interno"
                  and not c.metadata["doc_id"].startswith(("resolucao", "norma"))]
    candidates = []
    for chunk in picked + procedures:
        body = chunk.page_content.split("\n", 1)[1]
        try:
            data = ask_json(chat, NORMAL_PROMPT + body)
        except (json.JSONDecodeError, ValueError):
            continue
        evidence = data.get("evidence", "")
        if not evidence or flat(evidence) not in flat(body):
            continue
        base = f"{chunk.metadata['doc_id']}-{(chunk.metadata['article'] or 'p').lower().replace(' ', '').replace(',', '').replace('.', '')}"
        common = {"category": "normal", "reference_answer": data["reference_answer"], "evidence": evidence,
                  "doc_id": chunk.metadata["doc_id"], "pair_id": base, "source": "llm-suggested"}
        candidates.append({"id": base, "question": data["question"], "style": "formal", **common})
        if data.get("informal"):
            candidates.append({"id": f"{base}-informal", "question": data["informal"], "style": "informal", **common})
    return candidates


def extra_questions(chat) -> list[dict]:
    data = ask_json(chat, EXTRA_PROMPT)
    return [
        {"id": f"{category.replace('_', '-')}-{n}", "question": item["question"], "category": category,
         "style": item.get("style", "formal"), "source": "llm-suggested"}
        for category in ("not_found", "out_of_scope")
        for n, item in enumerate(data.get(category, []), start=1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-document", type=int, default=8)
    args = parser.parse_args()
    settings = load_settings()
    chat = chat_model(settings, settings.judge_model, json_output=True)
    candidates = normal_questions(chat, args.per_document) + extra_questions(chat)
    seen, unique = set(), []
    for candidate in candidates:
        if candidate["id"] not in seen:
            seen.add(candidate["id"])
            unique.append(candidate)
    OUTPUT.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in unique))
    print(f"{len(unique)} candidates in eval/candidates.jsonl")


if __name__ == "__main__":
    main()
