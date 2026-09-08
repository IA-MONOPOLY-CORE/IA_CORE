"""N8 checkpoint and post-block capture gate for UI/UX 1.201."""

import json
from pathlib import Path
import subprocess

from gokv.inheritance import validate_oci_consumption_result
from gokv.loop import validate_post_block_learning_loop
from gokv.capture import validate_execution_metric, validate_learning_event


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_POST_DIRECTION_OCI_FEEDBACK_CHECKPOINT_1_201.md"
EVENTS = ROOT / "knowledge" / "global_operational" / "events"


def _load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_n8_capture_pipeline_and_oci_consumption_are_valid():
    consumption = validate_oci_consumption_result(_load("knowledge/global_operational/events/oci_consumption/ui_ux_1_201_post_direction_oci_consumption.json"))
    event = validate_learning_event(_load("knowledge/global_operational/events/ui_ux_1_201_post_direction_oci_learning_event.json"))
    metric = validate_execution_metric(_load("knowledge/global_operational/metrics/ui_ux_1_201_post_direction_oci_execution_metric.json"))
    loop = validate_post_block_learning_loop(_load("knowledge/global_operational/events/post_block/ui_ux_1_201_post_direction_oci_loop.json"))

    assert consumption["pack_id"] == "gokv.pack.3ec8e3b20cc39e56"
    assert len(consumption["knowledge_items_available"]) == 9
    assert len(consumption["knowledge_items_selected"]) == 9
    assert len(consumption["knowledge_items_applied"]) == 8
    assert consumption["knowledge_items_unused"] == ["local_rollback"]
    assert consumption["knowledge_items_helpful"] == consumption["knowledge_items_applied"]
    assert consumption["knowledge_items_conflicted"] == []
    assert consumption["new_candidates"] == []
    assert consumption["operator_interventions"] == []
    assert event["completed_stations"] == 9 and event["planned_stations"] == 9
    assert event["candidate_knowledge_ids"] == []
    assert metric["station_count"] == 9 and metric["operator_interventions"] == 0
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["candidate_knowledge_ids"] == []
    assert loop["next_mission_id"] == "ui_ux_1_202_next_visual_block_selection_post_microcopy_closure"
    assert loop["next_pack_id"] == "gokv.pack.247d953d36141636"


def test_n8_checkpoint_records_product_boundary_and_next_readiness():
    text = CHECKPOINT.read_text(encoding="utf-8")
    for marker in (
        "N8_UI_UX_1_201_CHECKPOINT_AND_POST_BLOCK_LOOP_PASSED",
        "UI_UX_POST_DIRECTION_MICROCOPY_REVIEW_AND_OCI_FEEDBACK_1_201_PASSED",
        "NO_LEARNING_FOUND",
        "PROMOTED = 0",
        "PRODUCTIVE_DIFF_1_201 = EMPTY",
        "UI/UX 1.200 = PRESERVED",
        "ready_for_ui_ux_1_202_next_visual_block_selection_post_microcopy_closure",
        "UI/UX 1.202 no fue ejecutado",
    ):
        assert marker in text


def test_n8_productive_surface_is_unchanged_from_1_201_entry():
    result = subprocess.run(
        ["git", "diff", "--quiet", "a2afc307d7278657a324efba345c04e28c39525a", "--", "ui/web/index.html", "ui/web/styles.css", "ui/web/i18n_es.json", "api.py", "core/backend_internal_ui_payloads.py"],
        cwd=ROOT,
        check=False,
    )
    assert result.returncode == 0
    assert not any(subject.startswith(("feat(ui)", "fix(ui)")) for subject in subprocess.check_output(
        ["git", "log", "--format=%s", "a2afc307d7278657a324efba345c04e28c39525a..HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines())
