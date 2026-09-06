"""Checkpoint guards for UI/UX 1.184 P1 contractual second pass."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BASE = "b8db98f"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_1_184.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
BACKEND_PAYLOAD = ROOT / "core" / "backend_internal_ui_payloads.py"
API = ROOT / "api.py"

CHECKPOINT_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_1_184.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py",
}

HISTORICAL_ALLOWLIST_TESTS = {
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
    "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_PASSED",
    "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_PENDING_MINOR_FIX",
    "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_BLOCKED",
}

NEXT_PROMPT = (
    "PROMPT UI/UX 1.185 — Seleccionar próximo bloque visual del Panel Maestro "
    "IA_CORE contract-aware"
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


def checkpoint_paths() -> set[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{BASE}..HEAD").splitlines()))
    return {path.replace("\\", "/") for path in committed} | working_paths()


def p0_block(text: str) -> str:
    start = text.index('<section class="four-screen-baseline-summary p0-command-summary"')
    end = text.index('<div class="final-screen-contracts-rehousing"', start)
    return text[start:end]


def p1_block(text: str) -> str:
    start = text.index('<div class="final-screen-contracts-rehousing"')
    end = text.index('<section class="closure-matrix-section', start)
    return text[start:end]


def test_document_exists_and_records_required_checkpoint_markers():
    assert DOC.is_file()
    text = read(DOC)
    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Visual Hierarchy P1 Contractual Second Pass Checkpoint 1.184",
            "b8db98f",
            "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_PASSED",
            "ready_for_ui_ux_1_184_p1_contractual_second_pass_checkpoint",
            "P0",
            "P1",
            "P2",
            "P3",
            "Contrato",
            "Acciones",
            "Bloqueos",
            "Validacion",
            "Readiness",
            "Contract Overview",
            "Blocked",
            "Forbidden",
            "Validation",
            "Estado",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "Request Contract Preview",
            "Matriz",
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


def test_passed_checkpoint_has_matching_readiness_and_exact_next_prompt():
    text = read(DOC)
    if "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_PASSED" in text:
        assert "ready_for_ui_ux_1_185_next_visual_block_selection" in text
        assert NEXT_PROMPT in text


def test_readmes_record_the_scoped_1_184_checkpoint():
    assert_markers(
        read(README),
        [
            "UI/UX 1.184",
            "checkpointa",
            "segunda pasada P1 contractual",
            "b8db98f",
            "sin implementacion nueva",
            "sin UI activa",
            "CSS activo",
            "P0/P1",
            "P2/P3",
            "panel",
            "Matriz",
            "widgets contract-aware",
            "no backend",
            "no-runtime",
            "no-execution",
            "no endpoints",
            "no payload v2",
            "ready_for_ui_ux_1_185_next_visual_block_selection",
        ],
    )
    assert_markers(
        read(WEB_README),
        [
            "UI/UX 1.184",
            "checkpoint P1 contractual",
            "b8db98f",
            "Contract Overview",
            "Blocked & Forbidden",
            "Validation & Readiness",
            "P0",
            "P2/P3",
            "Request Contract Preview",
            "Matriz",
            "widgets contract-aware",
            "no implementacion nueva",
            "no UI activa",
            "CSS activo",
            "no backend",
            "no runtime",
            "no execution",
            "no endpoints",
            "no payload v2",
            "UI/UX 1.185",
        ],
    )


def test_p0_remains_unique_superior_read_only_and_complete():
    html = read(INDEX)
    block = p0_block(html)
    assert html.count('data-p0-layer="visual-hierarchy-1.180"') == 1
    assert_markers(
        block,
        [
            "Estado actual",
            "Modo documental",
            "read-only",
            "NO_RUNTIME",
            "NO_EXECUTION",
            "backend_internal_ui_payload.v1",
            "no_payload",
            "not_available",
            "blocked_by_contract",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
        ],
    )
    route_block = block[block.index('<ol class="p0-reading-route"') :]
    route_block = route_block[: route_block.index("</ol>")]
    route = ["Estado", "Contrato", "Limites", "Evidencia", "Proximo paso"]
    positions = [normalized(route_block).index(normalized(marker)) for marker in route]
    assert positions == sorted(positions)
    assert not re.search(r"<(?:button|input|select|textarea)\b", block, re.IGNORECASE)


def test_p1_is_below_p0_and_keeps_route_screens_and_contract_fields():
    html = read(INDEX)
    block = p1_block(html)
    assert html.index('data-p0-layer="visual-hierarchy-1.180"') < html.index(
        'data-p1-layer="contractual-second-pass-1.183"'
    )
    assert html.count('data-p1-layer="contractual-second-pass-1.183"') == 1
    assert html.count("data-contract-screen=") == 4
    assert_markers(
        block,
        [
            "P1",
            "Lectura contractual principal",
            "Contrato",
            "Acciones declaradas",
            "Bloqueos",
            "Validacion",
            "Contract Overview",
            "Blocked",
            "Forbidden",
            "Validation",
            "Readiness",
            "Request Contract Preview",
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "source",
            "status",
            "fallback",
            "warnings",
            "errors",
            "deny-by-default",
            "read-only",
            "no-runtime",
            "no-execution",
        ],
    )
    route_markers = [
        'data-p1-step="contract"',
        'data-p1-step="actions"',
        'data-p1-step="boundaries"',
        'data-p1-step="validation"',
    ]
    assert [block.index(marker) for marker in route_markers] == sorted(
        block.index(marker) for marker in route_markers
    )
    screen_ids = [
        'id="contract-overview-screen"',
        'id="blocked-forbidden-screen"',
        'id="validation-readiness-screen"',
        'id="request-contract-preview-screen"',
    ]
    assert [block.index(marker) for marker in screen_ids] == sorted(
        block.index(marker) for marker in screen_ids
    )
    assert not re.search(r"<(?:button|input|select|textarea|a\s+[^>]*href)\b", block, re.IGNORECASE)


def test_p2_p3_panel_matrix_and_blocked_lower_controls_are_preserved():
    html = read(INDEX)
    assert_markers(
        html,
        [
            "Matriz de cierre",
            "Ruta de lectura",
            "Indice interno",
            "Readiness Global",
            "Contract Core / Payload",
            "Raw-safe",
            "CAPAS IA_CORE",
            "Internal Services / Signals",
            "Actions",
            "Boundaries",
            "Evidence",
            "Tarjetas de agentes bloqueadas",
        ],
    )
    for marker in [
        'id="closure-matrix-ui-ux-1x"',
        'id="contract-read-only-inspector"',
        'id="functional-widgets"',
        'id="request-draft-panel"',
        'id="settings-fab"',
        'id="add-fab"',
        'id="domain-fab"',
    ]:
        assert marker in html
    assert html.index('id="request-contract-preview-screen"') < html.index(
        'id="closure-matrix-ui-ux-1x"'
    )
    for control in ["settings-fab", "add-fab", "domain-fab"]:
        assert re.search(
            rf'<button[^>]*id="{control}"[^>]*disabled[^>]*data-contract-blocked="true"',
            html,
            re.IGNORECASE,
        )


def test_request_contract_preview_is_read_only_blocked_and_non_operational():
    html = read(INDEX)
    assert_markers(
        html[html.index('id="request-contract-preview-screen"') :],
        [
            "Request Contract Preview",
            "read-only",
            "blocked",
            "no-submit",
            "no-dispatch",
            "no-runtime",
            "no-execution",
            "no-endpoint",
            "no-fetch",
        ],
    )
    assert re.search(r'<textarea[^>]*id="task-input"[^>]*readonly', html, re.IGNORECASE)
    assert re.search(
        r'<button[^>]*id="request-draft-blocked-control"[^>]*disabled',
        html,
        re.IGNORECASE,
    )


def test_p1_styles_remain_scoped_responsive_and_layout_safe():
    assert_markers(
        read(STYLES),
        [
            "P1 contractual hierarchy",
            "data-p1-layer",
            "p1-contractual-route",
            "p1-contractual-stage",
            "display: grid",
            "minmax(0, 1fr)",
            "overflow-wrap",
            "@media (max-width: 980px)",
            "@media (max-width: 760px)",
            "@media (max-width: 480px)",
        ],
    )


def test_contract_widget_renderer_keeps_fields_fallbacks_and_no_fetch():
    script = read(WIDGETS)
    assert_markers(
        script,
        [
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "source",
            "status",
            "fallback",
            "no_payload",
            "not_available",
            "deny-by-default",
        ],
    )
    assert "fetch(" not in script


def test_active_ui_javascript_backend_and_payload_match_the_1_183_base():
    for path in sorted(PROTECTED_FILES):
        result = subprocess.run(
            ["git", "diff", "--quiet", BASE, "--", path],
            cwd=ROOT,
            check=False,
        )
        assert result.returncode == 0, path


def test_no_payload_v2_or_positive_operational_state_is_present_in_p1():
    active_contract = "\n".join(
        read(path) for path in [INDEX, STYLES, WIDGETS, BACKEND_PAYLOAD, API]
    )
    for pattern in [
        r"backend_internal_ui_payload\.v2",
        r"payload\.v2",
        r"schema_version[\"']?\s*[:=]\s*[\"']v2[\"']",
    ]:
        assert not re.search(pattern, active_contract, flags=re.IGNORECASE)

    block = p1_block(read(INDEX))
    for pattern in [
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\brunning\b',
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\bexecuting\b',
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\bdispatching\b',
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\bsubmitted\b',
        r">\s*ready to run\s*<",
        r">\s*processing request\s*<",
        r">\s*capability active\s*<",
    ]:
        assert not re.search(pattern, block, flags=re.IGNORECASE)


def test_checkpoint_diff_is_strictly_limited_and_protected_paths_are_clean():
    paths = checkpoint_paths()
    assert paths <= ALLOWED_DIFF
    assert not paths.intersection(PROTECTED_FILES | PACKAGE_FILES)
    for path in paths:
        normalized_path = path.strip("/")
        assert normalized_path.split("/", 1)[0] not in PROTECTED_DIRS
        lowered = normalized_path.casefold()
        assert "secret" not in lowered
        assert not lowered.endswith((".env", ".env.local"))
        assert "/endpoints/" not in f"/{lowered}/"
        assert "/routers/" not in f"/{lowered}/"


def test_historical_tests_can_only_add_1_184_allowlist_continuity():
    for path in working_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [
            line
            for line in diff.splitlines()
            if line.startswith("-") and not line.startswith("---")
        ]
        assert not removed, f"Historical test change must be additive only: {path}"
        added_paths = {
            candidate
            for line in diff.splitlines()
            if line.startswith("+") and not line.startswith("+++")
            for match in [re.search(r'[\"\']([^\"\']+)[\"\']', line)]
            if match
            for candidate in [match.group(1)]
            if "/" in candidate or candidate.endswith((".md", ".py"))
        }
        assert added_paths <= CHECKPOINT_FILES
        assert "CONTINUITY_1_184" in diff


def test_checkpoint_test_requires_no_browser_network_or_dependency_install():
    source = read(Path(__file__))
    assert not re.search(
        r"^\s*(?:from|import)\s+(?:selenium|playwright|requests)\b",
        source,
        flags=re.MULTILINE,
    )
    assert "pip" + " install" not in source.casefold()
