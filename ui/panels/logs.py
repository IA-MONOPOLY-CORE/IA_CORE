from __future__ import annotations

import config
import streamlit as st

from ui.i18n import t
from ui.state.manager import UIStateManager

_LOG_CACHE_KEY = "ia_log_tail"


def render(state: UIStateManager) -> None:
    st.subheader(t("logs.title"))
    lines = st.slider(t("logs.lines"), 20, 200, 80, step=10)
    refresh = st.button(t("logs.refresh"), key="refresh_logs")

    if refresh:
        with st.spinner(t("ui.loading")):
            log_lines = state.service.tail_log_file(lines=lines)
        st.session_state[_LOG_CACHE_KEY] = {"lines": lines, "content": log_lines}
    else:
        cache_entry = st.session_state.get(_LOG_CACHE_KEY)
        if cache_entry is None:
            st.caption(t("logs.press_refresh"))
            log_lines = []
        elif cache_entry.get("lines") != lines:
            st.caption(t("logs.lines_changed"))
            log_lines = cache_entry.get("content") or []
        else:
            log_lines = cache_entry.get("content") or []

    if state.last_orchestration:
        st.markdown(t("logs.last_execution"))
        entry = state.last_orchestration
        st.caption(
            f"`{entry.get('execution_id', '-')}` · {entry.get('mode')} · "
            f"{entry.get('duration_ms', 0):.0f}ms · success={entry.get('success')}"
        )

    errors = [ln for ln in log_lines if "| ERROR" in ln or "ERROR" in ln]
    warnings = [ln for ln in log_lines if "| WARNING" in ln or "WARNING" in ln]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(t("logs.warnings", count=len(warnings)))
        st.code("\n".join(warnings[-30:]) or t("logs.none"), language="log")
    with c2:
        st.markdown(t("logs.errors", count=len(errors)))
        st.code("\n".join(errors[-30:]) or t("logs.none"), language="log")

    st.markdown(t("logs.runtime"))
    st.code("\n".join(log_lines) or t("logs.empty"), language="log")

    if state.live_events and not config.SAFE_MODE:
        st.markdown(t("logs.events"))
        for ev in reversed(state.live_events[-20:]):
            st.caption(f"[{ev['kind']}] {ev['message']}")
