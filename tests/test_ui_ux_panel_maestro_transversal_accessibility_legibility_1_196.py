"""N9 CSS-only accessibility and legibility guard."""

from pathlib import Path
import subprocess
import re

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
PRE_N9 = "c1cb001"
CSS = ROOT / "ui" / "web" / "styles.css"
HTML = ROOT / "ui" / "web" / "index.html"


def test_css_covers_focus_wrapping_disabled_and_long_label_legibility():
    css = CSS.read_text(encoding="utf-8")
    for marker in (
        ":focus-visible", "outline: 2px solid", "outline-offset: 2px",
        "overflow-wrap: anywhere", "line-height: 1.35", "min-width: 0",
        "[data-contract-blocked=\"true\"]:disabled[aria-disabled=\"true\"]",
    ):
        assert marker in css, marker
    relevant = css[css.index("/* UI/UX 1.194 S5:"):]
    assert not re.search(r"opacity\s*:\s*0\s*;", relevant)
    assert not re.search(r"visibility\s*:\s*hidden\s*;", relevant)


def test_disabled_and_blocked_evidence_remain_readable_and_non_operational():
    html = HTML.read_text(encoding="utf-8").casefold()
    for marker in (
        'disabled', 'aria-disabled="true"', 'data-contract-blocked="true"',
        'data-no-runtime="true"', 'data-no-execution="true"',
        'data-no-mutation="true"', 'data-interaction-mode="read-only"',
    ):
        assert marker in html, marker
    assert "payload v2" not in html


def test_n9_is_css_and_test_only_and_protected_files_match_n8():
    n9_commit = continuity.commit_for(continuity.STATION_MESSAGES["N9"])
    if n9_commit:
        files = set(filter(None, subprocess.check_output(
            ["git", "show", "--format=", "--name-only", n9_commit], cwd=ROOT, text=True, encoding="utf-8"
        ).splitlines()))
        assert files <= continuity.exact_station_paths("N9")
    else:
        assert subprocess.run(["git", "diff", "--quiet", PRE_N9, "HEAD", "--", "ui/web/styles.css"], cwd=ROOT).returncode == 0
    continuity.assert_protected_product_unchanged(PRE_N9)
    for path in (
        "ui/web/index.html", "ui/web/backend-contract-widgets.js", "ui/web/i18n_es.json",
        "core/backend_internal_ui_payloads.py", "api.py",
    ):
        current = (ROOT / path).read_text(encoding="utf-8")
        historical = continuity.git("show", f"{PRE_N9}:{path}")
        assert current.replace("\r\n", "\n").rstrip() == historical.replace("\r\n", "\n").rstrip(), path
