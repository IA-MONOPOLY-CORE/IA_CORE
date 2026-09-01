import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_RESTORE_POINT_DECISION_1_147.md"
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


def test_document_exists_and_records_restore_point_decision_context():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Closure Matrix Restore Point Decision 1.147",
        "167d521",
        "862e915",
        "784bc56",
        "120a686",
        "f69713a",
        "5c40fbc",
        "ff731d6",
        "581e342",
        "e0d087e",
        "31b1493",
        "CLOSURE_MATRIX_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
        "main",
        "ahead por 9 commits",
        "working tree limpio",
        "push no ejecutado",
        "Bloque acumulado desde restore point remoto",
        "Condicion de restore point",
    ]:
        assert marker in text


def test_document_records_restore_point_conditions_and_risks():
    text = read(DOC)

    for marker in [
        "Riesgos de publicar",
        "Mitigacion",
        "Riesgos de no publicar",
        "no behind/diverged",
        "revision visual humana aprobada",
        "matriz visible",
        "20 items visibles",
        "scroll/accesibilidad visual resuelta",
        "pruebas pasando",
        "node checks pasando",
        "FSC preservadas",
        "DEFER_FINALIZATION",
        "ausencia operativa",
        "no secretos",
        "no dependencias nuevas",
        "no CI modificado",
    ]:
        assert marker in text


def test_document_records_decision_next_prompt_and_limits():
    text = read(DOC)

    allowed_decisions = [
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_SELECTED",
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_DEFERRED_WITH_GUARDRAILS",
        "CLOSURE_MATRIX_RESTORE_POINT_DECISION_NEEDS_OPERATOR_CONFIRMATION",
        "CLOSURE_MATRIX_RESTORE_POINT_DECISION_BLOCKED_NEEDS_FIX",
        "CLOSURE_MATRIX_RESTORE_POINT_DECISION_BLOCKED_CRITICAL",
    ]
    assert any(decision in text for decision in allowed_decisions)
    assert "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_SELECTED" in text
    assert (
        "PROMPT UI/UX 1.148 - Publicar restore point matriz de cierre UI UX 1.x "
        "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text

    for marker in [
        "no se publico restore point",
        "no se hizo push",
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
        "no se avanzo al contrato de vocabulario/affordances",
        "no se avanzo al ledger de capacidades",
        "no se avanzo al cierre global UI/UX 1.x",
    ]:
        assert marker in text


def test_document_summarizes_all_nine_local_commits():
    text = read(DOC)

    expected_rows = {
        "784bc56": "Planificar siguiente paso post density refinement",
        "120a686": "Auditar Panel Maestro post density refinement",
        "f69713a": "Auditar candidatos estandar tope de gama",
        "5c40fbc": "Revisar candidatos y ordenar secuencia",
        "ff731d6": "Planificar matriz de cierre UI/UX 1.x",
        "581e342": "Planificar implementacion futura de matriz",
        "e0d087e": "Implementar matriz visual/documental",
        "31b1493": "Corregir accesibilidad visual/scroll",
        "167d521": "Checkpoint post revision visual humana",
    }
    for commit, purpose in expected_rows.items():
        assert commit in text
        assert purpose in text


def test_readme_cursors_record_restore_point_decision_1_147():
    for path in (README, WEB_README):
        text = read(path)
        assert "Decision 1.147: publicacion restore point matriz de cierre UI/UX 1.x" in text
        assert "862e915" in text
        assert "167d521" in text
        assert "ahead por 9 commits" in text
        assert "revision visual humana aprobada" in text
        assert "matriz visible" in text
        assert "20 items con etiquetas" in text
        assert "scroll/accesibilidad resuelta" in text
        assert "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_SELECTED" in text
        assert (
            "PROMPT UI/UX 1.148 - Publicar restore point matriz de cierre UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no push" in lower_text
        assert "no publicacion ejecutada" in lower_text
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text


def test_prompt_1_147_did_not_modify_readonly_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "167d521", "--", *PROTECTED],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
