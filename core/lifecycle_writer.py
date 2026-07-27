"""Non-operational lifecycle writer contract.

This module only evaluates whether a lifecycle event would be emitted. It does
not emit lifecycle events, write lifecycle_store, persist attempts, start
runtime, or call external systems.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


LIFECYCLE_WRITER_CONTRACT_STATUS = "contract_only"
LIFECYCLE_WRITER_ENABLED = False
LIFECYCLE_WRITER_REAL_WRITES_ENABLED = False
LIFECYCLE_WRITER_EVENTS_ENABLED = False
LIFECYCLE_WRITER_STORE_WRITES_ENABLED = False
LIFECYCLE_WRITER_ATTEMPT_STORE_WRITES_ENABLED = False
LIFECYCLE_WRITER_RESULT_STORE_ENABLED = False
LIFECYCLE_WRITER_HISTORY_WRITES_ENABLED = False
LIFECYCLE_WRITER_READ_MODEL_WRITES_ENABLED = False
LIFECYCLE_WRITER_PROJECTION_WRITES_ENABLED = False
LIFECYCLE_WRITER_RUNTIME_ENABLED = False
LIFECYCLE_WRITER_SCHEDULER_ENABLED = False
LIFECYCLE_WRITER_WORKER_ENABLED = False
LIFECYCLE_WRITER_QUEUE_ENABLED = False
LIFECYCLE_WRITER_MODEL_INVOCATION_ENABLED = False
LIFECYCLE_WRITER_TOOL_EXECUTION_ENABLED = False
LIFECYCLE_WRITER_MEMORY_PERSISTENCE_ENABLED = False
LIFECYCLE_WRITER_EXTERNAL_ACCESS_ENABLED = False
LIFECYCLE_WRITER_API_ENABLED = False
LIFECYCLE_WRITER_UI_ENABLED = False
MARKET_CATALOG_RUNTIME_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"would_emit", "blocked", "duplicate", "invalid"}
ALLOWED_READINESS = {"ready_for_lifecycle_writer_e2e_checkpoint", "blocked", "invalid"}
ALLOWED_IDEMPOTENCY_RESULTS = {"new", "duplicate", "conflict", "not_checked"}
ALLOWED_EVENT_TYPES = {
    "attempt_contract_created",
    "attempt_store_would_write",
    "attempt_schema_validated",
    "attempt_blocked",
    "attempt_cancelled_contractually",
}
ALLOWED_STATES = {"draft", "schema_validated", "blocked", "cancelled"}
ALLOWED_FROM_STATES = {*ALLOWED_STATES, None}
ALLOWED_TRANSITIONS = {
    (None, "draft"),
    ("draft", "schema_validated"),
    ("draft", "blocked"),
    ("schema_validated", "blocked"),
    ("draft", "cancelled"),
    ("schema_validated", "cancelled"),
    ("blocked", "blocked"),
    ("cancelled", "cancelled"),
}
FORBIDDEN_EVENTS = {
    "attempt_queued",
    "attempt_running",
    "attempt_succeeded",
    "attempt_failed",
    "attempt_partially_succeeded",
    "attempt_retrying",
    "attempt_expired",
    "result_created",
    "result_persisted",
    "history_written",
    "read_model_written",
    "projection_persisted",
    "runtime_started",
    "tool_invoked",
    "model_invoked",
    "external_accessed",
}
FORBIDDEN_STATES = {
    "preflight_ready",
    "queued",
    "running",
    "succeeded",
    "failed",
    "partially_succeeded",
    "retrying",
    "expired",
}
FORBIDDEN_OPERATIONAL_VALUES = {
    *FORBIDDEN_EVENTS,
    *FORBIDDEN_STATES,
    "ready_for_runtime",
    "runtime_enabled",
    "operations_enabled",
    "lifecycle_enabled",
    "events_enabled",
    "gate_open",
}
FORBIDDEN_TRUE_FLAGS = {
    "lifecycle_writer_enabled",
    "lifecycle_enabled",
    "lifecycle_writes_enabled",
    "lifecycle_events_enabled",
    "lifecycle_store_writes_enabled",
    "real_writes_enabled",
    "events_enabled",
    "store_writes_enabled",
    "attempt_store_writes_enabled",
    "result_store_enabled",
    "result_store_writes_enabled",
    "history_writes_enabled",
    "read_model_writes_enabled",
    "projection_writes_enabled",
    "runtime_enabled",
    "scheduler_enabled",
    "worker_enabled",
    "queue_enabled",
    "model_invocation_enabled",
    "tool_execution_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "api_enabled",
    "ui_enabled",
    "market_catalog_active",
    "market_catalog_runtime_enabled",
    "business_composition_enabled",
    "business_composition_active",
    "business_composition_layer_runtime_enabled",
    "gate_open",
    "operations_enabled",
}


@dataclass(frozen=True)
class LifecycleWriterDecision:
    lifecycle_decision_id: str
    status: str
    decision: str
    readiness: str
    event_id: str
    attempt_id: str
    event_type: str
    from_state: str | None
    to_state: str
    emitted: bool
    write_ref: str | None
    rollback_ref: str | None
    idempotency_key: str | None
    idempotency_result: str
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blocking_reasons"] = deepcopy(self.blocking_reasons)
        payload["warnings"] = deepcopy(self.warnings)
        payload["lineage"] = deepcopy(self.lineage)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_lifecycle_writer_decision(
    *,
    lifecycle_decision_id: str = "lifecycle_writer_contract",
    status: str = "evaluated",
    decision: str = "would_emit",
    readiness: str = "ready_for_lifecycle_writer_e2e_checkpoint",
    event_id: str = "",
    attempt_id: str = "",
    event_type: str = "attempt_contract_created",
    from_state: str | None = None,
    to_state: str = "draft",
    emitted: bool = False,
    write_ref: str | None = None,
    rollback_ref: str | None = None,
    idempotency_key: str | None = None,
    idempotency_result: str = "not_checked",
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> LifecycleWriterDecision:
    return LifecycleWriterDecision(
        lifecycle_decision_id=lifecycle_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        event_id=event_id,
        attempt_id=attempt_id,
        event_type=event_type,
        from_state=from_state,
        to_state=to_state,
        emitted=emitted,
        write_ref=write_ref,
        rollback_ref=rollback_ref,
        idempotency_key=idempotency_key,
        idempotency_result=idempotency_result,
        blocking_reasons=deepcopy(blocking_reasons or []),
        warnings=deepcopy(warnings or []),
        lineage=deepcopy(lineage or {}),
        metadata=deepcopy(metadata or {}),
    )


def evaluate_lifecycle_event_contract(
    *,
    event_id: str,
    attempt_id: str,
    event_type: str,
    from_state: str | None,
    to_state: str,
    idempotency_key: str | None = None,
    lineage: dict[str, Any] | None = None,
    existing_event_ids: list[str] | None = None,
    existing_idempotency_keys: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    allow_missing_idempotency_key: bool = False,
) -> LifecycleWriterDecision:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    merged_lineage = deepcopy(lineage or {})
    merged_metadata = deepcopy(metadata or {})
    merged_metadata.update(
        {
            "contract_only": True,
            "lifecycle_simulated": True,
            "emits_real_events": False,
            "real_lifecycle_writes": False,
        }
    )

    _require(event_id, blockers, "missing_event_id", "event_id requerido")
    _require(attempt_id, blockers, "missing_attempt_id", "attempt_id requerido")
    _validate_event_type(event_type, blockers)
    _validate_state(from_state, blockers, field_name="from_state", allow_none=True)
    _validate_state(to_state, blockers, field_name="to_state", allow_none=False)
    _validate_transition(from_state, to_state, blockers)
    _validate_lineage(merged_lineage, attempt_id, blockers)
    if not idempotency_key and not allow_missing_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")

    idempotency_result = _simulate_idempotency(
        event_id=event_id,
        idempotency_key=idempotency_key,
        existing_event_ids=existing_event_ids,
        existing_idempotency_keys=existing_idempotency_keys,
    )
    if idempotency_result == "conflict":
        _block(blockers, "idempotency_conflict", "event_id o idempotency_key en conflicto")

    if blockers:
        return _decision_from_blockers(
            event_id=event_id,
            attempt_id=attempt_id,
            event_type=event_type,
            from_state=from_state,
            to_state=to_state if to_state in ALLOWED_STATES else "blocked",
            idempotency_key=idempotency_key,
            idempotency_result="conflict" if idempotency_result == "conflict" else idempotency_result,
            blocking_reasons=blockers,
            warnings=warnings,
            lineage=merged_lineage,
            metadata=merged_metadata,
            decision="invalid" if any(blocker["code"].startswith(("invalid", "missing")) for blocker in blockers) else "blocked",
        )

    decision = "duplicate" if idempotency_result == "duplicate" else "would_emit"
    return build_lifecycle_writer_decision(
        status="evaluated",
        decision=decision,
        readiness="ready_for_lifecycle_writer_e2e_checkpoint",
        event_id=event_id,
        attempt_id=attempt_id,
        event_type=event_type,
        from_state=from_state,
        to_state=to_state,
        emitted=False,
        write_ref=f"conceptual:lifecycle_event:{event_id}",
        rollback_ref=None,
        idempotency_key=idempotency_key,
        idempotency_result=idempotency_result,
        blocking_reasons=[],
        warnings=warnings,
        lineage=merged_lineage,
        metadata=merged_metadata,
    )


def validate_lifecycle_writer_decision(decision: LifecycleWriterDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_lifecycle_writer_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("lifecycle_decision_id"), blockers, "missing_lifecycle_decision_id", "lifecycle_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision no permitida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")
    _require(payload.get("event_id"), blockers, "missing_event_id", "event_id requerido")
    _require(payload.get("attempt_id"), blockers, "missing_attempt_id", "attempt_id requerido")
    _validate_event_type(payload.get("event_type"), blockers)
    _validate_state(payload.get("from_state"), blockers, field_name="from_state", allow_none=True)
    _validate_state(payload.get("to_state"), blockers, field_name="to_state", allow_none=False)
    _validate_transition(payload.get("from_state"), payload.get("to_state"), blockers)
    if payload.get("emitted") is not False:
        _block(blockers, "emitted_not_allowed", "emitted debe ser false")
    _validate_conceptual_ref(payload.get("write_ref"), blockers, "write_ref")
    _validate_conceptual_ref(payload.get("rollback_ref"), blockers, "rollback_ref")
    if not payload.get("idempotency_key") and payload.get("idempotency_result") != "not_checked":
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")
    _allowed(payload.get("idempotency_result"), ALLOWED_IDEMPOTENCY_RESULTS, blockers, "invalid_idempotency_result", "idempotency_result no permitido")
    if not isinstance(payload.get("blocking_reasons"), list):
        _block(blockers, "invalid_blocking_reasons", "blocking_reasons debe ser list")
    if not isinstance(payload.get("warnings"), list):
        _block(blockers, "invalid_warnings", "warnings debe ser list")
    if not isinstance(payload.get("lineage"), dict):
        _block(blockers, "invalid_lineage", "lineage debe ser dict")
    else:
        _validate_lineage(payload.get("lineage") or {}, payload.get("attempt_id") or "", blockers)
    if not isinstance(payload.get("metadata"), dict):
        _block(blockers, "invalid_metadata", "metadata debe ser dict")

    _scan_forbidden_values(payload, blockers)
    _validate_market_and_business_boundaries(payload, blockers)
    _validate_boundaries(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "LIFECYCLE_WRITER_CONTRACT_READY" if not blockers else "LIFECYCLE_WRITER_CONTRACT_BLOCKED",
        "readiness": "ready_for_lifecycle_writer_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [] if not blockers else ["lifecycle_writer_decision_blocked"],
        "decision": payload,
        "contract_status": LIFECYCLE_WRITER_CONTRACT_STATUS,
        "lifecycle_writer_enabled": LIFECYCLE_WRITER_ENABLED,
        "real_writes_enabled": LIFECYCLE_WRITER_REAL_WRITES_ENABLED,
        "events_enabled": LIFECYCLE_WRITER_EVENTS_ENABLED,
        "store_writes_enabled": LIFECYCLE_WRITER_STORE_WRITES_ENABLED,
        "runtime_enabled": LIFECYCLE_WRITER_RUNTIME_ENABLED,
    }


def serialize_lifecycle_writer_decision(decision: LifecycleWriterDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, LifecycleWriterDecision):
        return decision.to_dict()
    return deepcopy(decision)


def get_lifecycle_writer_contract() -> dict[str, Any]:
    return {
        "status": LIFECYCLE_WRITER_CONTRACT_STATUS,
        "verdict": "LIFECYCLE_WRITER_CONTRACT_READY",
        "readiness": "ready_for_lifecycle_writer_e2e_checkpoint",
        "next_step": "PROMPT 3.18.1 — Checkpoint E2E de lifecycle writer",
        "allowed_statuses": sorted(ALLOWED_STATUSES),
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "allowed_readiness": sorted(ALLOWED_READINESS),
        "allowed_idempotency_results": sorted(ALLOWED_IDEMPOTENCY_RESULTS),
        "allowed_event_types": sorted(ALLOWED_EVENT_TYPES),
        "allowed_states": sorted(ALLOWED_STATES),
        "allowed_transitions": sorted([f"{source}->{target}" for source, target in ALLOWED_TRANSITIONS]),
        "forbidden_events": sorted(FORBIDDEN_EVENTS),
        "forbidden_states": sorted(FORBIDDEN_STATES),
        "boundaries": _boundary_flags(),
    }


def _decision_from_blockers(
    *,
    event_id: str,
    attempt_id: str,
    event_type: str,
    from_state: str | None,
    to_state: str,
    idempotency_key: str | None,
    idempotency_result: str,
    blocking_reasons: list[dict[str, str]],
    warnings: list[str],
    lineage: dict[str, Any],
    metadata: dict[str, Any],
    decision: str,
) -> LifecycleWriterDecision:
    return build_lifecycle_writer_decision(
        status="invalid" if decision == "invalid" else "blocked",
        decision=decision,
        readiness="invalid" if decision == "invalid" else "blocked",
        event_id=event_id,
        attempt_id=attempt_id,
        event_type=event_type,
        from_state=from_state,
        to_state=to_state,
        emitted=False,
        write_ref=None,
        rollback_ref=None,
        idempotency_key=idempotency_key,
        idempotency_result=idempotency_result,
        blocking_reasons=blocking_reasons,
        warnings=warnings,
        lineage=lineage,
        metadata=metadata,
    )


def _simulate_idempotency(
    *,
    event_id: str,
    idempotency_key: str | None,
    existing_event_ids: list[str] | None,
    existing_idempotency_keys: dict[str, Any] | None,
) -> str:
    if existing_event_ids is None and existing_idempotency_keys is None:
        return "not_checked"
    existing_ids = set(existing_event_ids or [])
    existing_keys = existing_idempotency_keys or {}
    if idempotency_key and idempotency_key in existing_keys:
        existing_value = existing_keys[idempotency_key]
        existing_event_id = existing_value.get("event_id") if isinstance(existing_value, dict) else existing_value
        return "duplicate" if existing_event_id == event_id else "conflict"
    if event_id in existing_ids:
        return "conflict"
    return "new"


def _validate_event_type(event_type: Any, blockers: list[dict[str, str]]) -> None:
    if event_type in FORBIDDEN_EVENTS:
        _block(blockers, "forbidden_event_type", "evento runtime/resultado no permitido")
    elif event_type not in ALLOWED_EVENT_TYPES:
        _block(blockers, "invalid_event_type", "event_type no permitido")


def _validate_state(state: Any, blockers: list[dict[str, str]], *, field_name: str, allow_none: bool) -> None:
    if state is None and allow_none:
        return
    if state in FORBIDDEN_STATES:
        _block(blockers, f"{field_name}_forbidden", f"{field_name} runtime/resultado no permitido")
    elif state not in ALLOWED_STATES:
        _block(blockers, f"{field_name}_invalid", f"{field_name} no permitido")


def _validate_transition(from_state: Any, to_state: Any, blockers: list[dict[str, str]]) -> None:
    if from_state in ALLOWED_FROM_STATES and to_state in ALLOWED_STATES and (from_state, to_state) not in ALLOWED_TRANSITIONS:
        _block(blockers, "transition_not_allowed", "transicion contractual no permitida")


def _validate_lineage(lineage: dict[str, Any], attempt_id: str, blockers: list[dict[str, str]]) -> None:
    if not lineage.get("intent_id"):
        _block(blockers, "missing_lineage_intent_id", "lineage.intent_id requerido")
    if not lineage.get("factory_id"):
        _block(blockers, "missing_lineage_factory_id", "lineage.factory_id requerido")
    if not lineage.get("attempt_id"):
        _block(blockers, "missing_lineage_attempt_id", "lineage.attempt_id requerido")
    elif attempt_id and lineage.get("attempt_id") != attempt_id:
        _block(blockers, "lineage_attempt_id_mismatch", "lineage.attempt_id debe coincidir con attempt_id")


def _validate_conceptual_ref(value: Any, blockers: list[dict[str, str]], field_name: str) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value.startswith("conceptual:"):
        _block(blockers, f"{field_name}_not_conceptual", f"{field_name} debe ser conceptual o null")


def _validate_market_and_business_boundaries(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for scope in (payload.get("metadata"), payload.get("lineage")):
        if not isinstance(scope, dict):
            continue
        if scope.get("market_catalog_status") == "active" or scope.get("market_catalog_active") is True:
            _block(blockers, "market_catalog_active_not_allowed", "Market Catalog activo no permitido")
        if scope.get("market_catalog_runtime_enabled") is True:
            _block(blockers, "market_catalog_runtime_not_allowed", "Market Catalog runtime no permitido")
        if scope.get("business_composition_layer_status") in {"active", "operational"}:
            _block(blockers, "business_composition_active_not_allowed", "Business Composition Layer activa no permitida")
        if scope.get("business_composition_enabled") is True or scope.get("business_composition_layer_operational") is True:
            _block(blockers, "business_composition_enabled_not_allowed", "Business Composition Layer operativa no permitida")


def _scan_forbidden_values(value: Any, blockers: list[dict[str, str]]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_TRUE_FLAGS and item is True:
                _block(blockers, f"{key}_not_allowed", f"{key}=true no permitido")
            _scan_forbidden_values(item, blockers)
    elif isinstance(value, list):
        for item in value:
            _scan_forbidden_values(item, blockers)
    elif isinstance(value, str) and value in FORBIDDEN_OPERATIONAL_VALUES:
        _block(blockers, f"{value}_not_allowed", f"{value} no permitido")


def _validate_boundaries(blockers: list[dict[str, str]]) -> None:
    for name, value in _boundary_flags().items():
        if value is not False:
            _block(blockers, f"{name}_not_allowed", f"{name} debe ser false")


def _boundary_flags() -> dict[str, bool]:
    return {
        "lifecycle_writer_enabled": LIFECYCLE_WRITER_ENABLED,
        "real_writes_enabled": LIFECYCLE_WRITER_REAL_WRITES_ENABLED,
        "lifecycle_events_enabled": LIFECYCLE_WRITER_EVENTS_ENABLED,
        "lifecycle_store_writes_enabled": LIFECYCLE_WRITER_STORE_WRITES_ENABLED,
        "attempt_store_writes_enabled": LIFECYCLE_WRITER_ATTEMPT_STORE_WRITES_ENABLED,
        "result_store_enabled": LIFECYCLE_WRITER_RESULT_STORE_ENABLED,
        "history_writes_enabled": LIFECYCLE_WRITER_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": LIFECYCLE_WRITER_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": LIFECYCLE_WRITER_PROJECTION_WRITES_ENABLED,
        "runtime_enabled": LIFECYCLE_WRITER_RUNTIME_ENABLED,
        "scheduler_enabled": LIFECYCLE_WRITER_SCHEDULER_ENABLED,
        "worker_enabled": LIFECYCLE_WRITER_WORKER_ENABLED,
        "queue_enabled": LIFECYCLE_WRITER_QUEUE_ENABLED,
        "model_invocation_enabled": LIFECYCLE_WRITER_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": LIFECYCLE_WRITER_TOOL_EXECUTION_ENABLED,
        "memory_persistence_enabled": LIFECYCLE_WRITER_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": LIFECYCLE_WRITER_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": LIFECYCLE_WRITER_API_ENABLED,
        "ui_enabled": LIFECYCLE_WRITER_UI_ENABLED,
        "market_catalog_runtime_enabled": MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_layer_runtime_enabled": BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED,
    }


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, "", {}, []):
        _block(blockers, code, message)


def _allowed(value: Any, allowed: set[Any], blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value not in allowed:
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
