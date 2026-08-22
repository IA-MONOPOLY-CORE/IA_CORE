from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_19.md"
README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_1_19_document_exists_and_references_base():
    text = read(DOC)

    for marker in [
        "bd4e370e",
        "UI_UX_NEXT_BLOCK_PLAN_1_19_DEFINED",
        "POST_1_18_STATE_REVIEWED",
        "docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md",
        "Admin Boundary / Exposure Review",
        "IA_CORE",
    ]:
        assert marker in text


def test_plan_1_19_contains_all_candidate_options():
    text = read(DOC)

    options = [
        "Operator Guidance / Empty-State Intelligence",
        "Density Reduction / Information Architecture",
        "Contract Storytelling / Operator Narrative",
        "Secondary Console Views / Detail Screens",
        "Visual Polish / Premium IA_CORE Layer",
        "Panel Maestro vs User Panel Separation",
        "Component Documentation / Style Reference",
        "Future Benchmark Review",
        "Frontend Incongruence Audit",
        "Readiness for Future Screens",
    ]
    for option in options:
        assert option in text

    assert "Matriz De Decision" in text
    assert "Criterios De Decision" in text


def test_plan_1_19_selects_frontend_incongruence_audit_with_evidence():
    text = read(DOC)

    assert "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE" in text
    assert "La opcion seleccionada es:\n\n`Frontend Incongruence Audit`" in text
    assert "FRONTEND_RESIDUAL_RISKS_RECORDED" in text
    assert "clases `.active`" in text
    assert "nombres legacy no operativos" in text
    assert "estilos duplicados" in text
    assert "JS legacy no-operativo" in text


def test_plan_1_19_records_postponed_options_and_sequence():
    text = read(DOC)

    assert "Opciones Pospuestas" in text
    for marker in [
        "1.20 - Auditar incongruencias restantes del frontend IA_CORE contract-aware sin runtime/no-execution.",
        "1.21 - Endurecer o documentar incongruencias frontend segun auditoria IA_CORE contract-aware sin runtime/no-execution.",
        "1.22 - Checkpoint Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution.",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
    ]:
        assert marker in text


def test_plan_1_19_next_prompt_exact():
    text = read(DOC)

    assert "PROMPT UI/UX 1.20 - Auditar incongruencias restantes del frontend IA_CORE contract-aware sin runtime/no-execution" in text
    assert "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK" in text


def test_plan_1_19_keeps_contract_and_no_runtime_boundaries():
    text = read(DOC)

    for marker in [
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "no endpoint publico, API ni router HTTP",
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
    ]:
        assert marker in text

    for phrase in [
        "La opcion seleccionada es:\n\n`Secondary Console Views / Detail Screens`",
        "La opcion seleccionada es:\n\n`Visual Polish / Premium IA_CORE Layer`",
        "La opcion seleccionada es:\n\n`Future Benchmark Review`",
    ]:
        assert phrase not in text


def test_plan_1_19_external_references_are_benchmarks_only():
    text = read(DOC)

    assert "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY" in text
    for marker in ["21st.dev", "UI UX Pro Max Skill", "Framer Motion / Motion"]:
        assert marker in text
    assert "No se instalan" not in text  # document uses lowercase boundaries, not an install instruction.
    assert "no assets externos, templates externos ni referencias instaladas" in text


def test_plan_1_19_confirms_identity_and_no_legacy_visual_active():
    text = read(DOC)
    html = read(INDEX)

    assert "IA_CORE como identidad visual activa" in text
    assert "ausencia de SAAOP" in text
    assert "IA_CORE" in html
    for marker in ["SAAOP", "S.A.A.O.P", "Loteria", "lottery", "Tactical HUD"]:
        assert marker.lower() not in html.lower()


def test_readme_registers_plan_1_19_and_selected_block():
    readme = read(README)

    for marker in [
        "Planificacion siguiente bloque UI/UX 1.19",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_19.md",
        "Frontend Incongruence Audit",
        "PROMPT UI/UX 1.20 - Auditar incongruencias restantes del frontend IA_CORE contract-aware sin runtime/no-execution",
        "21st.dev, UI UX Pro Max Skill y Framer Motion / Motion siguen como benchmarks futuros",
    ]:
        assert marker in readme
