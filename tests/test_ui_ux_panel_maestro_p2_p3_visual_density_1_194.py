"""S4 guard for P2/P3 density improvements without evidence loss."""

from pathlib import Path
import subprocess

import pytest

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "f5ddde4"
CSS = ROOT / "ui" / "web" / "styles.css"
S3_MESSAGE = "feat(ui): unificar coherencia visual widgets badges blockers"
S4_MESSAGE = "feat(ui): optimizar densidad visual p2 p3"
S4_CSS = scope.S4_CSS


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def station_commit(message: str) -> str | None:
    matches = [
        line.split("\t", 1)[0]
        for line in git("log", "--all", "--format=%H%x09%s").splitlines()
        if "\t" in line and line.split("\t", 1)[1] == message
    ]
    assert len(matches) <= 1, f"station commit must remain unique: {message}"
    return matches[0] if matches else None


def test_s4_css_is_exactly_appended_to_the_s3_snapshot():
    s3 = station_commit(S3_MESSAGE)
    assert s3, "S3 must be committed before S4"
    before = git("show", f"{s3}:ui/web/styles.css")
    s4 = station_commit(S4_MESSAGE)
    after = git("show", f"{s4}:ui/web/styles.css") if s4 else CSS.read_text(encoding="utf-8")
    assert after == before + S4_CSS
    for forbidden in ("display: none", "visibility: hidden", "opacity: 0", "height: 0", "overflow: hidden", "overflow: clip"):
        assert forbidden not in S4_CSS


def test_s4_preserves_p0_p1_matrix_widgets_and_request_draft_inventory():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    assert html.count('class="closure-matrix-row"') == 20
    assert html.count('<span class="closure-matrix-badge') == 26
    for marker in (
        'data-p0-layer="visual-hierarchy-1.180"',
        'data-p1-layer="contractual-second-pass-1.183"',
        'id="functional-widgets"',
        'id="request-draft-panel"',
        'data-density-tier="secondary"',
    ):
        assert marker in html, marker


def test_s4_rejects_evidence_hiding_and_operational_visual_changes():
    invalid = "\n#closure-matrix-ui-ux-1x .closure-matrix-row { display: none; opacity: 0; }\n"
    with pytest.raises(AssertionError, match="exact Gate 1/Gate 2"):
        scope.assert_css("baseline\n", "baseline\n" + scope.S1_CSS + scope.S2_CSS + scope.S3_CSS + S4_CSS + invalid)


def test_s4_product_contract_files_are_unchanged():
    for path in (
        "ui/web/index.html",
        "ui/web/console-interactions.js",
        "ui/web/backend-contract-widgets.js",
        "ui/web/i18n_es.json",
        "ui/web/admin-panels.js",
        "ui/web/domains.js",
        "core/backend_internal_ui_payloads.py",
        "api.py",
    ):
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path
