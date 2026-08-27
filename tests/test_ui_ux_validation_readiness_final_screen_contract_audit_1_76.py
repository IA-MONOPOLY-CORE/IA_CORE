from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_AUDIT_1_76.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)

DIMENSIONS = [
    "Readiness previa",
    "Surface",
    "Owner / Authority",
    "Purpose",
    "Source Contracts",
    "Validation Semantics",
    "Readiness Semantics",
    "Allowed Data",
    "Forbidden Operational Data",
    "Allowed Local Controls",
    "Forbidden Controls",
    "Allowed States",
    "Forbidden States",
    "Evidence Policy",
    "Navigation Policy",
    "Component Policy",
    "Guardrail Mapping",
    "Relation with existing final contracts",
    "Final Contract Readiness",
    "Test Coverage",
]

VERDICTS = [
    "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_AUDIT_COMPLETED",
    "VALIDATION_READINESS_SCREEN_DRAFT_READY_FOR_FINAL_CONTRACT_AUDIT_CONFIRMED",
    "VALIDATION_READINESS_12_GAPS_CLOSED_CONFIRMED",
    "VALIDATION_READINESS_P0_BLOCKERS_ZERO_CONFIRMED",
    "VALIDATION_READINESS_P1_MINOR_GAPS_ZERO_PENDING_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_DOCUMENTED_IN_1_76_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "TWO_FINAL_SCREEN_CONTRACTS_DOCUMENTAL_CONFIRMED",
    "VALIDATION_READINESS_AUDIT_DIMENSIONS_COMPLETED",
    "VALIDATION_READINESS_FINDINGS_REGISTER_CREATED",
    "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_GATE_DEFINED",
    "VALIDATION_READINESS_1_77_SCOPE_RECOMMENDATION_DEFINED",
    "VALIDATION_READINESS_1_77_FORBIDDEN_SCOPE_DEFINED",
    "VALIDATION_READINESS_RISK_REGISTER_DEFINED",
    "VALIDATION_READINESS_TEST_STRATEGY_DEFINED",
    "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_USER_PANEL_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_CHECKPOINT_1_78",
    "UI_READY_FOR_VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Validation & Readiness Final Screen Contract Audit 1.76",
        "0f04178c",
        "bd8c254a",
        "local ahead de `origin/main` por 1 commit esperado",
        "Validation & Readiness Final Screen Contract Audit",
        "push pospuesto",
    ]
    for marker in markers:
        assert marker in text


def test_current_state_candidate_and_previous_closure_are_confirmed():
    text = read(DOC)

    markers = [
        "Validation & Readiness Screen Draft",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "P0_BLOCKER: 0",
        "P1_MINOR_GAP: 0 pendientes",
        "VRG-172-001",
        "VRG-172-012",
        "12 gaps cerrados",
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "Dos Final Screen Contracts documentales existentes",
        "Validation & Readiness Final Screen Contract` no existe todavia",
        "No final contract documentado en 1.76",
    ]
    for marker in markers:
        assert marker in text


def test_no_scope_boundaries_are_explicit():
    text = read(DOC)

    markers = [
        "No se crea pantalla",
        "No se modifica UI activa",
        "No User Panel",
        "No endpoints/runtime",
        "No rutas/hash/API/router/fetches",
        "No runtime/execution/dispatch/controlled execution",
        "No unlock/override/bypass/permission escalation",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_all_20_dimensions_findings_gate_scope_risks_and_strategy_exist():
    text = read(DOC)

    assert "Auditoria Por Dimension" in text
    for dimension in DIMENSIONS:
        assert dimension in text
    for section in [
        "Findings Register",
        "Resumen de hallazgos por clasificacion",
        "Final Contract Documentation Gate",
        "1.77 Scope Recommendation",
        "1.77 Forbidden Scope",
        "Risk Register",
        "Test Strategy Para 1.77",
    ]:
        assert section in text

    for classification in ["PASS", "MINOR_NOTE", "P1_GAP", "P0_BLOCKER", "OUT_OF_SCOPE"]:
        assert classification in text


def test_decision_is_unique_and_allowed_next():
    text = read(DOC)

    assert "Decision unica: `VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT`" in text
    assert text.count("Decision unica:") == 1
    assert "Hallazgos bloqueantes: ninguno" in text
    assert "`P1_GAP`: 0" in text
    assert "`P0_BLOCKER`: 0" in text


def test_next_prompt_and_readme_cursors_are_updated():
    text = read(DOC)
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert NEXT_PROMPT in text
    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
    for content in (root, web):
        assert "UI/UX avanzado hasta 1.76" in content
        assert "Validation & Readiness Final Screen Contract Audit" in content
        assert "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT" in content
        assert "no final contract" in content
        assert "no pantalla" in content
        assert "no UI activa" in content or "sin UI activa modificada" in content
        assert "User Panel no implementado" in content or "No User Panel" in content
        assert "no-runtime/no-execution" in content
        assert "push pospuesto" in content.lower()
        assert NEXT_PROMPT in content


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
