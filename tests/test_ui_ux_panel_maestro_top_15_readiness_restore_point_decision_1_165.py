from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_15_READINESS_RESTORE_POINT_DECISION_1_165.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


FORBIDDEN_STATIC_ARTIFACTS = [
    ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json",
    ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json",
    ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json",
    ROOT / "tests" / "fixtures" / "ui_top_15_elite_audit_v1.json",
    ROOT / "ui" / "web" / "contracts" / "ui_ux_1x_closure_readiness_matrix.v1.json",
    ROOT / "tests" / "fixtures" / "ui_ux_1x_closure_readiness_matrix_v1.json",
]


PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
    "core",
    "domains",
    "providers",
    "tools",
    "scripts",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def test_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro TOP 15 Readiness Restore Point Decision 1.165",
        "53374ab",
        "07a15d8",
        "main",
        "ahead",
        "6 commits",
        "working tree limpio",
        "bloque 1.159-1.164 completo",
        "readiness matrix 1.163 implementada documentation-test-only",
        "checkpoint 1.164 pasado",
        "READINESS_MATRIX_CHECKPOINT_PASSED",
        "NO_BLOCKERS_FOUND",
        "RESTORE_POINT_DECISION_RECOMMENDED_NEXT",
        "UI/UX 1.x no cerrado globalmente",
        "restore point nuevo no publicado",
        "Decidir publicacion de restore point del bloque TOP 15 + readiness, sin publicarlo todavia",
    ]:
        assert marker in text


def test_local_block_1_159_to_1_164_is_confirmed():
    text = read(DOC)
    for marker in [
        "1.159 planifico auditoria TOP 15",
        "1.160 audito TOP 15",
        "1.161 decidio primera recomendacion",
        "1.162 planifico implementacion readiness",
        "1.163 implemento readiness documentation-test-only",
        "1.164 checkpointed readiness",
        "6 commits locales no publicados",
        "documentales/test-only",
        "No UI activa",
        "No JS",
        "No backend",
        "No runtime",
        "No User Panel",
        "No JSON/fixtures ledger/TOP15/readiness",
    ]:
        assert marker in text


def test_reasons_for_and_against_publication_are_documented():
    text = read(DOC)
    for marker in [
        "Motivos a favor de publicar restore point",
        "Bloque local coherente y checkpointed",
        "6 commits locales acumulados desde restore point remoto",
        "Cambios documentales/test-only con pruebas",
        "working tree limpio",
        "no behind/no divergence",
        "Respaldo remoto util antes de avanzar",
        "punto seguro despues de auditoria TOP 15 + readiness",
        "Reduce riesgo de perder bloque",
        "Permite retomar desde GitHub",
        "Consolida la base antes de decidir proximos pasos",
        "Motivos en contra de publicar restore point",
        "Todavia no se cerro UI/UX 1.x globalmente",
        "No hay UI visual nueva para revisar en navegador",
        "bloque es documental/test-only",
        "seguir acumulando",
        "restore point remoto anterior 07a15d8",
        "ruido historico",
    ]:
        assert marker in text


def test_publication_and_non_publication_risks_are_documented():
    text = read(DOC)
    for marker in [
        "Riesgos de publicar",
        "equivale a cerrar UI/UX 1.x",
        "readiness documentation-test-only con UI visible",
        "checkpoint pasado con producto terminado",
        "contradiccion documental",
        "artefactos prohibidos",
        "divergence/behind",
        "validaciones suficientes",
        "Riesgos de no publicar",
        "Acumular demasiados commits locales",
        "Perder bloque",
        "sin respaldo remoto actualizado",
        "rollback mental y tecnico",
        "Mezclar readiness con proximas recomendaciones",
        "costo de recuperacion",
    ]:
        assert marker in text


def test_blockers_decision_and_next_prompt_are_documented():
    text = read(DOC)
    for marker in [
        "Blockers evaluados",
        "NO_RESTORE_PUBLICATION_BLOCKERS_FOUND",
        "working tree limpio",
        "origin/main esperado",
        "branch main",
        "no behind",
        "no diverged",
        "tests",
        "UI/JS/backend sin diff",
        "JSON/fixtures prohibidos ausentes",
        "runtime/execution/User Panel/endpoints ausentes",
        "TOP_15_READINESS_RESTORE_POINT_PUBLICATION_SELECTED",
        "PROMPT UI/UX 1.166 - Publicar restore point bloque TOP 15 readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
    ]:
        assert marker in text


def test_negative_limits_are_preserved():
    text = read(DOC)
    for marker in [
        "no se publico restore point",
        "no se hizo push",
        "no se ejecuto git push",
        "no se implemento nada nuevo",
        "no se creo JSON readiness",
        "no se creo fixture readiness",
        "no se creo readiness consumida por UI/backend",
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
        "no se creo execution",
        "no se creo dispatch",
        "no se creo tool/model/integration invocation",
        "no se creo memory write",
        "no se creo context injection",
        "no se creo delivery",
        "no se creo JSON ledger",
        "no se creo fixture ledger",
        "no se creo JSON TOP 15",
        "no se creo fixture TOP 15",
        "no se creo helper operativo",
        "no se creo enforcement activo",
        "no se modifico contrato funcional",
        "no se creo contrato final operativo",
        "no se contradijo DEFER_FINALIZATION",
        "no se renombro +",
        "no se renombro DOMAIN",
        "no se modificaron scripts inferiores",
        "no se limpio deuda residual general",
        "no se corrigieron pyflakes",
        "no se cerro UI/UX 1.x globalmente",
    ]:
        assert marker in text


def test_static_artifacts_absent_and_ui_contract_markers_read_only():
    for path in FORBIDDEN_STATIC_ARTIFACTS:
        assert not path.exists(), f"Forbidden artifact exists: {path}"

    index = read(INDEX)
    assert "Matriz de cierre UI/UX 1.x" in index or "Closure Matrix" in index
    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
    ]:
        assert marker in index
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
        assert forbidden not in index


def test_readmes_have_1_165_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Decision 1.165 de publicacion restore point",
            "HEAD base `53374ab`",
            "restore point remoto vigente `07a15d8`",
            "main ahead por 6 commits al inicio",
            "bloque 1.159-1.164 coherente y checkpointed",
            "restore point publication selected",
            "TOP_15_READINESS_RESTORE_POINT_PUBLICATION_SELECTED",
            "PROMPT UI/UX 1.166 - Publicar restore point bloque TOP 15 readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
            "no push en 1.165",
            "restore point nuevo no publicado todavia",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no JSON readiness",
            "no fixture readiness",
            "no UI/UX 1.x cerrado globalmente",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_TOP_15_READINESS_RESTORE_POINT_DECISION_1_165.md",
        "tests/test_ui_ux_panel_maestro_top_15_readiness_restore_point_decision_1_165.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
