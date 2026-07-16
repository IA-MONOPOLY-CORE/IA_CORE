"""Politica declarativa comun para capabilities de agentes y equipos sandbox."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


CAPABILITY_POLICY_SCHEMA_VERSION = "1.0"

ALLOWED_SUBJECT_TYPES = {"agent", "team"}
ALLOWED_CAPABILITY_TYPES = {"memory", "tool", "policy"}
ALLOWED_POLICY_STATUSES = {
    "declared",
    "allowed_declared",
    "blocked",
    "forbidden",
    "future_requires_approval",
}
ALLOWED_APPROVAL_STATUSES = {
    "not_required",
    "future_required",
    "missing",
    "not_evaluated",
}

CAPABILITY_STATUSES_BY_TYPE = {
    "memory": {"declared", "allowed_declared", "future_requires_approval", "blocked"},
    "tool": {
        "declared",
        "allowed_declared",
        "future_requires_approval",
        "blocked",
        "forbidden",
    },
    "policy": {"declared", "allowed_declared", "future_requires_approval"},
}

REQUIRED_FIELDS = {
    "schema_version",
    "policy_id",
    "domain_id",
    "subject_type",
    "subject_id",
    "capability_type",
    "capability_id",
    "capability_category",
    "policy_status",
    "declared_only",
    "allowed_by_policy",
    "requires_approval",
    "approval_status",
    "runtime_enabled",
    "execution_allowed",
    "external_access",
    "restrictions",
    "audit_requirements",
    "dependencies",
    "created_at",
    "updated_at",
}

BLOCKED_MARKERS = {
    "api_call",
    "api_call_real",
    "auto_escalation",
    "browser_automation",
    "browser_automation_real",
    "calendar_automation",
    "email_automation",
    "external_call",
    "filesystem_write",
    "filesystem_write_real",
    "persistence_operativa_real",
    "real_persistence",
    "runtime_mutation",
    "self_approval",
    "storage_backend_real",
    "vector_store_real",
}

TEAM_MEMBER_AUTO_GRANT_FLAGS = {
    "auto_apply_to_members",
    "auto_enable_members",
    "grant_to_members",
    "inherits_to_members",
}


def build_capability_policy(
    *,
    policy_id: str,
    domain_id: str,
    subject_type: str,
    subject_id: str,
    capability_type: str,
    capability_id: str,
    capability_category: str,
    policy_status: str = "declared",
    allowed_by_policy: bool | None = None,
    requires_approval: bool | None = None,
    approval_status: str | None = None,
    restrictions: list[Any] | None = None,
    audit_requirements: list[Any] | None = None,
    dependencies: list[str] | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Construye una policy declarativa sin activar capability alguna."""
    now = _now()
    if allowed_by_policy is None:
        allowed_by_policy = policy_status == "allowed_declared"
    if requires_approval is None:
        requires_approval = policy_status == "future_requires_approval"
    if approval_status is None:
        approval_status = "future_required" if requires_approval else "not_required"
    payload = {
        "schema_version": CAPABILITY_POLICY_SCHEMA_VERSION,
        "policy_id": policy_id,
        "domain_id": domain_id,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "capability_type": capability_type,
        "capability_id": capability_id,
        "capability_category": capability_category,
        "policy_status": policy_status,
        "declared_only": True,
        "allowed_by_policy": allowed_by_policy,
        "requires_approval": requires_approval,
        "approval_status": approval_status,
        "runtime_enabled": False,
        "execution_allowed": False,
        "external_access": False,
        "restrictions": list(restrictions or []),
        "audit_requirements": list(audit_requirements or []),
        "dependencies": list(dependencies or []),
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_capability_policy(payload)


def validate_capability_policy(policy: dict[str, Any]) -> dict[str, Any]:
    """Valida una capability policy sin crear permisos ni runtime."""
    if not isinstance(policy, dict):
        raise ValueError("capability_policy debe ser un objeto")
    missing = REQUIRED_FIELDS - set(policy)
    if missing:
        raise ValueError(f"capability_policy incompleta: {', '.join(sorted(missing))}")
    if policy.get("schema_version") != CAPABILITY_POLICY_SCHEMA_VERSION:
        raise ValueError("schema_version de capability_policy invalida")

    _validate_id(policy.get("policy_id"), "policy_id")
    _validate_id(policy.get("domain_id"), "domain_id")
    if policy.get("subject_type") not in ALLOWED_SUBJECT_TYPES:
        raise ValueError(f"subject_type invalido: {policy.get('subject_type')}")
    _validate_id(policy.get("subject_id"), "subject_id")
    capability_type = policy.get("capability_type")
    if capability_type not in ALLOWED_CAPABILITY_TYPES:
        raise ValueError(f"capability_type invalido: {capability_type}")
    _validate_id(policy.get("capability_id"), "capability_id")
    _validate_non_empty_text(policy.get("capability_category"), "capability_category")
    _validate_policy_status(policy)
    _validate_policy_booleans(policy)
    _validate_restrictions(policy)
    _validate_list(policy.get("audit_requirements"), "audit_requirements")
    _validate_dependencies(policy.get("dependencies"))
    _validate_non_empty_text(policy.get("created_at"), "created_at")
    _validate_non_empty_text(policy.get("updated_at"), "updated_at")
    _ensure_json_serializable(policy)
    return deepcopy(policy)


def validate_capability_policy_for_subject(
    policy: dict[str, Any],
    *,
    subject_type: str,
    subject_id: str,
    domain_id: str,
) -> dict[str, Any]:
    """Valida que la policy pertenezca al sujeto sandbox esperado."""
    validated = validate_capability_policy(policy)
    if validated["subject_type"] != subject_type:
        raise ValueError("capability_policy no corresponde al subject_type esperado")
    if validated["subject_id"] != subject_id:
        raise ValueError("capability_policy no corresponde al subject_id esperado")
    if validated["domain_id"] != domain_id:
        raise ValueError("capability_policy no corresponde al domain_id esperado")
    return validated


def validate_agent_capability_policies(agent: dict[str, Any]) -> list[dict[str, Any]]:
    """Valida policies embebidas de agente sin exigirlas retroactivamente."""
    capabilities = agent.get("capabilities")
    if not isinstance(capabilities, dict):
        return []
    policies = capabilities.get("policies", [])
    if not isinstance(policies, list):
        raise ValueError("capabilities.policies debe ser una lista")
    return [
        validate_capability_policy_for_subject(
            policy,
            subject_type="agent",
            subject_id=agent["agent_id"],
            domain_id=agent["domain_id"],
        )
        for policy in policies
    ]


def validate_team_capability_policies(team: dict[str, Any]) -> list[dict[str, Any]]:
    """Valida policies embebidas de equipo y bloquea permisos heredados automaticos."""
    capabilities = team.get("capabilities")
    if not isinstance(capabilities, dict):
        return []
    policies = capabilities.get("policies", [])
    if not isinstance(policies, list):
        raise ValueError("capabilities.policies debe ser una lista")

    validated = []
    for policy in policies:
        if _looks_like_legacy_policy_capability(policy):
            continue
        validated_policy = validate_capability_policy_for_subject(
            policy,
            subject_type="team",
            subject_id=team["team_id"],
            domain_id=team["domain_id"],
        )
        validate_team_policy_member_boundary(validated_policy)
        validated.append(validated_policy)
    return validated


def validate_team_policy_member_boundary(policy: dict[str, Any]) -> dict[str, Any]:
    """Evita que una policy del equipo active automaticamente a sus miembros."""
    validated = validate_capability_policy(policy)
    if validated["subject_type"] != "team":
        raise ValueError("solo una policy de equipo puede validar frontera de miembros")
    for field in ("restrictions", "audit_requirements"):
        _reject_team_member_auto_grants(validated.get(field, []), field)
    return validated


def evaluate_capability_policy_status(
    *,
    capability_id: str,
    policies: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Devuelve estado declarativo cuando una capability aun no tiene policy."""
    _validate_id(capability_id, "capability_id")
    policies = list(policies or [])
    for policy in policies:
        validated = validate_capability_policy(policy)
        if validated["capability_id"] == capability_id:
            return {
                "capability_id": capability_id,
                "policy_status": validated["policy_status"],
                "approval_status": validated["approval_status"],
                "allowed_by_policy": validated["allowed_by_policy"],
                "requires_approval": validated["requires_approval"],
            }
    return {
        "capability_id": capability_id,
        "policy_status": "missing",
        "approval_status": "not_evaluated",
        "allowed_by_policy": False,
        "requires_approval": False,
    }


def _validate_policy_status(policy: dict[str, Any]) -> None:
    status = policy.get("policy_status")
    capability_type = policy.get("capability_type")
    if status not in ALLOWED_POLICY_STATUSES:
        raise ValueError(f"policy_status invalido: {status}")
    if status not in CAPABILITY_STATUSES_BY_TYPE[capability_type]:
        raise ValueError(f"policy_status {status} no permitido para {capability_type}")
    if policy.get("approval_status") not in ALLOWED_APPROVAL_STATUSES:
        raise ValueError(f"approval_status invalido: {policy.get('approval_status')}")
    if status == "allowed_declared" and policy.get("allowed_by_policy") is not True:
        raise ValueError("allowed_declared requiere allowed_by_policy=true")
    if status != "allowed_declared" and policy.get("allowed_by_policy") is True:
        raise ValueError("allowed_by_policy=true solo se permite con allowed_declared")
    if status == "future_requires_approval":
        if policy.get("requires_approval") is not True:
            raise ValueError("future_requires_approval requiere requires_approval=true")
        if policy.get("approval_status") != "future_required":
            raise ValueError("future_requires_approval requiere approval_status=future_required")
    elif policy.get("requires_approval") is True:
        raise ValueError("requires_approval=true solo se permite con future_requires_approval")
    if status in {"blocked", "forbidden"} and policy.get("allowed_by_policy") is True:
        raise ValueError(f"{status} no puede declararse como allowed")


def _validate_policy_booleans(policy: dict[str, Any]) -> None:
    if policy.get("declared_only") is not True:
        raise ValueError("capability_policy debe tener declared_only=true")
    if policy.get("runtime_enabled") is not False:
        raise ValueError("capability_policy debe tener runtime_enabled=false")
    if policy.get("execution_allowed") is not False:
        raise ValueError("capability_policy debe tener execution_allowed=false")
    if policy.get("external_access") is not False:
        raise ValueError("capability_policy debe tener external_access=false")
    for field in ("allowed_by_policy", "requires_approval"):
        if not isinstance(policy.get(field), bool):
            raise ValueError(f"{field} debe ser booleano")


def _validate_restrictions(policy: dict[str, Any]) -> None:
    restrictions = policy.get("restrictions")
    _validate_list(restrictions, "restrictions")
    _reject_blocked_markers(restrictions, "restrictions")
    if policy.get("capability_type") == "policy":
        _reject_blocked_markers(policy.get("audit_requirements"), "audit_requirements")


def _reject_blocked_markers(value: Any, field: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = _normalize_marker(key)
            if normalized in BLOCKED_MARKERS and child is True:
                raise ValueError(f"{field} no puede declarar {normalized}")
            _reject_blocked_markers(child, field)
    elif isinstance(value, list):
        for item in value:
            _reject_blocked_markers(item, field)
    elif isinstance(value, str):
        normalized = _normalize_marker(value)
        if normalized in BLOCKED_MARKERS:
            raise ValueError(f"{field} no puede declarar {normalized}")


def _reject_team_member_auto_grants(value: Any, field: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = _normalize_marker(key)
            if normalized in TEAM_MEMBER_AUTO_GRANT_FLAGS and child is True:
                raise ValueError("team capability no habilita automaticamente agentes miembros")
            _reject_team_member_auto_grants(child, field)
    elif isinstance(value, list):
        for item in value:
            _reject_team_member_auto_grants(item, field)
    elif isinstance(value, str):
        normalized = _normalize_marker(value)
        if normalized in TEAM_MEMBER_AUTO_GRANT_FLAGS:
            raise ValueError("team capability no habilita automaticamente agentes miembros")


def _looks_like_legacy_policy_capability(policy: Any) -> bool:
    if not isinstance(policy, dict):
        return False
    return "schema_version" not in policy and "capability_id" not in policy


def _validate_dependencies(dependencies: Any) -> None:
    if not isinstance(dependencies, list):
        raise ValueError("dependencies debe ser una lista")
    for dependency in dependencies:
        _validate_id(dependency, "dependencies")


def _validate_list(value: Any, field: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field} debe ser una lista")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _normalize_marker(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _ensure_json_serializable(policy: dict[str, Any]) -> None:
    try:
        json.dumps(policy, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("capability_policy debe ser serializable como JSON") from exc


def _now() -> str:
    return datetime.now().isoformat()
