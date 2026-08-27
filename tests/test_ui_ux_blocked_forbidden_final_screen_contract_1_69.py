from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_1_69.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_DOCUMENTED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION",
    "BLOCKED_FORBIDDEN_DRAFT_CONVERTED_DOCUMENTALLY",
    "BLOCKED_FORBIDDEN_CONTRACT_FINALIZATION_RECORD_DEFINED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_IDENTITY_DEFINED",
    "BLOCKED_FORBIDDEN_SOURCE_CONTRACTS_DEFINED",
    "BLOCKED_FORBIDDEN_CAPABILITIES_POLICY_DEFINED",
    "BLOCKED_FORBIDDEN_ACTIONS_POLICY_DEFINED",
    "BLOCKED_FORBIDDEN_ALLOWED_EXPLANATORY_DATA_DEFINED",
    "BLOCKED_FORBIDDEN_FORBIDDEN_OPERATIONAL_DATA_DEFINED",
    "BLOCKED_FORBIDDEN_ALLOWED_LOCAL_READ_ONLY_CONTROLS_DEFINED",
    "BLOCKED_FORBIDDEN_FORBIDDEN_CONTROLS_DEFINED",
    "BLOCKED_FORBIDDEN_ALLOWED_STATES_DEFINED",
    "BLOCKED_FORBIDDEN_FORBIDDEN_STATES_DEFINED",
    "BLOCKED_FORBIDDEN_EVIDENCE_POLICY_DEFINED",
    "BLOCKED_FORBIDDEN_NAVIGATION_POLICY_DEFINED",
    "BLOCKED_FORBIDDEN_COMPONENT_POLICY_DEFINED",
    "BLOCKED_FORBIDDEN_GUARDRAIL_MAPPING_DEFINED",
    "BLOCKED_FORBIDDEN_NO_UNLOCK_NO_OVERRIDE_BOUNDARY_DEFINED",
    "BLOCKED_FORBIDDEN_USER_SAFE_INTERNAL_ONLY_BOUNDARY_DEFINED",
    "BLOCKED_FORBIDDEN_IMPLEMENTATION_BOUNDARY_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_SCREEN_CREATED_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "UI_READY_FOR_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT",
]

REQUIRED_SECTIONS = [
    "Contract Finalization Record",
    "Final Screen Contract Identity",
    "Purpose",
    "Source Contracts",
    "Blocked Capabilities Policy",
    "Forbidden Actions Policy",
    "Allowed Explanatory Data",
    "Forbidden Operational Data",
    "Allowed Local / Read-Only Controls",
    "Forbidden Controls",
    "Allowed States",
    "Forbidden States",
    "Evidence Policy",
    "Navigation Policy",
    "Component Policy",
    "Guardrail Mapping",
    "No-Unlock / No-Override Boundary",
    "User-Safe / Internal-Only Boundary",
    "Contract Acceptance Criteria",
    "Risk Register",
    "Test Strategy",
    "Implementation Boundary",
    "Limites Para 1.70",
    "Riesgos Residuales",
]

DEFINITIONS = [
    "Blocked & Forbidden Final Screen Contract",
    "Final Screen Contract",
    "Blocked & Forbidden Screen",
    "Blocked Capability",
    "Forbidden Action",
    "No-Unlock Boundary",
    "Blocked/Forbidden Visibility Policy",
    "Safe Explanation Policy",
    "Final Contract Scope",
    "No-Implementation Boundary",
    "Panel Maestro Surface",
    "Read-Only Local Controls",
    "Forbidden Operational Controls",
    "Safe State Semantics",
    "Contract Evidence Policy",
    "Component Policy",
    "Contract Finalization Record",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Blocked & Forbidden Final Screen Contract 1.69",
        "94847522",
        "c0391f74",
        "1.68",
        "1.67",
        "1.66",
        "1.65",
        "1.61",
        "1.57",
        "BLOCKED_FORBIDDEN_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
        "bloque activo es `1.68 -> 1.70`",
        "segundo Final Screen Contract documental",
        "Contract Overview Final Screen Contract",
        "push pospuesto hasta checkpoint 1.70",
    ]
    for marker in markers:
        assert marker in text


def test_definitions_finalization_identity_and_purpose_are_documented():
    text = read(DOC)

    for marker in DEFINITIONS:
        assert marker in text

    finalization_markers = [
        "draft source",
        "`Blocked & Forbidden Capabilities Screen Draft`",
        "final contract target",
        "`Blocked & Forbidden Final Screen Contract`",
        "`FSC-BF-02`",
        "conversion type",
        "documental only",
        "implementation status",
        "not implemented",
        "UI active status",
        "unchanged",
        "route/endpoint/fetch status",
        "not created",
        "User Panel status",
        "not implemented",
        "unlock/override/bypass status",
        "not created",
        "runtime/execution status",
        "not enabled",
    ]
    for marker in finalization_markers:
        assert marker in text

    identity_markers = [
        "contract id",
        "contract name",
        "version",
        "status | `final-documental`",
        "surface | `Panel Maestro only`",
        "related readiness score",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "relationship with Contract Overview",
    ]
    for marker in identity_markers:
        assert marker in text

    assert "sin crear permisos nuevos" in text
    assert "sin accion operativa" in text or "No incluye accion operativa" in text


def test_policies_sections_guardrails_and_boundaries_are_complete():
    text = read(DOC)

    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text

    contract_markers = [
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
    ]
    for marker in contract_markers:
        assert marker in text

    policy_markers = [
        "no son acciones",
        "no son permisos pendientes",
        "no son features activables",
        "deben permanecer visibles",
        "no deben ocultarse",
        "no son CTAs",
        "no pueden mapearse a `allowed_actions`",
        "Allowed Explanatory Data",
        "Forbidden Operational Data",
        "Read-Only Controls",
        "Forbidden Controls",
        "Evidence Policy",
        "Navigation Policy",
        "Component Policy",
        "Guardrail Mapping",
        "No-Unlock / No-Override Boundary",
        "User-Safe / Internal-Only Boundary",
    ]
    for marker in policy_markers:
        assert marker in text


def test_states_risks_tests_and_no_scope_are_documented():
    text = read(DOC)

    allowed_states = [
        "final-documental",
        "final-documental-not-implemented",
        "not implemented",
        "read-only",
        "documented",
        "blocked",
        "forbidden",
        "unavailable",
        "not_available",
        "no_payload",
        "ready-no-permission",
        "no-runtime",
        "no-execution",
    ]
    for marker in allowed_states:
        assert marker in text

    forbidden_states = [
        "active",
        "running",
        "live",
        "operational",
        "executing",
        "dispatching",
        "submitted",
        "processing",
        "unlockable",
        "overridable",
        "pending permission",
        "escalation pending",
    ]
    for marker in forbidden_states:
        assert marker in text

    risks = [
        "final screen contract documental mistaken as screen",
        "blocked capability mistaken as unlockable feature",
        "forbidden action mistaken as disabled-but-available CTA",
        "endpoint/fetch leakage",
        "runtime/execution leakage",
        "User Panel leakage",
        "blocked/forbidden hidden",
        "legacy identity leakage",
        "external benchmark identity leakage",
    ]
    for marker in risks:
        assert marker in text

    no_scope = [
        "No pantalla creada",
        "No UI activa modificada",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
        "User Panel no creado y no implementado",
        "Sin endpoints/rutas/fetches",
        "Sin API/router nuevo",
        "No-runtime/no-execution",
        "No dispatch real",
        "No controlled execution",
        "No unlock/no override/no bypass/no permission escalation",
        "No dependencias nuevas",
        "Sin cambios CI",
        "Backend operativo untouched",
        "No se toco `core/`, `api.py`, `domains/`, `tools`, modelos ni integraciones",
        NEXT_PROMPT,
        "No avanzar a 1.70",
    ]
    for marker in no_scope:
        assert marker in text


def test_readmes_register_documentation_and_cursor():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )

    for text in (root, web):
        assert "Documentacion Blocked & Forbidden Final Screen Contract 1.69" in text
        assert "docs/UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_1_69.md" in text
        assert "Blocked & Forbidden Final Screen Contract" in text
        assert "segundo final screen contract documental" in text
        assert "Blocked & Forbidden Final Screen Contract creado" in text
        assert "draft convertido documentalmente" in text
        assert "no pantalla" in text
        assert "no UI activa" in text
        assert "User Panel no implementado" in text
        assert "sin endpoints" in text
        assert "sin rutas" in text
        assert "sin fetches" in text
        assert "sin dependencias" in text
        assert "no-runtime/no-execution" in text
        assert "no-unlock/no-override/no-bypass/no-permission-escalation" in text
        assert NEXT_PROMPT in text
        assert "push pospuesto" in text.lower()
        assert "c0391f74" in text


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
