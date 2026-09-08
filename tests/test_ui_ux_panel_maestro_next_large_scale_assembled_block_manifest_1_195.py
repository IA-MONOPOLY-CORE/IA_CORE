"""Guard for the read-only next large-scale block manifest of UI/UX 1.195."""

from pathlib import Path
import subprocess
import unicodedata

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "307067d"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_LARGE_SCALE_ASSEMBLED_BLOCK_MANIFEST_1_195.md"
TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_next_large_scale_assembled_block_manifest_1_195.py"
MESSAGE = "docs(ui): definir siguiente escala de bloques ensamblados"
PRODUCT_FILES = {
    "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json", "ui/web/admin-panels.js", "ui/web/console-interactions.js",
    "ui/web/domains.js", "core/backend_internal_ui_payloads.py", "api.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def commit_for(message: str) -> str:
    matches = [line.split("\t", 1)[0] for line in git("log", "--all", "--format=%H%x09%s").splitlines() if "\t" in line and line.split("\t", 1)[1] == message]
    assert len(matches) == 1, message
    return matches[0]


def test_manifest_defines_scale_and_hard_frontier():
    content = normalized(read(DOC))
    for marker in (
        "next_large_scale_assembled_block_selected", "css cascade, accessibility and responsive regression",
        "prompt ui/ux 1.196", "current_deterministic_station_count", "8",
        "preauthorized_station_count", "9", "self_bootstrapped_station_count", "10",
        "hard_frontier_station_index", "11", "recommended_station_count", "10",
        "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10",
        "n11", "microcopy contractual", "manifest_passed",
    ):
        assert normalized(marker) in content, marker


def test_manifest_has_dependencies_gates_commits_tests_browser_and_rollback():
    content = normalized(read(DOC))
    for marker in (
        "dependencia", "archivos permitidos", "archivos prohibidos", "tests:",
        "browser:", "gate pass", "gate fail", "commit:", "rollback:",
        "mandatory_stop", "preauthorized_autonomous_actions_v2",
        "mandatory_operator_stop_conditions_v2", "expected_operator_interventions_normal_path = 0",
        "no commit globo", "station_already_compliant_no_change", "suite historica completa",
    ):
        assert normalized(marker) in content, marker


def test_manifest_commit_is_documentation_only_and_product_is_unchanged():
    commit = commit_for(MESSAGE)
    files = set(filter(None, git("show", "--format=", "--name-only", commit).splitlines()))
    assert files <= {DOC.relative_to(ROOT).as_posix(), TEST.relative_to(ROOT).as_posix()}
    changed = set(filter(None, git("diff", "--name-only", BASE, "HEAD").splitlines()))
    assert changed <= ({
        "tests/ui_ux_1_192_scope.py",
        "docs/UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_1_194_POSTMORTEM_1_195.md",
        "tests/test_ui_ux_panel_maestro_assembled_block_1_194_postmortem_1_195.py",
        DOC.relative_to(ROOT).as_posix(), TEST.relative_to(ROOT).as_posix(),
        "docs/UI_UX_PANEL_MAESTRO_POST_ASSEMBLED_BLOCK_DIRECTION_REVIEW_1_195.md",
        "tests/test_ui_ux_panel_maestro_post_assembled_block_direction_review_1_195.py",
        "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
        "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
        "tests/test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py",
        "README.md", "ui/web/README.md", "ui/web/styles.css",
    } | scope.CONTINUITY_1_196)
    for path in PRODUCT_FILES - {"ui/web/styles.css"}:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path
    helper = normalized(read(ROOT / "tests" / "ui_ux_1_192_scope.py"))
    assert "continuity_1_195" in helper
    assert "no payload v2" in normalized(read(DOC))
