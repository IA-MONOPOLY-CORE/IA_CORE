"""Non-operational Runtime Governance contract.

This module only represents future governance decisions as deterministic,
JSON-safe data. It never opens files, writes stores, reads environment,
uses network/browser access, runs commands, invokes tools/models, starts
workers, mutates runtime state, or enables execution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping


RUNTIME_GOVERNANCE_CONTRACT_READY = True
RUNTIME_GOVERNANCE_OPERATIONAL = False
RUNTIME_GOVERNANCE_ACTIVATION_ENABLED = False
RUNTIME_GOVERNANCE_EXECUTION_ENABLED = False
RUNTIME_GOVERNANCE_CONTROLLER_ENABLED = False
RUNTIME_GOVERNANCE_MANAGER_ENABLED = False
RUNTIME_GOVERNANCE_STATE_MUTATION_ENABLED = False
RUNTIME_GOVERNANCE_EVENT_BUS_ENABLED = False
RUNTIME_GOVERNANCE_AUDIT_RUNTIME_ENABLED = False
RUNTIME_GOVERNANCE_APPROVAL_RUNTIME_ENABLED = False
RUNTIME_GOVERNANCE_KILL_SWITCH_RUNTIME_ENABLED = False
RUNTIME_GOVERNANCE_ROLLBACK_RUNTIME_ENABLED = False
RUNTIME_GOVERNANCE_DRY_RUN_EXECUTION_ENABLED = False
RUNTIME_GOVERNANCE_TOOL_EXECUTION_ENABLED = False
RUNTIME_GOVERNANCE_MODEL_INVOCATION_ENABLED = False
RUNTIME_GOVERNANCE_CONTEXT_INJECTION_ENABLED = False
RUNTIME_GOVERNANCE_OUTPUT_DELIVERY_ENABLED = False
RUNTIME_GOVERNANCE_OUTPUT_PUBLISHING_ENABLED = False
RUNTIME_GOVERNANCE_WRITES_ENABLED = False
RUNTIME_GOVERNANCE_STORES_ENABLED = False
RUNTIME_GOVERNANCE_MEMORY_PERSISTENCE_ENABLED = False
RUNTIME_GOVERNANCE_NETWORK_ENABLED = False
RUNTIME_GOVERNANCE_API_ENABLED = False
RUNTIME_GOVERNANCE_BROWSER_ENABLED = False
RUNTIME_GOVERNANCE_FILESYSTEM_ENABLED = False
RUNTIME_GOVERNANCE_ENV_ACCESS_ENABLED = False
RUNTIME_GOVERNANCE_SECRET_ACCESS_ENABLED = False
RUNTIME_GOVERNANCE_UI_CONTROL_ENABLED = False
RUNTIME_GOVERNANCE_DEVICE_CONTROL_ENABLED = False
RUNTIME_GOVERNANCE_UI_TARS_ENABLED = False
RUNTIME_GOVERNANCE_HERMES_ENABLED = False
RUNTIME_GOVERNANCE_N8N_ENABLED = False
RUNTIME_GOVERNANCE_HOME_ASSISTANT_ENABLED = False
RUNTIME_GOVERNANCE_MARKET_CATALOG_RUNTIME_ENABLED = False
RUNTIME_GOVERNANCE_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False
OBLITERATUS_RUNTIME_GOVERNANCE_ENABLED = False

CONTRACT_STATUS = "RUNTIME_GOVERNANCE_CONTRACT_READY"
CONTRACT_VERDICT = "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_runtime_governance_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 3.43.1 — Checkpoint E2E de Runtime Governance contract"


class RuntimeGovernanceScope(str, Enum):
    RUNTIME_ACTIVATION = "runtime_activation"
    RUNTIME_EXECUTION = "runtime_execution"
    RUNTIME_STATE = "runtime_state"
    DRY_RUN = "dry_run"
    ATTEMPT = "attempt"
    LIFECYCLE = "lifecycle"
    RESULT = "result"
    PROJECTION_READ_MODEL = "projection_read_model"
    TOOL_EXECUTION = "tool_execution"
    MODEL_INVOCATION = "model_invocation"
    CONTEXT_INJECTION = "context_injection"
    OUTPUT_DELIVERY = "output_delivery"
    WRITES_STORES = "writes_stores"
    MEMORY_PERSISTENCE = "memory_persistence"
    NETWORK_API_BROWSER = "network_api_browser"
    FILESYSTEM_ENV_SECRETS = "filesystem_env_secrets"
    HUMAN_APPROVAL = "human_approval"
    KILL_SWITCH = "kill_switch"
    ROLLBACK = "rollback"
    OBSERVABILITY_AUDIT_TRAIL = "observability_audit_trail"
    SIDE_EFFECTS = "side_effects"
    INTEGRATION = "integration"
    UI_RUNTIME_BRIDGE = "ui_runtime_bridge"
    MARKET_CATALOG_RUNTIME = "market_catalog_runtime"
    BUSINESS_COMPOSITION_RUNTIME = "business_composition_runtime"


class RuntimeGovernanceDecision(str, Enum):
    GOVERNANCE_ALLOWED_SIMULATED = "governance_allowed_simulated"
    GOVERNANCE_BLOCKED = "governance_blocked"
    GOVERNANCE_REQUIRES_HUMAN_APPROVAL = "governance_requires_human_approval"
    GOVERNANCE_REQUIRES_AUDIT_TRAIL = "governance_requires_audit_trail"
    GOVERNANCE_REQUIRES_KILL_SWITCH = "governance_requires_kill_switch"
    GOVERNANCE_REQUIRES_ROLLBACK = "governance_requires_rollback"
    GOVERNANCE_REQUIRES_RUNTIME_GATE = "governance_requires_runtime_gate"
    GOVERNANCE_REQUIRES_SECURITY_LAYER = "governance_requires_security_layer"
    GOVERNANCE_INVALID = "governance_invalid"


class RuntimeGovernanceReadiness(str, Enum):
    READY_FOR_RUNTIME_GOVERNANCE_CONTRACT_E2E = "ready_for_runtime_governance_contract_e2e"


class RuntimeGovernanceBlockReason(str, Enum):
    DEFAULT_DENY = "default_deny"
    MISSING_SECURITY_LAYER = "missing_security_layer"
    MISSING_RUNTIME_GATE = "missing_runtime_gate"
    MISSING_HUMAN_APPROVAL = "missing_human_approval"
    MISSING_AUDIT_TRAIL = "missing_audit_trail"
    MISSING_KILL_SWITCH = "missing_kill_switch"
    MISSING_ROLLBACK = "missing_rollback"
    MISSING_DRY_RUN = "missing_dry_run"
    DANGEROUS_METADATA = "dangerous_metadata"
    FORBIDDEN_READINESS = "forbidden_readiness"
    OPERATIONAL_SCOPE_REQUESTED = "operational_scope_requested"


class RuntimeGovernanceRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


ALLOWED_READINESS = (RuntimeGovernanceReadiness.READY_FOR_RUNTIME_GOVERNANCE_CONTRACT_E2E.value,)
FORBIDDEN_READINESS = (
    "ready_for_runtime",
    "ready_for_runtime_activation",
    "ready_for_execution",
    "ready_for_dry_run_execution",
    "ready_for_tool_execution",
    "ready_for_model_invocation",
    "ready_for_context_injection",
    "ready_for_output_delivery",
    "ready_for_writes",
    "ready_for_stores",
    "runtime_open",
    "runtime_active",
    "runtime_enabled",
    "execution_enabled",
    "operations_enabled",
    "gate_open",
    "approval_enabled",
    "human_approval_operational",
    "kill_switch_enabled",
    "rollback_enabled",
    "observability_runtime_enabled",
)
DANGEROUS_METADATA_KEYS = (
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "credential",
    "credentials",
    "private_key",
    "raw_payload",
    "payload",
    "raw_output",
    "output",
    "file_content",
    "env",
    "environment",
    "cookie",
    "authorization",
    "bearer",
)
REQUIRED_DEPENDENCIES = (
    "security_layer",
    "runtime_activation_gate",
    "human_approval",
    "audit_trail",
    "kill_switch",
    "rollback",
    "dry_run_before_execution",
)


@dataclass(frozen=True)
class RuntimeGovernancePolicy:
    contract_version: str
    security_layer_required: bool
    runtime_activation_gate_required: bool
    human_approval_required: bool
    audit_trail_required: bool
    kill_switch_required: bool
    rollback_required: bool
    dry_run_required_before_execution: bool
    default_decision: RuntimeGovernanceDecision
    allowed_readiness: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    forbidden_scopes_operational: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    metadata_schema_version: str


@dataclass(frozen=True)
class RuntimeGovernanceRequest:
    request_id: str
    scope: RuntimeGovernanceScope
    requested_decision: RuntimeGovernanceDecision
    requested_by: str
    reason: str
    target_scope: str
    target_ids: tuple[str, ...]
    risk_level: RuntimeGovernanceRiskLevel
    security_baseline_ref: str
    runtime_gate_ref: str
    dry_run_ref: str | None = None
    human_approval_ref: str | None = None
    audit_trail_ref: str | None = None
    kill_switch_ref: str | None = None
    rollback_ref: str | None = None
    metadata_sanitized: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class RuntimeGovernanceEvidence:
    security_layer_status: str
    post_security_checkpoint_status: str
    runtime_gate_status: str
    dry_run_contract_status: str
    observability_audit_status: str
    kill_switch_contract_status: str
    human_approval_plan_status: str
    policy_checks: tuple[str, ...]
    blocked_capabilities_confirmed: tuple[str, ...]
    missing_dependencies: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeGovernanceDecisionRecord:
    request_id: str
    scope: RuntimeGovernanceScope
    decision: RuntimeGovernanceDecision
    block_reasons: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    missing_dependencies: tuple[str, ...]
    readiness: RuntimeGovernanceReadiness
    side_effects_allowed: bool
    runtime_activation_allowed: bool
    runtime_execution_allowed: bool
    dry_run_execution_allowed: bool
    tool_execution_allowed: bool
    model_invocation_allowed: bool
    context_injection_allowed: bool
    output_delivery_allowed: bool
    writes_allowed: bool
    stores_allowed: bool
    memory_persistence_allowed: bool
    network_allowed: bool
    api_allowed: bool
    browser_allowed: bool
    filesystem_allowed: bool
    env_access_allowed: bool
    secret_access_allowed: bool
    ui_control_allowed: bool
    device_control_allowed: bool
    integration_allowed: bool
    metadata_sanitized: Mapping[str, Any]


@dataclass(frozen=True)
class RuntimeGovernanceContractSnapshot:
    status: str
    verdict: str
    readiness: RuntimeGovernanceReadiness
    operational: bool
    policy: RuntimeGovernancePolicy
    blocked_capabilities: tuple[str, ...]
    forbidden_modules: tuple[str, ...]
    next_step: str


def build_default_runtime_governance_policy() -> RuntimeGovernancePolicy:
    return RuntimeGovernancePolicy(
        contract_version="1.0",
        security_layer_required=True,
        runtime_activation_gate_required=True,
        human_approval_required=True,
        audit_trail_required=True,
        kill_switch_required=True,
        rollback_required=True,
        dry_run_required_before_execution=True,
        default_decision=RuntimeGovernanceDecision.GOVERNANCE_BLOCKED,
        allowed_readiness=ALLOWED_READINESS,
        forbidden_readiness=FORBIDDEN_READINESS,
        forbidden_scopes_operational=tuple(scope.value for scope in RuntimeGovernanceScope),
        blocked_capabilities=runtime_governance_blocked_capabilities(),
        metadata_schema_version="1.0",
    )


def validate_runtime_governance_request(
    request: RuntimeGovernanceRequest,
    policy: RuntimeGovernancePolicy | None = None,
) -> tuple[str, ...]:
    policy = policy or build_default_runtime_governance_policy()
    reasons: list[str] = []
    if not isinstance(request, RuntimeGovernanceRequest):
        raise TypeError("request must be RuntimeGovernanceRequest")
    for field_name in ("request_id", "requested_by", "reason", "target_scope", "security_baseline_ref", "runtime_gate_ref"):
        if not getattr(request, field_name).strip():
            reasons.append(f"missing_{field_name}")
    if not request.target_ids or any(not isinstance(item, str) or not item.strip() for item in request.target_ids):
        reasons.append("missing_target_ids")
    reasons.extend(_metadata_errors(request.metadata_sanitized or {}))
    if any(readiness not in ALLOWED_READINESS for readiness in policy.allowed_readiness):
        reasons.append(RuntimeGovernanceBlockReason.FORBIDDEN_READINESS.value)
    return tuple(reasons)


def evaluate_runtime_governance_request(
    request: RuntimeGovernanceRequest,
    evidence: RuntimeGovernanceEvidence,
    policy: RuntimeGovernancePolicy | None = None,
) -> RuntimeGovernanceDecisionRecord:
    policy = policy or build_default_runtime_governance_policy()
    block_reasons = list(validate_runtime_governance_request(request, policy))
    missing = list(evidence.missing_dependencies)
    if missing:
        block_reasons.extend(f"missing_dependency:{item}" for item in missing)
        decision = RuntimeGovernanceDecision.GOVERNANCE_BLOCKED
    elif any(reason.startswith("metadata_") for reason in block_reasons):
        decision = RuntimeGovernanceDecision.GOVERNANCE_INVALID
    elif request.scope == RuntimeGovernanceScope.RUNTIME_ACTIVATION:
        decision = RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_RUNTIME_GATE
    elif request.scope in {
        RuntimeGovernanceScope.TOOL_EXECUTION,
        RuntimeGovernanceScope.MODEL_INVOCATION,
        RuntimeGovernanceScope.CONTEXT_INJECTION,
        RuntimeGovernanceScope.OUTPUT_DELIVERY,
        RuntimeGovernanceScope.WRITES_STORES,
        RuntimeGovernanceScope.MEMORY_PERSISTENCE,
        RuntimeGovernanceScope.NETWORK_API_BROWSER,
        RuntimeGovernanceScope.FILESYSTEM_ENV_SECRETS,
        RuntimeGovernanceScope.INTEGRATION,
        RuntimeGovernanceScope.UI_RUNTIME_BRIDGE,
        RuntimeGovernanceScope.MARKET_CATALOG_RUNTIME,
        RuntimeGovernanceScope.BUSINESS_COMPOSITION_RUNTIME,
    }:
        decision = RuntimeGovernanceDecision.GOVERNANCE_BLOCKED
        block_reasons.append(RuntimeGovernanceBlockReason.OPERATIONAL_SCOPE_REQUESTED.value)
    elif _has_all_conceptual_refs(request) and not block_reasons:
        decision = RuntimeGovernanceDecision.GOVERNANCE_ALLOWED_SIMULATED
    else:
        decision = _dependency_decision_for_request(request)
        if not block_reasons:
            block_reasons.append(RuntimeGovernanceBlockReason.DEFAULT_DENY.value)
    if any(reason.startswith("metadata_") for reason in block_reasons):
        decision = RuntimeGovernanceDecision.GOVERNANCE_INVALID
    return RuntimeGovernanceDecisionRecord(
        request_id=request.request_id,
        scope=request.scope,
        decision=decision,
        block_reasons=tuple(dict.fromkeys(block_reasons)),
        required_dependencies=REQUIRED_DEPENDENCIES,
        missing_dependencies=tuple(missing),
        readiness=RuntimeGovernanceReadiness.READY_FOR_RUNTIME_GOVERNANCE_CONTRACT_E2E,
        side_effects_allowed=False,
        runtime_activation_allowed=False,
        runtime_execution_allowed=False,
        dry_run_execution_allowed=False,
        tool_execution_allowed=False,
        model_invocation_allowed=False,
        context_injection_allowed=False,
        output_delivery_allowed=False,
        writes_allowed=False,
        stores_allowed=False,
        memory_persistence_allowed=False,
        network_allowed=False,
        api_allowed=False,
        browser_allowed=False,
        filesystem_allowed=False,
        env_access_allowed=False,
        secret_access_allowed=False,
        ui_control_allowed=False,
        device_control_allowed=False,
        integration_allowed=False,
        metadata_sanitized=request.metadata_sanitized or {},
    )


def build_runtime_governance_snapshot(
    policy: RuntimeGovernancePolicy | None = None,
) -> RuntimeGovernanceContractSnapshot:
    policy = policy or build_default_runtime_governance_policy()
    return RuntimeGovernanceContractSnapshot(
        status=CONTRACT_STATUS,
        verdict=CONTRACT_VERDICT,
        readiness=RuntimeGovernanceReadiness.READY_FOR_RUNTIME_GOVERNANCE_CONTRACT_E2E,
        operational=False,
        policy=policy,
        blocked_capabilities=runtime_governance_blocked_capabilities(),
        forbidden_modules=runtime_governance_forbidden_modules(),
        next_step=CONTRACT_NEXT_STEP,
    )


def runtime_governance_contract_status() -> dict[str, Any]:
    return runtime_governance_to_dict(build_runtime_governance_snapshot())


def runtime_governance_forbidden_modules() -> tuple[str, ...]:
    return (
        "core/runtime_governance.py",
        "core/runtime_state.py",
        "core/runtime_state_contract.py",
        "core/runtime_controller.py",
        "core/runtime_manager.py",
        "core/runtime_runner.py",
        "core/runtime_scheduler.py",
        "core/runtime_worker.py",
        "core/runtime_queue.py",
        "core/runtime_executor.py",
        "core/runtime_orchestrator.py",
        "core/runtime_dispatcher.py",
        "core/runtime_event_schema.py",
        "core/runtime_event_bus.py",
        "core/human_approval_gate.py",
        "core/human_approval_contract.py",
        "core/human_approval_store.py",
        "core/human_approval_audit.py",
        "core/approval_request.py",
        "core/approval_decision.py",
        "core/approval_workflow.py",
        "core/approval_ui.py",
        "core/approval_api.py",
        "core/approval_endpoint.py",
        "core/approval_runtime.py",
        "core/kill_switch.py",
        "core/rollback_controller.py",
        "core/audit_trail.py",
        "core/event_bus.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    )


def runtime_governance_blocked_capabilities() -> tuple[str, ...]:
    return (
        "runtime governance operativo",
        "runtime governance activation",
        "runtime governance execution",
        "runtime state mutation",
        "runtime controller",
        "runtime manager",
        "runtime activation",
        "runtime execution",
        "runtime runner",
        "runtime scheduler",
        "runtime worker",
        "runtime queue",
        "runtime executor",
        "runtime orchestrator",
        "runtime dispatcher",
        "runtime event bus",
        "dry-run execution activation",
        "tool execution",
        "model invocation",
        "context injection",
        "output delivery",
        "writes reales",
        "stores operativos",
        "memory persistence",
        "API calls",
        "network",
        "browser",
        "real filesystem reads",
        "real filesystem writes",
        "env access",
        "secret access",
        "UI control",
        "device control",
        "UI-TARS runtime",
        "Hermes runtime",
        "n8n real workflows",
        "Home Assistant real actions",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS integration",
    )


def runtime_governance_to_dict(obj: Any) -> Any:
    payload = _to_json_safe(obj)
    json.dumps(payload, sort_keys=True)
    return payload


def _dependency_decision_for_request(request: RuntimeGovernanceRequest) -> RuntimeGovernanceDecision:
    if not request.security_baseline_ref:
        return RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_SECURITY_LAYER
    if not request.runtime_gate_ref:
        return RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_RUNTIME_GATE
    if not request.human_approval_ref:
        return RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_HUMAN_APPROVAL
    if not request.audit_trail_ref:
        return RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_AUDIT_TRAIL
    if not request.kill_switch_ref:
        return RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_KILL_SWITCH
    if not request.rollback_ref:
        return RuntimeGovernanceDecision.GOVERNANCE_REQUIRES_ROLLBACK
    return RuntimeGovernanceDecision.GOVERNANCE_BLOCKED


def _has_all_conceptual_refs(request: RuntimeGovernanceRequest) -> bool:
    return all(
        [
            request.security_baseline_ref,
            request.runtime_gate_ref,
            request.dry_run_ref,
            request.human_approval_ref,
            request.audit_trail_ref,
            request.kill_switch_ref,
            request.rollback_ref,
        ]
    )


def _metadata_errors(metadata: Mapping[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        json.dumps(metadata, sort_keys=True)
    except TypeError:
        return ("metadata_not_json_safe",)
    _scan_metadata(metadata, errors, "metadata_sanitized")
    return tuple(errors)


def _scan_metadata(value: Any, errors: list[str], path: str) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            lowered = str(key).lower()
            if lowered in DANGEROUS_METADATA_KEYS or any(fragment in lowered for fragment in DANGEROUS_METADATA_KEYS):
                errors.append(f"metadata_dangerous_key:{path}.{key}")
            _scan_metadata(nested, errors, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _scan_metadata(nested, errors, f"{path}[{index}]")


def _to_json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _to_json_safe(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _to_json_safe(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_to_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_to_json_safe(item) for item in value]
    json.dumps(value)
    return value
