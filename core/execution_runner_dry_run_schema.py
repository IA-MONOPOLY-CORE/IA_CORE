"""Schema de execution runner dry-run contract sin implementacion."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


EXECUTION_RUNNER_DRY_RUN_CONTRACT_SCHEMA_VERSION = "1.0"
EXECUTION_RUNNER_DRY_RUN_CONTRACT_TYPE = "execution_runner_dry_run_contract"
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
    "audit_store",
    "observability_context",
    "ui",
    "integration",
    "scheduler",
    "worker_queue",
}
ALLOWED_DRY_RUN_CONTRACT_MODES = {
    "dry_run_contract_only",
    "contract_only",
    "dry_run_only",
    "simulation_only",
    "no_model_execution_plan",
    "model_invocation_future",
    "tool_execution_future",
    "memory_persistence_future",
    "full_execution_future",
}
BLOCKED_DRY_RUN_CONTRACT_MODES = ALLOWED_DRY_RUN_CONTRACT_MODES - {"dry_run_contract_only", "contract_only"}
ALLOWED_STATUSES = {"passed", "blocked", "failed", "not_applicable"}
REQUIRED_FIELDS = {
    "schema_version",
    "contract_id",
    "contract_type",
    "version",
    "mode",
    "target_type",
    "target_id",
    "target_ref",
    "actor",
    "reason",
    "correlation_id",
    "idempotency_key",
    "created_at",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "preparation_id",
    "execution_runner_contract_ref",
    "audit_store_ref",
    "observability_context_ref",
    "capability_policy_ref",
    "readiness_contract",
    "simulation_contract",
    "plan_contract",
    "input_expectations",
    "output_expectations",
    "boundary_contract",
    "side_effect_contract",
    "risk_contract",
    "idempotency_contract",
    "lock_contract",
    "abort_contract",
    "rollback_contract",
    "audit_contract",
    "observability_contract",
    "status",
    "blockers",
    "warnings",
    "evidence",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
}
OBJECT_FIELDS = {
    "target_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "audit_store_ref",
    "observability_context_ref",
    "capability_policy_ref",
    "readiness_contract",
    "simulation_contract",
    "plan_contract",
    "input_expectations",
    "output_expectations",
    "boundary_contract",
    "side_effect_contract",
    "risk_contract",
    "idempotency_contract",
    "lock_contract",
    "abort_contract",
    "rollback_contract",
    "audit_contract",
    "observability_contract",
    "boundary_summary",
    "readiness_summary",
    "risk_summary",
}


def build_execution_runner_dry_run_contract_report(
    *,
    contract_id: str,
    mode: str,
    target_type: str,
    target_id: str,
    target_ref: dict[str, Any] | None,
    actor: str,
    reason: str,
    correlation_id: str | None,
    idempotency_key: str | None,
    runtime_contract_ref: dict[str, Any] | None,
    execution_contract_ref: dict[str, Any] | None,
    runtime_executor_contract_ref: dict[str, Any] | None,
    runtime_preparation_ref: dict[str, Any] | None,
    preparation_id: str | None,
    execution_runner_contract_ref: dict[str, Any] | None,
    audit_store_ref: dict[str, Any] | None,
    observability_context_ref: dict[str, Any] | None,
    capability_policy_ref: dict[str, Any] | None,
    readiness_contract: dict[str, Any] | None,
    simulation_contract: dict[str, Any] | None,
    plan_contract: dict[str, Any] | None,
    input_expectations: dict[str, Any] | None,
    output_expectations: dict[str, Any] | None,
    boundary_contract: dict[str, Any] | None,
    side_effect_contract: dict[str, Any] | None,
    risk_contract: dict[str, Any] | None,
    idempotency_contract: dict[str, Any] | None,
    lock_contract: dict[str, Any] | None,
    abort_contract: dict[str, Any] | None,
    rollback_contract: dict[str, Any] | None,
    audit_contract: dict[str, Any] | None,
    observability_contract: dict[str, Any] | None,
    status: str,
    blockers: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    boundary_summary: dict[str, Any] | None = None,
    readiness_summary: dict[str, Any] | None = None,
    risk_summary: dict[str, Any] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": EXECUTION_RUNNER_DRY_RUN_CONTRACT_SCHEMA_VERSION,
        "contract_id": contract_id,
        "contract_type": EXECUTION_RUNNER_DRY_RUN_CONTRACT_TYPE,
        "version": "1.0",
        "mode": mode,
        "target_type": target_type,
        "target_id": target_id,
        "target_ref": dict(target_ref or {}),
        "actor": actor,
        "reason": reason,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "created_at": created_at or datetime.now().isoformat(),
        "runtime_contract_ref": dict(runtime_contract_ref or {}),
        "execution_contract_ref": dict(execution_contract_ref or {}),
        "runtime_executor_contract_ref": dict(runtime_executor_contract_ref or {}),
        "runtime_preparation_ref": dict(runtime_preparation_ref or {}),
        "preparation_id": preparation_id,
        "execution_runner_contract_ref": dict(execution_runner_contract_ref or {}),
        "audit_store_ref": dict(audit_store_ref or {}),
        "observability_context_ref": dict(observability_context_ref or {}),
        "capability_policy_ref": dict(capability_policy_ref or {}),
        "readiness_contract": dict(readiness_contract or {}),
        "simulation_contract": dict(simulation_contract or {}),
        "plan_contract": dict(plan_contract or {}),
        "input_expectations": dict(input_expectations or {}),
        "output_expectations": dict(output_expectations or {}),
        "boundary_contract": dict(boundary_contract or {}),
        "side_effect_contract": dict(side_effect_contract or {}),
        "risk_contract": dict(risk_contract or {}),
        "idempotency_contract": dict(idempotency_contract or {}),
        "lock_contract": dict(lock_contract or {}),
        "abort_contract": dict(abort_contract or {}),
        "rollback_contract": dict(rollback_contract or {}),
        "audit_contract": dict(audit_contract or {}),
        "observability_contract": dict(observability_contract or {}),
        "status": status,
        "blockers": list(blockers or []),
        "warnings": list(warnings or []),
        "evidence": list(evidence or []),
        "boundary_summary": dict(boundary_summary or {}),
        "readiness_summary": dict(readiness_summary or {}),
        "risk_summary": dict(risk_summary or {}),
    }
    return validate_execution_runner_dry_run_contract_report(payload)


def validate_execution_runner_dry_run_contract_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("execution_runner_dry_run_contract debe ser un objeto")
    missing = REQUIRED_FIELDS - set(report)
    if missing:
        raise ValueError(f"execution_runner_dry_run_contract incompleto: {', '.join(sorted(missing))}")
    if report.get("schema_version") != EXECUTION_RUNNER_DRY_RUN_CONTRACT_SCHEMA_VERSION:
        raise ValueError("schema_version de execution_runner_dry_run_contract invalida")
    if report.get("contract_type") != EXECUTION_RUNNER_DRY_RUN_CONTRACT_TYPE:
        raise ValueError("contract_type de execution_runner_dry_run_contract invalido")
    _validate_id(report.get("contract_id"), "contract_id")
    if report.get("mode") not in ALLOWED_DRY_RUN_CONTRACT_MODES:
        raise ValueError(f"mode invalido: {report.get('mode')}")
    if report.get("target_type") not in ALLOWED_TARGET_TYPES | BLOCKED_TARGET_TYPES:
        raise ValueError(f"target_type invalido: {report.get('target_type')}")
    _validate_id(report.get("target_id"), "target_id")
    for field in ["actor", "reason", "created_at", "version"]:
        _validate_non_empty_text(report.get(field), field)
    if report.get("correlation_id") is not None:
        _validate_id(report.get("correlation_id"), "correlation_id")
    if report.get("idempotency_key") is not None:
        _validate_id(report.get("idempotency_key"), "idempotency_key")
    if report.get("preparation_id") is not None:
        _validate_id(report.get("preparation_id"), "preparation_id")
    if report.get("status") not in ALLOWED_STATUSES:
        raise ValueError(f"status invalido: {report.get('status')}")
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
        raise ValueError("execution_runner_dry_run_contract debe ser serializable como JSON") from exc
