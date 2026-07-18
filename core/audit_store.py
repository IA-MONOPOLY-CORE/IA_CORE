"""Audit store local append-only verificable para eventos observability."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from core.audit_persistence_schema import build_audit_store_contract, validate_audit_store_contract
from core.observability import summarize_observability_events
from core.observability_schema import validate_observability_event


MANIFEST_NAME = "store_manifest.json"
EVENTS_DIR_NAME = "events"


def create_audit_store(root_path: str | Path, *, audit_store_id: str) -> dict[str, Any]:
    """Crea o valida un store local; no borra ni reescribe eventos."""
    root = Path(root_path)
    events_dir = root / EVENTS_DIR_NAME
    manifest_path = root / MANIFEST_NAME
    root.mkdir(parents=True, exist_ok=True)
    events_dir.mkdir(exist_ok=True)
    if manifest_path.exists():
        manifest = _read_json(manifest_path)
        return validate_audit_store_contract(manifest)
    manifest = build_audit_store_contract(
        audit_store_id=audit_store_id,
        store_mode="local_safe",
        root_path=str(root),
        write_mode="append_only",
        append_only=True,
        immutable_records=True,
        checksum=_manifest_checksum(0, None),
        event_count=0,
        created_at=_now(),
        updated_at=_now(),
    )
    manifest.update(
        {
            "first_event_at": None,
            "last_event_at": None,
            "last_event_checksum": None,
        }
    )
    _write_json_exclusive(manifest_path, manifest)
    return validate_audit_store_contract(manifest)


def append_audit_event(root_path: str | Path, event: dict[str, Any]) -> dict[str, Any]:
    """Agrega un evento validado sin sobrescribir archivos existentes."""
    validated_event = validate_observability_event(event)
    root = Path(root_path)
    manifest_path = root / MANIFEST_NAME
    events_dir = root / EVENTS_DIR_NAME
    manifest = validate_audit_store_contract(_read_json(manifest_path))
    sequence_number = manifest["event_count"] + 1
    previous_event_checksum = manifest.get("last_event_checksum")
    record = deepcopy(validated_event)
    record.update(
        {
            "sequence_number": sequence_number,
            "previous_event_checksum": previous_event_checksum,
            "created_at": _now(),
        }
    )
    record["checksum"] = _event_checksum(record)
    event_path = events_dir / _event_filename(sequence_number, record["event_id"])
    _write_json_exclusive(event_path, record)

    updated = dict(manifest)
    updated["event_count"] = sequence_number
    updated["first_event_at"] = updated.get("first_event_at") or record["timestamp"]
    updated["last_event_at"] = record["timestamp"]
    updated["last_event_checksum"] = record["checksum"]
    updated["checksum"] = _manifest_checksum(sequence_number, record["checksum"])
    updated["updated_at"] = _now()
    _write_json_atomic(manifest_path, updated)
    return deepcopy(record)


def read_audit_events(root_path: str | Path) -> list[dict[str, Any]]:
    """Lee eventos persistidos en orden de secuencia."""
    events_dir = Path(root_path) / EVENTS_DIR_NAME
    events = [_read_json(path) for path in sorted(events_dir.glob("*.json"))]
    return sorted(events, key=lambda event: event["sequence_number"])


def verify_audit_store(root_path: str | Path) -> dict[str, Any]:
    """Verifica secuencia, checksum de eventos, chain y manifest."""
    root = Path(root_path)
    manifest = validate_audit_store_contract(_read_json(root / MANIFEST_NAME))
    event_paths = sorted((root / EVENTS_DIR_NAME).glob("*.json"))
    events = [_read_json(path) for path in event_paths]
    if len(events) != manifest["event_count"]:
        raise ValueError("event_count no coincide con archivos")
    previous_checksum = None
    for expected_sequence, (path, event) in enumerate(zip(event_paths, events), start=1):
        expected_prefix = f"{expected_sequence:08d}_"
        if not path.name.startswith(expected_prefix):
            raise ValueError("sequence rota")
        if event.get("sequence_number") != expected_sequence:
            raise ValueError("sequence rota")
        if event.get("previous_event_checksum") != previous_checksum:
            raise ValueError("previous_event_checksum invalido")
        if event.get("checksum") != _event_checksum(event):
            raise ValueError("event checksum invalido")
        validate_observability_event({key: value for key, value in event.items() if key not in {"sequence_number", "previous_event_checksum", "checksum"}})
        previous_checksum = event["checksum"]
    if manifest.get("last_event_checksum") != previous_checksum:
        raise ValueError("last_event_checksum no coincide")
    if manifest.get("checksum") != _manifest_checksum(manifest["event_count"], previous_checksum):
        raise ValueError("manifest checksum invalido")
    return {
        "audit_store_id": manifest["audit_store_id"],
        "event_count": manifest["event_count"],
        "last_event_checksum": previous_checksum,
        "verified": True,
    }


def summarize_audit_store(root_path: str | Path) -> dict[str, Any]:
    events = read_audit_events(root_path)
    clean_events = [
        {key: value for key, value in event.items() if key not in {"sequence_number", "previous_event_checksum", "checksum"}}
        for event in events
    ]
    summary = summarize_observability_events(clean_events)
    summary["audit_store"] = verify_audit_store(root_path)
    return summary


def _event_checksum(event: dict[str, Any]) -> str:
    payload = {key: value for key, value in event.items() if key != "checksum"}
    return _checksum(payload)


def _manifest_checksum(event_count: int, last_event_checksum: str | None) -> str:
    return _checksum({"event_count": event_count, "last_event_checksum": last_event_checksum})


def _checksum(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def _event_filename(sequence_number: int, event_id: str) -> str:
    safe_event_id = re.sub(r"[^a-zA-Z0-9_]+", "_", event_id).strip("_")
    return f"{sequence_number:08d}_{safe_event_id}.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json_exclusive(path: Path, payload: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def _now() -> str:
    return datetime.now().isoformat()
