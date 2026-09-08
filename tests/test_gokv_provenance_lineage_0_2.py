from pathlib import Path

import pytest

from gokv.schema import build_knowledge_item, validate_knowledge_item
from gokv.storage import default_paths, iter_knowledge_items, validate_vault


ROOT = Path(__file__).resolve().parents[1]


def evidence():
    return [{"evidence_id": "provenance_test", "kind": "test", "ref": "tests/provenance.py", "claim": "provenance passed"}]


def test_legacy_generation_zero_is_normalized_as_development_origin_without_rewrite():
    items = list(iter_knowledge_items(default_paths(ROOT)))

    assert len(items) == 23
    assert {item["learning_origin"] for item in items} == {"DEVELOPMENT_ORIGIN"}
    assert all(item["lineage"] == [] for item in items)
    assert validate_vault(default_paths(ROOT))["valid"] is True


def test_new_items_can_declare_origin_and_future_lineage_without_automatic_decision():
    item = build_knowledge_item(
        knowledge_id="field_refinement_example",
        kind="PATTERN",
        title="Field refinement example",
        summary="A future field record can refine a development-origin record.",
        evidence_refs=evidence(),
        source_commits=["5474b26"],
        source_checkpoints=["gokv_0_2"],
        confidence={"level": "MEDIUM", "rationale": "contract fixture"},
        learning_origin="FIELD_OPERATION",
        lineage=[
            {
                "relation": "REFINE",
                "related_knowledge_id": "conditioned_autonomy",
                "related_origin": "DEVELOPMENT_ORIGIN",
                "evidence_refs": ["field_event_1"],
                "notes": ["Relationship is represented, not resolved automatically."],
            }
        ],
    )

    assert item["learning_origin"] == "FIELD_OPERATION"
    assert item["lineage"][0]["relation"] == "REFINE"
    assert item["status"] == "OBSERVED"


def test_invalid_origin_and_lineage_relation_are_rejected():
    with pytest.raises(ValueError, match="learning_origin invalido"):
        build_knowledge_item(
            knowledge_id="bad_origin",
            kind="PRINCIPLE",
            title="Bad origin",
            summary="Invalid origin fixture.",
            evidence_refs=evidence(),
            source_commits=["5474b26"],
            source_checkpoints=["gokv_0_2"],
            confidence={"level": "LOW", "rationale": "fixture"},
            learning_origin="RUNTIME_LEARNING",
        )

    item = build_knowledge_item(
        knowledge_id="bad_lineage",
        kind="PRINCIPLE",
        title="Bad lineage",
        summary="Invalid lineage fixture.",
        evidence_refs=evidence(),
        source_commits=["5474b26"],
        source_checkpoints=["gokv_0_2"],
        confidence={"level": "LOW", "rationale": "fixture"},
    )
    item["lineage"] = [{"relation": "PROMOTE", "related_knowledge_id": "conditioned_autonomy", "related_origin": "DEVELOPMENT_ORIGIN", "evidence_refs": [], "notes": []}]
    with pytest.raises(ValueError, match="lineage relation invalida"):
        validate_knowledge_item(item)
