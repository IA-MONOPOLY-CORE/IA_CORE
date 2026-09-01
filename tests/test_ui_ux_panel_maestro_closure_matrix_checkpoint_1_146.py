import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_CHECKPOINT_1_146.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROTECTED = [
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


def closure_matrix_block() -> str:
    text = read(INDEX)
    match = re.search(
        r'<section class="closure-matrix-section\b.*?</section>',
        text,
        re.DOTALL,
    )
    assert match, "closure matrix section missing"
    return match.group(0)


def css_rule(selector: str) -> str:
    text = read(STYLES)
    match = re.search(
        rf"{re.escape(selector)}\s*\{{(?P<body>.*?)\n\}}",
        text,
        re.DOTALL,
    )
    assert match, f"{selector} rule missing"
    return match.group("body")


def test_document_exists_and_records_checkpoint_context():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Closure Matrix Checkpoint 1.146",
        "31b1493",
        "862e915",
        "784bc56",
        "120a686",
        "f69713a",
        "5c40fbc",
        "ff731d6",
        "581e342",
        "e0d087e",
        "CLOSURE_MATRIX_VISUAL_ACCESSIBILITY_FIX_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "main",
        "ahead por 8 commits",
        "working tree limpio",
        "push no ejecutado",
        "Implementacion 1.145 confirmada",
        "Fix 1.145.A confirmado",
        "Revision visual humana aprobada",
        "matriz visible",
        "20 items visibles",
        "etiquetas respectivas visibles",
        "scroll/accesibilidad visual resuelta",
        "sin nuevos bloqueos visuales reportados",
    ]:
        assert marker in text


def test_document_records_contract_and_operational_preservation():
    text = read(DOC)

    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "no quinta FSC",
        "DEFER_FINALIZATION",
        "contrato funcional no modificado",
        "contrato final operativo no creado",
        "JS nuevo",
        "backend nuevo",
        "runtime",
        "execution",
        "dispatch",
        "worker",
        "scheduler",
        "queue",
        "model invocation",
        "tool invocation",
        "endpoints/fetches nuevos",
        "POST/PUT/DELETE",
        "submit operativo",
        "fake success",
        "ghost actions",
        "User Panel",
        "rutas/hash",
        "localStorage nuevo",
    ]:
        assert marker in text


def test_document_records_decision_next_prompt_and_limits():
    text = read(DOC)

    allowed_decisions = [
        "CLOSURE_MATRIX_CHECKPOINT_PASSED_READY_FOR_NEXT_STRUCTURAL_BLOCK_PLANNING",
        "CLOSURE_MATRIX_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
        "CLOSURE_MATRIX_CHECKPOINT_BLOCKED_NEEDS_FIX",
        "CLOSURE_MATRIX_CHECKPOINT_BLOCKED_CRITICAL",
    ]
    assert any(decision in text for decision in allowed_decisions)
    assert "CLOSURE_MATRIX_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION" in text
    assert (
        "PROMPT UI/UX 1.147 - Decidir publicacion restore point matriz de cierre UI UX 1.x "
        "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text

    for marker in [
        "no se implemento cambio visual nuevo",
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
        "no se avanzo al proximo bloque",
        "no se avanzo a publicacion remota",
    ]:
        assert marker in text


def test_ui_readonly_contains_matrix_contract_dimensions_and_states():
    text = read(INDEX)
    block = closure_matrix_block()

    for marker in [
        "Matriz de cierre UI/UX 1.x",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in text

    for marker in [
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
        "Documentacion / tests",
        "Deuda visual / semantica",
        "Readiness de cierre",
        "Riesgo de sobreconstruccion",
        "Limites de no implementacion",
        "Restore points / publicacion",
        "Proximo paso seguro",
        "PASSED",
        "PASSED_WITH_MINOR_DEBT",
        "DEFERRED_WITH_GUARDRAILS",
        "BLOCKED_NEEDS_FIX",
        "BLOCKED_CRITICAL",
        "NOT_APPLICABLE",
    ]:
        assert marker in block

    assert block.count('class="closure-matrix-row"') == 20
    assert text.count('data-contract-screen="') == 4


def test_ui_readonly_avoids_prohibited_runtime_copy():
    text = read(INDEX)

    for forbidden in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "Processing request",
        "Capability active",
        "preview-and-run",
    ]:
        assert forbidden not in text


def test_css_readonly_contains_scroll_accessibility_fix_without_js_dependency():
    styles = read(STYLES)
    body = css_rule("body")
    app = css_rule(".app-container")

    for rule in (body, app):
        assert "overflow-x: hidden" in rule
        assert "overflow-y: auto" in rule

    assert "height: auto" in body
    assert "min-height: 100vh" in body
    assert "min-height: 100vh" in app
    assert "closure-matrix" in styles
    assert "javascript" not in styles.lower()


def test_readme_cursors_record_checkpoint_1_146():
    for path in (README, WEB_README):
        text = read(path)
        assert "Checkpoint 1.146: matriz de cierre UI/UX 1.x post revision visual humana" in text
        assert "revision visual humana aprobada" in text
        assert "matriz visible" in text
        assert "20 items con etiquetas respectivas" in text
        assert "scroll/accesibilidad visual resuelta" in text
        assert "862e915" in text
        assert "31b1493" in text
        assert "CLOSURE_MATRIX_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION" in text
        assert (
            "PROMPT UI/UX 1.147 - Decidir publicacion restore point matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text
        assert "no push" in lower_text


def test_prompt_1_146_did_not_modify_readonly_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "31b1493", "--", *PROTECTED],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
