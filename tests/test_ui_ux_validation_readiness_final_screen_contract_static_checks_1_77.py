from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_1_77.md"
README = ROOT / "README.md"
UI_FILES = [
    ROOT / "ui" / "web" / "index.html",
    ROOT / "ui" / "web" / "styles.css",
    ROOT / "ui" / "web" / "backend-contract-widgets.js",
    ROOT / "ui" / "web" / "admin-panels.js",
    ROOT / "ui" / "web" / "console-interactions.js",
    ROOT / "ui" / "web" / "domains.js",
    ROOT / "ui" / "web" / "i18n_es.json",
]

NEXT_PROMPT = (
    "PROMPT UI/UX 1.78 - Checkpoint Validation & Readiness Final Screen "
    "Contract IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_exact_final_contract_document_exists_once():
    assert DOC.exists()
    final_contracts = [
        path.name
        for path in (ROOT / "docs").glob("UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_*.md")
        if "_AUDIT_" not in path.name
    ]
    assert final_contracts == ["UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_1_77.md"]


def test_no_validation_readiness_screen_implementation_files_exist_in_active_ui():
    forbidden_file_name_parts = [
        "validation-readiness",
        "validation_readiness",
        "readiness-screen",
        "readiness_screen",
    ]
    active_ui_files = [
        path
        for path in (ROOT / "ui" / "web").glob("*")
        if path.is_file() and path.suffix in {".html", ".css", ".js", ".json"}
    ]

    unexpected = [
        path.name
        for path in active_ui_files
        if any(part in path.name.lower() for part in forbidden_file_name_parts)
    ]
    assert unexpected == []


def test_active_ui_files_do_not_materialize_validation_readiness_screen():
    forbidden_runtime_markers = [
        "validation-readiness-screen",
        "validationReadinessScreen",
        "renderValidationReadiness",
        "ValidationReadinessView",
        "#validation-readiness",
        "data-screen=\"validation-readiness\"",
        "fetch('/validation-readiness",
        'fetch("/validation-readiness',
        "/api/validation-readiness",
    ]

    for path in UI_FILES:
        text = read(path)
        for marker in forbidden_runtime_markers:
            assert marker not in text


def test_document_declares_no_screen_ui_user_panel_endpoints_or_runtime():
    text = read(DOC).lower()

    markers = [
        "no crea pantalla",
        "no modifica ui activa",
        "no crea user panel",
        "no crea rutas/hash",
        "no crea endpoints/api/router/fetches",
        "no instala dependencias",
        "no cambia ci",
        "no habilita runtime/execution/dispatch/controlled execution",
        "no crea unlock/override/bypass/permission escalation",
        "not implemented",
        "not created",
        "not modified",
        "not enabled",
    ]
    for marker in markers:
        assert marker in text


def test_semantic_guardrails_are_contextual_and_explicit():
    text = read(DOC)

    markers = [
        "Allowed States",
        "Forbidden States",
        "ready no significa ejecutable",
        "`ready` no significa permiso",
        "validation.valid=true no implica safe-to-execute",
        "`validation.valid` es dato declarado por contrato",
        "no live validation",
        "no background validation",
        "no runtime polling",
        "`allowed_actions` como dato, no CTA",
        "Allowed Actions as Data Guardrail",
        "Readiness Not Permission Guardrail",
        "Validation Not Execution Guardrail",
        "Relation With Existing Final Contracts",
        "Implementation Boundary",
    ]
    for marker in markers:
        assert marker in text


def test_readme_cursor_points_to_1_78_checkpoint():
    root = read(README)
    bt = "`"

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
