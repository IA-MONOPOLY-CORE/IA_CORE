"""In-memory execution history view derived from verified preflight stores.

This module builds a derived read model only. It does not create a history
store, result store, operational execution_attempt_id, JSONL files, parent
directories, executions, scheduler jobs, worker tasks or payload persistence.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
MODE = "execution_history_view_derived_only"
HISTORY_MODE = "derived_only"
VIEW_MODE = "preflight_only"
PASSED_CONTRACT_VERDICT = "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"

BUILT_VERDICT = "EXECUTION_HISTORY_VIEW_BUILT"
VALIDATED_VERDICT = "EXECUTION_HISTORY_VIEW_VALIDATED"
BLOCKED_VERDICT = "EXECUTION_HISTORY_VIEW_BLOCKED"
FAILED_VERDICT = "EXECUTION_HISTORY_VIEW_FAILED"
CONTRACT_NOT_PASSED_VERDICT = "EXECUTION_HISTORY_VIEW_CONTRACT_NOT_PASSED"
STORE_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_STORE_LEAK"
ATTEMPT_ID_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_ATTEMPT_ID_LEAK"
STATE_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_STATE_LEAK"
TIMELINE_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_TIMELINE_LEAK"
PAYLOAD_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_PAYLOAD_LEAK"
EXECUTION_BOUNDARY_VERDICT = "EXECUTION_HISTORY_VIEW_EXECUTION_BOUNDARY"
EXTERNAL_BOUNDARY_VERDICT = "EXECUTION_HISTORY_VIEW_EXTERNAL_BOUNDARY"
SCHEDULER_WORKER_BOUNDARY_VERDICT = "EXECUTION_HISTORY_VIEW_SCHEDULER_WORKER_BOUNDARY"
MUTATION_BOUNDARY_VERDICT = "EXECUTION_HISTORY_VIEW_MUTATION_BOUNDARY"

ALLOWED_TIMELINE_EVENTS = {
    "dry_run_created",
    "dry_run_store_verified",
    "execution_attempt_preflight_created",
    "execution_attempt_store_verified",
    "execution_lifecycle_transition_appended",
    "execution_lifecycle_store_verified",
    "history_view_built",
}
ALLOWED_VIEW_STATES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
    "noop_idempotent",
    "simulated",
    "prepared",
    "verified",
    "appended",
}
BLOCKED_TIMELINE_EVENTS = {
    "execution_queued",
    "execution_running",
    "execution_completed",
    "execution_cancelled",
    "execution_rolled_back",
    "agent_execution_started",
    "team_execution_started",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
    "execution_result_created",
    "execution_output_created",
    "history_store_written",
    "result_store_written",
}
BLOCKED_VIEW_STATES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
STORE_FLAGS = {
    "history_store_enabled": "history_store_enabled_not_allowed",
    "execution_history_store_enabled": "execution_history_store_enabled_not_allowed",
    "attempt_history_store_enabled": "attempt_history_store_enabled_not_allowed",
    "execution_result_store_enabled": "execution_result_store_enabled_not_allowed",
    "result_persistence_enabled": "result_persistence_enabled_not_allowed",
    "jsonl_history_enabled": "jsonl_history_enabled_not_allowed",
    "writes_enabled": "writes_enabled_not_allowed",
    "append_enabled": "append_enabled_not_allowed",
}
FORBIDDEN_STORE_REFS = {
    "execution_history_store_ref": "execution_history_store_ref_not_allowed",
    "attempt_history_store_ref": "attempt_history_store_ref_not_allowed",
    "execution_result_store_ref": "execution_result_store_ref_not_allowed",
    "history_store_path": "history_store_path_not_allowed",
    "execution_history_jsonl_path": "execution_history_jsonl_path_not_allowed",
    "result_store_path": "result_store_path_not_allowed",
    "write_path": "write_path_not_allowed",
    "append_path": "append_path_not_allowed",
}
ATTEMPT_ID_FLAGS = {
    "attempt_id_generation_enabled": "attempt_id_generation_enabled_not_allowed",
    "attempt_id_persistence_enabled": "attempt_id_persistence_enabled_not_allowed",
    "materialized_attempt_id": "materialized_attempt_id_not_allowed",
    "attempt_ref_is_operational_id": "attempt_ref_is_operational_id_not_allowed",
}
EXECUTION_FLAGS = {
    "execution_enabled": "execution_enabled_not_allowed",
    "agent_execution_enabled": "agent_execution_enabled_not_allowed",
    "team_execution_enabled": "team_execution_enabled_not_allowed",
    "model_invocation_enabled": "model_invocation_enabled_not_allowed",
    "tool_execution_enabled": "tool_execution_enabled_not_allowed",
    "memory_persistence_enabled": "memory_persistence_enabled_not_allowed",
    "external_access_enabled": "external_access_enabled_not_allowed",
    "scheduler_enabled": "scheduler_enabled_not_allowed",
    "worker_queue_enabled": "worker_queue_enabled_not_allowed",
    "queued_running_enabled": "queued_running_enabled_not_allowed",
    "completed_state_enabled": "completed_state_enabled_not_allowed",
    "rollback_operational_enabled": "rollback_operational_enabled_not_allowed",
    "retry_operational_enabled": "retry_operational_enabled_not_allowed",
    "cancel_operational_enabled": "cancel_operational_enabled_not_allowed",
}
FORBIDDEN_PAYLOAD_FIELDS = {
    "execution_payload": "execution_payload_not_allowed",
    "execution_result": "execution_result_not_allowed",
    "execution_output": "execution_output_not_allowed",
    "execution_history_payload": "execution_history_payload_not_allowed",
    "execution_result_history": "execution_result_history_not_allowed",
    "agent_output": "agent_output_not_allowed",
    "team_output": "team_output_not_allowed",
    "model_prompt_real": "model_prompt_real_not_allowed",
    "model_response": "model_response_not_allowed",
    "model_completion_real": "model_completion_real_not_allowed",
    "tool_call_real": "tool_call_real_not_allowed",
    "tool_result": "tool_result_not_allowed",
    "memory_write": "memory_write_not_allowed",
    "memory_read_result": "memory_read_result_not_allowed",
    "external_request": "external_request_not_allowed",
    "external_response": "external_response_not_allowed",
    "scheduler_job": "scheduler_job_not_allowed",
    "worker_task": "worker_task_not_allowed",
    "state_mutation": "state_mutation_not_allowed",
    "artifact_mutation": "artifact_mutation_not_allowed",
    "database_write_result": "database_write_result_not_allowed",
    "network_response": "network_response_not_allowed",
    "secret_value": "secret_value_not_allowed",
    "credential_value": "credential_value_not_allowed",
    "actual_output": "actual_output_not_allowed",
    "real_output": "real_output_not_allowed",
    "live_response": "live_response_not_allowed",
    "side_effect_result": "side_effect_result_not_allowed",
    "mutation_result": "mutation_result_not_allowed",
}
FORBIDDEN_FILES = {
    "core/execution_history_store.py": "execution_history_store_not_allowed",
    "core/attempt_history.py": "attempt_history_store_not_allowed",
    "core/execution_attempt_history.py": "execution_attempt_history_store_not_allowed",
    "core/execution_result_store.py": "execution_result_store_not_allowed",
    "core/execution_attempt_id.py": "execution_attempt_id_not_allowed",
    "core/scheduler_queue.py": "scheduler_worker_queue_not_allowed",
    "core/worker_queue.py": "scheduler_worker_queue_not_allowed",
}


@dataclass(frozen=True)
class ExecutionHistoryView:
    view_id: str
    schema_version: str
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
    execution_history_view_contract_ref: dict[str, Any]
    execution_history_view_contract_verdict: str | None
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_executor_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]
    summary: dict[str, Any]
    timeline: list[dict[str, Any]]
    preflight_status: dict[str, Any]
    transition_history: dict[str, Any]
    store_verification_summary: dict[str, Any]
    boundary_summary: dict[str, Any]
    risk_summary: dict[str, Any]
    evidence: list[dict[str, Any]]
    warnings: list[Any]
    blockers: list[dict[str, str]]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionHistoryViewOperationResult:
    status: str
    verdict: str
    operation: str
    mode: str
    history_mode: str
    view_mode: str
    view_id: str | None
    target_ref: dict[str, Any]
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
    blockers: list[dict[str, str]]
    evidence: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_execution_history_view(
    *,
    dry_run_store_entries: list[dict[str, Any]] | None,
    dry_run_store_verified: bool,
    execution_attempt_store_entries: list[dict[str, Any]] | None,
    execution_attempt_store_verified: bool,
    execution_lifecycle_store_entries: list[dict[str, Any]] | None,
    execution_lifecycle_store_verified: bool,
    execution_history_view_contract_ref: dict[str, Any] | None,
    execution_history_view_contract_verdict: str | None = None,
    attempt_ref: str | None = None,
    target_ref: dict[str, Any] | None = None,
    target_type: str | None = None,
    target_id: str | None = None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    audit_refs: dict[str, Any] | None = None,
    observability_refs: dict[str, Any] | None = None,
    capability_policy_ref: dict[str, Any] | None = None,
    runtime_contract_ref: dict[str, Any] | None = None,
    execution_contract_ref: dict[str, Any] | None = None,
    runtime_executor_contract_ref: dict[str, Any] | None = None,
    runtime_preparation_ref: dict[str, Any] | None = None,
    execution_runner_contract_ref: dict[str, Any] | None = None,
    dry_run_contract_ref: dict[str, Any] | None = None,
    dry_run_ref: dict[str, Any] | None = None,
    dry_run_store_ref: dict[str, Any] | None = None,
    dry_run_store_contract_ref: dict[str, Any] | None = None,
    execution_attempt_store_ref: dict[str, Any] | None = None,
    execution_attempt_store_contract_ref: dict[str, Any] | None = None,
    execution_lifecycle_store_ref: dict[str, Any] | None = None,
    execution_lifecycle_contract_ref: dict[str, Any] | None = None,
    store_prohibition_policy: dict[str, Any] | None = None,
    attempt_id_policy: dict[str, Any] | None = None,
    execution_boundary_policy: dict[str, Any] | None = None,
    payload_boundary_policy: dict[str, Any] | None = None,
    timeline: list[dict[str, Any]] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[Any] = []
    dry_entries = _list_copy(dry_run_store_entries)
    attempt_entries = _list_copy(execution_attempt_store_entries)
    lifecycle_entries = _list_copy(execution_lifecycle_store_entries)
    contract_ref = _copy_dict(execution_history_view_contract_ref)
    target = _copy_dict(target_ref)
    resolved_target_type = target_type or target.get("target_type")
    resolved_target_id = target_id or target.get("target_id")
    resolved_contract_verdict = execution_history_view_contract_verdict or contract_ref.get("verdict")
    dry_ref = _copy_dict(dry_run_ref) or _first_dict(dry_entries)
    attempt_store_ref = _copy_dict(execution_attempt_store_ref) or _first_dict(attempt_entries)
    lifecycle_store_ref = _copy_dict(execution_lifecycle_store_ref) or _first_dict(lifecycle_entries)
    resolved_attempt_ref = attempt_ref if attempt_ref is not None else attempt_store_ref.get("attempt_ref") or lifecycle_store_ref.get("attempt_ref")
    resolved_correlation_id = correlation_id if correlation_id is not None else attempt_store_ref.get("correlation_id") or lifecycle_store_ref.get("correlation_id") or dry_ref.get("correlation_id")
    resolved_idempotency_key = idempotency_key if idempotency_key is not None else attempt_store_ref.get("idempotency_key") or lifecycle_store_ref.get("idempotency_key") or dry_ref.get("idempotency_key")
    view_id = f"execution_history_view_{resolved_target_type or 'target'}_{resolved_target_id or 'target'}"

    _validate_forbidden_files(blockers)
    _validate_dependencies(
        blockers=blockers,
        dry_run_store_entries=dry_entries,
        dry_run_store_verified=dry_run_store_verified,
        execution_attempt_store_entries=attempt_entries,
        execution_attempt_store_verified=execution_attempt_store_verified,
        execution_lifecycle_store_entries=lifecycle_entries,
        execution_lifecycle_store_verified=execution_lifecycle_store_verified,
        execution_history_view_contract_ref=contract_ref,
        execution_history_view_contract_verdict=resolved_contract_verdict,
        attempt_ref=resolved_attempt_ref,
        target_ref=target,
        target_type=resolved_target_type,
        target_id=resolved_target_id,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        audit_refs=audit_refs,
        observability_refs=observability_refs,
        capability_policy_ref=capability_policy_ref,
        runtime_contract_ref=runtime_contract_ref,
        execution_contract_ref=execution_contract_ref,
        runtime_executor_contract_ref=runtime_executor_contract_ref,
        runtime_preparation_ref=runtime_preparation_ref,
        execution_runner_contract_ref=execution_runner_contract_ref,
        dry_run_contract_ref=dry_run_contract_ref,
    )
    _validate_cross_refs(
        refs=[
            ("target_ref", target),
            ("dry_run_ref", dry_ref),
            ("dry_run_store_ref", dry_run_store_ref),
            ("dry_run_store_contract_ref", dry_run_store_contract_ref),
            ("execution_attempt_store_ref", attempt_store_ref),
            ("execution_attempt_store_contract_ref", execution_attempt_store_contract_ref),
            ("execution_lifecycle_store_ref", lifecycle_store_ref),
            ("execution_lifecycle_contract_ref", execution_lifecycle_contract_ref),
            ("execution_history_view_contract_ref", contract_ref),
            ("runtime_contract_ref", runtime_contract_ref),
            ("execution_contract_ref", execution_contract_ref),
            ("runtime_executor_contract_ref", runtime_executor_contract_ref),
            ("runtime_preparation_ref", runtime_preparation_ref),
            ("execution_runner_contract_ref", execution_runner_contract_ref),
            ("dry_run_contract_ref", dry_run_contract_ref),
        ],
        target_type=resolved_target_type,
        target_id=resolved_target_id,
        attempt_ref=resolved_attempt_ref,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        dry_run_id=dry_ref.get("dry_run_id"),
        blockers=blockers,
    )
    store_policy = build_store_prohibition_policy() if store_prohibition_policy is None else _copy_dict(store_prohibition_policy)
    attempt_policy = build_attempt_id_policy(resolved_attempt_ref) if attempt_id_policy is None else _copy_dict(attempt_id_policy)
    execution_policy = build_execution_boundary_policy() if execution_boundary_policy is None else _copy_dict(execution_boundary_policy)
    payload_policy = build_payload_boundary_policy() if payload_boundary_policy is None else _copy_dict(payload_boundary_policy)
    resolved_timeline = _list_copy(timeline) if timeline is not None else derive_execution_history_timeline(
        dry_run_store_entries=dry_entries,
        execution_attempt_store_entries=attempt_entries,
        execution_lifecycle_store_entries=lifecycle_entries,
    )
    _validate_timeline(resolved_timeline, blockers)
    _validate_store_policy(store_policy, blockers)
    _validate_attempt_id_policy(attempt_policy, blockers)
    _validate_execution_boundary_policy(execution_policy, blockers)
    _validate_payload_boundary_policy(payload_policy, blockers)
    _scan_forbidden_payload(payload or {}, blockers)

    summary = derive_summary(
        dry_run_store_entries=dry_entries,
        execution_attempt_store_entries=attempt_entries,
        execution_lifecycle_store_entries=lifecycle_entries,
        target_type=resolved_target_type,
        target_id=resolved_target_id,
        attempt_ref=resolved_attempt_ref,
    )
    preflight_status = derive_preflight_status(dry_entries, attempt_entries, lifecycle_entries)
    transition_history = derive_transition_history(lifecycle_entries)
    store_summary = derive_store_verification_summary(
        dry_run_store_verified=dry_run_store_verified,
        execution_attempt_store_verified=execution_attempt_store_verified,
        execution_lifecycle_store_verified=execution_lifecycle_store_verified,
        dry_run_store_entries=dry_entries,
        execution_attempt_store_entries=attempt_entries,
        execution_lifecycle_store_entries=lifecycle_entries,
    )
    boundary_summary = derive_boundary_summary(blockers)
    risk_summary = derive_risk_summary()
    evidence = build_evidence(dry_run_store_verified, execution_attempt_store_verified, execution_lifecycle_store_verified, resolved_contract_verdict)
    status = "built" if not blockers else "blocked"
    verdict = BUILT_VERDICT if not blockers else _verdict(blockers)

    return ExecutionHistoryView(
        view_id=view_id,
        schema_version=SCHEMA_VERSION,
        status=status,
        verdict=verdict,
        mode=MODE,
        history_mode=HISTORY_MODE,
        view_mode=VIEW_MODE,
        target_ref=target,
        target_type=resolved_target_type or "",
        target_id=resolved_target_id or "",
        attempt_ref=resolved_attempt_ref,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        dry_run_ref=dry_ref,
        dry_run_store_ref=_copy_dict(dry_run_store_ref) or dry_ref,
        dry_run_store_verified=dry_run_store_verified,
        dry_run_store_contract_ref=_contract_ref(dry_run_store_contract_ref),
        execution_attempt_store_ref=attempt_store_ref,
        execution_attempt_store_verified=execution_attempt_store_verified,
        execution_attempt_store_contract_ref=_contract_ref(execution_attempt_store_contract_ref),
        execution_lifecycle_store_ref=lifecycle_store_ref,
        execution_lifecycle_store_verified=execution_lifecycle_store_verified,
        execution_lifecycle_contract_ref=_contract_ref(execution_lifecycle_contract_ref),
        execution_history_view_contract_ref=_contract_ref(contract_ref),
        execution_history_view_contract_verdict=resolved_contract_verdict,
        runtime_contract_ref=_contract_ref(runtime_contract_ref),
        execution_contract_ref=_contract_ref(execution_contract_ref),
        runtime_executor_contract_ref=_contract_ref(runtime_executor_contract_ref),
        runtime_preparation_ref=_contract_ref(runtime_preparation_ref),
        execution_runner_contract_ref=_contract_ref(execution_runner_contract_ref),
        dry_run_contract_ref=_contract_ref(dry_run_contract_ref),
        audit_refs=_copy_dict(audit_refs),
        observability_refs=_copy_dict(observability_refs),
        capability_policy_ref=_copy_dict(capability_policy_ref),
        summary=summary,
        timeline=resolved_timeline,
        preflight_status=preflight_status,
        transition_history=transition_history,
        store_verification_summary=store_summary,
        boundary_summary=boundary_summary,
        risk_summary=risk_summary,
        evidence=evidence,
        warnings=warnings,
        blockers=blockers,
        created_at=datetime.now().isoformat(),
    ).to_dict()


def validate_execution_history_view(
    view: dict[str, Any] | None,
    *,
    store_prohibition_policy: dict[str, Any] | None = None,
    attempt_id_policy: dict[str, Any] | None = None,
    execution_boundary_policy: dict[str, Any] | None = None,
    payload_boundary_policy: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[Any] = []
    candidate = _copy_dict(view)
    _validate_forbidden_files(blockers)
    if not candidate:
        _block(blockers, "missing_view", "execution history view requerida")
    if candidate.get("mode") != MODE:
        _block(blockers, "invalid_mode", "mode debe ser execution_history_view_derived_only")
    if candidate.get("history_mode") != HISTORY_MODE:
        _block(blockers, "invalid_history_mode", "history_mode debe ser derived_only")
    if candidate.get("view_mode") != VIEW_MODE:
        _block(blockers, "invalid_view_mode", "view_mode debe ser preflight_only")
    if candidate.get("execution_history_view_contract_verdict") != PASSED_CONTRACT_VERDICT:
        _block(blockers, "execution_history_view_contract_not_passed", "contract verdict requerido")
    _validate_timeline(candidate.get("timeline") or [], blockers)
    _validate_store_policy(store_prohibition_policy or build_store_prohibition_policy(), blockers)
    _validate_attempt_id_policy(attempt_id_policy or build_attempt_id_policy(candidate.get("attempt_ref")), blockers)
    _validate_execution_boundary_policy(execution_boundary_policy or build_execution_boundary_policy(), blockers)
    _validate_payload_boundary_policy(payload_boundary_policy or build_payload_boundary_policy(), blockers)
    _scan_forbidden_payload(payload or {}, blockers)
    _scan_forbidden_payload(candidate, blockers)
    status = "validated" if not blockers else "blocked"
    verdict = VALIDATED_VERDICT if not blockers else _verdict(blockers)
    return build_operation_result(
        status=status,
        verdict=verdict,
        operation="validate_execution_history_view",
        view=candidate,
        blockers=blockers,
        warnings=warnings,
    )


def derive_execution_history_timeline(
    *,
    dry_run_store_entries: list[dict[str, Any]],
    execution_attempt_store_entries: list[dict[str, Any]],
    execution_lifecycle_store_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {"event": "dry_run_created", "state": _entry_state(_first_dict(dry_run_store_entries), "simulated")},
        {"event": "dry_run_store_verified", "state": "verified"},
        {"event": "execution_attempt_preflight_created", "state": _entry_state(_first_dict(execution_attempt_store_entries), "preflight_passed")},
        {"event": "execution_attempt_store_verified", "state": "verified"},
        {"event": "execution_lifecycle_transition_appended", "state": _entry_state(_first_dict(execution_lifecycle_store_entries), "appended")},
        {"event": "execution_lifecycle_store_verified", "state": "verified"},
        {"event": "history_view_built", "state": "created"},
    ]


def derive_summary(
    *,
    dry_run_store_entries: list[dict[str, Any]],
    execution_attempt_store_entries: list[dict[str, Any]],
    execution_lifecycle_store_entries: list[dict[str, Any]],
    target_type: str | None,
    target_id: str | None,
    attempt_ref: str | None,
) -> dict[str, Any]:
    return {
        "source": "verified_primary_stores",
        "target_type": target_type,
        "target_id": target_id,
        "attempt_ref": attempt_ref,
        "dry_run_entry_count": len(dry_run_store_entries),
        "execution_attempt_entry_count": len(execution_attempt_store_entries),
        "execution_lifecycle_entry_count": len(execution_lifecycle_store_entries),
        "derived_only": True,
        "preflight_only": True,
    }


def derive_preflight_status(
    dry_run_store_entries: list[dict[str, Any]],
    execution_attempt_store_entries: list[dict[str, Any]],
    execution_lifecycle_store_entries: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "status": "preflight_passed",
        "dry_run_result_only": bool(dry_run_store_entries),
        "execution_attempt_preflight": bool(execution_attempt_store_entries),
        "execution_lifecycle_transition": bool(execution_lifecycle_store_entries),
        "execution_enabled": False,
    }


def derive_transition_history(execution_lifecycle_store_entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "source": "execution_lifecycle_store_entries",
        "entry_count": len(execution_lifecycle_store_entries),
        "transitions": [
            {
                "entry_id": entry.get("entry_id"),
                "from_state": entry.get("from_state"),
                "to_state": entry.get("to_state") or entry.get("state"),
                "attempt_ref": entry.get("attempt_ref"),
            }
            for entry in execution_lifecycle_store_entries
        ],
    }


def derive_store_verification_summary(
    *,
    dry_run_store_verified: bool,
    execution_attempt_store_verified: bool,
    execution_lifecycle_store_verified: bool,
    dry_run_store_entries: list[dict[str, Any]],
    execution_attempt_store_entries: list[dict[str, Any]],
    execution_lifecycle_store_entries: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "dry_run_store_verified": dry_run_store_verified,
        "execution_attempt_store_verified": execution_attempt_store_verified,
        "execution_lifecycle_store_verified": execution_lifecycle_store_verified,
        "dry_run_entry_count": len(dry_run_store_entries),
        "execution_attempt_entry_count": len(execution_attempt_store_entries),
        "execution_lifecycle_entry_count": len(execution_lifecycle_store_entries),
    }


def derive_boundary_summary(blockers: list[dict[str, str]] | None = None) -> dict[str, Any]:
    return {
        "derived_only": True,
        "in_memory": True,
        "history_store_created": Path("core/execution_history_store.py").exists(),
        "attempt_history_store_created": Path("core/attempt_history.py").exists() or Path("core/execution_attempt_history.py").exists(),
        "execution_result_store_created": Path("core/execution_result_store.py").exists(),
        "execution_attempt_id_operational": Path("core/execution_attempt_id.py").exists(),
        "jsonl_history_created": False,
        "execution_enabled": False,
        "scheduler_worker_enabled": False,
        "payloads_allowed": False,
        "mutation_allowed": False,
        "blocked": bool(blockers),
    }


def derive_risk_summary() -> dict[str, Any]:
    return {
        "scope": "execution_history_view_derived_only",
        "store_creation_allowed": False,
        "jsonl_history_allowed": False,
        "real_outputs_allowed": False,
        "execution_allowed": False,
        "mutation_allowed": False,
    }


def build_store_prohibition_policy() -> dict[str, Any]:
    return {flag: False for flag in STORE_FLAGS}


def build_attempt_id_policy(attempt_ref: str | None = None) -> dict[str, Any]:
    return {
        "attempt_ref": attempt_ref,
        "execution_attempt_id_enabled": False,
        "attempt_id_generation_enabled": False,
        "attempt_id_persistence_enabled": False,
        "materialized_attempt_id": False,
        "attempt_ref_is_operational_id": False,
    }


def build_execution_boundary_policy() -> dict[str, Any]:
    return {flag: False for flag in EXECUTION_FLAGS}


def build_payload_boundary_policy() -> dict[str, Any]:
    return {"forbidden_fields": sorted(FORBIDDEN_PAYLOAD_FIELDS), "deep_scan_required": True, "real_payloads_allowed": False}


def build_operation_result(
    *,
    status: str,
    verdict: str,
    operation: str,
    view: dict[str, Any],
    blockers: list[dict[str, str]],
    warnings: list[Any],
) -> dict[str, Any]:
    return ExecutionHistoryViewOperationResult(
        status=status,
        verdict=verdict,
        operation=operation,
        mode=MODE,
        history_mode=HISTORY_MODE,
        view_mode=VIEW_MODE,
        view_id=view.get("view_id"),
        target_ref=_copy_dict(view.get("target_ref")),
        attempt_ref=view.get("attempt_ref"),
        correlation_id=view.get("correlation_id"),
        idempotency_key=view.get("idempotency_key"),
        timeline_summary=build_timeline_summary(view.get("timeline") or []),
        dependency_summary=build_dependency_summary(view, blockers),
        store_prohibition_summary=build_store_prohibition_summary(build_store_prohibition_policy()),
        attempt_id_summary=build_attempt_id_summary(build_attempt_id_policy(view.get("attempt_ref"))),
        execution_boundary_summary=build_execution_boundary_summary(build_execution_boundary_policy()),
        payload_boundary_summary=build_payload_boundary_summary(build_payload_boundary_policy()),
        audit_summary=build_audit_summary(view.get("audit_refs")),
        observability_summary=build_observability_summary(view.get("observability_refs"), view.get("correlation_id")),
        boundary_summary=derive_boundary_summary(blockers),
        readiness_summary=build_readiness_summary(blockers),
        warnings=warnings,
        blockers=blockers,
        evidence=view.get("evidence") or [],
    ).to_dict()


def build_timeline_summary(timeline: list[dict[str, Any]]) -> dict[str, Any]:
    return {"event_count": len(timeline), "events": [item.get("event") for item in timeline], "derived_only": True}


def build_dependency_summary(view: dict[str, Any], blockers: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "dry_run_store_verified": view.get("dry_run_store_verified") is True,
        "execution_attempt_store_verified": view.get("execution_attempt_store_verified") is True,
        "execution_lifecycle_store_verified": view.get("execution_lifecycle_store_verified") is True,
        "execution_history_view_contract_passed": view.get("execution_history_view_contract_verdict") == PASSED_CONTRACT_VERDICT,
        "required_refs_present": not any(blocker["code"].startswith("missing_") for blocker in blockers),
        "cross_refs_valid": not any("mismatch" in blocker["code"] for blocker in blockers),
    }


def build_store_prohibition_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {**policy, "store_creation_allowed": False, "jsonl_history_allowed": False, "writes_allowed": False}


def build_attempt_id_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {**policy, "execution_attempt_id_operational_allowed": False}


def build_execution_boundary_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return dict(policy)


def build_payload_boundary_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "deep_scan_required": policy.get("deep_scan_required") is True,
        "real_payloads_allowed": policy.get("real_payloads_allowed") is True,
        "forbidden_fields_count": len(policy.get("forbidden_fields") or []),
    }


def build_audit_summary(audit_refs: Any) -> dict[str, Any]:
    return {"audit_refs_present": bool(audit_refs), "writes_audit_events": False}


def build_observability_summary(observability_refs: Any, correlation_id: str | None) -> dict[str, Any]:
    return {"observability_refs_present": bool(observability_refs), "correlation_id": correlation_id, "writes_observability_events": False}


def build_readiness_summary(blockers: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "ready_for_derived_only_view": not blockers,
        "ready_for_history_store": False,
        "ready_for_result_history": False,
        "ready_for_real_execution": False,
    }


def build_evidence(dry_run_verified: bool, attempt_verified: bool, lifecycle_verified: bool, contract_verdict: str | None) -> list[dict[str, Any]]:
    return [
        {"name": "dry_run_store_verified", "passed": dry_run_verified is True},
        {"name": "execution_attempt_store_verified", "passed": attempt_verified is True},
        {"name": "execution_lifecycle_store_verified", "passed": lifecycle_verified is True},
        {"name": "execution_history_view_contract_passed", "passed": contract_verdict == PASSED_CONTRACT_VERDICT},
        {"name": "derived_only_in_memory", "passed": True},
    ]


def _validate_dependencies(
    *,
    blockers: list[dict[str, str]],
    dry_run_store_entries,
    dry_run_store_verified,
    execution_attempt_store_entries,
    execution_attempt_store_verified,
    execution_lifecycle_store_entries,
    execution_lifecycle_store_verified,
    execution_history_view_contract_ref,
    execution_history_view_contract_verdict,
    attempt_ref,
    target_ref,
    target_type,
    target_id,
    correlation_id,
    idempotency_key,
    audit_refs,
    observability_refs,
    capability_policy_ref,
    runtime_contract_ref,
    execution_contract_ref,
    runtime_executor_contract_ref,
    runtime_preparation_ref,
    execution_runner_contract_ref,
    dry_run_contract_ref,
) -> None:
    if not dry_run_store_entries:
        _block(blockers, "missing_dry_run_store_entries", "dry_run_store_entries requerido")
    if dry_run_store_verified is not True:
        _block(blockers, "dry_run_store_not_verified", "dry_run_store_verified=true requerido")
    if not execution_attempt_store_entries:
        _block(blockers, "missing_execution_attempt_store_entries", "execution_attempt_store_entries requerido")
    if execution_attempt_store_verified is not True:
        _block(blockers, "execution_attempt_store_not_verified", "execution_attempt_store_verified=true requerido")
    if not execution_lifecycle_store_entries:
        _block(blockers, "missing_execution_lifecycle_store_entries", "execution_lifecycle_store_entries requerido")
    if execution_lifecycle_store_verified is not True:
        _block(blockers, "execution_lifecycle_store_not_verified", "execution_lifecycle_store_verified=true requerido")
    if not execution_history_view_contract_ref:
        _block(blockers, "missing_execution_history_view_contract_ref", "execution_history_view_contract_ref requerido")
    if execution_history_view_contract_verdict != PASSED_CONTRACT_VERDICT:
        _block(blockers, "execution_history_view_contract_not_passed", "contract passed requerido")
    if not attempt_ref:
        _block(blockers, "missing_attempt_ref", "attempt_ref requerido")
    elif not str(attempt_ref).startswith("preflight:"):
        _block(blockers, "attempt_ref_invalid", "attempt_ref debe empezar con preflight:")
    if not target_ref or not target_type or not target_id:
        _block(blockers, "missing_target_ref", "target_ref requerido")
    if not correlation_id:
        _block(blockers, "missing_correlation_id", "correlation_id requerido")
    if not idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")
    for name, value in {
        "audit_refs": audit_refs,
        "observability_refs": observability_refs,
        "capability_policy_ref": capability_policy_ref,
        "runtime_contract_ref": runtime_contract_ref,
        "execution_contract_ref": execution_contract_ref,
        "runtime_executor_contract_ref": runtime_executor_contract_ref,
        "runtime_preparation_ref": runtime_preparation_ref,
        "execution_runner_contract_ref": execution_runner_contract_ref,
        "dry_run_contract_ref": dry_run_contract_ref,
    }.items():
        if value in (None, "", {}, []):
            _block(blockers, f"missing_{name}", f"{name} requerido")


def _validate_forbidden_files(blockers: list[dict[str, str]]) -> None:
    for relative, code in FORBIDDEN_FILES.items():
        if Path(relative).exists():
            _block(blockers, code, f"{relative} no debe existir")


def _validate_cross_refs(*, refs, target_type, target_id, attempt_ref, correlation_id, idempotency_key, dry_run_id, blockers) -> None:
    for name, ref in refs:
        if not isinstance(ref, dict) or not ref:
            continue
        if ref.get("target_type") and target_type and ref.get("target_type") != target_type:
            _block(blockers, "target_type_mismatch", f"{name} target_type mismatch")
        if ref.get("target_id") and target_id and ref.get("target_id") != target_id:
            _block(blockers, "target_id_mismatch", f"{name} target_id mismatch")
        if ref.get("attempt_ref") and attempt_ref and ref.get("attempt_ref") != attempt_ref:
            _block(blockers, "attempt_ref_mismatch", f"{name} attempt_ref mismatch")
        if ref.get("correlation_id") and correlation_id and ref.get("correlation_id") != correlation_id:
            _block(blockers, "correlation_id_mismatch", f"{name} correlation_id mismatch")
        if ref.get("idempotency_key") and idempotency_key and ref.get("idempotency_key") != idempotency_key:
            _block(blockers, "idempotency_key_mismatch", f"{name} idempotency_key mismatch")
        if ref.get("dry_run_id") and dry_run_id and ref.get("dry_run_id") != dry_run_id:
            _block(blockers, "store_ref_mismatch", f"{name} dry_run_id mismatch")
        if name.endswith("contract_ref") and ref.get("status") == "failed":
            _block(blockers, "contract_ref_mismatch", f"{name} failed")


def _validate_timeline(timeline: list[dict[str, Any]], blockers: list[dict[str, str]]) -> None:
    for item in timeline:
        event = item.get("event")
        state = item.get("state")
        if event in BLOCKED_TIMELINE_EVENTS or event not in ALLOWED_TIMELINE_EVENTS:
            _block(blockers, "timeline_event_not_allowed", f"timeline event no permitido: {event}")
        if state in BLOCKED_VIEW_STATES:
            _block(blockers, f"{state}_state_not_allowed", f"{state} no permitido en history view")
        elif state and state not in ALLOWED_VIEW_STATES:
            _block(blockers, "invalid_view_state", f"estado no permitido: {state}")


def _validate_store_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for flag, code in STORE_FLAGS.items():
        if policy.get(flag) is True:
            _block(blockers, code, f"{flag} debe ser false")
    _scan_forbidden_store_refs(policy, blockers)


def _validate_attempt_id_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("execution_attempt_id") not in (None, "", {}, []):
        _block(blockers, "execution_attempt_id_not_allowed", "execution_attempt_id prohibido")
    if policy.get("attempt_id") not in (None, "", {}, []):
        _block(blockers, "attempt_id_not_allowed", "attempt_id prohibido")
    for flag, code in ATTEMPT_ID_FLAGS.items():
        if policy.get(flag) is True:
            _block(blockers, code, f"{flag} debe ser false")


def _validate_execution_boundary_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for flag, code in EXECUTION_FLAGS.items():
        if policy.get(flag) is True:
            _block(blockers, code, f"{flag} debe ser false")


def _validate_payload_boundary_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("real_payloads_allowed") is not False:
        _block(blockers, "execution_payload_not_allowed", "payloads reales prohibidos")
    forbidden = set(policy.get("forbidden_fields") or [])
    for field, code in FORBIDDEN_PAYLOAD_FIELDS.items():
        if field not in forbidden:
            _block(blockers, code, f"{field} debe estar prohibido")


def _scan_forbidden_payload(payload: Any, blockers: list[dict[str, str]]) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_PAYLOAD_FIELDS and value not in (None, "", {}, []):
                _block(blockers, FORBIDDEN_PAYLOAD_FIELDS[key], f"{key} no permitido")
            if key in {"execution_attempt_id", "attempt_id"} and value not in (None, "", {}, []):
                _block(blockers, f"{key}_not_allowed", f"{key} no permitido")
            _scan_forbidden_store_refs({key: value}, blockers)
            _scan_forbidden_payload(value, blockers)
    elif isinstance(payload, list):
        for item in payload:
            _scan_forbidden_payload(item, blockers)


def _scan_forbidden_store_refs(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for key, value in payload.items():
        if key in FORBIDDEN_STORE_REFS and value not in (None, "", {}, []):
            _block(blockers, FORBIDDEN_STORE_REFS[key], f"{key} no permitido")


def _verdict(blockers: list[dict[str, str]]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if not codes:
        return VALIDATED_VERDICT
    if "execution_history_view_contract_not_passed" in codes:
        return CONTRACT_NOT_PASSED_VERDICT
    if any("store" in code or "jsonl" in code or "write" in code or "append" in code or "path" in code or "result_persistence" in code for code in codes):
        return STORE_LEAK_VERDICT
    if any("attempt_id" in code or "operational_id" in code or code in {"execution_attempt_id_not_allowed", "attempt_id_not_allowed"} for code in codes):
        return ATTEMPT_ID_LEAK_VERDICT
    if any("state_not_allowed" in code or code == "invalid_view_state" for code in codes):
        return STATE_LEAK_VERDICT
    if any("timeline_event" in code for code in codes):
        return TIMELINE_LEAK_VERDICT
    if any(prefix in code for code in codes for prefix in ["execution_payload", "execution_result", "execution_output", "agent_output", "team_output", "model_", "tool_", "memory_", "secret_value", "credential_value"]):
        return PAYLOAD_LEAK_VERDICT
    if any(code in {"execution_enabled_not_allowed", "agent_execution_enabled_not_allowed", "team_execution_enabled_not_allowed", "queued_running_enabled_not_allowed", "completed_state_enabled_not_allowed", "rollback_operational_enabled_not_allowed", "retry_operational_enabled_not_allowed", "cancel_operational_enabled_not_allowed"} for code in codes):
        return EXECUTION_BOUNDARY_VERDICT
    if any("scheduler" in code or "worker" in code for code in codes):
        return SCHEDULER_WORKER_BOUNDARY_VERDICT
    if any("external" in code for code in codes):
        return EXTERNAL_BOUNDARY_VERDICT
    if any("mutation" in code or "database_write" in code for code in codes):
        return MUTATION_BOUNDARY_VERDICT
    return BLOCKED_VERDICT


def _contract_ref(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "contract_id": payload.get("contract_id") or payload.get("preparation_id") or payload.get("view_id"),
        "status": payload.get("status") or payload.get("contract_result"),
        "verdict": payload.get("verdict"),
        "target_type": (payload.get("target_ref") or {}).get("target_type") or payload.get("target_type"),
        "target_id": (payload.get("target_ref") or {}).get("target_id") or payload.get("target_id"),
        "attempt_ref": payload.get("attempt_ref"),
        "correlation_id": payload.get("correlation_id"),
        "idempotency_key": payload.get("idempotency_key"),
    }


def _entry_state(entry: dict[str, Any], fallback: str) -> str:
    return entry.get("state") or entry.get("status") or entry.get("to_state") or fallback


def _first_dict(items: list[dict[str, Any]]) -> dict[str, Any]:
    return _copy_dict(items[0]) if items else {}


def _copy_dict(value: Any) -> dict[str, Any]:
    return deepcopy(value) if isinstance(value, dict) else {}


def _list_copy(value: Any) -> list[dict[str, Any]]:
    return deepcopy(value) if isinstance(value, list) else []


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers[:] = [*blockers, blocker]
