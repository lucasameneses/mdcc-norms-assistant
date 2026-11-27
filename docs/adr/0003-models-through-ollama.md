# 0003 — Three generators on Ollama Cloud, embeddings local

- **Status**: accepted
- **Context**: The rubric asks for a justified model choice with cost, memory and latency. The
  user chose Ollama Cloud only for generation (key already available). The development machine
  has no NVIDIA GPU, so a local generator would take ~40 min per 100 answers. Ollama Cloud
  offers no embedding models.
- **Decision**: Three generators on Ollama Cloud behind one interface (`ChatOllama`):
  `gpt-oss:20b` (small), `gpt-oss:120b` (large, same family: isolates size) and one model of
  another family from the catalog (isolates family). The judge is a fourth cloud model, different
  from the three. Embeddings (`bge-m3`) stay on the local Ollama container. Exact tags are
  confirmed against the catalog in plan step 1.
- **Alternatives**: A local ~4B generator (measurable memory and full data locality, but too slow
  on CPU for the deadline); a commercial API (real per-token price, declined by the user).
- **Consequences**: Fast evaluation runs, light machines. Generator memory is estimated, not
  measured (parameters x bytes per weight at the served quantization + KV cache), stated as an
  estimate in the report; the embedding container's RAM is measured. Cost per 1000 questions is
  estimated from measured tokens times a public reference price for the same open model.
  Questions leave the machine, so they are masked before the call (T9) and the report discusses
  when local serving would be required.
