"""Gestor de estado de sesión Streamlit (preparado para streaming/async)."""

from __future__ import annotations

import logging
from typing import Any

import streamlit as st

from ui.backend.service import SupervisorService
from ui.i18n import t
from ui.state import cache

logger = logging.getLogger(__name__)

_SESSION_KEY = "ia_core_ui_state"
_SIDEBAR_HYBRID_KEY = "ia_sidebar_hybrid"


class UIStateManager:
    """
    Mantiene conexión al supervisor y buffers para actualizaciones en vivo.
    Futuro: websocket_events, async_jobs, stream_chunks.
    """

    def __init__(self) -> None:
        self.service = SupervisorService()
        self.live_events: list[dict[str, Any]] = []
        self.last_orchestration: dict[str, Any] | None = None
        self.stream_buffer: list[str] = []

    def ensure_connected(self) -> None:
        if not self.service.connected:
            self.service.connect()
            cache.invalidate()
            st.session_state[_SIDEBAR_HYBRID_KEY] = self.service.get_sidebar_hybrid_badge()
            self.push_event("connected", t("event.connected"))

    def disconnect(self) -> None:
        self.service.disconnect()
        cache.invalidate()
        st.session_state.pop(_SIDEBAR_HYBRID_KEY, None)

    def sidebar_hybrid_badge(self) -> dict[str, str]:
        if _SIDEBAR_HYBRID_KEY in st.session_state:
            return st.session_state[_SIDEBAR_HYBRID_KEY]
        badge = self.service.get_sidebar_hybrid_badge()
        st.session_state[_SIDEBAR_HYBRID_KEY] = badge
        return badge

    def push_event(self, kind: str, message: str) -> None:
        self.live_events.append({"kind": kind, "message": message})
        if len(self.live_events) > 200:
            self.live_events = self.live_events[-100:]

    def set_last_orchestration(self, payload: dict[str, Any]) -> None:
        self.last_orchestration = payload
        self.push_event(
            "orchestration",
            t("event.orchestration", id=payload.get("execution_id", "-")),
        )


def get_state() -> UIStateManager:
    if _SESSION_KEY not in st.session_state:
        st.session_state[_SESSION_KEY] = UIStateManager()
    return st.session_state[_SESSION_KEY]
