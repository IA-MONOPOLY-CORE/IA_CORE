from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_1_37.md"
AUDIT_1_36 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_1_36.md"
PLAN_1_35 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_35.md"
CHECKPOINT_1_34 = ROOT / "docs" / "UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


NEXT_PROMPT = (
    "PROMPT UI/UX 1.38 - Checkpoint boundaries Panel Maestro / User Panel "
    "IA_CORE contract-aware sin runtime/no-execution"
)


PREVIOUS_PROMPT = (
    "PROMPT UI/UX 1.37 - Documentar boundaries Panel Maestro / User Panel "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_boundaries_document_exists_and_links_previous_context():
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro / User Panel Boundaries 1.37",
        "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_DOCUMENTED",
        "e1459d46",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_35.md",
        "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_1_36.md",
        "docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md",
        "533d0c33",
        "IA_CORE sigue como identidad activa",
        "Panel Maestro / operador interno",
        "User Panel no existe como implementacion",
        "No-alcance",
    ]

    for marker in required:
        assert marker in text

    assert AUDIT_1_36.exists()
    assert PLAN_1_35.exists()
    assert CHECKPOINT_1_34.exists()


def test_formal_definitions_and_data_categories_are_complete():
    text = read(DOC)

    required = [
        "Panel Maestro",
        "User Panel",
        "shared contract boundary",
        "translation layer futura",
        "Categorias De Datos",
        "Datos tecnicos",
        "Datos traducibles",
        "Datos compartidos seguros",
        "Datos prohibidos",
        "Datos que requieren contrato futuro",
        "Fixtures/test only",
        "Ningun panel infiere permisos",
        "Ningun panel sugiere runtime/execution/dispatch",
    ]

    for marker in required:
        assert marker in text


def test_exposure_matrix_formalizes_required_elements_and_categories():
    text = read(DOC)

    required = [
        "PANEL_EXPOSURE_MATRIX_FORMALIZED",
        "Panel Maestro only",
        "User Panel translated",
        "Shared safe",
        "Prohibited for User Panel",
        "Future contract required",
        "Fixture/test only",
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

    for marker in required:
        assert marker in text


def test_language_translation_state_action_and_logs_rules_are_documented():
    text = read(DOC)

    required = [
        "SURFACE_LANGUAGE_BOUNDARIES_DEFINED",
        "Tabla De Traducciones Iniciales",
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
        "SURFACE_STATE_BOUNDARIES_DEFINED",
        "Estados prohibidos como validos de UI",
        "active",
        "running",
        "live",
        "executing",
        "dispatching",
        "submitted",
        "processing",
        "SURFACE_ACTION_PERMISSION_BOUNDARIES_DEFINED",
        "User Panel no hereda",
        "allowed_actions",
        "forbidden_actions",
        "nunca se muestran como botones",
        "blocked_capabilities",
        "nunca se muestran como CTAs",
        "No submit",
        "No dispatch",
        "No execution",
        "No runtime",
        "SURFACE_EVIDENCE_LOG_BOUNDARIES_DEFINED",
        "Evidence/logs no son live log",
    ]

    for marker in required:
        assert marker in text


def test_component_navigation_responsive_guardrails_and_risks_are_documented():
    text = read(DOC)

    required = [
        "SURFACE_COMPONENT_NAVIGATION_BOUNDARIES_DEFINED",
        "Reglas De Componentes Y Navegacion",
        "cards de contrato",
        "widgets contract-aware",
        "detail panels",
        "raw-safe panels",
        "request preview",
        "status chips",
        "blocked/forbidden panels",
        "next step",
        "glossary",
        "navigation local",
        "density tiers",
        "admin panels / config",
        "SURFACE_RESPONSIVE_MOBILE_BOUNDARIES_DEFINED",
        "Reglas Responsive / Mobile",
        "Guardrails Para Futuro User Panel",
        "no endpoint nuevo sin contrato",
        "no permisos por ausencia de listas",
        "no ocultar blockers criticos",
        "Riesgos Residuales",
        "Translation layer es conceptual",
        "Futuras pantallas deben pasar por auditoria",
    ]

    for marker in required:
        assert marker in text


def test_backup_policy_next_prompt_scope_and_verdicts_are_complete():
    text = read(DOC)

    required = [
        "Politica De Backup",
        "Push de 1.37 queda pospuesto",
        "restore point remoto vigente sigue siendo",
        "533d0c33",
        "proximo restore point recomendado queda despues del checkpoint 1.38",
        "No push despues de cada prompt",
        "Confirmaciones De Alcance",
        "No se modifico UI activa",
        "Sin endpoints",
        "sin API/router",
        "sin fetch nuevo",
        "sin dependencias nuevas",
        "Sin runtime",
        "sin execution",
        "sin dispatch",
        "sin controlled execution",
        "core/",
        "api.py",
        "domains/",
        "tools/",
        "PANEL_BOUNDARIES_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_PANEL_BOUNDARIES_CHECKPOINT",
        NEXT_PROMPT,
    ]

    for marker in required:
        assert marker in text

    verdicts = [
        "UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_DOCUMENTED",
        "PANEL_EXPOSURE_MATRIX_FORMALIZED",
        "SURFACE_LANGUAGE_BOUNDARIES_DEFINED",
        "SURFACE_STATE_BOUNDARIES_DEFINED",
        "SURFACE_ACTION_PERMISSION_BOUNDARIES_DEFINED",
        "SURFACE_EVIDENCE_LOG_BOUNDARIES_DEFINED",
        "SURFACE_COMPONENT_NAVIGATION_BOUNDARIES_DEFINED",
        "SURFACE_RESPONSIVE_MOBILE_BOUNDARIES_DEFINED",
        "USER_PANEL_TRANSLATION_LAYER_CONCEPTUAL_ONLY",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "PANEL_BOUNDARIES_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_PANEL_BOUNDARIES_CHECKPOINT",
    ]

    for verdict in verdicts:
        assert verdict in text


def test_readmes_reference_boundaries_1_37_and_advance_to_checkpoint_1_38():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_1_37.md" in text
        assert "Panel Maestro" in text
        assert "User Panel" in text
        assert PREVIOUS_PROMPT in text
        assert NEXT_PROMPT in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()
        assert "sin endpoints" in text or "no endpoints" in text.lower()
        assert "sin dependencias" in text or "no dependencies" in text.lower()
        assert "User Panel no implementado" in text or "no implementa User Panel" in text

    assert "Next pending step:" in root
    assert NEXT_PROMPT in root


def test_active_ui_remains_panel_maestro_without_user_panel_or_runtime_authority():
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