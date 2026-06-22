"""
IA_CORE — Visual Operating Interface
Launch: streamlit run ui/app.py
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

import config as app_config
from ui.components.badges import routing_badges, status_badge
from ui.components.page_shell import render_page
from ui.components.theme import apply_theme
from ui.i18n import get_i18n, set_language, t
from ui.panels import (
    agents,
    hybrid_panel,
    logs,
    memory_panel,
    orchestration,
    overview,
    providers,
    settings,
    agent_creator,
)
from ui.state.manager import get_state

HYBRID_MODE = getattr(app_config, "HYBRID_MODE", True)
SAFE_MODE = getattr(app_config, "SAFE_MODE", False)

app_config.LOG_DIR.mkdir(parents=True, exist_ok=True)
_log_handler = logging.FileHandler(app_config.LOG_DIR / "supervisor.log", encoding="utf-8")
_log_handler.setFormatter(logging.Formatter(app_config.LOG_FORMAT))
logging.basicConfig(
    level=getattr(logging, app_config.LOG_LEVEL.upper(), logging.INFO),
    handlers=[_log_handler],
)
logging.getLogger("ui.perf").addHandler(_log_handler)
logging.getLogger("ui.perf").setLevel(logging.INFO)

logger = logging.getLogger("ui.app")

PANEL_KEYS = [
    "panel.overview",
    "panel.hybrid",
    "panel.agents",
    "panel.providers",
    "panel.orchestration",
    "panel.memory",
    "panel.logs",
    "panel.settings",
    "panel.agent_creator",
]

PANELS = {
    "panel.overview": overview.render,
    "panel.hybrid": hybrid_panel.render,
    "panel.agents": agents.render,
    "panel.providers": providers.render,
    "panel.orchestration": orchestration.render,
    "panel.memory": memory_panel.render,
    "panel.logs": logs.render,
    "panel.settings": settings.render,
    "panel.agent_creator": agent_creator.render,
}


def _render_language_selector() -> None:
    i18n = get_i18n()
    options = {lang["code"]: lang["label"] for lang in i18n.available_languages()}
    codes = list(options.keys())
    labels = [options[c] for c in codes]

    current = i18n.current_language
    index = codes.index(current) if current in codes else 0

    selected_label = st.selectbox(
        t("sidebar.language"),
        labels,
        index=index,
        key="ui_language_select",
    )
    selected_code = codes[labels.index(selected_label)]
    if selected_code != current:
        set_language(selected_code)


def main() -> None:
    t0 = time.perf_counter()
    st.set_page_config(
        page_title="IA_CORE",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    get_i18n()
    apply_theme()

    st.title(t("app.title"))
    st.caption(t("app.subtitle"))

    state = get_state()
    state.service.set_translator(t)

    header = st.container()
    with header:
        if SAFE_MODE:
            status_badge("MODE", "SAFE", "#ff6b6b")
        if state.service.connected:
            badge = state.sidebar_hybrid_badge()
            routing_badges(
                safe_mode=SAFE_MODE,
                source=badge.get("source", "-"),
                model=getattr(app_config, "DEFAULT_LOCAL_MODEL", "phi3"),
                provider="ollama",
            )

    with st.sidebar:
        st.markdown(f"### {t('sidebar.control')}")
        _render_language_selector()

        if state.service.connected:
            st.success(t("sidebar.connected"))
            if HYBRID_MODE:
                badge = state.sidebar_hybrid_badge()
                st.caption(
                    f"{t('hybrid.badge.mode')}: {badge.get('execution_mode', '-')} · "
                    f"{t('hybrid.badge.source')}: {badge.get('source', '-')}"
                )
        else:
            st.warning(t("sidebar.offline"))

        if st.button(t("sidebar.connect"), use_container_width=True):
            with st.spinner(t("ui.connecting")):
                state.ensure_connected()
            st.session_state.pop("ia_loaded_panels", None)
            st.rerun()

        if st.button(t("sidebar.disconnect"), use_container_width=True):
            state.disconnect()
            st.session_state.pop("ia_loaded_panels", None)
            st.rerun()

        st.markdown("---")
        panel_key = st.radio(
            t("sidebar.panel"),
            PANEL_KEYS,
            format_func=t,
            label_visibility="collapsed",
            key="ia_active_panel",
        )

        st.markdown("---")
        st.caption(t("sidebar.version"))
        st.caption(t("sidebar.future"))

    if not state.service.connected:
        st.info(t("info.connect_first"))
        return

    loaded = st.session_state.setdefault("ia_loaded_panels", set())
    first_visit = panel_key not in loaded

    if first_visit:
        with st.spinner(t("ui.loading")):
            render_page(panel_key, PANELS[panel_key], state)
        loaded.add(panel_key)
    else:
        render_page(panel_key, PANELS[panel_key], state)

    elapsed_ms = (time.perf_counter() - t0) * 1000
    logging.getLogger("ui.perf").info("App frame | panel=%s | %.1fms", panel_key, elapsed_ms)


if __name__ == "__main__":
    logger.info("IA_CORE UI starting")
    main()