# mdcc-norms-assistant

A retrieval-augmented assistant that answers graduate students' questions about the MDCC/UFC
program rules in Portuguese, citing document, article and date, plus the evaluation harness behind
its model choice. Final project of the course *Modelos de Linguagem de Grande Escala* (MDCC/UFC).

- **Corpus**: 5 official PDFs and 6 procedure pages, split by article into 189 chunks.
- **Retrieval**: `bge-m3` embeddings (local Ollama) in PostgreSQL + pgvector, top 5.
- **Generation**: `gpt-oss:20b`, `gpt-oss:120b` and `gemma4:31b` on Ollama Cloud.
- **Evaluation**: retrieval hit@k and MRR, an LLM judge (`glm-5.3`), rule checks for refusals and
  prompt injection, cost, latency and memory estimates, and a blind human-rating sample.

## Results (114 questions)

| | gpt-oss:20b | gpt-oss:120b | gemma4:31b |
|---|---|---|---|
| Answers approved by the judge | 0.83 | 0.88 | 0.87 |
| Injection resisted | 0.17 | 0.50 | 0.50 |
| Out-of-scope refused | 1.00 | 1.00 | 0.88 |
| Latency p50 / p95 (s) | 2.08 / 5.07 | 0.94 / 1.83 | 0.50 / 0.89 |
| Cost per 1000 questions (US$) | 0.08 | 0.12 | 0.28 |

Article-based chunking reached hit@5 of 0.90, against 0.75 for fixed 1000-character chunks.
Full tables: [results/summary.md](results/summary.md). Human evaluation is still pending.

## Run

```bash
cp .env.example .env   # fill OLLAMA_API_KEY
./run.sh               # starts postgres + ollama, indexes once, opens the chat on 127.0.0.1
```

Evaluation scripts (`python -m eval.<name>`): `retrieval`, `run`, `report`, `human_sample`,
`agreement`, `embedding_memory`. See [eval/README.md](eval/README.md).

## Documents

- Architecture and ADRs: [docs/architecture.md](docs/architecture.md)
- Report and slides (LaTeX and PDF, in Portuguese): [latex/](latex/)
