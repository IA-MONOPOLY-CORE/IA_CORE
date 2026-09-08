"""N5 checkpoint and post-block feedback for UI/UX 1.202."""

import json
from pathlib import Path

from gokv.inheritance import validate_development_oci_pack, validate_oci_consumption_result
from gokv.manifest import validate_next_mission_inheritance_manifest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PROMOTED = [
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
]
NEXT_MANIFEST = ROOT / "knowledge/global_operational/packs/next_mission_manifest_ui_ux_1_203_deterministic_visual_terrain_hardening.json"
NEXT_PACK = ROOT / "knowledge/global_operational/packs/oci/gokv.pack.78a9e7d54dc5d62b_ui_ux_1_203_deterministic_visual_terrain_hardening_post_microcopy.json"
CONSUMPTION = ROOT / "knowledge/global_operational/events/oci_consumption/ui_ux_1_202_promoted_only_consumption.json"
INVENTORY = ROOT / "tests/fixtures/ui_ux_1_202_visual_terrain_inventory.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_next_mission_manifest_and_pack_are_promoted_only_and_scoped():
    manifest = validate_next_mission_inheritance_manifest(_load(NEXT_MANIFEST))
    pack = validate_development_oci_pack(_load(NEXT_PACK))

    assert manifest["mode"] == "PROMOTED_ONLY"
    assert manifest["recommended_oci_mode"] == "PROMOTED_ONLY"
    assert manifest["execution_pack_id"] == "gokv.pack.78a9e7d54dc5d62b"
    assert manifest["knowledge_ids"] == EXPECTED_PROMOTED
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert manifest["conflicts"] == []
    assert manifest["hard_frontier"]["index"] == 7
    assert manifest["ui_ux_1_203_executed"] is False
    assert pack["mode"] == "PROMOTED_ONLY"
    assert pack["allowed_statuses"] == ["PROMOTED"]
    assert pack["applicable_knowledge_ids"] == EXPECTED_PROMOTED
    assert pack["output_contract"]["execution_enabled"] is False


def test_visual_inventory_and_oci_consumption_close_without_new_knowledge():
    inventory = _load(INVENTORY)
    consumption = validate_oci_consumption_result(_load(CONSUMPTION))

    assert inventory["surfaces"]["product_diff"] == "EMPTY"
    assert inventory["classification_counts"]["DETERMINISTIC_FIX"] == 2
    assert inventory["classification_counts"]["CONTRACT_CHANGE_REQUIRED"] == 0
    assert consumption["knowledge_items_available"] == EXPECTED_PROMOTED
    assert consumption["knowledge_items_selected"] == EXPECTED_PROMOTED
    assert consumption["knowledge_items_applied"] == EXPECTED_PROMOTED
    assert consumption["knowledge_items_helpful"] == EXPECTED_PROMOTED
    assert consumption["knowledge_items_unused"] == []
    assert consumption["knowledge_items_irrelevant"] == []
    assert consumption["knowledge_items_conflicted"] == []
    assert consumption["new_candidates"] == []
    assert consumption["operator_interventions"] == []
