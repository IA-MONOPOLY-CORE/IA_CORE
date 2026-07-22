"""Execution lifecycle preflight-transitions-only append-only store.

This module records validated preflight lifecycle transitions. It does not
create an operational execution_attempt_id, run agents or teams, invoke models
or tools, persist memory, open external access, start queues/workers, or mutate
targets.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


EXECUTION_LIFECYCLE_SCHEMA_VERSION = "1.0"
EXECUTION_LIFECYCLE_STORE_VERSION = "1.0"
EXECUTION_LIFECYCLE_ENTRY_TYPE = "execution_lifecycle_transition"
EXECUTION_LIFECYCLE_MODE = "execution_lifecycle_append_only"
LIFECYCLE_MODE = "preflight_transitions_only"
RECOMMENDED_EXECUTION_LIFECYCLE_STORE_PATH = Path("runtime/execution_lifecycle/execution_lifecycle_store.jsonl")
PASSED_CONTRACT_VERDICT = "EXECUTION_LIFECYCLE_CONTRACT_PASSED"
ALLOWED_STATES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
    "noop_idempotent",
}
BLOCKED_STATES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back",
    "rolled_back_real",
    "aborted_real",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
ALLOWED_TRANSITIONS = {
    ("created", "preflight_passed"),
    ("created", "preflight_blocked"),
    ("created", "blocked"),
    ("created", "failed"),
    ("created", "not_applicable"),
    ("preflight_passed", "blocked"),
    ("preflight_blocked", "blocked"),
    ("blocked", "noop_idempotent"),
    ("failed", "noop_idempotent"),
    ("not_applicable", "noop_idempotent"),
}
BLOCKED_TRANSITIONS = {
    ("created", "queued"),
    ("preflight_passed", "queued"),
    ("queued", "running"),
    ("running", "completed"),
    ("running", "failed"),
    ("running", "cancelled"),
    ("running", "rolled_back"),
    ("completed", "rolled_back"),
    ("cancelled", "rolled_back"),
}
OPERATIONAL_TARGET_STATES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
EXECUTION_FLAGS = {
    "execution_enabled": "execution_enabled_not_allowed",
    "agent_execution_enabled": "agent_execution_enabled_not_allowed",
    "team_execution_enabled": "team_execution_enabled_not_allowed",
    "model_invocation_enabled": "model_invocation_enabled_not_allowed",
    "tool_execution_enabled": "tool_execution_enabled_not_allowed",
    "memory_persistence_enabled": "memory_persistence_enabled_not_allowed",
    "external_access_enabled": "external_access_enabled_not_allowed",
    "scheduler_enabled": "scheduler_enabled_not_allowed",
    "worker_queue_enabled": "worker_queue_enabled_not_allowed",
    "rollback_operational_enabled": "rollback_operational_enabled_not_allowed",
    "retry_operational_enabled": "retry_operational_enabled_not_allowed",
    "cancel_operational_enabled": "cancel_operational_enabled_not_allowed",
}
FORBIDDEN_NESTED_KEYS = {
    "execution_attempt_id",
    "attempt_id",
    "attempt_id_generation_enabled",
    "attempt_id_persistence_enabled",
    "materialized_attempt_id",
    "attempt_ref_is_operational_id",
    "execution_payload",
    "execution_result",
    "execution_output",
    "agent_output",
    "team_output",
    "model_prompt_real",
    "model_response",
    "model_completion_real",
    "tool_call_real",
    "tool_result",
    "memory_write",
    "memory_read_result",
    "external_request",
    "external_response",
    "scheduler_job",
    "worker_task",
    "state_mutation",
    "artifact_mutation",
    "database_write_result",
    "network_response",
    "secret_value",
    "credential_value",
    "actual_output",
    "real_output",
    "live_response",
    "side_effect_result",
    "mutation_result",
}
FORBIDDEN_PATH_PARTS = {
    "execution_attempt_lifecycle",
    "execution_attempt_id",
    "execution_history",
    "execution_history_store",
    "scheduler",
    "worker_queue",
    "memoria_agentes",
    "memory",
    "ui",
    "integrations",
}


@dataclass(frozen=True)
class ExecutionLifecycleEntry:
    entry_id: str
    schema_version: str
    store_version: str
    entry_type: str
    mode: str
    lifecycle_mode: str
    target_ref: dict[str, Any]
    target_type: str
    target_id: str
    attempt_ref: str
    transition_ref: str
    source_state: str
    target_state: str
    transition: str
    execution_lifecycle_contract_ref: dict[str, Any]
    execution_lifecycle_contract_verdict: str
    execution_attempt_store_ref: dict[str, Any]
    execution_attempt_store_verified: bool
    execution_attempt_store_contract_ref: dict[str, Any]
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    dry_run_store_verified: bool
    dry_run_store_contract_ref: dict[str, Any]
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_executor_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]
    correlation_id: str
    idempotency_key: str
    sequence_number: int
    previous_entry_checksum: str | None
    entry_checksum: str | None
    created_at: str
    boundary_summary: dict[str, Any]
    dependency_summary: dict[str, Any]
    state_summary: dict[str, Any]
    transition_summary: dict[str, Any]
    attempt_id_summary: dict[str, Any]
    execution_boundary_summary: dict[str, Any]
    payload_boundary_summary: dict[str, Any]
    audit_summary: dict[str, Any]
    observability_summary: dict[str, Any]
    risk_summary: dict[str, Any]
    evidence: list[Any] | dict[str, Any]
    warnings: list[Any]
    blockers: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionLifecycleOperationResult:
    status: str
    verdict: str
    operation: str
    store_path: str
    entry_id: str | None = None
    target_ref: dict[str, Any] = field(default_factory=dict)
    attempt_ref: str | None = None
    transition_ref: str | None = None
    source_state: str | None = None
    target_state: str | None = None
    transition: str | None = None
    sequence_number: int | None = None
    previous_entry_checksum: str | None = None
    entry_checksum: str | None = None
    idempotency_key: str | None = None
    correlation_id: str | None = None
    mode: str = EXECUTION_LIFECYCLE_MODE
    lifecycle_mode: str = LIFECYCLE_MODE
    dependency_summary: dict[str, Any] = field(default_factory=dict)
    state_summary: dict[str, Any] = field(default_factory=dict)
    transition_summary: dict[str, Any] = field(default_factory=dict)
    attempt_id_summary: dict[str, Any] = field(default_factory=dict)
    execution_boundary_summary: dict[str, Any] = field(default_factory=dict)
    payload_boundary_summary: dict[str, Any] = field(default_factory=dict)
    audit_summary: dict[str, Any] = field(default_factory=dict)
    observability_summary: dict[str, Any] = field(default_factory=dict)
    store_summary: dict[str, Any] = field(default_factory=dict)
    boundary_summary: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    blockers: list[dict[str, str]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    entry: dict[str, Any] | None = None
    entries: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_execution_lifecycle_entry(
    *,
    execution_lifecycle_contract: dict[str, Any] | None,
    source_state: str = "created",
    target_state: str = "preflight_passed",
    sequence_number: int = 1,
    previous_entry_checksum: str | None = None,
    created_at: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    _validate_contract(execution_lifecycle_contract, blockers)
    contract = execution_lifecycle_contract or {}
    _validate_transition(source_state, target_state, blockers)
    _scan_forbidden_payload(contract, blockers)
    _scan_forbidden_payload(payload or {}, blockers)
    target_ref = deepcopy(contract.get("target_ref") or {})
    target_type = target_ref.get("target_type") or contract.get("target_type") or "target"
    target_id = target_ref.get("target_id") or contract.get("target_id") or "target"
    attempt_ref = contract.get("attempt_ref")
    transition = f"{source_state}->{target_state}"
    transition_ref = f"preflight_transition:{target_type}:{target_id}:{attempt_ref}:{transition}:{contract.get('correlation_id')}:{contract.get('idempotency_key')}"
    entry = ExecutionLifecycleEntry(
        entry_id=f"lifecycle:{target_type}:{target_id}:{sequence_number}",
        schema_version=EXECUTION_LIFECYCLE_SCHEMA_VERSION,
        store_version=EXECUTION_LIFECYCLE_STORE_VERSION,
        entry_type=EXECUTION_LIFECYCLE_ENTRY_TYPE,
        mode=EXECUTION_LIFECYCLE_MODE,
        lifecycle_mode=LIFECYCLE_MODE,
        target_ref=target_ref,
        target_type=target_type,
        target_id=target_id,
        attempt_ref=attempt_ref,
        transition_ref=transition_ref,
        source_state=source_state,
        target_state=target_state,
        transition=transition,
        execution_lifecycle_contract_ref=_contract_ref(contract),
        execution_lifecycle_contract_verdict=contract.get("verdict"),
        execution_attempt_store_ref=deepcopy(contract.get("execution_attempt_store_ref") or {}),
        execution_attempt_store_verified=(contract.get("dependency_summary") or {}).get("execution_attempt_store_verified") is True,
        execution_attempt_store_contract_ref=deepcopy(contract.get("execution_attempt_store_contract_ref") or {}),
        dry_run_ref=deepcopy(contract.get("dry_run_ref") or {}),
        dry_run_store_ref=deepcopy(contract.get("dry_run_store_ref") or {}),
        dry_run_store_verified=(contract.get("dependency_summary") or {}).get("dry_run_store_verified") is True,
        dry_run_store_contract_ref=deepcopy(contract.get("dry_run_store_contract_ref") or {}),
        runtime_contract_ref=deepcopy(contract.get("runtime_contract_ref") or {}),
        execution_contract_ref=deepcopy(contract.get("execution_contract_ref") or {}),
        runtime_executor_contract_ref=deepcopy(contract.get("runtime_executor_contract_ref") or {}),
        runtime_preparation_ref=deepcopy(contract.get("runtime_preparation_ref") or {}),
        execution_runner_contract_ref=deepcopy(contract.get("execution_runner_contract_ref") or {}),
        dry_run_contract_ref=deepcopy(contract.get("dry_run_contract_ref") or {}),
        audit_refs=deepcopy(contract.get("audit_refs") or {}),
        observability_refs=deepcopy(contract.get("observability_refs") or {}),
        capability_policy_ref=deepcopy(contract.get("capability_policy_ref") or {}),
        correlation_id=contract.get("correlation_id"),
        idempotency_key=contract.get("idempotency_key"),
        sequence_number=sequence_number,
        previous_entry_checksum=previous_entry_checksum,
        entry_checksum=None,
        created_at=created_at or datetime.now().isoformat(),
        boundary_summary=build_boundary_summary(),
        dependency_summary=build_dependency_summary(contract),
        state_summary=build_state_summary(source_state, target_state),
        transition_summary=build_transition_summary(source_state, target_state),
        attempt_id_summary=build_attempt_id_summary(contract),
        execution_boundary_summary=deepcopy(contract.get("execution_boundary_summary") or contract.get("execution_boundary_policy") or {}),
        payload_boundary_summary=build_payload_boundary_summary(),
        audit_summary=deepcopy(contract.get("audit_summary") or {}),
        observability_summary=deepcopy(contract.get("observability_summary") or {}),
        risk_summary=build_risk_summary(),
        evidence=deepcopy(contract.get("evidence") or []),
        warnings=[],
        blockers=[],
    ).to_dict()
    validate_execution_lifecycle_entry(entry, blockers=blockers)
    if blockers:
        raise ValueError("; ".join(blocker["code"] for blocker in blockers))
    entry["entry_checksum"] = compute_execution_lifecycle_entry_checksum(entry)
    validate_execution_lifecycle_entry(entry)
    return entry


def append_execution_lifecycle_transition(
    *,
    execution_lifecycle_contract: dict[str, Any] | None,
    store_path: str | Path,
    source_state: str = "created",
    target_state: str = "preflight_passed",
    allow_external_test_path: bool = False,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path)
    _validate_contract(execution_lifecycle_contract, blockers)
    _validate_transition(source_state, target_state, blockers)
    _scan_forbidden_payload(payload or {}, blockers)
    entries, read_blockers = _read_entries(path)
    blockers.extend(read_blockers)
    if blockers:
        return _operation_result("blocked", _verdict(blockers), "append", path, blockers=blockers)
    previous_checksum = entries[-1]["entry_checksum"] if entries else None
    sequence = len(entries) + 1
    try:
        entry = build_execution_lifecycle_entry(
            execution_lifecycle_contract=execution_lifecycle_contract,
            source_state=source_state,
            target_state=target_state,
            sequence_number=sequence,
            previous_entry_checksum=previous_checksum,
            payload=payload,
        )
    except ValueError as exc:
        for code in str(exc).split("; "):
            _block(blockers, code, code)
        return _operation_result("blocked", _verdict(blockers), "append", path, blockers=blockers)
    scope = _idempotency_scope(entry)
    for existing in entries:
        if _idempotency_scope(existing) != scope:
            continue
        if _logical_lifecycle_payload(existing) == _logical_lifecycle_payload(entry):
            return _operation_result(
                "noop_idempotent",
                "EXECUTION_LIFECYCLE_IDEMPOTENT_NOOP",
                "append",
                path,
                entry=existing,
                idempotency_key=entry["idempotency_key"],
                correlation_id=entry["correlation_id"],
                entry_checksum=existing.get("entry_checksum"),
                previous_entry_checksum=existing.get("previous_entry_checksum"),
                sequence_number=existing.get("sequence_number"),
                entry_id=existing.get("entry_id"),
                target_ref=existing.get("target_ref") or {},
                attempt_ref=existing.get("attempt_ref"),
                transition_ref=existing.get("transition_ref"),
                source_state=existing.get("source_state"),
                target_state=existing.get("target_state"),
                transition=existing.get("transition"),
                store_summary=build_store_summary(path, entries),
            )
        _block(blockers, "idempotency_conflict", "same idempotency scope with different lifecycle payload")
        return _operation_result("blocked", "EXECUTION_LIFECYCLE_IDEMPOTENCY_CONFLICT", "append", path, blockers=blockers, entry=existing)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = canonicalize_execution_lifecycle_entry(entry)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    return _operation_result(
        "appended",
        "EXECUTION_LIFECYCLE_TRANSITION_APPENDED",
        "append",
        path,
        entry=entry,
        idempotency_key=entry["idempotency_key"],
        correlation_id=entry["correlation_id"],
        entry_checksum=entry["entry_checksum"],
        previous_entry_checksum=entry["previous_entry_checksum"],
        sequence_number=entry["sequence_number"],
        entry_id=entry["entry_id"],
        target_ref=entry["target_ref"],
        attempt_ref=entry["attempt_ref"],
        transition_ref=entry["transition_ref"],
        source_state=entry["source_state"],
        target_state=entry["target_state"],
        transition=entry["transition"],
        store_summary=build_store_summary(path, entries + [entry]),
        evidence=[{"name": "appended", "passed": True}],
    )


def get_execution_lifecycle_entry(*, entry_id: str, store_path: str | Path, allow_external_test_path: bool = False) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path, must_exist=True)
    entries, read_blockers = _read_entries(path)
    blockers.extend(read_blockers)
    if blockers:
        return _operation_result("blocked", _verdict(blockers), "get", path, blockers=blockers)
    for entry in entries:
        if entry.get("entry_id") == entry_id:
            return _operation_result("verified", "EXECUTION_LIFECYCLE_STORE_VERIFIED", "get", path, entry=entry, entry_id=entry_id, entries=[entry])
    return _operation_result("not_found", "EXECUTION_LIFECYCLE_NOT_FOUND", "get", path, entry_id=entry_id)


def list_execution_lifecycle_entries(
    *,
    store_path: str | Path,
    target_type: str | None = None,
    target_id: str | None = None,
    attempt_ref: str | None = None,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path, must_exist=True)
    entries, read_blockers = _read_entries(path)
    blockers.extend(read_blockers)
    if blockers:
        return _operation_result("blocked", _verdict(blockers), "list", path, blockers=blockers)
    filtered = []
    for entry in entries:
        if target_type and entry.get("target_type") != target_type:
            continue
        if target_id and entry.get("target_id") != target_id:
            continue
        if attempt_ref and entry.get("attempt_ref") != attempt_ref:
            continue
        filtered.append(entry)
    status = "verified" if filtered else "not_found"
    verdict = "EXECUTION_LIFECYCLE_STORE_VERIFIED" if filtered else "EXECUTION_LIFECYCLE_NOT_FOUND"
    return _operation_result(status, verdict, "list", path, entries=filtered, store_summary=build_store_summary(path, filtered))


def verify_execution_lifecycle_store(*, store_path: str | Path, allow_external_test_path: bool = False) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path, must_exist=True)
    entries, read_blockers = _read_entries(path, verify_canonical=True)
    blockers.extend(read_blockers)
    previous = None
    for index, entry in enumerate(entries, start=1):
        if entry.get("sequence_number") != index:
            _block(blockers, "sequence_mismatch", "sequence_number must be monotonic")
        if entry.get("previous_entry_checksum") != previous:
            _block(blockers, "previous_checksum_mismatch", "previous_entry_checksum mismatch")
        expected = compute_execution_lifecycle_entry_checksum(entry)
        if entry.get("entry_checksum") != expected:
            _block(blockers, "checksum_mismatch", "entry_checksum mismatch")
        validate_execution_lifecycle_entry(entry, blockers=blockers)
        previous = entry.get("entry_checksum")
    if blockers:
        return _operation_result("failed", _verdict(blockers), "verify", path, blockers=blockers, entries=entries)
    return _operation_result(
        "verified",
        "EXECUTION_LIFECYCLE_STORE_VERIFIED",
        "verify",
        path,
        entries=entries,
        entry_checksum=previous,
        store_summary=build_store_summary(path, entries),
        evidence=[{"name": "verified", "passed": True}],
    )


def replay_execution_lifecycle_idempotency(*, store_path: str | Path, entry: dict[str, Any], allow_external_test_path: bool = False) -> dict[str, Any]:
    path = Path(store_path)
    entries, blockers = _read_entries(path)
    if blockers:
        return _operation_result("blocked", _verdict(blockers), "replay_idempotency", path, blockers=blockers)
    scope = _idempotency_scope(entry)
    for existing in entries:
        if _idempotency_scope(existing) == scope and _logical_lifecycle_payload(existing) == _logical_lifecycle_payload(entry):
            return _operation_result(
                "noop_idempotent",
                "EXECUTION_LIFECYCLE_IDEMPOTENT_NOOP",
                "replay_idempotency",
                path,
                entry=existing,
                entry_id=existing.get("entry_id"),
                entry_checksum=existing.get("entry_checksum"),
                sequence_number=existing.get("sequence_number"),
            )
    return _operation_result("not_found", "EXECUTION_LIFECYCLE_NOT_FOUND", "replay_idempotency", path)


def compute_execution_lifecycle_entry_checksum(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("entry_checksum", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def canonicalize_execution_lifecycle_entry(entry: dict[str, Any]) -> str:
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate_execution_lifecycle_entry(entry: dict[str, Any], blockers: list[dict[str, str]] | None = None) -> bool:
    local_blockers: list[dict[str, str]] = [] if blockers is None else blockers
    required = {
        "entry_id",
        "schema_version",
        "store_version",
        "entry_type",
        "mode",
        "lifecycle_mode",
        "target_ref",
        "target_type",
        "target_id",
        "attempt_ref",
        "transition_ref",
        "source_state",
        "target_state",
        "transition",
        "execution_lifecycle_contract_ref",
        "execution_lifecycle_contract_verdict",
        "execution_attempt_store_ref",
        "execution_attempt_store_contract_ref",
        "dry_run_ref",
        "dry_run_store_ref",
        "dry_run_store_contract_ref",
        "runtime_contract_ref",
        "execution_contract_ref",
        "runtime_executor_contract_ref",
        "runtime_preparation_ref",
        "execution_runner_contract_ref",
        "dry_run_contract_ref",
        "audit_refs",
        "observability_refs",
        "capability_policy_ref",
        "correlation_id",
        "idempotency_key",
        "sequence_number",
        "created_at",
        "boundary_summary",
        "dependency_summary",
        "state_summary",
        "transition_summary",
        "attempt_id_summary",
        "execution_boundary_summary",
        "payload_boundary_summary",
        "audit_summary",
        "observability_summary",
        "risk_summary",
        "evidence",
        "warnings",
        "blockers",
    }
    allow_empty = {"warnings", "blockers"}
    for field_name in required:
        if entry.get(field_name) in (None, "", {}, []) and field_name not in allow_empty:
            _block(local_blockers, f"missing_{field_name}", f"{field_name} required")
    if entry.get("schema_version") != EXECUTION_LIFECYCLE_SCHEMA_VERSION:
        _block(local_blockers, "invalid_schema_version", "invalid schema_version")
    if entry.get("entry_type") != EXECUTION_LIFECYCLE_ENTRY_TYPE:
        _block(local_blockers, "invalid_entry_type", "invalid entry_type")
    if entry.get("mode") != EXECUTION_LIFECYCLE_MODE:
        _block(local_blockers, "invalid_mode", "invalid mode")
    if entry.get("lifecycle_mode") != LIFECYCLE_MODE:
        _block(local_blockers, "invalid_lifecycle_mode", "invalid lifecycle_mode")
    _validate_attempt_ref(entry.get("attempt_ref"), local_blockers)
    _validate_transition(entry.get("source_state"), entry.get("target_state"), local_blockers)
    if entry.get("transition") != f"{entry.get('source_state')}->{entry.get('target_state')}":
        _block(local_blockers, "invalid_transition", "transition string mismatch")
    _validate_summary_flags(entry, local_blockers)
    _scan_forbidden_payload(entry, local_blockers)
    if blockers is None and local_blockers:
        raise ValueError("; ".join(blocker["code"] for blocker in local_blockers))
    return not local_blockers


def build_dependency_summary(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "execution_lifecycle_contract_passed": contract.get("status") == "passed" and contract.get("verdict") == PASSED_CONTRACT_VERDICT,
        "execution_attempt_store_verified": (contract.get("dependency_summary") or {}).get("execution_attempt_store_verified") is True,
        "dry_run_store_verified": (contract.get("dependency_summary") or {}).get("dry_run_store_verified") is True,
        "required_refs_present": bool(contract.get("execution_attempt_store_ref") and contract.get("dry_run_store_ref")),
    }


def build_state_summary(source_state: str, target_state: str) -> dict[str, Any]:
    return {"source_state": source_state, "target_state": target_state, "allowed_states": sorted(ALLOWED_STATES), "blocked_states": sorted(BLOCKED_STATES)}


def build_transition_summary(source_state: str, target_state: str) -> dict[str, Any]:
    return {"transition": f"{source_state}->{target_state}", "allowed_transitions": [f"{src}->{dst}" for src, dst in sorted(ALLOWED_TRANSITIONS)]}


def build_attempt_id_summary(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "attempt_ref": contract.get("attempt_ref"),
        "attempt_ref_is_operational_id": False,
        "attempt_id_generation": "disabled",
        "attempt_id_persistence": "disabled",
        "materialized_attempt_id": False,
    }


def build_payload_boundary_summary() -> dict[str, Any]:
    return {"real_payloads_allowed": False, "forbidden_fields": sorted(FORBIDDEN_NESTED_KEYS), "deep_scan_required": True}


def build_boundary_summary() -> dict[str, Any]:
    return {
        "execution_lifecycle_preflight_only": True,
        "execution_enabled": False,
        "agent_execution_enabled": False,
        "team_execution_enabled": False,
        "model_invocation_enabled": False,
        "tool_execution_enabled": False,
        "memory_persistence_enabled": False,
        "external_access_enabled": False,
        "scheduler_enabled": False,
        "worker_queue_enabled": False,
        "mutation_allowed": False,
    }


def build_risk_summary() -> dict[str, Any]:
    return {"scope": "preflight_transitions_only_append_only", "real_execution_allowed": False}


def build_store_summary(path: Path, entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "store_path": str(path),
        "entry_count": len(entries),
        "append_only": True,
        "storage_format": "jsonl",
        "canonical_serialization": "json_sort_keys_compact_utf8",
    }


def _validate_contract(contract: dict[str, Any] | None, blockers: list[dict[str, str]]) -> None:
    if not contract:
        _block(blockers, "missing_execution_lifecycle_contract_ref", "execution_lifecycle_contract required")
        return
    if contract.get("status") != "passed" or contract.get("verdict") != PASSED_CONTRACT_VERDICT:
        _block(blockers, "execution_lifecycle_contract_not_passed", "execution_lifecycle_contract must be passed")
    required_refs = {
        "execution_attempt_store_ref": "missing_execution_attempt_store_ref",
        "execution_attempt_store_contract_ref": "missing_execution_attempt_store_contract_ref",
        "dry_run_ref": "missing_dry_run_ref",
        "dry_run_store_ref": "missing_dry_run_store_ref",
        "dry_run_store_contract_ref": "missing_dry_run_store_contract_ref",
        "runtime_contract_ref": "missing_runtime_contract_ref",
        "execution_contract_ref": "missing_execution_contract_ref",
        "runtime_executor_contract_ref": "missing_runtime_executor_contract_ref",
        "runtime_preparation_ref": "missing_runtime_preparation_ref",
        "execution_runner_contract_ref": "missing_execution_runner_contract_ref",
        "dry_run_contract_ref": "missing_dry_run_contract_ref",
        "audit_refs": "missing_audit_refs",
        "observability_refs": "missing_observability_refs",
        "capability_policy_ref": "missing_capability_policy_ref",
    }
    for field_name, code in required_refs.items():
        if contract.get(field_name) in (None, "", {}, []):
            _block(blockers, code, f"{field_name} required")
    if not contract.get("attempt_ref"):
        _block(blockers, "missing_attempt_ref", "attempt_ref required")
    _validate_attempt_ref(contract.get("attempt_ref"), blockers)
    if not contract.get("correlation_id"):
        _block(blockers, "missing_correlation_id", "correlation_id required")
    if not contract.get("idempotency_key"):
        _block(blockers, "missing_idempotency_key", "idempotency_key required")
    if (contract.get("dependency_summary") or {}).get("execution_attempt_store_verified") is not True:
        _block(blockers, "execution_attempt_store_not_verified", "execution_attempt_store must be verified")
    if (contract.get("dependency_summary") or {}).get("dry_run_store_verified") is not True:
        _block(blockers, "dry_run_store_not_verified", "dry_run_store must be verified")
    _validate_cross_refs(contract, blockers)
    _validate_summary_flags(contract, blockers)


def _validate_cross_refs(contract: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    target_ref = contract.get("target_ref") or {}
    target_type = target_ref.get("target_type")
    target_id = target_ref.get("target_id")
    attempt_ref = contract.get("attempt_ref")
    correlation_id = contract.get("correlation_id")
    idempotency_key = contract.get("idempotency_key")
    dry_run_id = (contract.get("dry_run_ref") or {}).get("dry_run_id")
    for name in [
        "execution_attempt_store_ref",
        "execution_attempt_store_contract_ref",
        "dry_run_ref",
        "dry_run_store_ref",
        "dry_run_store_contract_ref",
        "runtime_contract_ref",
        "execution_contract_ref",
        "runtime_executor_contract_ref",
        "runtime_preparation_ref",
        "execution_runner_contract_ref",
        "dry_run_contract_ref",
    ]:
        ref = contract.get(name) or {}
        if ref.get("target_type") and target_type and ref.get("target_type") != target_type:
            _block(blockers, "target_type_mismatch", f"{name} target_type mismatch")
        if ref.get("target_id") and target_id and ref.get("target_id") != target_id:
            _block(blockers, "target_id_mismatch", f"{name} target_id mismatch")
        if ref.get("attempt_ref") and attempt_ref and ref.get("attempt_ref") != attempt_ref:
            _block(blockers, "attempt_ref_mismatch", f"{name} attempt_ref mismatch")
        if ref.get("correlation_id") and correlation_id and ref.get("correlation_id") != correlation_id:
            _block(blockers, "correlation_id_mismatch", f"{name} correlation_id mismatch")
        if ref.get("idempotency_key") and idempotency_key and ref.get("idempotency_key") != idempotency_key:
            _block(blockers, "idempotency_key_mismatch", f"{name} idempotency_key mismatch")
        if ref.get("dry_run_id") and dry_run_id and ref.get("dry_run_id") != dry_run_id:
            _block(blockers, "dry_run_ref_mismatch", f"{name} dry_run_ref mismatch")
        if name == "execution_attempt_store_ref" and ref.get("entry_checksum") and not str(ref.get("entry_checksum")).startswith("sha256:"):
            _block(blockers, "execution_attempt_store_ref_mismatch", "execution_attempt_store_ref checksum mismatch")
        if name.endswith("contract_ref") and ref.get("status") == "failed":
            _block(blockers, "contract_ref_mismatch", f"{name} failed")


def _validate_summary_flags(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for container_name in ["boundary_summary", "execution_boundary_summary", "execution_boundary_policy", "scheduler_worker_policy", "model_tool_memory_policy", "external_access_policy"]:
        container = payload.get(container_name) or {}
        if not isinstance(container, dict):
            continue
        for flag, code in EXECUTION_FLAGS.items():
            if container.get(flag) is True:
                _block(blockers, code, f"{flag} must be false")
    attempt = payload.get("attempt_id_summary") or payload.get("attempt_id_policy") or {}
    if isinstance(attempt, dict):
        if attempt.get("execution_attempt_id") not in (None, "", {}, []):
            _block(blockers, "execution_attempt_id_not_allowed", "execution_attempt_id forbidden")
        if attempt.get("attempt_id") not in (None, "", {}, []):
            _block(blockers, "attempt_id_not_allowed", "attempt_id forbidden")
        if attempt.get("attempt_id_generation_enabled") is True:
            _block(blockers, "attempt_id_generation_enabled_not_allowed", "attempt_id_generation_enabled forbidden")
        if attempt.get("attempt_id_persistence_enabled") is True:
            _block(blockers, "attempt_id_persistence_enabled_not_allowed", "attempt_id_persistence_enabled forbidden")
        if attempt.get("materialized_attempt_id") is True:
            _block(blockers, "materialized_attempt_id_not_allowed", "materialized_attempt_id forbidden")
        if attempt.get("attempt_ref_is_operational_id") is True:
            _block(blockers, "attempt_ref_is_operational_id_not_allowed", "attempt_ref_is_operational_id forbidden")


def _validate_transition(source_state: str | None, target_state: str | None, blockers: list[dict[str, str]]) -> None:
    for state, role in [(source_state, "source"), (target_state, "target")]:
        if state in BLOCKED_STATES:
            _block(blockers, f"{state}_state_not_allowed", f"{role} state forbidden")
        elif state not in ALLOWED_STATES:
            _block(blockers, "invalid_lifecycle_state", f"{role} state invalid")
    transition = (source_state, target_state)
    if target_state in OPERATIONAL_TARGET_STATES:
        _block(blockers, f"{target_state}_transition_not_allowed", "operational transition forbidden")
    if transition in BLOCKED_TRANSITIONS:
        _block(blockers, f"{target_state}_transition_not_allowed", "blocked transition")
    if transition not in ALLOWED_TRANSITIONS:
        _block(blockers, "invalid_transition", "transition not allowed")


def _validate_attempt_ref(attempt_ref: Any, blockers: list[dict[str, str]]) -> None:
    if not isinstance(attempt_ref, str) or not attempt_ref:
        _block(blockers, "missing_attempt_ref", "attempt_ref required")
        return
    if not attempt_ref.startswith("preflight:"):
        _block(blockers, "attempt_ref_invalid", "attempt_ref must start with preflight:")
    if attempt_ref in {"attempt_id", "execution_attempt_id"}:
        _block(blockers, "attempt_ref_is_operational_id_not_allowed", "attempt_ref cannot be operational id")


def _scan_forbidden_payload(payload: Any, blockers: list[dict[str, str]]) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_NESTED_KEYS and value is not False and value not in (None, "", {}, []):
                _block(blockers, f"{key}_not_allowed", f"{key} forbidden")
            _scan_forbidden_payload(value, blockers)
    elif isinstance(payload, list):
        for item in payload:
            _scan_forbidden_payload(item, blockers)


def _validate_store_path(path: Path, blockers: list[dict[str, str]], *, allow_external_test_path: bool, must_exist: bool = False) -> None:
    if path.suffix != ".jsonl":
        _block(blockers, "invalid_storage_format", "execution_lifecycle store must be .jsonl")
    parts = {part.lower() for part in path.parts}
    if parts & FORBIDDEN_PATH_PARTS:
        _block(blockers, "invalid_storage_path", "blocked path part for execution_lifecycle store")
    if must_exist and not path.exists():
        _block(blockers, "store_not_found", "store not found")
    try:
        resolved = path.resolve()
        root = Path.cwd().resolve()
        temp_root = Path(tempfile.gettempdir()).resolve()
        inside_project = resolved == root or root in resolved.parents
        inside_temp = resolved == temp_root or temp_root in resolved.parents
        if not inside_project and not inside_temp and not allow_external_test_path:
            _block(blockers, "invalid_storage_path", "store path outside project/temp")
    except OSError as exc:
        _block(blockers, "invalid_storage_path", f"invalid path: {exc}")


def _read_entries(path: Path, *, verify_canonical: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    entries: list[dict[str, Any]] = []
    blockers: list[dict[str, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            _block(blockers, "store_corrupt_json", f"corrupt JSON at line {line_number}")
            continue
        if verify_canonical and canonicalize_execution_lifecycle_entry(entry) != line:
            _block(blockers, "canonical_serialization_mismatch", "canonical serialization mismatch")
        entries.append(entry)
    return entries, blockers


def _verdict(blockers: list[dict[str, str]]) -> str:
    codes = {blocker["code"] for blocker in blockers}
    if not codes:
        return "EXECUTION_LIFECYCLE_BLOCKED"
    if "store_corrupt_json" in codes:
        return "EXECUTION_LIFECYCLE_STORE_CORRUPT"
    if "checksum_mismatch" in codes:
        return "EXECUTION_LIFECYCLE_CHECKSUM_MISMATCH"
    if "previous_checksum_mismatch" in codes:
        return "EXECUTION_LIFECYCLE_PREVIOUS_CHECKSUM_MISMATCH"
    if "sequence_mismatch" in codes:
        return "EXECUTION_LIFECYCLE_SEQUENCE_MISMATCH"
    if any("attempt_id" in code or code == "execution_attempt_id_not_allowed" for code in codes):
        return "EXECUTION_LIFECYCLE_ATTEMPT_ID_LEAK"
    if any("state_not_allowed" in code or code == "invalid_lifecycle_state" for code in codes):
        return "EXECUTION_LIFECYCLE_STATE_LEAK"
    if any("transition_not_allowed" in code or code == "invalid_transition" for code in codes):
        return "EXECUTION_LIFECYCLE_TRANSITION_LEAK"
    if any(prefix in code for code in codes for prefix in ["execution_payload", "agent_output", "team_output", "model_", "tool_", "memory_", "secret_value", "credential_value"]):
        return "EXECUTION_LIFECYCLE_PAYLOAD_LEAK"
    if any(code in {"execution_enabled_not_allowed", "agent_execution_enabled_not_allowed", "team_execution_enabled_not_allowed", "rollback_operational_enabled_not_allowed", "retry_operational_enabled_not_allowed", "cancel_operational_enabled_not_allowed"} for code in codes):
        return "EXECUTION_LIFECYCLE_EXECUTION_BOUNDARY"
    if any("scheduler" in code or "worker" in code for code in codes):
        return "EXECUTION_LIFECYCLE_SCHEDULER_WORKER_BOUNDARY"
    if any("external" in code for code in codes):
        return "EXECUTION_LIFECYCLE_EXTERNAL_BOUNDARY"
    if any("mutation" in code or "database_write" in code for code in codes):
        return "EXECUTION_LIFECYCLE_MUTATION_BOUNDARY"
    if "execution_lifecycle_contract_not_passed" in codes:
        return "EXECUTION_LIFECYCLE_CONTRACT_NOT_PASSED"
    return "EXECUTION_LIFECYCLE_BLOCKED"


def _operation_result(
    status: str,
    verdict: str,
    operation: str,
    path: Path,
    *,
    entry: dict[str, Any] | None = None,
    entries: list[dict[str, Any]] | None = None,
    entry_id: str | None = None,
    target_ref: dict[str, Any] | None = None,
    attempt_ref: str | None = None,
    transition_ref: str | None = None,
    source_state: str | None = None,
    target_state: str | None = None,
    transition: str | None = None,
    sequence_number: int | None = None,
    previous_entry_checksum: str | None = None,
    entry_checksum: str | None = None,
    idempotency_key: str | None = None,
    correlation_id: str | None = None,
    store_summary: dict[str, Any] | None = None,
    blockers: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    selected = entry or {}
    return ExecutionLifecycleOperationResult(
        status=status,
        verdict=verdict,
        operation=operation,
        store_path=str(path),
        entry_id=entry_id or selected.get("entry_id"),
        target_ref=target_ref or selected.get("target_ref") or {},
        attempt_ref=attempt_ref or selected.get("attempt_ref"),
        transition_ref=transition_ref or selected.get("transition_ref"),
        source_state=source_state or selected.get("source_state"),
        target_state=target_state or selected.get("target_state"),
        transition=transition or selected.get("transition"),
        sequence_number=sequence_number if sequence_number is not None else selected.get("sequence_number"),
        previous_entry_checksum=previous_entry_checksum if previous_entry_checksum is not None else selected.get("previous_entry_checksum"),
        entry_checksum=entry_checksum or selected.get("entry_checksum"),
        idempotency_key=idempotency_key or selected.get("idempotency_key"),
        correlation_id=correlation_id or selected.get("correlation_id"),
        dependency_summary=selected.get("dependency_summary") or {},
        state_summary=selected.get("state_summary") or {},
        transition_summary=selected.get("transition_summary") or {},
        attempt_id_summary=selected.get("attempt_id_summary") or {},
        execution_boundary_summary=selected.get("execution_boundary_summary") or {},
        payload_boundary_summary=selected.get("payload_boundary_summary") or {},
        audit_summary=selected.get("audit_summary") or {},
        observability_summary=selected.get("observability_summary") or {},
        store_summary=store_summary or build_store_summary(path, entries or ([] if entry is None else [entry])),
        boundary_summary=selected.get("boundary_summary") or build_boundary_summary(),
        warnings=warnings or [],
        blockers=blockers or [],
        evidence=evidence or [],
        entry=entry,
        entries=entries,
    ).to_dict()


def _contract_ref(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": contract.get("contract_id"),
        "status": contract.get("status"),
        "verdict": contract.get("verdict"),
        "mode": contract.get("mode"),
        "lifecycle_mode": contract.get("lifecycle_mode"),
        "correlation_id": contract.get("correlation_id"),
        "idempotency_key": contract.get("idempotency_key"),
    }


def _idempotency_scope(entry: dict[str, Any]) -> tuple[Any, ...]:
    return (
        entry.get("target_type"),
        entry.get("target_id"),
        entry.get("attempt_ref"),
        entry.get("source_state"),
        entry.get("target_state"),
        entry.get("correlation_id"),
        entry.get("idempotency_key"),
    )


def _logical_lifecycle_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    for key in ["entry_id", "sequence_number", "previous_entry_checksum", "entry_checksum", "created_at"]:
        payload.pop(key, None)
    return payload


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
