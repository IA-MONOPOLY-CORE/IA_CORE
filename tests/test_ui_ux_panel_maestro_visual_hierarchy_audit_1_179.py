from pathlib import Path
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_AUDIT_1_179.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

ALLOWED_CHANGED = {
    "README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_AUDIT_1_179.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "ui/web/README.md",
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

ALLOWED_CHANGED |= CONTINUITY_1_180

CONTINUITY_1_181 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_1_181.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py",
}

ALLOWED_CHANGED |= CONTINUITY_1_181

CONTINUITY_1_182 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_1_182.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py",
}

ALLOWED_CHANGED |= CONTINUITY_1_182

CONTINUITY_1_183 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
}

# CONTINUITY_1_181 remains preserved; CONTINUITY_1_183 is additive.
ALLOWED_CHANGED |= CONTINUITY_1_183

CONTINUITY_1_184 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_1_184.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182 and CONTINUITY_1_183 remain preserved; CONTINUITY_1_184 is additive.
ALLOWED_CHANGED |= CONTINUITY_1_184

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
ALLOWED_CHANGED |= CONTINUITY_1_185

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

PROTECTED_FILES = {
    "api.py",
    "core/backend_internal_ui_payloads.py",
    "ui/web/admin-panels.js",
    "ui/web/backend-contract-widgets.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "ui/web/i18n_es.json",
    "ui/web/index.html",
    "ui/web/styles.css",
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
    "UI_UX_VISUAL_HIERARCHY_AUDIT_PASSED",
    "UI_UX_VISUAL_HIERARCHY_AUDIT_PENDING_MORE_EVIDENCE",
    "UI_UX_VISUAL_HIERARCHY_AUDIT_BLOCKED",
}

NEXT_PROMPTS = {
    "PROMPT UI/UX 1.180 — Implementar primera pasada de jerarquía visual superior del Panel Maestro IA_CORE contract-aware sin backend/no-runtime/no-execution",
    "PROMPT UI/UX 1.180 — Prototipo documental de jerarquía visual del Panel Maestro IA_CORE sin tocar UI activa",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(
        character for character in decomposed if not unicodedata.combining(character)
    )
    return without_marks.lower()


def assert_contains(text: str, marker: str) -> None:
    assert normalize(marker) in normalize(text), f"Missing marker: {marker}"


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def changed_paths() -> set[str]:
    changed = set(git_lines("diff", "--name-only", "HEAD"))
    untracked = set(git_lines("ls-files", "--others", "--exclude-standard"))
    return changed | untracked


def touches_protected(path: str) -> bool:
    normalized = path.replace("\\", "/").strip("/")
    if normalized in PROTECTED_FILES:
        return True

    top_level = normalized.split("/", 1)[0]
    return top_level in PROTECTED_DIRS


def test_visual_hierarchy_audit_document_exists_and_contains_contract_markers():
    assert DOC.exists()
    text = read(DOC)

    required_markers = [
        "UI/UX Panel Maestro Visual Hierarchy Audit 1.179",
        "3da91a8",
        "UI_UX_RESPONSIVE_VISUAL_CHECKPOINT_PASSED",
        "ready_for_ui_ux_1_179_panel_maestro_visual_hierarchy",
        "contractualmente solido",
        "visualmente denso",
        "jerarquia",
        "P0",
        "P1",
        "P2",
        "P3",
        "Estado",
        "Contrato",
        "Limites",
        "Evidencia",
        "Proximo paso",
        "Request Contract Preview",
        "Matriz de cierre",
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
    ]

    for marker in required_markers:
        assert_contains(text, marker)

    assert any(decision in text for decision in VALID_DECISIONS)


def test_passed_decision_declares_readiness_and_exact_next_prompt():
    text = read(DOC)
    if "UI_UX_VISUAL_HIERARCHY_AUDIT_PASSED" not in text:
        return

    assert "ready_for_ui_ux_1_180_visual_hierarchy_first_pass" in text
    assert any(prompt in text for prompt in NEXT_PROMPTS)


def test_readmes_record_1_179_without_runtime_or_backend_scope():
    readme = read(README)
    web_readme = read(WEB_README)

    for marker in [
        "UI/UX 1.179",
        "auditoria de jerarquia visual",
        "3da91a8",
        "no backend",
        "no-runtime",
        "no-execution",
        "ready_for_ui_ux_1_180_visual_hierarchy_first_pass",
    ]:
        assert_contains(readme, marker)

    for marker in [
        "UI/UX 1.179",
        "jerarquia visual",
        "Panel Maestro",
        "contract-aware",
        "no backend",
        "no-runtime",
        "no-execution",
        "1.180",
    ]:
        assert_contains(web_readme, marker)


def test_current_diff_is_limited_to_documentation_and_this_contract_test():
    changed = changed_paths()
    assert changed <= ALLOWED_CHANGED


def test_protected_ui_backend_runtime_payload_paths_have_no_diff():
    paths = changed_paths()
    approved_active_ui = (
        APPROVED_1_180_ACTIVE_UI if REQUIRED_1_180 <= paths else set()
    )
    protected_diff = set(
        git_lines(
            "diff",
            "--name-only",
            "HEAD",
            "--",
            "ui/web/index.html",
            "ui/web/backend-contract-widgets.js",
            "ui/web/styles.css",
            "ui/web/admin-panels.js",
            "ui/web/console-interactions.js",
            "ui/web/domains.js",
            "ui/web/i18n_es.json",
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
    )
    assert not protected_diff - approved_active_ui
    assert not {
        path
        for path in paths
        if touches_protected(path) and path not in approved_active_ui
    }
