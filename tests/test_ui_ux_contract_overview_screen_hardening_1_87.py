import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_SCREEN_HARDENING_1_87.md"


def read_index():
    return INDEX.read_text(encoding="utf-8")


def contract_overview_markup():
    match = re.search(
        r'<section\b[^>]*id="contract-overview-screen"[^>]*>(.*?)</section>',
        read_index(),
        re.DOTALL,
    )
    assert match, "Contract Overview section is missing"
    return match.group(0)


def test_hardened_contract_overview_keeps_identity_and_priority_guardrails():
    markup = contract_overview_markup().lower()
    markers = (
        'id="contract-overview-screen"',
        'data-contract-screen="fsc-co-01"',
        "contract overview",
        "fsc-co-01",
        "ia_core",
        "panel maestro",
        "backend_internal_ui_payload.v1",
        "ready-no-permission",
        "no-runtime",
        "no-execution",
        "data-contract-overview-state",
        "role=""status""",
        "evidence snapshot",
    )
    assert all(marker in markup for marker in markers if "role" not in marker)
    assert 'role="status"' in markup


def test_hardened_contract_overview_keeps_limits_visible_and_actions_read_only():
    markup = contract_overview_markup().lower()
    markers = (
        "allowed_actions",
        "no son botones",
        "forbidden_actions",
        "blocked_capabilities",
        "blockers",
        "runtime / execution / dispatch",
        "endpoint / worker / queue / user panel",
        "snapshot documental",
        "no log vivo",
        "no ejecuta, no envia, no conecta endpoints",
        "empty",
        "deferred",
    )
    assert all(marker in markup for marker in markers)
    assert 'data-contract-overview-block="forbidden-actions"' in markup
    assert 'data-contract-overview-block="blocked-capabilities"' in markup


def test_hardened_contract_overview_has_no_operational_affordance_or_new_surface():
    markup = contract_overview_markup().lower()
    assert "<button" not in markup
    assert "<form" not in markup
    assert "href=" not in markup
    assert "action=" not in markup
    assert "data-route" not in markup
    assert "data-hash" not in markup
    assert "window.location" not in markup
    assert "fetch(" not in markup
    assert "<script" not in markup
    assert 'data-state="running"' not in markup
    assert 'data-state="live"' not in markup
    assert 'data-state="executing"' not in markup
    assert "success operativo" not in markup
    assert "completed operativo" not in markup
    assert "ghost" not in markup


def test_hardened_contract_overview_does_not_activate_legacy_identity():
    markup = contract_overview_markup().lower()
    assert "loteria" not in markup
    assert "saaop" not in markup
    assert "active identity" not in markup


def test_hardening_document_records_decision_and_review_boundary():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8").lower()
    markers = (
        "ui/ux contract overview screen hardening 1.87",
        "1ceb9c6",
        "d20a5d1",
        "contract_overview_screen_implemented_needs_hardening",
        "fsc-co-01",
        "backend_internal_ui_payload.v1",
        "panel maestro",
        "visual review",
        "no fetch",
        "no endpoint",
        "no user panel",
        "no runtime",
        "no execution",
        "no dispatch",
        "rollback",
        "contract_overview_screen_hardened_ready_for_human_visual_review",
        "prompt ui/ux 1.88 - checkpoint contract overview screen implementada y hardenizada ia_core contract-aware sin runtime/no-execution",
    )
    assert all(marker in text for marker in markers)
