"""N1 integrity reconciliation for UI/UX 1.199."""

from collections import Counter

from ui_ux_panel_maestro_microcopy_1_198_support import (
    BASELINE,
    CLASSIFICATIONS,
    corpus_digest,
    corpus_items,
    decision_package_rows,
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


def test_n1_reconciles_all_layers_and_ids():
    items = corpus_items()
    classifications = semantic_classifications(items)
    rows = decision_package_rows(items)
    item_ids = {item.microcopy_id for item in items}
    classified_ids = {item.microcopy_id for item in classifications}
    package_ids = {row.microcopy_id for row in rows}
    assert len(items) == 1624
    assert len(classifications) == 1624
    assert len(rows) == 1624
    assert item_ids == classified_ids == package_ids
    assert all(row.recommendation for row in rows)


def test_n1_freezes_complete_classification_table_and_omitted_80():
    items = corpus_items()
    classifications = semantic_classifications(items)
    counts = Counter(item.classification for item in classifications)
    assert set(counts) <= set(CLASSIFICATIONS)
    assert counts == Counter({name: value for name, value in EXPECTED_CLASSIFICATIONS.items() if value})
    for name, value in EXPECTED_CLASSIFICATIONS.items():
        assert counts[name] == value
    omitted = {
        "NAVIGATION": 14,
        "FORM_LABEL": 42,
        "PLACEHOLDER": 20,
        "STATE_LABEL": 4,
    }
    assert sum(omitted.values()) == 80
    assert sum(EXPECTED_CLASSIFICATIONS.values()) == 1624
    assert sum(counts[name] for name in omitted) == 80


def test_n1_digest_and_protected_product_remain_unchanged():
    assert BASELINE == "6b9c806"
    assert corpus_digest() == "4e5e84fbfa63aeb257813536febf91b2fc73b99e0384340b4194609ba48201ff"
    assert protected_files_match_baseline() == []
