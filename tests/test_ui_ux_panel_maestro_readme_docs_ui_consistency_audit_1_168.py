from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_AUDIT_1_168.md"
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


def test_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro README Docs UI Consistency Audit 1.168",
        "readme_docs_ui_consistency_audit_1_168",
        "readme_docs_ui_consistency_audit",
        "DOCUMENTATION_TEST_AND_UI_READ_ONLY_AUDIT",
        "base_head: `cdb4075`",
        "base_origin_main: `65b44b4`",
        "main ahead de origin/main por 1 commit",
        "working tree limpio",
        "restore_point_remoto_vigente: `65b44b4`",
        "NEXT_TOP_15_RECOMMENDATION_PLAN_READY_FOR_README_DOCS_UI_CONSISTENCY_AUDIT",
        "UI/UX 1.x no cerrado globalmente",
        "NO_RUNTIME",
        "NO_EXECUTION",
        "READ_ONLY_SOURCE",
        "NOT_TOUCHED",
    ]:
        assert marker in text


def test_all_required_sources_are_recorded_as_reread():
    text = read(DOC)
    for marker in [
        "1.167 releido",
        "Test 1.167 releido",
        "1.166 releido",
        "Test 1.166 releido",
        "1.165 releido",
        "Test 1.165 releido",
        "1.164 releido",
        "Test 1.164 releido",
        "1.163 releido",
        "Test 1.163 releido",
        "1.162 releido",
        "Test 1.162 releido",
        "1.161 releido",
        "Test 1.161 releido",
        "1.160 releido",
        "Test 1.160 releido",
        "1.159 releido",
        "Test 1.159 releido",
        "1.158 releido",
        "Test 1.158 releido",
        "1.157 releido",
        "Test 1.157 releido",
        "1.156 releido",
        "Test 1.156 releido",
        "1.155 releido",
        "Test 1.155 releido",
        "Test 1.154 transition-aware releido",
        "1.154 releido",
        "1.153 releido",
        "Test 1.153 releido",
        "1.152 releido",
        "Test 1.152 releido",
        "1.151 releido",
        "Test 1.151 releido",
        "1.150 releido",
        "Test 1.150 releido",
        "1.149 releido",
        "Test 1.149 releido",
        "1.148 releido",
        "Test 1.148 releido",
        "Matriz actual leida solo lectura",
        "Contrato 1.151 leido",
        "Ledger 1.155 leido",
        "Readiness matrix 1.163 leida",
        "Checkpoint readiness 1.164 leido",
        "Publicacion restore point 1.166 leida",
        "Plan 1.167 leido",
        "README raiz leido",
        "ui/web/README.md",
        "UI actual leida solo lectura",
        "i18n actual leido solo lectura",
        "JS actual leido/verificado solo lectura",
    ]:
        assert marker in text


def test_categories_contradictions_findings_and_mapping_are_present():
    text = read(DOC)
    for marker in [
        "Estado Git y restore point",
        "Secuencia README/cursor",
        "Consistencia entre README raiz y `ui/web/README.md`",
        "Consistencia entre README/docs y UI HTML",
        "Consistencia entre README/docs y i18n",
        "Consistencia entre README/docs y JS read-only",
        "Capacidades presentes/bloqueadas/futuras",
        "Readiness `PASSED`/`NEEDS_REVIEW`/`DEFERRED`",
        "No-runtime/no-execution/no-dispatch",
        "Ausencia de JSON/fixtures y consumo UI/backend",
        "README dice algo que UI no refleja",
        "UI sugiere algo que README/docs niegan",
        "JSON/fixtures ausentes",
        "UI sugiere runtime/execution",
        "README dice cierre global",
        "User Panel futuro presentado como existente",
        "Ledger dice blocked/future",
        "Readiness dice NEEDS_REVIEW",
        "Estado de restore point desactualizado",
        "origin/main/HEAD mal documentados",
        "Docs o README anuncian prompts posteriores",
    ]:
        assert marker in text
    for marker in [
        "README_CURSOR_ADVANCED_BEYOND_1_168_EXPECTED_STATE",
        "RESTORE_POINT_1_166_HASH_PLACEHOLDER_DRIFT",
        "WEB_README_ENCODING_MOJIBAKE_DRIFT",
        "LEGACY_JS_LOCAL_MECHANISMS_REQUIRE_CONTEXT",
        "UI_FSC_DEFER_NO_RUNTIME_ALIGNMENT_PASSED",
        "STATIC_CONTRACT_ARTIFACTS_ABSENT_PASSED",
        "top_15_mapping",
        "readiness_mapping",
        "requires_fix",
        "requires_operator_review",
        "correction_applied: no",
    ]:
        assert marker in text


def test_finding_classification_and_decision_are_consistent():
    text = read(DOC)
    for marker in [
        "blocker_findings: `0`",
        "needs_review_findings",
        "minor_doc_drift_findings",
        "deferred_findings",
        "passed_findings",
        "requires_fix: `true`",
        "requires_operator_review: `true`",
        "ready_for_checkpoint: `false`",
        "README_DOCS_UI_CONSISTENCY_AUDIT_NEEDS_FIX",
        "PROMPT UI/UX 1.168.A - Fix inconsistencias README docs UI Panel Maestro IA_CORE post readiness contract-aware sin runtime/no-execution",
    ]:
        assert marker in text


def test_static_artifacts_absent_and_ui_markers_read_only():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"

    index = read(INDEX)
    assert "Matriz de cierre UI/UX 1.x" in index or "Closure Matrix" in index
    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in index
    for forbidden in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "Processing request",
        "Capability active",
        "preview-and-run",
    ]:
        assert forbidden not in index


def test_readmes_record_audit_without_correcting_findings():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Auditoria 1.168 de consistencia README/docs/UI",
            "HEAD base `cdb4075`",
            "restore point remoto vigente `65b44b4`",
            "main ahead por 1 commit al inicio",
            "readme_docs_ui_consistency_audit",
            "DOCUMENTATION_TEST_AND_UI_READ_ONLY_AUDIT",
            "README_DOCS_UI_CONSISTENCY_AUDIT_NEEDS_FIX",
            "PROMPT UI/UX 1.168.A - Fix inconsistencias README docs UI Panel Maestro IA_CORE post readiness contract-aware sin runtime/no-execution",
            "no se corrigieron inconsistencias",
            "UI/JS solo lectura",
            "no UI activa modificada",
            "no JS modificado",
            "no backend",
            "no runtime",
            "no execution",
            "no JSON readiness",
            "no fixture readiness",
            "no push",
            "no restore point nuevo",
            "UI/UX 1.x no cerrado globalmente",
        ]:
            assert marker in text


def test_negative_limits_are_preserved_in_document():
    text = read(DOC)
    for marker in [
        "no se corrigieron inconsistencias",
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
        "no se modifico contrato funcional",
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


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_AUDIT_1_168.md",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_audit_1_168.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
