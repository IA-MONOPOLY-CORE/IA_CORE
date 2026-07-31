"""Contract-only dry-run execution primitives.

This module models dry-run requests, decisions, and serializable contract
results. It never executes tools, invokes models, mutates stores, reads env or
secrets, touches the filesystem, opens network/browser access, or changes
runtime state.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any, Mapping


DRY_RUN_EXECUTION_CONTRACT_READY = True
DRY_RUN_EXECUTION_OPERATIONAL = False
DRY_RUN_EXECUTION_ENABLED = False
DRY_RUN_EXECUTOR_ENABLED = False
DRY_RUN_RUNNER_ENABLED = False
DRY_RUN_DISPATCHER_ENABLED = False
DRY_RUN_SCHEDULER_ENABLED = False
DRY_RUN_WORKER_ENABLED = False
DRY_RUN_QUEUE_ENABLED = False

DRY_RUN_TOOL_EXECUTION_ENABLED = False
DRY_RUN_MODEL_INVOCATION_ENABLED = False
DRY_RUN_CONTEXT_INJECTION_ENABLED = False
DRY_RUN_OUTPUT_DELIVERY_ENABLED = False
DRY_RUN_OUTPUT_PUBLISHING_ENABLED = False
DRY_RUN_WRITES_ENABLED = False
DRY_RUN_STORES_ENABLED = False
DRY_RUN_MEMORY_PERSISTENCE_ENABLED = False
DRY_RUN_NETWORK_ENABLED = False
DRY_RUN_API_ENABLED = False
DRY_RUN_BROWSER_ENABLED = False
DRY_RUN_FILESYSTEM_ENABLED = False
DRY_RUN_ENV_ACCESS_ENABLED = False
DRY_RUN_SECRET_ACCESS_ENABLED = False

DRY_RUN_UI_TARS_ENABLED = False
DRY_RUN_HERMES_ENABLED = False
DRY_RUN_N8N_ENABLED = False
DRY_RUN_HOME_ASSISTANT_ENABLED = False

DRY_RUN_ALLOWED_CONCEPTUAL_STATES = (
    "dry_run_draft",
    "dry_run_planned",
    "dry_run_preflight_validated",
    "dry_run_policy_checked",
    "dry_run_blocked",
    "dry_run_simulated",
    "dry_run_result_projected",
    "dry_run_cancelled",
    "dry_run_invalid",
)

DRY_RUN_FORBIDDEN_OPERATIONAL_STATES = (
    "queued",
    "running",
    "succeeded",
    "failed",
    "runtime_open",
    "runtime_active",
    "execution_enabled",
    "dry_run_execution_enabled",
    "operations_enabled",
    "gate_open",
)

DRY_RUN_CONTRACT_STATUS = "DRY_RUN_EXECUTION_CONTRACT_READY"
DRY_RUN_CONTRACT_READINESS = "ready_for_dry_run_execution_contract_e2e"
DRY_RUN_CONTRACT_NEXT_STEP = "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract"

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
)

SUSPICIOUS_METADATA_KEYS = (
    "secret",
    "token",
    "api_key",
    "password",
    "credential",
    "env",
    "private_key",
    "raw_output",
    "tool_payload",
    "model_prompt",
    "context_payload",
    "output_payload",
    "filesystem_path",
    "external_url",
    "provider_client",
    "runtime_executor",
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
    "external_url",
    "provider_client",
    "runtime_executor",
)


@dataclass(frozen=True)
class DryRunExecutionRequest:
    request_id: str
    intent_id: str
    attempt_id: str | None
    requested_by: str
    reason: str
    simulation_scope: tuple[str, ...]
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class DryRunExecutionDecision:
    request_id: str
    decision_id: str
    allowed: bool
    conceptual_state: str
    blocked_reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    security_baseline: tuple[str, ...]
    no_activation_confirmed: bool


@dataclass(frozen=True)
class DryRunExecutionContractResult:
    request: DryRunExecutionRequest
    decision: DryRunExecutionDecision
    contract_status: str
    readiness: str
    next_step: str
    runtime_activation_enabled: bool
    runtime_execution_enabled: bool
    dry_run_execution_enabled: bool
    tool_execution_enabled: bool
    model_invocation_enabled: bool
    context_injection_enabled: bool
    output_delivery_enabled: bool
    writes_enabled: bool
    stores_enabled: bool
    external_access_enabled: bool


def create_dry_run_execution_request(
    *,
    request_id: str,
    intent_id: str,
    requested_by: str,
    reason: str,
    simulation_scope: tuple[str, ...] | list[str],
    attempt_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DryRunExecutionRequest:
    """Create a validated dry-run request. No execution or I/O occurs."""
    _require_non_empty("request_id", request_id)
    _require_non_empty("intent_id", intent_id)
    _require_non_empty("requested_by", requested_by)
    _require_non_empty("reason", reason)
    scope = tuple(simulation_scope or ())
    if not scope or any(not isinstance(item, str) or not item.strip() for item in scope):
        raise ValueError("simulation_scope obligatorio y no vacio")
    clean_metadata = _validate_and_freeze_metadata(metadata or {})
    return DryRunExecutionRequest(
        request_id=request_id.strip(),
        intent_id=intent_id.strip(),
        attempt_id=attempt_id.strip() if isinstance(attempt_id, str) and attempt_id.strip() else None,
        requested_by=requested_by.strip(),
        reason=reason.strip(),
        simulation_scope=tuple(item.strip() for item in scope),
        metadata=clean_metadata,
    )


def evaluate_dry_run_execution_request(
    request: DryRunExecutionRequest,
    *,
    conceptual_state: str = "dry_run_policy_checked",
) -> DryRunExecutionDecision:
    """Evaluate representability of a dry-run request without enabling it."""
    if not isinstance(request, DryRunExecutionRequest):
        raise TypeError("request debe ser DryRunExecutionRequest")
    blocked_reasons: list[str] = []
    warnings = ["allowed_true_is_representability_only"]
    if conceptual_state in DRY_RUN_FORBIDDEN_OPERATIONAL_STATES:
        blocked_reasons.append(f"operational_state_forbidden:{conceptual_state}")
        resolved_state = "dry_run_blocked"
    elif conceptual_state not in DRY_RUN_ALLOWED_CONCEPTUAL_STATES:
        blocked_reasons.append(f"conceptual_state_not_allowed:{conceptual_state}")
        resolved_state = "dry_run_invalid"
    else:
        resolved_state = conceptual_state
    try:
        _validate_and_freeze_metadata(request.metadata)
    except ValueError as exc:
        blocked_reasons.append(str(exc))
        resolved_state = "dry_run_blocked"
    allowed = not blocked_reasons
    return DryRunExecutionDecision(
        request_id=request.request_id,
        decision_id=f"dry_run_decision_{request.request_id}",
        allowed=allowed,
        conceptual_state=resolved_state,
        blocked_reasons=tuple(blocked_reasons),
        warnings=tuple(warnings),
        security_baseline=SECURITY_BASELINE,
        no_activation_confirmed=True,
    )


def build_dry_run_execution_contract_result(request: DryRunExecutionRequest) -> DryRunExecutionContractResult:
    """Build the non-operational contract result for a dry-run request."""
    decision = evaluate_dry_run_execution_request(request)
    return DryRunExecutionContractResult(
        request=request,
        decision=decision,
        contract_status=DRY_RUN_CONTRACT_STATUS,
        readiness=DRY_RUN_CONTRACT_READINESS,
        next_step=DRY_RUN_CONTRACT_NEXT_STEP,
        runtime_activation_enabled=False,
        runtime_execution_enabled=False,
        dry_run_execution_enabled=False,
        tool_execution_enabled=False,
        model_invocation_enabled=False,
        context_injection_enabled=False,
        output_delivery_enabled=False,
        writes_enabled=False,
        stores_enabled=False,
        external_access_enabled=False,
    )


def serialize_dry_run_execution_contract_result(result: DryRunExecutionContractResult) -> dict[str, Any]:
    """Return a JSON-serializable dict for the contract result."""
    if not isinstance(result, DryRunExecutionContractResult):
        raise TypeError("result debe ser DryRunExecutionContractResult")
    payload = {
        "request": _request_to_dict(result.request),
        "decision": _decision_to_dict(result.decision),
        "contract_status": result.contract_status,
        "readiness": result.readiness,
        "next_step": result.next_step,
        "runtime_activation_enabled": result.runtime_activation_enabled,
        "runtime_execution_enabled": result.runtime_execution_enabled,
        "dry_run_execution_enabled": result.dry_run_execution_enabled,
        "tool_execution_enabled": result.tool_execution_enabled,
        "model_invocation_enabled": result.model_invocation_enabled,
        "context_injection_enabled": result.context_injection_enabled,
        "output_delivery_enabled": result.output_delivery_enabled,
        "writes_enabled": result.writes_enabled,
        "stores_enabled": result.stores_enabled,
        "external_access_enabled": result.external_access_enabled,
    }
    _ensure_json_serializable(payload)
    _validate_serialized_payload(payload)
    return payload


def _request_to_dict(request: DryRunExecutionRequest) -> dict[str, Any]:
    return {
        "request_id": request.request_id,
        "intent_id": request.intent_id,
        "attempt_id": request.attempt_id,
        "requested_by": request.requested_by,
        "reason": request.reason,
        "simulation_scope": list(request.simulation_scope),
        "metadata": _thaw_value(request.metadata),
    }


def _decision_to_dict(decision: DryRunExecutionDecision) -> dict[str, Any]:
    return {
        "request_id": decision.request_id,
        "decision_id": decision.decision_id,
        "allowed": decision.allowed,
        "conceptual_state": decision.conceptual_state,
        "blocked_reasons": list(decision.blocked_reasons),
        "warnings": list(decision.warnings),
        "security_baseline": list(decision.security_baseline),
        "no_activation_confirmed": decision.no_activation_confirmed,
    }


def _require_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} obligatorio")


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


def _validate_serialized_payload(payload: Mapping[str, Any]) -> None:
    serialized = json.dumps(payload.get("request", {}).get("metadata", {}), sort_keys=True).lower()
    for forbidden in SUSPICIOUS_METADATA_KEYS:
        if forbidden in serialized:
            raise ValueError(f"serialized_payload_contains_forbidden_token:{forbidden}")
