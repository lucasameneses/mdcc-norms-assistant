"""Pick answers for the human evaluation, with the model hidden.

Writes results/human/sample.csv (for the raters) and results/human/key.csv (sample -> model).
Usage: python -m eval.human_sample [--size 20]
"""

import argparse
from pathlib import Path

import pandas as pd

from eval.report import load_runs

HUMAN = Path(__file__).resolve().parents[1] / "results" / "human"
SCORE_COLUMNS = ["correcao_1a5", "utilidade_1a5", "clareza_1a5", "comentario"]


def sources_text(citations: list[dict]) -> str:
    return "; ".join(f"{c['title']}, {c['article']}" if c.get("article") else c["title"] for c in citations)


def draw_sample(runs: pd.DataFrame, size: int, seed: int = 42) -> pd.DataFrame:
    normal = runs[runs.category == "normal"]
    sample = normal.sample(n=min(size, len(normal)), random_state=seed).reset_index(drop=True)
    sample.insert(0, "sample_id", [f"s{n:02d}" for n in range(1, len(sample) + 1)])
    return sample


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=20)
    args = parser.parse_args()
    sample = draw_sample(load_runs(), args.size)
    HUMAN.mkdir(parents=True, exist_ok=True)
    sheet = pd.DataFrame({
        "sample_id": sample.sample_id,
        "pergunta": sample.question,
        "resposta": sample.answer,
        "fontes": sample.citations.map(sources_text),
    })
    for column in SCORE_COLUMNS:
        sheet[column] = ""
    sheet.to_csv(HUMAN / "sample.csv", index=False)
    sample[["sample_id", "run_id", "model", "question_id"]].to_csv(HUMAN / "key.csv", index=False)
    print(f"{len(sheet)} answers in results/human/sample.csv")


if __name__ == "__main__":
    main()
