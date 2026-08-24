from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md"
PLAN_1_39 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_39.md"
AUDIT_1_40 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_AUDIT_1_40.md"
READINESS_1_41 = ROOT / "docs" / "UI_UX_FUTURE_SCREENS_READINESS_1_41.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"

CURRENT_PROMPT = (
    "PROMPT UI/UX 1.42 - Checkpoint readiness futuras pantallas "
    "IA_CORE contract-aware sin runtime/no-execution"
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.43 - Consolidar siguiente bloque UI/UX post Future Screens "
    "Readiness IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_block_context():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Future Screens Readiness Checkpoint 1.42",
        "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_PASSED",
        "c0f8946e",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_39.md",
        "docs/UI_UX_FUTURE_SCREENS_READINESS_AUDIT_1_40.md",
        "docs/UI_UX_FUTURE_SCREENS_READINESS_1_41.md",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "6e474fd6",
        "Readiness for Future Screens",
    ]
    for marker in required:
        assert marker in text

    assert PLAN_1_39.exists()
    assert AUDIT_1_40.exists()
    assert READINESS_1_41.exists()


def test_checkpoint_confirms_required_definitions():
    text = read(DOC)

    for marker in [
        "Future Screen",
        "Readiness Gate",
        "Screen Contract",
        "Surface Ownership",
        "Screen Candidate Matrix",
        "Extraction Safety",
        "Navigation Safety",
        "User-Safe Variant",
    ]:
        assert marker in text


def test_checkpoint_confirms_all_readiness_gates():
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

    assert "FUTURE_SCREEN_READINESS_GATES_CONFIRMED" in text
    for gate in gates:
        assert gate in text


def test_screen_contract_template_is_confirmed_with_minimum_fields():
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

    assert "SCREEN_CONTRACT_TEMPLATE_CONFIRMED" in text
    assert "```yaml" in text
    for field in fields:
        assert field in text


def test_screen_candidate_matrix_is_confirmed_with_minimum_candidates():
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

    assert "SCREEN_CANDIDATE_MATRIX_CONFIRMED" in text
    for candidate in candidates:
        assert candidate in text


def test_navigation_data_action_state_extraction_and_component_readiness_are_confirmed():
    text = read(DOC)

    required = [
        "NAVIGATION_READINESS_CONFIRMED",
        "no route without Screen Contract",
        "no hash routing operativo",
        "no endpoint-driven screen sin contrato",
        "no deep-link que parezca feature activa",
        "navegacion local actual sigue segura",
        "future navigation preserva root console",
        "future navigation preserva critical always visible",
        "future navigation respeta Panel Maestro/User Panel boundaries",
        "DATA_ACTION_STATE_READINESS_CONFIRMED",
        "datos permitidos/prohibidos por pantalla",
        "acciones solo con contrato explicito",
        "estados siempre traducidos segun superficie",
        "empty states obligatorios",
        "blocked states obligatorios",
        "no permission inference",
        "no false availability",
        "no false operation",
        "EXTRACTION_SAFETY_CONFIRMED",
        "no extraer seccion si deja sin contexto la consola raiz",
        "no esconder blocked/forbidden",
        "no separar evidence de contexto",
        "no convertir raw/detail en pantalla sin owner",
        "no convertir disclosure en pantalla sin Screen Contract",
        "no mover warning/error sin preservar limites",
        "no crear screen por densidad solamente",
        "no crear screen si el problema real es copy/density/components",
        "COMPONENT_READINESS_CONFIRMED",
        "componentes actuales son Panel Maestro first",
        "todo componente futuro debe declarar surface",
        "user-safe variant requerida para User Panel",
        "chips/status mantienen semantica segura",
        "cards de contrato pueden ser internal only",
        "raw-safe/detail no son user-safe",
        "request preview no es form",
        "evidence/logs no son live log",
        "blocked/forbidden no son CTA",
    ]

    for marker in required:
        assert marker in text


def test_checkpoint_confirms_scope_limits_backup_and_next_prompt():
    text = read(DOC)

    required = [
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_READINESS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "FUTURE_SCREENS_READINESS_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "Future screens todavia no existen",
        "User Panel todavia no existe",
        "Translation layer sigue conceptual only",
        "no endpoint nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no fetch nuevo no autorizado",
        "no runtime/execution/dispatch/controlled execution",
        "no librerias nuevas",
        "no dependencias nuevas",
        "no se toco `core/`",
        "no se toco `api.py`",
        "no se toco `domains/` operativo",
        "no se toco `tools/`",
        "no se tocaron modelos",
        "no se tocaron integraciones",
        "no se cambio contrato backend",
        NEXT_PROMPT,
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]

    for marker in required:
        assert marker in text


def test_active_ui_remains_ia_core_panel_maestro_without_new_runtime_or_future_screens():
    index = read(INDEX)
    widgets = read(WIDGETS)
    admin = read(ADMIN)
    interactions = read(INTERACTIONS)
    domains = read(DOMAINS)
    i18n = read(I18N)

    assert "IA_CORE" in index
    assert "Panel Maestro / operador interno" in index
    assert "no Panel Usuario final" in index
    assert "REQUEST CONTRACT PREVIEW" in index
    assert "No submit / no dispatch / no execution" in index
    assert "backend_internal_ui_payload.v1" in index
    assert "backend_internal_ui_request.v1" in index
    assert "allowed_actions" in index
    assert "forbidden_actions" in index
    assert "blocked_capabilities" in index
    assert "dispatch bloqueado" in i18n or "Dispatch bloqueado" in i18n

    for marker in ["SAAOP //", "Loteria //", "Tactical HUD //", "U-Score //"]:
        assert marker not in index

    for source in (index, widgets, admin, interactions, domains):
        assert "/api/debate/start" not in source
        assert "/api/dispatch" not in source
        assert "startDebate" not in source
        assert "runOrchestration" not in source

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "location.hash" not in interactions
    assert "hashchange" not in interactions
    assert "no dispatch desde UI" in admin


def test_readmes_reference_checkpoint_1_42_and_next_prompt_1_43():
    root = read(README)
    ui = read(UI_README)

    for text in (root, ui):
        assert "docs/UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_1_42.md" in text
        assert CURRENT_PROMPT in text
        assert "Readiness for Future Screens" in text
        assert "bloque" in text.lower() and "cerrado" in text.lower()
        assert "future screens no implementadas" in text or "Future screens no implementadas" in text
        assert "User Panel no implementado" in text
        assert "readiness gates" in text
        assert "Screen Contract Template" in text
        assert "Screen Candidate Matrix" in text
        assert "restore point" in text.lower()
        assert "GitHub" in text
        assert NEXT_PROMPT in text

    bt = chr(96)
    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root


def test_expected_verdicts_are_documented():
    text = read(DOC)

    verdicts = [
        "UI_UX_FUTURE_SCREENS_READINESS_CHECKPOINT_PASSED",
        "FUTURE_SCREENS_READINESS_BLOCK_CONFIRMED",
        "FUTURE_SCREEN_READINESS_GATES_CONFIRMED",
        "SCREEN_CONTRACT_TEMPLATE_CONFIRMED",
        "SCREEN_CANDIDATE_MATRIX_CONFIRMED",
        "NAVIGATION_READINESS_CONFIRMED",
        "DATA_ACTION_STATE_READINESS_CONFIRMED",
        "EXTRACTION_SAFETY_CONFIRMED",
        "COMPONENT_READINESS_CONFIRMED",
        "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
        "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
        "FUTURE_SCREENS_READINESS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "FUTURE_SCREENS_READINESS_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_READY",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]

    for verdict in verdicts:
        assert verdict in text