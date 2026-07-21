"""Schema de execution_attempt_store_contract preflight-only, sin store real."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


EXECUTION_ATTEMPT_STORE_CONTRACT_SCHEMA_VERSION = "1.0"
EXECUTION_ATTEMPT_STORE_CONTRACT_TYPE = "execution_attempt_store_contract"
ALLOWED_MODES = {"execution_attempt_store_contract_only"}
ALLOWED_ATTEMPT_MODES = {"preflight_only"}
ALLOWED_STORE_TYPES = {"execution_attempt_store"}
ALLOWED_STORAGE_FORMATS = {"append_only_jsonl_future"}
ALLOWED_CONTRACT_STATUSES = {"passed", "blocked", "failed"}
ALLOWED_VERDICTS = {
    "EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_BLOCKED",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_FAILED",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_ATTEMPT_ID_LEAK",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_LIFECYCLE_LEAK",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_PAYLOAD_LEAK",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_EXECUTION_BOUNDARY",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_EXTERNAL_BOUNDARY",
    "EXECUTION_ATTEMPT_STORE_CONTRACT_MUTATION_BOUNDARY",
}
REQUIRED_FIELDS = {
    "schema_version",
    "contract_id",
    "contract_type",
    "version",
    "status",
    "verdict",
    "mode",
    "attempt_mode",
    "store_type",
    "storage_format",
    "target_ref",
    "dry_run_ref",
    "dry_run_store_ref",
    "dry_run_store_verification_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "dry_run_store_contract_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "correlation_id",
    "idempotency_key",
    "attempt_id_policy",
    "preflight_policy",
    "lifecycle_policy",
    "payload_boundary_policy",
    "append_only_policy",
    "checksum_policy",
    "reference_policy",
    "readiness_policy",
    "reference_summary",
    "preflight_summary",
    "lifecycle_summary",
    "attempt_id_summary",
    "payload_boundary_summary",
    "append_only_summary",
    "checksum_summary",
    "audit_summary",
    "observability_summary",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
    "warnings",
    "blockers",
    "evidence",
    "created_at",
}
OBJECT_FIELDS = {
    "target_ref",
    "dry_run_ref",
    "dry_run_store_ref",
    "dry_run_store_verification_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "dry_run_store_contract_ref",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "attempt_id_policy",
    "preflight_policy",
    "lifecycle_policy",
    "payload_boundary_policy",
    "append_only_policy",
    "checksum_policy",
    "reference_policy",
    "readiness_policy",
    "reference_summary",
    "preflight_summary",
    "lifecycle_summary",
    "attempt_id_summary",
    "payload_boundary_summary",
    "append_only_summary",
    "checksum_summary",
    "audit_summary",
    "observability_summary",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
}


@dataclass(frozen=True)
class ExecutionAttemptStoreReferencePolicy:
    required_refs: list[str]
    cross_target_refs_blocked: bool = True
    cross_correlation_refs_blocked: bool = True
    cross_idempotency_refs_blocked: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptPreflightPolicy:
    allowed_states: list[str]
    blocked_states: list[str]
    execution_enabled: bool = False
    agent_execution_enabled: bool = False
    team_execution_enabled: bool = False
    model_invocation_enabled: bool = False
    tool_execution_enabled: bool = False
    memory_persistence_enabled: bool = False
    external_access_enabled: bool = False
    scheduler_enabled: bool = False
    worker_queue_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptLifecyclePolicy:
    current_scope: str
    allowed_states: list[str]
    blocked_states: list[str]
    real_lifecycle_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptPayloadBoundaryPolicy:
    forbidden_fields: list[str]
    deep_scan_required: bool = True
    real_payloads_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptIdPolicy:
    attempt_ref: str = "future_preflight_attempt_ref"
    attempt_id_generation: str = "disabled"
    attempt_id_persistence: str = "disabled"
    attempt_id_must_not_be_materialized: bool = True
    execution_attempt_id_operational_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptStoreReadiness:
    ready_for_contract_only: bool
    ready_for_implementation: bool = False
    ready_for_execution_lifecycle: bool = False
    ready_for_real_execution: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptStoreContract:
    contract_id: str
    mode: str
    attempt_mode: str
    store_type: str
    storage_format: str
    target_ref: dict[str, Any]
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    dry_run_store_verification_ref: dict[str, Any]
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_executor_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    dry_run_store_contract_ref: dict[str, Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]
    correlation_id: str
    idempotency_key: str
    attempt_id_policy: dict[str, Any]
    preflight_policy: dict[str, Any]
    lifecycle_policy: dict[str, Any]
    payload_boundary_policy: dict[str, Any]
    append_only_policy: dict[str, Any]
    checksum_policy: dict[str, Any]
    reference_policy: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptStoreContractResult:
    status: str
    verdict: str
    mode: str
    attempt_mode: str
    store_type: str
    storage_format: str
    target_ref: dict[str, Any]
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    reference_summary: dict[str, Any]
    preflight_summary: dict[str, Any]
    lifecycle_summary: dict[str, Any]
    attempt_id_summary: dict[str, Any]
    payload_boundary_summary: dict[str, Any]
    append_only_summary: dict[str, Any]
    checksum_summary: dict[str, Any]
    audit_summary: dict[str, Any]
    observability_summary: dict[str, Any]
    boundary_summary: dict[str, Any]
    readiness_summary: dict[str, Any]
    blockers: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_execution_attempt_store_contract_report(
    *,
    contract_id: str,
    status: str,
    verdict: str,
    mode: str,
    attempt_mode: str,
    store_type: str,
    storage_format: str,
    target_ref: dict[str, Any] | None,
    dry_run_ref: dict[str, Any] | None,
    dry_run_store_ref: dict[str, Any] | None,
    dry_run_store_verification_ref: dict[str, Any] | None,
    runtime_contract_ref: dict[str, Any] | None,
    execution_contract_ref: dict[str, Any] | None,
    runtime_executor_contract_ref: dict[str, Any] | None,
    runtime_preparation_ref: dict[str, Any] | None,
    execution_runner_contract_ref: dict[str, Any] | None,
    dry_run_contract_ref: dict[str, Any] | None,
    dry_run_store_contract_ref: dict[str, Any] | None,
    audit_refs: dict[str, Any] | None,
    observability_refs: dict[str, Any] | None,
    capability_policy_ref: dict[str, Any] | None,
    correlation_id: str | None,
    idempotency_key: str | None,
    attempt_id_policy: dict[str, Any] | None,
    preflight_policy: dict[str, Any] | None,
    lifecycle_policy: dict[str, Any] | None,
    payload_boundary_policy: dict[str, Any] | None,
    append_only_policy: dict[str, Any] | None,
    checksum_policy: dict[str, Any] | None,
    reference_policy: dict[str, Any] | None,
    readiness_policy: dict[str, Any] | None,
    reference_summary: dict[str, Any] | None,
    preflight_summary: dict[str, Any] | None,
    lifecycle_summary: dict[str, Any] | None,
    attempt_id_summary: dict[str, Any] | None,
    payload_boundary_summary: dict[str, Any] | None,
    append_only_summary: dict[str, Any] | None,
    checksum_summary: dict[str, Any] | None,
    audit_summary: dict[str, Any] | None,
    observability_summary: dict[str, Any] | None,
    boundary_summary: dict[str, Any] | None,
    readiness_summary: dict[str, Any] | None,
    risk_summary: dict[str, Any] | None,
    blockers: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": EXECUTION_ATTEMPT_STORE_CONTRACT_SCHEMA_VERSION,
        "contract_id": contract_id,
        "contract_type": EXECUTION_ATTEMPT_STORE_CONTRACT_TYPE,
        "version": "1.0",
        "status": status,
        "verdict": verdict,
        "mode": mode,
        "attempt_mode": attempt_mode,
        "store_type": store_type,
        "storage_format": storage_format,
        "target_ref": dict(target_ref or {}),
        "dry_run_ref": dict(dry_run_ref or {}),
        "dry_run_store_ref": dict(dry_run_store_ref or {}),
        "dry_run_store_verification_ref": dict(dry_run_store_verification_ref or {}),
        "runtime_contract_ref": dict(runtime_contract_ref or {}),
        "execution_contract_ref": dict(execution_contract_ref or {}),
        "runtime_executor_contract_ref": dict(runtime_executor_contract_ref or {}),
        "runtime_preparation_ref": dict(runtime_preparation_ref or {}),
        "execution_runner_contract_ref": dict(execution_runner_contract_ref or {}),
        "dry_run_contract_ref": dict(dry_run_contract_ref or {}),
        "dry_run_store_contract_ref": dict(dry_run_store_contract_ref or {}),
        "audit_refs": dict(audit_refs or {}),
        "observability_refs": dict(observability_refs or {}),
        "capability_policy_ref": dict(capability_policy_ref or {}),
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "attempt_id_policy": dict(attempt_id_policy or {}),
        "preflight_policy": dict(preflight_policy or {}),
        "lifecycle_policy": dict(lifecycle_policy or {}),
        "payload_boundary_policy": dict(payload_boundary_policy or {}),
        "append_only_policy": dict(append_only_policy or {}),
        "checksum_policy": dict(checksum_policy or {}),
        "reference_policy": dict(reference_policy or {}),
        "readiness_policy": dict(readiness_policy or {}),
        "reference_summary": dict(reference_summary or {}),
        "preflight_summary": dict(preflight_summary or {}),
        "lifecycle_summary": dict(lifecycle_summary or {}),
        "attempt_id_summary": dict(attempt_id_summary or {}),
        "payload_boundary_summary": dict(payload_boundary_summary or {}),
        "append_only_summary": dict(append_only_summary or {}),
        "checksum_summary": dict(checksum_summary or {}),
        "audit_summary": dict(audit_summary or {}),
        "observability_summary": dict(observability_summary or {}),
        "boundary_summary": dict(boundary_summary or {}),
        "readiness_summary": dict(readiness_summary or {}),
        "risk_summary": dict(risk_summary or {}),
        "warnings": list(warnings or []),
        "blockers": list(blockers or []),
        "evidence": list(evidence or []),
        "created_at": created_at or datetime.now().isoformat(),
    }
    return validate_execution_attempt_store_contract_report(payload)


def validate_execution_attempt_store_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("execution_attempt_store_contract debe ser objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"execution_attempt_store_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != EXECUTION_ATTEMPT_STORE_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de execution_attempt_store_contract invalida")
    if report.get("contract_type") != EXECUTION_ATTEMPT_STORE_CONTRACT_TYPE:
        raise ValueError("contract_type de execution_attempt_store_contract invalido")
    _validate_id(report.get("contract_id"), "contract_id")
    if report.get("mode") not in ALLOWED_MODES:
        raise ValueError(f"mode invalido: {report.get('mode')}")
    if report.get("attempt_mode") not in ALLOWED_ATTEMPT_MODES:
        raise ValueError(f"attempt_mode invalido: {report.get('attempt_mode')}")
    if report.get("store_type") not in ALLOWED_STORE_TYPES:
        raise ValueError(f"store_type invalido: {report.get('store_type')}")
    if report.get("storage_format") not in ALLOWED_STORAGE_FORMATS:
        raise ValueError(f"storage_format invalido: {report.get('storage_format')}")
    if report.get("status") not in ALLOWED_CONTRACT_STATUSES:
        raise ValueError(f"status invalido: {report.get('status')}")
    if report.get("verdict") not in ALLOWED_VERDICTS:
        raise ValueError(f"verdict invalido: {report.get('verdict')}")
    for field in ["version", "created_at"]:
        _validate_non_empty_text(report.get(field), field)
    if report.get("correlation_id") is not None:
        _validate_id(report["correlation_id"], "correlation_id")
    if report.get("idempotency_key") is not None:
        _validate_id(report["idempotency_key"], "idempotency_key")
    for field in OBJECT_FIELDS:
        if not isinstance(report.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    for field in ["warnings", "evidence"]:
        if not isinstance(report.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    _validate_blockers(report.get("blockers"))
    _ensure_json_serializable(report)
    return deepcopy(report)


def _validate_blockers(blockers: Any) -> None:
    if not isinstance(blockers, list):
        raise ValueError("blockers debe ser lista")
    for blocker in blockers:
        if not isinstance(blocker, dict):
            raise ValueError("cada blocker debe ser objeto")
        for field in ["code", "message", "severity"]:
            _validate_non_empty_text(blocker.get(field), f"blocker.{field}")
        _validate_id(blocker["code"], "blocker.code")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError(f"{field} invalido: debe estar en snake_case")


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _ensure_json_serializable(payload: dict[str, Any]) -> None:
    try:
        json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("execution_attempt_store_contract debe ser serializable como JSON") from exc

