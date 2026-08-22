from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md"
PLAN_127 = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_27.md"
CHECKPOINT_126 = ROOT / "docs" / "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_1_28_document_exists_and_references_base_chain():
    text = read(DOC)

    for marker in [
        "f0e9da58",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_27.md",
        "docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md",
        "Density Reduction",
        "Information Architecture",
        "UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_COMPLETED",
    ]:
        assert marker in text

    assert PLAN_127.exists()
    assert CHECKPOINT_126.exists()
    assert "Density Reduction / Information Architecture" in read(PLAN_127)
    assert "UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_PASSED" in read(CHECKPOINT_126)


def test_audit_1_28_records_human_visual_evidence_and_post_guidance_state():
    text = read(DOC)

    for marker in [
        "POST_GUIDANCE_DENSITY_REVIEWED",
        "bitacora visual / capa de comprension",
        "no solo como pantalla estatica",
        "over-guidance",
        "operator guidance",
        "Panel Maestro",
        "Panel Usuario sigue futuro",
        "<section=11",
        "data-widget=52",
        "contract-detail-panel=16",
    ]:
        assert marker in text


def test_audit_1_28_contains_all_required_audit_areas():
    text = read(DOC)

    for marker in [
        "Header / identidad / estado global",
        "Readiness / payload / contract",
        "Internal services / service signals / read models",
        "Request draft / request contract",
        "Allowed / forbidden / blocked",
        "Evidence / logs-sanitized / Next Step",
        "Detail panels / raw-safe",
        "Navigation / focus / mobile",
        "Component vocabulary",
        "Lenguaje dual y densidad",
        "Visual human evidence",
        "Riesgo de over-guidance",
    ]:
        assert marker in text


def test_audit_1_28_contains_p0_p1_p2_p3_findings():
    text = read(DOC)

    for marker in [
        "P0-001",
        "P0-002",
        "P1-001",
        "P1-002",
        "P1-003",
        "P1-004",
        "P2-001",
        "P2-002",
        "P2-003",
        "P2-004",
        "P2-005",
        "P3-001",
        "P3-002",
        "No hay P0 implementativo detectado",
    ]:
        assert marker in text


def test_audit_1_28_defines_critical_secondary_and_safe_disclosure():
    text = read(DOC)

    for marker in [
        "critical always visible",
        "secondary readable",
        "disclosure seguro",
        "CRITICAL_ALWAYS_VISIBLE_DEFINED",
        "SAFE_DISCLOSURE_RULES_DEFINED",
        "DENSITY_REDUCTION_NO_HIDDEN_BLOCKERS_CONFIRMED",
        "Summary before detail",
        "Guidance breve por defecto",
    ]:
        assert marker in text


def test_audit_1_28_no_hiding_and_safe_compaction_criteria_are_recorded():
    text = read(DOC)

    for marker in [
        "no ocultar forbidden_actions",
        "no ocultar blocked_capabilities",
        "`forbidden_actions` criticos",
        "`blocked_capabilities` criticos",
        "no-runtime/no-execution",
        "request draft read-only/no-submit/no-dispatch/no-execution",
        "ausencia de payload",
        "Criterios de compactacion segura",
        "raw-safe extendido",
        "evidencia extendida",
        "service signals repetitivas",
        "microcopy de ayuda duplicada",
    ]:
        assert marker in text


def test_audit_1_28_recommends_concrete_1_29_scope_and_tests():
    text = read(DOC)

    for marker in [
        "Recomendacion concreta para 1.29",
        "header/global status",
        "readiness/payload/contract",
        "allowed/forbidden/blocked",
        "request draft/request contract",
        "evidence/Next Step",
        "raw-safe/detail",
        "mobile/responsive minimo",
        "test de critical always visible",
        "test de no hidden `forbidden_actions`",
        "test de no hidden `blocked_capabilities`",
        "P3 pospuestos",
    ]:
        assert marker in text


def test_audit_1_28_preserves_contract_identity_and_no_legacy_visual_active():
    text = read(DOC)

    for marker in [
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
        "summary/detail/raw-safe",
        "IA_CORE como identidad activa",
        "no SAAOP/Loteria/Tactical HUD/U-Score como UI activa",
    ]:
        assert marker in text


def test_audit_1_28_confirms_no_runtime_endpoints_dependencies_or_external_installs():
    text = read(DOC)
    lowered = text.lower()

    for marker in [
        "DENSITY_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "no endpoint publico nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no fetch nuevo",
        "no runtime, no execution, no dispatch real y no controlled execution",
        "no dependencias nuevas",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
        "benchmarks futuros solamente",
    ]:
        assert marker in text

    for forbidden in [
        "recomienda crear endpoint",
        "recomienda activar runtime",
        "recomienda activar execution",
        "recomienda instalar",
        "copiar template",
    ]:
        assert forbidden not in lowered


def test_audit_1_28_verdicts_next_prompt_and_readmes_are_recorded():
    text = read(DOC)
    root = read(README)
    ui = read(UI_README)
    next_prompt = (
        "PROMPT UI/UX 1.29 - Endurecer densidad y arquitectura de informacion "
        "IA_CORE contract-aware sin runtime/no-execution"
    )

    for verdict in [
        "UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_COMPLETED",
        "POST_GUIDANCE_DENSITY_REVIEWED",
        "INFORMATION_ARCHITECTURE_GAPS_IDENTIFIED",
        "CRITICAL_ALWAYS_VISIBLE_DEFINED",
        "SAFE_DISCLOSURE_RULES_DEFINED",
        "DENSITY_REDUCTION_NO_HIDDEN_BLOCKERS_CONFIRMED",
        "DENSITY_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_DENSITY_INFORMATION_ARCHITECTURE_HARDENING",
    ]:
        assert verdict in text

    assert next_prompt in text

    for readme in [root, ui]:
        assert "docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md" in readme
        assert "Density Reduction / Information Architecture" in readme
        assert next_prompt in readme
        assert "no-runtime/no-execution" in readme or "no runtime" in readme.lower()
        assert "sin endpoints" in readme.lower() or "No new public endpoints" in readme
