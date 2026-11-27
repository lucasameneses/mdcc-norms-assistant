"""Streamlit chat over the MDCC norms, laid out as the HTML mockup: sidebar, chat, sources panel.

Usage: streamlit run src/assistant/app.py
"""

from html import escape
from pathlib import Path

import streamlit as st

from assistant.answer import Answer, answer_question, chat_model
from assistant.corpus import load_sources
from assistant.log import append_record
from assistant.retrieve import retriever
from assistant.settings import load_settings
from assistant.ui import apply_style, sidebar_brand, sidebar_footer, topbar

LOG = Path(__file__).resolve().parents[2] / "logs" / "answers.jsonl"
TOP_K = 5
TEMPERATURE = 0
SUGGESTIONS = [
    "Quantos créditos são exigidos no mestrado e no doutorado?",
    "Qual o tempo máximo de vínculo no mestrado?",
    "Como é composta a banca de defesa de doutorado?",
    "O estágio de docência é obrigatório?",
    "Quais exames de proficiência em inglês são aceitos?",
    "Até quando posso pedir aproveitamento de disciplinas?",
]


@st.cache_resource
def chunks_for():
    settings = load_settings()
    return retriever(settings, settings.collection, TOP_K)


@st.cache_data
def document_count() -> int:
    return len(load_sources())


SHORT_TITLES = {"Regimento do Programa de Pós-Graduação em Ciência da Computação (MDCC)": "Regimento do MDCC"}


def short_title(title: str) -> str:
    title = title.split(":")[0]
    return SHORT_TITLES.get(title, title)


def label_of(source: dict) -> str:
    return ", ".join(part for part in (short_title(source["title"]), source["article"]) if part)


def sidebar(settings) -> str:
    sidebar_brand()
    model = st.sidebar.selectbox("Modelo LLM", settings.chat_models, help="Todos rodam no Ollama Cloud.")
    st.sidebar.markdown(
        '<div class="pipeline"><div class="pipeline-head">Pipeline ativo<span class="online">Online</span></div>'
        f'<div class="pipeline-row">Modelo LLM:<b>{escape(model)}</b></div>'
        '<div class="pipeline-row">Retriever:<span class="chip">Densa · BGE-M3</span></div>'
        f'<div class="pipeline-row">Top-K / Temp:<span class="mono">K={TOP_K} · T={TEMPERATURE}</span></div>'
        f'<div class="pipeline-row">Base indexada:<b class="blue">{document_count()} documentos</b></div></div>',
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Limpar conversa", icon=":material/restart_alt:", width="stretch"):
        st.session_state.history = []
        st.rerun()
    sidebar_footer()
    return model


def show_answer(answer: Answer, model: str) -> None:
    st.markdown(answer.text)
    if answer.citations:
        badges = "".join(
            f'<a class="citation-badge" href="{escape(c["url"])}" target="_blank">[{c["n"]}] {escape(label_of(c))}</a>'
            for c in answer.citations
        )
        st.markdown(f'<div class="cites">{badges}</div>', unsafe_allow_html=True)
    tokens = answer.prompt_tokens + answer.completion_tokens
    st.markdown(f'<div class="meta">{escape(model)} · {answer.latency_ms / 1000:.1f} s · {tokens} tokens</div>', unsafe_allow_html=True)


def welcome() -> None:
    with st.container(key="welcome"):
        welcome_content()


def welcome_content() -> None:
    st.markdown(
        f'<div class="welcome"><span class="pill-blue">✦ Base normativa MDCC · {document_count()} documentos oficiais</span>'
        "<h1>Olá! Sobre qual norma do MDCC você gostaria de perguntar?</h1>"
        "<p>Eu consulto o <b>Regimento do MDCC</b>, a <b>Resolução 17/CEPE</b> (normas gerais da pós-graduação da UFC), "
        "as <b>normas do colegiado</b> e as páginas de procedimentos sobre <b>créditos, qualificação, defesa, "
        "proficiência e aproveitamento de disciplinas</b>, citando o documento e o artigo de cada resposta.</p>"
        '<p class="section-label">Perguntas frequentes sugeridas</p></div>',
        unsafe_allow_html=True,
    )
    columns = st.columns(2)
    for index, suggestion in enumerate(SUGGESTIONS):
        columns[index % 2].button(
            f"{suggestion}  ↗", key=f"suggestion-{index}", width="stretch",
            on_click=lambda text=suggestion: st.session_state.update(pending=text),
        )


def ask(question: str, model: str, settings) -> None:
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(question)
    with st.chat_message("assistant", avatar=":material/menu_book:"):
        try:
            with st.spinner("Consultando as normas..."):
                answer = answer_question(question, chunks_for(), chat_model(settings, model))
        except SystemExit as missing_key:
            st.error(str(missing_key))
            return
        except Exception:
            st.error("Não foi possível obter a resposta agora. Tente de novo em instantes.")
            return
        show_answer(answer, model)
    st.session_state.history += [("user", answer.question, None), ("assistant", answer, model)]
    append_record(LOG, {
        "model": model, "collection": settings.collection, "top_k": TOP_K, "question": answer.question,
        "answer": answer.text, "citations": answer.citations, "prompt_tokens": answer.prompt_tokens,
        "completion_tokens": answer.completion_tokens, "latency_ms": answer.latency_ms,
    })


def sources_panel() -> None:
    answers = [content for role, content, _ in st.session_state.history if isinstance(content, Answer)]
    retrieved = answers[-1].retrieved if answers else []
    cited = {(c["doc_id"], c["article"]) for c in answers[-1].citations} if answers else set()
    st.markdown(f'<div class="panel-head">🗂️ Fontes recuperadas<span class="count">{len(retrieved)}</span></div>', unsafe_allow_html=True)
    if not retrieved:
        st.markdown(
            '<div class="empty"><div class="icon">🔍</div><b>Nenhuma consulta realizada ainda</b>'
            "<span>Os trechos recuperados, com a similaridade de cada um, aparecerão aqui.</span></div>",
            unsafe_allow_html=True,
        )
        return
    for rank, chunk in enumerate(retrieved, start=1):
        similarity = chunk.get("similarity") or 0
        excerpt = chunk.get("excerpt", "")
        excerpt = escape(excerpt[:260] + ("…" if len(excerpt) > 260 else ""))
        css = "chunk cited" if (chunk["doc_id"], chunk["article"]) in cited else "chunk"
        st.markdown(
            f'<div class="{css}"><div class="chunk-top"><span class="chunk-title">#{rank} · {escape(label_of(chunk))}</span>'
            f'<span class="score">{similarity:.3f}</span></div>'
            f'<div class="bar"><span style="width:{max(0, min(similarity, 1)) * 100:.0f}%"></span></div>'
            f'<div class="chunk-text">{excerpt}</div></div>',
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(page_title="MDCC.rag · Normas", page_icon="📘", layout="wide")
    apply_style()
    settings = load_settings()
    st.session_state.setdefault("history", [])
    model = sidebar(settings)

    typed = st.chat_input("Pergunte sobre prazos, créditos, qualificação, defesa, proficiência...")
    question = typed or st.session_state.pop("pending", None)

    chat, panel = st.columns([2.6, 1], gap="large")
    with chat:
        topbar("Consulta normativa", "Com citações", "Respostas fundamentadas no Regimento do MDCC, na Resolução 17/CEPE e nas normas e procedimentos do programa")
        if not st.session_state.history and not question:
            welcome()
        for role, content, used_model in st.session_state.history:
            with st.chat_message(role, avatar=":material/person:" if role == "user" else ":material/menu_book:"):
                show_answer(content, used_model) if isinstance(content, Answer) else st.markdown(content)
        if question:
            ask(question, model, settings)
        st.markdown('<div class="hint"><span>Enter para enviar</span><span>Citações extraídas por busca semântica nos documentos oficiais do MDCC</span></div>', unsafe_allow_html=True)
    with panel:
        with st.container(height=780, border=False):
            sources_panel()


main()
