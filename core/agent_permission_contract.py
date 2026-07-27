"""Contract-only agent permission model for IA_CORE Security Layer.

No porque un agente sepa hacer algo significa que tiene permiso para hacerlo.
Todo permiso debe declararse explícitamente.
Todo lo no declarado queda bloqueado por default.

This module is security-simulated and non-operational. It does not enforce
permissions over live actions, start runtime, execute tools, call models, write
stores, access external services, open UI, or activate integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


AGENT_PERMISSION_CONTRACT_STATUS = "contract_only"
AGENT_PERMISSION_CONTRACT_READY = True

AGENT_PERMISSION_RUNTIME_ENABLED = False
AGENT_PERMISSION_TOOLS_ENABLED = False
AGENT_PERMISSION_MODEL_INVOCATION_ENABLED = False
AGENT_PERMISSION_MEMORY_PERSISTENCE_ENABLED = False
AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED = False
AGENT_PERMISSION_API_ENABLED = False
AGENT_PERMISSION_UI_ENABLED = False
AGENT_PERMISSION_WRITES_ENABLED = False
AGENT_PERMISSION_STORES_ENABLED = False

AGENT_PERMISSION_UI_TARS_ENABLED = False
AGENT_PERMISSION_HERMES_ENABLED = False
AGENT_PERMISSION_N8N_ENABLED = False
AGENT_PERMISSION_HOME_ASSISTANT_ENABLED = False

AGENT_PERMISSION_MARKET_CATALOG_RUNTIME_ENABLED = False
AGENT_PERMISSION_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

SAFE_CAPABILITIES = {
    "read_contract",
    "read_documentation",
    "prepare_plan",
    "prepare_prompt",
    "prepare_report",
    "validate_schema",
    "simulate_decision",
    "request_human_approval",
    "generate_risk_report",
}

DANGEROUS_CAPABILITIES = {
    "runtime_execution",
    "tool_execution",
    "model_invocation",
    "memory_persistence",
    "external_access",
    "api_access",
    "ui_access",
    "ui_tars_operation",
    "hermes_orchestration",
    "n8n_workflow_execution",
    "home_assistant_action",
    "attempt_store_write",
    "lifecycle_event_write",
    "result_store_write",
    "history_write",
    "read_model_write",
    "projection_write",
    "market_catalog_runtime",
    "business_composition_runtime",
    "secret_read",
    "secret_write",
    "config_write",
    "filesystem_write",
    "network_access",
    "irreversible_action",
    "physical_world_action",
}

ALL_CAPABILITIES = SAFE_CAPABILITIES | DANGEROUS_CAPABILITIES

BLOCKED_SURFACES = {
    "runtime",
    "scheduler",
    "worker",
    "queue",
    "model_invocation",
    "tool_execution",
    "memory_persistence",
    "external_access",
    "API",
    "UI",
    "UI-TARS",
    "Hermes",
    "n8n",
    "Home Assistant",
    "attempt_store",
    "lifecycle_store",
    "result_store",
    "history",
    "read_model",
    "projection",
    "Market Catalog runtime",
    "Business Composition Layer runtime",
    "secrets",
    "config/env",
    "filesystem write",
    "network",
    "physical devices",
}

FUTURE_SURFACES_REQUIRING_SANDBOX = BLOCKED_SURFACES
HUMAN_APPROVAL_CAPABILITIES = {
    "ui_tars_operation",
    "hermes_orchestration",
    "n8n_workflow_execution",
    "home_assistant_action",
    "filesystem_write",
    "irreversible_action",
    "physical_world_action",
}
HUMAN_APPROVAL_SURFACES = {
    "external_access",
    "UI",
    "UI-TARS",
    "Hermes",
    "n8n",
    "Home Assistant",
    "filesystem write",
    "network",
    "physical devices",
}

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"allowed", "denied", "approval_required", "invalid"}
ALLOWED_READINESS = {"ready_for_agent_permission_e2e_checkpoint", "blocked", "invalid"}
ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "security_layer_enabled",
    "tools_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "api_enabled",
    "ui_enabled",
    "ui_tars_enabled",
    "hermes_enabled",
    "n8n_enabled",
    "home_assistant_enabled",
    "writes_enabled",
    "stores_enabled",
    "market_catalog_active",
    "market_catalog_runtime_enabled",
    "business_composition_enabled",
    "business_composition_runtime_enabled",
    "gate_open",
    "operations_enabled",
}
FORBIDDEN_STRING_VALUES = {
    "ready_for_runtime",
    "runtime_enabled",
    "operations_enabled",
    "gate_open",
    "market_catalog_active",
}
OBLITERATUS_TOKEN = "obliteratus"


@dataclass(frozen=True)
class AgentPermissionProfile:
    agent_id: str
    agent_name: str
    agent_role: str
    agent_specialization: str
    domain: str
    allowed_capabilities: list[str] = field(default_factory=list)
    denied_capabilities: list[str] = field(default_factory=lambda: sorted(DANGEROUS_CAPABILITIES))
    blocked_surfaces: list[str] = field(default_factory=lambda: sorted(BLOCKED_SURFACES))
    approval_required_for: list[str] = field(default_factory=list)
    risk_level: str = "low"
    lineage_required: bool = True
    idempotency_required: bool = True
    human_approval_required: bool = False
    sandbox_required: bool = True
    audit_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


@dataclass(frozen=True)
class AgentPermissionDecision:
    permission_decision_id: str
    status: str
    decision: str
    readiness: str
    agent_id: str
    agent_role: str
    agent_specialization: str
    domain: str
    requested_capability: str
    requested_surface: str | None
    allowed: bool
    requires_human_approval: bool
    requires_sandbox: bool
    requires_audit: bool
    requires_lineage: bool
    requires_idempotency: bool
    risk_level: str
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blocking_reasons"] = deepcopy(self.blocking_reasons)
        payload["warnings"] = deepcopy(self.warnings)
        payload["lineage"] = deepcopy(self.lineage)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_agent_permission_profile(
    *,
    agent_id: str,
    agent_name: str,
    agent_role: str,
    agent_specialization: str,
    domain: str,
    allowed_capabilities: list[str] | None = None,
    denied_capabilities: list[str] | None = None,
    blocked_surfaces: list[str] | None = None,
    approval_required_for: list[str] | None = None,
    risk_level: str = "low",
    metadata: dict[str, Any] | None = None,
) -> AgentPermissionProfile:
    safe_allowed = sorted(set(allowed_capabilities or SAFE_CAPABILITIES) & SAFE_CAPABILITIES)
    denied = sorted(set(denied_capabilities or DANGEROUS_CAPABILITIES) | DANGEROUS_CAPABILITIES)
    surfaces = sorted(set(blocked_surfaces or BLOCKED_SURFACES) | BLOCKED_SURFACES)
    approvals = sorted(set(approval_required_for or HUMAN_APPROVAL_CAPABILITIES))
    return AgentPermissionProfile(
        agent_id=agent_id,
        agent_name=agent_name,
        agent_role=agent_role,
        agent_specialization=agent_specialization,
        domain=domain,
        allowed_capabilities=safe_allowed,
        denied_capabilities=denied,
        blocked_surfaces=surfaces,
        approval_required_for=approvals,
        risk_level=risk_level,
        metadata=deepcopy(metadata or {}),
    )


def evaluate_agent_permission_contract(
    *,
    profile: AgentPermissionProfile | dict[str, Any] | None = None,
    agent_id: str | None = None,
    agent_name: str | None = None,
    agent_role: str | None = None,
    agent_specialization: str | None = None,
    domain: str | None = None,
    requested_capability: str,
    requested_surface: str | None = None,
    lineage: dict[str, Any] | None = None,
    idempotency_key: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> AgentPermissionDecision:
    profile_payload = _profile_payload(profile)
    resolved_agent_id = agent_id if agent_id is not None else profile_payload.get("agent_id", "")
    resolved_agent_name = agent_name if agent_name is not None else profile_payload.get("agent_name", "")
    resolved_role = agent_role if agent_role is not None else profile_payload.get("agent_role", "")
    resolved_specialization = agent_specialization if agent_specialization is not None else profile_payload.get("agent_specialization", "")
    resolved_domain = domain if domain is not None else profile_payload.get("domain", "")
    resolved_lineage = deepcopy(lineage or {})
    resolved_metadata = deepcopy(metadata or {})
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    _require(resolved_agent_id, blockers, "missing_agent_id", "agent_id requerido")
    _require(resolved_role, blockers, "missing_agent_role", "agent_role requerido")
    _require(resolved_specialization, blockers, "missing_agent_specialization", "agent_specialization requerido")
    _require(resolved_domain, blockers, "missing_domain", "domain requerido")
    _require(requested_capability, blockers, "missing_requested_capability", "requested_capability requerido")

    if requested_capability and requested_capability not in ALL_CAPABILITIES:
        _block(blockers, "unknown_capability", "requested_capability no existe en catalogo")

    capability_safe = requested_capability in SAFE_CAPABILITIES
    capability_dangerous = requested_capability in DANGEROUS_CAPABILITIES
    surface_blocked = requested_surface in BLOCKED_SURFACES if requested_surface else False
    requires_human_approval = requested_capability in HUMAN_APPROVAL_CAPABILITIES or requested_surface in HUMAN_APPROVAL_SURFACES
    requires_sandbox = requested_surface in FUTURE_SURFACES_REQUIRING_SANDBOX or capability_dangerous
    risk_level = _risk_for(requested_capability, requested_surface)

    if not resolved_lineage:
        if capability_dangerous or surface_blocked:
            _block(blockers, "missing_lineage", "lineage requerido para capability o surface sensible")
        else:
            warnings.append("lineage_recommended")

    if not idempotency_key and (capability_dangerous or surface_blocked):
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido para capability o surface sensible")

    if _contains_obliteratus([requested_capability, requested_surface, resolved_metadata, resolved_lineage, profile_payload]):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es capability, adapter, dependency ni integration de IA_CORE")

    _scan_forbidden_values(resolved_metadata, blockers)
    _scan_forbidden_values(resolved_lineage, blockers)
    _validate_boundary_flags(blockers)

    if blockers:
        return _decision(
            permission_decision_id=_decision_id(resolved_agent_id, requested_capability),
            status="invalid" if _has_invalid_blocker(blockers) else "blocked",
            decision="invalid" if _has_invalid_blocker(blockers) else "denied",
            readiness="invalid" if _has_invalid_blocker(blockers) else "blocked",
            agent_id=resolved_agent_id or "",
            agent_role=resolved_role or "",
            agent_specialization=resolved_specialization or "",
            domain=resolved_domain or "",
            requested_capability=requested_capability or "",
            requested_surface=requested_surface,
            allowed=False,
            requires_human_approval=requires_human_approval,
            requires_sandbox=True if requires_sandbox or surface_blocked else True,
            requires_audit=True,
            requires_lineage=True,
            requires_idempotency=True,
            risk_level=risk_level,
            blocking_reasons=blockers,
            warnings=warnings,
            lineage=resolved_lineage,
            metadata=resolved_metadata,
        )

    if capability_safe and not surface_blocked:
        decision = "allowed"
        allowed = True
    elif requires_human_approval:
        decision = "approval_required"
        allowed = False
    else:
        decision = "denied"
        allowed = False

    if capability_dangerous and allowed:
        _block(blockers, "dangerous_capability_allowed", "capability peligrosa no puede allowed=True")
    if surface_blocked and allowed:
        _block(blockers, "blocked_surface_allowed", "surface bloqueada no puede allowed=True")

    return _decision(
        permission_decision_id=_decision_id(resolved_agent_id, requested_capability),
        status="evaluated" if not blockers else "blocked",
        decision=decision if not blockers else "denied",
        readiness="ready_for_agent_permission_e2e_checkpoint" if not blockers else "blocked",
        agent_id=resolved_agent_id,
        agent_role=resolved_role,
        agent_specialization=resolved_specialization,
        domain=resolved_domain,
        requested_capability=requested_capability,
        requested_surface=requested_surface,
        allowed=allowed if not blockers else False,
        requires_human_approval=requires_human_approval,
        requires_sandbox=True,
        requires_audit=True,
        requires_lineage=True,
        requires_idempotency=True,
        risk_level=risk_level,
        blocking_reasons=blockers,
        warnings=warnings,
        lineage=resolved_lineage,
        metadata=resolved_metadata,
    )


def validate_agent_permission_decision(decision: AgentPermissionDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_agent_permission_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("permission_decision_id"), blockers, "missing_permission_decision_id", "permission_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision no permitida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")
    _require(payload.get("agent_id"), blockers, "missing_agent_id", "agent_id requerido")
    _require(payload.get("agent_role"), blockers, "missing_agent_role", "agent_role requerido")
    _require(payload.get("agent_specialization"), blockers, "missing_agent_specialization", "agent_specialization requerido")
    _require(payload.get("domain"), blockers, "missing_domain", "domain requerido")
    _require(payload.get("requested_capability"), blockers, "missing_requested_capability", "requested_capability requerido")
    if payload.get("requested_capability") and payload.get("requested_capability") not in ALL_CAPABILITIES:
        _block(blockers, "unknown_capability", "requested_capability no existe en catalogo")
    _allowed(payload.get("risk_level"), ALLOWED_RISK_LEVELS, blockers, "invalid_risk_level", "risk_level no permitido")

    capability = payload.get("requested_capability")
    surface = payload.get("requested_surface")
    if payload.get("allowed") is True and capability in DANGEROUS_CAPABILITIES:
        _block(blockers, "dangerous_capability_allowed", "allowed=True no permitido para capability peligrosa")
    if payload.get("allowed") is True and surface in BLOCKED_SURFACES:
        _block(blockers, "blocked_surface_allowed", "allowed=True no permitido para surface bloqueada")
    if capability in DANGEROUS_CAPABILITIES and payload.get("allowed") is not False:
        _block(blockers, "dangerous_capability_must_be_blocked", "capability peligrosa debe allowed=False")
    if surface in BLOCKED_SURFACES and payload.get("allowed") is not False:
        _block(blockers, "blocked_surface_must_be_blocked", "surface bloqueada debe allowed=False")
    if capability in {"runtime_execution", "tool_execution", "model_invocation", "memory_persistence", "external_access", "api_access", "ui_access"} and payload.get("decision") == "allowed":
        _block(blockers, "runtime_surface_allowed", "runtime/tool/model/memory/external/API/UI deben estar bloqueados")
    if capability in {"irreversible_action", "physical_world_action", "ui_tars_operation", "hermes_orchestration", "n8n_workflow_execution", "home_assistant_action"}:
        if payload.get("requires_human_approval") is not True:
            _block(blockers, "human_approval_required", "accion sensible requiere aprobacion humana")

    for field_name in ["requires_audit", "requires_lineage", "requires_idempotency", "requires_sandbox"]:
        if payload.get(field_name) is not True:
            _block(blockers, f"{field_name}_required", f"{field_name} debe ser true")
    for field_name in ["blocking_reasons", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"invalid_{field_name}", f"{field_name} debe ser list")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"invalid_{field_name}", f"{field_name} debe ser dict")

    _scan_forbidden_values(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no permitido")
    _validate_boundary_flags(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "AGENT_PERMISSION_CONTRACT_READY" if not blockers else "AGENT_PERMISSION_CONTRACT_BLOCKED",
        "readiness": "ready_for_agent_permission_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [] if not blockers else ["agent_permission_decision_blocked"],
        "decision": payload,
        "contract_status": AGENT_PERMISSION_CONTRACT_STATUS,
        "runtime_enabled": AGENT_PERMISSION_RUNTIME_ENABLED,
        "tools_enabled": AGENT_PERMISSION_TOOLS_ENABLED,
        "model_invocation_enabled": AGENT_PERMISSION_MODEL_INVOCATION_ENABLED,
        "memory_persistence_enabled": AGENT_PERMISSION_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": AGENT_PERMISSION_API_ENABLED,
        "ui_enabled": AGENT_PERMISSION_UI_ENABLED,
        "writes_enabled": AGENT_PERMISSION_WRITES_ENABLED,
        "stores_enabled": AGENT_PERMISSION_STORES_ENABLED,
    }


def serialize_agent_permission_decision(decision: AgentPermissionDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, AgentPermissionDecision):
        return decision.to_dict()
    return deepcopy(decision)


def get_agent_permission_contract() -> dict[str, Any]:
    return {
        "status": AGENT_PERMISSION_CONTRACT_STATUS,
        "ready": AGENT_PERMISSION_CONTRACT_READY,
        "verdict": "AGENT_PERMISSION_CONTRACT_READY",
        "readiness": "ready_for_agent_permission_e2e_checkpoint",
        "next_step": "PROMPT 3.22.1 — Checkpoint E2E de permisos por agente",
        "mode": ["contract-only", "security-simulated", "non-operational", "default-deny"],
        "safe_capabilities": sorted(SAFE_CAPABILITIES),
        "dangerous_capabilities": sorted(DANGEROUS_CAPABILITIES),
        "blocked_surfaces": sorted(BLOCKED_SURFACES),
        "boundaries": _boundary_flags(),
        "obliteratus": "not_integration_not_dependency_not_capability",
    }


def _decision(**kwargs: Any) -> AgentPermissionDecision:
    return AgentPermissionDecision(**kwargs)


def _decision_id(agent_id: str | None, capability: str | None) -> str:
    agent_part = agent_id or "missing_agent"
    capability_part = capability or "missing_capability"
    return f"agent_permission_{agent_part}_{capability_part}"


def _profile_payload(profile: AgentPermissionProfile | dict[str, Any] | None) -> dict[str, Any]:
    if isinstance(profile, AgentPermissionProfile):
        return profile.to_dict()
    return deepcopy(profile or {})


def _risk_for(capability: str | None, surface: str | None) -> str:
    if capability in {"runtime_execution", "tool_execution", "external_access", "home_assistant_action", "physical_world_action"}:
        return "critical"
    if capability in DANGEROUS_CAPABILITIES or surface in BLOCKED_SURFACES:
        return "high"
    return "low"


def _has_invalid_blocker(blockers: list[dict[str, str]]) -> bool:
    return any(blocker["code"].startswith(("missing_", "invalid_", "unknown_", "obliteratus")) for blocker in blockers)


def _validate_boundary_flags(blockers: list[dict[str, str]]) -> None:
    for name, value in _boundary_flags().items():
        if value is not False:
            _block(blockers, f"{name}_not_allowed", f"{name} debe ser false")


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": AGENT_PERMISSION_RUNTIME_ENABLED,
        "tools_enabled": AGENT_PERMISSION_TOOLS_ENABLED,
        "model_invocation_enabled": AGENT_PERMISSION_MODEL_INVOCATION_ENABLED,
        "memory_persistence_enabled": AGENT_PERMISSION_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": AGENT_PERMISSION_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": AGENT_PERMISSION_API_ENABLED,
        "ui_enabled": AGENT_PERMISSION_UI_ENABLED,
        "writes_enabled": AGENT_PERMISSION_WRITES_ENABLED,
        "stores_enabled": AGENT_PERMISSION_STORES_ENABLED,
        "ui_tars_enabled": AGENT_PERMISSION_UI_TARS_ENABLED,
        "hermes_enabled": AGENT_PERMISSION_HERMES_ENABLED,
        "n8n_enabled": AGENT_PERMISSION_N8N_ENABLED,
        "home_assistant_enabled": AGENT_PERMISSION_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": AGENT_PERMISSION_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": AGENT_PERMISSION_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    }


def _scan_forbidden_values(value: Any, blockers: list[dict[str, str]]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_TRUE_FLAGS and item is True:
                _block(blockers, f"{key}_not_allowed", f"{key}=true no permitido")
            _scan_forbidden_values(item, blockers)
    elif isinstance(value, list):
        for item in value:
            _scan_forbidden_values(item, blockers)
    elif isinstance(value, str) and value in FORBIDDEN_STRING_VALUES:
        _block(blockers, f"{value}_not_allowed", f"{value} no permitido")


def _contains_obliteratus(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_obliteratus(key) or _contains_obliteratus(item) for key, item in value.items())
    if isinstance(value, list | tuple | set):
        return any(_contains_obliteratus(item) for item in value)
    if isinstance(value, str):
        return OBLITERATUS_TOKEN in value.lower()
    return False


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, "", {}, []):
        _block(blockers, code, message)


def _allowed(value: Any, allowed: set[str], blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value not in allowed:
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
