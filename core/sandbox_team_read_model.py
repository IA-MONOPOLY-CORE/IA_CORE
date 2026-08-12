"""Read model interno de equipos sandbox sin operacion runtime."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import config
from core.sandbox_team_materializer import (
    SANDBOX_TEAMS_DIR,
    validate_materialized_sandbox_team,
)


READ_MODEL_STATUS = "SANDBOX_TEAM_READ_MODEL_READY"
READ_MODEL_VERDICT = "SANDBOX_TEAM_INTERNAL_LISTING_NO_OPERATIONAL_CONFIRMED"
READ_MODEL_READINESS = "ready_for_next_architecture_block_after_phase_5"
TEAM_LISTABLE_READINESS = "sandbox_team_non_operational_confirmed"
TEAM_INVALID_READINESS = "sandbox_team_invalid"
ARTIFACT_TYPE = "team"
ARTIFACT_KIND = "sandbox_team"
SENSITIVE_PERMISSION_FIELDS = {
    "can_execute",
    "can_call_tools",
    "can_call_models",
    "can_write_outputs",
    "can_access_network",
    "can_use_integrations",
}
EXECUTION_POLICY_FIELDS = {
    "execution_enabled",
    "runtime_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "external_integrations_enabled",
    "human_approval_required",
}
FORBIDDEN_PAYLOAD_FRAGMENTS = {
    "api_key",
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "env",
    "environment",
    "model_config",
    "model_provider_config",
    "password",
    "raw_prompt",
    "raw_payload",
    "runtime_handle",
    "secret",
    "token",
    "tool_config",
    "tool_runtime",
}
FORBIDDEN_TOP_LEVEL_FIELDS = {
    "agent_reference",
    "member_agents",
    "capabilities",
    "coordination_model",
    "rollback_info",
    "history",
    "materialization",
}


def list_sandbox_teams(domain_dir: str | Path) -> dict[str, Any]:
    """Lista equipos sandbox materializados en un dominio sandbox controlado."""
    target = _safe_domain_dir(domain_dir)
    teams_dir = _safe_child(target, SANDBOX_TEAMS_DIR)
    team_ids = []
    if teams_dir.exists():
        team_ids = sorted(
            path.stem
            for path in teams_dir.glob("*.json")
            if not path.name.endswith(".manifest.json")
        )
    teams = [
        get_sandbox_team_summary(target, team_id=team_id)
        for team_id in team_ids
    ]
    payload = {
        "status": "listed",
        "verdict": READ_MODEL_VERDICT,
        "readiness": READ_MODEL_READINESS,
        "read_model": "sandbox_team_internal_listing",
        "read_only": True,
        "operational": False,
        "passed": False,
        "domain_dir": str(target),
        "teams_count": len(teams),
        "teams": teams,
        "boundary_summary": _boundary_summary(),
    }
    _ensure_json_safe(payload)
    return payload


def get_sandbox_team_summary(domain_dir: str | Path, *, team_id: str) -> dict[str, Any]:
    """Construye summary seguro de un equipo sandbox materializado."""
    validation = validate_materialized_sandbox_team(domain_dir, team_id=team_id)
    return build_sandbox_team_read_model(validation)


def build_sandbox_team_read_model(validation: dict[str, Any]) -> dict[str, Any]:
    """Proyecta informacion segura desde team, team_manifest y artifact_manifest."""
    team = deepcopy(validation.get("team") or {})
    artifact = deepcopy(validation.get("artifact") or {})
    team_manifest = deepcopy(validation.get("team_manifest") or {})
    artifact_kind = artifact.get("created_from", {}).get("artifact_kind") or team_manifest.get("artifact_kind")
    payload = {
        "team_id": team.get("team_id", ""),
        "domain_id": team.get("domain_id", ""),
        "name": team.get("name", ""),
        "description": team.get("description", ""),
        "team_type": team.get("team_type", ""),
        "status": team.get("status", ""),
        "artifact_state": team.get("artifact_state", ""),
        "artifact_id": team.get("artifact_id", ""),
        "artifact_type": artifact.get("artifact_type", ARTIFACT_TYPE),
        "artifact_kind": artifact_kind,
        "materialization_id": team.get("materialization_id", ""),
        "source_team_template": deepcopy(team.get("source_team_template") or {}),
        "members_count": len(team.get("members") or []),
        "members_summary": _members_summary(team.get("members") or []),
        "permissions_summary": _permissions_summary(team.get("permissions") or {}),
        "execution_policy_summary": _execution_policy_summary(team.get("execution_policy") or {}),
        "operational": artifact.get("operational") is True,
        "passed": artifact.get("passed") is True,
        "readiness": TEAM_LISTABLE_READINESS,
        "warnings": list(team.get("warnings") or []),
        "validation": _validation_summary(team, team_manifest, artifact),
        "created_at": team.get("created_at", ""),
        "updated_at": team.get("updated_at", ""),
        "metadata": _metadata_summary(team.get("metadata") or {}),
    }
    return validate_sandbox_team_read_model(payload)


def validate_sandbox_team_read_model(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida un payload de listado interno sin escribir ni ejecutar."""
    if not isinstance(payload, dict):
        raise ValueError("sandbox team read model debe ser un objeto")
    required = {
        "team_id",
        "domain_id",
        "name",
        "description",
        "team_type",
        "status",
        "artifact_state",
        "artifact_id",
        "artifact_type",
        "artifact_kind",
        "materialization_id",
        "source_team_template",
        "members_count",
        "members_summary",
        "permissions_summary",
        "execution_policy_summary",
        "operational",
        "passed",
        "readiness",
        "warnings",
        "validation",
        "created_at",
        "updated_at",
        "metadata",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"sandbox team read model incompleto: {', '.join(sorted(missing))}")
    for field in ["team_id", "domain_id", "name", "description", "artifact_id", "materialization_id"]:
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError(f"{field} requerido")
    if payload.get("team_type") != "sandbox":
        raise ValueError("team_type debe ser sandbox")
    if payload.get("status") == "active" or payload.get("artifact_state") == "active":
        raise ValueError("sandbox team read model no puede representar active")
    if payload.get("artifact_type") != ARTIFACT_TYPE:
        raise ValueError("artifact_type debe ser team")
    if payload.get("artifact_kind") != ARTIFACT_KIND:
        raise ValueError("artifact_kind debe ser sandbox_team")
    if payload.get("operational") is not False:
        raise ValueError("operational debe ser false")
    if payload.get("passed") is not False:
        raise ValueError("passed debe ser false")
    if payload.get("readiness") in {
        "ready_for_runtime",
        "ready_for_execution",
        "runtime_open",
        "runtime_active",
        "execution_enabled",
        "operational",
    }:
        raise ValueError("readiness no puede sugerir operacion real")
    _validate_members_summary(payload)
    _validate_permissions_summary(payload.get("permissions_summary"))
    _validate_execution_policy_summary(payload.get("execution_policy_summary"))
    _reject_forbidden_fields(payload)
    _ensure_json_safe(payload)
    return deepcopy(payload)


def _members_summary(members: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for member in members:
        reference = member.get("agent_reference")
        summary.append(
            {
                "member_id": member.get("member_id", ""),
                "role_id": member.get("role_id", ""),
                "role_name": member.get("role_name", ""),
                "specialization_id": member.get("specialization_id"),
                "specialization_name": member.get("specialization_name"),
                "has_agent_reference": isinstance(reference, dict) and bool(reference),
                "responsibilities_count": len(member.get("responsibilities") or []),
                "status": member.get("status", ""),
                "artifact_state": member.get("artifact_state", ""),
            }
        )
    return summary


def _permissions_summary(permissions: dict[str, Any]) -> dict[str, bool]:
    return {field: permissions.get(field) is True for field in sorted(SENSITIVE_PERMISSION_FIELDS)}


def _execution_policy_summary(policy: dict[str, Any]) -> dict[str, bool]:
    return {
        "execution_enabled": policy.get("execution_enabled") is True,
        "runtime_enabled": policy.get("runtime_enabled") is True,
        "tool_execution_enabled": policy.get("tool_execution_enabled") is True,
        "model_invocation_enabled": policy.get("model_invocation_enabled") is True,
        "external_integrations_enabled": policy.get("external_integrations_enabled") is True,
        "human_approval_required": policy.get("human_approval_required") is True,
    }


def _validation_summary(
    team: dict[str, Any],
    team_manifest: dict[str, Any],
    artifact: dict[str, Any],
) -> dict[str, Any]:
    return {
        "team_schema_valid": True,
        "team_manifest_present": bool(team_manifest),
        "artifact_manifest_present": bool(artifact),
        "artifact_manifest_coherent": True,
        "non_operational_confirmed": True,
        "members_declarative": True,
        "permissions_blocked": True,
        "execution_policy_blocked": True,
        "source_team_template_traced": bool(team.get("source_team_template")),
    }


def _metadata_summary(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": metadata.get("artifact_type"),
        "manifest_artifact_type": metadata.get("manifest_artifact_type"),
        "source": metadata.get("source"),
        "operational": metadata.get("operational") is True,
        "active": metadata.get("active") is True,
        "template_derived": metadata.get("template_derived") is True,
    }


def _validate_members_summary(payload: dict[str, Any]) -> None:
    members = payload.get("members_summary")
    if not isinstance(members, list):
        raise ValueError("members_summary debe ser lista")
    if payload.get("members_count") != len(members):
        raise ValueError("members_count no coincide con members_summary")
    for member in members:
        if not isinstance(member, dict):
            raise ValueError("members_summary solo acepta objetos")
        allowed = {
            "member_id",
            "role_id",
            "role_name",
            "specialization_id",
            "specialization_name",
            "has_agent_reference",
            "responsibilities_count",
            "status",
            "artifact_state",
        }
        if set(member) != allowed:
            raise ValueError("members_summary contiene campos no permitidos")
        if member.get("status") == "active" or member.get("artifact_state") == "active":
            raise ValueError("members_summary no puede representar active")
        if not isinstance(member.get("has_agent_reference"), bool):
            raise ValueError("has_agent_reference debe ser booleano")
        if not isinstance(member.get("responsibilities_count"), int):
            raise ValueError("responsibilities_count debe ser entero")


def _validate_permissions_summary(summary: Any) -> None:
    if not isinstance(summary, dict):
        raise ValueError("permissions_summary debe ser objeto")
    missing = SENSITIVE_PERMISSION_FIELDS - set(summary)
    if missing:
        raise ValueError(f"permissions_summary incompleto: {', '.join(sorted(missing))}")
    for field in SENSITIVE_PERMISSION_FIELDS:
        if summary.get(field) is not False:
            raise ValueError(f"permissions_summary.{field} debe ser false")


def _validate_execution_policy_summary(summary: Any) -> None:
    if not isinstance(summary, dict):
        raise ValueError("execution_policy_summary debe ser objeto")
    missing = EXECUTION_POLICY_FIELDS - set(summary)
    if missing:
        raise ValueError(f"execution_policy_summary incompleto: {', '.join(sorted(missing))}")
    for field in EXECUTION_POLICY_FIELDS - {"human_approval_required"}:
        if summary.get(field) is not False:
            raise ValueError(f"execution_policy_summary.{field} debe ser false")
    if summary.get("human_approval_required") is not True:
        raise ValueError("execution_policy_summary.human_approval_required debe ser true")


def _reject_forbidden_fields(payload: Any) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_TOP_LEVEL_FIELDS:
                raise ValueError(f"campo prohibido en read model: {key}")
            if any(fragment == lowered or fragment in lowered for fragment in FORBIDDEN_PAYLOAD_FRAGMENTS):
                raise ValueError(f"campo sensible prohibido en read model: {key}")
            _reject_forbidden_fields(value)
    elif isinstance(payload, list):
        for item in payload:
            _reject_forbidden_fields(item)


def _boundary_summary() -> dict[str, bool]:
    return {
        "read_only": True,
        "writes_enabled": False,
        "creates_teams": False,
        "creates_agents": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "ui_enabled": False,
        "integrations_enabled": False,
    }


def _ensure_json_safe(payload: Any) -> None:
    try:
        json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("sandbox team read model debe ser JSON-safe") from exc


def _safe_domain_dir(domain_dir: str | Path) -> Path:
    target = Path(domain_dir).resolve()
    _reject_operational_paths(target)
    return target


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
        raise ValueError("read model de equipos sandbox no puede leer domains/ operativo")
    if path == agents_root or agents_root in path.parents:
        raise ValueError("read model de equipos sandbox no puede leer agents/ runtime")
