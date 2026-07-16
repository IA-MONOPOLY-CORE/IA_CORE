"""Materializacion de equipos sandbox sin coordinacion runtime."""

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
from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.artifact_manifest_schema import validate_artifact_manifest, validate_artifact_manifest_file
from core.artifact_state import ArtifactState
from core.domain_materializer import validate_materialized_sandbox_domain
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID, validate_materialized_paper_seed
from core.profile_catalog_materializer import (
    ARTIFACT_MANIFEST_RELATIVE_PATH,
    PROFILE_CATALOG_ARTIFACT_ID,
)
from core.sandbox_agent_materializer import SANDBOX_AGENTS_DIR, validate_materialized_sandbox_agent
from core.sandbox_team_schema import (
    build_sandbox_team_schema,
    sandbox_team_to_artifact_record,
    validate_sandbox_team_schema,
)


SANDBOX_TEAMS_DIR = Path("sandbox_teams")
CREATED_BY = "core.sandbox_team_materializer.materialize_sandbox_team"
BASE_DEPENDENCIES = [
    PROFILE_CATALOG_ARTIFACT_ID,
    AGENT_PRESETS_ARTIFACT_ID,
    PAPER_SEED_ARTIFACT_ID,
]


def materialize_sandbox_team(
    domain_dir: str | Path,
    *,
    team_id: str | None = None,
    name: str | None = None,
    purpose: str | None = None,
    agent_ids: list[str] | None = None,
    coordination_model: dict[str, Any] | None = None,
    capabilities: dict[str, Any] | None = None,
    regenerate: bool = False,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materializa un equipo sandbox declarativo y no ejecutable."""
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)

    domain_validation = validate_materialized_sandbox_domain(target)
    paper_validation = validate_materialized_paper_seed(target)
    domain = domain_validation["domain"]
    artifact_manifest = paper_validation["artifact_manifest"]
    _validate_base_dependencies(artifact_manifest)

    selected_agents = _select_agents(target, agent_ids=agent_ids)
    normalized_team_id = _normalize_id(team_id or f"{domain['domain_id']}_team")
    team_name = name or f"Sandbox Team {domain['domain_id']}"
    team_purpose = purpose or "Equipo sandbox declarativo sin ejecucion runtime."
    team_path = _safe_child(target, SANDBOX_TEAMS_DIR / f"{normalized_team_id}.json")
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_id = f"team_{normalized_team_id}"
    existing_index = _find_team_artifact_index(artifact_manifest, artifact_id)
    if existing_index is not None and not regenerate:
        raise FileExistsError(
            f"team_id ya existe en este sandbox: {normalized_team_id}; use regenerate=True"
        )

    now = _now()
    version = "1.0.0"
    previous_artifact = None
    previous_team = None
    previous_version = None
    history_entry = {
        "event": "materialized",
        "version": version,
        "at": now,
        "details": "Equipo sandbox materializado sin coordinacion runtime.",
    }
    created_paths = [str(team_path.parent), str(team_path)]
    if existing_index is not None:
        previous_artifact = artifact_manifest["artifacts"][existing_index]
        previous_version = previous_artifact["version"]
        version = _next_patch_version(previous_version)
        history_path = _archive_current_team(target, team_path, previous_version=previous_version)
        created_paths.append(str(history_path.parent))
        created_paths.append(str(history_path))
        previous_team = json.loads(team_path.read_text(encoding="utf-8"))
        history_entry = {
            "event": "regenerated",
            "version": version,
            "at": now,
            "details": "Equipo sandbox regenerado con misma identidad estable.",
            "previous_version": previous_version,
            "archived_team_path": str(history_path),
        }
    elif team_path.exists():
        raise FileExistsError(f"Equipo sandbox existe sin manifest coherente: {normalized_team_id}")

    team = _build_team_payload(
        domain=domain,
        team_id=normalized_team_id,
        name=team_name,
        purpose=team_purpose,
        agents=selected_agents,
        coordination_model=coordination_model,
        capabilities=capabilities,
        version=version,
        created_at=now,
        created_paths=created_paths,
        execution_metadata=execution_metadata or {},
        previous_team=previous_team,
        history_entry=history_entry,
    )
    team_path.parent.mkdir(parents=True, exist_ok=True)
    team_path.write_text(json.dumps(team, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    artifact = sandbox_team_to_artifact_record(team)
    full_dependencies = [*BASE_DEPENDENCIES, *team["dependencies"]]
    artifact["dependencies"] = full_dependencies
    artifact["created_by"] = CREATED_BY
    artifact["created_from"]["execution_metadata"] = deepcopy(execution_metadata or {})
    artifact["created_from"]["materialization_id"] = domain["materialization_id"]
    artifact["rollback_info"]["created_paths"] = _dedupe(
        [*(previous_artifact or {}).get("rollback_info", {}).get("created_paths", []), *created_paths]
    )
    artifact["rollback_info"]["depends_on"] = full_dependencies
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
        "team_id": normalized_team_id,
        "artifact_id": artifact_id,
        "artifact_type": "team",
        "version": version,
        "status": ArtifactState.MATERIALIZED.value,
        "regenerated": existing_index is not None,
        "team_path": str(team_path),
        "artifact_manifest_path": str(manifest_path),
        "team": team,
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "materialization_manifest": updated_materialization_manifest,
    }


def regenerate_sandbox_team(domain_dir: str | Path, **kwargs: Any) -> dict[str, Any]:
    """Regenera un equipo sandbox existente manteniendo identidad estable."""
    return materialize_sandbox_team(domain_dir, regenerate=True, **kwargs)


def validate_materialized_sandbox_team(
    domain_dir: str | Path,
    *,
    team_id: str,
) -> dict[str, Any]:
    """Valida un equipo sandbox materializado y no operativo."""
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)
    validate_materialized_paper_seed(target)
    normalized_team_id = _normalize_id(team_id)
    team_path = _safe_child(target, SANDBOX_TEAMS_DIR / f"{normalized_team_id}.json")
    if not team_path.is_file():
        raise FileNotFoundError(f"Equipo sandbox no encontrado: {normalized_team_id}")
    team = json.loads(team_path.read_text(encoding="utf-8"))
    validate_sandbox_team_schema(team)
    if team.get("status") == ArtifactState.ACTIVE.value or team.get("active") is True:
        raise ValueError("equipo sandbox no puede estar active")
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    artifact_id = f"team_{normalized_team_id}"
    index = _find_team_artifact_index(artifact_manifest, artifact_id)
    if index is None:
        raise FileNotFoundError("artifact_manifest sin equipo sandbox")
    artifact = artifact_manifest["artifacts"][index]
    expected_dependencies = [*BASE_DEPENDENCIES, *team["dependencies"]]
    if artifact["dependencies"] != expected_dependencies:
        raise ValueError("equipo sandbox con dependencias invalidas")
    return {
        "success": True,
        "team": team,
        "artifact": artifact,
        "artifact_manifest": artifact_manifest,
        "team_path": str(team_path),
    }


def rollback_sandbox_team(domain_dir: str | Path, *, team_id: str) -> dict[str, Any]:
    """Elimina solo el equipo sandbox y conserva agentes/dependencias base."""
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)
    validate_materialized_paper_seed(target)
    normalized_team_id = _normalize_id(team_id)
    manifest_path = _safe_child(target, ARTIFACT_MANIFEST_RELATIVE_PATH)
    artifact_manifest = validate_artifact_manifest_file(manifest_path)
    artifact_id = f"team_{normalized_team_id}"
    index = _find_team_artifact_index(artifact_manifest, artifact_id)
    if index is None:
        raise FileNotFoundError(f"No hay equipo sandbox para rollback: {normalized_team_id}")
    artifact = artifact_manifest["artifacts"][index]
    _ensure_no_dependents(artifact_manifest, artifact_id)

    removable_paths = _team_paths(target, artifact["rollback_info"]["created_paths"], normalized_team_id)
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
    team_root = _safe_child(target, SANDBOX_TEAMS_DIR)
    history_root = _safe_child(target, SANDBOX_TEAMS_DIR / "history")
    if history_root.exists() and not any(history_root.iterdir()):
        history_root.rmdir()
        deleted_paths.append(str(history_root))
    if team_root.exists() and not any(team_root.iterdir()):
        team_root.rmdir()
        deleted_paths.append(str(team_root))

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
        "team_id": normalized_team_id,
        "artifact_id": artifact_id,
        "deleted_paths": deleted_paths,
        "already_missing": already_missing,
        "artifact_manifest": artifact_manifest,
    }


def _build_team_payload(
    *,
    domain: dict[str, Any],
    team_id: str,
    name: str,
    purpose: str,
    agents: list[dict[str, Any]],
    coordination_model: dict[str, Any] | None,
    capabilities: dict[str, Any] | None,
    version: str,
    created_at: str,
    created_paths: list[str],
    execution_metadata: dict[str, Any],
    previous_team: dict[str, Any] | None,
    history_entry: dict[str, Any],
) -> dict[str, Any]:
    members = [
        {
            "agent_id": agent["agent_id"],
            "role": agent.get("role", {}).get("role_id") or agent.get("role_id") or "member",
            "specialization": (
                agent.get("specialization", {}).get("specialization_id")
                or agent.get("specialization_id")
                or "general"
            ),
            "responsibility": _responsibility_from_agent(agent),
            "required": True,
            "source_reference": {
                "artifact_id": f"agent_{agent['agent_id']}",
                "artifact_type": "agent",
                "agent_path": agent.get("metadata", {}).get("source_agent_path"),
            },
            "status": ArtifactState.MATERIALIZED.value,
        }
        for agent in agents
    ]
    team = build_sandbox_team_schema(
        team_id=team_id,
        domain_id=domain["domain_id"],
        name=name,
        purpose=purpose,
        member_agents=members,
        coordination_model=coordination_model or _default_coordination_model(members),
        capabilities=capabilities,
        version=version,
        status=ArtifactState.MATERIALIZED.value,
        created_at=previous_team.get("created_at", created_at) if previous_team else created_at,
        updated_at=created_at,
    )
    team["rollback_info"]["created_paths"] = list(created_paths)
    previous_history = list(previous_team.get("history", [])) if previous_team else []
    team["history"] = [*previous_history, history_entry]
    team["materialization"] = {
        "created_by": CREATED_BY,
        "execution_metadata": deepcopy(execution_metadata),
        "creates_runtime_team": False,
    }
    team["metadata"] = {
        **team.get("metadata", {}),
        "created_by": CREATED_BY,
        "source": "sandbox_team_materialization",
        "operational": False,
        "active": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }
    return validate_sandbox_team_schema(team)


def _select_agents(target: Path, *, agent_ids: list[str] | None) -> list[dict[str, Any]]:
    available = _load_sandbox_agents(target)
    if agent_ids is None:
        selected = available
    else:
        if not agent_ids:
            raise ValueError("team requiere al menos un agente")
        selected = []
        by_id = {agent["agent_id"]: agent for agent in available}
        for agent_id in agent_ids:
            normalized_agent_id = _normalize_id(agent_id)
            if normalized_agent_id not in by_id:
                raise FileNotFoundError(f"Agente sandbox inexistente para equipo: {normalized_agent_id}")
            selected.append(by_id[normalized_agent_id])
    if not selected:
        raise ValueError("team requiere sandbox_agents existentes")
    seen: set[str] = set()
    for agent in selected:
        agent_id = agent["agent_id"]
        if agent_id in seen:
            raise ValueError(f"agent_id duplicado en equipo: {agent_id}")
        seen.add(agent_id)
        _validate_agent_runtime_boundary(agent)
        validate_materialized_sandbox_agent(target, agent_id=agent_id)
    return selected


def _load_sandbox_agents(target: Path) -> list[dict[str, Any]]:
    root = _safe_child(target, SANDBOX_AGENTS_DIR)
    if not root.exists():
        return []
    agents = []
    for path in sorted(root.glob("*.json")):
        agent = json.loads(path.read_text(encoding="utf-8"))
        agent.setdefault("metadata", {})
        agent["metadata"] = {**agent["metadata"], "source_agent_path": str(path)}
        agents.append(agent)
    return agents


def _validate_agent_runtime_boundary(agent: dict[str, Any]) -> None:
    if agent.get("status") == ArtifactState.ACTIVE.value or agent.get("active") is True:
        raise ValueError("miembro de equipo no puede estar active")
    sandbox_config = agent.get("sandbox_config", {})
    if sandbox_config.get("runtime_enabled") is not False:
        raise ValueError("miembro de equipo requiere runtime_enabled=false")
    if sandbox_config.get("operational") is True:
        raise ValueError("miembro de equipo no puede ser operativo")


def _responsibility_from_agent(agent: dict[str, Any]) -> str:
    role_id = agent.get("role", {}).get("role_id") or "miembro"
    specialization_id = agent.get("specialization", {}).get("specialization_id") or "general"
    return f"Aporta rol {role_id} con especializacion {specialization_id} al equipo sandbox."


def _default_coordination_model(members: list[dict[str, Any]]) -> dict[str, Any]:
    order = [member["agent_id"] for member in members]
    return {
        "coordination_type": "parallel_review" if len(order) > 1 else "none",
        "coordinator_agent_id": order[0] if len(order) > 1 else None,
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": ["La coordinacion es declarativa; no ejecuta agentes."],
        "suggested_order": order,
        "restrictions": ["Sin debate runtime.", "Sin pipeline ejecutable."],
    }


def _validate_base_dependencies(manifest: dict[str, Any]) -> None:
    ids = {artifact["artifact_id"] for artifact in manifest.get("artifacts", [])}
    missing = [dependency for dependency in BASE_DEPENDENCIES if dependency not in ids]
    if missing:
        raise ValueError(f"equipo sandbox requiere dependencias base existentes: {missing}")


def _find_team_artifact_index(manifest: dict[str, Any], artifact_id: str) -> int | None:
    indexes = [
        index
        for index, artifact in enumerate(manifest.get("artifacts", []))
        if artifact.get("artifact_id") == artifact_id and artifact.get("artifact_type") == "team"
    ]
    if len(indexes) > 1:
        raise ValueError(f"artifact_manifest contiene multiples equipos para {artifact_id}")
    return indexes[0] if indexes else None


def _archive_current_team(domain_dir: Path, team_path: Path, *, previous_version: str) -> Path:
    if not team_path.is_file():
        raise FileNotFoundError("No se puede regenerar: falta equipo sandbox actual")
    history_dir = _safe_child(domain_dir, SANDBOX_TEAMS_DIR / "history")
    history_dir.mkdir(parents=True, exist_ok=True)
    history_path = _safe_child(
        domain_dir,
        SANDBOX_TEAMS_DIR
        / "history"
        / f"{team_path.stem}_{previous_version.replace('.', '_')}.json",
    )
    if history_path.exists():
        raise FileExistsError(f"Historial de equipo sandbox ya existe: {history_path.name}")
    shutil.copy2(team_path, history_path)
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
        raise ValueError(f"No se puede remover equipo sandbox; tiene dependientes: {dependents}")


def _team_paths(domain_dir: Path, raw_paths: list[str], team_id: str) -> list[Path]:
    paths: list[Path] = []
    team_root = _safe_child(domain_dir, SANDBOX_TEAMS_DIR)
    team_file = _safe_child(domain_dir, SANDBOX_TEAMS_DIR / f"{team_id}.json")
    for raw_path in raw_paths:
        path = Path(str(raw_path)).resolve()
        if path == team_file or (
            team_root in path.parents and path.name.startswith(f"{team_id}_")
        ):
            _safe_child(domain_dir, path.relative_to(domain_dir))
            paths.append(path)
    return _dedupe_paths(paths)


def _next_patch_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"version de equipo sandbox invalida: {version}")
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
        raise ValueError("equipo sandbox no puede escribirse en domains/ operativo")
    if path == agents_root or agents_root in path.parents:
        raise ValueError("equipo sandbox no puede escribirse en agents/ runtime")


def _normalize_id(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip())
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_value).strip("_")
    slug = re.sub(r"_+", "_", slug)
    if not slug:
        raise ValueError("id de equipo vacio")
    return slug


def _dedupe(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(paths))


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    return list(dict.fromkeys(paths))


def _now() -> str:
    return datetime.now().isoformat()
