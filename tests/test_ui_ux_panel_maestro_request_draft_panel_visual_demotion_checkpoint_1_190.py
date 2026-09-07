"""Formal checkpoint and deny-by-default guards for UI/UX 1.190."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "cef7b11"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_1_190.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
BACKEND = ROOT / "core" / "backend_internal_ui_payloads.py"

ALLOWED_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_1_190.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py",
}
HISTORICAL_TESTS = {
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py",
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
PROTECTED_FILES = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}
PROTECTED_DIRS = {"core", "domains", "providers", "tools", "scripts", "integrations", "runtime", "execution"}
VERDICT = "UI_UX_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_PASSED"
READINESS = "ready_for_ui_ux_1_191_next_visual_block_or_controlled_scope_experiment_selection"
NEXT_PROMPT = "PROMPT UI/UX 1.191 — Seleccionar próximo bloque visual o experimento controlado de alcance del Panel Maestro IA_CORE contract-aware"


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
    tracked = set(filter(None, git("diff", "--name-only").splitlines()))
    untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return {path.replace("\\", "/") for path in tracked | untracked}


def changed_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def test_checkpoint_document_records_state_and_visual_evidence():
    assert DOC.is_file()
    assert_markers(read(DOC), [
        "UI/UX Panel Maestro - Request Draft Panel Visual Demotion Checkpoint 1.190",
        BASE, "UI/UX 1.189", "UI/UX 1.189.A", "CSS-only", "scoped", "helper_unknown_error",
        "desktop", "mobile", "resize", "1425/1425", "375/375", "340 px", "no CTA",
        "no submit", "no runtime", "no execution", "read-only", "blocked", "P0", "P1",
        "Matriz P3", "20 filas", "26 badges", "widgets contract-aware", "SIN_CORRECCION_NECESARIA",
        "backend_internal_ui_payload.v1", "payload v2", "no endpoints", "no integraciones",
        VERDICT, READINESS, NEXT_PROMPT, "Recomendacion armonica", "Camino A", "Camino B",
    ])


def test_readmes_record_checkpoint_without_new_capability():
    for path in (README, WEB_README):
        assert_markers(read(path), [
            "UI/UX 1.190", "Request Draft Panel", "checkpoint", "desktop", "mobile", "resize",
            "no CTA", "no submit", "no runtime", "no execution", "read-only", "blocked",
            "P0", "P1", "Matriz", "widgets", "no JS contractual", "no backend", "payload v2",
            "1.191",
        ])


def test_active_contract_and_visual_surface_are_preserved():
    html = read(INDEX)
    css = read(STYLES)
    widgets = read(WIDGETS)
    backend = read(BACKEND)
    assert html.count('id="request-draft-panel"') == 1
    assert html.count('id="request-draft-toggle"') == 1
    assert html.count('id="request-draft-blocked-control"') == 1
    assert 'readonly aria-readonly="true"' in html
    assert 'disabled data-interaction-mode="read-only"' in html
    assert 'data-contract-blocked="true"' in html
    assert 'data-no-runtime="true"' in html
    assert 'data-no-execution="true"' in html
    assert "backend_internal_ui_payload.v1" in html
    assert len(re.findall(r'class="closure-matrix-row\b', html)) == 20
    assert len(re.findall(r'class="closure-matrix-badge\b', html)) == 26
    assert 'id="functional-widgets"' in html
    assert 'data-widget-reconstruction="1.174"' in html
    assert subprocess.run(["git", "diff", "--quiet", BASE, "--", "ui/web/styles.css"], cwd=ROOT, check=False).returncode == 0
    assert "body #request-draft-panel.request-draft-panel" in css
    assert "#request-draft-blocked-control.request-draft-control:disabled" in css
    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities", "source", "status"):
        assert token in widgets
        assert token in backend
    for token in ("fallback", "no_payload", "not_available"):
        assert token in widgets
    active = "\n".join([html, css, widgets, backend]).casefold()
    for token in ("backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"'):
        assert token not in active
    assert not re.search(r'>\s*(?:ready to run|processing request|capability active)\s*<', html, re.IGNORECASE)
    assert not re.search(r'data-(?:state|status)=["\'](?:running|executing|dispatching|submitted)["\']', html, re.IGNORECASE)


def test_diff_is_deny_by_default_and_historical_continuity_is_additive():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF, sorted(paths - ALLOWED_DIFF)
    assert not paths.intersection(PROTECTED_FILES)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)
    assert not any(path.startswith(".env") or "/.env" in path for path in paths)
    for path in PROTECTED_FILES:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "--", path], cwd=ROOT, check=False).returncode == 0, path
    for path in working_paths().intersection(HISTORICAL_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard removal: {path}"
        assert "CONTINUITY_1_190" in diff


def test_guard_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source
