"""Materializacion de agentes sandbox sin ejecucion runtime."""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.agent_lineage_schema import (
    build_agent_lineage,
    lineage_to_artifact_manifest_metadata,
    validate_agent_lineage,
)
from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.artifact_manifest_schema import validate_artifact_manifest, validate_artifact_manifest_file
from core.artifact_state import ArtifactState
from core.domain_materializer import validate_materialized_sandbox_domain
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID, validate_materialized_paper_seed
from core.profile_catalog_materializer import (
    ARTIFACT_MANIFEST_RELATIVE_PATH,
    PROFILE_CATALOG_ARTIFACT_ID,
)
from core.sandbox_agent_schema import (
    SANDBOX_AGENT_REQUIRED_DEPENDENCIES,
    build_sandbox_agent_schema,
    sandbox_agent_to_artifact_record,
    validate_sandbox_agent_schema,
)


SANDBOX_AGENTS_DIR = Path("sandbox_agents")
CREATED_BY = "core.sandbox_agent_materializer.materialize_sandbox_agent"


def materialize_sandbox_agent(
    domain_dir: str | Path,
    *,
    preset_id: str | None = None,
    regenerate: bool = False,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materializa una configuracion de agente sandbox sin activar runtime."""
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)

    domain_validation = validate_materialized_sandbox_domain(target)
    paper_validation = validate_materialized_paper_seed(target)
    domain = domain_validation["domain"]
    artifact_manifest = paper_validation["artifact_manifest"]
    _validate_base_dependencies(artifact_manifest)

    preset = _select_preset(target, preset_id=preset_id)
    paper_seed = _select_paper_seed(paper_validation["paper_seed"], preset["preset_id"])
    agent_id = _agent_id_from_preset(preset)
    agent_path = _safe_child(target, SANDBOX_AGENTS_DIR / f"{agent_id}.json")
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_id = f"agent_{agent_id}"
    existing_index = _find_agent_artifact_index(artifact_manifest, artifact_id)
    if existing_index is not None and not regenerate:
        raise FileExistsError(
            f"agent_id ya existe en este sandbox: {agent_id}; use regenerate=True"
        )

    now = _now()
    version = "1.0.0"
    previous_version = None
    history_entry = {
        "event": "materialized",
        "version": version,
        "at": now,
        "details": "Agente sandbox materializado sin activar runtime.",
    }
    created_paths = [str(agent_path.parent), str(agent_path)]
    previous_artifact = None
    previous_agent = None
    if existing_index is not None:
        previous_artifact = artifact_manifest["artifacts"][existing_index]
        previous_version = previous_artifact["version"]
        version = _next_patch_version(previous_version)
        history_path = _archive_current_agent(target, agent_path, previous_version=previous_version)
        created_paths.append(str(history_path))
        previous_agent = json.loads(agent_path.read_text(encoding="utf-8"))
        history_entry = {
            "event": "regenerated",
            "version": version,
            "at": now,
            "details": "Agente sandbox regenerado con misma identidad estable.",
            "previous_version": previous_version,
            "archived_agent_path": str(history_path),
        }
    elif agent_path.exists():
        raise FileExistsError(f"Config sandbox de agente existe sin manifest coherente: {agent_id}")

    lineage = _build_lineage(
        domain=domain,
        agent_id=agent_id,
        preset=preset,
        paper_seed=paper_seed,
        version=version,
        created_at=now,
        previous_agent=previous_agent,
        history_entry=history_entry,
    )
    agent = _build_agent_payload(
        domain=domain,
        agent_id=agent_id,
        preset=preset,
        paper_seed=paper_seed,
        lineage=lineage,
        version=version,
        created_at=now,
        created_paths=created_paths,
        execution_metadata=execution_metadata or {},
    )
    agent_path.parent.mkdir(parents=True, exist_ok=True)
    agent_path.write_text(json.dumps(agent, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    artifact = sandbox_agent_to_artifact_record(agent)
    artifact["created_by"] = CREATED_BY
    artifact["created_from"]["lineage"] = lineage_to_artifact_manifest_metadata(lineage)
    artifact["created_from"]["execution_metadata"] = deepcopy(execution_metadata or {})
    artifact["rollback_info"]["created_paths"] = _dedupe(
        [*(previous_artifact or {}).get("rollback_info", {}).get("created_paths", []), *created_paths]
    )
    artifact["status"] = ArtifactState.MATERIALIZED.value
    artifact["history"] = list(previous_artifact.get("history", [])) if previous_artifact else []
    artifact["history"].append(history_entry)
    artifact["operational"] = False
    artifact["passed"] = False

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
        "agent_id": agent_id,
        "artifact_id": artifact_id,
        "artifact_type": "agent",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "regenerated": existing_index is not None,
        "agent_path": str(agent_path),
        "artifact_manifest_path": str(manifest_path),
        "agent": agent,
        "lineage": lineage,
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "materialization_manifest": updated_materialization_manifest,
    }


def validate_materialized_sandbox_agent(
    domain_dir: str | Path,
    *,
    agent_id: str,
) -> dict[str, Any]:
    """Valida un agente sandbox materializado y no operativo."""
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)
    validate_materialized_paper_seed(target)
    agent_path = _safe_child(target, SANDBOX_AGENTS_DIR / f"{agent_id}.json")
    if not agent_path.is_file():
        raise FileNotFoundError(f"Agente sandbox no encontrado: {agent_id}")
    agent = json.loads(agent_path.read_text(encoding="utf-8"))
    validate_sandbox_agent_schema(agent)
    lineage = validate_agent_lineage(agent.get("lineage"))
    if agent.get("status") == ArtifactState.ACTIVE.value or agent.get("active") is True:
        raise ValueError("agente sandbox no puede estar active")
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    artifact_id = f"agent_{agent_id}"
    index = _find_agent_artifact_index(artifact_manifest, artifact_id)
    if index is None:
        raise FileNotFoundError("artifact_manifest sin agente sandbox")
    artifact = artifact_manifest["artifacts"][index]
    if artifact["dependencies"] != SANDBOX_AGENT_REQUIRED_DEPENDENCIES:
        raise ValueError("agente sandbox con dependencias invalidas")
    return {
        "success": True,
        "agent": agent,
        "lineage": lineage,
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "agent_path": str(agent_path),
    }


def rollback_sandbox_agent(domain_dir: str | Path, *, agent_id: str) -> dict[str, Any]:
    """Elimina solo la configuracion del agente sandbox y conserva dependencias."""
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)
    validate_materialized_paper_seed(target)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    artifact_id = f"agent_{agent_id}"
    index = _find_agent_artifact_index(artifact_manifest, artifact_id)
    if index is None:
        raise FileNotFoundError(f"No hay agente sandbox para rollback: {agent_id}")
    artifact = artifact_manifest["artifacts"][index]
    _ensure_no_dependents(artifact_manifest, artifact_id)

    removable_paths = _agent_paths(target, artifact["rollback_info"]["created_paths"], agent_id)
    deleted_paths: list[str] = []
    already_missing: list[str] = []
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
        "agent_id": agent_id,
        "artifact_id": artifact_id,
        "deleted_paths": deleted_paths,
        "already_missing": already_missing,
        "artifact_manifest": artifact_manifest,
    }


def _build_agent_payload(
    *,
    domain: dict[str, Any],
    agent_id: str,
    preset: dict[str, Any],
    paper_seed: dict[str, Any],
    lineage: dict[str, Any],
    version: str,
    created_at: str,
    created_paths: list[str],
    execution_metadata: dict[str, Any],
) -> dict[str, Any]:
    agent = build_sandbox_agent_schema(
        agent_id=agent_id,
        domain_id=domain["domain_id"],
        profile_reference=deepcopy(preset["profile_reference"]),
        preset_reference={
            "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
            "preset_id": preset["preset_id"],
            "preset_artifact_id": preset["artifact_id"],
        },
        paper_reference={
            "paper_seed_artifact_id": PAPER_SEED_ARTIFACT_ID,
            "paper_seed_id": paper_seed["artifact_id"],
        },
        role=deepcopy(preset["role"]),
        specialization=deepcopy(preset["specialization"]),
        model_policy_reference=preset["model_policy_reference"],
        version=version,
        status=ArtifactState.MATERIALIZED.value,
        created_at=created_at,
        updated_at=created_at,
    )
    agent["rollback_info"]["created_paths"] = list(created_paths)
    agent["lineage"] = deepcopy(lineage)
    agent["sandbox_config"] = {
        "runtime_enabled": False,
        "operational": False,
        "provider": preset.get("recommended_provider"),
        "model": preset.get("recommended_model"),
        "temperature": preset.get("recommended_temperature"),
        "system_prompt_seed": preset.get("system_prompt"),
        "knowledge_seed": deepcopy(paper_seed.get("knowledge_seed", {})),
        "execution_metadata": deepcopy(execution_metadata),
    }
    agent["metadata"] = {
        **agent.get("metadata", {}),
        "created_by": CREATED_BY,
        "source": "sandbox_materialization",
        "creates_runtime_agent": False,
    }
    return validate_sandbox_agent_schema(agent)


def _build_lineage(
    *,
    domain: dict[str, Any],
    agent_id: str,
    preset: dict[str, Any],
    paper_seed: dict[str, Any],
    version: str,
    created_at: str,
    previous_agent: dict[str, Any] | None,
    history_entry: dict[str, Any],
) -> dict[str, Any]:
    origin = {
        "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
        "source_profile_id": preset["source_profile_id"],
        "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
        "preset_id": preset["preset_id"],
        "paper_seed_artifact_id": PAPER_SEED_ARTIFACT_ID,
        "paper_seed_id": paper_seed["artifact_id"],
    }
    previous_history = []
    previous_created_at = created_at
    if previous_agent:
        previous_lineage = validate_agent_lineage(previous_agent["lineage"])
        previous_history = list(previous_lineage["history"])
        previous_created_at = previous_lineage["created_at"]
    return build_agent_lineage(
        agent_id=agent_id,
        domain_id=domain["domain_id"],
        origin=origin,
        current_version=version,
        history=[*previous_history, history_entry],
        created_at=previous_created_at,
        updated_at=created_at,
    )


def _select_preset(domain_dir: Path, *, preset_id: str | None) -> dict[str, Any]:
    presets = _agent_presets_from_domain(domain_dir)
    if not presets:
        raise ValueError("agent_presets materializado sin presets")
    if preset_id is None:
        return presets[0]
    for preset in presets:
        if preset.get("preset_id") == preset_id:
            return preset
    raise ValueError(f"preset_id inexistente en sandbox: {preset_id}")


def _agent_presets_from_domain(domain_dir: Path) -> list[dict[str, Any]]:
    agent_presets_path = _safe_child(domain_dir, Path("agent_presets") / "agent_presets.json")
    if not agent_presets_path.is_file():
        raise FileNotFoundError("agent_presets.json requerido para crear agente sandbox")
    return json.loads(agent_presets_path.read_text(encoding="utf-8")).get("presets", [])


def _select_paper_seed(paper_payload: dict[str, Any], preset_id: str) -> dict[str, Any]:
    for seed in paper_payload.get("paper_seeds", []):
        if seed.get("preset_reference", {}).get("preset_id") == preset_id:
            return seed
    raise ValueError(f"paper_seed inexistente para preset_id: {preset_id}")


def _agent_id_from_preset(preset: dict[str, Any]) -> str:
    value = preset.get("suggested_agent_id") or preset.get("source_profile_id") or preset["preset_id"]
    return _normalize_id(f"sandbox_{value}")


def _normalize_id(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip())
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_value).strip("_")
    slug = re.sub(r"_+", "_", slug)
    if not slug:
        raise ValueError("agent_id vacio")
    return slug


def _validate_base_dependencies(manifest: dict[str, Any]) -> None:
    ids = {artifact["artifact_id"] for artifact in manifest.get("artifacts", [])}
    missing = [dependency for dependency in SANDBOX_AGENT_REQUIRED_DEPENDENCIES if dependency not in ids]
    if missing:
        raise ValueError(f"agente sandbox requiere dependencias existentes: {missing}")


def _find_agent_artifact_index(manifest: dict[str, Any], artifact_id: str) -> int | None:
    indexes = [
        index
        for index, artifact in enumerate(manifest.get("artifacts", []))
        if artifact.get("artifact_id") == artifact_id and artifact.get("artifact_type") == "agent"
    ]
    if len(indexes) > 1:
        raise ValueError(f"artifact_manifest contiene multiples agentes para {artifact_id}")
    return indexes[0] if indexes else None


def _archive_current_agent(domain_dir: Path, agent_path: Path, *, previous_version: str) -> Path:
    if not agent_path.is_file():
        raise FileNotFoundError("No se puede regenerar: falta agente sandbox actual")
    history_dir = _safe_child(domain_dir, SANDBOX_AGENTS_DIR / "history")
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = _safe_child(
        domain_dir,
        SANDBOX_AGENTS_DIR
        / "history"
        / f"{agent_path.stem}_{previous_version.replace('.', '_')}.json",
    )
    if history_path.exists():
        raise FileExistsError(f"Historial de agente sandbox ya existe: {history_path.name}")
    shutil.copy2(agent_path, history_path)
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
        raise ValueError(f"No se puede remover agente sandbox; tiene dependientes: {dependents}")


def _agent_paths(domain_dir: Path, raw_paths: list[str], agent_id: str) -> list[Path]:
    paths: list[Path] = []
    agent_root = _safe_child(domain_dir, SANDBOX_AGENTS_DIR)
    agent_file = _safe_child(domain_dir, SANDBOX_AGENTS_DIR / f"{agent_id}.json")
    for raw_path in raw_paths:
        path = Path(str(raw_path)).resolve()
        if path == agent_file or path == agent_root or agent_root in path.parents:
            _safe_child(domain_dir, path.relative_to(domain_dir))
            paths.append(path)
    return _dedupe_paths(paths)


def _next_patch_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"version de agente sandbox invalida: {version}")
    major, minor, patch = [int(part) for part in parts]
    return f"{major}.{minor}.{patch + 1}"


def _safe_child(domain_dir: Path, relative_path: Path) -> Path:
    target = (domain_dir / relative_path).resolve()
    if target != domain_dir and domain_dir not in target.parents:
        raise ValueError(f"Path fuera del sandbox: {target}")
    _reject_operational_paths(target)
    return target


def _reject_operational_paths(path: Path) -> None:
    domains_root = Path(config.DOMAINS_DIR).resolve()
    agents_root = (Path(__file__).resolve().parent.parent / "agents").resolve()
    if path == domains_root or domains_root in path.parents:
        raise ValueError("agente sandbox no puede escribirse en domains/ operativo")
    if path == agents_root or agents_root in path.parents:
        raise ValueError("agente sandbox no puede escribirse en agents/ runtime")


def _dedupe(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    return list(dict.fromkeys(paths))


def _now() -> str:
    return datetime.now().isoformat()
