"""Reusable development-time post-block learning loop helpers."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

from gokv.capture import append_execution_metric, append_learning_event, validate_execution_metric, validate_learning_event
from gokv.inheritance import append_knowledge_conflict_event, validate_knowledge_conflict_event
from gokv.schema import validate_knowledge_item
from gokv.storage import VaultPaths, default_paths, save_knowledge_item


POST_BLOCK_SCHEMA_VERSION = "gokv.post_block_learning_loop.v1"
LEARNING_STATUSES = frozenset({"LEARNING_FOUND", "NO_LEARNING_FOUND"})
LOOP_STEPS = ["EXECUTE", "VALIDATE", "CAPTURE", "DISTILL", "ASSESS", "STORE", "COMPILE_NEXT"]
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def record_post_block_learning_loop(
    *,
    loop_id: str,
    mission_id: str,
    learning_status: str,
    learning_event: Mapping[str, Any],
    execution_metric: Mapping[str, Any],
    candidate_items: Sequence[Mapping[str, Any]] = (),
    conflict_events: Sequence[Mapping[str, Any]] = (),
    next_mission_id: str | None = None,
    next_pack_id: str | None = None,
    paths: VaultPaths | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    vault = paths or default_paths()
    event = validate_learning_event(dict(learning_event))
    metric = validate_execution_metric(dict(execution_metric))
    if learning_status not in LEARNING_STATUSES:
        raise ValueError("learning_status invalido")
    if not isinstance(loop_id, str) or not _ID_RE.fullmatch(loop_id):
        raise ValueError("loop_id invalido")
    if not isinstance(mission_id, str) or not _ID_RE.fullmatch(mission_id):
        raise ValueError("mission_id invalido")
    candidate_ids = []
    for item in candidate_items:
        candidate = validate_knowledge_item(dict(item))
        if candidate["status"] not in {"OBSERVED", "CANDIDATE"}:
            raise ValueError("post-block solo puede almacenar OBSERVED o CANDIDATE")
        save_knowledge_item(candidate, vault)
        candidate_ids.append(candidate["knowledge_id"])
    conflict_ids = []
    for conflict in conflict_events:
        validated_conflict = validate_knowledge_conflict_event(dict(conflict))
        append_knowledge_conflict_event(validated_conflict, vault)
        conflict_ids.append(validated_conflict["event_id"])
    if learning_status == "NO_LEARNING_FOUND" and candidate_ids:
        raise ValueError("NO_LEARNING_FOUND no puede tener candidate_items")
    append_execution_metric(metric, vault)
    append_learning_event(event, vault)
    record = {
        "loop_id": loop_id,
        "schema_version": POST_BLOCK_SCHEMA_VERSION,
        "mission_id": mission_id,
        "learning_status": learning_status,
        "learning_event_id": event["event_id"],
        "execution_metric_id": metric["metric_id"],
        "candidate_knowledge_ids": sorted(candidate_ids),
        "conflict_event_ids": sorted(conflict_ids),
        "next_mission_id": next_mission_id,
        "next_pack_id": next_pack_id,
        "loop_steps": list(LOOP_STEPS),
        "created_at": created_at or _now(),
    }
    validated = validate_post_block_learning_loop(record)
    destination = vault.events_dir / "post_block" / f"{validated['loop_id']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"post-block loop duplicado: {destination.stem}") from exc
    return validated


def validate_post_block_learning_loop(record: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "loop_id", "schema_version", "mission_id", "learning_status", "learning_event_id",
        "execution_metric_id", "candidate_knowledge_ids", "conflict_event_ids", "next_mission_id",
        "next_pack_id", "loop_steps", "created_at",
    }
    if not isinstance(record, Mapping) or not required <= set(record):
        raise ValueError("post-block learning loop incompleto")
    for field in ("loop_id", "mission_id", "learning_event_id", "execution_metric_id"):
        if not isinstance(record[field], str) or not _ID_RE.fullmatch(record[field]):
            raise ValueError(f"{field} invalido")
    if record["schema_version"] != POST_BLOCK_SCHEMA_VERSION:
        raise ValueError("post-block schema invalido")
    if record["learning_status"] not in LEARNING_STATUSES:
        raise ValueError("learning_status invalido")
    for field in ("candidate_knowledge_ids", "conflict_event_ids", "loop_steps"):
        if not isinstance(record[field], list) or not all(isinstance(value, str) for value in record[field]):
            raise ValueError(f"{field} debe ser una lista de strings")
    if record["loop_steps"] != LOOP_STEPS:
        raise ValueError("loop_steps invalido")
    if record["learning_status"] == "NO_LEARNING_FOUND" and record["candidate_knowledge_ids"]:
        raise ValueError("NO_LEARNING_FOUND no puede declarar candidatos")
    for field in ("next_mission_id", "next_pack_id"):
        if record[field] is not None and (not isinstance(record[field], str) or not record[field].strip()):
            raise ValueError(f"{field} invalido")
    return deepcopy(dict(record))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
