import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_IMPLEMENTATION_PLAN_1_144.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_143 = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_exists_and_contains_base_state():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Closure Matrix Implementation Plan 1.144",
        "ff731d6",
        "862e915",
        "784bc56",
        "120a686",
        "f69713a",
        "5c40fbc",
        "CLOSURE_MATRIX_PLAN_READY_FOR_IMPLEMENTATION_PLANNING",
        "main",
        "ahead por 5 commits",
        "working tree limpio",
        "push no ejecutado",
    ]:
        assert marker in text


def test_document_records_review_of_143_and_future_strategy():
    text = read(DOC)

    for marker in [
        "Revision de planificacion 1.143",
        "Estrategia de implementacion futura",
        "ubicación recomendada",
        "bloque documental",
        "Master Shell / Overview Layer",
        "Final Screen Contracts Rehousing",
        "Design System / Density Refinement",
        "elementos inferiores",
        "no debe parecer runtime",
        "no debe parecer panel de ejecucion",
    ]:
        assert marker in text


def test_future_content_structure_and_categories_are_defined():
    text = read(DOC)

    for marker in [
        "Estructura de contenido futura",
        "nombre de dimension",
        "estado permitido",
        "evidencia requerida",
        "criterio de aprobacion",
        "riesgo si falla",
        "dependencia",
        "relacion con cierre UI/UX 1.x",
        "nota de guardrail",
        "categoria",
        "identidad",
        "contrato",
        "UI",
        "estado",
        "evidencia",
        "deuda",
        "publicacion",
        "futuro",
    ]:
        assert marker in text


def test_allowed_and_prohibited_states_are_documented():
    text = read(DOC)

    for marker in [
        "Estados visuales permitidos",
        "Estados/copy prohibidos",
        "PASSED",
        "PASSED_WITH_MINOR_DEBT",
        "DEFERRED_WITH_GUARDRAILS",
        "BLOCKED_NEEDS_FIX",
        "BLOCKED_CRITICAL",
        "NOT_APPLICABLE",
        "active",
        "running",
        "live",
        "operational",
        "executing",
        "dispatching",
        "submitted",
        "processing",
        "ready to run",
    ]:
        assert marker in text


def test_affordances_and_next_blocks_are_defined():
    text = read(DOC)

    for marker in [
        "Affordances permitidas/prohibidas",
        "lectura",
        "inspeccion documental",
        "evidencia resumida",
        "criterios",
        "estados de cierre",
        "labels",
        "badges no operativos",
        "texto explicativo",
        "botones operativos",
        "CTA",
        "forms activos",
        "submit",
        "run",
        "execute",
        "dispatch",
        "send",
        "preview-and-run",
        "refresh operativo",
        "fetch nuevo",
        "rutas/hash",
        "navegacion nueva",
        "interaccion que cambie estado",
        "localStorage",
        "confirmacion activa",
        "mutacion de datos",
        "Relacion con proximos bloques",
        "contrato de vocabulario/affordances",
        "ledger de capacidades presentes/bloqueadas/futuras",
        "cierre global UI/UX 1.x",
    ]:
        assert marker in text


def test_future_implementation_criteria_and_decision_are_ready():
    text = read(DOC)

    for marker in [
        "Criterios de implementacion futura",
        "no expone raw Package",
        "no contradice DEFER_FINALIZATION",
        "preserva FSC",
        "revision visual humana",
        "CLOSURE_MATRIX_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION",
        (
            "PROMPT UI/UX 1.145 - Implementar matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ),
    ]:
        assert marker in text

    forbidden_decisions = [
        "CLOSURE_MATRIX_IMPLEMENTATION_PLAN_NEEDS_OPERATOR_DECISION",
        "CLOSURE_MATRIX_IMPLEMENTATION_PLAN_BLOCKED_NEEDS_FIX",
        "CLOSURE_MATRIX_IMPLEMENTATION_PLAN_BLOCKED_CRITICAL",
    ]
    assert not any(decision in text for decision in forbidden_decisions)


def test_document_records_preserved_limits():
    text = read(DOC)

    for marker in [
        "no se implemento matriz visual",
        "no se implemento bloque nuevo",
        "no se corrigio deuda",
        "no se modifico UI activa",
        "no se modifico index.html",
        "no se modifico styles.css",
        "no se modifico i18n_es.json",
        "no se modifico JS",
        "no se agregaron listeners",
        "no se agregaron fetches",
        "no se agrego localStorage",
        "no se agregaron rutas/hash",
        "no se creo User Panel",
        "no se crearon endpoints",
        "no se toco backend",
        "no se toco runtime",
        "no se modifico contrato funcional",
        "no se creo contrato final operativo",
        "no se contradijo DEFER_FINALIZATION",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se avanzo a implementacion",
        "no se avanzo a 1.145",
    ]:
        assert marker in text


def test_plan_prompt_does_not_touch_active_ui_js_or_backend_after_143():
    result = subprocess.run(
        ["git", "diff", "--name-only", "ff731d6", "--", *PROHIBITED_AFTER_143],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_closure_matrix_implementation_plan_1_144():
    for path in (README, WEB_README):
        text = read(path)
        assert "Planificación 1.144: implementación futura de matriz de cierre UI/UX 1.x" in text
        assert "ff731d6" in text
        assert "862e915" in text
        assert "CLOSURE_MATRIX_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION" in text
        assert (
            "PROMPT UI/UX 1.145 - Implementar matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion de matriz visual" in lower_text
        assert "no implementacion" in lower_text
        assert "no correccion" in lower_text
        assert "no push" in lower_text
