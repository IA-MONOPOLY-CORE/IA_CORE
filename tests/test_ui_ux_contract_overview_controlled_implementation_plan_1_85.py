from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_CONTROLLED_IMPLEMENTATION_PLAN_1_85.md"
DECISION = "CONTRACT_OVERVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY"
NEXT_PROMPT = (
    "PROMPT UI/UX 1.86 - Implementar Contract Overview Screen "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read_doc():
    return DOC.read_text(encoding="utf-8")


def test_controlled_plan_contains_required_contract_and_plan_sections():
    text = read_doc()
    markers = (
        "UI/UX Contract Overview Controlled Implementation Plan 1.85",
        "d20a5d1",
        "UI_UX_CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_CHECKPOINT_1_84",
        "CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "FSC-CO-01",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "vista documental",
        "solo lectura",
        "Alcance implementable futuro",
        "Alcance prohibido futuro",
        "Candidate future implementation files",
        "Prohibited files",
        "Future visual structure",
        "Future states",
        "Copy policy",
        "Future tests required",
        "Controlled implementation strategy",
        "Entry criteria",
        "Exit criteria",
        "Rollback strategy",
        "Future prompt sequence",
        "Risk register",
        DECISION,
        NEXT_PROMPT,
    )
    assert DOC.exists()
    normalized = text.lower()
    assert all(marker.lower() in normalized for marker in markers)


def test_controlled_plan_preserves_non_implementation_boundaries():
    text = read_doc().lower()
    markers = (
        "no se implemento pantalla",
        "no se modifico ui activa",
        "no se creo componente nuevo",
        "no se creo user panel",
        "no se crearon rutas/hash",
        "no se crearon endpoints",
        "no se crearon fetches",
        "no se activo runtime",
        "no se activo execution",
        "no se activo dispatch",
        "no se toco backend operativo",
        "no se limpio deuda residual",
        "no se corrigieron pyflakes",
        "no se hizo push",
        "ready-no-permission",
        "allowed_actions",
        "no son botones de ejecucion",
        "blocked_capabilities",
        "forbidden_actions",
        "snapshot documental",
        "no log vivo",
        "empty state honesto",
        "loteria",
        "saaop",
    )
    assert all(marker in text for marker in markers)


def test_controlled_plan_defines_future_files_states_copy_tests_and_rollback():
    text = read_doc().lower()
    markers = (
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/i18n_es.json",
        "api.py",
        "core/",
        "domains/",
        "providers/",
        "scripts/",
        "tools/",
        "no fetch",
        "no endpoint",
        "no runtime words",
        "no user panel",
        "no prohibited ctas",
        "dom test",
        "node --check",
        "git diff --check",
        "por commit",
        "1.86",
        "1.87",
        "1.88",
    )
    assert all(marker in text for marker in markers)
