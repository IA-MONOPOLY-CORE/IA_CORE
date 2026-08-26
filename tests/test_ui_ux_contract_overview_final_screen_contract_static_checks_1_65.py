from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_FINAL_SCREEN_CONTRACT_1_65.md"
ACTIVE_UI_FILES = [
    ROOT / "ui" / "web" / "index.html",
    ROOT / "ui" / "web" / "backend-contract-widgets.js",
    ROOT / "ui" / "web" / "admin-panels.js",
    ROOT / "ui" / "web" / "console-interactions.js",
    ROOT / "ui" / "web" / "styles.css",
    ROOT / "ui" / "web" / "domains.js",
]
FINAL_MARKERS = [
    "FSC-CO-01",
    "Contract Overview Final Screen Contract",
    "final-documental-not-implemented",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_final_contract_markers_are_documental_not_active_ui():
    doc = read(DOC)
    for marker in FINAL_MARKERS:
        assert marker in doc

    for path in ACTIVE_UI_FILES:
        text = read(path)
        for marker in FINAL_MARKERS:
            assert marker not in text, f"{marker} unexpectedly materialized in {path}"


def test_no_new_contract_overview_route_fetch_or_endpoint_is_declared():
    ui_text = "\n".join(read(path) for path in ACTIVE_UI_FILES)
    suspicious = [
        "contract-overview-final",
        "contractOverviewFinal",
        "/api/contract-overview",
        "/api/contracts/overview",
        "fetchContractOverview",
        "data-screen-contract-overview-final",
        "data-route-contract-overview",
    ]
    for marker in suspicious:
        assert marker not in ui_text


def test_document_preserves_static_no_runtime_and_no_execution_contract():
    doc = read(DOC)
    markers = [
        "no agrega endpoint",
        "no agrega fetch",
        "no modifica UI activa",
        "no crea User Panel",
        "no habilita runtime/execution/dispatch/controlled execution",
        "No-Implementation Boundary",
        "1.65 solo documenta y prueba",
        "No hacer push por defecto en 1.65",
    ]
    for marker in markers:
        assert marker in doc


def test_static_checks_are_contextual_and_do_not_forbid_documentary_mentions():
    doc = read(DOC)
    allowed_contexts = [
        "## Forbidden Actions",
        "## Forbidden States",
        "## Risk Register",
        "## Limites Para 1.66",
    ]
    for marker in allowed_contexts:
        assert marker in doc

    assert "Submit, send, execute, run, dispatch" in doc
    assert "active" in doc
    assert "runtime/execution leakage" in doc