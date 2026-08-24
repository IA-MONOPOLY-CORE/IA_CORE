from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_1_41.md"
AUDIT_1_40 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_AUDIT_1_40.md"
PLAN_1_39 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_39.md"
CHECKPOINT_1_38 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


CURRENT_PROMPT = (
    "PROMPT UI/UX 1.41 - Documentar readiness de futuras pantallas "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.42 - Checkpoint readiness futuras pantallas "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_readiness_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Future Screens Readiness 1.41",
        "UI_UX_FUTURE_SCREENS_READINESS_DOCUMENTED",
        "671fdc73",
        "docs/UI_UX_FUTURE_SCREENS_READINESS_AUDIT_1_40.md",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_39.md",
        "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md",
        "Readiness for Future Screens",
        "User Panel no implementado",
        "translation layer conceptual only",
        "restore point remoto 6e474fd6",
    ]

    for marker in required:
        assert marker in text

    assert AUDIT_1_40.exists()
    assert PLAN_1_39.exists()
    assert CHECKPOINT_1_38.exists()


def test_formal_definitions_are_present():
    text = read(DOC)

    definitions = [
        "Future Screen",
        "Readiness Gate",
        "Screen Contract",
        "Surface Ownership",
        "Screen Candidate Matrix",
        "Extraction Safety",
        "Navigation Safety",
        "User-Safe Variant",
        "Panel Maestro",
        "User Panel",
        "Shared safe",
        "Future only",
        "Prohibited",
    ]

    for marker in definitions:
        assert marker in text


def test_all_readiness_gates_are_formalized():
    text = read(DOC)

    gates = [
        "contract gate",
        "surface ownership gate",
        "data exposure gate",
        "action permission gate",
        "state/empty-state gate",
        "evidence/log gate",
        "navigation gate",
        "responsive/accessibility gate",
        "component reuse gate",
        "no-runtime/no-execution gate",
        "test gate",
    ]
    gate_rules = [
        "Toda future screen debe tener Screen Contract",
        "Ninguna pantalla puede quedar sin owner",
        "payload/schema/raw-safe/logs internos estan prohibidos para User Panel",
        "Ausencia de allowed_actions significa no mostrar accion",
        "forbidden_actions nunca se convierten en boton",
        "blocked_capabilities nunca son CTA ambiguo",
        "pending no significa corriendo",
        "planned no significa disponible",
        "No live log",
        "No rutas sin Screen Contract",
        "Critical info always visible",
        "Componente Panel Maestro no pasa a User Panel sin variante user-safe",
        "No endpoint nuevo",
        "Todo Screen Contract requiere test documental",
    ]

    assert "FUTURE_SCREEN_READINESS_GATES_FORMALIZED" in text
    for marker in gates + gate_rules:
        assert marker in text


def test_screen_contract_template_is_formal_and_complete():
    text = read(DOC)

    fields = [
        "screen_id",
        "title",
        "purpose",
        "surface",
        "audience",
        "owner",
        "source_contracts",
        "allowed_data",
        "prohibited_data",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "states",
        "empty_states",
        "blocked_states",
        "evidence_rules",
        "navigation_rules",
        "responsive_rules",
        "accessibility_rules",
        "component_rules",
        "translation_rules",
        "no_runtime_no_execution_confirmation",
        "endpoint_dependency_confirmation",
        "tests_required",
        "rollback_or_avoidance_notes",
        "approval_status",
    ]

    assert "SCREEN_CONTRACT_TEMPLATE_FORMALIZED" in text
    assert "Esta plantilla es documental y no crea pantallas" in text
    for marker in fields:
        assert marker in text


def test_screen_candidate_matrix_is_formalized_with_required_candidates():
    text = read(DOC)

    candidates = [
        "contract detail",
        "request contract preview",
        "evidence/logs",
        "validation/readiness",
        "blocked/forbidden/capabilities",
        "raw-safe/detail",
        "component/style reference",
        "Panel Maestro overview",
        "User Panel futuro",
        "domain/status overview",
        "prompts/checkpoints bitacora",
        "future screen readiness dashboard",
    ]
    columns = [
        "surface owner",
        "allowed data",
        "prohibited data",
        "actions",
        "required states",
        "readiness gates pendientes",
        "readiness actual",
        "recomendacion",
    ]

    assert "SCREEN_CANDIDATE_MATRIX_FORMALIZED" in text
    for marker in candidates + columns:
        assert marker in text


def test_navigation_data_action_state_extraction_and_component_rules_are_documented():
    text = read(DOC)

    required = [
        "NAVIGATION_READINESS_RULES_DEFINED",
        "no route without Screen Contract",
        "no hash routing operativo",
        "no endpoint-driven screen sin contrato",
        "no deep-link que parezca feature activa",
        "Navegacion local actual sigue segura",
        "DATA_ACTION_STATE_READINESS_RULES_DEFINED",
        "No permission inference",
        "No false availability",
        "No false operation",
        "EXTRACTION_SAFETY_RULES_FORMALIZED",
        "No extraer una seccion si deja sin contexto la consola raiz",
        "No esconder blocked/forbidden",
        "No convertir disclosure en pantalla sin Screen Contract",
        "No crear screen por densidad solamente",
        "COMPONENT_READINESS_RULES_DEFINED",
        "Componentes actuales son Panel Maestro first",
        "User-Safe Variant requerida para User Panel",
        "raw-safe/detail no son user-safe",
        "request preview no es form",
        "evidence/logs no son live log",
        "blocked/forbidden no son CTA",
    ]

    for marker in required:
        assert marker in text


def test_residual_risks_limits_for_1_42_and_next_prompt_are_documented():
    text = read(DOC)

    required = [
        "Riesgos Residuales",
        "Future screens todavia no existen",
        "User Panel todavia no existe",
        "Translation layer conceptual only",
        "No hay Screen Registry implementado",
        "Navegacion futura sigue pendiente",
        "Component docs quedan como bloque futuro",
        "Secondary views quedan pospuestas",
        "Polish premium queda pospuesto",
        "Benchmarks externos quedan pospuestos",
        "Limites Para 1.42",
        "1.42 debe cerrar checkpoint",
        "1.42 NO debe implementar pantallas",
        NEXT_PROMPT,
        "proximo restore point recomendado sigue siendo despues del checkpoint 1.42",
    ]

    for marker in required:
        assert marker in text


def test_scope_confirmations_and_contract_boundaries_are_preserved():
    text = read(DOC)

    required = [
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_READINESS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_FUTURE_SCREENS_READINESS_CHECKPOINT",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "IA_CORE sigue como identidad activa",
        "No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
        "No endpoint nuevo",
        "No API/router nuevo",
        "No fetch nuevo",
        "No dependencias nuevas",
        "No runtime, no execution, no dispatch, no controlled execution, no submit",
        "no core/",
        "no api.py",
        "no domains/",
        "no tools/",
        "no modelos",
        "no integraciones",
    ]

    for marker in required:
        assert marker in text


def test_readmes_reference_readiness_1_41_and_next_prompt_1_42():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_FUTURE_SCREENS_READINESS_1_41.md" in text
        assert CURRENT_PROMPT in text
        assert "readiness gates" in text
        assert "Screen Contract Template" in text
        assert "future screens no implementadas" in text or "Future screens no implementadas" in text
        assert "User Panel no implementado" in text or "User Panel sigue futuro" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoint" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert NEXT_PROMPT in text

    bt = chr(96)
    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root


def test_active_ui_remains_ia_core_panel_maestro_without_new_future_screen_runtime():
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
    assert "location.hash" not in interactions
    assert "hashchange" not in interactions
    assert "REQUEST CONTRACT" in admin
    assert "no dispatch desde UI" in admin


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_FUTURE_SCREENS_READINESS_DOCUMENTED",
        "FUTURE_SCREEN_READINESS_GATES_FORMALIZED",
        "SCREEN_CONTRACT_TEMPLATE_FORMALIZED",
        "SCREEN_CANDIDATE_MATRIX_FORMALIZED",
        "NAVIGATION_READINESS_RULES_DEFINED",
        "DATA_ACTION_STATE_READINESS_RULES_DEFINED",
        "EXTRACTION_SAFETY_RULES_FORMALIZED",
        "COMPONENT_READINESS_RULES_DEFINED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_READINESS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_FUTURE_SCREENS_READINESS_CHECKPOINT",
    ]

    for verdict in verdicts:
        assert verdict in text
