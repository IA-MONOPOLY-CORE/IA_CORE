"""Schema de execution_lifecycle_contract preflight-transitions-only."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


EXECUTION_LIFECYCLE_CONTRACT_SCHEMA_VERSION = "1.0"
EXECUTION_LIFECYCLE_CONTRACT_TYPE = "execution_lifecycle_contract"
ALLOWED_MODES = {"execution_lifecycle_contract_only"}
ALLOWED_LIFECYCLE_MODES = {"preflight_transitions_only"}
ALLOWED_CONTRACT_STATUSES = {"passed", "blocked", "failed"}
ALLOWED_VERDICTS = {
    "EXECUTION_LIFECYCLE_CONTRACT_PASSED",
    "EXECUTION_LIFECYCLE_CONTRACT_BLOCKED",
    "EXECUTION_LIFECYCLE_CONTRACT_FAILED",
    "EXECUTION_LIFECYCLE_CONTRACT_ATTEMPT_ID_LEAK",
    "EXECUTION_LIFECYCLE_CONTRACT_STATE_LEAK",
    "EXECUTION_LIFECYCLE_CONTRACT_TRANSITION_LEAK",
    "EXECUTION_LIFECYCLE_CONTRACT_PAYLOAD_LEAK",
    "EXECUTION_LIFECYCLE_CONTRACT_EXECUTION_BOUNDARY",
    "EXECUTION_LIFECYCLE_CONTRACT_EXTERNAL_BOUNDARY",
    "EXECUTION_LIFECYCLE_CONTRACT_SCHEDULER_WORKER_BOUNDARY",
    "EXECUTION_LIFECYCLE_CONTRACT_MUTATION_BOUNDARY",
}
REQUIRED_FIELDS = {
    "schema_version",
    "contract_id",
    "contract_type",
    "status",
    "verdict",
    "mode",
    "lifecycle_mode",
    "target_ref",
    "attempt_ref",
    "execution_attempt_store_ref",
    "execution_attempt_store_verification_ref",
    "execution_attempt_store_contract_ref",
    "dry_run_ref",
    "dry_run_store_ref",
    "dry_run_store_verification_ref",
    "dry_run_store_contract_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "correlation_id",
    "idempotency_key",
    "state_policy",
    "transition_policy",
    "attempt_id_policy",
    "execution_boundary_policy",
    "payload_boundary_policy",
    "scheduler_worker_policy",
    "model_tool_memory_policy",
    "external_access_policy",
    "readiness_policy",
    "state_summary",
    "transition_summary",
    "attempt_id_summary",
    "dependency_summary",
    "execution_boundary_summary",
    "payload_boundary_summary",
    "scheduler_worker_summary",
    "model_tool_memory_summary",
    "external_access_summary",
    "audit_summary",
    "observability_summary",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
    "warnings",
    "blockers",
    "evidence",
    "created_at",
}
OBJECT_FIELDS = {
    "target_ref",
    "execution_attempt_store_ref",
    "execution_attempt_store_verification_ref",
    "execution_attempt_store_contract_ref",
    "dry_run_ref",
    "dry_run_store_ref",
    "dry_run_store_verification_ref",
    "dry_run_store_contract_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "state_policy",
    "transition_policy",
    "attempt_id_policy",
    "execution_boundary_policy",
    "payload_boundary_policy",
    "scheduler_worker_policy",
    "model_tool_memory_policy",
    "external_access_policy",
    "readiness_policy",
    "state_summary",
    "transition_summary",
    "attempt_id_summary",
    "dependency_summary",
    "execution_boundary_summary",
    "payload_boundary_summary",
    "scheduler_worker_summary",
    "model_tool_memory_summary",
    "external_access_summary",
    "audit_summary",
    "observability_summary",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
}


@dataclass(frozen=True)
class ExecutionLifecycleStatePolicy:
    allowed_states: list[str]
    blocked_states: list[str]
    current_state: str
    target_state: str
    operational_states_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleTransitionPolicy:
    allowed_transitions: list[dict[str, str]]
    blocked_transitions: list[dict[str, str]]
    source_state: str
    target_state: str
    implicit_execution_allowed: bool = False
    implicit_scheduler_worker_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleReferencePolicy:
    required_refs: list[str]
    cross_target_refs_blocked: bool = True
    cross_attempt_refs_blocked: bool = True
    cross_correlation_refs_blocked: bool = True
    cross_idempotency_refs_blocked: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleBoundaryPolicy:
    execution_enabled: bool = False
    agent_execution_enabled: bool = False
    team_execution_enabled: bool = False
    model_invocation_enabled: bool = False
    tool_execution_enabled: bool = False
    memory_persistence_enabled: bool = False
    external_access_enabled: bool = False
    scheduler_enabled: bool = False
    worker_queue_enabled: bool = False
    rollback_operational_enabled: bool = False
    retry_operational_enabled: bool = False
    cancel_operational_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleReadiness:
    ready_for_contract_only: bool
    ready_for_preflight_transitions_only: bool
    ready_for_lifecycle_implementation: bool = False
    ready_for_real_execution: bool = False
    ready_for_scheduler_worker: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleEventPolicy:
    allowed_events: list[str]
    forbidden_events: list[str]
    writes_events: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleContract:
    contract_id: str
    mode: str
    lifecycle_mode: str
    target_ref: dict[str, Any]
    attempt_ref: str
    execution_attempt_store_ref: dict[str, Any]
    execution_attempt_store_verification_ref: dict[str, Any]
    execution_attempt_store_contract_ref: dict[str, Any]
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    dry_run_store_verification_ref: dict[str, Any]
    dry_run_store_contract_ref: dict[str, Any]
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_executor_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]
    correlation_id: str
    idempotency_key: str
    state_policy: dict[str, Any]
    transition_policy: dict[str, Any]
    attempt_id_policy: dict[str, Any]
    execution_boundary_policy: dict[str, Any]
    payload_boundary_policy: dict[str, Any]
    scheduler_worker_policy: dict[str, Any]
    model_tool_memory_policy: dict[str, Any]
    external_access_policy: dict[str, Any]
    readiness_policy: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleContractResult:
    status: str
    verdict: str
    mode: str
    lifecycle_mode: str
    target_ref: dict[str, Any]
    attempt_ref: str | None
    state_summary: dict[str, Any]
    transition_summary: dict[str, Any]
    attempt_id_summary: dict[str, Any]
    dependency_summary: dict[str, Any]
    execution_boundary_summary: dict[str, Any]
    payload_boundary_summary: dict[str, Any]
    scheduler_worker_summary: dict[str, Any]
    model_tool_memory_summary: dict[str, Any]
    external_access_summary: dict[str, Any]
    audit_summary: dict[str, Any]
    observability_summary: dict[str, Any]
    boundary_summary: dict[str, Any]
    readiness_summary: dict[str, Any]
    blockers: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_execution_lifecycle_contract_report(
    *,
    contract_id: str,
    status: str,
    verdict: str,
    mode: str,
    lifecycle_mode: str,
    target_ref: dict[str, Any],
    attempt_ref: str | None,
    execution_attempt_store_ref: dict[str, Any],
    execution_attempt_store_verification_ref: dict[str, Any],
    execution_attempt_store_contract_ref: dict[str, Any],
    dry_run_ref: dict[str, Any],
    dry_run_store_ref: dict[str, Any],
    dry_run_store_verification_ref: dict[str, Any],
    dry_run_store_contract_ref: dict[str, Any],
    runtime_contract_ref: dict[str, Any],
    execution_contract_ref: dict[str, Any],
    runtime_executor_contract_ref: dict[str, Any],
    runtime_preparation_ref: dict[str, Any],
    execution_runner_contract_ref: dict[str, Any],
    dry_run_contract_ref: dict[str, Any],
    audit_refs: dict[str, Any],
    observability_refs: dict[str, Any],
    capability_policy_ref: dict[str, Any],
    correlation_id: str | None,
    idempotency_key: str | None,
    state_policy: dict[str, Any],
    transition_policy: dict[str, Any],
    attempt_id_policy: dict[str, Any],
    execution_boundary_policy: dict[str, Any],
    payload_boundary_policy: dict[str, Any],
    scheduler_worker_policy: dict[str, Any],
    model_tool_memory_policy: dict[str, Any],
    external_access_policy: dict[str, Any],
    readiness_policy: dict[str, Any],
    state_summary: dict[str, Any],
    transition_summary: dict[str, Any],
    attempt_id_summary: dict[str, Any],
    dependency_summary: dict[str, Any],
    execution_boundary_summary: dict[str, Any],
    payload_boundary_summary: dict[str, Any],
    scheduler_worker_summary: dict[str, Any],
    model_tool_memory_summary: dict[str, Any],
    external_access_summary: dict[str, Any],
    audit_summary: dict[str, Any],
    observability_summary: dict[str, Any],
    boundary_summary: dict[str, Any],
    readiness_summary: dict[str, Any],
    risk_summary: dict[str, Any],
    blockers: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    report = {
        "schema_version": EXECUTION_LIFECYCLE_CONTRACT_SCHEMA_VERSION,
        "contract_id": contract_id,
        "contract_type": EXECUTION_LIFECYCLE_CONTRACT_TYPE,
        "status": status,
        "verdict": verdict,
        "mode": mode,
        "lifecycle_mode": lifecycle_mode,
        "target_ref": dict(target_ref or {}),
        "attempt_ref": attempt_ref,
        "execution_attempt_store_ref": dict(execution_attempt_store_ref or {}),
        "execution_attempt_store_verification_ref": dict(execution_attempt_store_verification_ref or {}),
        "execution_attempt_store_contract_ref": dict(execution_attempt_store_contract_ref or {}),
        "dry_run_ref": dict(dry_run_ref or {}),
        "dry_run_store_ref": dict(dry_run_store_ref or {}),
        "dry_run_store_verification_ref": dict(dry_run_store_verification_ref or {}),
        "dry_run_store_contract_ref": dict(dry_run_store_contract_ref or {}),
        "runtime_contract_ref": dict(runtime_contract_ref or {}),
        "execution_contract_ref": dict(execution_contract_ref or {}),
        "runtime_executor_contract_ref": dict(runtime_executor_contract_ref or {}),
        "runtime_preparation_ref": dict(runtime_preparation_ref or {}),
        "execution_runner_contract_ref": dict(execution_runner_contract_ref or {}),
        "dry_run_contract_ref": dict(dry_run_contract_ref or {}),
        "audit_refs": dict(audit_refs or {}),
        "observability_refs": dict(observability_refs or {}),
        "capability_policy_ref": dict(capability_policy_ref or {}),
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "state_policy": dict(state_policy or {}),
        "transition_policy": dict(transition_policy or {}),
        "attempt_id_policy": dict(attempt_id_policy or {}),
        "execution_boundary_policy": dict(execution_boundary_policy or {}),
        "payload_boundary_policy": dict(payload_boundary_policy or {}),
        "scheduler_worker_policy": dict(scheduler_worker_policy or {}),
        "model_tool_memory_policy": dict(model_tool_memory_policy or {}),
        "external_access_policy": dict(external_access_policy or {}),
        "readiness_policy": dict(readiness_policy or {}),
        "state_summary": dict(state_summary or {}),
        "transition_summary": dict(transition_summary or {}),
        "attempt_id_summary": dict(attempt_id_summary or {}),
        "dependency_summary": dict(dependency_summary or {}),
        "execution_boundary_summary": dict(execution_boundary_summary or {}),
        "payload_boundary_summary": dict(payload_boundary_summary or {}),
        "scheduler_worker_summary": dict(scheduler_worker_summary or {}),
        "model_tool_memory_summary": dict(model_tool_memory_summary or {}),
        "external_access_summary": dict(external_access_summary or {}),
        "audit_summary": dict(audit_summary or {}),
        "observability_summary": dict(observability_summary or {}),
        "boundary_summary": dict(boundary_summary or {}),
        "readiness_summary": dict(readiness_summary or {}),
        "risk_summary": dict(risk_summary or {}),
        "warnings": list(warnings or []),
        "blockers": list(blockers or []),
        "evidence": list(evidence or []),
        "created_at": datetime.now().isoformat(),
    }
    validate_execution_lifecycle_contract_report(report)
    return report


def validate_execution_lifecycle_contract_report(report: dict[str, Any]) -> bool:
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"missing execution_lifecycle_contract fields: {sorted(missing)}")
    if report["schema_version"] != EXECUTION_LIFECYCLE_CONTRACT_SCHEMA_VERSION:
        raise ValueError("invalid execution_lifecycle_contract schema_version")
    if report["contract_type"] != EXECUTION_LIFECYCLE_CONTRACT_TYPE:
        raise ValueError("invalid execution_lifecycle_contract contract_type")
    if report["status"] not in ALLOWED_CONTRACT_STATUSES:
        raise ValueError("invalid execution_lifecycle_contract status")
    if report["verdict"] not in ALLOWED_VERDICTS:
        raise ValueError("invalid execution_lifecycle_contract verdict")
    if report["mode"] not in ALLOWED_MODES:
        raise ValueError("invalid execution_lifecycle_contract mode")
    if report["lifecycle_mode"] not in ALLOWED_LIFECYCLE_MODES:
        raise ValueError("invalid execution_lifecycle_contract lifecycle_mode")
    for field_name in OBJECT_FIELDS:
        if not isinstance(report[field_name], dict):
            raise ValueError(f"{field_name} must be object")
    for field_name in ["warnings", "blockers", "evidence"]:
        if not isinstance(report[field_name], list):
            raise ValueError(f"{field_name} must be list")
    return True
