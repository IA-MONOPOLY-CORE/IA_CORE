"""Validacion end-to-end y regeneracion segura del ciclo sandbox."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.domain_materialization_preview import validate_domain_materialization_preview
from core.domain_materialization_rollback import rollback_domain_materialization
from core.domain_materializer import (
    MATERIALIZATION_MANIFEST,
    materialize_sandbox_domain,
    validate_materialized_sandbox_domain,
)
from core.sandbox_domain_schema import validate_sandbox_domain_schema


def validate_sandbox_lifecycle(
    *,
    preview: dict[str, Any],
    domain_schema: dict[str, Any],
    sandbox_root: str | Path,
    execution_metadata: dict[str, Any] | None = None,
    cleanup: bool = True,
) -> dict[str, Any]:
    """Ejecuta y valida el ciclo preview -> materializacion -> rollback."""
    validated_preview = validate_domain_materialization_preview(preview)
    validated_schema = validate_sandbox_domain_schema(domain_schema)
    _validate_traceable_origin(validated_preview, validated_schema)

    materialized = materialize_sandbox_domain(
        validated_schema,
        sandbox_root=sandbox_root,
        execution_metadata={
            "lifecycle_validation": True,
            **(execution_metadata or {}),
        },
    )
    post_validation = validate_materialized_sandbox_domain(materialized["domain_dir"])

    result: dict[str, Any] = {
        "success": True,
        "preview_id": validated_preview["preview_id"],
        "domain_id": materialized["domain_id"],
        "materialization": materialized,
        "post_validation": post_validation,
        "rollback": None,
        "clean": False,
    }
    if cleanup:
        rollback = rollback_domain_materialization(manifest_path=materialized["manifest_path"])
        result["rollback"] = rollback
        result["clean"] = not Path(materialized["domain_dir"]).exists()
    return result


def regenerate_sandbox_domain(
    domain_schema: dict[str, Any],
    *,
    sandbox_root: str | Path,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Regenera un sandbox existente con rollback previo y nuevo materialization_id."""
    root = Path(sandbox_root).resolve()
    validated_schema = validate_sandbox_domain_schema(domain_schema)
    domain_dir = (root / validated_schema["domain_id"]).resolve()
    previous_manifest: dict[str, Any] | None = None
    rollback_result: dict[str, Any] | None = None

    manifest_path = domain_dir / MATERIALIZATION_MANIFEST
    if domain_dir.exists():
        if not manifest_path.exists():
            raise FileNotFoundError("No se puede regenerar sandbox sin manifest")
        previous_manifest = _load_manifest(manifest_path)
        rollback_result = rollback_domain_materialization(manifest_path=manifest_path)
    elif manifest_path.exists():
        previous_manifest = _load_manifest(manifest_path)
        rollback_result = rollback_domain_materialization(manifest_path=manifest_path)

    previous_id = previous_manifest.get("materialization_id") if previous_manifest else None
    generation_number = int(previous_manifest.get("generation_number", 1)) + 1 if previous_manifest else 1
    history = _history_from_previous(previous_manifest, rollback_result)

    regenerated = materialize_sandbox_domain(
        validated_schema,
        sandbox_root=root,
        execution_metadata={
            "regeneration": True,
            **(execution_metadata or {}),
        },
        previous_materialization_id=previous_id,
        generation_number=generation_number,
        lifecycle_history=history,
    )
    post_validation = validate_materialized_sandbox_domain(regenerated["domain_dir"])
    return {
        "success": True,
        "domain_id": regenerated["domain_id"],
        "previous_materialization_id": previous_id,
        "materialization_id": regenerated["materialization_id"],
        "generation_number": generation_number,
        "rollback": rollback_result,
        "materialization": regenerated,
        "post_validation": post_validation,
        "history": post_validation["manifest"].get("lifecycle_history", []),
    }


def _validate_traceable_origin(preview: dict[str, Any], domain_schema: dict[str, Any]) -> None:
    source_request = domain_schema.get("source_request")
    if source_request != preview.get("domain_request"):
        raise ValueError("source_request no coincide con domain_request del preview")
    created_from = domain_schema.get("created_from", {})
    if created_from.get("type") == "preview" and created_from.get("preview_id") != preview.get("preview_id"):
        raise ValueError("created_from.preview_id no coincide con preview")


def _load_manifest(manifest_path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Manifest corrupto para regeneracion: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ValueError("Manifest de regeneracion debe ser un objeto")
    return manifest


def _history_from_previous(
    previous_manifest: dict[str, Any] | None,
    rollback_result: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if previous_manifest is None:
        return []
    history = deepcopy(previous_manifest.get("lifecycle_history", []))
    if rollback_result:
        history.append(
            {
                "event": "rolled_back",
                "materialization_id": rollback_result.get("materialization_id"),
                "domain_id": rollback_result.get("domain_id"),
                "status": rollback_result.get("status"),
            }
        )
    return history
