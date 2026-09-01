import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_VISUAL_ACCESSIBILITY_FIX_1_145_A.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROTECTED = [
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


def inline_body_rule() -> str:
    text = read(INDEX)
    match = re.search(r"\sbody\s*\{(?P<body>.*?)\n\s*\}", text, re.DOTALL)
    assert match, "inline body rule missing"
    return match.group("body")


def inline_request_draft_panel_rule() -> str:
    text = read(INDEX)
    matches = re.findall(
        r"\.request-draft-panel\s*\{(?P<panel>.*?)\n\s*\}",
        text,
        re.DOTALL,
    )
    for panel in matches:
        if "position: fixed" in panel:
            return panel
    raise AssertionError("fixed request draft panel rule missing")


def test_document_exists_and_records_fix_contract():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Closure Matrix Visual Accessibility Fix 1.145.A",
        "e0d087e",
        "862e915",
        "784bc56",
        "120a686",
        "f69713a",
        "5c40fbc",
        "ff731d6",
        "581e342",
        "CLOSURE_MATRIX_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "main",
        "ahead por 7 commits",
        "working tree limpio",
        "push no ejecutado",
        "revision visual humana no aprobada",
        "corte visual",
        "scroll",
        "Diagnostico",
        "Fix aplicado",
        "Preservacion matriz",
        "Preservacion contractual",
        "Preservacion operativa",
        "ui/web/styles.css",
        "ui/web/index.html",
        "matriz presente",
        "20 dimensiones",
        "estados permitidos",
        "copy prohibido evitado",
        "sin botones/forms/inputs/links activos",
        "documental/read-only",
    ]:
        assert marker in text


def test_document_records_contractual_operational_and_next_state():
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
        "nueva revision visual humana",
        "CLOSURE_MATRIX_VISUAL_ACCESSIBILITY_FIX_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        (
            "PROMPT UI/UX 1.146 - Checkpoint matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE post revision visual humana contract-aware sin runtime/no-execution"
        ),
    ]:
        assert marker in text


def test_document_records_preserved_limits():
    text = read(DOC)

    for marker in [
        "se corrigio solo accesibilidad visual/scroll de la matriz",
        "no se rediseño el Panel Maestro",
        "no se reimplemento la matriz desde cero",
        "no se implemento otro bloque nuevo",
        "no se corrigio deuda fuera del corte visual/scroll",
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


def test_ui_preserves_matrix_dimensions_and_allowed_states():
    text = read(INDEX)
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
        "PASSED",
        "PASSED_WITH_MINOR_DEBT",
        "DEFERRED_WITH_GUARDRAILS",
        "BLOCKED_NEEDS_FIX",
        "BLOCKED_CRITICAL",
        "NOT_APPLICABLE",
    ]:
        assert marker in block

    assert block.count('class="closure-matrix-row"') == 20
    assert "FSC-CO-01" in text
    assert "FSC-BF-02" in text
    assert "FSC-VR-03" in text
    assert "FSC-RCP-04" in text
    assert 'data-contract-screen-count="4"' in text


def test_closure_matrix_still_has_no_operational_affordances_or_prohibited_copy():
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


def test_scroll_and_accessibility_fix_is_present_in_css_and_inline_layout():
    styles = read(STYLES)
    body_rule = inline_body_rule()
    draft_panel = inline_request_draft_panel_rule()

    for marker in [
        "overflow-x: hidden",
        "overflow-y: auto",
        "height: auto",
        "min-height: 100vh",
    ]:
        assert marker in styles
        assert marker in body_rule

    styles_body = re.search(
        r"body\s*\{(?P<body>.*?)\n\}",
        styles,
        re.DOTALL,
    ).group("body")
    assert not re.search(r"(?<!-)height:\s*100vh", styles_body)
    assert not re.search(r"\boverflow:\s*hidden", styles_body)

    for marker in [
        "max-height: 100vh",
        "overflow-x: hidden",
        "overflow-y: auto",
    ]:
        assert marker in draft_panel


def test_styles_do_not_hide_matrix_fsc_or_lower_sections():
    styles = read(STYLES)

    forbidden_patterns = [
        r"\.closure-matrix-section\s*\{[^}]*display:\s*none",
        r"\.closure-matrix-section\s*\{[^}]*visibility:\s*hidden",
        r"\.final-screen-contracts-rehousing\s*\{[^}]*display:\s*none",
        r"\.console-utilities\s*\{[^}]*display:\s*none",
    ]

    for pattern in forbidden_patterns:
        assert not re.search(pattern, styles, re.DOTALL | re.IGNORECASE)


def test_readme_cursors_record_visual_accessibility_fix_1_145_a():
    for path in (README, WEB_README):
        text = read(path)
        assert "Fix 1.145.A: accesibilidad visual/scroll matriz de cierre UI/UX 1.x" in text
        assert "e0d087e" in text
        assert "862e915" in text
        assert "CLOSURE_MATRIX_VISUAL_ACCESSIBILITY_FIX_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW" in text
        assert (
            "PROMPT UI/UX 1.146 - Checkpoint matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE post revision visual humana contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "pendiente nueva revision visual humana" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text
        assert "no push" in lower_text


def test_i18n_js_and_backend_were_not_modified_by_1_145_a():
    result = subprocess.run(
        ["git", "diff", "--name-only", "e0d087e", "--", *PROTECTED],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
