# Project context — mdcc-norms-assistant

## Stack

Python 3.12; LangChain core (`langchain-core`, `langchain-text-splitters`, `langchain-ollama`,
`langchain-postgres`); PostgreSQL 17 with pgvector; PyMuPDF; Streamlit; pandas; pytest. Models via
Ollama: local container for `bge-m3` embeddings only; Ollama Cloud for the three generators and
the judge. See `docs/architecture.md` and `docs/adr/`.

## Layout

```
corpus/            official PDFs, sources.csv, poisoned/ (injection test only)
src/assistant/     settings, corpus, chunking, ingest, retrieve, prompts, answer, privacy, log, app
eval/              questions.jsonl and evaluation scripts (python -m eval.<name>)
results/           committed evaluation outputs; runs/, judged/, human/
logs/              chat logs (git-ignored)
tests/             pytest
docs/              architecture.md, adr/
```

## Storage

pgvector collections `mdcc-article`, `mdcc-fixed-500`, `mdcc-fixed-1000`, `mdcc-poisoned`,
rebuilt by `python -m assistant.ingest` (no migrations; the index is derived data).

## Configuration and secrets

Environment variables only, documented in `.env.example`. `OLLAMA_API_KEY` lives in `.env`, which
is git-ignored. Lab credentials (postgres `rag/rag`) and ports are bound to `127.0.0.1` only.

## Errors

Scripts fail fast with a clear message (missing key, empty collection, question without
evidence). The chat shows a Portuguese message when a model call fails, never a stack trace.

## Privacy

No user identification anywhere. Questions are masked (`assistant.privacy`) before the model call and the log.

## Commands

```bash
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
docker compose up -d postgres ollama
docker compose exec ollama ollama pull bge-m3
.venv/bin/python -m assistant.ingest
.venv/bin/streamlit run src/assistant/app.py   # chat at http://localhost:8501
.venv/bin/python -m eval.retrieval
.venv/bin/python -m eval.generate --model <tag> --strategy article --k 5
.venv/bin/python -m eval.judge --run <run_id>
.venv/bin/python -m eval.report
```

Commands are the planned ones; `dev` confirms each as it is built.

## Style

Clean-code principles, small modules, English identifiers and documents; prompts and
user-facing text in Portuguese. One-line Conventional Commits.
