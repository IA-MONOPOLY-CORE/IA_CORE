import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_PLAN_1_149.md"
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


def test_document_exists_and_records_base_transition_and_problem():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Vocabulary Affordances Contract Plan 1.149",
        "f455ca1",
        "main",
        "origin/main",
        "sincronizado",
        "working tree limpio",
        "matriz de cierre UI/UX 1.x publicada",
        "Planificar contrato de vocabulario/affordances",
        "sin implementarlo",
        "matriz de cierre completada",
        "restore point publicado",
        "secuencia 1.142",
        "segundo bloque",
        "ambiguedad semantica",
        "copy operativo falso",
        "affordances fantasma",
        "runtime copy",
        "no-execution",
    ]:
        assert marker in text


def test_document_records_scope_and_out_of_scope():
    text = read(DOC)

    for marker in [
        "vocabulario visible",
        "labels",
        "badges",
        "chips",
        "cards",
        "empty states",
        "blocked",
        "deferred",
        "read-only",
        "scripts UI",
        "documentacion UI",
        "tests UI",
        "matriz de cierre",
        "FSC",
        "Fuera de alcance",
        "backend",
        "runtime",
        "ejecucion",
        "endpoints",
        "modelos",
        "tools",
        "integrations",
        "User Panel",
        "acciones",
    ]:
        assert marker in text


def test_document_records_vocabularies_affordances_and_debts():
    text = read(DOC)

    for marker in [
        "lectura/documentacion",
        "estados seguros",
        "capacidades bloqueadas/futuras",
        "acciones no operativas",
        "runtime/ejecucion",
        "exito falso",
        "promesas no soportadas",
        "affordances operativas",
        "Affordances permitidas",
        "Affordances prohibidas",
        "+",
        "DOMAIN",
        "scripts inferiores heredados",
        "tecnicismo documental alto",
    ]:
        assert marker in text


def test_document_records_fsc_strategy_validations_risks_and_mitigations():
    text = read(DOC)

    for marker in [
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
        "no quinta FSC",
        "matriz no operativa",
        "FSC no operativas",
        "Estrategia futura de implementacion",
        "Validaciones futuras sugeridas",
        "sobrebloquear lenguaje util",
        "copy ambiguo",
        "contrato demasiado rigido",
        "confundir planificado con ejecutable",
        "allowlist",
        "denylist",
        "tests documentales",
        "inspeccion UI solo lectura",
    ]:
        assert marker in text


def test_document_records_decision_next_prompt_and_limits():
    text = read(DOC)

    allowed_decisions = [
        "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_IMPLEMENTATION_PLANNING",
        "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_GUARDED_IMPLEMENTATION",
        "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_NEEDS_OPERATOR_DECISION",
        "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_BLOCKED_NEEDS_FIX",
        "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_BLOCKED_CRITICAL",
    ]
    assert any(decision in text for decision in allowed_decisions)
    assert "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_IMPLEMENTATION_PLANNING" in text
    assert (
        "PROMPT UI/UX 1.150 - Planificar implementacion contrato de vocabulario affordances UI UX 1.x "
        "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
    ) in text

    for marker in [
        "no se implemento contrato",
        "no se creo contrato consumido por UI",
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
        "no se avanzo a implementacion",
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


def test_readme_cursors_record_vocabulary_affordances_plan_1_149():
    for path in (README, WEB_README):
        text = read(path)
        assert "Planificacion 1.149: contrato de vocabulario/affordances UI/UX 1.x" in text
        assert "f455ca1" in text
        assert "restore point remoto vigente f455ca1" in text
        assert "matriz de cierre UI/UX 1.x publicada" in text
        assert "segundo bloque de la secuencia 1.142" in text
        assert "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_IMPLEMENTATION_PLANNING" in text
        assert (
            "PROMPT UI/UX 1.150 - Planificar implementacion contrato de vocabulario affordances UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text
        assert "no push" in lower_text


def test_prompt_1_149_did_not_modify_readonly_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "f455ca1", "--", *PROTECTED],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
