"""Contract and diff guards for UI/UX 1.189 request draft visual demotion."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "72b6f71"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_1_189.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
DECISION = "UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_PASSED"
READINESS = "ready_for_ui_ux_1_190_request_draft_panel_visual_demotion_checkpoint"
NEXT_PROMPT = "PROMPT UI/UX 1.190 — Checkpoint de democión visual del Request Draft Panel del Panel Maestro IA_CORE contract-aware"

IMPLEMENTATION_FILES = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_1_189.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py",
}
HISTORICAL_ALLOWLIST_TESTS = {
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
ALLOWED_DIFF = IMPLEMENTATION_FILES | HISTORICAL_ALLOWLIST_TESTS
CONTINUITY_1_189_A = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py",
}
ALLOWED_DIFF |= CONTINUITY_1_189_A
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188 and CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
PROTECTED_FILES = {
    "ui/web/index.html", "ui/web/backend-contract-widgets.js", "ui/web/i18n_es.json",
    "ui/web/admin-panels.js", "ui/web/console-interactions.js", "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py", "api.py", "package.json", "package-lock.json",
    "pnpm-lock.yaml", "yarn.lock",
}
PROTECTED_DIRS = {"core", "domains", "providers", "tools", "scripts", "integrations", "runtime", "execution"}


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


def changed_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def test_document_records_scoped_visual_demotion_and_checkpoint_readiness():
    document = read(DOC)
    assert_markers(document, [
        "UI/UX Panel Maestro - Request Draft Panel Visual Demotion 1.189", BASE,
        "UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_MATRIX_CHECKPOINT",
        "ready_for_ui_ux_1_189_selected_visual_block_implementation", "Candidate A",
        "Request Contract Preview", "Request Draft Panel", "CSS-only", "styles.css",
        "secondary", "blocked", "read-only", "no submit", "no dispatch", "no execution",
        "no-runtime", "no endpoints", "no integrations", "no backend", "payload v2", "P0",
        "P1", "Matriz", "widgets contract-aware", "i18n", "desktop", "mobile drawer",
        "deny-by-default", "disabled", "aria-readonly", "aria-expanded", "aria-controls",
        "modelo", "herramienta", "nivel de esfuerzo", "no busca el minimo", "no busca el maximo",
        DECISION, READINESS, NEXT_PROMPT,
    ])


def test_readmes_record_implementation_and_next_checkpoint():
    for path in (README, WEB_README):
        assert_markers(read(path), [
            "UI/UX 1.189", "Request Draft Panel", "CSS-only", "read-only", "blocked",
            "no submit", "no dispatch", "no execution", "no runtime", "no backend",
            "payload v2", READINESS,
        ])


def test_index_and_widgets_preserve_existing_contract_without_new_operations():
    html = read(INDEX)
    assert html.count('id="request-draft-panel"') == 1
    assert html.count('id="request-draft-toggle"') == 1
    assert html.count('id="request-draft-blocked-control"') == 1
    assert 'readonly aria-readonly="true"' in html
    assert 'disabled data-interaction-mode="read-only"' in html
    assert 'data-contract-blocked="true"' in html
    assert 'data-no-runtime="true"' in html
    assert 'data-no-execution="true"' in html
    assert "backend_internal_ui_payload.v1" in "\n".join([html, read(STYLES), read(WIDGETS)])
    active = "\n".join([html, read(STYLES), read(WIDGETS)]).casefold()
    for token in ("backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"'):
        assert token not in active
    assert not re.search(r'>\s*(?:ready to run|processing request|capability active)\s*<', html, re.IGNORECASE)
    assert not re.search(r'data-(?:state|status)=["\'](?:running|executing|dispatching|submitted)["\']', html, re.IGNORECASE)
    assert_markers(read(WIDGETS), ["allowed_actions", "forbidden_actions", "blocked_capabilities", "no_payload", "not_available"])


def test_css_is_scoped_visible_secondary_and_non_cta_for_blocked_control():
    css = read(STYLES)
    panel_rule = re.search(r"body #request-draft-panel\.request-draft-panel \{.*?\n\}", css, re.DOTALL)
    blocked_rule = re.search(r"#request-draft-blocked-control\.request-draft-control:disabled \{.*?\n\}", css, re.DOTALL)
    assert panel_rule and blocked_rule
    demotion = panel_rule.group() + blocked_rule.group()
    assert "background: linear-gradient" not in demotion
    assert "cursor: pointer" not in blocked_rule.group()
    assert "display: none" not in demotion
    assert "visibility: hidden" not in demotion
    assert "opacity: 0.82" in blocked_rule.group()
    assert "@media (max-width: 760px)" in css
    assert "width:" not in panel_rule.group() and "transform:" not in panel_rule.group()


def test_diff_is_deny_by_default_and_contract_paths_are_untouched():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF, sorted(paths - ALLOWED_DIFF)
    assert not paths.intersection(PROTECTED_FILES)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)
    assert not any(path.startswith(".env") or "/.env" in path for path in paths)
    for path in PROTECTED_FILES:
        result = subprocess.run(["git", "diff", "--quiet", BASE, "--", path], cwd=ROOT, check=False)
        assert result.returncode == 0, f"Protected path changed: {path}"


def test_historical_allowlist_changes_are_additive_for_1_189_only():
    for path in working_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard lines removed from {path}: {removed}"
        assert "CONTINUITY_1_189" in diff


def test_guard_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source
