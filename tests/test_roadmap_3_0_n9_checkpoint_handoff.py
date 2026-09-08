import json
import subprocess
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.inheritance import validate_development_oci_pack, validate_oci_consumption_result
from gokv.loop import validate_post_block_learning_loop
from gokv.manifest import validate_next_mission_inheritance_manifest
from gokv.supplements import validate_operator_measurement_supplement


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "82d309f00ab99dfa9eb100e5594bf1d8d0559f5a"
DOC = ROOT / "docs/ROADMAP_3_0_BACKEND_ELITE_READ_ONLY_AUDIT_CHECKPOINT.md"
EVENT = ROOT / "knowledge/global_operational/events/roadmap_3_0_backend_elite_read_only_audit_learning_event.json"
METRIC = ROOT / "knowledge/global_operational/metrics/roadmap_3_0_backend_elite_read_only_audit_execution_metric.json"
CONSUMPTION = ROOT / "knowledge/global_operational/events/oci_consumption/roadmap_3_0_backend_elite_read_only_audit_promoted_only_consumption.json"
LOOP = ROOT / "knowledge/global_operational/events/post_block/roadmap_3_0_backend_elite_read_only_audit_loop.json"
MANIFEST = ROOT / "knowledge/global_operational/packs/next_mission_manifest_roadmap_3_1_security_permission_activation_boundary_read_only_audit.json"
SUPPLEMENT = ROOT / "knowledge/global_operational/events/supplements/roadmap_2_x_operator_measurement_supplement.json"
PACK = ROOT / "knowledge/global_operational/packs/oci/gokv.pack.112d1122146ee5c3_roadmap_3_1_security_permission_activation_boundary_read_only_audit.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_n9_checkpoint_validates_capture_loop_manifest_and_real_pack():
    checkpoint = DOC.read_text(encoding="utf-8")
    event = validate_learning_event(_load(EVENT))
    metric = validate_execution_metric(_load(METRIC))
    consumption = validate_oci_consumption_result(_load(CONSUMPTION))
    loop = validate_post_block_learning_loop(_load(LOOP))
    manifest = validate_next_mission_inheritance_manifest(_load(MANIFEST))
    pack = validate_development_oci_pack(_load(PACK))
    supplement = validate_operator_measurement_supplement(_load(SUPPLEMENT))

    assert "ROADMAP_3_0_N9_CHECKPOINT_HANDOFF_PASSED" in checkpoint
    assert event["completed_stations"] == event["planned_stations"] == 10
    assert event["candidate_knowledge_ids"] == []
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert metric["duration"] is None
    assert consumption["pack_id"] == "gokv.pack.419ba7a247ea447f"
    assert consumption["pack_item_count"] == 7
    assert consumption["knowledge_items_selected"] == consumption["knowledge_items_applied"]
    assert consumption["new_candidates"] == []
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["next_mission_id"] == "roadmap_3_1_security_permission_activation_boundary_read_only_audit"
    assert manifest["mode"] == manifest["recommended_oci_mode"] == "PROMOTED_ONLY"
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert pack["allowed_statuses"] == ["PROMOTED"]
    assert pack["operational_guidance_only"] is True
    assert supplement["result"] == "PASS"


def test_n9_does_not_execute_3_1_or_change_protected_product_surfaces():
    checkpoint = DOC.read_text(encoding="utf-8")
    assert "3.1 executed | **NO**" in checkpoint
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASELINE}..HEAD"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    protected_prefixes = ("ui/", "providers/", "domains/", "agents/", "core/")
    protected_names = {"api.py", "config.py"}
    assert not [path for path in changed if path.startswith(protected_prefixes) or path in protected_names]
