from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_CHECKPOINT_1_156.md"
LEDGER = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md"
LEDGER_TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_capabilities_ledger_1_155.py"
PLAN_TEST_154 = ROOT / "tests" / "test_ui_ux_panel_maestro_capabilities_ledger_implementation_plan_1_154.py"
CONTRACT_151 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


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


def assert_markers(text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    assert not missing


def test_checkpoint_document_records_state_transition_and_sections():
    assert DOC.exists()
    text = read(DOC)

    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Capabilities Ledger Checkpoint 1.156",
            "059b163",
            "f455ca1",
            "main",
            "ahead",
            "7 commits",
            "Working tree limpio",
            "Matriz de cierre publicada",
            "Vocabulario/affordances checkpointed",
            "Ledger implementado documental + test-only",
            "Test 1.154 transition-aware",
            "Push no ejecutado",
            "Restore point no publicado",
            "Checkpoint del ledger 1.155",
            "sin implementacion nueva",
            "micro-fix aplicado",
            "commit `059b163`",
            "CAPABILITIES_LEDGER_IMPLEMENTED_TEST_ONLY",
            "metadata",
            "purpose",
            "scope",
            "out of scope",
            "classification rules",
            "allowed statuses",
            "forbidden statuses",
            "minimum fields",
            "allowed field values",
            "table/register format",
            "evidence requirements",
            "present capabilities",
            "blocked capabilities",
            "future/deferred capabilities",
            "semantic debts",
            "relation with matrix",
            "relation with FSC",
            "relation with DEFER",
            "relation with vocabulary/affordances contract",
            "relation with allowed/forbidden/blocked",
            "non-runtime statement",
            "human review gates",
            "restore point gates",
            "TOP 15 future relation",
            "decision",
            "next prompt",
            "limits preserved",
        ],
    )


def test_checkpoint_confirms_minimum_inventory():
    text = read(DOC)
    inventory = [
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
    ]
    assert_markers(text, inventory)


def test_checkpoint_confirms_material_limits_and_transition_aware_test():
    text = read(DOC)

    assert_markers(
        text,
        [
            "ui/web/contracts/capabilities_ledger.v1.json",
            "no existe",
            "tests/fixtures/ui_capabilities_ledger_v1.json",
            "json_ledger: NOT_CREATED",
            "ui_consumption: NOT_CONSUMED_BY_UI",
            "backend_consumption: NOT_CONSUMED_BY_BACKEND",
            "enforcement: TEST_ONLY",
            "No import JS",
            "No fetch",
            "No endpoint",
            "No runtime validator",
            "No backend validator",
            "No helper operativo",
            "No enforcement activo",
            "Test 1.154 conserva validacion pre-1.155",
            "Test 1.154 valida post-1.155",
            "No borra cobertura historica",
            "Resuelve conflicto de fase",
            "UI solo lectura",
            "JS solo lectura",
            "Backend no tocado",
            "Scripts inferiores no modificados",
            "+ no renombrado",
            "DOMAIN no renombrado",
        ],
    )

    transition_test = read(PLAN_TEST_154)
    assert "transition" in transition_test
    assert "TEST_ONLY_LEDGER" in transition_test
    assert "DOCUMENTATION_ONLY" in transition_test
    assert "NO_RUNTIME" in transition_test
    assert "NO_EXECUTION" in transition_test
    assert "NOT_CONSUMED_BY_UI" in transition_test
    assert "NOT_CONSUMED_BY_BACKEND" in transition_test
    assert "NOT_CREATED" in transition_test


def test_checkpoint_confirms_fsc_defer_sequence_risks_mitigations_decision_and_limits():
    text = read(DOC)

    assert_markers(
        text,
        [
            "FSC-CO-01",
            "FSC-BF-02",
            "FSC-VR-03",
            "FSC-RCP-04",
            'data-contract-screen-count="4"',
            "No quinta FSC",
            "DEFER_FINALIZATION",
            "Matriz de cierre UI/UX 1.x",
            "Matriz read-only",
            "Matriz no wizard",
            "Matriz no operativa",
            "Matriz: cerrada y publicada",
            "Vocabulario/affordances: implementado y checkpointed",
            "Ledger: implementado y checkpointed",
            "TOP 15: futuro",
            "Cierre global UI/UX 1.x: futuro",
            "Restore point posterior al ledger todavia no publicado",
            "TOP 15 todavia no auditado",
            "UI/UX 1.x todavia no cerrado globalmente",
            "Ledger todavia no visible en UI",
            "Ledger todavia no consumido por UI",
            "+ / DOMAIN siguen como deuda semantica",
            "Scripts inferiores heredados siguen como deuda menor/futura",
            "Tecnicismo documental alto sigue pendiente",
            "No hay JSON ledger, por decision actual",
            "Cualquier activacion futura requiere contrato, tests, revision humana y restore point",
            "Ledger documental + test-only",
            "Test 1.155",
            "Test 1.154 transition-aware",
            "No JSON ledger",
            "No UI consumption",
            "No backend consumption",
            "No runtime",
            "No execution",
            "FSC preservadas",
            "DEFER_FINALIZATION` preservado",
            "Matriz preservada",
            "Contrato 1.151 respetado",
            "Restore point decision futura",
            "TOP 15 diferido",
            "CAPABILITIES_LEDGER_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
            "PROMPT UI/UX 1.157 - Decidir publicación restore point ledger capacidades UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "no se implemento ledger nuevo",
            "no se rehizo ledger 1.155",
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


def test_ledger_155_contract_and_static_absence_are_preserved():
    assert LEDGER.exists()
    assert LEDGER_TEST.exists()
    ledger = read(LEDGER)

    assert_markers(
        ledger,
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
            "CAPABILITIES_LEDGER_IMPLEMENTED_TEST_ONLY",
        ],
    )

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


def test_ui_markers_readonly_and_forbidden_visible_copy_absent():
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


def test_readme_cursors_record_checkpoint_156():
    for path in [README, UI_README]:
        text = read(path)
        assert_markers(
            text,
            [
                "Checkpoint 1.156 del ledger de capacidades",
                "HEAD base `059b163`",
                "restore point remoto vigente `f455ca1`",
                "main ahead por 7 commits al inicio",
                "matriz de cierre publicada",
                "contrato de vocabulario/affordances checkpointed",
                "ledger implementado documental + test-only",
                "test 1.154 transition-aware",
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
                "TOP 15 recomendaciones elite diferido",
                "CAPABILITIES_LEDGER_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
                "PROMPT UI/UX 1.157 - Decidir publicación restore point ledger capacidades UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            ],
        )


def test_protected_runtime_surfaces_were_not_modified_since_head():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout.strip() == ""

