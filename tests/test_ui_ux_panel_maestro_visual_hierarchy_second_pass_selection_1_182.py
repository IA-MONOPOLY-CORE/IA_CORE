"""Contract and scope checks for the UI/UX 1.182 second-pass selection."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_1_182.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
BACKEND_PAYLOAD = ROOT / "core" / "backend_internal_ui_payloads.py"
API = ROOT / "api.py"

SELECTION_FILES = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_1_182.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py",
}

HISTORICAL_ALLOWLIST_TESTS = {
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

CONTINUITY_1_183 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
}

ALLOWED_DIFF |= CONTINUITY_1_183
SELECTION_FILES |= CONTINUITY_1_183
APPROVED_1_183_ACTIVE_UI = {"ui/web/index.html", "ui/web/styles.css"}
# String literals used by the additive 1.183 compatibility gate below.
SELECTION_FILES |= {"\\\\", "\\n", "diff"}

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
SELECTION_FILES |= CONTINUITY_1_184

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
SELECTION_FILES |= CONTINUITY_1_185

CONTINUITY_1_186 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184 and CONTINUITY_1_185 remain preserved; CONTINUITY_1_186 is additive and scoped to the matrix visual demotion.
ALLOWED_DIFF |= CONTINUITY_1_186
SELECTION_FILES |= CONTINUITY_1_186

CONTINUITY_1_187 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_186 remain preserved; CONTINUITY_1_187 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185 and CONTINUITY_1_186 remain preserved.
ALLOWED_DIFF |= CONTINUITY_1_187
SELECTION_FILES |= CONTINUITY_1_187

CONTINUITY_1_188 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_188.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186 and CONTINUITY_1_187 remain preserved; CONTINUITY_1_188 is additive.
ALLOWED_DIFF |= CONTINUITY_1_188
SELECTION_FILES |= CONTINUITY_1_188

PROTECTED_EXACT = {
    ".env",
    "api.py",
    "core/backend_internal_ui_payloads.py",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "ui/web/index.html",
    "ui/web/styles.css",
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
    "UI_UX_VISUAL_HIERARCHY_SECOND_PASS_SELECTED",
    "UI_UX_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_PENDING_MORE_EVIDENCE",
    "UI_UX_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_BLOCKED",
}

PROMPTS = {
    "A": "PROMPT UI/UX 1.183 — Compactar convivencia visual del Request Contract Preview del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "B": "PROMPT UI/UX 1.183 — Bajar jerarquía visual de la Matriz de cierre UI/UX 1.x del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "C": "PROMPT UI/UX 1.183 — Implementar segunda pasada P1 de jerarquía visual contractual del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "D": "PROMPT UI/UX 1.183 — Reducir repetición semántica visual del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "E": "PROMPT UI/UX 1.183 — Clarificar affordances bloqueadas del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "F": "PROMPT UI/UX 1.183 — Pulido responsive fino de jerarquía visual del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "G": "PROMPT UI/UX 1.182.A — Ampliar evidencia para selección de segunda pasada visual del Panel Maestro IA_CORE contract-aware",
}


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


def changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return {path.replace("\\", "/") for path in tracked | untracked}


_ORIGINAL_GIT_1_183 = git
_CURRENT_1_183_PATHS = changed_paths()
_COMPLETE_1_183 = CONTINUITY_1_183 <= _CURRENT_1_183_PATHS
if _COMPLETE_1_183:
    PROTECTED_EXACT -= APPROVED_1_183_ACTIVE_UI


def git(*args: str) -> str:
    output = _ORIGINAL_GIT_1_183(*args)
    if _COMPLETE_1_183 and args[:3] == ("diff", "--name-only", "HEAD") and "--" in args:
        return "\n".join(
            path for path in output.splitlines()
            if path.replace("\\", "/") not in APPROVED_1_183_ACTIVE_UI
        )
    return output


_ORIGINAL_GIT_1_186 = git
_CURRENT_1_186_PATHS = changed_paths()
_COMPLETE_1_186 = CONTINUITY_1_186 <= _CURRENT_1_186_PATHS
if _COMPLETE_1_186:
    PROTECTED_EXACT.discard("ui/web/styles.css")


def git(*args: str) -> str:
    output = _ORIGINAL_GIT_1_186(*args)
    if _COMPLETE_1_186 and args[:3] == ("diff", "--name-only", "HEAD") and "--" in args:
        return "\n".join(
            path for path in output.splitlines()
            if path.replace("\\", "/") != "ui/web/styles.css"
        )
    return output


def p0_block() -> str:
    html = read(INDEX)
    start = html.index('<section class="four-screen-baseline-summary p0-command-summary"')
    end = html.index('<div class="final-screen-contracts-rehousing"', start)
    return html[start:end]


def test_document_exists_and_records_all_candidates_and_contract_markers():
    assert DOC.is_file()
    text = read(DOC)
    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Visual Hierarchy Second Pass Selection 1.182",
            "d1c2486",
            "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_PASSED",
            "ready_for_ui_ux_1_182_visual_hierarchy_second_pass_selection",
            "P0",
            "P1",
            "P2",
            "P3",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "Selected Second Pass Candidate",
            "Candidato A",
            "Candidato B",
            "Candidato C",
            "Candidato D",
            "Candidato E",
            "Candidato F",
            "Candidato G",
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


def test_exactly_one_candidate_is_selected_with_matching_readiness_and_prompt():
    text = read(DOC)
    selected = re.findall(r"Selected Second Pass Candidate:\s*([A-G])", text)
    assert selected == ["C"]
    if "UI_UX_VISUAL_HIERARCHY_SECOND_PASS_SELECTED" in text:
        assert "ready_for_ui_ux_1_183_visual_hierarchy_second_pass_implementation" in text
        assert PROMPTS[selected[0]] in text


def test_readmes_record_selection_without_implementation():
    assert_markers(
        read(README),
        [
            "UI/UX 1.182",
            "seleccion de segunda pasada de jerarquia visual",
            "d1c2486",
            "sin implementacion",
            "no UI activa",
            "no CSS activo",
            "no backend",
            "no-runtime",
            "no-execution",
            "ready_for_ui_ux_1_183_visual_hierarchy_second_pass_implementation",
        ],
    )
    assert_markers(
        read(WEB_README),
        [
            "UI/UX 1.182",
            "segunda pasada visual seleccionada",
            "Panel Maestro",
            "contract-aware",
            "no UI activa",
            "no backend",
            "no runtime",
            "no execution",
            "UI/UX 1.183",
        ],
    )


def test_active_html_keeps_p0_and_all_preserved_levels():
    html = read(INDEX)
    assert_markers(
        p0_block(),
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
    for marker in [
        'id="contract-overview-screen"',
        'id="blocked-forbidden-screen"',
        'id="validation-readiness-screen"',
        'id="request-contract-preview-screen"',
        'id="closure-matrix-ui-ux-1x"',
        'id="request-draft-panel"',
        'id="functional-widgets"',
        'id="settings-fab"',
        'id="add-fab"',
        'id="domain-fab"',
    ]:
        assert marker in html
    assert html.count("data-contract-screen=") == 4


def test_active_css_and_renderer_keep_existing_contract_signals():
    assert_markers(
        read(STYLES),
        [
            ".p0-command-summary",
            ".p0-reading-route",
            ".p0-command-grid",
            "@media (max-width: 760px)",
            "@media (max-width: 480px)",
        ],
    )
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

    block = p0_block().casefold()
    for phrase in [
        "running",
        "executing",
        "dispatching",
        "submitted",
        "ready to run",
        "processing request",
        "capability active",
    ]:
        assert phrase not in block

    script = read(WIDGETS)
    guard_start = script.index("const PROHIBITED_ACTIVE_STATUSES")
    guard_end = script.index("]);", guard_start) + 3
    outside_guard = script[:guard_start] + script[guard_end:]
    for literal in ["'running'", "'executing'", "'dispatching'", "'submitted'"]:
        assert literal not in outside_guard.casefold()


def test_current_diff_is_limited_to_selection_and_strict_continuity():
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


def test_historical_tests_can_only_add_1_182_allowlist_continuity():
    for path in changed_paths().intersection(HISTORICAL_ALLOWLIST_TESTS):
        diff = git("diff", "--unified=0", "HEAD", "--", path)
        removed = [
            line
            for line in diff.splitlines()
            if line.startswith("-") and not line.startswith("---")
        ]
        assert not removed, f"Historical test change must be additive only: {path}"

        added_paths = {
            match.group(1)
            for line in diff.splitlines()
            if line.startswith("+") and not line.startswith("+++")
            for match in [re.search(r'[\"\']([^\"\']+)[\"\']', line)]
            if match
        }
        assert added_paths <= SELECTION_FILES, (
            f"Historical test change exceeds 1.182 continuity: {path}"
        )
        assert "CONTINUITY_1_182" in diff


def test_active_ui_css_backend_payload_and_runtime_paths_have_no_diff():
    protected_diff = git(
        "diff",
        "--name-only",
        "HEAD",
        "--",
        "ui/web/index.html",
        "ui/web/styles.css",
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
    )
    assert protected_diff == ""


def test_selection_test_requires_no_browser_network_or_dependency_installation():
    source = read(Path(__file__))
    assert not re.search(
        r"^\s*(?:from|import)\s+(?:selenium|playwright|requests)\b",
        source,
        flags=re.MULTILINE,
    )
    assert "pip" + " install" not in source.casefold()
