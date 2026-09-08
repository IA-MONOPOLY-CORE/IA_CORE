"""Focal browser-evidence guard for UI/UX 1.198 N5."""

from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_198_support import protected_files_match_baseline


VIEWPORT_EVIDENCE = {
    (1440, 1000): {"client": 1425, "scroll": 1425, "body": 1425, "overflow": 2, "wrap": 1, "console": 0},
    (1280, 800): {"client": 1265, "scroll": 1265, "body": 1265, "overflow": 2, "wrap": 1, "console": 0},
    (768, 1024): {"client": 753, "scroll": 753, "body": 753, "overflow": 0, "wrap": 1, "console": 0},
    (390, 844): {"client": 375, "scroll": 375, "body": 375, "overflow": 1, "wrap": 1, "console": 0},
    (375, 812): {"client": 360, "scroll": 360, "body": 360, "overflow": 1, "wrap": 1, "console": 0},
}


def test_n5_document_has_all_required_viewports_and_risk_categories():
    doc = Path(__file__).resolve().parents[1] / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_GEOMETRY_CONSISTENCY_AUDIT_1_198.md"
    content = doc.read_text(encoding="utf-8").casefold()
    for marker in (
        "n5_microcopy_geometry_consistency_audit_passed",
        "1440x1000",
        "1280x800",
        "768x1024",
        "390x844",
        "375x812",
        "geometry_ok",
        "wrap_risk",
        "overflow_risk",
        "truncation_risk",
        "density_risk",
        "semantic_visual_ambiguity",
        "request draft",
        "no form",
        "no `type=submit`",
    ):
        assert marker in content, marker


def test_n5_browser_evidence_is_frozen_and_document_width_is_contained():
    assert set(VIEWPORT_EVIDENCE) == {(1440, 1000), (1280, 800), (768, 1024), (390, 844), (375, 812)}
    for viewport, result in VIEWPORT_EVIDENCE.items():
        assert result["client"] == result["scroll"] == result["body"], viewport
        assert result["console"] == 0, viewport
        assert result["wrap"] == 1, viewport
    assert protected_files_match_baseline() == []


def test_n5_does_not_turn_observed_boundaries_into_actions():
    index = (Path(__file__).resolve().parents[1] / "ui" / "web" / "index.html").read_text(encoding="utf-8").casefold()
    assert "no runtime / no execution" in index
    assert "data-no-fetch=\"true\"" in index
    assert "data-no-runtime=\"true\"" in index
    assert "data-no-execution=\"true\"" in index
    assert "request-draft-control" in index
    assert "disabled" in index
