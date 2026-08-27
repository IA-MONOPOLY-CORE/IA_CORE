from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_MINOR_GAPS_CHECKPOINT_1_74.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post "
    "Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin "
    "runtime/no-execution"
)
CURRENT_AFTER_1_75 = (
    "PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)

GAPS = [f"VRG-172-{index:03d}" for index in range(1, 13)]

DIMENSIONS = [
    "Surface Boundary",
    "Owner / Backend Authority",
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
    "Relation With Existing Final Contracts",
    "Finalization Gate",
]

CURRENT_AFTER_1_76 = (
    "PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)
VERDICTS = [
    "UI_UX_VALIDATION_READINESS_MINOR_GAPS_CHECKPOINT_CLOSED",
    "VALIDATION_READINESS_MINOR_GAPS_BLOCK_CLOSED",
    "PROMPT_1_71_PLAN_CONFIRMED",
    "PROMPT_1_72_AUDIT_CONFIRMED",
    "PROMPT_1_73_CLOSURE_CONFIRMED",
    "VALIDATION_READINESS_12_GAPS_CLOSED_CONFIRMED",
    "VALIDATION_READINESS_P0_BLOCKERS_ZERO_CONFIRMED",
    "VALIDATION_READINESS_P1_MINOR_GAPS_ZERO_PENDING_CONFIRMED",
    "VALIDATION_READINESS_STATUS_READY_FOR_FINAL_CONTRACT_AUDIT_NEXT_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_AUDIT_NOT_EXECUTED_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "VALIDATION_READINESS_SURFACE_BOUNDARY_VERIFIED",
    "VALIDATION_READINESS_BACKEND_AUTHORITY_VERIFIED",
    "VALIDATION_READINESS_VALIDATION_SEMANTICS_VERIFIED",
    "VALIDATION_READINESS_READINESS_SEMANTICS_VERIFIED",
    "VALIDATION_READINESS_ALLOWED_DATA_VERIFIED",
    "VALIDATION_READINESS_FORBIDDEN_OPERATIONAL_DATA_VERIFIED",
    "VALIDATION_READINESS_ALLOWED_LOCAL_CONTROLS_VERIFIED",
    "VALIDATION_READINESS_FORBIDDEN_CONTROLS_VERIFIED",
    "VALIDATION_READINESS_ALLOWED_STATES_VERIFIED",
    "VALIDATION_READINESS_FORBIDDEN_STATES_VERIFIED",
    "VALIDATION_READINESS_EVIDENCE_POLICY_VERIFIED",
    "VALIDATION_READINESS_NAVIGATION_POLICY_VERIFIED",
    "VALIDATION_READINESS_COMPONENT_POLICY_VERIFIED",
    "VALIDATION_READINESS_GUARDRAIL_MAPPING_VERIFIED",
    "VALIDATION_READINESS_RELATION_WITH_EXISTING_FINAL_CONTRACTS_VERIFIED",
    "VALIDATION_READINESS_FINALIZATION_GATE_VERIFIED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_USER_PANEL_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "VALIDATION_READINESS_MINOR_GAPS_GITHUB_RESTORE_POINT_READY",
    "UI_READY_FOR_POST_VALIDATION_READINESS_MINOR_GAPS_NEXT_BLOCK_PLANNING",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_git_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Validation & Readiness Minor Gaps Checkpoint 1.74",
        "b1515ccf",
        "c3bcf264",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "local ahead de `origin/main` por 3 commits",
        "1.71 -> 1.74",
        "Validation & Readiness Minor Gaps Closure",
        "GitHub Restore Point",
    ]
    for marker in markers:
        assert marker in text


def test_prompts_deliverables_and_gap_closure_are_verified():
    text = read(DOC)

    for prompt in ("1.71", "1.72", "1.73", "1.74"):
        assert prompt in text
    for path in [
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_71.md",
        "docs/UI_UX_VALIDATION_READINESS_MINOR_GAPS_AUDIT_1_72.md",
        "docs/UI_UX_VALIDATION_READINESS_MINOR_GAPS_CLOSURE_1_73.md",
        "docs/UI_UX_VALIDATION_READINESS_MINOR_GAPS_CHECKPOINT_1_74.md",
    ]:
        assert path in text
    for gap in GAPS:
        assert gap in text
    assert text.count("`CLOSED`") >= 12
    assert "P0_BLOCKER: 0" in text
    assert "P1_MINOR_GAP: 0 pendientes" in text


def test_candidate_status_and_no_final_contract_boundaries_are_recorded():
    text = read(DOC)

    markers = [
        "Validation & Readiness Screen Draft",
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "Validation & Readiness Final Screen Contract` no creado",
        "Final Contract Audit no ejecutado",
        "Pantalla Validation & Readiness no implementada",
        "no habilita submit/execute/dispatch",
    ]
    for marker in markers:
        assert marker in text


def test_all_hardening_dimensions_are_verified():
    text = read(DOC)

    assert "Hardening Verificado" in text
    for dimension in DIMENSIONS:
        assert f"### {dimension}" in text


def test_limits_identity_and_restore_point_are_preserved():
    text = read(DOC)

    markers = [
        "No UI activa modificada",
        "No User Panel",
        "No endpoints, rutas, routers, hashes operativos ni fetches",
        "No dependencias nuevas",
        "No cambios CI",
        "No runtime, execution, dispatch, controlled execution",
        "No unlock, override, bypass ni permission escalation",
        "Backend untouched",
        "IA_CORE sigue como identidad activa",
        "SAAOP, Loteria, Tactical HUD y U-Score",
        "VALIDATION_READINESS_MINOR_GAPS_GITHUB_RESTORE_POINT_READY",
    ]
    for marker in markers:
        assert marker in text


def test_validation_suite_next_prompt_and_readme_cursors_are_recorded():
    text = read(DOC)
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    for command in [
        "node --check ui/web/backend-contract-widgets.js",
        "node --check ui/web/admin-panels.js",
        "node --check ui/web/console-interactions.js",
        "pytest tests/test_ui_ux_validation_readiness_minor_gaps_checkpoint_1_74.py -q",
        "pytest tests/test_ia_core_github_backup_readiness.py -q",
        "git diff --check",
    ]:
        assert command in text

    assert NEXT_PROMPT in text
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_75}{bt}" in root
        or f"Next pending step: {bt}{CURRENT_AFTER_1_76}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )
    for content in (root, web):
        assert "UI/UX avanzado hasta 1.74" in content
        assert "Validation & Readiness Minor Gaps Closure" in content
        assert "12 gaps" in content
        assert "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT" in content
        assert "no final contract" in content
        assert "no pantalla" in content
        assert "User Panel no implementado" in content
        assert "no-runtime/no-execution" in content
        assert NEXT_PROMPT in content


def test_no_validation_readiness_final_contract_document_was_created():
    final_contracts = [
        path for path in (ROOT / "docs").glob("UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_*.md")
        if "_AUDIT_" not in path.name and path.name != "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_1_77.md"
    ]
    assert final_contracts == []


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
