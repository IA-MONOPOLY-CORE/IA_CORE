"""Focused contract checks for UI/UX 1.180 P0 visual hierarchy."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

CONTINUITY_TESTS = {
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
}

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
} | CONTINUITY_TESTS

CONTINUITY_1_181 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_1_181.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py",
}

ALLOWED_DIFF |= CONTINUITY_1_181

CONTINUITY_1_182 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_1_182.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py",
}

ALLOWED_DIFF |= CONTINUITY_1_182

CONTINUITY_1_183 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
}

# CONTINUITY_1_181 remains preserved; CONTINUITY_1_183 is additive.
ALLOWED_DIFF |= CONTINUITY_1_183

CONTINUITY_1_184 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_1_184.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182 and CONTINUITY_1_183 remain preserved; CONTINUITY_1_184 is additive.
ALLOWED_DIFF |= CONTINUITY_1_184

CONTINUITY_1_185 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_185.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_185.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182, CONTINUITY_1_183 and CONTINUITY_1_184 remain preserved;
# CONTINUITY_1_185 is additive.
ALLOWED_DIFF |= CONTINUITY_1_185

CONTINUITY_1_186 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184 and CONTINUITY_1_185 remain preserved; CONTINUITY_1_186 is additive and scoped to the matrix visual demotion.
ALLOWED_DIFF |= CONTINUITY_1_186

CONTINUITY_1_187 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_186 remain preserved; CONTINUITY_1_187 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185 and CONTINUITY_1_186 remain preserved.
ALLOWED_DIFF |= CONTINUITY_1_187

PROTECTED_EXACT = {
    ".env",
    "api.py",
    "core/backend_internal_ui_payloads.py",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "ui/web/admin-panels.js",
    "ui/web/backend-contract-widgets.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "ui/web/i18n_es.json",
}

PROTECTED_DIRS = {
    "core",
    "domains",
    "execution",
    "integrations",
    "providers",
    "runtime",
    "scripts",
    "tools",
}

VALID_DECISIONS = {
    "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_PASSED",
    "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_PENDING_MINOR_FIX",
    "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_BLOCKED",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(
        character for character in decomposed
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


def changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return {path.replace("\\", "/") for path in tracked | untracked}


def p0_block() -> str:
    html = read(INDEX)
    start = html.index('<section class="four-screen-baseline-summary p0-command-summary"')
    end = html.index('<div class="final-screen-contracts-rehousing"', start)
    return html[start:end]


def test_document_exists_and_records_required_contract_markers():
    assert DOC.is_file()
    text = read(DOC)
    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Visual Hierarchy First Pass 1.180",
            "82705e4",
            "UI_UX_VISUAL_HIERARCHY_AUDIT_PASSED",
            "ready_for_ui_ux_1_180_visual_hierarchy_first_pass",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "P0",
            "Ruta A",
            "no-runtime",
            "no-execution",
            "no backend",
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


def test_passed_decision_has_readiness_and_exact_next_prompt():
    text = read(DOC)
    if "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_PASSED" in text:
        assert "ready_for_ui_ux_1_181_visual_hierarchy_checkpoint_or_second_pass" in text
        assert (
            "PROMPT UI/UX 1.181 — Checkpoint de primera pasada de jerarquía "
            "visual superior del Panel Maestro IA_CORE"
        ) in text


def test_active_html_contains_a_clear_read_only_p0_layer():
    html = read(INDEX)
    block = p0_block()
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
            "Bloqueado por contrato",
            "Proximo paso seguro",
            "evidencia contractual completa sigue debajo",
        ],
    )
    assert 'data-visual-hierarchy-first-pass="1.180"' in html
    assert 'data-p0-layer="visual-hierarchy-1.180"' in block


def test_p0_styles_include_desktop_and_mobile_hierarchy_signals():
    css = read(STYLES)
    assert_markers(
        css,
        [
            "first-pass P0 hierarchy",
            ".p0-command-summary",
            ".p0-command-header",
            ".p0-reading-route",
            ".p0-command-grid",
            ".p0-summary-card",
            ".p0-evidence-next",
            ".p0-mode-lock",
            "display: grid",
            "flex-wrap: wrap",
            "@media (max-width: 760px)",
            "@media (max-width: 480px)",
        ],
    )


def test_p1_p2_p3_and_right_panel_remain_present():
    html = read(INDEX)
    for marker in [
        'id="contract-overview-screen"',
        'id="blocked-forbidden-screen"',
        'id="validation-readiness-screen"',
        'id="request-contract-preview-screen"',
        'id="closure-matrix-ui-ux-1x"',
        'id="contract-read-only-inspector"',
        'id="functional-widgets"',
        'id="request-draft-panel"',
        'id="settings-fab"',
        'id="add-fab"',
        'id="domain-fab"',
    ]:
        assert marker in html
    assert html.count("data-contract-screen=") == 4


def test_contract_renderer_keeps_required_fields_and_fallbacks():
    script = read(WIDGETS)
    for marker in [
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "source",
        "status",
        "fallback",
        "no_payload",
        "not_available",
        "deny-by-default",
    ]:
        assert marker in script


def test_no_new_active_v2_or_operational_state_is_introduced():
    active_contract = read(INDEX) + read(WIDGETS)
    for pattern in [
        r"backend_internal_ui_payload\.v2",
        r"payload\.v2",
        r"schema_version[\"']?\s*[:=]\s*[\"']v2[\"']",
    ]:
        assert not re.search(pattern, active_contract, flags=re.IGNORECASE)

    block = p0_block()
    for active_phrase in [
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "ready to run",
        "Processing request",
        "Capability active",
    ]:
        assert active_phrase.casefold() not in block.casefold()


def test_readmes_record_scoped_1_180_cursor():
    assert_markers(
        read(README),
        [
            "Cursor vigente UI/UX 1.180",
            "82705e4",
            "primera pasada P0",
            "no backend",
            "no-runtime",
            "no-execution",
            "no endpoints",
            "no payload v2",
            "ready_for_ui_ux_1_181_visual_hierarchy_checkpoint_or_second_pass",
        ],
    )
    assert_markers(
        read(WEB_README),
        [
            "Nota UI/UX 1.180",
            "capa superior/P0",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "P1/P2/P3",
            "panel derecho preservado",
            "no backend",
            "no runtime",
            "no execution",
            "no endpoints",
            "no payload v2",
            "UI/UX 1.181",
        ],
    )


def test_current_diff_is_limited_to_approved_1_180_scope():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    assert not paths.intersection(PROTECTED_EXACT)
    for path in paths:
        first = path.split("/", 1)[0]
        assert first not in PROTECTED_DIRS
        assert "secret" not in path.casefold()
        assert not path.casefold().endswith((".env", ".env.local"))
        assert "/endpoints/" not in f"/{path.casefold()}/"
        assert "/routers/" not in f"/{path.casefold()}/"


def test_backend_payload_and_runtime_paths_have_no_diff():
    protected_diff = git(
        "diff",
        "--name-only",
        "HEAD",
        "--",
        "core/backend_internal_ui_payloads.py",
        "api.py",
        "core",
        "domains",
        "providers",
        "tools",
        "scripts",
        "integrations",
        "runtime",
        "execution",
    )
    assert protected_diff == ""
