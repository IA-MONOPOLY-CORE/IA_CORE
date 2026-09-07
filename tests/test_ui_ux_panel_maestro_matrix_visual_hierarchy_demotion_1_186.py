"""Contract and diff guards for UI/UX 1.186 matrix visual demotion."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "9f83c34"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"

FOCAL_FILES = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
}

HISTORICAL_ALLOWLIST_TESTS = {
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

ALLOWED_DIFF = FOCAL_FILES | HISTORICAL_ALLOWLIST_TESTS
PROTECTED_FILES = {
    "ui/web/index.html",
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
NEXT_PROMPT = "PROMPT UI/UX 1.187 — Checkpoint de jerarquía visual secundaria de la Matriz de cierre UI/UX 1.x del Panel Maestro IA_CORE contract-aware"


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


def changed_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def test_document_records_scoped_1_186_contract():
    assert DOC.is_file()
    assert_markers(read(DOC), [
        "UI/UX Panel Maestro Matrix Visual Hierarchy Demotion 1.186",
        "9f83c34",
        "UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_PASSED",
        "ready_for_ui_ux_1_187_matrix_visual_hierarchy_checkpoint",
        "P0", "P1", "P2", "P3", "Matriz", "20 filas", "seis estados", "26 badges",
        "Request Contract Preview", "Contract Overview", "Blocked & Forbidden", "Validation & Readiness",
        "allowed_actions", "forbidden_actions", "blocked_capabilities", "source", "status", "fallback",
        "deny-by-default", "no_payload", "not_available", "backend_internal_ui_payload.v1",
        "no backend", "no-runtime", "no-execution", "no endpoints", "no payload v2",
        "no UI activa", "GPT-5.6 Terra", "high", NEXT_PROMPT,
    ])


def test_active_matrix_is_complete_and_not_hidden_or_collapsed():
    html = read(INDEX)
    start = html.index('<section class="closure-matrix-section')
    end = html.index("</section>", start) + len("</section>")
    block = html[start:end]
    assert html.count('id="closure-matrix-ui-ux-1x"') == 1
    assert block.count('class="closure-matrix-row"') == 20
    for state in ["PASSED", "PASSED_WITH_MINOR_DEBT", "DEFERRED_WITH_GUARDRAILS", "BLOCKED_NEEDS_FIX", "BLOCKED_CRITICAL", "NOT_APPLICABLE"]:
        assert state in block
    assert block.count('class="closure-matrix-badge') == 26
    assert not re.search(r"<details\b|accordion|\bhidden\b|aria-hidden\s*=\s*[\"']true", block, re.IGNORECASE)


def test_css_demotion_is_scoped_and_preserves_visibility():
    css = read(STYLES)
    assert "UI/UX 1.186" in css
    selector = 'body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"][data-visual-hierarchy-second-pass="1.183"] #closure-matrix-ui-ux-1x'
    assert css.count(selector) >= 10
    assert "box-shadow: 0 8px 20px" in css
    assert "opacity: 0.94" in css
    assert "font-size: 0.62rem" in css
    assert "padding: 12px" in css
    scoped = css[css.index("/* UI/UX 1.186"):]
    for forbidden in ["display: none", "visibility: hidden", "height: 0", "max-height: 0", "overflow: hidden"]:
        assert forbidden not in scoped


def test_readmes_record_1_186_and_next_readiness():
    assert_markers(read(README), ["UI/UX 1.186", "bajar jerarquia visual", "9f83c34", "Matriz", "20 filas", "P0/P1", "P2/P3", "no backend", "no-runtime", "no-execution", "no endpoints", "no payload v2", "ready_for_ui_ux_1_187_matrix_visual_hierarchy_checkpoint"])
    assert_markers(read(WEB_README), ["UI/UX 1.186", "jerarquia visual secundaria", "Matriz", "P3/auditoria", "P0/P1", "20 filas", "26 badges", "no UI activa", "no backend", "no runtime", "no execution", "no endpoints", "no payload v2", "UI/UX 1.187"])


def test_p0_p1_panel_widgets_and_contract_markers_remain_present():
    html = read(INDEX)
    assert html.count('data-p0-layer="visual-hierarchy-1.180"') == 1
    assert html.count('data-p1-layer="contractual-second-pass-1.183"') == 1
    assert 'id="request-contract-preview-screen"' in html
    assert 'id="request-draft-panel"' in html
    assert_markers(html, ["Contract Overview", "Blocked", "Forbidden", "Validation", "Readiness", "backend_internal_ui_payload.v1", "no_payload", "not_available", "blocked_by_contract", "no-runtime", "no-execution"])
    assert_markers(read(WIDGETS), ["allowed_actions", "forbidden_actions", "blocked_capabilities", "source", "status", "fallback", "no_payload", "not_available"])


def test_no_operational_v2_or_positive_state_is_introduced():
    active = normalized("\n".join([read(INDEX), read(STYLES), read(WIDGETS)]))
    for token in ["backend_internal_ui_payload.v2", "payload.v2", "ready to run", "processing request", "capability active"]:
        assert token not in active
    assert not re.search(r'data-(?:state|status)=["\'](?:running|executing|dispatching|submitted)["\']', active, re.IGNORECASE)


def test_diff_is_deny_by_default_and_protected_paths_are_unchanged():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF, sorted(paths - ALLOWED_DIFF)
    assert not paths.intersection(PROTECTED_FILES | PACKAGE_FILES)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)
    for path in PROTECTED_FILES:
        result = subprocess.run(["git", "diff", "--quiet", BASE, "--", path], cwd=ROOT, check=False)
        assert result.returncode == 0, f"Protected path changed: {path}"


def test_historical_changes_are_additive_1_186_continuity_only():
    for path in working_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [line for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
        assert not removed, f"Historical guard lines removed from {path}: {removed}"
        assert "CONTINUITY_1_186" in diff


def test_test_source_has_no_browser_network_or_install_dependency():
    tree = ast.parse(read(Path(__file__)))
    imported = {alias.name.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    imported.update(node.module.split(".", 1)[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module)
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})
    source = normalized(read(Path(__file__)))
    assert " ".join(["pip", "install"]) not in source
    assert " ".join(["npm", "install"]) not in source
