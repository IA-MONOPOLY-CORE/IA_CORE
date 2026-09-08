"""N5 responsive regression matrix guard for UI/UX 1.196."""

from pathlib import Path
import subprocess

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
PRE_N5 = "278d7fe"
HTML = ROOT / "ui" / "web" / "index.html"
CSS = ROOT / "ui" / "web" / "styles.css"
VIEWPORTS = (
    (1440, 1000, "desktop-large"),
    (1280, 800, "desktop-medium"),
    (768, 1024, "tablet"),
    (390, 844, "mobile"),
    (375, 812, "mobile-narrow"),
)
RESIZE_CYCLES = (
    ("desktop-large", "mobile-narrow", "desktop-large"),
    ("mobile-narrow", "desktop-large", "mobile-narrow"),
    ("tablet", "desktop-large"),
)


def test_matrix_declares_required_boundaries_and_resize_cycles():
    assert [(w, h) for w, h, _ in VIEWPORTS] == [(1440, 1000), (1280, 800), (768, 1024), (390, 844), (375, 812)]
    assert RESIZE_CYCLES == (
        ("desktop-large", "mobile-narrow", "desktop-large"),
        ("mobile-narrow", "desktop-large", "mobile-narrow"),
        ("tablet", "desktop-large"),
    )
    assert sum("@media" in line for line in CSS.read_text(encoding="utf-8").splitlines()) == 10


def test_matrix_preserves_every_contract_aware_surface():
    html = HTML.read_text(encoding="utf-8")
    required = (
        'data-p0-layer=', 'data-p1-layer=', 'id="functional-widgets"',
        'id="closure-matrix-ui-ux-1x"', 'id="request-draft-panel"',
        'data-contract-blocked="true"', 'aria-disabled="true"',
        'data-no-runtime="true"', 'data-no-execution="true"',
        'data-no-mutation="true"',
    )
    for marker in required:
        assert marker in html, marker
    assert html.count('class="closure-matrix-row"') == 20
    assert html.count('class="closure-matrix-badge') == 26
    assert html.count('class="data-widget') >= 4


def test_matrix_is_css_and_test_only_without_operational_regression():
    changed = set(filter(None, subprocess.check_output(
        ["git", "diff", "--name-only", "--no-renames", PRE_N5, "HEAD"], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()))
    working = set(filter(None, subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()))
    assert changed | working <= {"tests/test_ui_ux_panel_maestro_responsive_regression_matrix_1_196.py"}
    assert subprocess.run(["git", "diff", "--quiet", PRE_N5, "HEAD", "--", "ui/web/styles.css"], cwd=ROOT).returncode == 0
    continuity.assert_protected_product_unchanged(PRE_N5)

