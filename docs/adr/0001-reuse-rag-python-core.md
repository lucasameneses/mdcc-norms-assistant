# 0001 — Reuse the rag-python-langfuse core, change only what the domain needs

- **Status**: accepted
- **Context**: Six days to deliver, one developer. `~/dev/rag-python-langfuse` already loads a
  corpus, splits it with `langchain-text-splitters`, embeds with Ollama and stores in pgvector
  through `langchain-postgres`.
- **Decision**: Python 3.12, `langchain-core`, `langchain-text-splitters`, `langchain-ollama`,
  `langchain-postgres` and pgvector, copied and adapted into an independent repository. No agents
  or chains beyond retrieve-then-generate.
- **Alternatives**: Chroma embedded (no database container, but the ingestion would be rewritten
  for no gain at this corpus size); LlamaIndex (another framework to learn inside the deadline);
  no framework (more glue code for embeddings and the vector store).
- **Consequences**: Fast start and a known stack. The repository depends on LangChain's
  release pace; only the stable core packages are used.
