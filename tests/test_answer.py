from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from assistant.answer import answer_question

CHUNKS = [
    Document("Regimento, Art. 30 (2016)\nA qualificação ocorre em até 18 meses.",
             metadata={"doc_id": "regimento-interno", "title": "Regimento", "article": "Art. 30", "doc_date": "2016", "url": "u", "page": 9}),
    Document("Regimento, Art. 31 (2016)\nA banca tem três membros.",
             metadata={"doc_id": "regimento-interno", "title": "Regimento", "article": "Art. 31", "doc_date": "2016", "url": "u", "page": 9}),
]


class FakeChat:
    def __init__(self, reply: str):
        self.reply, self.messages = reply, None

    def invoke(self, messages):
        self.messages = messages
        return AIMessage(content=self.reply, usage_metadata={"input_tokens": 100, "output_tokens": 20, "total_tokens": 120})


def test_citations_come_from_the_metadata_of_the_cited_chunks():
    answer = answer_question("Prazo da qualificação?", lambda q: CHUNKS, FakeChat("Até 18 meses [1]."))
    assert [(c["n"], c["article"]) for c in answer.citations] == [(1, "Art. 30")]
    assert len(answer.retrieved) == 2 and answer.prompt_tokens == 100 and answer.completion_tokens == 20


def test_citation_numbers_outside_the_context_are_ignored():
    answer = answer_question("Prazo?", lambda q: CHUNKS, FakeChat("Até 18 meses [7]."))
    assert answer.citations == []


def test_question_is_masked_before_the_model_sees_it():
    chat = FakeChat("ok")
    answer = answer_question("Minha matrícula é 512345, qual o prazo?", lambda q: CHUNKS, chat)
    assert "512345" not in chat.messages[-1][1] and "512345" not in answer.question


def test_full_width_brackets_count_as_citations():
    answer = answer_question("Prazo?", lambda q: CHUNKS, FakeChat("Até 18 meses【1】【2】"))
    assert [c["n"] for c in answer.citations] == [1, 2]
