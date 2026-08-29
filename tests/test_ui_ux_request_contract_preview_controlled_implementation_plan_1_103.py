from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_1_103.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_exists_and_has_base_state():
    text = read(DOC)
    required = [
        "UI/UX Request Contract Preview Controlled Implementation Plan 1.103",
        "f4481d4",
        "c37f1bf",
        "REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED",
        "Request Contract Preview",
        "CFD-04",
        "FSC-RCP-04",
        "UI proposed id",
        "draft / not final",
        "DEFER_FINALIZATION",
        "sin contrato final",
        "sin implementacion",
        "triple baseline",
        "Contract Overview",
        "Blocked & Forbidden",
        "Validation & Readiness",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
    ]
    for marker in required:
        assert marker in text


def test_plan_has_required_policy_sections():
    text = read(DOC)
    for heading in [
        "Alcance implementable futuro",
        "Alcance prohibido futuro",
        "Candidate future implementation files",
        "Prohibited files",
        "Future placement strategy",
        "Future visual structure",
        "Data policy",
        "State policy",
        "Copy policy",
        "Affordance policy",
        "Controlled implementation strategy",
        "Future tests required",
        "Entry criteria",
        "Exit criteria",
        "Rollback strategy",
        "Risk register",
    ]:
        assert f"## {heading}" in text


def test_plan_has_copy_separation_markers():
    text = read(DOC)
    for marker in [
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
    ]:
        assert marker in text


def test_plan_has_negative_runtime_and_scope_markers():
    text = read(DOC)
    for marker in [
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
        "no contrato final",
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
    ]:
        assert marker in text


def test_plan_has_decision_and_exact_next_prompt():
    text = read(DOC)
    allowed = {
        "REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "REQUEST_CONTRACT_PREVIEW_NEEDS_IMPLEMENTATION_PREFLIGHT",
        "REQUEST_CONTRACT_PREVIEW_NEEDS_MORE_PLANNING",
        "REQUEST_CONTRACT_PREVIEW_IMPLEMENTATION_DEFERRED",
    }
    decisions = [marker for marker in allowed if marker in text]
    assert decisions == ["REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY"]
    assert (
        "PROMPT UI/UX 1.104 - Implementar Request Contract Preview "
        "IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_plan_declares_no_implementation_and_no_advance():
    text = read(DOC)
    lower = text.lower()
    assert "no se implemento pantalla" in lower or "no se implementó pantalla" in lower
    assert "no se modifico ui activa" in lower or "no se modificó ui activa" in lower
    assert "no se implemento request contract preview" in lower or "no se implementó request contract preview" in lower
    assert "no se creo contrato final" in lower or "no se creó contrato final" in lower
    assert "no se contradijo `defer_finalization`" in lower
    assert "no se avanzo a 1.104" in lower or "no se avanzó a 1.104" in lower


def test_readmes_record_cursor_and_defer():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "request contract preview controlled implementation plan 1.103" in lower
        assert "request_contract_preview_controlled_implementation_plan_ready" in lower
        assert "prompt ui/ux 1.104 - implementar request contract preview" in lower
        assert "no se implemento pantalla" in lower or "no se implementó pantalla" in lower
        assert "push pospuesto" in lower
