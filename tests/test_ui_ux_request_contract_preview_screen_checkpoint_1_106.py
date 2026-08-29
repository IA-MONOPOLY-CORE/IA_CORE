from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_REQUEST_CONTRACT_PREVIEW_SCREEN_CHECKPOINT_1_106.md"
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


def test_checkpoint_document_exists_and_records_base_state():
    text = read(DOC)
    for marker in [
        "UI/UX Request Contract Preview Screen Checkpoint 1.106",
        "4a824ea",
        "c37f1bf",
        "4e30238",
        "f4481d4",
        "ca4baff",
        "8353702",
        "1.101",
        "1.102",
        "1.103",
        "1.104",
        "1.105",
        "1.106",
        "NEXT_STEP_REQUEST_CONTRACT_PREVIEW_GUARDRAILS_SELECTED",
        "REQUEST_CONTRACT_PREVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "REQUEST_CONTRACT_PREVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "REQUEST_CONTRACT_PREVIEW_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "REQUEST_CONTRACT_PREVIEW_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "HUMAN_VISUAL_REVIEW_APPROVED",
    ]:
        assert marker in text


def test_checkpoint_document_records_single_final_affordance_decision():
    text = read(DOC)
    allowed_results = [
        "REQUEST_CONTRACT_PREVIEW_FINAL_AFFORDANCE_AUDIT_PASSED",
        "REQUEST_CONTRACT_PREVIEW_FINAL_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "REQUEST_CONTRACT_PREVIEW_FINAL_AFFORDANCE_AUDIT_BLOCKED_NEEDS_MINOR_FIX",
        "REQUEST_CONTRACT_PREVIEW_FINAL_AFFORDANCE_AUDIT_BLOCKED_CRITICAL",
    ]
    decision_lines = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed_results
    ]
    assert decision_lines == [
        "REQUEST_CONTRACT_PREVIEW_FINAL_AFFORDANCE_AUDIT_PASSED_WITH_NOTES"
    ]
    assert (
        "Auditoria final anti-CTA/anti-affordance" in text
        or "Auditoría final anti-CTA/anti-affordance" in text
    )


def test_checkpoint_document_contains_visual_review_and_contract_semantics():
    text = read(DOC)
    required = [
        "Request Contract Preview",
        "CFD-04",
        "FSC-RCP-04",
        "id UI propuesto",
        "draft / not final",
        "DEFER_FINALIZATION",
        "sin contrato final",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "documental",
        "read-only",
        "contract-aware",
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
        "correcta",
        "ordenada",
        "coherente",
        "cuarta sección hermana",
        "preview documental/read-only",
        "no flujo operativo",
        "chips, labels, pills, notices y bloques laterales",
    ]
    for marker in required:
        assert marker in text
    assert (
        "sin implementación operativa" in text
        or "sin implementacion operativa" in text
    )


def test_checkpoint_document_records_guardrails_baseline_and_validations():
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
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "node checks",
        "git diff --check",
        "backend contract tests",
        "backup readiness",
        "PROMPT UI/UX 1.107 - Planificar siguiente paso tras Request Contract Preview IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text or marker.lower() in lower


def test_checkpoint_document_records_scope_limits():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "no se implementó pantalla adicional",
        "no se modificó UI activa",
        "no se modificó Request Contract Preview en checkpoint",
        "no se creó contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se tocó backend/runtime/endpoints/CI/dependencias",
        "no se limpió deuda residual",
        "no se corrigieron pyflakes",
        "no se avanzó al prompt siguiente",
    ]:
        assert marker in text or marker.lower() in lower


def test_checkpoint_document_classifies_required_visual_elements():
    text = read(DOC)
    for marker in [
        "Header",
        "`CFD-04`",
        "`FSC-RCP-04`",
        "`draft / not final`",
        "`DEFER_FINALIZATION`",
        "status strip",
        "Request vs Submit",
        "Preview vs Dispatch",
        "Draft / Deferred",
        "Payload Summary Safe",
        "Allowed Actions Declared",
        "Forbidden Actions / Boundaries",
        "Evidence Snapshot",
        "Triple Baseline References",
        "Anti-affordance Notice",
        "chips/labels/pills visibles",
        "bloque lateral si existe",
        "READ_ONLY_LABEL",
        "DOCUMENTATION_REFERENCE",
        "NON_OPERATIONAL_STATUS",
        "SAFE_SUMMARY",
        "BOUNDARY_NOTICE",
        "AMBIGUOUS_AFFORDANCE",
    ]:
        assert marker in text
    assert "OPERATIONAL_CTA_BLOCKER" in text


def test_request_preview_html_remains_fourth_read_only_section():
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
        "id UI propuesto",
        "draft / not final",
        "DEFER_FINALIZATION",
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
    ]:
        assert marker in section


def test_request_preview_html_has_no_operational_affordances():
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


def test_readmes_record_checkpoint_cursor():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "request contract preview screen checkpoint 1.106" in lower
        assert (
            "request_contract_preview_final_affordance_audit_passed_with_notes"
            in lower
        )
        assert "human_visual_review_approved" in lower
        assert "baseline visual/contractual de cuatro secciones" in lower
        assert "contract overview" in lower
        assert "blocked & forbidden" in lower
        assert "validation & readiness" in lower
        assert "request contract preview" in lower
        assert "prompt ui/ux 1.107 - planificar siguiente paso tras request contract preview" in lower
        assert "no implementación adicional" in lower or "no implementacion adicional" in lower
