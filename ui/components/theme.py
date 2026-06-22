"""Estilo visual cyberpunk oscuro (CSS inyectado)."""

from __future__ import annotations

import streamlit as st

CYBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Orbitron:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: #0a0e14;
    color: #c8d3f5;
}

.stApp {
    background: radial-gradient(ellipse at top, #111827 0%, #0a0e14 55%);
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f5d4 !important;
    letter-spacing: 0.06em;
}

.ia-metric {
    background: linear-gradient(135deg, #121826 0%, #0f1420 100%);
    border: 1px solid #1f2a44;
    border-left: 3px solid #00f5d4;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
}

.ia-panel {
    background: #0f131c;
    border: 1px solid #243049;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 0 24px rgba(0, 245, 212, 0.04);
}

.ia-tag-ok { color: #00f5d4; }
.ia-tag-warn { color: #ffd166; }
.ia-tag-err { color: #ff6b6b; }

div[data-testid="stSidebar"] {
    background-color: #080b12;
    border-right: 1px solid #1c2740;
}

.stButton > button {
    background: linear-gradient(90deg, #0d9488, #0891b2);
    color: #041014;
    border: none;
    font-weight: 600;
}
</style>
"""


def apply_theme() -> None:
    st.markdown(CYBER_CSS, unsafe_allow_html=True)


def metric_card(label: str, value: str, tone: str = "ok") -> None:
    tone_class = {"ok": "ia-tag-ok", "warn": "ia-tag-warn", "err": "ia-tag-err"}.get(
        tone, "ia-tag-ok"
    )
    st.markdown(
        f'<div class="ia-metric"><div style="font-size:0.75rem;opacity:0.7">{label}</div>'
        f'<div class="{tone_class}" style="font-size:1.25rem;font-weight:600">{value}</div></div>',
        unsafe_allow_html=True,
    )
