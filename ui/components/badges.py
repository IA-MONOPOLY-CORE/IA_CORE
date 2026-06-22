"""Badges reutilizables para la UI."""

from __future__ import annotations

import streamlit as st

from ui.i18n import t


def status_badge(label: str, value: str, color: str = "#00f5d4") -> None:
    st.markdown(
        f"<span style='background:{color}22;color:{color};padding:4px 10px;"
        f"border-radius:6px;border:1px solid {color}55;margin-right:6px'>"
        f"<b>{label}</b>: {value}</span>",
        unsafe_allow_html=True,
    )


def provider_kind_badge(kind: str) -> None:
    colors = {
        "LOCAL_ACTIVE": "#00f5d4",
        "CLOUD_CONFIGURED": "#7b9eff",
        "CLOUD_PLACEHOLDER": "#6b7280",
        "OFFLINE": "#ff6b6b",
    }
    key = f"providers.kind.{kind.lower()}"
    label = t(key) if key else kind
    status_badge(t("providers.badge.kind"), label, colors.get(kind, "#ffd166"))


def routing_badges(*, safe_mode: bool, source: str, model: str, provider: str) -> None:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        status_badge("SAFE", t("hybrid.yes") if safe_mode else t("hybrid.no"), "#ff6b6b" if safe_mode else "#6b7280")
    with c2:
        status_badge(t("hybrid.badge.source"), source or "-", "#00f5d4" if source == "local" else "#7b9eff")
    with c3:
        status_badge(t("hybrid.badge.provider"), provider or "-", "#ffd166")
    with c4:
        status_badge(t("hybrid.model"), model or "-", "#00f5d4")
