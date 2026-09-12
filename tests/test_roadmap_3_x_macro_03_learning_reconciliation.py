from __future__ import annotations

import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.loop import validate_post_block_learning_loop
from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "global_operational"
EXPECTED = {
    "contract_precision_multiplies_verified_scope",
    "verified_responsibility_per_usage",
    "autonomous_wall_time_per_usage",
    "publication_metadata_must_not_chase_its_own_head",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_macro_03_vault_is_valid_and_candidates_are_explicit():
    result = validate_vault(default_paths(ROOT))
    assert result["valid"] is True
    assert result["item_count"] == 38
    assert result["status_counts"] == {"CANDIDATE": 22, "VALIDATED": 9, "PROMOTED": 7}
    for knowledge_id in EXPECTED:
        item = load(BASE / "items" / f"{knowledge_id}.json")
        assert item["status"] == "CANDIDATE"
        assert item["learning_origin"] == "DEVELOPMENT_ORIGIN"
        assert item["evidence_refs"]
        assert item["source_commits"]
        assert item["source_checkpoints"]
        assert item["metrics_refs"] == ["roadmap_3_x_macro_03_execution_metric"]


def test_macro_03_learning_event_metric_and_loop_are_valid():
    event = validate_learning_event(load(BASE / "events" / "roadmap_3_x_macro_03_learning_event.json"))
    metric = validate_execution_metric(load(BASE / "metrics" / "roadmap_3_x_macro_03_execution_metric.json"))
    loop = validate_post_block_learning_loop(load(BASE / "events" / "post_block" / "roadmap_3_x_macro_03_learning_loop.json"))
    assert set(event["candidate_knowledge_ids"]) == EXPECTED
    assert event["result"] == "LEARNING_FOUND_CANDIDATES_STORED_NO_PROMOTION"
    assert metric["measurement_quality"] == "OPERATOR_REPORTED"
    assert metric["operator_estimate"]["five_hour_measurement_quality"] == "RESET_INTERRUPTED"
    assert metric["operator_estimate"]["final_suite_tests_collected"] == 6916
    assert metric["operator_estimate"]["final_suite_passed"] == 6910
    assert metric["operator_estimate"]["historical_unique_nodes_reconciled"] == 173
    assert metric["operator_estimate"]["monetary_or_token_conversion"] is False
    assert loop["learning_status"] == "LEARNING_FOUND"
    assert set(loop["candidate_knowledge_ids"]) == EXPECTED
    assert loop["next_mission_id"] == "roadmap_4_x_entry_review"


def test_macro_03_learning_preserves_non_operational_governance():
    event = load(BASE / "events" / "roadmap_3_x_macro_03_learning_event.json")
    metric = load(BASE / "metrics" / "roadmap_3_x_macro_03_execution_metric.json")
    combined = json.dumps({"event": event, "metric": metric})
    assert "No provider" in combined
    assert "No current Macro 03 wall time" in combined
    assert "automatic" not in combined.lower() or "promotion" in combined.lower()
    assert metric["quota_5h_delta"] == "NOT_COMPARABLE_RESET_INTERRUPTED"
