"""Materializacion sandbox de agent_presets como artefacto interno."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.artifact_manifest_schema import validate_artifact_manifest, validate_artifact_manifest_file
from core.artifact_state import ArtifactState
from core.domain_materializer import validate_materialized_sandbox_domain
from core.professional_agent_preset_generator import generate_agent_presets_for_profile_catalog
from core.profile_catalog_materializer import (
    ARTIFACT_MANIFEST_RELATIVE_PATH,
    PROFILE_CATALOG_ARTIFACT_ID,
    validate_materialized_profile_catalog,
)


AGENT_PRESETS_RELATIVE_PATH = Path("agent_presets") / "agent_presets.json"
AGENT_PRESETS_ARTIFACT_ID = "agent_presets_main"
CREATED_BY = "core.agent_preset_materializer.materialize_agent_presets"


def materialize_agent_presets(
    domain_dir: str | Path,
    *,
    regenerate: bool = False,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materializa `agent_presets` dentro de un sandbox con profile_catalog valido."""
    target = Path(domain_dir).resolve()
    _reject_operational_domains_path(target)

    domain_validation = validate_materialized_sandbox_domain(target)
    profile_validation = validate_materialized_profile_catalog(target)
    domain = domain_validation["domain"]
    profile_artifact = profile_validation["artifact"]
    if profile_artifact["artifact_id"] != PROFILE_CATALOG_ARTIFACT_ID:
        raise ValueError("profile_catalog materializado con artifact_id invalido")

    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    agent_presets_path = _safe_child(target, AGENT_PRESETS_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    existing_index = _find_agent_presets_index(artifact_manifest)
    if existing_index is not None and not regenerate:
        raise FileExistsError(
            "agent_presets ya existe en este sandbox; use regenerate=True para versionar"
        )

    now = _now()
    version = "1.0.0"
    previous_version = None
    history_entry = None
    created_paths = [str(agent_presets_path.parent), str(agent_presets_path)]
    if existing_index is not None:
        existing_artifact = artifact_manifest["artifacts"][existing_index]
        previous_version = existing_artifact["version"]
        version = _next_patch_version(previous_version)
        history_path = _archive_current_agent_presets(
            target,
            agent_presets_path,
            previous_version=previous_version,
        )
        created_paths.append(str(history_path))
        history_entry = {
            "event": "regenerated",
            "previous_version": previous_version,
            "new_version": version,
            "archived_agent_presets_path": str(history_path),
            "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
            "at": now,
        }
    elif agent_presets_path.exists():
        raise FileExistsError("agent_presets.json existe sin artifact_manifest coherente")

    generated = _build_agent_presets(
        profile_validation["profile_catalog"],
        domain=domain,
    )
    payload = _build_agent_presets_payload(
        generated,
        domain=domain,
        version=version,
        created_at=now,
        regenerated_from=previous_version,
        created_paths=created_paths,
    )
    agent_presets_path.parent.mkdir(parents=True, exist_ok=True)
    agent_presets_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
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

    artifact_manifest = validate_artifact_manifest(artifact_manifest)
    manifest_path.write_text(
        json.dumps(artifact_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    updated_materialization_manifest = _extend_materialization_manifest(
        domain_validation["manifest_path"],
        domain_validation["manifest"],
        created_paths,
    )
    return {
        "success": True,
        "domain_id": domain["domain_id"],
        "artifact_id": AGENT_PRESETS_ARTIFACT_ID,
        "artifact_type": "agent_preset",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "regenerated": existing_index is not None,
        "agent_presets_path": str(agent_presets_path),
        "artifact_manifest_path": str(manifest_path),
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "materialization_manifest": updated_materialization_manifest,
    }


def validate_materialized_agent_presets(domain_dir: str | Path) -> dict[str, Any]:
    """Valida presets sandbox trazados, dependientes de profile_catalog y no activos."""
    target = Path(domain_dir).resolve()
    validate_materialized_profile_catalog(target)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    agent_presets_path = _safe_child(target, AGENT_PRESETS_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    index = _find_agent_presets_index(artifact_manifest)
    if index is None:
        raise FileNotFoundError("artifact_manifest sin agent_presets")
    artifact = artifact_manifest["artifacts"][index]
    if artifact["status"] == ArtifactState.ACTIVE.value:
        raise ValueError("agent_presets sandbox no puede estar active")
    if artifact["dependencies"] != [PROFILE_CATALOG_ARTIFACT_ID]:
        raise ValueError("agent_presets debe depender de profile_catalog")
    if not agent_presets_path.is_file():
        raise FileNotFoundError("agent_presets registrado sin archivo materializado")
    payload = json.loads(agent_presets_path.read_text(encoding="utf-8"))
    if payload.get("sandbox_artifact", {}).get("artifact_id") != artifact["artifact_id"]:
        raise ValueError("agent_presets.json no coincide con artifact_manifest")
    for preset in payload.get("presets", []):
        if preset.get("status") == ArtifactState.ACTIVE.value or preset.get("activo") is True:
            raise ValueError("preset sandbox no puede estar activo")
        if PROFILE_CATALOG_ARTIFACT_ID not in preset.get("dependencies", []):
            raise ValueError("preset sin dependencia a profile_catalog")
    return {
        "success": True,
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "agent_presets": payload,
        "agent_presets_path": str(agent_presets_path),
        "artifact_manifest_path": str(manifest_path),
    }


def rollback_agent_presets(domain_dir: str | Path) -> dict[str, Any]:
    """Elimina solo agent_presets sandbox y conserva profile_catalog."""
    target = Path(domain_dir).resolve()
    _reject_operational_domains_path(target)
    profile_validation = validate_materialized_profile_catalog(target)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    index = _find_agent_presets_index(artifact_manifest)
    if index is None:
        raise FileNotFoundError("No hay agent_presets para rollback")
    artifact = artifact_manifest["artifacts"][index]
    _ensure_no_dependents(artifact_manifest, artifact["artifact_id"])

    deleted_paths: list[str] = []
    already_missing: list[str] = []
    removable_paths = _agent_presets_paths(target, artifact["rollback_info"]["created_paths"])
    for path in sorted(removable_paths, key=lambda item: len(item.parts), reverse=True):
        if not path.exists():
            already_missing.append(str(path))
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        deleted_paths.append(str(path))

    artifact_manifest["artifacts"].pop(index)
    artifact_manifest = validate_artifact_manifest(artifact_manifest)
    manifest_path.write_text(
        json.dumps(artifact_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _remove_paths_from_materialization_manifest(target, [str(path) for path in removable_paths])
    return {
        "success": True,
        "status": "rolled_back",
        "domain_id": profile_validation["domain"]["domain_id"],
        "artifact_id": AGENT_PRESETS_ARTIFACT_ID,
        "deleted_paths": deleted_paths,
        "already_missing": already_missing,
        "profile_catalog_path": profile_validation["profile_catalog_path"],
        "artifact_manifest": artifact_manifest,
    }


def _build_agent_presets(profile_catalog: dict[str, Any], *, domain: dict[str, Any]) -> dict[str, Any]:
    request = dict(domain.get("source_request") or {})
    return generate_agent_presets_for_profile_catalog(
        profile_catalog,
        domain_id=domain["domain_id"],
        max_presets=request.get("max_presets"),
    )


def _build_agent_presets_payload(
    generated: dict[str, Any],
    *,
    domain: dict[str, Any],
    version: str,
    created_at: str,
    regenerated_from: str | None,
    created_paths: list[str],
) -> dict[str, Any]:
    payload = deepcopy(generated)
    payload["sandbox_artifact"] = {
        "artifact_id": AGENT_PRESETS_ARTIFACT_ID,
        "artifact_type": "agent_preset",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "operational": False,
        "active": False,
        "domain_id": domain["domain_id"],
        "materialization_id": domain["materialization_id"],
        "created_at": created_at,
        "regenerated_from": regenerated_from,
        "depends_on": [PROFILE_CATALOG_ARTIFACT_ID],
    }
    payload["status"] = ArtifactState.MATERIALIZED.value
    payload["operational"] = False
    payload["active"] = False
    for preset in payload.get("presets", []):
        _normalize_preset_for_sandbox(
            preset,
            domain=domain,
            version=version,
            created_paths=created_paths,
        )
    for preset in payload.get("agent_presets", {}).get("presets", []):
        preset["activo"] = False
        preset["status"] = ArtifactState.MATERIALIZED.value
    return payload


def _normalize_preset_for_sandbox(
    preset: dict[str, Any],
    *,
    domain: dict[str, Any],
    version: str,
    created_paths: list[str],
) -> None:
    preset["artifact_id"] = f"agent_preset_{preset['preset_id']}"
    preset["domain_id"] = domain["domain_id"]
    preset["profile_reference"] = {
        "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
        "source_profile_id": preset["source_profile_id"],
        "source_domain_profile_id": preset["source_domain_profile_id"],
    }
    preset["role"] = {"role_id": preset["role_id"]}
    preset["specialization"] = {"specialization_id": preset["specialization_id"]}
    preset["model_policy_reference"] = preset["default_model_policy"]
    preset["version"] = version
    preset["status"] = ArtifactState.MATERIALIZED.value
    preset["activo"] = False
    preset["active"] = False
    preset["operational"] = False
    preset["dependencies"] = [PROFILE_CATALOG_ARTIFACT_ID]
    preset["rollback_info"] = {
        "created_paths": list(created_paths),
        "depends_on": [PROFILE_CATALOG_ARTIFACT_ID],
        "safe_remove": True,
    }
    preset.setdefault("notes", []).append("Preset materializado en sandbox; no crea agente.")


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
    return {
        "artifact_id": AGENT_PRESETS_ARTIFACT_ID,
        "artifact_type": "agent_preset",
        "name": "Agent Presets Main",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "created_from": {
            "source_type": "sandbox_profile_catalog",
            "domain_id": domain["domain_id"],
            "materialization_id": domain["materialization_id"],
            "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
            "generator": (
                "core.professional_agent_preset_generator."
                "generate_agent_presets_for_profile_catalog"
            ),
            "execution_metadata": deepcopy(execution_metadata),
        },
        "created_by": CREATED_BY,
        "dependencies": [PROFILE_CATALOG_ARTIFACT_ID],
        "created_at": previous.get("created_at", created_at) if previous else created_at,
        "updated_at": created_at,
        "rollback_info": {
            "created_paths": all_created_paths,
            "depends_on": [PROFILE_CATALOG_ARTIFACT_ID],
            "safe_remove": True,
        },
        "history": history,
        "operational": False,
        "passed": False,
    }


def _find_agent_presets_index(manifest: dict[str, Any]) -> int | None:
    indexes = [
        index
        for index, artifact in enumerate(manifest.get("artifacts", []))
        if artifact.get("artifact_type") == "agent_preset"
    ]
    if len(indexes) > 1:
        raise ValueError("artifact_manifest contiene multiples agent_presets")
    return indexes[0] if indexes else None


def _archive_current_agent_presets(
    domain_dir: Path,
    agent_presets_path: Path,
    *,
    previous_version: str,
) -> Path:
    if not agent_presets_path.is_file():
        raise FileNotFoundError("No se puede regenerar: falta agent_presets actual")
    history_dir = _safe_child(domain_dir, Path("agent_presets") / "history")
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = _safe_child(
        domain_dir,
        Path("agent_presets")
        / "history"
        / f"agent_presets_{previous_version.replace('.', '_')}.json",
    )
    if history_path.exists():
        raise FileExistsError(f"Historial de agent_presets ya existe: {history_path.name}")
    shutil.copy2(agent_presets_path, history_path)
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


def _remove_paths_from_materialization_manifest(domain_dir: Path, removed_paths: list[str]) -> None:
    manifest_path = _safe_child(domain_dir, Path("materialization_manifest.json"))
    if not manifest_path.exists():
        return
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    removed = set(removed_paths)
    data["created_paths"] = [path for path in data.get("created_paths", []) if path not in removed]
    rollback = data.get("rollback_manifest", {})
    rollback["created_paths"] = [
        path for path in rollback.get("created_paths", []) if path not in removed
    ]
    data["rollback_manifest"] = rollback
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _ensure_no_dependents(manifest: dict[str, Any], artifact_id: str) -> None:
    dependents = [
        artifact["artifact_id"]
        for artifact in manifest.get("artifacts", [])
        if artifact["artifact_id"] != artifact_id and artifact_id in artifact.get("dependencies", [])
    ]
    if dependents:
        raise ValueError(f"No se puede remover agent_presets; tiene dependientes: {dependents}")


def _agent_presets_paths(domain_dir: Path, raw_paths: list[str]) -> list[Path]:
    paths: list[Path] = []
    agent_root = _safe_child(domain_dir, Path("agent_presets"))
    for raw_path in raw_paths:
        path = Path(str(raw_path)).resolve()
        if path == agent_root or agent_root in path.parents:
            _safe_child(domain_dir, path.relative_to(domain_dir))
            paths.append(path)
    return _dedupe_paths(paths)


def _next_patch_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"version de agent_presets invalida: {version}")
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
        raise ValueError("agent_presets sandbox no puede escribirse en domains/ operativo")


def _dedupe(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    return list(dict.fromkeys(paths))


def _now() -> str:
    return datetime.now().isoformat()
