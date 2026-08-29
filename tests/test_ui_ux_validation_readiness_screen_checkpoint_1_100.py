from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ui" / "web" / "index.html"
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_SCREEN_CHECKPOINT_1_100.md"
TEST = ROOT / "tests" / "test_ui_ux_validation_readiness_screen_checkpoint_1_100.py"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validation_readiness_section(text: str) -> str:
    start = text.index('<section class="validation-readiness-screen')
    end = text.index("</section>", start) + len("</section>")
    return text[start:end]


def test_checkpoint_artifacts_exist():
    assert DOC.exists()
    assert TEST.exists()


def test_checkpoint_document_contains_history_and_decisions():
    text = read(DOC)
    required = (
        "UI/UX Validation & Readiness Screen Checkpoint 1.100",
        "40d5f12",
        "7ad9a8b",
        "4299b0b",
        "c5518a4",
        "9a3dfd6",
        "d89da91",
        "NEXT_SCREEN_VALIDATION_READINESS_SELECTED",
        "VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "VALIDATION_READINESS_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "VALIDATION_READINESS_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "VALIDATION_READINESS_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "HUMAN_VISUAL_REVIEW_APPROVED",
        "VALIDATION_READINESS_FINAL_AFFORDANCE_AUDIT_PASSED_WITH_NOTES",
        "Auditoría final anti-CTA/anti-affordance",
        "Validation & Readiness Screen",
        "FSC-VR-03",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "documental",
        "read-only",
        "contract-aware",
    )
    assert all(marker in text for marker in required)


def test_checkpoint_document_contains_semantics_and_guardrails():
    text = read(DOC)
    required = (
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
        "blockers",
        "warnings",
        "missing requirements",
        "snapshot",
        "no live log",
        "no raw Package",
        "no runtime",
        "no execution",
        "no dispatch",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no unlock",
        "no override",
        "no bypass",
        "no fake success",
        "no ghost actions",
        "Contract Overview",
        "FSC-CO-01",
        "Blocked & Forbidden",
        "FSC-BF-02",
        "Request Contract Preview",
        "diferido",
        "IA_CORE",
        "Loter",
        "SAAOP",
        "Node checks",
        "git diff --check",
        "Backend contract tests",
        "Backup readiness",
    )
    assert all(marker in text for marker in required)


def test_checkpoint_document_contains_limits_and_next_prompt():
    text = read(DOC)
    lower = text.lower()
    required = (
        "no se implement",
        "pantalla adicional",
        "no se modific",
        "ui activa",
        "no se toc",
        "backend operativo",
        "no se limpi",
        "se corrigieron pyflakes",
        "no se avanzó a un bloque funcional adicional",
        "prompt ui/ux 1.101 - planificar siguiente paso tras validation & readiness screen ia_core contract-aware sin runtime/no-execution",
    )
    assert all(marker in lower for marker in required)


def test_final_affordance_audit_table_covers_all_visual_elements():
    text = read(DOC)
    elements = (
        "Header",
        "Status strip documental",
        "Readiness vs Permission",
        "Validation vs Execution",
        "Validation Findings",
        "Blockers/warnings/missing requirements",
        "Evidence Snapshot",
        "No-runtime boundary",
        "Baseline References",
        "Anti-affordance Notice",
        "Chips/labels/pills visibles",
        "READ_ONLY_LABEL",
        "DOCUMENTATION_REFERENCE",
        "NON_OPERATIONAL_STATUS",
    )
    assert all(element in text for element in elements)


def test_validation_readiness_final_surface_is_preserved():
    text = read(INDEX)
    section = validation_readiness_section(text)
    required = (
        "Validation &amp; Readiness Screen",
        "FSC-VR-03",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "read-only",
        "contract-aware",
        "readiness no permission",
        "validation no execution",
        "passed no operational success",
        "warning/error no live runtime",
        "review required no workflow active",
        "blockers",
        "warnings",
        "missing_requirements",
        "snapshot",
        "no log vivo",
        "raw Package",
        "no-runtime",
        "no-execution",
        "no-dispatch",
        "no-endpoint",
        "no-user-panel",
        "Contract Overview",
        "Blocked &amp; Forbidden",
        "Request Contract Preview",
    )
    assert all(marker in section for marker in required)
    assert "Loter" not in section
    assert "SAAOP" not in section


def test_previous_and_current_screens_keep_order_and_no_operational_markup():
    text = read(INDEX)
    assert text.index('id="contract-overview-screen"') < text.index('id="blocked-forbidden-screen"') < text.index('id="validation-readiness-screen"')
    section = validation_readiness_section(text)
    prohibited = (
        "<button",
        "<a ",
        "<form",
        "<input",
        "<select",
        "<textarea",
        "href=",
        "fetch(",
        "window.location.hash",
        "data-action=\"run\"",
        "data-action=\"dispatch\"",
        "data-action=\"submit\"",
        "data-action=\"execute\"",
        "data-action=\"retry\"",
        "data-action=\"unlock\"",
        "data-action=\"override\"",
        "data-action=\"bypass\"",
    )
    assert all(marker not in section for marker in prohibited)
    assert text.count('data-contract-screen="FSC-CO-01"') == 1
    assert text.count('data-contract-screen="FSC-BF-02"') == 1
    assert text.count('data-contract-screen="FSC-VR-03"') == 1


def test_checkpoint_document_records_verified_files_and_push_rule():
    text = read(DOC)
    for path in (
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/i18n_es.json",
        "Documentos, tests y README",
        "Backend no tocado",
        "push normal",
        "origin/main",
    ):
        assert path in text


def test_readmes_record_checkpoint_and_next_cursor():
    for path in (README, WEB_README):
        text = read(path)
        assert "Checkpoint Validation & Readiness Screen 1.100" in text
        assert "VALIDATION_READINESS_SCREEN_CHECKPOINT_CLOSED_AND_PUBLISHED" in text
        assert "HUMAN_VISUAL_REVIEW_APPROVED" in text
        assert "VALIDATION_READINESS_FINAL_AFFORDANCE_AUDIT_PASSED_WITH_NOTES" in text
        assert "PROMPT UI/UX 1.101 - Planificar siguiente paso tras Validation & Readiness Screen" in text
        assert "no se implement" in text.lower()
