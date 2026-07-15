"""Materializacion sandbox de profile_catalog como artefacto interno."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.artifact_manifest_schema import (
    empty_artifact_manifest,
    validate_artifact_manifest,
    validate_artifact_manifest_file,
)
from core.artifact_state import ArtifactState
from core.domain_materializer import MATERIALIZATION_MANIFEST, validate_materialized_sandbox_domain
from core.professional_profile_catalog_generator import generate_profile_catalog_for_domain


ARTIFACT_MANIFEST_RELATIVE_PATH = Path("manifests") / "artifact_manifest.json"
PROFILE_CATALOG_RELATIVE_PATH = Path("profile_catalog") / "profile_catalog.json"
PROFILE_CATALOG_ARTIFACT_ID = "profile_catalog_main"
CREATED_BY = "core.profile_catalog_materializer.materialize_profile_catalog"


def materialize_profile_catalog(
    domain_dir: str | Path,
    *,
    regenerate: bool = False,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materializa `profile_catalog` dentro de un dominio sandbox existente."""
    target = Path(domain_dir).resolve()
    _reject_operational_domains_path(target)

    validation = validate_materialized_sandbox_domain(target)
    domain = validation["domain"]
    materialization_manifest = validation["manifest"]
    domain_id = domain["domain_id"]

    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    profile_catalog_path = _safe_child(target, PROFILE_CATALOG_RELATIVE_PATH)
    artifact_manifest = _load_or_create_artifact_manifest(manifest_path, domain_id)
    existing_index = _find_profile_catalog_index(artifact_manifest)
    if existing_index is not None and not regenerate:
        raise FileExistsError(
            "profile_catalog ya existe en este sandbox; use regenerate=True para versionar"
        )

    now = _now()
    profile_catalog = _build_profile_catalog(domain)
    created_paths = [
        str(profile_catalog_path.parent),
        str(profile_catalog_path),
        str(manifest_path.parent),
        str(manifest_path),
    ]
    previous_version = None
    history_entry = None
    version = "1.0.0"

    if existing_index is not None:
        existing_artifact = artifact_manifest["artifacts"][existing_index]
        previous_version = existing_artifact["version"]
        version = _next_patch_version(previous_version)
        history_path = _archive_current_profile_catalog(
            target,
            profile_catalog_path,
            previous_version=previous_version,
        )
        created_paths.append(str(history_path))
        history_entry = {
            "event": "regenerated",
            "previous_version": previous_version,
            "new_version": version,
            "archived_profile_catalog_path": str(history_path),
            "at": now,
        }
    elif profile_catalog_path.exists():
        raise FileExistsError("profile_catalog.json existe sin artifact_manifest coherente")

    profile_catalog_path.parent.mkdir(parents=True, exist_ok=True)
    profile_catalog_payload = _build_profile_catalog_payload(
        profile_catalog,
        domain=domain,
        version=version,
        created_at=now,
        regenerated_from=previous_version,
    )
    profile_catalog_path.write_text(
        json.dumps(profile_catalog_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    artifact = _build_artifact_record(
        domain=domain,
        version=version,
        created_at=now,
        created_paths=created_paths,
        execution_metadata=execution_metadata or {},
        previous=artifact_manifest["artifacts"][existing_index] if existing_index is not None else None,
        history_entry=history_entry,
    )
    if existing_index is None:
        artifact_manifest["artifacts"].append(artifact)
    else:
        artifact_manifest["artifacts"][existing_index] = artifact

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_manifest = validate_artifact_manifest(artifact_manifest)
    manifest_path.write_text(
        json.dumps(artifact_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    updated_materialization_manifest = _extend_materialization_manifest(
        validation["manifest_path"],
        materialization_manifest,
        created_paths,
    )

    return {
        "success": True,
        "domain_id": domain_id,
        "artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
        "artifact_type": "profile_catalog",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "regenerated": existing_index is not None,
        "profile_catalog_path": str(profile_catalog_path),
        "artifact_manifest_path": str(manifest_path),
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "materialization_manifest": updated_materialization_manifest,
    }


def validate_materialized_profile_catalog(domain_dir: str | Path) -> dict[str, Any]:
    """Valida que el sandbox contenga un profile_catalog trazado y no activo."""
    target = Path(domain_dir).resolve()
    validation = validate_materialized_sandbox_domain(target)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    profile_catalog_path = _safe_child(target, PROFILE_CATALOG_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    index = _find_profile_catalog_index(artifact_manifest)
    if index is None:
        raise FileNotFoundError("artifact_manifest sin profile_catalog")
    artifact = artifact_manifest["artifacts"][index]
    if artifact["status"] == ArtifactState.ACTIVE.value:
        raise ValueError("profile_catalog sandbox no puede estar active")
    if not profile_catalog_path.is_file():
        raise FileNotFoundError("profile_catalog registrado sin archivo materializado")
    payload = json.loads(profile_catalog_path.read_text(encoding="utf-8"))
    if payload.get("sandbox_artifact", {}).get("artifact_id") != artifact["artifact_id"]:
        raise ValueError("profile_catalog.json no coincide con artifact_manifest")
    return {
        "success": True,
        "domain": validation["domain"],
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "profile_catalog": payload,
        "profile_catalog_path": str(profile_catalog_path),
        "artifact_manifest_path": str(manifest_path),
    }


def _build_profile_catalog(domain: dict[str, Any]) -> dict[str, Any]:
    request = dict(domain.get("source_request") or {})
    area_id = request.get("area_id")
    niche_ids = _request_niche_ids(request)
    if not area_id:
        raise ValueError("source_request.area_id requerido para generar profile_catalog")
    return generate_profile_catalog_for_domain(
        area_id=area_id,
        niche_ids=niche_ids,
        domain_id=domain["domain_id"],
        business_scale=request.get("business_scale"),
        required_capabilities=request.get("required_capabilities"),
        model_policy_preferences=request.get("model_policy_preferences"),
        complexity=request.get("complexity_level") or request.get("complexity"),
        max_profiles=request.get("max_profiles"),
    )


def _request_niche_ids(request: dict[str, Any]) -> list[str]:
    if isinstance(request.get("niche_ids"), list):
        return [item for item in request["niche_ids"] if isinstance(item, str) and item.strip()]
    niche_id = request.get("niche_id")
    return [niche_id] if isinstance(niche_id, str) and niche_id.strip() else []


def _build_profile_catalog_payload(
    profile_catalog: dict[str, Any],
    *,
    domain: dict[str, Any],
    version: str,
    created_at: str,
    regenerated_from: str | None,
) -> dict[str, Any]:
    payload = deepcopy(profile_catalog)
    payload["sandbox_artifact"] = {
        "artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
        "artifact_type": "profile_catalog",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "operational": False,
        "active": False,
        "domain_id": domain["domain_id"],
        "materialization_id": domain["materialization_id"],
        "created_at": created_at,
        "regenerated_from": regenerated_from,
    }
    return payload


def _build_artifact_record(
    *,
    domain: dict[str, Any],
    version: str,
    created_at: str,
    created_paths: list[str],
    execution_metadata: dict[str, Any],
    previous: dict[str, Any] | None,
    history_entry: dict[str, Any] | None,
) -> dict[str, Any]:
    history = list(previous.get("history", [])) if previous else []
    if history_entry:
        history.append(history_entry)
    all_created_paths = _dedupe(
        [*(previous or {}).get("rollback_info", {}).get("created_paths", []), *created_paths]
    )
    artifact = {
        "artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
        "artifact_type": "profile_catalog",
        "name": "Profile Catalog Main",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "created_from": {
            "source_type": "sandbox_materialized_domain",
            "domain_id": domain["domain_id"],
            "materialization_id": domain["materialization_id"],
            "domain_source_request": deepcopy(domain.get("source_request", {})),
            "generator": (
                "core.professional_profile_catalog_generator."
                "generate_profile_catalog_for_domain"
            ),
            "global_sources": [
                "catalogs/professional_profiles.json",
                "catalogs/areas.json",
                "catalogs/niches.json",
                "catalogs/profile_model_policies.json",
            ],
            "execution_metadata": deepcopy(execution_metadata),
        },
        "created_by": CREATED_BY,
        "dependencies": [],
        "created_at": previous.get("created_at", created_at) if previous else created_at,
        "updated_at": created_at,
        "rollback_info": {
            "created_paths": all_created_paths,
            "depends_on": [],
            "safe_remove": True,
        },
        "history": history,
        "operational": False,
        "passed": False,
    }
    return artifact


def _load_or_create_artifact_manifest(path: Path, domain_id: str) -> dict[str, Any]:
    if not path.exists():
        return empty_artifact_manifest(domain_id)
    manifest = validate_artifact_manifest_file(path)
    if manifest["domain_id"] != domain_id:
        raise ValueError("artifact_manifest no coincide con domain_id del sandbox")
    return manifest


def _find_profile_catalog_index(manifest: dict[str, Any]) -> int | None:
    indexes = [
        index
        for index, artifact in enumerate(manifest.get("artifacts", []))
        if artifact.get("artifact_type") == "profile_catalog"
    ]
    if len(indexes) > 1:
        raise ValueError("artifact_manifest contiene multiples profile_catalog")
    return indexes[0] if indexes else None


def _archive_current_profile_catalog(
    domain_dir: Path,
    profile_catalog_path: Path,
    *,
    previous_version: str,
) -> Path:
    if not profile_catalog_path.is_file():
        raise FileNotFoundError("No se puede regenerar: falta profile_catalog actual")
    history_dir = _safe_child(domain_dir, Path("profile_catalog") / "history")
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = _safe_child(
        domain_dir,
        Path("profile_catalog")
        / "history"
        / f"profile_catalog_{previous_version.replace('.', '_')}.json",
    )
    if history_path.exists():
        raise FileExistsError(f"Historial de profile_catalog ya existe: {history_path.name}")
    shutil.copy2(profile_catalog_path, history_path)
    return history_path


def _extend_materialization_manifest(
    manifest_path: str | Path,
    manifest: dict[str, Any],
    created_paths: list[str],
) -> dict[str, Any]:
    updated = deepcopy(manifest)
    updated["created_paths"] = _dedupe([*updated.get("created_paths", []), *created_paths])
    rollback = deepcopy(updated.get("rollback_manifest", {}))
    rollback["created_paths"] = _dedupe([*rollback.get("created_paths", []), *created_paths])
    updated["rollback_manifest"] = rollback
    Path(manifest_path).write_text(
        json.dumps(updated, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return updated


def _next_patch_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"version de profile_catalog invalida: {version}")
    major, minor, patch = [int(part) for part in parts]
    return f"{major}.{minor}.{patch + 1}"


def _safe_child(domain_dir: Path, relative_path: Path) -> Path:
    target = (domain_dir / relative_path).resolve()
    if target != domain_dir and domain_dir not in target.parents:
        raise ValueError(f"Path fuera del sandbox: {target}")
    _reject_operational_domains_path(target)
    return target


def _reject_operational_domains_path(path: Path) -> None:
    domains_root = Path(config.DOMAINS_DIR).resolve()
    if path == domains_root or domains_root in path.parents:
        raise ValueError("profile_catalog sandbox no puede escribirse en domains/ operativo")


def _dedupe(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def _now() -> str:
    return datetime.now().isoformat()
