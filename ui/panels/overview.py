from __future__ import annotations

import config
import streamlit as st

from ui.components.theme import metric_card
from ui.i18n import t
from ui.state import cache
from ui.state.manager import UIStateManager


def render(state: UIStateManager) -> None:
    st.subheader(t("overview.title"))
    ttl = getattr(config, "UI_CACHE_TTL_SAFE", 300) if config.SAFE_MODE else 30
    overview = cache.get("overview", state.service.get_system_overview, ttl=ttl)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        tone = "ok" if overview.get("supervisor_running") else "err"
        status = (
            t("overview.status.online")
            if overview.get("supervisor_running")
            else t("overview.status.offline")
        )
        metric_card(t("overview.metric.supervisor"), status, tone)
    with c2:
        metric_card(t("overview.metric.agents"), str(len(overview.get("agents") or [])))
    with c3:
        metric_card(t("overview.metric.providers"), str(len(overview.get("providers") or [])))
    with c4:
        metric_card(t("overview.metric.tools"), str(len(overview.get("tools") or [])))

    st.markdown('<div class="ia-panel">', unsafe_allow_html=True)
    mem = overview.get("memory") or {}
    if not config.SAFE_MODE:
        m = overview.get("metrics") or {}
        st.markdown(
            t(
                "overview.runtime",
                uptime=m.get("uptime_s", 0),
                orch=m.get("orchestrations", 0),
                disp=m.get("agent_dispatches", 0),
                last=m.get("last_orchestration_ms", 0),
            )
        )
    else:
        st.caption(t("overview.safe_metrics"))
    st.markdown(
        t(
            "overview.memory",
            path=mem.get("path", "-"),
            keys=mem.get("key_count", 0),
            runs=mem.get("history_count", 0),
        )
    )
    st.markdown("</div>", unsafe_allow_html=True)
