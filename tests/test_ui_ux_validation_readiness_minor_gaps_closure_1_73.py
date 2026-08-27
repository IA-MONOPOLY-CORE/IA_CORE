from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_MINOR_GAPS_CLOSURE_1_73.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps "
    "Closure IA_CORE contract-aware sin runtime/no-execution"
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

VERDICTS = [
    "UI_UX_VALIDATION_READINESS_MINOR_GAPS_CLOSURE_COMPLETED",
    "VALIDATION_READINESS_12_GAPS_CLOSED",
    "VALIDATION_READINESS_P0_BLOCKERS_ZERO_CONFIRMED",
    "VALIDATION_READINESS_P1_MINOR_GAPS_ZERO_PENDING",
    "VALIDATION_READINESS_STATUS_READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
    "VALIDATION_READINESS_FINAL_CONTRACT_NOT_CREATED_CONFIRMED",
    "VALIDATION_READINESS_FINAL_CONTRACT_AUDIT_NOT_EXECUTED_CONFIRMED",
    "VALIDATION_READINESS_SCREEN_NOT_IMPLEMENTED_CONFIRMED",
    "VALIDATION_READINESS_SURFACE_BOUNDARY_HARDENED",
    "VALIDATION_READINESS_BACKEND_AUTHORITY_HARDENED",
    "VALIDATION_READINESS_VALIDATION_SEMANTICS_HARDENED",
    "VALIDATION_READINESS_READINESS_SEMANTICS_HARDENED",
    "VALIDATION_READINESS_ALLOWED_DATA_HARDENED",
    "VALIDATION_READINESS_FORBIDDEN_OPERATIONAL_DATA_HARDENED",
    "VALIDATION_READINESS_ALLOWED_LOCAL_CONTROLS_HARDENED",
    "VALIDATION_READINESS_FORBIDDEN_CONTROLS_HARDENED",
    "VALIDATION_READINESS_ALLOWED_STATES_HARDENED",
    "VALIDATION_READINESS_FORBIDDEN_STATES_HARDENED",
    "VALIDATION_READINESS_EVIDENCE_POLICY_HARDENED",
    "VALIDATION_READINESS_NAVIGATION_POLICY_HARDENED",
    "VALIDATION_READINESS_COMPONENT_POLICY_HARDENED",
    "VALIDATION_READINESS_GUARDRAIL_MAPPING_HARDENED",
    "VALIDATION_READINESS_RELATION_WITH_EXISTING_FINAL_CONTRACTS_HARDENED",
    "VALIDATION_READINESS_FINALIZATION_GATE_SATISFIED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_USER_PANEL_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "NO_UNLOCK_NO_OVERRIDE_NO_BYPASS_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_CHECKPOINT_1_74",
    "UI_READY_FOR_VALIDATION_READINESS_MINOR_GAPS_CHECKPOINT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_closure_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Validation & Readiness Minor Gaps Closure 1.73",
        "72798a81",
        "c3bcf264",
        "local ahead de `origin/main` por 2 commits",
        "Validation & Readiness Minor Gaps Closure",
        "Validation & Readiness Screen Draft",
        "NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT",
        "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT",
        "P0_BLOCKER: 0",
        "P1_MINOR_GAP: 0 pendientes",
    ]
    for marker in markers:
        assert marker in text


def test_gap_closure_register_closes_all_12_gaps():
    text = read(DOC)

    assert "Gap Closure Register" in text
    assert text.count("`CLOSED`") >= 12
    for gap in GAPS:
        assert gap in text
    assert "12 gaps `CLOSED`" in text
    assert "P2/P3 residuales no bloqueantes" in text


def test_each_gap_has_test_coverage_and_residual_status():
    text = read(DOC)

    coverage_markers = [
        "Test documental 1.73",
        "static checks 1.73",
        "Cobertura de test",
        "Ningun P1 residual",
        "Residual no bloqueante",
        "Residual aceptado",
    ]
    for marker in coverage_markers:
        assert marker in text


def test_hardening_dimensions_are_documented():
    text = read(DOC)

    assert "Hardening Por Dimension" in text
    for dimension in DIMENSIONS:
        assert f"### {dimension}" in text


def test_semantics_controls_states_and_evidence_are_hardened():
    text = read(DOC)

    markers = [
        "Panel Maestro only",
        "Validation & Readiness no pertenece a UI inference",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions` solo como datos/no CTAs",
        "validation.valid` es resultado declarado por contrato",
        "no validacion viva",
        "Sin `validate now` operativo",
        "ready` no significa ejecutable ahora",
        "ready` no significa permiso",
        "no ignora `blocked_capabilities`",
        "no oculta `forbidden_actions`",
        "filter local sin ocultar errores criticos",
        "submit, send, execute, dispatch, activate, run, operate, materialize",
        "pending documental no-running",
        "ready contractual no-permission",
        "active, running, live, operational, executing, dispatching",
        "live logs",
        "runtime events",
        "execution simulation",
    ]
    for marker in markers:
        assert marker in text


def test_relation_with_existing_final_contracts_and_boundaries_are_explicit():
    text = read(DOC)

    markers = [
        "Contract Overview Final Screen Contract",
        "Blocked & Forbidden Final Screen Contract",
        "final-documental no es UI activa",
        "read-only no es permiso operativo",
        "`allowed_actions` como dato no es CTA",
        "blocked/forbidden permanecen visibles",
        "final contract documental no autoriza implementacion",
        "No final contract creado",
        "Final contract audit no ejecutado",
        "No pantalla, UI activa ni User Panel",
        "No endpoints/rutas/fetches/dependencias/CI",
        "No runtime/execution/dispatch/controlled execution",
        "No unlock/override/bypass/permission escalation",
    ]
    for marker in markers:
        assert marker in text


def test_updated_candidate_status_and_next_checkpoint_are_recorded():
    text = read(DOC)
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert "Estado anterior: `NEEDS_MINOR_GAPS_BEFORE_FINAL_CONTRACT`" in text
    assert "Estado nuevo documental: `READY_FOR_FINAL_CONTRACT_AUDIT_NEXT`" in text
    assert NEXT_PROMPT in text
    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
    assert NEXT_PROMPT in web


def test_verdicts_are_documented():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text
