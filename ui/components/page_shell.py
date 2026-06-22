"""Envoltorio seguro para renderizado de páginas + métricas de rendimiento."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable

import streamlit as st

from ui.i18n import t
from ui.state.manager import UIStateManager

logger = logging.getLogger("ui.perf")


def render_page(
    panel_key: str,
    render_fn: Callable[[UIStateManager], None],
    state: UIStateManager,
) -> None:
    """
    Renderiza una página con manejo de errores y log de duración.
    Nunca deja la página en blanco.
    """
    t0 = time.perf_counter()
    placeholder = st.empty()

    try:
        render_fn(state)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        logger.info("Page render | panel=%s | %.1fms", panel_key, elapsed_ms)
        if elapsed_ms > 500:
            st.caption(f"⏱ {elapsed_ms:.0f}ms")
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        logger.exception("Page render failed | panel=%s | %.1fms", panel_key, elapsed_ms)
        placeholder.error(t("ui.page_error", panel=t(panel_key), error=str(exc)))
        with st.expander(t("ui.error_details")):
            st.code(str(exc))
