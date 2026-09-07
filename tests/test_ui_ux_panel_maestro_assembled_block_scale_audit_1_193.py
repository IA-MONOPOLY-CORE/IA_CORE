"""Read-only contract and scope guard for the UI/UX 1.193 scale audit."""

from pathlib import Path
import subprocess
import unicodedata

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "ca9a8c8"
CHECKPOINT = "ef5a83d"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_SCALE_AUDIT_1_193.md"
PRODUCT_FILES = {
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
ALLOWED_FILES = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "tests/ui_ux_1_192_scope.py",
    "docs/UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_CHECKPOINT_1_193.md",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
    "docs/UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_SCALE_AUDIT_1_193.md",
    "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
}
ALLOWED_FILES |= scope.CONTINUITY_1_194


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return " ".join("".join(c for c in decomposed if not unicodedata.combining(c)).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def all_changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", BASE, "HEAD").splitlines()))
    working = set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return tracked | working


def test_audit_document_contains_required_scale_contract():
    assert DOC.is_file()
    content = normalized(read(DOC))
    markers = [
        "UI/UX Panel Maestro Assembled Block Scale Audit 1.193",
        "ef5a83d", "GPT-5.6 Luna Muy Alto", "assembled mission", "bloque ensamblado",
        "six natural stations", "station 1", "station 2", "station 3", "station 4",
        "station 5", "station 6", "dependencies", "commit", "gate", "pass", "stop",
        "rollback", "conditional autonomy", "autonomia condicionada", "predictable problems",
        "problemas previsibles", "preauthorization", "preautorizaciones", "genuine stop",
        "genuine nondeterministic frontier", "TECHNICAL_REAL_LIMIT",
        "CONTRACTUAL_REAL_LIMIT", "ARCHITECTURAL_REAL_LIMIT", "TEST_INFRASTRUCTURE_LIMIT",
        "GUARD_INFRASTRUCTURE_LIMIT", "PERMISSION_LIMIT", "PROMPT_DESIGN_LIMIT",
        "CONTEXT_LIMIT", "HUMAN_APPROVAL_LIMIT", "CONSERVATIVE_ASSUMPTION",
        "recommended size today", "potential expanded size", "first genuinely nondeterministic frontier",
        "NO_GLOBAL_PRODUCT_COMMIT_REQUIRED", "partial execution", "resume", "validations",
        "browser", "next prompt", "UI_UX_CONTROLLED_DOUBLE_SCOPE_CHECKPOINT_AND_ASSEMBLED_BLOCK_SCALE_AUDIT_PASSED",
        "ready_for_ui_ux_1_194_assembled_block_execution_prompt_design", "not executed",
    ]
    missing = [marker for marker in markers if normalized(marker) not in content]
    assert not missing, missing


def test_audit_has_six_traceable_station_commits_and_stops_before_semantic_frontier():
    content = normalized(read(DOC))
    for message in (
        "fix(ui): estabilizar contencion responsive del panel maestro",
        "feat(ui): armonizar severidad estados contract-aware",
        "feat(ui): alinear widgets badges y blockers",
        "feat(ui): refinar densidad p2 p3 sin perdida de evidencia",
        "fix(ui): cerrar legibilidad accesibilidad estados documentales",
        "docs(ui): checkpoint bloque ensamblado contract-state coherence",
    ):
        assert normalized(message) in content, message
    assert "microcopy contractual" in content
    assert "motion" in content
    assert "no_global_product_commit_required" in content


def test_product_and_protected_paths_remain_unchanged():
    assert all_changed_paths() <= ALLOWED_FILES, sorted(all_changed_paths() - ALLOWED_FILES)
    for path in PRODUCT_FILES - {"ui/web/styles.css"}:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path
    current_css = (ROOT / "ui/web/styles.css").read_text(encoding="utf-8")
    scope.assert_css(scope.text(scope.git(ROOT, "show", f"{scope.BASE}:{scope.CSS}")), current_css, ROOT)
    unexpected_1_194 = {path for path in all_changed_paths() if "1_194" in path} - scope.CONTINUITY_1_194
    assert not unexpected_1_194


def test_checkpoint_precedes_audit_and_continuity_guard_is_closed():
    assert subprocess.run(["git", "merge-base", "--is-ancestor", CHECKPOINT, "HEAD"], cwd=ROOT, check=False).returncode == 0
    helper = read(ROOT / "tests" / "ui_ux_1_192_scope.py")
    assert "CONTINUITY_1_193" in helper
    assert "assembled_block_scale_audit_1_193.py" in helper


def test_no_new_operational_semantics_are_proposed_as_current():
    content = normalized(read(DOC))
    for marker in ("no new actions", "no new permissions", "no permissions", "payload v2", "no runtime", "no execution", "no endpoints", "no integrations"):
        assert marker in content, marker
    assert "the next prompt is proposed, not executed" in content
