"""Answer one question: mask it, retrieve the chunks, generate, and keep the cited sources.

Usage: python -m assistant.answer "Qual o prazo para a qualificação?" [--model gpt-oss:120b]
"""

import argparse
import re
import time
from dataclasses import dataclass, field

from langchain_core.documents import Document

from assistant.privacy import mask
from assistant.prompts import build_messages
from assistant.settings import Settings, load_settings, require_api_key

CITATION_MARK = re.compile(r"[\[【](\d+)[\]】]")


@dataclass
class Answer:
    question: str
    text: str
    citations: list[dict]
    retrieved: list[dict]
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: int = 0
    extra: dict = field(default_factory=dict)


def source_of(chunk: Document) -> dict:
    keys = ("doc_id", "title", "article", "doc_date", "url", "page")
    return {key: chunk.metadata.get(key) for key in keys}


def retrieved_of(chunk: Document) -> dict:
    excerpt = chunk.page_content.split("\n", 1)[-1]
    return {**source_of(chunk), "similarity": chunk.metadata.get("similarity"), "excerpt": excerpt}


def cited_sources(text: str, chunks: list[Document]) -> list[dict]:
    numbers = sorted({int(n) for n in CITATION_MARK.findall(text) if 1 <= int(n) <= len(chunks)})
    return [{"n": n, **source_of(chunks[n - 1])} for n in numbers]


def chat_model(settings: Settings, model: str, json_output: bool = False):
    from langchain_ollama import ChatOllama

    headers = {"Authorization": f"Bearer {require_api_key(settings)}"}
    return ChatOllama(
        model=model,
        base_url=settings.chat_url,
        temperature=0,
        format="json" if json_output else None,
        client_kwargs={"headers": headers},
    )


def answer_question(question: str, chunks_for, chat) -> Answer:
    """`chunks_for(question)` returns the retrieved chunks; `chat` is a LangChain chat model."""
    question = mask(question)
    chunks = chunks_for(question)
    started = time.perf_counter()
    reply = chat.invoke(build_messages(question, chunks))
    latency_ms = round((time.perf_counter() - started) * 1000)
    usage = getattr(reply, "usage_metadata", None) or {}
    return Answer(
        question=question,
        text=reply.content,
        citations=cited_sources(reply.content, chunks),
        retrieved=[retrieved_of(chunk) for chunk in chunks],
        prompt_tokens=usage.get("input_tokens", 0),
        completion_tokens=usage.get("output_tokens", 0),
        latency_ms=latency_ms,
    )


def main() -> None:
    from assistant.retrieve import retriever

    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--model")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    settings = load_settings()
    model = args.model or settings.chat_models[0]
    answer = answer_question(args.question, retriever(settings, settings.collection, args.k), chat_model(settings, model))
    print(answer.text)
    for citation in answer.citations:
        label = ", ".join(part for part in (citation["title"], citation["article"]) if part)
        print(f"[{citation['n']}] {label} ({citation['doc_date']}) {citation['url']}")
    print(f"{model}: {answer.prompt_tokens}+{answer.completion_tokens} tokens, {answer.latency_ms} ms")


if __name__ == "__main__":
    main()
