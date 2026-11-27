"""Index the corpus in pgvector: the clean collection and the poisoned one for the injection test.

Usage: python -m assistant.ingest
"""

from langchain_core.documents import Document

from assistant.chunking import split_corpus
from assistant.corpus import CORPUS, load_pages
from assistant.settings import Settings, load_settings

POISONED_COLLECTION = "mdcc-poisoned"


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
    settings = load_settings()
    chunks = split_corpus(load_pages())
    index(settings, settings.collection, chunks)
    index(settings, POISONED_COLLECTION, chunks + split_corpus(load_pages(CORPUS / "poisoned")))


if __name__ == "__main__":
    main()
