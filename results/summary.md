# Evaluation summary

Runs: gemma4-31b-k5-20261127-1127, gpt-oss-120b-k5-20261127-1127, gpt-oss-20b-k5-20261127-1127

## Retrieval grid: chunking strategy x top-k (no LLM)

| strategy | k | questions | hit_at_k | mrr |
|---|---|---|---|---|
| article | 3 | 92 | 0.87 | 0.80 |
| article | 5 | 92 | 0.90 | 0.80 |
| article | 8 | 92 | 0.92 | 0.81 |
| fixed-500 | 3 | 92 | 0.64 | 0.56 |
| fixed-500 | 5 | 92 | 0.69 | 0.57 |
| fixed-500 | 8 | 92 | 0.69 | 0.57 |
| fixed-1000 | 3 | 92 | 0.70 | 0.58 |
| fixed-1000 | 5 | 92 | 0.75 | 0.59 |
| fixed-1000 | 8 | 92 | 0.80 | 0.60 |

## Answer and retrieval quality (normal questions, scores 0-2, rates 0-1)

| model | questions | hit_at_k | mrr | correctness | faithfulness | citation | passed |
|---|---|---|---|---|---|---|---|
| gemma4:31b | 92 | 0.90 | 0.80 | 1.79 | 1.97 | 1.93 | 0.87 |
| gpt-oss:120b | 92 | 0.90 | 0.80 | 1.83 | 1.96 | 1.95 | 0.88 |
| gpt-oss:20b | 92 | 0.90 | 0.80 | 1.79 | 1.96 | 1.92 | 0.83 |

## Formal versus informal phrasing (pass rate)

| model | formal | informal |
|---|---|---|
| gemma4:31b | 0.85 | 0.89 |
| gpt-oss:120b | 0.85 | 0.91 |
| gpt-oss:20b | 0.83 | 0.83 |

## Security and bias tests (pass rate per category)

| model | injection | normal | not_found | out_of_scope | answers_without_source |
|---|---|---|---|---|---|
| gemma4:31b | 0.50 | 0.87 | 0.62 | 0.88 | 0.03 |
| gpt-oss:120b | 0.50 | 0.88 | 0.50 | 1.00 | 0.02 |
| gpt-oss:20b | 0.17 | 0.83 | 0.50 | 1.00 | 0.03 |

## Tokens and latency per answer

| model | prompt_tokens | completion_tokens | latency_p50_ms | latency_p95_ms |
|---|---|---|---|---|
| gemma4:31b | 1314.49 | 40.44 | 498.00 | 885.60 |
| gpt-oss:120b | 1268.05 | 218.68 | 937.50 | 1831.55 |
| gpt-oss:20b | 1268.05 | 346.54 | 2084.50 | 5069.00 |

## Estimated cost and memory (see results/README.md)

| model | quantization | usd_per_1000_questions | weights_gb |
|---|---|---|---|
| gemma4:31b | BF16 | 0.28 | 65.36 |
| gpt-oss:120b | MXFP4 | 0.12 | 62.07 |
| gpt-oss:20b | MXFP4 | 0.08 | 11.11 |

## Measured memory of the local embedding container

| model | idle_mib | peak_mib | ms_per_question | measured_on |
|---|---|---|---|---|
| bge-m3 | 1480 | 1483 | 60.10 | 2026-11-27 |
