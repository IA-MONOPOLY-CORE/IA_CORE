"""Contrato validable de equipo sandbox previo a materializacion operativa."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any

from core.artifact_state import ArtifactState, coerce_artifact_state
from core.sandbox_agent_memory_contract import validate_memory_contract
from core.sandbox_agent_tool_contract import validate_tool_contract


SANDBOX_TEAM_SCHEMA_VERSION = "1.0"
ALLOWED_COORDINATION_TYPES = {
    "none",
    "single_coordinator",
    "parallel_review",
    "sequential_pipeline",
    "debate_future",
    "approval_future",
}
REQUIRED_FIELDS = {
    "schema_version",
    "team_id",
    "domain_id",
    "name",
    "purpose",
    "status",
    "version",
    "member_agents",
    "coordination_model",
    "capabilities",
    "dependencies",
    "rollback_info",
    "created_at",
    "updated_at",
}
MEMBER_REQUIRED_FIELDS = {
    "agent_id",
    "role",
    "specialization",
    "responsibility",
    "required",
    "source_reference",
    "status",
}
COORDINATION_REQUIRED_FIELDS = {
    "coordination_type",
    "declared_only",
    "runtime_enabled",
    "execution_enabled",
    "rules",
    "suggested_order",
    "restrictions",
}
POLICY_REQUIRED_FIELDS = {
    "policy_id",
    "status",
    "declared_only",
    "runtime_enabled",
    "execution_enabled",
    "external_access",
}


def build_sandbox_team_schema(
    *,
    team_id: str,
    domain_id: str,
    name: str,
    purpose: str,
    member_agents: list[dict[str, Any]],
    coordination_model: dict[str, Any] | None = None,
    capabilities: dict[str, Any] | None = None,
    version: str = "1.0.0",
    status: str = ArtifactState.MATERIALIZED.value,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye un contrato de equipo sandbox sin escribir archivos."""
    now = _now()
    dependencies = [f"agent_{member['agent_id']}" for member in member_agents]
    payload = {
        "schema_version": SANDBOX_TEAM_SCHEMA_VERSION,
        "team_id": team_id,
        "domain_id": domain_id,
        "name": name,
        "purpose": purpose,
        "status": status,
        "version": version,
        "member_agents": deepcopy(member_agents),
        "coordination_model": deepcopy(coordination_model)
        if coordination_model is not None
        else {
            "coordination_type": "none",
            "coordinator_agent_id": None,
            "declared_only": True,
            "runtime_enabled": False,
            "execution_enabled": False,
            "rules": [],
            "suggested_order": [],
            "restrictions": [],
        },
        "capabilities": deepcopy(capabilities)
        if capabilities is not None
        else {
            "memory": [],
            "tools": [],
            "policies": [],
        },
        "dependencies": dependencies,
        "rollback_info": {
            "created_paths": [],
            "depends_on": dependencies,
            "safe_remove": True,
        },
        "created_at": created_at or now,
        "updated_at": updated_at or now,
        "metadata": {
            "artifact_type": "team",
            "operational": False,
            "active": False,
            "creates_runtime_team": False,
            "schema_purpose": "contract_only",
        },
    }
    return validate_sandbox_team_schema(payload)


def validate_sandbox_team_schema(team: dict[str, Any]) -> dict[str, Any]:
    """Valida el contrato de equipo sandbox sin crear ni ejecutar equipos."""
    if not isinstance(team, dict):
        raise ValueError("sandbox team debe ser un objeto")
    missing = REQUIRED_FIELDS - set(team)
    if missing:
        raise ValueError(f"sandbox team incompleto: {', '.join(sorted(missing))}")
    if team.get("schema_version") != SANDBOX_TEAM_SCHEMA_VERSION:
        raise ValueError("schema_version de sandbox team invalida")
    _validate_id(team.get("team_id"), "team_id")
    _validate_id(team.get("domain_id"), "domain_id")
    _validate_non_empty_text(team.get("name"), "name")
    _validate_non_empty_text(team.get("purpose"), "purpose")
    _validate_status(team.get("status"))
    _validate_runtime_flags(team, source="sandbox team")
    _validate_version(team.get("version"))
    _validate_members(team.get("member_agents"))
    _validate_coordination_model(team.get("coordination_model"), team["member_agents"])
    _validate_capabilities(team.get("capabilities"))
    expected_dependencies = [f"agent_{member['agent_id']}" for member in team["member_agents"]]
    _validate_dependencies(team.get("dependencies"), expected_dependencies)
    _validate_rollback_info(team.get("rollback_info"), expected_dependencies)
    _validate_non_empty_text(team.get("created_at"), "created_at")
    _validate_non_empty_text(team.get("updated_at"), "updated_at")
    _ensure_json_serializable(team)
    return deepcopy(team)


def sandbox_team_to_artifact_record(team: dict[str, Any]) -> dict[str, Any]:
    """Representa el contrato como futuro registro `team` de artifact_manifest."""
    validated = validate_sandbox_team_schema(team)
    return {
        "artifact_id": f"team_{validated['team_id']}",
        "artifact_type": "team",
        "name": validated["name"],
        "version": validated["version"],
        "status": validated["status"],
        "created_from": {
            "source_type": "sandbox_team_contract",
            "domain_id": validated["domain_id"],
            "team_id": validated["team_id"],
            "member_agent_ids": [member["agent_id"] for member in validated["member_agents"]],
            "coordination_type": validated["coordination_model"]["coordination_type"],
            "schema": "core.sandbox_team_schema",
        },
        "created_by": "core.sandbox_team_schema.sandbox_team_to_artifact_record",
        "dependencies": list(validated["dependencies"]),
        "created_at": validated["created_at"],
        "updated_at": validated["updated_at"],
        "rollback_info": deepcopy(validated["rollback_info"]),
        "operational": False,
        "passed": False,
    }


def _validate_members(members: Any) -> None:
    if not isinstance(members, list) or not members:
        raise ValueError("member_agents debe contener al menos un miembro")
    seen: set[str] = set()
    for member in members:
        if not isinstance(member, dict):
            raise ValueError("cada miembro debe ser un objeto")
        missing = MEMBER_REQUIRED_FIELDS - set(member)
        if missing:
            raise ValueError(f"miembro incompleto: {', '.join(sorted(missing))}")
        _validate_id(member.get("agent_id"), "member.agent_id")
        if member["agent_id"] in seen:
            raise ValueError(f"agent_id duplicado en equipo: {member['agent_id']}")
        seen.add(member["agent_id"])
        _validate_non_empty_text(member.get("role"), "member.role")
        _validate_non_empty_text(member.get("specialization"), "member.specialization")
        _validate_non_empty_text(member.get("responsibility"), "member.responsibility")
        if not isinstance(member.get("required"), bool):
            raise ValueError("member.required debe ser booleano")
        if not isinstance(member.get("source_reference"), dict) or not member["source_reference"]:
            raise ValueError("member.source_reference debe ser un objeto no vacio")
        _validate_member_status(member.get("status"))
        _validate_runtime_flags(member, source="team member")


def _validate_coordination_model(model: Any, members: list[dict[str, Any]]) -> None:
    if not isinstance(model, dict):
        raise ValueError("coordination_model debe ser un objeto")
    missing = COORDINATION_REQUIRED_FIELDS - set(model)
    if missing:
        raise ValueError(f"coordination_model incompleto: {', '.join(sorted(missing))}")
    if model.get("coordination_type") not in ALLOWED_COORDINATION_TYPES:
        raise ValueError(f"coordination_type invalido: {model.get('coordination_type')}")
    _validate_declared_runtime_flags(model, source="coordination_model")
    coordinator = model.get("coordinator_agent_id")
    member_ids = {member["agent_id"] for member in members}
    if coordinator is not None:
        _validate_id(coordinator, "coordinator_agent_id")
        if coordinator not in member_ids:
            raise ValueError("coordinator_agent_id debe existir en member_agents")
    for field in ["rules", "suggested_order", "restrictions"]:
        if not isinstance(model.get(field), list):
            raise ValueError(f"coordination_model.{field} debe ser una lista")
    for agent_id in model.get("suggested_order", []):
        _validate_id(agent_id, "coordination_model.suggested_order")
        if agent_id not in member_ids:
            raise ValueError("suggested_order solo puede referenciar miembros")


def _validate_capabilities(capabilities: Any) -> None:
    if not isinstance(capabilities, dict):
        raise ValueError("capabilities debe ser un objeto")
    if set(capabilities) - {"memory", "tools", "policies"}:
        raise ValueError("capabilities solo acepta memory, tools y policies")
    memory = capabilities.get("memory", [])
    tools = capabilities.get("tools", [])
    policies = capabilities.get("policies", [])
    for field, value in [("memory", memory), ("tools", tools), ("policies", policies)]:
        if not isinstance(value, list):
            raise ValueError(f"capabilities.{field} debe ser una lista")
    for contract in memory:
        validate_memory_contract(contract)
    for contract in tools:
        validate_tool_contract(contract)
    for policy in policies:
        _validate_policy(policy)


def _validate_policy(policy: Any) -> None:
    if not isinstance(policy, dict):
        raise ValueError("policy capability debe ser un objeto")
    missing = POLICY_REQUIRED_FIELDS - set(policy)
    if missing:
        raise ValueError(f"policy capability incompleta: {', '.join(sorted(missing))}")
    _validate_id(policy.get("policy_id"), "policy_id")
    if policy.get("status") != "declared":
        raise ValueError("policy capability solo permite status declared")
    _validate_declared_runtime_flags(policy, source="policy capability")


def _validate_dependencies(dependencies: Any, expected: list[str]) -> None:
    if not isinstance(dependencies, list):
        raise ValueError("dependencies debe ser una lista")
    if dependencies != expected:
        raise ValueError("dependencies debe coincidir con los agentes miembros")


def _validate_rollback_info(rollback: Any, expected_dependencies: list[str]) -> None:
    if not isinstance(rollback, dict):
        raise ValueError("rollback_info debe ser un objeto")
    for field in ["created_paths", "depends_on", "safe_remove"]:
        if field not in rollback:
            raise ValueError(f"rollback_info incompleto: {field}")
    if not isinstance(rollback["created_paths"], list):
        raise ValueError("rollback_info.created_paths debe ser una lista")
    if rollback["depends_on"] != expected_dependencies:
        raise ValueError("rollback_info.depends_on debe coincidir con dependencies")
    if rollback["safe_remove"] is not True:
        raise ValueError("rollback_info.safe_remove debe ser true")


def _validate_status(status: Any) -> None:
    coerced = coerce_artifact_state(status)
    if coerced is ArtifactState.ACTIVE:
        raise ValueError("sandbox team no puede estar active")
    if coerced is not ArtifactState.MATERIALIZED:
        raise ValueError("sandbox team solo permite status materialized en esta fase")


def _validate_member_status(status: Any) -> None:
    coerced = coerce_artifact_state(status)
    if coerced is ArtifactState.ACTIVE:
        raise ValueError("miembro de equipo no puede estar active")
    if coerced not in {ArtifactState.READY_TO_MATERIALIZE, ArtifactState.MATERIALIZED}:
        raise ValueError(f"status de miembro no permitido: {status}")


def _validate_runtime_flags(payload: dict[str, Any], *, source: str) -> None:
    if payload.get("runtime_enabled") is True:
        raise ValueError(f"{source} no puede tener runtime_enabled=true")
    if payload.get("execution_enabled") is True:
        raise ValueError(f"{source} no puede tener execution_enabled=true")
    if payload.get("active") is True:
        raise ValueError(f"{source} no puede tener active=true")


def _validate_declared_runtime_flags(payload: dict[str, Any], *, source: str) -> None:
    if payload.get("declared_only") is not True:
        raise ValueError(f"{source} debe tener declared_only=true")
    if payload.get("runtime_enabled") is not False:
        raise ValueError(f"{source} debe tener runtime_enabled=false")
    if payload.get("execution_enabled") is not False:
        raise ValueError(f"{source} debe tener execution_enabled=false")
    for flag in ["enabled", "executable", "execution_allowed", "external_access", "external_call"]:
        if payload.get(flag) is True:
            raise ValueError(f"{source} no puede declarar {flag}=true")


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


def _ensure_json_serializable(team: dict[str, Any]) -> None:
    try:
        json.dumps(team, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("sandbox team debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
