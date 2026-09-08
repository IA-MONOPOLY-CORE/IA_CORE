"""Closed, exact-path continuity manifest and guards for UI/UX 1.196."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "357a08d"
CSS = "ui/web/styles.css"
PRODUCT_READ_ONLY = {
    "ui/web/index.html",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
}
STATION_MESSAGES = {
    "N1": "test(ui): crear manifest de continuidad bloque 1.196",
    "N2": "test(ui): generalizar snapshots y grupos de continuidad",
    "N3": "docs(ui): inventariar cascada visual panel maestro",
    "N4": "refactor(ui): consolidar cascada css contract-aware",
    "N5": "test(ui): ampliar matriz de regresion responsive",
    "N6": "feat(ui): consolidar jerarquia visual p0 p1",
    "N7": "feat(ui): consolidar coherencia visual widgets contract-aware",
    "N8": "feat(ui): consolidar densidad transversal p2 p3",
    "N9": "feat(ui): consolidar accesibilidad y legibilidad transversal",
    "N10": "docs(ui): checkpoint bloque gran escala css accesibilidad responsive",
}
STATION_PATHS = {
    "N1": {
        "docs/UI_UX_PANEL_MAESTRO_CONTINUITY_MANIFEST_1_196.md",
        "tests/ui_ux_1_196_continuity.py",
        "tests/test_ui_ux_panel_maestro_continuity_manifest_1_196.py",
        "tests/ui_ux_1_192_scope.py",
        "tests/test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py",
        "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
        "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
        "tests/test_ui_ux_panel_maestro_assembled_block_1_194_postmortem_1_195.py",
        "tests/test_ui_ux_panel_maestro_next_large_scale_assembled_block_manifest_1_195.py",
        "tests/test_ui_ux_panel_maestro_post_assembled_block_direction_review_1_195.py",
    },
    "N2": {
        "tests/ui_ux_1_196_snapshot_groups.py",
        "tests/test_ui_ux_panel_maestro_snapshot_groups_1_196.py",
    },
    "N3": {
        "docs/UI_UX_PANEL_MAESTRO_CSS_CASCADE_INVENTORY_1_196.md",
        "tests/test_ui_ux_panel_maestro_css_cascade_inventory_1_196.py",
    },
    "N4": {
        CSS,
        "tests/test_ui_ux_panel_maestro_css_cascade_consolidation_1_196.py",
    },
    "N5": {
        "tests/test_ui_ux_panel_maestro_responsive_regression_matrix_1_196.py",
    },
    "N6": {
        "tests/test_ui_ux_panel_maestro_p0_p1_visual_hierarchy_1_196.py",
    },
    "N7": {
        "tests/test_ui_ux_panel_maestro_contract_aware_widgets_visual_coherence_1_196.py",
    },
    "N8": {
        "tests/test_ui_ux_panel_maestro_p2_p3_transversal_density_1_196.py",
    },
    "N9": {
        "tests/test_ui_ux_panel_maestro_transversal_accessibility_legibility_1_196.py",
    },
    "N10": {
        "docs/UI_UX_PANEL_MAESTRO_CSS_ACCESSIBILITY_RESPONSIVE_LARGE_SCALE_BLOCK_1_196.md",
        "tests/test_ui_ux_panel_maestro_css_accessibility_responsive_large_scale_block_1_196.py",
        "README.md",
        "ui/web/README.md",
    },
}
CONTINUITY_1_196 = set().union(*STATION_PATHS.values())
ALLOWED_TEST_ONLY = CONTINUITY_1_196 | {"README.md", "ui/web/README.md"}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def changed_paths(base: str = BASELINE, head: str = "HEAD") -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "--no-renames", base, head).splitlines()))
    untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return tracked | untracked


def commit_for(message: str) -> str | None:
    matches = [
        line.split("\t", 1)[0]
        for line in git("log", "--all", "--format=%H%x09%s").splitlines()
        if "\t" in line and line.split("\t", 1)[1] == message
    ]
    if len(matches) > 1:
        raise AssertionError(f"duplicate station commit: {message}")
    return matches[0] if matches else None


def exact_station_paths(station: str) -> set[str]:
    if station not in STATION_PATHS:
        raise AssertionError(f"unknown station: {station}")
    return set(STATION_PATHS[station])


def assert_rejects_paths(paths: set[str]) -> None:
    unexpected = set(paths) - ALLOWED_TEST_ONLY
    if unexpected:
        raise AssertionError(f"forbidden paths: {sorted(unexpected)}")


def assert_protected_product_unchanged(base: str = BASELINE, head: str = "HEAD") -> None:
    for path in PRODUCT_READ_ONLY:
        result = subprocess.run(["git", "diff", "--quiet", base, head, "--", path], cwd=ROOT)
        if result.returncode != 0:
            raise AssertionError(f"protected product changed: {path}")


def assert_no_permissive_manifest_source() -> None:
    source = (ROOT / "tests" / "ui_ux_1_196_continuity.py").read_text(encoding="utf-8")
    forbidden = (
        "g" + "l" + "o" + "b" + "(",
        "r" + "g" + "l" + "o" + "b" + "(",
        "Path." + "g" + "l" + "o" + "b",
        "*" + "*" + "/" + "*",
        "*" + ".*",
        "allow" + "_all",
        "except " + "AssertionError" + ": pass",
    )
    for marker in forbidden:
        if marker in source:
            raise AssertionError(f"permissive manifest construct: {marker}")
    for marker in ("PRODUCT_READ_ONLY", "assert_rejects_paths", "commit_for", "STATION_PATHS"):
        assert marker in source, marker


def assert_current_station_is_exact(station: str) -> None:
    assert_rejects_paths(changed_paths())
    assert_protected_product_unchanged()
    expected = exact_station_paths(station)
    current = changed_paths()
    assert current <= ALLOWED_TEST_ONLY, sorted(current - ALLOWED_TEST_ONLY)
    assert expected >= {path for path in current if path in expected}
