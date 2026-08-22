from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "ui" / "web"
DOC = ROOT / "docs" / "UI_UX_FRONTEND_INCONGRUENCE_HARDENING_1_21.md"
README = WEB / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_hardening_document_records_scope_and_verdicts():
    text = read(DOC)

    assert "b2c2c1ce" in text
    assert "UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md" in text
    for verdict in [
        "UI_UX_FRONTEND_INCONGRUENCE_HARDENING_COMPLETED",
        "FRONTEND_P1_INCONGRUENCES_HARDENED",
        "DEBATE_LEGACY_FRONTEND_BOUNDARY_HARDENED",
        "ORCHESTRATION_LEGACY_FRONTEND_BOUNDARY_HARDENED",
        "LOGS_RUNTIME_FRONTEND_BOUNDARY_HARDENED",
        "STATUS_DOT_ACTIVE_OPERATIONAL_AMBIGUITY_REMOVED",
        "FRONTEND_FALSE_POSITIVES_PRESERVED",
        "FRONTEND_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_FRONTEND_INCONGRUENCE_CHECKPOINT",
    ]:
        assert verdict in text


def test_active_frontend_uses_request_draft_and_request_contract_names():
    active = "\n".join(
        read(WEB / name)
        for name in [
            "index.html",
            "admin-panels.js",
            "console-interactions.js",
            "styles.css",
        ]
    )

    legacy_tokens = [
        "debate-panel",
        "debate-toggle",
        "debate-input",
        "btn-debate",
        "debate-metrics",
        "debate-synthesis",
        "debate-consensus-score",
        "orchestration-task",
        "orchestration-mode",
        "orchestration-agents",
        "orchestration-status",
        "orchestration-scores",
        "orchestration-steps",
        "config-orchestration",
        'data-section="orchestration"',
        "logs-runtime",
        "activeAgentProfileCatalog",
        ".status-dot.active",
        ".config-sidebar-item.active",
        ".config-section.active",
        ".skin-option.active",
        "classList.add('active')",
        "classList.remove('active')",
    ]
    for token in legacy_tokens:
        assert token not in active

    for token in [
        "request-draft-panel",
        "request-draft-toggle",
        "request-draft-input",
        "request-draft-control",
        "request-draft-metrics",
        "request-draft-synthesis",
        "request-draft-consensus-score",
        "request-contract-draft",
        "request-contract-mode",
        "request-contract-sources",
        "request-contract-status",
        "request-contract-summary",
        "request-contract-validation",
        "config-request-contract",
        'data-section="request-contract"',
        "logs-sanitized",
        "currentAgentProfileCatalog",
        ".status-dot.ready",
        ".config-sidebar-item.is-selected",
        ".config-section.is-visible",
        ".skin-option.is-selected",
    ]:
        assert token in active


def test_contract_boundaries_and_false_positives_are_preserved():
    widgets = read(WEB / "backend-contract-widgets.js")
    interactions = read(WEB / "console-interactions.js")
    admin = read(WEB / "admin-panels.js")
    active = "\n".join(read(WEB / name) for name in ["index.html", "admin-panels.js"])

    assert "PROHIBITED_ACTIVE_STATUSES" in widgets
    assert "block: 'start'" in interactions
    assert "active_provider" in admin
    assert "active_model" in admin
    assert "status.running" in admin

    for forbidden in [
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
        "hashchange",
        "history.pushState",
        "history.replaceState",
    ]:
        assert forbidden not in active

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "SAAOP" not in active
    assert "Loteria" not in active
    assert "lottery" not in active.lower()
    assert "Tactical HUD" not in active
    assert "U-Score" not in active
    assert "CAZADOR" not in active
    assert "ESPEJO" not in active


def test_readme_registers_1_21_continuity():
    readme = read(README)

    assert "Hardening frontend incongruence 1.21" in readme
    assert "request-draft-*" in readme
    assert "request-contract-*" in readme
    assert "logs-sanitized" in readme
    assert "PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence" in readme