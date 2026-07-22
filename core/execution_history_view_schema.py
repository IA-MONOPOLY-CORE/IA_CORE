"""Schema de execution_history_view_contract derived-only preflight-only."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


EXECUTION_HISTORY_VIEW_SCHEMA_VERSION = "1.0"
EXECUTION_HISTORY_VIEW_CONTRACT_TYPE = "execution_history_view_contract"
ALLOWED_MODES = {"execution_history_view_contract_only"}
ALLOWED_HISTORY_MODES = {"derived_only"}
ALLOWED_VIEW_MODES = {"preflight_only"}
ALLOWED_STATUSES = {"passed", "blocked", "failed"}
ALLOWED_VERDICTS = {
    "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED",
    "EXECUTION_HISTORY_VIEW_CONTRACT_BLOCKED",
    "EXECUTION_HISTORY_VIEW_CONTRACT_FAILED",
    "EXECUTION_HISTORY_VIEW_STORE_LEAK",
    "EXECUTION_HISTORY_VIEW_ATTEMPT_ID_LEAK",
    "EXECUTION_HISTORY_VIEW_STATE_LEAK",
    "EXECUTION_HISTORY_VIEW_PAYLOAD_LEAK",
    "EXECUTION_HISTORY_VIEW_EXECUTION_BOUNDARY",
    "EXECUTION_HISTORY_VIEW_EXTERNAL_BOUNDARY",
    "EXECUTION_HISTORY_VIEW_SCHEDULER_WORKER_BOUNDARY",
    "EXECUTION_HISTORY_VIEW_MUTATION_BOUNDARY",
}
REQUIRED_FIELDS = {
    "schema_version",
    "contract_id",
    "contract_type",
    "status",
    "verdict",
    "mode",
    "history_mode",
    "view_mode",
    "target_ref",
    "target_type",
    "target_id",
    "attempt_ref",
    "correlation_id",
    "idempotency_key",
    "dry_run_ref",
    "dry_run_store_ref",
    "dry_run_store_verified",
    "dry_run_store_contract_ref",
    "execution_attempt_store_ref",
    "execution_attempt_store_verified",
    "execution_attempt_store_contract_ref",
    "execution_lifecycle_store_ref",
    "execution_lifecycle_store_verified",
    "execution_lifecycle_contract_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "reference_policy",
    "timeline_policy",
    "store_prohibition_policy",
    "attempt_id_policy",
    "execution_boundary_policy",
    "payload_boundary_policy",
    "readiness_policy",
    "timeline",
    "summary",
    "preflight_status",
    "transition_history",
    "store_verification_summary",
    "timeline_summary",
    "dependency_summary",
    "store_prohibition_summary",
    "attempt_id_summary",
    "execution_boundary_summary",
    "payload_boundary_summary",
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
    "dry_run_ref",
    "dry_run_store_ref",
    "dry_run_store_contract_ref",
    "execution_attempt_store_ref",
    "execution_attempt_store_contract_ref",
    "execution_lifecycle_store_ref",
    "execution_lifecycle_contract_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "reference_policy",
    "timeline_policy",
    "store_prohibition_policy",
    "attempt_id_policy",
    "execution_boundary_policy",
    "payload_boundary_policy",
    "readiness_policy",
    "summary",
    "preflight_status",
    "transition_history",
    "store_verification_summary",
    "timeline_summary",
    "dependency_summary",
    "store_prohibition_summary",
    "attempt_id_summary",
    "execution_boundary_summary",
    "payload_boundary_summary",
    "audit_summary",
    "observability_summary",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
}


@dataclass(frozen=True)
class ExecutionHistoryViewReferencePolicy:
    required_refs: list[str]
    derived_only: bool = True
    cross_target_refs_blocked: bool = True
    cross_attempt_refs_blocked: bool = True
    cross_correlation_refs_blocked: bool = True
    cross_idempotency_refs_blocked: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewTimelinePolicy:
    allowed_events: list[str]
    allowed_states: list[str]
    blocked_states: list[str]
    allows_operational_events: bool = False
    writes_history: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewBoundaryPolicy:
    execution_enabled: bool = False
    agent_execution_enabled: bool = False
    team_execution_enabled: bool = False
    model_invocation_enabled: bool = False
    tool_execution_enabled: bool = False
    memory_persistence_enabled: bool = False
    external_access_enabled: bool = False
    scheduler_enabled: bool = False
    worker_queue_enabled: bool = False
    queued_running_enabled: bool = False
    completed_state_enabled: bool = False
    rollback_operational_enabled: bool = False
    retry_operational_enabled: bool = False
    cancel_operational_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewPayloadPolicy:
    forbidden_fields: list[str]
    deep_scan_required: bool = True
    real_payloads_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewReadiness:
    ready_for_contract_only: bool
    ready_for_derived_view_contract: bool
    ready_for_history_store: bool = False
    ready_for_result_history: bool = False
    ready_for_real_execution: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewContract:
    contract_id: str
    mode: str
    history_mode: str
    view_mode: str
    target_ref: dict[str, Any]
    target_type: str
    target_id: str
    attempt_ref: str
    correlation_id: str
    idempotency_key: str
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    dry_run_store_verified: bool
    dry_run_store_contract_ref: dict[str, Any]
    execution_attempt_store_ref: dict[str, Any]
    execution_attempt_store_verified: bool
    execution_attempt_store_contract_ref: dict[str, Any]
    execution_lifecycle_store_ref: dict[str, Any]
    execution_lifecycle_store_verified: bool
    execution_lifecycle_contract_ref: dict[str, Any]
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_executor_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]
    reference_policy: dict[str, Any]
    timeline_policy: dict[str, Any]
    store_prohibition_policy: dict[str, Any]
    attempt_id_policy: dict[str, Any]
    execution_boundary_policy: dict[str, Any]
    payload_boundary_policy: dict[str, Any]
    readiness_policy: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewContractResult:
    status: str
    verdict: str
    mode: str
    history_mode: str
    view_mode: str
    target_ref: dict[str, Any]
    target_type: str
    target_id: str
    attempt_ref: str | None
    correlation_id: str | None
    idempotency_key: str | None
    timeline_summary: dict[str, Any]
    dependency_summary: dict[str, Any]
    store_prohibition_summary: dict[str, Any]
    attempt_id_summary: dict[str, Any]
    execution_boundary_summary: dict[str, Any]
    payload_boundary_summary: dict[str, Any]
    audit_summary: dict[str, Any]
    observability_summary: dict[str, Any]
    boundary_summary: dict[str, Any]
    readiness_summary: dict[str, Any]
    warnings: list[Any]
    blockers: list[Any]
    evidence: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_execution_history_view_contract_report(
    *,
    contract_id: str,
    status: str,
    verdict: str,
    mode: str,
    history_mode: str,
    view_mode: str,
    target_ref: dict[str, Any],
    target_type: str,
    target_id: str,
    attempt_ref: str | None,
    correlation_id: str | None,
    idempotency_key: str | None,
    dry_run_ref: dict[str, Any],
    dry_run_store_ref: dict[str, Any],
    dry_run_store_verified: bool,
    dry_run_store_contract_ref: dict[str, Any],
    execution_attempt_store_ref: dict[str, Any],
    execution_attempt_store_verified: bool,
    execution_attempt_store_contract_ref: dict[str, Any],
    execution_lifecycle_store_ref: dict[str, Any],
    execution_lifecycle_store_verified: bool,
    execution_lifecycle_contract_ref: dict[str, Any],
    runtime_contract_ref: dict[str, Any],
    execution_contract_ref: dict[str, Any],
    runtime_executor_contract_ref: dict[str, Any],
    runtime_preparation_ref: dict[str, Any],
    execution_runner_contract_ref: dict[str, Any],
    dry_run_contract_ref: dict[str, Any],
    audit_refs: dict[str, Any],
    observability_refs: dict[str, Any],
    capability_policy_ref: dict[str, Any],
    reference_policy: dict[str, Any],
    timeline_policy: dict[str, Any],
    store_prohibition_policy: dict[str, Any],
    attempt_id_policy: dict[str, Any],
    execution_boundary_policy: dict[str, Any],
    payload_boundary_policy: dict[str, Any],
    readiness_policy: dict[str, Any],
    timeline: list[dict[str, Any]],
    summary: dict[str, Any],
    preflight_status: dict[str, Any],
    transition_history: dict[str, Any],
    store_verification_summary: dict[str, Any],
    timeline_summary: dict[str, Any],
    dependency_summary: dict[str, Any],
    store_prohibition_summary: dict[str, Any],
    attempt_id_summary: dict[str, Any],
    execution_boundary_summary: dict[str, Any],
    payload_boundary_summary: dict[str, Any],
    audit_summary: dict[str, Any],
    observability_summary: dict[str, Any],
    boundary_summary: dict[str, Any],
    readiness_summary: dict[str, Any],
    risk_summary: dict[str, Any],
    warnings: list[Any],
    blockers: list[Any],
    evidence: list[Any],
    created_at: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": EXECUTION_HISTORY_VIEW_SCHEMA_VERSION,
        "contract_id": contract_id,
        "contract_type": EXECUTION_HISTORY_VIEW_CONTRACT_TYPE,
        "status": status,
        "verdict": verdict,
        "mode": mode,
        "history_mode": history_mode,
        "view_mode": view_mode,
        "target_ref": target_ref,
        "target_type": target_type,
        "target_id": target_id,
        "attempt_ref": attempt_ref,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "dry_run_ref": dry_run_ref,
        "dry_run_store_ref": dry_run_store_ref,
        "dry_run_store_verified": dry_run_store_verified,
        "dry_run_store_contract_ref": dry_run_store_contract_ref,
        "execution_attempt_store_ref": execution_attempt_store_ref,
        "execution_attempt_store_verified": execution_attempt_store_verified,
        "execution_attempt_store_contract_ref": execution_attempt_store_contract_ref,
        "execution_lifecycle_store_ref": execution_lifecycle_store_ref,
        "execution_lifecycle_store_verified": execution_lifecycle_store_verified,
        "execution_lifecycle_contract_ref": execution_lifecycle_contract_ref,
        "runtime_contract_ref": runtime_contract_ref,
        "execution_contract_ref": execution_contract_ref,
        "runtime_executor_contract_ref": runtime_executor_contract_ref,
        "runtime_preparation_ref": runtime_preparation_ref,
        "execution_runner_contract_ref": execution_runner_contract_ref,
        "dry_run_contract_ref": dry_run_contract_ref,
        "audit_refs": audit_refs,
        "observability_refs": observability_refs,
        "capability_policy_ref": capability_policy_ref,
        "reference_policy": reference_policy,
        "timeline_policy": timeline_policy,
        "store_prohibition_policy": store_prohibition_policy,
        "attempt_id_policy": attempt_id_policy,
        "execution_boundary_policy": execution_boundary_policy,
        "payload_boundary_policy": payload_boundary_policy,
        "readiness_policy": readiness_policy,
        "timeline": timeline,
        "summary": summary,
        "preflight_status": preflight_status,
        "transition_history": transition_history,
        "store_verification_summary": store_verification_summary,
        "timeline_summary": timeline_summary,
        "dependency_summary": dependency_summary,
        "store_prohibition_summary": store_prohibition_summary,
        "attempt_id_summary": attempt_id_summary,
        "execution_boundary_summary": execution_boundary_summary,
        "payload_boundary_summary": payload_boundary_summary,
        "audit_summary": audit_summary,
        "observability_summary": observability_summary,
        "boundary_summary": boundary_summary,
        "readiness_summary": readiness_summary,
        "risk_summary": risk_summary,
        "warnings": warnings,
        "blockers": blockers,
        "evidence": evidence,
        "created_at": created_at or datetime.now().isoformat(),
    }


def validate_execution_history_view_contract_report(report: dict[str, Any]) -> bool:
    if not isinstance(report, dict):
        return False
    if REQUIRED_FIELDS - set(report):
        return False
    if report.get("schema_version") != EXECUTION_HISTORY_VIEW_SCHEMA_VERSION:
        return False
    if report.get("contract_type") != EXECUTION_HISTORY_VIEW_CONTRACT_TYPE:
        return False
    if report.get("status") not in ALLOWED_STATUSES:
        return False
    if report.get("verdict") not in ALLOWED_VERDICTS:
        return False
    if report.get("mode") not in ALLOWED_MODES:
        return False
    if report.get("history_mode") not in ALLOWED_HISTORY_MODES:
        return False
    if report.get("view_mode") not in ALLOWED_VIEW_MODES:
        return False
    for field_name in OBJECT_FIELDS:
        if not isinstance(report.get(field_name), dict):
            return False
    if not isinstance(report.get("timeline"), list):
        return False
    if not isinstance(report.get("warnings"), list):
        return False
    if not isinstance(report.get("blockers"), list):
        return False
    if not isinstance(report.get("evidence"), list):
        return False
    return True
