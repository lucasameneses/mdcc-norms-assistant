from eval.retrieval import grid_rows


def test_grid_scores_each_k_from_the_same_ranking():
    ranked = [
        ("prazo de sete dias", ["outro", "outro", "outro", "o prazo de sete dias", "x", "x", "x", "x"]),
        ("trinta meses", ["vínculo de trinta meses", "x", "x", "x", "x", "x", "x", "x"]),
    ]
    rows = {row["k"]: row for row in grid_rows("article", ranked)}
    assert rows[3]["hit_at_k"] == 0.5 and rows[3]["mrr"] == 0.5
    assert rows[5]["hit_at_k"] == 1.0 and rows[5]["mrr"] == round((1 / 4 + 1) / 2, 3)
    assert rows[8]["questions"] == 2
