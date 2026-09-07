"""Read-only selection and deny-by-default guards for UI/UX 1.191."""

from ui_ux_1_192_scope import historical_paths, assert_current_scope
HISTORICAL_COMMIT = '82dd100'

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "66d73e3"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_1_191.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
DECISION = "CONTROLLED_DOUBLE_SCOPE_EXPERIMENT_SELECTED"
VERDICT = "UI_UX_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_PASSED"
READINESS = "ready_for_ui_ux_1_192_selected_visual_block_or_controlled_double_scope_implementation"
NEXT_PROMPT = "PROMPT UI/UX 1.192 — Implementar bloque visual seleccionado o doble pieza controlada del Panel Maestro IA_CORE contract-aware"

ALLOWED_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_1_191.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py",
}
HISTORICAL_TESTS = {
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py",
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
    """Paths in this closed checkpoint, never the current worktree."""
    return historical_paths(ROOT, HISTORICAL_COMMIT)


def changed_paths() -> set[str]:
    """Paths in this closed checkpoint, never the current worktree."""
    return historical_paths(ROOT, HISTORICAL_COMMIT)


def test_selection_document_records_candidates_and_decision():
    assert DOC.is_file()
    assert_markers(read(DOC), [
        "UI/UX Panel Maestro Next Visual Block Or Controlled Scope Selection 1.191",
        BASE, "UI/UX 1.190", "seleccion read-only", "no implementacion", "no ui activa",
        "no css activo", "no html", "no js contractual", "no i18n", "no backend", "no runtime",
        "no execution", "no endpoints", "no payload v2", "affordances bloqueadas", "severidad visual",
        "readiness global", "proximo paso", "estado de cierre", "microcopy contractual", "compactacion",
        "coherencia visual", "movimiento", "identidad audiovisual", "candidato a", "candidato b",
        "candidato c", "candidato d", "candidato e", "candidato f", "candidato g", "candidato h",
        "candidato i", "candidato j", "recomendacion armonica", "luna", "astra", "terra", "consumo",
        "calidad", "riesgo de retrabajo", DECISION, VERDICT, READINESS, NEXT_PROMPT,
    ])
    doc = normalized(read(DOC))
    assert "pieza principal" in doc and "pieza secundaria" in doc
    assert "gates internos" in doc and "condicion de corte" in doc
    assert "no se escala a triple" in doc
    assert "no es un benchmark artificial" in doc


def test_readmes_record_selection_without_implementation():
    for path in (README, WEB_README):
        assert_markers(read(path), [
            "UI/UX 1.191", "seleccion", "read-only", "candidato i", "affordances bloqueadas",
            "severidad", "no implementacion", "no CSS activo", "no backend", "no runtime", "no execution",
            "1.192",
        ])


def test_active_contract_is_untouched_and_v1_only():
    html = read(INDEX)
    css = read(STYLES)
    widgets = read(WIDGETS)
    assert subprocess.run(['git', 'diff', '--quiet', BASE, HISTORICAL_COMMIT, '--', 'ui/web/index.html', 'ui/web/styles.css', 'ui/web/backend-contract-widgets.js'], cwd=ROOT, check=False).returncode == 0
    assert 'id="request-draft-panel"' in html
    assert 'id="request-draft-blocked-control"' in html
    assert 'readonly aria-readonly="true"' in html
    assert 'disabled data-interaction-mode="read-only"' in html
    assert 'data-contract-blocked="true"' in html
    assert "backend_internal_ui_payload.v1" in html
    assert "body #request-draft-panel.request-draft-panel" in css
    assert "functional-widgets" in html
    assert "closure-matrix-row" in html and "closure-matrix-badge" in html
    for token in ["allowed_actions", "forbidden_actions", "blocked_capabilities", "source", "status", "fallback", "no_payload", "not_available"]:
        assert token in widgets
    active = "\n".join([html, css, widgets]).casefold()
    for token in ["backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"']:
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
        assert subprocess.run(['git', 'diff', '--quiet', BASE, HISTORICAL_COMMIT, '--', path], cwd=ROOT, check=False).returncode == 0, path
    for path in working_paths().intersection(HISTORICAL_TESTS):
        diff = git('diff', '--unified=0', HISTORICAL_COMMIT + '^', HISTORICAL_COMMIT, '--', path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard removal: {path}"
        assert "CONTINUITY_1_191" in diff


def test_guard_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source


def test_current_scope_is_strict_1_192():
    assert_current_scope(ROOT)
