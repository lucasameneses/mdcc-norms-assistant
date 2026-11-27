from assistant.corpus import CORPUS, clean_text, load_pages, load_sources


def test_every_listed_document_exists():
    for source in load_sources():
        assert (CORPUS / source.file).is_file(), source.file


def test_every_page_has_extractable_text():
    empty = [(page.source.doc_id, page.number) for page in load_pages() if len(page.text) < 50]
    assert empty == [], f"pages without text (scanned PDF?): {empty}"


def test_clean_text_removes_bidi_marks_and_blank_lines():
    assert clean_text("‭NORMA‬  Nº 01\n\n  \nArt. 1") == "NORMA Nº 01\nArt. 1"


def test_bidi_marks_between_words_become_spaces():
    assert clean_text("\u202dO\u202c\u202dColegiado\u202c\u202ddo\u202c MDCC") == "O Colegiado do MDCC"
