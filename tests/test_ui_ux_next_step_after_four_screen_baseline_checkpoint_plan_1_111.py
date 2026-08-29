from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_STEP_AFTER_FOUR_SCREEN_BASELINE_CHECKPOINT_PLAN_1_111.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_received_checkpoint_state():
    text = read(DOC)
    required = [
        "UI/UX Next Step After Four Screen Baseline Checkpoint Plan 1.111",
        "ccdef7a",
        "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_PASSED_WITH_NOTES",
        "HUMAN_VISUAL_REVIEW_APPROVED_WITH_NOTES",
        "baseline de cuatro secciones",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "Request Contract Preview",
        "FSC-RCP-04",
        "1.88",
        "1.94",
        "1.100",
        "1.106",
        "1.110",
        "Panel Maestro",
        "documental",
        "contract-aware",
    ]
    for marker in required:
        assert marker in text
    assert "read-only" in text or "solo lectura" in text


def test_plan_document_records_current_ui_boundaries_and_notes():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no submit",
        "no send",
        "no run",
        "no execute",
        "DEFER_FINALIZATION",
        "no raw Package",
        "no payload crudo",
        "no ghost actions",
        "no fake success",
        "elementos inferiores",
    ]:
        assert marker in text or marker.lower() in lower
    assert "UI técnica" in text or "UI tecnica" in text


def test_plan_document_evaluates_options_and_selects_consolidation():
    text = read(DOC)
    allowed_decisions = [
        "NEXT_STEP_FINAL_SCREEN_CONTRACTS_CONSOLIDATION_SELECTED",
        "NEXT_STEP_LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_SELECTED",
        "NEXT_STEP_GLOBAL_CONSOLE_DENSITY_REVIEW_SELECTED",
        "NEXT_STEP_NEXT_UI_UX_BLOCK_PLANNING_SELECTED",
        "NEXT_STEP_CONTINUITY_AUDIT_SELECTED",
        "NEXT_STEP_SELECTION_BLOCKED_NEEDS_MORE_REVIEW",
    ]
    for marker in [
        "Opciones evaluadas",
        "Final Screen Contracts Consolidation",
        "Lower Console Existing Elements Audit",
        "Global Console Density Review",
        "Next UI/UX Block Planning",
        "Continuity Audit / Strategic Pause",
        "Matriz de decisión",
        "Risk register",
    ]:
        assert marker in text
    decisions = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed_decisions
    ]
    assert decisions == ["NEXT_STEP_FINAL_SCREEN_CONTRACTS_CONSOLIDATION_SELECTED"]
    assert (
        "PROMPT UI/UX 1.112 - Consolidar bloque Final Screen Contracts implementado IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_plan_document_records_scope_limits_explicitly():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "no pantalla",
        "no quinta sección",
        "no UI activa",
        "no Contract Overview",
        "no Blocked & Forbidden",
        "no Validation & Readiness",
        "no Request Contract Preview",
        "no contrato funcional",
        "no contrato final",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no runtime",
        "no endpoint",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "No se implementó pantalla",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se avanzó a 1.112",
    ]:
        assert marker in text or marker.lower() in lower


def test_readmes_record_1_111_cursor_and_next_prompt():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "next step after four screen baseline checkpoint plan 1.111" in lower
        assert "ccdef7a" in text
        assert "baseline de cuatro secciones" in lower
        assert "next_step_final_screen_contracts_consolidation_selected" in lower
        assert (
            "prompt ui/ux 1.112 - consolidar bloque final screen contracts implementado ia_core contract-aware sin runtime/no-execution"
            in lower
        )
        assert "no implementación" in lower or "no implementacion" in lower
        assert "push pospuesto" in lower
