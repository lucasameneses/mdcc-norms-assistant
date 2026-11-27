# Architecture — MDCC norms assistant

A retrieval-augmented assistant that answers graduate students' questions about the MDCC/UFC
rules in Portuguese, citing document, article and date, plus the evaluation harness the LLM
course rubric asks for. Business rules and acceptance criteria: work item
`mdcc-norms-assistant` (`~/dev/pessoal/.agents/work/mdcc-norms-assistant.md`).

## Forces

- **Deadline**: course delivery on 2026-12-02; minimal results by 2026-11-29 (D14).
- **Team**: one developer; two colleagues run the chat and read results, not the pipeline.
- **Hardware**: development machine with no NVIDIA GPU, 15 GB RAM, 8 cores, so generation runs on
  Ollama Cloud; only embeddings run locally.
- **Corpus**: a few official PDFs in Portuguese, hundreds of chunks. No scale concern.
- **Rubric**: justified model choice, RAG strategy with variations, automatic and human
  evaluation, cost/memory/latency, bias/privacy/security. Every number in the report must come
  from a reproducible script.
- **Privacy**: no personal data stored (BR5); runs on localhost only, never exposed.
- **Reuse**: `~/dev/rag-python-langfuse` already has ingestion into pgvector with LangChain; copy
  and adapt, no shared code.

## Context and containers

```
 student ──► Streamlit chat (app) ──► retrieve (pgvector) ──► generate (Ollama Cloud)
                    │                        ▲                         │
                    ▼                        │ bge-m3 embeddings       ▼
              logs/*.jsonl ◄────────── answer + citations + usage ◄────┘

 eval scripts ──► questions.jsonl ──► retrieval grid ──► generation runs ──► judge ──► results/summary.md
                                                                     └──► human sample CSV ──► agreement
```

`docker compose up -d` starts two containers on localhost: `postgres` (pgvector) and `ollama`
(`bge-m3` embeddings only). The chat runs with `streamlit run`. Ollama Cloud is reached over HTTPS with
the key from `.env`.

## Modules (`src/assistant/`)

| Module | Responsibility |
|---|---|
| `settings.py` | Configuration from the environment, defaults for the compose lab |
| `corpus.py` | Read `corpus/sources.csv` and extract PDF text page by page (PyMuPDF) |
| `chunking.py` | Split a norm by article (`Art. N`), keep `§` and incisos inside it; cut long articles by size; strategies `fixed-500`, `fixed-1000`, `article` |
| `ingest.py` | Build one pgvector collection per chunking strategy |
| `retrieve.py` | Top-k search in a collection, returns chunks with metadata |
| `prompts.py` | System prompt in Portuguese enforcing BR1–BR4 and BR6 |
| `answer.py` | Retrieve, generate, parse citations, return answer + usage (tokens, latency) |
| `privacy.py` | Mask email, CPF and enrollment-like numbers before the model call and the log (BR5) |
| `log.py` | Append one JSON record per answer to `logs/answers.jsonl`; no user fields |
| `app.py` | Streamlit chat with citations and a model selector |

`eval/` holds the evaluation set and scripts; `results/` holds their committed outputs.

## Data model

pgvector collection per strategy (`mdcc-article`, `mdcc-fixed-500`, `mdcc-fixed-1000`) and a
separate `mdcc-poisoned` collection for the injection test. Chunk metadata:
`doc_id`, `title`, `url`, `doc_date`, `article` (e.g. `Art. 12`, or `null`), `page`.

`corpus/sources.csv`: `doc_id,title,file,url,doc_date`.

`eval/questions.jsonl`, one object per line:
`id, question, reference_answer, evidence, doc_id, category, style, pair_id`, where `category` is
`normal | not_found | out_of_scope | injection` and `style` is `formal | informal`. `evidence` is
mandatory for `normal` (BR7) and must occur verbatim in the extracted text.

Log record (`logs/answers.jsonl` and every run file): `ts, run_id, model, strategy, top_k,
question (masked), answer, citations, retrieved_ids, prompt_tokens, completion_tokens,
latency_ms, load_ms`. No name, email or enrollment field exists.

## Conventions

- Python 3.12, `src/` layout, `pytest`. Settings only from environment variables.
- Every script is runnable as `python -m eval.<name>` and writes to `results/`.
- Secrets only in `.env`; `.env.example` committed.

## Deployment

Local only. Ports bound to `127.0.0.1`. No public hosting (out of scope).

## ADRs

- [0001 — Reuse the rag-python-langfuse core, change only what the domain needs](adr/0001-reuse-rag-python-core.md)
- [0002 — Article-aware chunking and multilingual embeddings](adr/0002-article-chunking-bge-m3.md)
- [0003 — Three generators on Ollama Cloud, embeddings local](adr/0003-models-through-ollama.md)
- [0004 — JSONL logs instead of Langfuse](adr/0004-jsonl-logs.md)
- [0005 — Own evaluation metrics instead of RAGAS](adr/0005-own-evaluation-metrics.md)
- [0006 — Streamlit for the chat](adr/0006-streamlit-chat.md)
