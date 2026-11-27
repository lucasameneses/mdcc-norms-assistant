# Evaluation summary

Runs: gemma4-31b-k5-20261127-1025, gpt-oss-120b-k5-20261127-1027, gpt-oss-20b-k5-20261127-1026

## Retrieval grid: chunking strategy x top-k (no LLM)

| strategy | k | questions | hit_at_k | mrr |
|---|---|---|---|---|
| article | 3 | 4 | 0.75 | 0.62 |
| article | 5 | 4 | 1.00 | 0.69 |
| article | 8 | 4 | 1.00 | 0.69 |
| fixed-500 | 3 | 4 | 0.75 | 0.62 |
| fixed-500 | 5 | 4 | 1.00 | 0.68 |
| fixed-500 | 8 | 4 | 1.00 | 0.68 |
| fixed-1000 | 3 | 4 | 0.75 | 0.62 |
| fixed-1000 | 5 | 4 | 1.00 | 0.69 |
| fixed-1000 | 8 | 4 | 1.00 | 0.69 |

## Answer and retrieval quality (normal questions, scores 0-2, rates 0-1)

| model | questions | hit_at_k | mrr | correctness | faithfulness | citation | passed |
|---|---|---|---|---|---|---|---|
| gemma4:31b | 4 | 1.00 | 0.69 | 1.75 | 2.00 | 2.00 | 0.75 |
| gpt-oss:120b | 4 | 1.00 | 0.69 | 1.50 | 2.00 | 2.00 | 0.50 |
| gpt-oss:20b | 4 | 1.00 | 0.69 | 1.50 | 2.00 | 2.00 | 0.50 |

## Formal versus informal phrasing (pass rate)

| model | formal | informal |
|---|---|---|
| gemma4:31b | 0.00 | 1.00 |
| gpt-oss:120b | 0.00 | 0.00 |
| gpt-oss:20b | 0.00 | 0.00 |

## Security and bias tests (pass rate per category)

| model | injection | normal | not_found | out_of_scope | answers_without_source |
|---|---|---|---|---|---|
| gemma4:31b | 0.00 | 0.75 | 1.00 | 1.00 | 0.00 |
| gpt-oss:120b | 1.00 | 0.50 | 1.00 | 1.00 | 0.00 |
| gpt-oss:20b | 0.00 | 0.50 | 1.00 | 1.00 | 0.00 |

## Tokens and latency per answer

| model | prompt_tokens | completion_tokens | latency_p50_ms | latency_p95_ms |
|---|---|---|---|---|
| gemma4:31b | 1864.57 | 27.86 | 650.00 | 1344.20 |
| gpt-oss:120b | 1781.86 | 216.29 | 879.00 | 1736.20 |
| gpt-oss:20b | 1781.86 | 303.57 | 2654.00 | 3376.00 |

## Estimated cost and memory (see results/README.md)

| model | quantization | usd_per_1000_questions | weights_gb |
|---|---|---|---|
| gemma4:31b | BF16 | 0.38 | 65.36 |
| gpt-oss:120b | MXFP4 | 0.14 | 62.07 |
| gpt-oss:20b | MXFP4 | 0.09 | 11.11 |

## Measured memory of the local embedding container

| model | idle_mib | peak_mib | ms_per_question | measured_on |
|---|---|---|---|---|
| bge-m3 | 1480 | 1483 | 60.10 | 2026-11-27 |
