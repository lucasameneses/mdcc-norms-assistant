"""Split the norms into chunks that follow their structure, so each answer can cite the article.

A unit starts at an article (`Art. 12`) or at a numbered item (`3.2.`), whichever the document
uses. When the article numbering restarts, the rest is an annex (as in a resolution that
approves norms "na forma do Anexo"), so its units are labelled `Anexo, Art. N`. Text before
the first unit and documents with no numbering become units without a label. Units longer than
`max_chars` are cut by size and keep their label.
"""

import re
from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from assistant.corpus import Page, Source

ARTICLE = re.compile(r"^Art\.?\s*(\d+)\s*[oº°]?\.?\s+(?=[A-ZÀ-Ú])")
ITEM = re.compile(r"^(\d+(?:\.\d+)*)\.(?=\s|$|[A-ZÀ-Ú])")
MIN_UNIT_CHARS = 80


@dataclass
class Unit:
    label: str | None
    page: int
    lines: list[str]

    @property
    def text(self) -> str:
        return "\n".join(self.lines)


def split_units(pages: list[Page]) -> list[Unit]:
    units = [Unit(None, pages[0].number, [])]
    last_article, in_annex = 0, False
    for page in pages:
        for line in page.text.splitlines():
            label = None
            if article := ARTICLE.match(line):
                number = int(article.group(1))
                in_annex = in_annex or number <= last_article
                last_article = number
                label = f"{'Anexo, ' if in_annex else ''}Art. {number}"
            elif item := ITEM.match(line):
                label = f"item {item.group(1)}"
            if label:
                units.append(Unit(label, page.number, [line]))
            else:
                units[-1].lines.append(line)
    return merge_short_units([unit for unit in units if unit.lines])


def merge_short_units(units: list[Unit]) -> list[Unit]:
    """Join a heading-only unit (like `1. Conceitos e Definições`) to the unit that follows it."""
    merged: list[Unit] = []
    carry: Unit | None = None
    for unit in units:
        if carry:
            unit = Unit(unit.label, carry.page, carry.lines + unit.lines)
            carry = None
        if unit.label and unit.label.startswith("item") and len(unit.text) < MIN_UNIT_CHARS:
            carry = unit
        else:
            merged.append(unit)
    if carry:
        merged.append(carry)
    return merged


def citation(source: Source, label: str | None) -> str:
    return f"{source.title}{', ' + label if label else ''} ({source.doc_date})"


def split_document(pages: list[Page], max_chars: int = 1500, overlap: int = 150) -> list[Document]:
    source = pages[0].source
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_chars, chunk_overlap=overlap)
    chunks = []
    for unit in split_units(pages):
        metadata = {
            "doc_id": source.doc_id,
            "title": source.title,
            "url": source.url,
            "doc_date": source.doc_date,
            "article": unit.label,
            "page": unit.page,
        }
        for piece in splitter.split_text(unit.text):
            content = f"{citation(source, unit.label)}\n{piece}"
            chunks.append(Document(page_content=content, metadata=metadata))
    return chunks


def split_corpus(pages: list[Page]) -> list[Document]:
    by_document: dict[str, list[Page]] = {}
    for page in pages:
        by_document.setdefault(page.source.doc_id, []).append(page)
    return [chunk for document in by_document.values() for chunk in split_document(document)]
