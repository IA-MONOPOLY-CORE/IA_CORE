"""Normalizacion y deteccion de dominios duplicados/equivalentes."""

from __future__ import annotations

import re
import unicodedata
from itertools import combinations
from typing import Any


DUPLICATE_DOMAIN_ERROR = (
    "Ya existe un dominio equivalente. No se pueden crear dominios duplicados. "
    "Revisa el dominio existente o usa otro nombre/nicho."
)

_CONNECTOR_WORDS = {
    "a",
    "al",
    "de",
    "del",
    "el",
    "en",
    "la",
    "las",
    "los",
    "para",
    "por",
    "y",
}
_COSMETIC_DOMAIN_TOKENS = {
    "ia",
    "core",
    "iacore",
    "dominio",
    "framework",
}
_LOTTERY_TOKENS = {
    "azar",
    "combinatorio",
    "combinatoria",
    "juego",
    "juegos",
    "loteria",
    "sorteo",
    "sorteos",
}


def normalize_domain_name(value: str | None) -> str:
    """Normaliza texto visible de dominio para comparaciones estables."""
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value).strip())
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii").lower()
    ascii_name = ascii_name.replace("ia_core", "iacore")
    tokens = re.findall(r"[a-z0-9]+", ascii_name)
    meaningful = [
        token
        for token in tokens
        if token not in _CONNECTOR_WORDS and token not in _COSMETIC_DOMAIN_TOKENS
    ]
    return " ".join(meaningful)


def normalize_domain_slug(value: str | None) -> str:
    normalized = normalize_domain_name(value)
    return re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")


def _text_tokens(value: str | None) -> set[str]:
    return set(normalize_domain_name(value).split())


def _is_lottery_equivalent(record: dict[str, Any]) -> bool:
    fields = [
        record.get("id"),
        record.get("nombre"),
        record.get("descripcion"),
        record.get("instrucciones"),
        record.get("nicho_sugerido"),
        record.get("nicho_id"),
    ]
    tokens: set[str] = set()
    for field in fields:
        tokens.update(_text_tokens(str(field) if field is not None else ""))
    return "loteria" in tokens or (
        "analisis" in tokens and bool(tokens & _LOTTERY_TOKENS)
    )


def domain_identity_keys(record: dict[str, Any]) -> set[str]:
    """Devuelve claves de identidad conceptual para detectar duplicados."""
    keys: set[str] = set()
    for field in ("id", "slug", "nombre"):
        value = record.get(field)
        if value:
            slug = normalize_domain_slug(str(value))
            if slug:
                keys.add(f"{field}:{slug}")
                keys.add(f"slug:{slug}")

    area_id = record.get("area_profesional_id")
    niche_id = record.get("nicho_id")
    if area_id and niche_id:
        keys.add(f"catalog:{normalize_domain_slug(str(area_id))}:{normalize_domain_slug(str(niche_id))}")

    for alias in record.get("aliases", []) or []:
        slug = normalize_domain_slug(str(alias))
        if slug:
            keys.add(f"alias:{slug}")
            keys.add(f"slug:{slug}")

    if _is_lottery_equivalent(record):
        keys.add("concept:loteria_juegos_azar")

    return keys


def domains_are_equivalent(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return bool(domain_identity_keys(first) & domain_identity_keys(second))


def validate_unique_domain(
    candidate: dict[str, Any],
    existing_domains: list[dict[str, Any]],
) -> None:
    for existing in existing_domains:
        if domains_are_equivalent(candidate, existing):
            existing_name = existing.get("nombre") or existing.get("id") or "dominio existente"
            raise ValueError(f"{DUPLICATE_DOMAIN_ERROR} Conflicto: {existing_name}.")


def detect_duplicate_domains(domains: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    for first, second in combinations(domains, 2):
        shared = sorted(domain_identity_keys(first) & domain_identity_keys(second))
        if shared:
            conflicts.append(
                {
                    "domain_a": first.get("id"),
                    "domain_b": second.get("id"),
                    "nombre_a": first.get("nombre"),
                    "nombre_b": second.get("nombre"),
                    "shared_keys": shared,
                }
            )
    return conflicts
