"""Visual checkpoint and diff guards for UI/UX 1.189.A."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "07367d5"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"

ALLOWED_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py",
}
HISTORICAL_TESTS = {
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_185.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
}
ALLOWED_DIFF = ALLOWED_FILES | HISTORICAL_TESTS
CONTINUITY_1_190 = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_1_190.md", "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py"}
ALLOWED_DIFF |= CONTINUITY_1_190
CONTINUITY_1_191 = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_1_191.md", "tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py"}
ALLOWED_DIFF |= CONTINUITY_1_191
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188, CONTINUITY_1_189, CONTINUITY_1_189_A and CONTINUITY_1_190 remain preserved; CONTINUITY_1_191 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188, CONTINUITY_1_189 and CONTINUITY_1_189_A remain preserved; CONTINUITY_1_190 is additive.
PROTECTED = {
    "ui/web/index.html", "ui/web/backend-contract-widgets.js", "ui/web/i18n_es.json",
    "ui/web/admin-panels.js", "ui/web/console-interactions.js", "ui/web/domains.js",
    "ui/web/styles.css", "core/backend_internal_ui_payloads.py", "api.py",
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
}
PROTECTED_DIRS = {"core", "domains", "providers", "tools", "scripts", "integrations", "runtime", "execution"}
VERDICT = "UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_PASSED"
READINESS = "ready_for_ui_ux_1_190_request_draft_panel_visual_demotion_checkpoint"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return " ".join("".join(char for char in decomposed if not unicodedata.combining(char)).casefold().split())


def assert_markers(text: str, markers: list[str]) -> None:
    haystack = normalized(text)
    missing = [marker for marker in markers if normalized(marker) not in haystack]
    assert not missing, f"Missing markers: {missing}"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def working_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return {path.replace("\\", "/") for path in tracked | untracked}


def test_checkpoint_document_records_real_visual_evidence():
    assert DOC.is_file()
    assert_markers(read(DOC), [
        "UI/UX Panel Maestro Request Draft Panel Visual Demotion Fix 1.189.A", BASE,
        "UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_PASSED", READINESS,
        "helper_unknown_error", "Request Draft Panel", "desktop", "mobile", "resize",
        "clientWidth", "scrollWidth", "panel visible", "secundario", "no CTA", "no submit",
        "no runtime", "no execution", "read-only", "blocked", "P0", "P1", "Matriz", "P3",
        "widgets", "backend-contract-widgets.js", "i18n", "backend_internal_ui_payload.v1",
        "no payload v2", "no endpoints", "no integrations", "Recomendacion armonica",
        "SIN_CORRECCION_NECESARIA", VERDICT,
    ])


def test_readmes_record_visual_checkpoint_without_new_capability():
    for path in (README, WEB_README):
        assert_markers(read(path), [
            "UI/UX 1.189.A", "Request Draft Panel", "desktop", "mobile", "resize",
            "no CTA", "no submit", "no runtime", "no execution", "read-only", "blocked",
            "P0", "P1", "Matriz", "P3", "no JS contractual", "no i18n", "no backend",
            "no endpoints", "no payload v2", "1.190",
        ])


def test_contract_surface_is_preserved_and_css_was_not_changed():
    html = read(INDEX)
    css = read(STYLES)
    widgets = read(WIDGETS)
    assert subprocess.run(["git", "diff", "--quiet", BASE, "--", "ui/web/styles.css"], cwd=ROOT, check=False).returncode == 0
    assert html.count('id="request-draft-panel"') == 1
    assert 'readonly aria-readonly="true"' in html
    assert 'disabled data-interaction-mode="read-only"' in html
    assert "backend_internal_ui_payload.v1" in html
    active = "\n".join([html, css, widgets]).casefold()
    for token in ("backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"'):
        assert token not in active
    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities", "no_payload", "not_available"):
        assert token in widgets
    assert not re.search(r'>\s*(?:ready to run|processing request|capability active)\s*<', html, re.IGNORECASE)


def test_diff_is_deny_by_default_and_historical_continuity_is_additive():
    paths = working_paths()
    assert paths <= ALLOWED_DIFF, sorted(paths - ALLOWED_DIFF)
    assert not paths.intersection(PROTECTED)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)
    for path in paths.intersection(HISTORICAL_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard removal: {path}"
        assert "CONTINUITY_1_189_A" in diff


def test_guard_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source
