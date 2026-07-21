"""Execution attempt preflight-only append-only store.

Persists preflight/intention records in canonical JSONL. It does not create an
operational execution_attempt_id, lifecycle, execution history, model/tool
outputs, memory writes, external access records, scheduler jobs, worker tasks,
or target mutations.
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


EXECUTION_ATTEMPT_STORE_SCHEMA_VERSION = "1.0"
EXECUTION_ATTEMPT_STORE_RECORD_TYPE = "execution_attempt_preflight"
EXECUTION_ATTEMPT_STORE_MODE = "execution_attempt_store_preflight_only"
EXECUTION_ATTEMPT_MODE = "preflight_only"
RECOMMENDED_EXECUTION_ATTEMPT_STORE_PATH = Path("runtime/execution_attempts/execution_attempt_store.jsonl")
PASSED_CONTRACT_VERDICT = "EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED"
ALLOWED_APPEND_STATUSES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
    "noop_idempotent",
}
BLOCKED_LIFECYCLE_STATUSES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back_real",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
FORBIDDEN_PATH_PARTS = {
    "execution_attempt_id",
    "execution_attempt_lifecycle",
    "execution_history",
    "execution_history_store",
    "scheduler",
    "worker_queue",
    "memoria_agentes",
    "memory",
    "ui",
    "integrations",
}
FORBIDDEN_NESTED_KEYS = {
    "execution_attempt_id",
    "attempt_id",
    "attempt_id_generation_enabled",
    "attempt_id_persistence_enabled",
    "materialized_attempt_id",
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


@dataclass(frozen=True)
class ExecutionAttemptPreflightStoreEntry:
    record_type: str
    schema_version: str
    attempt_ref: str
    attempt_mode: str
    mode: str
    status: str
    target_ref: dict[str, Any]
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    dry_run_store_verification_ref: dict[str, Any]
    dry_run_store_checksum_ref: str
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_executor_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    dry_run_store_contract_ref: dict[str, Any]
    execution_attempt_store_contract_ref: dict[str, Any]
    preflight_summary: dict[str, Any]
    readiness_summary: dict[str, Any]
    boundary_summary: dict[str, Any]
    risk_summary: dict[str, Any]
    blocked_capabilities: list[Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]
    correlation_id: str
    idempotency_key: str
    created_at: str
    entry_checksum: str | None
    previous_entry_checksum: str | None
    evidence: dict[str, Any] | list[Any]
    warnings: list[Any]
    blockers: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionAttemptStoreOperationResult:
    status: str
    operation: str
    attempt_ref: str | None
    store_path: str
    entry_checksum: str | None = None
    previous_entry_checksum: str | None = None
    idempotency_status: str | None = None
    written: bool = False
    read_only: bool = False
    verified: bool = False
    blockers: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    entry: dict[str, Any] | None = None
    entries: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_attempt_ref(*, target_type: str, target_id: str, correlation_id: str, idempotency_key: str) -> str:
    """Build a declarative preflight reference, not an operational execution_attempt_id."""
    return f"preflight:{target_type}:{target_id}:{correlation_id}:{idempotency_key}"


def build_execution_attempt_preflight_entry(
    *,
    execution_attempt_store_contract: dict[str, Any],
    dry_run_store_verification: dict[str, Any],
    attempt_ref: str | None = None,
    status: str = "preflight_passed",
    previous_entry_checksum: str | None = None,
    preflight_summary: dict[str, Any] | None = None,
    readiness_summary: dict[str, Any] | None = None,
    boundary_summary: dict[str, Any] | None = None,
    risk_summary: dict[str, Any] | None = None,
    blocked_capabilities: list[Any] | None = None,
    evidence: dict[str, Any] | list[Any] | None = None,
    warnings: list[Any] | None = None,
    blockers: list[Any] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    validation_blockers: list[dict[str, str]] = []
    _validate_contract(execution_attempt_store_contract, validation_blockers)
    _validate_dry_run_store_verification(dry_run_store_verification, validation_blockers, execution_attempt_store_contract)

    contract = execution_attempt_store_contract or {}
    target_ref = deepcopy(contract.get("target_ref") or {})
    resolved_attempt_ref = build_attempt_ref(
        target_type=target_ref.get("target_type") or "target",
        target_id=target_ref.get("target_id") or "target",
        correlation_id=contract.get("correlation_id") or "correlation",
        idempotency_key=contract.get("idempotency_key") or "idempotency",
    ) if attempt_ref is None else attempt_ref

    entry = ExecutionAttemptPreflightStoreEntry(
        record_type=EXECUTION_ATTEMPT_STORE_RECORD_TYPE,
        schema_version=EXECUTION_ATTEMPT_STORE_SCHEMA_VERSION,
        attempt_ref=resolved_attempt_ref,
        attempt_mode=EXECUTION_ATTEMPT_MODE,
        mode=EXECUTION_ATTEMPT_STORE_MODE,
        status=status,
        target_ref=target_ref,
        dry_run_ref=deepcopy(contract.get("dry_run_ref") or {}),
        dry_run_store_ref=deepcopy(contract.get("dry_run_store_ref") or {}),
        dry_run_store_verification_ref=deepcopy(dry_run_store_verification or contract.get("dry_run_store_verification_ref") or {}),
        dry_run_store_checksum_ref=_dry_run_store_checksum_ref(contract, dry_run_store_verification),
        runtime_contract_ref=deepcopy(contract.get("runtime_contract_ref") or {}),
        execution_contract_ref=deepcopy(contract.get("execution_contract_ref") or {}),
        runtime_executor_contract_ref=deepcopy(contract.get("runtime_executor_contract_ref") or {}),
        runtime_preparation_ref=deepcopy(contract.get("runtime_preparation_ref") or {}),
        execution_runner_contract_ref=deepcopy(contract.get("execution_runner_contract_ref") or {}),
        dry_run_contract_ref=deepcopy(contract.get("dry_run_contract_ref") or {}),
        dry_run_store_contract_ref=deepcopy(contract.get("dry_run_store_contract_ref") or {}),
        execution_attempt_store_contract_ref=_contract_ref(contract),
        preflight_summary=deepcopy(preflight_summary if preflight_summary is not None else contract.get("preflight_summary") or {}),
        readiness_summary=deepcopy(readiness_summary if readiness_summary is not None else contract.get("readiness_summary") or {}),
        boundary_summary=deepcopy(boundary_summary if boundary_summary is not None else contract.get("boundary_summary") or {}),
        risk_summary=deepcopy(risk_summary if risk_summary is not None else contract.get("risk_summary") or {}),
        blocked_capabilities=deepcopy(blocked_capabilities if blocked_capabilities is not None else contract.get("blockers") or []),
        audit_refs=deepcopy(contract.get("audit_refs") or {}),
        observability_refs=deepcopy(contract.get("observability_refs") or {}),
        capability_policy_ref=deepcopy(contract.get("capability_policy_ref") or {}),
        correlation_id=contract.get("correlation_id"),
        idempotency_key=contract.get("idempotency_key"),
        created_at=created_at or contract.get("created_at") or datetime.now().isoformat(),
        entry_checksum=None,
        previous_entry_checksum=previous_entry_checksum,
        evidence=deepcopy(evidence if evidence is not None else {"contract_evidence": contract.get("evidence") or []}),
        warnings=deepcopy(warnings if warnings is not None else contract.get("warnings") or []),
        blockers=deepcopy(blockers if blockers is not None else []),
    ).to_dict()
    _validate_entry_dict(entry, validation_blockers)
    _validate_payload_boundary(entry, validation_blockers)
    if validation_blockers:
        raise ValueError("; ".join(blocker["code"] for blocker in validation_blockers))
    entry["entry_checksum"] = compute_execution_attempt_entry_checksum(entry)
    validate_execution_attempt_store_entry(entry)
    return entry


def append_execution_attempt_preflight(
    *,
    execution_attempt_store_contract: dict[str, Any] | None,
    dry_run_store_verification: dict[str, Any] | None,
    store_path: str | Path,
    attempt_ref: str | None = None,
    status: str = "preflight_passed",
    allow_external_test_path: bool = False,
    **entry_overrides: Any,
) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path)
    _validate_contract(execution_attempt_store_contract, blockers)
    _validate_dry_run_store_verification(dry_run_store_verification, blockers, execution_attempt_store_contract or {})
    if attempt_ref is not None:
        _validate_attempt_ref(attempt_ref, blockers)
    if status in BLOCKED_LIFECYCLE_STATUSES:
        _block(blockers, f"{status}_status_not_allowed", f"{status} no permitido")
    elif status not in ALLOWED_APPEND_STATUSES:
        _block(blockers, "invalid_status", f"status invalido: {status}")
    _validate_payload_boundary(entry_overrides, blockers)
    if blockers:
        return _operation_result("blocked", "append", attempt_ref, path, blockers=blockers)

    verification = verify_execution_attempt_store(path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("blocked", "append", attempt_ref, path, blockers=verification["blockers"])
    previous_checksum = _last_entry_checksum(verification.get("entries") or [])

    try:
        entry = build_execution_attempt_preflight_entry(
            execution_attempt_store_contract=execution_attempt_store_contract or {},
            dry_run_store_verification=dry_run_store_verification or {},
            attempt_ref=attempt_ref,
            status=status,
            previous_entry_checksum=previous_checksum,
            **entry_overrides,
        )
    except ValueError as exc:
        return _operation_result("blocked", "append", attempt_ref, path, blockers=[_blocker("invalid_execution_attempt_store_entry", str(exc))])

    replay = replay_execution_attempt_preflight_idempotency(path, entry, allow_external_test_path=allow_external_test_path)
    if replay["status"] == "noop_idempotent":
        return _operation_result(
            "noop_idempotent",
            "append",
            entry["attempt_ref"],
            path,
            entry_checksum=replay["entry_checksum"],
            previous_entry_checksum=replay["previous_entry_checksum"],
            idempotency_status="noop_idempotent",
            written=False,
            verified=True,
            evidence=replay["evidence"],
            entry=replay.get("entry"),
        )
    if replay["status"] == "blocked":
        return _operation_result("blocked", "append", entry["attempt_ref"], path, blockers=replay["blockers"], idempotency_status="blocked_conflict")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonicalize_execution_attempt_store_entry(entry) + "\n")
    return _operation_result(
        "appended",
        "append",
        entry["attempt_ref"],
        path,
        entry_checksum=entry["entry_checksum"],
        previous_entry_checksum=entry["previous_entry_checksum"],
        idempotency_status="appended",
        written=True,
        verified=True,
        evidence=[{"evidence_id": "execution_attempt_preflight_append_only_jsonl", "line_written": True}],
        entry=entry,
    )


def get_execution_attempt_preflight(
    *,
    attempt_ref: str,
    store_path: str | Path,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    verification = verify_execution_attempt_store(store_path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("failed", "get", attempt_ref, Path(store_path), blockers=verification["blockers"], read_only=True)
    for entry in verification["entries"]:
        if entry.get("attempt_ref") == attempt_ref:
            return _operation_result(
                "found",
                "get",
                attempt_ref,
                Path(store_path),
                entry_checksum=entry.get("entry_checksum"),
                previous_entry_checksum=entry.get("previous_entry_checksum"),
                read_only=True,
                verified=True,
                entry=entry,
            )
    return _operation_result("not_found", "get", attempt_ref, Path(store_path), read_only=True, verified=True)


def list_execution_attempt_preflights(
    *,
    store_path: str | Path,
    target_type: str | None = None,
    target_id: str | None = None,
    correlation_id: str | None = None,
    status: str | None = None,
    attempt_mode: str | None = None,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    verification = verify_execution_attempt_store(store_path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("failed", "list", None, Path(store_path), blockers=verification["blockers"], read_only=True)
    entries = []
    for entry in verification["entries"]:
        target_ref = entry.get("target_ref") or {}
        if target_type is not None and target_ref.get("target_type") != target_type:
            continue
        if target_id is not None and target_ref.get("target_id") != target_id:
            continue
        if correlation_id is not None and entry.get("correlation_id") != correlation_id:
            continue
        if status is not None and entry.get("status") != status:
            continue
        if attempt_mode is not None and entry.get("attempt_mode") != attempt_mode:
            continue
        entries.append(entry)
    return _operation_result("found", "list", None, Path(store_path), read_only=True, verified=True, entries=entries)


def verify_execution_attempt_store(
    store_path: str | Path,
    *,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path)
    if blockers:
        return _operation_result("failed", "verify", None, path, blockers=blockers, read_only=True)
    if not path.exists():
        return _operation_result("verified", "verify", None, path, read_only=True, verified=True, entries=[], warnings=["execution_attempt_store_missing_empty"])

    entries: list[dict[str, Any]] = []
    previous_checksum: str | None = None
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, start=1):
            raw = line.rstrip("\n")
            if not raw:
                _block(blockers, "corrupt_json_line", f"linea vacia: {index}")
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as exc:
                _block(blockers, "corrupt_json_line", f"linea {index}: {exc.msg}")
                continue
            try:
                validate_execution_attempt_store_entry(entry)
            except ValueError as exc:
                _block(blockers, "invalid_execution_attempt_store_entry", f"linea {index}: {exc}")
            expected = compute_execution_attempt_entry_checksum(entry)
            if entry.get("entry_checksum") != expected:
                _block(blockers, "checksum_mismatch", f"linea {index}: checksum invalido")
            if entry.get("previous_entry_checksum") != previous_checksum:
                _block(blockers, "previous_checksum_mismatch", f"linea {index}: previous_entry_checksum invalido")
            previous_checksum = entry.get("entry_checksum")
            entries.append(entry)
    return _operation_result(
        "verified" if not blockers else "failed",
        "verify",
        None,
        path,
        entry_checksum=previous_checksum,
        read_only=True,
        verified=not blockers,
        blockers=blockers,
        warnings=warnings,
        entries=entries,
    )


def replay_execution_attempt_preflight_idempotency(
    store_path: str | Path,
    entry: dict[str, Any],
    *,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    scope = _idempotency_scope(entry)
    blockers: list[dict[str, str]] = []
    if any(value in (None, "", {}, []) for value in scope):
        _block(blockers, "scope_missing", "idempotency scope incompleto")
        return _operation_result("blocked", "idempotency_replay", entry.get("attempt_ref"), Path(store_path), blockers=blockers)
    verification = verify_execution_attempt_store(store_path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("blocked", "idempotency_replay", entry.get("attempt_ref"), Path(store_path), blockers=verification["blockers"])
    for existing in verification.get("entries") or []:
        if _idempotency_scope(existing) == scope:
            if _entry_payload_without_chain(existing) == _entry_payload_without_chain(entry):
                return _operation_result(
                    "noop_idempotent",
                    "idempotency_replay",
                    entry.get("attempt_ref"),
                    Path(store_path),
                    entry_checksum=existing.get("entry_checksum"),
                    previous_entry_checksum=existing.get("previous_entry_checksum"),
                    read_only=True,
                    verified=True,
                    evidence=[{"evidence_id": "duplicate_same_scope_noop", "matched": True}],
                    entry=existing,
                )
            return _operation_result(
                "blocked",
                "idempotency_replay",
                entry.get("attempt_ref"),
                Path(store_path),
                blockers=[_blocker("duplicate_different_payload_conflict", "mismo scope con payload distinto")],
                read_only=True,
            )
    return _operation_result("not_found", "idempotency_replay", entry.get("attempt_ref"), Path(store_path), read_only=True, verified=True)


def canonicalize_execution_attempt_store_entry(entry: dict[str, Any]) -> str:
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_execution_attempt_entry_checksum(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("entry_checksum", None)
    canonical = canonicalize_execution_attempt_store_entry(payload)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def validate_execution_attempt_store_entry(entry: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    _validate_entry_dict(entry, blockers)
    _validate_payload_boundary(entry, blockers)
    if blockers:
        raise ValueError("; ".join(blocker["code"] for blocker in blockers))
    return deepcopy(entry)


def _validate_contract(contract: dict[str, Any] | None, blockers: list[dict[str, str]]) -> None:
    if contract is None:
        _block(blockers, "missing_execution_attempt_store_contract", "execution_attempt_store_contract requerido")
        return
    if contract.get("status") != "passed":
        _block(blockers, "execution_attempt_store_contract_not_passed", "execution_attempt_store_contract debe estar passed")
    if contract.get("verdict") != PASSED_CONTRACT_VERDICT:
        _block(blockers, "execution_attempt_store_contract_not_passed", "execution_attempt_store_contract verdict debe estar passed")
    if contract.get("attempt_mode") != EXECUTION_ATTEMPT_MODE:
        _block(blockers, "invalid_attempt_mode", "attempt_mode debe ser preflight_only")
    if contract.get("store_type") != "execution_attempt_store":
        _block(blockers, "invalid_store_type", "store_type debe ser execution_attempt_store")
    append_policy = contract.get("append_only_policy") or {}
    if append_policy.get("append_only") is not True:
        _block(blockers, "not_append_only", "append_only_policy.append_only debe ser true")
    for field_name, code in [
        ("overwrite_allowed", "overwrite_not_allowed"),
        ("update_allowed", "update_not_allowed"),
        ("delete_allowed", "delete_not_allowed"),
        ("truncate_allowed", "truncate_not_allowed"),
        ("replace_allowed", "replace_not_allowed"),
    ]:
        if append_policy.get(field_name) is True:
            _block(blockers, code, f"{field_name} debe ser false")
    _validate_payload_boundary(contract, blockers)


def _validate_dry_run_store_verification(verification: dict[str, Any] | None, blockers: list[dict[str, str]], contract: dict[str, Any]) -> None:
    if verification is None or verification == {}:
        _block(blockers, "missing_dry_run_store_verification", "dry_run_store verification requerida")
        return
    if verification.get("status") != "verified" or verification.get("verified") is not True:
        _block(blockers, "dry_run_store_not_verified", "dry_run_store debe estar verified")
    checksum_ref = _dry_run_store_checksum_ref(contract, verification)
    if not checksum_ref:
        _block(blockers, "dry_run_store_checksum_missing", "dry_run_store_checksum_ref requerido")
    verification_checksum = verification.get("entry_checksum") or verification.get("last_entry_checksum")
    if checksum_ref and verification_checksum and checksum_ref != verification_checksum:
        _block(blockers, "dry_run_store_checksum_mismatch", "checksum de dry_run_store no coincide")


def _validate_entry_dict(entry: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not isinstance(entry, dict):
        _block(blockers, "invalid_entry", "execution_attempt_store entry debe ser objeto")
        return
    required = [
        "record_type",
        "schema_version",
        "attempt_ref",
        "attempt_mode",
        "mode",
        "status",
        "target_ref",
        "dry_run_ref",
        "dry_run_store_ref",
        "dry_run_store_verification_ref",
        "dry_run_store_checksum_ref",
        "runtime_contract_ref",
        "execution_contract_ref",
        "runtime_executor_contract_ref",
        "runtime_preparation_ref",
        "execution_runner_contract_ref",
        "dry_run_contract_ref",
        "dry_run_store_contract_ref",
        "execution_attempt_store_contract_ref",
        "preflight_summary",
        "readiness_summary",
        "boundary_summary",
        "risk_summary",
        "audit_refs",
        "observability_refs",
        "capability_policy_ref",
        "correlation_id",
        "idempotency_key",
        "created_at",
        "evidence",
    ]
    for field_name in required:
        if entry.get(field_name) in (None, "", {}, []):
            _block(blockers, f"missing_{field_name}", f"{field_name} requerido")
    if entry.get("record_type") != EXECUTION_ATTEMPT_STORE_RECORD_TYPE:
        _block(blockers, "invalid_record_type", "record_type debe ser execution_attempt_preflight")
    if entry.get("schema_version") != EXECUTION_ATTEMPT_STORE_SCHEMA_VERSION:
        _block(blockers, "invalid_schema_version", "schema_version invalida")
    if entry.get("attempt_mode") != EXECUTION_ATTEMPT_MODE:
        _block(blockers, "invalid_attempt_mode", "attempt_mode debe ser preflight_only")
    if entry.get("mode") != EXECUTION_ATTEMPT_STORE_MODE:
        _block(blockers, "invalid_mode", "mode debe ser execution_attempt_store_preflight_only")
    _validate_attempt_ref(entry.get("attempt_ref"), blockers)
    status = entry.get("status")
    if status in BLOCKED_LIFECYCLE_STATUSES:
        _block(blockers, f"{status}_status_not_allowed", f"{status} no permitido")
    elif status not in ALLOWED_APPEND_STATUSES:
        _block(blockers, "invalid_status", f"status invalido: {status}")
    checksum = entry.get("entry_checksum")
    if checksum is not None and not str(checksum).startswith("sha256:"):
        _block(blockers, "checksum_invalid", "entry_checksum debe ser sha256")
    for list_field in ["blocked_capabilities", "warnings", "blockers"]:
        if not isinstance(entry.get(list_field), list):
            _block(blockers, f"invalid_{list_field}", f"{list_field} debe ser lista")
    if entry.get("dry_run_ref", {}).get("mode") != "dry_run_result_only":
        _block(blockers, "dry_run_result_not_result_only", "dry_run_ref debe ser result-only")
    if entry.get("dry_run_ref", {}).get("status") != "simulated":
        _block(blockers, "dry_run_result_not_simulated", "dry_run_ref debe estar simulated")


def _validate_attempt_ref(attempt_ref: Any, blockers: list[dict[str, str]]) -> None:
    if not isinstance(attempt_ref, str) or not attempt_ref:
        _block(blockers, "missing_attempt_ref", "attempt_ref requerido")
        return
    if not attempt_ref.startswith("preflight:"):
        _block(blockers, "invalid_attempt_ref", "attempt_ref debe empezar con preflight:")
    if attempt_ref in {"execution_attempt_id", "attempt_id"}:
        _block(blockers, "attempt_ref_materialized_as_execution_attempt_id", "attempt_ref no debe ser execution_attempt_id")


def _validate_payload_boundary(payload: Any, blockers: list[dict[str, str]], path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_NESTED_KEYS and value not in (None, "", {}, []):
                _block(blockers, f"{key}_not_allowed", f"{key} no permitido en {path}")
            _validate_payload_boundary(value, blockers, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _validate_payload_boundary(value, blockers, f"{path}[{index}]")


def _validate_store_path(path: Path, blockers: list[dict[str, str]], *, allow_external_test_path: bool) -> None:
    if path.suffix != ".jsonl":
        _block(blockers, "invalid_storage_format", "execution_attempt_store debe usar .jsonl")
    parts = {part.lower() for part in path.parts}
    if parts & FORBIDDEN_PATH_PARTS:
        _block(blockers, "invalid_storage_path", "ruta bloqueada para execution_attempt_store preflight-only")
    try:
        resolved = path.resolve()
        root = Path.cwd().resolve()
        temp_root = Path(tempfile.gettempdir()).resolve()
        inside_project = resolved == root or root in resolved.parents
        inside_temp = resolved == temp_root or temp_root in resolved.parents
        if not inside_project and not allow_external_test_path and not inside_temp:
            _block(blockers, "invalid_storage_path", "ruta fuera del proyecto no permitida")
    except OSError as exc:
        _block(blockers, "invalid_storage_path", f"ruta invalida: {exc}")


def _dry_run_store_checksum_ref(contract: dict[str, Any], verification: dict[str, Any] | None) -> str | None:
    return (
        (contract.get("checksum_summary") or {}).get("dry_run_store_checksum_ref")
        or (verification or {}).get("entry_checksum")
        or (verification or {}).get("last_entry_checksum")
    )


def _contract_ref(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": contract.get("contract_id"),
        "status": contract.get("status"),
        "verdict": contract.get("verdict"),
        "target_type": (contract.get("target_ref") or {}).get("target_type"),
        "target_id": (contract.get("target_ref") or {}).get("target_id"),
        "correlation_id": contract.get("correlation_id"),
        "idempotency_key": contract.get("idempotency_key"),
    }


def _idempotency_scope(entry: dict[str, Any]) -> tuple[Any, ...]:
    target_ref = entry.get("target_ref") or {}
    dry_run_ref = entry.get("dry_run_ref") or {}
    contract_ref = entry.get("execution_attempt_store_contract_ref") or {}
    return (
        target_ref.get("target_type"),
        target_ref.get("target_id"),
        entry.get("attempt_ref"),
        entry.get("correlation_id"),
        entry.get("idempotency_key"),
        dry_run_ref.get("dry_run_id"),
        entry.get("dry_run_store_checksum_ref"),
        contract_ref.get("contract_id") or contract_ref,
    )


def _entry_payload_without_chain(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("entry_checksum", None)
    payload.pop("previous_entry_checksum", None)
    return payload


def _last_entry_checksum(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    return entries[-1].get("entry_checksum")


def _operation_result(
    status: str,
    operation: str,
    attempt_ref: str | None,
    store_path: Path,
    *,
    entry_checksum: str | None = None,
    previous_entry_checksum: str | None = None,
    idempotency_status: str | None = None,
    written: bool = False,
    read_only: bool = False,
    verified: bool = False,
    blockers: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    entry: dict[str, Any] | None = None,
    entries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return ExecutionAttemptStoreOperationResult(
        status=status,
        operation=operation,
        attempt_ref=attempt_ref,
        store_path=str(store_path),
        entry_checksum=entry_checksum,
        previous_entry_checksum=previous_entry_checksum,
        idempotency_status=idempotency_status,
        written=written,
        read_only=read_only,
        verified=verified,
        blockers=blockers or [],
        warnings=warnings or [],
        evidence=evidence or [],
        entry=entry,
        entries=entries,
    ).to_dict()


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = _blocker(code, message)
    if blocker not in blockers:
        blockers.append(blocker)


def _blocker(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message, "severity": "error"}
