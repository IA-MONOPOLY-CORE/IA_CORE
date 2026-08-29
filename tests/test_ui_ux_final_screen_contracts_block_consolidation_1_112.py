from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATION_1_112.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_consolidation_document_exists_and_records_base_state():
    text = read_doc()
    for marker in [
        "UI/UX Final Screen Contracts Block Consolidation 1.112",
        "0403422",
        "ccdef7a",
        "NEXT_STEP_FINAL_SCREEN_CONTRACTS_CONSOLIDATION_SELECTED",
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
        "Mapa final del bloque",
        "Tabla de decisiones",
        "Tabla de restore points",
        "Riesgos residuales consolidados",
    ]:
        assert marker in text


def test_consolidation_document_records_history_and_decisions():
    text = read_doc()
    for marker in [
        "1.88",
        "1.94",
        "1.100",
        "1.106",
        "1.107",
        "1.108",
        "1.109",
        "1.110",
        "1.111",
        "9143c88",
        "97ee5e3",
        "ce39754",
        "NEXT_STEP_FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_SELECTED",
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_PASSED_NEEDS_MINOR_HARDENING",
        "FOUR_SCREEN_BASELINE_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_DENSITY_NEEDS_MINOR_HARDENING",
        "FOUR_SCREEN_BASELINE_RESPONSIVE_OK_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_INTEGRATION_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "FOUR_SCREEN_BASELINE_POST_HARDENING_AFFORDANCE_PASSED_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_POST_HARDENING_DENSITY_IMPROVED_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_POST_HARDENING_RESPONSIVE_OK_WITH_NOTES",
        "HUMAN_VISUAL_REVIEW_APPROVED_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_PASSED_WITH_NOTES",
    ]:
        assert marker in text


def test_consolidation_document_records_common_limits_and_boundary():
    text = read_doc()
    lower = text.lower()
    for marker in [
        "documental",
        "read-only",
        "contract-aware",
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
        "no delivery",
        "no confirmation gate activo",
        "no state mutation",
        "DEFER_FINALIZATION",
        "no raw Package",
        "no payload crudo",
        "no ghost actions",
        "no fake success",
        "no contrato final",
        "IA_CORE",
        "Lotería/SAAOP no identidad activa",
        "elementos inferiores",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "CFG",
        "DOMAIN",
    ]:
        assert marker in text or marker.lower() in lower


def test_consolidation_document_selects_one_allowed_final_decision_and_next_prompt():
    text = read_doc()
    allowed = [
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATED_READY_FOR_NEXT_STEP_PLANNING",
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATED_NEEDS_LOWER_CONSOLE_AUDIT_NEXT",
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATED_NEEDS_GLOBAL_DENSITY_REVIEW_NEXT",
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATION_BLOCKED_NEEDS_FIX",
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATION_BLOCKED_CRITICAL",
    ]
    decisions = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed
    ]
    assert decisions == [
        "FINAL_SCREEN_CONTRACTS_BLOCK_CONSOLIDATED_READY_FOR_NEXT_STEP_PLANNING"
    ]
    assert (
        "PROMPT UI/UX 1.113 - Planificar siguiente bloque tras consolidacion Final Screen Contracts IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_consolidation_document_records_preserved_safety_limits():
    text = read_doc()
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
        "No se avanzó a 1.113",
    ]:
        assert marker in text or marker.lower() in lower

