from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_1_171.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/src",
    "ui/web/styles",
    "ui/web/i18n",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
    "backend",
    "core",
    "domains",
    "providers",
    "integrations",
    "tools",
]


FORBIDDEN_STATIC_ARTIFACTS = [
    ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json",
    ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json",
    ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json",
    ROOT / "tests" / "fixtures" / "ui_top_15_elite_audit_v1.json",
    ROOT / "ui" / "web" / "contracts" / "ui_ux_1x_closure_readiness_matrix.v1.json",
    ROOT / "tests" / "fixtures" / "ui_ux_1x_closure_readiness_matrix_v1.json",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def test_publication_document_exists_and_has_identity():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro IA_CORE",
        "Restore Point Publication 1.171",
        "588f188",
        "65b44b4",
        "branch: `main`",
        "ahead/behind inicial: `0 5`",
        "working tree limpio",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_SELECTED",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
    ]:
        assert marker in text


def test_publication_document_lists_expected_commits_and_scope():
    text = read(DOC)
    for marker in [
        "cdb4075",
        "f15dc23",
        "1abb06e",
        "d1fc9ca",
        "588f188",
        "commit 1.171 a crear en este prompt",
        "no runtime",
        "no execution",
        "no integraciones",
        "no endpoints",
        "no backend",
        "no UI activa",
        "no User Panel",
        "no Owner Panel",
        "no multi-tenant",
        "no telemetry",
    ]:
        assert marker in text


def test_publication_document_declares_forbidden_future_docs_not_created():
    text = read(DOC)
    for marker in [
        "FUTURE_INTEGRATIONS_REGISTRY",
        "FUTURE_ORGANIZATIONAL_ACCESS_MODEL",
        "FUTURE_INTERNAL_COMMUNICATION_MODEL",
        "FUTURE_FINANCIAL_MIRROR",
        "FUTURE_SECURITY",
        "FUTURE_OWNER_SOVEREIGNTY",
        "FUTURE_LEGAL",
        "FUTURE_TAX",
        "FUTURE_ONBOARDING",
        "no Strategic Future Integrations Registry todavia",
        "no documentacion futura de organizacion",
    ]:
        assert marker in text


def test_publication_criteria_and_push_policy_are_explicit():
    text = read(DOC)
    for marker in [
        "el test 1.171 pasa",
        "las validaciones heredadas pasan",
        "el commit 1.171 se crea",
        "git push origin main",
        "HEAD y origin/main quedan alineados",
        "working tree queda limpio",
        "Push permitido y obligatorio en este prompt",
        "Force push prohibido",
        "Tags, releases y branches adicionales prohibidos",
    ]:
        assert marker in text


def test_readmes_record_restore_point_1_171_published():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Cursor vigente 1.171 restore point README/docs/UI publicado",
            "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
            "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_SELECTED",
            "PROMPT UI/UX 1.171 - Publicar restore point post fix consistencia README docs UI Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "docs(ui): publicar restore point consistencia readme docs ui",
            "origin/main = 65b44b4",
            "main ahead de origin/main por 5 commits",
            "no-runtime",
            "no-execution",
            "no UI activa",
        ]:
            assert marker in text


def test_static_artifacts_absent_and_protected_paths_untouched():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"

    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_1_171.md",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_restore_point_publication_1_171.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
