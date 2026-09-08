"""N6 post-promotion OCI inheritance preparation for UI/UX 1.202."""

import json
from pathlib import Path

from gokv.inheritance import compile_oci_inheritance_pack, validate_development_oci_pack
from gokv.manifest import validate_next_mission_inheritance_manifest
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]
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


def _request():
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    request["mission_id"] = "ui_ux_1_202_next_visual_block_selection_post_microcopy_closure"
    return request


def test_n6_promoted_only_oci_pack_and_manifest_are_consistent():
    pack = compile_oci_inheritance_pack(_request(), default_paths(ROOT))
    manifest = validate_next_mission_inheritance_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))
    assert validate_development_oci_pack(pack)["mode"] == "PROMOTED_ONLY"
    assert pack["execution_pack_id"] == "gokv.pack.c886fbab561dee9a"
    assert pack["applicable_knowledge_ids"] == EXPECTED
    assert manifest["mode"] == "PROMOTED_ONLY"
    assert manifest["recommended_oci_mode"] == "PROMOTED_ONLY"
    assert manifest["execution_pack_id"] == pack["execution_pack_id"]
    assert manifest["knowledge_ids"] == EXPECTED
    assert manifest["promoted_items_selected"] == EXPECTED
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert manifest["conflicts"] == []
    assert manifest["product_decisions_included"] == []
    assert manifest["ui_ux_1_202_executed"] is False


def test_n6_report_preserves_authority_and_no_execution_boundary():
    report = (ROOT / "docs/GOKV_UI_UX_1_202_POST_PROMOTION_INHERITANCE_REPORT.md").read_text(encoding="utf-8")
    assert "N6_GOKV_UI_UX_1_202_INHERITANCE_PREPARATION_PASSED" in report
    assert "PROMOTED_ONLY" in report
    assert "CURRENT_CONTRACT_WINS" in report
    assert "UI/UX 1.202 is prepared only" in report
