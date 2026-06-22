"""Políticas de recursos y modos de ejecución híbrida."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExecutionMode(str, Enum):
    """Modo global de ejecución del sistema híbrido."""

    ONLINE = "online"
    HYBRID = "hybrid"
    OFFLINE = "offline"
    SAFE_MODE = "safe_mode"


class ResourcePolicy(str, Enum):
    """Perfil de uso de hardware."""

    LIGHTWEIGHT = "lightweight"
    BALANCED = "balanced"
    PERFORMANCE = "performance"


@dataclass(frozen=True)
class PolicyProfile:
    """Parámetros por política (extensible)."""

    prefer_local: bool
    max_context_tokens: int
    prefer_fast_models: bool
    allow_cloud: bool


POLICY_PROFILES: dict[ResourcePolicy, PolicyProfile] = {
    ResourcePolicy.LIGHTWEIGHT: PolicyProfile(
        prefer_local=True,
        max_context_tokens=2048,
        prefer_fast_models=True,
        allow_cloud=False,
    ),
    ResourcePolicy.BALANCED: PolicyProfile(
        prefer_local=False,
        max_context_tokens=4096,
        prefer_fast_models=False,
        allow_cloud=True,
    ),
    ResourcePolicy.PERFORMANCE: PolicyProfile(
        prefer_local=False,
        max_context_tokens=8192,
        prefer_fast_models=False,
        allow_cloud=True,
    ),
}

# Mapeo modelo lógico → nombre Ollama
LOCAL_MODEL_ALIASES: dict[str, str] = {
    "phi3": "phi3:mini",
    "tinyllama": "tinyllama",
    "qwen2:1.5b": "qwen2:1.5b",
    "gemma:2b": "gemma:2b",
    "mistral": "mistral",
}
