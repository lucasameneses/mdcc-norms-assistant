# Results

- `runs/` — one JSONL file per evaluation run (`python -m eval.run`).
- `summary.md` — tables built from every run (`python -m eval.report`).
- `retrieval.csv` — chunking strategy x top-k grid, no LLM (`python -m eval.retrieval`).
- `reference_models.csv` — inputs of the cost and memory estimates. Parameters and quantization
  come from Ollama Cloud `/api/show`; prices are OpenRouter's public per-token prices for the same
  open models (`/api/v1/models`), collected on the date in the file. `bits_per_weight` is 4.25 for
  MXFP4 (4-bit values plus one 8-bit scale per 32 weights) and 16 for BF16. Memory estimates count
  weights only; with prompts of about 2,000 tokens the attention cache is small next to them.
- `embedding_memory.csv` — measured RAM of the local embedding container (`python -m eval.embedding_memory`).
- `human/` — sample for the raters, the key, filled ratings and `agreement.md`.
