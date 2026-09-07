"""S1 guard for the authorized responsive boundary containment correction."""

from pathlib import Path
import subprocess

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "f5ddde4"
CSS = ROOT / "ui" / "web" / "styles.css"
STATION_MESSAGE = "feat(ui): corregir containment responsive panel maestro"
S1_CSS = scope.S1_CSS
PROTECTED = (
    "ui/web/index.html",
    "ui/web/console-interactions.js",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def station_commit() -> str | None:
    matches = [
        line.split("\t", 1)[0]
        for line in git("log", "--all", "--format=%H%x09%s").splitlines()
        if "\t" in line and line.split("\t", 1)[1] == STATION_MESSAGE
    ]
    assert len(matches) <= 1, "S1 station commit must remain unique"
    return matches[0] if matches else None


def test_s1_css_is_exactly_scoped_to_existing_collapsed_disclosure():
    before = git("show", f"{BASE}:ui/web/styles.css")
    commit = station_commit()
    after = git("show", f"{commit}:ui/web/styles.css") if commit else CSS.read_text(encoding="utf-8")
    assert after == before + S1_CSS
    assert S1_CSS.count("{") == S1_CSS.count("}") == 1
    assert "#request-draft-panel.request-draft-panel.collapsed" in S1_CSS
    assert "translateX(calc(100% - 45px)) !important" in S1_CSS
    assert "display: none" not in S1_CSS
    assert "opacity: 0" not in S1_CSS


def test_s1_preserves_product_contract_and_behavior_files():
    for path in PROTECTED:
        assert subprocess.run(
            ["git", "diff", "--quiet", BASE, "HEAD", "--", path],
            cwd=ROOT,
            check=False,
        ).returncode == 0, path
    assert CSS.read_text(encoding="utf-8") != git("show", f"{BASE}:ui/web/styles.css")


def test_s1_scope_guard_rejects_unscoped_or_operational_css():
    before = "baseline\n"
    with_invalid = before + S1_CSS + "\nbody { overflow: hidden; }\n"
    try:
        scope.assert_css(before, with_invalid)
    except AssertionError:
        pass
    else:
        raise AssertionError("unscoped CSS must be rejected")


def test_s1_continuity_artifact_is_closed_and_no_html_change_is_allowed():
    assert "tests/test_ui_ux_panel_maestro_responsive_boundary_containment_1_194.py" in scope.CONTINUITY_1_194
    assert "ui/web/index.html" not in scope.CONTINUITY_1_194
    assert (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8") == git("show", f"{BASE}:ui/web/index.html")
