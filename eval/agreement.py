"""Human evaluation summary: mean scores, agreement between raters, and agreement with the judge.

Each rater fills a copy of results/human/sample.csv and saves it as
results/human/ratings/<rater>.csv. Scores are integers from 1 to 5.
Usage: python -m eval.agreement
"""

from pathlib import Path

import krippendorff
import pandas as pd

from eval.report import load_runs, markdown

HUMAN = Path(__file__).resolve().parents[1] / "results" / "human"
CRITERIA = {"correcao_1a5": "correctness", "utilidade_1a5": "usefulness", "clareza_1a5": "clarity"}


def _check_scores(frame: pd.DataFrame, name: str) -> None:
    for column in CRITERIA:
        scores = pd.to_numeric(frame[column], errors="coerce")
        out_of_scale = scores.isna() | scores.mod(1).ne(0) | scores.lt(1) | scores.gt(5)
        if out_of_scale.any():
            raise SystemExit(f"{name}: {column} must be integers from 1 to 5.")


def load_ratings(folder: Path = HUMAN / "ratings") -> pd.DataFrame:
    files = sorted(folder.glob("*.csv"))
    if len(files) < 2:
        raise SystemExit("Need at least two filled rating files in results/human/ratings/.")
    frames = []
    for file in files:
        frame = pd.read_csv(file)
        missing = set(CRITERIA) - set(frame.columns)
        if missing:
            raise SystemExit(f"{file.name}: missing column(s) {', '.join(sorted(missing))}.")
        _check_scores(frame, file.name)
        frame = frame[["sample_id", *CRITERIA]]
        frame["sample_id"] = frame.sample_id.str.strip().str.lower()
        frame["rater"] = file.stem
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def load_questions(folder: Path = HUMAN / "ratings") -> pd.DataFrame:
    """The questions each rater saw, as recorded in the rating sheets themselves."""
    frames = []
    for file in sorted(folder.glob("*.csv")):
        frame = pd.read_csv(file)
        if "pergunta" not in frame.columns:
            raise SystemExit(f"{file.name}: missing the pergunta column.")
        frames.append(frame[["sample_id", "pergunta"]].assign(sample_id=frame.sample_id.str.strip().str.lower()))
    questions = pd.concat(frames, ignore_index=True).drop_duplicates()
    if questions.sample_id.duplicated().any():
        raise SystemExit("The rating sheets do not agree on which question each sample_id holds.")
    return questions.set_index("sample_id")


def questions_match(questions: pd.DataFrame, sample: pd.DataFrame) -> bool:
    """True when the rated answers are exactly the official sample, question by question."""
    official = sample.set_index("sample_id").rename(columns={"pergunta": "official"})
    rated = questions.join(official, how="inner")
    same_ids = len(rated) == len(questions) == len(sample)
    if not same_ids:
        return False
    normalize = lambda series: series.str.normalize("NFKC").str.replace(r"\s+", " ", regex=True)
    return (normalize(rated.pergunta) == normalize(rated.official)).all()


def alpha(ratings: pd.DataFrame, criterion: str) -> float:
    matrix = ratings.pivot(index="rater", columns="sample_id", values=criterion).astype(float)
    return float(krippendorff.alpha(reliability_data=matrix.to_numpy(), level_of_measurement="ordinal"))


def human_table(ratings: pd.DataFrame) -> pd.DataFrame:
    rows = {
        name: {"mean_1_to_5": ratings[column].mean(), "krippendorff_alpha": alpha(ratings, column)}
        for column, name in CRITERIA.items()
    }
    return pd.DataFrame(rows).T.rename_axis("criterion")


def judge_agreement(ratings: pd.DataFrame, key: pd.DataFrame, runs: pd.DataFrame) -> pd.DataFrame:
    """Spearman correlation between the judge's 0-2 correctness and the mean human 1-5 correctness."""
    human = ratings.groupby("sample_id")["correcao_1a5"].mean().rename("human")
    judged = key.merge(runs[["run_id", "question_id", "correctness"]], on=["run_id", "question_id"])
    merged = judged.set_index("sample_id").join(human, how="inner")
    rho = merged["correctness"].rank().corr(merged["human"].rank())
    return pd.DataFrame({"samples": [len(merged)], "spearman_judge_vs_human": [rho]}, index=pd.Index(["correctness"], name="criterion"))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--human", type=Path, default=HUMAN)
    parser.add_argument("--runs", type=Path, default=None)
    args = parser.parse_args()
    human = args.human
    ratings = load_ratings(human / "ratings")
    sample = pd.read_csv(human / "sample.csv") if (human / "sample.csv").is_file() else None
    body = [
        "# Human evaluation",
        "",
        f"Raters: {ratings.rater.nunique()}; answers: {ratings.sample_id.nunique()}.",
        "",
        "## Scores and inter-rater agreement",
        "",
        markdown(human_table(ratings)),
    ]
    if sample is not None and questions_match(load_questions(human / "ratings"), sample):
        key = pd.read_csv(human / "key.csv")
        runs = load_runs(args.runs) if args.runs else load_runs()
        body += ["", "## Judge versus humans", "", markdown(judge_agreement(ratings, key, runs))]
    else:
        body += [
            "",
            "Judge versus humans: not applicable. The rated answers are not the official",
            "sample in results/human/sample.csv, so their judge scores cannot be compared.",
        ]
    report = "\n".join(body) + "\n"
    (human / "agreement.md").write_text(report)
    print(f"written {human / 'agreement.md'}")


if __name__ == "__main__":
    main()
