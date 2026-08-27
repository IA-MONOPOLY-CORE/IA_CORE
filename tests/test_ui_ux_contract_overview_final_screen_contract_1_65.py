from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_1_65.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CURRENT_AFTER_1_66 = (
    "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
    "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)
VERDICTS = [
    "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_DOCUMENTED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION",
    "CONTRACT_OVERVIEW_DRAFT_CONVERTED_DOCUMENTALLY",
    "CONTRACT_FINALIZATION_RECORD_DEFINED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_IDENTITY_DEFINED",
    "CONTRACT_OVERVIEW_SOURCE_CONTRACTS_DEFINED",
    "CONTRACT_OVERVIEW_ALLOWED_DATA_DEFINED",
    "CONTRACT_OVERVIEW_FORBIDDEN_DATA_DEFINED",
    "CONTRACT_OVERVIEW_ALLOWED_ACTIONS_DEFINED",
    "CONTRACT_OVERVIEW_FORBIDDEN_ACTIONS_DEFINED",
    "CONTRACT_OVERVIEW_ALLOWED_STATES_DEFINED",
    "CONTRACT_OVERVIEW_FORBIDDEN_STATES_DEFINED",
    "CONTRACT_OVERVIEW_EVIDENCE_POLICY_DEFINED",
    "CONTRACT_OVERVIEW_NAVIGATION_POLICY_DEFINED",
    "CONTRACT_OVERVIEW_COMPONENT_POLICY_DEFINED",
    "CONTRACT_OVERVIEW_GUARDRAIL_MAPPING_DEFINED",
    "CONTRACT_OVERVIEW_USER_SAFE_INTERNAL_ONLY_BOUNDARY_DEFINED",
    "CONTRACT_OVERVIEW_IMPLEMENTATION_BOUNDARY_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_NO_SCREEN_CREATED_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "UI_READY_FOR_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT",
]

SOURCE_CONTRACTS = [
    "backend_internal_ui_payload.v1",
    "backend_internal_ui_request.v1",
    "internal_exposure_registry",
    "internal_request_validation",
    "internal_dispatcher_no_runtime",
    "internal_confirmation_gate",
    "internal_response_adapter",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_final_contract_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Contract Overview Final Screen Contract 1.65",
        "a75f2d95",
        "5399f1f3",
        "docs/UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_AUDIT_1_64.md",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_63.md",
        "docs/UI_UX_FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_1_62.md",
        "docs/UI_UX_FINAL_SCREEN_CONTRACT_READINESS_1_61.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md",
        "CONTRACT_OVERVIEW_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
        "primer Final Screen Contract documental",
        "no es una pantalla implementada",
        "Push GitHub pospuesto por defecto hasta checkpoint 1.66",
    ]
    for marker in markers:
        assert marker in text


def test_definitions_finalization_record_and_identity_are_complete():
    text = read(DOC)

    markers = [
        "## Definiciones Formales",
        "Contract Overview Screen Draft",
        "Contract Overview Final Screen Contract",
        "Final Screen Contract documental",
        "Contract finalization record",
        "ready-no-permission",
        "summary/detail/raw-safe",
        "No-Implementation Boundary",
        "## Contract Finalization Record",
        "FSC-CO-01",
        "final-documental-not-implemented",
        "Draft convertido documentally; no convertido a UI activa",
        "## Final Screen Contract Identity",
        "Owner: `contract reader / payload contract reading`",
        "Surface: `Panel Maestro`",
        "User Panel requiere contrato futuro separado",
    ]
    for marker in markers:
        assert marker in text


def test_purpose_and_source_contracts_are_defined():
    text = read(DOC)

    assert "## Proposito" in text
    assert "entender el contrato backend/UI sin inferir permisos" in text
    assert "no incluye enviar requests" in text
    assert "## Source Contracts" in text
    for contract in SOURCE_CONTRACTS:
        assert contract in text

    assert "lectura solamente" in text
    assert "no submit, no dispatch" in text
    assert "no activa dispatcher" in text


def test_allowed_and_forbidden_data_surface_matrix_is_defined():
    text = read(DOC)

    markers = [
        "## Allowed Data",
        "| superficie | datos permitidos | presentacion permitida | limite |",
        "Panel Maestro",
        "Panel Maestro detail",
        "Panel Maestro raw-safe",
        "Shared safe future",
        "User Panel future",
        "schema_version",
        "service_kind",
        "status",
        "readiness",
        "validation",
        "warnings",
        "errors",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "## Forbidden Data",
        "Secrets, API keys, tokens, credentials",
        "Payload raw completo no sanitizado",
        "Runtime handles",
        "Datos de User Panel",
    ]
    for marker in markers:
        assert marker in text


def test_action_state_evidence_navigation_and_component_policies_are_defined():
    text = read(DOC)

    markers = [
        "## Allowed Actions",
        "Leer summary/detail/raw-safe",
        "Expandir o colapsar disclosure local",
        "Copiar una referencia textual segura solo como accion local",
        "## Forbidden Actions",
        "Submit, send, execute, run, dispatch",
        "Invocar modelos, herramientas, integraciones",
        "Convertir `allowed_actions` en permiso UI propio",
        "## Allowed States",
        "final-documental-not-implemented",
        "ready-no-permission",
        "no_payload",
        "not_available",
        "blocked",
        "forbidden",
        "## Forbidden States",
        "active",
        "running",
        "dispatching",
        "approved-for-execution",
        "## Evidence Policy",
        "Evidence se muestra como trazabilidad documental/sanitizada",
        "## Navigation Policy",
        "indice local, focus local, scroll local y disclosure local",
        "hash routing nuevo",
        "## Component Policy",
        "panels, detail panels, status badges, chips",
        "primary CTA operativo",
    ]
    for marker in markers:
        assert marker in text


def test_guardrails_boundaries_acceptance_risks_and_limits_are_defined():
    text = read(DOC)

    sections = [
        "## Guardrail Mapping",
        "## User-Safe / Internal-Only Boundary",
        "## Acceptance Criteria",
        "## Risk Register",
        "## Test Strategy",
        "## Implementation Boundary",
        "## Limites Para 1.66",
        "## Riesgos Residuales",
        "## Politica De Backup",
    ]
    for section in sections:
        assert section in text

    guardrails = [
        "Identity",
        "Surface",
        "Data",
        "Action",
        "State",
        "Evidence",
        "Navigation",
        "Component",
        "Extraction",
        "Endpoint/fetch",
        "Runtime",
        "Backup",
    ]
    for marker in guardrails:
        assert marker in text

    risks = [
        "final contract mistaken as screen",
        "final contract mistaken as implementation authorization",
        "route/hash leakage",
        "endpoint/fetch leakage",
        "CTA ghost",
        "runtime/execution leakage",
        "User Panel leakage",
        "state semantics leakage",
        "evidence/live-log confusion",
        "blocked/forbidden hidden",
        "legacy identity leakage",
        "external benchmark identity leakage",
    ]
    for marker in risks:
        assert marker in text


def test_no_scope_boundaries_next_prompt_and_verdicts_are_confirmed():
    text = read(DOC)

    no_scope = [
        "No se crea pantalla",
        "no debe implementar pantalla",
        "no debe crear User Panel",
        "no debe crear rutas",
        "no debe crear endpoints",
        "no debe agregar fetches",
        "no debe instalar dependencias",
        "no debe modificar CI",
        "no debe activar runtime/execution/dispatch/controlled execution",
        "No avanzar a 1.66 dentro de este bloque",
    ]
    for marker in no_scope:
        assert marker in text

    assert NEXT_PROMPT in text
    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_1_65_and_cursor_to_1_66():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )
    for text in (root, web):
        assert "documentado hasta 1.65" in text or "Documentacion Contract Overview Final Screen Contract 1.65" in text
        assert "docs/UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_1_65.md" in text
        assert "Contract Overview Final Screen Contract" in text
        assert "final screen contract documental" in text
        assert "no es pantalla implementada" in text or "no crea pantalla" in text
        assert "User Panel no implementado" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "no-runtime/no-execution" in text
        assert "push pospuesto" in text.lower()
        assert NEXT_PROMPT in text
