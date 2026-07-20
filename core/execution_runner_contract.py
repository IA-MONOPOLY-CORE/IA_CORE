"""Contrato declarativo del futuro execution runner, sin ejecucion real."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.audit_store import read_audit_events, verify_audit_store
from core.capability_policy_schema import validate_capability_policy_for_subject
from core.execution_contract_schema import validate_execution_contract_report
from core.execution_runner_schema import (
    ALLOWED_TARGET_TYPES,
    BLOCKED_EXECUTION_RUNNER_MODES,
    BLOCKED_TARGET_TYPES,
    build_execution_runner_contract_report,
)
from core.observability import validate_observability_context
from core.runtime_contract_schema import validate_runtime_contract_report
from core.runtime_executor_schema import validate_runtime_executor_contract_report


CONTRACT_EVENT_TYPES = {
    "execution_runner_contract_started",
    "execution_runner_contract_validated",
    "execution_runner_contract_passed",
    "execution_runner_contract_blocked",
    "execution_runner_contract_failed",
    "execution_runner_contract_replayed",
    "execution_runner_contract_boundary_verified",
}
FORBIDDEN_AUDIT_EVENT_TYPES = {
    "execution_runner_started",
    "execution_started",
    "agent_execution_started",
    "team_execution_started",
    "agent_executed",
    "team_executed",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "ui_triggered",
    "integration_triggered",
    "scheduler_started",
    "worker_queue_started",
}
FORBIDDEN_FLAGS = {
    "execution_enabled": "forbidden_execution_flag",
    "execution_runner_enabled": "forbidden_runner_flag",
    "agent_execution_enabled": "forbidden_execution_flag",
    "team_execution_enabled": "forbidden_execution_flag",
    "model_invocation_enabled": "forbidden_model_flag",
    "tool_execution_enabled": "forbidden_tool_flag",
    "memory_persistence_enabled": "forbidden_memory_flag",
    "external_access": "forbidden_external_access",
    "ui_trigger_enabled": "forbidden_ui_trigger",
    "integration_trigger_enabled": "forbidden_integration_trigger",
    "scheduler_enabled": "forbidden_scheduler",
    "worker_queue_enabled": "forbidden_worker_queue",
    "side_effects_enabled": "mutation_not_allowed",
    "mutation_enabled": "mutation_not_allowed",
}


def validate_execution_runner_contract(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    mode: str = "contract_only",
    runtime_contract_result: dict[str, Any] | None = None,
    execution_contract_result: dict[str, Any] | None = None,
    runtime_executor_contract_result: dict[str, Any] | None = None,
    runtime_prepare_result: dict[str, Any] | None = None,
    observability_context: dict[str, Any] | None = None,
    audit_store_path: str | Path | None = None,
    capability_policy: dict[str, Any] | None = None,
    input_contract: dict[str, Any] | None = None,
    boundary_contract: dict[str, Any] | None = None,
    readiness_contract: dict[str, Any] | None = None,
    idempotency_contract: dict[str, Any] | None = None,
    lock_contract: dict[str, Any] | None = None,
    abort_contract: dict[str, Any] | None = None,
    rollback_contract: dict[str, Any] | None = None,
    audit_contract: dict[str, Any] | None = None,
    observability_contract: dict[str, Any] | None = None,
    actor: str = "execution_runner_contract",
    reason: str = "validate execution runner contract only",
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Valida precondiciones del futuro runner sin ejecutar ni mutar nada."""
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    resolved_target_id = target_id or target_type
    domain_id = "unknown_domain"
    target_status = "unknown"
    target_payload: dict[str, Any] = {}
    resolved_correlation_id = correlation_id or (observability_context or {}).get("correlation_id") or None
    resolved_idempotency_key = idempotency_key or (runtime_prepare_result or {}).get("idempotency_key") or None
    validated_runtime: dict[str, Any] | None = None
    validated_execution: dict[str, Any] | None = None
    validated_executor_contract: dict[str, Any] | None = None
    audit_store_ref: dict[str, Any] = {}
    observability_ref: dict[str, Any] = {}
    capability_ref: dict[str, Any] = {}

    if target_type not in ALLOWED_TARGET_TYPES:
        code = "invalid_target_type"
        if target_type in BLOCKED_TARGET_TYPES:
            code = "invalid_target_type"
        _block(blockers, code, f"target_type sin execution_runner directo: {target_type}")
    if mode in BLOCKED_EXECUTION_RUNNER_MODES:
        _block(blockers, "mode_not_allowed", f"mode bloqueado en esta fase: {mode}")
    elif mode != "contract_only":
        _block(blockers, "mode_not_allowed", f"mode invalido para execution_runner_contract: {mode}")

    try:
        target_status, resolved_target_id, domain_id, target_payload = _resolve_target(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
        )
    except Exception as exc:  # noqa: BLE001
        _block(blockers, "target_not_active", f"target invalido: {exc}")

    _validate_target_status(target_status, blockers)
    _validate_forbidden_flags(target_payload, blockers)
    _validate_forbidden_flags(boundary_contract or {}, blockers)

    if runtime_contract_result is None:
        _block(blockers, "missing_runtime_contract", "runtime_contract requerido")
    else:
        try:
            validated_runtime = validate_runtime_contract_report(runtime_contract_result)
            if validated_runtime["contract_result"] != "passed":
                _block(blockers, "runtime_contract_not_passed", "runtime_contract debe estar passed")
            _validate_contract_identity(validated_runtime, target_type, resolved_target_id, domain_id, "runtime_contract", blockers)
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "runtime_contract_not_passed", f"runtime_contract invalido: {exc}")

    if execution_contract_result is None:
        _block(blockers, "missing_execution_contract", "execution_contract requerido")
    else:
        try:
            validated_execution = validate_execution_contract_report(execution_contract_result)
            if validated_execution["contract_result"] != "passed":
                _block(blockers, "execution_contract_not_passed", "execution_contract debe estar passed")
            _validate_contract_identity(validated_execution, target_type, resolved_target_id, domain_id, "execution_contract", blockers)
            _validate_forbidden_flags(validated_execution, blockers)
            if validated_execution.get("model_invocation_contract", {}).get("invocation_enabled") is True:
                _block(blockers, "forbidden_model_flag", "model invocation debe permanecer false")
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "execution_contract_not_passed", f"execution_contract invalido: {exc}")

    if runtime_executor_contract_result is None:
        _block(blockers, "missing_runtime_executor_contract", "runtime_executor_contract requerido")
    else:
        try:
            validated_executor_contract = validate_runtime_executor_contract_report(runtime_executor_contract_result)
            if validated_executor_contract.get("blockers"):
                _block(blockers, "runtime_executor_contract_not_passed", "runtime_executor_contract debe estar passed")
            if validated_executor_contract.get("runtime_executor_mode") != "prepare_only":
                _block(blockers, "runtime_executor_contract_not_passed", "runtime_executor_contract debe estar prepare_only")
            _validate_contract_identity(validated_executor_contract, target_type, resolved_target_id, domain_id, "runtime_executor_contract", blockers)
            _validate_forbidden_flags(validated_executor_contract, blockers)
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "runtime_executor_contract_not_passed", f"runtime_executor_contract invalido: {exc}")

    if runtime_prepare_result is None:
        _block(blockers, "missing_runtime_preparation", "runtime_prepare_result requerido")
    else:
        _validate_runtime_preparation(
            runtime_prepare_result,
            target_type=target_type,
            target_id=resolved_target_id,
            domain_id=domain_id,
            correlation_id=resolved_correlation_id,
            idempotency_key=resolved_idempotency_key,
            runtime_contract=validated_runtime,
            execution_contract=validated_execution,
            runtime_executor_contract=validated_executor_contract,
            blockers=blockers,
        )

    if not (runtime_prepare_result or {}).get("preparation_id"):
        _block(blockers, "missing_preparation_id", "preparation_id requerido")
    if not resolved_correlation_id:
        _block(blockers, "missing_correlation_id", "correlation_id requerido")
    if not resolved_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")

    if audit_store_path is None:
        _block(blockers, "missing_audit_store", "audit_store requerido")
    else:
        try:
            verification = verify_audit_store(audit_store_path)
            events = read_audit_events(audit_store_path)
            forbidden = sorted({event.get("event_type") for event in events} & FORBIDDEN_AUDIT_EVENT_TYPES)
            if forbidden:
                _block(blockers, "audit_store_not_verified", f"audit_store contiene eventos prohibidos: {', '.join(forbidden)}")
            audit_store_ref = {"audit_store_path": str(audit_store_path), "verification": verification, "event_count": len(events)}
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "audit_store_not_verified", f"audit_store invalido: {exc}")

    if observability_context is None:
        _block(blockers, "missing_observability_context", "observability_context requerido")
    else:
        try:
            context = validate_observability_context(observability_context)
            observability_ref = {
                "correlation_id": context["correlation_id"],
                "operation": context["operation"],
                "persist_events": context.get("persist_events", False),
            }
            if resolved_correlation_id and context["correlation_id"] != resolved_correlation_id:
                _block(blockers, "cross_target_contract_ref", "observability_context correlation_id cruzado")
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "missing_observability_context", f"observability_context invalido: {exc}")

    policy = capability_policy if capability_policy is not None else _extract_capability_policy(target_payload)
    if not policy:
        _block(blockers, "missing_capability_policy", "capability_policy requerida")
    else:
        try:
            validated_policy = validate_capability_policy_for_subject(
                policy,
                subject_type=target_type,
                subject_id=resolved_target_id,
                domain_id=domain_id,
            )
            capability_ref = {
                "policy_id": validated_policy["policy_id"],
                "capability_id": validated_policy["capability_id"],
                "declared_only": validated_policy["declared_only"],
            }
            _validate_forbidden_flags(validated_policy, blockers)
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "missing_capability_policy", f"capability_policy invalida: {exc}")

    resolved_input_contract = input_contract or build_input_contract()
    _validate_input_contract(resolved_input_contract, mode, blockers)
    resolved_boundary_contract = boundary_contract or build_boundary_contract()
    _validate_boundary_contract(resolved_boundary_contract, blockers)
    resolved_idempotency_contract = idempotency_contract or build_idempotency_contract(
        target_type=target_type,
        target_id=resolved_target_id,
        correlation_id=resolved_correlation_id,
        contract_id=f"execution_runner_contract_{target_type}_{resolved_target_id}",
    )
    _validate_idempotency_contract(resolved_idempotency_contract, blockers)
    resolved_lock_contract = lock_contract or build_lock_contract(target_type=target_type, target_id=resolved_target_id)
    _validate_lock_contract(resolved_lock_contract, blockers)
    resolved_abort_contract = abort_contract or build_abort_contract(runtime_prepare_result)
    _validate_abort_contract(resolved_abort_contract, blockers)
    resolved_rollback_contract = rollback_contract or build_rollback_contract(runtime_prepare_result)
    _validate_rollback_contract(resolved_rollback_contract, blockers)
    resolved_audit_contract = audit_contract or build_audit_contract(audit_store_ref)
    resolved_observability_contract = observability_contract or build_observability_contract(observability_ref)
    resolved_readiness_contract = readiness_contract or build_readiness_contract(target_type=target_type)

    readiness_summary = _readiness_summary(
        target_status=target_status,
        runtime_contract=validated_runtime,
        execution_contract=validated_execution,
        runtime_executor_contract=validated_executor_contract,
        runtime_prepare_result=runtime_prepare_result,
        audit_store_ref=audit_store_ref,
        observability_ref=observability_ref,
        capability_ref=capability_ref,
        input_contract=resolved_input_contract,
        boundary_contract=resolved_boundary_contract,
    )
    boundary_summary = _boundary_summary(resolved_boundary_contract)
    result_evidence = list(evidence or [])
    result_evidence.extend(
        [
            {"evidence_id": "target_ref", "target_type": target_type, "target_id": resolved_target_id, "status": target_status},
            {"evidence_id": "runtime_preparation_ref", "preparation_id": (runtime_prepare_result or {}).get("preparation_id")},
            {"evidence_id": "audit_store_ref", "verified": audit_store_ref.get("verification", {}).get("verified") is True},
            {"evidence_id": "observability_context_ref", "correlation_id": resolved_correlation_id},
        ]
    )

    status = "passed" if not blockers else "blocked"
    return build_execution_runner_contract_report(
        contract_id=f"execution_runner_contract_{target_type}_{resolved_target_id}",
        mode=mode,
        target_type=target_type if target_type else "agent",
        target_id=resolved_target_id,
        target_ref={"target_type": target_type, "target_id": resolved_target_id, "status": target_status, "domain_id": domain_id},
        actor=actor,
        reason=reason,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
        runtime_contract_ref=_contract_ref(validated_runtime, "runtime_contract_id"),
        execution_contract_ref=_contract_ref(validated_execution, "execution_contract_id"),
        runtime_executor_contract_ref=_contract_ref(validated_executor_contract, "runtime_executor_contract_id"),
        runtime_preparation_ref={
            "preparation_id": (runtime_prepare_result or {}).get("preparation_id"),
            "status": (runtime_prepare_result or {}).get("status"),
            "mode": (runtime_prepare_result or {}).get("mode"),
        },
        preparation_id=(runtime_prepare_result or {}).get("preparation_id"),
        audit_store_ref=audit_store_ref,
        observability_context_ref=observability_ref,
        capability_policy_ref=capability_ref,
        input_contract=resolved_input_contract,
        boundary_contract=resolved_boundary_contract,
        readiness_contract=resolved_readiness_contract,
        idempotency_contract=resolved_idempotency_contract,
        lock_contract=resolved_lock_contract,
        abort_contract=resolved_abort_contract,
        rollback_contract=resolved_rollback_contract,
        audit_contract=resolved_audit_contract,
        observability_contract=resolved_observability_contract,
        status=status,
        blockers=blockers,
        warnings=warnings,
        evidence=result_evidence,
        boundary_summary=boundary_summary,
        readiness_summary=readiness_summary,
    )


def build_input_contract() -> dict[str, Any]:
    return {
        "input_schema_ref": "future_execution_runner_input_schema",
        "input_payload_allowed": False,
        "input_payload_required": False,
        "max_input_size": 0,
        "allowed_input_types": [],
        "forbidden_input_types": ["tool_call", "model_instruction", "external_request", "execution_action"],
        "requires_sanitization": True,
        "sanitization_policy": "future_required_before_any_runtime_execution",
        "input_validation_required": True,
        "input_validation_status": "declarative",
    }


def build_boundary_contract() -> dict[str, bool]:
    return {
        "agent_execution_allowed": False,
        "team_execution_allowed": False,
        "model_invocation_allowed": False,
        "tool_execution_allowed": False,
        "memory_persistence_allowed": False,
        "external_access_allowed": False,
        "ui_trigger_allowed": False,
        "integration_trigger_allowed": False,
        "scheduler_allowed": False,
        "worker_queue_allowed": False,
        "side_effects_allowed": False,
        "mutation_allowed": False,
    }


def build_readiness_contract(*, target_type: str) -> dict[str, Any]:
    requirements = [
        "target_exists",
        "target_active",
        "runtime_contract_passed",
        "execution_contract_passed",
        "runtime_executor_contract_passed",
        "runtime_prepare_result_prepared",
        "preparation_id_valid",
        "audit_store_verified",
        "observability_context_valid",
        "capability_policy_valid",
        "idempotency_key_present",
        "lock_policy_present",
        "abort_plan_present",
        "rollback_plan_present",
        "input_contract_valid",
        "boundary_contract_valid",
    ]
    if target_type == "team":
        requirements.append("coordination_contract_declarative")
        requirements.append("members_compatible")
    return {"requirements": requirements, "contract_only": True}


def build_idempotency_contract(*, target_type: str, target_id: str, correlation_id: str | None, contract_id: str) -> dict[str, Any]:
    return {
        "idempotency_scope": [target_type, target_id, correlation_id, contract_id],
        "idempotency_policy": "replay_returns_equivalent_contract",
        "replay_policy": "no_duplicate_runtime_execution",
        "duplicate_policy": "block_or_replay_declaratively",
    }


def build_lock_contract(*, target_type: str, target_id: str) -> dict[str, Any]:
    return {
        "lock_scope": [target_type, target_id],
        "lock_policy": "declarative_single_target_lock_required",
        "concurrency_policy": "no_simultaneous_execution_runner_contract_for_same_target",
        "conflict_blocker": "runtime_preparation_lock_conflict",
        "real_lock_created": False,
        "scheduler_enabled": False,
        "worker_queue_enabled": False,
    }


def build_abort_contract(runtime_prepare_result: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "abort_plan_ref": (runtime_prepare_result or {}).get("abort_plan_ref", {}),
        "abort_policy": "future_runner_can_abort_before_execution",
        "abort_allowed": True,
        "abort_scope": "declarative_metadata_only",
        "executes_abort": False,
    }


def build_rollback_contract(runtime_prepare_result: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "rollback_plan_ref": (runtime_prepare_result or {}).get("rollback_plan_ref", {}),
        "rollback_policy": "future_runner_can_rollback_metadata_plan_only",
        "rollback_allowed": True,
        "rollback_scope": "declarative_metadata_only",
        "executes_rollback": False,
    }


def build_audit_contract(audit_store_ref: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_required": True,
        "audit_store_ref": dict(audit_store_ref or {}),
        "audit_store_verified": (audit_store_ref or {}).get("verification", {}).get("verified") is True,
        "audit_events_expected": sorted(CONTRACT_EVENT_TYPES),
        "audit_events_forbidden": sorted(FORBIDDEN_AUDIT_EVENT_TYPES),
        "writes_audit_events": False,
    }


def build_observability_contract(observability_ref: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "observability_required": True,
        "observability_context_ref": dict(observability_ref or {}),
        "correlation_id_required": True,
        "trace_id_required": False,
        "span_policy": "future_required_before_runtime_execution",
        "event_policy": "contract_only_declares_events_without_persisting",
    }


def _validate_runtime_preparation(
    preparation: dict[str, Any],
    *,
    target_type: str,
    target_id: str,
    domain_id: str,
    correlation_id: str | None,
    idempotency_key: str | None,
    runtime_contract: dict[str, Any] | None,
    execution_contract: dict[str, Any] | None,
    runtime_executor_contract: dict[str, Any] | None,
    blockers: list[dict[str, str]],
) -> None:
    if preparation.get("status") not in {"prepared", "noop_idempotent"}:
        _block(blockers, "runtime_preparation_not_prepared", "runtime_prepare_result debe estar prepared")
    if preparation.get("mode") != "prepare_only":
        _block(blockers, "runtime_preparation_not_prepared", "runtime_prepare_result debe ser prepare_only")
    for field, expected in [("target_type", target_type), ("target_id", target_id), ("domain_id", domain_id)]:
        if preparation.get(field) != expected:
            _block(blockers, "cross_target_contract_ref", f"runtime_prepare_result {field} cruzado")
    if correlation_id and preparation.get("correlation_id") != correlation_id:
        _block(blockers, "cross_target_contract_ref", "runtime_prepare_result correlation_id cruzado")
    if idempotency_key and preparation.get("idempotency_key") != idempotency_key:
        _block(blockers, "cross_target_contract_ref", "runtime_prepare_result idempotency_key cruzado")
    for contract, prep_field, id_field in [
        (runtime_contract, "runtime_contract_id", "runtime_contract_id"),
        (execution_contract, "execution_contract_id", "execution_contract_id"),
        (runtime_executor_contract, "runtime_executor_contract_id", "runtime_executor_contract_id"),
    ]:
        if contract and preparation.get(prep_field) != contract.get(id_field):
            _block(blockers, "cross_target_contract_ref", f"runtime_prepare_result {prep_field} cruzado")
    _validate_forbidden_flags(preparation, blockers)


def _validate_target_status(status: str, blockers: list[dict[str, str]]) -> None:
    if status == "legacy":
        _block(blockers, "legacy_target_not_allowed", "legacy target no permitido")
    elif status == "archived":
        _block(blockers, "archived_target_not_allowed", "archived target no permitido")
    elif status == "broken":
        _block(blockers, "broken_target_not_allowed", "broken target no permitido")
    elif status != "active":
        _block(blockers, "target_not_active", "target debe estar active")


def _validate_contract_identity(
    contract: dict[str, Any],
    target_type: str,
    target_id: str,
    domain_id: str,
    name: str,
    blockers: list[dict[str, str]],
) -> None:
    for field, expected in [("target_type", target_type), ("target_id", target_id), ("domain_id", domain_id)]:
        if contract.get(field) != expected:
            _block(blockers, "cross_target_contract_ref", f"{name} corresponde a otro {field}")


def _validate_input_contract(contract: dict[str, Any], mode: str, blockers: list[dict[str, str]]) -> None:
    required = set(build_input_contract())
    if not isinstance(contract, dict) or required - set(contract):
        _block(blockers, "invalid_input_contract", "input_contract incompleto")
        return
    if contract.get("input_validation_status") != "declarative":
        _block(blockers, "invalid_input_contract", "input_validation_status debe ser declarative")
    if mode == "contract_only":
        has_payload = "input_payload" in contract and contract.get("input_payload") not in (None, "", {}, [])
        if contract.get("input_payload_allowed") is not False or has_payload:
            _block(blockers, "input_payload_not_allowed_in_contract_only", "input_payload real no permitido en contract_only")
    for marker in ["tool_call", "model_instruction", "execute", "run", "invoke_model"]:
        if _contains_marker(contract.get("input_payload"), marker):
            _block(blockers, "input_payload_not_allowed_in_contract_only", f"input_payload contiene {marker}")


def _validate_boundary_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    required = set(build_boundary_contract())
    if not isinstance(contract, dict) or required - set(contract):
        _block(blockers, "forbidden_execution_flag", "boundary_contract incompleto")
        return
    for field, value in contract.items():
        if value is not False:
            code = "mutation_not_allowed" if field in {"side_effects_allowed", "mutation_allowed"} else _boundary_allowed_code(field)
            _block(blockers, code, f"{field} debe ser false")


def _validate_idempotency_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict) or not contract.get("idempotency_scope"):
        _block(blockers, "missing_idempotency_key", "idempotency_contract incompleto")


def _validate_lock_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict) or not contract.get("lock_scope"):
        _block(blockers, "missing_idempotency_key", "lock_contract incompleto")
        return
    if contract.get("scheduler_enabled") is not False:
        _block(blockers, "forbidden_scheduler", "scheduler_enabled debe ser false")
    if contract.get("worker_queue_enabled") is not False:
        _block(blockers, "forbidden_worker_queue", "worker_queue_enabled debe ser false")
    if contract.get("real_lock_created") is not False:
        _block(blockers, "mutation_not_allowed", "real_lock_created debe ser false")


def _validate_abort_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict) or not contract.get("abort_allowed"):
        _block(blockers, "runtime_preparation_not_prepared", "abort_contract incompleto")
    if contract.get("executes_abort") is not False:
        _block(blockers, "mutation_not_allowed", "abort_contract no debe ejecutar abort real")


def _validate_rollback_contract(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not isinstance(contract, dict) or not contract.get("rollback_allowed"):
        _block(blockers, "runtime_preparation_not_prepared", "rollback_contract incompleto")
    if contract.get("executes_rollback") is not False:
        _block(blockers, "mutation_not_allowed", "rollback_contract no debe ejecutar rollback real")


def _boundary_allowed_code(field: str) -> str:
    return {
        "agent_execution_allowed": "forbidden_execution_flag",
        "team_execution_allowed": "forbidden_execution_flag",
        "model_invocation_allowed": "forbidden_model_flag",
        "tool_execution_allowed": "forbidden_tool_flag",
        "memory_persistence_allowed": "forbidden_memory_flag",
        "external_access_allowed": "forbidden_external_access",
        "ui_trigger_allowed": "forbidden_ui_trigger",
        "integration_trigger_allowed": "forbidden_integration_trigger",
        "scheduler_allowed": "forbidden_scheduler",
        "worker_queue_allowed": "forbidden_worker_queue",
    }.get(field, "mutation_not_allowed")


def _validate_forbidden_flags(payload: Any, blockers: list[dict[str, str]]) -> None:
    for flag, code in FORBIDDEN_FLAGS.items():
        if _nested_true(payload, flag):
            _block(blockers, code, f"{flag}=true bloqueado")


def _readiness_summary(**kwargs: Any) -> dict[str, bool]:
    return {
        "target_active": kwargs["target_status"] == "active",
        "runtime_contract_passed": (kwargs["runtime_contract"] or {}).get("contract_result") == "passed",
        "execution_contract_passed": (kwargs["execution_contract"] or {}).get("contract_result") == "passed",
        "runtime_executor_contract_passed": bool(kwargs["runtime_executor_contract"]) and not kwargs["runtime_executor_contract"].get("blockers"),
        "runtime_prepared": (kwargs["runtime_prepare_result"] or {}).get("status") in {"prepared", "noop_idempotent"},
        "audit_store_verified": (kwargs["audit_store_ref"] or {}).get("verification", {}).get("verified") is True,
        "observability_valid": bool(kwargs["observability_ref"]),
        "capability_policy_valid": bool(kwargs["capability_ref"]),
        "input_contract_valid": bool(kwargs["input_contract"]),
        "boundary_contract_valid": bool(kwargs["boundary_contract"]),
    }


def _boundary_summary(boundary_contract: dict[str, Any]) -> dict[str, bool]:
    return {
        "agent_execution_allowed": boundary_contract.get("agent_execution_allowed") is True,
        "team_execution_allowed": boundary_contract.get("team_execution_allowed") is True,
        "execution_enabled": False,
        "execution_runner_enabled": False,
        "model_invocation_enabled": False,
        "tool_execution_enabled": False,
        "memory_persistence_enabled": False,
        "external_access_enabled": False,
        "ui_trigger_enabled": False,
        "integration_trigger_enabled": False,
        "scheduler_enabled": False,
        "worker_queue_enabled": False,
        "side_effects_enabled": False,
        "mutation_enabled": False,
    }


def _contract_ref(contract: dict[str, Any] | None, id_field: str) -> dict[str, Any]:
    if not contract:
        return {}
    return {
        id_field: contract.get(id_field),
        "target_type": contract.get("target_type"),
        "target_id": contract.get("target_id"),
        "domain_id": contract.get("domain_id"),
    }


def _extract_capability_policy(target_payload: dict[str, Any]) -> dict[str, Any] | None:
    policies = target_payload.get("capabilities", {}).get("policies", [])
    if isinstance(policies, list) and policies:
        for policy in policies:
            if isinstance(policy, dict) and "schema_version" in policy:
                return policy
    return None


def _resolve_target(*, target_type: str, domain_dir: str | Path | None, target_id: str | None) -> tuple[str, str, str, dict[str, Any]]:
    if target_type == "agent":
        resolved_id = target_id or ""
        payload = _read_json(Path(domain_dir) / "sandbox_agents" / f"{resolved_id}.json")
        return payload["status"], resolved_id, payload["domain_id"], payload
    if target_type == "team":
        resolved_id = target_id or ""
        payload = _read_json(Path(domain_dir) / "sandbox_teams" / f"{resolved_id}.json")
        return payload["status"], resolved_id, payload["domain_id"], payload
    return "unknown", target_id or target_type, "unknown_domain", {}


def _nested_true(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _contains_marker(value: Any, marker: str) -> bool:
    if isinstance(value, dict):
        return any(_contains_marker(key, marker) or _contains_marker(child, marker) for key, child in value.items())
    if isinstance(value, list):
        return any(_contains_marker(item, marker) for item in value)
    if isinstance(value, str):
        return marker in value.lower()
    return False


def _block(blockers: list[dict[str, str]], code: str, message: str, severity: str = "error") -> None:
    if not any(blocker["code"] == code and blocker["message"] == message for blocker in blockers):
        blockers.append({"code": code, "message": message, "severity": severity})


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
