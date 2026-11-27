import json

import pytest

from assistant.log import append_record


def test_record_is_appended_with_a_timestamp(tmp_path):
    path = tmp_path / "answers.jsonl"
    append_record(path, {"model": "m", "question": "q", "answer": "a"})
    record = json.loads(path.read_text())
    assert record["model"] == "m" and "ts" in record


@pytest.mark.parametrize("field", ["name", "email", "matricula", "user_id"])
def test_identifying_fields_are_refused(tmp_path, field):
    with pytest.raises(ValueError, match=field):
        append_record(tmp_path / "answers.jsonl", {"question": "q", field: "x"})
