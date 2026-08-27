from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_1_61.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CANDIDATES = [
    "Contract Overview Screen Draft",
    "Blocked & Forbidden Capabilities Screen Draft",
    "Validation & Readiness Screen Draft",
    "Request Contract Preview Screen Draft",
]

SCORES = [
    "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
    "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
    "DEFER_FINALIZATION",
]

DEFINITIONS = [
    "Final Screen Contract Readiness",
    "Final Screen Contract",
    "Readiness Documentation",
    "Finalization Candidate",
    "Finalization Gate",
    "Readiness Gap",
    "Readiness Risk",
    "Readiness Score",
    "Finalization Order",
    "No-Finalization Boundary",
    "Readiness Acceptance Criteria",
    "Readiness Evidence",
]

VERDICTS = [
    "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_DOCUMENTED",
    "FINAL_SCREEN_CONTRACT_READINESS_FORMALIZED",
    "READINESS_ACCEPTANCE_CRITERIA_DEFINED",
    "READINESS_MATRIX_FORMALIZED",
    "CONTRACT_OVERVIEW_READINESS_FORMALIZED",
    "BLOCKED_FORBIDDEN_READINESS_FORMALIZED",
    "VALIDATION_READINESS_FORMALIZED",
    "REQUEST_CONTRACT_PREVIEW_READINESS_DEFERRED",
    "READINESS_GAPS_REGISTER_FORMALIZED",
    "READINESS_RISK_REGISTER_FORMALIZED",
    "FINALIZATION_GATES_FORMALIZED",
    "FINALIZATION_ORDER_FORMALIZED",
    "NO_FINALIZATION_BOUNDARY_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "DRAFT_CONTRACTS_NOT_CONVERTED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "UI_READY_FOR_FINAL_SCREEN_CONTRACT_READINESS_CHECKPOINT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Final Screen Contract Readiness 1.61",
        "06aeac21",
        "ec8975b7",
        "docs/UI_UX_FINAL_SCREEN_CONTRACT_READINESS_AUDIT_1_60.md",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_59.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_CHECKPOINT_1_58.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md",
        "1.60 -> 1.62",
        "Push pospuesto hasta 1.62",
    ]
    for marker in markers:
        assert marker in text


def test_definitions_and_contractual_base_are_preserved():
    text = read(DOC)

    for definition in DEFINITIONS:
        assert definition in text

    contractual_markers = [
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
    for marker in contractual_markers:
        assert marker in text


def test_readiness_acceptance_criteria_matrix_and_candidates_are_documented():
    text = read(DOC)

    for marker in [
        "Readiness Acceptance Criteria",
        "Readiness Matrix Formal",
        "identity",
        "surface",
        "data",
        "action",
        "state",
        "evidence",
        "navigation",
        "component",
        "guardrail",
        "user-safe",
        "test",
        "finalization",
        "gaps",
        "risks",
        "recommendation",
    ]:
        assert marker in text

    for candidate in CANDIDATES:
        assert candidate in text
    for score in SCORES:
        assert score in text


def test_each_candidate_has_readiness_gates_evidence_and_recommendation():
    text = read(DOC)

    candidate_sections = [
        ("Contract Overview Screen Draft", "order: 1", "CONTRACT_OVERVIEW_READINESS_FORMALIZED"),
        (
            "Blocked & Forbidden Capabilities Screen Draft",
            "order: 2",
            "BLOCKED_FORBIDDEN_READINESS_FORMALIZED",
        ),
        ("Validation & Readiness Screen Draft", "order: 3", "VALIDATION_READINESS_FORMALIZED"),
        (
            "Request Contract Preview Screen Draft",
            "order: 4",
            "REQUEST_CONTRACT_PREVIEW_READINESS_DEFERRED",
        ),
    ]
    for candidate, order, verdict in candidate_sections:
        assert f"### {candidate}" in text
        assert order in text
        assert "readiness criteria status:" in text
        assert "finalization gates:" in text
        assert "acceptance criteria:" in text
        assert "evidence:" in text
        assert "recommendation:" in text
        assert verdict in text

    assert "minor gaps:" in text
    assert "defer reasons:" in text


def test_gaps_risks_gates_order_strategy_and_limits_are_documented():
    text = read(DOC)

    markers = [
        "Readiness Gaps Register",
        "gap id",
        "candidate",
        "criterion",
        "severity",
        "description",
        "impact on finalization",
        "recommended resolution",
        "can be automated",
        "false positive risk",
        "Readiness Risk Register",
        "draft-to-final confusion",
        "premature finalization",
        "UI implementation leakage",
        "route/hash leakage",
        "endpoint/fetch leakage",
        "CTA ghost",
        "runtime/execution leakage",
        "User Panel leakage",
        "state semantics leakage",
        "evidence/live-log confusion",
        "hidden blocked/forbidden",
        "request preview submit confusion",
        "Finalization Gates Formal",
        "required docs",
        "required tests",
        "required human review",
        "required no-scope confirmations",
        "finalization decision",
        "Finalization Order Formal",
        "Test Strategy",
        "Implementation Boundary",
        "Limites Para 1.62",
        "Riesgos Residuales",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_identity_and_next_prompt_are_confirmed():
    text = read(DOC)

    markers = [
        "Final screen contracts no creados",
        "Draft contracts no convertidos",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "Sin endpoints/dependencias/runtime",
        "IA_CORE como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no UI activa",
        "no endpoint/API/router/fetch nuevo",
        "no runtime, no execution, no dispatch y no controlled execution",
        "no instala dependencias",
        "no modifica CI",
        NEXT_PROMPT,
        "No avanzar a 1.62",
    ]
    for marker in markers:
        assert marker in text


def test_expected_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_1_61_and_cursor_1_62():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    current_after_1_62 = (
        "PROMPT UI/UX 1.63 - Consolidar siguiente bloque UI/UX post "
        "Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_63 = (
        "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_64 = (
        "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_65 = (
        "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_66 = (
        "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
        "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )

    for text in (root, web):
        assert "1.61" in text
        assert "Final Screen Contract Readiness" in text
        assert "readiness scores" in text.lower()
        assert "finalization order" in text.lower()
        assert "final screen contracts no creados" in text.lower()
        assert "draft contracts no convertidos" in text.lower()
        assert NEXT_PROMPT in text or current_after_1_63 in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "User Panel no implementado" in text
