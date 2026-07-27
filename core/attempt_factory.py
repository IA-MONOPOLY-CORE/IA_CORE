"""Non-operational contract for future execution attempt creation."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from core.execution_attempt import (
    ExecutionAttempt,
    build_attempt_schema_from_intent,
    serialize_execution_attempt_schema,
    validate_execution_attempt_schema,
)
from core.execution_intent import serialize_execution_intent, validate_execution_intent
from core.operational_readiness_gate import (
    evaluate_operational_readiness_contracts,
    serialize_operational_readiness_gate_decision,
    validate_operational_readiness_gate_decision,
)


ATTEMPT_FACTORY_CONTRACT_STATUS = "contract_only"
ATTEMPT_FACTORY_ENABLED = False
ATTEMPT_FACTORY_RUNTIME_ENABLED = False
ATTEMPT_FACTORY_STORE_WRITES_ENABLED = False
ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED = False
ATTEMPT_FACTORY_RESULT_STORE_ENABLED = False
ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED = False
ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED = False
ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED = False
ATTEMPT_FACTORY_SCHEDULER_ENABLED = False
ATTEMPT_FACTORY_WORKER_ENABLED = False
ATTEMPT_FACTORY_QUEUE_ENABLED = False
ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED = False
ATTEMPT_FACTORY_TOOL_EXECUTION_ENABLED = False
ATTEMPT_FACTORY_MEMORY_PERSISTENCE_ENABLED = False
ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED = False
ATTEMPT_FACTORY_API_ENABLED = False
ATTEMPT_FACTORY_UI_ENABLED = False
MARKET_CATALOG_RUNTIME_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"created_contractually", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_attempt_factory_e2e_checkpoint", "blocked", "invalid"}
ALLOWED_INITIAL_STATES = {"draft", "schema_validated", "blocked", None}
FORBIDDEN_INITIAL_STATES = {
    "queued",
    "running",
    "succeeded",
    "failed",
}
FORBIDDEN_OPERATIONAL_VALUES = {
    "queued",
    "running",
    "succeeded",
    "failed",
    "ready_for_runtime",
    "runtime_enabled",
    "operations_enabled",
    "factory_enabled",
    "gate_open",
}
FORBIDDEN_TRUE_FLAGS = {
    "attempt_factory_enabled",
    "attempt_creation_runtime_enabled",
    "runtime_enabled",
    "store_writes_enabled",
    "lifecycle_writes_enabled",
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
    "business_composition_enabled",
    "business_composition_active",
    "business_composition_layer_runtime_enabled",
    "market_catalog_runtime_enabled",
    "gate_open",
    "operations_enabled",
}


@dataclass(frozen=True)
class AttemptFactoryDecision:
    factory_id: str
    status: str
    decision: str
    readiness: str
    attempt_id: str | None
    initial_state: str | None
    execution_intent_ref: str
    attempt: ExecutionAttempt | dict[str, Any] | None = None
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["attempt"] = serialize_execution_attempt_schema(self.attempt) if self.attempt is not None else None
        payload["blocking_reasons"] = deepcopy(self.blocking_reasons)
        payload["warnings"] = deepcopy(self.warnings)
        payload["lineage"] = deepcopy(self.lineage)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_attempt_factory_decision(
    *,
    factory_id: str = "attempt_factory_contract",
    status: str = "evaluated",
    decision: str = "created_contractually",
    readiness: str = "ready_for_attempt_factory_e2e_checkpoint",
    attempt_id: str | None = None,
    initial_state: str | None = "schema_validated",
    execution_intent_ref: str = "",
    attempt: ExecutionAttempt | dict[str, Any] | None = None,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> AttemptFactoryDecision:
    return AttemptFactoryDecision(
        factory_id=factory_id,
        status=status,
        decision=decision,
        readiness=readiness,
        attempt_id=attempt_id,
        initial_state=initial_state,
        execution_intent_ref=execution_intent_ref,
        attempt=attempt,
        blocking_reasons=deepcopy(blocking_reasons or []),
        warnings=deepcopy(warnings or []),
        lineage=deepcopy(lineage or {}),
        metadata=deepcopy(metadata or {}),
    )


def build_attempt_contract_from_intent(
    execution_intent: Any,
    *,
    factory_id: str = "attempt_factory_contract",
    requested_by: str | None = None,
    source: str | None = None,
    idempotency_key: str | None = None,
    context_refs: list[Any] | None = None,
    preflight_flags: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    initial_state: str = "schema_validated",
    attempt_id: str | None = None,
    gate_decision: Any | None = None,
) -> AttemptFactoryDecision:
    intent_validation = validate_execution_intent(execution_intent)
    intent_payload = intent_validation.get("intent") or serialize_execution_intent(execution_intent)
    intent_ref = intent_payload.get("intent_id") or ""
    base_metadata = deepcopy(metadata or {})
    warnings: list[str] = []
    blockers: list[dict[str, str]] = []

    if intent_validation["status"] != "validated":
        _copy_blockers(intent_validation.get("blockers", []), blockers)
        return _blocked_or_invalid_decision(
            factory_id=factory_id,
            decision="invalid",
            readiness="invalid",
            execution_intent_ref=intent_ref,
            blocking_reasons=blockers,
            warnings=warnings,
            metadata=base_metadata,
        )

    gate = gate_decision or evaluate_operational_readiness_contracts()
    gate_validation = validate_operational_readiness_gate_decision(gate)
    gate_payload = serialize_operational_readiness_gate_decision(gate)
    if gate_validation["status"] != "validated" or gate_payload.get("decision") in {"blocked", "not_ready"}:
        _copy_blockers(gate_validation.get("blockers", []), blockers)
        if not blockers:
            _block(blockers, "gate_not_ready", "operational readiness gate blocked/not_ready")
        return _blocked_or_invalid_decision(
            factory_id=factory_id,
            decision="blocked",
            readiness="blocked",
            execution_intent_ref=intent_ref,
            blocking_reasons=blockers,
            warnings=warnings,
            metadata=base_metadata,
            lineage=_lineage(intent_payload, None, requested_by, source, idempotency_key, context_refs, gate_payload),
        )

    if initial_state not in {"draft", "schema_validated"}:
        _block(blockers, "invalid_initial_state", "initial_state debe ser draft o schema_validated")
        return _blocked_or_invalid_decision(
            factory_id=factory_id,
            decision="blocked",
            readiness="blocked",
            execution_intent_ref=intent_ref,
            blocking_reasons=blockers,
            warnings=warnings,
            metadata=base_metadata,
            lineage=_lineage(intent_payload, None, requested_by, source, idempotency_key, context_refs, gate_payload),
        )

    resolved_attempt_id = attempt_id or _generate_attempt_id(intent_ref, idempotency_key or source or factory_id)
    attempt_metadata = deepcopy(base_metadata)
    attempt_metadata.update(
        {
            "attempt_factory_contract_status": ATTEMPT_FACTORY_CONTRACT_STATUS,
            "attempt_factory_enabled": ATTEMPT_FACTORY_ENABLED,
            "idempotency_key": idempotency_key,
            "context_refs": deepcopy(context_refs or []),
            "preflight_flags": deepcopy(preflight_flags or {}),
            "state_machine_state": initial_state,
            "market_catalog_status": intent_payload.get("metadata", {}).get("market_catalog_status"),
            "market_catalog_runtime_enabled": intent_payload.get("metadata", {}).get("market_catalog_runtime_enabled"),
            "business_composition_layer_operational": intent_payload.get("metadata", {}).get("business_composition_layer_operational"),
        }
    )
    attempt = build_attempt_schema_from_intent(
        execution_intent,
        attempt_id=resolved_attempt_id,
        metadata=attempt_metadata,
    )
    if initial_state == "draft":
        attempt_payload = serialize_execution_attempt_schema(attempt)
        attempt_payload["status"] = "draft"
        attempt_payload["readiness"] = "not_ready"
        attempt_payload["metadata"]["state_machine_state"] = "draft"
        attempt = attempt_payload

    attempt_validation = validate_execution_attempt_schema(attempt)
    if attempt_validation["status"] != "validated":
        _copy_blockers(attempt_validation.get("blockers", []), blockers)
        return _blocked_or_invalid_decision(
            factory_id=factory_id,
            decision="blocked",
            readiness="blocked",
            attempt_id=resolved_attempt_id,
            initial_state="blocked",
            execution_intent_ref=intent_ref,
            blocking_reasons=blockers,
            warnings=warnings,
            metadata=base_metadata,
            lineage=_lineage(intent_payload, resolved_attempt_id, requested_by, source, idempotency_key, context_refs, gate_payload),
        )

    return build_attempt_factory_decision(
        factory_id=factory_id,
        status="evaluated",
        decision="created_contractually",
        readiness="ready_for_attempt_factory_e2e_checkpoint",
        attempt_id=resolved_attempt_id,
        initial_state=initial_state,
        execution_intent_ref=intent_ref,
        attempt=attempt,
        blocking_reasons=[],
        warnings=warnings,
        lineage=_lineage(intent_payload, resolved_attempt_id, requested_by, source, idempotency_key, context_refs, gate_payload),
        metadata={
            **base_metadata,
            "created_at": datetime.now().isoformat(),
            "contract_only": True,
            "in_memory_only": True,
            "persisted": False,
            "runtime_execution": False,
        },
    )


def validate_attempt_factory_decision(decision: AttemptFactoryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_attempt_factory_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("factory_id"), blockers, "missing_factory_id", "factory_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision no permitida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")
    _allowed(payload.get("initial_state"), ALLOWED_INITIAL_STATES, blockers, "invalid_initial_state", "initial_state no permitido")
    if payload.get("initial_state") in FORBIDDEN_INITIAL_STATES:
        _block(blockers, "runtime_state_not_allowed", "queued/running no permitidos")

    if payload.get("decision") == "created_contractually":
        _require(payload.get("attempt_id"), blockers, "missing_attempt_id", "attempt_id requerido")
        _require(payload.get("attempt"), blockers, "missing_attempt", "attempt en memoria requerido")
    if payload.get("decision") == "invalid":
        _block(blockers, "decision_invalid", "decision invalid no valida como contrato listo")
    _require(payload.get("execution_intent_ref"), blockers, "missing_execution_intent_ref", "execution_intent_ref requerido")

    if not isinstance(payload.get("blocking_reasons"), list):
        _block(blockers, "invalid_blocking_reasons", "blocking_reasons debe ser list")
    if not isinstance(payload.get("warnings"), list):
        _block(blockers, "invalid_warnings", "warnings debe ser list")
    if not isinstance(payload.get("lineage"), dict):
        _block(blockers, "invalid_lineage", "lineage debe ser dict")
    if not isinstance(payload.get("metadata"), dict):
        _block(blockers, "invalid_metadata", "metadata debe ser dict")

    lineage = payload.get("lineage") if isinstance(payload.get("lineage"), dict) else {}
    if payload.get("execution_intent_ref") and lineage.get("intent_id") not in {payload.get("execution_intent_ref"), None}:
        _block(blockers, "lineage_intent_mismatch", "lineage debe referenciar el intent")
    if payload.get("execution_intent_ref") and not lineage.get("intent_id"):
        _block(blockers, "lineage_missing_intent", "lineage debe incluir intent_id")

    attempt = payload.get("attempt")
    if attempt is not None:
        attempt_validation = validate_execution_attempt_schema(attempt)
        if attempt_validation["status"] != "validated":
            _copy_blockers(attempt_validation.get("blockers", []), blockers)
        attempt_payload = serialize_execution_attempt_schema(attempt)
        if attempt_payload.get("status") in FORBIDDEN_INITIAL_STATES:
            _block(blockers, "attempt_runtime_state_not_allowed", "attempt no puede estar queued/running")

    _scan_forbidden_values(payload, blockers)
    _validate_market_and_business_boundaries(payload, blockers)
    _validate_boundaries(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "ATTEMPT_FACTORY_CONTRACT_READY" if not blockers else "ATTEMPT_FACTORY_CONTRACT_BLOCKED",
        "readiness": "ready_for_attempt_factory_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [] if not blockers else ["attempt_factory_decision_blocked"],
        "decision": payload,
        "contract_status": ATTEMPT_FACTORY_CONTRACT_STATUS,
        "attempt_factory_enabled": ATTEMPT_FACTORY_ENABLED,
        "runtime_enabled": ATTEMPT_FACTORY_RUNTIME_ENABLED,
        "store_writes_enabled": ATTEMPT_FACTORY_STORE_WRITES_ENABLED,
        "lifecycle_writes_enabled": ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED,
        "result_store_enabled": ATTEMPT_FACTORY_RESULT_STORE_ENABLED,
        "history_writes_enabled": ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED,
        "scheduler_enabled": ATTEMPT_FACTORY_SCHEDULER_ENABLED,
        "worker_enabled": ATTEMPT_FACTORY_WORKER_ENABLED,
        "queue_enabled": ATTEMPT_FACTORY_QUEUE_ENABLED,
    }


def serialize_attempt_factory_decision(decision: AttemptFactoryDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, AttemptFactoryDecision):
        return decision.to_dict()
    payload = deepcopy(decision)
    if payload.get("attempt") is not None:
        payload["attempt"] = serialize_execution_attempt_schema(payload["attempt"])
    return payload


def get_attempt_factory_contract() -> dict[str, Any]:
    return {
        "status": ATTEMPT_FACTORY_CONTRACT_STATUS,
        "verdict": "ATTEMPT_FACTORY_CONTRACT_READY",
        "readiness": "ready_for_attempt_factory_e2e_checkpoint",
        "next_step": "PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract",
        "allowed_statuses": sorted(ALLOWED_STATUSES),
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "allowed_readiness": sorted(ALLOWED_READINESS),
        "allowed_initial_states": ["draft", "schema_validated", "blocked", None],
        "forbidden_values": sorted(FORBIDDEN_OPERATIONAL_VALUES),
        "boundaries": _boundary_flags(),
    }


def _blocked_or_invalid_decision(
    *,
    factory_id: str,
    decision: str,
    readiness: str,
    execution_intent_ref: str,
    blocking_reasons: list[dict[str, str]],
    warnings: list[str],
    metadata: dict[str, Any],
    attempt_id: str | None = None,
    initial_state: str | None = None,
    lineage: dict[str, Any] | None = None,
) -> AttemptFactoryDecision:
    return build_attempt_factory_decision(
        factory_id=factory_id,
        status="invalid" if decision == "invalid" else "blocked",
        decision=decision,
        readiness=readiness,
        attempt_id=attempt_id,
        initial_state=initial_state,
        execution_intent_ref=execution_intent_ref,
        attempt=None,
        blocking_reasons=blocking_reasons,
        warnings=warnings,
        lineage=lineage or {"intent_id": execution_intent_ref},
        metadata={**deepcopy(metadata), "contract_only": True, "in_memory_only": True, "persisted": False},
    )


def _generate_attempt_id(intent_id: str, idempotency_key: str) -> str:
    digest = hashlib.sha256(f"{intent_id}:{idempotency_key}".encode("utf-8")).hexdigest()[:12]
    return f"attempt_{intent_id}_1_{digest}"


def _lineage(
    intent_payload: dict[str, Any],
    attempt_id: str | None,
    requested_by: str | None,
    source: str | None,
    idempotency_key: str | None,
    context_refs: list[Any] | None,
    gate_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "intent_id": intent_payload.get("intent_id"),
        "attempt_id": attempt_id,
        "requested_by": requested_by or intent_payload.get("requested_by"),
        "source": source or intent_payload.get("source"),
        "idempotency_key": idempotency_key,
        "context_refs": deepcopy(context_refs or []),
        "contracts": {
            "execution_intent": True,
            "execution_attempt_schema": True,
            "execution_attempt_state_machine": True,
            "operational_readiness_gate": True,
        },
        "gate_decision": deepcopy(gate_payload or {}),
    }


def _validate_market_and_business_boundaries(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    lineage = payload.get("lineage") if isinstance(payload.get("lineage"), dict) else {}
    for scope in (metadata, lineage):
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
        "attempt_factory_enabled": ATTEMPT_FACTORY_ENABLED,
        "runtime_enabled": ATTEMPT_FACTORY_RUNTIME_ENABLED,
        "store_writes_enabled": ATTEMPT_FACTORY_STORE_WRITES_ENABLED,
        "lifecycle_writes_enabled": ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED,
        "result_store_enabled": ATTEMPT_FACTORY_RESULT_STORE_ENABLED,
        "history_writes_enabled": ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED,
        "scheduler_enabled": ATTEMPT_FACTORY_SCHEDULER_ENABLED,
        "worker_enabled": ATTEMPT_FACTORY_WORKER_ENABLED,
        "queue_enabled": ATTEMPT_FACTORY_QUEUE_ENABLED,
        "model_invocation_enabled": ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": ATTEMPT_FACTORY_TOOL_EXECUTION_ENABLED,
        "memory_persistence_enabled": ATTEMPT_FACTORY_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": ATTEMPT_FACTORY_API_ENABLED,
        "ui_enabled": ATTEMPT_FACTORY_UI_ENABLED,
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
