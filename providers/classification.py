"""Clasificación de proveedores para la UI (sin llamadas de red)."""

from __future__ import annotations

from providers.base import BaseProvider

KIND_LOCAL_ACTIVE = "LOCAL_ACTIVE"
KIND_CLOUD_CONFIGURED = "CLOUD_CONFIGURED"
KIND_CLOUD_PLACEHOLDER = "CLOUD_PLACEHOLDER"
KIND_OFFLINE = "OFFLINE"


def classify_provider(provider: BaseProvider) -> dict[str, str]:
    name = provider.provider_name()
    is_placeholder = getattr(provider, "IS_PLACEHOLDER", False)
    is_local = name == "ollama" or getattr(provider, "IS_LOCAL", False)

    if is_local:
        kind = KIND_LOCAL_ACTIVE
        origin = "local"
    elif is_placeholder:
        kind = KIND_CLOUD_PLACEHOLDER
        origin = "cloud"
    else:
        kind = KIND_CLOUD_CONFIGURED
        origin = "cloud"

    return {
        "kind": kind,
        "origin": origin,
        "display_kind": kind,
    }
