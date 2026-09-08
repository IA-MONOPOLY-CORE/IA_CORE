"""N4 promotion reassessment gate for the independent 1.200 evidence overlay."""

import json
from pathlib import Path

from gokv.promotion import validate_promotion_assessment


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "knowledge" / "global_operational" / "assessments" / "promotion_assessment_post_ui_ux_1_200.json"
EXPECTED_WITH_EVIDENCE = {
    "conditioned_autonomy",
    "compress_occurrences_into_decisions",
    "evidence_before_closure",
    "focal_group_canonical_deep_test_policy",
    "preserve_contract_until_explicit_change",
    "real_diff_over_planned_commit_name",
    "station_local_commits",
    "true_hard_frontier",
}


def test_n4_assesses_all_sixteen_validated_items_without_mutating_lifecycle():
    assessment = validate_promotion_assessment(json.loads(ASSESSMENT.read_text(encoding="utf-8")))
    assert assessment["total_validated_assessed"] == 16
    assert assessment["promoted_knowledge_ids"] == []
    assert assessment["policy"]["automatic_promotion"] is False
    assert assessment["policy"]["status_mutation"] == "PROHIBITED"
    assert set(assessment["category_counts"]) == {
        "INSUFFICIENT_EVIDENCE",
        "PROMOTION_READY",
        "DIRECTION_APPROVAL_REQUIRED",
    }
    assert assessment["category_counts"] == {
        "INSUFFICIENT_EVIDENCE": 8,
        "PROMOTION_READY": 7,
        "DIRECTION_APPROVAL_REQUIRED": 1,
    }

    decisions = {decision["knowledge_id"]: decision for decision in assessment["decisions"]}
    assert set(decisions) == {
        "already_compliant_do_not_invent_change",
        "compile_human_decisions_into_packages",
        "compress_occurrences_into_decisions",
        "conditioned_autonomy",
        "contract_over_ui_inference",
        "controlled_assembled_block_execution",
        "evidence_before_closure",
        "focal_group_canonical_deep_test_policy",
        "internal_gates",
        "local_rollback",
        "no_fake_operational_state",
        "no_giant_commit",
        "preserve_contract_until_explicit_change",
        "real_diff_over_planned_commit_name",
        "station_local_commits",
        "true_hard_frontier",
    }
    assert {key for key, value in decisions.items() if value["evidence_overlay_ref"]} == EXPECTED_WITH_EVIDENCE
    assert all(value["status"] == "VALIDATED" for value in decisions.values())
    assert all(value["evidence_after"] >= value["evidence_before"] for value in decisions.values())


def test_n4_no_item_json_or_promotion_executor_was_changed():
    assert not list((ROOT / "knowledge" / "global_operational" / "items").glob("*.py"))
