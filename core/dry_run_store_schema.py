"""Schema de dry_run_store_contract append-only, sin implementacion de store."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


DRY_RUN_STORE_CONTRACT_SCHEMA_VERSION = "1.0"
DRY_RUN_STORE_CONTRACT_TYPE = "dry_run_store_contract"
ALLOWED_MODES = {"dry_run_store_contract_only"}
ALLOWED_STORAGE_FORMATS = {
    "append_only_jsonl",
    "append_only_json",
    "database_future",
    "in_memory_only",
    "audit_store_only",
    "execution_attempt_store_future",
}
BLOCKED_STORAGE_FORMATS = ALLOWED_STORAGE_FORMATS - {"append_only_jsonl"}
ALLOWED_TARGET_TYPES = {"agent", "team"}
BLOCKED_TARGET_TYPES = {
    "domain",
    "profile_catalog",
    "agent_preset",
    "paper_seed",
    "capability_policy",
    "tool_contract",
    "memory_contract",
    "runtime_contract",
    "execution_contract",
    "runtime_executor_contract",
    "execution_runner_contract",
    "execution_runner_dry_run_contract",
    "dry_run_store_contract",
    "audit_store",
    "observability_context",
    "ui",
    "integration",
    "scheduler",
    "worker_queue",
    "execution_attempt_store",
}
ALLOWED_STATUSES = {"passed", "blocked", "failed", "not_applicable"}
REQUIRED_FIELDS = {
    "schema_version",
    "contract_id",
    "contract_type",
    "version",
    "mode",
    "store_type",
    "storage_format",
    "append_only",
    "target_type",
    "target_id",
    "target_ref",
    "actor",
    "reason",
    "correlation_id",
    "idempotency_key",
    "created_at",
    "dry_run_id",
    "dry_run_result_ref",
    "dry_run_contract_ref",
    "execution_runner_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_result_ref",
    "audit_store_ref",
    "observability_context_ref",
    "capability_policy_ref",
    "entry_contract",
    "append_only_contract",
    "idempotency_contract",
    "checksum_contract",
    "reference_contract",
    "payload_boundary_contract",
    "retention_contract",
    "audit_contract",
    "observability_contract",
    "status",
    "blockers",
    "warnings",
    "evidence",
    "boundary_summary",
    "readiness_summary",
    "store_summary",
}
OBJECT_FIELDS = {
    "target_ref",
    "dry_run_result_ref",
    "dry_run_contract_ref",
    "execution_runner_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_result_ref",
    "audit_store_ref",
    "observability_context_ref",
    "capability_policy_ref",
    "entry_contract",
    "append_only_contract",
    "idempotency_contract",
    "checksum_contract",
    "reference_contract",
    "payload_boundary_contract",
    "retention_contract",
    "audit_contract",
    "observability_contract",
    "boundary_summary",
    "readiness_summary",
    "store_summary",
}


def build_dry_run_store_contract_report(
    *,
    contract_id: str,
    mode: str,
    store_type: str,
    storage_format: str,
    append_only: bool,
    target_type: str,
    target_id: str,
    target_ref: dict[str, Any] | None,
    actor: str,
    reason: str,
    correlation_id: str | None,
    idempotency_key: str | None,
    dry_run_id: str | None,
    dry_run_result_ref: dict[str, Any] | None,
    dry_run_contract_ref: dict[str, Any] | None,
    execution_runner_contract_ref: dict[str, Any] | None,
    runtime_preparation_ref: dict[str, Any] | None,
    execution_runner_result_ref: dict[str, Any] | None,
    audit_store_ref: dict[str, Any] | None,
    observability_context_ref: dict[str, Any] | None,
    capability_policy_ref: dict[str, Any] | None,
    entry_contract: dict[str, Any] | None,
    append_only_contract: dict[str, Any] | None,
    idempotency_contract: dict[str, Any] | None,
    checksum_contract: dict[str, Any] | None,
    reference_contract: dict[str, Any] | None,
    payload_boundary_contract: dict[str, Any] | None,
    retention_contract: dict[str, Any] | None,
    audit_contract: dict[str, Any] | None,
    observability_contract: dict[str, Any] | None,
    status: str,
    blockers: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    boundary_summary: dict[str, Any] | None = None,
    readiness_summary: dict[str, Any] | None = None,
    store_summary: dict[str, Any] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": DRY_RUN_STORE_CONTRACT_SCHEMA_VERSION,
        "contract_id": contract_id,
        "contract_type": DRY_RUN_STORE_CONTRACT_TYPE,
        "version": "1.0",
        "mode": mode,
        "store_type": store_type,
        "storage_format": storage_format,
        "append_only": append_only,
        "target_type": target_type,
        "target_id": target_id,
        "target_ref": dict(target_ref or {}),
        "actor": actor,
        "reason": reason,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "created_at": created_at or datetime.now().isoformat(),
        "dry_run_id": dry_run_id,
        "dry_run_result_ref": dict(dry_run_result_ref or {}),
        "dry_run_contract_ref": dict(dry_run_contract_ref or {}),
        "execution_runner_contract_ref": dict(execution_runner_contract_ref or {}),
        "runtime_preparation_ref": dict(runtime_preparation_ref or {}),
        "execution_runner_result_ref": dict(execution_runner_result_ref or {}),
        "audit_store_ref": dict(audit_store_ref or {}),
        "observability_context_ref": dict(observability_context_ref or {}),
        "capability_policy_ref": dict(capability_policy_ref or {}),
        "entry_contract": dict(entry_contract or {}),
        "append_only_contract": dict(append_only_contract or {}),
        "idempotency_contract": dict(idempotency_contract or {}),
        "checksum_contract": dict(checksum_contract or {}),
        "reference_contract": dict(reference_contract or {}),
        "payload_boundary_contract": dict(payload_boundary_contract or {}),
        "retention_contract": dict(retention_contract or {}),
        "audit_contract": dict(audit_contract or {}),
        "observability_contract": dict(observability_contract or {}),
        "status": status,
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "evidence": list(evidence or []),
        "boundary_summary": dict(boundary_summary or {}),
        "readiness_summary": dict(readiness_summary or {}),
        "store_summary": dict(store_summary or {}),
    }
    return validate_dry_run_store_contract_report(payload)


def validate_dry_run_store_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("dry_run_store_contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"dry_run_store_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != DRY_RUN_STORE_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de dry_run_store_contract invalida")
    if report.get("contract_type") != DRY_RUN_STORE_CONTRACT_TYPE:
        raise ValueError("contract_type de dry_run_store_contract invalido")
    _validate_id(report.get("contract_id"), "contract_id")
    if report.get("mode") not in ALLOWED_MODES:
        raise ValueError(f"mode invalido: {report.get('mode')}")
    if report.get("storage_format") not in ALLOWED_STORAGE_FORMATS:
        raise ValueError(f"storage_format invalido: {report.get('storage_format')}")
    if report.get("target_type") not in ALLOWED_TARGET_TYPES | BLOCKED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_id(report.get("target_id"), "target_id")
    for field in ["actor", "reason", "created_at", "version", "store_type"]:
        _validate_non_empty_text(report.get(field), field)
    if report.get("dry_run_id") is not None:
        _validate_id(report["dry_run_id"], "dry_run_id")
    if report.get("correlation_id") is not None:
        _validate_id(report["correlation_id"], "correlation_id")
    if report.get("idempotency_key") is not None:
        _validate_id(report["idempotency_key"], "idempotency_key")
    if report.get("status") not in ALLOWED_STATUSES:
        raise ValueError(f"status invalido: {report.get('status')}")
    if not isinstance(report.get("append_only"), bool):
        raise ValueError("append_only debe ser booleano")
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
        raise ValueError("dry_run_store_contract debe ser serializable como JSON") from exc
