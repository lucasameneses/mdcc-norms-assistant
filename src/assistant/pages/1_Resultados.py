"""Progress page: the latest evaluation summary and every scored answer."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from assistant.ui import apply_style, sidebar_brand, sidebar_footer, topbar

RESULTS = Path(__file__).resolve().parents[3] / "results"

st.set_page_config(page_title="MDCC.rag · Resultados", page_icon="📊", layout="wide")
apply_style()
sidebar_brand()
sidebar_footer()
topbar("Resultados & Avaliação", "Preliminar", "Rodadas com as perguntas de exemplo; o conjunto completo ainda está sendo escrito")

summary = RESULTS / "summary.md"
if not summary.is_file():
    st.info("Nenhuma avaliação rodou ainda.")
    st.stop()
st.markdown(summary.read_text().split("\n", 1)[1])

records = [json.loads(line) for file in sorted((RESULTS / "runs").glob("*.jsonl")) for line in file.read_text().splitlines() if line]
answers = pd.DataFrame(records)
st.subheader("Respostas avaliadas")
model = st.selectbox("Modelo", sorted(answers.model.unique()))
columns = ["question_id", "category", "passed", "question", "answer", "judge_reason"]
st.dataframe(answers[answers.model == model][[c for c in columns if c in answers]], hide_index=True, width="stretch")
