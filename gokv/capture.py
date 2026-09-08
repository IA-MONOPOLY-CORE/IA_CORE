"""Development-only capture pipeline for experiences and execution metrics."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from gokv.storage import VaultPaths, default_paths


LEARNING_EVENT_SCHEMA_VERSION = "gokv.learning_event.v1"
EXECUTION_METRIC_SCHEMA_VERSION = "gokv.execution_metric.v1"
MEASUREMENT_QUALITY = frozenset({"MEASURED", "OPERATOR_REPORTED", "OPERATOR_ESTIMATED", "NOT_AVAILABLE", "RESET_INTERRUPTED"})
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def build_learning_event(
    *,
    event_id: str,
    source_prompt: str,
    source_phase: str,
    source_checkpoint: str | None,
    start_commit: str | None,
    end_commit: str | None,
    model: str | None,
    effort: str | None,
    mission_type: str,
    planned_stations: int,
    completed_stations: int,
    commits: list[str] | None = None,
    tests: list[str] | None = None,
    duration: float | None = None,
    operator_interventions: list[Any] | None = None,
    retries: int | None = None,
    rollbacks: int | None = None,
    autonomous_blockers_resolved: list[str] | None = None,
    result: str,
    observations: list[str] | None = None,
    candidate_knowledge_ids: list[str] | None = None,
    metrics_refs: list[str] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    event = {
        "event_id": event_id,
        "schema_version": LEARNING_EVENT_SCHEMA_VERSION,
        "source_prompt": source_prompt,
        "source_phase": source_phase,
        "source_checkpoint": source_checkpoint,
        "start_commit": start_commit,
        "end_commit": end_commit,
        "model": model,
        "effort": effort,
        "mission_type": mission_type,
        "planned_stations": planned_stations,
        "completed_stations": completed_stations,
        "commits": list(commits or []),
        "tests": list(tests or []),
        "duration": duration,
        "operator_interventions": deepcopy(operator_interventions or []),
        "retries": retries,
        "rollbacks": rollbacks,
        "autonomous_blockers_resolved": list(autonomous_blockers_resolved or []),
        "result": result,
        "observations": list(observations or []),
        "candidate_knowledge_ids": list(candidate_knowledge_ids or []),
        "metrics_refs": list(metrics_refs or []),
        "created_at": created_at or _now(),
    }
    return validate_learning_event(event)


def validate_learning_event(event: dict[str, Any]) -> dict[str, Any]:
    required = {
        "event_id", "schema_version", "source_prompt", "source_phase", "source_checkpoint",
        "start_commit", "end_commit", "model", "effort", "mission_type", "planned_stations",
        "completed_stations", "commits", "tests", "duration", "operator_interventions", "retries",
        "rollbacks", "autonomous_blockers_resolved", "result", "observations",
        "candidate_knowledge_ids", "metrics_refs", "created_at",
    }
    _validate_object(event, required, "learning_event")
    _validate_id(event["event_id"], "event_id")
    if event["schema_version"] != LEARNING_EVENT_SCHEMA_VERSION:
        raise ValueError("schema_version de learning_event invalida")
    for field in ("source_prompt", "source_phase", "mission_type", "result", "created_at"):
        _validate_text(event[field], field)
    for field in ("source_checkpoint", "start_commit", "end_commit", "model", "effort"):
        if event[field] is not None and not isinstance(event[field], str):
            raise ValueError(f"{field} debe ser texto o null")
    _validate_non_negative_int(event["planned_stations"], "planned_stations")
    _validate_non_negative_int(event["completed_stations"], "completed_stations")
    if event["completed_stations"] > event["planned_stations"]:
        raise ValueError("completed_stations no puede superar planned_stations")
    for field in ("commits", "tests", "autonomous_blockers_resolved", "observations", "candidate_knowledge_ids", "metrics_refs"):
        _validate_string_list(event[field], field)
    if event["duration"] is not None and (not isinstance(event["duration"], (int, float)) or event["duration"] < 0):
        raise ValueError("duration debe ser un numero no negativo o null")
    for field in ("retries", "rollbacks"):
        if event[field] is not None:
            _validate_non_negative_int(event[field], field)
    if not isinstance(event["operator_interventions"], list):
        raise ValueError("operator_interventions debe ser una lista")
    _validate_serializable(event)
    return deepcopy(event)


def build_execution_metric(
    *,
    metric_id: str,
    model: str | None,
    effort: str | None,
    task_type: str,
    duration: float | None = None,
    station_count: int | None = None,
    commits: list[str] | None = None,
    tests: list[str] | None = None,
    operator_interventions: int | None = None,
    retries: int | None = None,
    rollbacks: int | None = None,
    result: str | None = None,
    quota_5h_start: str | None = None,
    quota_5h_end: str | None = None,
    quota_5h_delta: str | None = None,
    quota_weekly_start: str | None = None,
    quota_weekly_end: str | None = None,
    quota_weekly_delta: str | None = None,
    measurement_quality: str = "NOT_AVAILABLE",
    operator_estimate: Any = None,
    notes: list[str] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    metric = {
        "metric_id": metric_id,
        "schema_version": EXECUTION_METRIC_SCHEMA_VERSION,
        "model": model,
        "effort": effort,
        "task_type": task_type,
        "duration": duration,
        "station_count": station_count,
        "commits": list(commits or []),
        "tests": list(tests or []),
        "operator_interventions": operator_interventions,
        "retries": retries,
        "rollbacks": rollbacks,
        "result": result,
        "quota_5h_start": quota_5h_start,
        "quota_5h_end": quota_5h_end,
        "quota_5h_delta": quota_5h_delta,
        "quota_weekly_start": quota_weekly_start,
        "quota_weekly_end": quota_weekly_end,
        "quota_weekly_delta": quota_weekly_delta,
        "measurement_quality": measurement_quality,
        "operator_estimate": deepcopy(operator_estimate),
        "notes": list(notes or []),
        "created_at": created_at or _now(),
    }
    return validate_execution_metric(metric)


def validate_execution_metric(metric: dict[str, Any]) -> dict[str, Any]:
    required = {
        "metric_id", "schema_version", "model", "effort", "task_type", "duration", "station_count",
        "commits", "tests", "operator_interventions", "retries", "rollbacks", "result",
        "quota_5h_start", "quota_5h_end", "quota_5h_delta", "quota_weekly_start", "quota_weekly_end",
        "quota_weekly_delta", "measurement_quality", "operator_estimate", "notes", "created_at",
    }
    _validate_object(metric, required, "execution_metric")
    _validate_id(metric["metric_id"], "metric_id")
    if metric["schema_version"] != EXECUTION_METRIC_SCHEMA_VERSION:
        raise ValueError("schema_version de execution_metric invalida")
    if metric["model"] is not None and not isinstance(metric["model"], str):
        raise ValueError("model debe ser texto o null")
    if metric["effort"] is not None and not isinstance(metric["effort"], str):
        raise ValueError("effort debe ser texto o null")
    _validate_text(metric["task_type"], "task_type")
    _validate_non_negative_number_or_none(metric["duration"], "duration")
    if metric["station_count"] is not None:
        _validate_non_negative_int(metric["station_count"], "station_count")
    for field in ("commits", "tests", "notes"):
        _validate_string_list(metric[field], field)
    for field in ("operator_interventions", "retries", "rollbacks"):
        if metric[field] is not None:
            _validate_non_negative_int(metric[field], field)
    for field in (
        "result", "quota_5h_start", "quota_5h_end", "quota_5h_delta", "quota_weekly_start",
        "quota_weekly_end", "quota_weekly_delta",
    ):
        if metric[field] is not None and not isinstance(metric[field], str):
            raise ValueError(f"{field} debe ser texto o null")
    if metric["measurement_quality"] not in MEASUREMENT_QUALITY:
        raise ValueError("measurement_quality invalida")
    _validate_text(metric["created_at"], "created_at")
    _validate_serializable(metric)
    return deepcopy(metric)


def append_learning_event(event: dict[str, Any], paths: VaultPaths | None = None) -> Path:
    validated = validate_learning_event(event)
    vault = paths or default_paths()
    return _append_json(vault.events_dir / f"{validated['event_id']}.json", validated)


def append_execution_metric(metric: dict[str, Any], paths: VaultPaths | None = None) -> Path:
    validated = validate_execution_metric(metric)
    vault = paths or default_paths()
    return _append_json(vault.metrics_dir / f"{validated['metric_id']}.json", validated)


def _append_json(path: Path, value: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"registro duplicado: {path.stem}") from exc
    return path


def _validate_object(value: Any, required: set[str], name: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} debe ser un objeto")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{name} incompleto: {', '.join(sorted(missing))}")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise ValueError(f"{field} invalido")


def _validate_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _validate_non_negative_int(value: Any, field: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} debe ser entero no negativo")


def _validate_non_negative_number_or_none(value: Any, field: str) -> None:
    if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
        raise ValueError(f"{field} debe ser numero no negativo o null")


def _validate_string_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} debe ser una lista de strings")


def _validate_serializable(value: Any) -> None:
    try:
        json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("registro no serializable") from exc


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
