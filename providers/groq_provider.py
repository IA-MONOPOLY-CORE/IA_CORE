"""Proveedor Groq (placeholder — sin API real)."""

from __future__ import annotations

from typing import Any

from providers.base import BaseProvider, GenerateResponse, HealthStatus

_MODELS = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]


class GroqProvider(BaseProvider):
    IS_PLACEHOLDER = True

    def provider_name(self) -> str:
        return "groq"

    def available_models(self) -> list[str]:
        return list(_MODELS)

    def health_check(self) -> HealthStatus:
        return HealthStatus(healthy=False, message="Groq API not configured (architecture only)")

    def generate(self, prompt: str, model: str | None = None, **kwargs: Any) -> GenerateResponse:
        raise NotImplementedError("Groq API not implemented yet")
