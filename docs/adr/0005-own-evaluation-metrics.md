# 0005 — Own evaluation metrics instead of RAGAS

- **Status**: accepted
- **Context**: Every normal question has a verbatim evidence excerpt (BR7). RAGAS prompts are in
  English, need a judge LLM anyway, and its API changes between versions: a deadline risk.
- **Decision**: Retrieval: hit@k and MRR, computed deterministically by checking whether the
  evidence excerpt is contained in a retrieved chunk. Answers: LLM-as-judge with a Portuguese
  rubric scoring correctness, faithfulness to the retrieved chunks and citation presence (0–2
  each), plus rule checks for `not_found`, `out_of_scope` and `injection` categories. Human
  agreement: Krippendorff's alpha (ordinal).
- **Alternatives**: RAGAS (cited in the report as the reference for the metric definitions);
  only human evaluation (too slow for 100 questions times 3 models).
- **Consequences**: Transparent, cheap, in Portuguese. The judge prompt must be validated against
  the human sample (judge versus human agreement is reported).
