"""Focal inventory guard for UI/UX 1.198 N2."""

from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_198_support import (
    corpus_counts,
    corpus_digest,
    corpus_items,
    protected_files_match_baseline,
)


EXPECTED_COUNTS = {
    "TOTAL_CORPUS_ITEMS": 1624,
    "HTML_ITEMS": 1084,
    "HTML_TEXT_ITEMS": 1032,
    "HTML_ATTRIBUTE_ITEMS": 52,
    "I18N_ITEMS": 217,
    "JS_ITEMS": 323,
    "STATE_ITEMS": 219,
    "WARNING_ITEMS": 27,
    "ERROR_ITEMS": 19,
    "FALLBACK_ITEMS": 93,
    "EDITORIAL_ITEMS": 1225,
    "UNKNOWN_ITEMS": 0,
    "ACCESSIBILITY_ITEMS": 41,
    "DUPLICATE_ITEMS": 714,
    "CONTRACT_AWARE_ITEMS": 1079,
    "WRAP_RISK_ITEMS": 48,
    "DENSITY_RISK_ITEMS": 94,
}


def test_n2_inventory_document_has_gate_and_count_contract():
    doc = Path(__file__).resolve().parents[1] / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_ACTIVE_CORPUS_INVENTORY_1_198.md"
    content = doc.read_text(encoding="utf-8").casefold()
    for marker in (
        "n2_active_microcopy_corpus_inventory_passed",
        "microcopy_id",
        "html_text_nnnn",
        "i18n_nnnn_<key>",
        "js_<source>_<line>_<ordinal>",
        "request draft panel",
        "contract-aware widgets",
        "no active wording was",
    ):
        assert marker in content, marker
    for key, value in EXPECTED_COUNTS.items():
        assert f"`{key.casefold()}`" in content
        assert str(value) in content


def test_n2_every_record_has_required_fields_and_exact_source_context():
    items = corpus_items()
    required = {
        "microcopy_id", "text", "source", "file", "location", "surface",
        "visibility", "language", "initial_type", "contract_aware", "active",
        "legacy", "potential_duplicate", "wrapping_risk", "semantic_risk",
    }
    for item in items:
        record = item.__dict__
        assert required <= record.keys()
        assert item.microcopy_id and item.text and item.file and item.location
        assert item.active is True
        assert item.surface
    assert len({item.microcopy_id for item in items}) == len(items)


def test_n2_counts_and_digest_are_frozen_for_this_baseline():
    items = corpus_items()
    assert corpus_counts(items) == EXPECTED_COUNTS
    assert corpus_digest(items) == "4e5e84fbfa63aeb257813536febf91b2fc73b99e0384340b4194609ba48201ff"
    assert protected_files_match_baseline() == []


def test_n2_required_corpus_families_are_present_without_context_loss():
    items = corpus_items()
    sources = {item.source for item in items}
    types = {item.initial_type for item in items}
    surfaces = {item.surface for item in items}
    assert {"HTML_DIRECT_TEXT", "I18N_VALUE", "JS_RENDERABLE_LITERAL"} <= sources
    assert {"BLOCKER", "READINESS_LABEL", "WARNING", "ERROR", "FALLBACK", "NO_PAYLOAD", "NOT_AVAILABLE"} <= types
    assert {"REQUEST_DRAFT_PANEL", "CONTRACT_AWARE_WIDGETS", "P1_VALIDATION_READINESS", "P2_P3_MATRIX_CLOSURE"} <= surfaces
    assert any(item.source.startswith("HTML_") and item.visibility == "ACCESSIBLE_ATTRIBUTE" for item in items)
    assert any(item.potential_duplicate for item in items)
