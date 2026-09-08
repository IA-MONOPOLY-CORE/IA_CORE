import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.inheritance import validate_oci_consumption_result, validate_development_oci_pack
from gokv.loop import validate_post_block_learning_loop
from gokv.manifest import validate_next_mission_inheritance_manifest


ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / "knowledge/global_operational/events/roadmap_2_x_continuity_rebase_learning_event.json"
METRIC = ROOT / "knowledge/global_operational/metrics/roadmap_2_x_continuity_rebase_execution_metric.json"
CONSUMPTION = ROOT / "knowledge/global_operational/events/oci_consumption/roadmap_2_x_continuity_rebase_promoted_only_consumption.json"
LOOP = ROOT / "knowledge/global_operational/events/post_block/roadmap_2_x_continuity_rebase_loop.json"
EVIDENCE = ROOT / "knowledge/global_operational/events/evidence/roadmap_2_x_conditioned_autonomy_evidence.json"
PACK = ROOT / "knowledge/global_operational/packs/oci/gokv.pack.419ba7a247ea447f_roadmap_2_x_continuity_rebase_after_ui_ux_current_line_closure.json"
MANIFEST = ROOT / "knowledge/global_operational/packs/next_mission_manifest_roadmap_3_0_backend_elite_read_only_inventory.json"
SUPPLEMENT = ROOT / "knowledge/global_operational/events/supplements/roadmap_2_x_operator_measurement_supplement.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_post_block_capture_records_validate_and_close_without_learning():
    event = validate_learning_event(_load(EVENT))
    metric = validate_execution_metric(_load(METRIC))
    consumption = validate_oci_consumption_result(_load(CONSUMPTION))
    loop = validate_post_block_learning_loop(_load(LOOP))
    assert event["result"] == "ROADMAP_2_X_CONTINUITY_REBASE_PASSED"
    assert event["completed_stations"] == event["planned_stations"] == 4
    assert event["candidate_knowledge_ids"] == []
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert metric["quota_5h_delta"] is None
    assert consumption["pack_id"] == "gokv.pack.419ba7a247ea447f"
    assert consumption["knowledge_items_selected"] == consumption["knowledge_items_applied"]
    assert consumption["new_candidates"] == []
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["next_mission_id"] == "roadmap_3_0_backend_elite_read_only_inventory"


def test_next_pack_manifest_and_conditioned_autonomy_evidence_remain_bounded():
    pack = validate_development_oci_pack(_load(PACK))
    manifest = validate_next_mission_inheritance_manifest(_load(MANIFEST))
    evidence = _load(EVIDENCE)
    supplement = _load(SUPPLEMENT)
    assert pack["allowed_statuses"] == ["PROMOTED"]
    assert pack["operational_guidance_only"] is True
    assert manifest["mode"] == manifest["recommended_oci_mode"] == "PROMOTED_ONLY"
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert evidence["schema_version"] == "gokv.independent_evidence_overlay.v1"
    assert evidence["excluded_from_overlay"] == [
        "promotion",
        "runtime_execution",
        "backend_activation",
        "semantic_contract_extension",
    ]
    assert any("Product change is NO" in note for note in supplement["notes"])
    assert supplement["result"] == "PASS"
    assert any("5H_MEASUREMENT_QUALITY=RESET_INTERRUPTED" in note for note in supplement["notes"])
    assert any("5H_DELTA=NOT_RECONSTRUCTABLE_EXACTLY" in note for note in supplement["notes"])


def test_post_block_capture_keeps_the_explicit_backend_frontier():
    checkpoint = (ROOT / "docs/ROADMAP_2_X_CONTINUITY_REBASE_CHECKPOINT.md").read_text(encoding="utf-8")
    handoff = (ROOT / "docs/ROADMAP_3_0_BACKEND_ELITE_AUDIT_HANDOFF.md").read_text(encoding="utf-8")
    assert "READ_ONLY_INVENTORY_FIRST" in checkpoint
    assert "BACKEND_ELITE_READ_ONLY_AUDIT" in handoff
    assert "not executed" in handoff
    assert "worker, scheduler, queue" in handoff
    assert "provider call, network access" in handoff
