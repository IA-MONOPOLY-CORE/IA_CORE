
"""Non-operational Runtime State contract.

Pure, deterministic, JSON-safe contract objects for future runtime state.
This module performs no IO, no env/secret reads, no network, no commands,
no runtime activation, no store mutation, and no execution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping


RUNTIME_STATE_CONTRACT_READY = True
RUNTIME_STATE_OPERATIONAL = False
RUNTIME_STATE_ACTIVATION_ENABLED = False
RUNTIME_STATE_MUTATION_ENABLED = False
RUNTIME_STATE_STORE_ENABLED = False
RUNTIME_STATE_WRITER_ENABLED = False
RUNTIME_STATE_READER_ENABLED = False
RUNTIME_STATE_TRANSITION_EXECUTION_ENABLED = False
RUNTIME_STATE_EVENT_BUS_ENABLED = False
RUNTIME_STATE_RUNTIME_ACTIVATION_ENABLED = False
RUNTIME_STATE_RUNTIME_EXECUTION_ENABLED = False
RUNTIME_STATE_DRY_RUN_EXECUTION_ENABLED = False
RUNTIME_STATE_TOOL_EXECUTION_ENABLED = False
RUNTIME_STATE_MODEL_INVOCATION_ENABLED = False
RUNTIME_STATE_CONTEXT_INJECTION_ENABLED = False
RUNTIME_STATE_OUTPUT_DELIVERY_ENABLED = False
RUNTIME_STATE_OUTPUT_PUBLISHING_ENABLED = False
RUNTIME_STATE_WRITES_ENABLED = False
RUNTIME_STATE_STORES_ENABLED = False
RUNTIME_STATE_MEMORY_PERSISTENCE_ENABLED = False
RUNTIME_STATE_NETWORK_ENABLED = False
RUNTIME_STATE_API_ENABLED = False
RUNTIME_STATE_BROWSER_ENABLED = False
RUNTIME_STATE_FILESYSTEM_ENABLED = False
RUNTIME_STATE_ENV_ACCESS_ENABLED = False
RUNTIME_STATE_SECRET_ACCESS_ENABLED = False
RUNTIME_STATE_UI_CONTROL_ENABLED = False
RUNTIME_STATE_DEVICE_CONTROL_ENABLED = False
RUNTIME_STATE_UI_TARS_ENABLED = False
RUNTIME_STATE_HERMES_ENABLED = False
RUNTIME_STATE_N8N_ENABLED = False
RUNTIME_STATE_HOME_ASSISTANT_ENABLED = False
RUNTIME_STATE_MARKET_CATALOG_RUNTIME_ENABLED = False
RUNTIME_STATE_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False
OBLITERATUS_RUNTIME_STATE_ENABLED = False

CONTRACT_STATUS = "RUNTIME_STATE_CONTRACT_READY"
CONTRACT_VERDICT = "RUNTIME_STATE_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_runtime_state_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 3.45.1 — Checkpoint E2E de Runtime State contract"


class RuntimeStateValue(str, Enum):
    UNINITIALIZED = "runtime_state_uninitialized"
    GOVERNANCE_PENDING = "runtime_state_governance_pending"
    SECURITY_BLOCKED = "runtime_state_security_blocked"
    POLICY_BLOCKED = "runtime_state_policy_blocked"
    READY_SIMULATED = "runtime_state_ready_simulated"
    DRY_RUN_REQUIRED = "runtime_state_dry_run_required"
    HUMAN_APPROVAL_REQUIRED = "runtime_state_human_approval_required"
    AUDIT_TRAIL_REQUIRED = "runtime_state_audit_trail_required"
    KILL_SWITCH_REQUIRED = "runtime_state_kill_switch_required"
    ROLLBACK_REQUIRED = "runtime_state_rollback_required"
    BLOCKED = "runtime_state_blocked"
    INVALID = "runtime_state_invalid"
    ARCHIVED_SIMULATED = "runtime_state_archived_simulated"


class RuntimeStateTransition(str, Enum):
    UNINITIALIZED_TO_GOVERNANCE_PENDING = "uninitialized_to_governance_pending"
    GOVERNANCE_PENDING_TO_SECURITY_BLOCKED = "governance_pending_to_security_blocked"
    GOVERNANCE_PENDING_TO_POLICY_BLOCKED = "governance_pending_to_policy_blocked"
    GOVERNANCE_PENDING_TO_READY_SIMULATED = "governance_pending_to_ready_simulated"
    READY_SIMULATED_TO_DRY_RUN_REQUIRED = "ready_simulated_to_dry_run_required"
    READY_SIMULATED_TO_HUMAN_APPROVAL_REQUIRED = "ready_simulated_to_human_approval_required"
    READY_SIMULATED_TO_AUDIT_TRAIL_REQUIRED = "ready_simulated_to_audit_trail_required"
    READY_SIMULATED_TO_KILL_SWITCH_REQUIRED = "ready_simulated_to_kill_switch_required"
    READY_SIMULATED_TO_ROLLBACK_REQUIRED = "ready_simulated_to_rollback_required"
    ANY_TO_BLOCKED = "any_to_blocked"
    ANY_TO_INVALID = "any_to_invalid"
    ANY_TO_ARCHIVED_SIMULATED = "any_to_archived_simulated"


class RuntimeStateDecision(str, Enum):
    TRANSITION_ALLOWED_SIMULATED = "runtime_state_transition_allowed_simulated"
    TRANSITION_BLOCKED = "runtime_state_transition_blocked"
    TRANSITION_INVALID = "runtime_state_transition_invalid"
    REQUIRES_RUNTIME_GOVERNANCE = "runtime_state_requires_runtime_governance"
    REQUIRES_SECURITY_LAYER = "runtime_state_requires_security_layer"
    REQUIRES_RUNTIME_GATE = "runtime_state_requires_runtime_gate"
    REQUIRES_HUMAN_APPROVAL = "runtime_state_requires_human_approval"
    REQUIRES_AUDIT_TRAIL = "runtime_state_requires_audit_trail"
    REQUIRES_KILL_SWITCH = "runtime_state_requires_kill_switch"
    REQUIRES_ROLLBACK = "runtime_state_requires_rollback"
    REQUIRES_DRY_RUN = "runtime_state_requires_dry_run"


class RuntimeStateReadiness(str, Enum):
    READY_FOR_RUNTIME_STATE_CONTRACT_E2E = "ready_for_runtime_state_contract_e2e"


class RuntimeStateBlockReason(str, Enum):
    DEFAULT_DENY = "default_deny"
    MISSING_RUNTIME_GOVERNANCE = "missing_runtime_governance"
    MISSING_SECURITY_LAYER = "missing_security_layer"
    MISSING_RUNTIME_GATE = "missing_runtime_gate"
    MISSING_HUMAN_APPROVAL = "missing_human_approval"
    MISSING_AUDIT_TRAIL = "missing_audit_trail"
    MISSING_KILL_SWITCH = "missing_kill_switch"
    MISSING_ROLLBACK = "missing_rollback"
    MISSING_DRY_RUN = "missing_dry_run"
    FORBIDDEN_STATE = "forbidden_state"
    FORBIDDEN_TRANSITION = "forbidden_transition"
    FORBIDDEN_READINESS = "forbidden_readiness"
    DANGEROUS_METADATA = "dangerous_metadata"
    METADATA_NOT_JSON_SAFE = "metadata_not_json_safe"
    OPERATIONAL_CAPABILITY_REQUESTED = "operational_capability_requested"


class RuntimeStateRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

ALLOWED_STATES = tuple(state.value for state in RuntimeStateValue)
FORBIDDEN_STATES = (
    "runtime_state_active", "runtime_state_running", "runtime_state_executing", "runtime_state_live",
    "runtime_state_open", "runtime_state_enabled", "runtime_state_operational",
    "runtime_state_tool_executing", "runtime_state_model_invoking", "runtime_state_context_injecting",
    "runtime_state_output_delivering", "runtime_state_writing", "runtime_state_persisting_memory",
    "runtime_state_network_active", "runtime_state_api_active", "runtime_state_browser_active",
    "runtime_state_filesystem_active", "runtime_state_env_active", "runtime_state_secret_active",
    "runtime_state_ui_control_active", "runtime_state_device_control_active", "runtime_state_integration_active",
    "runtime_state_market_catalog_active", "runtime_state_business_composition_active",
)
ALLOWED_TRANSITIONS = tuple(transition.value for transition in RuntimeStateTransition)
FORBIDDEN_TRANSITION_NAMES = (
    "ready_simulated_to_runtime_active", "ready_simulated_to_runtime_running", "ready_simulated_to_runtime_executing",
    "ready_simulated_to_tool_executing", "ready_simulated_to_model_invoking", "ready_simulated_to_context_injecting",
    "ready_simulated_to_output_delivering", "ready_simulated_to_writes_enabled", "ready_simulated_to_stores_enabled",
    "ready_simulated_to_memory_persistence_enabled", "ready_simulated_to_network_enabled", "ready_simulated_to_api_enabled",
    "ready_simulated_to_browser_enabled", "ready_simulated_to_filesystem_enabled", "ready_simulated_to_env_access_enabled",
    "ready_simulated_to_secret_access_enabled", "ready_simulated_to_ui_control_enabled", "ready_simulated_to_device_control_enabled",
    "ready_simulated_to_integration_enabled", "any_to_runtime_active", "any_to_runtime_execution",
    "any_to_operations_enabled", "any_to_gate_open",
)
FORBIDDEN_READINESS = (
    "ready_for_runtime", "ready_for_runtime_activation", "ready_for_execution", "ready_for_dry_run_execution",
    "ready_for_tool_execution", "ready_for_model_invocation", "ready_for_context_injection", "ready_for_output_delivery",
    "ready_for_writes", "ready_for_stores", "runtime_open", "runtime_active", "runtime_enabled",
    "execution_enabled", "operations_enabled", "gate_open", "approval_enabled", "human_approval_operational",
    "kill_switch_enabled", "rollback_enabled", "observability_runtime_enabled", "runtime_state_active",
    "runtime_state_running", "runtime_state_executing", "runtime_state_operational",
)
DANGEROUS_METADATA_KEYS = (
    "secret", "secrets", "api_key", "apikey", "token", "access_token", "refresh_token", "password",
    "passwd", "credential", "credentials", "private_key", "raw_payload", "payload", "raw_output",
    "output", "file_content", "env", "environment", "cookie", "authorization", "bearer",
)
REQUIRED_DEPENDENCIES = (
    "runtime_governance", "security_layer", "runtime_activation_gate", "human_approval",
    "audit_trail", "kill_switch", "rollback", "dry_run_before_execution",
)


@dataclass(frozen=True)
class RuntimeStatePolicy:
    contract_version: str
    runtime_governance_required: bool
    security_layer_required: bool
    runtime_activation_gate_required: bool
    human_approval_required: bool
    audit_trail_required: bool
    kill_switch_required: bool
    rollback_required: bool
    dry_run_required_before_execution: bool
    allowed_states: tuple[str, ...]
    forbidden_states: tuple[str, ...]
    allowed_transitions: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    default_decision: RuntimeStateDecision
    metadata_schema_version: str


@dataclass(frozen=True)
class RuntimeStateMetadata:
    runtime_state_id: str
    runtime_governance_ref: str
    runtime_gate_ref: str
    security_baseline_ref: str
    state_reason: str
    state_scope: str
    state_risk_level: RuntimeStateRiskLevel
    metadata_sanitized: Mapping[str, Any]
    intent_id: str | None = None
    attempt_id: str | None = None
    lifecycle_ref: str | None = None
    result_ref: str | None = None
    projection_ref: str | None = None
    dry_run_ref: str | None = None
    human_approval_ref: str | None = None
    audit_trail_ref: str | None = None
    kill_switch_ref: str | None = None
    rollback_ref: str | None = None


@dataclass(frozen=True)
class RuntimeStateSnapshot:
    runtime_state_id: str
    state: RuntimeStateValue
    metadata: RuntimeStateMetadata
    readiness: RuntimeStateReadiness
    side_effects_allowed: bool
    runtime_activation_allowed: bool
    runtime_execution_allowed: bool
    state_mutation_allowed: bool
    store_write_allowed: bool
    store_read_allowed: bool
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
    archived_simulated: bool


@dataclass(frozen=True)
class RuntimeStateTransitionRequest:
    request_id: str
    current_state: RuntimeStateValue | str
    requested_transition: RuntimeStateTransition | str
    requested_state: RuntimeStateValue | str
    requested_by: str
    reason: str
    metadata: RuntimeStateMetadata
    security_baseline_ref: str
    runtime_gate_ref: str
    runtime_governance_decision_ref: str | None = None
    human_approval_ref: str | None = None
    audit_trail_ref: str | None = None
    kill_switch_ref: str | None = None
    rollback_ref: str | None = None
    dry_run_ref: str | None = None
    requested_readiness: str | None = None
    requested_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeStateTransitionDecision:
    request_id: str
    from_state: RuntimeStateValue
    to_state: RuntimeStateValue
    transition: RuntimeStateTransition | str
    decision: RuntimeStateDecision
    block_reasons: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    missing_dependencies: tuple[str, ...]
    readiness: RuntimeStateReadiness
    result_snapshot: RuntimeStateSnapshot
    side_effects_allowed: bool
    runtime_activation_allowed: bool
    runtime_execution_allowed: bool
    state_mutation_allowed: bool
    store_write_allowed: bool
    store_read_allowed: bool
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
class RuntimeStateContractSnapshot:
    status: str
    verdict: str
    readiness: RuntimeStateReadiness
    operational: bool
    policy: RuntimeStatePolicy
    allowed_states: tuple[str, ...]
    forbidden_states: tuple[str, ...]
    allowed_transitions: tuple[str, ...]
    forbidden_modules: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    next_step: str

def build_default_runtime_state_policy() -> RuntimeStatePolicy:
    return RuntimeStatePolicy(
        contract_version="1.0",
        runtime_governance_required=True,
        security_layer_required=True,
        runtime_activation_gate_required=True,
        human_approval_required=True,
        audit_trail_required=True,
        kill_switch_required=True,
        rollback_required=True,
        dry_run_required_before_execution=True,
        allowed_states=ALLOWED_STATES,
        forbidden_states=FORBIDDEN_STATES,
        allowed_transitions=ALLOWED_TRANSITIONS,
        forbidden_readiness=FORBIDDEN_READINESS,
        blocked_capabilities=runtime_state_blocked_capabilities(),
        default_decision=RuntimeStateDecision.TRANSITION_BLOCKED,
        metadata_schema_version="1.0",
    )


def build_runtime_state_metadata(
    *,
    runtime_state_id: str,
    runtime_governance_ref: str,
    runtime_gate_ref: str,
    security_baseline_ref: str,
    state_reason: str,
    state_scope: str,
    state_risk_level: RuntimeStateRiskLevel | str,
    metadata_sanitized: Mapping[str, Any],
    intent_id: str | None = None,
    attempt_id: str | None = None,
    lifecycle_ref: str | None = None,
    result_ref: str | None = None,
    projection_ref: str | None = None,
    dry_run_ref: str | None = None,
    human_approval_ref: str | None = None,
    audit_trail_ref: str | None = None,
    kill_switch_ref: str | None = None,
    rollback_ref: str | None = None,
) -> RuntimeStateMetadata:
    metadata = RuntimeStateMetadata(
        runtime_state_id=runtime_state_id,
        runtime_governance_ref=runtime_governance_ref,
        runtime_gate_ref=runtime_gate_ref,
        security_baseline_ref=security_baseline_ref,
        state_reason=state_reason,
        state_scope=state_scope,
        state_risk_level=_coerce_risk_level(state_risk_level),
        metadata_sanitized=metadata_sanitized,
        intent_id=intent_id,
        attempt_id=attempt_id,
        lifecycle_ref=lifecycle_ref,
        result_ref=result_ref,
        projection_ref=projection_ref,
        dry_run_ref=dry_run_ref,
        human_approval_ref=human_approval_ref,
        audit_trail_ref=audit_trail_ref,
        kill_switch_ref=kill_switch_ref,
        rollback_ref=rollback_ref,
    )
    errors = validate_runtime_state_metadata(metadata)
    if errors:
        raise ValueError(";".join(errors))
    return metadata


def build_runtime_state_snapshot(
    state: RuntimeStateValue | str,
    metadata: RuntimeStateMetadata,
    policy: RuntimeStatePolicy | None = None,
) -> RuntimeStateSnapshot:
    policy = policy or build_default_runtime_state_policy()
    resolved_state = _coerce_state(state)
    if resolved_state.value not in policy.allowed_states or resolved_state.value in policy.forbidden_states:
        raise ValueError(f"forbidden_state:{_enum_value(state)}")
    metadata_errors = validate_runtime_state_metadata(metadata, policy)
    if metadata_errors:
        raise ValueError(";".join(metadata_errors))
    return RuntimeStateSnapshot(
        runtime_state_id=metadata.runtime_state_id,
        state=resolved_state,
        metadata=metadata,
        readiness=RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E,
        side_effects_allowed=False,
        runtime_activation_allowed=False,
        runtime_execution_allowed=False,
        state_mutation_allowed=False,
        store_write_allowed=False,
        store_read_allowed=False,
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
        archived_simulated=resolved_state == RuntimeStateValue.ARCHIVED_SIMULATED,
    )


def validate_runtime_state_metadata(metadata: RuntimeStateMetadata, policy: RuntimeStatePolicy | None = None) -> tuple[str, ...]:
    policy = policy or build_default_runtime_state_policy()
    if not isinstance(metadata, RuntimeStateMetadata):
        raise TypeError("metadata must be RuntimeStateMetadata")
    errors: list[str] = []
    for field_name in ("runtime_state_id", "runtime_governance_ref", "runtime_gate_ref", "security_baseline_ref", "state_reason", "state_scope"):
        if not isinstance(getattr(metadata, field_name), str) or not getattr(metadata, field_name).strip():
            errors.append(f"missing_{field_name}")
    if not isinstance(metadata.state_risk_level, RuntimeStateRiskLevel):
        errors.append("invalid_state_risk_level")
    errors.extend(_metadata_errors(metadata.metadata_sanitized))
    return tuple(dict.fromkeys(errors))


def validate_runtime_state_transition_request(request: RuntimeStateTransitionRequest, policy: RuntimeStatePolicy | None = None) -> tuple[str, ...]:
    policy = policy or build_default_runtime_state_policy()
    if not isinstance(request, RuntimeStateTransitionRequest):
        raise TypeError("request must be RuntimeStateTransitionRequest")
    errors: list[str] = []
    for field_name in ("request_id", "requested_by", "reason", "security_baseline_ref", "runtime_gate_ref"):
        if not isinstance(getattr(request, field_name), str) or not getattr(request, field_name).strip():
            errors.append(f"missing_{field_name}")
    errors.extend(validate_runtime_state_metadata(request.metadata, policy))
    requested_value = _enum_value(request.requested_state)
    transition_value = _enum_value(request.requested_transition)
    if _enum_value(request.current_state) in policy.forbidden_states or requested_value in policy.forbidden_states:
        errors.append(RuntimeStateBlockReason.FORBIDDEN_STATE.value)
    if requested_value not in policy.allowed_states:
        errors.append(f"state_not_allowed:{requested_value}")
    if transition_value in FORBIDDEN_TRANSITION_NAMES or transition_value not in policy.allowed_transitions:
        errors.append(RuntimeStateBlockReason.FORBIDDEN_TRANSITION.value)
    if request.requested_readiness and request.requested_readiness in policy.forbidden_readiness:
        errors.append(RuntimeStateBlockReason.FORBIDDEN_READINESS.value)
    for capability in request.requested_capabilities:
        if capability in policy.blocked_capabilities or _looks_operational(capability):
            errors.append(RuntimeStateBlockReason.OPERATIONAL_CAPABILITY_REQUESTED.value)
    return tuple(dict.fromkeys(errors))


def evaluate_runtime_state_transition(request: RuntimeStateTransitionRequest, policy: RuntimeStatePolicy | None = None) -> RuntimeStateTransitionDecision:
    policy = policy or build_default_runtime_state_policy()
    block_reasons = list(validate_runtime_state_transition_request(request, policy))
    missing = list(_missing_dependencies(request, policy))
    if missing:
        block_reasons.extend(f"missing_dependency:{item}" for item in missing)
    if RuntimeStateBlockReason.FORBIDDEN_STATE.value in block_reasons or RuntimeStateBlockReason.FORBIDDEN_TRANSITION.value in block_reasons:
        decision = RuntimeStateDecision.TRANSITION_INVALID
        result_state = RuntimeStateValue.INVALID
    elif any(reason.startswith("metadata_") or (reason.startswith("missing_") and not reason.startswith("missing_dependency:")) for reason in block_reasons):
        decision = RuntimeStateDecision.TRANSITION_INVALID
        result_state = RuntimeStateValue.INVALID
    elif missing:
        decision = _decision_for_missing(missing[0])
        result_state = RuntimeStateValue.BLOCKED
    elif block_reasons:
        decision = RuntimeStateDecision.TRANSITION_BLOCKED
        result_state = RuntimeStateValue.BLOCKED
    else:
        decision = RuntimeStateDecision.TRANSITION_ALLOWED_SIMULATED
        result_state = _coerce_state(request.requested_state)
    snapshot = build_runtime_state_snapshot(result_state, request.metadata, policy)
    return RuntimeStateTransitionDecision(
        request_id=request.request_id,
        from_state=_coerce_state(request.current_state),
        to_state=result_state,
        transition=request.requested_transition,
        decision=decision,
        block_reasons=tuple(dict.fromkeys(block_reasons)),
        required_dependencies=REQUIRED_DEPENDENCIES,
        missing_dependencies=tuple(dict.fromkeys(missing)),
        readiness=RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E,
        result_snapshot=snapshot,
        side_effects_allowed=False,
        runtime_activation_allowed=False,
        runtime_execution_allowed=False,
        state_mutation_allowed=False,
        store_write_allowed=False,
        store_read_allowed=False,
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
        metadata_sanitized=request.metadata.metadata_sanitized,
    )

def build_runtime_state_contract_snapshot(policy: RuntimeStatePolicy | None = None) -> RuntimeStateContractSnapshot:
    policy = policy or build_default_runtime_state_policy()
    return RuntimeStateContractSnapshot(
        status=CONTRACT_STATUS,
        verdict=CONTRACT_VERDICT,
        readiness=RuntimeStateReadiness.READY_FOR_RUNTIME_STATE_CONTRACT_E2E,
        operational=False,
        policy=policy,
        allowed_states=runtime_state_allowed_states(),
        forbidden_states=runtime_state_forbidden_states(),
        allowed_transitions=runtime_state_allowed_transitions(),
        forbidden_modules=runtime_state_forbidden_modules(),
        blocked_capabilities=runtime_state_blocked_capabilities(),
        next_step=CONTRACT_NEXT_STEP,
    )


def runtime_state_contract_status() -> dict[str, Any]:
    return runtime_state_to_dict(build_runtime_state_contract_snapshot())


def runtime_state_allowed_states() -> tuple[str, ...]:
    return ALLOWED_STATES


def runtime_state_forbidden_states() -> tuple[str, ...]:
    return FORBIDDEN_STATES


def runtime_state_allowed_transitions() -> tuple[str, ...]:
    return ALLOWED_TRANSITIONS


def runtime_state_forbidden_modules() -> tuple[str, ...]:
    return (
        "core/runtime_state.py", "core/runtime_state_machine.py", "core/runtime_state_validator.py",
        "core/runtime_state_snapshot.py", "core/runtime_state_store.py", "core/runtime_state_writer.py",
        "core/runtime_state_reader.py", "core/runtime_state_transition.py", "core/runtime_state_event.py",
        "core/runtime_state_event_bus.py", "core/runtime_governance.py", "core/runtime_controller.py",
        "core/runtime_manager.py", "core/runtime_runner.py", "core/runtime_scheduler.py", "core/runtime_worker.py",
        "core/runtime_queue.py", "core/runtime_executor.py", "core/runtime_orchestrator.py",
        "core/runtime_dispatcher.py", "core/runtime_event_schema.py", "core/runtime_event_bus.py",
        "core/human_approval_gate.py", "core/human_approval_contract.py", "core/human_approval_store.py",
        "core/human_approval_audit.py", "core/approval_request.py", "core/approval_decision.py",
        "core/approval_workflow.py", "core/approval_ui.py", "core/approval_api.py", "core/approval_endpoint.py",
        "core/approval_runtime.py", "core/kill_switch.py", "core/rollback_controller.py",
        "core/rollback_executor.py", "core/process_killer.py", "core/job_canceller.py", "core/queue_drain.py",
        "core/worker_stop.py", "core/scheduler_stop.py", "core/runner_stop.py", "core/executor_stop.py",
        "core/filesystem_rollback.py", "core/git_rollback.py", "core/store_rollback.py",
        "core/database_rollback.py", "core/memory_rollback.py", "core/audit_trail.py", "core/audit_logger.py",
        "core/event_log.py", "core/event_bus.py", "core/telemetry.py", "core/metrics_collector.py",
        "core/tracing.py", "core/dashboard.py", "core/correlation_ledger.py", "core/immutable_audit_log.py",
        "core/side_effect_ledger.py", "core/dry_run_executor.py", "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py", "core/dry_run_scheduler.py", "core/dry_run_worker.py", "core/dry_run_queue.py",
        "core/tool_executor.py", "core/tool_registry.py", "core/tool_adapter.py", "core/model_invoker.py",
        "core/model_router.py", "core/model_executor.py", "core/inference_runner.py", "core/context_builder.py",
        "core/context_injector.py", "core/prompt_assembler.py", "core/retrieval_engine.py", "core/rag_engine.py",
        "core/output_writer.py", "core/output_publisher.py", "core/output_notifier.py", "core/output_delivery.py",
        "core/message_sender.py", "core/email_sender.py", "core/webhook_client.py", "core/provider_client.py",
        "core/browser_operator.py", "core/sandbox_runner.py", "core/command_executor.py", "core/shell.py",
        "core/subprocess_runner.py", "core/ui_tars_adapter.py", "core/hermes_adapter.py", "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    )


def runtime_state_blocked_capabilities() -> tuple[str, ...]:
    return (
        "runtime state operativo", "runtime state activation", "runtime state mutation real",
        "runtime state store operativo", "runtime state writer operativo", "runtime state reader operativo",
        "runtime state transition real", "runtime state event bus", "runtime governance operativo",
        "runtime governance activation", "runtime governance execution", "runtime controller", "runtime manager",
        "runtime activation", "runtime execution", "runtime runner", "runtime scheduler", "runtime worker",
        "runtime queue", "runtime executor", "runtime orchestrator", "runtime dispatcher", "runtime event bus",
        "runtime event schema operativo", "dry-run execution activation", "dry-run executor", "dry-run runner",
        "dry-run dispatcher", "dry-run scheduler", "dry-run worker", "dry-run queue", "human approval operativo",
        "approval gate active", "approval workflow real", "approval UI real", "approval API real",
        "approval endpoint real", "approval store operativo", "automatic approval", "permission escalation",
        "runtime approval real", "execution approval real", "tool execution approval real",
        "model invocation approval real", "output delivery approval real", "writes approval real",
        "stores approval real", "integration approval real", "kill switch operativo", "rollback operativo",
        "process termination", "job cancellation", "queue drain", "worker stop", "scheduler stop", "runner stop",
        "executor stop", "filesystem rollback", "git rollback", "store mutation", "manifest mutation",
        "database rollback", "memory rollback", "observability runtime", "audit trail operativo",
        "event log operativo", "event bus", "telemetry real", "metrics collector", "tracing real",
        "dashboard operativo", "immutable audit log operativo", "correlation ledger runtime",
        "side-effect ledger operativo", "tool execution", "model invocation", "context injection",
        "prompt assembly runtime", "retrieval runtime", "RAG runtime", "output delivery", "output publishing",
        "writes reales", "stores operativos", "memory persistence", "external access", "API calls",
        "network", "browser", "command execution", "shell", "process spawn", "real filesystem reads",
        "real filesystem writes", "env access", "secret access", "host access", "device access",
        "clipboard access", "UI control", "device control", "UI-TARS runtime", "Hermes runtime",
        "n8n real workflows", "Home Assistant real actions", "Market Catalog runtime",
        "Business Composition Layer runtime", "OBLITERATUS integration",
    )


def runtime_state_to_dict(obj: Any) -> Any:
    payload = _to_json_safe(obj)
    json.dumps(payload, sort_keys=True)
    return payload


def _missing_dependencies(request: RuntimeStateTransitionRequest, policy: RuntimeStatePolicy) -> tuple[str, ...]:
    missing: list[str] = []
    if policy.runtime_governance_required and not (request.runtime_governance_decision_ref or request.metadata.runtime_governance_ref):
        missing.append("runtime_governance")
    if policy.security_layer_required and not (request.security_baseline_ref or request.metadata.security_baseline_ref):
        missing.append("security_layer")
    if policy.runtime_activation_gate_required and not (request.runtime_gate_ref or request.metadata.runtime_gate_ref):
        missing.append("runtime_activation_gate")
    if policy.human_approval_required and not (request.human_approval_ref or request.metadata.human_approval_ref):
        missing.append("human_approval")
    if policy.audit_trail_required and not (request.audit_trail_ref or request.metadata.audit_trail_ref):
        missing.append("audit_trail")
    if policy.kill_switch_required and not (request.kill_switch_ref or request.metadata.kill_switch_ref):
        missing.append("kill_switch")
    if policy.rollback_required and not (request.rollback_ref or request.metadata.rollback_ref):
        missing.append("rollback")
    if policy.dry_run_required_before_execution and request.requested_state == RuntimeStateValue.DRY_RUN_REQUIRED and not (request.dry_run_ref or request.metadata.dry_run_ref):
        missing.append("dry_run_before_execution")
    return tuple(missing)


def _decision_for_missing(name: str) -> RuntimeStateDecision:
    return {
        "runtime_governance": RuntimeStateDecision.REQUIRES_RUNTIME_GOVERNANCE,
        "security_layer": RuntimeStateDecision.REQUIRES_SECURITY_LAYER,
        "runtime_activation_gate": RuntimeStateDecision.REQUIRES_RUNTIME_GATE,
        "human_approval": RuntimeStateDecision.REQUIRES_HUMAN_APPROVAL,
        "audit_trail": RuntimeStateDecision.REQUIRES_AUDIT_TRAIL,
        "kill_switch": RuntimeStateDecision.REQUIRES_KILL_SWITCH,
        "rollback": RuntimeStateDecision.REQUIRES_ROLLBACK,
        "dry_run_before_execution": RuntimeStateDecision.REQUIRES_DRY_RUN,
    }.get(name, RuntimeStateDecision.TRANSITION_BLOCKED)


def _metadata_errors(metadata: Mapping[str, Any]) -> tuple[str, ...]:
    if not isinstance(metadata, Mapping):
        return ("metadata_not_mapping",)
    try:
        json.dumps(metadata, sort_keys=True)
    except TypeError:
        return (RuntimeStateBlockReason.METADATA_NOT_JSON_SAFE.value,)
    errors: list[str] = []
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


def _coerce_state(value: RuntimeStateValue | str) -> RuntimeStateValue:
    if isinstance(value, RuntimeStateValue):
        return value
    try:
        return RuntimeStateValue(str(value))
    except ValueError as exc:
        raise ValueError(f"state_not_allowed:{value}") from exc


def _coerce_risk_level(value: RuntimeStateRiskLevel | str) -> RuntimeStateRiskLevel:
    if isinstance(value, RuntimeStateRiskLevel):
        return value
    try:
        return RuntimeStateRiskLevel(str(value))
    except ValueError as exc:
        raise ValueError(f"risk_level_not_allowed:{value}") from exc


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, Enum) else str(value)


def _looks_operational(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in ("active", "running", "execut", "write", "store", "network", "secret", "tool", "model", "context", "output", "runtime"))


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

