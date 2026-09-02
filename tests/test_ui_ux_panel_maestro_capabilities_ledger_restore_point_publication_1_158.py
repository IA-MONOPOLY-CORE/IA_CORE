from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_RESTORE_POINT_PUBLICATION_1_158.md"
DECISION_157 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_RESTORE_POINT_DECISION_1_157.md"
CHECKPOINT_156 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_CHECKPOINT_1_156.md"
LEDGER_155 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md"
CONTRACT_151 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"

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


def assert_markers(text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    assert not missing


def test_publication_document_records_base_state_and_objective():
    assert DOC.exists()
    text = read(DOC)

    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Capabilities Ledger Restore Point Publication 1.158",
            "HEAD esperado al inicio `fba87de`",
            "Restore point remoto previo `f455ca1`",
            "`origin/main` previo `f455ca1`",
            "`main` ahead de `origin/main` por 9 commits al inicio",
            "Working tree limpio",
            "Publicacion seleccionada en 1.157",
            "Matriz publicada",
            "Vocabulario/affordances cerrado localmente",
            "Ledger cerrado localmente",
            "TOP 15 no ejecutado",
            "UI/UX 1.x no cerrado globalmente",
            "Publicar restore point remoto del bloque ledger con validaciones repetidas y push unico",
        ],
    )


def test_publication_document_lists_commits_conditions_validations_and_push_rules():
    text = read(DOC)

    assert_markers(
        text,
        [
            "89c83c5 docs(ui): planificar contrato vocabulario affordances",
            "c9867c4 docs(ui): planificar implementacion contrato vocabulario",
            "08da357 docs(ui): implementar contrato vocabulario affordances",
            "5eb2ed0 docs(ui): checkpoint contrato vocabulario affordances",
            "f524194 docs(ui): planificar ledger capacidades",
            "845896c docs(ui): planificar implementacion ledger capacidades",
            "059b163 docs(ui): implementar ledger capacidades",
            "1478a66 docs(ui): checkpoint ledger capacidades",
            "fba87de docs(ui): decidir restore point ledger capacidades",
            "commit de publicacion 1.158: PENDING_UNTIL_COMMIT",
            "HEAD `fba87de`",
            "origin/main `f455ca1`",
            "Local ahead por 9 commits",
            "No behind",
            "No diverged",
            "No JSON ledger",
            "No fixture ledger",
            "No UI activa",
            "No JS",
            "No backend",
            "No runtime",
            "No execution",
            "No TOP 15",
            "No cierre global UI/UX 1.x",
            "4 `node --check`",
            "test 1.158",
            "test 1.157",
            "test 1.156",
            "test 1.155",
            "test 1.154 transition-aware",
            "test 1.153",
            "test 1.152",
            "test 1.151",
            "test 1.150",
            "test 1.149",
            "test 1.148",
            "test 1.147",
            "test 1.146",
            "test 1.145.A",
            "test 1.145",
            "backup readiness",
            "backend payload/contracts",
            "`git diff --check`",
            "`git push origin main`",
            "Push unico",
            "No force push",
            "No rebase",
            "No reset",
            "No merge innecesario",
            "No branch nuevo",
        ],
    )


def test_publication_document_records_post_push_expectations_top15_decision_next_and_limits():
    text = read(DOC)

    assert_markers(
        text,
        [
            "Ejecutar `git fetch origin`",
            "Confirmar `HEAD == origin/main`",
            "Confirmar working tree limpio",
            "Confirmar `git status` sin ahead/behind",
            "Confirmar nuevo restore point remoto como commit de 1.158",
            "remoto ya no queda en `f455ca1`",
            "`origin/main` debe ser igual al commit final 1.158",
            "`HEAD` debe ser igual al commit final 1.158",
            "`main` no debe quedar ahead",
            "`main` no debe quedar behind",
            "Restore point ledger publicado",
            "TOP 15 no se ejecuta en 1.158",
            "TOP 15 no se planifica en detalle en 1.158",
            "TOP 15 queda como siguiente bloque despues de publicacion",
            "TOP 15 debe auditar, no implementar automaticamente",
            "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLISHED",
            "PROMPT UI/UX 1.159 - Planificar auditoria TOP 15 recomendaciones elite cierre coronado UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "no se ejecuto TOP 15 recomendaciones elite",
            "no se planifico TOP 15 en detalle",
            "no se cerro UI/UX 1.x globalmente",
            "no se implemento ledger nuevo",
            "no se rehizo ledger 1.155",
            "no se creo JSON ledger",
            "no se creo fixture ledger",
            "no se creo ledger consumido por UI",
            "no se creo helper operativo",
            "no se creo enforcement activo",
            "no se modifico UI activa",
            "no se modifico index.html",
            "no se modifico styles.css",
            "no se modifico i18n_es.json",
            "no se modifico JS",
            "no se agregaron listeners",
            "no se agregaron fetches",
            "no se agrego localStorage",
            "no se agregaron rutas/hash",
            "no se agrego window.location",
            "no se agrego history",
            "no se creo User Panel",
            "no se crearon endpoints",
            "no se toco backend",
            "no se toco runtime",
            "no se modifico contrato funcional",
            "no se creo contrato final operativo",
            "no se contradijo DEFER_FINALIZATION",
            "no se renombro +",
            "no se renombro DOMAIN",
            "no se modificaron scripts inferiores",
            "no se limpio deuda residual general",
            "no se corrigieron pyflakes",
            "no se uso force push",
            "no se uso rebase/reset/merge/branch nuevo",
        ],
    )


def test_ledger_checkpoint_decision_and_contract_are_preserved():
    assert LEDGER_155.exists()
    ledger = read(LEDGER_155)
    assert_markers(
        ledger,
        [
            "status: TEST_ONLY_LEDGER",
            "runtime: NO_RUNTIME",
            "execution: NO_EXECUTION",
            "json_ledger: NOT_CREATED",
            "ui_consumption: NOT_CONSUMED_BY_UI",
            "backend_consumption: NOT_CONSUMED_BY_BACKEND",
            "enforcement: TEST_ONLY",
        ],
    )

    assert CHECKPOINT_156.exists()
    assert "CAPABILITIES_LEDGER_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION" in read(CHECKPOINT_156)

    assert DECISION_157.exists()
    assert "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLICATION_SELECTED" in read(DECISION_157)

    assert CONTRACT_151.exists()
    contract = read(CONTRACT_151)
    assert_markers(
        contract,
        [
            "mode: DOCUMENTATION_ONLY",
            "status: TEST_ONLY_CONTRACT",
            "runtime: NO_RUNTIME",
            "execution: NO_EXECUTION",
            "ui_consumption: NOT_CONSUMED_BY_UI",
            "backend_consumption: NOT_CONSUMED_BY_BACKEND",
            "json_contract: NOT_CREATED",
            "enforcement: TEST_ONLY",
        ],
    )


def test_static_ledger_files_absent_and_ui_surface_read_only():
    assert not (ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json").exists()
    assert not (ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json").exists()

    index = read(INDEX)
    assert_markers(
        index,
        [
            "Matriz de cierre UI/UX 1.x",
            "FSC-CO-01",
            "FSC-BF-02",
            "FSC-VR-03",
            "FSC-RCP-04",
            'data-contract-screen-count="4"',
            "DEFER_FINALIZATION",
        ],
    )

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


def test_readme_cursors_record_publication_158():
    for path in (README, UI_README):
        text = read(path)
        assert_markers(
            text,
            [
                "Publicacion 1.158 del restore point ledger",
                "HEAD base `fba87de`",
                "restore point remoto previo `f455ca1`",
                "main ahead por 9 commits al inicio",
                "commit final 1.158",
                "nuevo restore point remoto despues del push",
                "matriz cerrada/publicada",
                "vocabulario/affordances publicado en nuevo restore point",
                "ledger publicado en nuevo restore point",
                "tres bloques recomendados publicados",
                "no JSON ledger",
                "no fixture ledger",
                "no ledger consumido por UI",
                "no helper operativo",
                "no enforcement activo",
                "no UI activa",
                "no JS",
                "no backend",
                "no runtime",
                "TOP 15 no ejecutado",
                "TOP 15 proximo bloque",
                "UI/UX 1.x no cerrado globalmente",
                "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLISHED",
                "PROMPT UI/UX 1.159 - Planificar auditoria TOP 15 recomendaciones elite cierre coronado UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            ],
        )


def test_protected_runtime_surfaces_have_no_diff_against_head():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout.strip() == ""

