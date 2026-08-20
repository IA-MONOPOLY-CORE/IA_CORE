from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_11.md"
CHECKPOINT_110 = ROOT / "docs" / "UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md"
README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


OPTIONS = (
    "Responsive / Accessibility Hardening",
    "Secondary Console Views / Detail Screens",
    "Visual Polish / Premium IA_CORE Layer",
    "Operator Guidance / Empty-State Intelligence",
    "Admin Boundary / Exposure Review",
    "Component Documentation / Style Reference",
    "Future Benchmark Review",
    "Panel Master vs User Panel Separation",
)


def _read(path):
    return path.read_text(encoding="utf-8")


def _active_ui():
    return "\n".join(
        _read(path)
        for path in (INDEX, README, WIDGETS, INTERACTIONS, ADMIN, I18N, STYLES)
    )


def test_document_exists_and_declares_expected_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_NEXT_BLOCK_PLAN_DEFINED",
        "POST_1_10_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ):
        assert verdict in text

    assert "6b8894a6" in text
    assert CHECKPOINT_110.exists()
    assert "UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_PASSED" in _read(CHECKPOINT_110)


def test_document_references_post_1_10_state_and_contractual_base():
    text = _read(DOC)

    for token in (
        "checkpoint `1.10`",
        "1.6 -> 1.9",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "read-only",
    ):
        assert token in text

    for heading in (
        "Fortalezas",
        "Deudas Visibles",
        "Deudas UX",
        "Deudas Responsive Y Accesibilidad",
        "Riesgos De Crecimiento",
    ):
        assert heading in text


def test_all_candidate_options_are_evaluated():
    text = _read(DOC)

    for option in OPTIONS:
        assert option in text

    for criterion in (
        "Valor",
        "Riesgo",
        "Costo",
        "Dependencia con bloques previos",
        "UI nueva",
        "Endpoints",
        "Confusion operativa",
        "Lectura",
    ):
        assert criterion in text


def test_decision_matrix_and_selected_option_are_present():
    text = _read(DOC)

    assert "Matriz De Decision" in text
    assert "Reduce riesgo ahora" in text
    assert "Responsive / Accessibility Hardening | Alto" in text
    assert "La opcion seleccionada es:" in text
    assert "`Responsive / Accessibility Hardening`" in text
    assert "Por Que Ahora" in text
    assert "Por Que No Las Otras Primero" in text
    assert "Riesgos Que Reduce" in text
    assert "Que Habilita Despues" in text


def test_postponed_options_and_sequence_are_recorded():
    text = _read(DOC)

    for token in (
        "Pantallas secundarias",
        "Polish premium",
        "Benchmarks externos",
        "Panel Maestro vs Panel Usuario",
        "Documentacion extendida de componentes",
        "Operator Guidance / Empty-State Intelligence",
        "Admin Boundary / Exposure Review",
    ):
        assert token in text

    for prompt in (
        "1.12 - Auditar responsive/accesibilidad",
        "1.13 - Endurecer responsive",
        "1.14 - Checkpoint responsive/accesibilidad",
    ):
        assert prompt in text


def test_next_exact_prompt_is_declared_without_implementing_it():
    text = _read(DOC)
    readme = _read(README)

    next_prompt = (
        "PROMPT UI/UX 1.12 - Auditar responsive/accesibilidad de consola "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    assert next_prompt in text
    assert next_prompt in readme
    assert "1.11 no implementa el bloque elegido" in readme


def test_plan_does_not_recommend_runtime_execution_endpoints_or_dependencies():
    text = _read(DOC)
    normalized = " ".join(text.split())

    for phrase in (
        "no endpoint publico",
        "no hash routing operativo",
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
        "no assets externos",
        "no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones",
    ):
        assert phrase in normalized

    assert "no instalar dependencias" in text
    assert "no crear endpoints/fetches" in text
    assert "no activar runtime/execution/dispatch/controlled execution" in text


def test_external_references_remain_future_benchmarks_only():
    text = _read(DOC)
    readme = _read(README)

    for reference in ("21st.dev", "UI UX Pro Max Skill", "Framer Motion / Motion"):
        assert reference in text
        assert reference in readme

    assert "benchmarks futuros solamente" in text
    assert "No se instalan" in text
    for dependency in ("tailwindcss", "react-dom", "framer-motion", "@motion"):
        assert dependency not in (_read(INDEX) + _read(WIDGETS) + _read(INTERACTIONS)).lower()


def test_identity_and_legacy_boundaries_are_preserved():
    text = _read(DOC)
    active_ui = _active_ui()

    assert "IA_CORE como identidad visual activa" in text
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


def test_readme_records_1_11_plan_and_selected_next_block():
    normalized = " ".join(_read(README).split())

    assert "Planificacion siguiente bloque UI/UX 1.11" in normalized
    assert "Responsive / Accessibility Hardening" in normalized
    assert "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK" in normalized
    assert "no runtime" in normalized
    assert "no execution" in normalized
    assert "no implementa el bloque elegido" in normalized
