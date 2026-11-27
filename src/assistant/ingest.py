"""Index the corpus in pgvector: one collection per chunking strategy, plus the poisoned one.

Usage: python -m assistant.ingest [--only article fixed-500 fixed-1000 poisoned]
"""

import argparse

from langchain_core.documents import Document

from assistant.chunking import STRATEGIES, split_corpus
from assistant.corpus import CORPUS, load_pages
from assistant.settings import Settings, load_settings

POISONED_COLLECTION = "mdcc-poisoned"
TARGETS = [*STRATEGIES, "poisoned"]


def collection_for(strategy: str) -> str:
    return f"mdcc-{strategy}"


def vector_store(settings: Settings, collection: str, recreate: bool = False):
    from langchain_ollama import OllamaEmbeddings
    from langchain_postgres import PGVector

    return PGVector(
        embeddings=OllamaEmbeddings(model=settings.embed_model, base_url=settings.embed_url),
        collection_name=collection,
        connection=settings.database_url,
        pre_delete_collection=recreate,
        use_jsonb=True,
    )


def index(settings: Settings, collection: str, chunks: list[Document]) -> None:
    vector_store(settings, collection, recreate=True).add_documents(chunks)
    print(f"{len(chunks)} chunks indexed in '{collection}'")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="+", choices=TARGETS, default=TARGETS)
    targets = parser.parse_args().only
    settings = load_settings()
    pages = load_pages()
    for strategy in STRATEGIES:
        if strategy in targets:
            index(settings, collection_for(strategy), split_corpus(pages, strategy))
    if "poisoned" in targets:
        poisoned = split_corpus(load_pages(CORPUS / "poisoned"))
        index(settings, POISONED_COLLECTION, split_corpus(pages) + poisoned)


if __name__ == "__main__":
    main()
