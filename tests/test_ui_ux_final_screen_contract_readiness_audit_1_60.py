from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_AUDIT_1_60.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.61 - Documentar Final Screen Contract Readiness "
    "IA_CORE contract-aware sin runtime/no-execution"
)

CANDIDATES = [
    "Contract Overview Screen Draft",
    "Validation & Readiness Screen Draft",
    "Blocked & Forbidden Capabilities Screen Draft",
    "Request Contract Preview Screen Draft",
]

DEFINITIONS = [
    "Final Screen Contract Readiness",
    "Final Screen Contract",
    "Readiness Audit",
    "Finalization Candidate",
    "Finalization Gate",
    "Readiness Gap",
    "Readiness Risk",
    "Readiness Score",
    "Finalization Order",
    "No-Finalization Boundary",
]

CRITERIA = [
    "identity readiness",
    "surface readiness",
    "data readiness",
    "action readiness",
    "state readiness",
    "evidence readiness",
    "navigation readiness",
    "component readiness",
    "guardrail readiness",
    "user-safe readiness",
    "test readiness",
    "finalization readiness",
]

VERDICTS = [
    "UI_UX_FINAL_SCREEN_CONTRACT_READINESS_AUDIT_COMPLETED",
    "POST_CONTRACT_FIRST_DRAFTS_STATE_REVIEWED",
    "FINAL_SCREEN_CONTRACT_READINESS_REVIEWED",
    "PRIORITY_1_DRAFTS_READINESS_AUDITED",
    "CONTRACT_OVERVIEW_READINESS_AUDITED",
    "VALIDATION_READINESS_READINESS_AUDITED",
    "BLOCKED_FORBIDDEN_READINESS_AUDITED",
    "REQUEST_CONTRACT_PREVIEW_READINESS_AUDITED",
    "READINESS_CRITERIA_DEFINED",
    "READINESS_MATRIX_DEFINED",
    "READINESS_RISK_REGISTER_DEFINED",
    "READINESS_SCORE_ASSIGNED",
    "FINALIZATION_ORDER_PROPOSED",
    "NO_FINALIZATION_BOUNDARY_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "DRAFT_CONTRACTS_NOT_CONVERTED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "FINAL_SCREEN_CONTRACT_READINESS_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "UI_READY_FOR_FINAL_SCREEN_CONTRACT_READINESS_DOCUMENTATION",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Final Screen Contract Readiness Audit 1.60",
        "4cd4ac8c",
        "ec8975b7",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_59.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_CHECKPOINT_1_58.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md",
        "1.60 -> 1.62",
        "no-runtime/no-execution",
        "sin endpoints/dependencias",
        "sin UI activa modificada",
        "sin User Panel",
        "sin final screen contracts creados",
    ]
    for marker in markers:
        assert marker in text


def test_definitions_candidates_and_criteria_are_present():
    text = read(DOC)

    for definition in DEFINITIONS:
        assert definition in text
    for candidate in CANDIDATES:
        assert candidate in text
    for criterion in CRITERIA:
        assert criterion in text

    assert "Readiness Criteria" in text
    assert "Auditoria Por Candidato" in text


def test_each_candidate_has_score_order_gaps_risks_and_recommendation():
    text = read(DOC)

    expected_scores = [
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "DEFER_FINALIZATION",
    ]
    for score in expected_scores:
        assert score in text

    for marker in [
        "Score:",
        "Finalization order:",
        "Gaps:",
        "Risks:",
        "Recommendation for 1.61:",
    ]:
        assert text.count(marker) >= 4


def test_readiness_matrix_and_risk_register_are_complete():
    text = read(DOC)

    assert "Readiness Matrix" in text
    assert "Readiness Risk Register" in text

    risk_markers = [
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
    ]
    for marker in risk_markers:
        assert marker in text

    for severity in ["P0", "P1", "P2", "P3"]:
        assert severity in text


def test_finalization_order_recommendation_and_limits_are_documented():
    text = read(DOC)

    markers = [
        "Finalization Order",
        "Orden tentativo no-operativo",
        "No convertir",
        "No-Finalization Boundary",
        "Recommended 1.61 Intervention",
        "1.61 deberia documentar Final Screen Contract Readiness formalmente",
        "Limites Para 1.61",
        "Documentation/hardening only",
        "No final screen contracts",
        "No draft conversion",
        "No UI active change",
        "No User Panel",
        "No endpoints",
        "No runtime/execution/dispatch/controlled execution",
        NEXT_PROMPT,
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
        "IA_CORE como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
        "No endpoint/API/router/fetch nuevo",
        "No runtime/execution/dispatch/controlled execution",
        "No dependencias nuevas",
        "Sin cambios CI",
        "No se toco `core/`, `api.py`, `domains/` operativo, `tools`, modelos ni integraciones",
        "No avanzar a 1.61",
    ]
    for marker in markers:
        assert marker in text


def test_expected_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_audit_and_cursor():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    current_after_1_61 = (
        "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
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
        or f"Next pending step: {bt}{current_after_1_61}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )

    for text in (root, web):
        assert "auditoria 1.60" in text
        assert "Final Screen Contract Readiness" in text
        assert "final screen contracts no creados" in text.lower()
        assert "draft contracts no convertidos" in text.lower()
        assert NEXT_PROMPT in text or current_after_1_63 in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "sin User Panel" in text or "User Panel no implementado" in text
