from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTATION_1_92.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.93 - Hardening visual y contractual Blocked & Forbidden "
    "Capabilities Screen IA_CORE contract-aware sin runtime/no-execution"
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


def test_blocked_forbidden_screen_exists_after_contract_overview():
    html = read(INDEX)
    assert html.count('id="contract-overview-screen"') == 1
    assert html.count('id="blocked-forbidden-screen"') == 1
    assert html.index('id="contract-overview-screen"') < html.index('id="blocked-forbidden-screen"')
    assert html.index('id="blocked-forbidden-screen"') < html.index('class="density-priority-strip"')


def test_screen_declares_contract_identity_and_sources():
    section = blocked_forbidden_section()
    markers = (
        "Blocked &amp; Forbidden Capabilities Screen",
        "FSC-BF-02",
        'data-main-console-zone="blocked-forbidden"',
        'data-contract-screen="FSC-BF-02"',
        'data-interaction-mode="read-only"',
        'data-interaction-state="read_only inspectable"',
        "Panel Maestro",
        "backend_internal_ui_payload.v1",
        "blocked_capabilities",
        "forbidden_actions",
    )
    assert all(marker in section for marker in markers)


def test_screen_keeps_blocked_and_forbidden_visible_without_operational_controls():
    section = blocked_forbidden_section()
    assert 'data-blocked-forbidden-block="blocked-capabilities"' in section
    assert 'data-blocked-forbidden-block="forbidden-actions"' in section
    assert "no-unlock/no-bypass/no-override" in section
    assert "no error operativo" in section
    assert "Deny-by-default" in section
    assert "nunca controles" in section
    forbidden_markup = ("<button", "<form", "<input", "<select", "<textarea", "href=")
    assert all(marker not in section.lower() for marker in forbidden_markup)


def test_screen_has_no_runtime_endpoint_fetch_route_or_user_panel_surface():
    section = blocked_forbidden_section()
    assert "fetch(" not in section
    assert "window.location" not in section
    assert "location.hash" not in section
    assert "#blocked" not in section
    assert "#/" not in section
    assert "api/" not in section.lower()
    assert "data-route" not in section
    assert "data-hash" not in section
    required_markers = (
        "no-runtime",
        "no-execution",
        "no-endpoint",
        "no-user-panel",
        "No User Panel",
        "no rutas/hash",
        "no fetch",
    )
    assert all(marker in section for marker in required_markers)


def test_screen_does_not_present_success_unlock_override_or_bypass_copy():
    section = blocked_forbidden_section()
    prohibited_copy = (
        "Ready to run",
        "Endpoint connected",
        "Worker active",
        "Queue active",
        "User Panel activo",
        "Resolver ahora",
        "Auto-fix",
        "Desbloquear",
        "Override available",
        "Bypass available",
        "Permission granted",
        "Success",
        "Completed",
        "Final output ready",
    )
    assert all(copy not in section for copy in prohibited_copy)
    assert not re.search(r"\b(run|execute|dispatch|submit|launch)\b", section, flags=re.IGNORECASE)


def test_documentation_records_implementation_and_boundaries():
    text = read(DOC)
    markers = (
        "# UI/UX Blocked & Forbidden Screen Implementation 1.92",
        "BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "87e2abb",
        "23f9185",
        "main` ahead de `origin/main` por 3 commits",
        "Blocked & Forbidden Capabilities Screen",
        "FSC-BF-02",
        "Panel Maestro",
        "backend_internal_ui_payload.v1",
        "blocked_capabilities",
        "forbidden_actions",
        "Contract Overview no fue reescrito ni reemplazado",
        "No unlock",
        "No override",
        "No bypass",
        "No User Panel",
        "No rutas/hash",
        "No endpoint",
        "No fetch",
        "No runtime",
        "No execution",
        "No dispatch",
        "Push queda pospuesto",
        NEXT_PROMPT,
    )
    assert all(marker in text for marker in markers)


def test_readmes_point_to_implementation_and_next_prompt():
    for path in (README, WEB_README):
        text = read(path)
        assert "Implementacion Blocked & Forbidden Capabilities Screen 1.92" in text
        assert "UI_UX_BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTATION_1_92.md" in text
        assert "BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTED_NEEDS_HARDENING" in text
        assert "blocked_capabilities" in text
        assert "forbidden_actions" in text
        assert "no User Panel" in text or "No User Panel" in text
        assert "no-runtime/no-execution" in text
        assert "push pospuesto" in text.lower()
        assert NEXT_PROMPT in text