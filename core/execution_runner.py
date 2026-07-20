"""Execution runner dry-run result-only.

Este modulo no ejecuta agentes/equipos, no invoca modelos, no ejecuta tools,
no persiste memoria real, no crea execution attempts ni stores.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_runner_dry_run_contract import FORBIDDEN_DRY_RUN_EVENTS
from core.execution_runner_dry_run_schema import validate_execution_runner_dry_run_contract_report
from core.observability import validate_observability_context


ALLOWED_STATUSES = {"prepared", "simulated", "blocked", "aborted", "rolled_back", "noop_idempotent", "failed"}
RESULT_ONLY_MODE = "dry_run_result_only"
ALLOWED_CONTRACT_MODES = {"dry_run_contract_only", "contract_only"}
BLOCKED_RESULT_MODES = {
    "dry_run_only",
    "simulation_only",
    "no_model_execution_plan",
    "model_invocation_future",
    "tool_execution_future",
    "memory_persistence_future",
    "full_execution_future",
}
PERMITTED_DRY_RUN_EVENTS = {
    "execution_runner_dry_run_prepare_started",
    "execution_runner_dry_run_prepare_completed",
    "execution_runner_dry_run_started",
    "execution_runner_dry_run_simulated",
    "execution_runner_dry_run_blocked",
    "execution_runner_dry_run_aborted",
    "execution_runner_dry_run_rolled_back",
    "execution_runner_dry_run_replayed",
    "execution_runner_dry_run_boundary_verified",
}
PROHIBITED_EVENTS = {
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
    "state_mutated",
    "artifact_mutated",
} | FORBIDDEN_DRY_RUN_EVENTS
BOUNDARY_FIELDS = {
    "agent_execution": False,
    "team_execution": False,
    "model_invocation": False,
    "tool_execution": False,
    "memory_persistence": False,
    "external_access": False,
    "ui_trigger": False,
    "integration_trigger": False,
    "scheduler": False,
    "worker_queue": False,
    "execution_attempt": False,
    "execution_attempt_store": False,
    "dry_run_store": False,
    "mutation": False,
    "side_effects": False,
}


def prepare_dry_run(
    *,
    dry_run_contract_result: dict[str, Any] | None,
    observability_context: dict[str, Any] | None,
    audit_store_path: str | Path | None,
    actor: str = "execution_runner_dry_run_result_only",
    reason: str = "prepare dry-run result only",
    idempotency_registry: set[tuple[str, str, str | None, str | None, str]] | None = None,
) -> dict[str, Any]:
    """Prepara un resultado dry-run declarativo. No ejecuta ni persiste."""
    return _build_result(
        requested_status="prepared",
        dry_run_contract_result=dry_run_contract_result,
        observability_context=observability_context,
        audit_store_path=audit_store_path,
        actor=actor,
        reason=reason,
        idempotency_registry=idempotency_registry,
        event_types=["execution_runner_dry_run_prepare_started", "execution_runner_dry_run_prepare_completed", "execution_runner_dry_run_boundary_verified"],
    )


def run_dry_run(
    *,
    dry_run_contract_result: dict[str, Any] | None = None,
    prepared_result: dict[str, Any] | None = None,
    observability_context: dict[str, Any] | None = None,
    audit_store_path: str | Path | None = None,
    actor: str = "execution_runner_dry_run_result_only",
    reason: str = "run dry-run result only",
    idempotency_registry: set[tuple[str, str, str | None, str | None, str]] | None = None,
) -> dict[str, Any]:
    """Construye un DryRunResult simulado. No ejecuta nada real."""
    contract = dry_run_contract_result or (prepared_result or {}).get("dry_run_contract_result")
    context = observability_context or (prepared_result or {}).get("observability_context")
    store_path = audit_store_path or (prepared_result or {}).get("audit_store_path")
    return _build_result(
        requested_status="simulated",
        dry_run_contract_result=contract,
        observability_context=context,
        audit_store_path=store_path,
        actor=actor,
        reason=reason,
        idempotency_registry=idempotency_registry,
        event_types=["execution_runner_dry_run_started", "execution_runner_dry_run_simulated", "execution_runner_dry_run_boundary_verified"],
    )


def abort_dry_run(
    dry_run_result: dict[str, Any] | None = None,
    *,
    dry_run_id: str | None = None,
    actor: str = "execution_runner_dry_run_result_only",
    reason: str = "abort dry-run result only",
) -> dict[str, Any]:
    """Devuelve abort result-only; no cancela ejecucion real ni toca targets."""
    return _terminal_result(dry_run_result, dry_run_id=dry_run_id, status="aborted", event_type="execution_runner_dry_run_aborted", actor=actor, reason=reason)


def rollback_dry_run(
    dry_run_result: dict[str, Any] | None = None,
    *,
    dry_run_id: str | None = None,
    actor: str = "execution_runner_dry_run_result_only",
    reason: str = "rollback dry-run result only",
) -> dict[str, Any]:
    """Devuelve rollback result-only; no revierte runtime ni targets reales."""
    return _terminal_result(dry_run_result, dry_run_id=dry_run_id, status="rolled_back", event_type="execution_runner_dry_run_rolled_back", actor=actor, reason=reason)


def _build_result(
    *,
    requested_status: str,
    dry_run_contract_result: dict[str, Any] | None,
    observability_context: dict[str, Any] | None,
    audit_store_path: str | Path | None,
    actor: str,
    reason: str,
    idempotency_registry: set[tuple[str, str, str | None, str | None, str]] | None,
    event_types: list[str],
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    contract = _validate_dry_run_contract(dry_run_contract_result, blockers)
    context = _validate_context(observability_context, blockers)
    audit_ref = _validate_audit_store(audit_store_path, blockers)

    if contract:
        _validate_contract_boundaries(contract, blockers)
        _validate_forbidden_events(contract.get("audit_contract", {}).get("audit_events_forbidden", []), blockers)
    correlation_id = (context or {}).get("correlation_id") or (contract or {}).get("correlation_id")
    idempotency_key = (contract or {}).get("idempotency_key")
    key = _idempotency_key(contract, correlation_id, idempotency_key)
    status = requested_status if not blockers else "blocked"

    if status != "blocked" and idempotency_registry is not None:
        if key in idempotency_registry:
            status = "noop_idempotent"
            warnings.append("dry_run_result_only_idempotent_replay")
            event_types = ["execution_runner_dry_run_replayed", "execution_runner_dry_run_boundary_verified"]
        else:
            idempotency_registry.add(key)

    result = _result(
        status=status,
        contract=contract,
        context=context,
        audit_store_path=audit_store_path,
        audit_ref=audit_ref,
        blockers=blockers,
        warnings=warnings,
        event_types=event_types if status != "blocked" else ["execution_runner_dry_run_blocked", "execution_runner_dry_run_boundary_verified"],
        actor=actor,
        reason=reason,
    )
    return result


def _validate_dry_run_contract(contract: dict[str, Any] | None, blockers: list[dict[str, str]]) -> dict[str, Any] | None:
    if contract is None:
        _block(blockers, "missing_dry_run_contract", "execution_runner_dry_run_contract requerido")
        return None
    try:
        validated = validate_execution_runner_dry_run_contract_report(contract)
    except Exception as exc:  # noqa: BLE001
        _block(blockers, "dry_run_contract_not_passed", f"execution_runner_dry_run_contract invalido: {exc}")
        return None
    if validated.get("status") != "passed":
        _block(blockers, "dry_run_contract_not_passed", "execution_runner_dry_run_contract debe estar passed")
    if validated.get("mode") not in ALLOWED_CONTRACT_MODES:
        _block(blockers, "mode_not_allowed", f"dry_run_contract mode no permitido: {validated.get('mode')}")
    if validated.get("mode") in BLOCKED_RESULT_MODES:
        _block(blockers, "dry_run_mode_not_allowed", f"dry_run mode bloqueado: {validated.get('mode')}")
    runner_ref = validated.get("execution_runner_contract_ref") or {}
    if not runner_ref.get("contract_id"):
        _block(blockers, "missing_execution_runner_contract", "execution_runner_contract_ref requerido")
    if validated.get("readiness_summary", {}).get("execution_runner_contract_passed") is False:
        _block(blockers, "execution_runner_contract_not_passed", "execution_runner_contract debe estar passed")
    preparation_ref = validated.get("runtime_preparation_ref") or {}
    if not preparation_ref:
        _block(blockers, "missing_runtime_preparation", "runtime_preparation_ref requerido")
    elif preparation_ref.get("status") not in {"prepared", "noop_idempotent"}:
        _block(blockers, "runtime_preparation_not_prepared", "runtime_preparation_ref debe estar prepared")
    plan = validated.get("plan_contract") or {}
    steps = plan.get("steps")
    if not steps:
        _block(blockers, "missing_simulated_plan", "simulated_plan requerido")
    elif not isinstance(steps, list):
        _block(blockers, "invalid_simulated_steps", "simulated_steps debe ser lista")
    else:
        _validate_simulated_steps(steps, blockers)
    target_status = validated.get("target_ref", {}).get("status")
    if target_status == "legacy":
        _block(blockers, "legacy_target_not_allowed", "legacy target no permitido")
    elif target_status == "archived":
        _block(blockers, "archived_target_not_allowed", "archived target no permitido")
    elif target_status == "broken":
        _block(blockers, "broken_target_not_allowed", "broken target no permitido")
    return validated


def _validate_context(context: dict[str, Any] | None, blockers: list[dict[str, str]]) -> dict[str, Any] | None:
    if context is None:
        _block(blockers, "missing_observability_context", "observability_context requerido")
        return None
    try:
        return validate_observability_context(context)
    except Exception as exc:  # noqa: BLE001
        _block(blockers, "missing_observability_context", f"observability_context invalido: {exc}")
        return None


def _validate_audit_store(path: str | Path | None, blockers: list[dict[str, str]]) -> dict[str, Any]:
    if path is None:
        _block(blockers, "missing_audit_store", "audit_store requerido")
        return {}
    try:
        verification = verify_audit_store(path)
        event_types = {event.get("event_type") for event in read_audit_events(path)}
    except Exception as exc:  # noqa: BLE001
        _block(blockers, "audit_store_not_verified", f"audit_store invalido: {exc}")
        return {}
    forbidden = sorted(event_types & PROHIBITED_EVENTS)
    if forbidden:
        _block(blockers, "audit_store_not_verified", f"audit_store contiene eventos prohibidos: {', '.join(forbidden)}")
    return {"audit_store_path": str(path), "verification": verification}


def _validate_contract_boundaries(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    boundary = contract.get("boundary_summary") or {}
    side_effects = contract.get("side_effect_contract") or {}
    risk = contract.get("risk_summary") or {}
    for field, code in [
        ("execution_attempt_enabled", "forbidden_execution_attempt"),
        ("execution_attempt_store_enabled", "forbidden_execution_attempt_store"),
        ("agent_execution_enabled", "forbidden_agent_execution"),
        ("team_execution_enabled", "forbidden_team_execution"),
        ("model_invocation_enabled", "forbidden_model_invocation"),
        ("tool_execution_enabled", "forbidden_tool_execution"),
        ("memory_persistence_enabled", "forbidden_memory_persistence"),
        ("external_access_enabled", "forbidden_external_access"),
        ("ui_trigger_enabled", "forbidden_ui_trigger"),
        ("integration_trigger_enabled", "forbidden_integration_trigger"),
        ("scheduler_enabled", "forbidden_scheduler"),
        ("worker_queue_enabled", "forbidden_worker_queue"),
        ("side_effects_enabled", "forbidden_side_effects"),
        ("mutation_enabled", "mutation_not_allowed"),
    ]:
        if boundary.get(field) is True:
            _block(blockers, code, f"{field}=true bloqueado")
    for field, value in side_effects.items():
        if value is not False:
            _block(blockers, _side_effect_code(field), f"{field}=true bloqueado")
    for field, code in [
        ("model_risk_enabled", "forbidden_model_invocation"),
        ("tool_risk_enabled", "forbidden_tool_execution"),
        ("memory_risk_enabled", "forbidden_memory_persistence"),
        ("external_access_risk_enabled", "forbidden_external_access"),
        ("mutation_risk_enabled", "mutation_not_allowed"),
    ]:
        if risk.get(field) is True:
            _block(blockers, code, f"{field}=true bloqueado")


def _validate_simulated_steps(steps: list[Any], blockers: list[dict[str, str]]) -> None:
    for step in steps:
        if not isinstance(step, dict):
            _block(blockers, "invalid_simulated_steps", "simulated_step debe ser objeto")
            continue
        for field in ["step_id", "order", "status"]:
            if step.get(field) in (None, ""):
                _block(blockers, "invalid_simulated_steps", f"{field} requerido")
        for field in ["requires_model", "requires_tool", "requires_memory", "requires_external_access", "has_side_effects"]:
            if step.get(field) is True:
                _block(blockers, "invalid_simulated_steps", f"{field} debe ser false")
        if step.get("produces_real_output") is True:
            _block(blockers, "invalid_simulated_steps", "produces_real_output debe ser false")


def _validate_forbidden_events(events: list[Any], blockers: list[dict[str, str]]) -> None:
    found = sorted(set(str(event) for event in events) & PROHIBITED_EVENTS)
    if found:
        return
    # The contract must declare forbidden events; if it does not, block result-only execution.
    if not events:
        _block(blockers, "forbidden_side_effects", "audit_events_forbidden requerido")


def _result(
    *,
    status: str,
    contract: dict[str, Any] | None,
    context: dict[str, Any] | None,
    audit_store_path: str | Path | None,
    audit_ref: dict[str, Any],
    blockers: list[dict[str, str]],
    warnings: list[str],
    event_types: list[str],
    actor: str,
    reason: str,
) -> dict[str, Any]:
    contract = dict(contract or {})
    dry_run_id = _dry_run_id(contract)
    target_ref = dict(contract.get("target_ref") or {})
    plan = deepcopy(contract.get("plan_contract") or {})
    event_refs = _declarative_events(event_types, contract=contract, context=context, status=status, actor=actor, reason=reason)
    result = {
        "dry_run_id": dry_run_id,
        "status": status,
        "mode": RESULT_ONLY_MODE,
        "target_type": contract.get("target_type") or target_ref.get("target_type"),
        "target_id": contract.get("target_id") or target_ref.get("target_id"),
        "target_ref": target_ref,
        "contract_refs": {
            "runtime_contract_ref": deepcopy(contract.get("runtime_contract_ref") or {}),
            "execution_contract_ref": deepcopy(contract.get("execution_contract_ref") or {}),
            "runtime_executor_contract_ref": deepcopy(contract.get("runtime_executor_contract_ref") or {}),
            "execution_runner_contract_ref": deepcopy(contract.get("execution_runner_contract_ref") or {}),
            "dry_run_contract_ref": {"contract_id": contract.get("contract_id"), "mode": contract.get("mode"), "status": contract.get("status")},
        },
        "runtime_preparation_ref": deepcopy(contract.get("runtime_preparation_ref") or {}),
        "preparation_id": contract.get("preparation_id"),
        "execution_runner_contract_ref": deepcopy(contract.get("execution_runner_contract_ref") or {}),
        "dry_run_contract_ref": {"contract_id": contract.get("contract_id"), "mode": contract.get("mode"), "status": contract.get("status")},
        "dry_run_contract_result": deepcopy(contract),
        "observability_context": deepcopy(context or {}),
        "audit_store_path": str(audit_store_path) if audit_store_path is not None else None,
        "simulated_plan": plan,
        "simulated_steps": deepcopy(plan.get("steps", [])),
        "input_expectations": deepcopy(contract.get("input_expectations") or {}),
        "output_expectations": deepcopy(contract.get("output_expectations") or {}),
        "risk_summary": deepcopy(contract.get("risk_summary") or {}),
        "boundary_summary": _boundary_summary(contract),
        "readiness_summary": deepcopy(contract.get("readiness_summary") or {}),
        "audit_events": event_refs,
        "observability_events": deepcopy(event_refs),
        "blocked_side_effects": _blocked_side_effects(),
        "idempotency_key": contract.get("idempotency_key"),
        "correlation_id": (context or {}).get("correlation_id") or contract.get("correlation_id"),
        "created_at": datetime.now().isoformat(),
        "warnings": list(warnings),
        "blockers": deepcopy(blockers),
        "evidence": _evidence(contract, audit_ref, status),
    }
    _validate_result(result)
    return result


def _terminal_result(
    dry_run_result: dict[str, Any] | None,
    *,
    dry_run_id: str | None,
    status: str,
    event_type: str,
    actor: str,
    reason: str,
) -> dict[str, Any]:
    base = deepcopy(dry_run_result or {})
    if not base:
        base = {
            "dry_run_id": dry_run_id or "missing_dry_run_id",
            "status": status,
            "mode": RESULT_ONLY_MODE,
            "target_type": None,
            "target_id": None,
            "target_ref": {},
            "contract_refs": {},
            "runtime_preparation_ref": {},
            "preparation_id": None,
            "execution_runner_contract_ref": {},
            "dry_run_contract_ref": {},
            "simulated_plan": {},
            "simulated_steps": [],
            "input_expectations": {},
            "output_expectations": {},
            "risk_summary": {},
            "boundary_summary": dict(BOUNDARY_FIELDS),
            "readiness_summary": {},
            "audit_events": [],
            "observability_events": [],
            "blocked_side_effects": _blocked_side_effects(),
            "idempotency_key": None,
            "correlation_id": None,
            "warnings": [],
            "blockers": [],
            "evidence": [],
        }
    base["dry_run_id"] = dry_run_id or base.get("dry_run_id")
    base["status"] = status
    base["mode"] = RESULT_ONLY_MODE
    base["audit_events"] = _declarative_events([event_type, "execution_runner_dry_run_boundary_verified"], contract=base.get("dry_run_contract_result") or {}, context=base.get("observability_context") or {}, status=status, actor=actor, reason=reason)
    base["observability_events"] = deepcopy(base["audit_events"])
    base["boundary_summary"] = {**dict(BOUNDARY_FIELDS), **{key: False for key in BOUNDARY_FIELDS}}
    base["created_at"] = datetime.now().isoformat()
    _validate_result(base)
    return base


def _dry_run_id(contract: dict[str, Any]) -> str:
    target_type = contract.get("target_type") or "unknown_target_type"
    target_id = contract.get("target_id") or "unknown_target"
    idempotency_key = contract.get("idempotency_key") or "missing_idempotency_key"
    return f"dry_run_{target_type}_{target_id}_{idempotency_key}"


def _idempotency_key(contract: dict[str, Any] | None, correlation_id: str | None, idempotency_key: str | None) -> tuple[str, str, str | None, str | None, str]:
    contract = contract or {}
    return (
        str(contract.get("target_type")),
        str(contract.get("target_id")),
        correlation_id,
        idempotency_key,
        str(contract.get("contract_id")),
    )


def _declarative_events(event_types: list[str], *, contract: dict[str, Any], context: dict[str, Any] | None, status: str, actor: str, reason: str) -> list[dict[str, Any]]:
    events = []
    for index, event_type in enumerate(event_types, start=1):
        if event_type in PROHIBITED_EVENTS:
            continue
        events.append(
            {
                "event_id": f"event_{event_type}_{contract.get('target_type', 'target')}_{contract.get('target_id', 'unknown')}_{index}",
                "event_type": event_type,
                "result_status": status,
                "target_type": contract.get("target_type"),
                "target_id": contract.get("target_id"),
                "correlation_id": (context or {}).get("correlation_id") or contract.get("correlation_id"),
                "actor": actor,
                "reason": reason,
                "persisted": False,
                "declarative_only": True,
            }
        )
    return events


def _boundary_summary(contract: dict[str, Any]) -> dict[str, bool]:
    summary = dict(BOUNDARY_FIELDS)
    contract_summary = contract.get("boundary_summary") or {}
    for key in summary:
        summary[key] = bool(contract_summary.get(f"{key}_enabled", False))
    return summary


def _blocked_side_effects() -> list[str]:
    return [
        "execution_attempt",
        "execution_attempt_store",
        "dry_run_store",
        "agent_execution",
        "team_execution",
        "model_invocation",
        "tool_execution",
        "memory_persistence",
        "external_access",
        "ui_trigger",
        "integration_trigger",
        "scheduler",
        "worker_queue",
        "state_mutation",
        "artifact_mutation",
    ]


def _evidence(contract: dict[str, Any], audit_ref: dict[str, Any], status: str) -> list[dict[str, Any]]:
    return [
        {"evidence_id": "dry_run_contract_ref", "contract_id": contract.get("contract_id"), "status": contract.get("status")},
        {"evidence_id": "simulated_plan_ref", "simulated_plan_id": contract.get("plan_contract", {}).get("simulated_plan_id")},
        {"evidence_id": "audit_store_verified", "verified": audit_ref.get("verification", {}).get("verified") is True},
        {"evidence_id": "result_only_boundary", "status": status, "persistent_store_created": False},
    ]


def _side_effect_code(field: str) -> str:
    return {
        "network_call_allowed": "forbidden_external_access",
        "tool_call_allowed": "forbidden_tool_execution",
        "memory_write_allowed": "forbidden_memory_persistence",
    }.get(field, "mutation_not_allowed" if "mutation" in field or "write" in field else "forbidden_side_effects")


def _block(blockers: list[dict[str, str]], code: str, message: str, severity: str = "error") -> None:
    if not any(blocker["code"] == code and blocker["message"] == message for blocker in blockers):
        blockers.append({"code": code, "message": message, "severity": severity})


def _validate_result(result: dict[str, Any]) -> None:
    if result.get("status") not in ALLOWED_STATUSES:
        raise ValueError(f"dry_run status invalido: {result.get('status')}")
    event_types = {event.get("event_type") for event in result.get("audit_events", [])}
    forbidden = sorted(event_types & PROHIBITED_EVENTS)
    if forbidden:
        raise ValueError(f"dry_run result contiene eventos prohibidos: {', '.join(forbidden)}")
