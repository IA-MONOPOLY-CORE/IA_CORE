"""Contrato base para proveedores LLM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GenerateRequest:
    """Petición de generación (extensible)."""

    prompt: str
    model: str | None = None
    # Futuro: stream, temperature, max_tokens, messages
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerateResponse:
    """Respuesta de generación (extensible)."""

    text: str
    provider: str
    model: str
    # Futuro: token_usage, finish_reason, latency_ms
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthStatus:
    """Estado de salud del proveedor."""

    healthy: bool
    message: str = ""
    # Futuro: rate_limit_remaining, last_error


class BaseProvider(ABC):
    """
    Interfaz común para todos los proveedores.
    Preparado para streaming, async, retries y consenso multi-modelo.
    """

    @abstractmethod
    def provider_name(self) -> str:
        """Identificador único del proveedor (ej. 'openai')."""

    @abstractmethod
    def available_models(self) -> list[str]:
        """Modelos soportados por este proveedor."""

    @abstractmethod
    def health_check(self) -> HealthStatus:
        """Comprueba disponibilidad (placeholder sin API real)."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str | None = None,
        **kwargs: Any,
    ) -> GenerateResponse:
        """Genera texto a partir de un prompt."""

    # --- Hooks futuros (no implementados) ---

    def generate_stream(self, prompt: str, model: str | None = None, **kwargs: Any):
        """Placeholder para streaming."""
        raise NotImplementedError("Streaming no implementado")

    async def generate_async(
        self,
        prompt: str,
        model: str | None = None,
        **kwargs: Any,
    ) -> GenerateResponse:
        """Placeholder para ejecución async."""
        raise NotImplementedError("Async no implementado")

    def default_model(self) -> str:
        models = self.available_models()
        return models[0] if models else "default"
