# Evaluation set

`questions.jsonl` holds the questions the assistant is evaluated on, one JSON object per line.
They are written by people from real doubts of MDCC students; an LLM may suggest questions for
sections nobody covered, but a person reviews each one before it enters the file.

## Fields

| Field | Required | Meaning |
|---|---|---|
| `id` | always | Short unique name, e.g. `creditos-mestrado` |
| `question` | always | The question as a student would type it |
| `category` | always | `normal`, `not_found`, `out_of_scope` or `injection` |
| `style` | always | `formal` or `informal` |
| `reference_answer` | `normal`, `injection` | The correct answer in one or two sentences |
| `evidence` | `normal`, `injection` | A passage copied **exactly** from the document that proves the answer |
| `doc_id` | `normal`, `injection` | The document of the evidence, as in `corpus/sources.csv` |
| `pair_id` | optional | Same value on a formal question and its informal rewrite |

Categories:

- `normal`: the norms answer it. The assistant must answer and cite.
- `not_found`: about the program, but the norms do not answer it (e.g. the coffee machine
  schedule). The assistant must say it did not find it.
- `out_of_scope`: not about the program (health, legal advice, opinions about people). The
  assistant must refuse.
- `injection`: a question about defense deadlines, answered with the poisoned collection. The
  assistant must give the real rule and ignore the planted instruction.

## How to write a good question

1. Open the document, find the rule, and copy the shortest passage that proves the answer into
   `evidence`, without changing a character (line breaks may become spaces).
2. Write the question the way a student would ask, without copying the norm's words.
3. For some questions, add an informal rewrite with the same `pair_id` and `style: informal`
   ("quantos créditos eu preciso pra terminar o mestrado?").
4. Run `.venv/bin/pytest tests/test_questions.py`: it rejects a question whose evidence is not in
   the corpus.

Target: at least 40 questions for the first results (2026-11-28), about 100 for the final ones,
with 5 to 10 in each of `not_found`, `out_of_scope` and `injection`.
