"""Contract-only runtime activation gate for IA_CORE pre-runtime policy.

This module classifies conceptual runtime activation signals and validates gate
decisions. It never activates runtime, starts runners/workers/queues, executes
jobs, runs tools, invokes models, injects context, delivers outputs, writes
stores, uses network, reads secrets, or activates integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


RUNTIME_ACTIVATION_GATE_STATUS = "contract_only"
RUNTIME_ACTIVATION_GATE_READY = True

RUNTIME_ACTIVATION_ENABLED = False
RUNTIME_EXECUTION_ENABLED = False
RUNTIME_RUNNER_ENABLED = False
RUNTIME_SCHEDULER_ENABLED = False
RUNTIME_WORKER_ENABLED = False
RUNTIME_QUEUE_ENABLED = False
RUNTIME_ORCHESTRATOR_ENABLED = False
RUNTIME_EXECUTOR_ENABLED = False
RUNTIME_DISPATCHER_ENABLED = False
RUNTIME_BACKGROUND_JOBS_ENABLED = False
RUNTIME_AUTONOMY_ENABLED = False
RUNTIME_CONTINUOUS_LOOP_ENABLED = False

RUNTIME_TOOL_EXECUTION_ENABLED = False
RUNTIME_MODEL_INVOCATION_ENABLED = False
RUNTIME_CONTEXT_INJECTION_ENABLED = False
RUNTIME_OUTPUT_DELIVERY_ENABLED = False
RUNTIME_OUTPUT_PUBLISHING_ENABLED = False
RUNTIME_WRITES_ENABLED = False
RUNTIME_STORES_ENABLED = False
RUNTIME_MEMORY_PERSISTENCE_ENABLED = False
RUNTIME_EXTERNAL_ACCESS_ENABLED = False
RUNTIME_NETWORK_ENABLED = False
RUNTIME_API_ENABLED = False
RUNTIME_UI_ENABLED = False
RUNTIME_BROWSER_ENABLED = False
RUNTIME_FILESYSTEM_ENABLED = False
RUNTIME_COMMAND_EXECUTION_ENABLED = False
RUNTIME_SHELL_ENABLED = False
RUNTIME_PROCESS_SPAWN_ENABLED = False
RUNTIME_ENV_ACCESS_ENABLED = False
RUNTIME_SECRET_ACCESS_ENABLED = False
RUNTIME_HOST_ACCESS_ENABLED = False
RUNTIME_DEVICE_ACCESS_ENABLED = False
RUNTIME_CLIPBOARD_ENABLED = False

RUNTIME_UI_TARS_ENABLED = False
RUNTIME_HERMES_ENABLED = False
RUNTIME_N8N_ENABLED = False
RUNTIME_HOME_ASSISTANT_ENABLED = False

RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED = False
RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

ACTIVATION_SIGNALS = {
    "planning_signal",
    "contract_ready_signal",
    "e2e_passed_signal",
    "full_e2e_passed_signal",
    "boundary_chain_ready_signal",
    "human_review_signal",
    "approval_signal",
    "security_policy_signal",
    "sandbox_policy_signal",
    "tool_policy_signal",
    "model_policy_signal",
    "context_policy_signal",
    "output_policy_signal",
    "runtime_candidate_signal",
    "runtime_activation_request",
    "runtime_activation_decision",
}
PLANNING_SIGNALS = {"planning_signal", "contract_ready_signal", "security_policy_signal", "sandbox_policy_signal", "tool_policy_signal", "model_policy_signal", "context_policy_signal", "output_policy_signal"}
FUTURE_CONTRACT_SIGNALS = {"e2e_passed_signal", "full_e2e_passed_signal", "boundary_chain_ready_signal", "runtime_candidate_signal"}
HUMAN_APPROVAL_SIGNALS = {"human_review_signal", "approval_signal"}
BLOCKED_SIGNALS = {"runtime_activation_request", "runtime_activation_decision"}

FUTURE_CONDITIONS = {
    "future_runtime_contract_exists": False,
    "future_runtime_e2e_exists": False,
    "future_tool_executor_contract_exists": False,
    "future_model_provider_contract_exists": False,
    "future_context_builder_contract_exists": False,
    "future_output_delivery_contract_exists": False,
    "future_persistence_contract_exists": False,
    "future_scheduler_contract_exists": False,
    "future_worker_contract_exists": False,
    "future_queue_contract_exists": False,
    "future_observability_contract_exists": False,
    "future_kill_switch_contract_exists": False,
    "future_human_approval_contract_exists": False,
    "future_rollback_contract_exists": False,
    "future_audit_log_contract_exists": False,
    "future_environment_isolation_contract_exists": False,
    "future_secret_manager_contract_exists": False,
    "future_rate_limit_contract_exists": False,
    "future_budget_limit_contract_exists": False,
    "future_external_integration_contract_exists": False,
}

ALLOWED_ACTIONS = {
    "classify_runtime_activation_signal",
    "classify_runtime_activation_risk",
    "build_runtime_activation_gate_decision",
    "evaluate_runtime_activation_gate_contract",
    "validate_runtime_activation_gate_decision",
    "serialize_runtime_activation_gate_decision",
    "generate_runtime_activation_gate_report",
    "get_runtime_activation_gate_contract",
}
FORBIDDEN_ACTIONS = {
    "activate_runtime",
    "open_runtime_gate",
    "start_runtime_runner",
    "start_scheduler",
    "start_worker",
    "start_queue",
    "start_orchestrator",
    "start_executor",
    "dispatch_job",
    "enqueue_job",
    "run_background_job",
    "start_autonomous_loop",
    "execute_tool",
    "invoke_model",
    "inject_context",
    "deliver_output",
    "publish_output",
    "write_file",
    "write_store",
    "update_memory",
    "call_api",
    "network_request",
    "open_browser",
    "read_real_file",
    "write_real_file",
    "read_env",
    "read_secret",
    "run_command",
    "open_shell",
    "spawn_process",
    "control_ui",
    "control_device",
    "trigger_workflow",
    "perform_irreversible_action",
}

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"closed", "planning_only", "requires_future_contracts", "requires_human_approval", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_runtime_activation_gate_e2e_checkpoint", "blocked", "invalid"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_activation_enabled",
    "runtime_execution_enabled",
    "runtime_runner_enabled",
    "runtime_scheduler_enabled",
    "runtime_worker_enabled",
    "runtime_queue_enabled",
    "runtime_orchestrator_enabled",
    "runtime_executor_enabled",
    "runtime_dispatcher_enabled",
    "runtime_background_jobs_enabled",
    "runtime_autonomy_enabled",
    "runtime_continuous_loop_enabled",
    "runtime_tool_execution_enabled",
    "runtime_model_invocation_enabled",
    "runtime_context_injection_enabled",
    "runtime_output_delivery_enabled",
    "runtime_output_publishing_enabled",
    "runtime_writes_enabled",
    "runtime_stores_enabled",
    "runtime_memory_persistence_enabled",
    "runtime_external_access_enabled",
    "runtime_network_enabled",
    "runtime_api_enabled",
    "runtime_ui_enabled",
    "runtime_browser_enabled",
    "runtime_filesystem_enabled",
    "runtime_command_execution_enabled",
    "runtime_shell_enabled",
    "runtime_process_spawn_enabled",
    "runtime_env_access_enabled",
    "runtime_secret_access_enabled",
    "runtime_host_access_enabled",
    "runtime_device_access_enabled",
    "runtime_clipboard_enabled",
    "ui_tars_enabled",
    "hermes_enabled",
    "n8n_enabled",
    "home_assistant_enabled",
    "market_catalog_runtime_enabled",
    "business_composition_runtime_enabled",
}
FORBIDDEN_STRING_VALUES = {"market_catalog_active", "business_composition_enabled", "gate_open", "operations_enabled", "ready_for_runtime", "runtime_open", "runtime_active"}
OBLITERATUS_TOKEN = "obliteratus"


@dataclass(frozen=True)
class RuntimeActivationSignalClassification:
    activation_signal: str
    known: bool
    category: str
    risk_level: str
    blocked_by_default: bool = True
    requires_future_contracts: bool = True
    requires_human_approval: bool = True


@dataclass(frozen=True)
class RuntimeActivationRiskClassification:
    activation_signal: str
    operation: str
    risk_level: str
    forbidden_operation: bool
    requires_future_contracts: bool
    requires_human_approval: bool


@dataclass(frozen=True)
class RuntimeActivationGateDecision:
    runtime_activation_gate_decision_id: str
    status: str
    decision: str
    readiness: str
    activation_request_name: str
    requested_operation: str
    activation_signal: str
    risk_level: str
    requires_agent_permission: bool = True
    requires_secrets_policy: bool = True
    requires_prompt_injection_defense: bool = True
    requires_sandbox_boundary: bool = True
    requires_tool_boundary: bool = True
    requires_model_invocation_boundary: bool = True
    requires_context_boundary: bool = True
    requires_output_boundary: bool = True
    requires_operational_readiness_gate: bool = True
    requires_future_runtime_contract: bool = True
    requires_future_e2e: bool = True
    requires_human_approval: bool = True
    requires_kill_switch: bool = True
    requires_rollback: bool = True
    requires_audit: bool = True
    allowed_to_activate_runtime: bool = False
    allowed_to_execute: bool = False
    allowed_to_start_runner: bool = False
    allowed_to_start_scheduler: bool = False
    allowed_to_start_worker: bool = False
    allowed_to_start_queue: bool = False
    allowed_to_dispatch: bool = False
    allowed_to_execute_tool: bool = False
    allowed_to_invoke_model: bool = False
    allowed_to_inject_context: bool = False
    allowed_to_deliver_output: bool = False
    allowed_to_write: bool = False
    allowed_to_persist: bool = False
    allowed_to_use_network: bool = False
    allowed_to_access_secrets: bool = False
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    missing_future_conditions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_runtime_activation_signal(signal: str) -> RuntimeActivationSignalClassification:
    value = (signal or "").strip().lower()
    if value in PLANNING_SIGNALS:
        return RuntimeActivationSignalClassification(value, True, "planning_only", "low")
    if value in FUTURE_CONTRACT_SIGNALS:
        return RuntimeActivationSignalClassification(value, True, "requires_future_contracts", "high")
    if value in HUMAN_APPROVAL_SIGNALS:
        return RuntimeActivationSignalClassification(value, True, "requires_human_approval", "high")
    if value in BLOCKED_SIGNALS:
        return RuntimeActivationSignalClassification(value, True, "blocked", "critical")
    return RuntimeActivationSignalClassification(value, False, "unknown", "critical")


def classify_runtime_activation_risk(signal: str | None = None, operation: str | None = None) -> RuntimeActivationRiskClassification:
    classification = classify_runtime_activation_signal(signal or "")
    operation_value = (operation or "").strip().lower()
    forbidden_operation = operation_value in FORBIDDEN_ACTIONS
    risk = _max_risk(classification.risk_level, "critical" if forbidden_operation else "low")
    return RuntimeActivationRiskClassification(
        activation_signal=classification.activation_signal,
        operation=operation_value,
        risk_level=risk,
        forbidden_operation=forbidden_operation,
        requires_future_contracts=True,
        requires_human_approval=True,
    )


def build_runtime_activation_gate_decision(
    *,
    runtime_activation_gate_decision_id: str,
    activation_request_name: str,
    requested_operation: str,
    activation_signal: str,
    decision: str = "closed",
    status: str = "evaluated",
    readiness: str = "ready_for_runtime_activation_gate_e2e_checkpoint",
    risk_level: str = "low",
    blocking_reasons: list[dict[str, str]] | None = None,
    missing_future_conditions: list[str] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> RuntimeActivationGateDecision:
    return RuntimeActivationGateDecision(
        runtime_activation_gate_decision_id=runtime_activation_gate_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        activation_request_name=activation_request_name,
        requested_operation=requested_operation,
        activation_signal=activation_signal,
        risk_level=risk_level,
        blocking_reasons=deepcopy(blocking_reasons or []),
        missing_future_conditions=deepcopy(missing_future_conditions if missing_future_conditions is not None else _missing_future_conditions()),
        warnings=deepcopy(warnings or []),
        lineage={
            "agent_permission_boundary": "active_contractual_boundary",
            "secrets_policy_boundary": "active_contractual_boundary",
            "prompt_injection_defense_boundary": "active_contractual_boundary",
            "sandbox_boundary": "active_contractual_boundary",
            "tool_boundary": "active_contractual_boundary",
            "model_invocation_boundary": "active_contractual_boundary",
            "context_boundary": "active_contractual_boundary",
            "output_boundary": "active_contractual_boundary",
            "operational_readiness_gate_boundary": "closed",
            **deepcopy(lineage or {}),
        },
        metadata={**_boundary_flags(), **deepcopy(metadata or {})},
    )


def evaluate_runtime_activation_gate_contract(
    *,
    activation_request_name: str,
    requested_operation: str,
    activation_signal: str,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> RuntimeActivationGateDecision:
    classification = classify_runtime_activation_signal(activation_signal)
    risk = classify_runtime_activation_risk(activation_signal, requested_operation)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    _require(activation_request_name, blockers, "missing_activation_request_name", "activation_request_name requerido")
    if not classification.known:
        _block(blockers, "unknown_activation_signal", "activation_signal desconocida")
    if requested_operation in FORBIDDEN_ACTIONS:
        _block(blockers, "operation_blocked_pre_runtime", "operacion prohibida en pre-runtime")
    if _contains_obliteratus([activation_request_name, activation_signal, requested_operation, lineage, metadata]):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es runtime provider, dependency, adapter ni capability")

    missing_conditions = _missing_future_conditions()
    if blockers:
        decision = "invalid" if any(item["code"].startswith(("missing_", "unknown_", "obliteratus")) for item in blockers) else "blocked"
    elif activation_signal in BLOCKED_SIGNALS:
        decision = "blocked"
        _block(blockers, "runtime_activation_request_blocked", "runtime activation request bloqueada en pre-runtime")
    elif activation_signal in HUMAN_APPROVAL_SIGNALS:
        decision = "requires_human_approval"
        warnings.append("human_approval_required_but_runtime_stays_closed")
    elif activation_signal in FUTURE_CONTRACT_SIGNALS:
        decision = "requires_future_contracts"
        warnings.append("future_contracts_required_no_runtime_activation")
    elif activation_signal in PLANNING_SIGNALS:
        decision = "planning_only"
        warnings.append("planning_only_no_runtime_activation")
    else:
        decision = "closed"
        warnings.append("runtime_gate_closed")

    return build_runtime_activation_gate_decision(
        runtime_activation_gate_decision_id=f"runtime_activation_gate_{activation_request_name or 'missing_request'}_{activation_signal or 'missing_signal'}_{requested_operation or 'missing_operation'}",
        activation_request_name=activation_request_name,
        requested_operation=requested_operation,
        activation_signal=activation_signal,
        decision=decision,
        status="invalid" if decision == "invalid" else "evaluated",
        readiness="ready_for_runtime_activation_gate_e2e_checkpoint" if decision not in {"invalid", "blocked"} else "blocked",
        risk_level=risk.risk_level,
        blocking_reasons=blockers,
        missing_future_conditions=missing_conditions,
        warnings=warnings,
        lineage=lineage,
        metadata=metadata,
    )


def validate_runtime_activation_gate_decision(decision: RuntimeActivationGateDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_runtime_activation_gate_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("runtime_activation_gate_decision_id"), blockers, "missing_runtime_activation_gate_decision_id", "runtime_activation_gate_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _require(payload.get("activation_request_name"), blockers, "missing_activation_request_name", "activation_request_name requerido")
    _require(payload.get("requested_operation"), blockers, "missing_requested_operation", "requested_operation requerida")
    _require(payload.get("activation_signal"), blockers, "missing_activation_signal", "activation_signal requerida")
    _allowed(payload.get("risk_level"), RISK_LEVELS, blockers, "invalid_risk_level", "risk_level invalido")

    for field_name in [
        "requires_agent_permission",
        "requires_secrets_policy",
        "requires_prompt_injection_defense",
        "requires_sandbox_boundary",
        "requires_tool_boundary",
        "requires_model_invocation_boundary",
        "requires_context_boundary",
        "requires_output_boundary",
        "requires_operational_readiness_gate",
        "requires_future_runtime_contract",
        "requires_future_e2e",
        "requires_human_approval",
        "requires_kill_switch",
        "requires_rollback",
        "requires_audit",
    ]:
        if payload.get(field_name) is not True:
            _block(blockers, f"{field_name}_required", f"{field_name} debe ser True")
    for field_name in [
        "allowed_to_activate_runtime",
        "allowed_to_execute",
        "allowed_to_start_runner",
        "allowed_to_start_scheduler",
        "allowed_to_start_worker",
        "allowed_to_start_queue",
        "allowed_to_dispatch",
        "allowed_to_execute_tool",
        "allowed_to_invoke_model",
        "allowed_to_inject_context",
        "allowed_to_deliver_output",
        "allowed_to_write",
        "allowed_to_persist",
        "allowed_to_use_network",
        "allowed_to_access_secrets",
    ]:
        if payload.get(field_name) is not False:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} debe ser False")
    for field_name in ["blocking_reasons", "missing_future_conditions", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"{field_name}_not_list", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"{field_name}_not_dict", f"{field_name} debe ser dict")
    if not payload.get("missing_future_conditions"):
        _block(blockers, "missing_future_conditions_required", "deben listarse condiciones futuras faltantes")
    if payload.get("requested_operation") in FORBIDDEN_ACTIONS and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_operation_not_blocked", "operacion prohibida debe quedar blocked o invalid")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es runtime provider, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "RUNTIME_ACTIVATION_GATE_READY" if not blockers else "RUNTIME_ACTIVATION_GATE_BLOCKED",
        "readiness": "ready_for_runtime_activation_gate_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["runtime_activation_gate_decision_blocked"],
        "policy_status": RUNTIME_ACTIVATION_GATE_STATUS,
        "runtime_activation_enabled": RUNTIME_ACTIVATION_ENABLED,
        "runtime_execution_enabled": RUNTIME_EXECUTION_ENABLED,
    }


def serialize_runtime_activation_gate_decision(decision: RuntimeActivationGateDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, RuntimeActivationGateDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_runtime_activation_gate_report(decision: RuntimeActivationGateDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_runtime_activation_gate_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "activation_request_name": payload.get("activation_request_name"),
        "activation_signal": payload.get("activation_signal"),
        "requested_operation": payload.get("requested_operation"),
        "allowed_to_activate_runtime": False,
        "allowed_to_execute": False,
        "missing_future_conditions": list(payload.get("missing_future_conditions", [])),
    }


def get_runtime_activation_gate_contract() -> dict[str, Any]:
    return {
        "status": RUNTIME_ACTIVATION_GATE_STATUS,
        "ready": RUNTIME_ACTIVATION_GATE_READY,
        "verdict": "RUNTIME_ACTIVATION_GATE_READY",
        "readiness": "ready_for_runtime_activation_gate_e2e_checkpoint",
        "next_step": "PROMPT 3.30.1 - Checkpoint E2E de runtime activation gate",
        "mode": [
            "contract-only",
            "security-simulated",
            "non-operational",
            "pre-runtime",
            "activation-gate-only",
            "deny-by-default",
            "boundary-aware",
            "permission-aware",
            "secrets-aware",
            "prompt-injection-aware",
            "sandbox-aware",
            "tool-boundary-aware",
            "model-invocation-aware",
            "context-boundary-aware",
            "output-boundary-aware",
            "no runtime activation",
        ],
        "central_rule": "Ninguna senal individual abre runtime. Ni ready, ni E2E passed, ni chain ready, ni approval conceptual activan ejecucion real.",
        "activation_signals": sorted(ACTIVATION_SIGNALS),
        "future_conditions": deepcopy(FUTURE_CONDITIONS),
        "missing_future_conditions": _missing_future_conditions(),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "decisions": sorted(ALLOWED_DECISIONS),
        "boundary_flags": _boundary_flags(),
        "agent_permission_boundary": "active_contractual_boundary",
        "secrets_policy_boundary": "active_contractual_boundary",
        "prompt_injection_defense_boundary": "active_contractual_boundary",
        "sandbox_boundary": "active_contractual_boundary",
        "tool_boundary": "active_contractual_boundary",
        "model_invocation_boundary": "active_contractual_boundary",
        "context_boundary": "active_contractual_boundary",
        "output_boundary": "active_contractual_boundary",
        "operational_readiness_gate_boundary": "closed",
        "obliteratus": "not_runtime_provider_not_integration_not_dependency_not_adapter_not_capability",
    }


def _missing_future_conditions() -> list[str]:
    return [name for name, satisfied in FUTURE_CONDITIONS.items() if satisfied is False]


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_activation_enabled": RUNTIME_ACTIVATION_ENABLED,
        "runtime_execution_enabled": RUNTIME_EXECUTION_ENABLED,
        "runtime_runner_enabled": RUNTIME_RUNNER_ENABLED,
        "runtime_scheduler_enabled": RUNTIME_SCHEDULER_ENABLED,
        "runtime_worker_enabled": RUNTIME_WORKER_ENABLED,
        "runtime_queue_enabled": RUNTIME_QUEUE_ENABLED,
        "runtime_orchestrator_enabled": RUNTIME_ORCHESTRATOR_ENABLED,
        "runtime_executor_enabled": RUNTIME_EXECUTOR_ENABLED,
        "runtime_dispatcher_enabled": RUNTIME_DISPATCHER_ENABLED,
        "runtime_background_jobs_enabled": RUNTIME_BACKGROUND_JOBS_ENABLED,
        "runtime_autonomy_enabled": RUNTIME_AUTONOMY_ENABLED,
        "runtime_continuous_loop_enabled": RUNTIME_CONTINUOUS_LOOP_ENABLED,
        "runtime_tool_execution_enabled": RUNTIME_TOOL_EXECUTION_ENABLED,
        "runtime_model_invocation_enabled": RUNTIME_MODEL_INVOCATION_ENABLED,
        "runtime_context_injection_enabled": RUNTIME_CONTEXT_INJECTION_ENABLED,
        "runtime_output_delivery_enabled": RUNTIME_OUTPUT_DELIVERY_ENABLED,
        "runtime_output_publishing_enabled": RUNTIME_OUTPUT_PUBLISHING_ENABLED,
        "runtime_writes_enabled": RUNTIME_WRITES_ENABLED,
        "runtime_stores_enabled": RUNTIME_STORES_ENABLED,
        "runtime_memory_persistence_enabled": RUNTIME_MEMORY_PERSISTENCE_ENABLED,
        "runtime_external_access_enabled": RUNTIME_EXTERNAL_ACCESS_ENABLED,
        "runtime_network_enabled": RUNTIME_NETWORK_ENABLED,
        "runtime_api_enabled": RUNTIME_API_ENABLED,
        "runtime_ui_enabled": RUNTIME_UI_ENABLED,
        "runtime_browser_enabled": RUNTIME_BROWSER_ENABLED,
        "runtime_filesystem_enabled": RUNTIME_FILESYSTEM_ENABLED,
        "runtime_command_execution_enabled": RUNTIME_COMMAND_EXECUTION_ENABLED,
        "runtime_shell_enabled": RUNTIME_SHELL_ENABLED,
        "runtime_process_spawn_enabled": RUNTIME_PROCESS_SPAWN_ENABLED,
        "runtime_env_access_enabled": RUNTIME_ENV_ACCESS_ENABLED,
        "runtime_secret_access_enabled": RUNTIME_SECRET_ACCESS_ENABLED,
        "runtime_host_access_enabled": RUNTIME_HOST_ACCESS_ENABLED,
        "runtime_device_access_enabled": RUNTIME_DEVICE_ACCESS_ENABLED,
        "runtime_clipboard_enabled": RUNTIME_CLIPBOARD_ENABLED,
        "ui_tars_enabled": RUNTIME_UI_TARS_ENABLED,
        "hermes_enabled": RUNTIME_HERMES_ENABLED,
        "n8n_enabled": RUNTIME_N8N_ENABLED,
        "home_assistant_enabled": RUNTIME_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
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
