"""Contract-only schema and validation for operational execution intents."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


EXECUTION_INTENT_CONTRACT_STATUS = "contract_only"
EXECUTION_INTENT_RUNTIME_ENABLED = False
EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED = False
EXECUTION_INTENT_EXECUTION_ENABLED = False
EXECUTION_INTENT_SCHEDULER_ENABLED = False
EXECUTION_INTENT_WORKER_ENABLED = False
EXECUTION_INTENT_MODEL_INVOCATION_ENABLED = False
EXECUTION_INTENT_TOOL_EXECUTION_ENABLED = False
EXECUTION_INTENT_MEMORY_PERSISTENCE_ENABLED = False
EXECUTION_INTENT_EXTERNAL_ACCESS_ENABLED = False
EXECUTION_INTENT_API_ENABLED = False
EXECUTION_INTENT_UI_ENABLED = False
EXECUTION_INTENT_QUEUE_ENABLED = False
BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED = False

ALLOWED_INTENT_TYPES = {
    "domain_operation",
    "agent_operation",
    "team_operation",
    "market_catalog_review",
    "business_composition_review",
}
ALLOWED_TARGET_TYPES = {
    "domain",
    "agent",
    "team",
    "market",
    "business_composition_candidate",
}
ALLOWED_MODES = {
    "audit_only",
    "contract_validation",
    "dry_run_requested",
    "preflight_requested",
}
ALLOWED_STATUSES = {
    "draft",
    "validated",
    "rejected",
    "blocked",
}
ALLOWED_READINESS = {
    "not_ready",
    "ready_for_preflight_design",
    "ready_for_attempt_design",
    "blocked",
}
OPERATIONAL_CONSTRAINTS = {
    "allow_runtime_execution": "runtime_execution_not_allowed",
    "allow_attempt_creation": "attempt_creation_not_allowed",
    "allow_scheduler": "scheduler_not_allowed",
    "allow_worker": "worker_not_allowed",
    "allow_model_invocation": "model_invocation_not_allowed",
    "allow_tool_execution": "tool_execution_not_allowed",
    "allow_memory_persistence": "memory_persistence_not_allowed",
    "allow_external_access": "external_access_not_allowed",
}
FORBIDDEN_RUNTIME_PATHS = {
    "core/execution_attempt_id.py",
    "core/execution_result_store.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
}


@dataclass(frozen=True)
class ExecutionIntentTarget:
    target_type: str
    target_id: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionIntentConstraints:
    allow_runtime_execution: bool = False
    allow_attempt_creation: bool = False
    allow_scheduler: bool = False
    allow_worker: bool = False
    allow_model_invocation: bool = False
    allow_tool_execution: bool = False
    allow_memory_persistence: bool = False
    allow_external_access: bool = False

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionIntent:
    intent_id: str
    intent_type: str
    source: str
    target: ExecutionIntentTarget
    mode: str
    requested_by: str
    readiness: str
    status: str
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)
    constraints: ExecutionIntentConstraints = field(default_factory=ExecutionIntentConstraints)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["target"] = self.target.to_dict()
        payload["constraints"] = self.constraints.to_dict()
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def build_execution_intent(
    *,
    intent_id: str,
    intent_type: str,
    source: str,
    target_type: str,
    target_id: str,
    mode: str,
    requested_by: str,
    readiness: str = "not_ready",
    status: str = "draft",
    created_at: str | None = None,
    metadata: dict[str, Any] | None = None,
    constraints: dict[str, bool] | None = None,
) -> ExecutionIntent:
    return ExecutionIntent(
        intent_id=intent_id,
        intent_type=intent_type,
        source=source,
        target=ExecutionIntentTarget(target_type=target_type, target_id=target_id),
        mode=mode,
        requested_by=requested_by,
        readiness=readiness,
        status=status,
        created_at=created_at or datetime.now().isoformat(),
        metadata=deepcopy(metadata or {}),
        constraints=ExecutionIntentConstraints(**(constraints or {})),
    )


def serialize_execution_intent(intent: ExecutionIntent | dict[str, Any]) -> dict[str, Any]:
    if isinstance(intent, ExecutionIntent):
        return intent.to_dict()
    return deepcopy(intent)


def validate_execution_intent(intent: ExecutionIntent | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_execution_intent(intent)
    blockers: list[dict[str, str]] = []
    target = payload.get("target") or {}
    constraints = payload.get("constraints") or {}

    _require(payload.get("intent_id"), blockers, "missing_intent_id", "intent_id requerido")
    _allowed(payload.get("intent_type"), ALLOWED_INTENT_TYPES, blockers, "invalid_intent_type", "intent_type no permitido")
    _allowed(target.get("target_type"), ALLOWED_TARGET_TYPES, blockers, "invalid_target_type", "target_type no permitido")
    _require(target.get("target_id"), blockers, "missing_target_id", "target_id requerido")
    _allowed(payload.get("mode"), ALLOWED_MODES, blockers, "invalid_mode", "mode no permitido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")

    for field_name, code in OPERATIONAL_CONSTRAINTS.items():
        if constraints.get(field_name) is not False:
            _block(blockers, code, f"{field_name}=true no permitido en execution intent contract-only")

    if target.get("target_type") == "market":
        if payload.get("metadata", {}).get("market_catalog_status") != "planned_not_active":
            _block(blockers, "market_catalog_not_planned", "Market Catalog debe permanecer planned_not_active")
        if payload.get("metadata", {}).get("market_catalog_runtime_enabled") not in (None, False):
            _block(blockers, "market_catalog_runtime_not_allowed", "Market Catalog runtime no permitido")

    if target.get("target_type") == "business_composition_candidate":
        if payload.get("metadata", {}).get("business_composition_layer_operational") not in (None, False):
            _block(blockers, "business_composition_layer_not_allowed", "Business Composition Layer no operativa")
        if BUSINESS_COMPOSITION_LAYER_RUNTIME_ENABLED is not False:
            _block(blockers, "business_composition_layer_runtime_not_allowed", "Business Composition Layer runtime no permitido")

    for relative_path in FORBIDDEN_RUNTIME_PATHS:
        if Path(relative_path).exists():
            _block(blockers, "runtime_path_not_allowed", f"{relative_path} no debe existir en contrato de intent")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "EXECUTION_INTENT_CONTRACT_READY" if not blockers else "EXECUTION_INTENT_CONTRACT_BLOCKED",
        "readiness": "ready_for_execution_attempt_id_audit" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [],
        "intent": payload,
        "contract_status": EXECUTION_INTENT_CONTRACT_STATUS,
        "runtime_enabled": EXECUTION_INTENT_RUNTIME_ENABLED,
        "attempt_creation_enabled": EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED,
        "execution_enabled": EXECUTION_INTENT_EXECUTION_ENABLED,
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
