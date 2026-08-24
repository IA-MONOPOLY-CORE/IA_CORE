from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_AUDIT_1_40.md"
PLAN_1_39 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_39.md"
CHECKPOINT_1_38 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


CURRENT_PROMPT = (
    "PROMPT UI/UX 1.40 - Auditar readiness para futuras pantallas "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.41 - Documentar readiness de futuras pantallas "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Future Screens Readiness Audit 1.40",
        "UI_UX_FUTURE_SCREENS_READINESS_AUDIT_COMPLETED",
        "655a21ac",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_39.md",
        "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_CHECKPOINT_1_38.md",
        "Readiness for Future Screens",
        "Panel Maestro / operador interno",
        "User Panel no implementado",
        "translation layer conceptual only",
        "UI activa untouched",
    ]

    for marker in required:
        assert marker in text

    assert PLAN_1_39.exists()
    assert CHECKPOINT_1_38.exists()


def test_required_definitions_and_human_visual_evidence_are_present():
    text = read(DOC)

    required = [
        "Future Screen",
        "Readiness Gate",
        "Screen Contract",
        "Surface Ownership",
        "Navigation Readiness",
        "Data Readiness",
        "Action Readiness",
        "Visual Readiness",
        "Lo veo muy bien",
        "Veo graficamente los prompts que mandamos",
        "ES TODO VISUAL",
        "NO HAY NINGUN BOTON",
        "TODO BIEN ORDENADO PROLIJO",
        "bitacora/capa visual de comprension",
    ]

    for marker in required:
        assert marker in text


def test_audited_areas_and_findings_cover_priorities():
    text = read(DOC)

    areas = [
        "Superficie actual",
        "Candidatos a future screens",
        "Contrato de pantalla",
        "Navegacion",
        "Datos",
        "Acciones/permisos",
        "Estados/empty states",
        "Evidence/logs/trazabilidad",
        "Componentes",
        "Responsive/accessibility",
        "README/documentacion",
    ]
    findings = [
        "P0-001",
        "P0-002",
        "P0-003",
        "P1-001",
        "P1-002",
        "P1-003",
        "P1-004",
        "P1-005",
        "P1-006",
        "P2-001",
        "P2-002",
        "P2-003",
        "P3-001",
        "P3-002",
        "No hay P0 implementativo detectado",
    ]

    for marker in areas + findings:
        assert marker in text


def test_candidate_matrix_is_complete_and_contract_aware():
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
        "Proposito",
        "Superficie probable",
        "Audience",
        "Datos permitidos",
        "Datos prohibidos",
        "Acciones",
        "Estados requeridos",
        "Riesgo principal",
        "Readiness actual",
        "Recomendacion",
    ]

    assert "FUTURE_SCREEN_CANDIDATES_IDENTIFIED" in text
    for marker in candidates + columns:
        assert marker in text


def test_readiness_gates_and_screen_contract_template_are_initialized():
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
    template_fields = [
        "screen_id",
        "title",
        "purpose",
        "surface",
        "audience",
        "allowed_data",
        "prohibited_data",
        "allowed_actions",
        "forbidden_actions",
        "states",
        "empty_states",
        "blocked_states",
        "evidence_rules",
        "navigation_rules",
        "responsive_rules",
        "accessibility_rules",
        "no_runtime_no_execution_confirmation",
        "tests_required",
        "rollback_avoidance_notes",
    ]

    assert "FUTURE_SCREEN_READINESS_GATES_INITIALIZED" in text
    assert "SCREEN_CONTRACT_TEMPLATE_INITIALIZED" in text
    for marker in gates + template_fields:
        assert marker in text


def test_extraction_safety_and_1_41_recommendation_are_explicit():
    text = read(DOC)

    required = [
        "EXTRACTION_SAFETY_RULES_DEFINED",
        "No mover informacion critica si deja hueco en la consola raiz",
        "No esconder forbidden_actions",
        "No esconder blocked_capabilities",
        "No romper story before raw detail",
        "No separar evidence de su contexto documental",
        "No convertir detail en accion",
        "No abrir route, hash routing o deep link sin Screen Contract",
        "No reutilizar Panel Maestro component en User Panel sin variante user-safe",
        "1.41 debe documentar readiness gates",
        "crear checklist para future screens",
        "crear Screen Contract Template",
        "definir reglas de navegacion futura",
        "definir reglas de data/action/state readiness",
        "definir reglas de component readiness",
        "actualizar READMEs",
        "crear tests",
        NEXT_PROMPT,
    ]

    for marker in required:
        assert marker in text


def test_scope_confirmations_are_preserved():
    text = read(DOC)

    required = [
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "IA_CORE sigue como identidad activa",
        "No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
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
        "6e474fd6",
        "proximo restore point recomendado sigue siendo despues del checkpoint 1.42",
    ]

    for marker in required:
        assert marker in text


def test_readmes_reference_audit_1_40_and_next_prompt_1_41():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_FUTURE_SCREENS_READINESS_AUDIT_1_40.md" in text
        assert CURRENT_PROMPT in text
        assert "Readiness for Future Screens" in text
        assert "future screens no implementadas" in text or "Future screens no implementadas" in text
        assert "User Panel no implementado" in text or "User Panel sigue futuro" in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoint" in text.lower()
        assert "sin dependencias" in text or "no dependencias" in text.lower() or "no dependencies" in text.lower()
        assert NEXT_PROMPT in text

    assert "Next pending step: `PROMPT UI/UX 1.46 - Checkpoint Component Documentation / Style Reference IA_CORE contract-aware sin runtime/no-execution`" in root


def test_active_ui_remains_panel_maestro_without_future_screen_implementation():
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
        "UI_UX_FUTURE_SCREENS_READINESS_AUDIT_COMPLETED",
        "POST_PANEL_BOUNDARIES_READINESS_REVIEWED",
        "FUTURE_SCREEN_CANDIDATES_IDENTIFIED",
        "FUTURE_SCREEN_READINESS_GATES_INITIALIZED",
        "SCREEN_CONTRACT_TEMPLATE_INITIALIZED",
        "SURFACE_OWNERSHIP_RULES_REVIEWED",
        "EXTRACTION_SAFETY_RULES_DEFINED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_FUTURE_SCREENS_READINESS_DOCUMENTATION",
    ]

    for verdict in verdicts:
        assert verdict in text
