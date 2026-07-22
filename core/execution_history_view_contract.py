"""Contrato declarativo de execution_history_view derived-only preflight-only.

No crea execution_history_store, attempt_history store, execution_result_store,
execution_attempt_id operativo, JSONL propio ni ejecucion real. Solo valida una
vista historica derivada desde stores primarios verified.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.execution_history_view_schema import (
    ExecutionHistoryViewBoundaryPolicy,
    ExecutionHistoryViewPayloadPolicy,
    ExecutionHistoryViewReadiness,
    ExecutionHistoryViewReferencePolicy,
    ExecutionHistoryViewTimelinePolicy,
    build_execution_history_view_contract_report,
)


CONTRACT_MODE = "execution_history_view_contract_only"
HISTORY_MODE = "derived_only"
VIEW_MODE = "preflight_only"
PASSED_VERDICT = "EXECUTION_HISTORY_VIEW_CONTRACT_PASSED"
BLOCKED_VERDICT = "EXECUTION_HISTORY_VIEW_CONTRACT_BLOCKED"
FAILED_VERDICT = "EXECUTION_HISTORY_VIEW_CONTRACT_FAILED"
STORE_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_STORE_LEAK"
ATTEMPT_ID_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_ATTEMPT_ID_LEAK"
STATE_LEAK_VERDICT = "EXECUTION_HISTORY_VIEW_STATE_LEAK"
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
    "history_view_contract_validated",
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
}
FORBIDDEN_STORE_REFS = {
    "execution_history_store_ref": "execution_history_store_ref_not_allowed",
    "attempt_history_store_ref": "attempt_history_store_ref_not_allowed",
    "execution_result_store_ref": "execution_result_store_ref_not_allowed",
    "history_store_path": "history_store_path_not_allowed",
    "execution_history_jsonl_path": "execution_history_jsonl_path_not_allowed",
    "result_store_path": "result_store_path_not_allowed",
}
ATTEMPT_ID_FLAGS = {
    "execution_attempt_id_enabled": "execution_attempt_id_enabled_not_allowed",
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
REQUIRED_REFS = {
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
}


def validate_execution_history_view_contract(
    *,
    dry_run_ref: dict[str, Any] | None,
    dry_run_store_ref: dict[str, Any] | None,
    dry_run_store_verification: dict[str, Any] | None,
    dry_run_store_contract_ref: dict[str, Any] | None,
    execution_attempt_store_ref: dict[str, Any] | None,
    execution_attempt_store_verification: dict[str, Any] | None,
    execution_attempt_store_contract_ref: dict[str, Any] | None,
    execution_lifecycle_store_ref: dict[str, Any] | None,
    execution_lifecycle_store_verification: dict[str, Any] | None,
    execution_lifecycle_contract_ref: dict[str, Any] | None,
    runtime_contract_ref: dict[str, Any] | None,
    execution_contract_ref: dict[str, Any] | None,
    runtime_executor_contract_ref: dict[str, Any] | None,
    runtime_preparation_ref: dict[str, Any] | None,
    execution_runner_contract_ref: dict[str, Any] | None,
    dry_run_contract_ref: dict[str, Any] | None,
    audit_refs: dict[str, Any] | None,
    observability_refs: dict[str, Any] | None,
    capability_policy_ref: dict[str, Any] | None,
    target_ref: dict[str, Any] | None = None,
    attempt_ref: str | None = None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    mode: str = CONTRACT_MODE,
    history_mode: str = HISTORY_MODE,
    view_mode: str = VIEW_MODE,
    reference_policy: dict[str, Any] | None = None,
    timeline_policy: dict[str, Any] | None = None,
    store_prohibition_policy: dict[str, Any] | None = None,
    attempt_id_policy: dict[str, Any] | None = None,
    execution_boundary_policy: dict[str, Any] | None = None,
    payload_boundary_policy: dict[str, Any] | None = None,
    readiness_policy: dict[str, Any] | None = None,
    timeline: list[dict[str, Any]] | None = None,
    summary: dict[str, Any] | None = None,
    preflight_status: dict[str, Any] | None = None,
    transition_history: dict[str, Any] | None = None,
    store_verification_summary: dict[str, Any] | None = None,
    risk_summary: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    dry_run = dict(dry_run_ref or {})
    attempt_store = dict(execution_attempt_store_ref or {})
    lifecycle_store = dict(execution_lifecycle_store_ref or {})
    resolved_target_ref = dict(target_ref if target_ref is not None else attempt_store.get("target_ref") or dry_run.get("target_ref") or {})
    target_type = resolved_target_ref.get("target_type") or attempt_store.get("target_type") or dry_run.get("target_type") or "target"
    target_id = resolved_target_ref.get("target_id") or attempt_store.get("target_id") or dry_run.get("target_id") or "target"
    resolved_attempt_ref = attempt_ref if attempt_ref is not None else attempt_store.get("attempt_ref") or lifecycle_store.get("attempt_ref")
    resolved_correlation_id = correlation_id if correlation_id is not None else attempt_store.get("correlation_id") or lifecycle_store.get("correlation_id") or dry_run.get("correlation_id")
    resolved_idempotency_key = idempotency_key if idempotency_key is not None else attempt_store.get("idempotency_key") or lifecycle_store.get("idempotency_key") or dry_run.get("idempotency_key")

    _validate_forbidden_files(blockers)
    if mode != CONTRACT_MODE:
        _block(blockers, "invalid_mode", "mode debe ser execution_history_view_contract_only")
    if history_mode != HISTORY_MODE:
        _block(blockers, "invalid_history_mode", "history_mode debe ser derived_only")
    if view_mode != VIEW_MODE:
        _block(blockers, "invalid_view_mode", "view_mode debe ser preflight_only")

    references = build_reference_policy() if reference_policy is None else reference_policy
    timeline_rules = build_timeline_policy() if timeline_policy is None else timeline_policy
    store_policy = build_store_prohibition_policy() if store_prohibition_policy is None else store_prohibition_policy
    attempt_policy = build_attempt_id_policy(resolved_attempt_ref) if attempt_id_policy is None else attempt_id_policy
    execution_boundary = build_execution_boundary_policy() if execution_boundary_policy is None else execution_boundary_policy
    payload_boundary = build_payload_boundary_policy() if payload_boundary_policy is None else payload_boundary_policy
    readiness = build_readiness_policy() if readiness_policy is None else readiness_policy
    resolved_timeline = timeline if timeline is not None else build_default_timeline()
    resolved_summary = summary if summary is not None else build_summary(target_type, target_id)
    resolved_preflight_status = preflight_status if preflight_status is not None else build_preflight_status()
    resolved_transition_history = transition_history if transition_history is not None else build_transition_history(lifecycle_store)
    resolved_store_summary = store_verification_summary if store_verification_summary is not None else build_store_verification_summary(
        dry_run_store_verification,
        execution_attempt_store_verification,
        execution_lifecycle_store_verification,
    )
    resolved_risk_summary = risk_summary if risk_summary is not None else build_risk_summary()
    resolved_evidence = evidence if evidence is not None else build_evidence(dry_run_store_verification, execution_attempt_store_verification, execution_lifecycle_store_verification)

    _validate_required_refs(
        refs={
            "dry_run_ref": dry_run,
            "dry_run_store_ref": dry_run_store_ref,
            "dry_run_store_contract_ref": dry_run_store_contract_ref,
            "execution_attempt_store_ref": attempt_store,
            "execution_attempt_store_contract_ref": execution_attempt_store_contract_ref,
            "execution_lifecycle_store_ref": lifecycle_store,
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
        },
        blockers=blockers,
    )
    _validate_verified_refs(dry_run_store_verification, execution_attempt_store_verification, execution_lifecycle_store_verification, blockers)
    _validate_attempt_ref(resolved_attempt_ref, blockers)
    if not resolved_target_ref:
        _block(blockers, "missing_target_ref", "target_ref requerido")
    if not resolved_correlation_id:
        _block(blockers, "missing_correlation_id", "correlation_id requerido")
    if not resolved_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")
    _validate_cross_refs(
        refs=[
            ("target_ref", resolved_target_ref),
            ("dry_run_ref", dry_run),
            ("dry_run_store_ref", dry_run_store_ref),
            ("dry_run_store_contract_ref", dry_run_store_contract_ref),
            ("execution_attempt_store_ref", attempt_store),
            ("execution_attempt_store_contract_ref", execution_attempt_store_contract_ref),
            ("execution_lifecycle_store_ref", lifecycle_store),
            ("execution_lifecycle_contract_ref", execution_lifecycle_contract_ref),
            ("runtime_contract_ref", runtime_contract_ref),
            ("execution_contract_ref", execution_contract_ref),
            ("runtime_executor_contract_ref", runtime_executor_contract_ref),
            ("runtime_preparation_ref", runtime_preparation_ref),
            ("execution_runner_contract_ref", execution_runner_contract_ref),
            ("dry_run_contract_ref", dry_run_contract_ref),
        ],
        target_type=target_type,
        target_id=target_id,
        attempt_ref=resolved_attempt_ref,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        dry_run_id=dry_run.get("dry_run_id"),
        blockers=blockers,
    )
    _validate_timeline_policy(timeline_rules, blockers)
    _validate_timeline(resolved_timeline, blockers)
    _validate_view_payloads([resolved_summary, resolved_preflight_status, resolved_transition_history, resolved_store_summary, resolved_risk_summary, {"evidence": resolved_evidence}, payload or {}], blockers)
    _validate_store_policy(store_policy, blockers)
    _validate_attempt_id_policy(attempt_policy, blockers)
    _validate_execution_boundary_policy(execution_boundary, blockers)
    _validate_payload_boundary_policy(payload_boundary, blockers)
    _scan_forbidden_payload(payload or {}, blockers)

    status = "passed" if not blockers else "blocked"
    verdict = _verdict(blockers)
    return build_execution_history_view_contract_report(
        contract_id=f"execution_history_view_contract_{target_type}_{target_id}",
        status=status,
        verdict=verdict,
        mode=CONTRACT_MODE if mode != CONTRACT_MODE else mode,
        history_mode=HISTORY_MODE if history_mode != HISTORY_MODE else history_mode,
        view_mode=VIEW_MODE if view_mode != VIEW_MODE else view_mode,
        target_ref=resolved_target_ref,
        target_type=target_type,
        target_id=target_id,
        attempt_ref=resolved_attempt_ref,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        dry_run_ref=dry_run,
        dry_run_store_ref=dry_run_store_ref or {},
        dry_run_store_verified=(dry_run_store_verification or {}).get("status") == "verified",
        dry_run_store_contract_ref=_contract_ref(dry_run_store_contract_ref),
        execution_attempt_store_ref=attempt_store,
        execution_attempt_store_verified=(execution_attempt_store_verification or {}).get("status") == "verified",
        execution_attempt_store_contract_ref=_contract_ref(execution_attempt_store_contract_ref),
        execution_lifecycle_store_ref=lifecycle_store,
        execution_lifecycle_store_verified=(execution_lifecycle_store_verification or {}).get("status") == "verified",
        execution_lifecycle_contract_ref=_contract_ref(execution_lifecycle_contract_ref),
        runtime_contract_ref=_contract_ref(runtime_contract_ref),
        execution_contract_ref=_contract_ref(execution_contract_ref),
        runtime_executor_contract_ref=_contract_ref(runtime_executor_contract_ref),
        runtime_preparation_ref=_contract_ref(runtime_preparation_ref),
        execution_runner_contract_ref=_contract_ref(execution_runner_contract_ref),
        dry_run_contract_ref=_contract_ref(dry_run_contract_ref),
        audit_refs=audit_refs or {},
        observability_refs=observability_refs or {},
        capability_policy_ref=capability_policy_ref or {},
        reference_policy=references,
        timeline_policy=timeline_rules,
        store_prohibition_policy=store_policy,
        attempt_id_policy=attempt_policy,
        execution_boundary_policy=execution_boundary,
        payload_boundary_policy=payload_boundary,
        readiness_policy=readiness,
        timeline=resolved_timeline,
        summary=resolved_summary,
        preflight_status=resolved_preflight_status,
        transition_history=resolved_transition_history,
        store_verification_summary=resolved_store_summary,
        timeline_summary=build_timeline_summary(resolved_timeline),
        dependency_summary=build_dependency_summary(blockers, dry_run_store_verification, execution_attempt_store_verification, execution_lifecycle_store_verification),
        store_prohibition_summary=build_store_prohibition_summary(store_policy),
        attempt_id_summary=build_attempt_id_summary(attempt_policy),
        execution_boundary_summary=build_execution_boundary_summary(execution_boundary),
        payload_boundary_summary=build_payload_boundary_summary(payload_boundary),
        audit_summary=build_audit_summary(audit_refs),
        observability_summary=build_observability_summary(observability_refs, resolved_correlation_id),
        boundary_summary=build_boundary_summary(blockers),
        readiness_summary=build_readiness_summary(blockers),
        risk_summary=resolved_risk_summary,
        warnings=warnings,
        blockers=blockers,
        evidence=resolved_evidence,
    )


def build_reference_policy() -> dict[str, Any]:
    return ExecutionHistoryViewReferencePolicy(required_refs=sorted(REQUIRED_REFS)).to_dict()


def build_timeline_policy() -> dict[str, Any]:
    return ExecutionHistoryViewTimelinePolicy(
        allowed_events=sorted(ALLOWED_TIMELINE_EVENTS),
        allowed_states=sorted(ALLOWED_VIEW_STATES),
        blocked_states=sorted(BLOCKED_VIEW_STATES),
    ).to_dict()


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
        "attempt_id_generation": "disabled",
        "attempt_id_persistence": "disabled",
    }


def build_execution_boundary_policy() -> dict[str, Any]:
    return ExecutionHistoryViewBoundaryPolicy().to_dict()


def build_payload_boundary_policy() -> dict[str, Any]:
    return ExecutionHistoryViewPayloadPolicy(forbidden_fields=sorted(FORBIDDEN_PAYLOAD_FIELDS)).to_dict()


def build_readiness_policy() -> dict[str, Any]:
    return ExecutionHistoryViewReadiness(ready_for_contract_only=True, ready_for_derived_view_contract=True).to_dict()


def build_default_timeline() -> list[dict[str, Any]]:
    return [{"event": event, "state": "verified" if event.endswith("_verified") else "created"} for event in sorted(ALLOWED_TIMELINE_EVENTS)]


def build_summary(target_type: str, target_id: str) -> dict[str, Any]:
    return {"target_type": target_type, "target_id": target_id, "view": "derived_preflight_history"}


def build_preflight_status() -> dict[str, Any]:
    return {"status": "preflight_passed", "execution_enabled": False}


def build_transition_history(lifecycle_store_ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "execution_lifecycle_store",
        "entry_count": lifecycle_store_ref.get("entry_count"),
        "allowed_states": sorted(ALLOWED_VIEW_STATES),
    }


def build_store_verification_summary(dry_run, attempt, lifecycle) -> dict[str, Any]:
    return {
        "dry_run_store_verified": (dry_run or {}).get("status") == "verified",
        "execution_attempt_store_verified": (attempt or {}).get("status") == "verified",
        "execution_lifecycle_store_verified": (lifecycle or {}).get("status") == "verified",
    }


def build_risk_summary() -> dict[str, Any]:
    return {"scope": "history_view_derived_only", "store_creation_allowed": False, "real_outputs_allowed": False}


def build_evidence(dry_run, attempt, lifecycle) -> list[dict[str, Any]]:
    return [
        {"name": "dry_run_store_verified", "passed": (dry_run or {}).get("status") == "verified"},
        {"name": "execution_attempt_store_verified", "passed": (attempt or {}).get("status") == "verified"},
        {"name": "execution_lifecycle_store_verified", "passed": (lifecycle or {}).get("status") == "verified"},
        {"name": "derived_only_contract", "passed": True},
    ]


def _validate_forbidden_files(blockers: list[dict[str, str]]) -> None:
    forbidden = {
        "core/execution_history_store.py": "execution_history_store_not_allowed",
        "core/attempt_history.py": "attempt_history_store_not_allowed",
        "core/execution_attempt_history.py": "execution_attempt_history_store_not_allowed",
        "core/execution_result_store.py": "execution_result_store_not_allowed",
        "core/execution_attempt_id.py": "execution_attempt_id_not_allowed",
        "core/scheduler_queue.py": "scheduler_worker_queue_not_allowed",
        "core/worker_queue.py": "scheduler_worker_queue_not_allowed",
    }
    for relative, code in forbidden.items():
        if Path(relative).exists():
            _block(blockers, code, f"{relative} no debe existir")


def _validate_required_refs(refs: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field_name, value in refs.items():
        if value in (None, "", {}, []):
            _block(blockers, f"missing_{field_name}", f"{field_name} requerido")


def _validate_verified_refs(dry_run, attempt, lifecycle, blockers) -> None:
    if (dry_run or {}).get("status") != "verified":
        _block(blockers, "dry_run_store_not_verified", "dry_run_store_verified=true requerido")
    if (attempt or {}).get("status") != "verified":
        _block(blockers, "execution_attempt_store_not_verified", "execution_attempt_store_verified=true requerido")
    if (lifecycle or {}).get("status") != "verified":
        _block(blockers, "execution_lifecycle_store_not_verified", "execution_lifecycle_store_verified=true requerido")


def _validate_attempt_ref(attempt_ref: str | None, blockers: list[dict[str, str]]) -> None:
    if not attempt_ref:
        _block(blockers, "missing_attempt_ref", "attempt_ref requerido")
        return
    if not str(attempt_ref).startswith("preflight:"):
        _block(blockers, "attempt_ref_invalid", "attempt_ref debe empezar con preflight:")


def _validate_cross_refs(*, refs, target_type, target_id, attempt_ref, correlation_id, idempotency_key, dry_run_id, blockers) -> None:
    for name, ref in refs:
        if not isinstance(ref, dict) or not ref:
            continue
        if ref.get("target_type") and ref.get("target_type") != target_type:
            _block(blockers, "target_type_mismatch", f"{name} target_type mismatch")
        if ref.get("target_id") and ref.get("target_id") != target_id:
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


def _validate_timeline_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("allows_operational_events") is not False:
        _block(blockers, "operational_timeline_events_not_allowed", "operational timeline events forbidden")
    if policy.get("writes_history") is not False:
        _block(blockers, "history_write_not_allowed", "history view no escribe history")
    if not ALLOWED_TIMELINE_EVENTS <= set(policy.get("allowed_events") or []):
        _block(blockers, "missing_allowed_timeline_event", "timeline policy incompleta")
    if not BLOCKED_VIEW_STATES <= set(policy.get("blocked_states") or []):
        _block(blockers, "missing_blocked_state", "blocked states incompletos")


def _validate_timeline(timeline: list[dict[str, Any]], blockers: list[dict[str, str]]) -> None:
    for item in timeline:
        event = item.get("event")
        state = item.get("state")
        if event not in ALLOWED_TIMELINE_EVENTS:
            _block(blockers, "timeline_event_not_allowed", f"timeline event no permitido: {event}")
        if state in BLOCKED_VIEW_STATES:
            _block(blockers, f"{state}_state_not_allowed", f"{state} no permitido en history view")
        elif state and state not in ALLOWED_VIEW_STATES:
            _block(blockers, "invalid_view_state", f"estado no permitido: {state}")


def _validate_view_payloads(items: list[Any], blockers: list[dict[str, str]]) -> None:
    for item in items:
        _scan_forbidden_payload(item, blockers)


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
        return PASSED_VERDICT
    if any("store" in code or "jsonl" in code or "history_write" in code or "result_persistence" in code for code in codes):
        return STORE_LEAK_VERDICT
    if any("attempt_id" in code or "operational_id" in code or code in {"execution_attempt_id_not_allowed", "attempt_id_not_allowed"} for code in codes):
        return ATTEMPT_ID_LEAK_VERDICT
    if any("state_not_allowed" in code or code in {"invalid_view_state", "operational_timeline_events_not_allowed"} for code in codes):
        return STATE_LEAK_VERDICT
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


def build_timeline_summary(timeline: list[dict[str, Any]]) -> dict[str, Any]:
    return {"event_count": len(timeline), "events": [item.get("event") for item in timeline], "derived_only": True}


def build_dependency_summary(blockers, dry_run, attempt, lifecycle) -> dict[str, Any]:
    return {
        "dry_run_store_verified": (dry_run or {}).get("status") == "verified",
        "execution_attempt_store_verified": (attempt or {}).get("status") == "verified",
        "execution_lifecycle_store_verified": (lifecycle or {}).get("status") == "verified",
        "required_refs_present": not any(blocker["code"].startswith("missing_") for blocker in blockers),
        "cross_refs_valid": not any("mismatch" in blocker["code"] for blocker in blockers),
    }


def build_store_prohibition_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {**policy, "store_creation_allowed": False, "jsonl_history_allowed": False}


def build_attempt_id_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {**policy, "execution_attempt_id_operational_allowed": False}


def build_execution_boundary_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return dict(policy)


def build_payload_boundary_summary(policy: dict[str, Any]) -> dict[str, Any]:
    return {"deep_scan_required": policy.get("deep_scan_required") is True, "real_payloads_allowed": policy.get("real_payloads_allowed") is True, "forbidden_fields_count": len(policy.get("forbidden_fields") or [])}


def build_audit_summary(audit_refs) -> dict[str, Any]:
    return {"audit_refs_present": bool(audit_refs), "writes_audit_events": False}


def build_observability_summary(observability_refs, correlation_id) -> dict[str, Any]:
    return {"observability_refs_present": bool(observability_refs), "correlation_id": correlation_id, "writes_observability_events": False}


def build_boundary_summary(blockers) -> dict[str, Any]:
    return {
        "derived_only": True,
        "history_store_created": Path("core/execution_history_store.py").exists(),
        "attempt_history_store_created": Path("core/attempt_history.py").exists() or Path("core/execution_attempt_history.py").exists(),
        "execution_result_store_created": Path("core/execution_result_store.py").exists(),
        "execution_attempt_id_operational": Path("core/execution_attempt_id.py").exists(),
        "execution_enabled": False,
        "payloads_allowed": False,
        "mutation_allowed": False,
        "blocked": bool(blockers),
    }


def build_readiness_summary(blockers) -> dict[str, Any]:
    return {
        "ready_for_contract_only": not blockers,
        "ready_for_derived_view_contract": not blockers,
        "ready_for_history_store": False,
        "ready_for_result_history": False,
        "ready_for_real_execution": False,
    }


def _contract_ref(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "contract_id": payload.get("contract_id") or payload.get("preparation_id"),
        "status": payload.get("status") or payload.get("contract_result"),
        "verdict": payload.get("verdict"),
        "target_type": (payload.get("target_ref") or {}).get("target_type") or payload.get("target_type"),
        "target_id": (payload.get("target_ref") or {}).get("target_id") or payload.get("target_id"),
        "attempt_ref": payload.get("attempt_ref"),
        "correlation_id": payload.get("correlation_id"),
        "idempotency_key": payload.get("idempotency_key"),
    }


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
