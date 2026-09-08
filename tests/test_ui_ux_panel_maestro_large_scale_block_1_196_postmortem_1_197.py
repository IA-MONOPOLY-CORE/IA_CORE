"""Documentary guard for the 1.196 postmortem."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_LARGE_SCALE_BLOCK_1_196_POSTMORTEM_1_197.md"
BASELINE = "8b4ce90"
HISTORICAL_HEAD = "d386c37"
PROTECTED = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def test_postmortem_contains_all_stations_and_verdicts():
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "large_scale_block_1_196_postmortem_passed",
        "eebb0e3",
        "c135472",
        "4136abb",
        "278d7fe",
        "9ed2ea6",
        "48036f6",
        "bdcea87",
        "c1cb001",
        "f73fa78",
        "8b4ce90",
        "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10",
        "mixed_with_justification",
        "already_compliant_validated",
        "155 passed",
        "microcopy contractual",
    ):
        assert marker in content, marker


def test_postmortem_is_documentary_and_protected_product_is_unchanged():
    for path in PROTECTED:
        assert subprocess.run(
            ["git", "diff", "--quiet", BASELINE, HISTORICAL_HEAD, "--", path],
            cwd=ROOT,
        ).returncode == 0, path
    changed = set(filter(None, git("diff", "--name-only", BASELINE, HISTORICAL_HEAD).splitlines()))
    assert not (changed & PROTECTED), sorted(changed & PROTECTED)
    assert "ui/web/index.html" not in git("diff", "--name-only", BASELINE, HISTORICAL_HEAD)


def test_postmortem_preserves_non_operational_boundary():
    content = " ".join(DOC.read_text(encoding="utf-8").casefold().split())
    for marker in (
        "no implementa microcopy",
        "no ejecuta ui/ux 1.198",
        "payload v2",
            "runtime, execution",
            "no se agregan acciones",
            "ni submit",
    ):
        assert marker in content, marker
