from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_MINOR_GAPS_AUDIT_1_72.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final "
    "Screen Contract IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_VALIDATION_READINESS_MINOR_GAPS_AUDIT_COMPLETED",
    "VALIDATION_READINESS_SCREEN_DRAFT_REVIEWED",
    "VALIDATION_READINESS_NEEDS_MINOR_GAPS_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "TWO_FINAL_SCREEN_CONTRACTS_DOCUMENTAL_CONFIRMED",
    "VALIDATION_READINESS_AUDIT_DIMENSIONS_COMPLETED",
    "VALIDATION_READINESS_GAP_REGISTER_CREATED",
    "VALIDATION_READINESS_GAPS_CLASSIFIED",
    "VALIDATION_READINESS_MINOR_GAPS_CLOSURE_PLAN_DEFINED",
    "VALIDATION_READINESS_OUT_OF_SCOPE_ITEMS_DEFINED",
    "VALIDATION_READINESS_FINALIZATION_GATE_DEFINED",
    "VALIDATION_READINESS_RISK_REGISTER_DEFINED",
    "VALIDATION_READINESS_TEST_STRATEGY_DEFINED",
    "VALIDATION_READINESS_CAN_MOVE_TO_GAPS_CLOSURE_NEXT",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_USER_PANEL_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_CHECKPOINT_1_74",
    "UI_READY_FOR_VALIDATION_READINESS_MINOR_GAPS_CLOSURE",
]

DIMENSIONS = [
    "Surface",
    "Owner",
    "Purpose",
    "Source contracts",
    "Validation semantics",
    "Readiness semantics",
    "Allowed data",
    "Forbidden operational data",
    "Allowed local controls",
    "Forbidden controls",
    "State semantics",
    "Evidence policy",
    "Component policy",
    "Navigation policy",
    "Guardrail mapping",
    "Finalization gate",
    "Relation with existing final contracts",
    "Test coverage",
]

GAPS = [
    "VRG-172-001",
    "VRG-172-002",
    "VRG-172-003",
    "VRG-172-004",
    "VRG-172-005",
    "VRG-172-006",
    "VRG-172-007",
    "VRG-172-008",
    "VRG-172-009",
    "VRG-172-010",
    "VRG-172-011",
    "VRG-172-012",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Validation & Readiness Minor Gaps Audit 1.72",
        "63461af9",
        "c3bcf264",
        "main",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "working tree limpio",
        "push pospuesto hasta checkpoint 1.74",
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "VALIDATION_READINESS_MINOR_GAPS_CAN_BE_CLOSED_NEXT",
    ]
    for marker in markers:
        assert marker in text


def test_audit_reviews_expected_sources_and_candidate_baseline():
    text = read(DOC)

    sources = [
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_71.md",
        "docs/UI_UX_FINAL_SCREEN_CONTRACT_READINESS_1_61.md",
        "docs/UI_UX_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_1_57.md",
        "docs/UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_1_65.md",
        "docs/UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_1_69.md",
        "docs/UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_70.md",
        "docs/UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_66.md",
    ]
    for source in sources:
        assert source in text

    baseline = [
        "Validation & Readiness Screen Draft",
        "CFD-02",
        "Panel Maestro",
        "readiness documental",
        "validaciones declaradas",
        "warnings",
        "errors",
        "flags",
        "gates",
        "evidencia/test-output segura",
        "no final",
        "no implementado",
    ]
    for marker in baseline:
        assert marker in text


def test_all_required_audit_dimensions_are_present_once_or_more():
    text = read(DOC)

    assert "Auditoria Por Dimension" in text
    assert text.count("| Dimension | Status | Findings / gaps | 1.73 puede cerrar | Sigue prohibido |") == 1
    for dimension in DIMENSIONS:
        assert f"| {dimension} |" in text


def test_gap_register_contains_expected_gaps_classification_and_counts():
    text = read(DOC)

    assert "Gap Register" in text
    for gap in GAPS:
        assert gap in text

    count_markers = [
        "`P0_BLOCKER`: 0",
        "`P1_MINOR_GAP`: 6",
        "`P2_DOC_CLARITY`: 4",
        "`P3_FUTURE_SCREEN_NOTE`: 1",
        "`OUT_OF_SCOPE`: 1",
        "`state_semantics`: 1",
        "`readiness_semantics`: 1",
        "`validation_semantics`: 1",
        "`evidence_policy`: 1",
        "`forbidden_controls`: 1",
        "`allowed_data`: 1",
        "`source_contracts`: 1",
        "`allowed_local_controls`: 1",
        "`user_panel_boundary`: 1",
        "`relation_with_existing_final_contracts`: 1",
        "`component_policy`: 1",
        "`no_implementation_boundary`: 1",
    ]
    for marker in count_markers:
        assert marker in text


def test_minor_gap_closure_plan_and_finalization_gate_are_non_operational():
    text = read(DOC)

    closure_markers = [
        "tabla estricta de estados `pending`, `passed`, `failed`, `ready`",
        "readiness no es permiso",
        "`validation.valid` no es validacion viva",
        "evidence/test-output como snapshot documental",
        "warnings/errors visibles sin remediation",
        "`allowed_actions` como dato backend-declared y no CTA",
        "payload leido vs request envelope no enviado",
        "critical warnings/errors",
        "Panel Maestro only",
        "User Panel no implementado",
    ]
    for marker in closure_markers:
        assert marker in text

    prohibited = [
        "No crear `Validation & Readiness Final Screen Contract`",
        "No crear pantalla/UI activa/User Panel",
        "No crear endpoint/ruta/fetch/dependencia/CI",
        "No activar runtime/execution/dispatch/controlled execution",
        "No introducir unlock/override/bypass/permission escalation",
    ]
    for marker in prohibited:
        assert marker in text


def test_no_implementation_boundary_and_forbidden_actions_are_explicit():
    text = read(DOC)

    forbidden_markers = [
        "no crea `Validation & Readiness Final Screen Contract`",
        "no crea pantalla",
        "no modifica UI activa",
        "no crea User Panel",
        "no crea endpoints/rutas/fetches",
        "no agrega dependencias",
        "no toca CI",
        "no activa runtime/execution/dispatch/controlled execution",
        "validate real",
        "fix",
        "repair",
        "submit",
        "execute",
        "dispatch",
        "activate",
        "materialize",
        "unlock",
        "override",
        "bypass",
        "permission escalation",
    ]
    for marker in forbidden_markers:
        assert marker in text


def test_readmes_register_audit_and_cursor_to_1_73():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
    assert "docs/UI_UX_VALIDATION_READINESS_MINOR_GAPS_AUDIT_1_72.md" in root

    for text in (root, web):
        assert "auditado hasta 1.72" in text
        assert "Validation & Readiness Minor Gaps Closure" in text
        assert "Validation & Readiness Screen Draft" in text
        assert "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT" in text
        assert "no crea final screen contract" in text
        assert "no crea pantalla" in text
        assert "User Panel no implementado" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "no-runtime/no-execution" in text
        assert "push pospuesto" in text.lower()
        assert "1.74" in text
        assert NEXT_PROMPT in text


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
