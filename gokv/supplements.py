"""Append-only operator measurement supplements for GOKV development records."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from gokv.storage import VaultPaths, default_paths


SUPPLEMENT_SCHEMA_VERSION = "gokv.operator_measurement_supplement.v1"
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def build_operator_measurement_supplement(
    *,
    supplement_id: str,
    original_event_id: str,
    model: str,
    effort: str,
    visible_duration: str,
    quota_5h_start_remaining: int,
    quota_5h_end_remaining: int,
    quota_5h_delta: int,
    quota_weekly_start_remaining: int,
    quota_weekly_end_remaining: int,
    quota_weekly_delta: int,
    planned_stations: int,
    completed_stations: int,
    commit_count: int,
    result: str,
    reported_at: str | None = None,
    source: str = "OPERATOR_REPORTED",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    supplement = {
        "supplement_id": supplement_id,
        "schema_version": SUPPLEMENT_SCHEMA_VERSION,
        "original_event_id": original_event_id,
        "source": source,
        "reported_at": reported_at or _now(),
        "model": model,
        "effort": effort,
        "visible_duration": visible_duration,
        "quota_5h_start_remaining": quota_5h_start_remaining,
        "quota_5h_end_remaining": quota_5h_end_remaining,
        "quota_5h_delta": quota_5h_delta,
        "quota_weekly_start_remaining": quota_weekly_start_remaining,
        "quota_weekly_end_remaining": quota_weekly_end_remaining,
        "quota_weekly_delta": quota_weekly_delta,
        "planned_stations": planned_stations,
        "completed_stations": completed_stations,
        "commit_count": commit_count,
        "result": result,
        "notes": list(notes or []),
    }
    return validate_operator_measurement_supplement(supplement)


def validate_operator_measurement_supplement(supplement: dict[str, Any]) -> dict[str, Any]:
    required = {
        "supplement_id", "schema_version", "original_event_id", "source", "reported_at", "model", "effort",
        "visible_duration", "quota_5h_start_remaining", "quota_5h_end_remaining", "quota_5h_delta",
        "quota_weekly_start_remaining", "quota_weekly_end_remaining", "quota_weekly_delta",
        "planned_stations", "completed_stations", "commit_count", "result", "notes",
    }
    if not isinstance(supplement, dict):
        raise ValueError("operator_measurement_supplement debe ser un objeto")
    missing = required - set(supplement)
    if missing:
        raise ValueError(f"operator_measurement_supplement incompleto: {', '.join(sorted(missing))}")
    _validate_id(supplement["supplement_id"], "supplement_id")
    _validate_id(supplement["original_event_id"], "original_event_id")
    if supplement["schema_version"] != SUPPLEMENT_SCHEMA_VERSION:
        raise ValueError("schema_version de supplement invalida")
    if supplement["source"] != "OPERATOR_REPORTED":
        raise ValueError("source debe ser OPERATOR_REPORTED")
    for field in ("reported_at", "model", "effort", "visible_duration", "result"):
        _validate_text(supplement[field], field)
    for field in (
        "quota_5h_start_remaining", "quota_5h_end_remaining", "quota_5h_delta",
        "quota_weekly_start_remaining", "quota_weekly_end_remaining", "quota_weekly_delta",
        "planned_stations", "completed_stations", "commit_count",
    ):
        _validate_non_negative_int(supplement[field], field)
    if supplement["completed_stations"] > supplement["planned_stations"]:
        raise ValueError("completed_stations no puede superar planned_stations")
    if not isinstance(supplement["notes"], list) or not all(isinstance(note, str) for note in supplement["notes"]):
        raise ValueError("notes debe ser una lista de strings")
    try:
        datetime.fromisoformat(supplement["reported_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("reported_at debe ser ISO-8601") from exc
    try:
        json.dumps(supplement, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("supplement no serializable") from exc
    return deepcopy(supplement)


def append_operator_measurement_supplement(
    supplement: dict[str, Any], paths: VaultPaths | None = None
) -> Path:
    validated = validate_operator_measurement_supplement(supplement)
    vault = paths or default_paths()
    original = vault.events_dir / f"{validated['original_event_id']}.json"
    if not original.is_file():
        raise FileNotFoundError(f"evento original ausente: {validated['original_event_id']}")
    destination = vault.events_dir / "supplements" / f"{validated['supplement_id']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"supplement duplicado: {destination.stem}") from exc
    return destination


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise ValueError(f"{field} invalido")


def _validate_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _validate_non_negative_int(value: Any, field: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} debe ser entero no negativo")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
