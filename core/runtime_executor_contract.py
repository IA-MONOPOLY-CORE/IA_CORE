"""Contrato prepare-only del futuro runtime executor, sin ejecucion real."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.audit_store import read_audit_events, verify_audit_store
from core.execution_contract_schema import validate_execution_contract_report
from core.observability import validate_observability_context
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.runtime_contract_schema import validate_runtime_contract_report
from core.runtime_executor_schema import (
    ALLOWED_TARGET_TYPES,
    BLOCKED_RUNTIME_EXECUTOR_MODES,
    build_runtime_executor_contract_report,
)


BLOCKED_ACTIONS = [
    "runtime_execution",
    "execution_runner",
    "model_invocation",
    "tool_execution",
    "memory_persistence",
    "external_access",
    "ui_trigger",
    "integration_runner",
]
REQUIRED_AUDIT_EVENT_TYPES = {
    "runtime_executor_contract_evaluated",
    "runtime_executor_prepare_only_validated",
    "mutation_scope_verified",
}
FORBIDDEN_AUDIT_EVENT_TYPES = {
    "runtime_executor_started",
    "runtime_execution_started",
    "execution_runner_started",
    "agent_executed",
    "team_executed",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
}


def evaluate_runtime_executor_contract(
    *,
    target_type: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    runtime_executor_mode: str = "prepare_only",
    runtime_contract_result: dict[str, Any] | None = None,
    execution_contract_result: dict[str, Any] | None = None,
    observability_context: dict[str, Any] | None = None,
    audit_store_path: str | Path | None = None,
    preparation_plan: dict[str, Any] | None = None,
    abort_plan: dict[str, Any] | None = None,
    rollback_plan: dict[str, Any] | None = None,
    idempotency_key: str | None = None,
    lock_policy: dict[str, Any] | None = None,
    concurrency_policy: dict[str, Any] | None = None,
    mutation_policy: dict[str, Any] | None = None,
    boundary_policy: dict[str, Any] | None = None,
    runtime_executor_enabled: bool = False,
    runtime_execution_enabled: bool = False,
    execution_runner_enabled: bool = False,
    evidence_refs: list[Any] | None = None,
) -> dict[str, Any]:
    """Evalua y prepara contrato; no ejecuta, no muta y no habilita runtime."""
    blockers: list[str] = []
    warnings: list[str] = []
    domain_id = "unknown_domain"
    resolved_target_id = target_id or target_type
    target_status = "unknown"
    target_payload: dict[str, Any] = {}
    runtime_contract_id = "missing_runtime_contract"
    runtime_result = "blocked"
    execution_contract_id = "missing_execution_contract"
    execution_result = "blocked"
    audit_store_ref: dict[str, Any] = {}
    correlation_id = (observability_context or {}).get("correlation_id")

    if target_type not in ALLOWED_TARGET_TYPES:
        blockers.append(f"target_type sin runtime executor directo: {target_type}")
    if runtime_executor_mode in BLOCKED_RUNTIME_EXECUTOR_MODES:
        blockers.append(f"runtime_executor_mode bloqueado en esta fase: {runtime_executor_mode}")
    elif runtime_executor_mode != "prepare_only":
        blockers.append(f"runtime_executor_mode invalido para esta fase: {runtime_executor_mode}")

    try:
        target_status, resolved_target_id, domain_id, target_payload = _resolve_target(
            target_type=target_type,
            domain_dir=domain_dir,
            target_id=target_id,
        )
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"target invalido: {exc}")

    if target_status != "active":
        blockers.append("target debe estar active")
    if target_status in {"legacy", "broken", "archived"}:
        blockers.append(f"current_status bloqueado: {target_status}")

    flags = _boundary_flags(target_payload)
    for flag, enabled in flags.items():
        if enabled:
            blockers.append(f"{flag}=true bloqueado")

    if runtime_contract_result is None:
        blockers.append("runtime_contract requerido")
    else:
        try:
            runtime = validate_runtime_contract_report(runtime_contract_result)
            runtime_contract_id = runtime["runtime_contract_id"]
            runtime_result = runtime["contract_result"]
            _validate_runtime_contract(runtime, target_type=target_type, target_id=resolved_target_id, domain_id=domain_id)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"runtime_contract invalido: {exc}")

    if execution_contract_result is None:
        blockers.append("execution_contract requerido")
    else:
        try:
            execution = validate_execution_contract_report(execution_contract_result)
            execution_contract_id = execution["execution_contract_id"]
            execution_result = execution["contract_result"]
            _validate_execution_contract(execution, target_type=target_type, target_id=resolved_target_id, domain_id=domain_id)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"execution_contract invalido: {exc}")

    if observability_context is None:
        blockers.append("observability_context requerido")
    else:
        try:
            context = validate_observability_context(observability_context)
            correlation_id = context["correlation_id"]
        except Exception as exc:  # noqa: BLE001
            correlation_id = None
            blockers.append(f"observability_context invalido: {exc}")

    if not correlation_id:
        blockers.append("correlation_id requerido")

    if audit_store_path is None:
        blockers.append("audit_store requerido")
    else:
        try:
            verification = verify_audit_store(audit_store_path)
            events = read_audit_events(audit_store_path)
            _validate_audit_store_events(
                events,
                target_type=target_type,
                target_id=resolved_target_id,
                domain_id=domain_id,
                correlation_id=correlation_id,
                operation=(observability_context or {}).get("operation"),
            )
            audit_store_ref = {"audit_store_path": str(audit_store_path), "verification": verification, "event_count": len(events)}
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"audit_store invalido: {exc}")

    _validate_required_plan(preparation_plan, "preparation_plan", blockers, _validate_preparation_plan)
    _validate_required_plan(abort_plan, "abort_plan", blockers, _validate_abort_plan)
    _validate_required_plan(rollback_plan, "rollback_plan", blockers, _validate_rollback_plan)
    if not idempotency_key:
        blockers.append("idempotency_key requerido")
    _validate_required_plan(lock_policy, "lock_policy", blockers, _validate_lock_policy)
    _validate_required_plan(concurrency_policy, "concurrency_policy", blockers, _validate_concurrency_policy)
    _validate_required_plan(mutation_policy, "mutation_policy", blockers, _validate_mutation_policy)
    _validate_required_plan(boundary_policy, "boundary_policy", blockers, _validate_boundary_policy)

    for flag_name, flag_value in [
        ("runtime_executor_enabled", runtime_executor_enabled),
        ("runtime_execution_enabled", runtime_execution_enabled),
        ("execution_runner_enabled", execution_runner_enabled),
    ]:
        if flag_value is True:
            blockers.append(f"{flag_name}=true bloqueado")

    return build_runtime_executor_contract_report(
        runtime_executor_contract_id=f"runtime_executor_contract_{target_type}_{resolved_target_id}",
        domain_id=domain_id,
        target_type=target_type if target_type else "agent",
        target_id=resolved_target_id,
        target_status=target_status,
        runtime_executor_mode=runtime_executor_mode,
        runtime_executor_allowed=False,
        runtime_executor_enabled=runtime_executor_enabled,
        runtime_execution_enabled=runtime_execution_enabled,
        execution_runner_enabled=execution_runner_enabled,
        runtime_contract_id=runtime_contract_id,
        runtime_contract_result=runtime_result,
        execution_contract_id=execution_contract_id,
        execution_contract_result=execution_result,
        preparation_plan=preparation_plan,
        abort_plan=abort_plan,
        rollback_plan=rollback_plan,
        required_inputs=(execution_contract_result or {}).get("input_contract", {}),
        required_outputs=(execution_contract_result or {}).get("output_contract", {}),
        required_policies={
            "timeout_policy": (execution_contract_result or {}).get("timeout_policy", {}),
            "retry_policy": (execution_contract_result or {}).get("retry_policy", {}),
            "cancellation_policy": (execution_contract_result or {}).get("cancellation_policy", {}),
            "failure_policy": (execution_contract_result or {}).get("failure_policy", {}),
        },
        required_observability={"context": observability_context or {}, "required": True},
        required_audit_store={"required": True, "verified": bool(audit_store_ref)},
        audit_store_ref=audit_store_ref,
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
        lock_policy=lock_policy,
        concurrency_policy=concurrency_policy,
        mutation_policy=mutation_policy,
        boundary_policy=boundary_policy,
        evidence_refs=list(evidence_refs or []),
        blockers=blockers,
        warnings=warnings,
    )


def build_prepare_only_plan(*, target_type: str, target_id: str, plan_id: str | None = None) -> dict[str, Any]:
    return {
        "plan_id": plan_id or f"prepare_plan_{target_type}_{target_id}",
        "mode": "prepare_only",
        "target_type": target_type,
        "target_id": target_id,
        "required_contracts": ["runtime_contract", "execution_contract"],
        "required_inputs": ["input_contract"],
        "required_outputs": ["output_contract"],
        "required_policies": ["timeout", "retry", "cancellation", "failure"],
        "required_evidence": ["observability_context", "audit_store"],
        "preflight_checks": ["target_active", "contracts_passed", "boundaries_blocked"],
        "blocked_actions": list(BLOCKED_ACTIONS),
        "expected_no_mutation": True,
        "created_at": "declarative",
    }


def build_abort_plan() -> dict[str, Any]:
    return {
        "abortable": True,
        "abort_conditions": ["preflight_failed", "boundary_violation", "audit_store_invalid"],
        "abort_result": "blocked_no_execution",
        "audit_required": True,
        "observability_required": True,
    }


def build_rollback_plan() -> dict[str, Any]:
    return {
        "rollback_required": False,
        "rollback_scope": "none",
        "rollback_allowed_mutations": [],
        "audit_required": True,
        "observability_required": True,
    }


def build_lock_policy() -> dict[str, Any]:
    return {
        "lock_required": True,
        "lock_scope": "single_target",
        "block_parallel_preparation": True,
        "real_lock_enabled": False,
    }


def build_concurrency_policy() -> dict[str, Any]:
    return {
        "concurrency_mode": "single_target_preparation",
        "parallel_targets_allowed": False,
        "queue_enabled": False,
        "scheduler_enabled": False,
    }


def build_mutation_policy() -> dict[str, Any]:
    return {
        "mutations_allowed": False,
        "allowed_mutation_scope": "none",
        "expected_no_mutation": True,
    }


def build_boundary_policy() -> dict[str, Any]:
    return {
        "runtime_enabled": False,
        "execution_enabled": False,
        "model_invocation_enabled": False,
        "tool_execution_enabled": False,
        "memory_persistence_enabled": False,
        "external_access_enabled": False,
        "ui_trigger_enabled": False,
        "integration_runner_enabled": False,
    }


def _validate_runtime_contract(runtime: dict[str, Any], *, target_type: str, target_id: str, domain_id: str) -> None:
    if runtime["contract_result"] != "passed":
        raise ValueError("runtime_contract debe estar passed")
    if runtime["target_type"] != target_type or runtime["target_id"] != target_id:
        raise ValueError("runtime_contract corresponde a otro target")
    if runtime["domain_id"] != domain_id:
        raise ValueError("runtime_contract corresponde a otro domain_id")


def _validate_execution_contract(execution: dict[str, Any], *, target_type: str, target_id: str, domain_id: str) -> None:
    if execution["contract_result"] != "passed":
        raise ValueError("execution_contract debe estar passed")
    if execution["target_type"] != target_type or execution["target_id"] != target_id:
        raise ValueError("execution_contract corresponde a otro target")
    if execution["domain_id"] != domain_id:
        raise ValueError("execution_contract corresponde a otro domain_id")
    if execution["execution_enabled"] is not False:
        raise ValueError("execution_contract execution_enabled debe ser false")
    if execution["model_invocation_contract"].get("invocation_enabled") is not False:
        raise ValueError("model invocation debe permanecer false")


def _validate_audit_store_events(
    events: list[dict[str, Any]],
    *,
    target_type: str,
    target_id: str,
    domain_id: str,
    correlation_id: str | None,
    operation: str | None,
) -> None:
    if not events:
        raise ValueError("audit_store sin eventos requeridos")
    forbidden_events = sorted({event.get("event_type") for event in events} & FORBIDDEN_AUDIT_EVENT_TYPES)
    if forbidden_events:
        raise ValueError(f"audit_store contiene eventos runtime prohibidos: {', '.join(forbidden_events)}")
    if not correlation_id:
        raise ValueError("audit_store correlation_id requerido")
    correlated = [event for event in events if event.get("correlation_id") == correlation_id]
    if not correlated:
        raise ValueError("audit_store correlation_id cruzado")
    target_events = [
        event
        for event in correlated
        if event.get("target_type") == target_type and event.get("target_id") == target_id and event.get("domain_id") == domain_id
    ]
    if not target_events:
        raise ValueError("audit_store eventos de otro target")
    if operation and not any(event.get("operation") == operation for event in target_events):
        raise ValueError("audit_store eventos de otra operation")
    event_types = {event.get("event_type") for event in target_events if event.get("operation") == operation}
    missing_event_types = REQUIRED_AUDIT_EVENT_TYPES - event_types
    if missing_event_types:
        raise ValueError(f"audit_store sin eventos requeridos: {', '.join(sorted(missing_event_types))}")
    if any(not event.get("evidence_refs") for event in target_events):
        raise ValueError("audit_store eventos sin evidence_refs")
    if any(event.get("mutation_scope") != "none" for event in target_events):
        raise ValueError("audit_store mutation_scope debe ser none")


def _validate_required_plan(value: dict[str, Any] | None, name: str, blockers: list[str], validator) -> None:
    if value is None:
        blockers.append(f"{name} requerido")
        return
    try:
        validator(value)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"{name} invalido: {exc}")


def _validate_preparation_plan(plan: dict[str, Any]) -> None:
    _require_fields(plan, "preparation_plan", {"plan_id", "mode", "target_type", "target_id", "required_contracts", "required_inputs", "required_outputs", "required_policies", "required_evidence", "preflight_checks", "blocked_actions", "expected_no_mutation", "created_at"})
    if plan["mode"] != "prepare_only":
        raise ValueError("mode debe ser prepare_only")
    missing_actions = set(BLOCKED_ACTIONS) - set(plan["blocked_actions"])
    if missing_actions:
        raise ValueError(f"blocked_actions incompleto: {', '.join(sorted(missing_actions))}")
    if plan["expected_no_mutation"] is not True:
        raise ValueError("expected_no_mutation debe ser true")


def _validate_abort_plan(plan: dict[str, Any]) -> None:
    _require_fields(plan, "abort_plan", {"abortable", "abort_conditions", "abort_result", "audit_required", "observability_required"})
    if plan["abortable"] is not True:
        raise ValueError("abortable debe ser true")
    if not isinstance(plan["abort_conditions"], list) or not plan["abort_conditions"]:
        raise ValueError("abort_conditions requerido")
    if plan["audit_required"] is not True or plan["observability_required"] is not True:
        raise ValueError("audit_required y observability_required deben ser true")


def _validate_rollback_plan(plan: dict[str, Any]) -> None:
    _require_fields(plan, "rollback_plan", {"rollback_required", "rollback_scope", "rollback_allowed_mutations", "audit_required", "observability_required"})
    if not isinstance(plan["rollback_allowed_mutations"], list):
        raise ValueError("rollback_allowed_mutations debe ser lista")
    if plan["rollback_allowed_mutations"]:
        raise ValueError("rollback_allowed_mutations debe ser vacio en prepare-only")
    if plan["audit_required"] is not True or plan["observability_required"] is not True:
        raise ValueError("audit_required y observability_required deben ser true")


def _validate_lock_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "lock_policy", {"lock_required", "lock_scope", "block_parallel_preparation", "real_lock_enabled"})
    if policy["lock_required"] is not True or policy["block_parallel_preparation"] is not True:
        raise ValueError("lock_policy debe bloquear doble preparacion simultanea")
    if policy["real_lock_enabled"] is not False:
        raise ValueError("real_lock_enabled debe ser false")


def _validate_concurrency_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "concurrency_policy", {"concurrency_mode", "parallel_targets_allowed", "queue_enabled", "scheduler_enabled"})
    if policy["concurrency_mode"] != "single_target_preparation":
        raise ValueError("concurrency_mode debe ser single_target_preparation")
    for field in ["parallel_targets_allowed", "queue_enabled", "scheduler_enabled"]:
        if policy[field] is not False:
            raise ValueError(f"{field} debe ser false")


def _validate_mutation_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "mutation_policy", {"mutations_allowed", "allowed_mutation_scope", "expected_no_mutation"})
    if policy["mutations_allowed"] is not False:
        raise ValueError("mutations_allowed debe ser false")
    if policy["allowed_mutation_scope"] != "none":
        raise ValueError("allowed_mutation_scope debe ser none")
    if policy["expected_no_mutation"] is not True:
        raise ValueError("expected_no_mutation debe ser true")


def _validate_boundary_policy(policy: dict[str, Any]) -> None:
    _require_fields(policy, "boundary_policy", set(build_boundary_policy()))
    for field, value in policy.items():
        if value is not False:
            raise ValueError(f"{field} debe ser false")


def _require_fields(payload: dict[str, Any], name: str, fields: set[str]) -> None:
    if not isinstance(payload, dict):
        raise ValueError(f"{name} debe ser objeto")
    missing = fields - set(payload)
    if missing:
        raise ValueError(f"{name} incompleto: {', '.join(sorted(missing))}")


def _resolve_target(*, target_type: str, domain_dir: str | Path | None, target_id: str | None) -> tuple[str, str, str, dict[str, Any]]:
    if target_type == "agent":
        agent_id = target_id or ""
        agent = _read_json(Path(domain_dir) / "sandbox_agents" / f"{agent_id}.json")
        return agent["status"], agent_id, agent["domain_id"], agent
    if target_type == "team":
        team_id = target_id or ""
        team = _read_json(Path(domain_dir) / "sandbox_teams" / f"{team_id}.json")
        return team["status"], team_id, team["domain_id"], team
    return "unknown", target_id or target_type, "unknown_domain", {}


def _boundary_flags(payload: dict[str, Any]) -> dict[str, bool]:
    return {
        "runtime_enabled": _nested_true(payload, "runtime_enabled"),
        "execution_enabled": _nested_true(payload, "execution_enabled") or _nested_true(payload, "operational"),
        "external_access": _nested_true(payload, "external_access") or _nested_true(payload, "external_access_enabled"),
        "tool_execution_enabled": _nested_true(payload, "tool_execution_enabled") or _nested_true(payload, "execution_allowed"),
        "memory_persistence_enabled": _nested_true(payload, "memory_persistence_enabled"),
    }


def _nested_true(value: Any, key: str) -> bool:
    if isinstance(value, dict):
        return any((item_key == key and child is True) or _nested_true(child, key) for item_key, child in value.items())
    if isinstance(value, list):
        return any(_nested_true(item, key) for item in value)
    return False


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
