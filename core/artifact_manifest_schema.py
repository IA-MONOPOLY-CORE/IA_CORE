"""Contrato de inventario y trazabilidad de artefactos sandbox."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.artifact_state import coerce_artifact_state


ARTIFACT_MANIFEST_VERSION = "1.0"

ALLOWED_ARTIFACT_TYPES = {
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "memory",
    "model_recommendation",
}

REQUIRED_MANIFEST_FIELDS = {
    "artifact_manifest_version",
    "domain_id",
    "artifacts",
}

REQUIRED_ARTIFACT_FIELDS = {
    "artifact_id",
    "artifact_type",
    "name",
    "version",
    "status",
    "created_from",
    "created_by",
    "dependencies",
    "created_at",
    "updated_at",
    "rollback_info",
}

REQUIRED_ROLLBACK_FIELDS = {
    "created_paths",
    "depends_on",
    "safe_remove",
}


def validate_artifact_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Valida un artifact_manifest sin crear artefactos ni escribir archivos."""
    if not isinstance(manifest, dict):
        raise ValueError("artifact_manifest debe ser un objeto")
    missing = REQUIRED_MANIFEST_FIELDS - set(manifest)
    if missing:
        raise ValueError(f"artifact_manifest incompleto: {', '.join(sorted(missing))}")
    if manifest.get("artifact_manifest_version") != ARTIFACT_MANIFEST_VERSION:
        raise ValueError("artifact_manifest_version invalida")
    _validate_id(manifest.get("domain_id"), "domain_id")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("artifacts debe ser una lista")
    _ensure_json_serializable(manifest)

    validated = deepcopy(manifest)
    artifact_ids: set[str] = set()
    for artifact in artifacts:
        _validate_artifact_shape(artifact)
        artifact_id = artifact["artifact_id"]
        if artifact_id in artifact_ids:
            raise ValueError(f"artifact_id duplicado: {artifact_id}")
        artifact_ids.add(artifact_id)

    for artifact in artifacts:
        _validate_dependencies(artifact, artifact_ids)
        _validate_rollback_info(artifact, artifact_ids)

    return validated


def validate_artifact_manifest_file(path: str | Path) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"artifact_manifest no es JSON valido: {exc}") from exc
    return validate_artifact_manifest(data)


def empty_artifact_manifest(domain_id: str) -> dict[str, Any]:
    _validate_id(domain_id, "domain_id")
    return {
        "artifact_manifest_version": ARTIFACT_MANIFEST_VERSION,
        "domain_id": domain_id,
        "artifacts": [],
    }


def _validate_artifact_shape(artifact: Any) -> None:
    if not isinstance(artifact, dict):
        raise ValueError("cada artefacto debe ser un objeto")
    missing = REQUIRED_ARTIFACT_FIELDS - set(artifact)
    if missing:
        raise ValueError(f"artefacto incompleto: {', '.join(sorted(missing))}")
    _validate_id(artifact.get("artifact_id"), "artifact_id")
    if artifact.get("artifact_type") not in ALLOWED_ARTIFACT_TYPES:
        raise ValueError(f"artifact_type invalido: {artifact.get('artifact_type')}")
    _validate_non_empty_text(artifact.get("name"), "name")
    _validate_non_empty_text(artifact.get("version"), "version")
    if coerce_artifact_state(artifact.get("status")) is None:
        raise ValueError(f"status de artefacto invalido: {artifact.get('status')}")
    if not isinstance(artifact.get("created_from"), dict) or not artifact["created_from"]:
        raise ValueError("created_from debe ser un objeto no vacio")
    _validate_non_empty_text(artifact.get("created_by"), "created_by")
    if not isinstance(artifact.get("dependencies"), list):
        raise ValueError("dependencies debe ser una lista")
    _validate_non_empty_text(artifact.get("created_at"), "created_at")
    _validate_non_empty_text(artifact.get("updated_at"), "updated_at")


def _validate_dependencies(artifact: dict[str, Any], artifact_ids: set[str]) -> None:
    for dependency in artifact["dependencies"]:
        if not isinstance(dependency, str) or not dependency.strip():
            raise ValueError("dependencies debe contener artifact_id validos")
        if dependency not in artifact_ids:
            raise ValueError(f"dependencia inexistente: {dependency}")
        if dependency == artifact["artifact_id"]:
            raise ValueError("un artefacto no puede depender de si mismo")


def _validate_rollback_info(artifact: dict[str, Any], artifact_ids: set[str]) -> None:
    rollback = artifact.get("rollback_info")
    if not isinstance(rollback, dict):
        raise ValueError("rollback_info debe estar presente como objeto")
    missing = REQUIRED_ROLLBACK_FIELDS - set(rollback)
    if missing:
        raise ValueError(f"rollback_info incompleto: {', '.join(sorted(missing))}")
    if not isinstance(rollback.get("created_paths"), list):
        raise ValueError("rollback_info.created_paths debe ser una lista")
    if not isinstance(rollback.get("depends_on"), list):
        raise ValueError("rollback_info.depends_on debe ser una lista")
    if not isinstance(rollback.get("safe_remove"), bool):
        raise ValueError("rollback_info.safe_remove debe ser booleano")
    for dependency in rollback["depends_on"]:
        if dependency not in artifact_ids:
            raise ValueError(f"rollback_info depende de artefacto inexistente: {dependency}")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(manifest: dict[str, Any]) -> None:
    try:
        json.dumps(manifest, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("artifact_manifest debe ser serializable como JSON") from exc
