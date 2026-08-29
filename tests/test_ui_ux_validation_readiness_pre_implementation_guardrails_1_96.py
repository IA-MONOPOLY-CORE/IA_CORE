from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_1_96.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.97 - Preparar plan de implementacion controlada Validation & Readiness "
    "Screen IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    assert path.exists(), f"Missing required file: {path}"
    return path.read_text(encoding="utf-8")


def test_guardrails_document_contains_required_identity_and_structure():
    text = read(DOC)
    markers = (
        "UI/UX Validation & Readiness Pre-Implementation Guardrails 1.96",
        "4299b0b",
        "7ad9a8b",
        "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
        "Contract Overview",
        "Blocked & Forbidden",
        "Request Contract Preview",
        "Validation & Readiness Screen",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "read-only",
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
        "Datos permitidos",
        "Datos prohibidos",
        "Estados permitidos",
        "Estados prohibidos",
        "Acciones UI prohibidas",
        "Copy permitido",
        "Copy prohibido",
        "Affordances permitidas/prohibidas",
        "Estructura visual futura",
        "Visual severity",
        "Tests futuros mínimos",
        "Entry criteria",
        "Exit criteria",
        "Risk register",
        "VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        NEXT_PROMPT,
    )
    assert all(marker in text for marker in markers)


def test_guardrails_document_contains_operational_boundaries():
    text = read(DOC)
    markers = (
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "no se implementó pantalla",
        "no se modificó UI activa",
        "no se tocó Contract Overview",
        "no se tocó Blocked & Forbidden",
        "no se creó User Panel",
        "no se avanzó a 1.97",
        "No se hace push",
    )
    assert all(marker in text for marker in markers)


def test_guardrails_document_does_not_authorize_implementation():
    text = read(DOC)
    assert "No implementa pantalla" in text
    assert "Estos prompts no se ejecutan" not in text
    assert "FSC-VR-03" in text
    assert "identificador operativo propuesto" in text
    assert "Lotería/SAAOP no pueden aparecer como identidad activa" in text


def test_readmes_record_guardrails_and_cursor():
    for path in (README, WEB_README):
        text = read(path)
        assert "Guardrails pre-implementación Validation & Readiness 1.96" in text
        assert "VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY" in text
        assert "Contract Overview" in text
        assert "Blocked & Forbidden" in text
        assert "push pospuesto" in text.lower()
        assert NEXT_PROMPT in text
