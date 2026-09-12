"""Contract checks for the Macro 02.2 GOKV/DOOL/OCI learning record."""

import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.loop import validate_post_block_learning_loop
from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_2_GOKV_DOOL_OCI_RECONCILIATION.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_macro_02_2_vault_contains_only_explicit_new_candidates():
    result = validate_vault(default_paths(ROOT))
    assert result["valid"] is True
    assert result["item_count"] == 34
    assert result["status_counts"] == {"CANDIDATE": 18, "VALIDATED": 9, "PROMOTED": 7}
    for knowledge_id in (
        "historical_checkpoint_requires_evidence_endpoint",
        "one_core_four_surfaces_preserves_canonical_authority",
    ):
        item = load(ROOT / "knowledge/global_operational/items" / f"{knowledge_id}.json")
        assert item["status"] == "CANDIDATE"
        assert item["learning_origin"] == "DEVELOPMENT_ORIGIN"
        assert item["evidence_refs"]
        assert item["source_commits"]
        assert item["source_checkpoints"]
        assert item["metrics_refs"] == ["roadmap_3_x_macro_02_2_execution_metric"]


def test_learning_event_metric_and_post_block_loop_are_schema_valid():
    base = ROOT / "knowledge/global_operational"
    event = validate_learning_event(load(base / "events/roadmap_3_x_macro_02_2_learning_event.json"))
    metric = validate_execution_metric(load(base / "metrics/roadmap_3_x_macro_02_2_execution_metric.json"))
    loop = validate_post_block_learning_loop(load(base / "events/post_block/roadmap_3_x_macro_02_2_learning_loop.json"))
    expected = [
        "historical_checkpoint_requires_evidence_endpoint",
        "one_core_four_surfaces_preserves_canonical_authority",
    ]
    assert event["candidate_knowledge_ids"] == expected
    assert event["end_commit"] == "84bfd59"
    assert metric["measurement_quality"] == "NOT_AVAILABLE"
    assert loop["learning_status"] == "LEARNING_FOUND"
    assert loop["candidate_knowledge_ids"] == expected
    assert loop["next_mission_id"] == "roadmap_3_x_macro_02_2_final_validation"


def test_reconciliation_preserves_no_promotion_and_no_operational_activation():
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "ROADMAP_3_X_MACRO_02_2_LEARNING_RECONCILIATION_STORED",
        "DEVELOPMENT_ORIGIN",
        "CANDIDATE",
        "No automatic promotion occurred",
        "development-only",
        "not automatically selected",
        "modifying model weights",
        "No GOKV promotion",
        "provider call",
        "runtime",
        "execution",
        "endpoint",
        "integration",
        "product payload",
    ):
        assert marker in text
