from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_checkpoint_1_22_document_exists_and_links_chain():
    text = read(DOC)

    for marker in [
        "d4d36563",
        "UI_UX_NEXT_BLOCK_PLAN_1_19.md",
        "UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md",
        "UI_UX_FRONTEND_INCONGRUENCE_HARDENING_1_21.md",
        "IA_CORE_GITHUB_BACKUP_READY.md",
        "GitHub",
        "https://github.com/IA-MONOPOLY-CORE/IA_CORE",
    ]:
        assert marker in text


def test_checkpoint_1_22_records_legacy_to_canonical_hardening():
    text = read(DOC)

    for marker in [
        "debate-*",
        "request-draft-*",
        "orchestration-*",
        "request-contract-*",
        "logs-runtime",
        "logs-sanitized",
        ".status-dot.active",
        ".status-dot.ready",
        "is-selected",
        "is-visible",
        "currentAgentProfileCatalog",
    ]:
        assert marker in text


def test_checkpoint_1_22_confirms_false_positives_and_visual_evidence():
    text = read(DOC)

    for marker in [
        "PROHIBITED_ACTIVE_STATUSES",
        "block: 'start'",
        "active_provider",
        "active_model",
        "status.running",
        "i18n legacy no enlazado activamente",
        "evidencia visual humana",
        "paleta mas descansada",
        "runner visual automatizado",
        "no hay `package.json`, configuracion Playwright/Vite ni runner visual local disponible",
    ]:
        assert marker in text


def test_checkpoint_1_22_confirms_contract_limits_and_identity():
    text = read(DOC)

    for marker in [
        "no-runtime/no-execution",
        "no endpoint nuevo",
        "no API/router nuevo",
        "no hash routing operativo nuevo",
        "no librerias nuevas",
        "no dependencias nuevas",
        "IA_CORE como identidad activa",
        "No aparece SAAOP como UI activa",
        "no aparece Loteria como UI activa",
        "no aparece Tactical HUD como UI activa",
        "no aparece U-Score como UI activa",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
    ]:
        assert marker in text


def test_checkpoint_1_22_verdicts_and_next_prompt_are_recorded():
    text = read(DOC)

    for verdict in [
        "UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_PASSED",
        "FRONTEND_INCONGRUENCE_BLOCK_CONFIRMED",
        "FRONTEND_P1_HARDENING_CONFIRMED",
        "FRONTEND_FALSE_POSITIVES_PRESERVED_CONFIRMED",
        "FRONTEND_UI_ACTIVE_LEGACY_BOUNDARY_CONFIRMED",
        "FRONTEND_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "FRONTEND_NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
        "GITHUB_BACKUP_RESTORE_POINT_CONFIRMED",
        "UI_READY_FOR_NEXT_BLOCK_PLANNING",
    ]:
        assert verdict in text

    assert (
        "PROMPT UI/UX 1.23 - Consolidar siguiente bloque UI/UX post Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution"
        in text
    )


def test_readmes_register_checkpoint_1_22_and_continuity():
    root = read(README)
    ui = read(UI_README)

    for text in [root, ui]:
        assert "UI/UX cerrado hasta 1.22" in text
        assert "PROMPT UI/UX 1.23 - Consolidar siguiente bloque UI/UX post Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution" in text

    assert "docs/UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md" in root
    assert "Checkpoint frontend incongruence 1.22" in ui