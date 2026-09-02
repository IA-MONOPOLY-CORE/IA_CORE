from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_RESTORE_POINT_DECISION_1_157.md"
LEDGER = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md"
CHECKPOINT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_CHECKPOINT_1_156.md"
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


def test_decision_document_records_base_state_and_local_commits():
    assert DOC.exists()
    text = read(DOC)

    assert_markers(
        text,
        [
            "UI/UX Panel Maestro Capabilities Ledger Restore Point Decision 1.157",
            "HEAD esperado: `1478a66`",
            "Restore point remoto vigente: `f455ca1`",
            "`origin/main`: `f455ca1`",
            "`main` ahead de `origin/main` por `8 commits`",
            "No behind",
            "No diverged",
            "Working tree limpio",
            "Push no ejecutado",
            "Restore point posterior al ledger no publicado",
            "Matriz cerrada/publicada",
            "Vocabulario/affordances cerrado localmente",
            "Ledger cerrado localmente",
            "TOP 15 no ejecutado",
            "UI/UX 1.x no cerrado globalmente",
            "1478a66 docs(ui): checkpoint ledger capacidades",
            "059b163 docs(ui): implementar ledger capacidades",
            "845896c docs(ui): planificar implementacion ledger capacidades",
            "f524194 docs(ui): planificar ledger capacidades",
            "5eb2ed0 docs(ui): checkpoint contrato vocabulario affordances",
            "08da357 docs(ui): implementar contrato vocabulario affordances",
            "c9867c4 docs(ui): planificar implementacion contrato vocabulario",
            "89c83c5 docs(ui): planificar contrato vocabulario affordances",
        ],
    )


def test_decision_document_records_three_closed_blocks():
    text = read(DOC)

    assert_markers(
        text,
        [
            "Matriz: cerrada y publicada",
            "Matriz de cierre: implementada",
            "Matriz de cierre: corregida visualmente",
            "Matriz de cierre: checkpointed",
            "Matriz de cierre: publicada en `f455ca1`",
            "Vocabulario/affordances: cerrado localmente",
            "Contrato de vocabulario/affordances: planificado",
            "Contrato de vocabulario/affordances: implementacion planificada",
            "Contrato de vocabulario/affordances: implementado documental + test-only",
            "Contrato de vocabulario/affordances: checkpointed",
            "Ledger: cerrado localmente",
            "Ledger de capacidades: planificado",
            "Ledger de capacidades: implementacion planificada",
            "Ledger de capacidades: implementado documental + test-only",
            "Ledger de capacidades: micro-fix transition-aware aplicado",
            "Ledger de capacidades: checkpointed",
            "Los tres bloques recomendados estan completos localmente",
            "Solo la matriz esta publicada en remoto",
            "Vocabulario/affordances + ledger todavia no estan publicados en remoto",
            "TOP 15: futuro",
            "Cierre global UI/UX 1.x: futuro",
        ],
    )


def test_decision_document_evaluates_reasons_risks_and_blockers():
    text = read(DOC)

    assert_markers(
        text,
        [
            "Razones a favor de publicar",
            "8 commits locales acumulados",
            "Unidad estructural completa",
            "Tres bloques recomendados cerrados localmente",
            "inventario contractual de capacidades presentes, bloqueadas y futuras",
            "test historico 1.154",
            "Validaciones relevantes pasan",
            "No hay runtime/execution",
            "No hay JSON ledger",
            "No hay consumo por UI/backend",
            "No hay cambios activos UI/JS/backend",
            "Antes de TOP 15 conviene tener punto remoto seguro",
            "repo clonable desde otro entorno",
            "Riesgos de publicar ahora",
            "deuda semantica aun no resuelta",
            "+ / DOMAIN",
            "Scripts inferiores heredados",
            "Tecnicismo documental alto",
            "TOP 15 aun no auditado",
            "UI/UX 1.x aun no cerrado globalmente",
            "No hay JSON ledger, por decision actual",
            "Ledger no es visible ni consumido por UI",
            "confundirse con cierre final",
            "Riesgos de no publicar ahora",
            "8 commits locales quedan sin respaldo remoto",
            "Bloque ledger queda sin restore point",
            "TOP 15 se iniciaria sin punto remoto seguro",
            "Rollback dificil",
            "Clonado/verificacion desde otra maquina",
            "Audit trail queda local-only",
            "Blockers evaluados",
            "Tests relevantes pasan",
            "Working tree limpio",
            "No secrets",
            "No .env",
            "No fixture ledger",
            "No UI activa",
            "No JS",
            "No backend",
            "No runtime",
            "No execution",
            "No endpoints",
            "No User Panel",
            "No cierre global falso",
        ],
    )


def test_decision_document_records_publication_conditions_top15_decision_next_and_limits():
    text = read(DOC)

    assert_markers(
        text,
        [
            "Condiciones obligatorias para publicar",
            "HEAD esperado de publicacion debe ser el commit de 1.157",
            "`origin/main` debe seguir en f455ca1",
            "`main` debe estar ahead de `origin/main` por 9 commits",
            "Tests relevantes deben pasar",
            "Backup readiness debe pasar",
            "Backend payload/contracts deben pasar",
            "`git diff --check` debe pasar",
            "No force push",
            "No rebase",
            "No reset",
            "No merge innecesario",
            "No branches nuevos",
            "HEAD == origin/main",
            "working tree limpio",
            "TOP 15 no se ejecuta en 1.157",
            "TOP 15 no se ejecuta en publicacion",
            "TOP 15 comienza recien despues del restore point ledger publicado",
            "TOP 15 debe auditar, no implementar automaticamente",
            "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLICATION_SELECTED",
            "PROMPT UI/UX 1.158 - Publicar restore point ledger capacidades UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "no se hizo push",
            "no se publico restore point",
            "no se ejecuto TOP 15 recomendaciones elite",
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
        ],
    )


def test_ledger_checkpoint_and_contract_151_are_preserved():
    assert LEDGER.exists()
    ledger = read(LEDGER)
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

    assert CHECKPOINT.exists()
    assert "CAPABILITIES_LEDGER_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION" in read(CHECKPOINT)

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


def test_static_ledger_files_absent_and_ui_markers_read_only():
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


def test_readme_cursors_record_decision_157():
    for path in (README, UI_README):
        text = read(path)
        assert_markers(
            text,
            [
                "Decision 1.157 de restore point ledger",
                "HEAD base `1478a66`",
                "restore point remoto vigente `f455ca1`",
                "main ahead por 8 commits al inicio",
                "matriz cerrada/publicada",
                "vocabulario/affordances cerrado localmente",
                "ledger cerrado localmente",
                "tres bloques recomendados cerrados localmente",
                "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLICATION_SELECTED",
                "publicacion seleccionada",
                "no push",
                "no restore point",
                "no JSON ledger",
                "no fixture ledger",
                "no ledger consumido por UI",
                "no helper operativo",
                "no enforcement activo",
                "no UI activa",
                "no JS",
                "no backend",
                "no runtime",
                "TOP 15 diferido",
                "UI/UX 1.x no cerrado globalmente",
                "PROMPT UI/UX 1.158 - Publicar restore point ledger capacidades UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
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

