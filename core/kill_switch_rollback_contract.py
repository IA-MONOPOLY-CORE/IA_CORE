"""Future-only kill switch and rollback contract.

This module represents future stop/rollback decisions as serializable contract
objects. It never terminates processes, cancels jobs, drains queues, stops
workers, performs rollbacks, runs git, mutates manifests/stores, reads env or
secrets, touches filesystem, opens network/browser access, executes tools, or
changes runtime state.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any, Mapping


KILL_SWITCH_ROLLBACK_CONTRACT_READY = True
KILL_SWITCH_ROLLBACK_OPERATIONAL = False

KILL_SWITCH_ENABLED = False
ROLLBACK_ENABLED = False
KILL_SWITCH_EXECUTION_ENABLED = False
ROLLBACK_EXECUTION_ENABLED = False
PROCESS_TERMINATION_ENABLED = False
JOB_CANCELLATION_ENABLED = False
QUEUE_DRAIN_ENABLED = False
WORKER_STOP_ENABLED = False
SCHEDULER_STOP_ENABLED = False
RUNNER_STOP_ENABLED = False
EXECUTOR_STOP_ENABLED = False

RUNTIME_ACTIVATION_FROM_KILL_SWITCH_ENABLED = False
RUNTIME_EXECUTION_FROM_KILL_SWITCH_ENABLED = False
DRY_RUN_EXECUTION_FROM_KILL_SWITCH_ENABLED = False

ROLLBACK_FILESYSTEM_ENABLED = False
ROLLBACK_GIT_ENABLED = False
ROLLBACK_STORE_MUTATION_ENABLED = False
ROLLBACK_MANIFEST_MUTATION_ENABLED = False
ROLLBACK_DATABASE_ENABLED = False
ROLLBACK_MEMORY_ENABLED = False

KILL_SWITCH_TOOL_EXECUTION_ENABLED = False
KILL_SWITCH_MODEL_INVOCATION_ENABLED = False
KILL_SWITCH_CONTEXT_INJECTION_ENABLED = False
KILL_SWITCH_OUTPUT_DELIVERY_ENABLED = False
KILL_SWITCH_NETWORK_ENABLED = False
KILL_SWITCH_API_ENABLED = False
KILL_SWITCH_BROWSER_ENABLED = False
KILL_SWITCH_FILESYSTEM_ENABLED = False
KILL_SWITCH_ENV_ACCESS_ENABLED = False
KILL_SWITCH_SECRET_ACCESS_ENABLED = False

KILL_SWITCH_UI_TARS_ENABLED = False
KILL_SWITCH_HERMES_ENABLED = False
KILL_SWITCH_N8N_ENABLED = False
KILL_SWITCH_HOME_ASSISTANT_ENABLED = False

KILL_SWITCH_ROLLBACK_ALLOWED_ACTION_TYPES = ("kill_switch", "rollback")
KILL_SWITCH_ROLLBACK_ALLOWED_CONCEPTUAL_STATES = (
    "kill_switch_requested",
    "kill_switch_policy_checked",
    "kill_switch_blocked",
    "kill_switch_simulated",
    "rollback_requested",
    "rollback_policy_checked",
    "rollback_blocked",
    "rollback_simulated",
    "rollback_manifest_projected",
    "rollback_invalid",
)
KILL_SWITCH_ROLLBACK_FORBIDDEN_OPERATIONAL_STATES = (
    "process_killed",
    "job_cancelled",
    "queue_drained",
    "worker_stopped",
    "scheduler_stopped",
    "runner_stopped",
    "executor_stopped",
    "files_reverted",
    "git_reverted",
    "store_mutated",
    "database_rolled_back",
    "memory_reverted",
    "runtime_open",
    "runtime_active",
    "execution_enabled",
    "operations_enabled",
    "gate_open",
)

KILL_SWITCH_ROLLBACK_CONTRACT_STATUS = "KILL_SWITCH_ROLLBACK_CONTRACT_READY"
KILL_SWITCH_ROLLBACK_READINESS = "ready_for_human_approval_gate_planning"
KILL_SWITCH_ROLLBACK_NEXT_STEP = "PROMPT 3.39 — Human approval gate planning"

SECURITY_BASELINE = (
    "Security Layer",
    "Agent Permission Contract",
    "Secrets Policy",
    "Prompt Injection Defense",
    "Sandbox Boundary",
    "Tool Boundary",
    "Model Invocation Boundary",
    "Context Boundary",
    "Output Boundary",
    "Runtime Activation Gate",
    "Observability/Audit Trail Audit",
)
BASE_AUDIT_REQUIREMENTS = (
    "future audit trail",
    "future manifest projection",
    "future human approval",
    "request id",
    "actor/requested_by",
    "reason",
    "action_type",
    "target_scope",
    "target_ids",
    "policy check",
    "decision",
    "manifest reference",
)

SUSPICIOUS_METADATA_KEY_FRAGMENTS = (
    "secret",
    "token",
    "api_key",
    "password",
    "credential",
    "private_key",
    "raw_output",
    "tool_payload",
    "model_prompt",
    "context_payload",
    "output_payload",
    "filesystem_path",
    "git_command",
    "shell_command",
    "process_id",
    "worker_id",
    "queue_id",
    "database_uri",
    "provider_client",
    "runtime_executor",
)


@dataclass(frozen=True)
class KillSwitchRollbackRequest:
    request_id: str
    requested_by: str
    reason: str
    action_type: str
    target_scope: tuple[str, ...]
    target_ids: tuple[str, ...]
    rollback_manifest_ref: str | None
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class KillSwitchRollbackDecision:
    request_id: str
    decision_id: str
    allowed: bool
    action_type: str
    conceptual_state: str
    blocked_reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    security_baseline: tuple[str, ...]
    audit_requirements: tuple[str, ...]
    no_activation_confirmed: bool
    no_runtime_effect_confirmed: bool


@dataclass(frozen=True)
class KillSwitchRollbackContractResult:
    request: KillSwitchRollbackRequest
    decision: KillSwitchRollbackDecision
    contract_status: str
    readiness: str
    next_step: str
    kill_switch_enabled: bool
    rollback_enabled: bool
    kill_switch_execution_enabled: bool
    rollback_execution_enabled: bool
    runtime_activation_enabled: bool
    runtime_execution_enabled: bool
    dry_run_execution_enabled: bool
    process_termination_enabled: bool
    job_cancellation_enabled: bool
    queue_drain_enabled: bool
    worker_stop_enabled: bool
    scheduler_stop_enabled: bool
    runner_stop_enabled: bool
    executor_stop_enabled: bool
    filesystem_rollback_enabled: bool
    git_rollback_enabled: bool
    store_mutation_enabled: bool
    manifest_mutation_enabled: bool
    database_rollback_enabled: bool
    memory_rollback_enabled: bool
    external_access_enabled: bool


def create_kill_switch_rollback_request(
    *,
    request_id: str,
    requested_by: str,
    reason: str,
    action_type: str,
    target_scope: tuple[str, ...] | list[str],
    target_ids: tuple[str, ...] | list[str],
    rollback_manifest_ref: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> KillSwitchRollbackRequest:
    """Create a future-only request. No stop/rollback or I/O occurs."""
    _require_non_empty("request_id", request_id)
    _require_non_empty("requested_by", requested_by)
    _require_non_empty("reason", reason)
    _require_non_empty("action_type", action_type)
    resolved_action = action_type.strip()
    if resolved_action not in KILL_SWITCH_ROLLBACK_ALLOWED_ACTION_TYPES:
        raise ValueError("action_type no permitido")
    scope = _validate_non_empty_tuple("target_scope", target_scope)
    ids = _validate_non_empty_tuple("target_ids", target_ids)
    manifest_ref = rollback_manifest_ref.strip() if isinstance(rollback_manifest_ref, str) and rollback_manifest_ref.strip() else None
    if resolved_action == "rollback" and not manifest_ref:
        raise ValueError("rollback_manifest_ref requerido para rollback")
    clean_metadata = _validate_and_freeze_metadata(metadata or {})
    return KillSwitchRollbackRequest(
        request_id=request_id.strip(),
        requested_by=requested_by.strip(),
        reason=reason.strip(),
        action_type=resolved_action,
        target_scope=scope,
        target_ids=ids,
        rollback_manifest_ref=manifest_ref,
        metadata=clean_metadata,
    )


def evaluate_kill_switch_rollback_request(
    request: KillSwitchRollbackRequest,
    *,
    conceptual_state: str | None = None,
) -> KillSwitchRollbackDecision:
    """Evaluate representability without allowing operational effects."""
    if not isinstance(request, KillSwitchRollbackRequest):
        raise TypeError("request debe ser KillSwitchRollbackRequest")
    blockers: list[str] = []
    default_state = "kill_switch_policy_checked" if request.action_type == "kill_switch" else "rollback_policy_checked"
    resolved_state = conceptual_state or default_state
    if resolved_state in KILL_SWITCH_ROLLBACK_FORBIDDEN_OPERATIONAL_STATES:
        blockers.append(f"operational_state_forbidden:{resolved_state}")
        resolved_state = "kill_switch_blocked" if request.action_type == "kill_switch" else "rollback_blocked"
    elif resolved_state not in KILL_SWITCH_ROLLBACK_ALLOWED_CONCEPTUAL_STATES:
        blockers.append(f"conceptual_state_not_allowed:{resolved_state}")
        resolved_state = "rollback_invalid"
    try:
        _validate_and_freeze_metadata(request.metadata)
    except ValueError as exc:
        blockers.append(str(exc))
        resolved_state = "kill_switch_blocked" if request.action_type == "kill_switch" else "rollback_blocked"
    allowed = not blockers
    return KillSwitchRollbackDecision(
        request_id=request.request_id,
        decision_id=f"kill_switch_rollback_decision_{request.request_id}",
        allowed=allowed,
        action_type=request.action_type,
        conceptual_state=resolved_state,
        blocked_reasons=tuple(blockers),
        warnings=("allowed_true_is_representability_only", "human_approval_gate_required_future"),
        security_baseline=SECURITY_BASELINE,
        audit_requirements=_audit_requirements_for(request),
        no_activation_confirmed=True,
        no_runtime_effect_confirmed=True,
    )


def build_kill_switch_rollback_contract_result(request: KillSwitchRollbackRequest) -> KillSwitchRollbackContractResult:
    """Build a closed, serializable future-only contract result."""
    decision = evaluate_kill_switch_rollback_request(request)
    return KillSwitchRollbackContractResult(
        request=request,
        decision=decision,
        contract_status=KILL_SWITCH_ROLLBACK_CONTRACT_STATUS,
        readiness=KILL_SWITCH_ROLLBACK_READINESS,
        next_step=KILL_SWITCH_ROLLBACK_NEXT_STEP,
        kill_switch_enabled=False,
        rollback_enabled=False,
        kill_switch_execution_enabled=False,
        rollback_execution_enabled=False,
        runtime_activation_enabled=False,
        runtime_execution_enabled=False,
        dry_run_execution_enabled=False,
        process_termination_enabled=False,
        job_cancellation_enabled=False,
        queue_drain_enabled=False,
        worker_stop_enabled=False,
        scheduler_stop_enabled=False,
        runner_stop_enabled=False,
        executor_stop_enabled=False,
        filesystem_rollback_enabled=False,
        git_rollback_enabled=False,
        store_mutation_enabled=False,
        manifest_mutation_enabled=False,
        database_rollback_enabled=False,
        memory_rollback_enabled=False,
        external_access_enabled=False,
    )


def serialize_kill_switch_rollback_contract_result(result: KillSwitchRollbackContractResult) -> dict[str, Any]:
    """Return a JSON-serializable dict for the future-only result."""
    if not isinstance(result, KillSwitchRollbackContractResult):
        raise TypeError("result debe ser KillSwitchRollbackContractResult")
    payload = {
        "request": _request_to_dict(result.request),
        "decision": _decision_to_dict(result.decision),
        "contract_status": result.contract_status,
        "readiness": result.readiness,
        "next_step": result.next_step,
        "kill_switch_enabled": result.kill_switch_enabled,
        "rollback_enabled": result.rollback_enabled,
        "kill_switch_execution_enabled": result.kill_switch_execution_enabled,
        "rollback_execution_enabled": result.rollback_execution_enabled,
        "runtime_activation_enabled": result.runtime_activation_enabled,
        "runtime_execution_enabled": result.runtime_execution_enabled,
        "dry_run_execution_enabled": result.dry_run_execution_enabled,
        "process_termination_enabled": result.process_termination_enabled,
        "job_cancellation_enabled": result.job_cancellation_enabled,
        "queue_drain_enabled": result.queue_drain_enabled,
        "worker_stop_enabled": result.worker_stop_enabled,
        "scheduler_stop_enabled": result.scheduler_stop_enabled,
        "runner_stop_enabled": result.runner_stop_enabled,
        "executor_stop_enabled": result.executor_stop_enabled,
        "filesystem_rollback_enabled": result.filesystem_rollback_enabled,
        "git_rollback_enabled": result.git_rollback_enabled,
        "store_mutation_enabled": result.store_mutation_enabled,
        "manifest_mutation_enabled": result.manifest_mutation_enabled,
        "database_rollback_enabled": result.database_rollback_enabled,
        "memory_rollback_enabled": result.memory_rollback_enabled,
        "external_access_enabled": result.external_access_enabled,
    }
    _ensure_json_serializable(payload)
    _validate_serialized_metadata(payload)
    return payload


def _request_to_dict(request: KillSwitchRollbackRequest) -> dict[str, Any]:
    return {
        "request_id": request.request_id,
        "requested_by": request.requested_by,
        "reason": request.reason,
        "action_type": request.action_type,
        "target_scope": list(request.target_scope),
        "target_ids": list(request.target_ids),
        "rollback_manifest_ref": request.rollback_manifest_ref,
        "metadata": _thaw_value(request.metadata),
    }


def _decision_to_dict(decision: KillSwitchRollbackDecision) -> dict[str, Any]:
    return {
        "request_id": decision.request_id,
        "decision_id": decision.decision_id,
        "allowed": decision.allowed,
        "action_type": decision.action_type,
        "conceptual_state": decision.conceptual_state,
        "blocked_reasons": list(decision.blocked_reasons),
        "warnings": list(decision.warnings),
        "security_baseline": list(decision.security_baseline),
        "audit_requirements": list(decision.audit_requirements),
        "no_activation_confirmed": decision.no_activation_confirmed,
        "no_runtime_effect_confirmed": decision.no_runtime_effect_confirmed,
    }


def _audit_requirements_for(request: KillSwitchRollbackRequest) -> tuple[str, ...]:
    requirements = list(BASE_AUDIT_REQUIREMENTS)
    if request.action_type == "rollback":
        requirements.append("rollback result futuro")
    requirements.append("approval reference futura")
    requirements.append("timestamp futuro controlado")
    return tuple(requirements)


def _require_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} obligatorio")


def _validate_non_empty_tuple(field_name: str, values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    resolved = tuple(values or ())
    if not resolved or any(not isinstance(item, str) or not item.strip() for item in resolved):
        raise ValueError(f"{field_name} obligatorio y no vacio")
    return tuple(item.strip() for item in resolved)


def _validate_and_freeze_metadata(metadata: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(metadata, Mapping):
        raise ValueError("metadata debe ser mapping serializable")
    copied = deepcopy(dict(metadata))
    _ensure_json_serializable(copied)
    _validate_metadata_keys(copied)
    return MappingProxyType(_freeze_value(copied))


def _validate_metadata_keys(value: Any, path: str = "metadata") -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key).lower()
            if key_text == "env" or any(fragment in key_text for fragment in SUSPICIOUS_METADATA_KEY_FRAGMENTS):
                raise ValueError(f"metadata_suspicious_key:{path}.{key}")
            if key_text in {"provider", "client", "runtime", "executor"} and _looks_active(nested):
                raise ValueError(f"metadata_active_runtime_reference:{path}.{key}")
            _validate_metadata_keys(nested, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _validate_metadata_keys(nested, f"{path}[{index}]")


def _looks_active(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in ("active", "enabled", "runtime", "executor", "client"))
    if isinstance(value, Mapping):
        return any(_looks_active(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_looks_active(item) for item in value)
    return False


def _ensure_json_serializable(value: Any) -> None:
    try:
        json.dumps(value, sort_keys=True)
    except TypeError as exc:
        raise ValueError(f"payload no serializable: {exc}") from exc


def _freeze_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _freeze_value(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_value(item) for item in value)
    return value


def _thaw_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw_value(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_thaw_value(item) for item in value]
    return value


def _validate_serialized_metadata(payload: Mapping[str, Any]) -> None:
    serialized = json.dumps(payload.get("request", {}).get("metadata", {}), sort_keys=True).lower()
    for forbidden in SUSPICIOUS_METADATA_KEY_FRAGMENTS:
        if forbidden in serialized:
            raise ValueError(f"serialized_payload_contains_forbidden_token:{forbidden}")
