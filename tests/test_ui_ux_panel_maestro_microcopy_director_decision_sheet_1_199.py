"""N7 Director Decision Sheet and checkpoint tests for UI/UX 1.199."""

from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_199_support import (
    direction_packages,
    protected_product_is_unchanged,
)


ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTOR_DECISION_SHEET_1_199.md"
CHECKPOINT = ROOT / "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_REVIEW_CHECKPOINT_1_199.md"


def test_n7_decision_sheet_has_exactly_eight_director_decisions():
    text = SHEET.read_text(encoding="utf-8")
    assert "## DECISIONES QUE NECESITA TOMAR SANTI" in text
    assert "**Cantidad total: 8**" in text
    decision_headings = [line for line in text.splitlines() if line.startswith("## ") and line[3:4].isdigit()]
    assert len(decision_headings) == 8
    for index, package in enumerate(direction_packages(), start=1):
        assert f"## {index}. {package.direction_package_id}" in text
        assert str(package.occurrence_count) in text


def test_n7_decision_sheet_preserves_direction_boundary():
    text = SHEET.read_text(encoding="utf-8")
    assert "NO ES UNA DECISION DE MICROCOPY SIMPLE" in text
    assert "Lo que Santi no necesita decidir" in text
    assert "Lo que el agente puede hacer solo después de una respuesta aprobada" in text
    assert "Aprobación de patrones" in text
    assert "Cambio contractual" in text
    assert "UI/UX 1.200 no se ejecuta" in text


def test_n7_checkpoint_has_exact_verdict_and_readiness():
    text = CHECKPOINT.read_text(encoding="utf-8")
    assert "N7_MICROCOPY_DIRECTOR_DECISION_SHEET_CHECKPOINT_PASSED" in text
    assert "UI_UX_MICROCOPY_DIRECTION_DECISION_COMPRESSION_REVIEW_PASSED" in text
    assert "ready_for_ui_ux_1_200_microcopy_direction_decisions" in text
    assert "PROMPT UI/UX 1.200" in text


def test_n7_product_is_unchanged():
    assert protected_product_is_unchanged()
