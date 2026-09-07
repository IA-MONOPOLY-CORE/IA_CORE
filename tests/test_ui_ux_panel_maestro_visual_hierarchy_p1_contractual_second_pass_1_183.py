"""Focused contract checks for UI/UX 1.183 P1 contractual hierarchy."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
BACKEND_PAYLOAD = ROOT / "core" / "backend_internal_ui_payloads.py"
API = ROOT / "api.py"

IMPLEMENTATION_FILES = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
}

HISTORICAL_ALLOWLIST_TESTS = {
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
IMPLEMENTATION_FILES |= CONTINUITY_1_184

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
IMPLEMENTATION_FILES |= CONTINUITY_1_185

CONTINUITY_1_186 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184 and CONTINUITY_1_185 remain preserved; CONTINUITY_1_186 is additive and scoped to the matrix visual demotion.
ALLOWED_DIFF |= CONTINUITY_1_186
IMPLEMENTATION_FILES |= CONTINUITY_1_186

CONTINUITY_1_187 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_186 remain preserved; CONTINUITY_1_187 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185 and CONTINUITY_1_186 remain preserved.
ALLOWED_DIFF |= CONTINUITY_1_187
IMPLEMENTATION_FILES |= CONTINUITY_1_187

CONTINUITY_1_188 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_188.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186 and CONTINUITY_1_187 remain preserved; CONTINUITY_1_188 is additive.
ALLOWED_DIFF |= CONTINUITY_1_188
CONTINUITY_1_189 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_1_189.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.
ALLOWED_DIFF |= CONTINUITY_1_189
CONTINUITY_1_189_A = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md", "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py"}
# CONTINUITY_1_175 through CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
ALLOWED_DIFF |= CONTINUITY_1_189_A
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188 and CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187 and CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.
IMPLEMENTATION_FILES |= CONTINUITY_1_189
IMPLEMENTATION_FILES |= CONTINUITY_1_188

PROTECTED_EXACT = {
    ".env",
    "api.py",
    "core/backend_internal_ui_payloads.py",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
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

VALID_DECISIONS = {
    "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_PASSED",
    "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_PENDING_MINOR_FIX",
    "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_BLOCKED",
}

NEXT_PROMPT = (
    "PROMPT UI/UX 1.184 — Checkpoint de segunda pasada P1 contractual del "
    "Panel Maestro IA_CORE contract-aware"
)


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


def p0_block(text: str) -> str:
    start = text.index('<section class="four-screen-baseline-summary p0-command-summary"')
    end = text.index('<div class="final-screen-contracts-rehousing', start)
    return text[start:end]


def p1_block(text: str) -> str:
    start = text.index('<div class="final-screen-contracts-rehousing"')
    end = text.index('<section class="closure-matrix-section', start)
    return text[start:end]


def test_document_exists_and_records_required_contract_and_scope_markers():
    assert DOC.is_file()
    text = read(DOC)
    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Visual Hierarchy P1 Contractual Second Pass 1.183",
            "aeb7607",
            "UI_UX_VISUAL_HIERARCHY_SECOND_PASS_SELECTED",
            "ready_for_ui_ux_1_183_visual_hierarchy_second_pass_implementation",
            "Candidato C",
            "P1",
            "Contract Overview",
            "Blocked",
            "Forbidden",
            "Validation",
            "Readiness",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "no panel derecho",
            "no matriz",
            "no widgets contract-aware",
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


def test_passed_decision_has_matching_readiness_and_exact_next_prompt():
    text = read(DOC)
    if "UI_UX_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_PASSED" in text:
        assert "ready_for_ui_ux_1_184_p1_contractual_second_pass_checkpoint" in text
        assert NEXT_PROMPT in text


def test_readmes_record_p1_implementation_without_capability_expansion():
    assert_markers(
        read(README),
        [
            "UI/UX 1.183",
            "segunda pasada P1 contractual",
            "aeb7607",
            "P0 preservado",
            "P1 ordenado",
            "P2/P3 preservados",
            "panel derecho preservado",
            "widgets contract-aware preservados",
            "no backend",
            "no-runtime",
            "no-execution",
            "no endpoints",
            "no payload v2",
            "ready_for_ui_ux_1_184_p1_contractual_second_pass_checkpoint",
        ],
    )
    assert_markers(
        read(WEB_README),
        [
            "UI/UX 1.183",
            "P1 contractual",
            "Contract Overview",
            "Blocked & Forbidden",
            "Validation & Readiness",
            "Panel Maestro",
            "contract-aware",
            "P0 preservado",
            "P2/P3 preservados",
            "Request Contract Preview preservado",
            "widgets contract-aware preservados",
            "no backend",
            "no runtime",
            "no execution",
            "no endpoints",
            "no payload v2",
            "UI/UX 1.184",
        ],
    )


def test_p0_is_byte_preserved_and_keeps_its_full_reading_route():
    html = read(INDEX)
    baseline = git("show", "HEAD:ui/web/index.html")
    assert p0_block(html) == p0_block(baseline)
    assert_markers(
        p0_block(html),
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
            "Proximo paso",
            "evidencia contractual completa sigue debajo",
        ],
    )


def test_p1_has_one_layer_an_explicit_route_and_preserved_screen_order():
    html = read(INDEX)
    block = p1_block(html)
    assert html.count('data-p1-layer="contractual-second-pass-1.183"') == 1
    assert html.count("data-contract-screen=") == 4
    assert_markers(
        block,
        [
            "P1",
            "Lectura contractual principal",
            "Contrato",
            "Acciones declaradas",
            "Acciones prohibidas",
            "Bloqueos",
            "Validacion",
            "Readiness",
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
    ordered_ids = [
        'id="contract-overview-screen"',
        'id="blocked-forbidden-screen"',
        'id="validation-readiness-screen"',
        'id="request-contract-preview-screen"',
    ]
    positions = [block.index(marker) for marker in ordered_ids]
    assert positions == sorted(positions)
    for stage in ["contract", "actions-boundaries", "validation"]:
        assert f'data-p1-stage="{stage}"' in block


def test_p2_p3_panel_matrix_and_widget_anchors_remain_available():
    html = read(INDEX)
    for marker in [
        'id="request-contract-preview-screen"',
        'id="closure-matrix-ui-ux-1x"',
        'id="request-draft-panel"',
        'id="functional-widgets"',
        'id="settings-fab"',
        'id="add-fab"',
        'id="domain-fab"',
    ]:
        assert marker in html


def test_p1_styles_are_scoped_responsive_and_layout_safe():
    css = read(STYLES)
    assert_markers(
        css,
        [
            "data-visual-hierarchy-second-pass",
            "data-p1-layer",
            "p1-contractual-route",
            "p1-contractual-stage",
            "grid",
            "minmax(0, 1fr)",
            "overflow-wrap",
            "@media (max-width: 980px)",
            "@media (max-width: 760px)",
            "@media (max-width: 480px)",
        ],
    )


def test_contract_widget_renderer_keeps_all_required_fields_and_fallbacks():
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
    ]:
        assert marker in script


def test_no_payload_v2_or_active_operational_state_is_introduced():
    active_contract = "\n".join(
        read(path) for path in [INDEX, STYLES, WIDGETS, BACKEND_PAYLOAD, API]
    )
    for pattern in [
        r"backend_internal_ui_payload\.v2",
        r"payload\.v2",
        r"schema_version[\"']?\s*[:=]\s*[\"']v2[\"']",
    ]:
        assert not re.search(pattern, active_contract, flags=re.IGNORECASE)

    p1 = p1_block(read(INDEX))
    for pattern in [
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\brunning\b',
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\bexecuting\b',
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\bdispatching\b',
        r'data-[^=]*(?:state|status)[^=]*="[^"]*\bsubmitted\b',
        r">\s*ready to run\s*<",
        r">\s*processing request\s*<",
        r">\s*capability active\s*<",
    ]:
        assert not re.search(pattern, p1, flags=re.IGNORECASE)


def test_current_diff_is_limited_to_implementation_and_strict_continuity():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    assert not paths.intersection(PROTECTED_EXACT)
    for path in paths:
        normalized_path = path.strip("/")
        assert normalized_path.split("/", 1)[0] not in PROTECTED_DIRS
        lowered = normalized_path.casefold()
        assert "secret" not in lowered
        assert not lowered.endswith((".env", ".env.local"))
        assert "/endpoints/" not in f"/{lowered}/"
        assert "/routers/" not in f"/{lowered}/"


def test_historical_tests_only_add_1_183_allowlist_continuity():
    for path in changed_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [
            line for line in diff.splitlines()
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
        assert added_paths <= IMPLEMENTATION_FILES
        assert "CONTINUITY_1_183" in diff


def test_protected_ui_backend_payload_and_runtime_paths_have_no_diff():
    protected_diff = set(
        filter(
            None,
            git(
                "diff",
                "--name-only",
                "HEAD",
                "--",
                "ui/web/backend-contract-widgets.js",
                "ui/web/i18n_es.json",
                "ui/web/admin-panels.js",
                "ui/web/console-interactions.js",
                "ui/web/domains.js",
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
            ).splitlines(),
        )
    )
    assert not protected_diff


def test_implementation_test_requires_no_browser_network_or_dependency_install():
    source = read(Path(__file__))
    assert not re.search(
        r"^\s*(?:from|import)\s+(?:selenium|playwright|requests)\b",
        source,
        flags=re.MULTILINE,
    )
    assert "pip" + " install" not in source.casefold()

PROTECTED_EXACT.discard("ui/web/styles.css")
