"""Caché en session_state con TTL (ligero, sin dependencias externas)."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, TypeVar

import streamlit as st

import config

logger = logging.getLogger("ui.perf")

T = TypeVar("T")

_PREFIX = "ia_cache_"


def _ttl(default: int | None = None) -> float:
    if getattr(config, "SAFE_MODE", False):
        return float(default or getattr(config, "UI_CACHE_TTL_SAFE", 300))
    return float(default or getattr(config, "UI_CACHE_TTL", 60))


def get(
    key: str,
    factory: Callable[[], T],
    *,
    ttl: float | None = None,
    force: bool = False,
) -> T:
    """Obtiene valor cacheado o lo genera con factory()."""
    full_key = _PREFIX + key
    effective_ttl = ttl if ttl is not None else _ttl()
    now = time.perf_counter()

    if not force and full_key in st.session_state:
        entry = st.session_state[full_key]
        if now - entry["ts"] < entry["ttl"]:
            return entry["data"]

    t0 = time.perf_counter()
    data = factory()
    elapsed_ms = (time.perf_counter() - t0) * 1000
    st.session_state[full_key] = {"data": data, "ts": now, "ttl": effective_ttl}
    logger.info("Cache miss | key=%s | %.1fms", key, elapsed_ms)
    return data


def has(key: str) -> bool:
    full_key = _PREFIX + key
    if full_key not in st.session_state:
        return False
    entry = st.session_state[full_key]
    return time.perf_counter() - entry["ts"] < entry["ttl"]


def invalidate(prefix: str | None = None) -> None:
    """Invalida entradas (todas o por prefijo de clave)."""
    keys = [k for k in st.session_state.keys() if str(k).startswith(_PREFIX)]
    for key in keys:
        if prefix is None or str(key).startswith(_PREFIX + prefix):
            del st.session_state[key]


def set_value(key: str, data: Any, ttl: float | None = None) -> None:
    st.session_state[_PREFIX + key] = {
        "data": data,
        "ts": time.perf_counter(),
        "ttl": ttl if ttl is not None else _ttl(),
    }
