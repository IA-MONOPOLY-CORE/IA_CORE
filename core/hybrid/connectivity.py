"""Detección de conectividad y disponibilidad de proveedores."""

from __future__ import annotations

import logging
import socket
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)

# Proveedores cloud (arquitectura; APIs no implementadas aún)
ONLINE_PROVIDER_IDS = (
    "claude",
    "deepseek",
    "openai",
    "groq",
    "gemini",
    "openrouter",
)

LOCAL_PROVIDER_IDS = ("ollama",)


class ConnectivityState(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"


class ConnectivityManager:
    """Comprueba internet, proveedores y Ollama."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self._registry = registry
        self._last_state = ConnectivityState.OFFLINE
        self._internet_cache: bool | None = None

    def is_online(self, force_refresh: bool = False) -> bool:
        if not force_refresh and self._internet_cache is not None:
            return self._internet_cache

        try:
            socket.create_connection(("1.1.1.1", 53), timeout=2.0)
            self._internet_cache = True
        except OSError:
            self._internet_cache = False

        return self._internet_cache

    def check_provider(self, provider_name: str) -> bool:
        if self._registry is None:
            return False

        provider = self._registry.get(provider_name)
        if provider is None:
            return False

        try:
            status = provider.health_check()
            return bool(status.healthy)
        except Exception as exc:
            logger.debug("Provider %s health failed: %s", provider_name, exc)
            return False

    def check_ollama(self) -> bool:
        return self.check_provider("ollama")

    def refresh_state(self) -> ConnectivityState:
        online = self.is_online(force_refresh=True)
        ollama_ok = self.check_ollama()
        any_cloud = any(self.check_provider(p) for p in ONLINE_PROVIDER_IDS)

        if online and (any_cloud or ollama_ok):
            self._last_state = ConnectivityState.ONLINE
        elif ollama_ok:
            self._last_state = ConnectivityState.DEGRADED
        else:
            self._last_state = ConnectivityState.OFFLINE

        logger.info(
            "Connectivity | internet=%s ollama=%s cloud=%s state=%s",
            online,
            ollama_ok,
            any_cloud,
            self._last_state.value,
        )
        return self._last_state

    @property
    def state(self) -> ConnectivityState:
        return self._last_state

    def snapshot(self) -> dict[str, bool]:
        return {
            "internet": self.is_online(),
            "ollama": self.check_ollama(),
            **{name: self.check_provider(name) for name in ONLINE_PROVIDER_IDS},
        }
