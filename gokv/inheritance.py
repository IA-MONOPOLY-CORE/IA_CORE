"""Development-time Operational Capability Inheritance (OCI)."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Mapping

from gokv.compiler import compile_execution_pack, validate_execution_pack
from gokv.storage import VaultPaths, default_paths


DEVELOPMENT_OCI_SCHEMA_VERSION = "gokv.development_oci.v1"
CONSUMPTION_SCHEMA_VERSION = "gokv.oci_consumption_result.v1"
CONFLICT_EVENT_SCHEMA_VERSION = "gokv.knowledge_conflict_event.v1"
AUTHORITY_PRECEDENCE = [
    "SECURITY_PRIVACY_HARD_CONTRACTS",
    "CURRENT_MISSION_EXPLICIT_CONSTRAINTS",
    "CURRENT_CANONICAL_ARCHITECTURE",
    "CURRENT_REPOSITORY_STATE",
    "GOKV_OPERATIONAL_GUIDANCE",
]
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def compile_development_oci_pack(
    request: Mapping[str, Any], paths: VaultPaths | None = None
) -> dict[str, Any]:
    if request.get("mode") != "DEVELOPMENT_VALIDATED":
        raise ValueError("DEVELOPMENT_TIME_OCI_V1 requiere mode DEVELOPMENT_VALIDATED")
    mission_id = request.get("mission_id")
    if not isinstance(mission_id, str) or not _ID_RE.fullmatch(mission_id):
        raise ValueError("mission_id invalido")
    base = compile_execution_pack(request, paths or default_paths())
    pack = deepcopy(base)
    pack.update(
        {
            "oci_schema_version": DEVELOPMENT_OCI_SCHEMA_VERSION,
            "inheritance_mode": "DEVELOPMENT_TIME_OCI_V1",
            "mission_id": mission_id,
            "authority_precedence": list(AUTHORITY_PRECEDENCE),
            "conflict_policy": {
                "id": "CURRENT_CONTRACT_WINS",
                "on_conflict": "EXCLUDE_KNOWLEDGE_AND_RECORD_EVENT",
                "silent_application": False,
                "automatic_resolution": False,
            },
            "operational_guidance_only": True,
        }
    )
    return validate_development_oci_pack(pack)


def compile_oci_inheritance_pack(
    request: Mapping[str, Any], paths: VaultPaths | None = None
) -> dict[str, Any]:
    """Compile an OCI inheritance pack for either explicit compiler mode."""

    if request.get("mode") not in {"PROMOTED_ONLY", "DEVELOPMENT_VALIDATED"}:
        raise ValueError("OCI inheritance requiere PROMOTED_ONLY o DEVELOPMENT_VALIDATED")
    mission_id = request.get("mission_id")
    if not isinstance(mission_id, str) or not _ID_RE.fullmatch(mission_id):
        raise ValueError("mission_id invalido")
    base = compile_execution_pack(request, paths or default_paths())
    pack = deepcopy(base)
    pack.update(
        {
            "oci_schema_version": DEVELOPMENT_OCI_SCHEMA_VERSION,
            "inheritance_mode": "DEVELOPMENT_TIME_OCI_V1",
            "mission_id": mission_id,
            "authority_precedence": list(AUTHORITY_PRECEDENCE),
            "conflict_policy": {
                "id": "CURRENT_CONTRACT_WINS",
                "on_conflict": "EXCLUDE_KNOWLEDGE_AND_RECORD_EVENT",
                "silent_application": False,
                "automatic_resolution": False,
            },
            "operational_guidance_only": True,
        }
    )
    return validate_development_oci_pack(pack)


def validate_development_oci_pack(pack: Mapping[str, Any]) -> dict[str, Any]:
    validate_execution_pack(pack)
    required = {
        "oci_schema_version", "inheritance_mode", "mission_id", "authority_precedence",
        "conflict_policy", "operational_guidance_only",
    }
    if not required <= set(pack):
        raise ValueError("development OCI pack incompleto")
    if pack["oci_schema_version"] != DEVELOPMENT_OCI_SCHEMA_VERSION:
        raise ValueError("oci_schema_version invalida")
    if pack["inheritance_mode"] != "DEVELOPMENT_TIME_OCI_V1":
        raise ValueError("inheritance_mode invalido")
    if not isinstance(pack["mission_id"], str) or not _ID_RE.fullmatch(pack["mission_id"]):
        raise ValueError("mission_id invalido")
    if pack["authority_precedence"] != AUTHORITY_PRECEDENCE:
        raise ValueError("authority_precedence invalida")
    if pack["conflict_policy"] != {
        "id": "CURRENT_CONTRACT_WINS",
        "on_conflict": "EXCLUDE_KNOWLEDGE_AND_RECORD_EVENT",
        "silent_application": False,
        "automatic_resolution": False,
    }:
        raise ValueError("conflict_policy invalida")
    if pack["operational_guidance_only"] is not True:
        raise ValueError("OCI debe ser operational_guidance_only")
    return json.loads(json.dumps(pack, ensure_ascii=False))


def save_development_oci_pack(pack: Mapping[str, Any], paths: VaultPaths | None = None) -> Path:
    validated = validate_development_oci_pack(pack)
    vault = paths or default_paths()
    destination = vault.packs_dir / "oci" / f"{validated['execution_pack_id']}_{validated['mission_id']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"OCI pack duplicado: {destination.stem}") from exc
    return destination


def build_oci_consumption_result(
    *,
    consumption_id: str,
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
    result: str = "INSPECTION_ONLY",
    created_at: str | None = None,
) -> dict[str, Any]:
    validated_pack = validate_development_oci_pack(pack)
    available = list(validated_pack["applicable_knowledge_ids"])
    selected = list(available)
    consumption = {
        "consumption_id": consumption_id,
        "schema_version": CONSUMPTION_SCHEMA_VERSION,
        "pack_id": validated_pack["execution_pack_id"],
        "mission_id": mission_id,
        "knowledge_items_available": available,
        "knowledge_items_selected": selected,
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
    return validate_oci_consumption_result(consumption)


def validate_oci_consumption_result(result: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "consumption_id", "schema_version", "pack_id", "mission_id", "knowledge_items_available",
        "knowledge_items_selected", "knowledge_items_applied", "knowledge_items_unused",
        "knowledge_items_irrelevant", "knowledge_items_conflicted", "knowledge_items_helpful",
        "new_candidates", "operator_interventions", "clarification_requests", "result",
        "pack_size_bytes", "pack_item_count", "created_at",
    }
    if not isinstance(result, Mapping) or not required <= set(result):
        raise ValueError("OCI consumption result incompleto")
    if result["schema_version"] != CONSUMPTION_SCHEMA_VERSION:
        raise ValueError("consumption schema invalido")
    for field in ("consumption_id", "mission_id"):
        if not isinstance(result[field], str) or not _ID_RE.fullmatch(result[field]):
            raise ValueError(f"{field} invalido")
    list_fields = [field for field in required if field.startswith("knowledge_items_")] + [
        "new_candidates", "operator_interventions", "clarification_requests"
    ]
    for field in list_fields:
        if not isinstance(result[field], list) or not all(isinstance(value, str) for value in result[field]):
            raise ValueError(f"{field} debe ser una lista de strings")
    if result["pack_item_count"] != len(result["knowledge_items_available"]):
        raise ValueError("pack_item_count inconsistente")
    if not isinstance(result["pack_size_bytes"], int) or result["pack_size_bytes"] < 0:
        raise ValueError("pack_size_bytes invalido")
    if not isinstance(result["result"], str) or not result["result"].strip():
        raise ValueError("result invalido")
    return deepcopy(dict(result))


def append_oci_consumption_result(
    result: Mapping[str, Any], paths: VaultPaths | None = None
) -> Path:
    validated = validate_oci_consumption_result(result)
    vault = paths or default_paths()
    destination = vault.events_dir / "oci_consumption" / f"{validated['consumption_id']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"consumption result duplicado: {destination.stem}") from exc
    return destination


def build_knowledge_conflict_event(
    *,
    event_id: str,
    mission_id: str,
    knowledge_id: str,
    conflict_field: str,
    current_contract_reference: str,
    created_at: str | None = None,
) -> dict[str, Any]:
    event = {
        "event_id": event_id,
        "schema_version": CONFLICT_EVENT_SCHEMA_VERSION,
        "mission_id": mission_id,
        "knowledge_id": knowledge_id,
        "conflict_field": conflict_field,
        "current_contract_reference": current_contract_reference,
        "resolution": "CURRENT_CONTRACT_WINS",
        "knowledge_applied": False,
        "created_at": created_at or _now(),
    }
    return validate_knowledge_conflict_event(event)


def validate_knowledge_conflict_event(event: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "event_id", "schema_version", "mission_id", "knowledge_id", "conflict_field",
        "current_contract_reference", "resolution", "knowledge_applied", "created_at",
    }
    if not isinstance(event, Mapping) or not required <= set(event):
        raise ValueError("knowledge conflict event incompleto")
    for field in ("event_id", "mission_id", "knowledge_id"):
        if not isinstance(event[field], str) or not _ID_RE.fullmatch(event[field]):
            raise ValueError(f"{field} invalido")
    if event["schema_version"] != CONFLICT_EVENT_SCHEMA_VERSION:
        raise ValueError("conflict event schema invalido")
    for field in ("conflict_field", "current_contract_reference", "created_at"):
        if not isinstance(event[field], str) or not event[field].strip():
            raise ValueError(f"{field} invalido")
    if event["resolution"] != "CURRENT_CONTRACT_WINS" or event["knowledge_applied"] is not False:
        raise ValueError("conflict policy invalida")
    return deepcopy(dict(event))


def append_knowledge_conflict_event(
    event: Mapping[str, Any], paths: VaultPaths | None = None
) -> Path:
    validated = validate_knowledge_conflict_event(event)
    vault = paths or default_paths()
    destination = vault.events_dir / "conflicts" / f"{validated['event_id']}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"conflict event duplicado: {destination.stem}") from exc
    return destination


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
