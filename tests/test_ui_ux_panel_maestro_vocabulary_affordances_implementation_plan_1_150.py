import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_IMPLEMENTATION_PLAN_1_150.md"
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


def test_document_exists_and_records_base_transition_and_strategy():
    assert DOC.exists()
    text = read(DOC)

    for marker in [
        "UI/UX Panel Maestro Vocabulary Affordances Implementation Plan 1.150",
        "89c83c5",
        "f455ca1",
        "main",
        "ahead",
        "working tree limpio",
        "contrato de vocabulario/affordances planificado pero no implementado",
        "Planificar implementacion futura",
        "sin implementarlo",
        "VOCABULARY_AFFORDANCES_CONTRACT_PLAN_READY_FOR_IMPLEMENTATION_PLANNING",
        "problema definido",
        "alcance",
        "fuera de alcance",
        "vocabulario permitido/prohibido",
        "affordances permitidas/prohibidas",
        "deudas actuales",
        "relacion con FSC/matriz",
        "validaciones futuras",
        "documental + test-only",
        "no conviene JSON estatico todavia",
    ]:
        assert marker in text


def test_document_records_future_files_and_contract_structure():
    text = read(DOC)

    for marker in [
        "docs/UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md",
        "tests/test_ui_ux_panel_maestro_vocabulary_affordances_contract_1_151.py",
        "ui/web/contracts/vocabulary_affordances_contract.v1.json",
        "tests/fixtures/ui_vocabulary_affordances_contract_v1.json",
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
        "known semantic debts",
        "enforcement plan",
        "future implementation gates",
    ]:
        assert marker in text


def test_document_records_allowlist_denylist_context_and_rules():
    text = read(DOC)

    for marker in [
        "Allowlist planificada",
        "Denylist planificada",
        "Terminos contextuales",
        "Reglas para UI visible",
        "Reglas para JS",
        "Reglas para docs/README",
        "Reglas para FSC/matriz",
        "Reglas para deudas actuales",
        "Validaciones futuras obligatorias",
        "Criterios de aceptacion futura",
        "FSC-CO-01",
        "FSC-BF-02",
        "FSC-VR-03",
        "FSC-RCP-04",
        'data-contract-screen-count="4"',
        "DEFER_FINALIZATION",
        "no fifth FSC",
        "matriz no operativa",
        "FSC no operativas",
        "+",
        "DOMAIN",
    ]:
        assert marker in text


def test_document_records_risks_mitigations_decision_and_limits():
    text = read(DOC)

    for marker in [
        "test demasiado fragil",
        "falsos positivos",
        "denylist demasiado amplia",
        "allowlist demasiado laxa",
        "contrato documental que parezca operativo",
        "JSON estatico confundido como runtime",
        "test contextual",
        "no JSON por defecto",
        "no UI activa",
        "no JS",
        "no backend",
        "VOCABULARY_AFFORDANCES_IMPLEMENTATION_PLAN_READY_FOR_GUARDED_IMPLEMENTATION",
        (
            "PROMPT UI/UX 1.151 - Implementar contrato de vocabulario affordances UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ),
        "no se implemento contrato",
        "no se creo contrato consumido por UI",
        "no se creo JSON contractual",
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


def test_readme_cursors_record_implementation_plan_1_150():
    for path in (README, WEB_README):
        text = read(path)
        assert "Planificacion de implementacion 1.150" in text
        assert "89c83c5" in text
        assert "restore point remoto vigente f455ca1" in text
        assert "main ahead por 1 commit al inicio" in text
        assert "contrato de vocabulario/affordances planificado pero no implementado" in text
        assert "documental + test-only" in text
        assert (
            "PROMPT UI/UX 1.151 - Implementar contrato de vocabulario affordances UI UX 1.x "
            "Panel Maestro IA_CORE contract-aware sin runtime/no-execution"
        ) in text
        lower_text = text.lower()
        assert "no implementacion" in lower_text
        assert "no contrato consumido por ui" in lower_text
        assert "no json contractual" in lower_text
        assert "no ui activa" in lower_text
        assert "no js" in lower_text
        assert "no backend" in lower_text
        assert "no runtime" in lower_text
        assert "no push" in lower_text


def test_prompt_1_150_did_not_modify_readonly_surfaces():
    result = subprocess.run(
        ["git", "diff", "--name-only", "89c83c5", "--", *PROTECTED],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout.strip() == ""
