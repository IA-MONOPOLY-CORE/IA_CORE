"""Proveedor OpenRouter (placeholder — sin API real)."""

from __future__ import annotations

from typing import Any

from providers.base import BaseProvider, GenerateResponse, HealthStatus

_MODELS = ["openrouter/auto"]


class OpenRouterProvider(BaseProvider):
    IS_PLACEHOLDER = True

    def provider_name(self) -> str:
        return "openrouter"

    def available_models(self) -> list[str]:
        return list(_MODELS)

    def health_check(self) -> HealthStatus:
        return HealthStatus(healthy=False, message="OpenRouter API not configured (architecture only)")

    def generate(self, prompt: str, model: str | None = None, **kwargs: Any) -> GenerateResponse:
        raise NotImplementedError("OpenRouter API not implemented yet")
