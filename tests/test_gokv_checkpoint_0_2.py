import json
from pathlib import Path

from gokv.manifest import build_next_mission_inheritance_manifest, validate_next_mission_inheritance_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_next_mission_manifest_matches_shadow_pack_and_has_no_product_decisions():
    manifest_path = ROOT / "knowledge/global_operational/packs/next_mission_inheritance_manifest_ui_ux_1_200.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validated = validate_next_mission_inheritance_manifest(manifest)

    assert validated["execution_pack_id"] == "gokv.pack.422f3d1b277abcfb"
    assert len(validated["knowledge_ids"]) == 9
    assert validated["product_decisions_included"] == []
    assert validated["ui_ux_1_200_executed"] is False


def test_checkpoint_status_and_manifest_builder_are_explicit():
    checkpoint = (ROOT / "docs" / "GOKV_DOOL_OCI_CHECKPOINT_0_2.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    manifest = build_next_mission_inheritance_manifest(
        mission_id="ui_ux_1_200",
        mission="microcopy_direction_decision_execution_preparation",
        execution_pack_id="gokv.pack.fixture",
        knowledge_ids=["conditioned_autonomy"],
    )

    assert "N8_GOKV_DOOL_OCI_CHECKPOINT_PASSED" in checkpoint
    assert "IA_CORE_GOKV_DOOL_OPERATIONAL_CAPABILITY_INHERITANCE_0_2_PASSED" in checkpoint
    assert "ready_for_first_development_mission_with_operational_inheritance" in checkpoint
    assert "GOKV 0.2" in readme
    assert manifest["conflict_policy"] == "CURRENT_CONTRACT_WINS"
    assert manifest["product_decisions_included"] == []


def test_ui_ux_1_200_execution_is_not_claimed_anywhere_in_gokv_checkpoint():
    checkpoint = (ROOT / "docs" / "GOKV_DOOL_OCI_CHECKPOINT_0_2.md").read_text(encoding="utf-8")
    report = (ROOT / "docs" / "GOKV_UI_UX_1_200_SHADOW_INHERITANCE_REPORT.md").read_text(encoding="utf-8")

    assert "UI_UX_1_200_EXECUTED = NO" in checkpoint
    assert "UI/UX 1.200 was not executed" in report
