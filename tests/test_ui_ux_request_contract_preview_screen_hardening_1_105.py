from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENING_1_105.md"
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


def test_hardening_document_exists_and_records_base_state():
    text = read(DOC)
    required = [
        "UI/UX Request Contract Preview Screen Hardening 1.105",
        "8353702",
        "c37f1bf",
        "4e30238",
        "f4481d4",
        "ca4baff",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
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
        "Auditoría visual contractual inicial",
        "Affordance audit result",
    ]
    for marker in required:
        assert marker in text
    assert (
        "sin implementación operativa" in text
        or "sin implementacion operativa" in text
    )


def test_hardening_document_has_audit_result_semantics_and_blocks():
    text = read(DOC)
    allowed_results = [
        "REQUEST_CONTRACT_PREVIEW_AFFORDANCE_AUDIT_PASSED",
        "REQUEST_CONTRACT_PREVIEW_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "REQUEST_CONTRACT_PREVIEW_AFFORDANCE_AUDIT_BLOCKED_NEEDS_MINOR_FIX",
        "REQUEST_CONTRACT_PREVIEW_AFFORDANCE_AUDIT_BLOCKED_CRITICAL",
    ]
    assert any(marker in text for marker in allowed_results)
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
        "Header",
        "Status strip",
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
    ]:
        assert marker in text


def test_hardening_document_has_final_decision_scope_and_next_prompt():
    text = read(DOC)
    allowed_decisions = [
        "REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENING_BLOCKED_NEEDS_MINOR_FIX",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENING_BLOCKED_CRITICAL",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENING_ROLLED_BACK",
    ]
    decisions = [marker for marker in allowed_decisions if marker in text]
    assert decisions == [
        "REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW"
    ]
    assert (
        "PROMPT UI/UX 1.106 - Checkpoint Request Contract Preview implementada y "
        "hardenizada IA_CORE contract-aware sin runtime/no-execution"
    ) in text
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
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no se implementó pantalla nueva",
        "no se implementó más de una sección",
        "no se modificó Contract Overview",
        "no se modificó Blocked & Forbidden",
        "no se modificó Validation & Readiness",
        "no se creó contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se hizo push",
        "no se avanzó a 1.106",
    ]:
        assert marker in text or marker.lower() in lower


def test_request_preview_html_has_hardened_markers_and_order():
    text = read(HTML)
    positions = [
        text.index('id="contract-overview-screen"'),
        text.index('id="blocked-forbidden-screen"'),
        text.index('id="validation-readiness-screen"'),
        text.index('id="request-contract-preview-screen"'),
    ]
    assert positions == sorted(positions)
    section = request_preview_section()
    for marker in [
        "Request Contract Preview",
        "CFD-04",
        "FSC-RCP-04",
        "draft / not final",
        "DEFER_FINALIZATION",
        "sin contrato final",
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
        "not rendered as action",
        "Etiquetas documentales no interactivas",
    ]:
        assert marker in section
    assert (
        "sin implementación operativa" in section
        or "sin implementacion operativa" in section
    )


def test_request_preview_html_has_no_operational_controls_or_affordances():
    section = request_preview_section()
    for marker in [
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
        "button",
        'role="button"',
        'href="#',
        "onclick",
        "fetch(",
        "window.location.hash",
    ]:
        assert marker not in section


def test_readmes_record_hardening_cursor():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "request contract preview screen hardening 1.105" in lower
        assert (
            "request_contract_preview_screen_hardened_ready_for_human_visual_review"
            in lower
        )
        assert (
            "request_contract_preview_affordance_audit_passed_with_notes" in lower
        )
        assert "prompt ui/ux 1.106 - checkpoint request contract preview" in lower
        assert "defer_finalization" in lower
        assert "sin contrato final" in lower
        assert "revision visual humana" in lower or "revisión visual humana" in lower
        assert "push pospuesto" in lower
