"""Final documentation-only review guard for UI/UX 1.195."""

from pathlib import Path
import subprocess
import unicodedata

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "307067d"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_POST_ASSEMBLED_BLOCK_DIRECTION_REVIEW_1_195.md"
TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_post_assembled_block_direction_review_1_195.py"
MESSAGE = "docs(ui): registrar revision post bloque ensamblado 1.195"
PRODUCT_FILES = {
    "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json", "ui/web/admin-panels.js", "ui/web/console-interactions.js",
    "ui/web/domains.js", "core/backend_internal_ui_payloads.py", "api.py",
}
ALLOWED = {
    "README.md", "ui/web/README.md", "tests/ui_ux_1_192_scope.py",
    "docs/UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_1_194_POSTMORTEM_1_195.md",
    "tests/test_ui_ux_panel_maestro_assembled_block_1_194_postmortem_1_195.py",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_LARGE_SCALE_ASSEMBLED_BLOCK_MANIFEST_1_195.md",
    "tests/test_ui_ux_panel_maestro_next_large_scale_assembled_block_manifest_1_195.py",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
    "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py",
    "ui/web/styles.css",
    DOC.relative_to(ROOT).as_posix(), TEST.relative_to(ROOT).as_posix(),
}
ALLOWED |= scope.CONTINUITY_1_196
ALLOWED |= scope.CONTINUITY_1_197
ALLOWED |= scope.CONTINUITY_1_198
ALLOWED |= scope.CONTINUITY_1_199


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


def test_direction_review_contains_complete_decision():
    content = normalized(read(DOC))
    for marker in (
        "ui_ux_post_assembled_block_direction_review_1_195_passed", "307067d",
        "evidencia de consumo", "post-mortem", "auditoria actual", "deudas activas",
        "cadenas candidatas", "next_large_scale_assembled_block_selected",
        "current_deterministic_station_count", "preauthorized_station_count",
        "self_bootstrapped_station_count", "hard_frontier_station_index",
        "recommended_station_count", "n1", "n2", "n3", "n4", "n5", "n6",
        "n7", "n8", "n9", "n10", "n11", "microcopy contractual",
        "preauthorized_autonomous_actions_v2", "mandatory_operator_stop_conditions_v2",
        "expected_operator_interventions_normal_path = 0", "economia de ejecucion",
        "luna alto", "luna muy alto", "no se justifica un modelo mayor",
        "no commit globo", "manifest", "no se ejecuta ui/ux 1.196",
        "ready_for_ui_ux_1_196_large_scale_assembled_block_prompt_compilation",
    ):
        assert normalized(marker) in content, marker


def test_final_review_is_documentation_only_and_commits_are_traceable():
    commit = commit_for(MESSAGE)
    files = set(filter(None, git("show", "--format=", "--name-only", commit).splitlines()))
    assert files <= {"README.md", "ui/web/README.md", DOC.relative_to(ROOT).as_posix(), TEST.relative_to(ROOT).as_posix(), "tests/test_ui_ux_panel_maestro_next_large_scale_assembled_block_manifest_1_195.py", "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py", "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py", "tests/test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py"}
    changed = set(filter(None, git("diff", "--name-only", BASE, "HEAD").splitlines()))
    assert changed <= ALLOWED, sorted(changed - ALLOWED)
    for path in PRODUCT_FILES - {"ui/web/styles.css"}:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path
    assert "CONTINUITY_1_195" in read(ROOT / "tests" / "ui_ux_1_192_scope.py")


def test_final_review_keeps_contract_and_next_prompt_unexecuted():
    active = "\n".join(read(ROOT / path) for path in (
        "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
        "core/backend_internal_ui_payloads.py",
    )).casefold()
    assert "backend_internal_ui_payload.v1" in active
    for forbidden in ("backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"'):
        assert forbidden not in active, forbidden
    content = normalized(read(DOC))
    assert "no se ejecuta ui/ux 1.196" in content
    assert "no se modificaron producto" in content
