from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md"
DOCS = {
    "0.6": ROOT / "docs" / "UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md",
    "0.7": ROOT / "docs" / "UI_UX_VISUAL_ARCHITECTURE_0_7.md",
    "0.8": ROOT / "docs" / "UI_UX_SUPERIOR_LAYOUT_0_8.md",
    "0.9": ROOT / "docs" / "UI_UX_VISUAL_BASE_CHECKPOINT_0_9.md",
    "1.0": ROOT / "docs" / "UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md",
    "1.1": ROOT / "docs" / "UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md",
    "1.2": ROOT / "docs" / "UI_UX_MAIN_CONSOLE_FLOW_1_2.md",
    "1.3": ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_1_3.md",
    "1.4": ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md",
    "1.5": ROOT / "docs" / "UI_UX_NEXT_CONSOLE_BLOCK_PLAN_1_5.md",
    "1.6": ROOT / "docs" / "UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md",
    "1.7": ROOT / "docs" / "UI_UX_CONTRACT_DETAIL_PANELS_1_7.md",
    "1.8": ROOT / "docs" / "UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md",
    "1.9": ROOT / "docs" / "UI_UX_COMPONENT_SYSTEM_1_9.md",
}
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "ui" / "web" / "README.md"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


COMPONENTS = (
    "ia-panel",
    "ia-detail-panel",
    "ia-status-badge",
    "ia-chip",
    "ia-empty-state",
    "ia-warning",
    "ia-error",
    "ia-blocker",
    "ia-evidence",
    "ia-nav-button",
    "ia-readonly-control",
)

NAV_ZONES = (
    "readiness",
    "contract-core",
    "payload-reading",
    "detail-panels",
    "actions-boundaries",
    "evidence",
    "next-step",
)

DETAIL_PANELS = (
    "readiness",
    "payload-contract",
    "validation",
    "actions",
    "blocked-capabilities",
    "warnings-errors",
    "evidence",
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, WIDGETS, INTERACTIONS, ADMIN, I18N, STYLES)
    )


def test_checkpoint_document_exists_and_declares_required_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_PASSED",
        "PAYLOAD_CONTRACT_READING_MODEL_PRESERVED",
        "CONTRACT_DETAIL_PANELS_PRESERVED",
        "INTERNAL_NAVIGATION_PRESERVED",
        "IA_CORE_COMPONENT_SYSTEM_PRESERVED",
        "SECOND_CONSOLE_BLOCK_CONTRACT_AWARE_CONFIRMED",
        "SECOND_CONSOLE_BLOCK_READ_ONLY_BOUNDARIES_CONFIRMED",
        "SECOND_CONSOLE_BLOCK_NO_PERMISSION_INFERENCE_CONFIRMED",
        "SECOND_CONSOLE_BLOCK_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_NEXT_UI_UX_BLOCK",
    ):
        assert verdict in text

    for commit in ("85b0cbd5", "1b04f7a8", "512a3391", "371d77ea"):
        assert commit in text


def test_checkpoint_references_required_documental_base():
    text = _read(DOC)

    for label, path in DOCS.items():
        assert path.exists(), label

    for token in (
        "0.6",
        "0.7",
        "0.8",
        "0.9",
        "1.0 -> 1.3",
        "1.4",
        "1.5",
        "1.6 -> 1.9",
    ):
        assert token in text

    for section in ("Que Dejo 1.6", "Que Dejo 1.7", "Que Dejo 1.8", "Que Dejo 1.9"):
        assert section in text


def test_active_ui_preserves_1_6_1_7_1_8_and_1_9_markers():
    html = _read(INDEX)

    assert 'data-payload-reading-model="contract-aware-1.6"' in html
    assert 'data-contract-detail-panels="contract-aware-1.7"' in html
    assert 'data-internal-navigation="contract-aware-1.8"' in html
    assert 'data-component-system="ia-core-contract-aware-1.9"' in html

    assert html.count('data-reading-layer="') == 3
    for layer in ("summary", "detail", "raw-safe"):
        assert f'data-reading-layer="{layer}"' in html

    assert html.count('<article class="contract-detail-panel" data-detail-panel="') == 7
    for panel in DETAIL_PANELS:
        assert f'data-detail-panel="{panel}"' in html

    assert html.count('data-nav-target="') == 7
    assert html.count('data-nav-section="') == 7
    for zone in NAV_ZONES:
        assert f'data-nav-target="{zone}"' in html
        assert f'data-nav-section="{zone}"' in html


def test_component_system_vocabulary_is_preserved_without_new_dependencies():
    doc = _read(DOC)
    implementation = _read(INDEX) + _read(WIDGETS)

    for component in COMPONENTS:
        assert component in doc
        assert component in implementation

    assert not (ROOT / "package.json").exists()
    assert not (ROOT / "package-lock.json").exists()
    for dependency in ("tailwindcss", "react-dom", "framer-motion", "@motion"):
        assert dependency not in implementation.lower()


def test_payload_contract_reading_remains_summary_detail_raw_safe_and_read_only():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    raw_section = html.split('data-reading-layer="raw-safe"', 1)[1].split("</article>", 1)[0]
    assert 'data-interaction-mode="read-only"' in raw_section
    assert "<button" not in raw_section
    assert "<form" not in raw_section.lower()
    assert "<textarea" not in raw_section.lower()
    assert 'type="submit"' not in raw_section.lower()
    assert "safeRawProjection" in widgets
    assert "contract-raw-safe-value" in widgets

    for phrase in ("no edita", "no envia", "no ejecuta", "no muestra secretos"):
        assert phrase in doc


def test_detail_panels_and_navigation_remain_read_only_and_local():
    html = _read(INDEX)
    interactions = _read(INTERACTIONS)
    doc = _read(DOC)

    assert html.count('data-detail-state="read_only"') == 7
    assert html.count('class="internal-nav-control" type="button"') == 7
    assert 'aria-current="true"' in html
    assert 'href="#' not in html

    for forbidden_write in (
        "fetch(",
        "localStorage",
        "sessionStorage",
        "indexedDB",
        "location.hash",
        "history.pushState",
        "history.replaceState",
    ):
        assert forbidden_write not in interactions

    normalized_doc = " ".join(doc.split())
    for phrase in ("hash routing", "no crea router", "no crea rutas", "no agrega fetch"):
        assert phrase in normalized_doc


def test_permissions_actions_and_blockers_remain_backend_authority():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    doc = _read(DOC)

    for token in ("allowed_actions", "forbidden_actions", "blocked_capabilities"):
        assert token in html
        assert token in widgets
        assert token in doc

    assert 'id="contract-forbidden-actions"' in html
    assert 'id="contract-blocked-list"' in html
    assert "true = blocked" in html
    assert "no se infiere" in doc
    assert "no ejecutable" in doc


def test_no_new_endpoints_routes_runtime_execution_or_controlled_execution():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    interactions = _read(INTERACTIONS)
    admin = _read(ADMIN)
    doc = _read(DOC)

    for route in ("/api/debate/start", "/api/dispatch", "/api/runtime", "/api/execution"):
        assert route not in html
        assert route not in widgets
        assert route not in interactions
        assert route not in admin

    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "controlled execution" in doc
    assert "dispatch real" in doc

    for invalid_label in (
        ">active<",
        ">running<",
        ">executing<",
        ">live<",
        ">operational<",
        ">dispatching<",
        ">submitted<",
        ">processing<",
    ):
        assert invalid_label not in _active_ui()


def test_ia_core_identity_active_and_legacy_not_visible_as_active_ui():
    active_ui = _active_ui()

    assert '<h1 id="brand-title">IA_CORE</h1>' in _read(INDEX)
    for legacy in (
        "SAAOP",
        "S.A.A.O.P.",
        "Loteria",
        "Loteria",
        "lottery",
        "Tactical HUD",
        "TACTICAL HUD",
        "U-Score",
        "CAZADOR",
        "ESPEJO",
        "combinatoria",
    ):
        assert legacy not in active_ui


def test_responsive_accessibility_and_external_reference_boundaries_are_recorded():
    html = _read(INDEX)
    doc = _read(DOC)

    assert "1440 x 1000" in doc
    assert "390 x 844" in doc
    assert "sin overflow horizontal" in doc
    assert "foco visible" in doc
    ids = [value for value in re.findall(r'id="([^"]+)"', html) if "$" not in value]
    assert len(ids) == len(set(ids))

    for reference in ("21st.dev", "UI UX Pro Max Skill", "Framer Motion / Motion"):
        assert reference in doc
    assert "benchmarks futuros" in doc
    assert "No se instalan" in doc


def test_readme_records_1_10_checkpoint_without_advancing_next_block():
    normalized = " ".join(_read(README).split())

    assert "Checkpoint segundo bloque de consola 1.10" in normalized
    assert "1.6 -> 1.9" in normalized
    assert "UI_READY_FOR_NEXT_UI_UX_BLOCK" in normalized
    assert "no runtime" in normalized
    assert "1.11" in normalized
    assert "no implementa el siguiente bloque" in normalized
