"""Read the official documents listed in corpus/sources.csv as text, page by page."""

import csv
import re
from dataclasses import dataclass
from pathlib import Path

import pymupdf

CORPUS = Path(__file__).resolve().parents[2] / "corpus"
INVISIBLE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060\ufeff]")
WORD_BOUNDARY_MARKS = re.compile(r"\u202c\u202d")


@dataclass(frozen=True)
class Source:
    doc_id: str
    title: str
    file: str
    url: str
    doc_date: str


@dataclass(frozen=True)
class Page:
    source: Source
    number: int
    text: str


def load_sources(corpus: Path = CORPUS) -> list[Source]:
    with open(corpus / "sources.csv", newline="") as sources:
        return [Source(**row) for row in csv.DictReader(sources)]


def clean_text(text: str) -> str:
    text = INVISIBLE.sub("", WORD_BOUNDARY_MARKS.sub(" ", text))
    lines = (re.sub(r"[ \t\xa0]+", " ", line).strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def read_pages(source: Source, corpus: Path = CORPUS) -> list[Page]:
    path = corpus / source.file
    if path.suffix == ".pdf":
        with pymupdf.open(path) as document:
            texts = [page.get_text() for page in document]
    else:
        texts = [path.read_text()]
    return [Page(source, number, clean_text(text)) for number, text in enumerate(texts, start=1)]


def load_pages(corpus: Path = CORPUS) -> list[Page]:
    return [page for source in load_sources(corpus) for page in read_pages(source, corpus)]
