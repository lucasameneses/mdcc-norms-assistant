"""Aggregate every run in results/runs into results/summary.md.

Usage: python -m eval.report
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "results" / "runs"
RETRIEVAL = ROOT / "results" / "retrieval.csv"
MODELS = ROOT / "results" / "reference_models.csv"
EMBEDDING_MEMORY = ROOT / "results" / "embedding_memory.csv"
SUMMARY = ROOT / "results" / "summary.md"


def load_runs(runs: Path = RUNS) -> pd.DataFrame:
    files = sorted(runs.glob("*.jsonl"))
    if not files:
        raise SystemExit("No runs in results/runs: run python -m eval.run first.")
    return pd.concat((pd.read_json(file, lines=True) for file in files), ignore_index=True)


def markdown(frame: pd.DataFrame) -> str:
    frame = frame.reset_index()
    cells = [[f"{value:.2f}" if isinstance(value, float) else str(value) for value in row] for row in frame.itertuples(index=False)]
    header = "| " + " | ".join(map(str, frame.columns)) + " |"
    rule = "|" + "---|" * len(frame.columns)
    return "\n".join([header, rule] + ["| " + " | ".join(row) + " |" for row in cells])


def quality(runs: pd.DataFrame) -> pd.DataFrame:
    normal = runs[runs.category == "normal"]
    return normal.groupby("model").agg(
        questions=("question_id", "count"),
        hit_at_k=("hit", "mean"),
        mrr=("reciprocal_rank", "mean"),
        correctness=("correctness", "mean"),
        faithfulness=("faithfulness", "mean"),
        citation=("citation", "mean"),
        passed=("passed", "mean"),
    )


def by_style(runs: pd.DataFrame) -> pd.DataFrame:
    paired = runs[runs.pair_id.notna()] if "pair_id" in runs else runs.iloc[0:0]
    return paired.pivot_table(index="model", columns="style", values="passed", aggfunc="mean")


def security(runs: pd.DataFrame) -> pd.DataFrame:
    table = runs.pivot_table(index="model", columns="category", values="passed", aggfunc="mean")
    normal = runs[runs.category == "normal"]
    table["answers_without_source"] = normal.groupby("model").citations.apply(lambda c: c.map(len).eq(0).mean())
    return table


def cost_and_latency(runs: pd.DataFrame) -> pd.DataFrame:
    return runs.groupby("model").agg(
        prompt_tokens=("prompt_tokens", "mean"),
        completion_tokens=("completion_tokens", "mean"),
        latency_p50_ms=("latency_ms", lambda s: s.quantile(0.5)),
        latency_p95_ms=("latency_ms", lambda s: s.quantile(0.95)),
    )


def estimates(runs: pd.DataFrame, models: pd.DataFrame) -> pd.DataFrame:
    """Estimated cost per 1000 questions (reference prices) and weight memory per generator."""
    means = runs.groupby("model")[["prompt_tokens", "completion_tokens"]].mean()
    table = means.join(models.set_index("model"), how="inner")
    table["usd_per_1000_questions"] = 1000 * (
        table.prompt_tokens * table.usd_per_input_token + table.completion_tokens * table.usd_per_output_token
    )
    table["weights_gb"] = table.parameters * table.bits_per_weight / 8 / 1e9
    return table[["quantization", "usd_per_1000_questions", "weights_gb"]]


def build_summary(runs: pd.DataFrame) -> str:
    sections = [
        ("Answer and retrieval quality (normal questions, scores 0-2, rates 0-1)", quality(runs)),
        ("Formal versus informal phrasing (pass rate)", by_style(runs)),
        ("Security and bias tests (pass rate per category)", security(runs)),
        ("Tokens and latency per answer", cost_and_latency(runs)),
    ]
    if MODELS.is_file():
        sections.append(("Estimated cost and memory (see results/README.md)", estimates(runs, pd.read_csv(MODELS))))
    if EMBEDDING_MEMORY.is_file():
        sections.append(("Measured memory of the local embedding container", pd.read_csv(EMBEDDING_MEMORY).set_index("model")))
    if RETRIEVAL.is_file():
        grid = pd.read_csv(RETRIEVAL).set_index(["strategy", "k"])
        sections.insert(0, ("Retrieval grid: chunking strategy x top-k (no LLM)", grid))
    body = [f"# Evaluation summary\n\nRuns: {', '.join(sorted(runs.run_id.unique()))}"]
    body += [f"## {title}\n\n{markdown(table)}" for title, table in sections]
    return "\n\n".join(body) + "\n"


def main() -> None:
    SUMMARY.write_text(build_summary(load_runs()))
    print(f"written {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
