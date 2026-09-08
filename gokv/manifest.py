"""Next-mission inheritance manifest builder for development-only use."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from gokv.inheritance import AUTHORITY_PRECEDENCE


MANIFEST_SCHEMA_VERSION = "gokv.next_mission_inheritance_manifest.v1"


def build_next_mission_inheritance_manifest(
    *,
    mission_id: str,
    mission: str,
    execution_pack_id: str,
    knowledge_ids: list[str],
) -> dict[str, Any]:
    manifest = {
        "manifest_id": f"{mission_id}_inheritance_manifest",
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "mission_id": mission_id,
        "mission": mission,
        "execution_pack_id": execution_pack_id,
        "knowledge_ids": sorted(set(knowledge_ids)),
        "mode": "DEVELOPMENT_VALIDATED",
        "authority_precedence": list(AUTHORITY_PRECEDENCE),
        "conflict_policy": "CURRENT_CONTRACT_WINS",
        "capture_protocol": ["GOKV_PRE_MISSION_INHERITANCE_V1", "GOKV_POST_BLOCK_CAPTURE_V1"],
        "product_decisions_included": [],
        "ui_ux_1_200_executed": False,
    }
    return validate_next_mission_inheritance_manifest(manifest)


def validate_next_mission_inheritance_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "manifest_id", "schema_version", "mission_id", "mission", "execution_pack_id", "knowledge_ids",
        "mode", "authority_precedence", "conflict_policy", "capture_protocol",
        "product_decisions_included", "ui_ux_1_200_executed",
    }
    if not isinstance(manifest, Mapping) or not required <= set(manifest):
        raise ValueError("next mission inheritance manifest incompleto")
    if manifest["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise ValueError("manifest schema invalido")
    for field in ("manifest_id", "mission_id", "mission", "execution_pack_id"):
        if not isinstance(manifest[field], str) or not manifest[field].strip():
            raise ValueError(f"{field} invalido")
    if manifest["mode"] not in {"PROMOTED_ONLY", "DEVELOPMENT_VALIDATED"}:
        raise ValueError("manifest mode invalido")
    if manifest["authority_precedence"] != AUTHORITY_PRECEDENCE:
        raise ValueError("manifest authority_precedence invalida")
    if manifest["conflict_policy"] != "CURRENT_CONTRACT_WINS":
        raise ValueError("manifest conflict_policy invalida")
    if manifest["capture_protocol"] != ["GOKV_PRE_MISSION_INHERITANCE_V1", "GOKV_POST_BLOCK_CAPTURE_V1"]:
        raise ValueError("manifest capture_protocol invalido")
    for field in ("knowledge_ids", "product_decisions_included"):
        if not isinstance(manifest[field], list) or not all(isinstance(value, str) for value in manifest[field]):
            raise ValueError(f"{field} debe ser una lista de strings")
    if manifest["product_decisions_included"] != []:
        raise ValueError("manifest no puede contener decisiones de producto")
    if manifest["ui_ux_1_200_executed"] is not False:
        raise ValueError("manifest no puede ejecutar UI/UX 1.200")
    if "ui_ux_1_202_executed" in manifest and manifest["ui_ux_1_202_executed"] is not False:
        raise ValueError("manifest no puede ejecutar UI/UX 1.202")
    for field in ("promoted_items_selected", "validated_items_selected", "candidate_items_selected", "conflicts"):
        if field in manifest and (not isinstance(manifest[field], list) or not all(isinstance(value, str) for value in manifest[field])):
            raise ValueError(f"{field} debe ser una lista de strings")
    if "recommended_oci_mode" in manifest and manifest["recommended_oci_mode"] not in {"PROMOTED_ONLY", "DEVELOPMENT_VALIDATED"}:
        raise ValueError("recommended_oci_mode invalido")
    return deepcopy(dict(manifest))
