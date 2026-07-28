"""Contract-only tool boundary for IA_CORE pre-runtime policy.

This module classifies conceptual tool requests and validates tool boundary
decisions. It never executes tools, calls adapters, invokes models, opens
network/browser/API/UI surfaces, reads or writes real files, reads env/secrets,
spawns processes, persists memory, writes stores, or activates integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


TOOL_BOUNDARY_STATUS = "contract_only"
TOOL_BOUNDARY_READY = True

TOOL_BOUNDARY_RUNTIME_ENABLED = False
TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED = False
TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED = False
TOOL_BOUNDARY_TOOL_REGISTRY_RUNTIME_ENABLED = False
TOOL_BOUNDARY_TOOL_CALLS_ENABLED = False
TOOL_BOUNDARY_MODEL_INVOCATION_ENABLED = False
TOOL_BOUNDARY_MEMORY_PERSISTENCE_ENABLED = False
TOOL_BOUNDARY_EXTERNAL_ACCESS_ENABLED = False
TOOL_BOUNDARY_NETWORK_ENABLED = False
TOOL_BOUNDARY_API_ENABLED = False
TOOL_BOUNDARY_UI_ENABLED = False
TOOL_BOUNDARY_WRITES_ENABLED = False
TOOL_BOUNDARY_STORES_ENABLED = False

TOOL_BOUNDARY_FILESYSTEM_ENABLED = False
TOOL_BOUNDARY_COMMAND_EXECUTION_ENABLED = False
TOOL_BOUNDARY_SHELL_ENABLED = False
TOOL_BOUNDARY_PROCESS_SPAWN_ENABLED = False
TOOL_BOUNDARY_ENV_ACCESS_ENABLED = False
TOOL_BOUNDARY_SECRET_ACCESS_ENABLED = False
TOOL_BOUNDARY_HOST_ACCESS_ENABLED = False
TOOL_BOUNDARY_DEVICE_ACCESS_ENABLED = False
TOOL_BOUNDARY_BROWSER_ENABLED = False
TOOL_BOUNDARY_CLIPBOARD_ENABLED = False

TOOL_BOUNDARY_UI_TARS_ENABLED = False
TOOL_BOUNDARY_HERMES_ENABLED = False
TOOL_BOUNDARY_N8N_ENABLED = False
TOOL_BOUNDARY_HOME_ASSISTANT_ENABLED = False

TOOL_BOUNDARY_MARKET_CATALOG_RUNTIME_ENABLED = False
TOOL_BOUNDARY_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

TOOL_TYPES = {
    "read_only_tool",
    "analysis_tool",
    "planning_tool",
    "reporting_tool",
    "validation_tool",
    "filesystem_tool",
    "network_tool",
    "browser_tool",
    "api_tool",
    "database_tool",
    "memory_tool",
    "model_tool",
    "ui_tool",
    "automation_tool",
    "workflow_tool",
    "device_tool",
    "secret_tool",
    "payment_tool",
    "publishing_tool",
    "external_connector",
}
CONCEPTUAL_TOOL_TYPES = {
    "read_only_tool",
    "analysis_tool",
    "planning_tool",
    "reporting_tool",
    "validation_tool",
}
SANDBOX_REQUIRED_TOOL_TYPES = {
    "filesystem_tool",
    "network_tool",
    "browser_tool",
    "api_tool",
    "database_tool",
    "memory_tool",
    "model_tool",
    "ui_tool",
    "automation_tool",
    "workflow_tool",
    "external_connector",
}
BLOCKED_TOOL_TYPES = {"secret_tool", "device_tool"}
APPROVAL_TOOL_TYPES = {"payment_tool", "publishing_tool"}

TOOL_SURFACES = {
    "filesystem",
    "network",
    "browser",
    "api",
    "database",
    "memory",
    "model_invocation",
    "secrets",
    "environment",
    "host",
    "shell",
    "processes",
    "stores",
    "external_services",
    "ui",
    "screen",
    "clipboard",
    "workflow",
    "scheduler",
    "worker",
    "queue",
    "physical_devices",
    "payments",
    "publishing",
    "future_integrations",
}
OPERATIONAL_SURFACES = TOOL_SURFACES - {"screen"}
CRITICAL_SURFACES = {"secrets", "environment", "host", "shell", "processes", "physical_devices", "payments"}
HIGH_RISK_SURFACES = {
    "filesystem",
    "network",
    "browser",
    "api",
    "database",
    "memory",
    "model_invocation",
    "stores",
    "external_services",
    "ui",
    "clipboard",
    "workflow",
    "scheduler",
    "worker",
    "queue",
    "publishing",
    "future_integrations",
}

ALLOWED_ACTIONS = {
    "classify_tool_type",
    "classify_tool_surface",
    "classify_tool_risk",
    "build_tool_boundary_decision",
    "evaluate_tool_boundary_contract",
    "validate_tool_boundary_decision",
    "serialize_tool_boundary_decision",
    "generate_tool_risk_report",
}
FORBIDDEN_ACTIONS = {
    "execute_tool",
    "call_tool",
    "invoke_adapter",
    "open_browser",
    "call_api",
    "network_request",
    "read_real_file",
    "write_real_file",
    "read_env",
    "read_secret",
    "run_command",
    "open_shell",
    "spawn_process",
    "persist_memory",
    "write_store",
    "modify_host",
    "control_ui",
    "control_device",
    "trigger_workflow",
    "publish_content",
    "send_payment",
    "send_message",
    "delete_resource",
    "irreversible_action",
}
APPROVAL_OPERATIONS = {"publish_content", "send_payment", "send_message", "delete_resource", "irreversible_action"}
BLOCKED_OPERATIONS = FORBIDDEN_ACTIONS - APPROVAL_OPERATIONS

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"allowed_contractually", "requires_approval", "sandbox_required", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_tool_boundary_e2e_checkpoint", "blocked", "invalid"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "tool_execution_enabled",
    "tool_adapters_enabled",
    "tool_registry_runtime_enabled",
    "tool_calls_enabled",
    "model_invocation_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "network_enabled",
    "api_enabled",
    "ui_enabled",
    "writes_enabled",
    "stores_enabled",
    "filesystem_enabled",
    "command_execution_enabled",
    "shell_enabled",
    "process_spawn_enabled",
    "env_access_enabled",
    "secret_access_enabled",
    "host_access_enabled",
    "device_access_enabled",
    "browser_enabled",
    "clipboard_enabled",
    "ui_tars_enabled",
    "hermes_enabled",
    "n8n_enabled",
    "home_assistant_enabled",
    "market_catalog_active",
    "business_composition_enabled",
    "market_catalog_runtime_enabled",
    "business_composition_runtime_enabled",
    "gate_open",
    "operations_enabled",
}
FORBIDDEN_STRING_VALUES = {"ready_for_runtime", "gate_open", "operations_enabled", "market_catalog_active"}
OBLITERATUS_TOKEN = "obliteratus"


@dataclass(frozen=True)
class ToolTypeClassification:
    tool_type: str
    known: bool
    category: str
    risk_level: str
    requires_sandbox: bool
    requires_human_approval: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ToolSurfaceClassification:
    surface: str
    known: bool
    operational: bool
    risk_level: str
    blocked_by_default: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ToolRiskClassification:
    tool_type: str | None
    surface: str | None
    operation: str | None
    risk_level: str
    forbidden_operation: bool
    requires_human_approval: bool
    requires_sandbox: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ToolBoundaryDecision:
    tool_boundary_decision_id: str
    status: str
    decision: str
    readiness: str
    tool_name: str
    tool_type: str
    requested_operation: str
    requested_surface: str
    risk_level: str
    requires_agent_permission: bool
    requires_secrets_policy: bool
    requires_prompt_injection_defense: bool
    requires_sandbox_boundary: bool
    requires_human_approval: bool
    requires_audit: bool
    allowed_to_execute: bool
    allowed_to_call_adapter: bool
    allowed_to_use_network: bool
    allowed_to_access_secret: bool
    allowed_to_read_host: bool
    allowed_to_write_host: bool
    allowed_to_persist: bool
    allowed_to_control_ui: bool
    allowed_to_control_device: bool
    allowed_to_perform_irreversible_action: bool
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


def classify_tool_type(tool_type_or_name: Any) -> ToolTypeClassification:
    value = "" if tool_type_or_name is None else str(tool_type_or_name)
    if value in CONCEPTUAL_TOOL_TYPES:
        category = "contractual"
        risk = "low"
        requires_sandbox = False
        requires_approval = False
    elif value in SANDBOX_REQUIRED_TOOL_TYPES:
        category = "operational_surface"
        risk = "high"
        requires_sandbox = True
        requires_approval = False
    elif value in BLOCKED_TOOL_TYPES:
        category = "blocked_sensitive"
        risk = "critical"
        requires_sandbox = True
        requires_approval = True
    elif value in APPROVAL_TOOL_TYPES:
        category = "irreversible_or_external"
        risk = "critical"
        requires_sandbox = True
        requires_approval = True
    else:
        category = "unknown"
        risk = "critical"
        requires_sandbox = True
        requires_approval = True
    return ToolTypeClassification(
        tool_type=value,
        known=value in TOOL_TYPES,
        category=category,
        risk_level=risk,
        requires_sandbox=requires_sandbox,
        requires_human_approval=requires_approval,
    )


def classify_tool_surface(surface: Any) -> ToolSurfaceClassification:
    value = "" if surface is None else str(surface)
    if value in CRITICAL_SURFACES:
        risk = "critical"
    elif value in HIGH_RISK_SURFACES:
        risk = "high"
    elif value in TOOL_SURFACES:
        risk = "medium"
    else:
        risk = "critical"
    return ToolSurfaceClassification(
        surface=value,
        known=value in TOOL_SURFACES,
        operational=value in OPERATIONAL_SURFACES,
        risk_level=risk,
        blocked_by_default=True,
    )


def classify_tool_risk(tool_type: Any = None, surface: Any = None, operation: Any = None) -> ToolRiskClassification:
    type_classification = classify_tool_type(tool_type)
    surface_classification = classify_tool_surface(surface)
    operation_value = "" if operation is None else str(operation)
    forbidden_operation = operation_value in FORBIDDEN_ACTIONS
    requires_approval = type_classification.requires_human_approval or operation_value in APPROVAL_OPERATIONS
    requires_sandbox = type_classification.requires_sandbox or surface_classification.operational
    risk = _max_risk(
        type_classification.risk_level,
        surface_classification.risk_level,
        "critical" if forbidden_operation else "low",
    )
    return ToolRiskClassification(
        tool_type=type_classification.tool_type,
        surface=surface_classification.surface,
        operation=operation_value,
        risk_level=risk,
        forbidden_operation=forbidden_operation,
        requires_human_approval=requires_approval,
        requires_sandbox=requires_sandbox,
    )


def build_tool_boundary_decision(
    *,
    tool_boundary_decision_id: str,
    tool_name: str,
    tool_type: str,
    requested_operation: str,
    requested_surface: str,
    decision: str = "allowed_contractually",
    status: str = "evaluated",
    readiness: str = "ready_for_tool_boundary_e2e_checkpoint",
    risk_level: str = "low",
    requires_agent_permission: bool = True,
    requires_secrets_policy: bool = True,
    requires_prompt_injection_defense: bool = True,
    requires_sandbox_boundary: bool = True,
    requires_human_approval: bool = False,
    requires_audit: bool = True,
    allowed_to_execute: bool = False,
    allowed_to_call_adapter: bool = False,
    allowed_to_use_network: bool = False,
    allowed_to_access_secret: bool = False,
    allowed_to_read_host: bool = False,
    allowed_to_write_host: bool = False,
    allowed_to_persist: bool = False,
    allowed_to_control_ui: bool = False,
    allowed_to_control_device: bool = False,
    allowed_to_perform_irreversible_action: bool = False,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ToolBoundaryDecision:
    return ToolBoundaryDecision(
        tool_boundary_decision_id=tool_boundary_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        tool_name=tool_name,
        tool_type=tool_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        risk_level=risk_level,
        requires_agent_permission=requires_agent_permission,
        requires_secrets_policy=requires_secrets_policy,
        requires_prompt_injection_defense=requires_prompt_injection_defense,
        requires_sandbox_boundary=requires_sandbox_boundary,
        requires_human_approval=requires_human_approval,
        requires_audit=requires_audit,
        allowed_to_execute=allowed_to_execute,
        allowed_to_call_adapter=allowed_to_call_adapter,
        allowed_to_use_network=allowed_to_use_network,
        allowed_to_access_secret=allowed_to_access_secret,
        allowed_to_read_host=allowed_to_read_host,
        allowed_to_write_host=allowed_to_write_host,
        allowed_to_persist=allowed_to_persist,
        allowed_to_control_ui=allowed_to_control_ui,
        allowed_to_control_device=allowed_to_control_device,
        allowed_to_perform_irreversible_action=allowed_to_perform_irreversible_action,
        blocking_reasons=list(blocking_reasons or []),
        warnings=list(warnings or []),
        lineage=dict(lineage or {}),
        metadata=dict(metadata or {}),
    )


def evaluate_tool_boundary_contract(
    *,
    tool_name: str,
    tool_type: str,
    requested_operation: str,
    requested_surface: str,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ToolBoundaryDecision:
    type_classification = classify_tool_type(tool_type)
    surface_classification = classify_tool_surface(requested_surface)
    risk = classify_tool_risk(tool_type, requested_surface, requested_operation)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    _require(tool_name, blockers, "missing_tool_name", "tool_name requerido")
    if not type_classification.known:
        _block(blockers, "unknown_tool_type", "tool_type desconocido")
    if not surface_classification.known:
        _block(blockers, "unknown_tool_surface", "requested_surface desconocida")
    if requested_operation in BLOCKED_OPERATIONS:
        _block(blockers, "operation_blocked_pre_runtime", "operacion prohibida en pre-runtime")
    if _contains_obliteratus([tool_name, tool_type, requested_surface, requested_operation, lineage, metadata]):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es tool provider, dependency, adapter ni capability")

    if blockers:
        decision = "invalid" if any(item["code"].startswith(("missing_", "unknown_", "obliteratus")) for item in blockers) else "blocked"
    elif tool_type in APPROVAL_TOOL_TYPES or requested_operation in APPROVAL_OPERATIONS:
        decision = "requires_approval"
        warnings.append("human_approval_required_but_no_execution_allowed")
    elif tool_type in BLOCKED_TOOL_TYPES or requested_surface in CRITICAL_SURFACES:
        decision = "blocked"
        _block(blockers, "sensitive_surface_blocked", "surface sensible bloqueada en pre-runtime")
    elif risk.requires_sandbox:
        decision = "sandbox_required"
        warnings.append("sandbox_required_contract_only_no_sandbox_created")
    else:
        decision = "allowed_contractually"

    return build_tool_boundary_decision(
        tool_boundary_decision_id=f"tool_boundary_{tool_name or 'missing_tool'}_{tool_type or 'missing_type'}_{requested_operation or 'missing_operation'}",
        tool_name=tool_name,
        tool_type=tool_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        decision=decision,
        status="invalid" if decision == "invalid" else "evaluated",
        readiness="ready_for_tool_boundary_e2e_checkpoint" if decision not in {"invalid", "blocked"} else "blocked",
        risk_level=risk.risk_level,
        requires_human_approval=risk.requires_human_approval,
        blocking_reasons=blockers,
        warnings=warnings,
        lineage={
            "agent_permission_boundary": "active_contractual_boundary",
            "secrets_policy_boundary": "active_contractual_boundary",
            "prompt_injection_defense_boundary": "active_contractual_boundary",
            "sandbox_boundary": "active_contractual_boundary",
            "operational_readiness_gate_boundary": "closed",
            **deepcopy(lineage or {}),
        },
        metadata={**_boundary_flags(), **deepcopy(metadata or {})},
    )


def validate_tool_boundary_decision(decision: ToolBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_tool_boundary_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("tool_boundary_decision_id"), blockers, "missing_tool_boundary_decision_id", "tool_boundary_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _require(payload.get("tool_name"), blockers, "missing_tool_name", "tool_name requerido")
    _require(payload.get("tool_type"), blockers, "missing_tool_type", "tool_type requerido")
    _require(payload.get("requested_operation"), blockers, "missing_requested_operation", "requested_operation requerida")
    _require(payload.get("requested_surface"), blockers, "missing_requested_surface", "requested_surface requerida")
    _allowed(payload.get("risk_level"), RISK_LEVELS, blockers, "invalid_risk_level", "risk_level invalido")

    for field_name in [
        "requires_agent_permission",
        "requires_secrets_policy",
        "requires_prompt_injection_defense",
        "requires_sandbox_boundary",
        "requires_audit",
    ]:
        if payload.get(field_name) is not True:
            _block(blockers, f"{field_name}_required", f"{field_name} debe ser True")
    for field_name in [
        "allowed_to_execute",
        "allowed_to_call_adapter",
        "allowed_to_use_network",
        "allowed_to_access_secret",
        "allowed_to_read_host",
        "allowed_to_write_host",
        "allowed_to_persist",
        "allowed_to_control_ui",
        "allowed_to_control_device",
        "allowed_to_perform_irreversible_action",
    ]:
        if payload.get(field_name) is not False:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} debe ser False")
    if not isinstance(payload.get("requires_human_approval"), bool):
        _block(blockers, "requires_human_approval_not_bool", "requires_human_approval debe ser bool")
    for field_name in ["blocking_reasons", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"{field_name}_not_list", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"{field_name}_not_dict", f"{field_name} debe ser dict")

    operation = payload.get("requested_operation")
    if operation in BLOCKED_OPERATIONS and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_operation_not_blocked", "operacion prohibida debe quedar blocked o invalid")
    if operation in APPROVAL_OPERATIONS and payload.get("decision") not in {"requires_approval", "blocked", "invalid"}:
        _block(blockers, "approval_operation_not_gated", "operacion irreversible requiere approval/blocked/invalid")
    if payload.get("tool_type") in BLOCKED_TOOL_TYPES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_tool_type_not_blocked", "tool_type sensible debe quedar blocked o invalid")
    if payload.get("tool_type") in APPROVAL_TOOL_TYPES and payload.get("decision") == "allowed_contractually":
        _block(blockers, "approval_tool_type_allowed", "payment/publishing no puede allowed_contractually")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es tool provider, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "TOOL_BOUNDARY_READY" if not blockers else "TOOL_BOUNDARY_BLOCKED",
        "readiness": "ready_for_tool_boundary_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["tool_boundary_decision_blocked"],
        "policy_status": TOOL_BOUNDARY_STATUS,
        "runtime_enabled": TOOL_BOUNDARY_RUNTIME_ENABLED,
        "tool_execution_enabled": TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED,
        "tool_adapters_enabled": TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED,
        "tool_calls_enabled": TOOL_BOUNDARY_TOOL_CALLS_ENABLED,
    }


def serialize_tool_boundary_decision(decision: ToolBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, ToolBoundaryDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_tool_risk_report(decision: ToolBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_tool_boundary_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "tool_name": payload.get("tool_name"),
        "tool_type": payload.get("tool_type"),
        "requested_surface": payload.get("requested_surface"),
        "requested_operation": payload.get("requested_operation"),
        "allowed_to_execute": False,
        "requires_human_approval": bool(payload.get("requires_human_approval")),
    }


def get_tool_boundary_contract() -> dict[str, Any]:
    return {
        "status": TOOL_BOUNDARY_STATUS,
        "ready": TOOL_BOUNDARY_READY,
        "verdict": "TOOL_BOUNDARY_READY",
        "readiness": "ready_for_tool_boundary_e2e_checkpoint",
        "next_step": "PROMPT 3.26.1 - Checkpoint E2E de tool boundary",
        "mode": [
            "contract-only",
            "security-simulated",
            "non-operational",
            "pre-runtime",
            "tool-request-only",
            "deny-by-default",
            "permission-aware",
            "sandbox-aware",
            "secrets-aware",
            "prompt-injection-aware",
            "no real tool execution",
        ],
        "central_rule": "En pre-runtime, una herramienta puede describirse, clasificarse o evaluarse. Pero no puede ejecutarse.",
        "tool_types": sorted(TOOL_TYPES),
        "tool_surfaces": sorted(TOOL_SURFACES),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "decisions": sorted(ALLOWED_DECISIONS),
        "boundary_flags": _boundary_flags(),
        "agent_permission_boundary": "active_contractual_boundary",
        "secrets_policy_boundary": "active_contractual_boundary",
        "prompt_injection_defense_boundary": "active_contractual_boundary",
        "sandbox_boundary": "active_contractual_boundary",
        "operational_readiness_gate_boundary": "closed",
        "obliteratus": "not_tool_provider_not_integration_not_dependency_not_adapter_not_capability",
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": TOOL_BOUNDARY_RUNTIME_ENABLED,
        "tool_execution_enabled": TOOL_BOUNDARY_TOOL_EXECUTION_ENABLED,
        "tool_adapters_enabled": TOOL_BOUNDARY_TOOL_ADAPTERS_ENABLED,
        "tool_registry_runtime_enabled": TOOL_BOUNDARY_TOOL_REGISTRY_RUNTIME_ENABLED,
        "tool_calls_enabled": TOOL_BOUNDARY_TOOL_CALLS_ENABLED,
        "model_invocation_enabled": TOOL_BOUNDARY_MODEL_INVOCATION_ENABLED,
        "memory_persistence_enabled": TOOL_BOUNDARY_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": TOOL_BOUNDARY_EXTERNAL_ACCESS_ENABLED,
        "network_enabled": TOOL_BOUNDARY_NETWORK_ENABLED,
        "api_enabled": TOOL_BOUNDARY_API_ENABLED,
        "ui_enabled": TOOL_BOUNDARY_UI_ENABLED,
        "writes_enabled": TOOL_BOUNDARY_WRITES_ENABLED,
        "stores_enabled": TOOL_BOUNDARY_STORES_ENABLED,
        "filesystem_enabled": TOOL_BOUNDARY_FILESYSTEM_ENABLED,
        "command_execution_enabled": TOOL_BOUNDARY_COMMAND_EXECUTION_ENABLED,
        "shell_enabled": TOOL_BOUNDARY_SHELL_ENABLED,
        "process_spawn_enabled": TOOL_BOUNDARY_PROCESS_SPAWN_ENABLED,
        "env_access_enabled": TOOL_BOUNDARY_ENV_ACCESS_ENABLED,
        "secret_access_enabled": TOOL_BOUNDARY_SECRET_ACCESS_ENABLED,
        "host_access_enabled": TOOL_BOUNDARY_HOST_ACCESS_ENABLED,
        "device_access_enabled": TOOL_BOUNDARY_DEVICE_ACCESS_ENABLED,
        "browser_enabled": TOOL_BOUNDARY_BROWSER_ENABLED,
        "clipboard_enabled": TOOL_BOUNDARY_CLIPBOARD_ENABLED,
        "ui_tars_enabled": TOOL_BOUNDARY_UI_TARS_ENABLED,
        "hermes_enabled": TOOL_BOUNDARY_HERMES_ENABLED,
        "n8n_enabled": TOOL_BOUNDARY_N8N_ENABLED,
        "home_assistant_enabled": TOOL_BOUNDARY_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": TOOL_BOUNDARY_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": TOOL_BOUNDARY_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    }


def _validate_boundary_flags(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for scope in [payload, payload.get("metadata", {}), payload.get("lineage", {})]:
        if isinstance(scope, dict):
            for key, value in scope.items():
                if key in FORBIDDEN_TRUE_FLAGS and value is True:
                    _block(blockers, f"{key}_not_allowed", f"{key}=True no permitido")
    for name, value in _boundary_flags().items():
        if value is not False:
            _block(blockers, f"{name}_not_allowed", f"{name} debe ser False")
    for value in _flatten_values(payload):
        if isinstance(value, str) and value.lower() in FORBIDDEN_STRING_VALUES:
            _block(blockers, "forbidden_state_value", f"valor prohibido: {value}")


def _max_risk(*levels: str) -> str:
    order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    return max(levels, key=lambda level: order[level])


def _flatten_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        items: list[Any] = []
        for key, child in value.items():
            items.append(key)
            items.extend(_flatten_values(child))
        return items
    if isinstance(value, list | tuple | set):
        items = []
        for child in value:
            items.extend(_flatten_values(child))
        return items
    return [value]


def _contains_obliteratus(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_obliteratus(k) or _contains_obliteratus(v) for k, v in value.items())
    if isinstance(value, list | tuple | set):
        return any(_contains_obliteratus(item) for item in value)
    return isinstance(value, str) and OBLITERATUS_TOKEN in value.lower()


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, ""):
        _block(blockers, code, message)


def _allowed(value: Any, allowed: set[str], blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value not in allowed:
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message}
    if blocker not in blockers:
        blockers.append(blocker)
