from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_1_102.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_guardrails_document_exists_and_records_received_state():
    text = read(DOC)
    required = (
        "UI/UX Request Contract Preview Pre-Implementation Guardrails 1.102",
        "4e30238",
        "c37f1bf",
        "NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "triple baseline",
        "Request Contract Preview",
        "CFD-04",
        "draft / not final",
        "DEFER_FINALIZATION",
        "sin contrato final",
        "sin implementacion",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "read-only",
        "contract-aware",
        "diferido",
        "push pospuesto",
    )
    assert all(marker in text for marker in required)


def test_guardrails_document_contains_required_semantic_boundaries():
    text = read(DOC)
    required = (
        "request no submit",
        "preview no dispatch",
        "contract preview no raw Package",
        "payload summary no payload crudo",
        "allowed actions no CTA",
        "confirmation gate documented no active gate",
        "request shape no state mutation",
        "preview state no delivery",
        "evidence no live log",
        "draft no ready",
        "deferred no implementado",
        "readable contract no executable payload",
        "human review no approval to run",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no runtime",
        "no execution",
        "no dispatch",
        "no delivery",
        "no confirmation gate activo",
        "no state mutation",
        "no success operativo",
        "no route/hash",
        "no raw Package",
        "no payload crudo",
        "anti-affordance audit obligatoria",
        "revision visual humana obligatoria",
        "checkpoint propio antes de push",
    )
    assert all(marker in text for marker in required)


def test_guardrails_document_contains_required_sections_and_registers():
    text = read(DOC)
    required = (
        "Datos permitidos",
        "Datos prohibidos",
        "Estados permitidos",
        "Estados prohibidos",
        "Acciones UI prohibidas",
        "Copy permitido",
        "Copy obligatorio",
        "Copy prohibido",
        "Affordances permitidas y prohibidas",
        "Estructura visual futura",
        "Visual severity",
        "Tests futuros minimos",
        "Entry criteria",
        "Exit criteria",
        "Risk register",
        "RCP-102-001",
        "RCP-102-027",
    )
    assert all(marker in text for marker in required)


def test_guardrails_document_selects_ready_and_next_prompt():
    text = read(DOC)
    decision = "REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY"
    allowed = (
        decision,
        "REQUEST_CONTRACT_PREVIEW_NEEDS_MORE_PRE_IMPLEMENTATION_AUDIT",
        "REQUEST_CONTRACT_PREVIEW_REMAINS_DEFERRED",
        "REQUEST_CONTRACT_PREVIEW_SELECTION_REQUIRES_REVIEW",
    )
    assert any(item in text for item in allowed)
    assert decision in text
    assert "PROMPT UI/UX 1.103 - Preparar plan de implementacion controlada Request Contract Preview IA_CORE contract-aware sin runtime/no-execution" in text
    assert "No se avanzo a 1.103" in text


def test_guardrails_document_preserves_no_scope():
    text = read(DOC)
    required = (
        "No se implemento pantalla",
        "No se modifico UI activa",
        "No se toco Contract Overview",
        "No se toco Blocked & Forbidden",
        "No se toco Validation & Readiness",
        "No se implemento Request Contract Preview",
        "No se creo contrato final",
        "No se contradijo `DEFER_FINALIZATION`",
        "No se creo User Panel",
        "No se crearon rutas/hash",
        "No se tocaron backend, runtime, endpoints, CI ni dependencias",
        "No se limpio deuda residual",
        "No se corrigieron pyflakes",
        "No se hizo push",
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
        "no fetch",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
    )
    assert all(marker in text for marker in required)


def test_readmes_record_guardrails_cursor_and_push_postponed():
    for path in (README, WEB_README):
        text = read(path)
        assert "Request Contract Preview Pre-Implementation Guardrails 1.102" in text
        assert "CFD-04" in text
        assert "draft / not final" in text
        assert "DEFER_FINALIZATION" in text
        assert "REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY" in text
        assert "PROMPT UI/UX 1.103 - Preparar plan de implementacion controlada Request Contract Preview" in text
        lower = text.lower()
        assert "no se implemento pantalla" in lower or "no se implementó pantalla" in lower
        assert "push pospuesto" in lower
