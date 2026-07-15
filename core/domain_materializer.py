"""Materializacion controlada de dominios sandbox."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.artifact_state import ArtifactState
from core.domain_identity import validate_unique_domain
from core.domain_registry import list_domains
from core.domain_state import DomainState
from core.sandbox_domain_schema import validate_sandbox_domain_file, validate_sandbox_domain_schema


MATERIALIZATION_MANIFEST = "materialization_manifest.json"
MATERIALIZATION_SCHEMA_VERSION = "1.0"


def materialize_sandbox_domain(
    domain_schema: dict[str, Any],
    *,
    sandbox_root: str | Path,
    execution_metadata: dict[str, Any] | None = None,
    previous_materialization_id: str | None = None,
    generation_number: int = 1,
    lifecycle_history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Materializa un dominio sandbox en una raiz temporal/controlada."""
    root = _safe_sandbox_root(sandbox_root)

    existing_domains = [
        *list_domains(include_internal=True),
        *_load_existing_sandbox_records(root),
    ]
    validated = validate_sandbox_domain_schema(
        domain_schema,
        existing_domains=existing_domains,
    )
    _reject_legacy_candidate(validated)

    domain_id = validated["domain_id"]
    domain_dir = _safe_domain_dir(root, domain_id)
    if domain_dir.exists():
        raise FileExistsError(f"Ya existe sandbox materializado: {domain_id}")

    materialization_id = _materialization_id(validated, execution_metadata or {})
    materialized_at = _now()
    domain_payload = _build_materialized_domain_payload(
        validated,
        materialization_id=materialization_id,
        materialized_at=materialized_at,
        domain_dir=domain_dir,
    )
    validate_sandbox_domain_schema(
        domain_payload,
        existing_domains=existing_domains,
    )

    manifest = _build_manifest(
        domain_payload,
        materialization_id=materialization_id,
        previous_materialization_id=previous_materialization_id,
        generation_number=generation_number,
        materialized_at=materialized_at,
        domain_dir=domain_dir,
        execution_metadata=execution_metadata or {},
        lifecycle_history=lifecycle_history or [],
    )

    domain_dir.mkdir(parents=True, exist_ok=False)
    domain_path = domain_dir / "domain.json"
    manifest_path = domain_dir / MATERIALIZATION_MANIFEST
    domain_path.write_text(
        json.dumps(domain_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    validation = validate_materialized_sandbox_domain(domain_dir)
    return {
        "success": True,
        "domain_id": domain_id,
        "materialization_id": materialization_id,
        "domain_dir": str(domain_dir),
        "domain_json_path": str(domain_path),
        "manifest_path": str(manifest_path),
        "domain": validation["domain"],
        "manifest": validation["manifest"],
    }


def validate_materialized_sandbox_domain(domain_dir: str | Path) -> dict[str, Any]:
    """Valida estructura post-materializacion sin activar el dominio."""
    target = Path(domain_dir).resolve()
    domain_path = target / "domain.json"
    manifest_path = target / MATERIALIZATION_MANIFEST
    if not target.is_dir():
        raise FileNotFoundError(f"Sandbox no encontrado: {target}")
    if not domain_path.is_file():
        raise FileNotFoundError("Sandbox materializado sin domain.json")
    if not manifest_path.is_file():
        raise FileNotFoundError("Sandbox materializado sin manifest de materializacion")

    domain = validate_sandbox_domain_file(domain_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("materialization_manifest.json debe ser un objeto")
    if manifest.get("schema_version") != MATERIALIZATION_SCHEMA_VERSION:
        raise ValueError("materialization_manifest.json tiene schema_version invalida")
    if manifest.get("domain_id") != domain["domain_id"]:
        raise ValueError("materialization_manifest.json no coincide con domain_id")
    if manifest.get("materialization_id") != domain["materialization_id"]:
        raise ValueError("materialization_manifest.json no coincide con materialization_id")
    if domain.get("status") == DomainState.ACTIVE.value:
        raise ValueError("Sandbox materializado no puede estar active")
    if domain.get("artifact_state") == ArtifactState.ACTIVE.value:
        raise ValueError("Sandbox materializado no puede tener artifact_state active")
    if not domain.get("rollback_manifest"):
        raise ValueError("Sandbox materializado sin rollback_manifest")
    if not manifest.get("created_paths"):
        raise ValueError("Manifest de materializacion sin paths creados")
    return {
        "success": True,
        "domain": domain,
        "manifest": manifest,
        "domain_json_path": str(domain_path),
        "manifest_path": str(manifest_path),
    }


def _safe_sandbox_root(sandbox_root: str | Path) -> Path:
    root = Path(sandbox_root).resolve()
    domains_root = Path(config.DOMAINS_DIR).resolve()
    if root == domains_root or domains_root in root.parents:
        raise ValueError("La materializacion sandbox no puede escribir en domains/ operativo")
    return root


def _safe_domain_dir(root: Path, domain_id: str) -> Path:
    target = (root / domain_id).resolve()
    if target.parent != root:
        raise ValueError("Ruta de sandbox invalida")
    domains_root = Path(config.DOMAINS_DIR).resolve()
    if target == domains_root or domains_root in target.parents:
        raise ValueError("La materializacion sandbox no puede escribir en domains/ operativo")
    return target


def _load_existing_sandbox_records(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    records: list[dict[str, Any]] = []
    for manifest_path in sorted(root.glob("*/domain.json")):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                records.append(
                    {
                        "id": data.get("domain_id") or data.get("id"),
                        "nombre": data.get("name") or data.get("nombre"),
                        "descripcion": data.get("description") or data.get("descripcion"),
                        "nicho_id": data.get("source_request", {}).get("niche_id"),
                    }
                )
        except (OSError, json.JSONDecodeError):
            continue
    return records


def _reject_legacy_candidate(domain: dict[str, Any]) -> None:
    validate_unique_domain(
        {
            "id": domain["domain_id"],
            "nombre": domain["name"],
            "descripcion": domain["description"],
        },
        list_domains(include_internal=True),
    )


def _build_materialized_domain_payload(
    domain: dict[str, Any],
    *,
    materialization_id: str,
    materialized_at: str,
    domain_dir: Path,
) -> dict[str, Any]:
    payload = deepcopy(domain)
    created_paths = [
        str(domain_dir),
        str(domain_dir / "domain.json"),
        str(domain_dir / MATERIALIZATION_MANIFEST),
    ]
    payload["materialization_id"] = materialization_id
    payload["materialization_status"] = "materialized"
    payload["status"] = DomainState.MATERIALIZED.value
    payload["artifact_state"] = ArtifactState.MATERIALIZED.value
    payload["updated_at"] = materialized_at
    payload["human_review_required"] = True
    rollback = deepcopy(payload["rollback_manifest"])
    rollback["created_paths"] = created_paths
    rollback.setdefault("modified_paths", [])
    rollback.setdefault("backup_paths", [])
    rollback.setdefault("notes", [])
    rollback["notes"].append("Rollback real queda diferido a una fase posterior.")
    payload["rollback_manifest"] = rollback
    payload.setdefault("metadata", {})
    payload["metadata"] = {
        **payload["metadata"],
        "materialized_by": "core.domain_materializer.materialize_sandbox_domain",
        "operational": False,
    }
    payload.setdefault("validation", {})
    payload["validation"] = {
        **payload["validation"],
        "validated": True,
        "passed": False,
        "post_materialization_required": True,
    }
    return payload


def _build_manifest(
    domain: dict[str, Any],
    *,
    materialization_id: str,
    previous_materialization_id: str | None,
    generation_number: int,
    materialized_at: str,
    domain_dir: Path,
    execution_metadata: dict[str, Any],
    lifecycle_history: list[dict[str, Any]],
) -> dict[str, Any]:
    created_paths = list(domain["rollback_manifest"]["created_paths"])
    history = [
        *deepcopy(lifecycle_history),
        {
            "event": "materialized",
            "materialization_id": materialization_id,
            "previous_materialization_id": previous_materialization_id,
            "generation_number": generation_number,
            "at": materialized_at,
        },
    ]
    return {
        "schema_version": MATERIALIZATION_SCHEMA_VERSION,
        "materialization_id": materialization_id,
        "previous_materialization_id": previous_materialization_id,
        "generation_number": generation_number,
        "domain_id": domain["domain_id"],
        "domain_type": domain["domain_type"],
        "status": domain["status"],
        "artifact_state": domain["artifact_state"],
        "materialized_at": materialized_at,
        "target_path": str(domain_dir),
        "created_paths": created_paths,
        "modified_paths": list(domain["rollback_manifest"]["modified_paths"]),
        "backup_paths": list(domain["rollback_manifest"]["backup_paths"]),
        "rollback_manifest": deepcopy(domain["rollback_manifest"]),
        "execution_metadata": deepcopy(execution_metadata),
        "lifecycle_history": history,
        "post_validation": {
            "required": True,
            "passed": False,
        },
    }


def _materialization_id(domain: dict[str, Any], execution_metadata: dict[str, Any]) -> str:
    seed = json.dumps(
        {
            "domain_id": domain["domain_id"],
            "source_request": domain["source_request"],
            "created_from": domain["created_from"],
            "execution_metadata": execution_metadata,
            "created_at": _now(),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"mat_{domain['domain_id']}_{digest}"


def _now() -> str:
    return datetime.now().isoformat()
