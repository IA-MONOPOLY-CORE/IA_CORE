"""Selection guards for UI/UX 1.185 next Panel Maestro visual block."""

import ast
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "2ab27f9"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_185.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"

SELECTION_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_185.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_185.py",
}

HISTORICAL_ALLOWLIST_TESTS = {
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

PROTECTED_DIRS = {
    "core",
    "domains",
    "providers",
    "tools",
    "scripts",
    "integrations",
    "runtime",
    "execution",
}

PACKAGE_FILES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}

VALID_DECISIONS = {
    "UI_UX_NEXT_VISUAL_BLOCK_SELECTED",
    "UI_UX_NEXT_VISUAL_BLOCK_SELECTION_PENDING_MORE_EVIDENCE",
    "UI_UX_NEXT_VISUAL_BLOCK_SELECTION_BLOCKED",
}

NEXT_PROMPT = (
    "PROMPT UI/UX 1.186 — Bajar jerarquía visual de la Matriz de cierre UI/UX "
    "1.x del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character)
    )
    return " ".join(without_marks.casefold().split())


def assert_markers(text: str, markers: list[str]) -> None:
    haystack = normalized(text)
    missing = [marker for marker in markers if normalized(marker) not in haystack]
    assert not missing, f"Missing markers: {missing}"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def working_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return {path.replace("\\", "/") for path in tracked | untracked}


def selection_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def test_document_exists_and_records_selection_contract():
    assert DOC.is_file()
    text = read(DOC)
    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Next Visual Block Selection 1.185",
            "2ab27f9",
            "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_PASSED",
            "ready_for_ui_ux_1_185_next_visual_block_selection",
            "P0",
            "P1",
            "P2",
            "P3",
            "Selected Next Visual Block Candidate",
            "Candidato A",
            "Candidato B",
            "Candidato C",
            "Candidato D",
            "Candidato E",
            "Candidato F",
            "Candidato G",
            "Candidato H",
            "Request Contract Preview",
            "Matriz",
            "affordances",
            "repeticion semantica",
            "no UI activa",
            "no CSS activo",
            "no backend",
            "no-runtime",
            "no-execution",
            "no endpoints",
            "no payload v2",
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "source",
            "status",
            "fallback",
            "deny-by-default",
            "no_payload",
            "not_available",
            "backend_internal_ui_payload.v1",
        ],
    )
    assert any(decision in text for decision in VALID_DECISIONS)


def test_selected_candidate_is_single_and_has_matching_readiness_and_prompt():
    text = read(DOC)
    selections = re.findall(
        r"Selected Next Visual Block Candidate:\s*([A-H])", text, re.IGNORECASE
    )
    assert selections == ["B"]
    if "UI_UX_NEXT_VISUAL_BLOCK_SELECTED" in text:
        assert "ready_for_ui_ux_1_186_next_visual_block_implementation" in text
        assert NEXT_PROMPT in text


def test_readmes_record_scoped_1_185_selection():
    assert_markers(
        read(README),
        [
            "UI/UX 1.185",
            "seleccion de proximo bloque visual",
            "2ab27f9",
            "sin implementacion",
            "no UI activa",
            "no CSS activo",
            "P0/P1",
            "contrato",
            "no backend",
            "no-runtime",
            "no-execution",
            "no endpoints",
            "no payload v2",
            "ready_for_ui_ux_1_186_next_visual_block_implementation",
        ],
    )
    assert_markers(
        read(WEB_README),
        [
            "UI/UX 1.185",
            "proximo bloque visual seleccionado",
            "Panel Maestro",
            "contract-aware",
            "P0/P1",
            "P2/P3",
            "no UI activa",
            "no CSS activo",
            "no backend",
            "no runtime",
            "no execution",
            "no endpoints",
            "no payload v2",
            "UI/UX 1.186",
        ],
    )


def test_active_html_keeps_p0_p1_and_contract_signals():
    html = read(INDEX)
    assert html.count('data-p0-layer="visual-hierarchy-1.180"') == 1
    assert html.count('data-p1-layer="contractual-second-pass-1.183"') == 1
    assert_markers(
        html,
        [
            "Estado actual",
            "documental",
            "read-only",
            "no-runtime",
            "no-execution",
            "backend_internal_ui_payload.v1",
            "no_payload",
            "not_available",
            "blocked_by_contract",
            "Proximo paso",
            "Contract Overview",
            "Blocked",
            "Forbidden",
            "Validation",
            "Readiness",
        ],
    )
    order = [
        html.index('data-p0-layer="visual-hierarchy-1.180"'),
        html.index('data-p1-layer="contractual-second-pass-1.183"'),
        html.index('id="closure-matrix-ui-ux-1x"'),
    ]
    assert order == sorted(order)
    assert html.count('class="closure-matrix-row"') == 20


def test_contract_widgets_keep_required_fields_and_honest_fallbacks():
    assert_markers(
        read(WIDGETS),
        [
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "source",
            "status",
            "fallback",
            "no_payload",
            "not_available",
        ],
    )


def test_active_surface_has_no_payload_v2_or_positive_operational_state():
    active = "\n".join([read(INDEX), read(STYLES), read(WIDGETS)])
    active_normalized = normalized(active)
    for token in [
        "backend_internal_ui_payload.v2",
        "payload.v2",
        'schema_version\": \"v2\"',
        "ready to run",
        "processing request",
        "capability active",
    ]:
        assert normalized(token) not in active_normalized
    assert not re.search(
        r'data-(?:state|status)=["\'](?:running|executing|dispatching|submitted)["\']',
        active,
        re.IGNORECASE,
    )


def test_diff_is_strictly_limited_and_protected_paths_are_unchanged():
    paths = selection_paths()
    unexpected = paths - ALLOWED_DIFF
    assert not unexpected, f"Unexpected UI/UX 1.185 diff: {sorted(unexpected)}"
    assert not (paths & PROTECTED_FILES)
    assert not (paths & PACKAGE_FILES)
    assert not any(path.startswith(".env") or "/.env" in path for path in paths)
    assert not any(path.split("/", 1)[0] in PROTECTED_DIRS for path in paths)

    for path in PROTECTED_FILES:
        result = subprocess.run(
            ["git", "diff", "--quiet", BASE, "--", path], cwd=ROOT, check=False
        )
        assert result.returncode == 0, f"Protected path changed: {path}"


def test_historical_test_changes_are_additive_allowlist_continuity_only():
    changed = selection_paths() & HISTORICAL_ALLOWLIST_TESTS
    for path in changed:
        diff = git("diff", BASE, "--unified=0", "--", path)
        removed = [
            line
            for line in diff.splitlines()
            if line.startswith("-") and not line.startswith("---")
        ]
        assert not removed, f"Historical guard lines removed from {path}: {removed}"
        assert "CONTINUITY_1_185" in diff


def test_selection_test_requires_no_browser_network_or_dependency_install():
    tree = ast.parse(read(Path(__file__)))
    imported = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    assert imported.isdisjoint({"playwright", "selenium", "requests", "urllib"})

    source = normalized(read(Path(__file__)))
    install_command = " ".join(["pip", "install"])
    npm_command = " ".join(["npm", "install"])
    assert install_command not in source
    assert npm_command not in source
