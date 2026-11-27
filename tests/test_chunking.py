from assistant.chunking import split_document
from assistant.corpus import Page, Source, load_pages

SOURCE = Source("doc", "Regimento", "doc.pdf", "https://example.org/doc.pdf", "2016")


def pages(*texts):
    return [Page(SOURCE, number, text) for number, text in enumerate(texts, start=1)]


def test_each_article_becomes_a_chunk_with_its_label_and_page():
    chunks = split_document(pages(
        "REGIMENTO\nArt. 1º O programa tem por finalidade formar mestres e doutores em computação.",
        "Art. 2º O prazo máximo para a defesa é de 24 meses.\n§ 1º O prazo pode ser prorrogado por 6 meses.",
    ))
    labels = [(chunk.metadata["article"], chunk.metadata["page"]) for chunk in chunks]
    assert labels == [(None, 1), ("Art. 1", 1), ("Art. 2", 2)]
    assert "§ 1º O prazo pode ser prorrogado" in chunks[2].page_content


def test_chunk_text_starts_with_the_citation():
    chunk = split_document(pages("Art. 5o A matrícula é semestral e obrigatória para todos os alunos regulares."))[0]
    assert chunk.page_content.startswith("Regimento, Art. 5 (2016)\n")
    assert chunk.metadata["url"] == "https://example.org/doc.pdf"


def test_annex_articles_are_labelled_apart():
    chunks = split_document(pages(
        "Art. 1o Aprova as normas gerais na forma do Anexo, parte integrante desta resolução.",
        "NORMAS GERAIS\nArt. 1o Os programas de pós-graduação stricto sensu têm por objetivo a formação.",
    ))
    assert [chunk.metadata["article"] for chunk in chunks] == ["Art. 1", "Anexo, Art. 1"]


def test_numbered_items_are_units_and_headings_join_the_next_item():
    chunks = split_document(pages(
        "1.Conceitos e Definições\n1.1. O PROAP se destina a proporcionar melhores condições para a formação de recursos humanos.\n"
        "1.2. Os recursos são concedidos conforme a disponibilidade orçamentária do programa a cada ano."
    ))
    assert [chunk.metadata["article"] for chunk in chunks] == ["item 1.1", "item 1.2"]
    assert "Conceitos e Definições" in chunks[0].page_content


def test_long_article_is_cut_and_keeps_its_label():
    long_text = "Art. 9º " + " ".join(["O aluno deve cumprir os créditos exigidos."] * 80)
    chunks = split_document(pages(long_text), max_chars=500, overlap=50)
    assert len(chunks) > 1
    assert {chunk.metadata["article"] for chunk in chunks} == {"Art. 9"}


def test_real_norms_yield_labelled_chunks():
    regimento = [page for page in load_pages() if page.source.doc_id == "regimento-interno"]
    labels = {chunk.metadata["article"] for chunk in split_document(regimento)}
    assert {"Art. 1", "Art. 20"} <= labels


def test_a_reference_to_an_article_at_the_start_of_a_line_is_not_a_new_unit():
    chunks = split_document(pages(
        "Art. 40. Para obter o diploma o aluno deve cumprir os requisitos do\nArt. 5o destas Normas;\nII - ter depositado a dissertação."
    ))
    assert [chunk.metadata["article"] for chunk in chunks] == ["Art. 40"]


def test_fixed_strategy_cuts_by_size_without_article_labels():
    from assistant.chunking import split_corpus

    text = "Art. 1º " + " ".join(["O aluno deve cumprir os créditos exigidos."] * 60)
    chunks = split_corpus(pages(text), strategy="fixed-500")
    assert len(chunks) > 1
    assert {chunk.metadata["article"] for chunk in chunks} == {None}
    assert all(len(chunk.page_content.split("\n", 1)[1]) <= 500 for chunk in chunks)
