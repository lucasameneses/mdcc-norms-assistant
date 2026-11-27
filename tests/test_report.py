import json

from eval.human_sample import draw_sample
from eval.report import build_summary, load_runs


def record(model, qid, category="normal", style="formal", passed=True, pair=None, latency=1000):
    return {
        "run_id": f"{model}-run", "question_id": qid, "model": model, "category": category, "style": style,
        "pair_id": pair, "question": "q", "answer": "a [1]", "citations": [{"n": 1, "title": "T", "article": "Art. 1"}],
        "hit": True, "reciprocal_rank": 1.0, "correctness": 2, "faithfulness": 2, "citation": 2, "passed": passed,
        "prompt_tokens": 900, "completion_tokens": 80, "latency_ms": latency,
    }


def write_run(path, records):
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n")


def test_summary_has_every_section_for_every_model(tmp_path):
    for model in ("small", "large"):
        write_run(tmp_path / f"{model}.jsonl", [
            record(model, "a", pair="p"), record(model, "b", style="informal", passed=False, pair="p"),
            record(model, "c", category="injection"), record(model, "d", category="out_of_scope"),
            record(model, "e", latency=3000),
        ])
    summary = build_summary(load_runs(tmp_path))
    for title in ("quality", "Formal versus informal", "Security", "latency"):
        assert title in summary
    assert "| large |" in summary and "| small |" in summary


def test_human_sample_takes_only_normal_answers(tmp_path):
    write_run(tmp_path / "m.jsonl", [record("m", f"q{n}") for n in range(30)] + [record("m", "x", category="out_of_scope")])
    sample = draw_sample(load_runs(tmp_path), size=20)
    assert len(sample) == 20 and set(sample.category) == {"normal"}
    assert sample.sample_id.iloc[0] == "s01"
