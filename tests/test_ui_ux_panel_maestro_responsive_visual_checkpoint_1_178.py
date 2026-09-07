"""Checkpoint checks for UI/UX 1.178 responsive visual stability."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_RESPONSIVE_VISUAL_CHECKPOINT_1_178.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
PAYLOAD_SOURCE = ROOT / "core" / "backend_internal_ui_payloads.py"

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_RESPONSIVE_VISUAL_CHECKPOINT_1_178.md",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
}

CONTINUITY_1_180 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
}

ALLOWED_DIFF |= CONTINUITY_1_180

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

APPROVED_1_180_ACTIVE_UI = {"ui/web/index.html", "ui/web/styles.css"}
REQUIRED_1_180 = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
}

# The complete 1.183 artifact set is the current authorized active-UI gate.
REQUIRED_1_183 = CONTINUITY_1_183
REQUIRED_1_180 = REQUIRED_1_183

PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "ui/web/styles.css",
    "core/backend_internal_ui_payloads.py",
    "api.py",
    "core",
    "domains",
    "providers",
    "tools",
    "scripts",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def assert_markers(path: Path, markers: list[str]) -> None:
    text = normalized(read(path))
    missing = [marker for marker in markers if normalized(marker) not in text]
    assert not missing, f"{path.name}: missing {missing}"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return tracked | untracked


def test_document_exists_and_records_checkpoint_chain():
    assert DOC.is_file()
    assert_markers(
        DOC,
        [
            "UI/UX Panel Maestro Responsive Visual Checkpoint 1.178",
            "d98e999",
            "4403489",
            "fdc2b7d",
            "e9f5b94",
            "UI_UX_WIDGETS_CONTRACT_AWARE_CHECKPOINTED",
            "UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_STRATEGIC_DOCS",
            "UI_UX_RESPONSIVE_DEBT_PANEL_MAESTRO_RESOLVED",
            "UI_UX_POST_1_175_SURGICAL_AUDIT_PASSED",
            "ready_for_ui_ux_1_178_responsive_visual_checkpoint",
        ],
    )


def test_document_records_responsive_and_visual_evidence():
    text = normalized(read(DOC))
    assert (
        normalized("overflow horizontal movil ausente") in text
        or normalized("overflow horizontal móvil ausente") in text
    )
    for marker in [
        "sidebar/drawer estable",
        "resize desktop",
        "mobile",
        "390",
        "844",
        "1440",
        "1000",
        "clientWidth = 375",
        "scrollWidth = 375",
        "Codex In-app Browser",
    ]:
        assert normalized(marker) in text


def test_document_records_contract_and_backend_boundaries():
    assert_markers(
        DOC,
        [
            "source",
            "status",
            "fallback",
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "deny-by-default",
            "no_payload",
            "not_available",
            "backend_internal_ui_payload.v1",
            "no payload v2",
            "no backend",
            "no runtime",
            "no execution",
            "no endpoints",
            "no integraciones",
            "no integrations",
            "no credenciales",
            "no credentials",
        ],
    )


def test_document_records_strategic_docs_future_only_and_passed_readiness():
    text = read(DOC)
    assert (
        "Strategic Docs 1.1-1.3" in text
        or "Strategic Docs 1.1–1.3" in text
    )
    assert "documentacion futura" in normalized(text) or "documentación futura" in normalized(text)
    assert "UI_UX_RESPONSIVE_VISUAL_CHECKPOINT_PASSED" in text
    assert "ready_for_ui_ux_1_179_panel_maestro_visual_hierarchy" in text
    assert (
        "PROMPT UI/UX 1.179 — Reordenar jerarquía visual del Panel Maestro "
        "IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_readme_records_1_178_briefly():
    assert_markers(
        README,
        [
            "UI/UX 1.178",
            "checkpoint responsive visual",
            "d98e999",
            "overflow movil ausente",
            "sidebar/drawer estable",
            "widgets contract-aware preservados",
            "no backend/runtime/payload v2",
            "ready_for_ui_ux_1_179_panel_maestro_visual_hierarchy",
        ],
    )


def test_web_readme_records_1_178_briefly():
    assert_markers(
        WEB_README,
        [
            "UI/UX 1.178",
            "overflow movil ausente",
            "sidebar/drawer estable",
            "desktop/mobile/resize verificados",
            "widgets contract-aware preservados",
            "source/status/fallback preservados",
            "deny-by-default/no_payload/not_available preservados",
            "no backend/runtime/payload v2",
            "UI/UX 1.179",
        ],
    )


def test_index_contains_responsive_protection_mechanisms():
    html = read(INDEX)
    lower = html.casefold()
    assert 'data-responsive-debt-fix="1.177"' in html
    required_any = [
        "overflow-x",
        "min-width",
        "max-width",
        "overflow-wrap",
        "word-break",
        "flex-wrap",
        "@media",
        "drawer",
        "sidebar",
        "aria-expanded",
        "resize",
        "clientWidth",
        "scrollWidth",
    ]
    present = [token for token in required_any if token.casefold() in lower]
    assert len(present) >= 8
    for marker in [
        ".four-screen-baseline-summary",
        ".four-screen-baseline-list",
        "grid-template-columns: minmax(0, 1fr)",
        "width: 100%",
        "max-width: 100%",
        "overflow-wrap: anywhere",
        "window.matchMedia('(max-width: 760px)')",
        "syncRequestDraftResponsiveState",
        "handleRequestDraftBreakpointChange",
        "requestDraftMobileViewport.addEventListener('change'",
        "requestDraftPanel.classList.add('collapsed')",
        "requestDraftToggle.focus()",
    ]:
        assert marker in html


def test_contract_widgets_preserve_required_fields_and_deny_by_default():
    script = read(WIDGETS)
    for marker in [
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no_payload",
        "not_available",
        "source",
        "status",
        "fallback",
        "deny-by-default",
        "warnings",
        "errors",
    ]:
        assert marker in script
    assert "fetch(" not in script


def test_prohibited_operational_terms_are_absent_or_guarded():
    active_ui = "\n".join(
        read(path)
        for path in [
            INDEX,
            WIDGETS,
            ROOT / "ui" / "web" / "admin-panels.js",
            ROOT / "ui" / "web" / "console-interactions.js",
            ROOT / "ui" / "web" / "domains.js",
            ROOT / "ui" / "web" / "styles.css",
        ]
        if path.exists()
    )
    for phrase in [
        "preview-and-run",
        "ready to run",
        "DISPATCHING",
        "SUBMITTED",
        "Processing request",
        "Capability active",
    ]:
        assert phrase.casefold() not in active_ui.casefold()

    widget_lines = read(WIDGETS).splitlines()
    guarded_lines = [
        line
        for line in widget_lines
        if re.search(r"\b(running|executing)\b", line, flags=re.I)
    ]
    assert guarded_lines
    assert all(
        "PROHIBITED_ACTIVE_STATUSES" in "\n".join(widget_lines[:30])
        and line.strip().strip(",") in {"'running'", "'executing'"}
        for line in guarded_lines
    )


def test_payload_v2_is_absent_from_active_payload_surfaces():
    tracked_names = git("ls-files").casefold()
    assert "backend_internal_ui_payload.v2" not in tracked_names
    assert "payload.v2" not in tracked_names

    active_contract = "\n".join(read(path) for path in [INDEX, WIDGETS, PAYLOAD_SOURCE])
    forbidden_patterns = [
        r"backend_internal_ui_payload\.v2",
        r"payload\.v2",
        r"schema_version\"\s*:\s*\"v2\"",
        r"schema_version'\s*:\s*'v2'",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, active_contract)


def test_diff_is_limited_to_1_178_documentation_test_checkpoint_scope():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    approved_active_ui = (
        APPROVED_1_180_ACTIVE_UI if REQUIRED_1_180 <= paths else set()
    )
    for protected in PROTECTED_PATHS:
        if protected in approved_active_ui:
            continue
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""


def test_current_prompt_does_not_modify_backend_runtime_or_active_ui():
    paths = changed_paths()
    approved_active_ui = (
        APPROVED_1_180_ACTIVE_UI if REQUIRED_1_180 <= paths else set()
    )
    forbidden_prefixes = (
        "core/",
        "domains/",
        "providers/",
        "tools/",
        "scripts/",
        "integrations/",
        "runtime/",
        "execution/",
        ".github/",
    )
    forbidden_exact = {
        "api.py",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/i18n_es.json",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/styles.css",
        "core/backend_internal_ui_payloads.py",
    }
    assert not (paths.intersection(forbidden_exact) - approved_active_ui)
    assert not any(path.startswith(forbidden_prefixes) for path in paths)
