"""Helpers no mutantes de observability y correlacion."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any

from core.audit_persistence_schema import validate_audit_store_contract
from core.observability_schema import MINIMUM_EVENT_TYPES, validate_observability_event


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
        "missing_evidence_total": sum(1 for event in validated if not event["evidence_refs"]),
        "invalid_correlation_total": 0,
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
