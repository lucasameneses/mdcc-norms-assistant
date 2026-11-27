import pandas as pd
import pytest

from eval.agreement import human_table, judge_agreement, load_questions, load_ratings, questions_match


def write_rater(folder, name, scores, sample_ids=None, questions=None):
    n = len(scores)
    frame = pd.DataFrame({
        "sample_id": sample_ids or [f"s{n:02d}" for n in range(1, n + 1)],
        "correcao_1a5": scores, "utilidade_1a5": scores, "clareza_1a5": scores,
    })
    if questions is not None:
        frame.insert(1, "pergunta", questions)
    frame.to_csv(folder / f"{name}.csv", index=False)


def test_identical_raters_agree_perfectly(tmp_path):
    write_rater(tmp_path, "ana", [1, 3, 5, 4, 2])
    write_rater(tmp_path, "bia", [1, 3, 5, 4, 2])
    table = human_table(load_ratings(tmp_path))
    assert table.loc["correctness", "krippendorff_alpha"] == pytest.approx(1.0)
    assert table.loc["correctness", "mean_1_to_5"] == pytest.approx(3.0)


def test_one_rater_is_not_enough(tmp_path):
    write_rater(tmp_path, "ana", [1, 2, 3])
    with pytest.raises(SystemExit, match="two"):
        load_ratings(tmp_path)


def test_sample_ids_are_normalized(tmp_path):
    write_rater(tmp_path, "ana", [1, 3], sample_ids=["S01", "S02"])
    write_rater(tmp_path, "bia", [1, 3], sample_ids=["s01", "s02"])
    ratings = load_ratings(tmp_path)
    assert set(ratings.sample_id) == {"s01", "s02"}


def test_scores_must_be_integers_from_1_to_5(tmp_path):
    write_rater(tmp_path, "ana", [1, 3, 3.5, 4, 2])
    write_rater(tmp_path, "bia", [1, 3, 5, 4, 2])
    with pytest.raises(SystemExit, match="integers"):
        load_ratings(tmp_path)


def test_raters_must_see_the_same_questions(tmp_path):
    write_rater(tmp_path, "ana", [1, 3], questions=["Qual o prazo?", "Quantos créditos?"])
    write_rater(tmp_path, "bia", [1, 3], questions=["Qual o prazo?", "Outra pergunta"])
    with pytest.raises(SystemExit, match="agree"):
        load_questions(tmp_path)


def test_questions_match_detects_a_different_sample(tmp_path):
    write_rater(tmp_path, "ana", [1, 3], questions=["Qual o prazo?", "Quantos créditos?"])
    write_rater(tmp_path, "bia", [1, 3], questions=["Qual o prazo?", "Quantos créditos?"])
    questions = load_questions(tmp_path)
    official = pd.DataFrame({
        "sample_id": ["s01", "s02"],
        "pergunta": ["Qual o prazo?", "Quantos créditos?"],
    })
    assert questions_match(questions, official)
    other = pd.DataFrame({"sample_id": ["s01", "s02"], "pergunta": ["Banca?", "Trancamento?"]})
    assert not questions_match(questions, other)


def test_judge_agreement_follows_the_key(tmp_path):
    write_rater(tmp_path, "ana", [1, 3, 5])
    write_rater(tmp_path, "bia", [1, 3, 5])
    key = pd.DataFrame({"sample_id": ["s01", "s02", "s03"], "run_id": ["r"] * 3, "question_id": ["a", "b", "c"]})
    runs = pd.DataFrame({"run_id": ["r"] * 3, "question_id": ["a", "b", "c"], "correctness": [0, 1, 2]})
    table = judge_agreement(load_ratings(tmp_path), key, runs)
    assert table.loc["correctness", "spearman_judge_vs_human"] == pytest.approx(1.0)
    assert table.loc["correctness", "samples"] == 3
