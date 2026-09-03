from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_15_READINESS_RESTORE_POINT_PUBLICATION_1_166.md"
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
        "UI/UX Panel Maestro TOP 15 Readiness Restore Point Publication 1.166",
        "a5102e5",
        "07a15d8",
        "main",
        "ahead",
        "7 commits",
        "working tree limpio",
        "bloque 1.159-1.165 completo",
        "TOP_15_READINESS_RESTORE_POINT_PUBLICATION_SELECTED",
        "NO_RESTORE_PUBLICATION_BLOCKERS_FOUND",
        "publicacion restore point pendiente al inicio",
        "UI/UX 1.x no cerrado globalmente",
        "Publicar restore point remoto",
        "push unico controlado",
    ]:
        assert marker in text


def test_published_block_is_documented():
    text = read(DOC)
    for marker in [
        "1.159 plan TOP 15",
        "1.160 auditoria TOP 15",
        "1.161 decision primera recomendacion",
        "1.162 plan readiness",
        "1.163 readiness documentation-test-only",
        "1.164 checkpoint readiness",
        "1.165 decision restore point",
        "1.166 publicacion restore point",
        "documentado/test-only",
        "no UI activa",
        "no JS",
        "no backend",
        "no runtime",
        "no User Panel",
        "no endpoints",
        "no JSON/fixtures ledger/TOP15/readiness",
    ]:
        assert marker in text


def test_pre_publication_validations_are_documented():
    text = read(DOC)
    for marker in [
        "Validaciones pre-publicacion",
        "node --check",
        "Test 1.166",
        "Test 1.165",
        "Test 1.164",
        "Test 1.163",
        "Test 1.162",
        "Test 1.161",
        "Test 1.160",
        "Test 1.159",
        "Ledger 1.153-1.158",
        "Vocabulario 1.149-1.152",
        "Matriz 1.145-1.148",
        "Backup readiness",
        "Backend payload/contracts",
        "git diff --check",
        "diff final limitado",
        "UI/JS/backend sin diff",
    ]:
        assert marker in text


def test_commit_push_post_publication_and_decision_are_documented():
    text = read(DOC)
    for marker in [
        "docs(ui): publicar restore point top 15 readiness",
        "git push origin main",
        "force push prohibido",
        "tags/releases/branches prohibidos",
        "HEAD == origin/main",
        "nuevo restore point remoto sera el hash final 1.166",
        "Estado post-publicacion esperado",
        "up to date with origin/main",
        "working tree limpio",
        "nuevo restore point remoto confirmado",
        "restore point previo 07a15d8",
        "UI/UX 1.x sigue no cerrado globalmente",
        "TOP_15_READINESS_RESTORE_POINT_PUBLISHED",
        "PROMPT UI/UX 1.167 - Planificar siguiente recomendacion TOP 15 post restore point readiness cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in text


def test_negative_limits_are_preserved():
    text = read(DOC)
    for marker in [
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
        "push controlado permitido",
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


def test_readmes_have_1_166_cursor():
    for path in [README, WEB_README]:
        text = read(path)
        for marker in [
            "Publicacion 1.166 de restore point bloque TOP 15 readiness",
            "HEAD base `a5102e5`",
            "restore point remoto previo `07a15d8`",
            "main ahead por 7 commits al inicio",
            "bloque 1.159-1.166 coherente y publicado",
            "restore point published",
            "TOP_15_READINESS_RESTORE_POINT_PUBLISHED",
            "nuevo restore point remoto: hash final 1.166",
            "HEAD == origin/main post-push",
            "branch up to date post-push",
            "working tree limpio post-push",
            "PROMPT UI/UX 1.167 - Planificar siguiente recomendacion TOP 15 post restore point readiness cierre UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
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
        "docs/UI_UX_PANEL_MAESTRO_TOP_15_READINESS_RESTORE_POINT_PUBLICATION_1_166.md",
        "tests/test_ui_ux_panel_maestro_top_15_readiness_restore_point_publication_1_166.py",
    }
    assert changed <= allowed
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
