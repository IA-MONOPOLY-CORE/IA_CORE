"""N1 read-only product integrity gate for UI/UX 1.201."""

from pathlib import Path
import subprocess

from ui_ux_panel_maestro_microcopy_1_200_support import EXPECTED_GEOMETRY_CSS, baseline_bytes


ROOT = Path(__file__).resolve().parents[1]
CURRENT = "a2afc307d7278657a324efba345c04e28c39525a"
PRODUCT_BASELINE = "4618c59"


def _git_diff_names(*args):
    return set(subprocess.check_output(
        ["git", "diff", "--name-only", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines())


def test_n1_current_product_is_unchanged_after_1_200():
    assert _git_diff_names(CURRENT, "--", "ui/web", "api.py", "core/backend_internal_ui_payloads.py") == set()


def test_n1_historical_product_diff_has_only_the_authorized_css_block():
    changed = _git_diff_names(PRODUCT_BASELINE, CURRENT, "--", "ui/web")
    assert changed - {"ui/web/README.md"} == {"ui/web/styles.css"}
    baseline = baseline_bytes("ui/web/styles.css").replace(b"\r\n", b"\n").decode()
    current = (ROOT / "ui" / "web" / "styles.css").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert current == baseline + EXPECTED_GEOMETRY_CSS


def test_n1_css_scope_is_geometry_only_and_contract_surfaces_are_read_only():
    css = (ROOT / "ui" / "web" / "styles.css").read_text(encoding="utf-8")
    assert css.count("UI/UX 1.200 N5") == 1
    assert "data-main-console-zone=\"readiness\"" in css
    assert ".layout-value" in css
    assert ".state-guidance-card" in css
    assert "#request-draft-panel.request-draft-panel.collapsed" in css
    assert "display: none" not in css[css.index("UI/UX 1.200 N5"):]
    assert "pointer-events: none" not in css[css.index("UI/UX 1.200 N5"):]
    assert "payload" not in css[css.index("UI/UX 1.200 N5"):].lower()


def test_n1_contract_files_remain_at_product_baseline():
    assert _git_diff_names(PRODUCT_BASELINE, CURRENT, "--", "ui/web/index.html", "ui/web/i18n_es.json") == set()
    assert _git_diff_names(PRODUCT_BASELINE, CURRENT, "--", "api.py", "core/backend_internal_ui_payloads.py") == set()
