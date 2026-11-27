"""Shared look of the Streamlit pages: dark slate and blue, as in the HTML mockup."""

from html import escape

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
html, body, .stMarkdown, .stChatMessage, button, input, textarea, select {font-family: 'Inter', sans-serif;}
.block-container {padding-top: 1.2rem; max-width: 1400px;}
header[data-testid="stHeader"] {background: transparent;}
[data-testid="stSidebar"] {background: #0F172A; border-right: 1px solid #1E293B;}
[data-testid="stSidebarNav"] {display: none;}
.mono {font-family: 'JetBrains Mono', monospace;}

.brand {display: flex; align-items: center; gap: .7rem; padding: .2rem 0 1rem 0; border-bottom: 1px solid #1E293B; margin-bottom: .9rem;}
.brand-icon {width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
             background: linear-gradient(135deg, #2563EB, #4F46E5); font-size: 1.25rem; box-shadow: 0 4px 14px rgba(37,99,235,.35);}
.brand-name {font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 1.15rem; color: #F1F5F9; line-height: 1.1;}
.brand-name span {color: #60A5FA;}
.brand-tag {font-family: 'JetBrains Mono', monospace; font-size: .62rem; color: #93C5FD; border: 1px solid #1E3A8A;
            background: rgba(30,58,138,.35); border-radius: 4px; padding: 0 .3rem; margin-left: .3rem; vertical-align: middle;}
.brand-sub {color: #94A3B8; font-size: .78rem;}

[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {border-radius: 10px; padding: .45rem .7rem;}
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {background: #1E293B;}

.pipeline {border: 1px solid #1E293B; background: rgba(30,41,59,.4); border-radius: 14px; padding: .8rem .9rem; margin: 1rem 0 .6rem 0;}
.pipeline-head {display: flex; justify-content: space-between; font-size: .7rem; font-weight: 600; letter-spacing: .06em;
                text-transform: uppercase; color: #94A3B8; margin-bottom: .55rem;}
.online {color: #34D399; text-transform: none; letter-spacing: 0;}
.online::before {content: "●"; font-size: .6rem; margin-right: .3rem; vertical-align: middle;}
.pipeline-row {display: flex; justify-content: space-between; align-items: center; font-size: .78rem; color: #94A3B8; padding: .22rem 0;}
.pipeline-row b {color: #E2E8F0; font-weight: 600;}
.chip {font-family: 'JetBrains Mono', monospace; font-size: .7rem; background: #1E293B; color: #CBD5E1; border-radius: 4px; padding: .05rem .35rem;}
.blue {color: #60A5FA !important;}
.side-foot {color: #94A3B8; font-size: .72rem; border-top: 1px solid #1E293B; padding-top: .7rem; margin-top: 1.2rem;}
.side-foot b {color: #CBD5E1;}

.topbar {display: flex; align-items: flex-start; justify-content: space-between; border-bottom: 1px solid #1E293B; padding-bottom: .8rem; margin-bottom: 1.1rem;}
.topbar h2 {font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 1.25rem; color: #F1F5F9; margin: 0; padding: 0;}
.badge-green {font-size: .72rem; font-weight: 600; color: #34D399; border: 1px solid rgba(52,211,153,.35);
              background: rgba(6,78,59,.35); border-radius: 999px; padding: .1rem .55rem; margin-left: .5rem; vertical-align: middle;}
.topbar p {color: #94A3B8; font-size: .8rem; margin: .2rem 0 0 0;}

.st-key-welcome {border: 1px solid #1E293B; background: #0F172A; border-radius: 22px; padding: 1.8rem 2rem 1.6rem 2rem; margin-bottom: .8rem;}
[data-testid="stSidebarHeader"] {height: 1rem; padding: 0;}
[data-testid="stSidebarUserContent"] {padding-top: .6rem;}
.pill-blue {display: inline-block; font-size: .78rem; font-weight: 500; color: #93C5FD; background: rgba(23,37,84,.6);
            border: 1px solid #1E3A8A; border-radius: 999px; padding: .15rem .7rem; margin-bottom: .9rem;}
.welcome h1 {font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 1.75rem; color: #F8FAFC; line-height: 1.25; margin: 0 0 .6rem 0; padding: 0;}
.welcome p {color: #94A3B8; font-size: .95rem; line-height: 1.6; margin: 0;}
.welcome p b {color: #CBD5E1;}
.section-label {font-size: .72rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase; color: #64748B; margin: 1.3rem 0 0 0 !important;}

div.stButton > button {background: #0F172A; border: 1px solid #1E293B; border-radius: 14px; color: #E2E8F0;
                       min-height: 3.1rem; padding: .7rem 1rem; text-align: left; justify-content: flex-start; font-weight: 500;
                       transition: all .15s ease;}
div.stButton > button > div {justify-content: flex-start; width: 100%;}
div.stButton > button p {white-space: normal; text-align: left; line-height: 1.35;}
.st-key-welcome div.stButton > button {background: transparent; min-height: 3.6rem;}
[data-testid="stSidebar"] div.stButton > button > div {justify-content: center;}
div.stButton > button:hover {border-color: #2563EB; background: rgba(23,37,84,.45); color: #FFFFFF; transform: translateY(-1px);}

[data-testid="stChatMessage"] {background: #0F172A; border: 1px solid #1E293B; border-radius: 16px; padding: .9rem 1rem; margin-bottom: .7rem;}
.cites {display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .6rem;}
.citation-badge {font-size: .76rem; color: #93C5FD; background: rgba(23,37,84,.6); border: 1px solid #1E3A8A;
                 border-radius: 8px; padding: .15rem .55rem; text-decoration: none !important; transition: all .15s ease;}
.citation-badge:hover {transform: translateY(-1px); border-color: #3B82F6; color: #DBEAFE;}
.meta {font-family: 'JetBrains Mono', monospace; color: #64748B; font-size: .7rem; margin-top: .55rem;}

.panel-head {display: flex; justify-content: space-between; align-items: center; font-family: 'Plus Jakarta Sans', sans-serif;
             font-weight: 700; color: #F1F5F9; font-size: .98rem; padding-bottom: .7rem; border-bottom: 1px solid #1E293B; margin-bottom: .8rem;}
.count {font-family: 'JetBrains Mono', monospace; font-size: .7rem; background: #1E293B; color: #CBD5E1; border-radius: 6px; padding: .05rem .45rem;}
.empty {text-align: center; color: #94A3B8; padding: 2.2rem .6rem;}
.empty .icon {width: 40px; height: 40px; border-radius: 50%; background: #1E293B; display: inline-flex; align-items: center; justify-content: center; margin-bottom: .7rem;}
.empty b {display: block; color: #E2E8F0; font-size: .85rem; font-weight: 600; margin-bottom: .3rem;}
.empty span {font-size: .74rem;}
.chunk {border: 1px solid #1E293B; background: #0F172A; border-radius: 12px; padding: .65rem .75rem; margin-bottom: .55rem;}
.chunk.cited {border-color: #1E40AF; box-shadow: inset 3px 0 0 #3B82F6;}
.chunk-top {display: flex; justify-content: space-between; align-items: center; gap: .4rem; margin-bottom: .3rem;}
.chunk-title {font-size: .78rem; font-weight: 600; color: #E2E8F0;}
.score {font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #34D399;}
.bar {height: 4px; background: #1E293B; border-radius: 999px; margin: .25rem 0 .4rem 0;}
.bar span {display: block; height: 4px; border-radius: 999px; background: linear-gradient(90deg, #2563EB, #34D399);}
.chunk-text {font-size: .74rem; color: #94A3B8; line-height: 1.45;}
.hint {display: flex; justify-content: space-between; color: #64748B; font-size: .7rem; margin-top: .2rem;}
</style>
"""


def apply_style() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_brand() -> None:
    st.sidebar.markdown(
        '<div class="brand"><div class="brand-icon">📘</div><div>'
        '<div class="brand-name">MDCC.<span>rag</span><span class="brand-tag">UFC</span></div>'
        '<div class="brand-sub">Normas &amp; Regimentos</div></div></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.page_link("app.py", label="Chat & Consulta", icon=":material/forum:")
    st.sidebar.page_link("pages/1_Resultados.py", label="Resultados & Avaliação", icon=":material/bar_chart:")


def sidebar_footer() -> None:
    st.sidebar.markdown(
        '<div class="side-foot"><b>Protótipo acadêmico · não oficial</b><br>'
        "Disciplina de Modelos de Linguagem de Grande Escala · MDCC/UFC<br>"
        "Confirme regras importantes com a secretaria do MDCC.</div>",
        unsafe_allow_html=True,
    )


def topbar(title: str, badge: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="topbar"><div><h2>{escape(title)}<span class="badge-green">{escape(badge)}</span></h2>'
        f"<p>{escape(subtitle)}</p></div></div>",
        unsafe_allow_html=True,
    )
