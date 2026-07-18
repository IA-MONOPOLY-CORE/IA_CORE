"""Helpers no mutantes de observability y correlacion."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from datetime import datetime
from typing import Any

from core.audit_persistence_schema import validate_audit_store_contract
from core.observability_schema import MINIMUM_EVENT_TYPES, build_observability_event, validate_observability_event


MINIMUM_METRICS = {
    "events_total",
    "events_by_type",
    "blocked_operations_total",
    "successful_operations_total",
    "rollback_operations_total",
    "runtime_boundary_violations_total",
    "mutation_scope_violations_total",
    "missing_evidence_total",
    "invalid_correlation_total",
    "last_event_at",
}


def build_observability_context(
    *,
    correlation_id: str,
    causation_id: str | None = None,
    actor: str = "system_service",
    actor_type: str = "service",
    domain_id: str | None = None,
    operation: str,
    requested_status: str | None = None,
    runtime_mode: str | None = None,
    contract_refs: dict[str, Any] | None = None,
    approval_refs: dict[str, Any] | None = None,
    audit_refs: dict[str, Any] | None = None,
    audit_store_path: str | None = None,
    persist_events: bool = False,
    verify_after_write: bool | None = None,
) -> dict[str, Any]:
    resolved_verify_after_write = persist_events if verify_after_write is None else verify_after_write
    context = {
        "correlation_id": correlation_id,
        "causation_id": causation_id,
        "actor": actor,
        "actor_type": actor_type,
        "domain_id": domain_id,
        "operation": operation,
        "requested_status": requested_status,
        "runtime_mode": runtime_mode,
        "contract_refs": dict(contract_refs or {}),
        "approval_refs": dict(approval_refs or {}),
        "audit_refs": dict(audit_refs or {}),
        "audit_store_path": audit_store_path,
        "persist_events": persist_events,
        "verify_after_write": resolved_verify_after_write,
    }
    return validate_observability_context(context)


def validate_observability_context(context: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("observability_context debe ser un objeto")
    for field in ["correlation_id", "actor", "actor_type", "operation"]:
        if not isinstance(context.get(field), str) or not context[field].strip():
            raise ValueError(f"observability_context requiere {field}")
    for field in ["contract_refs", "approval_refs", "audit_refs"]:
        if not isinstance(context.get(field, {}), dict):
            raise ValueError(f"observability_context.{field} debe ser objeto")
    if context.get("audit_store_path") is not None and not isinstance(context.get("audit_store_path"), str):
        raise ValueError("observability_context.audit_store_path debe ser texto")
    for field in ["persist_events", "verify_after_write"]:
        if field in context and not isinstance(context.get(field), bool):
            raise ValueError(f"observability_context.{field} debe ser booleano")
    return deepcopy(context)


def build_snapshot_ref(
    before_snapshot: dict[str, Any],
    after_snapshot: dict[str, Any],
    *,
    mutation_scope: str,
    rollback_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    changed = sorted(
        key
        for key in set(before_snapshot) | set(after_snapshot)
        if before_snapshot.get(key) != after_snapshot.get(key)
    )
    snapshot = {
        "before_snapshot": deepcopy(before_snapshot),
        "after_snapshot": deepcopy(after_snapshot),
        "diff_summary": {"changed": changed},
        "mutation_scope": mutation_scope,
        "rollback_snapshot": deepcopy(rollback_snapshot if rollback_snapshot is not None else before_snapshot),
    }
    snapshot["checksum"] = _checksum(snapshot)
    return snapshot


def build_observability_event_from_context(
    *,
    context: dict[str, Any] | None,
    event_type: str,
    source_module: str,
    target_type: str,
    target_id: str,
    domain_id: str,
    operation_phase: str,
    result_status: str,
    evidence_refs: dict[str, Any],
    requested_status: str | None = None,
    previous_status: str | None = None,
    next_status: str | None = None,
    mutation_scope: str = "none",
    snapshot_refs: dict[str, Any] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    runtime_enabled: bool = False,
    execution_enabled: bool = False,
    external_access: bool = False,
    tool_execution_enabled: bool = False,
    memory_persistence_enabled: bool = False,
) -> dict[str, Any] | None:
    if context is None:
        return None
    ctx = validate_observability_context(context)
    event_id = f"event_{event_type}_{target_type}_{target_id}_{_short_stamp()}"
    return build_observability_event(
        event_id=event_id,
        correlation_id=ctx["correlation_id"],
        causation_id=ctx.get("causation_id"),
        event_type=event_type,
        actor=ctx["actor"],
        actor_type=ctx["actor_type"],
        source_module=source_module,
        target_type=target_type,
        target_id=target_id,
        domain_id=ctx.get("domain_id") or domain_id,
        operation=ctx["operation"],
        operation_phase=operation_phase,
        result_status=result_status,
        requested_status=requested_status or ctx.get("requested_status") or ctx.get("runtime_mode"),
        previous_status=previous_status,
        next_status=next_status,
        mutation_scope=mutation_scope,
        runtime_flags={"runtime_enabled": runtime_enabled, "runtime_allowed": False},
        execution_flags={"execution_enabled": execution_enabled, "execution_allowed": False},
        external_access_flags={"external_access": external_access, "external_access_enabled": external_access},
        tool_memory_flags={
            "tool_execution_enabled": tool_execution_enabled,
            "memory_persistence_enabled": memory_persistence_enabled,
        },
        evidence_refs=evidence_refs,
        approval_refs=ctx.get("approval_refs") or {},
        contract_refs=ctx.get("contract_refs") or {},
        audit_refs=ctx.get("audit_refs") or {},
        snapshot_refs=snapshot_refs or {},
        blockers=blockers or [],
        warnings=warnings or [],
        rollback_available=event_type in {"promotion_executed", "active_executed"},
        rollback_ref=f"rollback_{event_id}" if event_type in {"promotion_executed", "active_executed"} else None,
    )


def validate_event_correlation(
    events: list[dict[str, Any]],
    *,
    correlation_id: str,
    target_type: str,
    target_id: str,
    domain_id: str,
    operation: str,
    requested_status: str | None = None,
    contract_ref: str | None = None,
) -> list[dict[str, Any]]:
    """Valida que los eventos pertenezcan al mismo flujo esperado."""
    validated = [validate_observability_event(event) for event in events]
    if not validated:
        raise ValueError("events requerido")
    for event in validated:
        if event["correlation_id"] != correlation_id:
            raise ValueError("correlation_id cruzado")
        if event["target_type"] != target_type or event["target_id"] != target_id:
            raise ValueError("target cruzado")
        if event["domain_id"] != domain_id:
            raise ValueError("domain cruzado")
        if event["operation"] != operation:
            raise ValueError("operation cruzada")
        if requested_status is not None and event["requested_status"] != requested_status:
            raise ValueError("requested_status cruzado")
        if contract_ref is not None:
            contract_refs = set(str(value) for value in event.get("contract_refs", {}).values())
            if contract_ref not in contract_refs:
                raise ValueError("contract_ref cruzado")
    return deepcopy(validated)


def validate_reference_belongs_to_event(event: dict[str, Any], *, ref_group: str, ref_key: str, expected_value: str) -> dict[str, Any]:
    """Evita reusar approvals/contracts/audits de otro target o contrato."""
    validated = validate_observability_event(event)
    refs = validated.get(ref_group)
    if not isinstance(refs, dict):
        raise ValueError(f"{ref_group} inexistente")
    if refs.get(ref_key) != expected_value:
        raise ValueError(f"{ref_group}.{ref_key} cruzado")
    return validated


def record_observability_events(events: list[dict[str, Any]], observability_context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Persiste eventos en audit store solo si el context lo solicita."""
    validated_events = [validate_observability_event(event) for event in events]
    if observability_context is None:
        return {
            "persisted": False,
            "reason": "observability_context_missing",
            "events": deepcopy(validated_events),
            "records": [],
        }
    context = validate_observability_context(observability_context)
    if not context.get("persist_events"):
        return {
            "persisted": False,
            "reason": "persist_events_false",
            "events": deepcopy(validated_events),
            "records": [],
        }
    audit_store_path = context.get("audit_store_path")
    if not audit_store_path:
        return {
            "persisted": False,
            "reason": "audit_store_path_missing",
            "events": deepcopy(validated_events),
            "records": [],
        }

    try:
        from core.audit_store import append_audit_event, verify_audit_store

        records = [append_audit_event(audit_store_path, event) for event in validated_events]
        verification = verify_audit_store(audit_store_path) if context.get("verify_after_write", True) else None
    except Exception as exc:  # noqa: BLE001
        return {
            "persisted": False,
            "reason": "audit_store_error",
            "error": str(exc),
            "events": deepcopy(validated_events),
            "records": [],
        }
    return {
        "persisted": True,
        "reason": "persisted",
        "events": deepcopy(validated_events),
        "records": records,
        "verification": verification,
    }


def summarize_observability_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Devuelve metricas minimas sin persistir ni mutar eventos."""
    validated = [validate_observability_event(event) for event in events]
    events_by_type = Counter(event["event_type"] for event in validated)
    return {
        "events_total": len(validated),
        "events_by_type": dict(events_by_type),
        "blocked_operations_total": sum(1 for event in validated if event["result_status"] == "blocked"),
        "successful_operations_total": sum(1 for event in validated if event["result_status"] in {"passed", "applied", "recorded"}),
        "rollback_operations_total": sum(1 for event in validated if "rollback" in event["event_type"]),
        "runtime_boundary_violations_total": events_by_type.get("runtime_boundary_violation", 0),
        "mutation_scope_violations_total": sum(
            1
            for event in validated
            if event["event_type"] == "mutation_scope_verified" and event["result_status"] == "blocked"
        ),
        "missing_evidence_total": sum(
            1
            for event in validated
            if not event["evidence_refs"] or any("evidence" in blocker for blocker in event["blockers"])
        ),
        "invalid_correlation_total": sum(
            1
            for event in validated
            if any("correlation" in blocker for blocker in event["blockers"])
        ),
        "last_event_at": max((event["timestamp"] for event in validated), default=None),
    }


def validate_observability_store(store: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    """Valida contrato de store local seguro contra eventos observables."""
    validated_store = validate_audit_store_contract(store)
    validated_events = [validate_observability_event(event) for event in events]
    if validated_store["event_count"] != len(validated_events):
        raise ValueError("event_count no coincide con eventos")
    return {
        "store": validated_store,
        "events": validated_events,
        "minimum_event_types": sorted(MINIMUM_EVENT_TYPES),
        "minimum_metrics": sorted(MINIMUM_METRICS),
    }


def _checksum(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _short_stamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")
