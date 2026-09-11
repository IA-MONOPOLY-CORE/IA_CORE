import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.loop import validate_post_block_learning_loop


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "knowledge" / "global_operational"
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_LEARNING_LOOP.md"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_macro_02_learning_loop_persists_refinement_without_silent_loss():
    event = validate_learning_event(_load(VAULT / "events" / "roadmap_3_x_macro_02_learning_loop.json"))
    metric = validate_execution_metric(_load(VAULT / "metrics" / "roadmap_3_x_macro_02_learning_loop_metric.json"))
    loop = validate_post_block_learning_loop(_load(VAULT / "events" / "post_block" / "roadmap_3_x_macro_02_learning_loop.json"))
    doc = DOC.read_text(encoding="utf-8")

    assert event["candidate_knowledge_ids"] == []
    assert event["result"] == "ROADMAP_3_X_MACRO_02_REFINEMENT_CAPTURED_NO_NEW_CANDIDATE"
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert loop["learning_status"] == "NO_LEARNING_FOUND"
    assert loop["candidate_knowledge_ids"] == []
    assert loop["next_mission_id"] == "roadmap_3_x_macro_03"
    assert "does not discard the observations" in doc


def test_macro_02_learning_loop_keeps_runtime_learning_disabled():
    doc = DOC.read_text(encoding="utf-8")

    for marker in (
        "No automatic promotion occurred",
        "No candidate was silently applied",
        "No runtime learning",
        "provider call",
        "network call",
        "product write",
        "execution was performed",
    ):
        assert marker in doc
