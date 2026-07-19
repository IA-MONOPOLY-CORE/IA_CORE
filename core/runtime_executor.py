"""Runtime executor prepare-only.

Este modulo prepara runtime de forma declarativa. No ejecuta agentes/equipos,
no invoca modelos, no ejecuta tools y no persiste memoria real.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from core.audit_store import append_audit_event, read_audit_events, verify_audit_store
from core.observability import validate_observability_context
from core.observability_schema import build_observability_event
from core.runtime_executor_schema import ALLOWED_TARGET_TYPES, validate_runtime_executor_contract_report


ALLOWED_STATUSES = {"prepared", "blocked", "aborted", "rolled_back", "noop_idempotent"}
FORBIDDEN_EXECUTION_EVENTS = {
    "runtime_execution_started",
    "execution_runner_started",
    "agent_executed",
    "team_executed",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
}
_ACTIVE_PREPARATIONS: set[tuple[str, str]] = set()


def prepare_runtime(
    *,
    target_type: str,
    target_id: str,
    runtime_contract_result: dict[str, Any] | None,
    execution_contract_result: dict[str, Any] | None,
    runtime_executor_contract_result: dict[str, Any] | None,
    observability_context: dict[str, Any] | None,
    audit_store_path: str | Path | None,
    correlation_id: str | None = None,
    idempotency_key: str | None = None,
    actor: str = "runtime_executor_prepare_only",
    reason: str = "prepare runtime declaratively",
    lock_registry: set[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    """Prepara runtime declarativo, registra audit/observability y no ejecuta nada."""
    registry = _ACTIVE_PREPARATIONS if lock_registry is None else lock_registry
    target_key = (target_type, target_id)
    blockers: list[str] = []
    warnings: list[str] = []
    context = _validate_context(observability_context, blockers)
    resolved_correlation_id = correlation_id or (context or {}).get("correlation_id")
    resolved_idempotency_key = idempotency_key
    contract = _validate_runtime_executor_contract(runtime_executor_contract_result, blockers)
    runtime_contract_id = _contract_id(runtime_contract_result, "runtime_contract_id")
    execution_contract_id = _contract_id(execution_contract_result, "execution_contract_id")
    runtime_executor_contract_id = _contract_id(runtime_executor_contract_result, "runtime_executor_contract_id")
    domain_id = (contract or {}).get("domain_id") or (context or {}).get("domain_id") or "unknown_domain"
    audit_events: list[dict[str, Any]] = []

    if target_type not in ALLOWED_TARGET_TYPES:
        blockers.append(f"target_type sin runtime executor directo: {target_type}")
    if not target_id:
        blockers.append("target_id requerido")
    if not resolved_correlation_id:
        blockers.append("correlation_id requerido")
    if not resolved_idempotency_key:
        blockers.append("idempotency_key requerido")
    if runtime_contract_result is None:
        blockers.append("runtime_contract requerido")
    elif runtime_contract_result.get("contract_result") != "passed":
        blockers.append("runtime_contract debe estar passed")
    if execution_contract_result is None:
        blockers.append("execution_contract requerido")
    elif execution_contract_result.get("contract_result") != "passed":
        blockers.append("execution_contract debe estar passed")
    if contract and contract.get("blockers"):
        blockers.append("runtime_executor_contract debe estar passed")
    if contract and contract.get("runtime_executor_mode") != "prepare_only":
        blockers.append(f"runtime_executor_mode bloqueado en esta fase: {contract.get('runtime_executor_mode')}")
    if contract:
        _validate_contract_boundaries(contract, blockers)
        if resolved_idempotency_key is None:
            resolved_idempotency_key = contract.get("idempotency_key")

    store_path = Path(audit_store_path) if audit_store_path is not None else None
    existing_events: list[dict[str, Any]] = []
    if store_path is None:
        blockers.append("audit_store requerido")
    else:
        try:
            verify_audit_store(store_path)
            existing_events = read_audit_events(store_path)
            _ensure_no_forbidden_events(existing_events)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"audit_store invalido: {exc}")

    if context and resolved_correlation_id and context["correlation_id"] != resolved_correlation_id:
        blockers.append("correlation_id cruzado")
    if contract and resolved_correlation_id and contract.get("correlation_id") != resolved_correlation_id:
        blockers.append("runtime_executor_contract correlation_id cruzado")
    if contract and resolved_idempotency_key and contract.get("idempotency_key") != resolved_idempotency_key:
        blockers.append("runtime_executor_contract idempotency_key cruzado")
    if contract:
        _validate_contract_identity(
            runtime_contract_result,
            contract,
            contract_name="runtime_contract",
            id_field="runtime_contract_id",
            blockers=blockers,
        )
        _validate_contract_identity(
            execution_contract_result,
            contract,
            contract_name="execution_contract",
            id_field="execution_contract_id",
            blockers=blockers,
        )

    if blockers:
        result = _result(
            status="blocked",
            target_type=target_type,
            target_id=target_id,
            correlation_id=resolved_correlation_id,
            idempotency_key=resolved_idempotency_key,
            runtime_contract_id=runtime_contract_id,
            execution_contract_id=execution_contract_id,
            runtime_executor_contract_id=runtime_executor_contract_id,
            runtime_executor_contract_result=contract,
            audit_event_refs=[],
            observability_event_refs=[],
            mutation_summary=_mutation_summary(),
            boundary_summary=_boundary_summary(),
            blockers=blockers,
            warnings=warnings,
        )
        _append_if_possible(
            store_path=store_path,
            context=context,
            event_type="runtime_prepare_blocked",
            result_status="blocked",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            actor=actor,
            reason=reason,
            idempotency_key=resolved_idempotency_key,
            preparation_id=result["preparation_id"],
            contract_ids=(runtime_contract_id, execution_contract_id, runtime_executor_contract_id),
            blockers=blockers,
            audit_events=audit_events,
        )
        result["audit_event_refs"] = _event_refs(audit_events)
        result["observability_event_refs"] = _event_refs(audit_events)
        return result

    assert store_path is not None
    assert context is not None
    assert resolved_correlation_id is not None
    assert resolved_idempotency_key is not None
    if _has_completed_preparation(
        existing_events,
        target_type=target_type,
        target_id=target_id,
        correlation_id=resolved_correlation_id,
        idempotency_key=resolved_idempotency_key,
    ):
        result = _result(
            status="noop_idempotent",
            target_type=target_type,
            target_id=target_id,
            correlation_id=resolved_correlation_id,
            idempotency_key=resolved_idempotency_key,
            runtime_contract_id=runtime_contract_id,
            execution_contract_id=execution_contract_id,
            runtime_executor_contract_id=runtime_executor_contract_id,
            runtime_executor_contract_result=contract,
            audit_event_refs=[],
            observability_event_refs=[],
            mutation_summary=_mutation_summary(),
            boundary_summary=_boundary_summary(),
            blockers=[],
            warnings=["runtime_prepare_idempotent_replay"],
        )
        _append_event(
            store_path=store_path,
            context=context,
            event_type="runtime_prepare_idempotent_replay",
            result_status="recorded",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            actor=actor,
            reason=reason,
            idempotency_key=resolved_idempotency_key,
            preparation_id=result["preparation_id"],
            contract_ids=(runtime_contract_id, execution_contract_id, runtime_executor_contract_id),
            blockers=[],
            audit_events=audit_events,
        )
        result["audit_event_refs"] = _event_refs(audit_events)
        result["observability_event_refs"] = _event_refs(audit_events)
        return result

    if target_key in registry:
        result = _result(
            status="blocked",
            target_type=target_type,
            target_id=target_id,
            correlation_id=resolved_correlation_id,
            idempotency_key=resolved_idempotency_key,
            runtime_contract_id=runtime_contract_id,
            execution_contract_id=execution_contract_id,
            runtime_executor_contract_id=runtime_executor_contract_id,
            runtime_executor_contract_result=contract,
            audit_event_refs=[],
            observability_event_refs=[],
            mutation_summary=_mutation_summary(),
            boundary_summary=_boundary_summary(),
            blockers=["runtime_preparation_lock_conflict"],
            warnings=[],
        )
        _append_event(
            store_path=store_path,
            context=context,
            event_type="runtime_prepare_blocked",
            result_status="blocked",
            target_type=target_type,
            target_id=target_id,
            domain_id=domain_id,
            actor=actor,
            reason=reason,
            idempotency_key=resolved_idempotency_key,
            preparation_id=result["preparation_id"],
            contract_ids=(runtime_contract_id, execution_contract_id, runtime_executor_contract_id),
            blockers=result["blockers"],
            audit_events=audit_events,
        )
        result["audit_event_refs"] = _event_refs(audit_events)
        result["observability_event_refs"] = _event_refs(audit_events)
        return result

    registry.add(target_key)
    try:
        result = _result(
            status="prepared",
            target_type=target_type,
            target_id=target_id,
            correlation_id=resolved_correlation_id,
            idempotency_key=resolved_idempotency_key,
            runtime_contract_id=runtime_contract_id,
            execution_contract_id=execution_contract_id,
            runtime_executor_contract_id=runtime_executor_contract_id,
            runtime_executor_contract_result=contract,
            audit_event_refs=[],
            observability_event_refs=[],
            mutation_summary=_mutation_summary(),
            boundary_summary=_boundary_summary(),
            blockers=[],
            warnings=[],
        )
        for event_type, result_status in [
            ("runtime_prepare_started", "recorded"),
            ("runtime_prepare_validated", "passed"),
            ("runtime_prepare_completed", "passed"),
            ("mutation_scope_verified", "passed"),
        ]:
            _append_event(
                store_path=store_path,
                context=context,
                event_type=event_type,
                result_status=result_status,
                target_type=target_type,
                target_id=target_id,
                domain_id=domain_id,
                actor=actor,
                reason=reason,
                idempotency_key=resolved_idempotency_key,
                preparation_id=result["preparation_id"],
                contract_ids=(runtime_contract_id, execution_contract_id, runtime_executor_contract_id),
                blockers=[],
                audit_events=audit_events,
            )
        result["audit_event_refs"] = _event_refs(audit_events)
        result["observability_event_refs"] = _event_refs(audit_events)
        result["audit_store_verification"] = verify_audit_store(store_path)
        return result
    finally:
        registry.discard(target_key)


def abort_runtime_preparation(
    *,
    preparation_result: dict[str, Any],
    observability_context: dict[str, Any],
    audit_store_path: str | Path,
    actor: str = "runtime_executor_prepare_only",
    reason: str = "abort runtime preparation",
) -> dict[str, Any]:
    """Registra abort declarativo; no revierte ni toca targets."""
    return _terminal_preparation_event(
        preparation_result=preparation_result,
        observability_context=observability_context,
        audit_store_path=audit_store_path,
        actor=actor,
        reason=reason,
        status="aborted",
        event_type="runtime_prepare_aborted",
        result_status="recorded",
    )


def rollback_runtime_preparation(
    *,
    preparation_result: dict[str, Any],
    observability_context: dict[str, Any],
    audit_store_path: str | Path,
    actor: str = "runtime_executor_prepare_only",
    reason: str = "rollback runtime preparation",
) -> dict[str, Any]:
    """Registra rollback declarativo; su alcance es metadata/audit solamente."""
    return _terminal_preparation_event(
        preparation_result=preparation_result,
        observability_context=observability_context,
        audit_store_path=audit_store_path,
        actor=actor,
        reason=reason,
        status="rolled_back",
        event_type="runtime_prepare_rolled_back",
        result_status="rolled_back",
    )


def _terminal_preparation_event(
    *,
    preparation_result: dict[str, Any],
    observability_context: dict[str, Any],
    audit_store_path: str | Path,
    actor: str,
    reason: str,
    status: str,
    event_type: str,
    result_status: str,
) -> dict[str, Any]:
    blockers: list[str] = []
    context = _validate_context(observability_context, blockers)
    store_path = Path(audit_store_path)
    try:
        verify_audit_store(store_path)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"audit_store invalido: {exc}")
    if preparation_result.get("status") not in {"prepared", "noop_idempotent", "blocked", "aborted", "rolled_back"}:
        blockers.append("preparation_result invalido")
    if blockers or context is None:
        return _result(
            status="blocked",
            target_type=preparation_result.get("target_type", "agent"),
            target_id=preparation_result.get("target_id", "unknown_target"),
            correlation_id=preparation_result.get("correlation_id"),
            idempotency_key=preparation_result.get("idempotency_key"),
            runtime_contract_id=preparation_result.get("runtime_contract_id", "unknown_runtime_contract"),
            execution_contract_id=preparation_result.get("execution_contract_id", "unknown_execution_contract"),
            runtime_executor_contract_id=preparation_result.get("runtime_executor_contract_id", "unknown_runtime_executor_contract"),
            runtime_executor_contract_result=preparation_result.get("runtime_executor_contract_result", {}),
            audit_event_refs=[],
            observability_event_refs=[],
            mutation_summary=_mutation_summary(),
            boundary_summary=_boundary_summary(),
            blockers=blockers,
            warnings=[],
        )

    audit_events: list[dict[str, Any]] = []
    result = _result(
        status=status,
        target_type=preparation_result["target_type"],
        target_id=preparation_result["target_id"],
        correlation_id=preparation_result["correlation_id"],
        idempotency_key=preparation_result["idempotency_key"],
        runtime_contract_id=preparation_result["runtime_contract_id"],
        execution_contract_id=preparation_result["execution_contract_id"],
        runtime_executor_contract_id=preparation_result["runtime_executor_contract_id"],
        runtime_executor_contract_result=preparation_result.get("runtime_executor_contract_result", {}),
        audit_event_refs=[],
        observability_event_refs=[],
        mutation_summary=_mutation_summary(),
        boundary_summary=_boundary_summary(),
        blockers=[],
        warnings=[],
    )
    _append_event(
        store_path=store_path,
        context=context,
        event_type=event_type,
        result_status=result_status,
        target_type=result["target_type"],
        target_id=result["target_id"],
        domain_id=preparation_result.get("domain_id") or context.get("domain_id") or "unknown_domain",
        actor=actor,
        reason=reason,
        idempotency_key=result["idempotency_key"],
        preparation_id=result["preparation_id"],
        contract_ids=(result["runtime_contract_id"], result["execution_contract_id"], result["runtime_executor_contract_id"]),
        blockers=[],
        audit_events=audit_events,
    )
    result["audit_event_refs"] = _event_refs(audit_events)
    result["observability_event_refs"] = _event_refs(audit_events)
    result["audit_store_verification"] = verify_audit_store(store_path)
    return result


def _validate_context(context: dict[str, Any] | None, blockers: list[str]) -> dict[str, Any] | None:
    if context is None:
        blockers.append("observability_context requerido")
        return None
    try:
        return validate_observability_context(context)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"observability_context invalido: {exc}")
        return None


def _validate_runtime_executor_contract(contract: dict[str, Any] | None, blockers: list[str]) -> dict[str, Any] | None:
    if contract is None:
        blockers.append("runtime_executor_contract requerido")
        return None
    try:
        validated = validate_runtime_executor_contract_report(contract)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"runtime_executor_contract invalido: {exc}")
        return None
    if validated["blockers"]:
        blockers.append("runtime_executor_contract debe estar passed")
    return validated


def _validate_contract_boundaries(contract: dict[str, Any], blockers: list[str]) -> None:
    if contract["runtime_executor_enabled"] is not False:
        blockers.append("runtime_executor_enabled=true bloqueado")
    if contract["runtime_execution_enabled"] is not False:
        blockers.append("runtime_execution_enabled=true bloqueado")
    if contract["execution_runner_enabled"] is not False:
        blockers.append("execution_runner_enabled=true bloqueado")
    for field, enabled in contract.get("boundary_policy", {}).items():
        if enabled is not False:
            blockers.append(f"{field}=true bloqueado")
    if contract.get("mutation_policy", {}).get("mutations_allowed") is not False:
        blockers.append("mutations_allowed debe ser false")


def _validate_contract_identity(
    payload: dict[str, Any] | None,
    runtime_executor_contract: dict[str, Any],
    *,
    contract_name: str,
    id_field: str,
    blockers: list[str],
) -> None:
    if not isinstance(payload, dict):
        return
    for field in ["target_type", "target_id", "domain_id"]:
        if payload.get(field) != runtime_executor_contract.get(field):
            blockers.append(f"{contract_name} corresponde a otro {field}")
    if payload.get(id_field) != runtime_executor_contract.get(id_field):
        blockers.append(f"{contract_name} corresponde a otro contrato")


def _append_if_possible(**kwargs: Any) -> None:
    if kwargs["store_path"] is not None and kwargs["context"] is not None:
        try:
            _append_event(**kwargs)
        except Exception:  # noqa: BLE001
            return


def _append_event(
    *,
    store_path: Path,
    context: dict[str, Any],
    event_type: str,
    result_status: str,
    target_type: str,
    target_id: str,
    domain_id: str,
    actor: str,
    reason: str,
    idempotency_key: str | None,
    preparation_id: str,
    contract_ids: tuple[str, str, str],
    blockers: list[str],
    audit_events: list[dict[str, Any]],
) -> None:
    event = build_observability_event(
        event_id=f"event_{event_type}_{target_type}_{target_id}_{len(read_audit_events(store_path)) + 1}",
        correlation_id=context["correlation_id"],
        causation_id=context.get("causation_id"),
        event_type=event_type,
        actor=actor,
        actor_type=context.get("actor_type") or "service",
        source_module="core.runtime_executor",
        target_type=target_type,
        target_id=target_id,
        domain_id=domain_id,
        operation=context["operation"],
        operation_phase="verification",
        result_status=result_status,
        requested_status="prepare_only",
        previous_status="active",
        next_status="active",
        mutation_scope="none",
        runtime_flags={"runtime_enabled": False, "runtime_allowed": False},
        execution_flags={"execution_enabled": False, "execution_allowed": False},
        external_access_flags={"external_access": False, "external_access_enabled": False},
        tool_memory_flags={"tool_execution_enabled": False, "memory_persistence_enabled": False},
        evidence_refs={
            "preparation_id": preparation_id,
            "idempotency_key": idempotency_key or "missing_idempotency_key",
            "reason": reason,
        },
        contract_refs={
            "runtime_contract_id": contract_ids[0],
            "execution_contract_id": contract_ids[1],
            "runtime_executor_contract_id": contract_ids[2],
        },
        blockers=blockers,
    )
    record = append_audit_event(store_path, event)
    audit_events.append(record)
    _ensure_no_forbidden_events([record])


def _has_completed_preparation(
    events: list[dict[str, Any]],
    *,
    target_type: str,
    target_id: str,
    correlation_id: str,
    idempotency_key: str,
) -> bool:
    return any(
        event.get("event_type") == "runtime_prepare_completed"
        and event.get("target_type") == target_type
        and event.get("target_id") == target_id
        and event.get("correlation_id") == correlation_id
        and event.get("evidence_refs", {}).get("idempotency_key") == idempotency_key
        for event in events
    )


def _ensure_no_forbidden_events(events: list[dict[str, Any]]) -> None:
    found = sorted({event.get("event_type") for event in events} & FORBIDDEN_EXECUTION_EVENTS)
    if found:
        raise ValueError(f"eventos de ejecucion prohibidos: {', '.join(found)}")


def _result(
    *,
    status: str,
    target_type: str,
    target_id: str,
    correlation_id: str | None,
    idempotency_key: str | None,
    runtime_contract_id: str,
    execution_contract_id: str,
    runtime_executor_contract_id: str,
    runtime_executor_contract_result: dict[str, Any] | None,
    audit_event_refs: list[dict[str, Any]],
    observability_event_refs: list[dict[str, Any]],
    mutation_summary: dict[str, Any],
    boundary_summary: dict[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"status invalido: {status}")
    preparation_id = f"runtime_preparation_{target_type}_{target_id}_{idempotency_key or 'missing_idempotency_key'}"
    contract = dict(runtime_executor_contract_result or {})
    return {
        "preparation_id": preparation_id,
        "target_type": target_type,
        "target_id": target_id,
        "mode": "prepare_only",
        "status": status,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "domain_id": contract.get("domain_id"),
        "runtime_contract_id": runtime_contract_id,
        "execution_contract_id": execution_contract_id,
        "runtime_executor_contract_id": runtime_executor_contract_id,
        "runtime_executor_contract_result": contract,
        "preparation_plan_ref": contract.get("preparation_plan", {}),
        "abort_plan_ref": contract.get("abort_plan", {}),
        "rollback_plan_ref": contract.get("rollback_plan", {}),
        "audit_event_refs": audit_event_refs,
        "observability_event_refs": observability_event_refs,
        "mutation_summary": mutation_summary,
        "boundary_summary": boundary_summary,
        "blockers": list(blockers),
        "warnings": list(warnings),
        "created_at": datetime.now().isoformat(),
    }


def _mutation_summary() -> dict[str, Any]:
    return {
        "mutation_scope": "audit_and_observability_metadata_only",
        "target_status_mutated": False,
        "artifact_state_mutated": False,
        "runtime_flags_mutated": False,
        "legacy_or_global_paths_mutated": False,
    }


def _boundary_summary() -> dict[str, bool]:
    return {
        "runtime_execution_enabled": False,
        "execution_runner_enabled": False,
        "execution_enabled": False,
        "model_invocation_enabled": False,
        "tool_execution_enabled": False,
        "memory_persistence_enabled": False,
        "external_access_enabled": False,
        "ui_touched": False,
        "integrations_touched": False,
    }


def _event_refs(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "sequence_number": event["sequence_number"],
            "checksum": event["checksum"],
        }
        for event in events
    ]


def _contract_id(contract: dict[str, Any] | None, field: str) -> str:
    if isinstance(contract, dict) and isinstance(contract.get(field), str):
        return contract[field]
    return f"missing_{field}"
