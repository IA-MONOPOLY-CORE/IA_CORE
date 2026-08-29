from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_REQUEST_CONTRACT_PREVIEW_SCREEN_IMPLEMENTATION_1_104.md"
HTML = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def request_preview_section() -> str:
    text = read(HTML)
    start = text.index('<section class="request-contract-preview-screen')
    end = text.index("</section>", start) + len("</section>")
    return text[start:end]


def test_implementation_document_has_base_and_contract_state():
    text = read(DOC)
    required = [
        "UI/UX Request Contract Preview Screen Implementation 1.104",
        "ca4baff",
        "c37f1bf",
        "4e30238",
        "f4481d4",
        "REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED",
        "Request Contract Preview",
        "CFD-04",
        "FSC-RCP-04",
        "id UI propuesto",
        "draft / not final",
        "DEFER_FINALIZATION",
        "sin contrato final",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "read-only",
        "contract-aware",
    ]
    for marker in required:
        assert marker in text


def test_implementation_document_has_all_blocks_and_semantics():
    text = read(DOC)
    for marker in [
        "Header",
        "Status strip documental",
        "Request vs Submit",
        "Preview vs Dispatch",
        "Draft / Deferred",
        "Payload Summary Safe",
        "Allowed Actions Declared",
        "Forbidden Actions / Boundaries",
        "Evidence Snapshot",
        "Triple Baseline References",
        "Anti-affordance Notice",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
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


def test_implementation_document_has_scope_and_decision():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "no submit",
        "no send",
        "no dispatch",
        "no run",
        "no execute",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no route/hash",
        "no runtime",
        "no execution",
        "no delivery",
        "no confirmation gate activo",
        "no state mutation",
        "no raw Package",
        "no payload crudo",
        "no fake success",
        "no ghost actions",
        "no contrato final",
        "no contradiccion de `DEFER_FINALIZATION`",
        "no se implemento mas de una pantalla",
        "no se modifico Contract Overview",
        "no se modifico Blocked & Forbidden",
        "no se modifico Validation & Readiness",
        "no se creo contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se hizo push",
        "no se avanzo a 1.105",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "PROMPT UI/UX 1.105 - Hardening visual y contractual Request Contract Preview IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text or marker.lower() in lower


def test_request_preview_is_the_fourth_sibling_and_has_all_blocks():
    text = read(HTML)
    positions = [
        text.index('id="contract-overview-screen"'),
        text.index('id="blocked-forbidden-screen"'),
        text.index('id="validation-readiness-screen"'),
        text.index('id="request-contract-preview-screen"'),
    ]
    assert positions == sorted(positions)
    section = request_preview_section()
    assert section.count("<article") == 9
    assert section.count("<button") == 0
    for marker in [
        "Request Contract Preview",
        "CFD-04",
        "FSC-RCP-04",
        "id UI propuesto",
        "draft / not final",
        "DEFER_FINALIZATION",
        "sin contrato final",
        "sin implementación operativa",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
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
        "no raw Package",
        "no payload crudo",
        "no fake success",
        "no ghost actions",
    ]:
        assert marker in section
    for block in [
        "Request vs Submit",
        "Preview vs Dispatch",
        "Draft / Deferred",
        "Payload Summary Safe",
        "Allowed Actions Declared",
        "Forbidden Actions / Boundaries",
        "Evidence Snapshot",
        "Triple Baseline References",
        "Anti-affordance Notice",
    ]:
        assert block in section


def test_request_preview_has_no_operational_controls_or_navigation():
    section = request_preview_section()
    for marker in [
        "<button",
        'role="button"',
        "href=\"#",
        "onclick",
        "fetch(",
        "window.location.hash",
        ">Submit<",
        ">Send<",
        ">Dispatch<",
        ">Run<",
        ">Execute<",
        ">Start<",
        ">Launch<",
        ">Continue<",
        ">Next<",
        ">Publish<",
        ">Deliver<",
        ">Retry<",
        ">Re-run<",
        ">Validate live<",
        ">Fetch preview<",
        ">Refresh backend<",
        ">Open endpoint<",
        ">Open User Panel<",
        ">Copy raw payload<",
        ">Copy raw Package<",
        ">Download package<",
        ">Approve request<",
        ">Activate gate<",
    ]:
        assert marker not in section


def test_readmes_record_implementation_cursor():
    for path in (README, WEB_README):
        text = read(path).lower()
        assert "request contract preview screen implementation 1.104" in text
        assert "request_contract_preview_screen_implemented_needs_hardening" in text
        assert "prompt ui/ux 1.105 - hardening visual y contractual request contract preview" in text
        assert "defer_finalization" in text
        assert "hardening 1.105" in text
        assert "revision visual humana" in text
        assert "checkpoint/push 1.106" in text
        assert "push pospuesto" in text
