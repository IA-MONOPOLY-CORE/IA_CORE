from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CURRENT_LINE_CLOSURE_AND_HANDOFF_1_204.md"
N1 = ROOT / "docs" / "UI_UX_CURRENT_BOOK_OBJECTIVE_COVERAGE_AUDIT_1_204.md"
N2 = ROOT / "docs" / "UI_UX_INTEGRAL_CONTRACT_NO_GHOST_AUDIT_1_204.md"
N3 = ROOT / "docs" / "UI_UX_INTEGRAL_VISUAL_RESPONSIVE_ACCESSIBILITY_AUDIT_1_204.md"
N4 = ROOT / "docs" / "UI_UX_INTEGRAL_REGRESSION_DEBT_CLASSIFICATION_1_204.md"

PRODUCT_SURFACES = (
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/admin-panels.js",
    "ui/web/backend-contract-widgets.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "ui/web/i18n.js",
    "api.py",
    "core/backend_internal_ui_payloads.py",
)


def test_current_line_closure_contract_is_explicit():
    text = DOC.read_text(encoding="utf-8")
    assert "UI_UX_CURRENT_LINE_CLOSED" in text
    assert "CURRENT_UI_UX_BASELINE=PRESERVED_AND_CLOSED" in text
    assert "DIRECTION_DECISION=B_PRESERVE_BASELINE" in text
    assert "SEMANTIC_CONTRACTUAL_EXTENSION=NOT_AUTHORIZED_IN_UI_LAYER" in text
    assert "N5_UI_UX_1_204_CLOSURE_DECISION_CLOSED" in text


def test_integral_audits_are_present_and_green():
    for path, marker in (
        (N1, "N1_UI_UX_1_204_BOOK_COVERAGE_AUDIT_PASSED"),
        (N2, "N2_UI_UX_1_204_INTEGRAL_CONTRACT_AUDIT_PASSED"),
        (N3, "N3_UI_UX_1_204_VISUAL_RESPONSIVE_ACCESSIBILITY_AUDIT_PASSED"),
        (N4, "N4_UI_UX_1_204_REGRESSION_CLASSIFICATION_PASSED"),
    ):
        text = path.read_text(encoding="utf-8")
        assert marker in text
        normalized = text.lower()
        assert (
            "blocking_gap: 0" in normalized
            or "blocking_gaps: 0" in normalized
            or "blocking: 0" in normalized
            or "no visual, responsive or accessibility blocker" in normalized
            or "no current contract ghost and no blocking contract gap" in normalized
        )


def test_protected_product_surfaces_are_unchanged_from_1_203():
    import subprocess

    for surface in PRODUCT_SURFACES:
        result = subprocess.run(
            ["git", "diff", "--quiet", "c2794799", "--", surface],
            cwd=ROOT,
            check=False,
        )
        assert result.returncode == 0, surface
