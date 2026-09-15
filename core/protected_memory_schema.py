"""Versioned, bounded projections for the protected memory route."""

from __future__ import annotations

import math
from numbers import Real
from typing import Any, Mapping


PROTECTED_MEMORY_CONTRACT_VERSION = "protected_memory.v1"
PROTECTED_MEMORY_EXTERNAL_POLICY = "DEFAULT_DENIED"
MAX_AUDIT_RECORDS = 25
MEMORY_HISTORY_KEY = "orchestration_history"

COMMON_KEYS = frozenset(
    {
        "contract_version",
        "view",
        "scope",
        "status",
        "external_access",
        "content_exposed",
        "bounded",
        "data",
    }
)
METADATA_DATA_KEYS = frozenset(
    {"memory_state", "record_count", "content_classes", "projection"}
)
AUDIT_DATA_KEYS = frozenset({"record_count", "records", "projection"})
AUDIT_RECORD_KEYS = frozenset({"status", "started_at", "duration_ms"})


class ProtectedMemoryContractError(ValueError):
    """Raised when a response falls outside the explicit contract."""


def _bounded_text(value: Any, *, max_length: int = 80) -> str | None:
    if not isinstance(value, str) or not value or value != value.strip():
        return None
    if len(value) > max_length or "\r" in value or "\n" in value:
        return None
    return value


def _bounded_number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, Real):
        return None
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < 0 or numeric > 86_400_000:
        return None
    return int(numeric) if numeric.is_integer() else round(numeric, 3)


def _safe_status(entry: Mapping[str, Any]) -> str:
    if entry.get("success") is True:
        return "success"
    if entry.get("success") is False:
        return "failed"
    return "unknown"


def _read_history(memory: Any) -> list[Mapping[str, Any]]:
    history = memory.get(MEMORY_HISTORY_KEY, [])
    if not isinstance(history, list):
        return []
    return [entry for entry in history if isinstance(entry, Mapping)]


def _memory_state(memory: Any) -> str:
    return "available" if memory.running else "not_available"


def build_metadata_payload(memory: Any) -> dict[str, Any]:
    history = _read_history(memory)
    payload = {
        "contract_version": PROTECTED_MEMORY_CONTRACT_VERSION,
        "view": "metadata",
        "scope": "platform",
        "status": "available",
        "external_access": {
            "policy": PROTECTED_MEMORY_EXTERNAL_POLICY,
            "enabled": False,
        },
        "content_exposed": False,
        "bounded": True,
        "data": {
            "memory_state": _memory_state(memory),
            "record_count": min(len(history), 1_000_000),
            "content_classes": [
                "PLATFORM_OPERATIONAL_METADATA",
                "SANITIZED_AUDIT_EVIDENCE",
                "TENANT_CONFIDENTIAL_MEMORY",
                "GLOBAL_INHERITABLE_LEARNING",
                "UNKNOWN_UNCLASSIFIED_MEMORY",
            ],
            "projection": "allowlist_first",
        },
    }
    return validate_protected_memory_payload(payload, expected_view="metadata")


def build_audit_payload(memory: Any, *, limit: int) -> dict[str, Any]:
    history = _read_history(memory)
    records: list[dict[str, Any]] = []
    for entry in reversed(history[-limit:]):
        record: dict[str, Any] = {"status": _safe_status(entry)}
        started_at = _bounded_text(entry.get("started_at"), max_length=64)
        duration_ms = _bounded_number(entry.get("duration_ms"))
        if started_at is not None:
            record["started_at"] = started_at
        if duration_ms is not None:
            record["duration_ms"] = duration_ms
        records.append(record)

    payload = {
        "contract_version": PROTECTED_MEMORY_CONTRACT_VERSION,
        "view": "audit",
        "scope": "platform",
        "status": "available",
        "external_access": {
            "policy": PROTECTED_MEMORY_EXTERNAL_POLICY,
            "enabled": False,
        },
        "content_exposed": False,
        "bounded": True,
        "data": {
            "record_count": len(history),
            "records": records,
            "projection": "allowlist_first_sanitized",
        },
    }
    return validate_protected_memory_payload(payload, expected_view="audit")


def validate_protected_memory_payload(
    payload: Mapping[str, Any],
    *,
    expected_view: str,
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ProtectedMemoryContractError("payload must be an object")
    if set(payload) != set(COMMON_KEYS):
        raise ProtectedMemoryContractError("payload fields are not allowlisted")
    if payload["contract_version"] != PROTECTED_MEMORY_CONTRACT_VERSION:
        raise ProtectedMemoryContractError("unsupported contract version")
    if payload["view"] != expected_view or payload["scope"] != "platform":
        raise ProtectedMemoryContractError("invalid view or scope")
    if payload["status"] not in {"available", "not_available", "degraded"}:
        raise ProtectedMemoryContractError("invalid status")
    if payload["external_access"] != {
        "policy": PROTECTED_MEMORY_EXTERNAL_POLICY,
        "enabled": False,
    }:
        raise ProtectedMemoryContractError("external access must remain denied")
    if payload["content_exposed"] is not False or payload["bounded"] is not True:
        raise ProtectedMemoryContractError("unsafe exposure markers")
    data = payload["data"]
    allowed_data_keys = METADATA_DATA_KEYS if expected_view == "metadata" else AUDIT_DATA_KEYS
    if not isinstance(data, Mapping) or not set(data).issubset(allowed_data_keys):
        raise ProtectedMemoryContractError("data fields are not allowlisted")
    if expected_view == "metadata":
        if not isinstance(data.get("memory_state"), str):
            raise ProtectedMemoryContractError("invalid memory state")
        if type(data.get("record_count")) is not int or data["record_count"] < 0:
            raise ProtectedMemoryContractError("invalid record count")
        if not isinstance(data.get("content_classes"), list):
            raise ProtectedMemoryContractError("invalid content classes")
    else:
        if type(data.get("record_count")) is not int or data["record_count"] < 0:
            raise ProtectedMemoryContractError("invalid record count")
        records = data.get("records")
        if not isinstance(records, list) or len(records) > MAX_AUDIT_RECORDS:
            raise ProtectedMemoryContractError("audit response is not bounded")
        for record in records:
            if not isinstance(record, Mapping) or not set(record).issubset(AUDIT_RECORD_KEYS):
                raise ProtectedMemoryContractError("audit fields are not allowlisted")
            if record.get("status") not in {"success", "failed", "unknown"}:
                raise ProtectedMemoryContractError("invalid audit status")
    return dict(payload)
