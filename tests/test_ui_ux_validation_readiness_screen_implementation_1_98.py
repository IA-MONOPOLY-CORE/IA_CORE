from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_SCREEN_IMPLEMENTATION_1_98.md"
TEST = ROOT / "tests" / "test_ui_ux_validation_readiness_screen_implementation_1_98.py"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validation_readiness_section(text: str) -> str:
    start = text.index('<section class="validation-readiness-screen')
    end = text.index("</section>", start) + len("</section>")
    return text[start:end]


def test_implementation_artifacts_exist():
    assert DOC.exists()
    assert TEST.exists()


def test_validation_readiness_screen_identity_and_status_strip():
    text = read(INDEX)
    section = validation_readiness_section(text)
    required = (
        "Validation &amp; Readiness Screen",
        "FSC-VR-03",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "read-only",
        "contract-aware",
        "validation-documented",
        "readiness-documented",
        "ready-no-permission",
        "no-runtime",
        "no-execution",
        "no-dispatch",
        "no-endpoint",
        "no-user-panel",
    )
    assert all(marker in section for marker in required)


def test_validation_readiness_screen_semantics_and_copy():
    section = validation_readiness_section(read(INDEX))
    required = (
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
        "Readiness informa, no habilita.",
        "Validation documenta, no ejecuta.",
        "Passed no equivale a éxito operativo.",
        "Warning/Error no representa runtime vivo.",
        "Review required no abre workflow activo.",
        "Los blockers permanecen visibles.",
        "Sin submit, dispatch ni ejecución.",
        "Sin endpoint, fetch ni User Panel.",
        "Snapshot documental, no log vivo.",
        "Request Contract Preview permanece diferido.",
        "Contract Overview",
        "Blocked &amp; Forbidden",
        "blockers",
        "warnings",
        "missing_requirements",
        "snapshot",
        "no log vivo",
    )
    assert all(marker in section for marker in required)


def test_validation_readiness_is_third_sibling_and_previous_screens_remain():
    text = read(INDEX)
    contract_overview = text.index('id="contract-overview-screen"')
    blocked_forbidden = text.index('id="blocked-forbidden-screen"')
    validation_readiness = text.index('id="validation-readiness-screen"')
    assert contract_overview < blocked_forbidden < validation_readiness
    assert text.count('data-contract-screen="FSC-CO-01"') == 1
    assert text.count('data-contract-screen="FSC-BF-02"') == 1
    assert text.count('data-contract-screen="FSC-VR-03"') == 1


def test_validation_readiness_has_no_new_operational_affordances():
    section = validation_readiness_section(read(INDEX))
    prohibited = (
        "<button",
        "data-action=\"run\"",
        "data-action=\"dispatch\"",
        "data-action=\"submit\"",
        "data-action=\"execute\"",
        "data-action=\"retry\"",
        "data-action=\"unlock\"",
        "data-action=\"override\"",
        "data-action=\"bypass\"",
        'href="#validation-readiness"',
        "window.location.hash",
        "fetch(",
    )
    assert all(marker not in section for marker in prohibited)
    assert "no User Panel" in section
    assert "no-endpoint" in section
    assert "no fetch" in section


def test_implementation_document_contains_decision_and_boundaries():
    text = read(DOC)
    required = (
        "UI/UX Validation & Readiness Screen Implementation 1.98",
        "9a3dfd6",
        "7ad9a8b",
        "4299b0b",
        "c5518a4",
        "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
        "VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "VALIDATION_READINESS_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "PROMPT UI/UX 1.99 - Hardening visual y contractual Validation & Readiness Screen IA_CORE contract-aware sin runtime/no-execution",
        "no push",
        "no visual approval",
        "no backend",
        "no runtime",
        "no endpoint/fetch",
        "no User Panel",
        "no rutas/hash",
        "no deuda residual",
        "no pyflakes",
        "no se avanzó a 1.99",
    )
    assert all(marker in text for marker in required)


def test_readmes_record_1_98_cursor():
    for path in (README, WEB_README):
        text = read(path)
        assert "Implementación Validation & Readiness Screen 1.98" in text
        assert "VALIDATION_READINESS_SCREEN_IMPLEMENTED_NEEDS_HARDENING" in text
        assert "PROMPT UI/UX 1.99 - Hardening visual y contractual Validation & Readiness Screen" in text
        assert "push pospuesto" in text
        assert "hardening" in text
        assert "revisión visual humana" in text
