"""N4 post-promotion integrity and governance reassessment."""

from pathlib import Path

import json

from gokv.promotion import assess_current_validated, build_post_promotion_assessment, validate_promotion_assessment
from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]


def test_n4_vault_and_governance_reassessment_are_exact():
    paths = default_paths(ROOT)
    assert validate_vault(paths)["status_counts"] == {"CANDIDATE": 7, "PROMOTED": 7, "VALIDATED": 9}
    live_assessment = assess_current_validated(paths)
    assert live_assessment["total_validated_assessed"] == 9
    source = json.loads((ROOT / "knowledge/global_operational/assessments/promotion_assessment_post_ui_ux_1_200.json").read_text(encoding="utf-8"))
    reassessment = build_post_promotion_assessment(
        source,
        [
            "compress_occurrences_into_decisions",
            "evidence_before_closure",
            "focal_group_canonical_deep_test_policy",
            "preserve_contract_until_explicit_change",
            "real_diff_over_planned_commit_name",
            "station_local_commits",
            "true_hard_frontier",
        ],
        assessed_at="2026-09-08T18:30:00+00:00",
    )
    assert validate_promotion_assessment(reassessment)["total_validated_assessed"] == 9
    assert reassessment["category_counts"] == {"DIRECTION_APPROVAL_REQUIRED": 1, "INSUFFICIENT_EVIDENCE": 8}
    assert reassessment["promoted_knowledge_ids"] == []


def test_n4_report_records_integrity_gate_and_boundaries():
    report = (ROOT / "docs/GOKV_FIRST_INSTITUTIONAL_PROMOTION_REPORT_0_3.md").read_text(encoding="utf-8")
    assert "N4_GOKV_POST_PROMOTION_INTEGRITY_PASSED" in report
    assert "PROMOTED = 0" in report
    assert "conditioned_autonomy" in report
    projected = json.loads((ROOT / "knowledge/global_operational/assessments/promotion_assessment_post_gokv_0_3.json").read_text(encoding="utf-8"))
    assert projected["category_counts"] == {"DIRECTION_APPROVAL_REQUIRED": 1, "INSUFFICIENT_EVIDENCE": 8}
