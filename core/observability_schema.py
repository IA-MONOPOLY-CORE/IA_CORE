"""Schema de observability previo a runtime executor."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


OBSERVABILITY_EVENT_SCHEMA_VERSION = "1.0"

MINIMUM_EVENT_TYPES = {
    "promotion_gate_evaluated",
    "approval_requested",
    "approval_decision_recorded",
    "promotion_executed",
    "promotion_rollback_recorded",
    "active_contract_evaluated",
    "active_executed",
    "active_rollback_recorded",
    "runtime_contract_evaluated",
    "runtime_contract_blocked",
    "runtime_boundary_violation",
    "mutation_scope_verified",
    "snapshot_recorded",
    "rollback_plan_recorded",
}
RUNTIME_EXECUTOR_EVENT_TYPES = {
    "runtime_executor_contract_evaluated",
    "runtime_executor_prepare_only_validated",
    "runtime_executor_contract_blocked",
}
ALLOWED_EVENT_TYPES = MINIMUM_EVENT_TYPES | RUNTIME_EXECUTOR_EVENT_TYPES
ALLOWED_TARGET_TYPES = {
    "domain",
    "artifact",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "agent",
    "team",
    "capability_policy",
    "tool_contract",
    "memory_contract",
}
ALLOWED_ACTOR_TYPES = {"system", "human", "service", "test"}
ALLOWED_OPERATION_PHASES = {
    "gate",
    "approval",
    "promotion",
    "active_contract",
    "active_execution",
    "runtime_contract",
    "rollback",
    "snapshot",
    "verification",
}
ALLOWED_RESULTS = {"passed", "blocked", "failed", "recorded", "applied", "rolled_back", "future"}
ALLOWED_MUTATION_SCOPES = {
    "none",
    "status_only",
    "status_and_artifact_state",
    "manifest_status_only",
    "in_memory_status_only",
}
REQUIRED_FIELDS = {
    "schema_version",
    "event_id",
    "correlation_id",
    "causation_id",
    "event_type",
    "event_version",
    "timestamp",
    "actor",
    "actor_type",
    "source_module",
    "target_type",
    "target_id",
    "domain_id",
    "operation",
    "operation_phase",
    "result_status",
    "decision",
    "requested_status",
    "previous_status",
    "next_status",
    "mutation_scope",
    "runtime_flags",
    "execution_flags",
    "external_access_flags",
    "tool_memory_flags",
    "evidence_refs",
    "approval_refs",
    "contract_refs",
    "audit_refs",
    "snapshot_refs",
    "blockers",
    "warnings",
    "error_code",
    "error_message",
    "rollback_available",
    "rollback_ref",
    "immutability",
    "redaction_policy",
    "retention_policy",
    "created_at",
}
FLAG_FIELDS = {
    "runtime_flags",
    "execution_flags",
    "external_access_flags",
    "tool_memory_flags",
}
REF_FIELDS = {
    "evidence_refs",
    "approval_refs",
    "contract_refs",
    "audit_refs",
    "snapshot_refs",
}


def build_observability_event(
    *,
    event_id: str,
    correlation_id: str,
    event_type: str,
    actor: str,
    actor_type: str,
    source_module: str,
    target_type: str,
    target_id: str,
    domain_id: str,
    operation: str,
    operation_phase: str,
    result_status: str,
    evidence_refs: dict[str, Any],
    mutation_scope: str = "none",
    runtime_flags: dict[str, Any] | None = None,
    execution_flags: dict[str, Any] | None = None,
    external_access_flags: dict[str, Any] | None = None,
    tool_memory_flags: dict[str, Any] | None = None,
    causation_id: str | None = None,
    event_version: str = "1.0",
    timestamp: str | None = None,
    decision: str | None = None,
    requested_status: str | None = None,
    previous_status: str | None = None,
    next_status: str | None = None,
    approval_refs: dict[str, Any] | None = None,
    contract_refs: dict[str, Any] | None = None,
    audit_refs: dict[str, Any] | None = None,
    snapshot_refs: dict[str, Any] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    error_code: str | None = None,
    error_message: str | None = None,
    rollback_available: bool = False,
    rollback_ref: str | None = None,
    immutability: bool = True,
    redaction_policy: str = "safe_metadata_only",
    retention_policy: str = "local_project_retained",
    created_at: str | None = None,
) -> dict[str, Any]:
    now = datetime.now().isoformat()
    payload = {
        "schema_version": OBSERVABILITY_EVENT_SCHEMA_VERSION,
        "event_id": event_id,
        "correlation_id": correlation_id,
        "causation_id": causation_id,
        "event_type": event_type,
        "event_version": event_version,
        "timestamp": timestamp or now,
        "actor": actor,
        "actor_type": actor_type,
        "source_module": source_module,
        "target_type": target_type,
        "target_id": target_id,
        "domain_id": domain_id,
        "operation": operation,
        "operation_phase": operation_phase,
        "result_status": result_status,
        "decision": decision,
        "requested_status": requested_status,
        "previous_status": previous_status,
        "next_status": next_status,
        "mutation_scope": mutation_scope,
        "runtime_flags": dict(runtime_flags or {"runtime_enabled": False, "runtime_allowed": False}),
        "execution_flags": dict(execution_flags or {"execution_enabled": False, "execution_allowed": False}),
        "external_access_flags": dict(external_access_flags or {"external_access": False, "external_access_enabled": False}),
        "tool_memory_flags": dict(tool_memory_flags or {
            "tool_execution_enabled": False,
            "memory_persistence_enabled": False,
        }),
        "evidence_refs": dict(evidence_refs),
        "approval_refs": dict(approval_refs or {}),
        "contract_refs": dict(contract_refs or {}),
        "audit_refs": dict(audit_refs or {}),
        "snapshot_refs": dict(snapshot_refs or {}),
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "error_code": error_code,
        "error_message": error_message,
        "rollback_available": rollback_available,
        "rollback_ref": rollback_ref,
        "immutability": immutability,
        "redaction_policy": redaction_policy,
        "retention_policy": retention_policy,
        "created_at": created_at or now,
    }
    return validate_observability_event(payload)


def validate_observability_event(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("observability_event debe ser un objeto")
    missing = REQUIRED_FIELDS - set(event)
    if missing:
        raise ValueError(f"observability_event incompleto: {', '.join(sorted(missing))}")
    if event.get("schema_version") != OBSERVABILITY_EVENT_SCHEMA_VERSION:
        raise ValueError("schema_version de observability_event invalida")
    for field in ["event_id", "correlation_id", "target_id", "domain_id"]:
        _validate_id(event.get(field), field)
    if event.get("causation_id") is not None:
        _validate_id(event.get("causation_id"), "causation_id")
    if event.get("event_type") not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"event_type invalido: {event.get('event_type')}")
    _validate_non_empty_text(event.get("event_version"), "event_version")
    for field in ["timestamp", "actor", "source_module", "operation", "created_at"]:
        _validate_non_empty_text(event.get(field), field)
    if event.get("actor_type") not in ALLOWED_ACTOR_TYPES:
        raise ValueError(f"actor_type invalido: {event.get('actor_type')}")
    if event.get("target_type") not in ALLOWED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {event.get('target_type')}")
    if event.get("operation_phase") not in ALLOWED_OPERATION_PHASES:
        raise ValueError(f"operation_phase invalida: {event.get('operation_phase')}")
    if event.get("result_status") not in ALLOWED_RESULTS:
        raise ValueError(f"result_status invalido: {event.get('result_status')}")
    if event.get("mutation_scope") not in ALLOWED_MUTATION_SCOPES:
        raise ValueError(f"mutation_scope invalido: {event.get('mutation_scope')}")
    for field in FLAG_FIELDS:
        _validate_flags(event.get(field), field)
    for field in REF_FIELDS:
        if not isinstance(event.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    if not event["evidence_refs"]:
        raise ValueError("evidence_refs requerido")
    for field in ["blockers", "warnings"]:
        if not isinstance(event.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    if event.get("rollback_available") is not False and not isinstance(event.get("rollback_ref"), str):
        raise ValueError("rollback_ref requerido cuando rollback_available=true")
    if event.get("immutability") is not True:
        raise ValueError("observability_event requiere immutability=true")
    for field in ["redaction_policy", "retention_policy"]:
        _validate_non_empty_text(event.get(field), field)
    _validate_snapshots(event["snapshot_refs"])
    _ensure_json_serializable(event)
    return deepcopy(event)


def _validate_snapshots(snapshot_refs: dict[str, Any]) -> None:
    snapshots = snapshot_refs.get("snapshots", [])
    if not isinstance(snapshots, list):
        raise ValueError("snapshot_refs.snapshots debe ser lista")
    for snapshot in snapshots:
        if not isinstance(snapshot, dict):
            raise ValueError("snapshot debe ser objeto")
        for field in ["before_snapshot", "after_snapshot", "diff_summary", "mutation_scope", "rollback_snapshot", "checksum"]:
            if field not in snapshot:
                raise ValueError(f"snapshot incompleto: {field}")
        _validate_non_empty_text(snapshot["checksum"], "snapshot.checksum")
        if snapshot["mutation_scope"] not in ALLOWED_MUTATION_SCOPES:
            raise ValueError("snapshot mutation_scope invalido")


def _validate_flags(flags: Any, field: str) -> None:
    if not isinstance(flags, dict) or not flags:
        raise ValueError(f"{field} debe ser objeto no vacio")
    for key, value in flags.items():
        _validate_non_empty_text(key, field)
        if not isinstance(value, bool):
            raise ValueError(f"{field}.{key} debe ser booleano")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(payload: dict[str, Any]) -> None:
    try:
        json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("observability_event debe ser serializable como JSON") from exc
