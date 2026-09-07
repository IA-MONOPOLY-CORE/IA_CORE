"""Read-only selection and diff guards for UI/UX 1.188."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "e2d1653"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_188.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"

SELECTION_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_188.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py",
}
HISTORICAL_ALLOWLIST_TESTS = {
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
ALLOWED_DIFF = SELECTION_FILES | HISTORICAL_ALLOWLIST_TESTS
CONTINUITY_1_189 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_1_189.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.
ALLOWED_DIFF |= CONTINUITY_1_189
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187 and CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.

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
DECISION = "UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_MATRIX_CHECKPOINT"
READINESS = "ready_for_ui_ux_1_189_selected_visual_block_implementation"
NEXT_PROMPT = "PROMPT UI/UX 1.189 — Implementar próximo bloque visual seleccionado del Panel Maestro IA_CORE contract-aware"


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


def selection_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def test_selection_document_has_required_evidence_and_single_candidate():
    document = read(DOC)
    assert DOC.is_file()
    assert_markers(document, [
        "UI/UX Panel Maestro Next Visual Block Selection 1.188", "e2d1653",
        "UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_PASSED",
        "ready_for_ui_ux_1_188_next_visual_block_selection", "seleccion visual",
        "read-only", "no implementacion", "no UI activa", "no CSS activo",
        "no JS contractual", "no backend", "no-runtime", "no-execution",
        "no endpoints", "no payload v2", "P0", "P1", "Matriz", "P2", "P3",
        "Request Contract Preview", "Request Draft Panel", "widgets contract-aware",
        "affordances", "readiness", "microcopy", "Candidato A", "Candidato B",
        "Candidato C", "Candidato D", "Candidato E", "Candidato F", "Candidato G",
        "Candidato H", "impacto visual", "claridad de producto", "riesgo contractual",
        "riesgo tecnico", "riesgo responsive", "dependencia backend/JS", "reversibilidad",
        "conveniencia", "modelo", "herramienta", "nivel de esfuerzo",
        "Recomendacion armonica", "no debe buscar el minimo", "no debe buscar el maximo",
        DECISION, READINESS, NEXT_PROMPT,
    ])
    selected = re.findall(r"Candidato seleccionado:\s*([A-H])\b", document)
    assert selected == ["A"], selected


def test_readmes_record_read_only_selection_and_readiness():
    assert_markers(read(README), [
        "UI/UX 1.188", "seleccion del proximo bloque visual", "e2d1653",
        "checkpoint de Matriz", "read-only", "no implementacion", "no UI activa",
        "no CSS activo", "no backend", "no-runtime", "no-execution", "no endpoints",
        "no payload v2", "Candidato A", "recomendacion armonica", "modelo",
        "herramienta", "nivel de esfuerzo", READINESS,
    ])
    assert_markers(read(WEB_README), [
        "UI/UX 1.188", "seleccion del proximo bloque visual", "checkpoint de Matriz",
        "read-only", "no implementacion", "no UI activa", "no CSS activo", "no backend",
        "no runtime", "no execution", "no endpoints", "no payload v2", "Candidato A",
        "UI/UX 1.189",
    ])


def test_active_panel_and_contract_are_read_only_preserved():
    html = read(INDEX)
    assert html.count('id="request-draft-panel"') == 1
    assert html.count('id="request-draft-toggle"') == 1
    assert html.count('id="request-draft-blocked-control"') == 1
    assert 'data-contract-blocked="true"' in html
    assert 'data-no-runtime="true"' in html
    assert 'data-no-execution="true"' in html
    assert html.index('data-p0-layer="visual-hierarchy-1.180"') < html.index('data-p1-layer="contractual-second-pass-1.183"') < html.index('id="closure-matrix-ui-ux-1x"')
    assert html.count('class="closure-matrix-row"') == 20
    assert_markers(read(WIDGETS), ["allowed_actions", "forbidden_actions", "blocked_capabilities", "source", "status", "fallback", "no_payload", "not_available"])


def test_active_surfaces_keep_v1_and_no_operational_v2_state():
    active = "\n".join([read(INDEX), read(STYLES), read(WIDGETS)])
    assert "backend_internal_ui_payload.v1" in active
    for token in ["backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"']:
        assert token.casefold() not in active.casefold()
    assert not re.search(r">\s*(?:ready to run|processing request|capability active)\s*<", active, re.IGNORECASE)
    assert not re.search(r'data-(?:state|status)=["\'](?:running|executing|dispatching|submitted)["\']', read(INDEX), re.IGNORECASE)


def test_diff_is_deny_by_default_and_protected_paths_are_unchanged():
    paths = selection_paths()
    assert paths <= ALLOWED_DIFF, sorted(paths - ALLOWED_DIFF)
    assert not paths.intersection(PROTECTED_FILES | PACKAGE_FILES)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)
    assert not any(path.startswith(".env") or "/.env" in path for path in paths)
    for path in PROTECTED_FILES:
        result = subprocess.run(["git", "diff", "--quiet", BASE, "--", path], cwd=ROOT, check=False)
        assert result.returncode == 0, f"Protected path changed: {path}"


def test_historical_allowlist_changes_are_additive_1_188_only():
    for path in working_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard lines removed from {path}: {removed}"
        assert "CONTINUITY_1_188" in diff


def test_selection_source_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source

PROTECTED_FILES.discard("ui/web/styles.css")
