"""Observable shadow evaluation for development-time OCI packs."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Mapping

from gokv.inheritance import validate_development_oci_pack
from gokv.storage import VaultPaths, default_paths


SHADOW_SCHEMA_VERSION = "gokv.shadow_inheritance_evaluation.v1"
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_LIST_FIELDS = (
    "knowledge_items_available", "knowledge_items_selected", "knowledge_items_applied",
    "knowledge_items_unused", "knowledge_items_irrelevant", "knowledge_items_conflicted",
    "knowledge_items_helpful", "new_candidates", "operator_interventions", "clarification_requests",
)


def build_shadow_evaluation(
    *,
    evaluation_id: str,
    pack: Mapping[str, Any],
    mission_id: str,
    knowledge_items_applied: list[str] | None = None,
    knowledge_items_unused: list[str] | None = None,
    knowledge_items_irrelevant: list[str] | None = None,
    knowledge_items_conflicted: list[str] | None = None,
    knowledge_items_helpful: list[str] | None = None,
    new_candidates: list[str] | None = None,
    operator_interventions: list[str] | None = None,
    clarification_requests: list[str] | None = None,
    result: str = "SHADOW_INSPECTION_ONLY",
    created_at: str | None = None,
) -> dict[str, Any]:
    validated_pack = validate_development_oci_pack(pack)
    available = list(validated_pack["applicable_knowledge_ids"])
    evaluation = {
        "evaluation_id": evaluation_id,
        "schema_version": SHADOW_SCHEMA_VERSION,
        "pack_id": validated_pack["execution_pack_id"],
        "mission_id": mission_id,
        "knowledge_items_available": available,
        "knowledge_items_selected": list(available),
        "knowledge_items_applied": list(knowledge_items_applied or []),
        "knowledge_items_unused": list(knowledge_items_unused or []),
        "knowledge_items_irrelevant": list(knowledge_items_irrelevant or []),
        "knowledge_items_conflicted": list(knowledge_items_conflicted or []),
        "knowledge_items_helpful": list(knowledge_items_helpful or []),
        "new_candidates": list(new_candidates or []),
        "operator_interventions": list(operator_interventions or []),
        "clarification_requests": list(clarification_requests or []),
        "result": result,
        "pack_size_bytes": len(json.dumps(validated_pack, ensure_ascii=False, sort_keys=True).encode("utf-8")),
        "pack_item_count": len(available),
        "created_at": created_at or _now(),
    }
    return validate_shadow_evaluation(evaluation)


def validate_shadow_evaluation(evaluation: Mapping[str, Any]) -> dict[str, Any]:
    required = {"evaluation_id", "schema_version", "pack_id", "mission_id", *_LIST_FIELDS, "result", "pack_size_bytes", "pack_item_count", "created_at"}
    if not isinstance(evaluation, Mapping) or not required <= set(evaluation):
        raise ValueError("shadow evaluation incompleta")
    if evaluation["schema_version"] != SHADOW_SCHEMA_VERSION:
        raise ValueError("shadow schema invalido")
    for field in ("evaluation_id", "mission_id"):
        if not isinstance(evaluation[field], str) or not _ID_RE.fullmatch(evaluation[field]):
            raise ValueError(f"{field} invalido")
    for field in _LIST_FIELDS:
        if not isinstance(evaluation[field], list) or not all(isinstance(value, str) for value in evaluation[field]):
            raise ValueError(f"{field} debe ser una lista de strings")
    available = set(evaluation["knowledge_items_available"])
    selected = set(evaluation["knowledge_items_selected"])
    for field in ("knowledge_items_applied", "knowledge_items_unused", "knowledge_items_irrelevant", "knowledge_items_conflicted", "knowledge_items_helpful"):
        if not set(evaluation[field]) <= selected:
            raise ValueError(f"{field} debe ser subconjunto de selected")
    if selected != available:
        raise ValueError("shadow selected debe reflejar todos los items disponibles")
    if evaluation["pack_item_count"] != len(evaluation["knowledge_items_available"]):
        raise ValueError("pack_item_count inconsistente")
    if not isinstance(evaluation["pack_size_bytes"], int) or evaluation["pack_size_bytes"] < 0:
        raise ValueError("pack_size_bytes invalido")
    if not isinstance(evaluation["result"], str) or not evaluation["result"].strip():
        raise ValueError("result invalido")
    return deepcopy(dict(evaluation))


def save_shadow_evaluation(
    evaluation: Mapping[str, Any], paths: VaultPaths | None = None
) -> Path:
    validated = validate_shadow_evaluation(evaluation)
    vault = paths or default_paths()
    destination = vault.events_dir / "shadow" / f"{validated['evaluation_id']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"shadow evaluation duplicada: {destination.stem}") from exc
    return destination


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
