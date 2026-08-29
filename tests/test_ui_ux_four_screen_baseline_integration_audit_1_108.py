from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_1_108.md"
HTML = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_document_exists_and_records_received_state():
    text = read(DOC)
    required = [
        "UI/UX Four Screen Baseline Integration Audit 1.108",
        "9143c88",
        "ec0e25f",
        "NEXT_STEP_FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_SELECTED",
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
        "read-only",
        "contract-aware",
    ]
    for marker in required:
        assert marker in text


def test_audit_document_records_common_boundaries():
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


def test_audit_document_has_required_audit_sections_and_results():
    text = read(DOC)
    for marker in [
        "Auditoría de orden",
        "Auditoría de identidad",
        "Auditoría de rol de cada sección",
        "Auditoría de semántica común",
        "Auditoría anti-affordance global",
        "Hallazgos clasificados",
        "Matriz de riesgos",
    ]:
        assert marker in text
    assert "FOUR_SCREEN_BASELINE_AFFORDANCE_AUDIT_PASSED_WITH_NOTES" in text
    assert "FOUR_SCREEN_BASELINE_DENSITY_NEEDS_MINOR_HARDENING" in text
    assert "FOUR_SCREEN_BASELINE_RESPONSIVE_OK_WITH_NOTES" in text


def test_audit_document_has_single_final_decision_and_matching_prompt():
    text = read(DOC)
    allowed_decisions = [
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_PASSED_READY_FOR_CONSOLIDATION",
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_PASSED_NEEDS_MINOR_HARDENING",
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_NEEDS_GLOBAL_DENSITY_REVIEW",
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_BLOCKED_NEEDS_FIX",
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_BLOCKED_CRITICAL",
    ]
    decisions = [
        line.strip("` ")
        for line in text.splitlines()
        if line.strip("` ") in allowed_decisions
    ]
    assert decisions == [
        "FOUR_SCREEN_BASELINE_INTEGRATION_AUDIT_PASSED_NEEDS_MINOR_HARDENING"
    ]
    assert (
        "PROMPT UI/UX 1.109 - Hardening menor integracion baseline de cuatro secciones Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_audit_document_records_scope_limits():
    text = read(DOC)
    lower = text.lower()
    for marker in [
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
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no push",
        "no se implementó pantalla",
        "no se modificó UI activa",
        "no se avanzó a 1.109",
    ]:
        assert marker in text or marker.lower() in lower


def test_current_html_preserves_four_screen_order_and_no_duplicates():
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
        "DEFER_FINALIZATION",
    ]:
        assert marker in text


def test_readmes_record_1_108_cursor():
    for path in (README, WEB_README):
        text = read(path)
        lower = text.lower()
        assert "four screen baseline integration audit 1.108" in lower
        assert "baseline de cuatro secciones" in lower
        assert "four_screen_baseline_affordance_audit_passed_with_notes" in lower
        assert "four_screen_baseline_density_needs_minor_hardening" in lower
        assert "four_screen_baseline_integration_audit_passed_needs_minor_hardening" in lower
        assert (
            "prompt ui/ux 1.109 - hardening menor integracion baseline de cuatro secciones panel maestro ia_core contract-aware sin runtime/no-execution"
            in lower
        )
        assert "no implementación" in lower or "no implementacion" in lower
        assert "push pospuesto" in lower
