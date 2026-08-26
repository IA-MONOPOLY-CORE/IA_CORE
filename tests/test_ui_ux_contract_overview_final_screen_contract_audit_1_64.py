from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_AUDIT_1_64.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_AUDIT_COMPLETED",
    "POST_FINAL_SCREEN_CONTRACT_READINESS_STATE_REVIEWED",
    "CONTRACT_OVERVIEW_DRAFT_REVIEWED",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_ELIGIBILITY_REVIEWED",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_ACCEPTANCE_CRITERIA_DEFINED",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_RISK_REGISTER_DEFINED",
    "CONTRACT_OVERVIEW_DRAFT_TO_FINAL_DECISION_DEFINED",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "CONTRACT_OVERVIEW_DRAFT_NOT_CONVERTED_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_AUDIT_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "CONTRACT_OVERVIEW_FINAL_CONTRACT_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "UI_READY_FOR_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_DOCUMENTATION",
]

AUDIT_CRITERIA = [
    "identity readiness",
    "surface readiness",
    "owner readiness",
    "purpose readiness",
    "source contract readiness",
    "data readiness",
    "action readiness",
    "state readiness",
    "evidence readiness",
    "navigation readiness",
    "component readiness",
    "guardrail readiness",
    "user-safe readiness",
    "test readiness",
    "final contract eligibility",
    "no-implementation boundary",
]

RISK_MARKERS = [
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

CONTRACT_MARKERS = [
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_has_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Contract Overview Final Screen Contract Audit 1.64",
        "2269c37e",
        "5399f1f3",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_63.md",
        "docs/UI_UX_FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT_1_62.md",
        "docs/UI_UX_FINAL_SCREEN_CONTRACT_READINESS_1_61.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md",
        "1.64 auditoria",
        "1.65 documentacion/hardening",
        "1.66 checkpoint",
        "Candidato unico auditado: `Contract Overview Screen Draft`",
    ]
    for marker in markers:
        assert marker in text


def test_definitions_and_contract_markers_are_present():
    text = read(DOC)

    definitions = [
        "Contract Overview Screen Draft",
        "Contract Overview Final Screen Contract",
        "Final Contract Audit",
        "Draft-to-Final Decision",
        "Final Contract Eligibility",
        "Final Contract Blocker",
        "Final Contract Risk",
        "Final Contract Acceptance Criteria",
        "Final Contract Scope",
        "No-Implementation Boundary",
    ]
    for marker in definitions + CONTRACT_MARKERS:
        assert marker in text


def test_post_1_63_state_and_candidate_score_are_confirmed():
    text = read(DOC)

    markers = [
        "Bloque seleccionado: `Contract Overview Final Screen Contract Audit`",
        "Score previo: `READY_FOR_FINAL_CONTRACT_AUDIT_NEXT`",
        "Orden previo: 1",
        "Contract Overview score previo: `READY_FOR_FINAL_CONTRACT_AUDIT_NEXT`",
        "Final screen contracts no creados",
        "Draft contracts no convertidos",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "No endpoints, no rutas, no fetches, no dependencias, no cambios CI",
        "No-runtime/no-execution",
    ]
    for marker in markers:
        assert marker in text


def test_audit_covers_all_required_criteria():
    text = read(DOC)

    assert "## Auditoria Por Criterios" in text
    for criterion in AUDIT_CRITERIA:
        assert criterion in text

    assert "identity alta" not in text.lower() or "IA_CORE" in text
    assert "Panel Maestro" in text
    assert "Shared safe future" in text or "Shared safe futuro" in text
    assert "User Panel not implemented" in text or "User Panel no implementado" in text


def test_acceptance_criteria_and_risk_register_are_complete():
    text = read(DOC)

    assert "## Final Contract Acceptance Criteria" in text
    acceptance = [
        "Scope definitivo",
        "Surface definitivo",
        "Owner definitivo",
        "Source contracts definitivos",
        "Allowed data definitivo",
        "Forbidden data definitivo",
        "Allowed actions definitivo",
        "Forbidden actions definitivo",
        "Allowed states definitivo",
        "Forbidden states definitivo",
        "Evidence policy definitiva",
        "Navigation policy definitiva",
        "Component policy definitiva",
        "Guardrails definitivos",
        "User-safe/internal-only definitivo",
        "No-Implementation Boundary",
        "Tests documentales",
        "Static checks contextuales",
        "README cursor",
        "No UI active change",
    ]
    for marker in acceptance:
        assert marker in text

    assert "## Final Contract Risk Register" in text
    for marker in RISK_MARKERS:
        assert marker in text


def test_findings_include_p0_p1_p2_p3_with_required_columns():
    text = read(DOC)

    assert "## Hallazgos P0/P1/P2/P3" in text
    columns = [
        "| id | criterio | severidad | descripcion | riesgo | recomendacion | tipo | falso positivo |",
        "| CO-P0-001 |",
        "| CO-P1-001 |",
        "| CO-P1-002 |",
        "| CO-P1-003 |",
        "| CO-P2-001 |",
        "| CO-P2-002 |",
        "| CO-P2-003 |",
        "| CO-P2-004 |",
        "| CO-P2-005 |",
        "| CO-P3-001 |",
        "| CO-P3-002 |",
    ]
    for marker in columns:
        assert marker in text

    for severity in ["| P0 |", "| P1 |", "| P2 |", "| P3 |"]:
        assert severity in text


def test_draft_to_final_decision_and_1_65_recommendation_are_explicit():
    text = read(DOC)

    markers = [
        "Decision: `CONTRACT_OVERVIEW_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT`",
        "No se detectan blockers P0 abiertos",
        "data surface matrix",
        "ready-no-permission",
        "user-safe/internal-only split",
        "## Recommended 1.65 Intervention",
        "1.65 deberia documentar `Contract Overview Final Screen Contract`",
        "marcarlo como final screen contract documental",
        "confirmar que no es pantalla implementada",
        "## Limites Para 1.65",
        "Documentation/hardening only",
        "No UI active change",
        "No Contract Overview implemented screen",
        "No User Panel",
        "No endpoints",
        "No runtime/execution",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_identity_legacy_and_next_prompt_are_confirmed():
    text = read(DOC)

    markers = [
        "Contract Overview Final Screen Contract no creado todavia",
        "Contract Overview Draft no convertido todavia",
        "Final screen contracts no creados",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "IA_CORE como identidad activa",
        "Sin SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
        "Sin endpoint/API/router/fetch nuevo",
        "Sin runtime/execution/dispatch/controlled execution",
        "Sin dependencias nuevas",
        "Sin cambios CI",
        "No se toco `core/`, `api.py`, `domains/`, `tools`, modelos ni integraciones",
        NEXT_PROMPT,
        "No avanzar a 1.65",
    ]
    for marker in markers:
        assert marker in text

    assert "CONTRACT_OVERVIEW_FINAL_CONTRACT_DOCUMENTATION_BLOCKED" not in text


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_1_64_and_cursor_1_65():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root

    for text in (root, web):
        assert "1.64" in text
        assert "Contract Overview Final Screen Contract Audit" in text
        assert "Contract Overview Screen Draft" in text
        assert "CONTRACT_OVERVIEW_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT" in text
        assert "final screen contract no creado" in text.lower()
        assert "draft no convertido" in text.lower()
        assert "User Panel no implementado" in text
        assert "UI activa no modificada" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "no-runtime/no-execution" in text
        assert "push pospuesto" in text.lower()
        assert "5399f1f3" in text
        assert NEXT_PROMPT in text