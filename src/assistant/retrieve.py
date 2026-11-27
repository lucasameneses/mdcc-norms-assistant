"""Top-k similarity search in one pgvector collection."""

from langchain_core.documents import Document

from assistant.ingest import vector_store
from assistant.settings import Settings


def retriever(settings: Settings, collection: str, k: int):
    store = vector_store(settings, collection)

    def chunks_for(question: str) -> list[Document]:
        """Chunks ordered by similarity; `similarity` is 1 minus the cosine distance."""
        chunks = []
        for chunk, distance in store.similarity_search_with_score(question, k=k):
            chunk.metadata["similarity"] = round(1 - distance, 3)
            chunks.append(chunk)
        return chunks

    return chunks_for
