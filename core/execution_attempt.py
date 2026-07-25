"""Schema-only contract for future operational execution attempts."""

from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from core.execution_intent import (
    ALLOWED_INTENT_TYPES,
    ALLOWED_MODES,
    ALLOWED_TARGET_TYPES,
    validate_execution_intent,
)


EXECUTION_ATTEMPT_SCHEMA_STATUS = "schema_only"
EXECUTION_ATTEMPT_RUNTIME_ENABLED = False
EXECUTION_ATTEMPT_FACTORY_ENABLED = False
EXECUTION_ATTEMPT_STORE_WRITES_ENABLED = False
EXECUTION_ATTEMPT_RESULT_STORE_ENABLED = False
EXECUTION_ATTEMPT_EXECUTION_ENABLED = False
EXECUTION_ATTEMPT_SCHEDULER_ENABLED = False
EXECUTION_ATTEMPT_WORKER_ENABLED = False
EXECUTION_ATTEMPT_QUEUE_ENABLED = False
EXECUTION_ATTEMPT_MODEL_INVOCATION_ENABLED = False
EXECUTION_ATTEMPT_TOOL_EXECUTION_ENABLED = False
EXECUTION_ATTEMPT_MEMORY_PERSISTENCE_ENABLED = False
EXECUTION_ATTEMPT_EXTERNAL_ACCESS_ENABLED = False
EXECUTION_ATTEMPT_API_ENABLED = False
EXECUTION_ATTEMPT_UI_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ATTEMPT_ID_PATTERN = re.compile(r"^attempt_(?P<intent_id>[A-Za-z0-9_.:-]+)_(?P<sequence>[0-9]{1,8})_(?P<hash>[a-f0-9]{8,16})$")
ALLOWED_ATTEMPT_STATUSES = {
    "draft",
    "schema_validated",
    "rejected",
    "blocked",
}
ALLOWED_LIFECYCLE_STATES = {
    "not_started",
    "preflight_only",
    "blocked",
}
ALLOWED_READINESS = {
    "not_ready",
    "ready_for_state_machine_design",
    "blocked",
}
OPERATIONAL_CONSTRAINTS = {
    "allow_runtime_execution": "runtime_execution_not_allowed",
    "allow_store_write": "store_write_not_allowed",
    "allow_result_store_write": "result_store_write_not_allowed",
    "allow_scheduler": "scheduler_not_allowed",
    "allow_worker": "worker_not_allowed",
    "allow_queue": "queue_not_allowed",
    "allow_model_invocation": "model_invocation_not_allowed",
    "allow_tool_execution": "tool_execution_not_allowed",
    "allow_memory_persistence": "memory_persistence_not_allowed",
    "allow_external_access": "external_access_not_allowed",
}
FORBIDDEN_RUNTIME_PATHS = {
    "core/execution_attempt_factory.py",
    "core/execution_result_store.py",
    "core/result_store.py",
    "core/runtime_runner.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
}


@dataclass(frozen=True)
class ExecutionAttemptTarget:
    target_type: str
    target_id: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptConstraints:
    allow_runtime_execution: bool = False
    allow_store_write: bool = False
    allow_result_store_write: bool = False
    allow_scheduler: bool = False
    allow_worker: bool = False
    allow_queue: bool = False
    allow_model_invocation: bool = False
    allow_tool_execution: bool = False
    allow_memory_persistence: bool = False
    allow_external_access: bool = False

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttempt:
    attempt_id: str
    intent_id: str
    intent_type: str
    target: ExecutionAttemptTarget
    mode: str
    requested_by: str
    status: str
    lifecycle_state: str
    readiness: str
    created_at: str
    updated_at: str | None = None
    result_ref: Any | None = None
    error_ref: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    constraints: ExecutionAttemptConstraints = field(default_factory=ExecutionAttemptConstraints)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["target"] = self.target.to_dict()
        payload["constraints"] = self.constraints.to_dict()
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_execution_attempt_schema(
    *,
    attempt_id: str,
    intent_id: str,
    intent_type: str,
    target_type: str,
    target_id: str,
    mode: str,
    requested_by: str,
    status: str = "draft",
    lifecycle_state: str = "not_started",
    readiness: str = "not_ready",
    created_at: str | None = None,
    updated_at: str | None = None,
    result_ref: Any | None = None,
    error_ref: Any | None = None,
    metadata: dict[str, Any] | None = None,
    constraints: dict[str, bool] | None = None,
) -> ExecutionAttempt:
    return ExecutionAttempt(
        attempt_id=attempt_id,
        intent_id=intent_id,
        intent_type=intent_type,
        target=ExecutionAttemptTarget(target_type=target_type, target_id=target_id),
        mode=mode,
        requested_by=requested_by,
        status=status,
        lifecycle_state=lifecycle_state,
        readiness=readiness,
        created_at=created_at or datetime.now().isoformat(),
        updated_at=updated_at,
        result_ref=result_ref,
        error_ref=error_ref,
        metadata=deepcopy(metadata or {}),
        constraints=ExecutionAttemptConstraints(**(constraints or {})),
    )


def serialize_execution_attempt_schema(attempt: ExecutionAttempt | dict[str, Any]) -> dict[str, Any]:
    if isinstance(attempt, ExecutionAttempt):
        return attempt.to_dict()
    return deepcopy(attempt)


def build_attempt_schema_from_intent(
    intent: Any,
    *,
    attempt_id: str,
    sequence: int = 1,
    metadata: dict[str, Any] | None = None,
) -> ExecutionAttempt:
    intent_validation = validate_execution_intent(intent)
    if intent_validation["status"] != "validated":
        raise ValueError("execution_intent_not_validated")
    payload = intent_validation["intent"]
    target = payload.get("target") or {}
    merged_metadata = deepcopy(metadata or {})
    merged_metadata["source_intent_validated"] = True
    merged_metadata["sequence"] = sequence
    return build_execution_attempt_schema(
        attempt_id=attempt_id,
        intent_id=payload["intent_id"],
        intent_type=payload["intent_type"],
        target_type=target.get("target_type"),
        target_id=target.get("target_id"),
        mode=payload["mode"],
        requested_by=payload["requested_by"],
        status="schema_validated",
        lifecycle_state="not_started",
        readiness="ready_for_state_machine_design",
        metadata=merged_metadata,
    )


def validate_execution_attempt_schema(attempt: ExecutionAttempt | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_execution_attempt_schema(attempt)
    blockers: list[dict[str, str]] = []
    target = payload.get("target") or {}
    constraints = payload.get("constraints") or {}

    _require(payload.get("attempt_id"), blockers, "missing_attempt_id", "attempt_id requerido")
    _validate_attempt_id(payload.get("attempt_id"), payload.get("intent_id"), blockers)
    _require(payload.get("intent_id"), blockers, "missing_intent_id", "intent_id requerido")
    _allowed(payload.get("intent_type"), ALLOWED_INTENT_TYPES, blockers, "invalid_intent_type", "intent_type no permitido")
    _allowed(target.get("target_type"), ALLOWED_TARGET_TYPES, blockers, "invalid_target_type", "target_type no permitido")
    _require(target.get("target_id"), blockers, "missing_target_id", "target_id requerido")
    _allowed(payload.get("mode"), ALLOWED_MODES, blockers, "invalid_mode", "mode no permitido")
    _allowed(payload.get("status"), ALLOWED_ATTEMPT_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("lifecycle_state"), ALLOWED_LIFECYCLE_STATES, blockers, "invalid_lifecycle_state", "lifecycle_state no permitido")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")

    if payload.get("result_ref") is not None:
        _block(blockers, "result_ref_not_allowed", "result_ref debe ser None en schema-only")
    if payload.get("error_ref") is not None:
        _block(blockers, "error_ref_not_allowed", "error_ref debe ser None en schema-only")

    for field_name, code in OPERATIONAL_CONSTRAINTS.items():
        if constraints.get(field_name) is not False:
            _block(blockers, code, f"{field_name}=true no permitido en execution attempt schema-only")

    if target.get("target_type") == "market":
        metadata = payload.get("metadata") or {}
        if metadata.get("market_catalog_status") != "planned_not_active":
            _block(blockers, "market_catalog_not_planned", "Market Catalog debe permanecer planned_not_active")
        if metadata.get("market_catalog_runtime_enabled") not in (None, False):
            _block(blockers, "market_catalog_runtime_not_allowed", "Market Catalog runtime no permitido")

    if target.get("target_type") == "business_composition_candidate":
        metadata = payload.get("metadata") or {}
        if metadata.get("business_composition_layer_operational") not in (None, False):
            _block(blockers, "business_composition_layer_not_allowed", "Business Composition Layer no operativa")
        if BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED is not False:
            _block(blockers, "business_composition_layer_runtime_not_allowed", "Business Composition Layer runtime no permitido")

    for relative_path in FORBIDDEN_RUNTIME_PATHS:
        if Path(relative_path).exists():
            _block(blockers, "runtime_path_not_allowed", f"{relative_path} no debe existir en schema-only")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "EXECUTION_ATTEMPT_SCHEMA_READY" if not blockers else "EXECUTION_ATTEMPT_SCHEMA_BLOCKED",
        "readiness": "ready_for_operational_state_machine_contract" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [],
        "attempt": payload,
        "schema_status": EXECUTION_ATTEMPT_SCHEMA_STATUS,
        "runtime_enabled": EXECUTION_ATTEMPT_RUNTIME_ENABLED,
        "factory_enabled": EXECUTION_ATTEMPT_FACTORY_ENABLED,
        "store_writes_enabled": EXECUTION_ATTEMPT_STORE_WRITES_ENABLED,
        "result_store_enabled": EXECUTION_ATTEMPT_RESULT_STORE_ENABLED,
        "execution_enabled": EXECUTION_ATTEMPT_EXECUTION_ENABLED,
    }


def _validate_attempt_id(attempt_id: Any, intent_id: Any, blockers: list[dict[str, str]]) -> None:
    if not attempt_id:
        return
    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.match(attempt_id):
        _block(blockers, "invalid_attempt_id_format", "attempt_id debe seguir attempt_<intent_id>_<sequence>_<short_hash>")
        return
    if intent_id and not attempt_id.startswith(f"attempt_{intent_id}_"):
        _block(blockers, "attempt_id_intent_mismatch", "attempt_id debe incluir intent_id")


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, "", {}, []):
        _block(blockers, code, message)


def _allowed(value: Any, allowed: set[str], blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value not in allowed:
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
