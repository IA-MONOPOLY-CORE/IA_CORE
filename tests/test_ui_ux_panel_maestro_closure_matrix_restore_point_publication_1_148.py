import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_1_148.md"
INDEX = ROOT / "ui" / "web" / "index.html"
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


def test_document_exists_and_records_publication_context():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Closure Matrix Restore Point Publication 1.148",
        "fc5e9e3",
        "862e915",
        "main",
        "ahead por 10 commits",
        "working tree limpio",
        "push pendiente",
        "restore point todavia no publicado",
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_SELECTED",
        "784bc56",
        "120a686",
        "f69713a",
        "5c40fbc",
        "ff731d6",
        "581e342",
        "e0d087e",
        "31b1493",
        "167d521",
        "Condiciones de publicacion",
    ]:
        assert marker in text


def test_document_records_publication_conditions_and_controls():
    text = read(DOC)

    for marker in [
        "remoto correcto",
        "origin/main anterior 862e915",
        "no behind/diverged",
        "validaciones previas",
        "decision seleccionada",
        "revision visual humana aprobada",
        "matriz visible",
        "20 items visibles",
        "etiquetas respectivas visibles",
        "scroll/accesibilidad visual resuelta",
        "FSC preservadas",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
        "ausencia operativa",
        "no secretos",
        "no dependencias nuevas",
        "no CI modificado",
        "git push origin main",
        "force push",
        "rebase",
        "reset",
        "merge",
        "cambio de rama",
        "origin/main debe apuntar al HEAD final",
        "main debe quedar sincronizada",
        "restore point matriz de cierre UI/UX 1.x debe quedar publicado",
    ]:
        assert marker in text


def test_document_records_decision_next_prompt_and_limits():
    text = read(DOC)

    allowed_decisions = [
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLISHED",
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_BLOCKED_NEEDS_FIX",
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_BLOCKED_REMOTE_STATE_CHANGED",
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_BLOCKED_VALIDATION_FAILURE",
        "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_BLOCKED_CRITICAL",
    ]
    assert any(decision in text for decision in allowed_decisions)
    assert "CLOSURE_MATRIX_RESTORE_POINT_PUBLISHED" in text
    assert (
        "PROMPT UI/UX 1.149 - Planificar contrato de vocabulario affordances UI UX 1.x "
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
        "no se avanzo al contrato de vocabulario/affordances",
        "no se avanzo al ledger de capacidades",
        "no se avanzo al cierre global UI/UX 1.x",
    ]:
        assert marker in text


def test_ui_readonly_contract_remains_present_without_runtime_copy():
    text = read(INDEX)

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


def test_readme_cursors_record_publication_1_148():
    for path in (README, WEB_README):
        text = read(path)
        assert "Publicacion 1.148: restore point matriz de cierre UI/UX 1.x" in text
        assert "fc5e9e3" in text
        assert "862e915" in text
        assert "ahead por 10 commits" in text
        assert "CLOSURE_MATRIX_RESTORE_POINT_PUBLICATION_SELECTED" in text
        assert "commit creado por este prompt" in text
        assert "matriz visible" in text
        assert "20 items con etiquetas" in text
        assert "scroll/accesibilidad resuelta" in text
        assert "revision visual humana aprobada" in text
        assert "FSC preservadas" in text
        assert "DEFER_FINALIZATION preservado" in text
        assert (
            "PROMPT UI/UX 1.149 - Planificar contrato de vocabulario affordances UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text


def test_prompt_1_148_did_not_modify_readonly_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "fc5e9e3", "--", *PROTECTED],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
