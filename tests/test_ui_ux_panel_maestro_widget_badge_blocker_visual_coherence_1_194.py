"""S3 guard for presentational coherence of existing widgets and blockers."""

from pathlib import Path
import subprocess

import pytest

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "f5ddde4"
CSS = ROOT / "ui" / "web" / "styles.css"
S1_MESSAGE = "feat(ui): corregir containment responsive panel maestro"
S2_MESSAGE = "feat(ui): consolidar severidad visual existente"
S3_MESSAGE = "feat(ui): unificar coherencia visual widgets badges blockers"
S3_CSS = scope.S3_CSS


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


def test_s3_css_is_exactly_appended_to_the_s2_snapshot():
    s2 = station_commit(S2_MESSAGE)
    assert s2, "S2 must be committed before S3"
    before = git("show", f"{s2}:ui/web/styles.css")
    s3 = station_commit(S3_MESSAGE)
    after = git("show", f"{s3}:ui/web/styles.css") if s3 else CSS.read_text(encoding="utf-8")
    assert after == before + S3_CSS
    assert "#functional-widgets" in S3_CSS
    assert "display: none" not in S3_CSS
    assert "opacity: 0" not in S3_CSS
    assert "cursor: pointer" not in S3_CSS
    assert "transform:" not in S3_CSS
    assert "data-contract-state=\"active\"" not in S3_CSS


def test_s3_preserves_widget_inventory_and_contract_attributes():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    assert html.count('class="data-widget"') == 4
    assert html.count('<p class="data-widget-fallback"') == 4
    for marker in (
        'id="functional-widgets"',
        'data-contract-state="no_payload"',
        'data-contract-state="not_available"',
        'data-contract-state="blocked"',
        'data-contract-state="pending"',
        'backend_internal_ui_payload.v1',
        'data-component="ia-panel ia-blocker"',
    ):
        assert marker in html, marker


def test_s3_product_behavior_and_payload_surfaces_are_unchanged():
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


def test_s3_rejects_hidden_widgets_or_operational_visuals():
    invalid = "\n#functional-widgets .data-widget { display: none; transform: translateY(-4px); }\n"
    with pytest.raises(AssertionError, match="exact Gate 1/Gate 2"):
        scope.assert_css("baseline\n", "baseline\n" + scope.S1_CSS + scope.S2_CSS + S3_CSS + invalid)
