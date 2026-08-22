from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md"
PLAN_123 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_23.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_1_24_document_exists_and_references_base_plan():
    text = read(DOC)

    for marker in [
        "b13b2f47",
        "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_COMPLETED",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_23.md",
        "Operator Guidance / Empty-State Intelligence",
        "1.24",
    ]:
        assert marker in text

    assert PLAN_123.exists()
    assert "UI_UX_NEXT_BLOCK_PLAN_1_23_DEFINED" in read(PLAN_123)


def test_audit_1_24_contains_required_audit_sections():
    text = read(DOC)

    for marker in [
        "Guidance Global",
        "Guidance Por Estados",
        "Empty States",
        "Request Draft Guidance",
        "Actions / Boundaries Guidance",
        "Internal Exposure Guidance",
        "Evidence / Next Step Guidance",
        "Raw-Safe / Detail Panels Guidance",
        "Navegacion / Foco / Responsive",
        "Microcopy / Tono",
        "Riesgo De Saturacion",
        "Tests / Cobertura",
        "Mapa De Guidance Gaps",
        "Matriz P0/P1/P2/P3",
        "Plan Recomendado Para 1.25",
    ]:
        assert marker in text


def test_audit_1_24_records_all_relevant_states():
    text = read(DOC)

    for state in [
        "`ready`",
        "`passed`",
        "`blocked`",
        "`planned`",
        "`pending`",
        "`invalid`",
        "`failed`",
        "`not_available`",
        "`no_payload`",
        "`contract_fixture`",
        "`read_only`",
        "`backend_only`",
        "`forbidden`",
        "`warning`",
        "`error`",
    ]:
        assert state in text

    assert "Recomendacion 1.25" in text


def test_audit_1_24_records_empty_state_intelligence_gaps():
    text = read(DOC)

    for marker in [
        "EMPTY_STATE_INTELLIGENCE_GAPS_IDENTIFIED",
        "no payload",
        "no warnings",
        "no errors",
        "no forbidden actions",
        "no blocked capabilities",
        "not_available",
        "pending",
        "planned",
        "empty arrays",
        "ausencia de service signals",
        "ausencia de read model",
        "ausencia de request draft",
        "ausencia de evidence",
        "ausencia de next step",
        "causa",
        "consecuencia",
        "limite",
        "Proximo paso sugerido",
    ]:
        assert marker in text


def test_audit_1_24_records_priority_findings_and_no_p0():
    text = read(DOC)

    for marker in [
        "P0 | Ningun hallazgo P0",
        "P1 | Estados `not_available`, `pending`, `planned`, `no_payload`",
        "P1 | `forbidden_actions vacio o no informado`",
        "P1 | Next Step planned contiene narrativa historica 1.18",
        "P2 | Admin `Sin datos`, `Error`, `Cargando...`",
        "P2 | Request draft explica bloqueo",
        "P3 | Mezcla espanol/ingles tecnica",
    ]:
        assert marker in text


def test_audit_1_24_preserves_contractual_boundaries():
    text = read(DOC)

    for marker in [
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "summary/detail/raw-safe",
        "paneles de detalle 1.7",
        "navegacion interna 1.8",
        "sistema de componentes 1.9",
    ]:
        assert marker in text


def test_audit_1_24_does_not_recommend_runtime_endpoints_or_dependencies():
    text = read(DOC).lower()

    for forbidden in [
        "activar runtime",
        "habilitar execution",
        "crear endpoints",
        "instalar dependencias",
        "crear rutas",
        "crear pantallas nuevas",
        "usar referencias externas como fuente operativa",
    ]:
        assert forbidden not in text.replace("no " + forbidden, "")

    for marker in [
        "guidance_no_runtime_no_execution_confirmed",
        "guidance_no_endpoints_no_dependencies_confirmed",
        "no endpoint publico, api ni router http",
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
    ]:
        assert marker in text


def test_audit_1_24_confirms_identity_and_no_legacy_visual_active():
    text = read(DOC)

    for marker in [
        "IA_CORE como identidad visual activa",
        "ausencia de SAAOP",
        "Loteria",
        "Tactical HUD",
        "como UI activa",
    ]:
        assert marker in text


def test_audit_1_24_next_prompt_and_readmes_are_recorded():
    text = read(DOC)
    root = read(README)
    ui = read(UI_README)

    next_prompt = (
        "PROMPT UI/UX 1.25 - Endurecer guidance y empty states de operador "
        "IA_CORE contract-aware sin runtime/no-execution"
    )

    assert next_prompt in text
    for readme in [root, ui]:
        assert "docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md" in readme
        assert next_prompt in readme
        assert "no-runtime/no-execution" in readme or "no runtime" in readme.lower()
        assert "sin endpoints" in readme.lower() or "no new public endpoints" in readme.lower()


def test_audit_1_24_verdicts_are_recorded():
    text = read(DOC)

    for verdict in [
        "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_COMPLETED",
        "OPERATOR_GUIDANCE_GAPS_IDENTIFIED",
        "EMPTY_STATE_INTELLIGENCE_GAPS_IDENTIFIED",
        "GUIDANCE_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "GUIDANCE_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "UI_READY_FOR_OPERATOR_GUIDANCE_HARDENING",
    ]:
        assert verdict in text

def test_audit_1_24_records_dual_language_guidance_criterion():
    text = read(DOC)

    for marker in [
        "Criterio de lenguaje dual",
        "Panel Maestro",
        "Panel Usuario",
        "Información recibida (payload)",
        "Todavía no hay información cargada (no_payload)",
        "Pendiente / todavía no disponible (planned)",
        "Bloqueado por seguridad (blocked)",
        "Solo lectura (read-only)",
        "Acciones disponibles declaradas por el sistema (allowed_actions)",
        "Acciones no permitidas (forbidden_actions)",
        "Funciones bloqueadas (blocked_capabilities)",
        "El Panel Maestro puede enseñar el término técnico",
        "El Panel Usuario debe ocultar la complejidad técnica",
        "no inventar permisos",
        "no ocultar bloqueos",
        "sin runtime",
        "sin execution",
        "PROMPT UI/UX 1.25 - Endurecer guidance y empty states de operador IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text

    for verdict in [
        "DUAL_LANGUAGE_GUIDANCE_CRITERION_RECORDED",
        "MASTER_PANEL_TECHNICAL_TERMS_CAN_BE_TAUGHT_WITH_PARENTHESES",
        "USER_PANEL_TECHNICAL_JARGON_MUST_BE_TRANSLATED",
    ]:
        assert verdict in text