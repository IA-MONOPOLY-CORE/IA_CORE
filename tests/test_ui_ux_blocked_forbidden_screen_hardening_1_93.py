from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_SCREEN_HARDENING_1_93.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.94 - Checkpoint Blocked & Forbidden Capabilities Screen "
    "implementada y hardenizada IA_CORE contract-aware sin runtime/no-execution"
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


def article(section: str, block_name: str) -> str:
    start = section.index(f'data-blocked-forbidden-block="{block_name}"')
    article_start = section.rfind("<article", 0, start)
    article_end = section.index("</article>", start) + len("</article>")
    return section[article_start:article_end]


def test_hardened_screen_is_identified_and_always_visible():
    section = blocked_forbidden_section()
    markers = (
        'data-screen-role="contract-limits"',
        'data-visibility="always-visible"',
        'data-contract-screen="FSC-BF-02"',
        'data-contract-authority="backend_internal_ui_payload.v1"',
        'data-rendering-policy="documentary-only"',
        'data-blocked-forbidden-visibility="always-visible"',
        'data-state-severity="contractual"',
        "Panel Maestro / Contract limits / Read-only",
    )
    assert all(marker in section for marker in markers)
    assert section.count('data-visibility="always-visible"') >= 3


def test_primary_contract_fields_have_visual_priority_without_controls():
    section = blocked_forbidden_section()
    blocked = article(section, "blocked-capabilities")
    forbidden = article(section, "forbidden-actions")
    for item, field in ((blocked, "blocked_capabilities"), (forbidden, "forbidden_actions")):
        assert "blocked-forbidden-block--primary" in item
        assert 'data-visibility="always-visible"' in item
        assert f'data-contract-field="{field}"' in item
        assert not re.search(r"<(button|a|form|input|select|textarea)\b", item, re.I)
        assert "role=\"button\"" not in item


def test_hardening_preserves_contract_boundaries_and_honest_states():
    section = blocked_forbidden_section()
    required = (
        "FSC-BF-02",
        "backend_internal_ui_payload.v1",
        "blocked_capabilities",
        "forbidden_actions",
        "no-unlock/no-bypass/no-override",
        "documented / blocked / forbidden / deferred",
        "1.68 / 1.69 / 1.70 / 1.90 / 1.91 / 1.92",
        "No User Panel",
        "no rutas/hash",
        "no endpoint",
        "no fetch",
        "no runtime",
        "no execution",
        "no despacha jobs",
        "log vivo",
    )
    assert all(marker in section for marker in required)
    assert "Contract Overview intacto" in section
    assert "FSC-CO-01 baseline" in section
    assert "forbidden_actions" in article(section, "forbidden-actions")
    assert "blocked_capabilities" in article(section, "blocked-capabilities")


def test_hardening_surface_has_no_operational_or_navigation_surface():
    section = blocked_forbidden_section()
    forbidden_markup = ("fetch(", "window.location", "location.hash", "data-route", "data-hash", "href=", "api/")
    assert all(marker.lower() not in section.lower() for marker in forbidden_markup)
    assert not re.search(r"\b(run|execute|dispatch|submit|launch)\b", section, flags=re.I)
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
    assert "Loteria" not in section
    assert "SAAOP" not in section


def test_contract_overview_remains_the_prior_baseline_screen():
    html = read(INDEX)
    assert html.count('id="contract-overview-screen"') == 1
    assert html.count('id="blocked-forbidden-screen"') == 1
    assert html.index('id="contract-overview-screen"') < html.index('id="blocked-forbidden-screen"')


def test_documentation_and_readmes_record_hardening_scope():
    doc = read(DOC)
    doc_markers = (
        "# UI/UX Blocked & Forbidden Screen Hardening 1.93",
        "BLOCKED_FORBIDDEN_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "3f28780",
        "23f9185",
        "`main` inicial: ahead de `origin/main` por 4 commits",
        "UI_UX_BLOCKED_FORBIDDEN_SCREEN_IMPLEMENTATION_1_92.md",
        "Contract Overview",
        "FSC-BF-02",
        "blocked_capabilities",
        "forbidden_actions",
        "always-visible",
        "No CTA operativo",
        "No endpoint",
        "No fetch",
        "No runtime",
        "No execution",
        "Push queda pospuesto",
        NEXT_PROMPT,
    )
    assert all(marker in doc for marker in doc_markers)
    for path in (README, WEB_README):
        text = read(path)
        assert "Hardening Blocked & Forbidden Capabilities Screen 1.93" in text
        assert "UI_UX_BLOCKED_FORBIDDEN_SCREEN_HARDENING_1_93.md" in text
        assert "BLOCKED_FORBIDDEN_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW" in text
        assert NEXT_PROMPT in text
