import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "UI_UX_PANEL_MAESTRO_DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_1_136.md"
)
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_135 = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
]
JS_FILES = [
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_document_contains_required_checkpoint_context_and_human_review():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Design System Density Refinement Checkpoint 1.136",
        "67bd324",
        "2d178d8",
        "commit local a checkpoint",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_HUMAN_VISUAL_REVIEW_PASSED",
        "main",
        "ahead por 1 commit",
        "push no ejecutado",
        "working tree limpio",
        "no pedido de fix visual inmediato",
        "visualmente se ve muy bien",
        "no hay nada para hacer",
        "solo lectura/documental",
        "Design System / Density Refinement implementado",
        "tokens CSS",
        "densidad",
        "spacing/layout",
        "badges/estados",
        "read-only/blocked/no-runtime",
        "anti-CTA operativo",
        "evidence/documentation",
        "responsive",
    ]

    for marker in required:
        assert marker in text

    assert "operador reviso navegador" in text or "operador revisó navegador" in text
    assert "sin accion operativa visible" in text or "sin acción operativa visible" in text
    assert "jerarquia visual" in text or "jerarquía visual" in text


def test_document_records_contract_lower_runtime_identity_and_limits():
    text = read(DOC)
    decisions = [
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_PASSED_WITH_MINOR_VISUAL_DEBT_READY_FOR_RESTORE_POINT_DECISION",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_BLOCKED_NEEDS_FIX",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_BLOCKED_CRITICAL",
    ]
    required = [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "no quinta FSC",
        "DEFER_FINALIZATION",
        "Final Screen Contracts documentales",
        "contrato funcional no modificado",
        "contrato final no creado",
        "lower console",
        "CFG",
        "DOMAIN",
        "+",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "formularios",
        "agent cards inferiores",
        "bloqueado/read-only",
        "no submit",
        "no mutaciones",
        "sin runtime",
        "sin execution",
        "sin dispatch",
        "sin worker",
        "sin scheduler",
        "sin queue",
        "sin model invocation",
        "sin tool invocation",
        "sin endpoints/fetches nuevos",
        "sin POST/PUT/DELETE",
        "sin fake success",
        "sin ghost actions",
        "sin acciones operativas visibles",
        "IA_CORE como identidad visible activa",
        "SAAOP/Loteria ausente",
        "Tactical HUD ausente",
        "U-Score ausente",
        "Cazador ausente",
        "Espejo ausente",
        "combinatoria ausente",
        "PROMPT UI/UX 1.137 - Decidir publicación restore point Design System Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no se implemento bloque nuevo",
        "no se modifico UI activa",
        "no se modifico index.html",
        "no se modifico styles.css",
        "no se modifico i18n_es.json",
        "no se modifico JS",
        "no se agrego JS",
        "no se agregaron listeners",
        "no se agregaron fetches",
        "no se agrego localStorage",
        "no se agregaron rutas/hash",
        "no se creo User Panel",
        "no se crearon endpoints",
        "no se toco backend",
        "no se toco runtime",
        "no se modifico contrato funcional",
        "no se creo contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "no se avanzo a 1.137",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == [
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION"
    ]
    for marker in required:
        assert marker in text


def test_ui_and_css_remain_read_only_sources_with_density_refinement_visible():
    index = read(INDEX)
    styles = read(STYLES)

    for marker in [
        "IA_CORE",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        "DEFER_FINALIZATION",
    ]:
        assert marker in index

    assert "--ds-" in styles or "Design System" in styles

    for marker in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "SAAOP",
        "Loteria",
        "Lotería",
    ]:
        assert marker not in index


def test_checkpoint_does_not_touch_active_ui_js_or_backend_after_135():
    result = subprocess.run(
        ["git", "diff", "--name-only", "67bd324", "--", *PROHIBITED_AFTER_135],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""

    js_result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main", "--", *JS_FILES],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert js_result.stdout.strip() == ""


def test_readme_cursors_record_checkpoint_1_136():
    for path in (README, WEB_README):
        text = read(path)
        assert "Checkpoint 1.136: Design System y Density Refinement" in text
        assert "67bd324" in text
        assert "2d178d8" in text
        assert "DESIGN_SYSTEM_DENSITY_REFINEMENT_HUMAN_VISUAL_REVIEW_PASSED" in text
        assert (
            "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION"
            in text
        )
        assert (
            "PROMPT UI/UX 1.137 - Decidir publicación restore point Design System "
            "Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no push" in lower_text
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
