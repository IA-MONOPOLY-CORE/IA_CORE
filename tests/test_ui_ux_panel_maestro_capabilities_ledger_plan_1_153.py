import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_PLAN_1_153.md"
CONTRACT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
FUTURE_LEDGER_DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_154.md"
FUTURE_LEDGER_TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_capabilities_ledger_1_154.py"
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


def test_plan_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Capabilities Ledger Plan 1.153",
        "5eb2ed0",
        "f455ca1",
        "main",
        "ahead",
        "4 commits",
        "working tree limpio",
        "matriz de cierre publicada",
        "vocabulario/affordances checkpointed",
        "ledger todavia no planificado ni implementado",
        "Planificar ledger de capacidades presentes/bloqueadas/futuras",
        "sin implementarlo",
        "bloque 1 matriz",
        "bloque 2 vocabulario/affordances",
        "bloque 3 ledger",
        "no cierre global UI/UX 1.x todavia",
        "TOP 15 diferido",
    ]:
        assert marker in text


def test_plan_defines_problem_purpose_scope_and_out_of_scope():
    text = read(DOC)

    for marker in [
        "Problema a resolver",
        "que la UI muestre capacidades sin estado contractual claro",
        "que una capacidad parezca disponible cuando esta bloqueada",
        "que una capacidad futura parezca presente",
        "que una capacidad presente no tenga evidencia",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "que se confunda documentacion con ejecucion",
        "que se confunda preparacion con disponibilidad",
        "que se confunda backend declarado con runtime activo",
        "que se confunda contrato test-only con capacidad operativa",
        "Proposito del ledger",
        "inventariar capacidades visibles o mencionadas",
        "clasificar capacidades presentes",
        "clasificar capacidades bloqueadas",
        "clasificar capacidades futuras",
        "relacionar cada capacidad con evidencia",
        "relacionar cada capacidad con contrato",
        "relacionar cada capacidad con UI visible",
        "relacionar cada capacidad con backend declarado",
        "proteger no-runtime/no-execution",
        "preparar cierre UI/UX 1.x",
        "preparar auditoria TOP 15 posterior",
        "Alcance",
        "Panel Maestro UI/UX 1.x",
        "UI visible",
        "matriz de cierre",
        "FSC",
        "contrato de vocabulario/affordances",
        "READMEs seleccionados",
        "docs UI/UX recientes",
        "tests UI/UX recientes",
        "capacidades declaradas",
        "capacidades bloqueadas",
        "capacidades futuras",
        "acciones permitidas",
        "acciones prohibidas",
        "evidencias documentales",
        "payloads backend ya existentes",
        "Fuera de alcance",
        "ejecutar capacidades",
        "activar capacidades",
        "crear runtime",
        "crear dispatcher",
        "crear scheduler",
        "crear worker",
        "crear queue",
        "invocar modelos",
        "invocar tools",
        "llamar integraciones",
        "escribir memoria",
        "inyectar contexto",
        "entregar outputs",
        "crear User Panel",
        "crear endpoints",
        "crear fetches",
        "modificar backend",
        "modificar JS",
        "modificar UI activa",
        "cerrar UI/UX 1.x",
        "resolver deudas `+` / `DOMAIN`",
        "ejecutar TOP 15 de recomendaciones elite",
    ]:
        assert marker in text


def test_plan_defines_categories_states_and_fields():
    text = read(DOC)

    for marker in [
        "presentes documentales",
        "presentes no operativas",
        "bloqueadas",
        "futuras",
        "deudas semanticas",
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
    ]:
        assert marker in text


def test_plan_defines_classification_criteria_and_contract_relations():
    text = read(DOC)

    for marker in [
        "Criterios para capacidades presentes",
        "existe evidencia concreta",
        "la evidencia esta en archivo/documento/test/UI",
        "el estado no implica ejecucion",
        "no contradice FSC",
        "no contradice `DEFER_FINALIZATION`",
        "no requiere runtime",
        "puede ser auditada sin ejecutar",
        "Criterios para capacidades bloqueadas",
        "requiere runtime",
        "requiere ejecucion",
        "requiere dispatch",
        "requiere scheduler/worker/queue",
        "requiere modelos",
        "requiere tools",
        "requiere integraciones",
        "requiere memoria operativa",
        "requiere context injection",
        "requiere delivery",
        "requiere endpoint publico",
        "requiere User Panel",
        "requiere state mutation",
        "no tiene backend declarado suficiente",
        "Criterios para capacidades futuras",
        "es deseable pero no necesaria para cierre actual",
        "requiere una fase posterior",
        "requiere backend futuro",
        "requiere restore point previo",
        "requiere revision humana",
        "pertenece a vision IA_CORE mas amplia",
        "reflejar acciones permitidas como lectura/auditoria/documentacion",
        "reflejar acciones prohibidas como ejecucion/dispatch/submit/send",
        "reflejar capacidades bloqueadas explicitamente",
        "no inventar acciones permitidas",
        "no ocultar acciones prohibidas",
        "no convertir blocked capabilities en UI activa",
        "usar el contrato 1.151 como limite semantico",
    ]:
        assert marker in text


def test_plan_preserves_matrix_fsc_defer_vocab_contract_and_debts():
    text = read(DOC)

    for marker in [
        "usar matriz de cierre como evidencia de estado global",
        "no reemplazar la matriz",
        "no convertir matriz en runtime",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "no agregar quinta FSC",
        "DEFER_FINALIZATION",
        "no declarar cierre global UI/UX 1.x",
        "no declarar finalization total",
        "no habilitar ejecucion",
        "contrato 1.151",
        "respetar allowlist/denylist de 1.151",
        "respetar terminos contextuales",
        "no usar estados prohibidos",
        "no usar affordances prohibidas",
        "no crear copy operativo falso",
        "no crear success falso",
        "no crear promesas no soportadas",
        "active/running/live/operational/executing/dispatching/submitted/processing",
        "lenguaje read-only/documental",
        "+",
        "DOMAIN",
        "scripts inferiores heredados",
        "tecnicismo documental alto",
        "+ no debe parecer accion operativa",
        "DOMAIN no debe parecer runtime/endpoint",
        "ninguna deuda debe resolverse en 1.153",
    ]:
        assert marker in text


def test_plan_defines_future_files_validations_acceptance_risks_and_mitigations():
    text = read(DOC)

    for marker in [
        "docs/UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_154.md",
        "tests/test_ui_ux_panel_maestro_capabilities_ledger_1_154.py",
        "ui/web/contracts/capabilities_ledger.v1.json",
        "tests/fixtures/ui_capabilities_ledger_v1.json",
        "no crear JSON en 1.154 salvo justificacion fuerte",
        "documental + test-only",
        "no consumo por UI",
        "no backend",
        "no runtime",
        "no enforcement activo",
        "Archivos prohibidos futuros 1.154",
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "api.py",
        "core/",
        "providers/",
        "tools/",
        "scripts/",
        "Validaciones futuras",
        "existencia de ledger documental",
        "campos minimos por capacidad",
        "categorias minimas presentes",
        "estados permitidos presentes",
        "estados prohibidos ausentes como estado actual",
        "capacidades bloqueadas explicitas",
        "capacidades futuras explicitas",
        "relacion con allowed_actions",
        "relacion con forbidden_actions",
        "relacion con blocked_capabilities",
        "no ledger visual activo",
        "Criterios de aceptacion futura",
        "ledger documental creado",
        "test creado",
        "capacidades presentes/bloqueadas/futuras documentadas",
        "blocked capabilities explicitas",
        "future capabilities explicitas",
        "validaciones pasan",
        "commit creado",
        "working tree limpio",
        "ledger demasiado amplio",
        "ledger demasiado chico",
        "confundir capacidad futura con presente",
        "confundir capacidad documental con operativa",
        "duplicar contrato de vocabulario",
        "falsa sensacion de cierre global",
        "JSON prematuro",
        "test fragil",
        "clasificar por evidencia",
        "evidence_path",
        "separar presente/bloqueado/futuro",
        "no JSON por defecto",
        "no UI consumption",
        "no backend consumption",
        "no execution",
        "no cierre global todavia",
        "TOP 15 diferido",
    ]:
        assert marker in text


def test_plan_records_top_15_future_decision_next_prompt_and_limits():
    text = read(DOC)

    for marker in [
        "TOP 15 de recomendaciones elite",
        "aplican ahora",
        "futuras",
        "descartables",
        "cubiertas por contratos",
        "chocan con no-runtime/no-execution",
        "sobreconstruccion",
        "necesarias para cierre coronado",
        "CAPABILITIES_LEDGER_PLAN_READY_FOR_IMPLEMENTATION_PLANNING",
        (
            "PROMPT UI/UX 1.154 - Planificar implementacion ledger de capacidades presentes "
            "bloqueadas futuras UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ),
        "no se implemento ledger",
        "no se creo documento ledger 1.154",
        "no se creo test ledger 1.154",
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


def test_contract_1_151_remains_documentation_only_and_test_only():
    assert CONTRACT.exists()
    text = read(CONTRACT)

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
        assert marker in text


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


def test_future_ledger_artifacts_were_not_created():
    assert not FUTURE_LEDGER_DOC.exists()
    assert not FUTURE_LEDGER_TEST.exists()
    assert not FUTURE_LEDGER_JSON.exists()
    assert not FUTURE_LEDGER_FIXTURE.exists()


def test_readme_cursors_record_plan_1_153():
    for path in (README, WEB_README):
        text = read(path)
        assert "Planificacion 1.153: ledger de capacidades presentes/bloqueadas/futuras" in text
        assert "HEAD base `5eb2ed0`" in text
        assert "restore point remoto vigente `f455ca1`" in text
        assert "main ahead por 4 commits al inicio" in text
        assert "matriz de cierre publicada" in text
        assert "contrato de vocabulario/affordances checkpointed" in text
        assert "inicio del bloque 3 de secuencia 1.142" in text
        assert "CAPABILITIES_LEDGER_PLAN_READY_FOR_IMPLEMENTATION_PLANNING" in text
        assert (
            "PROMPT UI/UX 1.154 - Planificar implementacion ledger de capacidades presentes "
            "bloqueadas futuras UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
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


def test_prompt_1_153_did_not_modify_protected_runtime_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "5eb2ed0", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
