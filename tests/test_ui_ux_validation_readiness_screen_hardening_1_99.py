from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_SCREEN_HARDENING_1_99.md"
TEST = ROOT / "tests" / "test_ui_ux_validation_readiness_screen_hardening_1_99.py"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validation_readiness_section(text: str) -> str:
    start = text.index('<section class="validation-readiness-screen')
    end = text.index("</section>", start) + len("</section>")
    return text[start:end]


def test_hardening_artifacts_exist():
    assert DOC.exists()
    assert TEST.exists()


def test_hardening_document_contains_identity_and_state():
    text = read(DOC)
    required = (
        "UI/UX Validation & Readiness Screen Hardening 1.99",
        "d89da91",
        "7ad9a8b",
        "4299b0b",
        "c5518a4",
        "9a3dfd6",
        "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
        "VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "VALIDATION_READINESS_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "Contract Overview",
        "Blocked & Forbidden",
        "Request Contract Preview",
        "Auditoría anti-CTA/anti-affordance",
        "VALIDATION_READINESS_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "VALIDATION_READINESS_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "PROMPT UI/UX 1.100 - Checkpoint Validation & Readiness Screen implementada y hardenizada IA_CORE contract-aware sin runtime/no-execution",
    )
    assert all(marker in text for marker in required)


def test_hardening_document_contains_boundaries_and_limits():
    text = read(DOC)
    required = (
        "no-runtime",
        "no-execution",
        "no-dispatch",
        "no-endpoint",
        "no-fetch",
        "no-user-panel",
        "no rutas/hash",
        "no unlock",
        "no override",
        "no bypass",
        "no fake success",
        "no ghost actions",
        "no raw Package",
        "no live log",
        "no push",
        "no checkpoint",
        "no visual approval",
        "no backend",
        "no runtime",
        "no execution",
        "no dispatch",
        "no CI",
        "no dependencias",
        "no deuda residual",
        "no pyflakes",
        "no se avanzó a 1.100",
    )
    assert all(marker in text for marker in required)


def test_hardening_document_contains_audit_and_pending_review():
    text = read(DOC)
    required = (
        "Status strip",
        "Readiness vs Permission",
        "Validation vs Execution",
        "Validation Findings",
        "Blockers/warnings/missing requirements",
        "Evidence Snapshot",
        "No Runtime Boundary",
        "Baseline References",
        "Anti-affordance Notice",
        "NON_OPERATIONAL_STATUS",
        "READ_ONLY_LABEL",
        "DOCUMENTATION_REFERENCE",
        "no affordance operativa pendiente",
        "revisión visual humana",
        "visual severity",
        "responsive",
    )
    assert all(marker in text for marker in required)


def test_validation_readiness_preserves_structure_and_semantics():
    text = read(INDEX)
    section = validation_readiness_section(text)
    required = (
        "Validation &amp; Readiness Screen",
        "FSC-VR-03",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "read-only",
        "contract-aware",
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
        "Readiness informa, no habilita",
        "Validation documenta, no ejecuta",
        "Passed no equivale a éxito operativo",
        "Warning/Error no representa runtime vivo",
        "Review required no abre workflow activo",
        "Los blockers permanecen visibles",
        "Sin submit, dispatch ni ejecución",
        "Sin endpoint, fetch ni User Panel",
        "Snapshot documental, no log vivo",
        "Request Contract Preview permanece diferido",
        "no-runtime",
        "no-execution",
        "no-dispatch",
        "no-endpoint",
        "no-user-panel",
    )
    assert all(marker in section for marker in required)
    assert text.index('id="contract-overview-screen"') < text.index('id="blocked-forbidden-screen"') < text.index('id="validation-readiness-screen"')
    assert "Lotería" not in section
    assert "SAAOP" not in section


def test_validation_readiness_has_no_operational_affordances():
    section = validation_readiness_section(read(INDEX))
    prohibited = (
        "<button",
        "<a ",
        "<form",
        "<input",
        "<select",
        "<textarea",
        "href=",
        "fetch(",
        "window.location.hash",
        "data-action=\"run\"",
        "data-action=\"dispatch\"",
        "data-action=\"submit\"",
        "data-action=\"execute\"",
        "data-action=\"retry\"",
        "data-action=\"unlock\"",
        "data-action=\"override\"",
        "data-action=\"bypass\"",
    )
    assert all(marker not in section for marker in prohibited)


def test_hardening_styles_reduce_operational_severity():
    text = read(INDEX)
    assert "letter-spacing: 0;" in text[text.index(".validation-readiness-title h2"):text.index(".validation-readiness-id")]
    assert ".validation-readiness-status .visual-state.blocked" in text
    assert "color: var(--amber);" in text[text.index(".validation-readiness-status .visual-state.blocked"):text.index(".validation-readiness-grid")]
    assert "border-color: rgba(245,158,11,0.42);" in text
    assert "border-color: rgba(0,212,255,0.3);" in text


def test_previous_screen_contracts_remain_single_and_present():
    text = read(INDEX)
    assert text.count('data-contract-screen="FSC-CO-01"') == 1
    assert text.count('data-contract-screen="FSC-BF-02"') == 1
    assert text.count('data-contract-screen="FSC-VR-03"') == 1
    assert text.count('id="contract-overview-screen"') == 1
    assert text.count('id="blocked-forbidden-screen"') == 1
    assert text.count('id="validation-readiness-screen"') == 1


def test_readmes_record_1_99_cursor():
    for path in (README, WEB_README):
        text = read(path)
        assert "Hardening Validation & Readiness Screen 1.99" in text
        assert "VALIDATION_READINESS_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW" in text
        assert "VALIDATION_READINESS_AFFORDANCE_AUDIT_PASSED_WITH_NOTES" in text
        assert "PROMPT UI/UX 1.100 - Checkpoint Validation & Readiness Screen" in text
        assert "push pospuesto" in text
        assert "revisión visual humana" in text
        assert "no checkpoint publicado" in text
