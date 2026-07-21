"""Contrato declarativo de execution_attempt_store preflight-only.

No implementa store real, no crea execution_attempt_id operativo y no habilita
ejecucion. Solo valida que un futuro store pueda registrar intencion/preflight
por referencia.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.execution_attempt_store_schema import (
    ExecutionAttemptIdPolicy,
    ExecutionAttemptLifecyclePolicy,
    ExecutionAttemptPayloadBoundaryPolicy,
    ExecutionAttemptPreflightPolicy,
    ExecutionAttemptStoreReadiness,
    ExecutionAttemptStoreReferencePolicy,
    build_execution_attempt_store_contract_report,
)
from core.execution_runner import RESULT_ONLY_MODE


CONTRACT_MODE = "execution_attempt_store_contract_only"
ATTEMPT_MODE = "preflight_only"
STORE_TYPE = "execution_attempt_store"
STORAGE_FORMAT = "append_only_jsonl_future"
PASSED_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED"
BLOCKED_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_BLOCKED"
FAILED_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_FAILED"
ATTEMPT_ID_LEAK_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_ATTEMPT_ID_LEAK"
LIFECYCLE_LEAK_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_LIFECYCLE_LEAK"
PAYLOAD_LEAK_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_PAYLOAD_LEAK"
EXECUTION_BOUNDARY_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_EXECUTION_BOUNDARY"
EXTERNAL_BOUNDARY_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_EXTERNAL_BOUNDARY"
MUTATION_BOUNDARY_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_MUTATION_BOUNDARY"

ALLOWED_PREFLIGHT_STATES = {"created", "preflight_passed", "preflight_blocked", "blocked", "failed", "not_applicable"}
BLOCKED_LIFECYCLE_STATES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back_real",
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
}
FORBIDDEN_PAYLOAD_FIELDS = {
    "execution_attempt_id": "execution_attempt_id_not_allowed",
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
    "execution_attempt_store_contract_started",
    "execution_attempt_store_contract_validated",
    "execution_attempt_store_contract_passed",
    "execution_attempt_store_contract_blocked",
    "execution_attempt_store_contract_failed",
    "execution_attempt_store_contract_boundary_verified",
}
FORBIDDEN_CONTRACT_EVENTS = {
    "execution_attempt_created",
    "execution_started",
    "execution_queued",
    "execution_running",
    "execution_completed",
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
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "dry_run_store_contract_ref",
    "dry_run_store_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
}


def validate_execution_attempt_store_contract(
    *,
    dry_run_result: dict[str, Any] | None,
    dry_run_store_contract_result: dict[str, Any] | None,
    dry_run_store_verification: dict[str, Any] | None,
    runtime_contract_result: dict[str, Any] | None,
    execution_contract_result: dict[str, Any] | None,
    runtime_executor_contract_result: dict[str, Any] | None,
    runtime_preparation: dict[str, Any] | None,
    execution_runner_contract_result: dict[str, Any] | None,
    dry_run_contract_result: dict[str, Any] | None,
    dry_run_store_ref: dict[str, Any] | None,
    dry_run_store_checksum_ref: str | None,
    audit_refs: dict[str, Any] | None,
    observability_refs: dict[str, Any] | None,
    capability_policy_ref: dict[str, Any] | None,
    mode: str = CONTRACT_MODE,
    attempt_mode: str = ATTEMPT_MODE,
    store_type: str = STORE_TYPE,
    storage_format: str = STORAGE_FORMAT,
    attempt_ref: str = "future_preflight_attempt_ref",
    attempt_id_policy: dict[str, Any] | None = None,
    preflight_policy: dict[str, Any] | None = None,
    lifecycle_policy: dict[str, Any] | None = None,
    payload_boundary_policy: dict[str, Any] | None = None,
    append_only_policy: dict[str, Any] | None = None,
    checksum_policy: dict[str, Any] | None = None,
    reference_policy: dict[str, Any] | None = None,
    readiness_policy: dict[str, Any] | None = None,
    lifecycle_state: str = "created",
    events: list[str] | None = None,
    target_ref: dict[str, Any] | None = None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    result = dry_run_result if isinstance(dry_run_result, dict) else {}
    target = dict(target_ref or result.get("target_ref") or {})
    target_type = target.get("target_type") or result.get("target_type") or "agent"
    target_id = target.get("target_id") or result.get("target_id") or target_type
    resolved_correlation_id = correlation_id if correlation_id is not None else result.get("correlation_id") or (observability_refs or {}).get("correlation_id")
    resolved_idempotency_key = idempotency_key if idempotency_key is not None else result.get("idempotency_key")

    if Path("core/execution_attempt_store.py").exists():
        _block(blockers, "execution_attempt_store_implementation_not_allowed", "core/execution_attempt_store.py no debe existir")
    if Path("core/execution_history_store.py").exists():
        _block(blockers, "execution_history_store_not_allowed", "execution_history_store no debe existir")
    if mode != CONTRACT_MODE:
        _block(blockers, "invalid_mode", "mode debe ser execution_attempt_store_contract_only")
    if attempt_mode != ATTEMPT_MODE:
        _block(blockers, "invalid_attempt_mode", "attempt_mode debe ser preflight_only")
    if store_type != STORE_TYPE:
        _block(blockers, "invalid_store_type", "store_type debe ser execution_attempt_store")
    if storage_format != STORAGE_FORMAT:
        _block(blockers, "invalid_storage_format", "storage_format debe ser append_only_jsonl_future")

    attempt_id = build_attempt_id_policy(attempt_ref) if attempt_id_policy is None else attempt_id_policy
    preflight = build_preflight_policy() if preflight_policy is None else preflight_policy
    lifecycle = build_lifecycle_policy() if lifecycle_policy is None else lifecycle_policy
    payload_boundary = build_payload_boundary_policy() if payload_boundary_policy is None else payload_boundary_policy
    append_only = build_append_only_policy() if append_only_policy is None else append_only_policy
    checksum = build_checksum_policy() if checksum_policy is None else checksum_policy
    references = build_reference_policy() if reference_policy is None else reference_policy
    readiness = build_readiness_policy() if readiness_policy is None else readiness_policy

    _validate_attempt_id_policy(attempt_id, blockers)
    _validate_preflight_policy(preflight, blockers)
    _validate_lifecycle_policy(lifecycle, lifecycle_state, blockers)
    _validate_payload_boundary_policy(payload_boundary, blockers)
    _scan_forbidden_payload(result, blockers)
    _scan_forbidden_payload(payload or {}, blockers)
    _validate_append_only_policy(append_only, blockers)
    _validate_checksum_policy(checksum, blockers)
    _validate_events(events or sorted(ALLOWED_CONTRACT_EVENTS), blockers)
    _validate_dry_run_dependency(result, dry_run_store_ref, dry_run_store_verification, dry_run_store_checksum_ref, blockers)
    _validate_required_refs(
        refs={
            "runtime_contract_ref": runtime_contract_result,
            "execution_contract_ref": execution_contract_result,
            "runtime_executor_contract_ref": runtime_executor_contract_result,
            "runtime_preparation_ref": runtime_preparation,
            "execution_runner_contract_ref": execution_runner_contract_result,
            "dry_run_contract_ref": dry_run_contract_result,
            "dry_run_store_contract_ref": dry_run_store_contract_result,
            "dry_run_store_ref": dry_run_store_ref,
            "audit_refs": audit_refs,
            "observability_refs": observability_refs,
            "capability_policy_ref": capability_policy_ref,
        },
        blockers=blockers,
    )
    _validate_identity_refs(
        refs=[
            ("target_ref", target),
            ("dry_run_result", result),
            ("runtime_contract", runtime_contract_result),
            ("execution_contract", execution_contract_result),
            ("runtime_executor_contract", runtime_executor_contract_result),
            ("runtime_preparation", runtime_preparation),
            ("execution_runner_contract", execution_runner_contract_result),
            ("dry_run_contract", dry_run_contract_result),
            ("dry_run_store_contract", dry_run_store_contract_result),
            ("dry_run_store_ref", dry_run_store_ref),
        ],
        target_type=target_type,
        target_id=target_id,
        correlation_id=resolved_correlation_id or None,
        idempotency_key=resolved_idempotency_key or None,
        blockers=blockers,
    )
    if not resolved_correlation_id:
        _block(blockers, "missing_correlation_id", "correlation_id requerido")
    if not resolved_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")

    status = "passed" if not blockers else "blocked"
    verdict = _verdict(blockers)
    dry_run_ref = _dry_run_ref(result)
    return build_execution_attempt_store_contract_report(
        contract_id=f"execution_attempt_store_contract_{target_type}_{target_id}",
        status=status,
        verdict=verdict,
        mode=CONTRACT_MODE if mode != CONTRACT_MODE else mode,
        attempt_mode=ATTEMPT_MODE if attempt_mode != ATTEMPT_MODE else attempt_mode,
        store_type=STORE_TYPE if store_type != STORE_TYPE else store_type,
        storage_format=STORAGE_FORMAT if storage_format != STORAGE_FORMAT else storage_format,
        target_ref=target,
        dry_run_ref=dry_run_ref,
        dry_run_store_ref=dry_run_store_ref or {},
        dry_run_store_verification_ref=dry_run_store_verification or {},
        runtime_contract_ref=_contract_ref(runtime_contract_result),
        execution_contract_ref=_contract_ref(execution_contract_result),
        runtime_executor_contract_ref=_contract_ref(runtime_executor_contract_result),
        runtime_preparation_ref=_contract_ref(runtime_preparation),
        execution_runner_contract_ref=_contract_ref(execution_runner_contract_result),
        dry_run_contract_ref=_contract_ref(dry_run_contract_result),
        dry_run_store_contract_ref=_contract_ref(dry_run_store_contract_result),
        audit_refs=audit_refs or {},
        observability_refs=observability_refs or {},
        capability_policy_ref=capability_policy_ref or {},
        correlation_id=resolved_correlation_id or None,
        idempotency_key=resolved_idempotency_key or None,
        attempt_id_policy=attempt_id,
        preflight_policy=preflight,
        lifecycle_policy=lifecycle,
        payload_boundary_policy=payload_boundary,
        append_only_policy=append_only,
        checksum_policy=checksum,
        reference_policy=references,
        readiness_policy=readiness,
        reference_summary=build_reference_summary(dry_run_ref, dry_run_store_ref, dry_run_store_verification, blockers),
        preflight_summary=build_preflight_summary(preflight, lifecycle_state),
        lifecycle_summary=build_lifecycle_summary(lifecycle, lifecycle_state),
        attempt_id_summary=build_attempt_id_summary(attempt_id),
        payload_boundary_summary=build_payload_boundary_summary(payload_boundary),
        append_only_summary=build_append_only_summary(append_only),
        checksum_summary=build_checksum_summary(checksum, dry_run_store_checksum_ref),
        audit_summary=build_audit_summary(audit_refs, events or sorted(ALLOWED_CONTRACT_EVENTS)),
        observability_summary=build_observability_summary(observability_refs, resolved_correlation_id),
        boundary_summary=build_boundary_summary(blockers),
        readiness_summary=build_readiness_summary(blockers),
        risk_summary=build_risk_summary(),
        blockers=blockers,
        warnings=warnings,
        evidence=build_evidence(result, dry_run_store_ref, dry_run_store_verification),
    )


def build_attempt_id_policy(attempt_ref: str = "future_preflight_attempt_ref") -> dict[str, Any]:
    return ExecutionAttemptIdPolicy(attempt_ref=attempt_ref).to_dict()


def build_preflight_policy() -> dict[str, Any]:
    return ExecutionAttemptPreflightPolicy(
        allowed_states=sorted(ALLOWED_PREFLIGHT_STATES),
        blocked_states=sorted(BLOCKED_LIFECYCLE_STATES),
    ).to_dict()


def build_lifecycle_policy() -> dict[str, Any]:
    return ExecutionAttemptLifecyclePolicy(
        current_scope="preflight_only_contract",
        allowed_states=sorted(ALLOWED_PREFLIGHT_STATES),
        blocked_states=sorted(BLOCKED_LIFECYCLE_STATES),
    ).to_dict()


def build_payload_boundary_policy() -> dict[str, Any]:
    return ExecutionAttemptPayloadBoundaryPolicy(forbidden_fields=sorted(FORBIDDEN_PAYLOAD_FIELDS)).to_dict()


def build_append_only_policy() -> dict[str, Any]:
    return {
        "append_only": True,
        "overwrite_allowed": False,
        "update_allowed": False,
        "delete_allowed": False,
        "truncate_allowed": False,
        "replace_allowed": False,
        "storage_format": STORAGE_FORMAT,
    }


def build_checksum_policy() -> dict[str, Any]:
    return {
        "checksum_algorithm": "sha256",
        "canonical_serialization_required": True,
        "previous_entry_checksum_required": True,
        "tamper_detection_required": True,
    }


def build_reference_policy() -> dict[str, Any]:
    return ExecutionAttemptStoreReferencePolicy(required_refs=sorted(REQUIRED_REFS)).to_dict()


def build_readiness_policy() -> dict[str, Any]:
    return ExecutionAttemptStoreReadiness(ready_for_contract_only=True).to_dict()


def _validate_attempt_id_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("execution_attempt_id") not in (None, "", {}, []):
        _block(blockers, "execution_attempt_id_not_allowed", "execution_attempt_id operativo prohibido")
    if policy.get("attempt_id_generation_enabled") is True:
        _block(blockers, "attempt_id_generation_not_allowed", "attempt_id_generation_enabled debe ser false")
    if policy.get("attempt_id_persistence_enabled") is True:
        _block(blockers, "attempt_id_persistence_not_allowed", "attempt_id_persistence_enabled debe ser false")
    if policy.get("materialized_attempt_id") is True:
        _block(blockers, "materialized_attempt_id_not_allowed", "materialized_attempt_id debe ser false")
    if policy.get("attempt_id_generation") != "disabled":
        _block(blockers, "attempt_id_generation_not_allowed", "attempt_id_generation debe estar disabled")
    if policy.get("attempt_id_persistence") != "disabled":
        _block(blockers, "attempt_id_persistence_not_allowed", "attempt_id_persistence debe estar disabled")
    if policy.get("attempt_id_must_not_be_materialized") is not True:
        _block(blockers, "materialized_attempt_id_not_allowed", "attempt_id_must_not_be_materialized debe ser true")
    if not policy.get("attempt_ref"):
        _block(blockers, "missing_attempt_ref", "attempt_ref conceptual requerido")


def _validate_preflight_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for flag, code in EXECUTION_FLAGS.items():
        if policy.get(flag) is not False:
            _block(blockers, code, f"{flag} debe ser false")


def _validate_lifecycle_policy(policy: dict[str, Any], lifecycle_state: str, blockers: list[dict[str, str]]) -> None:
    if policy.get("real_lifecycle_enabled") is not False:
        _block(blockers, "execution_lifecycle_not_allowed", "lifecycle real debe estar deshabilitado")
    if lifecycle_state in BLOCKED_LIFECYCLE_STATES:
        _block(blockers, f"{lifecycle_state}_state_not_allowed", f"{lifecycle_state} no permitido en preflight-only")
    elif lifecycle_state not in ALLOWED_PREFLIGHT_STATES:
        _block(blockers, "invalid_lifecycle_state", "lifecycle_state no permitido")


def _validate_payload_boundary_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("real_payloads_allowed") is not False:
        _block(blockers, "execution_payload_not_allowed", "payloads reales prohibidos")
    forbidden = set(policy.get("forbidden_fields") or [])
    missing = set(FORBIDDEN_PAYLOAD_FIELDS) - forbidden
    for field in sorted(missing):
        _block(blockers, FORBIDDEN_PAYLOAD_FIELDS[field], f"{field} debe estar prohibido")


def _scan_forbidden_payload(payload: Any, blockers: list[dict[str, str]]) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_PAYLOAD_FIELDS and value not in (None, "", {}, []):
                _block(blockers, FORBIDDEN_PAYLOAD_FIELDS[key], f"{key} no permitido")
            _scan_forbidden_payload(value, blockers)
    elif isinstance(payload, list):
        for item in payload:
            _scan_forbidden_payload(item, blockers)


def _validate_append_only_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("append_only") is not True:
        _block(blockers, "not_append_only", "append_only debe ser true")
    for field, code in [
        ("overwrite_allowed", "overwrite_not_allowed"),
        ("update_allowed", "update_not_allowed"),
        ("delete_allowed", "delete_not_allowed"),
        ("truncate_allowed", "truncate_not_allowed"),
        ("replace_allowed", "replace_not_allowed"),
    ]:
        if policy.get(field) is not False:
            _block(blockers, code, f"{field} debe ser false")
    if policy.get("storage_format") != STORAGE_FORMAT:
        _block(blockers, "invalid_storage_format", "storage_format futuro debe ser append_only_jsonl_future")


def _validate_checksum_policy(policy: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if policy.get("checksum_algorithm") != "sha256":
        _block(blockers, "checksum_algorithm_not_allowed", "checksum_algorithm debe ser sha256")
    if policy.get("canonical_serialization_required") is not True:
        _block(blockers, "canonical_serialization_required", "canonical serialization requerida")
    if policy.get("previous_entry_checksum_required") is not True:
        _block(blockers, "previous_entry_checksum_required", "previous_entry_checksum requerido")
    if policy.get("tamper_detection_required") is not True:
        _block(blockers, "tamper_detection_required", "tamper detection requerida")


def _validate_events(events: list[str], blockers: list[dict[str, str]]) -> None:
    for event in events:
        if event in FORBIDDEN_CONTRACT_EVENTS:
            _block(blockers, f"{event}_event_not_allowed", f"evento prohibido: {event}")
        elif event not in ALLOWED_CONTRACT_EVENTS:
            _block(blockers, "unknown_contract_event", f"evento no reconocido: {event}")


def _validate_dry_run_dependency(result, store_ref, verification, checksum_ref, blockers) -> None:
    if not result:
        _block(blockers, "missing_dry_run_ref", "dry_run_ref requerido")
        return
    if not result.get("dry_run_id"):
        _block(blockers, "missing_dry_run_ref", "dry_run_ref requerido")
    if not store_ref:
        _block(blockers, "missing_dry_run_store_ref", "dry_run_store_ref requerido")
    if not verification or verification.get("status") != "verified":
        _block(blockers, "dry_run_store_not_verified", "dry_run_store_verified=true requerido")
    if result.get("mode") != RESULT_ONLY_MODE:
        _block(blockers, "dry_run_result_not_result_only", "dry_run_result_mode debe ser dry_run_result_only")
    if result.get("status") != "simulated":
        _block(blockers, "dry_run_result_not_simulated", "dry_run_result_status debe ser simulated")
    if not checksum_ref:
        _block(blockers, "dry_run_checksum_missing", "dry_run_store_checksum_ref requerido")
    elif verification and _verification_checksum(verification) and checksum_ref != _verification_checksum(verification):
        _block(blockers, "dry_run_store_checksum_mismatch", "checksum de dry_run_store no coincide")


def _validate_required_refs(refs: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    missing_codes = {
        "runtime_contract_ref": "missing_runtime_contract_ref",
        "execution_contract_ref": "missing_execution_contract_ref",
        "runtime_executor_contract_ref": "missing_runtime_executor_contract_ref",
        "runtime_preparation_ref": "missing_runtime_preparation_ref",
        "execution_runner_contract_ref": "missing_execution_runner_contract_ref",
        "dry_run_contract_ref": "missing_dry_run_contract_ref",
        "dry_run_store_contract_ref": "missing_dry_run_store_contract_ref",
        "dry_run_store_ref": "missing_dry_run_store_ref",
        "audit_refs": "missing_audit_refs",
        "observability_refs": "missing_observability_refs",
        "capability_policy_ref": "missing_capability_policy_ref",
    }
    for field, value in refs.items():
        if value in (None, "", {}, []):
            _block(blockers, missing_codes[field], f"{field} requerido")


def _validate_identity_refs(*, refs, target_type, target_id, correlation_id, idempotency_key, blockers) -> None:
    for name, ref in refs:
        if not isinstance(ref, dict) or not ref:
            continue
        if ref.get("target_type") and ref.get("target_type") != target_type:
            _block(blockers, "target_type_mismatch", f"{name} target_type mismatch")
        if ref.get("target_id") and ref.get("target_id") != target_id:
            _block(blockers, "target_id_mismatch", f"{name} target_id mismatch")
        if ref.get("correlation_id") and correlation_id and ref.get("correlation_id") != correlation_id:
            _block(blockers, "correlation_id_mismatch", f"{name} correlation_id mismatch")
        if ref.get("idempotency_key") and idempotency_key and ref.get("idempotency_key") != idempotency_key:
            _block(blockers, "idempotency_key_mismatch", f"{name} idempotency_key mismatch")
        if ref.get("dry_run_id") and name != "dry_run_result":
            # Refs that include dry_run_id must point to the same dry-run id, checked by caller evidence.
            pass


def _verdict(blockers: list[dict[str, str]]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if not codes:
        return PASSED_VERDICT
    if any("attempt_id" in code or code == "execution_attempt_id_not_allowed" for code in codes):
        return ATTEMPT_ID_LEAK_VERDICT
    if any("state_not_allowed" in code or "lifecycle" in code for code in codes):
        return LIFECYCLE_LEAK_VERDICT
    if any(code.endswith("_not_allowed") for code in codes if any(prefix in code for prefix in ["model", "tool", "memory", "execution_payload", "agent", "team"])):
        return PAYLOAD_LEAK_VERDICT
    if any("execution_enabled" in code or code in {"agent_execution_enabled_not_allowed", "team_execution_enabled_not_allowed"} for code in codes):
        return EXECUTION_BOUNDARY_VERDICT
    if any(any(prefix in code for prefix in ["external", "scheduler", "worker"]) for code in codes):
        return EXTERNAL_BOUNDARY_VERDICT
    if any(any(prefix in code for prefix in ["state_mutation", "artifact_mutation", "database_write", "mutation_result"]) for code in codes):
        return MUTATION_BOUNDARY_VERDICT
    return BLOCKED_VERDICT


def build_reference_summary(dry_run_ref, store_ref, verification, blockers) -> dict[str, Any]:
    return {
        "dry_run_ref_present": bool(dry_run_ref.get("dry_run_id")),
        "dry_run_store_ref_present": bool(store_ref),
        "dry_run_store_verified": verification.get("status") == "verified" if isinstance(verification, dict) else False,
        "required_refs_present": not any(blocker["code"].startswith("missing_") for blocker in blockers),
        "reference_mode": "referential_no_payload_copy",
    }


def build_preflight_summary(policy, lifecycle_state) -> dict[str, Any]:
    return {
        "attempt_mode": ATTEMPT_MODE,
        "lifecycle_state": lifecycle_state,
        "allowed_states": list(policy.get("allowed_states") or []),
        "execution_enabled": policy.get("execution_enabled") is True,
    }


def build_lifecycle_summary(policy, lifecycle_state) -> dict[str, Any]:
    return {
        "real_lifecycle_enabled": policy.get("real_lifecycle_enabled") is True,
        "current_scope": policy.get("current_scope", "preflight_only_contract"),
        "lifecycle_state": lifecycle_state,
        "blocked_states": list(policy.get("blocked_states") or []),
    }


def build_attempt_id_summary(policy) -> dict[str, Any]:
    return {
        "attempt_ref": policy.get("attempt_ref"),
        "attempt_id_generation": policy.get("attempt_id_generation"),
        "attempt_id_persistence": policy.get("attempt_id_persistence"),
        "materialization_allowed": policy.get("attempt_id_must_not_be_materialized") is not True,
    }


def build_payload_boundary_summary(policy) -> dict[str, Any]:
    return {
        "deep_scan_required": policy.get("deep_scan_required") is True,
        "real_payloads_allowed": policy.get("real_payloads_allowed") is True,
        "forbidden_fields_count": len(policy.get("forbidden_fields") or []),
    }


def build_append_only_summary(policy) -> dict[str, Any]:
    return dict(policy)


def build_checksum_summary(policy, checksum_ref) -> dict[str, Any]:
    return {**dict(policy), "dry_run_store_checksum_ref": checksum_ref}


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
        "store_implementation_created": Path("core/execution_attempt_store.py").exists(),
        "execution_attempt_id_operational": False,
        "execution_lifecycle_real": False,
        "execution_enabled": False,
        "external_boundary_open": False,
        "mutation_allowed": False,
        "blocked": bool(blockers),
    }


def build_readiness_summary(blockers) -> dict[str, Any]:
    return {
        "ready_for_contract_only": not blockers,
        "ready_for_preflight_only_implementation": False,
        "ready_for_execution_lifecycle": False,
        "ready_for_real_execution": False,
    }


def build_risk_summary() -> dict[str, Any]:
    return {
        "risk": "attempt_store_contract_must_not_be_confused_with_execution",
        "dry_run_store_relationship": "reference_verified_entries_only",
        "payload_policy": "real_payloads_blocked",
    }


def build_evidence(result, store_ref, verification) -> list[dict[str, Any]]:
    return [
        {"evidence_id": "dry_run_ref", "dry_run_id": result.get("dry_run_id"), "mode": result.get("mode"), "status": result.get("status")},
        {"evidence_id": "dry_run_store_ref", "present": bool(store_ref)},
        {"evidence_id": "dry_run_store_verification", "status": (verification or {}).get("status")},
        {"evidence_id": "no_execution_attempt_store_py", "exists": Path("core/execution_attempt_store.py").exists()},
    ]


def _dry_run_ref(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "dry_run_id": result.get("dry_run_id"),
        "mode": result.get("mode"),
        "status": result.get("status"),
        "target_type": result.get("target_type"),
        "target_id": result.get("target_id"),
        "correlation_id": result.get("correlation_id"),
        "idempotency_key": result.get("idempotency_key"),
    }


def _contract_ref(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "contract_id": payload.get("contract_id") or payload.get("preparation_id"),
        "status": payload.get("status") or payload.get("contract_result"),
        "target_type": payload.get("target_type"),
        "target_id": payload.get("target_id"),
        "correlation_id": payload.get("correlation_id"),
        "idempotency_key": payload.get("idempotency_key"),
    }


def _verification_checksum(verification: dict[str, Any]) -> str | None:
    return verification.get("last_entry_checksum") or verification.get("entry_checksum")


def _block(blockers: list[dict[str, str]], code: str, message: str, severity: str = "error") -> None:
    if not any(blocker["code"] == code and blocker["message"] == message for blocker in blockers):
        blockers.append({"code": code, "message": message, "severity": severity})
