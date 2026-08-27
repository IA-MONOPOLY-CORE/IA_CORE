from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_AUDIT_1_68.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_AUDIT_COMPLETED",
    "POST_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_STATE_REVIEWED",
    "BLOCKED_FORBIDDEN_DRAFT_REVIEWED",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_ELIGIBILITY_REVIEWED",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_ACCEPTANCE_CRITERIA_DEFINED",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_RISK_REGISTER_DEFINED",
    "BLOCKED_FORBIDDEN_DRAFT_TO_FINAL_DECISION_DEFINED",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "BLOCKED_FORBIDDEN_DRAFT_NOT_CONVERTED_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_IN_1_68_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_AUDIT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "BLOCKED_FORBIDDEN_FINAL_CONTRACT_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "UI_READY_FOR_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_DOCUMENTATION",
]

CRITERIA = [
    "identity",
    "surface",
    "owner",
    "purpose",
    "source contract",
    "blocked capabilities",
    "forbidden actions",
    "data",
    "action",
    "state",
    "evidence",
    "navigation",
    "component",
    "guardrail",
    "user-safe",
    "test",
    "final contract eligibility",
    "no-implementation boundary",
]

RISKS = [
    "Final contract mistaken as screen",
    "Final contract mistaken as implementation authorization",
    "Blocked capability mistaken as unlockable feature",
    "Forbidden action mistaken as disabled-but-available CTA",
    "Route/hash leakage",
    "Endpoint/fetch leakage",
    "CTA ghost",
    "Unlock/override/bypass leakage",
    "Permission escalation leakage",
    "Runtime/execution leakage",
    "User Panel leakage",
    "State semantics leakage",
    "Evidence/live-log confusion",
    "Blocked/forbidden hidden",
    "Legacy identity leakage",
    "External benchmark identity leakage",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Blocked & Forbidden Final Screen Contract Audit 1.68",
        "99cf7a9d",
        "c0391f74",
        "1.67",
        "1.66",
        "1.65",
        "1.61",
        "1.57",
        "Blocked & Forbidden Capabilities Screen Draft",
        "Blocked & Forbidden Final Screen Contract",
        "no-operativa",
        "no crea pantalla",
        "no modifica UI activa",
        "no crea User Panel",
        "no crea endpoints",
        "no activa runtime/execution/dispatch/controlled execution",
    ]
    for marker in markers:
        assert marker in text


def test_definitions_criteria_acceptance_and_risks_are_complete():
    text = read(DOC)

    definitions = [
        "Final Contract Audit",
        "Draft-to-Final Decision",
        "Final Contract Eligibility",
        "Final Contract Blocker",
        "Final Contract Risk",
        "Blocked Capability",
        "Forbidden Action",
        "No-Unlock Boundary",
        "Blocked/Forbidden Visibility Policy",
        "Safe Explanation Policy",
        "Final Contract Acceptance Criteria",
        "Final Contract Scope",
        "No-Implementation Boundary",
    ]
    for marker in definitions:
        assert marker in text

    for criterion in CRITERIA:
        assert f"| {criterion} |" in text

    for risk in RISKS:
        assert risk in text

    acceptance_markers = [
        "scope definitivo",
        "Panel Maestro only",
        "source contracts",
        "blocked capabilities policy always-visible",
        "forbidden actions policy",
        "allowed explanatory data",
        "operational/internal data",
        "controles locales/read-only",
        "unlock, override, bypass",
        "allowed states",
        "prohibir estados",
        "evidence policy",
        "navigation policy",
        "component policy",
        "guardrails",
        "no-unlock/no-override/no-bypass boundary",
        "user-safe futuro",
        "no-implementation boundary",
        "tests documentales/static checks",
        "README cursor",
        "no UI activa, no endpoint, no runtime",
    ]
    for marker in acceptance_markers:
        assert marker in text


def test_findings_decision_and_no_scope_are_documented():
    text = read(DOC)

    findings = [
        "BF-P0-001",
        "BF-P1-001",
        "BF-P1-002",
        "BF-P1-003",
        "BF-P2-001",
        "BF-P2-002",
        "BF-P2-003",
        "BF-P2-004",
        "BF-P2-005",
        "BF-P3-001",
        "BF-P3-002",
    ]
    for finding in findings:
        assert finding in text

    no_scope = [
        "Decision: `BLOCKED_FORBIDDEN_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT`",
        "`Blocked & Forbidden Final Screen Contract` no creado",
        "`Blocked & Forbidden Capabilities Screen Draft` no convertido",
        "No se crean nuevos final screen contracts en 1.68",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
        "No endpoint/API/router/fetch nuevo",
        "No runtime/execution/dispatch/controlled execution",
        "No unlock/override/bypass/permission escalation",
        "No dependencias nuevas",
        "Sin cambios CI",
        "Backend operativo untouched",
        NEXT_PROMPT,
        "No avanzar a 1.69",
    ]
    for marker in no_scope:
        assert marker in text


def test_verdicts_and_contract_markers_are_present():
    text = read(DOC)

    contract_markers = [
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
    ]
    for marker in contract_markers:
        assert marker in text

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_audit_and_next_cursor():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root

    for text in (root, web):
        assert "Auditoria Blocked & Forbidden Final Screen Contract 1.68" in text
        assert "docs/UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_AUDIT_1_68.md" in text
        assert "BLOCKED_FORBIDDEN_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT" in text
        assert "Blocked & Forbidden Final Screen Contract no creado" in text
        assert "draft no convertido" in text
        assert "no UI activa" in text
        assert "User Panel no implementado" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "no-runtime/no-execution" in text
        assert "no-unlock/no-override/no-bypass" in text
        assert NEXT_PROMPT in text
        assert "push pospuesto" in text.lower()
        assert "c0391f74" in text
