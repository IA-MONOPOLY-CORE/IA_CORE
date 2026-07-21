"""Contrato declarativo de execution lifecycle preflight-transitions-only.

No implementa lifecycle real, no crea execution_attempt_id operativo y no
habilita ejecucion. Solo valida estados y transiciones preflight por referencia.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.execution_lifecycle_schema import (
    ExecutionLifecycleBoundaryPolicy,
    ExecutionLifecycleEventPolicy,
    ExecutionLifecycleReadiness,
    ExecutionLifecycleReferencePolicy,
    ExecutionLifecycleStatePolicy,
    ExecutionLifecycleTransitionPolicy,
    build_execution_lifecycle_contract_report,
)


CONTRACT_MODE = "execution_lifecycle_contract_only"
LIFECYCLE_MODE = "preflight_transitions_only"
PASSED_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_PASSED"
BLOCKED_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_BLOCKED"
FAILED_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_FAILED"
ATTEMPT_ID_LEAK_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_ATTEMPT_ID_LEAK"
STATE_LEAK_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_STATE_LEAK"
TRANSITION_LEAK_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_TRANSITION_LEAK"
PAYLOAD_LEAK_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_PAYLOAD_LEAK"
EXECUTION_BOUNDARY_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_EXECUTION_BOUNDARY"
EXTERNAL_BOUNDARY_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_EXTERNAL_BOUNDARY"
SCHEDULER_WORKER_BOUNDARY_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_SCHEDULER_WORKER_BOUNDARY"
MUTATION_BOUNDARY_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_MUTATION_BOUNDARY"

ALLOWED_STATES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
    "noop_idempotent",
}
BLOCKED_STATES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back",
    "rolled_back_real",
    "aborted_real",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
ALLOWED_TRANSITIONS = {
    ("created", "preflight_passed"),
    ("created", "preflight_blocked"),
    ("created", "blocked"),
    ("created", "failed"),
    ("created", "not_applicable"),
    ("preflight_passed", "blocked"),
    ("preflight_blocked", "blocked"),
    ("blocked", "noop_idempotent"),
    ("failed", "noop_idempotent"),
    ("not_applicable", "noop_idempotent"),
}
BLOCKED_TRANSITIONS = {
    ("created", "queued"),
    ("preflight_passed", "queued"),
    ("queued", "running"),
    ("running", "completed"),
    ("running", "failed"),
    ("running", "cancelled"),
    ("running", "rolled_back"),
    ("completed", "rolled_back"),
    ("cancelled", "rolled_back"),
}
OPERATIONAL_TARGET_STATES = {
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
    "rollback_operational_enabled": "rollback_operational_enabled_not_allowed",
    "retry_operational_enabled": "retry_operational_enabled_not_allowed",
    "cancel_operational_enabled": "cancel_operational_enabled_not_allowed",
}
FORBIDDEN_PAYLOAD_FIELDS = {
    "execution_attempt_id": "execution_attempt_id_not_allowed",
    "attempt_id": "attempt_id_not_allowed",
    "execution_payload": "execution_payload_not_allowed",
    "execution_result": "execution_result_not_allowed",
    "execution_output": "execution_output_not_allowed",
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
ALLOWED_CONTRACT_EVENTS = {
    "execution_lifecycle_contract_started",
    "execution_lifecycle_contract_validated",
    "execution_lifecycle_contract_passed",
    "execution_lifecycle_contract_blocked",
    "execution_lifecycle_contract_failed",
    "execution_lifecycle_contract_boundary_verified",
    "execution_lifecycle_transition_validated",
    "execution_lifecycle_transition_blocked",
}
FORBIDDEN_CONTRACT_EVENTS = {
    "execution_lifecycle_created",
    "execution_started",
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
    "state_mutated",
    "artifact_mutated",
}
REQUIRED_REFS = {
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
}


def validate_execution_lifecycle_contract(
    *,
    execution_attempt_store_ref: dict[str, Any] | None,
    execution_attempt_store_verification: dict[str, Any] | None,
    execution_attempt_store_contract_result: dict[str, Any] | None,
    dry_run_ref: dict[str, Any] | None,
    dry_run_store_ref: dict[str, Any] | None,
    dry_run_store_verification_ref: dict[str, Any] | None,
    dry_run_store_contract_result: dict[str, Any] | None,
    runtime_contract_result: dict[str, Any] | None,
    execution_contract_result: dict[str, Any] | None,
    runtime_executor_contract_result: dict[str, Any] | None,
    runtime_preparation: dict[str, Any] | None,
    execution_runner_contract_result: dict[str, Any] | None,
    dry_run_contract_result: dict[str, Any] | None,
    audit_refs: dict[str, Any] | None,
    observability_refs: dict[str, Any] | None,
    capability_policy_ref: dict[str, Any] | None,
    target_ref: dict[str, Any] | None = None,
    attempt_ref: str | None = None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    source_state: str = "created",
    target_state: str = "preflight_passed",
    mode: str = CONTRACT_MODE,
    lifecycle_mode: str = LIFECYCLE_MODE,
    state_policy: dict[str, Any] | None = None,
    transition_policy: dict[str, Any] | None = None,
    attempt_id_policy: dict[str, Any] | None = None,
    execution_boundary_policy: dict[str, Any] | None = None,
    payload_boundary_policy: dict[str, Any] | None = None,
    scheduler_worker_policy: dict[str, Any] | None = None,
    model_tool_memory_policy: dict[str, Any] | None = None,
    external_access_policy: dict[str, Any] | None = None,
    readiness_policy: dict[str, Any] | None = None,
    events: list[str] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    attempt_store_ref = dict(execution_attempt_store_ref or {})
    attempt_store_contract = execution_attempt_store_contract_result or {}
    resolved_attempt_ref = attempt_ref if attempt_ref is not None else attempt_store_ref.get("attempt_ref") or attempt_store_contract.get("attempt_ref")
    resolved_target_ref = dict(target_ref or attempt_store_ref.get("target_ref") or attempt_store_contract.get("target_ref") or {})
    resolved_correlation_id = correlation_id if correlation_id is not None else attempt_store_ref.get("correlation_id") or attempt_store_contract.get("correlation_id") or (observability_refs or {}).get("correlation_id")
    resolved_idempotency_key = idempotency_key if idempotency_key is not None else attempt_store_ref.get("idempotency_key") or attempt_store_contract.get("idempotency_key")

    if Path("core/execution_lifecycle.py").exists():
        _block(blockers, "execution_lifecycle_implementation_not_allowed", "core/execution_lifecycle.py no debe existir")
    if Path("core/execution_attempt_lifecycle.py").exists():
        _block(blockers, "execution_attempt_lifecycle_not_allowed", "core/execution_attempt_lifecycle.py no debe existir")
    if Path("core/execution_attempt_id.py").exists():
        _block(blockers, "execution_attempt_id_operational_not_allowed", "execution_attempt_id operativo no debe existir")
    if Path("core/execution_history_store.py").exists():
        _block(blockers, "execution_history_store_not_allowed", "execution_history_store no debe existir")
    if Path("core/scheduler_queue.py").exists() or Path("core/worker_queue.py").exists():
        _block(blockers, "scheduler_worker_queue_not_allowed", "scheduler/worker queue no debe existir")
    if mode != CONTRACT_MODE:
        _block(blockers, "invalid_mode", "mode debe ser execution_lifecycle_contract_only")
    if lifecycle_mode != LIFECYCLE_MODE:
        _block(blockers, "invalid_lifecycle_mode", "lifecycle_mode debe ser preflight_transitions_only")

    states = build_state_policy(source_state=source_state, target_state=target_state) if state_policy is None else state_policy
    transitions = build_transition_policy(source_state=source_state, target_state=target_state) if transition_policy is None else transition_policy
    attempt_id = build_attempt_id_policy(resolved_attempt_ref) if attempt_id_policy is None else attempt_id_policy
    execution_boundary = build_execution_boundary_policy() if execution_boundary_policy is None else execution_boundary_policy
    payload_boundary = build_payload_boundary_policy() if payload_boundary_policy is None else payload_boundary_policy
    scheduler_worker = build_scheduler_worker_policy() if scheduler_worker_policy is None else scheduler_worker_policy
    model_tool_memory = build_model_tool_memory_policy() if model_tool_memory_policy is None else model_tool_memory_policy
    external_access = build_external_access_policy() if external_access_policy is None else external_access_policy
    readiness = build_readiness_policy() if readiness_policy is None else readiness_policy

    _validate_states(states, source_state, target_state, blockers)
    _validate_transition(transitions, source_state, target_state, blockers)
    _validate_attempt_id_policy(attempt_id, resolved_attempt_ref, blockers)
    _validate_execution_boundary_policy(execution_boundary, blockers)
    _validate_execution_boundary_policy(scheduler_worker, blockers)
    _validate_execution_boundary_policy(model_tool_memory, blockers)
    _validate_execution_boundary_policy(external_access, blockers)
    _validate_payload_boundary_policy(payload_boundary, blockers)
    _scan_forbidden_payload(payload or {}, blockers)
    _validate_required_refs(
        refs={
            "execution_attempt_store_ref": attempt_store_ref,
            "execution_attempt_store_verification_ref": execution_attempt_store_verification,
            "execution_attempt_store_contract_ref": attempt_store_contract,
            "dry_run_ref": dry_run_ref,
            "dry_run_store_ref": dry_run_store_ref,
            "dry_run_store_verification_ref": dry_run_store_verification_ref,
            "dry_run_store_contract_ref": dry_run_store_contract_result,
            "runtime_contract_ref": runtime_contract_result,
            "execution_contract_ref": execution_contract_result,
            "runtime_executor_contract_ref": runtime_executor_contract_result,
            "runtime_preparation_ref": runtime_preparation,
            "execution_runner_contract_ref": execution_runner_contract_result,
            "dry_run_contract_ref": dry_run_contract_result,
            "audit_refs": audit_refs,
            "observability_refs": observability_refs,
            "capability_policy_ref": capability_policy_ref,
        },
        blockers=blockers,
    )
    _validate_verified_refs(
        execution_attempt_store_verification=execution_attempt_store_verification,
        dry_run_store_verification_ref=dry_run_store_verification_ref,
        blockers=blockers,
    )
    _validate_cross_refs(
        refs=[
            ("target_ref", resolved_target_ref),
            ("execution_attempt_store_ref", attempt_store_ref),
            ("execution_attempt_store_contract_ref", attempt_store_contract),
            ("dry_run_ref", dry_run_ref),
            ("dry_run_store_ref", dry_run_store_ref),
            ("dry_run_store_contract_ref", dry_run_store_contract_result),
            ("runtime_contract_ref", runtime_contract_result),
            ("execution_contract_ref", execution_contract_result),
            ("runtime_executor_contract_ref", runtime_executor_contract_result),
            ("runtime_preparation_ref", runtime_preparation),
            ("execution_runner_contract_ref", execution_runner_contract_result),
            ("dry_run_contract_ref", dry_run_contract_result),
        ],
        target_ref=resolved_target_ref,
        attempt_ref=resolved_attempt_ref,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        dry_run_ref=dry_run_ref,
        blockers=blockers,
    )
    if not resolved_correlation_id:
        _block(blockers, "missing_correlation_id", "correlation_id requerido")
    if not resolved_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")
    _validate_events(events or sorted(ALLOWED_CONTRACT_EVENTS), blockers)

    status = "passed" if not blockers else "blocked"
    verdict = _verdict(blockers)
    return build_execution_lifecycle_contract_report(
        contract_id=f"execution_lifecycle_contract_{resolved_target_ref.get('target_type', 'target')}_{resolved_target_ref.get('target_id', 'target')}",
        status=status,
        verdict=verdict,
        mode=CONTRACT_MODE if mode != CONTRACT_MODE else mode,
        lifecycle_mode=LIFECYCLE_MODE if lifecycle_mode != LIFECYCLE_MODE else lifecycle_mode,
        target_ref=resolved_target_ref,
        attempt_ref=resolved_attempt_ref,
        execution_attempt_store_ref=attempt_store_ref,
        execution_attempt_store_verification_ref=execution_attempt_store_verification or {},
        execution_attempt_store_contract_ref=_contract_ref(attempt_store_contract),
        dry_run_ref=dry_run_ref or {},
        dry_run_store_ref=dry_run_store_ref or {},
        dry_run_store_verification_ref=dry_run_store_verification_ref or {},
        dry_run_store_contract_ref=_contract_ref(dry_run_store_contract_result),
        runtime_contract_ref=_contract_ref(runtime_contract_result),
        execution_contract_ref=_contract_ref(execution_contract_result),
        runtime_executor_contract_ref=_contract_ref(runtime_executor_contract_result),
        runtime_preparation_ref=_contract_ref(runtime_preparation),
        execution_runner_contract_ref=_contract_ref(execution_runner_contract_result),
        dry_run_contract_ref=_contract_ref(dry_run_contract_result),
        audit_refs=audit_refs or {},
        observability_refs=observability_refs or {},
        capability_policy_ref=capability_policy_ref or {},
        correlation_id=resolved_correlation_id or None,
        idempotency_key=resolved_idempotency_key or None,
        state_policy=states,
        transition_policy=transitions,
        attempt_id_policy=attempt_id,
        execution_boundary_policy=execution_boundary,
        payload_boundary_policy=payload_boundary,
        scheduler_worker_policy=scheduler_worker,
        model_tool_memory_policy=model_tool_memory,
        external_access_policy=external_access,
        readiness_policy=readiness,
        state_summary=build_state_summary(states, source_state, target_state),
        transition_summary=build_transition_summary(transitions, source_state, target_state),
        attempt_id_summary=build_attempt_id_summary(attempt_id),
        dependency_summary=build_dependency_summary(blockers, execution_attempt_store_verification, dry_run_store_verification_ref),
        execution_boundary_summary=build_execution_boundary_summary(execution_boundary),
        payload_boundary_summary=build_payload_boundary_summary(payload_boundary),
        scheduler_worker_summary=build_execution_boundary_summary(scheduler_worker),
        model_tool_memory_summary=build_execution_boundary_summary(model_tool_memory),
        external_access_summary=build_execution_boundary_summary(external_access),
        audit_summary=build_audit_summary(audit_refs, events or sorted(ALLOWED_CONTRACT_EVENTS)),
        observability_summary=build_observability_summary(observability_refs, resolved_correlation_id),
        boundary_summary=build_boundary_summary(blockers),
        readiness_summary=build_readiness_summary(blockers),
        risk_summary=build_risk_summary(),
        blockers=blockers,
        warnings=warnings,
        evidence=build_evidence(attempt_store_ref, execution_attempt_store_verification, dry_run_store_verification_ref),
    )


def build_state_policy(source_state: str = "created", target_state: str = "preflight_passed") -> dict[str, Any]:
    return ExecutionLifecycleStatePolicy(
        allowed_states=sorted(ALLOWED_STATES),
        blocked_states=sorted(BLOCKED_STATES),
        current_state=source_state,
        target_state=target_state,
    ).to_dict()


def build_transition_policy(source_state: str = "created", target_state: str = "preflight_passed") -> dict[str, Any]:
    return ExecutionLifecycleTransitionPolicy(
        allowed_transitions=[{"source": source, "target": target} for source, target in sorted(ALLOWED_TRANSITIONS)],
        blocked_transitions=[{"source": source, "target": target} for source, target in sorted(BLOCKED_TRANSITIONS)],
        source_state=source_state,
        target_state=target_state,
    ).to_dict()


def build_attempt_id_policy(attempt_ref: str | None = None) -> dict[str, Any]:
    return {
        "attempt_ref": attempt_ref,
        "attempt_ref_is_operational_id": False,
        "attempt_id_generation": "disabled",
        "attempt_id_persistence": "disabled",
        "materialized_attempt_id": False,
        "execution_attempt_id_operational_allowed": False,
    }


def build_execution_boundary_policy() -> dict[str, Any]:
    return ExecutionLifecycleBoundaryPolicy().to_dict()


def build_payload_boundary_policy() -> dict[str, Any]:
    return {"forbidden_fields": sorted(FORBIDDEN_PAYLOAD_FIELDS), "deep_scan_required": True, "real_payloads_allowed": False}


def build_scheduler_worker_policy() -> dict[str, Any]:
    return {"scheduler_enabled": False, "worker_queue_enabled": False}


def build_model_tool_memory_policy() -> dict[str, Any]:
    return {"model_invocation_enabled": False, "tool_execution_enabled": False, "memory_persistence_enabled": False}


def build_external_access_policy() -> dict[str, Any]:
    return {"external_access_enabled": False}


def build_readiness_policy() -> dict[str, Any]:
    return ExecutionLifecycleReadiness(ready_for_contract_only=True, ready_for_preflight_transitions_only=True).to_dict()


def build_reference_policy() -> dict[str, Any]:
    return ExecutionLifecycleReferencePolicy(required_refs=sorted(REQUIRED_REFS)).to_dict()


def build_event_policy() -> dict[str, Any]:
    return ExecutionLifecycleEventPolicy(
        allowed_events=sorted(ALLOWED_CONTRACT_EVENTS),
        forbidden_events=sorted(FORBIDDEN_CONTRACT_EVENTS),
    ).to_dict()


def _validate_states(policy: dict[str, Any], source_state: str, target_state: str, blockers: list[dict[str, str]]) -> None:
    allowed = set(policy.get("allowed_states") or [])
    blocked = set(policy.get("blocked_states") or [])
    if not ALLOWED_STATES <= allowed:
        _block(blockers, "missing_allowed_lifecycle_state", "state_policy debe declarar estados permitidos")
    if not BLOCKED_STATES <= blocked:
        _block(blockers, "missing_blocked_lifecycle_state", "state_policy debe declarar estados bloqueados")
    for state, role in [(source_state, "source"), (target_state, "target")]:
        if state in BLOCKED_STATES:
            _block(blockers, f"{state}_state_not_allowed", f"{role}_state operativo bloqueado")
        elif state not in ALLOWED_STATES:
            _block(blockers, "invalid_lifecycle_state", f"{role}_state no permitido")
    if policy.get("operational_states_allowed") is not False:
        _block(blockers, "operational_states_not_allowed", "operational_states_allowed debe ser false")


def _validate_transition(policy: dict[str, Any], source_state: str, target_state: str, blockers: list[dict[str, str]]) -> None:
    transition = (source_state, target_state)
    if target_state in OPERATIONAL_TARGET_STATES:
        _block(blockers, f"{target_state}_transition_not_allowed", f"transicion hacia {target_state} bloqueada")
    if transition in BLOCKED_TRANSITIONS:
        _block(blockers, f"{target_state}_transition_not_allowed", f"{source_state}->{target_state} bloqueada")
    if transition not in ALLOWED_TRANSITIONS:
        _block(blockers, "invalid_transition", "transicion no declarada para preflight")
    if policy.get("implicit_execution_allowed") is not False:
        _block(blockers, "implicit_execution_not_allowed", "implicit_execution_allowed debe ser false")
    if policy.get("implicit_scheduler_worker_allowed") is not False:
        _block(blockers, "implicit_scheduler_worker_not_allowed", "implicit scheduler/worker bloqueado")


def _validate_attempt_id_policy(policy: dict[str, Any], attempt_ref: str | None, blockers: list[dict[str, str]]) -> None:
    if not attempt_ref:
        _block(blockers, "missing_attempt_ref", "attempt_ref requerido")
    elif not str(attempt_ref).startswith("preflight:"):
        _block(blockers, "invalid_attempt_ref", "attempt_ref debe empezar con preflight:")
    if policy.get("execution_attempt_id") not in (None, "", {}, []):
        _block(blockers, "execution_attempt_id_not_allowed", "execution_attempt_id operativo prohibido")
    if policy.get("attempt_id") not in (None, "", {}, []):
        _block(blockers, "attempt_id_not_allowed", "attempt_id operativo prohibido")
    if policy.get("attempt_ref_is_operational_id") is not False:
        _block(blockers, "attempt_ref_materialized_as_execution_attempt_id", "attempt_ref no es operational id")
    if policy.get("attempt_id_generation_enabled") is True:
        _block(blockers, "attempt_id_generation_enabled_not_allowed", "attempt_id_generation_enabled debe ser false")
    if policy.get("attempt_id_persistence_enabled") is True:
        _block(blockers, "attempt_id_persistence_enabled_not_allowed", "attempt_id_persistence_enabled debe ser false")
    if policy.get("materialized_attempt_id") is not False:
        _block(blockers, "materialized_attempt_id_not_allowed", "materialized_attempt_id debe ser false")
    if policy.get("attempt_id_generation") != "disabled":
        _block(blockers, "attempt_id_generation_not_allowed", "attempt_id_generation debe estar disabled")
    if policy.get("attempt_id_persistence") != "disabled":
        _block(blockers, "attempt_id_persistence_not_allowed", "attempt_id_persistence debe estar disabled")


def _validate_execution_boundary_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for flag, code in EXECUTION_FLAGS.items():
        if flag in policy and policy.get(flag) is not False:
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
            _scan_forbidden_payload(value, blockers)
    elif isinstance(payload, list):
        for item in payload:
            _scan_forbidden_payload(item, blockers)


def _validate_required_refs(refs: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field_name, value in refs.items():
        if value in (None, "", {}, []):
            _block(blockers, f"missing_{field_name}", f"{field_name} requerido")


def _validate_verified_refs(*, execution_attempt_store_verification, dry_run_store_verification_ref, blockers) -> None:
    if not execution_attempt_store_verification or execution_attempt_store_verification.get("status") != "verified":
        _block(blockers, "execution_attempt_store_not_verified", "execution_attempt_store_verified=true requerido")
    if not dry_run_store_verification_ref or dry_run_store_verification_ref.get("status") != "verified":
        _block(blockers, "dry_run_store_not_verified", "dry_run_store_verified=true requerido")


def _validate_cross_refs(*, refs, target_ref, attempt_ref, correlation_id, idempotency_key, dry_run_ref, blockers) -> None:
    target_type = target_ref.get("target_type")
    target_id = target_ref.get("target_id")
    dry_run_id = (dry_run_ref or {}).get("dry_run_id")
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
            _block(blockers, "dry_run_ref_mismatch", f"{name} dry_run_ref mismatch")
        if ref.get("contract_id") and name.endswith("contract_ref") and ref.get("status") == "failed":
            _block(blockers, "contract_ref_mismatch", f"{name} failed")


def _validate_events(events: list[str], blockers: list[dict[str, str]]) -> None:
    for event in events:
        if event in FORBIDDEN_CONTRACT_EVENTS:
            _block(blockers, f"{event}_event_not_allowed", f"evento prohibido: {event}")
        elif event not in ALLOWED_CONTRACT_EVENTS:
            _block(blockers, "unknown_contract_event", f"evento no reconocido: {event}")


def _verdict(blockers: list[dict[str, str]]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if not codes:
        return PASSED_VERDICT
    if any("attempt_id" in code or code == "execution_attempt_id_not_allowed" for code in codes):
        return ATTEMPT_ID_LEAK_VERDICT
    if any("state_not_allowed" in code or code in {"invalid_lifecycle_state", "operational_states_not_allowed"} for code in codes):
        return STATE_LEAK_VERDICT
    if any("transition_not_allowed" in code or code in {"invalid_transition", "implicit_execution_not_allowed", "implicit_scheduler_worker_not_allowed"} for code in codes):
        return TRANSITION_LEAK_VERDICT
    if any(prefix in code for code in codes for prefix in ["execution_payload", "agent_output", "team_output", "model_prompt", "model_response", "tool_call", "tool_result", "memory_write", "memory_read", "secret_value", "credential_value"]):
        return PAYLOAD_LEAK_VERDICT
    if any(code in {"execution_enabled_not_allowed", "agent_execution_enabled_not_allowed", "team_execution_enabled_not_allowed", "rollback_operational_enabled_not_allowed", "retry_operational_enabled_not_allowed", "cancel_operational_enabled_not_allowed"} for code in codes):
        return EXECUTION_BOUNDARY_VERDICT
    if any("scheduler" in code or "worker" in code for code in codes):
        return SCHEDULER_WORKER_BOUNDARY_VERDICT
    if any("external" in code for code in codes):
        return EXTERNAL_BOUNDARY_VERDICT
    if any("mutation" in code or "database_write" in code for code in codes):
        return MUTATION_BOUNDARY_VERDICT
    return BLOCKED_VERDICT


def build_state_summary(policy, source_state, target_state) -> dict[str, Any]:
    return {
        "source_state": source_state,
        "target_state": target_state,
        "allowed_states": list(policy.get("allowed_states") or []),
        "blocked_states": list(policy.get("blocked_states") or []),
        "operational_states_allowed": policy.get("operational_states_allowed") is True,
    }


def build_transition_summary(policy, source_state, target_state) -> dict[str, Any]:
    return {
        "source_state": source_state,
        "target_state": target_state,
        "transition": f"{source_state}->{target_state}",
        "allowed_transitions": list(policy.get("allowed_transitions") or []),
        "blocked_transitions": list(policy.get("blocked_transitions") or []),
        "implicit_execution_allowed": policy.get("implicit_execution_allowed") is True,
        "implicit_scheduler_worker_allowed": policy.get("implicit_scheduler_worker_allowed") is True,
    }


def build_attempt_id_summary(policy) -> dict[str, Any]:
    return {
        "attempt_ref": policy.get("attempt_ref"),
        "attempt_ref_is_operational_id": policy.get("attempt_ref_is_operational_id") is True,
        "attempt_id_generation": policy.get("attempt_id_generation"),
        "attempt_id_persistence": policy.get("attempt_id_persistence"),
        "materialized_attempt_id": policy.get("materialized_attempt_id") is True,
    }


def build_dependency_summary(blockers, attempt_verification, dry_run_verification) -> dict[str, Any]:
    return {
        "execution_attempt_store_verified": (attempt_verification or {}).get("status") == "verified",
        "dry_run_store_verified": (dry_run_verification or {}).get("status") == "verified",
        "required_refs_present": not any(blocker["code"].startswith("missing_") for blocker in blockers),
        "cross_refs_valid": not any("mismatch" in blocker["code"] for blocker in blockers),
    }


def build_execution_boundary_summary(policy) -> dict[str, Any]:
    return {key: value for key, value in policy.items() if key.endswith("_enabled") or key.endswith("_allowed")}


def build_payload_boundary_summary(policy) -> dict[str, Any]:
    return {
        "deep_scan_required": policy.get("deep_scan_required") is True,
        "real_payloads_allowed": policy.get("real_payloads_allowed") is True,
        "forbidden_fields_count": len(policy.get("forbidden_fields") or []),
    }


def build_audit_summary(audit_refs, events) -> dict[str, Any]:
    return {
        "audit_refs_present": bool(audit_refs),
        "allowed_events": sorted(ALLOWED_CONTRACT_EVENTS),
        "forbidden_events": sorted(FORBIDDEN_CONTRACT_EVENTS),
        "declared_events": list(events),
        "writes_audit_events": False,
    }


def build_observability_summary(observability_refs, correlation_id) -> dict[str, Any]:
    return {
        "observability_refs_present": bool(observability_refs),
        "correlation_id": correlation_id,
        "writes_observability_events": False,
    }


def build_boundary_summary(blockers) -> dict[str, Any]:
    return {
        "execution_lifecycle_implementation_created": Path("core/execution_lifecycle.py").exists(),
        "execution_attempt_lifecycle_created": Path("core/execution_attempt_lifecycle.py").exists(),
        "execution_attempt_id_operational": Path("core/execution_attempt_id.py").exists(),
        "execution_history_store_created": Path("core/execution_history_store.py").exists(),
        "scheduler_worker_created": Path("core/scheduler_queue.py").exists() or Path("core/worker_queue.py").exists(),
        "execution_enabled": False,
        "payloads_allowed": False,
        "mutation_allowed": False,
        "blocked": bool(blockers),
    }


def build_readiness_summary(blockers) -> dict[str, Any]:
    return {
        "ready_for_contract_only": not blockers,
        "ready_for_preflight_transitions_only": not blockers,
        "ready_for_lifecycle_implementation": False,
        "ready_for_real_execution": False,
    }


def build_risk_summary() -> dict[str, Any]:
    return {
        "risk": "lifecycle_contract_must_not_be_confused_with_lifecycle_implementation",
        "scope": "preflight_transitions_only",
        "payload_policy": "real_payloads_blocked",
    }


def build_evidence(attempt_store_ref, attempt_verification, dry_run_verification) -> list[dict[str, Any]]:
    return [
        {"name": "execution_attempt_store_ref_present", "passed": bool(attempt_store_ref)},
        {"name": "execution_attempt_store_verified", "passed": (attempt_verification or {}).get("status") == "verified"},
        {"name": "dry_run_store_verified", "passed": (dry_run_verification or {}).get("status") == "verified"},
        {"name": "contract_only", "passed": True},
    ]


def _contract_ref(contract: dict[str, Any] | None) -> dict[str, Any]:
    data = contract or {}
    return {
        "contract_id": data.get("contract_id"),
        "status": data.get("status"),
        "verdict": data.get("verdict"),
        "target_type": (data.get("target_ref") or {}).get("target_type") or data.get("target_type"),
        "target_id": (data.get("target_ref") or {}).get("target_id") or data.get("target_id"),
        "correlation_id": data.get("correlation_id"),
        "idempotency_key": data.get("idempotency_key"),
    }


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
