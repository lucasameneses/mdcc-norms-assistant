#!/usr/bin/env bash
# One command for the demo: start the lab, index the corpus once, open the chat.
set -euo pipefail
cd "$(dirname "$0")"

[ -f .env ] || { echo "Copy .env.example to .env and fill in OLLAMA_API_KEY."; exit 1; }
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install -q -e .; }

docker compose up -d --wait
docker compose exec -T ollama ollama pull bge-m3 >/dev/null

indexed=$(docker compose exec -T postgres psql -U rag -tAc \
  "select count(*) from langchain_pg_embedding e join langchain_pg_collection c on c.uuid = e.collection_id where c.name = 'mdcc-article'" 2>/dev/null || echo 0)
if [ "${indexed:-0}" -eq 0 ]; then
  echo "Indexing the corpus (first run only, a few minutes)..."
  .venv/bin/python -m assistant.ingest
fi

exec .venv/bin/streamlit run src/assistant/app.py --server.address 127.0.0.1
