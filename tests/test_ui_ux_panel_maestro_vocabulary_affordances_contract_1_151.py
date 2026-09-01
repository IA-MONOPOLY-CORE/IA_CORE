import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
DISALLOWED_JSON = ROOT / "ui" / "web" / "contracts" / "vocabulary_affordances_contract.v1.json"
DISALLOWED_FIXTURE = ROOT / "tests" / "fixtures" / "ui_vocabulary_affordances_contract_v1.json"
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


def assert_contains_any(text: str, options: tuple[str, ...]) -> None:
    assert any(option in text for option in options), options


def test_contract_exists_and_records_metadata():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Vocabulary Affordances Contract 1.151",
        "contract_id: ui_ux_panel_maestro_vocabulary_affordances_contract",
        "contract_version: 1.151",
        "source_plan: 1.150",
        "base_head: c9867c4",
        "remote_restore_point: f455ca1",
        "mode: DOCUMENTATION_ONLY",
        "status: TEST_ONLY_CONTRACT",
        "runtime: NO_RUNTIME",
        "execution: NO_EXECUTION",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "json_contract: NOT_CREATED",
        "enforcement: TEST_ONLY",
        "c9867c4",
        "f455ca1",
        "main",
        "ahead",
        "89c83c5 docs(ui): planificar contrato vocabulario affordances",
        "c9867c4 docs(ui): planificar implementacion contrato vocabulario",
        "working tree limpio",
        "push no ejecutado",
    ]:
        assert marker in text


def test_contract_records_transition_purpose_scope_and_out_of_scope():
    text = read(DOC)

    for marker in [
        "documental + test-only",
        "no crear JSON estatico todavia",
        "VOCABULARY_AFFORDANCES_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION",
        "reducir ambiguedad semantica",
        "prevenir affordances fantasma",
        "impedir copy operativo falso",
        "preservar limites contractuales",
        "evitar que la UI prometa capacidades no disponibles",
        "proteger `DEFER_FINALIZATION`",
        "proteger FSC",
        "separar lectura/documentacion de ejecucion real",
        "UI visible",
        "documentacion UI",
        "READMEs seleccionados",
        "tests UI/UX",
        "FSC",
        "matriz de cierre",
        "futuros componentes del Panel Maestro",
        "labels",
        "badges",
        "chips",
        "pills",
        "cards",
        "empty states",
        "blocked states",
        "deferred states",
        "read-only states",
        "helper text",
        "captions",
        "futuros botones/links/acciones",
        "backend",
        "runtime",
        "execution",
        "model invocation",
        "tool invocation",
        "integrations",
        "User Panel",
        "endpoints",
        "fetches",
        "scheduler",
        "worker",
        "queue",
        "dispatcher/event bus",
        "state mutation",
        "memory writes",
        "context injection",
        "delivery",
        "auth",
        "secrets",
        "environment variables",
    ]:
        assert marker in text


def test_contract_records_allowed_and_forbidden_vocabulary():
    text = read(DOC)

    for marker in [
        "Allowed vocabulary",
        "Lectura",
        "Documental",
        "Vista",
        "Resumen",
        "Contrato visible",
        "Evidencia",
        "Trazabilidad",
        "Snapshot",
        "Checklist",
        "Matriz",
        "Inventario",
        "Referencia",
        "Plan",
        "Checkpoint",
        "PASSED",
        "PASSED_WITH_MINOR_DEBT",
        "DEFERRED_WITH_GUARDRAILS",
        "BLOCKED_NEEDS_FIX",
        "BLOCKED_CRITICAL",
        "NOT_APPLICABLE",
        "READ_ONLY",
        "BLOCKED_BY_CONTRACT",
        "DOCUMENTED",
        "PLANNED",
        "NOT_IMPLEMENTED",
        "NOT_EXECUTABLE",
        "NO_RUNTIME",
        "NO_EXECUTION",
        "Bloqueado",
        "Diferido",
        "No implementado",
        "Futuro",
        "No ejecutable",
        "Sin runtime",
        "Sin ejecucion",
        "Solo lectura",
        "Pendiente de contrato",
        "Pendiente de backend",
        "Pendiente de validacion",
        "Ver",
        "Revisar",
        "Leer",
        "Consultar",
        "Auditar",
        "Inspeccionar",
        "Comparar",
        "Documentar",
        "Planificar",
        "Forbidden vocabulary",
        "ready to run",
        "run now",
        "execute",
        "executing",
        "launch",
        "start",
        "stop",
        "deploy",
        "submit",
        "send",
        "dispatch",
        "dispatching",
        "process",
        "processing",
        "trigger",
        "fire",
        "invoke",
        "call model",
        "call tool",
        "running",
        "live",
        "operational",
        "success",
        "completed",
        "done",
        "delivered",
        "sent",
        "processed",
        "created in backend",
        "materialized",
        "autonomous",
        "automatic execution",
        "real-time",
        "connected",
        "synced",
        "agent running",
        "model selected for execution",
        "tool ready",
        "integration active",
        "memory updated",
        "context injected",
        "boton ejecutar",
        "boton enviar",
        "boton lanzar",
        "boton procesar",
        "boton despachar",
        "boton activar",
        "boton iniciar",
        "CTA operativo",
        "form operativo",
        "input operativo",
        "preview-and-run",
        "Processing request",
        "Capability active",
    ]:
        assert marker in text


def test_contract_records_contextual_terms_and_affordances():
    text = read(DOC)

    for marker in [
        "Contextual terms",
        "completed",
        "done",
        "materialized",
        "active",
        "enabled",
        "available",
        "ready",
        "connected",
        "synced",
        "generated",
        "created",
        "published",
        "selected",
        "DOCUMENTATION_ONLY",
        "READ_ONLY",
        "BLOCKED",
        "DEFERRED",
        "NOT_EXECUTABLE",
        "no aparecen como estado actual operativo visible",
        "Allowed affordances",
        "cards read-only",
        "informational badges",
        "non-interactive chips",
        "documentary pills",
        "blocked banners",
        "deferred notes",
        "evidence sections",
        "read-only matrices",
        "disabled visual markers",
        "navigation visual no operativa",
        "copy de inspeccion/documentacion",
        "indicadores derivados de contrato existente",
        "scroll/accesibilidad visual sin accion",
        "labels contractuales",
        "warnings contractuales",
        "Forbidden affordances",
        "botones activos no respaldados por backend",
        "forms activos",
        "inputs con submit",
        "fake disabled",
        "links que parezcan ejecutar",
        "loaders falsos",
        "spinners de procesamiento",
        "progress bars",
        "toasts de exito operativo",
        "estados live/running",
        "cards que sugieran agente activo",
        "badges que sugieran conexion real",
        "toggles activos",
        "switches activos",
        "dropdowns que cambien contrato",
        "selector que dispare operacion",
        "wizard ejecutable",
        "command palette operativa",
        "terminal/console que sugiera ejecucion",
        "cualquier affordance que implique runtime/execution/dispatch",
        "cualquier affordance que no este respaldada por backend declarado",
    ]:
        assert marker in text


def test_contract_preserves_fsc_defer_matrix_debts_and_enforcement_limits():
    text = read(DOC)

    for marker in [
        "FSC preservation",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "no debe agregarse quinta FSC",
        "FSC no debe convertirse en pantalla operativa",
        "FSC no debe transformarse en wizard",
        "FSC no debe disparar backend",
        "FSC no debe prometer ejecucion",
        "DEFER preservation",
        "DEFER_FINALIZATION",
        "finalization remains deferred",
        "ningun texto visible debe contradecir `DEFER_FINALIZATION`",
        "no debe anunciarse UI/UX 1.x como totalmente cerrada antes del ledger",
        "Matrix preservation",
        "matriz de cierre UI/UX 1.x debe preservarse como read-only",
        "matriz no es wizard",
        "matriz no dispara acciones",
        "matriz no ejecuta backend",
        "matriz no crea estado",
        "matriz no publica datos",
        "matriz no valida en runtime",
        "matriz funciona como evidencia visual/documental",
        "Known semantic debts",
        "duplicidad semantica + / DOMAIN",
        "+ no debe parecer accion operativa",
        "DOMAIN no debe parecer endpoint/runtime",
        "no se renombra `+` en 1.151",
        "no se renombra `DOMAIN` en 1.151",
        "scripts inferiores heredados",
        "tecnicismo documental alto",
        "ninguna de estas deudas se corrige en 1.151",
        "Enforcement model",
        "enforcement es test-only",
        "no hay enforcement runtime",
        "no hay backend validator",
        "no hay JS validator activo",
        "no hay UI consumer",
        "no hay JSON contractual",
        "tests pueden leer contrato/documentos/UI/JS como archivos estaticos",
        "tests no deben modificar archivos",
        "tests no deben requerir red",
        "tests no deben requerir browser externo",
        "tests no deben requerir dependencias nuevas",
        "tests deben evitar global repo scan fragil",
        "archivos seleccionados",
    ]:
        assert marker in text


def test_contract_records_contextual_validation_future_gates_non_goals_and_decision():
    text = read(DOC)

    for marker in [
        "Contextual validation rules",
        "terminos prohibidos pueden aparecer en la propia denylist",
        "terminos prohibidos pueden aparecer en tests que validan la denylist",
        "terminos prohibidos pueden aparecer en historial/commits",
        "terminos prohibidos pueden aparecer en documentacion si estan marcados como prohibidos",
        "terminos prohibidos NO deben aparecer como copy visible operativo actual",
        "terminos contextuales deben estar calificados",
        "falsos positivos",
        "documentacion historica correctamente marcada",
        "Future gates",
        "cualquier cambio futuro de texto visible requiere revision humana",
        "cualquier implementacion visual futura debe preservar no-runtime/no-execution",
        "cualquier implementacion visual futura debe preservar FSC",
        "cualquier implementacion visual futura debe preservar `DEFER_FINALIZATION`",
        "ledger futuro debe respetar este contrato",
        "cierre global UI/UX 1.x debe verificar este contrato",
        "Non-goals",
        "no resolver + / DOMAIN",
        "no corregir scripts inferiores",
        "no reducir tecnicismo documental",
        "no limpiar deuda residual",
        "no implementar ledger",
        "no cerrar UI/UX 1.x globalmente",
        "no publicar restore point",
        "no crear runtime",
        "no crear backend",
        "VOCABULARY_AFFORDANCES_CONTRACT_IMPLEMENTED_TEST_ONLY",
        (
            "PROMPT UI/UX 1.152 - Checkpoint contrato de vocabulario affordances UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ),
    ]:
        assert marker in text


def test_limits_preserved_and_no_json_contract_created():
    text = read(DOC)

    assert not DISALLOWED_JSON.exists()
    assert not DISALLOWED_FIXTURE.exists()

    for marker in [
        "no se creo JSON contractual",
        "no se creo contrato consumido por UI",
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
        "no se avanzo al ledger de capacidades",
        "no se avanzo al cierre global UI/UX 1.x",
    ]:
        assert marker in text


def test_current_ui_readonly_surface_preserves_fsc_defer_and_avoids_operational_copy():
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


def test_readme_cursors_record_contract_1_151():
    for path in (README, WEB_README):
        text = read(path)
        assert "Contrato 1.151: vocabulario/affordances UI/UX 1.x" in text
        assert "HEAD base `c9867c4`" in text
        assert "restore point remoto vigente `f455ca1`" in text
        assert "main ahead por 2 commits al inicio" in text
        assert "documental + test-only" in text
        assert "docs/UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md" in text
        assert "tests/test_ui_ux_panel_maestro_vocabulary_affordances_contract_1_151.py" in text
        assert "no JSON contractual" in text
        assert "no contrato consumido por UI" in text
        assert "no UI activa" in text
        assert "no JS" in text
        assert "no backend" in text
        assert "no runtime" in text
        assert "no push" in text
        assert (
            "PROMPT UI/UX 1.152 - Checkpoint contrato de vocabulario affordances UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text


def test_prompt_1_151_did_not_modify_protected_runtime_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "c9867c4", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
