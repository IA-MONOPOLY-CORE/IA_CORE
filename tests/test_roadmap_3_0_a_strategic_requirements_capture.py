import json
import subprocess
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.inheritance import validate_development_oci_pack, validate_oci_consumption_result
from gokv.loop import validate_post_block_learning_loop


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "ba3f091449cd9fd736ec58981d0e41aa3c5d66eb"
CHECKPOINT = ROOT / "docs/ROADMAP_3_0_A_STRATEGIC_BUSINESS_WORKFORCE_MODEL_REQUIREMENTS_CHECKPOINT.md"
INDEX = ROOT / "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md"
EVENT = ROOT / "knowledge/global_operational/events/roadmap_3_0_a_strategic_business_workforce_model_platform_requirements_capture_learning_event.json"
METRIC = ROOT / "knowledge/global_operational/metrics/roadmap_3_0_a_strategic_requirements_execution_metric.json"
CONSUMPTION = ROOT / "knowledge/global_operational/events/oci_consumption/roadmap_3_0_a_strategic_requirements_promoted_only_consumption.json"
LOOP = ROOT / "knowledge/global_operational/events/post_block/roadmap_3_0_a_strategic_requirements_loop.json"
PACK = ROOT / "knowledge/global_operational/packs/oci/gokv.pack.419ba7a247ea447f_roadmap_2_x_continuity_rebase_after_ui_ux_current_line_closure.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_roadmap_3_0_a_documents_all_future_contracts_and_gokv_capture():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    event = validate_learning_event(_load(EVENT))
    metric = validate_execution_metric(_load(METRIC))
    consumption = validate_oci_consumption_result(_load(CONSUMPTION))
    loop = validate_post_block_learning_loop(_load(LOOP))
    pack = validate_development_oci_pack(_load(PACK))

    assert "ROADMAP_3_0_A_N7_CHECKPOINT_PASSED" in checkpoint
    assert "ROADMAP_3_0_A_STRATEGIC_BUSINESS_WORKFORCE_MODEL_REQUIREMENTS_CAPTURE_PASSED" in checkpoint
    assert "IA_CORE_OPEN_ENDED_BUSINESS_CREATION_AND_COVERAGE_REQUIREMENTS.md" in index
    assert "ROADMAP_6X_AGENT_MODEL_WORKFORCE_READINESS_GATE.md" in index
    assert event["completed_stations"] == event["planned_stations"] == 8
    assert event["candidate_knowledge_ids"] == []
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert consumption["pack_id"] == pack["execution_pack_id"]
    assert consumption["new_candidates"] == []
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["next_mission_id"] == "roadmap_3_1_security_permission_activation_boundary_read_only_audit"


def test_roadmap_3_0_a_does_not_change_product_surfaces():
    changed = subprocess.check_output(["git", "diff", "--name-only", f"{BASELINE}..HEAD"], cwd=ROOT, text=True).splitlines()
    protected = ("api.py", "config.py")
    prefixes = ("core/", "providers/", "agents/", "catalogs/", "domains/", "memory/", "ui/")
    assert not [path for path in changed if path in protected or path.startswith(prefixes)]
    assert "3.1" in CHECKPOINT.read_text(encoding="utf-8")

