"""N7 checkpoint guard for the UI/UX 1.199 Direction review."""

from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_199_support import protected_product_is_unchanged


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_REVIEW_CHECKPOINT_1_199.md"


def test_n7_checkpoint_document_is_present_and_closed():
    text = CHECKPOINT.read_text(encoding="utf-8")
    assert "N7_MICROCOPY_DIRECTOR_DECISION_SHEET_CHECKPOINT_PASSED" in text
    assert "UI_UX_MICROCOPY_DIRECTION_DECISION_COMPRESSION_REVIEW_PASSED" in text
    assert "1624" in text and "1143" in text and "8" in text
    assert "ready_for_ui_ux_1_200_microcopy_direction_decisions" in text


def test_n7_checkpoint_does_not_cross_product_boundary():
    text = CHECKPOINT.read_text(encoding="utf-8")
    for marker in ("HTML", "CSS activo", "JavaScript contractual", "i18n", "backend", "payload", "runtime", "execution"):
        assert marker in text
    assert protected_product_is_unchanged()
