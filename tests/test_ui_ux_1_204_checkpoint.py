import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.inheritance import validate_oci_consumption_result
from gokv.loop import validate_post_block_learning_loop


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs/UI_UX_CURRENT_LINE_FINAL_CHECKPOINT_1_204.md"
MANIFEST = ROOT / "knowledge/global_operational/packs/next_roadmap_entry_manifest_ui_ux_1_204.json"
EVENT = ROOT / "knowledge/global_operational/events/ui_ux_1_204_integral_closure_and_handoff_learning_event.json"
METRIC = ROOT / "knowledge/global_operational/metrics/ui_ux_1_204_integral_closure_and_handoff_execution_metric.json"
CONSUMPTION = ROOT / "knowledge/global_operational/events/oci_consumption/ui_ux_1_204_promoted_only_consumption.json"
LOOP = ROOT / "knowledge/global_operational/events/post_block/ui_ux_1_204_integral_closure_and_handoff_loop.json"
EVIDENCE = ROOT / "knowledge/global_operational/events/evidence/ui_ux_1_204_conditioned_autonomy_evidence.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_final_checkpoint_and_manifest_preserve_handoff_boundary():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    manifest = _load(MANIFEST)
    assert "N6_UI_UX_1_204_FINAL_CHECKPOINT_AND_HANDOFF_PASSED" in checkpoint
    assert "UI_UX_CURRENT_LINE_INTEGRAL_CLOSURE_AND_HANDOFF_1_204_PASSED" in checkpoint
    assert manifest["mission_id"] == "roadmap_2_0_continuity_preflight_after_ui_ux_closure"
    assert manifest["mission_type"] == "READ_ONLY_CONTINUITY_REBASE"
    assert manifest["executed"] is False
    assert manifest["readiness"] == "ready_for_roadmap_2_x_continuity_rebase"
    assert manifest["protected_product_baseline"]["product_diff"] == "EMPTY"
    assert manifest["next_pack_id"] is None


def test_gokv_capture_and_consumption_validate_without_promotion():
    event = validate_learning_event(_load(EVENT))
    metric = validate_execution_metric(_load(METRIC))
    consumption = validate_oci_consumption_result(_load(CONSUMPTION))
    loop = validate_post_block_learning_loop(_load(LOOP))
    evidence = _load(EVIDENCE)
    assert event["completed_stations"] == 7
    assert event["candidate_knowledge_ids"] == []
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert metric["quota_5h_start"] is None and metric["quota_weekly_end"] is None
    assert consumption["pack_id"] == "gokv.pack.0df1216585208f07"
    assert consumption["knowledge_items_selected"] == consumption["knowledge_items_helpful"]
    assert consumption["new_candidates"] == []
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["next_mission_id"] == "roadmap_2_0_continuity_preflight_after_ui_ux_closure"
    assert evidence["evidence_refs"][0]["knowledge_id"] == "conditioned_autonomy"
    assert evidence["excluded_from_overlay"] == ["promotion", "runtime_execution", "semantic_contract_extension"]


def test_next_documents_to_read_exist():
    for relative_path in _load(MANIFEST)["next_documents_to_read"]:
        assert (ROOT / relative_path).is_file(), relative_path
