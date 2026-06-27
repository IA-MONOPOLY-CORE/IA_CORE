"""Registro central de proveedores LLM."""

from __future__ import annotations

import logging
from typing import Any

from providers.base import BaseProvider
from providers.claude_provider import ClaudeProvider
from providers.gemini_provider import GeminiProvider
from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.nvidia_provider import NvidiaProvider  # ✅ NUEVO

logger = logging.getLogger(__name__)

try:
    import config as app_config
except ImportError:
    app_config = None

_BUILTIN_PROVIDERS: list[type[BaseProvider]] = [
    OpenAIProvider,
    ClaudeProvider,
    GeminiProvider,
    OllamaProvider,
    NvidiaProvider,  # ✅ NUEVO
]


class ProviderRegistry:
    """
    Registro dinámico de proveedores.
    Preparado para fallback, multi-modelo y votación entre modelos.
    """

    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}
        self._fallback_chain: list[str] = []

    def register(self, provider: BaseProvider) -> None:
        name = provider.provider_name()
        if name in self._providers:
            logger.warning("Reemplazando proveedor existente: %s", name)
        self._providers[name] = provider
        logger.info("Proveedor registrado: %s", name)

    def get(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)

    def require(self, name: str) -> BaseProvider:
        provider = self.get(name)
        if provider is None:
            raise KeyError(f"Proveedor no encontrado: {name}")
        return provider

    def list_active(self) -> list[str]:
        return list(self._providers.keys())

    def list_providers(self) -> list[BaseProvider]:
        return list(self._providers.values())

    def set_fallback_chain(self, provider_names: list[str]) -> None:
        self._fallback_chain = list(provider_names)
        logger.info("Cadena de fallback configurada: %s", self._fallback_chain)

    def get_fallback_chain(self) -> list[str]:
        return list(self._fallback_chain)

    def load_builtin_providers(self) -> int:
        """Registra los proveedores integrados."""
        logger.info("Cargando proveedores integrados")
        count = 0
        skip_health = bool(
            app_config
            and (
                getattr(app_config, "SKIP_PROVIDER_HEALTH_ON_START", False)
                or getattr(app_config, "SAFE_MODE", False)
            )
        )
        for cls in _BUILTIN_PROVIDERS:
            provider = cls()
            self.register(provider)
            name = provider.provider_name()
            if skip_health:
                logger.info("Proveedor %s registrado (health omitido en arranque)", name)
            else:
                status = provider.health_check()
                logger.info(
                    "Proveedor %s cargado | healthy=%s",
                    name,
                    status.healthy,
                )
            count += 1
        if app_config and getattr(app_config, "HYBRID_REGISTER_CLOUD_STUBS", False):
            count += self.load_cloud_stubs()
        return count

    def load_cloud_stubs(self) -> int:
        """Registra proveedores cloud placeholder para routing híbrido."""
        from providers.deepseek_provider import DeepSeekProvider
        from providers.groq_provider import GroqProvider
        from providers.openrouter_provider import OpenRouterProvider

        stubs = [DeepSeekProvider, GroqProvider, OpenRouterProvider]
        loaded = 0
        for cls in stubs:
            provider = cls()
            self.register(provider)
            loaded += 1
        logger.info("Proveedores cloud stub registrados: %d", loaded)
        return loaded

    def generate_with_fallback(
        self,
        provider_name: str,
        prompt: str,
        model: str | None = None,
        **kwargs: Any,
    ):
        chain = [provider_name, *self._fallback_chain]
        last_error: Exception | None = None

        for name in chain:
            provider = self.get(name)
            if provider is None:
                continue
            try:
                return provider.generate(prompt, model=model, **kwargs)
            except Exception as exc:
                last_error = exc
                logger.warning("Proveedor '%s' falló, probando siguiente", name)

        raise RuntimeError(f"Ningún proveedor disponible en cadena: {chain}") from last_error
