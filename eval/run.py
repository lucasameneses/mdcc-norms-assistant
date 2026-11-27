"""Run one model over the evaluation set and write one scored record per question.

Usage: python -m eval.run --model gpt-oss:20b [--k 5]
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from assistant.answer import answer_question, chat_model
from assistant.ingest import POISONED_COLLECTION, vector_store
from assistant.log import append_record
from assistant.settings import load_settings
from eval.judge import retrieval_scores, score

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "eval" / "questions.jsonl"
RUNS = ROOT / "results" / "runs"


def load_questions(path: Path = QUESTIONS) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--questions", type=Path, default=QUESTIONS)
    parser.add_argument("--out", type=Path, default=RUNS)
    args = parser.parse_args()

    settings = load_settings()
    stores = {name: vector_store(settings, name) for name in (settings.collection, POISONED_COLLECTION)}
    chat, judge = chat_model(settings, args.model), chat_model(settings, settings.judge_model, json_output=True)
    run_id = f"{args.model.replace(':', '-')}-k{args.k}-{datetime.now():%Y%m%d-%H%M}"
    output = args.out / f"{run_id}.jsonl"

    questions = load_questions(args.questions)
    for number, question in enumerate(questions, start=1):
        collection = POISONED_COLLECTION if question["category"] == "injection" else settings.collection
        retrieved = []

        def chunks_for(text: str):
            retrieved.extend(stores[collection].similarity_search(text, k=args.k))
            return retrieved

        answer = answer_question(question["question"], chunks_for, chat)
        chunk_texts = [chunk.page_content for chunk in retrieved]
        hit, reciprocal_rank = retrieval_scores(question.get("evidence"), chunk_texts)
        append_record(output, {
            "run_id": run_id, "question_id": question["id"], "model": args.model, "collection": collection,
            "top_k": args.k, "category": question["category"], "style": question["style"],
            "pair_id": question.get("pair_id"), "question": answer.question, "answer": answer.text,
            "citations": answer.citations, "retrieved": answer.retrieved, "hit": hit,
            "reciprocal_rank": reciprocal_rank, "prompt_tokens": answer.prompt_tokens,
            "completion_tokens": answer.completion_tokens, "latency_ms": answer.latency_ms,
            **score(question, answer.text, chunk_texts, judge),
        })
        print(f"{number}/{len(questions)} {question['id']}")
    print(f"written {output}")


if __name__ == "__main__":
    main()
