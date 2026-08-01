"""Non-operational Observability contract.

Pure, deterministic, JSON-safe contract objects for future conceptual
observability. This module performs no IO, no env/secret reads, no network,
no logging, no event publishing, no store mutation, and no execution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping, Sequence


OBSERVABILITY_CONTRACT_READY = True
OBSERVABILITY_OPERATIONAL = False
OBSERVABILITY_RUNTIME_ENABLED = False
OBSERVABILITY_AUDIT_TRAIL_ENABLED = False
OBSERVABILITY_LOGGER_ENABLED = False
OBSERVABILITY_EVENT_LOG_ENABLED = False
OBSERVABILITY_EVENT_BUS_ENABLED = False
OBSERVABILITY_TELEMETRY_ENABLED = False
OBSERVABILITY_METRICS_ENABLED = False
OBSERVABILITY_TRACING_ENABLED = False
OBSERVABILITY_DASHBOARD_ENABLED = False
OBSERVABILITY_IMMUTABLE_AUDIT_LOG_ENABLED = False
OBSERVABILITY_CORRELATION_LEDGER_ENABLED = False
OBSERVABILITY_SIDE_EFFECT_LEDGER_ENABLED = False
OBSERVABILITY_REDACTION_ENGINE_ENABLED = False
OBSERVABILITY_LOG_WRITE_ENABLED = False
OBSERVABILITY_EVENT_PUBLISH_ENABLED = False
OBSERVABILITY_STORE_WRITE_ENABLED = False
OBSERVABILITY_STORE_MUTATION_ENABLED = False
OBSERVABILITY_RUNTIME_STATE_MUTATION_ENABLED = False
OBSERVABILITY_RUNTIME_GOVERNANCE_EXECUTION_ENABLED = False
OBSERVABILITY_RUNTIME_ACTIVATION_ENABLED = False
OBSERVABILITY_RUNTIME_EXECUTION_ENABLED = False
OBSERVABILITY_DRY_RUN_EXECUTION_ENABLED = False
OBSERVABILITY_HUMAN_APPROVAL_RUNTIME_ENABLED = False
OBSERVABILITY_KILL_SWITCH_RUNTIME_ENABLED = False
OBSERVABILITY_ROLLBACK_RUNTIME_ENABLED = False
OBSERVABILITY_TOOL_EXECUTION_ENABLED = False
OBSERVABILITY_MODEL_INVOCATION_ENABLED = False
OBSERVABILITY_CONTEXT_INJECTION_ENABLED = False
OBSERVABILITY_OUTPUT_DELIVERY_ENABLED = False
OBSERVABILITY_OUTPUT_PUBLISHING_ENABLED = False
OBSERVABILITY_WRITES_ENABLED = False
OBSERVABILITY_STORES_ENABLED = False
OBSERVABILITY_MEMORY_PERSISTENCE_ENABLED = False
OBSERVABILITY_NETWORK_ENABLED = False
OBSERVABILITY_API_ENABLED = False
OBSERVABILITY_BROWSER_ENABLED = False
OBSERVABILITY_FILESYSTEM_ENABLED = False
OBSERVABILITY_ENV_ACCESS_ENABLED = False
OBSERVABILITY_SECRET_ACCESS_ENABLED = False
OBSERVABILITY_UI_CONTROL_ENABLED = False
OBSERVABILITY_DEVICE_CONTROL_ENABLED = False
OBSERVABILITY_UI_TARS_ENABLED = False
OBSERVABILITY_HERMES_ENABLED = False
OBSERVABILITY_N8N_ENABLED = False
OBSERVABILITY_HOME_ASSISTANT_ENABLED = False
OBSERVABILITY_MARKET_CATALOG_RUNTIME_ENABLED = False
OBSERVABILITY_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False
OBLITERATUS_OBSERVABILITY_ENABLED = False

CONTRACT_STATUS = "OBSERVABILITY_CONTRACT_READY"
CONTRACT_VERDICT = "OBSERVABILITY_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_observability_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 3.47.1 — Checkpoint E2E de Observability Contract"


class ObservabilityEventType(str, Enum):
    CONTRACT_INITIALIZED = "observability_event_contract_initialized"
    GOVERNANCE_EVALUATED = "observability_event_governance_evaluated"
    RUNTIME_STATE_SNAPSHOT_CREATED = "observability_event_runtime_state_snapshot_created"
    RUNTIME_STATE_TRANSITION_SIMULATED = "observability_event_runtime_state_transition_simulated"
    SECURITY_BLOCKED = "observability_event_security_blocked"
    POLICY_BLOCKED = "observability_event_policy_blocked"
    DRY_RUN_REQUIRED = "observability_event_dry_run_required"
    HUMAN_APPROVAL_REQUIRED = "observability_event_human_approval_required"
    AUDIT_TRAIL_REQUIRED = "observability_event_audit_trail_required"
    KILL_SWITCH_REQUIRED = "observability_event_kill_switch_required"
    ROLLBACK_REQUIRED = "observability_event_rollback_required"
    ATTEMPT_CREATED_SIMULATED = "observability_event_attempt_created_simulated"
    LIFECYCLE_TRANSITION_SIMULATED = "observability_event_lifecycle_transition_simulated"
    RESULT_PROJECTED = "observability_event_result_projected"
    OUTPUT_BOUNDARY_CHECKED = "observability_event_output_boundary_checked"
    METADATA_REJECTED = "observability_event_metadata_rejected"
    SECRET_REDACTED = "observability_event_secret_redacted"
    INTEGRATION_BLOCKED = "observability_event_integration_blocked"
    OBLITERATUS_EXCLUDED = "observability_event_obliteratus_excluded"
    ARCHIVED_SIMULATED = "observability_event_archived_simulated"


class ObservabilityEventDecision(str, Enum):
    RECORD_ALLOWED_SIMULATED = "observability_event_record_allowed_simulated"
    RECORD_BLOCKED = "observability_event_record_blocked"
    RECORD_INVALID = "observability_event_record_invalid"
    REQUIRES_RUNTIME_GOVERNANCE = "observability_requires_runtime_governance"
    REQUIRES_RUNTIME_STATE = "observability_requires_runtime_state"
    REQUIRES_SECURITY_LAYER = "observability_requires_security_layer"
    REQUIRES_OUTPUT_BOUNDARY = "observability_requires_output_boundary"
    REQUIRES_SECRETS_POLICY = "observability_requires_secrets_policy"
    REQUIRES_METADATA_SANITIZATION = "observability_requires_metadata_sanitization"
    REQUIRES_REDACTION_SIMULATED = "observability_requires_redaction_simulated"


class ObservabilityReadiness(str, Enum):
    READY_FOR_OBSERVABILITY_CONTRACT_E2E = "ready_for_observability_contract_e2e"


class ObservabilityBlockReason(str, Enum):
    DEFAULT_DENY = "default_deny"
    FORBIDDEN_EVENT_TYPE = "forbidden_event_type"
    FORBIDDEN_READINESS = "forbidden_readiness"
    DANGEROUS_METADATA = "dangerous_metadata"
    METADATA_NOT_JSON_SAFE = "metadata_not_json_safe"
    MISSING_RUNTIME_GOVERNANCE = "missing_runtime_governance"
    MISSING_RUNTIME_STATE = "missing_runtime_state"
    MISSING_SECURITY_LAYER = "missing_security_layer"
    MISSING_OUTPUT_BOUNDARY = "missing_output_boundary"
    MISSING_SECRETS_POLICY = "missing_secrets_policy"
    MISSING_METADATA_SANITIZATION = "missing_metadata_sanitization"
    MISSING_REDACTION_SIMULATED = "missing_redaction_simulated"
    OPERATIONAL_CAPABILITY_REQUESTED = "operational_capability_requested"


class ObservabilityRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ObservabilitySourceType(str, Enum):
    CONTRACT = "contract"
    CHECKPOINT = "checkpoint"
    BOUNDARY = "boundary"
    SECURITY = "security"
    READ_MODEL = "read_model"
    PROJECTION = "projection"
    PLAN = "plan"
    PREEXISTING_HELPER = "preexisting_helper"


ALLOWED_EVENT_TYPES = tuple(event.value for event in ObservabilityEventType)
FORBIDDEN_EVENT_TYPES = (
    "observability_event_runtime_started",
    "observability_event_runtime_executed",
    "observability_event_runner_started",
    "observability_event_scheduler_started",
    "observability_event_worker_started",
    "observability_event_queue_started",
    "observability_event_executor_started",
    "observability_event_tool_executed",
    "observability_event_model_invoked",
    "observability_event_context_injected",
    "observability_event_output_delivered",
    "observability_event_output_published",
    "observability_event_write_performed",
    "observability_event_store_mutated",
    "observability_event_memory_persisted",
    "observability_event_network_called",
    "observability_event_api_called",
    "observability_event_browser_opened",
    "observability_event_filesystem_read",
    "observability_event_filesystem_written",
    "observability_event_env_read",
    "observability_event_secret_read",
    "observability_event_ui_controlled",
    "observability_event_device_controlled",
    "observability_event_integration_executed",
    "observability_event_market_catalog_runtime_started",
    "observability_event_business_composition_runtime_started",
)
FORBIDDEN_DATA_KEYS = (
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
    "raw_prompt",
    "prompt",
    "raw_completion",
    "completion",
    "model_response",
    "tool_response",
    "external_response",
    "browser_content",
    "filesystem_content",
    "personal_data_unsanitized",
)
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
    "observability_logger_enabled",
    "observability_event_bus_enabled",
    "telemetry_enabled",
    "metrics_enabled",
    "tracing_enabled",
    "dashboard_enabled",
)
REQUIRED_DEPENDENCIES = (
    "runtime_governance",
    "runtime_state",
    "security_layer",
    "secrets_policy",
    "prompt_injection_defense",
    "output_boundary",
    "metadata_sanitization",
    "redaction_simulated",
)


@dataclass(frozen=True)
class ObservabilityPolicy:
    contract_version: str
    runtime_governance_required: bool
    runtime_state_required: bool
    security_layer_required: bool
    secrets_policy_required: bool
    prompt_injection_defense_required: bool
    output_boundary_required: bool
    metadata_sanitization_required: bool
    redaction_required_simulated: bool
    allowed_event_types: tuple[str, ...]
    forbidden_event_types: tuple[str, ...]
    forbidden_data_keys: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    default_decision: ObservabilityEventDecision
    metadata_schema_version: str


@dataclass(frozen=True)
class ObservabilityMetadata:
    observability_event_id: str
    correlation_id: str
    causation_id: str | None
    event_type: ObservabilityEventType
    event_source: str
    event_scope: str
    actor_ref: str | None
    runtime_governance_ref: str | None
    runtime_state_ref: str | None
    runtime_gate_ref: str | None
    security_baseline_ref: str
    policy_check_ref: str | None
    dry_run_ref: str | None
    attempt_id: str | None
    lifecycle_ref: str | None
    result_ref: str | None
    projection_ref: str | None
    human_approval_ref: str | None
    kill_switch_ref: str | None
    rollback_ref: str | None
    event_reason: str
    event_risk_level: ObservabilityRiskLevel
    metadata_sanitized: Mapping[str, Any]


@dataclass(frozen=True)
class ObservabilityEventRecord:
    observability_event_id: str
    correlation_id: str
    causation_id: str | None
    event_type: ObservabilityEventType
    event_source: str
    event_scope: str
    metadata: ObservabilityMetadata
    readiness: ObservabilityReadiness
    record_allowed_simulated: bool
    log_write_allowed: bool
    event_publish_allowed: bool
    store_write_allowed: bool
    store_mutation_allowed: bool
    telemetry_allowed: bool
    metrics_allowed: bool
    tracing_allowed: bool
    dashboard_allowed: bool
    runtime_activation_allowed: bool
    runtime_execution_allowed: bool
    runtime_state_mutation_allowed: bool
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


@dataclass(frozen=True)
class ObservabilitySnapshot:
    snapshot_id: str
    correlation_id: str
    event_count: int
    event_types: tuple[str, ...]
    policy_ref: str
    runtime_governance_ref: str | None
    runtime_state_ref: str | None
    security_baseline_ref: str
    readiness: ObservabilityReadiness
    events: tuple[ObservabilityEventRecord, ...]
    side_effects_allowed: bool
    log_writes_allowed: bool
    event_publishing_allowed: bool
    store_writes_allowed: bool
    runtime_activation_allowed: bool
    runtime_execution_allowed: bool
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
    integration_allowed: bool
    archived_simulated: bool
    metadata_sanitized: Mapping[str, Any]


@dataclass(frozen=True)
class ObservabilityDecisionRecord:
    observability_event_id: str
    correlation_id: str
    event_type: ObservabilityEventType | str
    decision: ObservabilityEventDecision
    block_reasons: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    missing_dependencies: tuple[str, ...]
    readiness: ObservabilityReadiness
    event_record: ObservabilityEventRecord | None
    side_effects_allowed: bool
    log_write_allowed: bool
    event_publish_allowed: bool
    store_write_allowed: bool
    store_mutation_allowed: bool
    telemetry_allowed: bool
    metrics_allowed: bool
    tracing_allowed: bool
    dashboard_allowed: bool
    runtime_activation_allowed: bool
    runtime_execution_allowed: bool
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
    integration_allowed: bool
    metadata_sanitized: Mapping[str, Any]


@dataclass(frozen=True)
class ObservabilityContractSnapshot:
    status: str
    verdict: str
    readiness: ObservabilityReadiness
    operational: bool
    policy: ObservabilityPolicy
    allowed_event_types: tuple[str, ...]
    forbidden_event_types: tuple[str, ...]
    forbidden_data_keys: tuple[str, ...]
    forbidden_modules: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    next_step: str


def build_default_observability_policy() -> ObservabilityPolicy:
    return ObservabilityPolicy(
        contract_version="1.0",
        runtime_governance_required=True,
        runtime_state_required=True,
        security_layer_required=True,
        secrets_policy_required=True,
        prompt_injection_defense_required=True,
        output_boundary_required=True,
        metadata_sanitization_required=True,
        redaction_required_simulated=True,
        allowed_event_types=ALLOWED_EVENT_TYPES,
        forbidden_event_types=FORBIDDEN_EVENT_TYPES,
        forbidden_data_keys=FORBIDDEN_DATA_KEYS,
        forbidden_readiness=FORBIDDEN_READINESS,
        blocked_capabilities=observability_blocked_capabilities(),
        default_decision=ObservabilityEventDecision.RECORD_BLOCKED,
        metadata_schema_version="1.0",
    )


def build_observability_metadata(
    *,
    observability_event_id: str,
    correlation_id: str,
    event_type: ObservabilityEventType | str,
    event_source: str,
    event_scope: str,
    security_baseline_ref: str,
    event_reason: str,
    event_risk_level: ObservabilityRiskLevel | str,
    metadata_sanitized: Mapping[str, Any],
    causation_id: str | None = None,
    actor_ref: str | None = None,
    runtime_governance_ref: str | None = None,
    runtime_state_ref: str | None = None,
    runtime_gate_ref: str | None = None,
    policy_check_ref: str | None = None,
    dry_run_ref: str | None = None,
    attempt_id: str | None = None,
    lifecycle_ref: str | None = None,
    result_ref: str | None = None,
    projection_ref: str | None = None,
    human_approval_ref: str | None = None,
    kill_switch_ref: str | None = None,
    rollback_ref: str | None = None,
) -> ObservabilityMetadata:
    metadata = ObservabilityMetadata(
        observability_event_id=observability_event_id,
        correlation_id=correlation_id,
        causation_id=causation_id,
        event_type=_coerce_event_type(event_type),
        event_source=event_source,
        event_scope=event_scope,
        actor_ref=actor_ref,
        runtime_governance_ref=runtime_governance_ref,
        runtime_state_ref=runtime_state_ref,
        runtime_gate_ref=runtime_gate_ref,
        security_baseline_ref=security_baseline_ref,
        policy_check_ref=policy_check_ref,
        dry_run_ref=dry_run_ref,
        attempt_id=attempt_id,
        lifecycle_ref=lifecycle_ref,
        result_ref=result_ref,
        projection_ref=projection_ref,
        human_approval_ref=human_approval_ref,
        kill_switch_ref=kill_switch_ref,
        rollback_ref=rollback_ref,
        event_reason=event_reason,
        event_risk_level=_coerce_risk_level(event_risk_level),
        metadata_sanitized=metadata_sanitized,
    )
    errors = validate_observability_metadata(metadata)
    if errors:
        raise ValueError(";".join(errors))
    return metadata


def validate_observability_metadata(
    metadata: ObservabilityMetadata,
    policy: ObservabilityPolicy | None = None,
) -> tuple[str, ...]:
    policy = policy or build_default_observability_policy()
    if not isinstance(metadata, ObservabilityMetadata):
        raise TypeError("metadata must be ObservabilityMetadata")
    errors: list[str] = []
    for field_name in ("observability_event_id", "correlation_id", "event_source", "event_scope", "security_baseline_ref", "event_reason"):
        if not isinstance(getattr(metadata, field_name), str) or not getattr(metadata, field_name).strip():
            errors.append(f"missing_{field_name}")
    if metadata.event_type.value not in policy.allowed_event_types:
        errors.append(ObservabilityBlockReason.FORBIDDEN_EVENT_TYPE.value)
    if not isinstance(metadata.event_risk_level, ObservabilityRiskLevel):
        errors.append("invalid_event_risk_level")
    errors.extend(_metadata_errors(metadata.metadata_sanitized, policy))
    return tuple(dict.fromkeys(errors))


def build_observability_event_record(
    metadata: ObservabilityMetadata,
    policy: ObservabilityPolicy | None = None,
) -> ObservabilityEventRecord:
    policy = policy or build_default_observability_policy()
    errors = validate_observability_metadata(metadata, policy)
    if errors:
        raise ValueError(";".join(errors))
    return ObservabilityEventRecord(
        observability_event_id=metadata.observability_event_id,
        correlation_id=metadata.correlation_id,
        causation_id=metadata.causation_id,
        event_type=metadata.event_type,
        event_source=metadata.event_source,
        event_scope=metadata.event_scope,
        metadata=metadata,
        readiness=ObservabilityReadiness.READY_FOR_OBSERVABILITY_CONTRACT_E2E,
        record_allowed_simulated=True,
        log_write_allowed=False,
        event_publish_allowed=False,
        store_write_allowed=False,
        store_mutation_allowed=False,
        telemetry_allowed=False,
        metrics_allowed=False,
        tracing_allowed=False,
        dashboard_allowed=False,
        runtime_activation_allowed=False,
        runtime_execution_allowed=False,
        runtime_state_mutation_allowed=False,
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
    )


def evaluate_observability_event(
    metadata: ObservabilityMetadata,
    policy: ObservabilityPolicy | None = None,
    missing_dependencies: Sequence[str] = (),
    requested_readiness: str | None = None,
    requested_capabilities: Sequence[str] = (),
) -> ObservabilityDecisionRecord:
    policy = policy or build_default_observability_policy()
    block_reasons = list(validate_observability_metadata(metadata, policy))
    missing = list(dict.fromkeys([*missing_dependencies, *_missing_dependencies(metadata, policy)]))
    if missing:
        block_reasons.extend(f"missing_dependency:{item}" for item in missing)
    if requested_readiness and requested_readiness in policy.forbidden_readiness:
        block_reasons.append(ObservabilityBlockReason.FORBIDDEN_READINESS.value)
    for capability in requested_capabilities:
        if capability in policy.blocked_capabilities or _looks_operational(capability):
            block_reasons.append(ObservabilityBlockReason.OPERATIONAL_CAPABILITY_REQUESTED.value)
    if ObservabilityBlockReason.FORBIDDEN_EVENT_TYPE.value in block_reasons:
        decision = ObservabilityEventDecision.RECORD_INVALID
        event_record = None
    elif any(reason.startswith("metadata_") or (reason.startswith("missing_") and not reason.startswith("missing_dependency:")) for reason in block_reasons):
        decision = ObservabilityEventDecision.RECORD_INVALID
        event_record = None
    elif missing:
        decision = _decision_for_missing(missing[0])
        event_record = None
    elif block_reasons:
        decision = ObservabilityEventDecision.RECORD_BLOCKED
        event_record = None
    else:
        decision = ObservabilityEventDecision.RECORD_ALLOWED_SIMULATED
        event_record = build_observability_event_record(metadata, policy)
    return ObservabilityDecisionRecord(
        observability_event_id=metadata.observability_event_id,
        correlation_id=metadata.correlation_id,
        event_type=metadata.event_type,
        decision=decision,
        block_reasons=tuple(dict.fromkeys(block_reasons)),
        required_dependencies=REQUIRED_DEPENDENCIES,
        missing_dependencies=tuple(dict.fromkeys(missing)),
        readiness=ObservabilityReadiness.READY_FOR_OBSERVABILITY_CONTRACT_E2E,
        event_record=event_record,
        side_effects_allowed=False,
        log_write_allowed=False,
        event_publish_allowed=False,
        store_write_allowed=False,
        store_mutation_allowed=False,
        telemetry_allowed=False,
        metrics_allowed=False,
        tracing_allowed=False,
        dashboard_allowed=False,
        runtime_activation_allowed=False,
        runtime_execution_allowed=False,
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
        integration_allowed=False,
        metadata_sanitized=metadata.metadata_sanitized,
    )


def build_observability_snapshot(
    events: Sequence[ObservabilityEventRecord],
    policy: ObservabilityPolicy | None = None,
    *,
    snapshot_id: str,
    correlation_id: str,
    policy_ref: str,
    security_baseline_ref: str,
    runtime_governance_ref: str | None = None,
    runtime_state_ref: str | None = None,
    metadata_sanitized: Mapping[str, Any] | None = None,
    archived_simulated: bool = False,
) -> ObservabilitySnapshot:
    policy = policy or build_default_observability_policy()
    event_tuple = tuple(events)
    if not isinstance(snapshot_id, str) or not snapshot_id.strip():
        raise ValueError("missing_snapshot_id")
    if not isinstance(correlation_id, str) or not correlation_id.strip():
        raise ValueError("missing_correlation_id")
    if not isinstance(security_baseline_ref, str) or not security_baseline_ref.strip():
        raise ValueError("missing_security_baseline_ref")
    for event in event_tuple:
        if not isinstance(event, ObservabilityEventRecord):
            raise TypeError("events must contain ObservabilityEventRecord")
        if event.correlation_id != correlation_id:
            raise ValueError("correlation_id_mismatch")
    metadata_payload = dict(metadata_sanitized or {})
    metadata_errors = _metadata_errors(metadata_payload, policy)
    if metadata_errors:
        raise ValueError(";".join(metadata_errors))
    event_types = tuple(event.event_type.value for event in event_tuple)
    return ObservabilitySnapshot(
        snapshot_id=snapshot_id,
        correlation_id=correlation_id,
        event_count=len(event_tuple),
        event_types=event_types,
        policy_ref=policy_ref,
        runtime_governance_ref=runtime_governance_ref,
        runtime_state_ref=runtime_state_ref,
        security_baseline_ref=security_baseline_ref,
        readiness=ObservabilityReadiness.READY_FOR_OBSERVABILITY_CONTRACT_E2E,
        events=event_tuple,
        side_effects_allowed=False,
        log_writes_allowed=False,
        event_publishing_allowed=False,
        store_writes_allowed=False,
        runtime_activation_allowed=False,
        runtime_execution_allowed=False,
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
        integration_allowed=False,
        archived_simulated=archived_simulated,
        metadata_sanitized=metadata_payload,
    )


def build_observability_contract_snapshot(policy: ObservabilityPolicy | None = None) -> ObservabilityContractSnapshot:
    policy = policy or build_default_observability_policy()
    return ObservabilityContractSnapshot(
        status=CONTRACT_STATUS,
        verdict=CONTRACT_VERDICT,
        readiness=ObservabilityReadiness.READY_FOR_OBSERVABILITY_CONTRACT_E2E,
        operational=False,
        policy=policy,
        allowed_event_types=observability_allowed_event_types(),
        forbidden_event_types=observability_forbidden_event_types(),
        forbidden_data_keys=observability_forbidden_data_keys(),
        forbidden_modules=observability_forbidden_modules(),
        blocked_capabilities=observability_blocked_capabilities(),
        next_step=CONTRACT_NEXT_STEP,
    )


def observability_contract_status() -> dict[str, Any]:
    return observability_to_dict(build_observability_contract_snapshot())


def observability_allowed_event_types() -> tuple[str, ...]:
    return ALLOWED_EVENT_TYPES


def observability_forbidden_event_types() -> tuple[str, ...]:
    return FORBIDDEN_EVENT_TYPES


def observability_forbidden_data_keys() -> tuple[str, ...]:
    return FORBIDDEN_DATA_KEYS


def observability_forbidden_modules() -> tuple[str, ...]:
    return (
        "core/observability_event.py", "core/observability_event_schema.py", "core/observability_snapshot.py",
        "core/observability_store.py", "core/observability_writer.py", "core/observability_reader.py",
        "core/observability_logger.py", "core/audit_trail.py", "core/audit_logger.py", "core/event_log.py",
        "core/event_bus.py", "core/telemetry.py", "core/metrics_collector.py", "core/tracing.py",
        "core/dashboard.py", "core/correlation_ledger.py", "core/immutable_audit_log.py",
        "core/side_effect_ledger.py", "core/redaction_engine.py", "core/runtime_state.py",
        "core/runtime_state_machine.py", "core/runtime_state_validator.py", "core/runtime_state_store.py",
        "core/runtime_state_writer.py", "core/runtime_state_reader.py", "core/runtime_state_event.py",
        "core/runtime_state_event_bus.py", "core/runtime_governance.py", "core/runtime_controller.py",
        "core/runtime_manager.py", "core/runtime_runner.py", "core/runtime_scheduler.py", "core/runtime_worker.py",
        "core/runtime_queue.py", "core/runtime_orchestrator.py", "core/runtime_dispatcher.py",
        "core/runtime_event_schema.py", "core/runtime_event_bus.py", "core/human_approval_gate.py",
        "core/human_approval_contract.py", "core/human_approval_store.py", "core/human_approval_audit.py",
        "core/approval_request.py", "core/approval_decision.py", "core/approval_api.py", "core/approval_ui.py",
        "core/approval_endpoint.py", "core/approval_store.py", "core/kill_switch.py", "core/rollback_controller.py",
        "core/process_terminator.py", "core/job_canceller.py", "core/queue_drain.py", "core/worker_stop.py",
        "core/scheduler_stop.py", "core/runner_stop.py", "core/executor_stop.py", "core/filesystem_rollback.py",
        "core/git_rollback.py", "core/store_rollback.py", "core/manifest_rollback.py", "core/database_rollback.py",
        "core/memory_rollback.py", "core/dry_run_executor.py", "core/dry_run_runner.py",
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


def observability_blocked_capabilities() -> tuple[str, ...]:
    return (
        "observability operativo", "observability runtime", "audit trail operativo", "logger operativo",
        "event log operativo", "event bus operativo", "telemetry real", "metrics collector", "tracing real",
        "dashboard operativo", "immutable audit log operativo", "correlation ledger runtime",
        "side-effect ledger operativo", "redaction engine operativo", "log write real", "event publish real",
        "store write real", "store mutation real", "runtime state operativo", "runtime state activation",
        "runtime state mutation real", "runtime state store operativo", "runtime state writer operativo",
        "runtime state reader operativo", "runtime state transition real", "runtime state event bus",
        "runtime governance operativo", "runtime governance activation", "runtime governance execution",
        "runtime controller", "runtime manager", "runtime activation", "runtime execution", "runtime runner",
        "runtime scheduler", "runtime worker", "runtime queue", "runtime executor", "runtime orchestrator",
        "runtime dispatcher", "runtime event bus", "runtime event schema operativo", "dry-run execution activation",
        "dry-run executor", "dry-run runner", "dry-run dispatcher", "dry-run scheduler", "dry-run worker",
        "dry-run queue", "human approval operativo", "approval gate active", "approval workflow real",
        "approval UI real", "approval API real", "approval endpoint real", "approval store operativo",
        "automatic approval", "permission escalation", "runtime approval real", "execution approval real",
        "tool execution approval real", "model invocation approval real", "output delivery approval real",
        "writes approval real", "stores approval real", "integration approval real", "kill switch operativo",
        "rollback operativo", "process termination", "job cancellation", "queue drain", "worker stop", "scheduler stop",
        "runner stop", "executor stop", "filesystem rollback", "git rollback", "store mutation", "manifest mutation",
        "database rollback", "memory rollback", "tool execution", "model invocation", "context injection",
        "prompt assembly runtime", "retrieval runtime", "RAG runtime", "output delivery", "output publishing",
        "writes reales", "stores operativos", "memory persistence", "external access", "API calls", "network",
        "browser", "command execution", "shell", "process spawn", "real filesystem reads", "real filesystem writes",
        "env access", "secret access", "host access", "device access", "clipboard access", "UI control",
        "device control", "UI-TARS runtime", "Hermes runtime", "n8n real workflows",
        "Home Assistant real actions", "Market Catalog runtime", "Business Composition Layer runtime",
        "OBLITERATUS integration",
    )


def observability_to_dict(obj: Any) -> Any:
    payload = _to_json_safe(obj)
    json.dumps(payload, sort_keys=True)
    return payload


def _missing_dependencies(metadata: ObservabilityMetadata, policy: ObservabilityPolicy) -> tuple[str, ...]:
    missing: list[str] = []
    if policy.runtime_governance_required and not metadata.runtime_governance_ref:
        missing.append("runtime_governance")
    if policy.runtime_state_required and not metadata.runtime_state_ref:
        missing.append("runtime_state")
    if policy.security_layer_required and not metadata.security_baseline_ref:
        missing.append("security_layer")
    if policy.secrets_policy_required and not metadata.policy_check_ref:
        missing.append("secrets_policy")
    if policy.prompt_injection_defense_required and not metadata.policy_check_ref:
        missing.append("prompt_injection_defense")
    if policy.output_boundary_required and not metadata.policy_check_ref:
        missing.append("output_boundary")
    if policy.metadata_sanitization_required and metadata.metadata_sanitized is None:
        missing.append("metadata_sanitization")
    if policy.redaction_required_simulated and metadata.event_type == ObservabilityEventType.SECRET_REDACTED and not metadata.policy_check_ref:
        missing.append("redaction_simulated")
    return tuple(missing)


def _decision_for_missing(name: str) -> ObservabilityEventDecision:
    return {
        "runtime_governance": ObservabilityEventDecision.REQUIRES_RUNTIME_GOVERNANCE,
        "runtime_state": ObservabilityEventDecision.REQUIRES_RUNTIME_STATE,
        "security_layer": ObservabilityEventDecision.REQUIRES_SECURITY_LAYER,
        "output_boundary": ObservabilityEventDecision.REQUIRES_OUTPUT_BOUNDARY,
        "secrets_policy": ObservabilityEventDecision.REQUIRES_SECRETS_POLICY,
        "prompt_injection_defense": ObservabilityEventDecision.REQUIRES_SECRETS_POLICY,
        "metadata_sanitization": ObservabilityEventDecision.REQUIRES_METADATA_SANITIZATION,
        "redaction_simulated": ObservabilityEventDecision.REQUIRES_REDACTION_SIMULATED,
    }.get(name, ObservabilityEventDecision.RECORD_BLOCKED)


def _metadata_errors(metadata: Mapping[str, Any], policy: ObservabilityPolicy) -> tuple[str, ...]:
    if not isinstance(metadata, Mapping):
        return ("metadata_not_mapping",)
    try:
        json.dumps(metadata, sort_keys=True)
    except TypeError:
        return (ObservabilityBlockReason.METADATA_NOT_JSON_SAFE.value,)
    errors: list[str] = []
    _scan_metadata(metadata, errors, "metadata_sanitized", policy)
    return tuple(errors)


def _scan_metadata(value: Any, errors: list[str], path: str, policy: ObservabilityPolicy) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            lowered = str(key).lower()
            if lowered in policy.forbidden_data_keys or any(fragment in lowered for fragment in policy.forbidden_data_keys):
                errors.append(f"metadata_dangerous_key:{path}.{key}")
            _scan_metadata(nested, errors, f"{path}.{key}", policy)
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _scan_metadata(nested, errors, f"{path}[{index}]", policy)


def _coerce_event_type(value: ObservabilityEventType | str) -> ObservabilityEventType:
    if isinstance(value, ObservabilityEventType):
        return value
    try:
        return ObservabilityEventType(str(value))
    except ValueError as exc:
        raise ValueError(f"event_type_not_allowed:{value}") from exc


def _coerce_risk_level(value: ObservabilityRiskLevel | str) -> ObservabilityRiskLevel:
    if isinstance(value, ObservabilityRiskLevel):
        return value
    try:
        return ObservabilityRiskLevel(str(value))
    except ValueError as exc:
        raise ValueError(f"risk_level_not_allowed:{value}") from exc


def _looks_operational(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in (
        "active", "running", "execut", "write", "store", "network", "secret", "tool", "model",
        "context", "output", "runtime", "logger", "event bus", "telemetry", "metrics", "tracing",
        "dashboard", "ledger", "publish",
    ))


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
