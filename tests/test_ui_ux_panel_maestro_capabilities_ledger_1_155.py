from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md"
PLAN_154 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_IMPLEMENTATION_PLAN_1_154.md"
PLAN_153 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_PLAN_1_153.md"
CONTRACT_151 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "ui/web/contracts/capabilities_ledger.v1.json",
    "tests/fixtures/ui_capabilities_ledger_v1.json",
    "api.py",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_markers(text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    assert not missing


def test_document_exists_with_metadata_purpose_scope_and_out_of_scope():
    assert DOC.exists()
    text = read(DOC)

    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Capabilities Ledger 1.155",
            "ledger_id: ui_ux_panel_maestro_capabilities_ledger",
            "ledger_version: 1.155",
            "source_plan: 1.153",
            "implementation_plan: 1.154",
            "base_head: 845896c",
            "remote_restore_point: f455ca1",
            "mode: DOCUMENTATION_ONLY",
            "status: TEST_ONLY_LEDGER",
            "runtime: NO_RUNTIME",
            "execution: NO_EXECUTION",
            "ui_consumption: NOT_CONSUMED_BY_UI",
            "backend_consumption: NOT_CONSUMED_BY_BACKEND",
            "json_ledger: NOT_CREATED",
            "enforcement: TEST_ONLY",
            "inventaria capacidades visibles o mencionadas",
            "clasifica capacidades presentes",
            "clasifica capacidades bloqueadas",
            "clasifica capacidades futuras",
            "registra deudas semanticas",
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "evita que una capacidad futura parezca presente",
            "evita que una capacidad documental parezca operativa",
            "evita que una capacidad bloqueada parezca utilizable",
            "protege no-runtime/no-execution",
            "prepara cierre UI/UX 1.x",
            "prepara auditoria TOP 15 posterior",
            "Panel Maestro UI/UX 1.x",
            "UI visible",
            "matriz de cierre",
            "FSC",
            "contrato de vocabulario/affordances 1.151",
            "READMEs seleccionados",
            "docs UI/UX recientes",
            "tests UI/UX recientes",
            "payloads backend ya existentes como fuente declarativa",
            "ejecucion de capacidades",
            "activacion de capacidades",
            "runtime",
            "dispatcher",
            "scheduler",
            "worker",
            "queue",
            "model invocation",
            "tool invocation",
            "integrations",
            "memory writes",
            "context injection",
            "delivery",
            "User Panel",
            "public endpoints",
            "fetches",
            "backend changes",
            "JS changes",
            "UI active changes",
            "visual activation",
            "global UI/UX 1.x closure",
            "TOP 15 recommendations audit",
            "restore point publication",
        ],
    )


def test_classification_statuses_fields_values_table_and_evidence():
    text = read(DOC)

    assert_markers(
        text,
        [
            "una capacidad presente requiere evidencia concreta",
            "una capacidad bloqueada requiere razon contractual",
            "una capacidad futura requiere `next_allowed_step`",
            "ninguna capacidad puede quedar sin categoria",
            "ninguna capacidad puede usar estado prohibido como estado actual",
            "Backend declarativo no equivale a runtime",
            "Read-only no equivale a operativo",
            "Test-only no equivale a capacidad activa",
            "Documentacion no equivale a ejecucion",
            "Preparacion no equivale a disponibilidad",
            "PRESENT_DOCUMENTED",
            "PRESENT_READ_ONLY",
            "PRESENT_TEST_ONLY",
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
            "nunca como estado real de capacidad",
            "capability_id",
            "display_name",
            "category",
            "status",
            "summary",
            "evidence_type",
            "evidence_path",
            "ui_surface",
            "backend_reference",
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
            "BLOCKED",
            "FUTURE_DEFERRED",
            "SEMANTIC_DEBT",
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
            "capability_id | category | status | evidence_path | ui_surface | runtime_status | execution_status | allowed_actions | forbidden_actions | blocked_capabilities | next_allowed_step",
            "DOC",
            "TEST",
            "UI_STATIC",
            "README",
            "BACKEND_DECLARATIVE",
            "HUMAN_REVIEW",
            "COMMIT",
            "RESTORE_POINT",
            "NOT_IMPLEMENTED",
            "FUTURE_PLAN",
            "toda capacidad presente debe tener evidence_path",
            "toda capacidad bloqueada debe tener razon contractual",
            "toda capacidad futura debe tener next_allowed_step",
            "toda deuda debe tener ubicacion o descripcion minima",
        ],
    )


def test_required_inventory_is_present():
    text = read(DOC)

    present = [
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
    ]
    blocked = [
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
    ]
    future = [
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
    ]
    debts = [
        "plus_domain_semantic_duplication",
        "domain_label_ambiguity",
        "lower_scripts_legacy_affordances",
        "high_documentary_technicality",
    ]

    for marker in present + blocked + future + debts:
        assert marker in text

    assert "category: BLOCKED" in text
    assert "blocked_capabilities` explicito" in text
    assert "forbidden_actions` explicito" in text
    assert "FUTURE_DEFERRED" in text
    assert "category: SEMANTIC_DEBT" in text
    assert "no se resuelve en 1.155" in text


def test_relations_non_runtime_gates_decision_and_limits():
    text = read(DOC)

    assert_markers(
        text,
        [
            "ledger complementa matriz de cierre",
            "ledger no reemplaza matriz",
            "ledger no convierte matriz en runtime",
            "matriz sigue read-only",
            "matriz sigue no operativa",
            "FSC-CO-01",
            "FSC-BF-02",
            "FSC-VR-03",
            "FSC-RCP-04",
            'data-contract-screen-count="4"',
            "No quinta FSC",
            "Ledger no crea nueva pantalla final",
            "Ledger no crea wizard",
            "DEFER_FINALIZATION",
            "Ledger no declara cierre global UI/UX 1.x",
            "Ledger no declara finalizacion total",
            "Ledger respeta vocabulario permitido/prohibido",
            "ledger usa estados seguros",
            "ledger evita estados prohibidos como estado actual",
            "ledger evita affordances fantasma",
            "ledger evita copy operativo falso",
            "runtime/execution como bloqueado/futuro, nunca presente",
            "Ledger refleja acciones permitidas como lectura/auditoria/documentacion",
            "Ledger refleja acciones prohibidas como ejecucion/dispatch/submit/send",
            "Ledger refleja capacidades bloqueadas explicitamente",
            "Ledger no inventa acciones permitidas",
            "ledger no oculta acciones prohibidas",
            "ledger no convierte blocked capabilities en UI activa",
            "Ledger no ejecuta",
            "Ledger no activa",
            "Ledger no despacha",
            "Ledger no invoca modelos",
            "Ledger no invoca tools",
            "Ledger no integra",
            "Ledger no escribe memoria",
            "Ledger no inyecta contexto",
            "Ledger no entrega outputs",
            "Ledger no crea endpoint",
            "Ledger no cambia estado",
            "Si el ledger se vuelve visible en UI futura, requiere revision humana",
            "Si una capacidad se vuelve operativa futura, requiere backend/contrato/tests/restore point",
            "No se publica restore point en este prompt",
            "Posible decision de restore point despues de checkpoint del ledger",
            "No push automatico",
            "TOP 15 queda diferido",
            "TOP 15 se audita despues de matriz + vocabulario + ledger",
            "aplican ahora",
            "futuras",
            "descartables",
            "cubiertas por contratos",
            "chocan con no-runtime/no-execution",
            "sobreconstruccion",
            "necesarias para cierre coronado",
            "TOP 15 no se implementa automaticamente",
            "CAPABILITIES_LEDGER_IMPLEMENTED_TEST_ONLY",
            "PROMPT UI/UX 1.156 - Checkpoint ledger de capacidades presentes bloqueadas futuras UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
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
        ],
    )


def test_static_ledger_files_do_not_exist_and_contract_plan_are_preserved():
    assert not (ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json").exists()
    assert not (ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json").exists()

    contract = read(CONTRACT_151)
    assert_markers(
        contract,
        [
            "UI/UX Panel Maestro Vocabulary Affordances Contract 1.151",
            "mode: DOCUMENTATION_ONLY",
            "status: TEST_ONLY_CONTRACT",
            "runtime: NO_RUNTIME",
            "execution: NO_EXECUTION",
            "ui_consumption: NOT_CONSUMED_BY_UI",
            "backend_consumption: NOT_CONSUMED_BY_BACKEND",
            "json_contract: NOT_CREATED",
            "enforcement: TEST_ONLY",
        ],
    )

    assert "CAPABILITIES_LEDGER_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION" in read(PLAN_154)
    assert "UI/UX Panel Maestro Capabilities Ledger Implementation Plan 1.154" in read(PLAN_154)
    assert "CAPABILITIES_LEDGER_PLAN_READY_FOR_IMPLEMENTATION_PLANNING" in read(PLAN_153)


def test_ui_markers_are_preserved_and_forbidden_visible_copy_absent():
    index = read(INDEX)
    for marker in [
        "Matriz de cierre UI/UX 1.x",
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


def test_readmes_record_155_cursor():
    for path in [README, UI_README]:
        text = read(path)
        assert_markers(
            text,
            [
                "Implementacion 1.155 del ledger",
                "HEAD base `845896c`",
                "restore point remoto vigente `f455ca1`",
                "main ahead por 6 commits al inicio",
                "matriz de cierre publicada",
                "contrato de vocabulario/affordances checkpointed",
                "ledger planificado en 1.153",
                "implementacion ledger planificada en 1.154",
                "ledger implementado como documental + test-only en 1.155",
                "docs/UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md",
                "tests/test_ui_ux_panel_maestro_capabilities_ledger_1_155.py",
                "no JSON ledger",
                "no fixture ledger",
                "no ledger consumido por UI",
                "no helper operativo",
                "no enforcement activo",
                "no UI activa",
                "no JS",
                "no backend",
                "no runtime",
                "no push",
                "no restore point",
                "TOP 15 recomendaciones elite diferido hasta despues de checkpoint del ledger",
                "PROMPT UI/UX 1.156 - Checkpoint ledger de capacidades presentes bloqueadas futuras UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            ],
        )


def test_protected_runtime_surfaces_were_not_modified_since_base_head():
    result = subprocess.run(
        ["git", "diff", "--name-only", "845896c", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout.strip() == ""

