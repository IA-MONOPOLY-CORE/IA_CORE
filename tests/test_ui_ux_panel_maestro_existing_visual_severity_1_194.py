"""S2 guard for existing blocked, forbidden and deferred visual severity."""

from pathlib import Path
import subprocess

import pytest

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "f5ddde4"
CSS = ROOT / "ui" / "web" / "styles.css"
STATION_MESSAGE = "feat(ui): consolidar severidad visual existente"
S1_MESSAGE = "feat(ui): corregir containment responsive panel maestro"
S2_CSS = scope.S2_CSS


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


def test_s2_css_is_exactly_appended_to_the_s1_snapshot():
    s1 = station_commit(S1_MESSAGE)
    assert s1, "S1 must be committed before S2"
    before = git("show", f"{s1}:ui/web/styles.css")
    s2 = station_commit(STATION_MESSAGE)
    after = git("show", f"{s2}:ui/web/styles.css") if s2 else CSS.read_text(encoding="utf-8")
    assert after == before + S2_CSS
    assert S2_CSS.count("{") == S2_CSS.count("}") == 2
    assert "cursor: pointer" not in S2_CSS
    assert "display: none" not in S2_CSS
    assert "opacity: 0" not in S2_CSS
    assert "transform:" not in S2_CSS
    assert "animation:" not in S2_CSS


def test_s2_uses_only_existing_contract_state_tokens():
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    for marker in (
        'visual-state blocked',
        'visual-state contract-limit',
        'visual-state deferred',
        'visual-state boundary',
        'contract-chip blocked',
    ):
        assert marker in html, marker
    for forbidden in ("data-state-severity=\"new\"", "data-state=\"active\"", "data-action=\"run\""):
        assert forbidden not in html


def test_s2_does_not_touch_html_or_contract_behavior_files():
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


def test_s2_rejects_unscoped_or_operational_additions():
    invalid = "\nbody { color: red; }\n"
    with pytest.raises(AssertionError, match="exact Gate 1/Gate 2"):
        scope.assert_css("baseline\n", "baseline\n" + scope.S1_CSS + S2_CSS + invalid)
