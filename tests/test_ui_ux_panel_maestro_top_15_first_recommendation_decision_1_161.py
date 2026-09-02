from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_15_FIRST_RECOMMENDATION_DECISION_1_161.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


FORBIDDEN_STATIC_ARTIFACTS = [
    ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json",
    ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json",
    ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json",
    ROOT / "tests" / "fixtures" / "ui_top_15_elite_audit_v1.json",
    ROOT / "ui" / "web" / "contracts" / "readiness_matrix.v1.json",
    ROOT / "tests" / "fixtures" / "ui_readiness_matrix_v1.json",
]


APPLICABLE_OPTIONS = [
    "global_closure_status_visible",
    "coronated_closure_criteria",
    "readme_docs_ui_consistency_audit",
    "ghost_affordances_audit",
    "operational_copy_audit",
    "safe_states_glossary",
    "honest_debt_map",
    "human_review_gate_layer",
    "panel_master_executive_summary",
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
        "UI/UX Panel Maestro TOP 15 First Recommendation Decision 1.161",
        "391dd00",
        "07a15d8",
        "main",
        "ahead",
        "2 commits",
        "working tree limpio",
        "plan TOP 15 1.159 cerrado localmente",
        "Auditoria TOP 15 1.160 cerrada localmente",
        "Implementacion TOP 15 no iniciada",
        "Decision primera recomendacion ejecutada en este prompt",
        "UI/UX 1.x no cerrado globalmente",
        "Decidir primera recomendacion TOP 15 a planificar",
        "sin implementar",
    ]:
        assert marker in text


def test_document_confirms_1_160_audit_counts_and_decision():
    text = read(DOC)
    for marker in [
        "15 recomendaciones auditadas",
        "9 aplicables ahora",
        "3 futuras/diferidas",
        "1 ya cubierta",
        "1 bloqueada",
        "0 descartadas",
        "1 requiere decision del operador",
        "ui_ux_1x_closure_readiness_matrix",
        "TOP_15_ELITE_AUDIT_COMPLETED_READY_FOR_OPERATOR_DECISION",
    ]:
        assert marker in text


def test_document_compares_applicable_options_with_required_criteria():
    text = read(DOC)
    assert "Comparacion de opciones aplicables ahora" in text
    for option in APPLICABLE_OPTIONS:
        assert option in text
    for marker in [
        "valor estructural",
        "seguridad",
        "alineacion con ledger",
        "alineacion con contrato 1.151",
        "alineacion con matriz/FSC/DEFER",
        "menor riesgo de sobreconstruccion",
        "menor riesgo de affordance fantasma",
        "bajo costo",
        "utilidad para cierre coronado",
        "orden logico",
    ]:
        assert marker in text


def test_document_evaluates_winning_recommendation_boundaries():
    text = read(DOC)
    for marker in [
        "Evaluacion de ui_ux_1x_closure_readiness_matrix",
        "Aporte",
        "Motivo para ser primera",
        "Que no debe hacer",
        "Riesgos",
        "Restricciones",
        "Por que no se implementa en 1.161",
        "docs-only",
        "tests-only",
        "static UI-only",
        "requiere backend",
        "requiere runtime",
        "requiere User Panel",
        "requiere JS",
        "Relacion con ledger",
        "Relacion con contrato 1.151",
        "Relacion con matriz/FSC/DEFER",
        "Utilidad para cierre coronado",
    ]:
        assert marker in text


def test_non_winning_future_covered_and_careful_options_are_documented():
    text = read(DOC)
    for marker in [
        "Evaluacion alternativas no ganadoras",
        "Futuras/diferidas no elegidas",
        "present_blocked_future_map_humanized",
        "master_panel_vs_user_panel_separation",
        "future_visual_phase_readiness_without_runtime",
        "Ya cubierta no elegida",
        "panel_information_hierarchy_review",
        "Bloqueada/cuidadosa no elegida",
        "visible_technicality_reduction",
    ]:
        assert marker in text


def test_checkpoint_restore_decision_final_next_and_limits_are_documented():
    text = read(DOC)
    for marker in [
        "Checkpoint/restore antes de planificar",
        "NO_RESTORE_REQUIRED_BEFORE_PLANNING",
        "Solo hay 2 commits locales desde 07a15d8",
        "documentales/test-only",
        "sin UI/JS/backend/runtime",
        "avanzarse a planificacion",
        "TOP_15_FIRST_RECOMMENDATION_SELECTED_READINESS_MATRIX",
        "PROMPT UI/UX 1.162 - Planificar implementacion matriz readiness cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no se implemento ui_ux_1x_closure_readiness_matrix",
        "no se creo matriz readiness",
        "no se implemento ninguna recomendacion TOP 15",
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
        "no se creo JSON ledger",
        "no se creo fixture ledger",
        "no se creo JSON TOP 15",
        "no se creo fixture TOP 15",
        "no se creo JSON readiness",
        "no se creo fixture readiness",
        "no se creo TOP 15 consumido por UI/backend",
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
        "no se publico restore point",
        "no se cerro UI/UX 1.x globalmente",
    ]:
        assert marker in text


def test_static_artifacts_absent_including_readiness_json_and_fixture():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"
    assert not list((ROOT / "ui" / "web" / "contracts").glob("*readiness*.json"))
    assert not list((ROOT / "tests" / "fixtures").glob("*readiness*.json"))


def test_existing_ui_contract_markers_remain_read_only():
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


def test_readmes_have_1_161_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Decision 1.161 primera recomendacion TOP 15",
            "391dd00",
            "07a15d8",
            "main ahead por 2 commits al inicio",
            "plan TOP 15 1.159 cerrado",
            "auditoria TOP 15 1.160 cerrada",
            "ui_ux_1x_closure_readiness_matrix",
            "no implementacion",
            "no matriz readiness creada",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no JSON readiness",
            "no fixture readiness",
            "no push",
            "no restore point",
            "UI/UX 1.x no cerrado globalmente",
            "TOP_15_FIRST_RECOMMENDATION_SELECTED_READINESS_MATRIX",
            "PROMPT UI/UX 1.162 - Planificar implementacion matriz readiness cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_TOP_15_FIRST_RECOMMENDATION_DECISION_1_161.md",
        "tests/test_ui_ux_panel_maestro_top_15_first_recommendation_decision_1_161.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
