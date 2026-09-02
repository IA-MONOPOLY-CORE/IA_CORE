from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_IMPLEMENTATION_PLAN_1_162.md"
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


GROUPS = [
    "FOUNDATION_RESTORE_AND_GIT",
    "UI_VISUAL_STRUCTURE",
    "FSC_AND_DEFER_BOUNDARY",
    "VOCABULARY_AFFORDANCES_CONTRACT",
    "CAPABILITIES_LEDGER_ALIGNMENT",
    "TOP_15_AUDIT_ALIGNMENT",
    "NO_RUNTIME_NO_EXECUTION_BOUNDARY",
    "NO_GHOST_AFFORDANCES",
    "COPY_AND_STATE_TRUTHFULNESS",
    "HUMAN_REVIEW_AND_OPERATOR_GUIDANCE",
    "DOCUMENTATION_AND_CURSOR_CONSISTENCY",
    "BACKEND_CONTRACT_SAFETY",
    "FUTURE_PANEL_AND_RUNTIME_SEPARATION",
    "DEBT_VISIBILITY",
    "CLOSURE_DECISION_GATES",
]


FIELDS = [
    "condition_id",
    "group",
    "title",
    "description",
    "status",
    "required_for_1x_closure",
    "current_evidence",
    "source_documents",
    "source_tests",
    "ui_surface",
    "requires_ui_change",
    "requires_js_change",
    "requires_backend_change",
    "requires_runtime",
    "requires_user_panel",
    "blocked_by",
    "deferred_reason",
    "operator_action",
    "next_prompt_hint",
    "risk_if_ignored",
    "notes",
]


CONDITIONS = [
    "restore_point_remote_current",
    "working_tree_clean",
    "git_ahead_behind_known",
    "master_shell_structure_preserved",
    "overview_panel_preserved",
    "closure_matrix_present",
    "fsc_count_preserved",
    "defer_finalization_present",
    "vocabulary_contract_present",
    "forbidden_operational_terms_blocked",
    "allowed_affordances_documented",
    "capabilities_ledger_present",
    "present_blocked_future_separation",
    "ledger_not_consumed_by_ui",
    "top_15_audit_present",
    "first_top_15_recommendation_selected",
    "runtime_execution_absent",
    "dispatch_absent",
    "model_tool_integration_invocation_absent",
    "ghost_affordances_review_needed",
    "operational_copy_review_needed",
    "human_review_gate_needed",
    "readme_docs_ui_consistency_needed",
    "backend_contract_tests_passing",
    "backup_readiness_tests_passing",
    "user_panel_not_created",
    "future_runtime_separated",
    "plus_domain_debt_visible",
    "lower_scripts_debt_visible",
    "cross_platform_future_debt_visible",
    "closure_requires_operator_decision",
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


def test_document_exists_and_records_base_state_and_objective():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro Closure Readiness Matrix Implementation Plan 1.162",
        "b2c7cc1",
        "07a15d8",
        "main",
        "ahead",
        "3 commits",
        "working tree limpio",
        "plan TOP 15 1.159 cerrado localmente",
        "Auditoria TOP 15 1.160 cerrada localmente",
        "Decision primera recomendacion 1.161 cerrada localmente",
        "ui_ux_1x_closure_readiness_matrix",
        "Implementacion readiness pendiente",
        "UI/UX 1.x no cerrado globalmente",
        "Planificar implementacion de la readiness matrix",
        "sin implementarla",
    ]:
        assert marker in text


def test_decision_1_161_purpose_and_non_goals_are_documented():
    text = read(DOC)
    for marker in [
        "TOP_15_FIRST_RECOMMENDATION_SELECTED_READINESS_MATRIX",
        "no se implemento en 1.161",
        "no se creo matriz readiness",
        "evaluar si UI/UX 1.x esta listo para cierre coronado",
        "PASSED",
        "NEEDS_REVIEW",
        "BLOCKED",
        "DEFERRED",
        "evitar cierre global prematuro",
        "evitar promesas falsas",
        "No declarar UI/UX 1.x cerrado automaticamente",
        "No crear una accion de cierre",
        "No crear boton",
        "No crear runtime",
        "No crear backend",
        "No crear User Panel",
        "No crear JSON consumido por UI",
        "No reemplazar matriz/FSC/DEFER",
        "No ocultar deuda",
        "DOCUMENTATION_ONLY_AND_TEST_ONLY",
        "criterio verificable",
        "sin UI activa",
        "sin affordances fantasma",
    ]:
        assert marker in text


def test_groups_fields_allowed_and_forbidden_states_are_present():
    text = read(DOC)
    for marker in GROUPS:
        assert marker in text
    for marker in FIELDS:
        assert marker in text
    for marker in [
        "PASSED",
        "NEEDS_REVIEW",
        "BLOCKED",
        "DEFERRED",
        "ACTIVE",
        "RUNNING",
        "LIVE",
        "OPERATIONAL",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "PROCESSING",
        "READY_TO_RUN",
        "CAPABILITY_ACTIVE",
        "DONE sin evidencia",
        "COMPLETE sin evidencia",
        "FINAL sin criterio",
    ]:
        assert marker in text


def test_minimum_conditions_and_closure_rules_are_present():
    text = read(DOC)
    for marker in CONDITIONS:
        assert marker in text
    for marker in [
        "no hay BLOCKED required_for_1x_closure",
        "NEEDS_REVIEW no bloquea automaticamente",
        "DEFERRED no bloquea",
        "PASSED requiere evidencia",
        "No se puede cerrar solo porque hay muchos PASSED",
        "affordance fantasma",
        "copy operativo ambiguo",
        "README/docs/UI se contradicen",
        "FSC/DEFER",
        "ledger/contrato",
        "UI sugiere runtime/execution",
        "backend/runtime/User Panel",
    ]:
        assert marker in text


def test_required_relationships_are_documented():
    text = read(DOC)
    for marker in [
        "Usar la matriz existente como fuente",
        "No reemplazarla",
        "No crear quinta FSC",
        'data-contract-screen-count=\"4\"',
        "DEFER_FINALIZATION",
        "contrato 1.151",
        "vocabulario permitido/prohibido",
        "estados seguros",
        "estados operativos prohibidos",
        "ledger 1.155",
        "separacion presente/bloqueado/futuro",
        "No convertir capacidades futuras en presentes",
        "No convertir bloqueadas en utilizables",
        "TOP 15",
        "1.160",
        "1.161",
        "No implementar el resto de recomendaciones",
        "No crear 15 prompts",
        "no debe tocar UI activa",
        "No debe tocar JS",
        "No debe tocar backend",
        "No debe crear JSON/fixture readiness",
    ]:
        assert marker in text


def test_risks_mitigations_and_future_validations_are_documented():
    text = read(DOC)
    for marker in [
        "Convertir matriz readiness en cierre automatico",
        "sensacion falsa de terminado",
        "Duplicar la matriz de cierre existente",
        "Sobreconstruir",
        "burocracia sin valor",
        "NEEDS_REVIEW en blocker eterno",
        "DEFERRED en ocultamiento de deuda",
        "estados prohibidos",
        "affordance de cierre",
        "Abrir UI/JS/backend antes de tiempo",
        "Panel Maestro con User Panel",
        "JSON prematuro",
        "runtime validator",
        "Documento/test-only primero",
        "Sin UI activa",
        "Sin JS",
        "Sin backend",
        "Sin JSON",
        "Sin fixture",
        "Sin helper operativo",
        "Sin enforcement activo",
        "Evidencia por condicion",
        "Operador humano como gate",
        "Checkpoint posterior",
        "Documento readiness existe",
        "Test readiness existe",
        "Contiene grupos obligatorios",
        "Contiene condiciones minimas",
        "Contiene campos obligatorios",
        "Contiene estados permitidos",
        "Contiene estados prohibidos",
        "No usa estados prohibidos como estado real",
        "Contiene reglas de cierre",
        "No crea JSON readiness",
        "No crea fixture readiness",
        "No toca UI activa",
        "No toca JS",
        "No toca backend",
        "No cierra UI/UX 1.x",
        "No crea runtime/execution/User Panel/endpoints",
    ]:
        assert marker in text


def test_next_prompt_allowed_files_decision_and_limits_are_documented():
    text = read(DOC)
    for marker in [
        "docs/UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_1_163.md",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_1_163.py",
        "README.md",
        "ui/web/README.md",
        "PROMPT UI/UX 1.163 - Implementar matriz readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
        "CLOSURE_READINESS_MATRIX_IMPLEMENTATION_PLAN_READY_FOR_DOCUMENTATION_TEST_IMPLEMENTATION",
        "no se implemento readiness matrix",
        "no se creo matriz readiness final",
        "no se creo JSON readiness",
        "no se creo fixture readiness",
        "no se creo readiness consumida por UI/backend",
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


def test_readmes_have_1_162_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Planificacion 1.162 de implementacion readiness matrix",
            "b2c7cc1",
            "07a15d8",
            "main ahead por 3 commits al inicio",
            "plan TOP 15 1.159 cerrado",
            "auditoria TOP 15 1.160 cerrada",
            "decision primera recomendacion 1.161 cerrada",
            "ui_ux_1x_closure_readiness_matrix",
            "DOCUMENTATION_ONLY_AND_TEST_ONLY",
            "readiness matrix no implementada todavia",
            "no JSON readiness",
            "no fixture readiness",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no push",
            "no restore point",
            "UI/UX 1.x no cerrado globalmente",
            "CLOSURE_READINESS_MATRIX_IMPLEMENTATION_PLAN_READY_FOR_DOCUMENTATION_TEST_IMPLEMENTATION",
            "PROMPT UI/UX 1.163 - Implementar matriz readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_IMPLEMENTATION_PLAN_1_162.md",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_implementation_plan_1_162.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
