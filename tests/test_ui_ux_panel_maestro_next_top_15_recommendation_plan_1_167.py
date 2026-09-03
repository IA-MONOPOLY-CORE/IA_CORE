from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_NEXT_TOP_15_RECOMMENDATION_PLAN_1_167.md"
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
        "UI/UX Panel Maestro Next TOP 15 Recommendation Plan 1.167",
        "65b44b4",
        "HEAD == origin/main",
        "up to date with origin/main",
        "working tree limpio",
        "restore point remoto vigente 65b44b4",
        "bloque TOP 15 + readiness publicado",
        "readiness matrix implementada documentation-test-only",
        "checkpoint readiness pasado",
        "UI/UX 1.x no cerrado globalmente",
        "Planificar siguiente recomendacion TOP 15",
        "sin implementarla",
    ]:
        assert marker in text


def test_published_block_is_confirmed():
    text = read(DOC)
    for marker in [
        "1.159 plan TOP 15",
        "1.160 auditoria TOP 15",
        "1.161 decision primera recomendacion",
        "1.162 plan readiness",
        "1.163 readiness documentation-test-only",
        "1.164 checkpoint readiness",
        "1.165 decision restore point",
        "1.166 publicacion restore point",
        "no UI activa",
        "no JS",
        "no backend",
        "no runtime",
        "no User Panel",
        "no endpoints",
        "no JSON/fixtures ledger/TOP15/readiness",
    ]:
        assert marker in text


def test_top_15_recommendations_are_classified():
    text = read(DOC)
    for marker in [
        "ui_ux_1x_closure_readiness_matrix",
        "global_closure_status_visible",
        "coronated_closure_criteria",
        "readme_docs_ui_consistency_audit",
        "ghost_affordances_audit",
        "operational_copy_audit",
        "safe_states_glossary",
        "honest_debt_map",
        "human_review_gate_layer",
        "panel_master_executive_summary",
        "present_blocked_future_map_humanized",
        "master_panel_vs_user_panel_separation",
        "future_visual_phase_readiness_without_runtime",
        "panel_information_hierarchy_review",
        "visible_technicality_reduction",
    ]:
        assert marker in text


def test_readiness_cross_and_candidate_comparison_are_present():
    text = read(DOC)
    for marker in [
        "ghost_affordances_review_needed",
        "operational_copy_review_needed",
        "human_review_gate_needed",
        "readme_docs_ui_consistency_needed",
        "closure_requires_operator_decision",
        "plus_domain_debt_visible",
        "lower_scripts_debt_visible",
        "cross_platform_future_debt_visible",
        "Comparacion de candidatas aplicables ahora",
        "impacto sobre readiness",
        "riesgo de tocar UI activa",
        "riesgo de sobreconstruccion",
        "seguridad no-runtime/no-execution",
        "utilidad para cierre coronado",
        "relacion con blockers/reviews pendientes",
        "facilidad de validacion documental/test-only",
        "orden logico",
        "ojo humano visual",
        "sin browser ni UI activa",
    ]:
        assert marker in text


def test_selection_modality_scope_and_contradictions_are_documented():
    text = read(DOC)
    for marker in [
        "readme_docs_ui_consistency_audit",
        "DOCUMENTATION_TEST_AND_UI_READ_ONLY_AUDIT",
        "README raiz",
        "ui/web/README.md",
        "ui/web/index.html",
        "ui/web/i18n_es.json",
        "JS como solo lectura",
        "docs 1.148 a 1.166",
        "contrato 1.151",
        "ledger 1.155",
        "readiness matrix 1.163",
        "publicacion restore point 1.166",
        "README dice algo que UI no refleja",
        "UI sugiere algo que README/docs niegan",
        "JSON/fixtures ausentes",
        "UI sugiere runtime/execution",
        "README dice cierre global",
        "User Panel futuro",
        "ledger dice blocked/future",
        "readiness dice NEEDS_REVIEW",
        "estado de restore point desactualizado",
        "origin/main/HEAD mal documentados",
    ]:
        assert marker in text


def test_future_out_of_scope_risks_mitigations_and_next_files_are_documented():
    text = read(DOC)
    for marker in [
        "no modificar UI activa",
        "no modificar JS",
        "no modificar backend",
        "no corregir copy",
        "no corregir affordances",
        "no crear glosario",
        "no crear resumen ejecutivo",
        "no cerrar UI/UX 1.x",
        "no crear JSON/fixtures",
        "no crear runtime",
        "no crear User Panel",
        "no publicar restore point",
        "no corregir pyflakes",
        "no limpiar deuda residual",
        "transformar auditoria en implementacion",
        "modificar UI al detectar contradicciones",
        "mezclar copy audit",
        "mezclar ghost affordances audit",
        "cerrar UI/UX 1.x prematuramente",
        "esconder deuda",
        "README como verdad",
        "UI como verdad",
        "tests demasiado fragiles",
        "abrir muchas lineas de trabajo",
        "auditoria documental/test-only",
        "UI/JS solo lectura",
        "no correccion en el mismo prompt",
        "findings con severity",
        "BLOCKER",
        "NEEDS_REVIEW",
        "DEFERRED",
        "PASSED",
        "mapear cada finding a fuente",
        "mapear cada finding a recomendacion TOP 15",
        "diff limitado",
        "docs/UI_UX_PANEL_MAESTRO_README_DOCS_UI_CONSISTENCY_AUDIT_1_168.md",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_audit_1_168.py",
        "README.md",
        "ui/web/README.md",
        "UI solo lectura",
        "JS solo lectura",
        "backend prohibido",
    ]:
        assert marker in text


def test_decision_next_and_negative_limits_are_present():
    text = read(DOC)
    for marker in [
        "NEXT_TOP_15_RECOMMENDATION_PLAN_READY_FOR_README_DOCS_UI_CONSISTENCY_AUDIT",
        "PROMPT UI/UX 1.168 - Auditar consistencia README docs UI Panel Maestro IA_CORE post readiness contract-aware sin runtime/no-execution",
        "no se implemento la siguiente recomendacion TOP 15",
        "no se ejecuto auditoria README/docs/UI",
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


def test_static_artifacts_absent_and_ui_contract_markers_read_only():
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


def test_readmes_have_1_167_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Planificacion 1.167 de siguiente recomendacion TOP 15",
            "HEAD base `65b44b4`",
            "restore point remoto vigente `65b44b4`",
            "branch up to date con origin/main al inicio",
            "bloque TOP 15 + readiness publicado",
            "siguiente recomendacion seleccionada: `readme_docs_ui_consistency_audit`",
            "modalidad: `DOCUMENTATION_TEST_AND_UI_READ_ONLY_AUDIT`",
            "no implementacion",
            "no auditoria ejecutada todavia",
            "no correcciones",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no JSON readiness",
            "no fixture readiness",
            "no push",
            "no restore point nuevo",
            "UI/UX 1.x no cerrado globalmente",
            "NEXT_TOP_15_RECOMMENDATION_PLAN_READY_FOR_README_DOCS_UI_CONSISTENCY_AUDIT",
            "PROMPT UI/UX 1.168 - Auditar consistencia README docs UI Panel Maestro IA_CORE post readiness contract-aware sin runtime/no-execution",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_NEXT_TOP_15_RECOMMENDATION_PLAN_1_167.md",
        "tests/test_ui_ux_panel_maestro_next_top_15_recommendation_plan_1_167.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
