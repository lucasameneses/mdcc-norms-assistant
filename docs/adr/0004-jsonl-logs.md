# 0004 — JSONL logs instead of Langfuse

- **Status**: accepted
- **Context**: Self-hosted Langfuse v3 needs Postgres, ClickHouse, Redis and object storage: too
  heavy for the colleagues' machines. Langfuse Cloud would send questions outside the machine.
  The report needs tables, not a trace UI. rag-python-langfuse already shows Langfuse.
- **Decision**: Every answer appends one JSON record to a file (`logs/answers.jsonl` for the
  chat, `results/runs/<run_id>.jsonl` for evaluation); pandas scripts aggregate them.
- **Alternatives**: Langfuse self-hosted; Langfuse Cloud; OpenTelemetry traces to Jaeger.
- **Consequences**: Data never leaves the machine (BR5), everything is reproducible from files.
  No visual trace explorer.
