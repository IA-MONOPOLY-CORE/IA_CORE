"""Formal, product-read-only checkpoint for the closed UI/UX 1.192 state."""

from pathlib import Path
import subprocess
import unicodedata

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "ca9a8c8"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_CHECKPOINT_1_193.md"
REPORT_192 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_AFFORDANCES_SEVERITY_1_192.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PRODUCT_FILES = {
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
ALLOWED_1_193 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "tests/ui_ux_1_192_scope.py",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py",
    "docs/UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_CHECKPOINT_1_193.md",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
    "docs/UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_SCALE_AUDIT_1_193.md",
    "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
}
ALLOWED_1_193 |= scope.CONTINUITY_1_194
ALLOWED_1_193 |= scope.CONTINUITY_1_195


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return " ".join("".join(c for c in decomposed if not unicodedata.combining(c)).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def test_checkpoint_document_contains_closed_192_contract():
    assert DOC.is_file()
    content = normalized(read(DOC))
    markers = [
        "UI/UX Panel Maestro Controlled Double Scope Checkpoint 1.193",
        "ca9a8c8", "main", "origin/main", "ahead/behind", "working tree", "limpio",
        "UI_UX_CONTROLLED_DOUBLE_SCOPE_AFFORDANCES_SEVERITY_PASSED",
        "GATE_1_AFFORDANCES_BLOCKED_PASSED", "GATE_2_SEVERITY_VISUAL_PASSED",
        "DOUBLE_SCOPE_FULLY_IMPLEMENTED", "NO_CORRECTIVE_NEEDED",
        "055e70e", "6ae13f4", "1c41cd8", "275 tests", "P0", "P1", "Matriz P3",
        "widgets contract-aware", "Request Draft Panel", "html", "css", "javascript",
        "i18n", "backend", "payload", "payload v2", "no runtime", "no execution",
        "no endpoints", "no integrations", "UI_UX_CONTROLLED_DOUBLE_SCOPE_AFFORDANCES_SEVERITY_CHECKPOINT_PASSED",
        "ui_ux_1_192_safe_checkpoint_at_ca9a8c8", "deny-by-default", "continuidad 1.193",
    ]
    missing = [marker for marker in markers if normalized(marker) not in content]
    assert not missing, missing


def test_readmes_record_checkpoint_without_product_scope():
    for path in (README, WEB_README):
        content = normalized(read(path))
        for marker in ("UI/UX 1.193", "checkpoint", "1.192", "no UI", "no backend", "no runtime", "no execution"):
            assert normalized(marker) in content, (path, marker)


def test_product_files_are_unchanged_from_published_base():
    changed = set(filter(None, git("diff", "--name-only", BASE, "HEAD", "--", ".").splitlines()))
    assert changed <= ALLOWED_1_193, sorted(changed - ALLOWED_1_193)
    for path in PRODUCT_FILES - {"ui/web/styles.css"}:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path
    current_css = (ROOT / "ui/web/styles.css").read_text(encoding="utf-8")
    scope.assert_css(scope.text(scope.git(ROOT, "show", f"{scope.BASE}:{scope.CSS}")), current_css, ROOT)


def test_active_contract_remains_v1_and_non_operational():
    active = "\n".join(read(ROOT / path) for path in (
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "core/backend_internal_ui_payloads.py",
    )).casefold()
    for marker in ("backend_internal_ui_payload.v1", "allowed_actions", "forbidden_actions", "blocked_capabilities", "no_payload", "not_available"):
        assert marker in active, marker
    for forbidden in ("backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"'):
        assert forbidden not in active, forbidden


def test_continuity_allowlist_is_exact_and_additive():
    helper = read(ROOT / "tests" / "ui_ux_1_192_scope.py")
    assert "CONTINUITY_1_193" in helper
    for path in (
        "docs/UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_CHECKPOINT_1_193.md",
        "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
        "docs/UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_SCALE_AUDIT_1_193.md",
        "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
    ):
        assert path in helper
    assert "aserciones" in normalized(read(REPORT_192))
