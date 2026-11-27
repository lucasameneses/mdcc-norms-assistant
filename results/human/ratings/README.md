# Human ratings

Filled sheets from three blind raters (the authors), received 2026-11-27.

Each file keeps the sheet exactly as sent: `sample_id` (S01-S20), the question, the answer
rated, the source shown by the assistant, the three integer scores from 1 to 5 and an
optional comment. Files are named `pessoa1`-`pessoa3` to keep the evaluation blind and the
raters unnamed; which file belongs to whom is not recorded.

Provenance: these ratings cover the 20 answers of the interface prototype (mockup), which
ran on a synthetic regulation document (`regulamento-sintetico.pdf`), not the official MDCC
corpus. They are therefore **not** the random sample of official answers described in
`../sample.csv` and `../key.csv`, and the judge-vs-human correlation computed from those
files does not apply here (see `../agreement.md`).
