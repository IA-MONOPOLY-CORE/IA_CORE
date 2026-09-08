"""N6 P0/P1 visual hierarchy and contract-preservation guard."""

from pathlib import Path
import subprocess

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
PRE_N6 = "9ed2ea6"
HTML = ROOT / "ui" / "web" / "index.html"
CSS = ROOT / "ui" / "web" / "styles.css"


def test_p0_route_remains_canonical_and_presentational_only():
    html = HTML.read_text(encoding="utf-8")
    for marker in (
        'data-p0-zone="state"', 'data-p0-zone="contract"', 'data-p0-zone="limits"',
        'data-p0-zone="evidence"', 'data-p0-zone="next-step"',
        'data-no-runtime="true"', 'data-no-execution="true"',
    ):
        assert marker in html, marker
    assert 'data-p0-layer="visual-hierarchy-1.180"' in html
    assert 'data-interaction-mode="read-only"' in html


def test_p1_sequence_and_contractual_anchors_are_unchanged():
    html = HTML.read_text(encoding="utf-8")
    sequence = [
        'data-p1-step="contract"', 'data-p1-step="actions"',
        'data-p1-step="boundaries"', 'data-p1-step="validation"',
    ]
    positions = [html.index(marker) for marker in sequence]
    assert positions == sorted(positions)
    for marker in (
        'data-p1-layer="contractual-second-pass-1.183"',
        'data-contract-screen="FSC-CO-01"', 'data-contract-screen="FSC-BF-02"',
        'data-contract-screen="FSC-RCP-04"', 'data-contract-screen="FSC-VR-03"',
        'backend_internal_ui_payload.v1',
    ):
        assert marker in html, marker
    assert 'data-p1-layer="contractual-second-pass-1.183"' in CSS.read_text(encoding="utf-8") or "p1-contractual" in CSS.read_text(encoding="utf-8")


def test_hierarchy_does_not_create_cta_or_operational_surface():
    html = HTML.read_text(encoding="utf-8").casefold()
    active = "\n".join((ROOT / path).read_text(encoding="utf-8").rstrip() for path in (
        "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
    )).casefold()
    for marker in ("data-no-runtime", "data-no-execution", "data-no-mutation"):
        assert marker in active, marker
    assert 'data-p0-layer="visual-hierarchy-1.180"' in html
    assert 'data-p1-layer="contractual-second-pass-1.183"' in html
    historical = "\n".join(continuity.git("show", f"{PRE_N6}:{path}") for path in (
        "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
    )).replace("\r\n", "\n").rstrip().casefold()
    assert active.replace("\r\n", "\n").rstrip() == historical


def test_n6_has_no_product_diff_and_preserves_protected_surfaces():
    n6_commit = continuity.commit_for(continuity.STATION_MESSAGES["N6"])
    assert n6_commit
    files = set(filter(None, subprocess.check_output(
        ["git", "show", "--format=", "--name-only", n6_commit], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()))
    assert files <= continuity.exact_station_paths("N6")
    assert "tests/test_ui_ux_panel_maestro_p0_p1_visual_hierarchy_1_196.py" in files
    continuity.assert_protected_product_unchanged(PRE_N6)
