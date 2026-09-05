from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_RESTORE_POINT_DECISION_1_170.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


FORBIDDEN_STATIC_ARTIFACTS = [
    ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json",
    ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json",
    ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json",
    ROOT / "tests" / "fixtures" / "ui_top_15_elite_audit_v1.json",
    ROOT / "ui" / "web" / "contracts" / "ui_ux_1x_closure_readiness_matrix.v1.json",
    ROOT / "tests" / "fixtures" / "ui_ux_1x_closure_readiness_matrix_v1.json",
]


PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/main.js",
    "ui/web/state.js",
    "ui/web/app.js",
    "ui/web/data.js",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
    "core",
    "domains",
    "providers",
    "integrations",
    "tools",
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


def test_decision_document_exists_and_records_git_context():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro README Docs UI Consistency Restore Point Decision 1.170",
        "d1fc9ca",
        "65b44b4",
        "65b44b4 docs(ui): publicar restore point top 15 readiness",
        "origin/main",
        "main",
        "ahead",
        "4 commits",
        "behind de `origin/main` por `0 commits`",
        "working tree inicial limpio",
    ]:
        assert marker in text


def test_decision_document_lists_expected_local_commits():
    text = read(DOC)
    for marker in [
        "cdb4075 docs(ui): planificar siguiente recomendacion top 15",
        "f15dc23 docs(ui): auditar consistencia readme docs ui",
        "1abb06e docs(ui): corregir consistencia readme docs ui",
        "d1fc9ca docs(ui): checkpoint fix consistencia readme docs ui",
    ]:
        assert marker in text


def test_decision_and_publication_policy_are_explicit():
    text = read(DOC)
    allowed = [
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_SELECTED",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_DEFERRED",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_DECISION_NEEDS_REVIEW",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_DECISION_BLOCKED",
    ]
    assert any(decision in text for decision in allowed)
    for marker in [
        "no push en 1.170",
        "no restore point publicado en 1.170",
        "1.171 publicara solo si la decision es selected",
        "PROMPT UI/UX 1.171 - Publicar restore point post fix consistencia README docs UI Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text


def test_findings_and_residual_debt_are_classified():
    text = read(DOC)
    for marker in [
        "README cursor avanzado mas alla del estado esperado",
        "Placeholder drift de hash 1.166",
        "Mojibake en `ui/web/README.md`",
        "Legacy JS local mechanisms require context",
        "FIX_CONFIRMED",
        "ENCAPSULATION_CONFIRMED",
        "RESIDUAL_DOC_DEBT_PRESENT",
        "RESIDUAL_DOC_DEBT_NON_BLOCKING",
        "no equivalen a runtime activo",
        "no autorizan mecanismos nuevos",
    ]:
        assert marker in text


def test_eligibility_checklist_and_safety_boundaries_are_present():
    text = read(DOC)
    for marker in [
        "Checklist de Elegibilidad",
        "Working tree limpio",
        "HEAD local correcto",
        "origin/main correcto",
        "Ahead local esperado",
        "No behind",
        "No diverged",
        "Bloque local coherente",
        "Tests relevantes pasaron",
        "git diff --check",
        "No UI activa modificada",
        "No JS modificado",
        "No backend modificado",
        "No endpoints creados",
        "No runtime/execution activado",
        "No models/tools/integrations invocados",
        "No User Panel creado",
        "No Owner Panel creado",
        "No multi-tenant creado",
        "No telemetria creada",
        "No JSON/fixtures ledger/TOP15/readiness creados",
        "Push puede hacerse en prompt separado",
    ]:
        assert marker in text


def test_forbidden_future_or_operational_work_is_not_current():
    text = read(DOC)
    for marker in [
        "no runtime activado",
        "no execution activado",
        "no dispatcher operativo creado",
        "no modelos invocados",
        "no tools invocados",
        "no integrations invocadas",
        "no User Panel creado",
        "no Owner Panel creado",
        "no multi-tenant creado",
        "no telemetria creada",
        "no OpenClaw/UI-TARS incorporado en este prompt",
        "no UI/UX 1.x cerrado globalmente",
    ]:
        assert marker in text


def test_readmes_record_1_170_cursor_and_next_prompt():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Cursor vigente 1.170 decision restore point README/docs/UI",
            "PROMPT UI/UX 1.170",
            "d1fc9ca docs(ui): checkpoint fix consistencia readme docs ui",
            "1abb06e docs(ui): corregir consistencia readme docs ui",
            "f15dc23 docs(ui): auditar consistencia readme docs ui",
            "cdb4075 docs(ui): planificar siguiente recomendacion top 15",
            "65b44b4 docs(ui): publicar restore point top 15 readiness",
            "origin/main = 65b44b4",
            "main ahead de origin/main por 4 commits",
            "README_DOCS_UI_CONSISTENCY_FIX_CHECKPOINT_1_169_PASSED_WITH_RESIDUAL_DOC_DEBT",
            "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLICATION_SELECTED",
            "PROMPT UI/UX 1.171 - Publicar restore point post fix consistencia README docs UI Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no User Panel",
            "no endpoints",
            "no JSON/fixtures",
            "no push",
            "UI/UX 1.x no cerrado globalmente",
        ]:
            assert marker in text


def test_static_artifacts_absent_and_no_mojibake_in_web_readme():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"
    text = read(WEB_README)
    for bad in [
        "Ã¡",
        "Ã©",
        "Ã­",
        "Ã³",
        "Ãº",
        "Ã±",
        "Â¿",
        "Â¡",
        "â€™",
        "â€œ",
        "â€�",
        "â€“",
    ]:
        assert bad not in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_RESTORE_POINT_DECISION_1_170.md",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_restore_point_decision_1_170.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
