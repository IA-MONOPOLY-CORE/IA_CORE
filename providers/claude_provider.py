"""Proveedor Anthropic Claude (placeholder)."""

from __future__ import annotations

from typing import Any

from providers.base import BaseProvider, GenerateResponse, HealthStatus

_MODELS = ["claude-sonnet-4", "claude-haiku-4"]


class ClaudeProvider(BaseProvider):
    IS_PLACEHOLDER = True

    def provider_name(self) -> str:
        return "claude"

    def available_models(self) -> list[str]:
        return list(_MODELS)

    def health_check(self) -> HealthStatus:
        return HealthStatus(healthy=False, message="Claude placeholder (no API key configured)")

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        **kwargs: Any,
    ) -> GenerateResponse:
        selected = model or self.default_model()
        return GenerateResponse(
            text=f"[claude/{selected}] placeholder response for: {prompt[:80]}",
            provider=self.provider_name(),
            model=selected,
            metadata={"api_called": False},
        )
