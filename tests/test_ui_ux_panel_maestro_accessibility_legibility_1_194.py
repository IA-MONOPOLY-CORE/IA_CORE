"""S5 guard for visual accessibility and legibility of existing states."""

from pathlib import Path
import subprocess

import pytest

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "f5ddde4"
CSS = ROOT / "ui" / "web" / "styles.css"
S4_MESSAGE = "feat(ui): optimizar densidad visual p2 p3"
S5_MESSAGE = "feat(ui): mejorar accesibilidad y legibilidad panel maestro"
S5_CSS = scope.S5_CSS


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


def test_s5_css_is_exactly_appended_to_the_s4_snapshot():
    s4 = station_commit(S4_MESSAGE)
    assert s4, "S4 must be committed before S5"
    before = git("show", f"{s4}:ui/web/styles.css")
    s5 = station_commit(S5_MESSAGE)
    after = git("show", f"{s5}:ui/web/styles.css") if s5 else CSS.read_text(encoding="utf-8")
    assert after == before + S5_CSS
    for forbidden in ("display: none", "visibility: hidden", "opacity: 0;", "cursor: pointer", "transform:", "content:", "pointer-events"):
        assert forbidden not in S5_CSS


def test_s5_preserves_contractual_disabled_and_read_only_attributes():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    for marker in (
        'id="settings-fab" type="button" disabled aria-disabled="true" data-contract-blocked="true" data-no-runtime="true" data-no-execution="true" data-no-mutation="true"',
        'id="add-fab" type="button" disabled aria-disabled="true" data-contract-blocked="true"',
        'id="domain-fab" type="button" disabled aria-disabled="true" data-contract-blocked="true"',
        'id="request-draft-blocked-control" disabled',
        'id="request-draft-panel"',
    ):
        assert marker in html, marker


def test_s5_focus_and_legibility_rules_are_visual_only():
    assert ":focus-visible" in S5_CSS
    assert "outline: 2px solid var(--cyan)" in S5_CSS
    assert "line-height: 1.35" in S5_CSS
    assert "overflow-wrap: anywhere" in S5_CSS
    with pytest.raises(AssertionError, match="exact Gate 1/Gate 2"):
        scope.assert_css("baseline\n", "baseline\n" + scope.S1_CSS + scope.S2_CSS + scope.S3_CSS + scope.S4_CSS + S5_CSS + "\nbody { pointer-events: auto; }\n")


def test_s5_product_behavior_files_are_unchanged():
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
