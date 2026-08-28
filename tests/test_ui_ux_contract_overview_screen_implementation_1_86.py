import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_SCREEN_IMPLEMENTATION_1_86.md"


def read_index():
    return INDEX.read_text(encoding="utf-8")


def contract_overview_markup():
    text = read_index()
    match = re.search(
        r'<section\b[^>]*id="contract-overview-screen"[^>]*>(.*?)</section>',
        text,
        re.DOTALL,
    )
    assert match, "Contract Overview section is missing"
    return match.group(0)


def test_contract_overview_screen_has_contract_identity_and_read_only_structure():
    markup = contract_overview_markup().lower()
    markers = (
        'id="contract-overview-screen"',
        'data-contract-screen="FSC-CO-01"',
        "Contract Overview",
        "FSC-CO-01",
        "IA_CORE",
        "Panel Maestro",
        "solo lectura",
        "ready-no-permission",
        "backend_internal_ui_payload.v1",
        "Readiness vs permission",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "snapshot documental",
        "no-runtime",
        "no-execution",
        "no User Panel",
        "empty",
        "deferred",
    )
    assert all(marker.lower() in markup for marker in markers)


def test_contract_overview_actions_are_data_only_and_blockers_are_visible():
    markup = contract_overview_markup().lower()
    assert "allowed_actions</code> son datos contractuales y no son botones" in markup
    assert "forbidden_actions" in markup
    assert "blocked_capabilities" in markup
    assert "runtime / execution / dispatch" in markup
    assert "endpoint / worker / queue / user panel" in markup
    assert "no ejecuta, no envia, no conecta endpoints" in markup
    assert "no hay run, dispatch ni submit" in markup
    assert "no log vivo" in markup


def test_contract_overview_has_no_operational_controls_or_new_navigation():
    markup = contract_overview_markup()
    assert "<button" not in markup.lower()
    assert "<form" not in markup.lower()
    assert "href=" not in markup.lower()
    assert "action=" not in markup.lower()
    assert "data-route" not in markup.lower()
    assert "data-hash" not in markup.lower()
    assert "window.location" not in markup
    assert "fetch(" not in markup
    assert "<script" not in markup.lower()


def test_contract_overview_does_not_activate_legacy_identity_or_runtime_state():
    markup = contract_overview_markup().lower()
    assert "loteria" not in markup
    assert "saaop" not in markup
    assert "running" not in markup
    assert "executing" not in markup
    assert "dispatching" not in markup
    assert "ready to run" not in markup
    assert "success operativo" not in markup
    assert "completed operativo" not in markup


def test_implementation_document_exists_and_records_review_boundary():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8").lower()
    markers = (
        "ui/ux contract overview screen implementation 1.86",
        "9fb9d55",
        "d20a5d1",
        "fsc-co-01",
        "backend_internal_ui_payload.v1",
        "panel maestro",
        "revision visual humana queda pendiente",
        "rollback",
    )
    assert all(marker in text for marker in markers)
