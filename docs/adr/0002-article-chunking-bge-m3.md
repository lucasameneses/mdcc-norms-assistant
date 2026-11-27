# 0002 — Article-aware chunking and multilingual embeddings

- **Status**: accepted
- **Context**: BR1 requires citing the article. The corpus is legal-style Portuguese in PDF.
  `nomic-embed-text`, used in rag-python-langfuse, is trained mostly on English.
- **Decision**: Extract text with PyMuPDF; split by `Art. N` boundaries keeping its paragraphs
  and incisos together, cutting only articles longer than the size limit; store the article in
  the chunk metadata. Embed with `bge-m3` on local Ollama. Fixed-size strategies (500 and 1000
  characters) are kept for comparison.
- **Alternatives**: Markdown-header splitting (the PDFs have no headers); fixed-size only (cuts
  articles in half and loses the citation); `multilingual-e5` (needs a separate runtime, bge-m3
  runs in the Ollama container already there).
- **Consequences**: Citations come from metadata, not from the model's memory. A scanned PDF
  would need OCR (Tesseract); checked in the first plan step.
