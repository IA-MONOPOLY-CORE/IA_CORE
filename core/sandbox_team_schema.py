"""Contrato validable de equipo sandbox real sin ejecucion operativa."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from core.artifact_state import ArtifactState, coerce_artifact_state
from core.capability_policy_schema import validate_team_capability_policies
from core.sandbox_agent_memory_contract import validate_memory_contract
from core.sandbox_agent_tool_contract import validate_tool_contract


SANDBOX_TEAM_SCHEMA_VERSION = "1.0"
SANDBOX_TEAM_ARTIFACT_TYPE = "sandbox_team"
MANIFEST_ARTIFACT_TYPE = "team"
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
    "description",
    "team_type",
    "status",
    "artifact_state",
    "created_from",
    "source_team_template",
    "materialization_id",
    "artifact_id",
    "members",
    "coordination_model",
    "permissions",
    "execution_policy",
    "validation",
    "warnings",
    "metadata",
    "created_at",
    "updated_at",
}
MEMBER_REQUIRED_FIELDS = {
    "member_id",
    "role_id",
    "role_name",
    "agent_reference",
    "responsibilities",
    "inputs",
    "outputs",
    "status",
    "artifact_state",
}
LEGACY_MEMBER_REQUIRED_FIELDS = {
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
EXECUTION_POLICY_REQUIRED_FIELDS = {
    "execution_enabled",
    "runtime_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "external_integrations_enabled",
    "human_approval_required",
}
SENSITIVE_PERMISSION_FIELDS = {
    "can_execute",
    "can_call_tools",
    "can_call_models",
    "can_write_outputs",
    "can_access_network",
    "can_use_integrations",
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
    description: str | None = None,
    members: list[dict[str, Any]] | None = None,
    created_from: dict[str, Any] | None = None,
    source_team_template: dict[str, Any] | None = None,
    materialization_id: str | None = None,
    artifact_id: str | None = None,
    permissions: dict[str, Any] | None = None,
    execution_policy: dict[str, Any] | None = None,
    validation: dict[str, Any] | None = None,
    warnings: list[Any] | None = None,
    metadata: dict[str, Any] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye un contrato de equipo sandbox sin escribir archivos."""
    now = _now()
    canonical_members = deepcopy(members) if members is not None else [
        _member_agent_to_member(member) for member in member_agents
    ]
    dependencies = _expected_member_dependencies(canonical_members)
    team_artifact_id = artifact_id or f"team_{team_id}"
    payload = {
        "schema_version": SANDBOX_TEAM_SCHEMA_VERSION,
        "team_id": team_id,
        "domain_id": domain_id,
        "name": name,
        "description": description or purpose,
        "purpose": purpose,
        "team_type": "sandbox",
        "status": status,
        "artifact_state": status,
        "version": version,
        "created_from": deepcopy(created_from)
        if created_from is not None
        else {
            "source_type": "sandbox_team_schema",
            "schema": "core.sandbox_team_schema",
            "domain_id": domain_id,
        },
        "source_team_template": deepcopy(source_team_template)
        if source_team_template is not None
        else {
            "source_type": "derived_team_template",
            "team_template_id": f"{team_id}_template",
            "artifact_state": ArtifactState.DERIVED_PREVIEW.value,
            "operational": False,
        },
        "materialization_id": materialization_id or f"mat_{team_id}",
        "artifact_id": team_artifact_id,
        "members": canonical_members,
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
        "permissions": deepcopy(permissions) if permissions is not None else _default_permissions(),
        "execution_policy": deepcopy(execution_policy)
        if execution_policy is not None
        else _default_execution_policy(),
        "validation": deepcopy(validation)
        if validation is not None
        else {
            "schema_validated": True,
            "validator": "core.sandbox_team_schema.validate_sandbox_team_schema",
            "writes_files": False,
            "registers_operational_team": False,
        },
        "warnings": list(warnings or []),
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
            "artifact_type": SANDBOX_TEAM_ARTIFACT_TYPE,
            "manifest_artifact_type": MANIFEST_ARTIFACT_TYPE,
            "operational": False,
            "active": False,
            "creates_runtime_team": False,
            "schema_purpose": "contract_only",
            **deepcopy(metadata or {}),
        },
    }
    return validate_sandbox_team_schema(payload)


def validate_sandbox_team_schema(team: dict[str, Any]) -> dict[str, Any]:
    """Valida un equipo sandbox real sin crear ni ejecutar equipos."""
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
    _validate_non_empty_text(team.get("description"), "description")
    if "purpose" in team:
        _validate_non_empty_text(team.get("purpose"), "purpose")
    if team.get("team_type") != "sandbox":
        raise ValueError("team_type debe ser sandbox")
    _validate_status(team.get("status"), "sandbox team")
    _validate_status(team.get("artifact_state"), "artifact_state")
    _validate_runtime_flags(team, source="sandbox team")
    if "version" in team:
        _validate_version(team.get("version"))
    _validate_non_empty_object(team.get("created_from"), "created_from")
    _validate_non_empty_object(team.get("source_team_template"), "source_team_template")
    _validate_id(team.get("materialization_id"), "materialization_id")
    _validate_id(team.get("artifact_id"), "artifact_id")
    _validate_members(team.get("members"))
    if "member_agents" in team:
        _validate_legacy_members(team.get("member_agents"))
    _validate_coordination_model(team.get("coordination_model"), team["members"])
    _validate_permissions(team.get("permissions"))
    _validate_execution_policy(team.get("execution_policy"))
    _validate_non_empty_object(team.get("validation"), "validation")
    if not isinstance(team.get("warnings"), list):
        raise ValueError("warnings debe ser una lista")
    if not isinstance(team.get("metadata"), dict):
        raise ValueError("metadata debe ser un objeto")
    _validate_capabilities(team)
    expected_dependencies = _expected_member_dependencies(team["members"])
    if "dependencies" in team:
        _validate_dependencies(team.get("dependencies"), expected_dependencies)
    if "rollback_info" in team:
        _validate_rollback_info(team.get("rollback_info"), expected_dependencies)
    _validate_non_empty_text(team.get("created_at"), "created_at")
    _validate_non_empty_text(team.get("updated_at"), "updated_at")
    _ensure_json_serializable(team)
    return deepcopy(team)


def is_valid_sandbox_team(team: dict[str, Any]) -> bool:
    """Indica si un payload representa un equipo sandbox real valido."""
    try:
        validate_sandbox_team_schema(team)
    except ValueError:
        return False
    return True


def validate_sandbox_team_file(path: str | Path) -> dict[str, Any]:
    """Lee y valida un archivo JSON de equipo sandbox sin side effects."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"sandbox team no es JSON valido: {exc}") from exc
    return validate_sandbox_team_schema(payload)


def sandbox_team_to_artifact_record(team: dict[str, Any]) -> dict[str, Any]:
    """Representa el contrato como futuro registro `team` de artifact_manifest."""
    validated = validate_sandbox_team_schema(team)
    return {
        "artifact_id": validated["artifact_id"],
        "artifact_type": MANIFEST_ARTIFACT_TYPE,
        "name": validated["name"],
        "version": validated.get("version", "1.0.0"),
        "status": validated["status"],
        "created_from": {
            "source_type": "sandbox_team_contract",
            "domain_id": validated["domain_id"],
            "team_id": validated["team_id"],
            "artifact_kind": SANDBOX_TEAM_ARTIFACT_TYPE,
            "member_ids": [member["member_id"] for member in validated["members"]],
            "member_agent_ids": [
                member["agent_reference"]["agent_id"]
                for member in validated["members"]
                if isinstance(member.get("agent_reference"), dict)
                and member["agent_reference"].get("agent_id")
            ],
            "coordination_type": validated["coordination_model"]["coordination_type"],
            "source_team_template": deepcopy(validated["source_team_template"]),
            "materialization_id": validated["materialization_id"],
            "schema": "core.sandbox_team_schema",
        },
        "created_by": "core.sandbox_team_schema.sandbox_team_to_artifact_record",
        "dependencies": list(validated.get("dependencies", [])),
        "created_at": validated["created_at"],
        "updated_at": validated["updated_at"],
        "rollback_info": deepcopy(
            validated.get(
                "rollback_info",
                {
                    "created_paths": [],
                    "depends_on": list(validated.get("dependencies", [])),
                    "safe_remove": True,
                },
            )
        ),
        "operational": False,
        "passed": False,
    }


def _member_agent_to_member(member: dict[str, Any]) -> dict[str, Any]:
    agent_id = member.get("agent_id")
    role_id = member.get("role")
    specialization_id = member.get("specialization")
    source_reference = deepcopy(member.get("source_reference"))
    agent_reference = None
    if isinstance(source_reference, dict) and source_reference:
        agent_reference = {
            "agent_id": agent_id,
            **source_reference,
        }
    return {
        "member_id": agent_id,
        "role_id": role_id,
        "role_name": _humanize_id(role_id),
        "specialization_id": specialization_id,
        "specialization_name": _humanize_id(specialization_id),
        "agent_reference": agent_reference,
        "responsibilities": [member.get("responsibility")],
        "inputs": [],
        "outputs": [],
        "status": member.get("status"),
        "artifact_state": member.get("status"),
    }


def _validate_members(members: Any) -> None:
    if not isinstance(members, list) or not members:
        raise ValueError("members debe contener al menos un miembro")
    seen: set[str] = set()
    for member in members:
        if not isinstance(member, dict):
            raise ValueError("cada miembro debe ser un objeto")
        missing = MEMBER_REQUIRED_FIELDS - set(member)
        if missing:
            raise ValueError(f"miembro incompleto: {', '.join(sorted(missing))}")
        _validate_id(member.get("member_id"), "member.member_id")
        if member["member_id"] in seen:
            raise ValueError(f"member_id duplicado en equipo: {member['member_id']}")
        seen.add(member["member_id"])
        _validate_id(member.get("role_id"), "member.role_id")
        _validate_non_empty_text(member.get("role_name"), "member.role_name")
        if member.get("specialization_id") is not None:
            _validate_id(member.get("specialization_id"), "member.specialization_id")
        if member.get("specialization_name") is not None:
            _validate_non_empty_text(member.get("specialization_name"), "member.specialization_name")
        _validate_agent_reference(member.get("agent_reference"), member["member_id"])
        _validate_non_empty_string_list(member.get("responsibilities"), "member.responsibilities")
        for field in ["inputs", "outputs"]:
            if not isinstance(member.get(field), list):
                raise ValueError(f"member.{field} debe ser una lista")
        _validate_status(member.get("status"), "miembro de equipo")
        _validate_status(member.get("artifact_state"), "member.artifact_state")
        _validate_runtime_flags(member, source="team member")


def _validate_legacy_members(members: Any) -> None:
    if not isinstance(members, list) or not members:
        raise ValueError("member_agents debe contener al menos un miembro")
    seen: set[str] = set()
    for member in members:
        if not isinstance(member, dict):
            raise ValueError("cada member_agent debe ser un objeto")
        missing = LEGACY_MEMBER_REQUIRED_FIELDS - set(member)
        if missing:
            raise ValueError(f"member_agent incompleto: {', '.join(sorted(missing))}")
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
        _validate_status(member.get("status"), "miembro de equipo")
        _validate_runtime_flags(member, source="team member")


def _validate_agent_reference(reference: Any, member_id: str) -> None:
    if reference is None:
        return
    if not isinstance(reference, dict) or not reference:
        raise ValueError("member.agent_reference debe ser null o un objeto no vacio")
    if reference.get("agent_id") is not None:
        _validate_id(reference.get("agent_id"), "member.agent_reference.agent_id")
    artifact_id = reference.get("artifact_id")
    if artifact_id is not None:
        _validate_id(artifact_id, "member.agent_reference.artifact_id")
    if reference.get("operational") is True or reference.get("active") is True:
        raise ValueError(f"member {member_id} no puede referenciar agente operativo")


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
    member_ids = {member["member_id"] for member in members}
    if coordinator is not None:
        _validate_id(coordinator, "coordinator_agent_id")
        if coordinator not in member_ids:
            raise ValueError("coordinator_agent_id debe existir en members")
    for field in ["rules", "suggested_order", "restrictions"]:
        if not isinstance(model.get(field), list):
            raise ValueError(f"coordination_model.{field} debe ser una lista")
    for member_id in model.get("suggested_order", []):
        _validate_id(member_id, "coordination_model.suggested_order")
        if member_id not in member_ids:
            raise ValueError("suggested_order solo puede referenciar miembros")


def _validate_permissions(permissions: Any) -> None:
    if not isinstance(permissions, dict):
        raise ValueError("permissions debe ser un objeto")
    missing = SENSITIVE_PERMISSION_FIELDS - set(permissions)
    if missing:
        raise ValueError(f"permissions incompletas: {', '.join(sorted(missing))}")
    for field in SENSITIVE_PERMISSION_FIELDS:
        if permissions.get(field) is not False:
            raise ValueError(f"permissions.{field} debe ser false")
    _reject_nested_true_flags(permissions, "permissions")


def _validate_execution_policy(policy: Any) -> None:
    if not isinstance(policy, dict):
        raise ValueError("execution_policy debe ser un objeto")
    missing = EXECUTION_POLICY_REQUIRED_FIELDS - set(policy)
    if missing:
        raise ValueError(f"execution_policy incompleta: {', '.join(sorted(missing))}")
    for field in [
        "execution_enabled",
        "runtime_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ]:
        if policy.get(field) is not False:
            raise ValueError(f"execution_policy.{field} debe ser false")
    if policy.get("human_approval_required") is not True:
        raise ValueError("execution_policy.human_approval_required debe ser true")
    _reject_nested_true_flags(policy, "execution_policy")


def _validate_capabilities(team: dict[str, Any]) -> None:
    capabilities = team.get("capabilities")
    if capabilities is None:
        return
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
        if not _is_capability_policy(policy):
            _validate_policy(policy)
    validate_team_capability_policies(team)


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


def _is_capability_policy(policy: Any) -> bool:
    return isinstance(policy, dict) and "schema_version" in policy and "capability_id" in policy


def _expected_member_dependencies(members: list[dict[str, Any]]) -> list[str]:
    dependencies: list[str] = []
    for member in members:
        reference = member.get("agent_reference")
        if isinstance(reference, dict) and reference.get("artifact_id"):
            dependencies.append(reference["artifact_id"])
    return list(dict.fromkeys(dependencies))


def _validate_dependencies(dependencies: Any, expected: list[str]) -> None:
    if not isinstance(dependencies, list):
        raise ValueError("dependencies debe ser una lista")
    if dependencies != expected:
        raise ValueError("dependencies debe coincidir con los agentes miembros trazados")


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


def _validate_status(status: Any, source: str) -> None:
    coerced = coerce_artifact_state(status)
    if coerced is ArtifactState.ACTIVE:
        raise ValueError(f"{source} no puede estar active")
    if coerced not in {
        ArtifactState.READY_TO_MATERIALIZE,
        ArtifactState.MATERIALIZED,
        ArtifactState.VALIDATED,
        ArtifactState.CANDIDATE_FOR_ACTIVATION,
    }:
        raise ValueError(
            f"{source} solo permite status ready_to_materialize/materialized/validated/candidate"
        )


def _validate_runtime_flags(payload: dict[str, Any], *, source: str) -> None:
    if payload.get("runtime_enabled") is True:
        raise ValueError(f"{source} no puede tener runtime_enabled=true")
    if payload.get("execution_enabled") is True:
        raise ValueError(f"{source} no puede tener execution_enabled=true")
    if payload.get("tool_execution_enabled") is True:
        raise ValueError(f"{source} no puede tener tool_execution_enabled=true")
    if payload.get("model_invocation_enabled") is True:
        raise ValueError(f"{source} no puede tener model_invocation_enabled=true")
    if payload.get("external_integrations_enabled") is True:
        raise ValueError(f"{source} no puede tener external_integrations_enabled=true")
    if payload.get("active") is True:
        raise ValueError(f"{source} no puede tener active=true")


def _validate_declared_runtime_flags(payload: dict[str, Any], *, source: str) -> None:
    if payload.get("declared_only") is not True:
        raise ValueError(f"{source} debe tener declared_only=true")
    if payload.get("runtime_enabled") is not False:
        raise ValueError(f"{source} debe tener runtime_enabled=false")
    if payload.get("execution_enabled") is not False:
        raise ValueError(f"{source} debe tener execution_enabled=false")
    for flag in [
        "enabled",
        "execute",
        "executable",
        "execution_allowed",
        "external_access",
        "external_call",
        "pipeline_enabled",
        "debate_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ]:
        if payload.get(flag) is True:
            raise ValueError(f"{source} no puede declarar {flag}=true")


def _reject_nested_true_flags(payload: Any, source: str) -> None:
    blocked = {
        "active",
        "can_execute",
        "can_call_tools",
        "can_call_models",
        "can_write_outputs",
        "can_access_network",
        "can_use_integrations",
        "execution_enabled",
        "runtime_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
        "external_access",
        "execution_allowed",
    }
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in blocked and value is True:
                raise ValueError(f"{source}.{key} no puede ser true")
            _reject_nested_true_flags(value, source)
    elif isinstance(payload, list):
        for item in payload:
            _reject_nested_true_flags(item, source)


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


def _validate_non_empty_object(value: Any, field: str) -> None:
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{field} debe ser un objeto no vacio")


def _validate_non_empty_string_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} debe ser una lista no vacia")
    for item in value:
        _validate_non_empty_text(item, field)


def _ensure_json_serializable(team: dict[str, Any]) -> None:
    try:
        json.dumps(team, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("sandbox team debe ser serializable como JSON") from exc


def _default_execution_policy() -> dict[str, bool]:
    return {
        "execution_enabled": False,
        "runtime_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "external_integrations_enabled": False,
        "human_approval_required": True,
    }


def _default_permissions() -> dict[str, bool]:
    return {
        "can_execute": False,
        "can_call_tools": False,
        "can_call_models": False,
        "can_write_outputs": False,
        "can_access_network": False,
        "can_use_integrations": False,
    }


def _humanize_id(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        return "General"
    return value.replace("_", " ").strip().title()


def _now() -> str:
    return datetime.now().isoformat()
