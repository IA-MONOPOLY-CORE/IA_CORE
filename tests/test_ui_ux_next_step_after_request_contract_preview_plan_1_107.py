from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_STEP_AFTER_REQUEST_CONTRACT_PREVIEW_PLAN_1_107.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_received_state():
    text = read(DOC)
    required = [
        "UI/UX Next Step After Request Contract Preview Plan 1.107",
        "ec0e25f",
        "REQUEST_CONTRACT_PREVIEW_FINAL_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "HUMAN_VISUAL_REVIEW_APPROVED",
        "baseline de cuatro secciones",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "Request Contract Preview",
        "FSC-RCP-04",
        "Panel Maestro",
        "documental",
        "read-only",
        "contract-aware",
    ]
    for marker in required:
        assert marker in text


def test_plan_document_records_no_execution_boundaries():
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
    ]:
        assert marker in text or marker.lower() in lower


def test_plan_document_has_options_matrix_decision_and_next_prompt():
    text = read(DOC)
    allowed_decisions = [
        "NEXT_STEP_FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_SELECTED",
        "NEXT_STEP_FINAL_SCREEN_CONTRACTS_CONSOLIDATION_SELECTED",
        "NEXT_STEP_GLOBAL_CONSOLE_DENSITY_AUDIT_SELECTED",
        "NEXT_STEP_NEXT_UI_UX_BLOCK_PLANNING_SELECTED",
        "NEXT_STEP_CONTINUITY_AUDIT_SELECTED",
        "NEXT_STEP_SELECTION_BLOCKED_NEEDS_MORE_REVIEW",
    ]
    for marker in [
        "Opciones evaluadas",
        "Matriz de decisión",
        "Four Screen Baseline Integration Audit",
        "Final Screen Contracts Consolidation",
        "Global Console Density and Readability Audit",
        "Next UI/UX Block Planning",
        "Continuity Audit / no new action yet",
        "Risk register",
    ]:
        assert marker in text
    decisions = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed_decisions
    ]
    assert decisions == ["NEXT_STEP_FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_SELECTED"]
    assert (
        "PROMPT UI/UX 1.108 - Auditar integracion baseline de cuatro secciones Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_plan_document_records_required_scope_limits():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "no pantalla",
        "no UI activa",
        "no Contract Overview",
        "no Blocked & Forbidden",
        "no Validation & Readiness",
        "no Request Contract Preview",
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
        "no se implementó pantalla",
        "no se modificó UI activa",
        "no se avanzó a 1.108",
    ]:
        assert marker in text or marker.lower() in lower


def test_readmes_record_1_107_cursor():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "next step after request contract preview plan 1.107" in lower
        assert "baseline de cuatro secciones" in lower
        assert "next_step_four_screen_baseline_integration_audit_selected" in lower
        assert (
            "prompt ui/ux 1.108 - auditar integracion baseline de cuatro secciones panel maestro ia_core contract-aware sin runtime/no-execution"
            in lower
        )
        assert "no implementación" in lower or "no implementacion" in lower
        assert "push pospuesto" in lower
