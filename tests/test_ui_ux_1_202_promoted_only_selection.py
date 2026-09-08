"""N0 gate for the first normal PROMOTED_ONLY UI/UX 1.202 mission."""

import json
from pathlib import Path

from gokv.inheritance import compile_oci_inheritance_pack, validate_development_oci_pack
from gokv.manifest import validate_next_mission_inheritance_manifest
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]
MISSION_ID = "ui_ux_1_202_next_visual_block_selection_post_microcopy_closure"
REQUEST = ROOT / "knowledge/global_operational/requests/gokv_0_3_ui_ux_1_202_comparison.json"
MANIFEST = ROOT / "knowledge/global_operational/packs/next_mission_inheritance_manifest_ui_ux_1_202_post_promotion.json"
EXPECTED = [
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
]


def _request() -> dict:
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    request["mission_id"] = MISSION_ID
    return request


def test_promoted_only_inheritance_is_minimum_sufficient_for_1_202():
    pack = compile_oci_inheritance_pack(_request(), default_paths(ROOT))
    manifest = validate_next_mission_inheritance_manifest(
        json.loads(MANIFEST.read_text(encoding="utf-8"))
    )

    assert validate_development_oci_pack(pack)["mode"] == "PROMOTED_ONLY"
    assert pack["execution_pack_id"] == "gokv.pack.c886fbab561dee9a"
    assert pack["applicable_knowledge_ids"] == EXPECTED
    assert manifest["mode"] == "PROMOTED_ONLY"
    assert manifest["execution_pack_id"] == pack["execution_pack_id"]
    assert manifest["knowledge_ids"] == EXPECTED
    assert manifest["promoted_items_selected"] == EXPECTED
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert manifest["conflicts"] == []
    assert manifest["product_decisions_included"] == []


def test_conditioned_autonomy_and_microcopy_decision_corpus_are_not_inherited():
    pack = compile_oci_inheritance_pack(_request(), default_paths(ROOT))

    assert "conditioned_autonomy" not in pack["applicable_knowledge_ids"]
    assert "compress_occurrences_into_decisions" not in pack["applicable_knowledge_ids"]
    assert pack["output_contract"]["runtime_enabled"] is False
    assert pack["output_contract"]["execution_enabled"] is False
    assert pack["output_contract"]["payload_enabled"] is False
