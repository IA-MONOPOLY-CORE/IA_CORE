from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_AFTER_FINAL_SCREEN_CONTRACTS_PLAN_1_113.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_received_consolidation():
    text = read_doc()
    for marker in [
        "UI/UX Next Block After Final Screen Contracts Plan 1.113",
        "9a6e8c1",
        "ccdef7a",
        "0403422",
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATED_READY_FOR_NEXT_STEP_PLANNING",
        "NEXT_STEP_FINAL_SCREEN_CONTRACTS_CONSOLIDATION_SELECTED",
        "Final Screen Contracts",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "Request Contract Preview",
        "FSC-RCP-04",
        "elementos inferiores",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "CFG",
        "DOMAIN",
    ]:
        assert marker in text


def test_plan_document_evaluates_all_options_and_selects_one():
    text = read_doc()
    for marker in [
        "Opciones evaluadas",
        "Lower Console Existing Elements Audit",
        "Global Console Density Review",
        "Console Navigation and Structure Planning",
        "Next Product Area UI/UX Planning",
        "Checkpoint Local Commits / Publish Planning",
        "Continuity Audit / Strategic Pause",
        "Matriz de decisión",
        "Risk register",
    ]:
        assert marker in text
    allowed = [
        "NEXT_BLOCK_LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_SELECTED",
        "NEXT_BLOCK_GLOBAL_CONSOLE_DENSITY_REVIEW_SELECTED",
        "NEXT_BLOCK_CONSOLE_NAVIGATION_STRUCTURE_PLANNING_SELECTED",
        "NEXT_BLOCK_NEXT_PRODUCT_AREA_UI_UX_PLANNING_SELECTED",
        "NEXT_BLOCK_RESTORE_POINT_PLANNING_SELECTED",
        "NEXT_BLOCK_CONTINUITY_AUDIT_SELECTED",
        "NEXT_BLOCK_SELECTION_BLOCKED_NEEDS_MORE_REVIEW",
    ]
    decisions = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed
    ]
    assert decisions == [
        "NEXT_BLOCK_LOWER_CONSOLE_EXISTING_ELEMENTS_AUDIT_SELECTED"
    ]
    assert (
        "PROMPT UI/UX 1.114 - Auditar elementos inferiores existentes del Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_plan_document_records_common_safety_limits():
    text = read_doc()
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
        "no contrato final",
        "no fake success",
        "no ghost actions",
        "IA_CORE",
    ]:
        assert marker in text or marker.lower() in lower


def test_plan_document_records_scope_preservation():
    text = read_doc()
    lower = text.lower()
    for marker in [
        "no pantalla",
        "no quinta sección",
        "no UI activa",
        "no Final Screen Contracts",
        "no elementos inferiores",
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
        "No se avanzó a 1.114",
    ]:
        assert marker in text or marker.lower() in lower

