from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FOUR_SCREEN_BASELINE_INTEGRATION_CHECKPOINT_1_110.md"
HTML = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_sequence():
    text = read(DOC)
    required = [
        "UI/UX Four Screen Baseline Integration Checkpoint 1.110",
        "ce39754",
        "ec0e25f",
        "9143c88",
        "97ee5e3",
        "1.107",
        "1.108",
        "1.109",
        "1.110",
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
    ]
    for marker in required:
        assert marker in text


def test_checkpoint_document_records_baseline_and_boundaries():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "baseline de cuatro secciones",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Validation & Readiness",
        "FSC-VR-03",
        "Request Contract Preview",
        "FSC-RCP-04",
        "CFD-04",
        "DEFER_FINALIZATION",
        "draft / not final",
        "sin contrato final",
        "Panel Maestro",
        "documental",
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
        "no raw Package",
        "no payload crudo",
        "no fake success",
        "no ghost actions",
        "no pantalla nueva",
        "no contrato funcional",
        "no contrato final",
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
    ]:
        assert marker in text or marker.lower() in lower
    assert "sin implementación operativa" in text or "sin implementacion operativa" in lower
    assert "read-only" in text or "solo lectura" in lower
    assert "no quinta sección" in text or "no quinta seccion" in lower


def test_checkpoint_document_has_single_allowed_audit_result_and_push_rule():
    text = read(DOC)
    allowed = [
        "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_PASSED",
        "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_PASSED_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_BLOCKED_NEEDS_MINOR_FIX",
        "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_BLOCKED_CRITICAL",
    ]
    assert "FOUR_SCREEN_BASELINE_CHECKPOINT_AUDIT_PASSED_WITH_NOTES" in text
    assert any(marker in text for marker in allowed)
    assert "Regla de push" in text
    assert "nuevo restore point remoto" in text
    assert (
        "PROMPT UI/UX 1.111 - Planificar siguiente paso tras checkpoint baseline de cuatro secciones IA_CORE contract-aware sin runtime/no-execution"
        in text
    )
    for marker in [
        "No se implementó pantalla nueva",
        "No se agregó quinta sección",
        "No se modificó UI activa",
        "No se modificó contrato funcional",
        "No se avanzó a 1.111",
    ]:
        assert marker in text


def test_current_html_preserves_four_screen_baseline_checkpoint():
    text = read(HTML)
    sections = [
        'id="contract-overview-screen"',
        'id="blocked-forbidden-screen"',
        'id="validation-readiness-screen"',
        'id="request-contract-preview-screen"',
    ]
    positions = [text.index(marker) for marker in sections]
    assert positions == sorted(positions)
    for marker in sections:
        assert text.count(marker) == 1
    assert text.count('data-contract-screen="') == 4

    for marker in [
        "Contract Overview",
        "Blocked &amp; Forbidden",
        "Validation &amp; Readiness",
        "Request Contract Preview",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "CFD-04",
        "DEFER_FINALIZATION",
        "draft / not final",
        "no runtime",
        "no execution",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no submit",
        "no dispatch",
    ]:
        assert marker in text


def test_current_html_has_no_operational_affordance_inside_baseline_region():
    text = read(HTML)
    start = text.index('class="four-screen-baseline-summary"')
    end = text.index('id="request-contract-preview-note"')
    baseline_region = text[start:end]

    assert "<section class=\"four-screen-baseline-summary\"" not in baseline_region
    for forbidden in [
        'href="#',
        "onclick",
        "fetch(",
        "window.location.hash",
    ]:
        assert forbidden not in baseline_region

    assert "BLOQUEADO POR CONTRATO" in text
    assert text.index("BLOQUEADO POR CONTRATO") > end


def test_readmes_record_1_110_cursor():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "four screen baseline integration checkpoint 1.110" in lower
        assert "human_visual_review_approved_with_notes" in lower
        assert "four_screen_baseline_checkpoint_audit_passed_with_notes" in lower
        assert "baseline de cuatro secciones" in lower
        assert "nuevo restore point remoto" in lower
        assert (
            "prompt ui/ux 1.111 - planificar siguiente paso tras checkpoint baseline de cuatro secciones ia_core contract-aware sin runtime/no-execution"
            in lower
        )
        assert "no implementación adicional" in lower or "no implementacion adicional" in lower
