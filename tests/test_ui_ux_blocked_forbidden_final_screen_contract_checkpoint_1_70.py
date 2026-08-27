from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_70.md"
CONTRACT_DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_1_69.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & "
    "Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT_CLOSED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_BLOCK_CLOSED",
    "PROMPT_1_67_PLAN_CONFIRMED",
    "PROMPT_1_68_AUDIT_CONFIRMED",
    "PROMPT_1_69_DOCUMENTATION_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_VERIFIED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION_CONFIRMED",
    "BLOCKED_FORBIDDEN_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "FINAL_DOCUMENTAL_NOT_UI_ACTIVE_CONFIRMED",
    "BLOCKED_FORBIDDEN_CONTRACT_FINALIZATION_RECORD_VERIFIED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_IDENTITY_VERIFIED",
    "BLOCKED_FORBIDDEN_SOURCE_CONTRACTS_VERIFIED",
    "BLOCKED_FORBIDDEN_CAPABILITIES_POLICY_VERIFIED",
    "BLOCKED_FORBIDDEN_ACTIONS_POLICY_VERIFIED",
    "BLOCKED_FORBIDDEN_ALLOWED_EXPLANATORY_DATA_VERIFIED",
    "BLOCKED_FORBIDDEN_FORBIDDEN_OPERATIONAL_DATA_VERIFIED",
    "BLOCKED_FORBIDDEN_ALLOWED_LOCAL_READ_ONLY_CONTROLS_VERIFIED",
    "BLOCKED_FORBIDDEN_FORBIDDEN_CONTROLS_VERIFIED",
    "BLOCKED_FORBIDDEN_ALLOWED_STATES_VERIFIED",
    "BLOCKED_FORBIDDEN_FORBIDDEN_STATES_VERIFIED",
    "BLOCKED_FORBIDDEN_EVIDENCE_POLICY_VERIFIED",
    "BLOCKED_FORBIDDEN_NAVIGATION_POLICY_VERIFIED",
    "BLOCKED_FORBIDDEN_COMPONENT_POLICY_VERIFIED",
    "BLOCKED_FORBIDDEN_GUARDRAIL_MAPPING_VERIFIED",
    "BLOCKED_FORBIDDEN_NO_UNLOCK_NO_OVERRIDE_BOUNDARY_VERIFIED",
    "BLOCKED_FORBIDDEN_USER_SAFE_INTERNAL_ONLY_BOUNDARY_VERIFIED",
    "BLOCKED_FORBIDDEN_IMPLEMENTATION_BOUNDARY_VERIFIED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_GITHUB_RESTORE_POINT_READY",
    "UI_READY_FOR_POST_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_NEXT_BLOCK_PLANNING",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Blocked & Forbidden Final Screen Contract Checkpoint 1.70",
        "ed7d6b80",
        "c0391f74",
        "1.67",
        "1.68",
        "1.69",
        "1.70",
        "Blocked & Forbidden Final Screen Contract",
        "Final Screen Contract",
        "segundo Final Screen Contract documental",
        "restore point GitHub",
    ]
    for marker in markers:
        assert marker in text


def test_final_screen_contract_fields_and_policies_are_verified():
    text = read(DOC)

    markers = [
        "final-documental",
        "not implemented",
        "Panel Maestro only",
        "Contract Finalization Record",
        "Final Screen Contract Identity",
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
        "No-Implementation Boundary",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_identity_and_backend_boundaries_are_confirmed():
    text = read(DOC)

    markers = [
        "Pantalla `Blocked & Forbidden` no creada",
        "UI activa no modificada",
        "User Panel no implementado",
        "Sin endpoints nuevos",
        "Sin API/router nuevo",
        "Sin rutas nuevas ni hash routing operativo",
        "Sin fetches nuevos",
        "Sin dependencias nuevas",
        "Sin cambios CI",
        "Sin runtime",
        "Sin execution",
        "Sin dispatch real",
        "Sin controlled execution",
        "Sin unlock",
        "Sin override",
        "Sin bypass",
        "Sin permission escalation",
        "Backend operativo untouched",
        "no se toco `core/`, `api.py`, `domains/` operativo, `tools/`, modelos ni integraciones",
        "IA_CORE sigue como identidad activa",
        "SAAOP, Loteria, Tactical HUD y U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_contractual_base_and_blocked_forbidden_semantics_are_preserved():
    text = read(DOC)

    markers = [
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
        "`blocked_capabilities` se tratan como limites",
        "`forbidden_actions` se tratan como prohibiciones",
        "no features desbloqueables",
        "no CTAs deshabilitados disponibles",
    ]
    for marker in markers:
        assert marker in text


def test_checkpoint_references_deliverables_validations_restore_and_next_prompt():
    text = read(DOC)

    markers = [
        "Documento 1.67",
        "Documento 1.68",
        "Documento 1.69",
        "Tests 1.67",
        "Tests 1.68",
        "Tests 1.69",
        "README raiz",
        "README UI",
        "git status --short",
        "git rev-parse --short HEAD",
        "git branch --show-current",
        "git remote -v",
        "git fetch origin",
        "node --check ui/web/backend-contract-widgets.js",
        "node --check ui/web/admin-panels.js",
        "node --check ui/web/console-interactions.js",
        "git diff --check",
        "git push origin main",
        NEXT_PROMPT,
        "No avanzar a 1.71 desde este checkpoint",
    ]
    for marker in markers:
        assert marker in text


def test_readmes_point_to_1_71_and_reference_checkpoint():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        (f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or (f"Next pending step: {bt}PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root or f"Next pending step: {bt}PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root)
    )
    assert NEXT_PROMPT in web
    assert "docs/UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_70.md" in root
    assert "docs/UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_70.md" in web
    assert "segundo Final Screen Contract documental" in root
    assert "segundo final screen contract documental" in web
    assert "restore point remoto actualizado" in root
    assert "restore point GitHub" in web


def test_verdicts_are_documented_and_contract_doc_still_declares_boundary():
    text = read(DOC)
    contract = read(CONTRACT_DOC)

    for verdict in VERDICTS:
        assert verdict in text

    markers = [
        "Blocked & Forbidden Final Screen Contract",
        "final-documental",
        "not implemented",
        "No-Implementation Boundary",
        "No-Unlock / No-Override Boundary",
        "push pospuesto hasta checkpoint 1.70",
    ]
    for marker in markers:
        assert marker in contract
