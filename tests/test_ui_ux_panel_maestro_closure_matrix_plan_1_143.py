import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_PLAN_1_143.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_142 = [
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
        "UI/UX Panel Maestro Closure Matrix Plan 1.143",
        "5c40fbc",
        "862e915",
        "784bc56",
        "120a686",
        "f69713a",
        "TOP_TIER_CANDIDATES_REVIEW_ACCEPTED_SEQUENCE_READY_FOR_CLOSURE_MATRIX_PLANNING",
        "main",
        "ahead por 4 commits",
        "working tree limpio",
        "push no ejecutado",
        "Objetivo",
        "Estado recibido",
    ]:
        assert marker in text


def test_document_records_accepted_sequence_and_all_dimensions():
    text = read(DOC)

    for marker in [
        "Secuencia aceptada antes del cierre UI/UX 1.x",
        "matriz de cierre UI/UX 1.x",
        "contrato de vocabulario/affordances",
        "ledger de capacidades presentes/bloqueadas/futuras",
        "Identidad visible",
        "Master Shell / Overview Layer",
        "Final Screen Contracts Rehousing",
        "Design System / Density Refinement",
        "No-runtime / no-execution",
        "Read-only / blocked states",
        "FSC preservation",
        "DEFER_FINALIZATION",
        "Elementos inferiores",
        "CFG",
        "DOMAIN",
        "+",
        "Vocabulario / affordances",
        "Capacidades presentes / bloqueadas / futuras",
        "Evidencia / trazabilidad",
        "Documentación / tests",
        "Deuda visual / semántica",
        "Readiness de cierre",
        "Riesgo de sobreconstrucción",
        "Límites de no implementación",
        "Restore points / publicación",
        "Próximo paso seguro",
    ]:
        assert marker in text


def test_each_dimension_contract_fields_are_present():
    text = read(DOC)

    for marker in [
        "qué evalúa",
        "por qué importa",
        "evidencia requerida",
        "estado permitido",
        "riesgo si falla",
        "criterio de aprobación",
        "relación con cierre UI/UX 1.x",
    ]:
        assert marker in text


def test_states_allowed_and_prohibited_are_documented():
    text = read(DOC)

    for marker in [
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


def test_global_closure_criteria_and_dependencies_are_documented():
    text = read(DOC)

    for marker in [
        "Criterios de cierre global UI/UX 1.x",
        "sin blockers críticos",
        "sin acciones fantasma",
        "sin runtime visible",
        "sin ejecución visible",
        "sin contradicción de contrato",
        "sin quinta FSC",
        "sin User Panel",
        "sin rutas/hash",
        "sin endpoints/fetches nuevos",
        "sin payload crudo operativo",
        "sin identidad SAAOP/Lotería visible activa",
        "affordances",
        "capacidades presentes/bloqueadas/futuras",
        "evidencia trazable",
        "tests/documentación actualizados",
        "deuda menor clasificada",
        "restore point publicado antes del cierre final",
        "Dependencia con próximos bloques",
        "contrato de vocabulario/affordances",
        "ledger de capacidades presentes/bloqueadas/futuras",
        "cierre global UI/UX 1.x",
    ]:
        assert marker in text


def test_document_selects_single_decision_and_next_prompt():
    text = read(DOC)
    decisions = [
        "CLOSURE_MATRIX_PLAN_READY_FOR_IMPLEMENTATION_PLANNING",
        "CLOSURE_MATRIX_PLAN_NEEDS_OPERATOR_DECISION",
        "CLOSURE_MATRIX_PLAN_BLOCKED_NEEDS_FIX",
        "CLOSURE_MATRIX_PLAN_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["CLOSURE_MATRIX_PLAN_READY_FOR_IMPLEMENTATION_PLANNING"]
    assert (
        "PROMPT UI/UX 1.144 - Planificar implementación matriz de cierre UI UX 1.x "
        "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_document_records_preserved_limits():
    text = read(DOC)

    required_limits = [
        ("no se implementó matriz visual", "no se implemento matriz visual"),
        ("no se implementó bloque nuevo", "no se implemento bloque nuevo"),
        ("no se corrigió deuda", "no se corrigio deuda"),
        ("no se modificó UI activa", "no se modifico UI activa"),
        ("no se modificó index.html", "no se modifico index.html"),
        ("no se modificó styles.css", "no se modifico styles.css"),
        ("no se modificó i18n_es.json", "no se modifico i18n_es.json"),
        ("no se modificó JS", "no se modifico JS"),
        ("no se agregaron listeners",),
        ("no se agregaron fetches",),
        ("no se agregó localStorage", "no se agrego localStorage"),
        ("no se agregaron rutas/hash",),
        ("no se creó User Panel", "no se creo User Panel"),
        ("no se crearon endpoints",),
        ("no se tocó backend", "no se toco backend"),
        ("no se tocó runtime", "no se toco runtime"),
        ("no se modificó contrato funcional", "no se modifico contrato funcional"),
        ("no se creó contrato final operativo", "no se creo contrato final operativo"),
        ("no se contradijo `DEFER_FINALIZATION`", "no se contradijo DEFER_FINALIZATION"),
        ("no se limpió deuda residual general", "no se limpio deuda residual general"),
        ("no se corrigieron pyflakes",),
        ("no se hizo push",),
        ("no se avanzó a implementación", "no se avanzo a implementacion"),
        ("no se avanzó a 1.144", "no se avanzo a 1.144"),
    ]

    for variants in required_limits:
        assert any(variant in text for variant in variants), variants


def test_plan_prompt_does_not_touch_active_ui_js_or_backend_after_142():
    result = subprocess.run(
        ["git", "diff", "--name-only", "5c40fbc", "--", *PROHIBITED_AFTER_142],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_closure_matrix_plan_1_143():
    for path in (README, WEB_README):
        text = read(path)
        assert "Planificación 1.143: matriz de cierre UI/UX 1.x" in text
        assert "5c40fbc" in text
        assert "862e915" in text
        assert "CLOSURE_MATRIX_PLAN_READY_FOR_IMPLEMENTATION_PLANNING" in text
        assert (
            "PROMPT UI/UX 1.144 - Planificar implementación matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion de matriz visual" in lower_text
        assert "no implementacion" in lower_text
        assert "no correccion" in lower_text
        assert "no push" in lower_text
