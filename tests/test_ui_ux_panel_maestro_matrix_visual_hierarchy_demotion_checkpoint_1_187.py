"""Read-only checkpoint guards for UI/UX 1.187 matrix demotion."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "8ed0c3e"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"

CHECKPOINT_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
}
HISTORICAL_ALLOWLIST_TESTS = {
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
ALLOWED_DIFF = CHECKPOINT_FILES | HISTORICAL_ALLOWLIST_TESTS
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
}
PROTECTED_DIRS = {"core", "domains", "providers", "tools", "scripts", "integrations", "runtime", "execution"}
PACKAGE_FILES = {"package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
NEXT_PROMPT = "PROMPT UI/UX 1.188 — Seleccionar próximo bloque visual del Panel Maestro IA_CORE contract-aware posterior al checkpoint de Matriz"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return " ".join("".join(c for c in decomposed if not unicodedata.combining(c)).casefold().split())


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


def checkpoint_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def test_document_contains_checkpoint_contract():
    assert DOC.is_file()
    assert_markers(read(DOC), [
        "UI/UX Panel Maestro Matrix Visual Hierarchy Demotion Checkpoint 1.187",
        "8ed0c3e",
        "UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_PASSED",
        "ready_for_ui_ux_1_187_matrix_visual_hierarchy_checkpoint",
        "Candidate B", "Matriz", "P3", "auditoria", "20 filas", "seis estados", "26 badges",
        "visible", "completa", "no colapsada", "no oculta", "no accordion", "no aria-hidden",
        "P0", "P1", "P2", "Estado", "Contrato", "Limites", "Evidencia", "Proximo paso",
        "Acciones", "Bloqueos", "Validacion", "Readiness", "Request Contract Preview",
        "widgets contract-aware", "backend-contract-widgets.js", "no UI activa", "no CSS activo",
        "no JS contractual", "no i18n", "no backend", "no-runtime", "no-execution", "no endpoints",
        "no payload v2", "allowed_actions", "forbidden_actions", "blocked_capabilities", "source",
        "status", "fallback", "deny-by-default", "no_payload", "not_available", "backend_internal_ui_payload.v1",
        "Recomendacion armonica", "modelo", "herramienta", "nivel de esfuerzo", "balance",
        "no debe buscar el minimo", "no debe buscar el maximo", NEXT_PROMPT,
    ])
    assert "UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_PASSED" in read(DOC)
    assert "ready_for_ui_ux_1_188_next_visual_block_selection" in read(DOC)


def test_readmes_record_the_checkpoint():
    assert_markers(read(README), [
        "UI/UX 1.187", "checkpoint de jerarquia visual secundaria de la Matriz", "8ed0c3e",
        "no implementacion nueva", "no UI activa", "no CSS activo", "matriz completa", "preservada",
        "P0", "P1", "no backend", "no-runtime", "no-execution", "recomendacion armonica",
        "modelo", "herramienta", "ready_for_ui_ux_1_188_next_visual_block_selection",
    ])
    assert_markers(read(WEB_README), [
        "UI/UX 1.187", "checkpoint de Matriz", "P3", "auditoria", "visible", "completa",
        "no colapsada", "no oculta", "no UI activa", "no CSS activo", "P0/P1", "no backend",
        "no runtime", "no execution", "recomendacion armonica", "modelo", "herramienta", "UI/UX 1.188",
    ])


def test_matrix_is_active_complete_visible_and_secondary():
    html = read(INDEX)
    start = html.index('<section class="closure-matrix-section')
    end = html.index("</section>", start) + len("</section>")
    block = html[start:end]
    assert html.count('id="closure-matrix-ui-ux-1x"') == 1
    assert block.count('class="closure-matrix-row"') == 20
    assert block.count('class="closure-matrix-badge') == 26
    for state in ["PASSED", "PASSED_WITH_MINOR_DEBT", "DEFERRED_WITH_GUARDRAILS", "BLOCKED_NEEDS_FIX", "BLOCKED_CRITICAL", "NOT_APPLICABLE"]:
        assert state in block
    assert not re.search(r"<details\b|<summary\b|accordion|\bhidden\b|aria-hidden\s*=\s*[\"']true", block, re.IGNORECASE)
    assert 'data-density-tier="secondary"' in block
    assert 'data-interaction-mode="read-only"' in block


def test_p0_p1_p2_p3_panel_and_widgets_remain_contract_aware():
    html = read(INDEX)
    assert html.count('data-p0-layer="visual-hierarchy-1.180"') == 1
    assert html.count('data-p1-layer="contractual-second-pass-1.183"') == 1
    assert html.index('data-p0-layer="visual-hierarchy-1.180"') < html.index('data-p1-layer="contractual-second-pass-1.183"') < html.index('id="closure-matrix-ui-ux-1x"')
    assert_markers(html, ["Estado", "Contrato", "Limites", "Evidencia", "Proximo paso", "Acciones", "Bloqueos", "Validacion", "Readiness", "Request Contract Preview", "Matriz", "Ruta de lectura", "Indice interno", "Raw-safe", "Internal Services", "Evidence", "Tarjetas de agentes bloqueadas", "read-only", "no-runtime", "no-execution", "backend_internal_ui_payload.v1", "no_payload", "not_available", "allowed_actions", "forbidden_actions", "blocked_capabilities"])
    assert 'id="request-draft-panel"' in html
    assert_markers(read(WIDGETS), ["allowed_actions", "forbidden_actions", "blocked_capabilities", "source", "status", "fallback", "no_payload", "not_available"])


def test_css_and_active_contract_show_demotion_without_new_capability():
    css = read(STYLES)
    assert "UI/UX 1.186" in css
    assert "#closure-matrix-ui-ux-1x" in css
    assert re.search(r"box-shadow|border|opacity|background|padding|gap|font-size", css, re.IGNORECASE)
    assert re.search(r"@media\s*\(", css, re.IGNORECASE)
    active = "\n".join([read(INDEX), css, read(WIDGETS)])
    for token in ["backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"']:
        assert token.casefold() not in active.casefold()
    assert not re.search(r">\s*(?:ready to run|processing request|capability active)\s*<", active, re.IGNORECASE)
    assert not re.search(r'data-(?:state|status)=["\'](?:running|executing|dispatching|submitted)["\']', read(INDEX), re.IGNORECASE)


def test_diff_is_strictly_limited_and_protected_paths_are_unchanged():
    paths = checkpoint_paths()
    assert paths <= ALLOWED_DIFF, sorted(paths - ALLOWED_DIFF)
    assert not paths.intersection(PROTECTED_FILES | PACKAGE_FILES)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)
    assert not any(path.startswith(".env") or "/.env" in path for path in paths)
    for path in PROTECTED_FILES:
        result = subprocess.run(["git", "diff", "--quiet", BASE, "--", path], cwd=ROOT, check=False)
        assert result.returncode == 0, f"Protected path changed: {path}"


def test_historical_allowlist_changes_are_additive_1_187_only():
    for path in working_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard lines removed from {path}: {removed}"
        assert "CONTINUITY_1_187" in diff


def test_checkpoint_source_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source
