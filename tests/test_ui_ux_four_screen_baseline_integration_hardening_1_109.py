from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FOUR_SCREEN_BASELINE_INTEGRATION_HARDENING_1_109.md"
HTML = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_hardening_document_exists_and_records_received_state():
    text = read(DOC)
    required = [
        "UI/UX Four Screen Baseline Integration Hardening 1.109",
        "97ee5e3",
        "ec0e25f",
        "9143c88",
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_PASSED_NEEDS_MINOR_HARDENING",
        "FOUR_SCREEN_BASELINE_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "FOUR_SCREEN_BASELINE_DENSITY_NEEDS_MINOR_HARDENING",
        "FOUR_SCREEN_BASELINE_RESPONSIVE_OK_WITH_NOTES",
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
        "contract-aware",
    ]
    for marker in required:
        assert marker in text
    assert "read-only" in text or "solo lectura" in text


def test_hardening_document_records_contractual_boundaries():
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


def test_hardening_document_has_required_sections_results_and_prompt():
    text = read(DOC)
    for marker in [
        "Hallazgos 1.108 atendidos",
        "Cambios aplicados",
        "Cambios NO aplicados",
        "Auditoría post-hardening de orden",
        "Auditoría post-hardening de identidad",
        "Auditoría post-hardening de roles",
        "Auditoría post-hardening de semántica común",
        "Auditoría post-hardening anti-affordance",
        "Auditoría post-hardening densidad/legibilidad",
        "Auditoría post-hardening responsive",
    ]:
        assert marker in text

    assert "FOUR_SCREEN_BASELINE_POST_HARDENING_AFFORDANCE_PASSED_WITH_NOTES" in text
    assert "FOUR_SCREEN_BASELINE_POST_HARDENING_DENSITY_IMPROVED_WITH_NOTES" in text
    assert "FOUR_SCREEN_BASELINE_POST_HARDENING_RESPONSIVE_OK_WITH_NOTES" in text
    assert "FOUR_SCREEN_BASELINE_INTEGRATION_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW" in text
    assert (
        "PROMPT UI/UX 1.110 - Checkpoint integracion baseline de cuatro secciones Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_hardening_document_records_scope_limits_explicitly():
    text = read(DOC)
    lower = text.lower()
    for marker in [
        "no pantalla nueva",
        "no quinta sección",
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
        "No se implementó pantalla nueva",
        "No se agregó quinta sección",
        "No se modificó contrato funcional",
        "No se avanzó a 1.110",
    ]:
        assert marker in text or marker.lower() in lower


def test_current_html_preserves_four_screen_order_and_ids():
    text = read(HTML)
    ids = [
        'id="contract-overview-screen"',
        'id="blocked-forbidden-screen"',
        'id="validation-readiness-screen"',
        'id="request-contract-preview-screen"',
    ]
    positions = [text.index(marker) for marker in ids]
    assert positions == sorted(positions)
    for marker in ids:
        assert text.count(marker) == 1

    for marker in [
        'data-contract-screen="FSC-CO-01"',
        'data-contract-screen="FSC-BF-02"',
        'data-contract-screen="FSC-VR-03"',
        'data-contract-screen="FSC-RCP-04"',
        'data-contract-document="CFD-04"',
    ]:
        assert text.count(marker) == 1

    for marker in [
        "Contract Overview",
        "Blocked &amp; Forbidden",
        "Validation &amp; Readiness",
        "Request Contract Preview",
        "DEFER_FINALIZATION",
        "no runtime",
        "no execution",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no submit",
        "no dispatch",
    ]:
        assert marker in text


def test_current_html_adds_non_operational_summary_without_fifth_section():
    text = read(HTML)
    assert 'class="four-screen-baseline-summary"' in text
    assert 'data-four-screen-baseline-summary="1.109"' in text
    assert "<section class=\"four-screen-baseline-summary\"" not in text
    assert text.index('class="four-screen-baseline-summary"') < text.index(
        'id="contract-overview-screen"'
    )

    baseline_region = text[
        text.index('class="four-screen-baseline-summary"') : text.index(
            'id="request-contract-preview-note"'
        )
    ]
    for forbidden in [
        'href="#',
        "onclick",
        "fetch(",
        "window.location.hash",
    ]:
        assert forbidden not in baseline_region


def test_readmes_record_1_109_cursor():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "four screen baseline integration hardening 1.109" in lower
        assert "baseline de cuatro secciones" in lower
        assert "four_screen_baseline_post_hardening_affordance_passed_with_notes" in lower
        assert "four_screen_baseline_post_hardening_density_improved_with_notes" in lower
        assert "four_screen_baseline_integration_hardened_ready_for_human_visual_review" in lower
        assert (
            "prompt ui/ux 1.110 - checkpoint integracion baseline de cuatro secciones panel maestro ia_core contract-aware sin runtime/no-execution"
            in lower
        )
        assert "revisión visual humana" in lower or "revision visual humana" in lower
        assert "push pospuesto" in lower
