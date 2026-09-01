import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "UI_UX_PANEL_MAESTRO_RESTORE_POINT_PUBLICATION_DENSITY_REFINEMENT_1_138.md"
)
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_137 = [
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


def test_document_contains_publication_context_and_scope():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Restore Point Publication Density Refinement 1.138",
        "1d14e35",
        "2d178d8",
        "67bd324",
        "dc0c100",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_HUMAN_VISUAL_REVIEW_PASSED",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
        "RESTORE_POINT_PUBLICATION_SELECTED_AFTER_DENSITY_REFINEMENT_CHECKPOINT",
        "main",
        "ahead por 3 commits",
        "push no ejecutado antes de 1.138",
        "working tree limpio",
        "no fix visual inmediato pendiente",
        "Alcance publicado",
        "implementación Design System / Density Refinement",
        "checkpoint Design System / Density Refinement",
        "decisión 1.137",
        "publicación 1.138",
        "sin nuevo bloque visual",
        "sin cambios UI activos dentro de 1.138",
    ]

    for marker in required:
        assert marker in text


def test_document_records_limits_publication_result_decision_and_next_prompt():
    text = read(DOC)
    decisions = [
        "DENSITY_REFINEMENT_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED",
        "DENSITY_REFINEMENT_RESTORE_POINT_PUBLICATION_BLOCKED_NEEDS_FIX",
        "DENSITY_REFINEMENT_RESTORE_POINT_PUBLICATION_BLOCKED_CRITICAL",
    ]
    required = [
        "no-runtime/no-execution",
        "sin JS nuevo",
        "sin listeners/fetches",
        "sin localStorage",
        "sin rutas/hash",
        "sin User Panel",
        "sin endpoints",
        "sin backend",
        "sin contrato funcional nuevo",
        "sin contrato final",
        "DEFER_FINALIZATION",
        "FSC preservadas",
        "elementos inferiores preservados",
        "CFG",
        "DOMAIN",
        "+",
        "IA_CORE como identidad visible activa",
        "SAAOP/Loteria ausente",
        "sin deuda residual general",
        "sin pyflakes",
        "Validaciones pre-push",
        "Resultado de publicacion",
        "commit local 1.138",
        "hash corto 1.138",
        "push ejecutado",
        "origin/main",
        "HEAD",
        "HEAD == origin/main",
        "nuevo restore point remoto",
        "PROMPT UI/UX 1.139 - Planificar siguiente paso post Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
        "no se implemento bloque nuevo",
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
        "no se creo contrato final",
        "no se contradijo `DEFER_FINALIZATION`",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "si se hizo push",
        "no se avanzo a 1.139",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["DENSITY_REFINEMENT_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED"]

    for marker in required:
        assert marker in text


def test_publication_prompt_does_not_touch_active_ui_js_or_backend_after_137():
    result = subprocess.run(
        ["git", "diff", "--name-only", "1d14e35", "--", *PROHIBITED_AFTER_137],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_publication_1_138():
    for path in (README, WEB_README):
        text = read(path)
        assert "Publicación restore point Density Refinement 1.138" in text
        assert "2d178d8" in text
        assert "67bd324" in text
        assert "dc0c100" in text
        assert "1d14e35" in text
        assert "DENSITY_REFINEMENT_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED" in text
        assert (
            "PROMPT UI/UX 1.139 - Planificar siguiente paso post Density "
            "Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no bloque nuevo" in lower_text
        assert "no ui activa" in lower_text
        assert "nuevo restore point remoto" in lower_text
