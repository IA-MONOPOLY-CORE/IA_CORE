"""Schema de persistencia local segura para audit/observability."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any


AUDIT_PERSISTENCE_SCHEMA_VERSION = "1.0"
ALLOWED_STORE_MODES = {"local_safe", "memory_only_test", "future_external_store"}
ALLOWED_WRITE_MODES = {"append_only"}
REQUIRED_FIELDS = {
    "schema_version",
    "audit_store_id",
    "store_mode",
    "root_path",
    "write_mode",
    "append_only",
    "immutable_records",
    "checksum",
    "event_count",
    "created_at",
    "updated_at",
}


def build_audit_store_contract(
    *,
    audit_store_id: str,
    root_path: str,
    store_mode: str = "local_safe",
    write_mode: str = "append_only",
    append_only: bool = True,
    immutable_records: bool = True,
    checksum: str,
    event_count: int = 0,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    now = datetime.now().isoformat()
    payload = {
        "schema_version": AUDIT_PERSISTENCE_SCHEMA_VERSION,
        "audit_store_id": audit_store_id,
        "store_mode": store_mode,
        "root_path": root_path,
        "write_mode": write_mode,
        "append_only": append_only,
        "immutable_records": immutable_records,
        "checksum": checksum,
        "event_count": event_count,
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }
    return validate_audit_store_contract(payload)


def validate_audit_store_contract(store: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(store, dict):
        raise ValueError("audit_store debe ser un objeto")
    missing = REQUIRED_FIELDS - set(store)
    if missing:
        raise ValueError(f"audit_store incompleto: {', '.join(sorted(missing))}")
    if store.get("schema_version") != AUDIT_PERSISTENCE_SCHEMA_VERSION:
        raise ValueError("schema_version de audit_store invalida")
    _validate_id(store.get("audit_store_id"), "audit_store_id")
    if store.get("store_mode") not in ALLOWED_STORE_MODES:
        raise ValueError(f"store_mode invalido: {store.get('store_mode')}")
    _validate_non_empty_text(store.get("root_path"), "root_path")
    if store.get("write_mode") not in ALLOWED_WRITE_MODES:
        raise ValueError("audit_store requiere write_mode append_only")
    if store.get("append_only") is not True:
        raise ValueError("audit_store requiere append_only=true")
    if store.get("immutable_records") is not True:
        raise ValueError("audit_store requiere immutable_records=true")
    _validate_non_empty_text(store.get("checksum"), "checksum")
    if not isinstance(store.get("event_count"), int) or store["event_count"] < 0:
        raise ValueError("event_count debe ser entero no negativo")
    for field in ["created_at", "updated_at"]:
        _validate_non_empty_text(store.get(field), field)
    _ensure_json_serializable(store)
    return deepcopy(store)


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
        raise ValueError("audit_store debe ser serializable como JSON") from exc
