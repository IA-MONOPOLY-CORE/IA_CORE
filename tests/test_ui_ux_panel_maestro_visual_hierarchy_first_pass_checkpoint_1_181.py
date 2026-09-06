"""Contract and scope checks for the UI/UX 1.181 visual checkpoint."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_1_181.md"
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
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_1_181.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py",
}

HISTORICAL_ALLOWLIST_TESTS = {
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
}

ALLOWED_DIFF = CHECKPOINT_FILES | HISTORICAL_ALLOWLIST_TESTS

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
    "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_PASSED",
    "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_PENDING_MINOR_FIX",
    "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_BLOCKED",
}

NEXT_PROMPT = (
    "PROMPT UI/UX 1.182 — Seleccionar segunda pasada de jerarquía visual "
    "del Panel Maestro IA_CORE contract-aware"
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


def test_document_exists_and_records_checkpoint_evidence():
    assert DOC.is_file()
    text = read(DOC)
    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Visual Hierarchy First Pass Checkpoint 1.181",
            "d960aeb",
            "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_PASSED",
            "ready_for_ui_ux_1_181_visual_hierarchy_checkpoint_or_second_pass",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "P0",
            "P1",
            "P2",
            "P3",
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
            "Request Contract Preview",
        ],
    )
    assert any(decision in text for decision in VALID_DECISIONS)


def test_passed_checkpoint_has_readiness_and_exact_next_prompt():
    text = read(DOC)
    if "UI_UX_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_PASSED" in text:
        assert "ready_for_ui_ux_1_182_visual_hierarchy_second_pass_selection" in text
        assert NEXT_PROMPT in text


def test_readmes_record_the_scoped_1_181_checkpoint():
    assert_markers(
        read(README),
        [
            "UI/UX 1.181",
            "checkpoint de primera pasada de jerarquia visual",
            "d960aeb",
            "no hay implementacion nueva",
            "no backend",
            "no-runtime",
            "no-execution",
            "ready_for_ui_ux_1_182_visual_hierarchy_second_pass_selection",
        ],
    )
    assert_markers(
        read(WEB_README),
        [
            "UI/UX 1.181",
            "checkpoint visual",
            "P0 preservado",
            "Estado",
            "Contrato",
            "Limites",
            "Evidencia",
            "Proximo paso",
            "no backend",
            "no runtime",
            "no execution",
            "UI/UX 1.182",
        ],
    )


def test_active_html_keeps_the_read_only_p0_contract():
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
            "Proximo paso",
            "evidencia contractual completa sigue debajo",
        ],
    )
    assert 'data-visual-hierarchy-first-pass="1.180"' in read(INDEX)
    assert 'data-p0-layer="visual-hierarchy-1.180"' in block


def test_active_css_keeps_p0_and_responsive_layout_signals():
    assert_markers(
        read(STYLES),
        [
            "first-pass P0 hierarchy",
            ".p0-command-summary",
            ".p0-reading-route",
            ".p0-command-grid",
            ".p0-summary-card",
            ".p0-evidence-next",
            "display: grid",
            "flex-wrap: wrap",
            "@media (max-width: 760px)",
            "@media (max-width: 480px)",
        ],
    )


def test_p1_p2_p3_right_panel_and_preview_remain_present():
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
    assert_markers(
        html[html.index('id="request-contract-preview-screen"') :],
        ["read-only", "no-submit", "no-dispatch", "no-execution"],
    )


def test_contract_renderer_keeps_required_fields_and_honest_fallbacks():
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


def test_current_diff_is_limited_to_checkpoint_and_strict_continuity():
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


def test_historical_tests_can_only_add_1_181_allowlist_continuity():
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
        assert added_paths <= CHECKPOINT_FILES, (
            f"Historical test change exceeds 1.181 continuity: {path}"
        )
        assert "CONTINUITY_1_181" in diff


def test_active_ui_backend_payload_and_runtime_paths_have_no_diff():
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
