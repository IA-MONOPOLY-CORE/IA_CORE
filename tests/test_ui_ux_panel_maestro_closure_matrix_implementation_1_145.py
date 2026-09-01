import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_IMPLEMENTATION_1_145.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
JS_READONLY = [
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
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


def test_document_exists_and_contains_required_contract():
    assert DOC.exists()
    text = read(DOC)
    lower_text = text.lower()

    for marker in [
        "UI/UX Panel Maestro Closure Matrix Implementation 1.145",
        "581e342",
        "862e915",
        "784bc56",
        "120a686",
        "f69713a",
        "5c40fbc",
        "ff731d6",
        "CLOSURE_MATRIX_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION",
        "main",
        "ahead por 6 commits",
        "working tree limpio",
        "push no ejecutado",
        "bloque documental/read-only",
        "20 dimensiones",
        "estados permitidos",
        "estados/copy prohibidos",
    ]:
        assert marker in text
    for marker in [
        "sin js",
        "sin backend",
        "sin runtime",
        "sin rutas/hash",
        "sin acciones operativas",
    ]:
        assert marker in lower_text
    assert "sin ejecución" in lower_text or "sin ejecucion" in lower_text


def test_document_records_contractual_and_operational_preservation():
    text = read(DOC)

    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "no quinta FSC",
        "DEFER_FINALIZATION",
        "contrato funcional no modificado",
        "contrato final operativo no creado",
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
        "ui/web/index.html",
        "ui/web/styles.css",
        "revision visual humana",
        "CLOSURE_MATRIX_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        (
            "PROMPT UI/UX 1.146 - Checkpoint matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE post revision visual humana contract-aware sin runtime/no-execution"
        ),
    ]:
        assert marker in text


def test_document_records_preserved_limits():
    text = read(DOC)

    for marker in [
        "se implemento solo matriz visual/documental",
        "no se implemento otro bloque nuevo",
        "no se corrigio deuda fuera de la matriz",
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
        "no se avanzo a 1.146",
    ]:
        assert marker in text


def test_ui_contains_closure_matrix_and_all_dimensions():
    block = closure_matrix_block()

    for marker in [
        "Matriz de cierre UI/UX 1.x",
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
    ]:
        assert marker in block

    assert block.count('class="closure-matrix-row"') == 20


def test_ui_uses_allowed_states_and_preserves_fsc_contracts():
    text = read(INDEX)
    block = closure_matrix_block()

    for marker in [
        "PASSED",
        "PASSED_WITH_MINOR_DEBT",
        "DEFERRED_WITH_GUARDRAILS",
        "BLOCKED_NEEDS_FIX",
        "BLOCKED_CRITICAL",
        "NOT_APPLICABLE",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
    ]:
        assert marker in block

    assert 'data-contract-screen-count="4"' in text
    assert text.count('data-contract-screen="') == 4


def test_closure_matrix_block_has_no_prohibited_copy_or_controls():
    block = closure_matrix_block()
    lower_block = block.lower()

    for forbidden in [
        "active",
        "ready to run",
        "running",
        "operational",
        "executing",
        "dispatching",
        "submitted",
        "processing request",
        "capability active",
        "preview-and-run",
        "<button",
        "<form",
        "<input",
        "onclick",
        "href=",
    ]:
        assert forbidden not in lower_block


def test_styles_define_static_responsive_matrix_using_design_tokens():
    text = read(STYLES)

    for marker in [
        ".closure-matrix-section",
        ".closure-matrix-header",
        ".closure-matrix-state-row",
        ".closure-matrix-badge",
        ".closure-matrix-grid",
        ".closure-matrix-row",
        ".closure-matrix-summary",
        "@media (max-width: 980px)",
        "@media (max-width: 620px)",
        "var(--ds-surface-primary)",
        "var(--ds-border-contract)",
        "var(--ds-density-gap)",
        "var(--ds-text-secondary)",
    ]:
        assert marker in text

    assert "closure-matrix" in text
    assert "javascript" not in text.lower()


def test_readme_cursors_record_closure_matrix_implementation_1_145():
    for path in (README, WEB_README):
        text = read(path)
        assert "Implementación 1.145: matriz visual/documental de cierre UI/UX 1.x" in text
        assert "581e342" in text
        assert "862e915" in text
        assert "CLOSURE_MATRIX_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW" in text
        assert (
            "PROMPT UI/UX 1.146 - Checkpoint matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE post revision visual humana contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "pendiente revision visual humana" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text
        assert "no push" in lower_text


def test_js_i18n_and_backend_were_not_modified_by_1_145():
    protected_paths = [
        "ui/web/i18n_es.json",
        "api.py",
        *JS_READONLY,
    ]
    result = subprocess.run(
        ["git", "diff", "--name-only", "581e342", "--", *protected_paths],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
