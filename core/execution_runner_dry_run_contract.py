"""Contrato declarativo del futuro execution runner dry-run, sin implementacion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.audit_store import read_audit_events, verify_audit_store
from core.capability_policy_schema import validate_capability_policy_for_subject
from core.execution_contract_schema import validate_execution_contract_report
from core.execution_runner_dry_run_schema import (
    ALLOWED_TARGET_TYPES,
    BLOCKED_DRY_RUN_CONTRACT_MODES,
    BLOCKED_TARGET_TYPES,
    build_execution_runner_dry_run_contract_report,
)
from core.execution_runner_schema import validate_execution_runner_contract_report
from core.observability import validate_observability_context
from core.runtime_contract_schema import validate_runtime_contract_report
from core.runtime_executor_schema import validate_runtime_executor_contract_report


DRY_RUN_CONTRACT_EVENT_TYPES = {
    "execution_runner_dry_run_contract_started",
    "execution_runner_dry_run_contract_validated",
    "execution_runner_dry_run_contract_passed",
    "execution_runner_dry_run_contract_blocked",
    "execution_runner_dry_run_contract_failed",
    "execution_runner_dry_run_contract_replayed",
    "execution_runner_dry_run_contract_boundary_verified",
}
FORBIDDEN_DRY_RUN_EVENTS = {
    "execution_runner_dry_run_started",
    "dry_run_started",
    "execution_runner_started",
    "execution_started",
    "execution_attempt_created",
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
}
FORBIDDEN_FLAGS = {
    "execution_enabled": "forbidden_execution_flag",
    "execution_runner_enabled": "forbidden_runner_flag",
    "dry_run_enabled": "forbidden_dry_run_flag",
    "execution_attempt_allowed": "forbidden_attempt_flag",
    "execution_attempt_store_allowed": "forbidden_attempt_flag",
    "execution_attempt_created": "forbidden_attempt_flag",
    "model_invocation_enabled": "forbidden_model_flag",
    "tool_execution_enabled": "forbidden_tool_flag",
    "memory_persistence_enabled": "forbidden_memory_flag",
    "external_access": "forbidden_external_access",
    "ui_trigger_enabled": "forbidden_ui_trigger",
    "integration_trigger_enabled": "forbidden_integration_trigger",
    "scheduler_enabled": "forbidden_scheduler",
    "worker_queue_enabled": "forbidden_worker_queue",
    "side_effects_enabled": "forbidden_side_effects",
    "mutation_enabled": "mutation_not_allowed",
}
_MISSING = object()


def validate_execution_runner_dry_run_contract(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    mode: str = "dry_run_contract_only",
    runtime_contract_result: dict[str, Any] | None = None,
    execution_contract_result: dict[str, Any] | None = None,
    runtime_executor_contract_result: dict[str, Any] | None = None,
    runtime_prepare_result: dict[str, Any] | None = None,
    execution_runner_contract_result: dict[str, Any] | None = None,
    observability_context: dict[str, Any] | None = None,
    audit_store_path: str | Path | None = None,
    capability_policy: dict[str, Any] | None = None,
    simulated_plan: dict[str, Any] | None | object = _MISSING,
    input_expectations: dict[str, Any] | None | object = _MISSING,
    output_expectations: dict[str, Any] | None | object = _MISSING,
    simulation_contract: dict[str, Any] | None = None,
    boundary_contract: dict[str, Any] | None = None,
    side_effect_contract: dict[str, Any] | None = None,
    risk_contract: dict[str, Any] | None = None,
    idempotency_contract: dict[str, Any] | None = None,
    lock_contract: dict[str, Any] | None = None,
    abort_contract: dict[str, Any] | None = None,
    rollback_contract: dict[str, Any] | None = None,
    audit_contract: dict[str, Any] | None = None,
    observability_contract: dict[str, Any] | None = None,
    actor: str = "execution_runner_dry_run_contract",
    reason: str = "validate dry-run contract only",
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
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
    validated_runner_contract: dict[str, Any] | None = None
    audit_store_ref: dict[str, Any] = {}
    observability_ref: dict[str, Any] = {}
    capability_ref: dict[str, Any] = {}

    if target_type not in ALLOWED_TARGET_TYPES:
        _block(blockers, "invalid_target_type", f"target_type sin dry-run directo: {target_type}")
    if mode in BLOCKED_DRY_RUN_CONTRACT_MODES:
        _block(blockers, "mode_not_allowed", f"mode bloqueado en esta fase: {mode}")
    elif mode not in {"dry_run_contract_only", "contract_only"}:
        _block(blockers, "mode_not_allowed", f"mode invalido: {mode}")

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

    validated_runtime = _validate_prior_contract(
        runtime_contract_result,
        validator=validate_runtime_contract_report,
        missing_code="missing_runtime_contract",
        not_passed_code="runtime_contract_not_passed",
        result_field="contract_result",
        expected_result="passed",
        target_type=target_type,
        target_id=resolved_target_id,
        domain_id=domain_id,
        name="runtime_contract",
        blockers=blockers,
    )
    validated_execution = _validate_prior_contract(
        execution_contract_result,
        validator=validate_execution_contract_report,
        missing_code="missing_execution_contract",
        not_passed_code="execution_contract_not_passed",
        result_field="contract_result",
        expected_result="passed",
        target_type=target_type,
        target_id=resolved_target_id,
        domain_id=domain_id,
        name="execution_contract",
        blockers=blockers,
    )
    if validated_execution:
        _validate_forbidden_flags(validated_execution, blockers)
        if validated_execution.get("model_invocation_contract", {}).get("invocation_enabled") is True:
            _block(blockers, "forbidden_model_flag", "model invocation debe permanecer false")

    validated_executor_contract = _validate_prior_contract(
        runtime_executor_contract_result,
        validator=validate_runtime_executor_contract_report,
        missing_code="missing_runtime_executor_contract",
        not_passed_code="runtime_executor_contract_not_passed",
        result_field=None,
        expected_result=None,
        target_type=target_type,
        target_id=resolved_target_id,
        domain_id=domain_id,
        name="runtime_executor_contract",
        blockers=blockers,
    )
    if validated_executor_contract:
        if validated_executor_contract.get("blockers"):
            _block(blockers, "runtime_executor_contract_not_passed", "runtime_executor_contract debe estar passed")
        if validated_executor_contract.get("runtime_executor_mode") != "prepare_only":
            _block(blockers, "runtime_executor_contract_not_passed", "runtime_executor_contract debe estar prepare_only")
        _validate_forbidden_flags(validated_executor_contract, blockers)

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

    if execution_runner_contract_result is None:
        _block(blockers, "missing_execution_runner_contract", "execution_runner_contract requerido")
    else:
        try:
            validated_runner_contract = validate_execution_runner_contract_report(execution_runner_contract_result)
            if validated_runner_contract.get("status") != "passed":
                _block(blockers, "execution_runner_contract_not_passed", "execution_runner_contract debe estar passed")
            _validate_contract_identity(
                validated_runner_contract,
                target_type,
                resolved_target_id,
                domain_id,
                "execution_runner_contract",
                blockers,
            )
            if resolved_correlation_id and validated_runner_contract.get("correlation_id") != resolved_correlation_id:
                _block(blockers, "cross_target_contract_ref", "execution_runner_contract correlation_id cruzado")
        except Exception as exc:  # noqa: BLE001
            _block(blockers, "execution_runner_contract_not_passed", f"execution_runner_contract invalido: {exc}")

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
            forbidden = sorted({event.get("event_type") for event in events} & FORBIDDEN_DRY_RUN_EVENTS)
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
            observability_ref = {"correlation_id": context["correlation_id"], "operation": context["operation"]}
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

    resolved_simulation = simulation_contract or build_simulation_contract()
    _validate_simulation_contract(resolved_simulation, blockers)
    resolved_plan = build_plan_contract(target_type=target_type, target_id=resolved_target_id) if simulated_plan is _MISSING else simulated_plan
    _validate_plan_contract(resolved_plan, blockers)
    resolved_inputs = build_input_expectations() if input_expectations is _MISSING else input_expectations
    _validate_input_expectations(resolved_inputs, blockers)
    resolved_outputs = build_output_expectations() if output_expectations is _MISSING else output_expectations
    _validate_output_expectations(resolved_outputs, blockers)
    resolved_boundary = boundary_contract or build_boundary_contract()
    _validate_boundary_contract(resolved_boundary, blockers)
    resolved_side_effects = side_effect_contract or build_side_effect_contract()
    _validate_side_effect_contract(resolved_side_effects, blockers)
    resolved_risk = risk_contract or build_risk_contract()
    _validate_risk_contract(resolved_risk, blockers)
    resolved_idempotency = idempotency_contract or build_idempotency_contract(
        target_type=target_type,
        target_id=resolved_target_id,
        correlation_id=resolved_correlation_id,
        contract_id=f"execution_runner_dry_run_contract_{target_type}_{resolved_target_id}",
    )
    _validate_idempotency_contract(resolved_idempotency, blockers)
    resolved_lock = lock_contract or build_lock_contract(target_type=target_type, target_id=resolved_target_id)
    _validate_lock_contract(resolved_lock, blockers)
    resolved_abort = abort_contract or build_abort_contract(runtime_prepare_result)
    resolved_rollback = rollback_contract or build_rollback_contract(runtime_prepare_result)
    resolved_audit = audit_contract or build_audit_contract(audit_store_ref)
    resolved_observability = observability_contract or build_observability_contract(observability_ref)
    readiness_contract = build_readiness_contract(target_type=target_type)
    boundary_summary = _boundary_summary(resolved_boundary, resolved_side_effects)
    readiness_summary = _readiness_summary(
        target_status=target_status,
        runtime_contract=validated_runtime,
        execution_contract=validated_execution,
        runtime_executor_contract=validated_executor_contract,
        runtime_prepare_result=runtime_prepare_result,
        execution_runner_contract=validated_runner_contract,
        audit_store_ref=audit_store_ref,
        observability_ref=observability_ref,
        capability_ref=capability_ref,
        plan_contract=resolved_plan,
        input_expectations=resolved_inputs,
        output_expectations=resolved_outputs,
    )
    risk_summary = _risk_summary(resolved_risk)
    result_evidence = list(evidence or [])
    result_evidence.extend(
        [
            {"evidence_id": "simulated_plan", "simulated_plan_id": (resolved_plan or {}).get("simulated_plan_id") if isinstance(resolved_plan, dict) else None},
            {"evidence_id": "runtime_preparation_ref", "preparation_id": (runtime_prepare_result or {}).get("preparation_id")},
            {"evidence_id": "execution_runner_contract_ref", "contract_id": (validated_runner_contract or {}).get("contract_id")},
            {"evidence_id": "audit_store_ref", "verified": audit_store_ref.get("verification", {}).get("verified") is True},
        ]
    )

    status = "passed" if not blockers else "blocked"
    return build_execution_runner_dry_run_contract_report(
        contract_id=f"execution_runner_dry_run_contract_{target_type}_{resolved_target_id}",
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
        execution_runner_contract_ref=_contract_ref(validated_runner_contract, "contract_id"),
        audit_store_ref=audit_store_ref,
        observability_context_ref=observability_ref,
        capability_policy_ref=capability_ref,
        readiness_contract=readiness_contract,
        simulation_contract=resolved_simulation,
        plan_contract=resolved_plan,
        input_expectations=resolved_inputs,
        output_expectations=resolved_outputs,
        boundary_contract=resolved_boundary,
        side_effect_contract=resolved_side_effects,
        risk_contract=resolved_risk,
        idempotency_contract=resolved_idempotency,
        lock_contract=resolved_lock,
        abort_contract=resolved_abort,
        rollback_contract=resolved_rollback,
        audit_contract=resolved_audit,
        observability_contract=resolved_observability,
        status=status,
        blockers=blockers,
        warnings=warnings,
        evidence=result_evidence,
        boundary_summary=boundary_summary,
        readiness_summary=readiness_summary,
        risk_summary=risk_summary,
    )


def build_simulation_contract() -> dict[str, Any]:
    return {
        "simulation_allowed": True,
        "simulation_type": "declarative_dry_run_contract",
        "simulation_scope": "contract_only_no_runtime_effects",
        "simulated_plan_required": True,
        "simulated_steps_required": True,
        "real_execution_forbidden": True,
        "real_output_forbidden": True,
        "side_effects_forbidden": True,
        "model_invocation_forbidden": True,
        "tool_execution_forbidden": True,
        "memory_persistence_forbidden": True,
        "external_access_forbidden": True,
    }


def build_plan_contract(*, target_type: str, target_id: str) -> dict[str, Any]:
    return {
        "simulated_plan_id": f"dry_run_plan_{target_type}_{target_id}",
        "plan_type": "declarative_simulated_execution_plan",
        "plan_source": "execution_runner_dry_run_contract",
        "steps": [
            build_step_contract(
                step_id=f"dry_run_step_validate_contracts_{target_type}_{target_id}",
                name="validate_contracts",
                description="Validate already passed contracts before any future dry-run implementation.",
                order=1,
            ),
            build_step_contract(
                step_id=f"dry_run_step_declare_expected_outputs_{target_type}_{target_id}",
                name="declare_expected_outputs",
                description="Declare synthetic output expectations without producing real output.",
                order=2,
            ),
        ],
        "expected_duration_policy": "declarative_only",
        "timeout_policy": {"timeout_enabled": False, "future_timeout_required": True},
        "retry_policy": {"retry_enabled": False, "future_retry_required": True},
        "failure_policy": {"failure_simulation_only": True},
        "cancellation_policy": {"cancellation_simulation_only": True},
        "input_validation_policy": "synthetic_examples_only",
        "output_validation_policy": "synthetic_expectations_only",
        "risk_review_required": True,
        "human_review_required": False,
    }


def build_step_contract(*, step_id: str, name: str, description: str, order: int) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "name": name,
        "description": description,
        "order": order,
        "step_type": "declarative",
        "requires_model": False,
        "requires_tool": False,
        "requires_memory": False,
        "requires_external_access": False,
        "produces_real_output": False,
        "has_side_effects": False,
        "status": "declared",
        "blockers": [],
    }


def build_input_expectations() -> dict[str, Any]:
    return {
        "input_schema_ref": "future_dry_run_input_schema",
        "input_examples_allowed": True,
        "real_input_payload_allowed": False,
        "allowed_input_types": ["synthetic_fixture"],
        "forbidden_input_types": ["real_user_payload", "tool_call", "model_instruction", "execution_action"],
        "max_input_size": 0,
        "sanitization_policy": "future_required",
        "validation_policy": "declarative_schema_only",
        "sensitive_data_policy": "no_sensitive_data",
    }


def build_output_expectations() -> dict[str, Any]:
    return {
        "output_schema_ref": "future_dry_run_output_schema",
        "expected_output_types": ["synthetic_summary", "simulated_step_result"],
        "real_output_allowed": False,
        "synthetic_output_allowed": True,
        "output_validation_policy": "declarative_schema_only",
        "artifact_write_allowed": False,
        "external_write_allowed": False,
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
        "execution_attempt_allowed": False,
        "execution_attempt_store_allowed": False,
        "mutation_allowed": False,
        "side_effects_allowed": False,
    }


def build_side_effect_contract() -> dict[str, bool]:
    return {
        "file_write_allowed": False,
        "database_write_allowed": False,
        "network_call_allowed": False,
        "tool_call_allowed": False,
        "memory_write_allowed": False,
        "state_mutation_allowed": False,
        "artifact_mutation_allowed": False,
        "external_system_mutation_allowed": False,
    }


def build_risk_contract() -> dict[str, Any]:
    return {
        "risk_level": "low",
        "risk_categories": ["simulation_boundary", "no_execution"],
        "risk_summary": "Declarative dry-run contract only; no real execution.",
        "required_reviews": [],
        "blocking_risks": [],
        "non_blocking_warnings": [],
        "human_review_required": False,
        "model_risk": {"real_model_enabled": False},
        "tool_risk": {"real_tool_enabled": False},
        "memory_risk": {"real_persistence_enabled": False},
        "external_access_risk": {"external_access_enabled": False},
        "data_sensitivity_risk": {"sensitive_data_allowed": False},
        "mutation_risk": {"mutation_allowed": False},
        "rollback_risk": {"rollback_declarative_only": True},
    }


def build_readiness_contract(*, target_type: str) -> dict[str, Any]:
    requirements = [
        "target_exists",
        "target_active",
        "runtime_contract_passed",
        "execution_contract_passed",
        "runtime_executor_contract_passed",
        "runtime_prepare_result_prepared",
        "execution_runner_contract_passed",
        "preparation_id_valid",
        "audit_store_verified",
        "observability_context_valid",
        "capability_policy_valid",
        "input_expectations_declarative",
        "output_expectations_declarative",
        "boundary_contract_valid",
        "side_effect_contract_valid",
        "risk_contract_valid",
        "idempotency_key_present",
        "lock_policy_present",
        "abort_plan_present",
        "rollback_plan_present",
    ]
    if target_type == "team":
        requirements.extend(["members_compatible", "coordination_contract_declarative"])
    return {"requirements": requirements, "dry_run_contract_only": True}


def build_idempotency_contract(*, target_type: str, target_id: str, correlation_id: str | None, contract_id: str) -> dict[str, Any]:
    return {
        "idempotency_scope": [target_type, target_id, correlation_id, contract_id],
        "idempotency_policy": "replay_returns_equivalent_dry_run_contract",
        "replay_policy": "no_duplicate_execution_attempt",
        "duplicate_policy": "block_or_replay_declaratively",
    }


def build_lock_contract(*, target_type: str, target_id: str) -> dict[str, Any]:
    return {
        "lock_scope": [target_type, target_id],
        "lock_policy": "declarative_single_target_dry_run_contract_lock_required",
        "concurrency_policy": "no_simultaneous_dry_run_contract_for_same_target",
        "conflict_blocker": "dry_run_contract_lock_conflict",
        "real_lock_created": False,
        "scheduler_enabled": False,
        "worker_queue_enabled": False,
    }


def build_abort_contract(runtime_prepare_result: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "abort_plan_ref": (runtime_prepare_result or {}).get("abort_plan_ref", {}),
        "abort_policy": "future_dry_run_can_abort_before_any_execution",
        "abort_allowed": True,
        "abort_scope": "declarative_metadata_only",
        "executes_abort": False,
    }


def build_rollback_contract(runtime_prepare_result: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "rollback_plan_ref": (runtime_prepare_result or {}).get("rollback_plan_ref", {}),
        "rollback_policy": "future_dry_run_can_rollback_metadata_plan_only",
        "rollback_allowed": True,
        "rollback_scope": "declarative_metadata_only",
        "executes_rollback": False,
    }


def build_audit_contract(audit_store_ref: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_required": True,
        "audit_store_ref": dict(audit_store_ref or {}),
        "audit_store_verified": (audit_store_ref or {}).get("verification", {}).get("verified") is True,
        "audit_events_expected": sorted(DRY_RUN_CONTRACT_EVENT_TYPES),
        "audit_events_forbidden": sorted(FORBIDDEN_DRY_RUN_EVENTS),
        "writes_audit_events": False,
    }


def build_observability_contract(observability_ref: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "observability_required": True,
        "observability_context_ref": dict(observability_ref or {}),
        "correlation_id_required": True,
        "trace_id_required": False,
        "span_policy": "future_required_before_dry_run_implementation",
        "event_policy": "contract_only_declares_events_without_persisting",
    }


def _validate_prior_contract(payload, *, validator, missing_code, not_passed_code, result_field, expected_result, target_type, target_id, domain_id, name, blockers):
    if payload is None:
        _block(blockers, missing_code, f"{name} requerido")
        return None
    try:
        validated = validator(payload)
        if result_field and validated.get(result_field) != expected_result:
            _block(blockers, not_passed_code, f"{name} debe estar {expected_result}")
        _validate_contract_identity(validated, target_type, target_id, domain_id, name, blockers)
        return validated
    except Exception as exc:  # noqa: BLE001
        _block(blockers, not_passed_code, f"{name} invalido: {exc}")
        return None


def _validate_runtime_preparation(preparation, *, target_type, target_id, domain_id, correlation_id, idempotency_key, runtime_contract, execution_contract, runtime_executor_contract, blockers):
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


def _validate_contract_identity(contract, target_type, target_id, domain_id, name, blockers):
    target_ref = contract.get("target_ref", {}) if isinstance(contract.get("target_ref"), dict) else {}
    for field, expected in [("target_type", target_type), ("target_id", target_id), ("domain_id", domain_id)]:
        actual = contract.get(field, target_ref.get(field))
        if actual != expected:
            _block(blockers, "cross_target_contract_ref", f"{name} corresponde a otro {field}")


def _validate_simulation_contract(contract, blockers):
    required = set(build_simulation_contract())
    if not isinstance(contract, dict) or required - set(contract):
        _block(blockers, "invalid_simulated_plan", "simulation_contract incompleto")
        return
    if contract.get("simulation_allowed") is not True:
        _block(blockers, "missing_simulated_plan", "simulation_allowed requerido")
    for field in [
        "real_execution_forbidden",
        "real_output_forbidden",
        "side_effects_forbidden",
        "model_invocation_forbidden",
        "tool_execution_forbidden",
        "memory_persistence_forbidden",
        "external_access_forbidden",
    ]:
        if contract.get(field) is not True:
            _block(blockers, "invalid_simulated_plan", f"{field} debe ser true")


def _validate_plan_contract(plan, blockers):
    if plan is None:
        _block(blockers, "missing_simulated_plan", "simulated_plan requerido")
        return
    required = set(build_plan_contract(target_type="agent", target_id="example_agent")) - {"simulated_plan_id", "steps"}
    if not isinstance(plan, dict) or required - set(plan):
        _block(blockers, "invalid_simulated_plan", "simulated_plan incompleto")
        return
    steps = plan.get("steps")
    if not isinstance(steps, list) or not steps:
        _block(blockers, "missing_simulated_steps", "simulated_steps requeridos")
        return
    for step in steps:
        _validate_step_contract(step, blockers)


def _validate_step_contract(step, blockers):
    required = set(build_step_contract(step_id="dry_run_step_example", name="example", description="example", order=1))
    if not isinstance(step, dict) or required - set(step):
        _block(blockers, "invalid_simulated_step", "simulated_step incompleto")
        return
    for field, code in [
        ("requires_model", "forbidden_model_flag"),
        ("requires_tool", "forbidden_tool_flag"),
        ("requires_memory", "forbidden_memory_flag"),
        ("requires_external_access", "forbidden_external_access"),
        ("produces_real_output", "real_output_not_allowed"),
        ("has_side_effects", "forbidden_side_effects"),
    ]:
        if step.get(field) is True:
            _block(blockers, "invalid_simulated_step" if field.startswith("requires_") else code, f"{field} debe ser false")


def _validate_input_expectations(expectations, blockers):
    if expectations is None:
        _block(blockers, "missing_input_expectations", "input_expectations requerido")
        return
    required = set(build_input_expectations())
    if not isinstance(expectations, dict) or required - set(expectations):
        _block(blockers, "invalid_input_expectations", "input_expectations incompleto")
        return
    if expectations.get("real_input_payload_allowed") is not False:
        _block(blockers, "real_input_payload_not_allowed", "real_input_payload_allowed debe ser false")
    if _contains_marker(expectations.get("input_payload"), "tool_call") or _contains_marker(expectations.get("input_payload"), "invoke_model") or _contains_marker(expectations.get("input_payload"), "execute"):
        _block(blockers, "real_input_payload_not_allowed", "input_payload real no permitido")


def _validate_output_expectations(expectations, blockers):
    if expectations is None:
        _block(blockers, "missing_output_expectations", "output_expectations requerido")
        return
    required = set(build_output_expectations())
    if not isinstance(expectations, dict) or required - set(expectations):
        _block(blockers, "invalid_output_expectations", "output_expectations incompleto")
        return
    if expectations.get("real_output_allowed") is not False:
        _block(blockers, "real_output_not_allowed", "real_output_allowed debe ser false")
    if expectations.get("synthetic_output_allowed") is not True:
        _block(blockers, "synthetic_output_not_declarative", "synthetic_output_allowed debe ser true")
    if expectations.get("artifact_write_allowed") is not False:
        _block(blockers, "mutation_not_allowed", "artifact_write_allowed debe ser false")
    if expectations.get("external_write_allowed") is not False:
        _block(blockers, "forbidden_external_access", "external_write_allowed debe ser false")


def _validate_boundary_contract(contract, blockers):
    required = set(build_boundary_contract())
    if not isinstance(contract, dict) or required - set(contract):
        _block(blockers, "forbidden_execution_flag", "boundary_contract incompleto")
        return
    for field, value in contract.items():
        if value is not False:
            _block(blockers, _boundary_code(field), f"{field} debe ser false")


def _validate_side_effect_contract(contract, blockers):
    required = set(build_side_effect_contract())
    if not isinstance(contract, dict) or required - set(contract):
        _block(blockers, "forbidden_side_effects", "side_effect_contract incompleto")
        return
    for field, value in contract.items():
        if value is not False:
            _block(blockers, _side_effect_code(field), f"{field} debe ser false")


def _validate_risk_contract(contract, blockers):
    required = set(build_risk_contract())
    if not isinstance(contract, dict) or required - set(contract):
        _block(blockers, "critical_risk_without_human_review", "risk_contract incompleto")
        return
    if contract.get("risk_level") == "critical" and contract.get("human_review_required") is not True:
        _block(blockers, "critical_risk_without_human_review", "critical risk requiere human review")
    nested = {
        "model_risk": ("real_model_enabled", "forbidden_model_flag"),
        "tool_risk": ("real_tool_enabled", "forbidden_tool_flag"),
        "memory_risk": ("real_persistence_enabled", "forbidden_memory_flag"),
        "external_access_risk": ("external_access_enabled", "forbidden_external_access"),
        "mutation_risk": ("mutation_allowed", "mutation_not_allowed"),
    }
    for section, (field, code) in nested.items():
        if contract.get(section, {}).get(field) is True:
            _block(blockers, code, f"{section}.{field} debe ser false")


def _validate_idempotency_contract(contract, blockers):
    if not isinstance(contract, dict) or not contract.get("idempotency_scope"):
        _block(blockers, "missing_idempotency_key", "idempotency_contract incompleto")


def _validate_lock_contract(contract, blockers):
    if not isinstance(contract, dict) or not contract.get("lock_scope"):
        _block(blockers, "missing_idempotency_key", "lock_contract incompleto")
        return
    if contract.get("scheduler_enabled") is not False:
        _block(blockers, "forbidden_scheduler", "scheduler_enabled debe ser false")
    if contract.get("worker_queue_enabled") is not False:
        _block(blockers, "forbidden_worker_queue", "worker_queue_enabled debe ser false")
    if contract.get("real_lock_created") is not False:
        _block(blockers, "mutation_not_allowed", "real_lock_created debe ser false")


def _boundary_code(field):
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
        "execution_attempt_allowed": "forbidden_attempt_flag",
        "execution_attempt_store_allowed": "forbidden_attempt_flag",
        "mutation_allowed": "mutation_not_allowed",
        "side_effects_allowed": "forbidden_side_effects",
    }.get(field, "mutation_not_allowed")


def _side_effect_code(field):
    return {
        "network_call_allowed": "forbidden_external_access",
        "tool_call_allowed": "forbidden_tool_flag",
        "memory_write_allowed": "forbidden_memory_flag",
    }.get(field, "mutation_not_allowed" if "mutation" in field or "write" in field else "forbidden_side_effects")


def _validate_forbidden_flags(payload, blockers):
    for flag, code in FORBIDDEN_FLAGS.items():
        if _nested_true(payload, flag):
            _block(blockers, code, f"{flag}=true bloqueado")


def _readiness_summary(**kwargs):
    return {
        "target_active": kwargs["target_status"] == "active",
        "runtime_contract_passed": (kwargs["runtime_contract"] or {}).get("contract_result") == "passed",
        "execution_contract_passed": (kwargs["execution_contract"] or {}).get("contract_result") == "passed",
        "runtime_executor_contract_passed": bool(kwargs["runtime_executor_contract"]) and not kwargs["runtime_executor_contract"].get("blockers"),
        "runtime_prepared": (kwargs["runtime_prepare_result"] or {}).get("status") in {"prepared", "noop_idempotent"},
        "execution_runner_contract_passed": (kwargs["execution_runner_contract"] or {}).get("status") == "passed",
        "audit_store_verified": (kwargs["audit_store_ref"] or {}).get("verification", {}).get("verified") is True,
        "observability_valid": bool(kwargs["observability_ref"]),
        "capability_policy_valid": bool(kwargs["capability_ref"]),
        "simulated_plan_valid": bool(kwargs["plan_contract"]),
        "input_expectations_valid": bool(kwargs["input_expectations"]),
        "output_expectations_valid": bool(kwargs["output_expectations"]),
    }


def _boundary_summary(boundary_contract, side_effect_contract):
    summary = {key.replace("_allowed", "_enabled"): value is True for key, value in boundary_contract.items()}
    summary.update({key.replace("_allowed", "_enabled"): value is True for key, value in side_effect_contract.items()})
    return summary


def _risk_summary(risk_contract):
    return {
        "risk_level": risk_contract.get("risk_level"),
        "human_review_required": risk_contract.get("human_review_required"),
        "blocking_risks": list(risk_contract.get("blocking_risks", [])),
        "model_risk_enabled": risk_contract.get("model_risk", {}).get("real_model_enabled") is True,
        "tool_risk_enabled": risk_contract.get("tool_risk", {}).get("real_tool_enabled") is True,
        "memory_risk_enabled": risk_contract.get("memory_risk", {}).get("real_persistence_enabled") is True,
        "external_access_risk_enabled": risk_contract.get("external_access_risk", {}).get("external_access_enabled") is True,
        "mutation_risk_enabled": risk_contract.get("mutation_risk", {}).get("mutation_allowed") is True,
    }


def _contract_ref(contract, id_field):
    if not contract:
        return {}
    return {id_field: contract.get(id_field), "target_type": contract.get("target_type"), "target_id": contract.get("target_id"), "domain_id": contract.get("domain_id")}


def _extract_capability_policy(target_payload):
    policies = target_payload.get("capabilities", {}).get("policies", [])
    if isinstance(policies, list) and policies:
        for policy in policies:
            if isinstance(policy, dict) and "schema_version" in policy:
                return policy
    return None


def _resolve_target(*, target_type, domain_dir, target_id):
    if target_type == "agent":
        resolved_id = target_id or ""
        payload = _read_json(Path(domain_dir) / "sandbox_agents" / f"{resolved_id}.json")
        return payload["status"], resolved_id, payload["domain_id"], payload
    if target_type == "team":
        resolved_id = target_id or ""
        payload = _read_json(Path(domain_dir) / "sandbox_teams" / f"{resolved_id}.json")
        return payload["status"], resolved_id, payload["domain_id"], payload
    if target_type in BLOCKED_TARGET_TYPES:
        return "unknown", target_id or target_type, "unknown_domain", {}
    return "unknown", target_id or target_type, "unknown_domain", {}


def _nested_true(value, key):
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _contains_marker(value, marker):
    if isinstance(value, dict):
        return any(_contains_marker(key, marker) or _contains_marker(child, marker) for key, child in value.items())
    if isinstance(value, list):
        return any(_contains_marker(item, marker) for item in value)
    if isinstance(value, str):
        return marker in value.lower()
    return False


def _block(blockers, code, message, severity="error"):
    if not any(blocker["code"] == code and blocker["message"] == message for blocker in blockers):
        blockers.append({"code": code, "message": message, "severity": severity})


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
