from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_STEP_AFTER_VALIDATION_READINESS_PLAN_1_101.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_received_state():
    text = read(DOC)
    required = (
        "UI/UX Next Step After Validation & Readiness Plan 1.101",
        "c37f1bf",
        "VALIDATION_READINESS_SCREEN_CHECKPOINT_CLOSED_AND_PUBLISHED",
        "VALIDATION_READINESS_FINAL_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "HUMAN_VISUAL_REVIEW_APPROVED",
        "triple baseline",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "Request Contract Preview",
        "diferido",
        "Opciones evaluadas",
        "Matriz de decision",
    )
    assert all(marker in text for marker in required)


def test_plan_selects_guardrails_and_records_safety_contract():
    text = read(DOC)
    required = (
        "NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED",
        "request no submit",
        "preview no dispatch",
        "contract preview no raw Package",
        "payload summary no payload crudo",
        "allowed actions no CTA",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no runtime",
        "no execution",
        "no delivery",
        "no confirmation gate activo",
        "no state mutation",
        "no success operativo",
        "no route/hash",
        "anti-affordance audit obligatoria",
        "Risk register especifico",
        "RCP-001",
        "RCP-021",
    )
    assert all(marker in text for marker in required)


def test_plan_records_future_sequence_and_exact_next_prompt():
    text = read(DOC)
    assert "1.102" in text
    assert "1.103" in text
    assert "1.104" in text
    assert "1.105" in text
    assert "1.106" in text
    assert "PROMPT UI/UX 1.102 - Preparar guardrails pre-implementacion Request Contract Preview IA_CORE contract-aware sin runtime/no-execution" in text
    assert "No se avanzó a 1.102" in text


def test_plan_records_all_preserved_limits():
    text = read(DOC)
    required = (
        "No se implementó pantalla",
        "No se modificó UI activa",
        "No se tocó Contract Overview",
        "No se tocó Blocked & Forbidden",
        "No se tocó Validation & Readiness",
        "No se implementó Request Contract Preview",
        "No se creó User Panel",
        "No se crearon rutas/hash",
        "No se tocaron backend, runtime, endpoints, CI ni dependencias",
        "No se limpió deuda residual",
        "No se corrigieron pyflakes",
        "No se hizo push",
        "no pantalla",
        "no UI activa",
        "no Contract Overview",
        "no Blocked & Forbidden",
        "no Validation & Readiness",
        "no Request Contract Preview",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no runtime",
        "no endpoint",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "No se avanzó a 1.102",
    )
    assert all(marker in text for marker in required)


def test_readmes_record_plan_and_push_postponed():
    for path in (README, WEB_README):
        text = read(path)
        assert "Next Step After Validation & Readiness Plan 1.101" in text
        assert "NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED" in text
        assert "PROMPT UI/UX 1.102 - Preparar guardrails pre-implementacion Request Contract Preview" in text
        assert "no se implementó pantalla" in text.lower()
        assert "push pospuesto" in text.lower()
