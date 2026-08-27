from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_1_77.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_DOCUMENTED",
    "VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CREATED_AS_DOCUMENTATION",
    "VALIDATION_READINESS_THIRD_FINAL_SCREEN_CONTRACT_DOCUMENTAL_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_AUDIT_ALLOWED_DECISION_RESPECTED",
    "VALIDATION_READINESS_FINAL_CONTRACT_STATUS_FINAL_DOCUMENTAL",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_IMPLEMENTED_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_UI_ACTIVE_NOT_MODIFIED_CONFIRMED",
    "VALIDATION_READINESS_USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "VALIDATION_READINESS_SOURCE_CONTRACTS_DEFINED",
    "VALIDATION_READINESS_VALIDATION_SEMANTICS_POLICY_DEFINED",
    "VALIDATION_READINESS_READINESS_SEMANTICS_POLICY_DEFINED",
    "VALIDATION_READINESS_ALLOWED_DATA_DEFINED",
    "VALIDATION_READINESS_FORBIDDEN_OPERATIONAL_DATA_DEFINED",
    "VALIDATION_READINESS_ALLOWED_LOCAL_READ_ONLY_CONTROLS_DEFINED",
    "VALIDATION_READINESS_FORBIDDEN_CONTROLS_DEFINED",
    "VALIDATION_READINESS_ALLOWED_STATES_DEFINED",
    "VALIDATION_READINESS_FORBIDDEN_STATES_DEFINED",
    "VALIDATION_READINESS_EVIDENCE_POLICY_DEFINED",
    "VALIDATION_READINESS_NAVIGATION_POLICY_DEFINED",
    "VALIDATION_READINESS_COMPONENT_POLICY_DEFINED",
    "VALIDATION_READINESS_GUARDRAIL_MAPPING_DEFINED",
    "VALIDATION_READINESS_RELATION_WITH_EXISTING_FINAL_CONTRACTS_DEFINED",
    "VALIDATION_READINESS_CONTRACT_ACCEPTANCE_CRITERIA_DEFINED",
    "VALIDATION_READINESS_RISK_REGISTER_DEFINED",
    "VALIDATION_READINESS_TEST_STRATEGY_DEFINED",
    "VALIDATION_READINESS_IMPLEMENTATION_BOUNDARY_DEFINED",
    "READY_NOT_PERMISSION_CONFIRMED",
    "VALIDATION_NOT_EXECUTION_CONFIRMED",
    "VALID_TRUE_NOT_SAFE_TO_EXECUTE_CONFIRMED",
    "ALLOWED_ACTIONS_AS_DATA_NOT_CTA_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_CHECKPOINT_1_78",
    "UI_READY_FOR_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CHECKPOINT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_records_finalization_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Validation & Readiness Final Screen Contract 1.77",
        "d8b732e",
        "bd8c254a",
        "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_AUDIT_1_76",
        "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT",
        "FINAL_SCREEN_CONTRACT_DOCUMENTED",
        "not implemented",
        "not created",
        "not modified",
        "not enabled",
        "Contract Finalization Record",
        "Final Screen Contract Identity",
        "Validation & Readiness Final Screen Contract",
        "Final Screen Contract",
        "final-documental",
        "Panel Maestro only",
    ]
    for marker in markers:
        assert marker in text


def test_required_contract_sections_are_defined():
    text = read(DOC)

    sections = [
        "Purpose",
        "Source Contracts",
        "Validation Semantics Policy",
        "Readiness Semantics Policy",
        "Allowed Data",
        "Forbidden Operational Data",
        "Allowed Local / Read-Only Controls",
        "Forbidden Controls",
        "Allowed States",
        "Forbidden States",
        "Evidence Policy",
        "Navigation Policy",
        "Component Policy",
        "Guardrail Mapping",
        "Relation With Existing Final Contracts",
        "Contract Acceptance Criteria",
        "Risk Register",
        "Test Strategy",
        "Implementation Boundary",
        "Next Checkpoint",
    ]
    for section in sections:
        assert f"## {section}" in text


def test_source_contracts_validation_readiness_and_action_semantics_are_explicit():
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
        "payload vs request",
        "ready no significa ejecutable",
        "validation.valid=true no implica safe-to-execute",
        "allowed_actions como datos",
        "warnings/errors` son datos declarados, no logs vivos",
        "evidence` son referencias, no timeline operativo",
    ]
    for marker in markers:
        assert marker in text


def test_allowed_and_forbidden_data_controls_states_are_defined():
    text = read(DOC)

    allowed = [
        "validation.valid",
        "errors",
        "warnings",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "blocked_capabilities",
        "forbidden_actions",
        "allowed_actions como datos",
        "evidence refs",
        "summary/detail/raw-safe",
        "source contract references",
        "test/readiness outcomes",
        "read",
        "focus",
        "expand/collapse",
        "inspect",
        "local filter sin ocultar errores criticos",
        "local group",
        "copy-safe textual reference",
        "local-only details disclosure",
        "read-only",
        "documented",
        "final-documental",
        "draft",
        "candidate",
        "not implemented",
        "planned",
        "blocked",
        "forbidden",
        "unavailable",
        "no_payload",
        "invalid",
        "passed",
        "failed",
        "ready_for_final_contract_audit_next",
    ]
    for marker in allowed:
        assert marker in text

    forbidden = [
        "secrets",
        "env",
        "credentials",
        "API keys",
        "runtime queues",
        "dispatch payloads",
        "tool/model/integration invocation payloads",
        "hidden permissions",
        "operational live logs",
        "scheduler/worker state",
        "internal tokens",
        "request execution traces",
        "submit",
        "send",
        "execute",
        "dispatch",
        "activate",
        "run",
        "operate",
        "materialize",
        "lifecycle actions",
        "unlock",
        "override",
        "bypass",
        "escalate permission",
        "request permission",
        "validate now as operation",
        "retry as operation",
        "auto-fix",
        "fix and run",
        "active",
        "running",
        "live",
        "operational",
        "executing",
        "dispatching",
        "submitted",
        "processing",
        "activated",
        "operating",
        "queued",
        "in progress as runtime",
        "unlockable",
        "overridable",
        "pending permission",
        "escalation pending",
    ]
    for marker in forbidden:
        assert marker in text


def test_policies_relation_risks_and_boundaries_are_documented():
    text = read(DOC)

    markers = [
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "final-documental != UI activa",
        "read-only != permiso operativo",
        "`allowed_actions como datos` != CTA",
        "`blocked_capabilities` y `forbidden_actions` siempre visibles como limites",
        "readiness/validation no contradicen blocked/forbidden",
        "1.76 allowed decision respected",
        "no implementation",
        "no screen",
        "no UI active",
        "no User Panel",
        "no endpoints",
        "no routes/hash",
        "no fetches",
        "no runtime",
        "no execution",
        "no unlock/override/bypass/permission escalation",
        "final contract confundido con pantalla",
        "readiness interpretado como permiso operativo",
        "`validation.valid` interpretado como safe-to-execute",
        "`allowed_actions` convertidas en botones",
        "warnings/errors convertidos en logs vivos",
        "evidence refs convertidas en live logs",
        "endpoint/fetch leakage",
        "User Panel leakage",
        "state semantics leakage",
        "relation mismatch with existing final contracts",
        "Implementacion futura requiere bloque separado",
    ]
    for marker in markers:
        assert marker in text


def test_next_prompt_readmes_and_verdicts_are_documented():
    text = read(DOC)
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert NEXT_PROMPT in text
    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
    for content in (root, web):
        assert "UI/UX avanzado hasta 1.77" in content
        assert "Validation & Readiness Final Screen Contract" in content
        assert "tercer Final Screen Contract documental" in content
        assert "1.78 checkpoint" in content
        assert "no pantalla" in content
        assert "no UI activa" in content or "sin UI activa modificada" in content
        assert "User Panel no implementado" in content
        assert "no-runtime/no-execution" in content
        assert "push pospuesto" in content.lower()
        assert NEXT_PROMPT in content

    for verdict in VERDICTS:
        assert verdict in text
