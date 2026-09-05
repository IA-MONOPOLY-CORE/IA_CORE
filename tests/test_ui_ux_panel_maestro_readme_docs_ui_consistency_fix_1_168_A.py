from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_FIX_1_168_A.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


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
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
    "core",
    "domains",
    "providers",
    "tools",
    "scripts",
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


def test_fix_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro README Docs UI Consistency Fix 1.168.A",
        "f15dc23",
        "65b44b4",
        "main",
        "ahead",
        "2 commits",
        "working tree inicial limpio",
        "restore point remoto vigente: `65b44b4`",
        "restore point remoto vigente `65b44b4`",
        "README_DOCS_UI_CONSISTENCY_AUDIT_NEEDS_FIX",
        "PROMPT UI/UX 1.168.A",
        "UI/UX 1.x no cerrado globalmente",
        "restore point nuevo no publicado",
    ]:
        assert marker in text


def test_fix_document_records_findings_treatments_and_decision():
    text = read(DOC)
    for marker in [
        "README_CURSOR_ADVANCED_BEYOND_1_168_EXPECTED_STATE",
        "RESTORE_POINT_1_166_HASH_PLACEHOLDER_DRIFT",
        "WEB_README_ENCODING_MOJIBAKE_DRIFT",
        "LEGACY_JS_LOCAL_MECHANISMS_REQUIRE_CONTEXT",
        "FIXED",
        "ENCAPSULATED_AS_DEBT",
        "NOT_MODIFIED_BY_DESIGN",
        "README_DOCS_UI_CONSISTENCY_FIX_1_168_A_PASSED_WITH_RESIDUAL_DOC_DEBT",
        "PROMPT UI/UX 1.169 - Checkpoint fix consistencia README docs UI Panel Maestro IA_CORE post readiness contract-aware sin runtime/no-execution",
    ]:
        assert marker in text


def test_root_readme_has_correct_current_cursor_and_limits():
    text = read(README)
    for marker in [
        "Cursor vigente 1.168.A fix consistencia README/docs/UI",
        "65b44b4 docs(ui): publicar restore point top 15 readiness",
        "cdb4075 docs(ui): planificar siguiente recomendacion top 15",
        "f15dc23 docs(ui): auditar consistencia readme docs ui",
        "PROMPT UI/UX 1.168.A",
        "origin/main = 65b44b4",
        "main` ahead de `origin/main` por 2 commits",
        "README_DOCS_UI_CONSISTENCY_AUDIT_NEEDS_FIX",
        "UI/UX 1.x no cerrado globalmente",
        "no UI activa",
        "no JS funcional",
        "no backend",
        "no runtime",
        "no execution",
        "no User Panel",
        "no endpoints",
        "no JSON/fixtures",
        "no push",
    ]:
        assert marker in text


def test_future_readme_references_are_framed_as_non_current():
    for text in [read(README), read(WEB_README)]:
        assert "no cursor vigente/no estado actual" in text
        assert "registro historico/no vigente" in text or "Registro historico no vigente/no estado actual" in text
        for marker in ["1.78", "1.79", "1.80", "1.81", "1.83"]:
            assert marker in text
        for forbidden_current in [
            "## Plan siguiente bloque UI/UX 1.79",
            "## Auditoria readiness implementacion Final Screen Contracts 1.80",
            "## Plan implementacion futura Final Screen Contracts 1.81",
            "## Guardrails pre-implementacion Contract Overview 1.83",
        ]:
            assert forbidden_current not in text


def test_web_readme_has_contract_ui_context_and_legacy_js_frame():
    text = read(WEB_README)
    for marker in [
        "65b44b4",
        "cdb4075",
        "f15dc23",
        "PROMPT UI/UX 1.168.A",
        "DEFER_FINALIZATION",
        'data-contract-screen-count="4"',
        "FSC",
        "no-runtime",
        "no-execution",
        "no se modifico JS",
        "legacy",
        "localStorage",
        "window.location",
        "listeners",
        "fetches",
        "deuda",
        "contexto",
        "no equivale a runtime activo",
        "No existen JSON/fixtures",
        "UI/UX 1.x no cerrado globalmente",
    ]:
        assert marker in text


def test_web_readme_mojibake_was_corrected():
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
        "Ãƒ",
    ]:
        assert bad not in text


def test_negative_limits_are_preserved_in_fix_document():
    text = read(DOC)
    for marker in [
        "no se modifico UI activa",
        "no se modifico index.html",
        "no se modifico styles.css",
        "no se modifico i18n_es.json",
        "no se modifico JS",
        "no se agregaron listeners",
        "no se agregaron fetches",
        "no se agrego localStorage",
        "no se agregaron rutas/hash",
        "no se creo User Panel",
        "no se crearon endpoints",
        "no se toco backend",
        "no se toco runtime",
        "no se creo execution",
        "no se creo dispatch",
        "no se creo tool/model/integration invocation",
        "no se creo memory write",
        "no se creo context injection",
        "no se creo delivery",
        "no se creo JSON readiness",
        "no se creo fixture readiness",
        "no se creo readiness consumida por UI/backend",
        "no se creo JSON ledger",
        "no se creo fixture ledger",
        "no se creo JSON TOP 15",
        "no se creo fixture TOP 15",
        "no se creo helper operativo",
        "no se creo enforcement activo",
        "no se modifico contrato funcional activo",
        "no se creo contrato final operativo",
        "no se contradijo DEFER_FINALIZATION",
        "no se renombro +",
        "no se renombro DOMAIN",
        "no se modificaron scripts inferiores",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se publico restore point nuevo",
        "no se cerro UI/UX 1.x globalmente",
    ]:
        assert marker in text


def test_static_artifacts_absent_and_ui_markers_preserved():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"

    index = read(INDEX)
    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in index


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_FIX_1_168_A.md",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_fix_1_168_A.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
