from __future__ import annotations

import config
import streamlit as st

from ui.i18n import t
from ui.state import cache
from ui.state.manager import UIStateManager


def render(state: UIStateManager) -> None:
    st.subheader(t("memory.title"))
    ttl = getattr(config, "UI_CACHE_TTL_SAFE", 300) if config.SAFE_MODE else 20

    snapshot = cache.get(
        "memory_snapshot",
        state.service.get_memory_snapshot,
        ttl=ttl,
    )
    status = snapshot.get("status") or {}

    st.markdown(t("memory.path", path=status.get("path", "-")))
    st.markdown(
        t(
            "memory.keys",
            keys=status.get("key_count", 0),
            history=status.get("history_count", 0),
        )
    )

    preview = status.get("keys_preview") or []
    if preview:
        st.caption(", ".join(preview))

    keys = cache.get("memory_keys", state.service.list_memory_keys, ttl=ttl)
    if keys:
        key = st.selectbox(t("memory.inspect"), keys)
        if key:
            try:
                st.json(state.service.get_memory_value(key))
            except Exception as exc:
                st.error(t("ui.page_error", panel=key, error=str(exc)))

    st.markdown("---")
    st.markdown(t("memory.timeline"))
    history = snapshot.get("history") or []
    if history:
        for entry in history:
            ok = "✓" if entry.get("success") else "✗"
            st.caption(
                f"{ok} `{entry.get('execution_id', '-')[:8]}` · "
                f"{entry.get('mode', '-')} · {entry.get('started_at', '-')[:19]}"
            )
        st.dataframe(history, use_container_width=True, hide_index=True)
    else:
        st.info(t("memory.history_empty"))

    if st.checkbox(t("memory.latest"), value=False):
        try:
            latest = state.service.get_latest_execution_detail()
            if latest:
                st.json(latest.get("detail"))
            else:
                st.info(t("memory.history_empty"))
        except Exception as exc:
            st.error(t("ui.page_error", panel=t("memory.latest"), error=str(exc)))
