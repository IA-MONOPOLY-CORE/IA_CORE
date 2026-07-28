"""Contract-only sandbox boundary for IA_CORE pre-runtime isolation.

This module describes and validates sandbox limits. It never executes commands,
spawns processes, opens shells, reads or writes real files, reads env/secrets,
uses network/browser/tools/models, persists memory, writes stores, controls UI
or devices, or activates integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


SANDBOX_BOUNDARY_STATUS = "contract_only"
SANDBOX_BOUNDARY_READY = True

SANDBOX_RUNTIME_ENABLED = False
SANDBOX_COMMAND_EXECUTION_ENABLED = False
SANDBOX_TOOL_EXECUTION_ENABLED = False
SANDBOX_MODEL_INVOCATION_ENABLED = False
SANDBOX_MEMORY_PERSISTENCE_ENABLED = False
SANDBOX_EXTERNAL_ACCESS_ENABLED = False
SANDBOX_NETWORK_ENABLED = False
SANDBOX_API_ENABLED = False
SANDBOX_UI_ENABLED = False
SANDBOX_WRITES_ENABLED = False
SANDBOX_STORES_ENABLED = False

SANDBOX_FILESYSTEM_READ_ENABLED = False
SANDBOX_FILESYSTEM_WRITE_ENABLED = False
SANDBOX_PROCESS_SPAWN_ENABLED = False
SANDBOX_SHELL_ENABLED = False
SANDBOX_ENV_ACCESS_ENABLED = False
SANDBOX_SECRET_ACCESS_ENABLED = False
SANDBOX_HOST_ACCESS_ENABLED = False
SANDBOX_DEVICE_ACCESS_ENABLED = False
SANDBOX_CLIPBOARD_ACCESS_ENABLED = False
SANDBOX_BROWSER_ACCESS_ENABLED = False

SANDBOX_UI_TARS_ENABLED = False
SANDBOX_HERMES_ENABLED = False
SANDBOX_N8N_ENABLED = False
SANDBOX_HOME_ASSISTANT_ENABLED = False

SANDBOX_MARKET_CATALOG_RUNTIME_ENABLED = False
SANDBOX_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

ISOLATION_SURFACES = {
    "filesystem",
    "network",
    "environment",
    "secrets",
    "processes",
    "shell",
    "tools",
    "model_invocation",
    "memory",
    "stores",
    "API",
    "UI",
    "browser",
    "clipboard",
    "screen",
    "documents",
    "tool_results",
    "agent_outputs",
    "host_system",
    "external_services",
    "physical_devices",
    "future_integrations",
}
SANDBOX_MODES = {"disabled", "contract_only", "dry_run", "simulation", "quarantine"}
ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"allowed_contractually", "isolated", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_sandbox_boundary_e2e_checkpoint", "blocked", "invalid"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

ALLOWED_ACTIONS = {
    "build_sandbox_boundary_profile",
    "evaluate_sandbox_boundary_contract",
    "validate_sandbox_boundary_decision",
    "serialize_sandbox_boundary_decision",
    "classify_sandbox_surface",
    "classify_requested_operation",
    "generate_sandbox_risk_report",
}
FORBIDDEN_ACTIONS = {
    "execute_command",
    "spawn_process",
    "open_shell",
    "read_real_file",
    "write_real_file",
    "read_env",
    "read_secret",
    "network_request",
    "browser_open",
    "tool_call",
    "model_call",
    "persist_memory",
    "write_store",
    "modify_host",
    "access_clipboard",
    "control_screen",
    "perform_ui_action",
    "trigger_workflow",
    "control_physical_device",
}
BLOCKED_OPERATIONS = FORBIDDEN_ACTIONS
HIGH_RISK_SURFACES = {
    "filesystem",
    "network",
    "environment",
    "secrets",
    "processes",
    "shell",
    "tools",
    "model_invocation",
    "memory",
    "stores",
    "API",
    "UI",
    "browser",
    "clipboard",
    "host_system",
    "external_services",
    "physical_devices",
    "future_integrations",
}
FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "command_execution_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "network_enabled",
    "api_enabled",
    "ui_enabled",
    "writes_enabled",
    "stores_enabled",
    "filesystem_read_enabled",
    "filesystem_write_enabled",
    "process_spawn_enabled",
    "shell_enabled",
    "env_access_enabled",
    "secret_access_enabled",
    "host_access_enabled",
    "device_access_enabled",
    "clipboard_access_enabled",
    "browser_access_enabled",
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
class SandboxSurfaceClassification:
    surface: str
    known: bool
    risk_level: str
    requires_isolation: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SandboxOperationClassification:
    operation: str
    forbidden: bool
    risk_level: str
    requires_dry_run: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SandboxBoundaryDecision:
    sandbox_boundary_decision_id: str
    status: str
    decision: str
    readiness: str
    sandbox_mode: str
    requested_surface: str
    requested_operation: str
    risk_level: str
    requires_isolation: bool
    requires_dry_run: bool
    requires_human_review: bool
    allowed_to_execute: bool
    allowed_to_read_host: bool
    allowed_to_write_host: bool
    allowed_to_use_network: bool
    allowed_to_call_tool: bool
    allowed_to_persist: bool
    allowed_to_access_secret: bool
    allowed_to_control_ui: bool
    allowed_to_control_device: bool
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


def classify_sandbox_surface(surface: Any) -> SandboxSurfaceClassification:
    value = "" if surface is None else str(surface)
    risk = "high" if value in HIGH_RISK_SURFACES else "medium" if value in ISOLATION_SURFACES else "critical"
    return SandboxSurfaceClassification(
        surface=value,
        known=value in ISOLATION_SURFACES,
        risk_level=risk,
        requires_isolation=True,
    )


def classify_requested_operation(operation: Any) -> SandboxOperationClassification:
    value = "" if operation is None else str(operation)
    forbidden = value in BLOCKED_OPERATIONS
    return SandboxOperationClassification(
        operation=value,
        forbidden=forbidden,
        risk_level="critical" if forbidden else "low",
        requires_dry_run=True,
    )


def build_sandbox_boundary_profile() -> dict[str, Any]:
    return get_sandbox_boundary_contract()


def build_sandbox_boundary_decision(
    *,
    sandbox_boundary_decision_id: str,
    requested_surface: str,
    requested_operation: str,
    sandbox_mode: str = "contract_only",
    decision: str = "allowed_contractually",
    status: str = "evaluated",
    readiness: str = "ready_for_sandbox_boundary_e2e_checkpoint",
    risk_level: str = "low",
    requires_isolation: bool = True,
    requires_dry_run: bool = True,
    requires_human_review: bool = False,
    allowed_to_execute: bool = False,
    allowed_to_read_host: bool = False,
    allowed_to_write_host: bool = False,
    allowed_to_use_network: bool = False,
    allowed_to_call_tool: bool = False,
    allowed_to_persist: bool = False,
    allowed_to_access_secret: bool = False,
    allowed_to_control_ui: bool = False,
    allowed_to_control_device: bool = False,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> SandboxBoundaryDecision:
    return SandboxBoundaryDecision(
        sandbox_boundary_decision_id=sandbox_boundary_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        sandbox_mode=sandbox_mode,
        requested_surface=requested_surface,
        requested_operation=requested_operation,
        risk_level=risk_level,
        requires_isolation=requires_isolation,
        requires_dry_run=requires_dry_run,
        requires_human_review=requires_human_review,
        allowed_to_execute=allowed_to_execute,
        allowed_to_read_host=allowed_to_read_host,
        allowed_to_write_host=allowed_to_write_host,
        allowed_to_use_network=allowed_to_use_network,
        allowed_to_call_tool=allowed_to_call_tool,
        allowed_to_persist=allowed_to_persist,
        allowed_to_access_secret=allowed_to_access_secret,
        allowed_to_control_ui=allowed_to_control_ui,
        allowed_to_control_device=allowed_to_control_device,
        blocking_reasons=list(blocking_reasons or []),
        warnings=list(warnings or []),
        lineage=dict(lineage or {}),
        metadata=dict(metadata or {}),
    )


def evaluate_sandbox_boundary_contract(
    *,
    requested_surface: str,
    requested_operation: str,
    sandbox_mode: str = "contract_only",
) -> SandboxBoundaryDecision:
    surface = classify_sandbox_surface(requested_surface)
    operation = classify_requested_operation(requested_operation)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    if not surface.known or not requested_surface or not requested_operation:
        decision = "invalid"
        _block(blockers, "invalid_sandbox_request", "surface u operation invalida")
    elif operation.forbidden:
        decision = "blocked"
        _block(blockers, "operation_blocked_pre_runtime", "operacion prohibida en pre-runtime")
    elif surface.risk_level in {"high", "critical"}:
        decision = "isolated"
        warnings.append("surface_requires_isolation")
    else:
        decision = "allowed_contractually"

    risk_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    risk = surface.risk_level if risk_order[surface.risk_level] >= risk_order[operation.risk_level] else operation.risk_level

    return build_sandbox_boundary_decision(
        sandbox_boundary_decision_id=f"sandbox_boundary_{requested_surface or 'missing'}_{requested_operation or 'missing'}",
        requested_surface=requested_surface,
        requested_operation=requested_operation,
        sandbox_mode=sandbox_mode,
        decision=decision,
        status="evaluated" if decision != "invalid" else "invalid",
        risk_level=risk,
        requires_isolation=True,
        requires_dry_run=True,
        requires_human_review=risk in {"high", "critical"},
        allowed_to_execute=False,
        allowed_to_read_host=False,
        allowed_to_write_host=False,
        allowed_to_use_network=False,
        allowed_to_call_tool=False,
        allowed_to_persist=False,
        allowed_to_access_secret=False,
        allowed_to_control_ui=False,
        allowed_to_control_device=False,
        blocking_reasons=blockers,
        warnings=warnings,
        lineage={
            "agent_permission_boundary": "active_contractual_boundary",
            "secrets_policy_boundary": "active_contractual_boundary",
            "prompt_injection_defense_boundary": "active_contractual_boundary",
            "operational_readiness_gate_boundary": "closed",
        },
        metadata=_boundary_flags(),
    )


def validate_sandbox_boundary_decision(decision: SandboxBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_sandbox_boundary_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("sandbox_boundary_decision_id"), blockers, "missing_decision_id", "sandbox_boundary_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _allowed(payload.get("sandbox_mode"), SANDBOX_MODES, blockers, "invalid_sandbox_mode", "sandbox_mode invalido")
    _require(payload.get("requested_surface"), blockers, "missing_requested_surface", "requested_surface requerida")
    _require(payload.get("requested_operation"), blockers, "missing_requested_operation", "requested_operation requerida")
    _allowed(payload.get("risk_level"), RISK_LEVELS, blockers, "invalid_risk_level", "risk_level invalido")

    for field_name in ["requires_isolation", "requires_dry_run", "requires_human_review"]:
        if not isinstance(payload.get(field_name), bool):
            _block(blockers, f"{field_name}_not_bool", f"{field_name} debe ser booleano")
    for field_name in [
        "allowed_to_execute",
        "allowed_to_read_host",
        "allowed_to_write_host",
        "allowed_to_use_network",
        "allowed_to_call_tool",
        "allowed_to_persist",
        "allowed_to_access_secret",
        "allowed_to_control_ui",
        "allowed_to_control_device",
    ]:
        if payload.get(field_name) is not False:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} debe ser False")
    for field_name in ["blocking_reasons", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"{field_name}_not_list", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"{field_name}_not_dict", f"{field_name} debe ser dict")

    if payload.get("requested_operation") in BLOCKED_OPERATIONS and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_operation_not_blocked", "operacion prohibida debe quedar blocked o invalid")
    if payload.get("risk_level") in {"high", "critical"} and payload.get("decision") == "allowed_contractually" and not payload.get("requires_isolation"):
        _block(blockers, "high_risk_requires_isolation", "high/critical risk requiere aislamiento")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es sandbox provider, integration, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "SANDBOX_BOUNDARY_READY" if not blockers else "SANDBOX_BOUNDARY_BLOCKED",
        "readiness": "ready_for_sandbox_boundary_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["sandbox_boundary_decision_blocked"],
        "policy_status": SANDBOX_BOUNDARY_STATUS,
        "runtime_enabled": SANDBOX_RUNTIME_ENABLED,
        "command_execution_enabled": SANDBOX_COMMAND_EXECUTION_ENABLED,
        "network_enabled": SANDBOX_NETWORK_ENABLED,
        "tool_execution_enabled": SANDBOX_TOOL_EXECUTION_ENABLED,
    }


def serialize_sandbox_boundary_decision(decision: SandboxBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, SandboxBoundaryDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_sandbox_risk_report(decision: SandboxBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_sandbox_boundary_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "requested_surface": payload.get("requested_surface"),
        "requested_operation": payload.get("requested_operation"),
        "runtime_enabled": False,
        "requires_human_review": bool(payload.get("requires_human_review")),
    }


def get_sandbox_boundary_contract() -> dict[str, Any]:
    return {
        "status": SANDBOX_BOUNDARY_STATUS,
        "ready": SANDBOX_BOUNDARY_READY,
        "verdict": "SANDBOX_BOUNDARY_READY",
        "readiness": "ready_for_sandbox_boundary_e2e_checkpoint",
        "next_step": "PROMPT 3.25.1 — Checkpoint E2E de sandbox boundary",
        "mode": ["contract-only", "security-simulated", "non-operational", "pre-runtime", "isolation-first", "deny-by-default"],
        "central_rule": "En pre-runtime, el sandbox boundary solo describe limites. No concede acceso real a ninguna superficie operativa.",
        "isolation_surfaces": sorted(ISOLATION_SURFACES),
        "sandbox_modes": sorted(SANDBOX_MODES),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "boundary_flags": _boundary_flags(),
        "agent_permission_boundary": "active_contractual_boundary",
        "secrets_policy_boundary": "active_contractual_boundary",
        "prompt_injection_defense_boundary": "active_contractual_boundary",
        "operational_readiness_gate_boundary": "closed",
        "obliteratus": "not_sandbox_provider_not_integration_not_dependency_not_adapter_not_capability",
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": SANDBOX_RUNTIME_ENABLED,
        "command_execution_enabled": SANDBOX_COMMAND_EXECUTION_ENABLED,
        "tool_execution_enabled": SANDBOX_TOOL_EXECUTION_ENABLED,
        "model_invocation_enabled": SANDBOX_MODEL_INVOCATION_ENABLED,
        "memory_persistence_enabled": SANDBOX_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": SANDBOX_EXTERNAL_ACCESS_ENABLED,
        "network_enabled": SANDBOX_NETWORK_ENABLED,
        "api_enabled": SANDBOX_API_ENABLED,
        "ui_enabled": SANDBOX_UI_ENABLED,
        "writes_enabled": SANDBOX_WRITES_ENABLED,
        "stores_enabled": SANDBOX_STORES_ENABLED,
        "filesystem_read_enabled": SANDBOX_FILESYSTEM_READ_ENABLED,
        "filesystem_write_enabled": SANDBOX_FILESYSTEM_WRITE_ENABLED,
        "process_spawn_enabled": SANDBOX_PROCESS_SPAWN_ENABLED,
        "shell_enabled": SANDBOX_SHELL_ENABLED,
        "env_access_enabled": SANDBOX_ENV_ACCESS_ENABLED,
        "secret_access_enabled": SANDBOX_SECRET_ACCESS_ENABLED,
        "host_access_enabled": SANDBOX_HOST_ACCESS_ENABLED,
        "device_access_enabled": SANDBOX_DEVICE_ACCESS_ENABLED,
        "clipboard_access_enabled": SANDBOX_CLIPBOARD_ACCESS_ENABLED,
        "browser_access_enabled": SANDBOX_BROWSER_ACCESS_ENABLED,
        "ui_tars_enabled": SANDBOX_UI_TARS_ENABLED,
        "hermes_enabled": SANDBOX_HERMES_ENABLED,
        "n8n_enabled": SANDBOX_N8N_ENABLED,
        "home_assistant_enabled": SANDBOX_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": SANDBOX_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": SANDBOX_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    }


def _validate_boundary_flags(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for scope in [payload, payload.get("metadata", {}), payload.get("lineage", {})]:
        if isinstance(scope, dict):
            for key, value in scope.items():
                if key in FORBIDDEN_TRUE_FLAGS and value is True:
                    _block(blockers, f"{key}_not_allowed", f"{key}=True no permitido")
    for value in _flatten_values(payload):
        if isinstance(value, str) and value.lower() in FORBIDDEN_STRING_VALUES:
            _block(blockers, "forbidden_state_value", f"valor prohibido: {value}")


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
    blockers.append({"code": code, "message": message})
