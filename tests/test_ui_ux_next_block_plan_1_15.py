from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_15.md"
CHECKPOINT_114 = ROOT / "docs" / "UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md"
README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"
STYLES = ROOT / "ui" / "web" / "styles.css"


OPTIONS = (
    "Operator Guidance / Empty-State Intelligence",
    "Admin Boundary / Exposure Review",
    "Secondary Console Views / Detail Screens",
    "Visual Polish / Premium IA_CORE Layer",
    "Panel Maestro vs User Panel Separation",
    "Component Documentation / Style Reference",
    "Future Benchmark Review",
    "Contract Storytelling / Operator Narrative",
    "Density Reduction / Information Architecture",
)


FORBIDDEN_OPERATIONAL_ROUTES = (
    "/api/debate/start",
    "/api/dispatch",
    "/api/runtime",
    "/api/execution",
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
        "UI_UX_NEXT_BLOCK_PLAN_1_15_DEFINED",
        "POST_1_14_STATE_REVIEWED",
        "NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE",
        "NEXT_BLOCK_SEQUENCE_PROPOSED",
        "EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK",
    ):
        assert verdict in text

    assert "a611db90" in text
    assert CHECKPOINT_114.exists()
    assert "UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_PASSED" in _read(CHECKPOINT_114)


def test_document_references_post_1_14_state_and_contractual_base():
    text = _read(DOC)

    for token in (
        "checkpoint responsive/accesibilidad `1.14`",
        "1.11 -> 1.13",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "summary/detail/raw-safe",
        "paneles de detalle 1.7",
        "navegacion interna 1.8",
        "sistema de componentes 1.9",
        "hardening responsive/accesibilidad 1.13",
        "raw-safe read-only",
    ):
        assert token in text

    for viewport in (
        "1440x1000",
        "1280x800",
        "1024x768",
        "768x1024",
        "430x932",
        "390x844",
        "360x740",
    ):
        assert viewport in text


def test_post_1_14_audit_sections_are_recorded():
    text = _read(DOC)

    for section in (
        "Fortalezas",
        "Deudas Visibles",
        "Deudas UX",
        "Deudas De Orientacion",
        "Deudas De Densidad",
        "Deudas De Documentacion",
        "Riesgos De Crecimiento",
    ):
        assert section in text

    for risk in (
        "UI Frankenstein",
        "Saturacion visual",
        "Permisos inferidos",
        "Pantallas demasiado pronto",
        "Polish antes de guia/limites",
    ):
        assert risk in text


def test_all_candidate_options_are_evaluated_with_required_fields():
    text = _read(DOC)

    for option in OPTIONS:
        assert option in text

    for field in (
        "Descripcion:",
        "Valor:",
        "Riesgo:",
        "Costo:",
        "Dependencia con bloques previos:",
        "UI nueva:",
        "Endpoints:",
        "Confusion operativa:",
        "Lectura:",
    ):
        assert text.count(field) >= len(OPTIONS)


def test_decision_criteria_matrix_and_selected_option_are_present():
    text = _read(DOC)

    for criterion in (
        "continuidad con 1.14",
        "riesgo de UI Frankenstein",
        "riesgo de permisos inferidos",
        "riesgo de saturacion visual",
        "riesgo de crear pantallas demasiado pronto",
        "valor para operador",
        "costo de implementacion",
        "impacto sobre contract-awareness",
        "compatibilidad con no-runtime/no-execution",
        "si conviene guiar mejor antes de pulir",
        "si conviene auditar limites antes de expandir",
    ):
        assert criterion in text

    assert "Matriz De Decision" in text
    assert "Admin Boundary / Exposure Review | Alto" in text
    assert "La opcion seleccionada es:" in text
    assert "`Admin Boundary / Exposure Review`" in text


def test_selected_option_is_justified_and_has_first_prompt():
    text = _read(DOC)

    for heading in (
        "Por Que Ahora",
        "Por Que No Las Otras Primero",
        "Riesgos Que Reduce",
        "Que Habilita Despues",
        "Que No Debe Hacer Todavia",
        "Primer prompt exacto del bloque",
    ):
        assert heading in text

    assert (
        "PROMPT UI/UX 1.16 - Auditar boundaries administrativos y exposicion "
        "interna de consola IA_CORE contract-aware sin runtime/no-execution"
    ) in text


def test_admin_boundary_sequence_and_postponed_options_are_recorded():
    text = _read(DOC)

    for prompt in (
        "1.16 - Auditar boundaries administrativos y exposicion interna",
        "1.17 - Endurecer affordances",
        "1.18 - Checkpoint Admin Boundary / Exposure Review",
    ):
        assert prompt in text

    for token in (
        "Operator Guidance / Empty-State Intelligence: pospuesta cercana",
        "Contract Storytelling / Operator Narrative: pospuesta cercana",
        "Density Reduction / Information Architecture: pospuesta cercana",
        "Pantallas secundarias: pospuestas",
        "Polish premium: pospuesto",
        "Benchmarks externos",
        "Panel Maestro vs Panel Usuario",
        "Documentacion extendida de componentes",
    ):
        assert token in text


def test_next_exact_prompt_is_declared_in_doc_and_readme_without_implementing_it():
    text = _read(DOC)
    readme = _read(README)

    next_prompt = (
        "PROMPT UI/UX 1.16 - Auditar boundaries administrativos y exposicion "
        "interna de consola IA_CORE contract-aware sin runtime/no-execution"
    )
    assert next_prompt in text
    assert next_prompt in readme
    assert "1.15 no implementa el bloque elegido" in readme


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

    active_code = _read(INDEX) + _read(WIDGETS) + _read(INTERACTIONS)
    for route in FORBIDDEN_OPERATIONAL_ROUTES:
        assert route not in active_code


def test_external_references_remain_future_benchmarks_only():
    text = _read(DOC)
    readme = _read(README)

    for reference in ("21st.dev", "UI UX Pro Max Skill", "Framer Motion / Motion"):
        assert reference in text
        assert reference in readme

    assert "benchmarks futuros solamente" in text
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


def test_readme_records_1_15_plan_and_selected_next_block():
    normalized = " ".join(_read(README).split())

    assert "Planificacion siguiente bloque UI/UX 1.15" in normalized
    assert "UI_UX_NEXT_BLOCK_PLAN_1_15.md" in normalized
    assert "Admin Boundary / Exposure Review" in normalized
    assert "UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK" in normalized
    assert "no runtime" in normalized
    assert "no execution" in normalized
    assert "benchmarks futuros" in normalized
    assert "no implementa el bloque elegido" in normalized
