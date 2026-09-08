import json
from pathlib import Path

import pytest

from gokv.promotion import (
    assess_current_validated,
    assess_promotion,
    validate_promotion_assessment,
)
from gokv.schema import build_knowledge_item
from gokv.storage import default_paths, iter_knowledge_items


ROOT = Path(__file__).resolve().parents[1]


def _evidence():
    return [
        {"evidence_id": "evidence_one", "kind": "test", "ref": "tests/one.py", "claim": "one"},
        {"evidence_id": "evidence_two", "kind": "checkpoint", "ref": "docs/two.md", "claim": "two"},
    ]


def _strong_item(kind="PRINCIPLE", lineage=None, applicability=None):
    return build_knowledge_item(
        knowledge_id="promotion_fixture",
        kind=kind,
        title="Promotion fixture",
        summary="Fixture with explicit promotion evidence.",
        status="VALIDATED",
        applicability=applicability or {"mission_types": ["all_development"], "scopes": ["IA_CORE_BUILD"]},
        evidence_refs=_evidence(),
        source_commits=["one1111", "two2222"],
        source_checkpoints=["checkpoint_one", "checkpoint_two"],
        confidence={"level": "HIGH", "rationale": "repeated fixture evidence"},
        lineage=lineage or [],
    )


def test_all_sixteen_validated_items_are_assessed_without_promotion():
    assessment = assess_current_validated(default_paths(ROOT))
    validated = [item for item in iter_knowledge_items(default_paths(ROOT)) if item["status"] == "VALIDATED"]

    assert assessment["total_validated_assessed"] == 16
    assert assessment["category_counts"] == {"INSUFFICIENT_EVIDENCE": 16}
    assert assessment["promoted_knowledge_ids"] == []
    assert {decision["knowledge_id"] for decision in assessment["decisions"]} == {
        item["knowledge_id"] for item in validated
    }
    assert all(decision["recommendation"] == "collect repeated independent evidence and reassess" for decision in assessment["decisions"])
    assert validate_promotion_assessment(assessment)["total_validated_assessed"] == 16
    stored = json.loads(
        (ROOT / "knowledge/global_operational/assessments/promotion_assessment_v1.json").read_text(encoding="utf-8")
    )
    assert validate_promotion_assessment(stored)["category_counts"] == {"INSUFFICIENT_EVIDENCE": 16}


def test_policy_exposes_ready_direction_and_conflict_categories_without_mutation():
    ready = assess_promotion(_strong_item())
    direction = assess_promotion(_strong_item(kind="AUTONOMY_RULE"))
    conflict = assess_promotion(
        _strong_item(
            lineage=[
                {
                    "relation": "CONTRADICT",
                    "related_knowledge_id": "field_record",
                    "related_origin": "FIELD_OPERATION",
                    "evidence_refs": ["field_conflict"],
                    "notes": ["fixture contradiction"],
                }
            ]
        )
    )
    incomplete = _strong_item(applicability={})
    incomplete["evidence_refs"] = _evidence()[:1]
    incomplete_result = assess_promotion(incomplete)

    assert ready["promotion_readiness"] == "PROMOTION_READY"
    assert direction["promotion_readiness"] == "DIRECTION_APPROVAL_REQUIRED"
    assert conflict["promotion_readiness"] == "CONFLICTING_EVIDENCE"
    assert incomplete_result["promotion_readiness"] == "INSUFFICIENT_EVIDENCE"
    assert all(result["status"] == "VALIDATED" for result in (ready, direction, conflict, incomplete_result))


def test_promotion_assessment_rejects_any_automatic_promotion():
    assessment = assess_current_validated(default_paths(ROOT))
    assessment["promoted_knowledge_ids"] = ["conditioned_autonomy"]
    with pytest.raises(ValueError, match="no puede promover automaticamente"):
        validate_promotion_assessment(assessment)
