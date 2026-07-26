"""Contract-only state machine for future execution attempts."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from core.execution_attempt import (
    EXECUTION_ATTEMPT_EXTERNAL_ACCESS_ENABLED,
    EXECUTION_ATTEMPT_MEMORY_PERSISTENCE_ENABLED,
    EXECUTION_ATTEMPT_MODEL_INVOCATION_ENABLED,
    EXECUTION_ATTEMPT_QUEUE_ENABLED,
    EXECUTION_ATTEMPT_RESULT_STORE_ENABLED,
    EXECUTION_ATTEMPT_RUNTIME_ENABLED,
    EXECUTION_ATTEMPT_SCHEDULER_ENABLED,
    EXECUTION_ATTEMPT_STORE_WRITES_ENABLED,
    EXECUTION_ATTEMPT_TOOL_EXECUTION_ENABLED,
    EXECUTION_ATTEMPT_WORKER_ENABLED,
    serialize_execution_attempt_schema,
    validate_execution_attempt_schema,
)


EXECUTION_ATTEMPT_STATE_MACHINE_STATUS = "contract_only"
EXECUTION_ATTEMPT_STATE_MACHINE_RUNTIME_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_STORE_WRITES_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_LIFECYCLE_WRITES_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_RESULT_STORE_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_EXECUTION_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_SCHEDULER_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_WORKER_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_QUEUE_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_MODEL_INVOCATION_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_TOOL_EXECUTION_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_MEMORY_PERSISTENCE_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_EXTERNAL_ACCESS_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_API_ENABLED = False
EXECUTION_ATTEMPT_STATE_MACHINE_UI_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

CONTRACT_ONLY_STATES = (
    "draft",
    "schema_validated",
    "preflight_ready",
    "blocked",
    "cancelled",
)
FUTURE_RESERVED_STATES = (
    "queued",
    "running",
    "succeeded",
    "failed",
    "partially_succeeded",
    "retrying",
    "expired",
)
TERMINAL_STATES = (
    "blocked",
    "cancelled",
)
FUTURE_TERMINAL_STATES = (
    "succeeded",
    "failed",
    "partially_succeeded",
    "expired",
)
ALLOWED_TRANSITIONS = {
    "draft": ("schema_validated", "blocked", "cancelled"),
    "schema_validated": ("preflight_ready", "blocked", "cancelled"),
    "preflight_ready": ("blocked", "cancelled"),
    "blocked": (),
    "cancelled": (),
}
FUTURE_RESERVED_TRANSITIONS = {
    "preflight_ready": ("queued",),
    "queued": ("running",),
    "running": ("succeeded", "failed", "partially_succeeded"),
    "failed": ("retrying",),
    "retrying": ("queued",),
}
FORBIDDEN_RUNTIME_PATHS = {
    "core/execution_attempt_factory.py",
    "core/execution_result_store.py",
    "core/result_store.py",
    "core/runtime_runner.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
}


def get_allowed_execution_attempt_states() -> tuple[str, ...]:
    return CONTRACT_ONLY_STATES


def get_future_reserved_execution_attempt_states() -> tuple[str, ...]:
    return FUTURE_RESERVED_STATES


def get_terminal_execution_attempt_states() -> tuple[str, ...]:
    return TERMINAL_STATES


def get_allowed_execution_attempt_transitions() -> dict[str, tuple[str, ...]]:
    return deepcopy(ALLOWED_TRANSITIONS)


def get_future_reserved_execution_attempt_transitions() -> dict[str, tuple[str, ...]]:
    return deepcopy(FUTURE_RESERVED_TRANSITIONS)


def is_valid_execution_attempt_state(state: str) -> bool:
    return state in CONTRACT_ONLY_STATES


def is_terminal_execution_attempt_state(state: str) -> bool:
    return state in TERMINAL_STATES


def is_valid_execution_attempt_transition(from_state: str, to_state: str) -> bool:
    if not is_valid_execution_attempt_state(from_state):
        return False
    if not is_valid_execution_attempt_state(to_state):
        return False
    if is_terminal_execution_attempt_state(from_state):
        return False
    return to_state in ALLOWED_TRANSITIONS.get(from_state, ())


def validate_execution_attempt_state_machine_transition(attempt: Any, to_state: str) -> dict[str, Any]:
    original = serialize_execution_attempt_schema(attempt)
    payload = deepcopy(original)
    blockers: list[dict[str, str]] = []
    schema_validation = validate_execution_attempt_schema(payload)
    if schema_validation["status"] != "validated":
        for blocker in schema_validation["blockers"]:
            _block(blockers, blocker["code"], blocker["message"])

    current_state = _current_state(payload)
    _validate_state(current_state, blockers, role="from")
    _validate_state(to_state, blockers, role="to")
    if current_state in TERMINAL_STATES:
        _block(blockers, "terminal_state_transition_not_allowed", f"{current_state} es terminal")
    if current_state in FUTURE_RESERVED_STATES or to_state in FUTURE_RESERVED_STATES:
        _block(blockers, "future_reserved_state_not_active", "estado futuro/no activo no permitido")
    if current_state in CONTRACT_ONLY_STATES and to_state in CONTRACT_ONLY_STATES:
        if to_state not in ALLOWED_TRANSITIONS.get(current_state, ()):
            _block(blockers, "transition_not_allowed", f"{current_state}->{to_state} no permitido")
    _validate_boundaries(blockers)
    _validate_no_runtime_paths(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY" if not blockers else "EXECUTION_ATTEMPT_STATE_MACHINE_BLOCKED",
        "readiness": "ready_for_result_store_boundary_audit" if not blockers else "blocked",
        "from_state": current_state,
        "to_state": to_state,
        "transition": f"{current_state}->{to_state}",
        "blockers": blockers,
        "warnings": [],
        "attempt": payload,
        "mutated": payload != original,
        "state_machine_status": EXECUTION_ATTEMPT_STATE_MACHINE_STATUS,
        "runtime_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_RUNTIME_ENABLED,
        "store_writes_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_STORE_WRITES_ENABLED,
        "lifecycle_writes_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_LIFECYCLE_WRITES_ENABLED,
        "result_store_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_RESULT_STORE_ENABLED,
        "execution_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_EXECUTION_ENABLED,
        "scheduler_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_SCHEDULER_ENABLED,
        "worker_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_WORKER_ENABLED,
        "queue_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_QUEUE_ENABLED,
    }


def serialize_execution_attempt_state_machine_contract() -> dict[str, Any]:
    return {
        "status": EXECUTION_ATTEMPT_STATE_MACHINE_STATUS,
        "verdict": "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY",
        "readiness": "ready_for_result_store_boundary_audit",
        "allowed_states": CONTRACT_ONLY_STATES,
        "future_reserved_states": FUTURE_RESERVED_STATES,
        "terminal_states": TERMINAL_STATES,
        "future_terminal_states": FUTURE_TERMINAL_STATES,
        "allowed_transitions": get_allowed_execution_attempt_transitions(),
        "future_reserved_transitions": get_future_reserved_execution_attempt_transitions(),
        "boundaries": {
            "runtime_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_RUNTIME_ENABLED,
            "store_writes_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_STORE_WRITES_ENABLED,
            "lifecycle_writes_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_LIFECYCLE_WRITES_ENABLED,
            "result_store_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_RESULT_STORE_ENABLED,
            "execution_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_EXECUTION_ENABLED,
            "scheduler_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_SCHEDULER_ENABLED,
            "worker_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_WORKER_ENABLED,
            "queue_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_QUEUE_ENABLED,
            "model_invocation_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_MODEL_INVOCATION_ENABLED,
            "tool_execution_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_TOOL_EXECUTION_ENABLED,
            "memory_persistence_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_MEMORY_PERSISTENCE_ENABLED,
            "external_access_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_EXTERNAL_ACCESS_ENABLED,
            "api_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_API_ENABLED,
            "ui_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_UI_ENABLED,
        },
    }


def _current_state(payload: dict[str, Any]) -> Any:
    metadata = payload.get("metadata") or {}
    return metadata.get("state_machine_state") or payload.get("status") or payload.get("lifecycle_state")


def _validate_state(state: Any, blockers: list[dict[str, str]], *, role: str) -> None:
    if state in FUTURE_RESERVED_STATES:
        _block(blockers, f"{role}_state_future_reserved", f"{state} es futuro/no activo")
    elif state not in CONTRACT_ONLY_STATES:
        _block(blockers, f"{role}_state_invalid", f"{state} no es estado contract-only valido")


def _validate_boundaries(blockers: list[dict[str, str]]) -> None:
    boundaries = {
        "runtime_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_RUNTIME_ENABLED,
        "store_writes_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_STORE_WRITES_ENABLED,
        "lifecycle_writes_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_LIFECYCLE_WRITES_ENABLED,
        "result_store_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_RESULT_STORE_ENABLED,
        "execution_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_EXECUTION_ENABLED,
        "scheduler_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_SCHEDULER_ENABLED,
        "worker_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_WORKER_ENABLED,
        "queue_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_QUEUE_ENABLED,
        "model_invocation_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_TOOL_EXECUTION_ENABLED,
        "memory_persistence_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": EXECUTION_ATTEMPT_STATE_MACHINE_EXTERNAL_ACCESS_ENABLED,
        "attempt_runtime_enabled": EXECUTION_ATTEMPT_RUNTIME_ENABLED,
        "attempt_store_writes_enabled": EXECUTION_ATTEMPT_STORE_WRITES_ENABLED,
        "attempt_result_store_enabled": EXECUTION_ATTEMPT_RESULT_STORE_ENABLED,
        "attempt_scheduler_enabled": EXECUTION_ATTEMPT_SCHEDULER_ENABLED,
        "attempt_worker_enabled": EXECUTION_ATTEMPT_WORKER_ENABLED,
        "attempt_queue_enabled": EXECUTION_ATTEMPT_QUEUE_ENABLED,
        "attempt_model_invocation_enabled": EXECUTION_ATTEMPT_MODEL_INVOCATION_ENABLED,
        "attempt_tool_execution_enabled": EXECUTION_ATTEMPT_TOOL_EXECUTION_ENABLED,
        "attempt_memory_persistence_enabled": EXECUTION_ATTEMPT_MEMORY_PERSISTENCE_ENABLED,
        "attempt_external_access_enabled": EXECUTION_ATTEMPT_EXTERNAL_ACCESS_ENABLED,
    }
    for field, value in boundaries.items():
        if value is not False:
            _block(blockers, f"{field}_not_allowed", f"{field} debe ser false")


def _validate_no_runtime_paths(blockers: list[dict[str, str]]) -> None:
    for relative_path in FORBIDDEN_RUNTIME_PATHS:
        if Path(relative_path).exists():
            _block(blockers, "runtime_path_not_allowed", f"{relative_path} no debe existir")


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
