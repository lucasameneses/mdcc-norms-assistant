# 0006 — Streamlit for the chat

- **Status**: accepted
- **Context**: The colleagues need a demo chat for the presentation; no accounts (D4).
- **Decision**: Streamlit chat page with a model selector and the citations under each answer.
- **Alternatives**: Gradio (similar, less control over the citation layout); FastAPI plus HTML
  (more code for no gain).
- **Consequences**: A few dozen lines of Python, started by `./run.sh` on localhost.
