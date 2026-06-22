from __future__ import annotations

import config
import streamlit as st

from ui.components.badges import status_badge
from ui.i18n import t
from ui.state import cache
from ui.state.manager import UIStateManager


def render(state: UIStateManager) -> None:
    st.subheader(t("hybrid.title"))
    force_full = st.button(t("hybrid.refresh"), key="hybrid_refresh_btn")
    ttl = getattr(config, "UI_CACHE_TTL_SAFE", 300) if config.SAFE_MODE else 60

    status = cache.get(
        "hybrid_status",
        lambda: state.service.get_hybrid_status(full=force_full),
        ttl=ttl,
        force=force_full,
    )

    if not status:
        st.info(t("hybrid.disabled"))
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        status_badge(t("hybrid.badge.mode"), status.get("execution_mode", "-"))
    with c2:
        status_badge(t("hybrid.badge.source"), status.get("source", "-"))
    with c3:
        status_badge(
            t("hybrid.badge.provider"),
            status.get("active_provider") or t("hybrid.not_loaded"),
            "#ffd166",
        )
    with c4:
        status_badge(
            "SAFE",
            t("hybrid.yes") if status.get("safe_mode") else t("hybrid.no"),
            "#ff6b6b" if status.get("safe_mode") else "#6b7280",
        )

    st.markdown('<div class="ia-panel">', unsafe_allow_html=True)
    st.markdown(
        f"**{t('hybrid.model')}:** `{status.get('active_model') or t('hybrid.not_loaded')}`"
    )
    st.markdown(f"**{t('hybrid.policy')}:** `{status.get('policy', '-')}`")
    if status.get("routing_reason"):
        st.caption(status.get("routing_reason"))
    elif not force_full:
        st.caption(t("hybrid.light_hint"))
    st.markdown("</div>", unsafe_allow_html=True)

    if force_full:
        conn = status.get("connectivity")
        if conn is not None:
            st.markdown(f"**{t('hybrid.connectivity')}**")
            st.json(conn)
        summary = status.get("metrics_summary")
        if summary and not config.SAFE_MODE:
            st.markdown(f"**{t('hybrid.metrics')}**")
            st.json(summary)
    elif config.SAFE_MODE:
        st.info(t("hybrid.safe_hint"))
