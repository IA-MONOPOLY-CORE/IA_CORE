from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_SCREEN_CHECKPOINT_1_94.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.95 - Planificar siguiente pantalla Final Screen Contract tras "
    "Blocked & Forbidden IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    assert path.exists(), f"Missing required file: {path}"
    return path.read_text(encoding="utf-8")


def blocked_forbidden_section() -> str:
    html = read(INDEX)
    start = html.index('id="blocked-forbidden-screen"')
    section_start = html.rfind("<section", 0, start)
    section_end = html.index('<section class="density-priority-strip"', start)
    return html[section_start:section_end]


def test_checkpoint_document_contains_required_history_and_decisions():
    text = read(DOC)
    markers = (
        "UI/UX Blocked & Forbidden Screen Checkpoint 1.94",
        "5597377",
        "23f9185",
        "72affc4",
        "be485cb",
        "87e2abb",
        "3f28780",
        "1.89",
        "1.90",
        "1.91",
        "1.92",
        "1.93",
        "1.94",
        "NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED",
        "BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "BLOCKED_FORBIDDEN_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "HUMAN_VISUAL_REVIEW_APPROVED",
        "Auditoría anti-CTA/anti-affordance",
        "READ_ONLY_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "Ver raw-safe read-only",
        "Ver detalle",
        "Releer payload local",
        "Bloqueado por contrato",
        "Request Contract Preview",
        "No submit",
        "No dispatch",
        "No execution",
        "Inspeccionar resumen contractual",
        "Blocked & Forbidden Capabilities Screen",
        "FSC-BF-02",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "documental",
        "read-only",
        "blocked_capabilities",
        "forbidden_actions",
        "no unlock",
        "no override",
        "no bypass",
        "snapshot",
        "no log vivo",
        "no fake success",
        "no ghost actions",
        "no User Panel",
        "no endpoint",
        "no fetch",
        "no rutas/hash",
        "IA_CORE",
        "SAAOP",
        "node",
        "git diff --check",
        "backend contract tests",
        "backup readiness",
        NEXT_PROMPT,
        "no se implementó pantalla adicional",
        "no se modificó Contract Overview",
        "no se tocó backend operativo",
        "no se limpió deuda residual",
        "no se corrigió pyflakes",
        "No avanzar a Validation & Readiness",
    )
    assert all(marker in text for marker in markers)
    assert "Loteria" in text or "Lotería" in text


def test_checkpoint_document_selects_exactly_one_affordance_decision():
    text = read(DOC)
    decision_block = text.split("## Base y objetivo", 1)[0]
    assert "READ_ONLY_AFFORDANCE_AUDIT_PASSED_WITH_NOTES" in decision_block
    assert "READ_ONLY_AFFORDANCE_AUDIT_PASSED`" not in decision_block.replace(
        "READ_ONLY_AFFORDANCE_AUDIT_PASSED_WITH_NOTES", ""
    )
    assert "READ_ONLY_AFFORDANCE_AUDIT_BLOCKED_NEEDS_MINOR_FIX" not in decision_block
    assert "READ_ONLY_AFFORDANCE_AUDIT_BLOCKED_CRITICAL" not in decision_block


def test_blocked_forbidden_surface_has_no_affordance_or_operational_markup():
    section = blocked_forbidden_section()
    assert 'data-contract-screen="FSC-BF-02"' in section
    assert 'data-contract-authority="backend_internal_ui_payload.v1"' in section
    assert 'data-interaction-mode="read-only"' in section
    assert 'data-visibility="always-visible"' in section
    assert "blocked_capabilities" in section
    assert "forbidden_actions" in section
    assert "no-unlock/no-bypass/no-override" in section
    assert "no-runtime" in section
    assert "no-execution" in section
    assert "no-endpoint" in section
    assert "no-user-panel" in section
    assert not re.search(r"<(button|a|form|input|select|textarea|details|summary)\b", section, re.I)
    assert "href=" not in section
    assert "fetch(" not in section
    assert "data-route" not in section
    assert "data-hash" not in section
    assert "Loteria" not in section
    assert "Lotería" not in section
    assert "SAAOP" not in section


def test_checkpoint_preserves_contract_overview_and_expected_files():
    html = read(INDEX)
    assert html.count('id="contract-overview-screen"') == 1
    assert html.count('id="blocked-forbidden-screen"') == 1
    assert html.index('id="contract-overview-screen"') < html.index('id="blocked-forbidden-screen"')
    for relative in (
        "docs/UI_UX_BLOCKED_FORBIDDEN_SCREEN_HARDENING_1_93.md",
        "docs/UI_UX_BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTATION_1_92.md",
        "tests/test_ui_ux_blocked_forbidden_screen_hardening_1_93.py",
        "tests/test_ui_ux_blocked_forbidden_screen_implementation_1_92.py",
        "README.md",
        "ui/web/README.md",
    ):
        assert (ROOT / relative).exists(), relative
