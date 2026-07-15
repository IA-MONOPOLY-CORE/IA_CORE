"""Materializacion sandbox de paper_seed como artefacto de conocimiento."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.agent_preset_materializer import (
    AGENT_PRESETS_ARTIFACT_ID,
    validate_materialized_agent_presets,
)
from core.artifact_manifest_schema import validate_artifact_manifest, validate_artifact_manifest_file
from core.artifact_state import ArtifactState
from core.domain_materializer import validate_materialized_sandbox_domain
from core.profile_catalog_materializer import (
    ARTIFACT_MANIFEST_RELATIVE_PATH,
    PROFILE_CATALOG_ARTIFACT_ID,
)


PAPER_SEED_RELATIVE_PATH = Path("paper_seed") / "paper_seed.json"
PAPER_SEED_ARTIFACT_ID = "paper_seed_main"
CREATED_BY = "core.paper_seed_materializer.materialize_paper_seed"
DEPENDENCIES = [PROFILE_CATALOG_ARTIFACT_ID, AGENT_PRESETS_ARTIFACT_ID]


def materialize_paper_seed(
    domain_dir: str | Path,
    *,
    regenerate: bool = False,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materializa paper_seed dentro de un sandbox con presets trazados."""
    target = Path(domain_dir).resolve()
    _reject_operational_domains_path(target)

    domain_validation = validate_materialized_sandbox_domain(target)
    presets_validation = validate_materialized_agent_presets(target)
    domain = domain_validation["domain"]
    artifact_manifest = presets_validation["artifact_manifest"]
    _validate_base_dependencies(artifact_manifest)

    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    paper_seed_path = _safe_child(target, PAPER_SEED_RELATIVE_PATH)
    existing_index = _find_paper_seed_index(artifact_manifest)
    if existing_index is not None and not regenerate:
        raise FileExistsError(
            "paper_seed ya existe en este sandbox; use regenerate=True para versionar"
        )

    now = _now()
    version = "1.0.0"
    previous_version = None
    history_entry = None
    created_paths = [str(paper_seed_path.parent), str(paper_seed_path)]
    if existing_index is not None:
        existing_artifact = artifact_manifest["artifacts"][existing_index]
        previous_version = existing_artifact["version"]
        version = _next_patch_version(previous_version)
        history_path = _archive_current_paper_seed(
            target,
            paper_seed_path,
            previous_version=previous_version,
        )
        created_paths.append(str(history_path))
        history_entry = {
            "event": "regenerated",
            "previous_version": previous_version,
            "new_version": version,
            "archived_paper_seed_path": str(history_path),
            "dependencies": list(DEPENDENCIES),
            "at": now,
        }
    elif paper_seed_path.exists():
        raise FileExistsError("paper_seed.json existe sin artifact_manifest coherente")

    payload = _build_paper_seed_payload(
        presets_validation["agent_presets"],
        domain=domain,
        version=version,
        created_at=now,
        regenerated_from=previous_version,
        created_paths=created_paths,
    )
    paper_seed_path.parent.mkdir(parents=True, exist_ok=True)
    paper_seed_path.write_text(
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
        "artifact_id": PAPER_SEED_ARTIFACT_ID,
        "artifact_type": "paper_seed",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "regenerated": existing_index is not None,
        "paper_seed_path": str(paper_seed_path),
        "artifact_manifest_path": str(manifest_path),
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "materialization_manifest": updated_materialization_manifest,
    }


def validate_materialized_paper_seed(domain_dir: str | Path) -> dict[str, Any]:
    """Valida paper_seed sandbox trazado, dependiente de perfiles y presets."""
    target = Path(domain_dir).resolve()
    validate_materialized_agent_presets(target)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    paper_seed_path = _safe_child(target, PAPER_SEED_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    index = _find_paper_seed_index(artifact_manifest)
    if index is None:
        raise FileNotFoundError("artifact_manifest sin paper_seed")
    artifact = artifact_manifest["artifacts"][index]
    if artifact["status"] == ArtifactState.ACTIVE.value:
        raise ValueError("paper_seed sandbox no puede estar active")
    if artifact["dependencies"] != DEPENDENCIES:
        raise ValueError("paper_seed debe depender de profile_catalog y agent_presets")
    if not paper_seed_path.is_file():
        raise FileNotFoundError("paper_seed registrado sin archivo materializado")
    payload = json.loads(paper_seed_path.read_text(encoding="utf-8"))
    if payload.get("sandbox_artifact", {}).get("artifact_id") != artifact["artifact_id"]:
        raise ValueError("paper_seed.json no coincide con artifact_manifest")
    for seed in payload.get("paper_seeds", []):
        if seed.get("status") == ArtifactState.ACTIVE.value or seed.get("active") is True:
            raise ValueError("paper_seed sandbox no puede estar activo")
        if seed.get("dependencies") != DEPENDENCIES:
            raise ValueError("paper_seed sin dependencias completas")
    return {
        "success": True,
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "paper_seed": payload,
        "paper_seed_path": str(paper_seed_path),
        "artifact_manifest_path": str(manifest_path),
    }


def rollback_paper_seed(domain_dir: str | Path) -> dict[str, Any]:
    """Elimina solo paper_seed sandbox y conserva profile_catalog y agent_presets."""
    target = Path(domain_dir).resolve()
    _reject_operational_domains_path(target)
    presets_validation = validate_materialized_agent_presets(target)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    index = _find_paper_seed_index(artifact_manifest)
    if index is None:
        raise FileNotFoundError("No hay paper_seed para rollback")
    artifact = artifact_manifest["artifacts"][index]
    _ensure_no_dependents(artifact_manifest, artifact["artifact_id"])

    deleted_paths: list[str] = []
    already_missing: list[str] = []
    removable_paths = _paper_seed_paths(target, artifact["rollback_info"]["created_paths"])
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
        "domain_id": presets_validation["agent_presets"]["domain_id"],
        "artifact_id": PAPER_SEED_ARTIFACT_ID,
        "deleted_paths": deleted_paths,
        "already_missing": already_missing,
        "agent_presets_path": presets_validation["agent_presets_path"],
        "artifact_manifest": artifact_manifest,
    }


def _build_paper_seed_payload(
    agent_presets: dict[str, Any],
    *,
    domain: dict[str, Any],
    version: str,
    created_at: str,
    regenerated_from: str | None,
    created_paths: list[str],
) -> dict[str, Any]:
    seeds = [
        _build_seed_from_preset(
            preset,
            domain=domain,
            version=version,
            created_at=created_at,
            created_paths=created_paths,
        )
        for preset in agent_presets.get("presets", [])
    ]
    return {
        "schema_version": "1.0",
        "artifact_type": "sandbox_paper_seed_collection",
        "domain_id": domain["domain_id"],
        "status": ArtifactState.MATERIALIZED.value,
        "operational": False,
        "active": False,
        "sandbox_artifact": {
            "artifact_id": PAPER_SEED_ARTIFACT_ID,
            "artifact_type": "paper_seed",
            "version": version,
            "status": ArtifactState.MATERIALIZED.value,
            "operational": False,
            "active": False,
            "domain_id": domain["domain_id"],
            "materialization_id": domain["materialization_id"],
            "created_at": created_at,
            "regenerated_from": regenerated_from,
            "depends_on": list(DEPENDENCIES),
        },
        "source": "agent_presets.paper_seed",
        "generator": CREATED_BY,
        "dependencies": list(DEPENDENCIES),
        "summary": {
            "paper_seed_count": len(seeds),
            "source_preset_ids": [seed["preset_reference"]["preset_id"] for seed in seeds],
        },
        "paper_seeds": seeds,
    }


def _build_seed_from_preset(
    preset: dict[str, Any],
    *,
    domain: dict[str, Any],
    version: str,
    created_at: str,
    created_paths: list[str],
) -> dict[str, Any]:
    seed = preset.get("paper_seed") or {}
    for field in ["identity", "operating_style", "learning_focus"]:
        if not seed.get(field):
            raise ValueError(f"preset {preset.get('preset_id', '?')} sin paper_seed.{field}")
    preset_artifact_id = preset.get("artifact_id")
    return {
        "artifact_id": f"paper_seed_{preset['preset_id']}",
        "domain_id": domain["domain_id"],
        "profile_reference": deepcopy(preset["profile_reference"]),
        "preset_reference": {
            "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
            "preset_artifact_id": preset_artifact_id,
            "preset_id": preset["preset_id"],
            "source_profile_id": preset["source_profile_id"],
        },
        "source": "agent_preset.paper_seed",
        "generator": CREATED_BY,
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "active": False,
        "operational": False,
        "dependencies": list(DEPENDENCIES),
        "rollback_info": {
            "created_paths": list(created_paths),
            "depends_on": list(DEPENDENCIES),
            "safe_remove": True,
        },
        "knowledge_seed": {
            "identity": seed["identity"],
            "operating_style": seed["operating_style"],
            "learning_focus": seed["learning_focus"],
            "decision_criteria": list(preset.get("decision_criteria", [])),
            "avoid": list(preset.get("avoid", [])),
            "memory_policy": deepcopy(preset.get("memory_policy", {})),
            "paper_seed_expected": preset.get("paper_seed_expected"),
        },
        "created_at": created_at,
        "updated_at": created_at,
    }


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
        "artifact_id": PAPER_SEED_ARTIFACT_ID,
        "artifact_type": "paper_seed",
        "name": "Paper Seed Main",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "created_from": {
            "source_type": "sandbox_agent_presets",
            "domain_id": domain["domain_id"],
            "materialization_id": domain["materialization_id"],
            "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
            "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
            "generator": CREATED_BY,
            "execution_metadata": deepcopy(execution_metadata),
        },
        "created_by": CREATED_BY,
        "dependencies": list(DEPENDENCIES),
        "created_at": previous.get("created_at", created_at) if previous else created_at,
        "updated_at": created_at,
        "rollback_info": {
            "created_paths": all_created_paths,
            "depends_on": list(DEPENDENCIES),
            "safe_remove": True,
        },
        "history": history,
        "operational": False,
        "passed": False,
    }


def _validate_base_dependencies(manifest: dict[str, Any]) -> None:
    ids = {artifact["artifact_id"] for artifact in manifest.get("artifacts", [])}
    missing = [dependency for dependency in DEPENDENCIES if dependency not in ids]
    if missing:
        raise ValueError(f"paper_seed requiere dependencias existentes: {missing}")


def _find_paper_seed_index(manifest: dict[str, Any]) -> int | None:
    indexes = [
        index
        for index, artifact in enumerate(manifest.get("artifacts", []))
        if artifact.get("artifact_type") == "paper_seed"
    ]
    if len(indexes) > 1:
        raise ValueError("artifact_manifest contiene multiples paper_seed")
    return indexes[0] if indexes else None


def _archive_current_paper_seed(
    domain_dir: Path,
    paper_seed_path: Path,
    *,
    previous_version: str,
) -> Path:
    if not paper_seed_path.is_file():
        raise FileNotFoundError("No se puede regenerar: falta paper_seed actual")
    history_dir = _safe_child(domain_dir, Path("paper_seed") / "history")
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = _safe_child(
        domain_dir,
        Path("paper_seed") / "history" / f"paper_seed_{previous_version.replace('.', '_')}.json",
    )
    if history_path.exists():
        raise FileExistsError(f"Historial de paper_seed ya existe: {history_path.name}")
    shutil.copy2(paper_seed_path, history_path)
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
        raise ValueError(f"No se puede remover paper_seed; tiene dependientes: {dependents}")


def _paper_seed_paths(domain_dir: Path, raw_paths: list[str]) -> list[Path]:
    paths: list[Path] = []
    paper_root = _safe_child(domain_dir, Path("paper_seed"))
    for raw_path in raw_paths:
        path = Path(str(raw_path)).resolve()
        if path == paper_root or paper_root in path.parents:
            _safe_child(domain_dir, path.relative_to(domain_dir))
            paths.append(path)
    return _dedupe_paths(paths)


def _next_patch_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"version de paper_seed invalida: {version}")
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
        raise ValueError("paper_seed sandbox no puede escribirse en domains/ operativo")


def _dedupe(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    return list(dict.fromkeys(paths))


def _now() -> str:
    return datetime.now().isoformat()
