"""Write-safe simulated contract for future attempt store persistence."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from core.execution_attempt import serialize_execution_attempt_schema, validate_execution_attempt_schema


ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS = "contract_only"
ATTEMPT_STORE_WRITE_SAFE_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_HISTORY_WRITES_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_SCHEDULER_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_WORKER_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_QUEUE_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_MODEL_INVOCATION_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_TOOL_EXECUTION_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_MEMORY_PERSISTENCE_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_EXTERNAL_ACCESS_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_API_ENABLED = False
ATTEMPT_STORE_WRITE_SAFE_UI_ENABLED = False
MARKET_CATALOG_RUNTIME_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"would_write", "blocked", "duplicate", "invalid"}
ALLOWED_READINESS = {"ready_for_attempt_store_write_safe_e2e_checkpoint", "blocked", "invalid"}
ALLOWED_IDEMPOTENCY_RESULTS = {"new", "duplicate", "conflict", "not_checked"}
ALLOWED_INITIAL_STATES = {"draft", "schema_validated", "blocked"}
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
    *FORBIDDEN_STATES,
    "ready_for_runtime",
    "runtime_enabled",
    "operations_enabled",
    "store_enabled",
    "writes_enabled",
    "gate_open",
}
FORBIDDEN_TRUE_FLAGS = {
    "attempt_store_enabled",
    "attempt_store_writes_enabled",
    "attempt_persistence_enabled",
    "real_writes_enabled",
    "persistence_enabled",
    "runtime_enabled",
    "store_enabled",
    "writes_enabled",
    "store_writes_enabled",
    "lifecycle_writes_enabled",
    "lifecycle_events_enabled",
    "result_store_enabled",
    "result_store_writes_enabled",
    "history_writes_enabled",
    "read_model_writes_enabled",
    "projection_writes_enabled",
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
class AttemptStoreWriteSafeDecision:
    store_decision_id: str
    status: str
    decision: str
    readiness: str
    attempt_id: str
    write_ref: str | None
    persisted: bool
    idempotency_key: str | None
    idempotency_result: str
    initial_state: str
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollback_ref: str | None = None
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blocking_reasons"] = deepcopy(self.blocking_reasons)
        payload["warnings"] = deepcopy(self.warnings)
        payload["lineage"] = deepcopy(self.lineage)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_attempt_store_write_safe_decision(
    *,
    store_decision_id: str = "attempt_store_write_safe_contract",
    status: str = "evaluated",
    decision: str = "would_write",
    readiness: str = "ready_for_attempt_store_write_safe_e2e_checkpoint",
    attempt_id: str = "",
    write_ref: str | None = None,
    persisted: bool = False,
    idempotency_key: str | None = None,
    idempotency_result: str = "not_checked",
    initial_state: str = "schema_validated",
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    rollback_ref: str | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> AttemptStoreWriteSafeDecision:
    return AttemptStoreWriteSafeDecision(
        store_decision_id=store_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        attempt_id=attempt_id,
        write_ref=write_ref,
        persisted=persisted,
        idempotency_key=idempotency_key,
        idempotency_result=idempotency_result,
        initial_state=initial_state,
        blocking_reasons=deepcopy(blocking_reasons or []),
        warnings=deepcopy(warnings or []),
        rollback_ref=rollback_ref,
        lineage=deepcopy(lineage or {}),
        metadata=deepcopy(metadata or {}),
    )


def evaluate_attempt_store_write_safe(
    *,
    attempt: Any,
    idempotency_key: str | None = None,
    lineage: dict[str, Any] | None = None,
    existing_attempt_ids: list[str] | None = None,
    existing_idempotency_keys: dict[str, Any] | None = None,
    write_mode: str = "contract_only",
    preflight_flags: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    allow_missing_idempotency_key: bool = False,
) -> AttemptStoreWriteSafeDecision:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    payload = serialize_execution_attempt_schema(attempt)
    attempt_id = payload.get("attempt_id") or ""
    initial_state = payload.get("metadata", {}).get("state_machine_state") or payload.get("status")
    merged_lineage = deepcopy(lineage or {})
    merged_metadata = deepcopy(metadata or {})
    merged_metadata.update(
        {
            "write_mode": write_mode,
            "preflight_flags": deepcopy(preflight_flags or {}),
            "contract_only": True,
            "write_safe_simulated": True,
            "real_persistence": False,
        }
    )

    schema_validation = validate_execution_attempt_schema(payload)
    if schema_validation["status"] != "validated":
        _copy_blockers(schema_validation.get("blockers", []), blockers)

    _require(attempt_id, blockers, "missing_attempt_id", "attempt_id requerido")
    _validate_initial_state(initial_state, blockers)
    _validate_lineage(merged_lineage, blockers)
    if not idempotency_key and not allow_missing_idempotency_key:
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")

    idempotency_result = _simulate_idempotency(
        attempt_id=attempt_id,
        idempotency_key=idempotency_key,
        existing_attempt_ids=existing_attempt_ids,
        existing_idempotency_keys=existing_idempotency_keys,
    )
    if idempotency_result == "conflict":
        _block(blockers, "idempotency_conflict", "idempotency_key o attempt_id en conflicto")

    if blockers:
        return _decision_from_blockers(
            attempt_id=attempt_id,
            initial_state=initial_state if initial_state in ALLOWED_INITIAL_STATES else "blocked",
            idempotency_key=idempotency_key,
            idempotency_result="conflict" if idempotency_result == "conflict" else idempotency_result,
            blocking_reasons=blockers,
            warnings=warnings,
            lineage=merged_lineage,
            metadata=merged_metadata,
            decision="invalid" if any(blocker["code"].startswith(("invalid", "missing")) for blocker in blockers) else "blocked",
        )

    decision = "duplicate" if idempotency_result == "duplicate" else "would_write"
    return build_attempt_store_write_safe_decision(
        status="evaluated",
        decision=decision,
        readiness="ready_for_attempt_store_write_safe_e2e_checkpoint",
        attempt_id=attempt_id,
        write_ref=f"conceptual:attempt_store:{attempt_id}",
        persisted=False,
        idempotency_key=idempotency_key,
        idempotency_result=idempotency_result,
        initial_state=initial_state,
        blocking_reasons=[],
        warnings=warnings,
        rollback_ref=None,
        lineage=merged_lineage,
        metadata=merged_metadata,
    )


def validate_attempt_store_write_safe_decision(decision: AttemptStoreWriteSafeDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_attempt_store_write_safe_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("store_decision_id"), blockers, "missing_store_decision_id", "store_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision no permitida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")
    _require(payload.get("attempt_id"), blockers, "missing_attempt_id", "attempt_id requerido")
    if not payload.get("idempotency_key") and payload.get("idempotency_result") != "not_checked":
        _block(blockers, "missing_idempotency_key", "idempotency_key requerido")
    _allowed(payload.get("idempotency_result"), ALLOWED_IDEMPOTENCY_RESULTS, blockers, "invalid_idempotency_result", "idempotency_result no permitido")
    _allowed(payload.get("initial_state"), ALLOWED_INITIAL_STATES, blockers, "invalid_initial_state", "initial_state no permitido")
    if payload.get("initial_state") in FORBIDDEN_STATES:
        _block(blockers, "forbidden_initial_state", "estado runtime/resultado no permitido")
    if payload.get("persisted") is not False:
        _block(blockers, "persisted_not_allowed", "persisted debe ser false")
    _validate_conceptual_ref(payload.get("write_ref"), blockers, "write_ref")
    _validate_conceptual_ref(payload.get("rollback_ref"), blockers, "rollback_ref")

    if not isinstance(payload.get("blocking_reasons"), list):
        _block(blockers, "invalid_blocking_reasons", "blocking_reasons debe ser list")
    if not isinstance(payload.get("warnings"), list):
        _block(blockers, "invalid_warnings", "warnings debe ser list")
    if not isinstance(payload.get("lineage"), dict):
        _block(blockers, "invalid_lineage", "lineage debe ser dict")
    else:
        _validate_lineage(payload.get("lineage") or {}, blockers)
    if not isinstance(payload.get("metadata"), dict):
        _block(blockers, "invalid_metadata", "metadata debe ser dict")

    _scan_forbidden_values(payload, blockers)
    _validate_market_and_business_boundaries(payload, blockers)
    _validate_boundaries(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_READY" if not blockers else "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_BLOCKED",
        "readiness": "ready_for_attempt_store_write_safe_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [] if not blockers else ["attempt_store_write_safe_decision_blocked"],
        "decision": payload,
        "contract_status": ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS,
        "attempt_store_enabled": ATTEMPT_STORE_WRITE_SAFE_ENABLED,
        "real_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED,
        "persistence_enabled": ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED,
        "lifecycle_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED,
        "lifecycle_events_enabled": ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED,
        "result_store_enabled": ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED,
        "history_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED,
        "runtime_enabled": ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED,
    }


def serialize_attempt_store_write_safe_decision(decision: AttemptStoreWriteSafeDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, AttemptStoreWriteSafeDecision):
        return decision.to_dict()
    return deepcopy(decision)


def get_attempt_store_write_safe_contract() -> dict[str, Any]:
    return {
        "status": ATTEMPT_STORE_WRITE_SAFE_CONTRACT_STATUS,
        "verdict": "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_READY",
        "readiness": "ready_for_attempt_store_write_safe_e2e_checkpoint",
        "next_step": "PROMPT 3.16.1 — Checkpoint E2E de attempt store write-safe",
        "allowed_statuses": sorted(ALLOWED_STATUSES),
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "allowed_readiness": sorted(ALLOWED_READINESS),
        "allowed_idempotency_results": sorted(ALLOWED_IDEMPOTENCY_RESULTS),
        "allowed_initial_states": sorted(ALLOWED_INITIAL_STATES),
        "forbidden_states": sorted(FORBIDDEN_STATES),
        "boundaries": _boundary_flags(),
    }


def _decision_from_blockers(
    *,
    attempt_id: str,
    initial_state: str,
    idempotency_key: str | None,
    idempotency_result: str,
    blocking_reasons: list[dict[str, str]],
    warnings: list[str],
    lineage: dict[str, Any],
    metadata: dict[str, Any],
    decision: str,
) -> AttemptStoreWriteSafeDecision:
    return build_attempt_store_write_safe_decision(
        status="invalid" if decision == "invalid" else "blocked",
        decision=decision,
        readiness="invalid" if decision == "invalid" else "blocked",
        attempt_id=attempt_id,
        write_ref=None,
        persisted=False,
        idempotency_key=idempotency_key,
        idempotency_result=idempotency_result,
        initial_state=initial_state,
        blocking_reasons=blocking_reasons,
        warnings=warnings,
        rollback_ref=None,
        lineage=lineage,
        metadata=metadata,
    )


def _simulate_idempotency(
    *,
    attempt_id: str,
    idempotency_key: str | None,
    existing_attempt_ids: list[str] | None,
    existing_idempotency_keys: dict[str, Any] | None,
) -> str:
    if existing_attempt_ids is None and existing_idempotency_keys is None:
        return "not_checked"
    existing_ids = set(existing_attempt_ids or [])
    existing_keys = existing_idempotency_keys or {}
    if idempotency_key and idempotency_key in existing_keys:
        existing_value = existing_keys[idempotency_key]
        existing_attempt_id = existing_value.get("attempt_id") if isinstance(existing_value, dict) else existing_value
        return "duplicate" if existing_attempt_id == attempt_id else "conflict"
    if attempt_id in existing_ids:
        return "conflict"
    return "new"


def _validate_initial_state(initial_state: Any, blockers: list[dict[str, str]]) -> None:
    if initial_state in FORBIDDEN_STATES:
        _block(blockers, "forbidden_initial_state", "estado runtime/resultado no permitido")
    elif initial_state not in ALLOWED_INITIAL_STATES:
        _block(blockers, "invalid_initial_state", "initial_state no permitido")


def _validate_lineage(lineage: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not lineage.get("intent_id"):
        _block(blockers, "missing_lineage_intent_id", "lineage.intent_id requerido")
    if not lineage.get("factory_id"):
        _block(blockers, "missing_lineage_factory_id", "lineage.factory_id requerido")


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
        "attempt_store_enabled": ATTEMPT_STORE_WRITE_SAFE_ENABLED,
        "real_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_REAL_WRITES_ENABLED,
        "attempt_persistence_enabled": ATTEMPT_STORE_WRITE_SAFE_PERSISTENCE_ENABLED,
        "lifecycle_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_WRITES_ENABLED,
        "lifecycle_events_enabled": ATTEMPT_STORE_WRITE_SAFE_LIFECYCLE_EVENTS_ENABLED,
        "result_store_enabled": ATTEMPT_STORE_WRITE_SAFE_RESULT_STORE_ENABLED,
        "history_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": ATTEMPT_STORE_WRITE_SAFE_PROJECTION_WRITES_ENABLED,
        "runtime_enabled": ATTEMPT_STORE_WRITE_SAFE_RUNTIME_ENABLED,
        "scheduler_enabled": ATTEMPT_STORE_WRITE_SAFE_SCHEDULER_ENABLED,
        "worker_enabled": ATTEMPT_STORE_WRITE_SAFE_WORKER_ENABLED,
        "queue_enabled": ATTEMPT_STORE_WRITE_SAFE_QUEUE_ENABLED,
        "model_invocation_enabled": ATTEMPT_STORE_WRITE_SAFE_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": ATTEMPT_STORE_WRITE_SAFE_TOOL_EXECUTION_ENABLED,
        "memory_persistence_enabled": ATTEMPT_STORE_WRITE_SAFE_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": ATTEMPT_STORE_WRITE_SAFE_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": ATTEMPT_STORE_WRITE_SAFE_API_ENABLED,
        "ui_enabled": ATTEMPT_STORE_WRITE_SAFE_UI_ENABLED,
        "market_catalog_runtime_enabled": MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_layer_runtime_enabled": BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED,
    }


def _copy_blockers(source: list[dict[str, str]], target: list[dict[str, str]]) -> None:
    for blocker in source:
        _block(target, blocker.get("code", "blocked"), blocker.get("message", "blocked"))


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
