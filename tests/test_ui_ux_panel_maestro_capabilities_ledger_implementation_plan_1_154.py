import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_IMPLEMENTATION_PLAN_1_154.md"
PLAN = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_PLAN_1_153.md"
CONTRACT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
FUTURE_LEDGER_DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md"
FUTURE_LEDGER_TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_capabilities_ledger_1_155.py"
FUTURE_LEDGER_JSON = ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json"
FUTURE_LEDGER_FIXTURE = ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json"
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


def test_document_exists_and_records_base_state_and_strategy():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Capabilities Ledger Implementation Plan 1.154",
        "f524194",
        "f455ca1",
        "main",
        "ahead",
        "5 commits",
        "working tree limpio",
        "matriz de cierre publicada",
        "vocabulario/affordances checkpointed",
        "ledger planificado en 1.153",
        "ledger todavia no implementado",
        "Planificar implementacion futura del ledger",
        "sin implementarlo",
        "CAPABILITIES_LEDGER_PLAN_READY_FOR_IMPLEMENTATION_PLANNING",
        "documental + test-only",
        "no JSON ledger por defecto",
        "no fixture JSON ledger por defecto",
        "JSON futuro solo con decision especifica",
        "tabla documental + test parsing simple",
    ]:
        assert marker in text


def test_document_defines_future_ledger_structure():
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Capabilities Ledger 1.155",
        "ledger_id: ui_ux_panel_maestro_capabilities_ledger",
        "ledger_version: 1.155",
        "source_plan: 1.153",
        "implementation_plan: 1.154",
        "base_head: <HEAD inicial de 1.155>",
        "remote_restore_point: f455ca1",
        "mode: DOCUMENTATION_ONLY",
        "status: TEST_ONLY_LEDGER",
        "runtime: NO_RUNTIME",
        "execution: NO_EXECUTION",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "json_ledger: NOT_CREATED",
        "enforcement: TEST_ONLY",
        "Purpose",
        "Scope",
        "Out of scope",
        "Classification rules",
        "Allowed statuses",
        "Forbidden statuses",
        "Minimum fields per capability",
        "Present documented capabilities",
        "Present read-only/test-only capabilities",
        "Blocked capabilities",
        "Future/deferred capabilities",
        "Semantic debts",
        "Capability records",
        "Relation with matrix",
        "Relation with FSC",
        "Relation with DEFER_FINALIZATION",
        "Relation with vocabulary/affordances contract 1.151",
        "Relation with allowed_actions/forbidden_actions/blocked_capabilities",
        "Evidence requirements",
        "Non-runtime statement",
        "Human review gates",
        "Restore point gates",
        "Future TOP 15 relation",
    ]:
        assert marker in text


def test_document_defines_minimum_inventory():
    text = read(DOC)

    for marker in [
        "master_shell_visual_structure",
        "panel_maestro_overview",
        "backend_contract_widgets_read_model",
        "final_screen_contracts_rehousing",
        "closure_matrix_ui_ux_1x",
        "vocabulary_affordances_contract",
        "capabilities_ledger_documental",
        "readme_cursor_state",
        "ui_ux_regression_tests",
        "backend_payload_contract_tests",
        "github_backup_readiness_tests",
        "human_visual_review_gate",
        "restore_point_publication_protocol",
        "no_runtime_no_execution_boundary",
        "defer_finalization_boundary",
        "runtime_execution",
        "agent_dispatch",
        "model_invocation",
        "tool_invocation",
        "integration_invocation",
        "scheduler_worker_queue",
        "state_mutation",
        "memory_writes",
        "context_injection",
        "output_delivery",
        "public_endpoints",
        "user_panel",
        "raw_package_exposure",
        "confirmation_gate_active",
        "business_composition_runtime",
        "market_catalog_runtime",
        "domain_runtime_operations",
        "ledger_visual_consumed_by_ui",
        "capabilities_contract_versioned_json",
        "user_panel_future",
        "controlled_execution_future",
        "runtime_orchestrator_future",
        "integrations_gateway_future",
        "model_routing_operational_future",
        "tools_runtime_future",
        "memory_context_engine_operational_future",
        "delivery_layer_future",
        "observability_economics_future",
        "multi_tenant_business_composition_ui_future",
        "top_15_elite_recommendations_audit_future",
        "global_ui_ux_1x_closure_future",
        "cross_platform_validation_future",
        "plus_domain_semantic_duplication",
        "domain_label_ambiguity",
        "lower_scripts_legacy_affordances",
        "high_documentary_technicality",
    ]:
        assert marker in text


def test_document_defines_fields_allowed_values_and_forbidden_statuses():
    text = read(DOC)

    for marker in [
        "capability_id",
        "display_name",
        "category",
        "status",
        "summary",
        "evidence_type",
        "evidence_path",
        "ui_surface",
        "backend_reference",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "runtime_status",
        "execution_status",
        "ui_consumption",
        "backend_consumption",
        "risk_level",
        "debt_level",
        "human_review_required",
        "restore_point_required_before_activation",
        "next_allowed_step",
        "notes",
        "PRESENT_DOCUMENTED",
        "PRESENT_READ_ONLY",
        "PRESENT_TEST_ONLY",
        "BLOCKED",
        "FUTURE_DEFERRED",
        "SEMANTIC_DEBT",
        "BLOCKED_BY_CONTRACT",
        "BLOCKED_NO_RUNTIME",
        "BLOCKED_NO_EXECUTION",
        "DEFERRED_FUTURE_PHASE",
        "DEFERRED_REQUIRES_BACKEND",
        "DEFERRED_REQUIRES_HUMAN_REVIEW",
        "DEFERRED_REQUIRES_RESTORE_POINT",
        "NOT_IMPLEMENTED",
        "NOT_APPLICABLE",
        "UNKNOWN_NEEDS_AUDIT",
        "NO_RUNTIME",
        "FUTURE_ONLY",
        "NO_EXECUTION",
        "NOT_CONSUMED_BY_UI",
        "VISIBLE_READ_ONLY",
        "DOCUMENTED_ONLY",
        "NOT_CONSUMED_BY_BACKEND",
        "DECLARATIVE_REFERENCE_ONLY",
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL_IF_ENABLED",
        "NONE",
        "MINOR",
        "FUTURE_PHASE_DEBT",
        "YES",
        "NO",
        "BEFORE_VISUAL_ACTIVATION",
        "BEFORE_RUNTIME_ACTIVATION",
        "BEFORE_RUNTIME",
        "BEFORE_PUBLICATION",
        "ACTIVE",
        "RUNNING",
        "LIVE",
        "OPERATIONAL",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "PROCESSING",
        "READY_TO_RUN",
        "ENABLED_FOR_EXECUTION",
        "AVAILABLE_FOR_RUNTIME",
        "CONNECTED_LIVE",
        "SYNCED_ACTIVE",
        "solo pueden aparecer",
        "seccion de estados prohibidos",
        "no como estado real de capacidad",
    ]:
        assert marker in text


def test_document_defines_table_evidence_and_runtime_boundaries():
    text = read(DOC)

    for marker in [
        "capability_id | category | status | evidence_path",
        "DOC",
        "TEST",
        "UI_STATIC",
        "README",
        "BACKEND_DECLARATIVE",
        "HUMAN_REVIEW",
        "COMMIT",
        "RESTORE_POINT",
        "FUTURE_PLAN",
        "toda capacidad presente debe tener evidence_path",
        "toda capacidad bloqueada debe tener razon contractual",
        "toda capacidad futura debe tener next_allowed_step",
        "ledger 1.155 no modifica UI visible",
        "ledger no se muestra todavia en pantalla",
        "ledger no crea widget",
        "ledger no crea card visual",
        "ledger no crea boton",
        "ledger no crea accion",
        "ledger no cambia layout",
        "JS queda solo lectura",
        "backend queda solo lectura",
        "ledger no se importa desde JS",
        "ledger no se fetch-ea",
        "ledger no se carga por endpoint",
        "contrato 1.151",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in text


def test_document_records_top_15_future_validations_acceptance_risks_and_mitigations():
    text = read(DOC)

    for marker in [
        "TOP 15",
        "aplican ahora",
        "futuras",
        "descartables",
        "cubiertas por contratos",
        "chocan con no-runtime/no-execution",
        "sobreconstruccion",
        "necesarias para cierre coronado",
        "Validaciones futuras para 1.155",
        "Criterios de aceptacion futura",
        "ledger demasiado grande",
        "ledger demasiado superficial",
        "capacidad presente sin evidencia",
        "capacidad bloqueada mal clasificada como futura",
        "capacidad futura mal clasificada como presente",
        "deuda semantica omitida",
        "JSON prematuro",
        "test fragil por tabla Markdown",
        "test demasiado laxo",
        "duplicacion con contrato 1.151",
        "duplicacion con matriz",
        "sensacion falsa de cierre global",
        "TOP 15 adelantado",
        "confundir backend declarativo con runtime",
        "confundir read-only con operativo",
        "sobrecargar README",
        "inventario minimo obligatorio",
        "categorias cerradas",
        "estados permitidos cerrados",
        "estados prohibidos explicitos",
        "evidence_path obligatorio para presentes",
        "blocked_capabilities obligatorio para bloqueadas",
        "next_allowed_step obligatorio para futuras",
        "deudas explicitas",
        "no JSON por defecto",
        "no UI consumption",
        "no backend consumption",
        "test-only",
        "no UI activa",
        "no JS",
        "no backend",
        "no runtime",
        "no cierre global",
        "TOP 15 diferido",
    ]:
        assert marker in text


def test_document_records_decision_next_prompt_and_limits():
    text = read(DOC)

    for marker in [
        "CAPABILITIES_LEDGER_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION",
        (
            "PROMPT UI/UX 1.155 - Implementar ledger de capacidades presentes bloqueadas futuras "
            "UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ),
        "no se implemento ledger",
        "no se creo documento ledger 1.155",
        "no se creo test ledger 1.155",
        "no se creo JSON ledger",
        "no se creo fixture ledger",
        "no se creo ledger consumido por UI",
        "no se creo helper operativo",
        "no se creo enforcement activo",
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
        "no se ejecuto TOP 15 recomendaciones elite",
        "no se cerro UI/UX 1.x globalmente",
    ]:
        assert marker in text


def test_contract_1_151_and_plan_1_153_remain_available():
    assert CONTRACT.exists()
    contract = read(CONTRACT)
    for marker in [
        "UI/UX Panel Maestro Vocabulary Affordances Contract 1.151",
        "mode: DOCUMENTATION_ONLY",
        "status: TEST_ONLY_CONTRACT",
        "runtime: NO_RUNTIME",
        "execution: NO_EXECUTION",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "json_contract: NOT_CREATED",
        "enforcement: TEST_ONLY",
    ]:
        assert marker in contract

    assert PLAN.exists()
    plan = read(PLAN)
    assert "UI/UX Panel Maestro Capabilities Ledger Plan 1.153" in plan
    assert "CAPABILITIES_LEDGER_PLAN_READY_FOR_IMPLEMENTATION_PLANNING" in plan


def test_current_ui_readonly_surface_preserves_expected_markers():
    text = read(INDEX)

    for marker in [
        "Matriz de cierre UI/UX 1.x",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in text

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
        assert forbidden not in text


def test_future_ledger_artifacts_are_transition_aware():
    assert not FUTURE_LEDGER_JSON.exists()
    assert not FUTURE_LEDGER_FIXTURE.exists()

    if not FUTURE_LEDGER_DOC.exists() and not FUTURE_LEDGER_TEST.exists():
        return

    assert FUTURE_LEDGER_DOC.exists()
    assert FUTURE_LEDGER_TEST.exists()

    ledger = read(FUTURE_LEDGER_DOC)
    for marker in [
        "mode: DOCUMENTATION_ONLY",
        "status: TEST_ONLY_LEDGER",
        "runtime: NO_RUNTIME",
        "execution: NO_EXECUTION",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "json_ledger: NOT_CREATED",
        "enforcement: TEST_ONLY",
    ]:
        assert marker in ledger


def test_readme_cursors_record_implementation_plan_1_154():
    for path in (README, WEB_README):
        text = read(path)
        assert "Planificacion de implementacion 1.154 del ledger" in text
        assert "HEAD base `f524194`" in text
        assert "restore point remoto vigente `f455ca1`" in text
        assert "main ahead por 5 commits al inicio" in text
        assert "matriz de cierre publicada" in text
        assert "contrato de vocabulario/affordances checkpointed" in text
        assert "ledger planificado en 1.153" in text
        assert "implementacion del ledger planificada en 1.154" in text
        assert "documental + test-only" in text
        assert "no JSON ledger por defecto" in text
        assert (
            "PROMPT UI/UX 1.155 - Implementar ledger de capacidades presentes bloqueadas futuras "
            "UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        assert "TOP 15 recomendaciones elite diferido" in text
        assert "no implementacion ledger" in text
        assert "no JSON ledger" in text
        assert "no ledger consumido por UI" in text
        assert "no UI activa" in text
        assert "no JS" in text
        assert "no backend" in text
        assert "no runtime" in text
        assert "no push" in text


def test_prompt_1_154_did_not_modify_protected_runtime_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "f524194", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
