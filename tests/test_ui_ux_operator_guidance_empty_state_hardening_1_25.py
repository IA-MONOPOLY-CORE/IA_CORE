from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_1_25.md"
AUDIT_124 = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def active_ui_text() -> str:
    return "\n".join(read(path) for path in [INDEX, WIDGETS, ADMIN])


def test_hardening_1_25_document_exists_and_references_base_chain():
    text = read(DOC)

    for marker in [
        "c15bc493",
        "docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md",
        "criterio de lenguaje dual registrado en 1.24.1",
        "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_COMPLETED",
        "PROMPT UI/UX 1.26 - Checkpoint Operator Guidance / Empty-State Intelligence IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text

    assert AUDIT_124.exists()
    assert "DUAL_LANGUAGE_GUIDANCE_CRITERION_RECORDED" in read(AUDIT_124)


def test_active_ui_contains_guidance_for_p1_states():
    text = active_ui_text()

    for marker in [
        "No disponible en este estado (not_available)",
        "Pendiente de información (pending)",
        "Pendiente / todavía no disponible (planned)",
        "Todavía no hay información cargada (no_payload)",
        "Bloqueado por seguridad (blocked)",
        "Solo lectura (read-only)",
        "no implica error",
        "no significa ejecución en curso",
        "la UI no inventa datos",
        "ausencia de lista no desbloquea",
    ]:
        assert marker in text


def test_active_ui_distinguishes_forbidden_and_blocked_empty_states():
    text = active_ui_text()

    for marker in [
        "lista vacía declarada",
        "dato no informado",
        "ausencia de dato no significa permiso UI",
        "ausencia de prohibiciones visibles no significa permiso UI",
        "allowed_actions declarado vacío",
        "blocked_capabilities no informado",
        "blocked sin lista disponible",
        "Lista sin bloqueos true declarados",
        "Acciones disponibles declaradas por el sistema (allowed_actions)",
        "Acciones no permitidas (forbidden_actions)",
        "Funciones bloqueadas (blocked_capabilities)",
    ]:
        assert marker in text


def test_request_draft_and_next_step_remain_non_operational():
    text = active_ui_text()

    for marker in [
        "REQUEST CONTRACT DRAFT",
        "Solo lectura (read-only): draft local; no submit, no dispatch, no execution",
        "backend_internal_ui_request.v1 aceptado",
        "allowed_actions declarado",
        "blocked_capabilities sin bloqueo",
        "Hoy no envía nada",
        "operator guidance checkpoint planned",
        "continuidad documental hacia checkpoint 1.26",
        "no es workflow activo",
        "no es workflow activo ni botón",
    ]:
        assert marker in text

    assert "request-contract-readonly-control" in text
    assert "disabled" in text


def test_internal_exposure_and_raw_safe_use_dual_language():
    text = active_ui_text()

    for marker in [
        "Panel Maestro read-only",
        "Información recibida (payload)",
        "Vista segura de datos (raw-safe)",
        "Validación del sistema (validation)",
        "Registro interno de exposición (registry)",
        "Adaptador de respuesta (response adapter)",
        "Despachador sin ejecución real (dispatcher no-runtime)",
        "sin secretos",
        "sin env",
        "sin payload externo crudo",
        "sin edición",
    ]:
        assert marker in text


def test_document_records_user_panel_future_and_limits():
    text = read(DOC)

    for marker in [
        "Panel Usuario no se implementa en 1.25",
        "futura experiencia final debe usar lenguaje simple",
        "no ocultar bloqueos",
        "no inventar permisos",
        "GUIDANCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "GUIDANCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "IA_CORE como identidad activa",
        "no SAAOP/Loteria/Tactical HUD como UI activa",
    ]:
        assert marker in text


def test_active_ui_does_not_add_forbidden_endpoints_or_active_ctas():
    text = active_ui_text()

    for forbidden in [
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
        "hashchange",
        "history.pushState",
        "history.replaceState",
        "START</button>",
        "RUN</button>",
        "EXECUTE</button>",
        "DISPATCH</button>",
        "LAUNCH</button>",
    ]:
        assert forbidden not in text

    assert "fetch(" not in read(WIDGETS)
    assert "fetch(" not in read(ROOT / "ui" / "web" / "console-interactions.js")


def test_readmes_record_hardening_1_25_continuity():
    root = read(README)
    ui = read(UI_README)
    next_prompt = "PROMPT UI/UX 1.26 - Checkpoint Operator Guidance / Empty-State Intelligence IA_CORE contract-aware sin runtime/no-execution"

    for text in [root, ui]:
        assert "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_1_25.md" in text
        assert "1.25" in text
        assert "guidance" in text.lower()
        assert "empty states" in text.lower() or "empty-state" in text.lower()
        assert next_prompt in text
        assert "no-runtime/no-execution" in text or "no runtime" in text.lower()


def test_hardening_1_25_verdicts_are_recorded():
    text = read(DOC)

    for verdict in [
        "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_COMPLETED",
        "OPERATOR_GUIDANCE_P1_GAPS_HARDENED",
        "EMPTY_STATE_INTELLIGENCE_HARDENED",
        "DUAL_LANGUAGE_GUIDANCE_APPLIED",
        "MASTER_PANEL_CLEAR_LANGUAGE_WITH_TECHNICAL_TERMS_CONFIRMED",
        "USER_PANEL_SIMPLE_LANGUAGE_RECORDED_FOR_FUTURE",
        "GUIDANCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "GUIDANCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "UI_READY_FOR_OPERATOR_GUIDANCE_CHECKPOINT",
    ]:
        assert verdict in text