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


def load_ratings(folder: Path = HUMAN / "ratings") -> pd.DataFrame:
    files = sorted(folder.glob("*.csv"))
    if len(files) < 2:
        raise SystemExit("Need at least two filled rating files in results/human/ratings/.")
    frames = []
    for file in files:
        frame = pd.read_csv(file)[["sample_id", *CRITERIA]]
        frame["rater"] = file.stem
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


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
    ratings = load_ratings()
    key = pd.read_csv(HUMAN / "key.csv")
    report = (
        "# Human evaluation\n\n"
        f"Raters: {ratings.rater.nunique()}; answers: {ratings.sample_id.nunique()}.\n\n"
        f"## Scores and inter-rater agreement\n\n{markdown(human_table(ratings))}\n\n"
        f"## Judge versus humans\n\n{markdown(judge_agreement(ratings, key, load_runs()))}\n"
    )
    (HUMAN / "agreement.md").write_text(report)
    print("written results/human/agreement.md")


if __name__ == "__main__":
    main()
