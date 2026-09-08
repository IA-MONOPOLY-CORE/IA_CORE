"""Checkpoint and post-block capture guards for UI/UX 1.203."""

import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.inheritance import validate_oci_consumption_result
from gokv.loop import validate_post_block_learning_loop


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/UI_UX_PANEL_MAESTRO_DETERMINISTIC_VISUAL_TERRAIN_HARDENING_CHECKPOINT_1_203.md"
DECISION = ROOT / "docs/UI_UX_PANEL_MAESTRO_NEXT_HARD_FRONTIER_DECISION_PACKAGE_1_203.md"
EVENT = ROOT / "knowledge/global_operational/events/ui_ux_1_203_deterministic_visual_terrain_hardening_learning_event.json"
METRIC = ROOT / "knowledge/global_operational/metrics/ui_ux_1_203_deterministic_visual_terrain_hardening_execution_metric.json"
CONSUMPTION = ROOT / "knowledge/global_operational/events/oci_consumption/ui_ux_1_203_promoted_only_consumption.json"
LOOP = ROOT / "knowledge/global_operational/events/post_block/ui_ux_1_203_deterministic_visual_terrain_hardening_loop.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_checkpoint_records_two_fixes_and_the_station_seven_frontier():
    text = DOC.read_text(encoding="utf-8")
    assert "UI_UX_DETERMINISTIC_VISUAL_TERRAIN_HARDENING_1_203_PASSED" in text
    assert "195/231" in text and "195/195" in text
    assert "available/client width `292`" in text and "scroll width `300`" in text
    assert "`292/292`" in text
    assert "18 added CSS lines" in text
    assert "Current deterministic station count: 6" in text
    assert "Hard frontier index: 7" in text
    assert "Requires Direction: yes" in text
    assert "Station 7" in text and "was not executed" in text
    assert DECISION.is_file()


def test_post_block_records_validate_without_new_knowledge_or_pack():
    event = validate_learning_event(_load(EVENT))
    metric = validate_execution_metric(_load(METRIC))
    consumption = validate_oci_consumption_result(_load(CONSUMPTION))
    loop = validate_post_block_learning_loop(_load(LOOP))
    assert event["completed_stations"] == 6
    assert event["operator_interventions"] == []
    assert metric["station_count"] == 6
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert consumption["pack_id"] == "gokv.pack.78a9e7d54dc5d62b"
    assert consumption["knowledge_items_helpful"] == consumption["knowledge_items_selected"]
    assert consumption["new_candidates"] == []
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["next_mission_id"] is None
    assert loop["next_pack_id"] is None
