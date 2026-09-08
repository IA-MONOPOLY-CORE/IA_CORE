"""N10 integral checkpoint and restore-point guard for UI/UX 1.196."""

from pathlib import Path
import subprocess

import ui_ux_1_196_continuity as continuity
import ui_ux_1_196_snapshot_groups as groups


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CSS_ACCESSIBILITY_RESPONSIVE_LARGE_SCALE_BLOCK_1_196.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
HASHES = {
    "N1": "eebb0e3", "N2": "c135472", "N3": "4136abb", "N4": "278d7fe",
    "N5": "9ed2ea6", "N6": "48036f6", "N7": "bdcea87", "N8": "c1cb001", "N9": "f73fa78",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def test_n10_document_contains_integral_contract_and_restore_point():
    content = DOC.read_text(encoding="utf-8").casefold()
    for marker in (
        "baseline", "gpt-5.6 luna", "muy alto", "n1-n10", "g1", "g2", "g3",
        "1874", "1866", "1440x1000", "1280x800", "768x1024", "390x844", "375x812",
        "clientwidth", "scrollwidth", "overflow", "consola", "p0", "p1", "20 filas",
        "26 badges", "4 widgets", "request draft panel", "backend_internal_ui_payload.v1",
        "payload v2", "no runtime", "no execution", "microcopy contractual", "motion",
        "audiovisual", "no commit globo", "restore point", "readiness", "1.197",
        "no se redacta ni implementa microcopy",
    ):
        assert marker in content, marker


def test_n10_station_chain_is_ordered_and_hashes_are_traceable():
    previous = None
    for station in ("N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9"):
        commit = continuity.commit_for(continuity.STATION_MESSAGES[station])
        assert commit and commit.startswith(HASHES[station]), station
        if previous:
            assert subprocess.run(["git", "merge-base", "--is-ancestor", previous, commit], cwd=ROOT).returncode == 0
        previous = commit


def test_n10_allowed_diff_is_closed_and_protected_product_is_unchanged():
    allowed = continuity.CONTINUITY_1_196 | {"README.md", "ui/web/README.md", "ui/web/styles.css"}
    changed = continuity.changed_paths()
    assert changed <= allowed, sorted(changed - allowed)
    continuity.assert_protected_product_unchanged()
    current_css = (ROOT / "ui" / "web" / "styles.css").read_text(encoding="utf-8")
    n4_css = groups.snapshot(groups.SnapshotRef(HASHES["N4"], "ui/web/styles.css"))
    assert current_css.replace("\r\n", "\n").rstrip() == n4_css.replace("\r\n", "\n").rstrip()
    for path in (README, WEB_README):
        content = path.read_text(encoding="utf-8").casefold()
        for marker in ("ui/ux 1.196", "no runtime", "no execution", "payload v2", "no se ejecuta ui/ux 1.197"):
            assert marker in content, (path, marker)
    active = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in (
        "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
        "core/backend_internal_ui_payloads.py",
    )).casefold()
    for forbidden in ("backend_internal_ui_payload.v2", "payload.v2", "schema_version\": \"v2\""):
        assert forbidden not in active, forbidden
