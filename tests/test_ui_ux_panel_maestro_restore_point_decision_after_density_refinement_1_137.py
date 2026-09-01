import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "UI_UX_PANEL_MAESTRO_RESTORE_POINT_DECISION_AFTER_DENSITY_REFINEMENT_1_137.md"
)
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
PROHIBITED_AFTER_136 = [
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


def test_document_contains_required_context_and_closure_markers():
    assert DOC.exists()
    text = read(DOC)

    required = [
        "UI/UX Panel Maestro Restore Point Decision After Density Refinement 1.137",
        "dc0c100",
        "2d178d8",
        "67bd324",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_IMPLEMENTED_WITH_NOTES_READY_FOR_HUMAN_VISUAL_REVIEW",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_HUMAN_VISUAL_REVIEW_PASSED",
        "DESIGN_SYSTEM_DENSITY_REFINEMENT_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
        "main",
        "ahead por 2 commits",
        "push no ejecutado",
        "working tree limpio",
        "no fix visual inmediato pendiente",
        "Razones para publicar",
        "Razones para no publicar",
        "implementación Design System / Density Refinement",
        "checkpoint Design System / Density Refinement",
        "sin nuevo bloque visual",
    ]

    for marker in required:
        assert marker in text


def test_document_records_limits_decision_and_next_prompt():
    text = read(DOC)
    decisions = [
        "RESTORE_POINT_PUBLICATION_SELECTED_AFTER_DENSITY_REFINEMENT_CHECKPOINT",
        "RESTORE_POINT_PUBLICATION_DEFERRED_AFTER_DENSITY_REFINEMENT_CHECKPOINT",
        "RESTORE_POINT_DECISION_AFTER_DENSITY_REFINEMENT_BLOCKED_NEEDS_FIX",
        "RESTORE_POINT_DECISION_AFTER_DENSITY_REFINEMENT_BLOCKED_CRITICAL",
    ]
    required_limits = [
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
        "PROMPT UI/UX 1.138 - Publicar restore point Design System Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
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
        "no se hizo push",
        "no se avanzo a 1.138",
    ]

    present = [decision for decision in decisions if decision in text]
    assert present == ["RESTORE_POINT_PUBLICATION_SELECTED_AFTER_DENSITY_REFINEMENT_CHECKPOINT"]

    for marker in required_limits:
        assert marker in text


def test_decision_prompt_does_not_touch_active_ui_js_or_backend_after_136():
    result = subprocess.run(
        ["git", "diff", "--name-only", "dc0c100", "1d14e35", "--", *PROHIBITED_AFTER_136],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""


def test_readme_cursors_record_decision_1_137():
    for path in (README, WEB_README):
        text = read(path)
        assert "Decisión restore point después de Density Refinement 1.137" in text
        assert "67bd324" in text
        assert "dc0c100" in text
        assert "2d178d8" in text
        assert "RESTORE_POINT_PUBLICATION_SELECTED_AFTER_DENSITY_REFINEMENT_CHECKPOINT" in text
        assert (
            "PROMPT UI/UX 1.138 - Publicar restore point Design System Density "
            "Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no push" in lower_text
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
