from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_CHECKPOINT_1_164.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
READINESS_DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_1_163.md"
READINESS_TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_closure_readiness_matrix_1_163.py"
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


def test_checkpoint_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro Closure Readiness Matrix Checkpoint 1.164",
        "c247d11",
        "07a15d8",
        "main",
        "ahead",
        "5 commits",
        "working tree limpio",
        "plan TOP 15 1.159 cerrado localmente",
        "auditoria TOP 15 1.160 cerrada localmente",
        "decision primera recomendacion 1.161 cerrada localmente",
        "plan implementacion readiness 1.162 cerrado localmente",
        "readiness matrix 1.163 implementada documentation-test-only",
        "UI/UX 1.x no cerrado globalmente",
        "restore point nuevo no publicado",
        "Checkpoint de la readiness matrix 1.163 sin implementacion nueva",
    ]:
        assert marker in text


def test_implementation_1_163_is_confirmed_by_checkpoint_and_sources():
    assert READINESS_DOC.exists()
    assert READINESS_TEST.exists()
    text = read(DOC)
    readiness = read(READINESS_DOC)
    for marker in [
        "documento readiness existe",
        "test readiness existe",
        "metadata completa",
        "15 grupos",
        "campos obligatorios",
        "estados permitidos",
        "estados prohibidos como denylist/bloqueo",
        "31 condiciones minimas",
        "status por condicion validado",
        "resumen readiness",
        "reglas de cierre",
        "matriz/FSC/DEFER",
        "contrato 1.151",
        "ledger 1.155",
        "TOP 15",
        "UI/JS/backend",
        "riesgos y mitigaciones",
        "no JSON readiness",
        "no fixture readiness",
        "no consumo UI/backend",
    ]:
        assert marker in text
    for marker in [
        "mode: DOCUMENTATION_ONLY_AND_TEST_ONLY",
        "status: TEST_ONLY_READINESS_MATRIX",
        "total conditions: 31",
        "CLOSURE_READINESS_MATRIX_IMPLEMENTED_TEST_ONLY",
    ]:
        assert marker in readiness


def test_checkpoint_coherence_sections_are_present():
    text = read(DOC)
    for marker in [
        "coherencia con plan 1.162",
        "coherencia con decision 1.161",
        "coherencia con auditoria 1.160",
        "coherencia con ledger 1.155",
        "coherencia con contrato 1.151",
        "coherencia con matriz/FSC/DEFER",
        "coherencia con UI/JS/backend",
        "coherencia README/cursor",
        "modalidad correcta",
        "recomendacion seleccionada",
        "ganadora sugerida",
        "separacion presente/bloqueado/futuro preservada",
        "estados seguros preservados",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
        "No consumo UI/backend",
    ]:
        assert marker in text


def test_blockers_results_restore_point_recommendation_and_decision_are_present():
    text = read(DOC)
    for marker in [
        "NO_BLOCKERS_FOUND",
        "READINESS_MATRIX_CHECKPOINT_PASSED",
        "RESTORE_POINT_DECISION_RECOMMENDED_NEXT",
        "5 commits locales desde 07a15d8",
        "bloque 1.159-1.164 es coherente",
        "documentales/test-only",
        "no se toco UI/JS/backend/runtime",
        "no se crearon JSON/fixtures",
        "readiness matrix ya esta checkpointed",
        "decidir publicacion de restore point",
        "CLOSURE_READINESS_MATRIX_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
        "PROMPT UI/UX 1.165 - Decidir publicacion restore point bloque TOP 15 readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
    ]:
        assert marker in text


def test_negative_limits_are_preserved_in_checkpoint():
    text = read(DOC)
    for marker in [
        "no se implemento nueva readiness matrix",
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
        "no se hizo push",
        "no se publico restore point",
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


def test_readmes_have_1_164_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Checkpoint 1.164 de readiness matrix",
            "HEAD base `c247d11`",
            "restore point remoto vigente `07a15d8`",
            "main ahead por 5 commits al inicio",
            "bloque 1.159-1.164 coherente",
            "readiness matrix implementada en 1.163 como documentation-test-only",
            "checkpoint readiness pasado",
            "READINESS_MATRIX_CHECKPOINT_PASSED",
            "CLOSURE_READINESS_MATRIX_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION",
            "PROMPT UI/UX 1.165 - Decidir publicacion restore point bloque TOP 15 readiness cierre UI UX 1.x Panel Maestro IA_CORE documentation-test-only sin runtime/no-execution",
            "no JSON readiness",
            "no fixture readiness",
            "no readiness consumida por UI/backend",
            "no UI activa",
            "no JS",
            "no backend",
            "no runtime",
            "no execution",
            "no push",
            "no restore point nuevo publicado",
            "UI/UX 1.x no cerrado globalmente",
        ]:
            assert marker in text


def test_only_allowed_files_changed_against_head_and_protected_paths_are_untouched():
    changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    allowed = {
        "README.md",
        "ui/web/README.md",
        "docs/UI_UX_PANEL_MAESTRO_CLOSURE_READINESS_MATRIX_CHECKPOINT_1_164.md",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_checkpoint_1_164.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
