"""Append answer records to a JSONL file. Records never carry who asked (BR5)."""

import json
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_FIELDS = {
    "ts", "run_id", "question_id", "model", "collection", "top_k", "question", "answer",
    "citations", "retrieved", "prompt_tokens", "completion_tokens", "latency_ms",
    "category", "style", "pair_id", "hit", "reciprocal_rank", "correctness", "faithfulness",
    "citation", "passed", "judge_reason",
}


def append_record(path: Path, record: dict) -> None:
    unknown = set(record) - ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"fields not allowed in a log record: {sorted(unknown)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), **record}
    with path.open("a") as log:
        log.write(json.dumps(line, ensure_ascii=False) + "\n")
