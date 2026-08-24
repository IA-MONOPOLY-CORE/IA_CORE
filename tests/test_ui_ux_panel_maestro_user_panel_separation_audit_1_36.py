from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_1_36.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


NEXT_PROMPT = (
    "PROMPT UI/UX 1.37 - Documentar boundaries Panel Maestro / User Panel "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_context():
    text = read(DOC)

    required = [
        "UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_COMPLETED",
        "ec39e9ac",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_35.md",
        "docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md",
        "Panel Maestro",
        "User Panel",
        "shared contract boundary",
        "translation layer",
        "POST_STORYTELLING_SURFACE_SEPARATION_REVIEWED",
    ]

    for marker in required:
        assert marker in text


def test_audit_contains_visual_evidence_and_areas():
    text = read(DOC)

    required = [
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "Areas Auditadas",
        "Superficie actual",
        "Exposicion de datos",
        "Lenguaje",
        "Acciones/permisos",
        "Estados",
        "Evidence/logs/bitacora visual",
        "Request Contract Preview",
        "Raw-safe/detail",
        "Navigation/components",
        "Mobile/responsive",
        "Documentacion/README",
    ]

    for marker in required:
        assert marker in text


def test_findings_include_p0_p1_p2_p3_and_boundary_verdict():
    text = read(DOC)

    required = [
        "PANEL_MAESTRO_USER_PANEL_BOUNDARY_GAPS_IDENTIFIED",
        "PMUP-P0-001",
        "PMUP-P1-001",
        "PMUP-P1-002",
        "PMUP-P1-003",
        "PMUP-P2-001",
        "PMUP-P2-002",
        "PMUP-P3-001",
        "P0",
        "P1",
        "P2",
        "P3",
    ]

    for marker in required:
        assert marker in text


def test_exposure_matrix_categories_are_initialized():
    text = read(DOC)

    required = [
        "PANEL_EXPOSURE_MATRIX_INITIALIZED",
        "Panel Maestro only",
        "User Panel translated",
        "Shared safe",
        "Prohibited for User Panel",
        "Future contract required",
        "Fixture/test only",
        "payload",
        "raw-safe",
        "logs internos",
        "acciones de usuario",
        "contract_fixture",
    ]

    for marker in required:
        assert marker in text


def test_surface_language_state_action_and_logs_rules_are_defined():
    text = read(DOC)

    required = [
        "SURFACE_LANGUAGE_RULES_DEFINED",
        "SURFACE_STATE_RULES_DEFINED",
        "SURFACE_ACTION_PERMISSION_RULES_DEFINED",
        "User Panel no debe mostrar objetos contractuales crudos",
        "User Panel no debe mostrar logs internos",
        "no_payload` -> todavia no hay informacion disponible",
        "planned` -> todavia no disponible",
        "pending` -> pendiente, no en ejecucion",
        "not_available` -> no disponible en este estado",
        "blocked` -> bloqueado/no disponible por seguridad o contrato",
        "forbidden_actions` -> acciones no permitidas",
        "blocked_capabilities` -> funciones no disponibles",
        "read-only` -> solo lectura",
        "backend-only` -> definido por el sistema interno",
        "contract_fixture` -> dato de prueba / ejemplo tecnico solo interno",
        "User Panel no hereda `allowed_actions` internos por defecto",
        "Evidence no debe parecer live log",
    ]

    for marker in required:
        assert marker in text


def test_recommendation_for_1_37_and_limits_are_explicit():
    text = read(DOC)

    required = [
        "Recomendacion Concreta Para 1.37",
        NEXT_PROMPT,
        "matriz Panel Maestro/User Panel por zona",
        "tabla de traducciones",
        "datos prohibidos para User Panel",
        "componentes internos vs reutilizables vs user-safe",
        "1.37 no debe implementar User Panel",
        "no debe implementar User Panel, crear pantallas nuevas, crear rutas, crear endpoints",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "PANEL_SEPARATION_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_PANEL_BOUNDARIES_DOCUMENTATION",
    ]

    for marker in required:
        assert marker in text


def test_audit_confirms_no_runtime_no_endpoints_no_dependencies_and_identity():
    text = read(DOC)

    required = [
        "IA_CORE sigue como identidad activa",
        "No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
        "User Panel no implementado",
        "No se modifico UI activa",
        "Sin endpoints",
        "sin API/router",
        "sin fetch nuevo",
        "sin dependencias nuevas",
        "Sin runtime",
        "sin execution",
        "sin dispatch",
        "sin controlled execution",
        "no `core/`",
        "no `api.py`",
        "no `domains/`",
        "no `tools/`",
        "no modelos",
        "no integraciones",
    ]

    for marker in required:
        assert marker in text


def test_readmes_reference_audit_1_36_and_next_prompt():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_1_36.md" in text
        assert "Panel Maestro" in text
        assert "User Panel" in text
        assert NEXT_PROMPT in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencies" in text.lower()
        assert "no User Panel implementado" in text or "User Panel no implementado" in text

    assert "Next pending step: `PROMPT UI/UX 1.40 - Auditar readiness para futuras pantallas IA_CORE contract-aware sin runtime/no-execution`" in root


def test_active_ui_remains_panel_maestro_not_user_panel_implementation():
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)

    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert 'data-contract-storytelling="contract-aware-1.33"' in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index
    assert "raw-safe" in index
    assert "allowed_actions" in index
    assert "forbidden_actions" in index
    assert "blocked_capabilities" in index

    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in index

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "REQUEST CONTRACT" in admin
    assert "no dispatch desde UI" in admin


def test_all_expected_verdicts_are_present():
    text = read(DOC)

    verdicts = [
        "UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_COMPLETED",
        "POST_STORYTELLING_SURFACE_SEPARATION_REVIEWED",
        "PANEL_MAESTRO_USER_PANEL_BOUNDARY_GAPS_IDENTIFIED",
        "PANEL_EXPOSURE_MATRIX_INITIALIZED",
        "SURFACE_LANGUAGE_RULES_DEFINED",
        "SURFACE_STATE_RULES_DEFINED",
        "SURFACE_ACTION_PERMISSION_RULES_DEFINED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "PANEL_SEPARATION_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_PANEL_BOUNDARIES_DOCUMENTATION",
    ]

    for verdict in verdicts:
        assert verdict in text
