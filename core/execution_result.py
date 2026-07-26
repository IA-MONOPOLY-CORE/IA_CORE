"""Read-only contract for future execution results and result store entries."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from core.execution_attempt import serialize_execution_attempt_schema, validate_execution_attempt_schema
from core.execution_attempt_state_machine import is_valid_execution_attempt_state


EXECUTION_RESULT_CONTRACT_STATUS = "read_only_contract"
EXECUTION_RESULT_STORE_ENABLED = False
EXECUTION_RESULT_STORE_WRITES_ENABLED = False
EXECUTION_RESULT_ID_GENERATOR_ENABLED = False
EXECUTION_RESULT_RUNTIME_ENABLED = False
EXECUTION_RESULT_EXECUTION_ENABLED = False
EXECUTION_RESULT_LIFECYCLE_WRITES_ENABLED = False
EXECUTION_RESULT_SCHEDULER_ENABLED = False
EXECUTION_RESULT_WORKER_ENABLED = False
EXECUTION_RESULT_QUEUE_ENABLED = False
EXECUTION_RESULT_MODEL_INVOCATION_ENABLED = False
EXECUTION_RESULT_TOOL_EXECUTION_ENABLED = False
EXECUTION_RESULT_MEMORY_PERSISTENCE_ENABLED = False
EXECUTION_RESULT_EXTERNAL_ACCESS_ENABLED = False
EXECUTION_RESULT_API_ENABLED = False
EXECUTION_RESULT_UI_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ALLOWED_RESULT_STATUSES = {
    "draft",
    "schema_validated",
    "blocked",
    "rejected",
}
FUTURE_RESULT_STATUSES = {
    "succeeded",
    "failed",
    "partially_succeeded",
    "completed",
}
ALLOWED_RESULT_TYPES = {
    "audit_only",
    "contract_validation",
    "dry_run_placeholder",
    "preflight_placeholder",
    "error_placeholder",
}
OPERATIONAL_CONSTRAINTS = {
    "allow_runtime_execution": "runtime_execution_not_allowed",
    "allow_external_access": "external_access_not_allowed",
    "allow_model_invocation": "model_invocation_not_allowed",
    "allow_tool_execution": "tool_execution_not_allowed",
    "allow_memory_persistence": "memory_persistence_not_allowed",
    "allow_store_write": "store_write_not_allowed",
    "allow_lifecycle_write": "lifecycle_write_not_allowed",
    "allow_result_store_write": "result_store_write_not_allowed",
}
FORBIDDEN_RUNTIME_PATHS = {
    "runtime/execution_results",
    "core/result_store.py",
    "core/result_store_writer.py",
    "core/result_id_generator.py",
    "core/execution_result_store.py",
}


@dataclass(frozen=True)
class ExecutionResultConstraints:
    allow_runtime_execution: bool = False
    allow_external_access: bool = False
    allow_model_invocation: bool = False
    allow_tool_execution: bool = False
    allow_memory_persistence: bool = False
    allow_store_write: bool = False
    allow_lifecycle_write: bool = False
    allow_result_store_write: bool = False

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionResult:
    result_id: str
    attempt_id: str
    intent_id: str
    status: str
    result_type: str
    created_at: str
    completed_at: str | None = None
    output_ref: Any | None = None
    error_ref: Any | None = None
    summary: str | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    artifacts: list[Any] = field(default_factory=list)
    warnings: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    constraints: ExecutionResultConstraints = field(default_factory=ExecutionResultConstraints)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["metrics"] = deepcopy(self.metrics)
        payload["artifacts"] = deepcopy(self.artifacts)
        payload["warnings"] = deepcopy(self.warnings)
        payload["metadata"] = deepcopy(self.metadata)
        payload["constraints"] = self.constraints.to_dict()
        return payload


def build_execution_result_contract(
    *,
    result_id: str,
    attempt_id: str,
    intent_id: str,
    status: str = "draft",
    result_type: str = "contract_validation",
    created_at: str | None = None,
    completed_at: str | None = None,
    output_ref: Any | None = None,
    error_ref: Any | None = None,
    summary: str | None = None,
    metrics: dict[str, Any] | None = None,
    artifacts: list[Any] | None = None,
    warnings: list[Any] | None = None,
    metadata: dict[str, Any] | None = None,
    constraints: dict[str, bool] | None = None,
) -> ExecutionResult:
    return ExecutionResult(
        result_id=result_id,
        attempt_id=attempt_id,
        intent_id=intent_id,
        status=status,
        result_type=result_type,
        created_at=created_at or datetime.now().isoformat(),
        completed_at=completed_at,
        output_ref=output_ref,
        error_ref=error_ref,
        summary=summary,
        metrics=deepcopy(metrics or {}),
        artifacts=deepcopy(artifacts or []),
        warnings=deepcopy(warnings or []),
        metadata=deepcopy(metadata or {}),
        constraints=ExecutionResultConstraints(**(constraints or {})),
    )


def serialize_execution_result_contract(result: ExecutionResult | dict[str, Any]) -> dict[str, Any]:
    if isinstance(result, ExecutionResult):
        return result.to_dict()
    return deepcopy(result)


def build_result_contract_from_attempt(
    attempt: Any,
    *,
    result_id: str,
    result_type: str = "contract_validation",
    metadata: dict[str, Any] | None = None,
) -> ExecutionResult:
    if not result_id:
        raise ValueError("result_id_required")
    attempt_validation = validate_execution_attempt_schema(attempt)
    if attempt_validation["status"] != "validated":
        raise ValueError("execution_attempt_schema_not_validated")
    payload = serialize_execution_attempt_schema(attempt)
    state = (payload.get("metadata") or {}).get("state_machine_state") or payload.get("status")
    if state and not is_valid_execution_attempt_state(state):
        raise ValueError("execution_attempt_state_not_contract_only")
    merged_metadata = deepcopy(metadata or {})
    merged_metadata["source_attempt_validated"] = True
    merged_metadata["source_attempt_state"] = state
    return build_execution_result_contract(
        result_id=result_id,
        attempt_id=payload["attempt_id"],
        intent_id=payload["intent_id"],
        status="schema_validated",
        result_type=result_type,
        output_ref=None,
        error_ref=None,
        metadata=merged_metadata,
    )


def validate_execution_result_contract(result: ExecutionResult | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_execution_result_contract(result)
    blockers: list[dict[str, str]] = []
    constraints = payload.get("constraints") or {}

    _require(payload.get("result_id"), blockers, "missing_result_id", "result_id requerido")
    _require(payload.get("attempt_id"), blockers, "missing_attempt_id", "attempt_id requerido")
    _require(payload.get("intent_id"), blockers, "missing_intent_id", "intent_id requerido")
    _allowed(payload.get("status"), ALLOWED_RESULT_STATUSES, blockers, "invalid_status", "status no permitido")
    if payload.get("status") in FUTURE_RESULT_STATUSES:
        _block(blockers, "future_result_status_not_allowed", "status operativo futuro no permitido")
    _allowed(payload.get("result_type"), ALLOWED_RESULT_TYPES, blockers, "invalid_result_type", "result_type no permitido")
    _require(payload.get("created_at"), blockers, "missing_created_at", "created_at requerido")
    if payload.get("output_ref") is not None:
        _block(blockers, "output_ref_not_allowed", "output_ref debe ser None en contrato read-only")
    if payload.get("error_ref") is not None:
        _block(blockers, "error_ref_not_allowed", "error_ref debe ser None en contrato read-only")
    if payload.get("summary") is not None and not isinstance(payload.get("summary"), str):
        _block(blockers, "invalid_summary", "summary debe ser string o None")
    if not isinstance(payload.get("metrics"), dict):
        _block(blockers, "invalid_metrics", "metrics debe ser dict")
    if not isinstance(payload.get("artifacts"), list):
        _block(blockers, "invalid_artifacts", "artifacts debe ser list")
    if not isinstance(payload.get("warnings"), list):
        _block(blockers, "invalid_warnings", "warnings debe ser list")
    if not isinstance(payload.get("metadata"), dict):
        _block(blockers, "invalid_metadata", "metadata debe ser dict")
    for field_name, code in OPERATIONAL_CONSTRAINTS.items():
        if constraints.get(field_name) is not False:
            _block(blockers, code, f"{field_name}=true no permitido en execution result read-only")
    _validate_boundaries(blockers)
    _validate_no_runtime_paths(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "EXECUTION_RESULT_CONTRACT_READY" if not blockers else "EXECUTION_RESULT_CONTRACT_BLOCKED",
        "readiness": "ready_for_result_history_read_model_integration_audit" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [],
        "result": payload,
        "contract_status": EXECUTION_RESULT_CONTRACT_STATUS,
        "result_store_enabled": EXECUTION_RESULT_STORE_ENABLED,
        "store_writes_enabled": EXECUTION_RESULT_STORE_WRITES_ENABLED,
        "result_id_generator_enabled": EXECUTION_RESULT_ID_GENERATOR_ENABLED,
        "runtime_enabled": EXECUTION_RESULT_RUNTIME_ENABLED,
        "execution_enabled": EXECUTION_RESULT_EXECUTION_ENABLED,
        "lifecycle_writes_enabled": EXECUTION_RESULT_LIFECYCLE_WRITES_ENABLED,
    }


def _validate_boundaries(blockers: list[dict[str, str]]) -> None:
    boundaries = {
        "result_store_enabled": EXECUTION_RESULT_STORE_ENABLED,
        "store_writes_enabled": EXECUTION_RESULT_STORE_WRITES_ENABLED,
        "result_id_generator_enabled": EXECUTION_RESULT_ID_GENERATOR_ENABLED,
        "runtime_enabled": EXECUTION_RESULT_RUNTIME_ENABLED,
        "execution_enabled": EXECUTION_RESULT_EXECUTION_ENABLED,
        "lifecycle_writes_enabled": EXECUTION_RESULT_LIFECYCLE_WRITES_ENABLED,
        "scheduler_enabled": EXECUTION_RESULT_SCHEDULER_ENABLED,
        "worker_enabled": EXECUTION_RESULT_WORKER_ENABLED,
        "queue_enabled": EXECUTION_RESULT_QUEUE_ENABLED,
        "model_invocation_enabled": EXECUTION_RESULT_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": EXECUTION_RESULT_TOOL_EXECUTION_ENABLED,
        "memory_persistence_enabled": EXECUTION_RESULT_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": EXECUTION_RESULT_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": EXECUTION_RESULT_API_ENABLED,
        "ui_enabled": EXECUTION_RESULT_UI_ENABLED,
    }
    for field, value in boundaries.items():
        if value is not False:
            _block(blockers, f"{field}_not_allowed", f"{field} debe ser false")


def _validate_no_runtime_paths(blockers: list[dict[str, str]]) -> None:
    for relative_path in FORBIDDEN_RUNTIME_PATHS:
        if Path(relative_path).exists():
            _block(blockers, "runtime_path_not_allowed", f"{relative_path} no debe existir")


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
