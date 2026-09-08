"""Focal semantic classification guard for UI/UX 1.198 N3."""

from collections import Counter
from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_198_support import (
    CLASSIFICATIONS,
    RISK_LEVELS,
    corpus_items,
    protected_files_match_baseline,
    semantic_classifications,
)


EXPECTED_CLASSIFICATIONS = {
    "EDITORIAL_SAFE": 408,
    "CONTRACTUAL_EXACT": 556,
    "CONTRACTUAL_EXPLANATORY": 93,
    "STATE_LABEL": 4,
    "READINESS_LABEL": 58,
    "PERMISSION_SENSITIVE": 0,
    "ACTION_SENSITIVE": 15,
    "BLOCKER": 138,
    "WARNING": 27,
    "ERROR": 19,
    "FALLBACK": 10,
    "NO_PAYLOAD": 31,
    "NOT_AVAILABLE": 52,
    "NAVIGATION": 14,
    "FORM_LABEL": 42,
    "PLACEHOLDER": 20,
    "ACCESSIBILITY_COPY": 41,
    "LEGACY_ACTIVE": 0,
    "LEGACY_INACTIVE": 0,
    "AMBIGUOUS_REQUIRES_DIRECTION": 96,
    "UNKNOWN_REQUIRES_DIRECTION": 0,
}
EXPECTED_RISKS = {
    "RISK_0_EDITORIAL": 398,
    "RISK_1_PRESENTATIONAL": 66,
    "RISK_2_CONTRACT_ADJACENT": 65,
    "RISK_3_CONTRACT_SENSITIVE": 984,
    "RISK_4_DIRECTION_REQUIRED": 111,
}


def test_n3_document_declares_classification_and_direction_boundary():
    doc = Path(__file__).resolve().parents[1] / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_SEMANTIC_CLASSIFICATION_1_198.md"
    content = doc.read_text(encoding="utf-8").casefold()
    for marker in (
        "n3_microcopy_semantic_classification_passed",
        "contractual_exact",
        "ambiguous_requires_direction",
        "risk_0_editorial",
        "risk_4_direction_required",
        "duplicate_equivalent",
        "must_remain_exact",
        "no automatic harmonization",
    ):
        assert marker in content, marker


def test_n3_every_inventory_item_has_one_allowed_primary_classification():
    items = corpus_items()
    classifications = semantic_classifications(items)
    assert len(classifications) == len(items)
    assert {item.microcopy_id for item in items} == {item.microcopy_id for item in classifications}
    assert all(item.classification in CLASSIFICATIONS for item in classifications)
    assert all(item.risk in RISK_LEVELS for item in classifications)
    assert all(item.reason and item.future_change and item.decision_owner and item.contract_touched for item in classifications)


def test_n3_classification_and_risk_counts_are_frozen():
    classifications = semantic_classifications()
    assert Counter(item.classification for item in classifications) == Counter(EXPECTED_CLASSIFICATIONS)
    assert Counter(item.risk for item in classifications) == Counter(EXPECTED_RISKS)


def test_n3_ambiguous_and_contract_sensitive_items_cannot_be_automated():
    classifications = semantic_classifications()
    for item in classifications:
        if item.classification == "AMBIGUOUS_REQUIRES_DIRECTION" or item.risk == "RISK_4_DIRECTION_REQUIRED":
            assert item.direction_required is True
            assert item.automatable is False
    assert sum(item.direction_required for item in classifications) == 1140
    assert sum(item.must_remain_exact for item in classifications) == 845
    assert protected_files_match_baseline() == []
