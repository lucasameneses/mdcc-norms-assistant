# Evaluation summary

Runs: gpt-oss-120b-k5-20261126-2349, gpt-oss-20b-k5-20261126-2349

## Answer and retrieval quality (normal questions, scores 0-2, rates 0-1)

| model | questions | hit_at_k | mrr | correctness | faithfulness | citation | passed |
|---|---|---|---|---|---|---|---|
| gpt-oss:120b | 4 | 1.00 | 0.69 | 1.50 | 2.00 | 2.00 | 0.50 |
| gpt-oss:20b | 4 | 1.00 | 0.69 | 1.50 | 2.00 | 2.00 | 0.50 |

## Formal versus informal phrasing (pass rate)

| model | formal | informal |
|---|---|---|
| gpt-oss:120b | 0.00 | 0.00 |
| gpt-oss:20b | 0.00 | 0.00 |

## Security and bias tests (pass rate per category)

| model | injection | normal | not_found | out_of_scope | answers_without_source |
|---|---|---|---|---|---|
| gpt-oss:120b | 0.00 | 0.50 | 0.00 | 1.00 | 0.00 |
| gpt-oss:20b | 0.00 | 0.50 | 0.00 | 1.00 | 0.00 |

## Tokens and latency per answer

| model | prompt_tokens | completion_tokens | latency_p50_ms | latency_p95_ms |
|---|---|---|---|---|
| gpt-oss:120b | 1811.29 | 197.29 | 841.00 | 1362.90 |
| gpt-oss:20b | 1811.29 | 268.57 | 1858.00 | 3563.40 |
