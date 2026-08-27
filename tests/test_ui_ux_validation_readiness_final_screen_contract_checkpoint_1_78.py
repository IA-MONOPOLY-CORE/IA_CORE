from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CHECKPOINT_1_78.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.79 - Consolidar siguiente bloque UI/UX post "
    "Validation & Readiness Final Screen Contract IA_CORE contract-aware "
    "sin runtime/no-execution"
)

VERDICTS = [
    "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_CHECKPOINT_CLOSED",
    "VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_BLOCK_CLOSED",
    "PROMPT_1_75_PLAN_CONFIRMED",
    "PROMPT_1_76_AUDIT_CONFIRMED",
    "PROMPT_1_77_DOCUMENTATION_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_DECISION_CONFIRMED",
    "VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_DOCUMENTED_CONFIRMED",
    "VALIDATION_READINESS_THIRD_FINAL_SCREEN_CONTRACT_DOCUMENTAL_CONFIRMED",
    "THREE_FINAL_SCREEN_CONTRACTS_DOCUMENTAL_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_STATUS_FINAL_DOCUMENTAL_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_IMPLEMENTED_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_UI_ACTIVE_NOT_MODIFIED_CONFIRMED",
    "VALIDATION_READINESS_USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "VALIDATION_READINESS_SOURCE_CONTRACTS_VERIFIED",
    "VALIDATION_READINESS_VALIDATION_SEMANTICS_POLICY_VERIFIED",
    "VALIDATION_READINESS_READINESS_SEMANTICS_POLICY_VERIFIED",
    "VALIDATION_READINESS_ALLOWED_DATA_VERIFIED",
    "VALIDATION_READINESS_FORBIDDEN_OPERATIONAL_DATA_VERIFIED",
    "VALIDATION_READINESS_ALLOWED_LOCAL_READ_ONLY_CONTROLS_VERIFIED",
    "VALIDATION_READINESS_FORBIDDEN_CONTROLS_VERIFIED",
    "VALIDATION_READINESS_ALLOWED_STATES_VERIFIED",
    "VALIDATION_READINESS_FORBIDDEN_STATES_VERIFIED",
    "VALIDATION_READINESS_EVIDENCE_POLICY_VERIFIED",
    "VALIDATION_READINESS_NAVIGATION_POLICY_VERIFIED",
    "VALIDATION_READINESS_COMPONENT_POLICY_VERIFIED",
    "VALIDATION_READINESS_GUARDRAIL_MAPPING_VERIFIED",
    "VALIDATION_READINESS_RELATION_WITH_EXISTING_FINAL_CONTRACTS_VERIFIED",
    "VALIDATION_READINESS_CONTRACT_ACCEPTANCE_CRITERIA_VERIFIED",
    "VALIDATION_READINESS_RISK_REGISTER_VERIFIED",
    "VALIDATION_READINESS_TEST_STRATEGY_VERIFIED",
    "VALIDATION_READINESS_IMPLEMENTATION_BOUNDARY_VERIFIED",
    "READY_NOT_PERMISSION_CONFIRMED",
    "VALIDATION_NOT_EXECUTION_CONFIRMED",
    "VALID_TRUE_NOT_SAFE_TO_EXECUTE_CONFIRMED",
    "ALLOWED_ACTIONS_AS_DATA_NOT_CTA_CONFIRMED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_USER_PANEL_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_GITHUB_RESTORE_POINT_READY",
    "UI_READY_FOR_POST_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_NEXT_BLOCK_PLANNING",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "# UI/UX Validation & Readiness Final Screen Contract Checkpoint 1.78",
        "1e231f8",
        "bd8c254a",
        "1.75",
        "1.76",
        "1.77",
        "1.78",
        "Validation & Readiness Final Screen Contract",
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "tercer contrato documental",
        "VALIDATION_READINESS_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_DECISION_CONFIRMED",
        "restore point GitHub",
        NEXT_PROMPT,
    ]:
        assert marker in text


def test_contract_sections_and_semantics_are_verified():
    text = read(DOC)
    sections = [
        "Contract Finalization Record",
        "Final Screen Contract Identity",
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
    ]
    for section in sections:
        assert section in text

    semantics = [
        "ready` no significa ejecutable",
        "readiness` no significa permiso operativo",
        "validation.valid=true` no implica safe-to-execute",
        "validation` no es ejecucion viva",
        "allowed_actions` son datos, no CTAs",
        "warnings/errors` son datos declarados, no logs vivos",
        "evidence` son referencias, no timeline operativo",
        "final-documental` no es UI activa",
    ]
    for marker in semantics:
        assert marker in text


def test_boundaries_identity_and_restore_requirements_are_explicit():
    text = read(DOC)
    for marker in [
        "no creada",
        "UI activa: no modificada",
        "User Panel: no implementado",
        "No endpoints",
        "rutas",
        "fetches",
        "No dependencias nuevas",
        "No cambios CI",
        "No runtime",
        "execution",
        "dispatch",
        "controlled execution",
        "No unlock",
        "override",
        "bypass",
        "permission escalation",
        "Backend operativo untouched",
        "IA_CORE sigue siendo la identidad activa",
        "SAAOP, Loteria, Tactical HUD y U-Score no son UI activa",
        "git push origin main",
        "sincronizado con `origin/main`",
    ]:
        assert marker in text


def test_readmes_record_checkpoint_and_next_prompt():
    root = read(README)
    web = read(WEB_README)
    for content in (root, web):
        assert "UI/UX avanzado hasta 1.78" in content
        assert "Validation & Readiness Final Screen Contract" in content
        assert "tercer Final Screen Contract documental" in content
        assert "no pantalla" in content
        assert "no UI activa" in content or "sin UI activa modificada" in content
        assert "User Panel no implementado" in content
        assert "no-runtime/no-execution" in content
        assert "sin endpoints" in content or "no endpoints" in content
        assert "sin dependencias" in content or "no dependencias" in content
        assert "sin cambios CI" in content or "no cambios CI" in content
        assert NEXT_PROMPT in content


def test_all_checkpoint_verdicts_are_documented():
    text = read(DOC)
    for verdict in VERDICTS:
        assert verdict in text
