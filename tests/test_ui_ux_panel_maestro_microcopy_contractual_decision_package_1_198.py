"""Checkpoint guard for UI/UX 1.198 N6."""

from collections import Counter
from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_198_support import (
    DECISION_CATEGORIES,
    DECISION_RECOMMENDATIONS,
    decision_package_rows,
    protected_files_match_baseline,
)


EXPECTED_CATEGORIES = {
    "SAFE_TO_KEEP": 30,
    "EDITORIAL_CANDIDATE": 295,
    "CONSISTENCY_CANDIDATE": 197,
    "GEOMETRY_DRIVEN_CANDIDATE": 15,
    "CONTRACT_SENSITIVE_CANDIDATE": 139,
    "ACTION_PERMISSION_SENSITIVE": 15,
    "READINESS_SENSITIVE": 145,
    "AMBIGUOUS_REQUIRES_DIRECTION": 96,
    "MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE": 692,
}
EXPECTED_RECOMMENDATIONS = {
    "KEEP": 30,
    "REVIEW": 507,
    "DIRECTION_REQUIRED": 395,
    "CONTRACT_CHANGE_REQUIRED": 692,
    "NO_CHANGE": 0,
}


def test_n6_document_has_checkpoint_boundary_and_next_prompt():
    doc = Path(__file__).resolve().parents[1] / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_CONTRACTUAL_DECISION_PACKAGE_1_198.md"
    content = doc.read_text(encoding="utf-8").casefold()
    for marker in (
        "n6_microcopy_decision_package_checkpoint_passed",
        "ui_ux_microcopy_contractual_inventory_classification_decision_package_passed",
        "safe_to_keep",
        "editorial_candidate",
        "consistency_candidate",
        "geometry_driven_candidate",
        "contract_sensitive_candidate",
        "action_permission_sensitive",
        "readiness_sensitive",
        "ambiguous_requires_direction",
        "must_not_change_without_contract_change",
        "ready_for_ui_ux_1_199_microcopy_direction_decision_review",
        "prompt ui/ux 1.199",
        "1.199 is not executed",
        "no wording is implemented",
    ):
        assert marker in content, marker


def test_n6_every_decision_row_has_required_evidence_fields():
    rows = decision_package_rows()
    required = {
        "microcopy_id", "text", "file", "location", "classification",
        "decision_category", "risk", "reason", "possible_breakage",
        "contract_touched", "duplicate", "visual_issue", "inconsistency",
        "recommendation", "proposal_status",
    }
    assert len(rows) == 1624
    for row in rows:
        assert required <= row.__dict__.keys()
        assert row.text and row.file and row.location and row.reason
        assert row.decision_category in DECISION_CATEGORIES
        assert row.recommendation in DECISION_RECOMMENDATIONS
        if row.recommendation == "REVIEW":
            assert row.proposal_status == "PROPOSED_NOT_IMPLEMENTED"
    assert len({row.microcopy_id for row in rows}) == len(rows)


def test_n6_category_and_recommendation_counts_are_frozen():
    rows = decision_package_rows()
    assert Counter(row.decision_category for row in rows) == Counter(EXPECTED_CATEGORIES)
    assert Counter(row.recommendation for row in rows) == Counter(EXPECTED_RECOMMENDATIONS)
    assert protected_files_match_baseline() == []


def test_n6_direction_and_contract_changes_are_not_automated():
    rows = decision_package_rows()
    for row in rows:
        if row.decision_category in {"ACTION_PERMISSION_SENSITIVE", "AMBIGUOUS_REQUIRES_DIRECTION", "READINESS_SENSITIVE", "CONTRACT_SENSITIVE_CANDIDATE"}:
            assert row.recommendation == "DIRECTION_REQUIRED"
        if row.decision_category == "MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE":
            assert row.recommendation == "CONTRACT_CHANGE_REQUIRED"
    assert sum(row.decision_category in {"ACTION_PERMISSION_SENSITIVE", "AMBIGUOUS_REQUIRES_DIRECTION", "READINESS_SENSITIVE", "CONTRACT_SENSITIVE_CANDIDATE"} for row in rows) == 395
    assert sum(row.decision_category == "MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE" for row in rows) == 692


def test_n6_historical_allowlist_adaptation_is_exact_and_not_permissive():
    root = Path(__file__).resolve().parents[1]
    guard_paths = (
        root / "tests" / "ui_ux_1_192_scope.py",
        root / "tests" / "ui_ux_1_196_continuity.py",
        root / "tests" / "test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
        root / "tests" / "test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
        root / "tests" / "test_ui_ux_panel_maestro_next_large_scale_assembled_block_manifest_1_195.py",
        root / "tests" / "test_ui_ux_panel_maestro_post_assembled_block_direction_review_1_195.py",
        root / "tests" / "test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py",
    )
    exact_markers = ("CONTINUITY_1_197", "CONTINUITY_1_198")
    forbidden = ("glob(", "rglob(", "allow_all", "except AssertionError: pass")
    for path in guard_paths:
        source = path.read_text(encoding="utf-8")
        for marker in exact_markers:
            assert marker in source, (path, marker)
        for marker in forbidden:
            assert marker not in source.casefold(), (path, marker)
    shared = (root / "tests" / "ui_ux_1_192_scope.py").read_text(encoding="utf-8")
    for marker in (
        "docs/UI_UX_PANEL_MAESTRO_LARGE_SCALE_BLOCK_1_196_POSTMORTEM_1_197.md",
        "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_CONTINUITY_MANIFEST_1_198.md",
        "tests/test_ui_ux_panel_maestro_microcopy_contractual_decision_package_1_198.py",
        "tests/ui_ux_panel_maestro_microcopy_1_198_support.py",
    ):
        assert marker in shared, marker
    assert protected_files_match_baseline() == []
