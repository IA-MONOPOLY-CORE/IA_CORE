import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_TIER_STANDARD_CANDIDATES_REVIEW_1_142.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_141 = [
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

    required = [
        "UI/UX Panel Maestro Top Tier Standard Candidates Review 1.142",
        "f69713a",
        "862e915",
        "784bc56",
        "120a686",
        "TOP_TIER_STANDARD_CANDIDATES_AUDIT_READY_FOR_OPERATOR_REVIEW",
        "main",
        "ahead por 3 commits",
        "working tree limpio",
        "push no ejecutado",
        "Objetivo",
        "Estado recibido",
        "Base documental releida",
    ]

    for marker in required:
        assert marker in text


def test_document_reviews_audit_1_141_and_candidate_set():
    text = read(DOC)

    for marker in [
        "Revisión de auditoría 1.141",
        "matriz de cierre UI/UX 1.x",
        "contrato de vocabulario/affordances",
        "ledger de capacidades presentes/bloqueadas/futuras",
        "no recomendo abrir polish",
        "no recomendo runtime",
        "candidatos estructurales",
        "no-runtime/no-execution",
        "lista para revision del operador",
    ]:
        assert marker in text


def test_document_evaluates_each_candidate_with_required_fields():
    text = read(DOC)

    for candidate in [
        "Matriz de cierre UI/UX 1.x",
        "Contrato de vocabulario/affordances",
        "Ledger de capacidades presentes/bloqueadas/futuras",
    ]:
        assert candidate in text

    for marker in [
        "problema que resuelve",
        "valor estructural",
        "valor invisible",
        "riesgo de hacerlo ahora",
        "riesgo de diferirlo",
        "dependencia previa",
        "alcance minimo seguro",
        "criterio de aprobacion",
        "debe hacerse antes del cierre UI/UX 1.x",
    ]:
        assert marker in text


def test_document_selects_single_decision_sequence_and_next_prompt():
    text = read(DOC)
    decisions = [
        "TOP_TIER_CANDIDATES_REVIEW_ACCEPTED_SEQUENCE_READY_FOR_CLOSURE_MATRIX_PLANNING",
        "TOP_TIER_CANDIDATES_REVIEW_ACCEPTED_REORDERED_SEQUENCE_READY_FOR_NEXT_PLANNING",
        "TOP_TIER_CANDIDATES_REVIEW_NEEDS_OPERATOR_DECISION",
        "TOP_TIER_CANDIDATES_REVIEW_BLOCKED_NEEDS_FIX",
        "TOP_TIER_CANDIDATES_REVIEW_BLOCKED_CRITICAL",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == [
        "TOP_TIER_CANDIDATES_REVIEW_ACCEPTED_SEQUENCE_READY_FOR_CLOSURE_MATRIX_PLANNING"
    ]

    for marker in [
        "Secuencia recomendada",
        "Matriz de cierre UI/UX 1.x",
        "Contrato de vocabulario/affordances",
        "Ledger de capacidades presentes/bloqueadas/futuras",
        "PROMPT UI/UX 1.143 - Planificar matriz de cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text


def test_document_records_preserved_limits():
    text = read(DOC)

    required_limits = [
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
        ("no se avanzó a 1.143", "no se avanzo a 1.143"),
    ]

    for variants in required_limits:
        assert any(variant in text for variant in variants), variants


def test_review_prompt_does_not_touch_active_ui_js_or_backend_after_141():
    result = subprocess.run(
        ["git", "diff", "--name-only", "f69713a", "--", *PROHIBITED_AFTER_141],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_review_1_142():
    for path in (README, WEB_README):
        text = read(path)
        assert "Revisión 1.142: candidatos estándar tope de gama" in text
        assert "f69713a" in text
        assert "862e915" in text
        assert (
            "TOP_TIER_CANDIDATES_REVIEW_ACCEPTED_SEQUENCE_READY_FOR_CLOSURE_MATRIX_PLANNING"
            in text
        )
        assert (
            "PROMPT UI/UX 1.143 - Planificar matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no correccion" in lower_text
        assert "no push" in lower_text
