"""Contrato declarativo de dry_run_store append-only, sin implementacion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.audit_store import verify_audit_store
from core.dry_run_store_schema import (
    ALLOWED_TARGET_TYPES,
    BLOCKED_STORAGE_FORMATS,
    BLOCKED_TARGET_TYPES,
    build_dry_run_store_contract_report,
)
from core.execution_runner import RESULT_ONLY_MODE
from core.observability import validate_observability_context


DRY_RUN_STORE_CONTRACT_EVENTS = {
    "dry_run_store_contract_started",
    "dry_run_store_contract_validated",
    "dry_run_store_contract_passed",
    "dry_run_store_contract_blocked",
    "dry_run_store_contract_failed",
    "dry_run_store_contract_replayed",
    "dry_run_store_contract_boundary_verified",
}
FORBIDDEN_DRY_RUN_STORE_EVENTS = {
    "dry_run_store_append_started",
    "dry_run_store_entry_persisted",
    "execution_attempt_created",
    "execution_started",
    "agent_execution_started",
    "team_execution_started",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "ui_triggered",
    "integration_triggered",
    "scheduler_started",
    "worker_queue_started",
    "state_mutated",
    "artifact_mutated",
}
ALLOWED_DRY_RUN_STATUSES = {"prepared", "simulated", "noop_idempotent"}
FORBIDDEN_ENTRY_FIELDS = {
    "execution_attempt_id": "execution_attempt_id_not_allowed",
    "execution_payload": "execution_payload_not_allowed",
    "execution_result": "execution_result_not_allowed",
    "agent_output": "agent_output_not_allowed",
    "team_output": "team_output_not_allowed",
    "model_response": "model_response_not_allowed",
    "model_prompt_real": "model_prompt_not_allowed",
    "model_completion_real": "model_completion_not_allowed",
    "tool_result": "tool_result_not_allowed",
    "tool_call_real": "tool_call_not_allowed",
    "memory_write": "memory_write_not_allowed",
    "memory_read_result": "memory_read_result_not_allowed",
    "external_response": "external_response_not_allowed",
    "external_request": "external_request_not_allowed",
    "scheduler_job": "scheduler_job_not_allowed",
    "worker_task": "worker_task_not_allowed",
    "state_mutation": "state_mutation_not_allowed",
    "artifact_mutation": "artifact_mutation_not_allowed",
    "database_write_result": "artifact_mutation_not_allowed",
    "network_response": "external_response_not_allowed",
    "secret_value": "secret_value_not_allowed",
    "credential_value": "credential_value_not_allowed",
}


def validate_dry_run_store_contract(
    *,
    dry_run_result: dict[str, Any] | None,
    dry_run_contract_result: dict[str, Any] | None = None,
    execution_runner_contract_result: dict[str, Any] | None = None,
    runtime_preparation: dict[str, Any] | None = None,
    audit_store_path: str | Path | None = None,
    observability_context: dict[str, Any] | None = None,
    capability_policy: dict[str, Any] | None = None,
    mode: str = "dry_run_store_contract_only",
    store_type: str = "dry_run_store",
    storage_format: str = "append_only_jsonl",
    target_type: str | None = None,
    target_id: str | None = None,
    append_only_contract: dict[str, Any] | None = None,
    checksum_contract: dict[str, Any] | None = None,
    payload_boundary_contract: dict[str, Any] | None = None,
    actor: str = "dry_run_store_contract",
    reason: str = "validate dry-run store contract only",
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    result = dry_run_result if isinstance(dry_run_result, dict) else {}
    resolved_target_ref = dict(result.get("target_ref") or {})
    resolved_target_type = target_type or result.get("target_type") or resolved_target_ref.get("target_type") or "agent"
    resolved_target_id = target_id or result.get("target_id") or resolved_target_ref.get("target_id") or resolved_target_type
    resolved_correlation_id = correlation_id or result.get("correlation_id") or (observability_context or {}).get("correlation_id")
    resolved_idempotency_key = idempotency_key or result.get("idempotency_key")
    resolved_audit_store_path = audit_store_path if audit_store_path is not None else result.get("audit_store_path")
    resolved_observability_context = observability_context if observability_context is not None else result.get("observability_context")
    dry_run_contract_ref = dict(result.get("dry_run_contract_ref") or {})
    execution_runner_contract_ref = dict(result.get("execution_runner_contract_ref") or {})
    runtime_preparation_ref = dict(result.get("runtime_preparation_ref") or {})

    if Path("core/dry_run_store.py").exists():
        _block(blockers, "store_implementation_not_allowed", "core/dry_run_store.py no debe existir en contrato")
    if Path("core/execution_attempt_store.py").exists():
        _block(blockers, "execution_attempt_store_not_allowed", "core/execution_attempt_store.py no debe existir")
    if mode != "dry_run_store_contract_only":
        _block(blockers, "invalid_mode", f"mode no permitido: {mode}")
    if store_type != "dry_run_store":
        _block(blockers, "invalid_store_type", f"store_type no permitido: {store_type}")
    if storage_format in BLOCKED_STORAGE_FORMATS or storage_format != "append_only_jsonl":
        _block(blockers, "invalid_storage_format", f"storage_format bloqueado: {storage_format}")
    if resolved_target_type not in ALLOWED_TARGET_TYPES:
        _block(blockers, "invalid_target_type", f"target_type sin dry_run_store directo: {resolved_target_type}")
    if resolved_target_type in BLOCKED_TARGET_TYPES:
        _block(blockers, "not_applicable", f"target_type no aplicable: {resolved_target_type}", severity="warning")
    _validate_target_status(resolved_target_ref.get("status"), blockers)

    if dry_run_result is None:
        _block(blockers, "missing_dry_run_result", "dry_run_result requerido")
    else:
        _validate_dry_run_result(result, blockers)
    if not dry_run_contract_ref:
        _block(blockers, "missing_dry_run_contract_ref", "dry_run_contract_ref requerido")
    if not execution_runner_contract_ref:
        _block(blockers, "missing_execution_runner_contract_ref", "execution_runner_contract_ref requerido")
    if not runtime_preparation_ref:
        _block(blockers, "missing_runtime_preparation_ref", "runtime_preparation_ref requerido")
    if not resolved_target_ref:
        _block(blockers, "missing_target_ref", "target_ref requerido")
    if not resolved_correlation_id:
        _block(blockers, "missing_correlation_id", "correlation_id requerido")
    if not resolved_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")
    if not result.get("boundary_summary"):
        _block(blockers, "missing_boundary_summary", "boundary_summary requerido")
    if not result.get("readiness_summary"):
        _block(blockers, "missing_readiness_summary", "readiness_summary requerido")
    if not result.get("risk_summary"):
        _block(blockers, "missing_risk_summary", "risk_summary requerido")
    if audit_store_path is None:
        _block(blockers, "missing_audit_store", "audit_store requerido")
        audit_store_ref: dict[str, Any] = {}
    else:
        audit_store_ref = _audit_ref(resolved_audit_store_path, blockers)
    if observability_context is None:
        _block(blockers, "missing_observability_context", "observability_context requerido")
        observability_ref: dict[str, Any] = {}
    else:
        observability_ref = _observability_ref(resolved_observability_context, blockers)
    if not capability_policy:
        _block(blockers, "missing_capability_policy", "capability_policy requerida")
        capability_ref: dict[str, Any] = {}
    else:
        capability_ref = _capability_ref(capability_policy)

    resolved_append = build_append_only_contract() if append_only_contract is None else append_only_contract
    _validate_append_only_contract(resolved_append, blockers)
    resolved_checksum = build_checksum_contract() if checksum_contract is None else checksum_contract
    _validate_checksum_contract(resolved_checksum, blockers)
    resolved_payload = build_payload_boundary_contract() if payload_boundary_contract is None else payload_boundary_contract
    _validate_payload_boundary_contract(resolved_payload, blockers)
    _validate_refs(
        result=result,
        dry_run_contract_result=dry_run_contract_result,
        execution_runner_contract_result=execution_runner_contract_result,
        runtime_preparation=runtime_preparation,
        target_type=resolved_target_type,
        target_id=resolved_target_id,
        correlation_id=resolved_correlation_id,
        blockers=blockers,
    )

    status = "passed" if not blockers else "blocked"
    entry_contract = build_entry_contract()
    reference_contract = build_reference_contract(
        dry_run_result=result,
        dry_run_contract_ref=dry_run_contract_ref,
        execution_runner_contract_ref=execution_runner_contract_ref,
        runtime_preparation_ref=runtime_preparation_ref,
    )
    return build_dry_run_store_contract_report(
        contract_id=f"dry_run_store_contract_{resolved_target_type}_{resolved_target_id}",
        mode=mode if mode == "dry_run_store_contract_only" else "dry_run_store_contract_only",
        store_type=store_type or "dry_run_store",
        storage_format=storage_format if storage_format == "append_only_jsonl" else "append_only_jsonl",
        append_only=bool(resolved_append.get("append_only")),
        target_type=resolved_target_type,
        target_id=resolved_target_id,
        target_ref=resolved_target_ref,
        actor=actor,
        reason=reason,
        correlation_id=resolved_correlation_id or None,
        idempotency_key=resolved_idempotency_key or None,
        dry_run_id=result.get("dry_run_id") or None,
        dry_run_result_ref=_dry_run_result_ref(result),
        dry_run_contract_ref=dry_run_contract_ref,
        execution_runner_contract_ref=execution_runner_contract_ref,
        runtime_preparation_ref=runtime_preparation_ref,
        execution_runner_result_ref={"mode": result.get("mode"), "status": result.get("status"), "dry_run_id": result.get("dry_run_id")},
        audit_store_ref=audit_store_ref,
        observability_context_ref=observability_ref,
        capability_policy_ref=capability_ref,
        entry_contract=entry_contract,
        append_only_contract=resolved_append,
        idempotency_contract=build_idempotency_contract(
            target_type=resolved_target_type,
            target_id=resolved_target_id,
            correlation_id=resolved_correlation_id,
            idempotency_key=resolved_idempotency_key,
            dry_run_id=result.get("dry_run_id"),
            dry_run_contract_ref=dry_run_contract_ref,
        ),
        checksum_contract=resolved_checksum,
        reference_contract=reference_contract,
        payload_boundary_contract=resolved_payload,
        retention_contract=build_retention_contract(),
        audit_contract=build_audit_contract(audit_store_ref),
        observability_contract=build_observability_contract(observability_ref),
        status=status,
        blockers=blockers,
        warnings=warnings,
        evidence=_evidence(result, audit_store_ref, observability_ref, capability_ref),
        boundary_summary=build_boundary_summary(resolved_append, resolved_checksum, resolved_payload),
        readiness_summary=build_readiness_summary(blockers, audit_store_ref, observability_ref, capability_ref),
        store_summary=build_store_summary(storage_format=storage_format, status=status),
    )


def build_entry_contract() -> dict[str, Any]:
    return {
        "entry_type": "dry_run_result_only",
        "allowed_fields": [
            "dry_run_id",
            "status",
            "mode",
            "target_ref",
            "contract_refs",
            "runtime_preparation_ref",
            "preparation_id",
            "execution_runner_contract_ref",
            "dry_run_contract_ref",
            "simulated_plan",
            "simulated_steps",
            "input_expectations",
            "output_expectations",
            "risk_summary",
            "boundary_summary",
            "readiness_summary",
            "audit_events",
            "observability_events",
            "blocked_side_effects",
            "idempotency_key",
            "correlation_id",
            "created_at",
            "warnings",
            "blockers",
            "evidence",
            "checksum",
            "lineage_ref",
        ],
        "forbidden_fields": sorted(FORBIDDEN_ENTRY_FIELDS),
    }


def build_append_only_contract() -> dict[str, Any]:
    return {
        "append_only": True,
        "overwrite_allowed": False,
        "delete_allowed": False,
        "physical_delete_allowed": False,
        "update_existing_allowed": False,
        "mutable_entry_allowed": False,
        "entry_replacement_allowed": False,
        "replace_allowed": False,
        "allowed_operations": ["append"],
        "blocked_operations": ["overwrite", "update", "delete", "replace", "truncate", "compact_without_policy"],
    }


def build_checksum_contract() -> dict[str, Any]:
    return {
        "checksum_required": True,
        "checksum_algorithm": "sha256",
        "checksum_scope": ["dry_run_id", "target_ref", "contract_refs", "simulated_plan", "boundary_summary"],
        "entry_hash_required": True,
        "canonical_serialization_policy": "json_sort_keys_utf8_no_mutation",
        "tamper_detection_required": True,
    }


def build_payload_boundary_contract() -> dict[str, Any]:
    return {
        "execution_attempt_allowed": False,
        "execution_payload_allowed": False,
        "agent_output_allowed": False,
        "team_output_allowed": False,
        "model_response_allowed": False,
        "model_prompt_allowed": False,
        "model_completion_allowed": False,
        "tool_result_allowed": False,
        "tool_call_allowed": False,
        "memory_write_allowed": False,
        "memory_read_result_allowed": False,
        "external_response_allowed": False,
        "external_request_allowed": False,
        "scheduler_job_allowed": False,
        "worker_task_allowed": False,
        "state_mutation_allowed": False,
        "artifact_mutation_allowed": False,
        "secret_value_allowed": False,
        "credential_value_allowed": False,
    }


def build_reference_contract(**kwargs) -> dict[str, Any]:
    return {
        "required_refs": [
            "dry_run_result_ref",
            "dry_run_contract_ref",
            "execution_runner_contract_ref",
            "runtime_preparation_ref",
            "target_ref",
            "audit_store_ref",
            "observability_context_ref",
            "capability_policy_ref",
        ],
        "dry_run_result_ref": _dry_run_result_ref(kwargs.get("dry_run_result") or {}),
        "dry_run_contract_ref": dict(kwargs.get("dry_run_contract_ref") or {}),
        "execution_runner_contract_ref": dict(kwargs.get("execution_runner_contract_ref") or {}),
        "runtime_preparation_ref": dict(kwargs.get("runtime_preparation_ref") or {}),
        "cross_target_refs_blocked": True,
    }


def build_idempotency_contract(*, target_type, target_id, correlation_id, idempotency_key, dry_run_id, dry_run_contract_ref) -> dict[str, Any]:
    return {
        "idempotency_required": True,
        "idempotency_scope": [target_type, target_id, correlation_id, idempotency_key, dry_run_id, dry_run_contract_ref.get("contract_id")],
        "duplicate_same_scope_policy": "noop_idempotent_or_equivalent_future_behavior",
        "duplicate_different_payload_policy": "blocked",
        "missing_idempotency_key_policy": "blocked",
        "missing_correlation_id_policy": "blocked",
    }


def build_retention_contract() -> dict[str, Any]:
    return {
        "retention_policy_required": True,
        "physical_delete_forbidden_until_policy": True,
        "redaction_policy_future": True,
        "compaction_policy_future": True,
        "export_policy_future": True,
        "privacy_review_required_for_payloads": True,
        "physical_delete_now_allowed": False,
        "compaction_now_allowed": False,
        "sensitive_payloads_now_allowed": False,
    }


def build_audit_contract(audit_store_ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_required": True,
        "audit_store_ref": dict(audit_store_ref),
        "audit_store_verified": audit_store_ref.get("verification", {}).get("verified") is True,
        "audit_events_expected": sorted(DRY_RUN_STORE_CONTRACT_EVENTS),
        "audit_events_forbidden": sorted(FORBIDDEN_DRY_RUN_STORE_EVENTS),
        "writes_audit_events": False,
    }


def build_observability_contract(observability_ref: dict[str, Any]) -> dict[str, Any]:
    return {
        "observability_required": True,
        "observability_context_ref": dict(observability_ref),
        "correlation_id_required": True,
        "trace_id_required": False,
        "event_policy": "contract_only_declares_events_without_persisting",
    }


def build_boundary_summary(append_contract, checksum_contract, payload_contract) -> dict[str, bool]:
    return {
        "append_only": append_contract.get("append_only") is True,
        "overwrite_allowed": append_contract.get("overwrite_allowed") is True,
        "delete_allowed": append_contract.get("delete_allowed") is True,
        "update_existing_allowed": append_contract.get("update_existing_allowed") is True,
        "replace_allowed": append_contract.get("replace_allowed") is True or append_contract.get("entry_replacement_allowed") is True,
        "checksum_required": checksum_contract.get("checksum_required") is True,
        "tamper_detection_required": checksum_contract.get("tamper_detection_required") is True,
        "payloads_real_allowed": any(value is True for value in payload_contract.values()),
        "store_implementation_created": Path("core/dry_run_store.py").exists(),
        "execution_attempt_store_created": Path("core/execution_attempt_store.py").exists(),
    }


def build_readiness_summary(blockers, audit_store_ref, observability_ref, capability_ref) -> dict[str, bool]:
    return {
        "dry_run_store_contract_only": True,
        "dry_run_store_implementation_absent": not Path("core/dry_run_store.py").exists(),
        "execution_attempt_store_absent": not Path("core/execution_attempt_store.py").exists(),
        "audit_store_verified": audit_store_ref.get("verification", {}).get("verified") is True,
        "observability_valid": bool(observability_ref),
        "capability_policy_present": bool(capability_ref),
        "ready_for_contract_only": not blockers,
        "ready_for_implementation": False,
    }


def build_store_summary(*, storage_format: str, status: str) -> dict[str, Any]:
    return {
        "store_type": "dry_run_store",
        "storage_format": storage_format,
        "recommended_persistence": "append_only_jsonl",
        "implementation_created": False,
        "jsonl_written": False,
        "storage_real_created": False,
        "execution_attempt_id_created": False,
        "status": status,
    }


def _validate_dry_run_result(result: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if result.get("mode") != RESULT_ONLY_MODE:
        _block(blockers, "dry_run_result_not_result_only", "dry_run_result debe ser dry_run_result_only")
    if result.get("status") not in ALLOWED_DRY_RUN_STATUSES:
        _block(blockers, "dry_run_result_not_simulated_or_prepared", "dry_run_result debe estar prepared/simulated/noop_idempotent")
    for field, code in [
        ("dry_run_id", "missing_dry_run_id"),
        ("dry_run_contract_ref", "missing_dry_run_contract_ref"),
        ("execution_runner_contract_ref", "missing_execution_runner_contract_ref"),
        ("runtime_preparation_ref", "missing_runtime_preparation_ref"),
        ("target_ref", "missing_target_ref"),
        ("correlation_id", "missing_correlation_id"),
        ("idempotency_key", "missing_idempotency_key"),
        ("boundary_summary", "missing_boundary_summary"),
        ("readiness_summary", "missing_readiness_summary"),
        ("risk_summary", "missing_risk_summary"),
    ]:
        if result.get(field) in (None, "", {}, []):
            _block(blockers, code, f"{field} requerido")
    for field, code in FORBIDDEN_ENTRY_FIELDS.items():
        if field in result and result.get(field) not in (None, "", {}, []):
            _block(blockers, code, f"{field} no permitido en dry_run_store_contract")


def _validate_append_only_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if contract.get("append_only") is not True:
        _block(blockers, "not_append_only", "append_only debe ser true")
    for field, code in [
        ("overwrite_allowed", "overwrite_not_allowed"),
        ("update_existing_allowed", "update_not_allowed"),
        ("delete_allowed", "delete_not_allowed"),
        ("physical_delete_allowed", "delete_not_allowed"),
        ("mutable_entry_allowed", "mutable_entry_not_allowed"),
        ("entry_replacement_allowed", "replace_not_allowed"),
        ("replace_allowed", "replace_not_allowed"),
    ]:
        if contract.get(field) is not False:
            _block(blockers, code, f"{field} debe ser false")


def _validate_checksum_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not contract:
        _block(blockers, "missing_checksum_policy", "checksum_contract requerido")
        return
    if contract.get("checksum_required") is not True or contract.get("entry_hash_required") is not True:
        _block(blockers, "checksum_missing", "checksum y entry_hash requeridos")
    if contract.get("checksum_algorithm") != "sha256":
        _block(blockers, "checksum_algorithm_not_allowed", "checksum_algorithm debe ser sha256")
    if not contract.get("checksum_scope"):
        _block(blockers, "checksum_scope_missing", "checksum_scope requerido")
    if not contract.get("canonical_serialization_policy"):
        _block(blockers, "non_canonical_serialization", "canonical_serialization_policy requerido")
    if contract.get("tamper_detection_required") is not True:
        _block(blockers, "tamper_detection_missing", "tamper_detection_required debe ser true")


def _validate_payload_boundary_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for field, value in contract.items():
        if value is True:
            code = field.replace("_allowed", "_not_allowed")
            if field == "execution_attempt_allowed":
                code = "execution_attempt_id_not_allowed"
            if field == "execution_payload_allowed":
                code = "execution_payload_not_allowed"
            _block(blockers, code, f"{field} debe ser false")


def _validate_refs(*, result, dry_run_contract_result, execution_runner_contract_result, runtime_preparation, target_type, target_id, correlation_id, blockers) -> None:
    for ref_name, ref in [
        ("target_ref", result.get("target_ref") or {}),
        ("dry_run_contract_ref", result.get("dry_run_contract_ref") or {}),
        ("execution_runner_contract_ref", result.get("execution_runner_contract_ref") or {}),
        ("runtime_preparation_ref", result.get("runtime_preparation_ref") or {}),
    ]:
        if ref.get("target_type") and ref.get("target_type") != target_type:
            _block(blockers, "cross_target_ref", f"{ref_name} target_type cruzado")
        if ref.get("target_id") and ref.get("target_id") != target_id:
            _block(blockers, "cross_target_ref", f"{ref_name} target_id cruzado")
    for name, payload in [
        ("dry_run_contract", dry_run_contract_result),
        ("execution_runner_contract", execution_runner_contract_result),
        ("runtime_preparation", runtime_preparation),
    ]:
        if payload:
            if payload.get("target_type") and payload.get("target_type") != target_type:
                _block(blockers, "cross_target_ref", f"{name} target_type cruzado")
            if payload.get("target_id") and payload.get("target_id") != target_id:
                _block(blockers, "cross_target_ref", f"{name} target_id cruzado")
            if payload.get("correlation_id") and correlation_id and payload.get("correlation_id") != correlation_id:
                _block(blockers, "cross_target_ref", f"{name} correlation_id cruzado")


def _validate_target_status(status: str | None, blockers: list[dict[str, str]]) -> None:
    if status == "legacy":
        _block(blockers, "legacy_target_not_allowed", "legacy target no permitido")
    elif status == "archived":
        _block(blockers, "archived_target_not_allowed", "archived target no permitido")
    elif status == "broken":
        _block(blockers, "broken_target_not_allowed", "broken target no permitido")
    elif status and status != "active":
        _block(blockers, "target_not_active", "target debe estar active")


def _audit_ref(path: str | Path, blockers: list[dict[str, str]]) -> dict[str, Any]:
    try:
        verification = verify_audit_store(path)
        return {"audit_store_path": str(path), "verification": verification}
    except Exception as exc:  # noqa: BLE001
        _block(blockers, "audit_store_not_verified", f"audit_store invalido: {exc}")
        return {}


def _observability_ref(context: dict[str, Any], blockers: list[dict[str, str]]) -> dict[str, Any]:
    try:
        validated = validate_observability_context(context)
        return {"correlation_id": validated["correlation_id"], "operation": validated["operation"]}
    except Exception as exc:  # noqa: BLE001
        _block(blockers, "missing_observability_context", f"observability_context invalido: {exc}")
        return {}


def _capability_ref(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy_id": policy.get("policy_id"),
        "capability_id": policy.get("capability_id"),
        "declared_only": policy.get("declared_only"),
    }


def _dry_run_result_ref(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "dry_run_id": result.get("dry_run_id"),
        "status": result.get("status"),
        "mode": result.get("mode"),
        "target_type": result.get("target_type"),
        "target_id": result.get("target_id"),
    }


def _evidence(result, audit_store_ref, observability_ref, capability_ref) -> list[dict[str, Any]]:
    return [
        {"evidence_id": "dry_run_result_ref", "dry_run_id": result.get("dry_run_id"), "mode": result.get("mode")},
        {"evidence_id": "append_only_policy", "append_only": True, "storage_format": "append_only_jsonl"},
        {"evidence_id": "audit_store_ref", "verified": audit_store_ref.get("verification", {}).get("verified") is True},
        {"evidence_id": "observability_ref", "valid": bool(observability_ref)},
        {"evidence_id": "capability_policy_ref", "present": bool(capability_ref)},
        {"evidence_id": "no_store_implementation", "core_dry_run_store_py": Path("core/dry_run_store.py").exists()},
    ]


def _block(blockers: list[dict[str, str]], code: str, message: str, severity: str = "error") -> None:
    if not any(blocker["code"] == code and blocker["message"] == message for blocker in blockers):
        blockers.append({"code": code, "message": message, "severity": severity})
