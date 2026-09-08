"""Focal continuity guard for UI/UX 1.198 N1."""

import pytest

from ui_ux_panel_maestro_microcopy_1_198_support import (
    BASELINE,
    MICROCOPY_SOURCE_PATHS,
    PROTECTED_PRODUCT_PATHS,
    corpus_counts,
    corpus_digest,
    corpus_items,
    protected_files_match_baseline,
    validate_i18n_key,
    validate_source_registry,
)


def test_n1_manifest_document_and_helper_exist():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    doc = root / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_CONTINUITY_MANIFEST_1_198.md"
    helper = root / "tests" / "ui_ux_panel_maestro_microcopy_1_198_support.py"
    assert doc.is_file()
    assert helper.is_file()
    content = doc.read_text(encoding="utf-8").casefold()
    for marker in (
        "n1_microcopy_continuity_manifest_passed",
        "6b9c806",
        "microcopy_id",
        "payload v2",
        "wildcard",
        "n7",
    ):
        assert marker in content, marker


def test_n1_registry_is_exact_and_does_not_use_wildcards():
    validate_source_registry(MICROCOPY_SOURCE_PATHS)
    with pytest.raises(ValueError, match="wildcard"):
        validate_source_registry(["ui/web/*.html"])
    with pytest.raises(ValueError, match="unregistered source"):
        validate_source_registry(["ui/web/unknown-microcopy.txt"])
    assert all("*" not in path and "?" not in path for path in MICROCOPY_SOURCE_PATHS)


def test_n1_unknown_i18n_key_is_rejected():
    validate_i18n_key("common.accept")
    with pytest.raises(ValueError, match="unknown i18n key"):
        validate_i18n_key("common.unknown_key_created_by_test")
    with pytest.raises(ValueError, match="unknown i18n key"):
        validate_i18n_key("common.*")


def test_n1_corpus_is_nonempty_and_has_stable_ids_and_digest():
    items = corpus_items()
    assert items
    assert len({item.microcopy_id for item in items}) == len(items)
    assert corpus_digest(items) == corpus_digest(items)
    counts = corpus_counts(items)
    assert counts["TOTAL_CORPUS_ITEMS"] == len(items)
    assert counts["HTML_ITEMS"] > 0
    assert counts["I18N_ITEMS"] > 0
    assert counts["JS_ITEMS"] > 0


def test_n1_all_product_paths_match_6b9c806_and_no_active_copy_can_drift():
    assert BASELINE == "6b9c806"
    assert PROTECTED_PRODUCT_PATHS
    assert protected_files_match_baseline() == []
