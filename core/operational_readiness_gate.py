"""Contract-only operational readiness gate evaluation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


OPERATIONAL_READINESS_GATE_CONTRACT_STATUS = "contract_only"
OPERATIONAL_READINESS_GATE_ENABLED = False
OPERATIONAL_READINESS_GATE_RUNTIME_ENABLED = False
OPERATIONAL_READINESS_GATE_ATTEMPT_FACTORY_ENABLED = False
OPERATIONAL_READINESS_GATE_ATTEMPT_STORE_WRITES_ENABLED = False
OPERATIONAL_READINESS_GATE_LIFECYCLE_WRITES_ENABLED = False
OPERATIONAL_READINESS_GATE_RESULT_STORE_ENABLED = False
OPERATIONAL_READINESS_GATE_RESULT_STORE_WRITES_ENABLED = False
OPERATIONAL_READINESS_GATE_HISTORY_WRITES_ENABLED = False
OPERATIONAL_READINESS_GATE_READ_MODEL_WRITES_ENABLED = False
OPERATIONAL_READINESS_GATE_PROJECTION_WRITES_ENABLED = False
OPERATIONAL_READINESS_GATE_SCHEDULER_ENABLED = False
OPERATIONAL_READINESS_GATE_WORKER_ENABLED = False
OPERATIONAL_READINESS_GATE_QUEUE_ENABLED = False
OPERATIONAL_READINESS_GATE_MODEL_INVOCATION_ENABLED = False
OPERATIONAL_READINESS_GATE_TOOL_EXECUTION_ENABLED = False
OPERATIONAL_READINESS_GATE_MEMORY_PERSISTENCE_ENABLED = False
OPERATIONAL_READINESS_GATE_EXTERNAL_ACCESS_ENABLED = False
OPERATIONAL_READINESS_GATE_API_ENABLED = False
OPERATIONAL_READINESS_GATE_UI_ENABLED = False
MARKET_CATALOG_RUNTIME_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "not_ready"}
ALLOWED_DECISIONS = {"ready_for_next_contract", "blocked", "not_ready"}
ALLOWED_READINESS = {"ready_for_pre_operational_e2e_checkpoint", "blocked", "not_ready"}
REQUIRED_CONTRACTS = {
    "execution_intent",
    "execution_attempt_schema",
    "execution_attempt_state_machine",
    "execution_result_contract",
    "execution_result_projection",
    "long_suite_validation_policy",
}
REQUIRED_DISABLED_CAPABILITIES = {
    "runtime_execution",
    "attempt_factory",
    "attempt_store_writes",
    "lifecycle_writes",
    "result_store_writes",
    "history_writes",
    "read_model_writes",
    "projection_writes",
    "scheduler",
    "worker",
    "queue",
    "model_invocation",
    "tool_execution",
    "memory_persistence",
    "external_access",
}
FORBIDDEN_OPERATIONAL_VALUES = {"ready_for_runtime", "runtime_enabled", "operations_enabled", "gate_open"}
FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "runtime_execution",
    "attempt_factory_enabled",
    "attempt_factory",
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
    "business_composition_active",
    "business_composition_enabled",
    "gate_open",
    "operations_enabled",
}


@dataclass(frozen=True)
class OperationalReadinessGateDecision:
    gate_id: str
    status: str
    decision: str
    readiness: str
    checked_at: str
    contracts: dict[str, bool]
    disabled_capabilities: dict[str, bool]
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_step: str = "PROMPT 3.11 — Checkpoint E2E pre-operational"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["contracts"] = deepcopy(self.contracts)
        payload["disabled_capabilities"] = deepcopy(self.disabled_capabilities)
        payload["blocking_reasons"] = deepcopy(self.blocking_reasons)
        payload["warnings"] = deepcopy(self.warnings)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_operational_readiness_gate_decision(
    *,
    gate_id: str = "operational_readiness_gate_contract",
    status: str = "evaluated",
    decision: str = "ready_for_next_contract",
    readiness: str = "ready_for_pre_operational_e2e_checkpoint",
    checked_at: str | None = None,
    contracts: dict[str, bool] | None = None,
    disabled_capabilities: dict[str, bool] | None = None,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    next_step: str = "PROMPT 3.11 — Checkpoint E2E pre-operational",
    metadata: dict[str, Any] | None = None,
) -> OperationalReadinessGateDecision:
    return OperationalReadinessGateDecision(
        gate_id=gate_id,
        status=status,
        decision=decision,
        readiness=readiness,
        checked_at=checked_at or datetime.now().isoformat(),
        contracts=deepcopy(contracts or _ready_contracts()),
        disabled_capabilities=deepcopy(disabled_capabilities or _disabled_capabilities()),
        blocking_reasons=deepcopy(blocking_reasons or []),
        warnings=deepcopy(warnings or []),
        next_step=next_step,
        metadata=deepcopy(metadata or {}),
    )


def evaluate_operational_readiness_contracts() -> OperationalReadinessGateDecision:
    return build_operational_readiness_gate_decision(
        metadata={
            "contract_status": OPERATIONAL_READINESS_GATE_CONTRACT_STATUS,
            "system_ready_for_runtime": False,
            "system_ready_for_operational_gate_opening": False,
            "market_catalog_status": "planned_not_active",
            "business_composition_layer_status": "future_non_operational",
        }
    )


def validate_operational_readiness_gate_decision(decision: OperationalReadinessGateDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_operational_readiness_gate_decision(decision)
    blockers: list[dict[str, str]] = []
    contracts = payload.get("contracts")
    disabled = payload.get("disabled_capabilities")

    _require(payload.get("gate_id"), blockers, "missing_gate_id", "gate_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision no permitida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")
    _require(payload.get("checked_at"), blockers, "missing_checked_at", "checked_at requerido")
    if not isinstance(contracts, dict):
        _block(blockers, "invalid_contracts", "contracts debe ser dict")
        contracts = {}
    if not isinstance(disabled, dict):
        _block(blockers, "invalid_disabled_capabilities", "disabled_capabilities debe ser dict")
        disabled = {}
    if not isinstance(payload.get("blocking_reasons"), list):
        _block(blockers, "invalid_blocking_reasons", "blocking_reasons debe ser list")
    if not isinstance(payload.get("warnings"), list):
        _block(blockers, "invalid_warnings", "warnings debe ser list")
    if not isinstance(payload.get("metadata"), dict):
        _block(blockers, "invalid_metadata", "metadata debe ser dict")

    _validate_required_contracts(contracts, blockers)
    _validate_disabled_capabilities(disabled, blockers)
    _scan_forbidden_values(payload, blockers)
    _validate_boundaries(blockers)

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "OPERATIONAL_READINESS_GATE_CONTRACT_READY" if not blockers else "OPERATIONAL_READINESS_GATE_CONTRACT_BLOCKED",
        "readiness": "ready_for_pre_operational_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [],
        "decision": payload,
        "gate_contract_status": OPERATIONAL_READINESS_GATE_CONTRACT_STATUS,
        "gate_enabled": OPERATIONAL_READINESS_GATE_ENABLED,
        "runtime_enabled": OPERATIONAL_READINESS_GATE_RUNTIME_ENABLED,
        "attempt_factory_enabled": OPERATIONAL_READINESS_GATE_ATTEMPT_FACTORY_ENABLED,
        "store_writes_enabled": OPERATIONAL_READINESS_GATE_ATTEMPT_STORE_WRITES_ENABLED,
        "lifecycle_writes_enabled": OPERATIONAL_READINESS_GATE_LIFECYCLE_WRITES_ENABLED,
        "result_store_enabled": OPERATIONAL_READINESS_GATE_RESULT_STORE_ENABLED,
        "history_writes_enabled": OPERATIONAL_READINESS_GATE_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": OPERATIONAL_READINESS_GATE_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": OPERATIONAL_READINESS_GATE_PROJECTION_WRITES_ENABLED,
    }


def serialize_operational_readiness_gate_decision(decision: OperationalReadinessGateDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, OperationalReadinessGateDecision):
        return decision.to_dict()
    return deepcopy(decision)


def get_operational_readiness_gate_contract() -> dict[str, Any]:
    return {
        "status": OPERATIONAL_READINESS_GATE_CONTRACT_STATUS,
        "verdict": "OPERATIONAL_READINESS_GATE_CONTRACT_READY",
        "readiness": "ready_for_pre_operational_e2e_checkpoint",
        "next_step": "PROMPT 3.11 — Checkpoint E2E pre-operational",
        "allowed_statuses": sorted(ALLOWED_STATUSES),
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "allowed_readiness": sorted(ALLOWED_READINESS),
        "required_contracts": sorted(REQUIRED_CONTRACTS),
        "required_disabled_capabilities": sorted(REQUIRED_DISABLED_CAPABILITIES),
        "boundaries": _boundary_flags(),
    }


def _ready_contracts() -> dict[str, bool]:
    return {name: True for name in REQUIRED_CONTRACTS}


def _disabled_capabilities() -> dict[str, bool]:
    return {name: True for name in REQUIRED_DISABLED_CAPABILITIES}


def _validate_required_contracts(contracts: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for name in REQUIRED_CONTRACTS:
        if contracts.get(name) is not True:
            _block(blockers, f"{name}_not_ready", f"{name} debe estar listo")


def _validate_disabled_capabilities(disabled: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for name in REQUIRED_DISABLED_CAPABILITIES:
        if disabled.get(name) is not True:
            _block(blockers, f"{name}_not_disabled", f"{name} debe permanecer deshabilitada")


def _scan_forbidden_values(value: Any, blockers: list[dict[str, str]], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "disabled_capabilities":
                continue
            if key in FORBIDDEN_TRUE_FLAGS and item is True:
                _block(blockers, f"{key}_not_allowed", f"{key}=true no permitido")
            if key in {"market_catalog_status", "market_catalog"} and item == "active":
                _block(blockers, "market_catalog_active_not_allowed", "Market Catalog activo no permitido")
            if key in {"business_composition_layer_status", "business_composition_layer"} and item in {"active", "operational"}:
                _block(blockers, "business_composition_active_not_allowed", "Business Composition Layer activa no permitida")
            _scan_forbidden_values(item, blockers, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_forbidden_values(item, blockers, f"{path}[{index}]")
    elif isinstance(value, str) and value in FORBIDDEN_OPERATIONAL_VALUES:
        _block(blockers, f"{value}_not_allowed", f"{value} no permitido")


def _validate_boundaries(blockers: list[dict[str, str]]) -> None:
    for name, value in _boundary_flags().items():
        if value is not False:
            _block(blockers, f"{name}_not_allowed", f"{name} debe ser false")


def _boundary_flags() -> dict[str, bool]:
    return {
        "operational_readiness_gate_enabled": OPERATIONAL_READINESS_GATE_ENABLED,
        "runtime_enabled": OPERATIONAL_READINESS_GATE_RUNTIME_ENABLED,
        "attempt_factory_enabled": OPERATIONAL_READINESS_GATE_ATTEMPT_FACTORY_ENABLED,
        "attempt_store_writes_enabled": OPERATIONAL_READINESS_GATE_ATTEMPT_STORE_WRITES_ENABLED,
        "lifecycle_writes_enabled": OPERATIONAL_READINESS_GATE_LIFECYCLE_WRITES_ENABLED,
        "result_store_enabled": OPERATIONAL_READINESS_GATE_RESULT_STORE_ENABLED,
        "result_store_writes_enabled": OPERATIONAL_READINESS_GATE_RESULT_STORE_WRITES_ENABLED,
        "history_writes_enabled": OPERATIONAL_READINESS_GATE_HISTORY_WRITES_ENABLED,
        "read_model_writes_enabled": OPERATIONAL_READINESS_GATE_READ_MODEL_WRITES_ENABLED,
        "projection_writes_enabled": OPERATIONAL_READINESS_GATE_PROJECTION_WRITES_ENABLED,
        "scheduler_enabled": OPERATIONAL_READINESS_GATE_SCHEDULER_ENABLED,
        "worker_enabled": OPERATIONAL_READINESS_GATE_WORKER_ENABLED,
        "queue_enabled": OPERATIONAL_READINESS_GATE_QUEUE_ENABLED,
        "model_invocation_enabled": OPERATIONAL_READINESS_GATE_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": OPERATIONAL_READINESS_GATE_TOOL_EXECUTION_ENABLED,
        "memory_persistence_enabled": OPERATIONAL_READINESS_GATE_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": OPERATIONAL_READINESS_GATE_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": OPERATIONAL_READINESS_GATE_API_ENABLED,
        "ui_enabled": OPERATIONAL_READINESS_GATE_UI_ENABLED,
        "market_catalog_runtime_enabled": MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_layer_runtime_enabled": BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED,
    }


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
