import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CHECKPOINT_1_152.md"
CONTRACT = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
DISALLOWED_JSON = ROOT / "ui" / "web" / "contracts" / "vocabulary_affordances_contract.v1.json"
DISALLOWED_FIXTURE = ROOT / "tests" / "fixtures" / "ui_vocabulary_affordances_contract_v1.json"
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


def test_checkpoint_document_exists_and_records_base_state():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Vocabulary Affordances Checkpoint 1.152",
        "08da357",
        "f455ca1",
        "main",
        "ahead",
        "3 commits",
        "working tree limpio",
        "contrato de vocabulario/affordances implementado como documental + test-only",
        "Checkpoint del contrato de vocabulario/affordances",
        "sin implementar nada nuevo",
        "89c83c5 docs(ui): planificar contrato vocabulario affordances",
        "c9867c4 docs(ui): planificar implementacion contrato vocabulario",
        "08da357 docs(ui): implementar contrato vocabulario affordances",
    ]:
        assert marker in text


def test_checkpoint_records_transition_and_contract_sections():
    text = read(DOC)

    for marker in [
        "contrato documental creado",
        "test creado",
        "READMEs actualizados",
        "no JSON contractual",
        "no UI consumption",
        "no backend consumption",
        "no helper operativo",
        "no enforcement activo",
        "no UI activa",
        "no JS",
        "no backend",
        "VOCABULARY_AFFORDANCES_CONTRACT_IMPLEMENTED_TEST_ONLY",
        "metadata",
        "purpose",
        "scope",
        "out of scope",
        "allowed vocabulary",
        "forbidden vocabulary",
        "contextual terms",
        "allowed affordances",
        "forbidden affordances",
        "FSC preservation",
        "DEFER preservation",
        "matrix preservation",
        "known semantic debts",
        "enforcement model test-only",
        "contextual validation rules",
        "future gates",
        "non-goals",
        "limits preserved",
    ]:
        assert marker in text


def test_checkpoint_records_material_limits_and_contract_metadata():
    text = read(DOC)

    for marker in [
        "ui/web/contracts/vocabulary_affordances_contract.v1.json",
        "no existe",
        "tests/fixtures/ui_vocabulary_affordances_contract_v1.json",
        "json_contract: NOT_CREATED",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "enforcement: TEST_ONLY",
        "no import JS",
        "no fetch",
        "no endpoint",
        "no runtime validator",
        "no backend validator",
        "no helper operativo",
        "UI solo lectura",
        "JS solo lectura",
        "backend no tocado",
        "scripts inferiores no modificados",
        "+ no renombrado",
        "DOMAIN no renombrado",
    ]:
        assert marker in text

    assert CONTRACT.exists()
    contract = read(CONTRACT)
    for marker in [
        "UI/UX Panel Maestro Vocabulary Affordances Contract 1.151",
        "contract_id: ui_ux_panel_maestro_vocabulary_affordances_contract",
        "mode: DOCUMENTATION_ONLY",
        "status: TEST_ONLY_CONTRACT",
        "runtime: NO_RUNTIME",
        "execution: NO_EXECUTION",
        "ui_consumption: NOT_CONSUMED_BY_UI",
        "backend_consumption: NOT_CONSUMED_BY_BACKEND",
        "json_contract: NOT_CREATED",
        "enforcement: TEST_ONLY",
        "VOCABULARY_AFFORDANCES_CONTRACT_IMPLEMENTED_TEST_ONLY",
    ]:
        assert marker in contract


def test_checkpoint_preserves_fsc_defer_matrix_sequence_and_risks():
    text = read(DOC)

    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "no quinta FSC",
        "DEFER_FINALIZATION",
        "matriz de cierre UI/UX 1.x",
        "matriz read-only",
        "matriz no wizard",
        "matriz no operativa",
        "Matriz: cerrada y publicada",
        "Vocabulario/affordances: checkpointed",
        "Ledger de capacidades: proximo bloque pendiente",
        "contrato todavia no aplicado visualmente",
        "copy visible futuro puede necesitar revision humana",
        "ledger aun no existe",
        "+ / DOMAIN siguen como deuda semantica",
        "scripts inferiores heredados siguen como deuda menor/futura",
        "tecnicismo documental alto sigue pendiente",
        "aun no hay cierre global UI/UX 1.x",
        "aun no hay restore point posterior al contrato",
        "tests estaticos",
        "FSC preservadas",
        "DEFER_FINALIZATION` preservado",
        "proximo bloque ledger",
    ]:
        assert marker in text


def test_checkpoint_decision_next_prompt_and_limits():
    text = read(DOC)

    for marker in [
        "VOCABULARY_AFFORDANCES_CHECKPOINT_PASSED_READY_FOR_LEDGER_PLANNING",
        (
            "PROMPT UI/UX 1.153 - Planificar ledger de capacidades presentes bloqueadas futuras "
            "UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ),
        "no se implemento ledger",
        "no se planifico ledger con detalle",
        "no se creo documento ledger",
        "no se creo test ledger",
        "no se implemento contrato adicional",
        "no se amplio contrato 1.151 con reglas nuevas",
        "no se creo JSON contractual",
        "no se creo fixture contractual JSON",
        "no se creo contrato consumido por UI",
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
        "no se hizo push",
        "no se publico restore point",
        "no se cerro UI/UX 1.x globalmente",
    ]:
        assert marker in text


def test_no_static_json_contract_files_exist():
    assert not DISALLOWED_JSON.exists()
    assert not DISALLOWED_FIXTURE.exists()


def test_current_ui_readonly_surface_preserves_expected_markers():
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


def test_readme_cursors_record_checkpoint_1_152():
    for path in (README, WEB_README):
        text = read(path)
        assert "Checkpoint 1.152: contrato de vocabulario/affordances" in text
        assert "HEAD base `08da357`" in text
        assert "restore point remoto vigente `f455ca1`" in text
        assert "main ahead por 3 commits al inicio" in text
        assert "contrato 1.151 implementado como documental + test-only" in text
        assert "no JSON contractual" in text
        assert "no contrato consumido por UI" in text
        assert "no helper operativo" in text
        assert "no enforcement activo" in text
        assert "no UI activa" in text
        assert "no JS" in text
        assert "no backend" in text
        assert "no runtime" in text
        assert "matriz: cerrada y publicada" in text
        assert "vocabulario/affordances: checkpointed" in text
        assert "ledger de capacidades: proximo bloque pendiente" in text
        assert (
            "PROMPT UI/UX 1.153 - Planificar ledger de capacidades presentes bloqueadas futuras "
            "UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        assert "no push" in text


def test_prompt_1_152_did_not_modify_protected_runtime_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "08da357", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
