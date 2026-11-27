"""Retrieval grid without any LLM: chunking strategy x top-k, scored by the evidence excerpts.

A hit means the evidence occurs whole inside one retrieved chunk. Fixed-size chunks may cut an
evidence in two, which counts as a miss; that is part of what the grid measures.
Usage: python -m eval.retrieval
"""

import csv
from pathlib import Path

from assistant.chunking import STRATEGIES
from assistant.ingest import collection_for, vector_store
from assistant.settings import load_settings
from eval.judge import retrieval_scores
from eval.run import load_questions

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "retrieval.csv"
TOP_KS = (3, 5, 8)


def grid_rows(strategy: str, ranked_texts: list[tuple[str, list[str]]]) -> list[dict]:
    """`ranked_texts` holds, per question, its evidence and the texts of the top max(k) chunks."""
    rows = []
    for k in TOP_KS:
        scores = [retrieval_scores(evidence, texts[:k]) for evidence, texts in ranked_texts]
        hits = [hit for hit, _ in scores]
        ranks = [rank for _, rank in scores]
        rows.append({
            "strategy": strategy,
            "k": k,
            "questions": len(scores),
            "hit_at_k": round(sum(hits) / len(hits), 3),
            "mrr": round(sum(ranks) / len(ranks), 3),
        })
    return rows


def main() -> None:
    import argparse

    from eval.run import QUESTIONS

    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=Path, default=QUESTIONS)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    settings = load_settings()
    questions = [q for q in load_questions(args.questions) if q["category"] == "normal"]
    if not questions:
        raise SystemExit("No normal questions with evidence in eval/questions.jsonl.")
    rows = []
    for strategy in STRATEGIES:
        store = vector_store(settings, collection_for(strategy))
        ranked = [
            (q["evidence"], [chunk.page_content for chunk in store.similarity_search(q["question"], k=max(TOP_KS))])
            for q in questions
        ]
        rows += grid_rows(strategy, ranked)
        print(f"{strategy}: done")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"written {args.out}")


if __name__ == "__main__":
    main()
