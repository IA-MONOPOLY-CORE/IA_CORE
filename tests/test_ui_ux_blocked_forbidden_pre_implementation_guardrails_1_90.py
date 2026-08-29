from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_1_90.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

ALLOWED_DECISIONS = (
    "BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY",
    "BLOCKED_FORBIDDEN_NEEDS_MORE_PRE_IMPLEMENTATION_AUDIT",
    "BLOCKED_FORBIDDEN_IMPLEMENTATION_DEFERRED",
    "BLOCKED_FORBIDDEN_SELECTION_REQUIRES_REVIEW",
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.91 - Preparar plan de implementacion controlada "
    "Blocked & Forbidden Capabilities Screen IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    assert path.exists(), f"Missing required file: {path}"
    return path.read_text(encoding="utf-8")


def test_guardrails_document_exists_and_records_base_state():
    text = read(DOC)
    markers = (
        "# UI/UX Blocked & Forbidden Pre-Implementation Guardrails 1.90",
        "72affc4",
        "23f9185",
        "NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED",
        "Contract Overview Screen",
        "Baseline visual/contractual",
        "main` ahead de `origin/main` por 1 commit",
        "Push: pospuesto",
    )
    assert all(marker in text for marker in markers)


def test_guardrails_define_screen_identity_data_states_and_copy():
    text = read(DOC)
    markers = (
        "Blocked & Forbidden Capabilities Screen",
        "FSC-BF-02",
        "Blocked & Forbidden Final Screen Contract",
        "backend_internal_ui_payload.v1",
        "Panel Maestro only",
        "read-only",
        "blocked_capabilities",
        "forbidden_actions",
        "allowed_actions",
        "## Datos permitidos",
        "## Datos prohibidos",
        "## Estados permitidos",
        "## Estados prohibidos",
        "## Acciones UI prohibidas",
        "## Copy permitido",
        "## Copy prohibido",
    )
    assert all(marker in text for marker in markers)


def test_guardrails_define_visual_structure_tests_entry_exit_and_risks():
    text = read(DOC)
    markers = (
        "## Estructura visual futura",
        "## Visual severity",
        "## Tests futuros minimos",
        "## Entry criteria",
        "## Exit criteria",
        "## Risk register",
        "always-visible",
        "deny-by-default",
        "no-unlock/no-override/no-bypass",
        "No se avanzo a 1.91",
    )
    assert all(marker in text for marker in markers)


def test_guardrails_record_exactly_one_allowed_decision_and_next_prompt():
    text = read(DOC)
    decisions = [decision for decision in ALLOWED_DECISIONS if decision in text]
    assert decisions, "No allowed final decision recorded"
    assert decisions == ["BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY"]
    assert NEXT_PROMPT in text


def test_guardrails_preserve_forbidden_scope():
    text = read(DOC)
    markers = (
        "No se implemento pantalla",
        "No se modifico UI activa",
        "No se toco Contract Overview",
        "No se creo componente nuevo",
        "No se creo User Panel",
        "No se crearon rutas/hash",
        "No se crearon endpoints ni fetches",
        "No se toco backend operativo",
        "No se activo runtime, execution, dispatch ni controlled execution",
        "No se modifico CI ni dependencias",
        "No se limpio deuda residual",
        "No se corrigieron pyflakes",
        "No se hizo push",
    )
    assert all(marker in text for marker in markers)


def test_readmes_point_to_guardrails_and_next_prompt():
    for path in (README, WEB_README):
        text = read(path)
        assert "Guardrails pre-implementacion Blocked & Forbidden 1.90" in text
        assert "UI_UX_BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_1_90.md" in text
        assert "BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY" in text
        assert NEXT_PROMPT in text
        assert "no implementa pantalla" in text
        assert "no modifica UI activa" in text
        assert "no toca Contract Overview" in text
        assert "no crea User Panel" in text
        assert "sin backend/runtime/endpoints/CI/dependencias" in text
        assert "sin limpiar deuda residual" in text
        assert "sin corregir pyflakes" in text
        assert "no push" in text.lower()

