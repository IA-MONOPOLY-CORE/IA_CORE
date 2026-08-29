from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_1_91.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

ALLOWED_DECISIONS = (
    "BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_READY",
    "BLOCKED_FORBIDDEN_NEEDS_IMPLEMENTATION_PREFLIGHT",
    "BLOCKED_FORBIDDEN_NEEDS_MORE_PLANNING",
    "BLOCKED_FORBIDDEN_IMPLEMENTATION_DEFERRED",
)

NEXT_PROMPT = (
    "PROMPT UI/UX 1.92 - Implementar Blocked & Forbidden Capabilities Screen "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    assert path.exists(), f"Missing required file: {path}"
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    text = read(DOC)
    markers = (
        "# UI/UX Blocked & Forbidden Controlled Implementation Plan 1.91",
        "be485cb",
        "23f9185",
        "BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED",
        "Blocked & Forbidden Capabilities Screen",
        "Contract Overview",
        "baseline",
        "main` ahead de `origin/main` por 2 commits",
        "Push: pospuesto",
    )
    assert all(marker in text for marker in markers)


def test_plan_contains_required_sections_and_contract_markers():
    text = read(DOC)
    markers = (
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "blocked_capabilities",
        "forbidden_actions",
        "## Alcance implementable futuro",
        "## Alcance prohibido futuro",
        "## Candidate future implementation files",
        "## Prohibited files",
        "## Future placement strategy",
        "## Future visual structure",
        "## Data policy",
        "## State policy",
        "## Copy policy",
        "## Controlled implementation strategy",
        "## Future tests required",
        "## Entry criteria",
        "## Exit criteria",
        "## Rollback strategy",
        "## Risk register",
    )
    assert all(marker in text for marker in markers)


def test_plan_defines_candidate_and_prohibited_files():
    text = read(DOC)
    candidate_markers = (
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/i18n_es.json",
        "tests/",
    )
    prohibited_markers = (
        "api.py",
        "core/",
        "domains/",
        "providers/",
        "tools/",
        "scripts/",
        ".github/workflows",
        ".env",
        "dependencias",
    )
    assert all(marker in text for marker in candidate_markers)
    assert all(marker in text for marker in prohibited_markers)


def test_plan_records_single_allowed_decision_and_next_prompt():
    text = read(DOC)
    decisions = [decision for decision in ALLOWED_DECISIONS if decision in text]
    assert decisions == ["BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_READY"]
    assert NEXT_PROMPT in text
    assert "solo si el operador humano lo aprueba" in text
    assert "checkpoint con push vendria en 1.94" in text


def test_plan_preserves_no_scope_boundaries():
    text = read(DOC)
    markers = (
        "no runtime",
        "no execution",
        "no endpoint",
        "no fetch",
        "no User Panel",
        "no rutas/hash",
        "no backend",
        "no CI",
        "no deuda residual",
        "no pyflakes",
        "No se implemento pantalla",
        "No se modifico UI activa",
        "No se toco Contract Overview",
        "No se avanzo a 1.92",
    )
    assert all(marker in text for marker in markers)


def test_plan_lists_future_tests_and_risks():
    text = read(DOC)
    future_test_markers = (
        "No unlock/override/bypass",
        "No botones operativos",
        "No endpoint/fetch nuevo",
        "No raw package",
        "No fake success",
        "No ghost actions",
        "No hidden blockers",
        "Contract Overview sigue presente",
        "git diff --check",
    )
    risk_markers = (
        "Duplicacion con Contract Overview",
        "Visual de error/alarma excesiva",
        "Blockers percibidos como falla",
        "forbidden_actions` convertidos en CTA negativo",
        "Unlock sugerido",
        "Override/bypass sugerido",
        "Ocultar blockers",
        "Raw package leakage",
        "Exposicion de secretos",
        "Fetch/endpoint accidental",
        "Backend accidental",
        "Rutas/hash accidentales",
        "Mezcla con Validation & Readiness",
        "Fake success",
        "Ghost actions",
        "Saltar revision visual",
        "Push antes de checkpoint",
    )
    assert all(marker in text for marker in future_test_markers)
    assert all(marker in text for marker in risk_markers)


def test_readmes_point_to_plan_and_next_prompt():
    for path in (README, WEB_README):
        text = read(path)
        assert "Plan implementacion controlada Blocked & Forbidden 1.91" in text
        assert "UI_UX_BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_1_91.md" in text
        assert "BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_READY" in text
        assert NEXT_PROMPT in text
        assert "no implementa pantalla" in text
        assert "push pospuesto" in text.lower()
