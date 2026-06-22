from __future__ import annotations

import streamlit as st

from ui.components.badges import provider_kind_badge
from ui.i18n import t
from ui.state import cache
from ui.state.manager import UIStateManager

import config


def render(state: UIStateManager) -> None:
    st.subheader(t("providers.title"))
    force = st.button(t("providers.refresh"), key="refresh_providers")
    ttl = getattr(config, "UI_PROVIDER_HEALTH_TTL", 120)

    if force:
        with st.spinner(t("providers.checking")):
            rows = cache.get(
                "providers_health",
                state.service.refresh_providers_health,
                ttl=ttl,
                force=True,
            )
    elif cache.has("providers_health"):
        rows = cache.get(
            "providers_health",
            state.service.refresh_providers_health,
            ttl=ttl,
        )
    else:
        rows = state.service.list_providers_catalog()
        st.info(t("providers.click_refresh"))

    for row in rows:
        kind = row.get("kind", "OFFLINE")
        healthy = row.get("healthy")
        if healthy is True:
            status = t("status.active")
            color = "#00f5d4"
        elif healthy is False:
            status = t("status.inactive")
            color = "#ff6b6b"
        else:
            status = t("providers.unknown")
            color = "#ffd166"

        st.markdown('<div class="ia-panel">', unsafe_allow_html=True)
        st.markdown(
            f"### {row['name']} — <span style='color:{color}'>{status}</span>",
            unsafe_allow_html=True,
        )
        provider_kind_badge(kind)
        st.caption(row.get("message") or "-")
        st.caption(
            f"{t('providers.origin')}: {row.get('origin', '-')} · "
            f"{t('providers.routing')}: {row.get('routing', '-')}"
        )
        models = row.get("models") or []
        st.markdown(t("providers.models", count=len(models)) + " " + (", ".join(models[:8]) or "-"))
        st.markdown("</div>", unsafe_allow_html=True)
