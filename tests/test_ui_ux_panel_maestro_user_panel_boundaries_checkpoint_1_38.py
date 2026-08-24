from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md"
PLAN_1_35 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_35.md"
AUDIT_1_36 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_1_36.md"
BOUNDARIES_1_37 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_1_37.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


NEXT_PROMPT = (
    "PROMPT UI/UX 1.39 - Consolidar siguiente bloque UI/UX post Panel Boundaries "
    "IA_CORE contract-aware sin runtime/no-execution"
)


PREVIOUS_PROMPT = (
    "PROMPT UI/UX 1.38 - Checkpoint boundaries Panel Maestro / User Panel "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_context():
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro / User Panel Boundaries Checkpoint 1.38",
        "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_PASSED",
        "dc953c1a",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_35.md",
        "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_1_36.md",
        "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_1_37.md",
        "Panel Maestro",
        "User Panel",
        "shared contract boundary",
        "translation layer",
        "translation layer conceptual only",
    ]

    for marker in required:
        assert marker in text

    assert PLAN_1_35.exists()
    assert AUDIT_1_36.exists()
    assert BOUNDARIES_1_37.exists()


def test_checkpoint_confirms_plan_audit_boundaries_and_runner_incident():
    text = read(DOC)

    required = [
        "Panel Maestro vs User Panel Separation Planning",
        "1.36 audit -> 1.37 boundaries -> 1.38 checkpoint",
        "1.36 fue auditoria documental",
        "P0/P1/P2/P3",
        "matriz formal de exposicion",
        "reglas de lenguaje por superficie",
        "tabla de traducciones iniciales",
        "reglas de estados por superficie",
        "reglas de acciones/permisos",
        "reglas de evidence/logs",
        "reglas de componentes/navegacion",
        "reglas responsive/mobile",
        "guardrails para futuro User Panel",
        "RUNNER_INCIDENT_RESOLVED_WITHOUT_REPO_DAMAGE",
        "test vacio fue completado",
    ]

    for marker in required:
        assert marker in text


def test_exposure_categories_and_elements_are_confirmed():
    text = read(DOC)

    categories = [
        "Panel Maestro only",
        "User Panel translated",
        "Shared safe",
        "Prohibited for User Panel",
        "Future contract required",
        "Fixture/test only",
    ]
    elements = [
        "payload",
        "schema",
        "raw-safe",
        "summary",
        "detail",
        "validation",
        "readiness",
        "status",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
        "request contract preview",
        "evidence/logs",
        "prompts/checkpoints",
        "internal exposure registry",
        "internal dispatcher no-runtime",
        "response adapter",
        "contract_fixture",
        "no_payload",
        "planned",
        "pending",
        "not_available",
        "blocked",
        "read-only",
        "backend-only",
        "service_kind",
        "schema_version",
    ]

    assert "PANEL_EXPOSURE_MATRIX_CONFIRMED" in text
    for marker in categories + elements:
        assert marker in text


def test_translations_and_surface_rules_are_confirmed():
    text = read(DOC)

    translations = [
        "Todavia no hay informacion disponible.",
        "Todavia no disponible.",
        "Pendiente; no se esta ejecutando.",
        "No disponible en este estado.",
        "No disponible por seguridad o contrato.",
        "Acciones no permitidas.",
        "Funciones no disponibles.",
        "Solo lectura.",
        "Definido por el sistema interno.",
        "Dato de prueba interno.",
        "Vista previa interna del pedido.",
        "Registro interno de trazabilidad.",
        "Version interna del formato.",
        "Tipo interno de servicio.",
    ]
    rules = [
        "SURFACE_LANGUAGE_BOUNDARIES_CONFIRMED",
        "SURFACE_STATE_BOUNDARIES_CONFIRMED",
        "SURFACE_ACTION_PERMISSION_BOUNDARIES_CONFIRMED",
        "SURFACE_EVIDENCE_LOG_BOUNDARIES_CONFIRMED",
        "SURFACE_COMPONENT_NAVIGATION_BOUNDARIES_CONFIRMED",
        "SURFACE_RESPONSIVE_MOBILE_BOUNDARIES_CONFIRMED",
        "Ningun panel infiere permisos",
        "User Panel no hereda allowed_actions internos",
        "forbidden_actions nunca se muestran como botones",
        "blocked_capabilities nunca se muestran como CTAs",
        "No submit",
        "No dispatch",
        "No execution",
        "No runtime",
        "Evidence/logs no son live log",
        "no endpoint nuevo sin contrato",
        "no ocultar blockers criticos",
    ]

    for marker in translations + rules:
        assert marker in text


def test_scope_ui_backend_backup_and_next_prompt_are_confirmed():
    text = read(DOC)

    required = [
        "User Panel no existe implementado",
        "No aparecen CTAs nuevos de ejecucion",
        "Request contract preview sigue read-only/no-submit/no-dispatch/no-execution",
        "backend-contract-widgets.js y console-interactions.js siguen sin fetch",
        "no endpoint nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no fetch nuevo no autorizado",
        "no /api/debate/start",
        "no /api/dispatch nuevo ni operativo",
        "no runtime/execution/dispatch/controlled execution",
        "no librerias nuevas",
        "no dependencias nuevas",
        "no se toco core/",
        "no se toco api.py",
        "no se toco domains/ operativo",
        "no se toco tools/",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "533d0c33",
        NEXT_PROMPT,
    ]

    for marker in required:
        assert marker in text


def test_readmes_reference_checkpoint_and_next_planning_prompt():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md" in text
        assert PREVIOUS_PROMPT in text
        assert NEXT_PROMPT in text
        assert "UI/UX cerrado hasta 1.38" in text or "Checkpoint Panel Maestro vs User Panel boundaries 1.38" in text
        assert "User Panel no implementado" in text or "User Panel no existe implementado" in text
        assert "translation layer conceptual" in text or "translation layer queda conceptual" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoint" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower()

    assert "Next pending step:" in root
    assert NEXT_PROMPT in root


def test_active_ui_remains_panel_maestro_contract_aware_without_new_authority():
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert 'data-contract-storytelling="contract-aware-1.33"' in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index
    assert "allowed_actions" in index
    assert "forbidden_actions" in index
    assert "blocked_capabilities" in index

    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in index

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "REQUEST CONTRACT" in admin
    assert "no dispatch desde UI" in admin


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_PASSED",
        "PANEL_BOUNDARIES_BLOCK_CONFIRMED",
        "PANEL_MAESTRO_INTERNAL_SURFACE_CONFIRMED",
        "USER_PANEL_FUTURE_SURFACE_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "SHARED_CONTRACT_BOUNDARY_CONFIRMED",
        "TRANSLATION_LAYER_CONCEPTUAL_ONLY_CONFIRMED",
        "PANEL_EXPOSURE_MATRIX_CONFIRMED",
        "SURFACE_LANGUAGE_BOUNDARIES_CONFIRMED",
        "SURFACE_STATE_BOUNDARIES_CONFIRMED",
        "SURFACE_ACTION_PERMISSION_BOUNDARIES_CONFIRMED",
        "SURFACE_EVIDENCE_LOG_BOUNDARIES_CONFIRMED",
        "SURFACE_COMPONENT_NAVIGATION_BOUNDARIES_CONFIRMED",
        "SURFACE_RESPONSIVE_MOBILE_BOUNDARIES_CONFIRMED",
        "RUNNER_INCIDENT_RESOLVED_WITHOUT_REPO_DAMAGE",
        "PANEL_BOUNDARIES_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "PANEL_BOUNDARIES_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]

    for verdict in verdicts:
        assert verdict in text