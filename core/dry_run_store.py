"""Dry-run append-only store.

Persiste DryRunResult result-only en JSONL canonico. No crea execution attempts,
no ejecuta agentes/equipos y no escribe payloads reales.
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

from core.dry_run_store_contract import FORBIDDEN_ENTRY_FIELDS
from core.execution_runner import RESULT_ONLY_MODE


DRY_RUN_STORE_SCHEMA_VERSION = "1.0"
DRY_RUN_STORE_RECORD_TYPE = "dry_run_result"
RECOMMENDED_DRY_RUN_STORE_PATH = Path("runtime/dry_runs/dry_run_store.jsonl")
ALLOWED_APPEND_STATUSES = {"simulated", "prepared", "aborted", "rolled_back", "noop_idempotent", "blocked", "failed"}
FORBIDDEN_PATH_PARTS = {
    "execution_attempt_store",
    "execution_attempts",
    "scheduler",
    "worker_queue",
    "memoria_agentes",
    "memory",
    "ui",
    "integrations",
}
FORBIDDEN_NESTED_KEYS = set(FORBIDDEN_ENTRY_FIELDS)


@dataclass(frozen=True)
class DryRunStoreOperationResult:
    status: str
    operation: str
    dry_run_id: str | None
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


def build_dry_run_store_entry(
    dry_run_result: dict[str, Any],
    *,
    dry_run_store_contract: dict[str, Any],
    previous_entry_checksum: str | None = None,
) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    _validate_contract(dry_run_store_contract, blockers)
    _validate_dry_run_result(dry_run_result, blockers)
    _validate_payload_boundary(dry_run_result, blockers)
    if blockers:
        raise ValueError("; ".join(blocker["code"] for blocker in blockers))

    entry = {
        "record_type": DRY_RUN_STORE_RECORD_TYPE,
        "schema_version": DRY_RUN_STORE_SCHEMA_VERSION,
        "dry_run_id": dry_run_result.get("dry_run_id"),
        "status": dry_run_result.get("status"),
        "mode": dry_run_result.get("mode"),
        "target_ref": deepcopy(dry_run_result.get("target_ref") or {}),
        "contract_refs": deepcopy(dry_run_result.get("contract_refs") or {}),
        "runtime_preparation_ref": deepcopy(dry_run_result.get("runtime_preparation_ref") or {}),
        "preparation_id": dry_run_result.get("preparation_id"),
        "dry_run_contract_ref": deepcopy(dry_run_result.get("dry_run_contract_ref") or {}),
        "execution_runner_contract_ref": deepcopy(dry_run_result.get("execution_runner_contract_ref") or {}),
        "simulated_plan": deepcopy(dry_run_result.get("simulated_plan") or {}),
        "simulated_steps": deepcopy(dry_run_result.get("simulated_steps") or []),
        "input_expectations": deepcopy(dry_run_result.get("input_expectations") or {}),
        "output_expectations": deepcopy(dry_run_result.get("output_expectations") or {}),
        "risk_summary": deepcopy(dry_run_result.get("risk_summary") or {}),
        "boundary_summary": deepcopy(dry_run_result.get("boundary_summary") or {}),
        "readiness_summary": deepcopy(dry_run_result.get("readiness_summary") or {}),
        "blocked_side_effects": deepcopy(dry_run_result.get("blocked_side_effects") or []),
        "audit_events": deepcopy(dry_run_result.get("audit_events") or []),
        "observability_events": deepcopy(dry_run_result.get("observability_events") or []),
        "audit_refs": {"audit_store_path": dry_run_result.get("audit_store_path")},
        "observability_refs": {"correlation_id": dry_run_result.get("correlation_id")},
        "correlation_id": dry_run_result.get("correlation_id"),
        "idempotency_key": dry_run_result.get("idempotency_key"),
        "created_at": dry_run_result.get("created_at") or datetime.now().isoformat(),
        "entry_checksum": None,
        "previous_entry_checksum": previous_entry_checksum,
        "evidence": deepcopy(dry_run_result.get("evidence") or []),
        "warnings": deepcopy(dry_run_result.get("warnings") or []),
        "blockers": deepcopy(dry_run_result.get("blockers") or []),
        "lineage_ref": deepcopy(dry_run_result.get("lineage_ref") or {}),
    }
    entry["entry_checksum"] = compute_dry_run_entry_checksum(entry)
    validate_dry_run_store_entry(entry)
    return entry


def append_dry_run_result(
    *,
    dry_run_result: dict[str, Any] | None,
    dry_run_store_contract: dict[str, Any] | None,
    store_path: str | Path,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    path = Path(store_path)
    blockers: list[dict[str, str]] = []
    _validate_store_path(path, blockers, allow_external_test_path=allow_external_test_path)
    _validate_contract(dry_run_store_contract, blockers)
    if dry_run_result is None:
        _block(blockers, "missing_dry_run_result", "dry_run_result requerido")
        result = {}
    else:
        result = dry_run_result
        _validate_dry_run_result(result, blockers)
        _validate_payload_boundary(result, blockers)
    if blockers:
        return _operation_result("blocked", "append", result.get("dry_run_id"), path, blockers=blockers)

    verification = verify_dry_run_store(path)
    if verification["status"] == "failed":
        return _operation_result("blocked", "append", result.get("dry_run_id"), path, blockers=verification["blockers"])

    previous_checksum = _last_entry_checksum(verification.get("entries") or [])
    try:
        entry = build_dry_run_store_entry(result, dry_run_store_contract=dry_run_store_contract or {}, previous_entry_checksum=previous_checksum)
    except ValueError as exc:
        return _operation_result("blocked", "append", result.get("dry_run_id"), path, blockers=[_blocker("invalid_dry_run_store_entry", str(exc))])

    replay = replay_dry_run_idempotency(path, entry, allow_external_test_path=allow_external_test_path)
    if replay["status"] == "noop_idempotent":
        return _operation_result(
            "noop_idempotent",
            "append",
            entry["dry_run_id"],
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
        return _operation_result("blocked", "append", entry["dry_run_id"], path, blockers=replay["blockers"], idempotency_status="blocked_conflict")

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonicalize_dry_run_store_entry(entry) + "\n")
    return _operation_result(
        "appended",
        "append",
        entry["dry_run_id"],
        path,
        entry_checksum=entry["entry_checksum"],
        previous_entry_checksum=entry["previous_entry_checksum"],
        idempotency_status="appended",
        written=True,
        verified=True,
        evidence=[{"evidence_id": "append_only_jsonl", "line_written": True}],
        entry=entry,
    )


def get_dry_run_result(
    *,
    dry_run_id: str,
    store_path: str | Path,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    verification = verify_dry_run_store(store_path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("failed", "get", dry_run_id, Path(store_path), blockers=verification["blockers"], read_only=True)
    for entry in verification["entries"]:
        if entry.get("dry_run_id") == dry_run_id:
            return _operation_result(
                "found",
                "get",
                dry_run_id,
                Path(store_path),
                entry_checksum=entry.get("entry_checksum"),
                previous_entry_checksum=entry.get("previous_entry_checksum"),
                read_only=True,
                verified=True,
                entry=entry,
            )
    return _operation_result("not_found", "get", dry_run_id, Path(store_path), read_only=True, verified=True)


def list_dry_run_results(
    *,
    store_path: str | Path,
    target_type: str | None = None,
    target_id: str | None = None,
    correlation_id: str | None = None,
    status: str | None = None,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    verification = verify_dry_run_store(store_path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("failed", "list", None, Path(store_path), blockers=verification["blockers"], read_only=True)
    entries = []
    for entry in verification["entries"]:
        ref = entry.get("target_ref") or {}
        if target_type is not None and ref.get("target_type") != target_type:
            continue
        if target_id is not None and ref.get("target_id") != target_id:
            continue
        if correlation_id is not None and entry.get("correlation_id") != correlation_id:
            continue
        if status is not None and entry.get("status") != status:
            continue
        entries.append(entry)
    return _operation_result("found", "list", None, Path(store_path), read_only=True, verified=True, entries=entries)


def verify_dry_run_store(
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
        return _operation_result("verified", "verify", None, path, read_only=True, verified=True, entries=[], warnings=["dry_run_store_missing_empty"])

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
                validate_dry_run_store_entry(entry)
            except ValueError as exc:
                _block(blockers, "invalid_dry_run_store_entry", f"linea {index}: {exc}")
            expected = compute_dry_run_entry_checksum(entry)
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


def replay_dry_run_idempotency(
    store_path: str | Path,
    entry: dict[str, Any],
    *,
    allow_external_test_path: bool = False,
) -> dict[str, Any]:
    scope = _idempotency_scope(entry)
    blockers: list[dict[str, str]] = []
    if any(value in (None, "", {}, []) for value in scope):
        _block(blockers, "scope_missing", "idempotency scope incompleto")
        return _operation_result("blocked", "idempotency_replay", entry.get("dry_run_id"), Path(store_path), blockers=blockers)
    verification = verify_dry_run_store(store_path, allow_external_test_path=allow_external_test_path)
    if verification["status"] == "failed":
        return _operation_result("blocked", "idempotency_replay", entry.get("dry_run_id"), Path(store_path), blockers=verification["blockers"])
    for existing in verification.get("entries") or []:
        if _idempotency_scope(existing) == scope:
            if _entry_payload_without_chain(existing) == _entry_payload_without_chain(entry):
                return _operation_result(
                    "noop_idempotent",
                    "idempotency_replay",
                    entry.get("dry_run_id"),
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
                entry.get("dry_run_id"),
                Path(store_path),
                blockers=[_blocker("duplicate_different_payload_conflict", "mismo scope con payload distinto")],
                read_only=True,
            )
    return _operation_result("not_found", "idempotency_replay", entry.get("dry_run_id"), Path(store_path), read_only=True, verified=True)


def canonicalize_dry_run_store_entry(entry: dict[str, Any]) -> str:
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_dry_run_entry_checksum(entry: dict[str, Any]) -> str:
    payload = deepcopy(entry)
    payload.pop("entry_checksum", None)
    canonical = canonicalize_dry_run_store_entry(payload)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def validate_dry_run_store_entry(entry: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    if not isinstance(entry, dict):
        raise ValueError("dry_run_store_entry debe ser objeto")
    if entry.get("record_type") != DRY_RUN_STORE_RECORD_TYPE:
        _block(blockers, "invalid_record_type", "record_type debe ser dry_run_result")
    if entry.get("schema_version") != DRY_RUN_STORE_SCHEMA_VERSION:
        _block(blockers, "invalid_schema_version", "schema_version invalida")
    for field_name in [
        "dry_run_id",
        "status",
        "mode",
        "target_ref",
        "contract_refs",
        "runtime_preparation_ref",
        "dry_run_contract_ref",
        "execution_runner_contract_ref",
        "correlation_id",
        "idempotency_key",
        "created_at",
        "entry_checksum",
    ]:
        if entry.get(field_name) in (None, "", {}, []):
            _block(blockers, f"missing_{field_name}", f"{field_name} requerido")
    if entry.get("mode") != RESULT_ONLY_MODE:
        _block(blockers, "dry_run_result_not_result_only", "mode debe ser dry_run_result_only")
    if entry.get("status") not in ALLOWED_APPEND_STATUSES:
        _block(blockers, "invalid_dry_run_status", f"status invalido: {entry.get('status')}")
    if not str(entry.get("entry_checksum", "")).startswith("sha256:"):
        _block(blockers, "missing_checksum", "entry_checksum sha256 requerido")
    _validate_payload_boundary(entry, blockers)
    if blockers:
        raise ValueError("; ".join(blocker["code"] for blocker in blockers))
    return deepcopy(entry)


def _validate_contract(contract: dict[str, Any] | None, blockers: list[dict[str, str]]) -> None:
    if contract is None:
        _block(blockers, "missing_dry_run_store_contract", "dry_run_store_contract requerido")
        return
    if contract.get("status") != "passed":
        _block(blockers, "dry_run_store_contract_not_passed", "dry_run_store_contract debe estar passed")
    if contract.get("mode") != "dry_run_store_contract_only":
        _block(blockers, "invalid_contract_mode", "dry_run_store_contract mode invalido")
    if contract.get("storage_format") != "append_only_jsonl":
        _block(blockers, "invalid_storage_format", "storage_format debe ser append_only_jsonl")
    if contract.get("append_only") is not True:
        _block(blockers, "storage_not_append_only", "append_only requerido")


def _validate_dry_run_result(result: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    if not isinstance(result, dict):
        _block(blockers, "missing_dry_run_result", "dry_run_result debe ser objeto")
        return
    if result.get("mode") != RESULT_ONLY_MODE:
        _block(blockers, "dry_run_result_not_result_only", "dry_run_result debe ser result-only")
    if result.get("status") not in ALLOWED_APPEND_STATUSES:
        _block(blockers, "invalid_dry_run_status", f"status invalido: {result.get('status')}")
    for field_name in ["dry_run_id", "target_ref", "correlation_id", "idempotency_key", "boundary_summary", "readiness_summary"]:
        if result.get(field_name) in (None, "", {}, []):
            _block(blockers, f"missing_{field_name}", f"{field_name} requerido")


def _validate_payload_boundary(payload: Any, blockers: list[dict[str, str]], path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_NESTED_KEYS and value not in (None, "", {}, []):
                _block(blockers, FORBIDDEN_ENTRY_FIELDS[key], f"{key} no permitido en {path}")
            _validate_payload_boundary(value, blockers, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _validate_payload_boundary(value, blockers, f"{path}[{index}]")


def _validate_store_path(path: Path, blockers: list[dict[str, str]], *, allow_external_test_path: bool) -> None:
    if path.suffix != ".jsonl":
        _block(blockers, "invalid_storage_format", "dry_run_store debe usar .jsonl")
    parts = {part.lower() for part in path.parts}
    if parts & FORBIDDEN_PATH_PARTS:
        _block(blockers, "invalid_storage_path", "ruta bloqueada para dry_run_store")
    if "execution_attempt" in path.as_posix().lower():
        _block(blockers, "execution_attempt_store_not_allowed", "ruta de execution_attempt bloqueada")
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


def _idempotency_scope(entry: dict[str, Any]) -> tuple[Any, ...]:
    target_ref = entry.get("target_ref") or {}
    dry_run_contract_ref = entry.get("dry_run_contract_ref") or {}
    return (
        target_ref.get("target_type") or entry.get("target_type"),
        target_ref.get("target_id") or entry.get("target_id"),
        entry.get("correlation_id"),
        entry.get("idempotency_key"),
        entry.get("dry_run_id"),
        dry_run_contract_ref.get("contract_id") or dry_run_contract_ref,
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
    dry_run_id: str | None,
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
    return DryRunStoreOperationResult(
        status=status,
        operation=operation,
        dry_run_id=dry_run_id,
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
