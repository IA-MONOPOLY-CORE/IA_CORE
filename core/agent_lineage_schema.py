"""Contrato de lineage para agentes sandbox."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any

from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID
from core.profile_catalog_materializer import PROFILE_CATALOG_ARTIFACT_ID
from core.sandbox_agent_schema import SANDBOX_AGENT_REQUIRED_DEPENDENCIES


AGENT_LINEAGE_SCHEMA_VERSION = "1.0"
REQUIRED_FIELDS = {
    "schema_version",
    "agent_id",
    "domain_id",
    "origin",
    "current_version",
    "history",
    "related_artifacts",
    "replaced_by",
    "created_at",
    "updated_at",
}
REQUIRED_ORIGIN_FIELDS = {
    "profile_catalog_artifact_id",
    "source_profile_id",
    "agent_presets_artifact_id",
    "preset_id",
    "paper_seed_artifact_id",
    "paper_seed_id",
}
ALLOWED_EVENTS = {
    "created",
    "materialized",
    "regenerated",
    "updated",
    "archived",
    "replaced",
    "rolled_back",
}


def build_agent_lineage(
    *,
    agent_id: str,
    domain_id: str,
    origin: dict[str, Any],
    current_version: str = "1.0.0",
    history: list[dict[str, Any]] | None = None,
    related_artifacts: dict[str, str] | None = None,
    replaced_by: str | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye lineage sin crear ni materializar agentes."""
    now = _now()
    payload = {
        "schema_version": AGENT_LINEAGE_SCHEMA_VERSION,
        "agent_id": agent_id,
        "domain_id": domain_id,
        "origin": deepcopy(origin),
        "current_version": current_version,
        "history": deepcopy(history) if history is not None else [
            {
                "event": "created",
                "version": current_version,
                "at": created_at or now,
                "details": "Contrato de lineage creado para agente sandbox.",
            }
        ],
        "related_artifacts": deepcopy(related_artifacts)
        if related_artifacts is not None
        else {
            "profile_catalog": PROFILE_CATALOG_ARTIFACT_ID,
            "agent_presets": AGENT_PRESETS_ARTIFACT_ID,
            "paper_seed": PAPER_SEED_ARTIFACT_ID,
        },
        "replaced_by": replaced_by,
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_agent_lineage(payload)


def validate_agent_lineage(lineage: dict[str, Any]) -> dict[str, Any]:
    """Valida lineage de agente sandbox sin escribir artefactos operativos."""
    if not isinstance(lineage, dict):
        raise ValueError("agent_lineage debe ser un objeto")
    missing = REQUIRED_FIELDS - set(lineage)
    if missing:
        raise ValueError(f"agent_lineage incompleto: {', '.join(sorted(missing))}")
    if lineage.get("schema_version") != AGENT_LINEAGE_SCHEMA_VERSION:
        raise ValueError("schema_version de agent_lineage invalida")
    _validate_id(lineage.get("agent_id"), "agent_id")
    _validate_id(lineage.get("domain_id"), "domain_id")
    _validate_origin(lineage.get("origin"))
    _validate_version(lineage.get("current_version"))
    _validate_history(lineage.get("history"), current_version=lineage["current_version"])
    _validate_related_artifacts(lineage.get("related_artifacts"))
    replaced_by = lineage.get("replaced_by")
    if replaced_by is not None:
        _validate_id(replaced_by, "replaced_by")
        if replaced_by == lineage["agent_id"]:
            raise ValueError("replaced_by no puede apuntar al mismo agent_id")
    _validate_non_empty_text(lineage.get("created_at"), "created_at")
    _validate_non_empty_text(lineage.get("updated_at"), "updated_at")
    _ensure_json_serializable(lineage)
    return deepcopy(lineage)


def lineage_to_artifact_manifest_metadata(lineage: dict[str, Any]) -> dict[str, Any]:
    """Devuelve metadata de lineage para embeber en el futuro artefacto `agent`."""
    validated = validate_agent_lineage(lineage)
    return {
        "agent_id": validated["agent_id"],
        "domain_id": validated["domain_id"],
        "lineage_schema": "core.agent_lineage_schema",
        "origin": deepcopy(validated["origin"]),
        "current_version": validated["current_version"],
        "related_artifacts": deepcopy(validated["related_artifacts"]),
        "replaced_by": validated["replaced_by"],
        "history_event_count": len(validated["history"]),
        "dependencies": list(SANDBOX_AGENT_REQUIRED_DEPENDENCIES),
    }


def _validate_origin(origin: Any) -> None:
    if not isinstance(origin, dict):
        raise ValueError("origin debe ser un objeto")
    missing = REQUIRED_ORIGIN_FIELDS - set(origin)
    if missing:
        raise ValueError(f"origin incompleto: {', '.join(sorted(missing))}")
    if origin["profile_catalog_artifact_id"] != PROFILE_CATALOG_ARTIFACT_ID:
        raise ValueError("origin.profile_catalog_artifact_id invalido")
    if origin["agent_presets_artifact_id"] != AGENT_PRESETS_ARTIFACT_ID:
        raise ValueError("origin.agent_presets_artifact_id invalido")
    if origin["paper_seed_artifact_id"] != PAPER_SEED_ARTIFACT_ID:
        raise ValueError("origin.paper_seed_artifact_id invalido")
    for field in ["source_profile_id", "preset_id", "paper_seed_id"]:
        _validate_non_empty_text(origin[field], f"origin.{field}")


def _validate_history(history: Any, *, current_version: str) -> None:
    if not isinstance(history, list) or not history:
        raise ValueError("history debe ser una lista no vacia")
    versions = set()
    for event in history:
        if not isinstance(event, dict):
            raise ValueError("history debe contener objetos")
        if event.get("event") not in ALLOWED_EVENTS:
            raise ValueError(f"history.event invalido: {event.get('event')}")
        _validate_version(event.get("version"))
        _validate_non_empty_text(event.get("at"), "history.at")
        versions.add(event["version"])
    if current_version not in versions:
        raise ValueError("history debe contener current_version")


def _validate_related_artifacts(related: Any) -> None:
    if not isinstance(related, dict):
        raise ValueError("related_artifacts debe ser un objeto")
    expected = {
        "profile_catalog": PROFILE_CATALOG_ARTIFACT_ID,
        "agent_presets": AGENT_PRESETS_ARTIFACT_ID,
        "paper_seed": PAPER_SEED_ARTIFACT_ID,
    }
    for key, artifact_id in expected.items():
        if related.get(key) != artifact_id:
            raise ValueError(f"related_artifacts.{key} invalido")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_version(value: Any) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("version debe usar formato semver simple")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(lineage: dict[str, Any]) -> None:
    try:
        json.dumps(lineage, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("agent_lineage debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
