import json
import re
from collections import Counter
from pathlib import Path

import pytest

from assistant.corpus import load_pages, load_sources

QUESTIONS = Path(__file__).resolve().parents[1] / "eval" / "questions.jsonl"
CATEGORIES = {"normal", "not_found", "out_of_scope", "injection"}
NEEDS_EVIDENCE = {"normal", "injection"}


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_questions() -> list[dict]:
    return [json.loads(line) for line in QUESTIONS.read_text().splitlines() if line.strip()]


QUESTION_LIST = load_questions()


@pytest.fixture(scope="module")
def corpus_text() -> dict[str, str]:
    texts: dict[str, list[str]] = {}
    for page in load_pages():
        texts.setdefault(page.source.doc_id, []).append(page.text)
    return {doc_id: flat("\n".join(pages)) for doc_id, pages in texts.items()}


def test_ids_are_unique():
    duplicated = [key for key, count in Counter(q["id"] for q in QUESTION_LIST).items() if count > 1]
    assert duplicated == []


@pytest.mark.parametrize("question", QUESTION_LIST, ids=lambda q: q["id"])
def test_question_has_a_valid_shape(question):
    assert question["question"].strip()
    assert question["category"] in CATEGORIES
    assert question["style"] in {"formal", "informal"}
    if question["category"] in NEEDS_EVIDENCE:
        assert question.get("reference_answer", "").strip()
        assert question.get("doc_id") in {source.doc_id for source in load_sources()}


@pytest.mark.parametrize("question", [q for q in QUESTION_LIST if q["category"] in NEEDS_EVIDENCE], ids=lambda q: q["id"])
def test_evidence_is_copied_verbatim_from_the_document(question, corpus_text):
    assert flat(question["evidence"]) in corpus_text[question["doc_id"]], "evidence not found in the document"


def test_pairs_have_one_formal_and_one_informal_question():
    pairs: dict[str, list[str]] = {}
    for question in QUESTION_LIST:
        if "pair_id" in question:
            pairs.setdefault(question["pair_id"], []).append(question["style"])
    assert all(sorted(styles) == ["formal", "informal"] for styles in pairs.values())
