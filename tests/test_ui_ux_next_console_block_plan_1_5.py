from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_CONSOLE_BLOCK_PLAN_1_5.md"
DOC_14 = ROOT / "docs" / "UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "ui" / "web" / "README.md"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_next_console_block_plan_document_exists_and_declares_verdicts():
    text = _read(DOC)

    for verdict in (
        "UI_UX_NEXT_CONSOLE_BLOCK_PLAN_DEFINED",
        "IA_CORE_CONSOLE_BLOCK_CONTINUITY_CONFIRMED",
        "NEXT_CONSOLE_BLOCK_SELECTED_WITH_EVIDENCE",
        "EXTERNAL_REFERENCES_REGISTERED_AS_BENCHMARKS_ONLY",
        "NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED",
        "UI_READY_FOR_SELECTED_NEXT_CONSOLE_BLOCK",
    ):
        assert verdict in text

    assert "ee7323d5" in text
    assert DOC_14.exists()


def test_plan_summarizes_console_block_1_0_through_1_4():
    text = _read(DOC)

    for token in (
        "1.0 estructuro",
        "1.1 refino",
        "1.2 definio",
        "1.3 definio",
        "1.4 cerro",
        'data-main-console="contract-aware-1.0"',
        'data-console-refinement="1.1"',
        'data-console-flow="contract-aware-1.2"',
        'data-console-interaction="contract-aware-1.3"',
    ):
        assert token in text


def test_plan_evaluates_required_options_and_selects_one():
    text = _read(DOC)

    for option in (
        "Opcion A - Navegacion interna de consola",
        "Opcion B - Paneles de detalle contract-aware",
        "Opcion C - Modelo de lectura de payload/contract",
        "Opcion D - Sistema de componentes IA_CORE",
        "Opcion E - Primera pantalla secundaria",
        "Opcion F - Benchmark visual externo futuro",
    ):
        assert option in text

    assert "`Opcion C - Modelo de lectura de payload/contract`" in text
    assert "summary/detail/raw-safe" in text
    assert "mas reduce riesgo antes de construir mas UI" in text


def test_plan_includes_exact_next_prompt_and_sequence():
    text = _read(DOC)

    assert (
        "PROMPT UI/UX 1.6 - Definir modelo de lectura de payload/contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    ) in text
    for step in ("1.6", "1.7", "1.8", "1.9", "1.10"):
        assert step in text


def test_plan_preserves_no_runtime_no_execution_and_no_endpoints():
    text = _read(DOC)

    for token in (
        "no endpoint publico, API ni router HTTP",
        "no runtime ni execution",
        "no dispatch real",
        "no controlled execution",
        "no agentes ejecutados",
        "no invocacion de models, tools o integrations",
        "no cambio de contrato backend",
    ):
        assert token in text


def test_plan_confirms_contract_authority_and_identity():
    text = _read(DOC)

    for token in (
        "IA_CORE como identidad visual activa",
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "internal_dispatcher_no_runtime",
    ):
        assert token in text


def test_external_references_are_benchmarks_only_without_install_or_copy():
    text = _read(DOC)

    for reference in ("21st.dev", "UI UX Pro Max Skill", "Framer Motion / Motion"):
        assert reference in text

    for constraint in (
        "benchmarks futuros",
        "No se instalan ahora",
        "no se copian",
        "no definen identidad",
        "no reemplazan IA_CORE",
        "no agregan dependencias",
        "no habilitan templates externos",
    ):
        assert constraint in text


def test_active_ui_and_contract_files_remain_unmodified_by_plan():
    html = _read(INDEX)
    widgets = _read(WIDGETS)
    admin = _read(ADMIN)
    interactions = _read(INTERACTIONS)

    assert 'data-main-console="contract-aware-1.0"' in html
    assert 'data-console-refinement="1.1"' in html
    assert 'data-console-flow="contract-aware-1.2"' in html
    assert 'data-console-interaction="contract-aware-1.3"' in html
    assert "fetch(" not in widgets
    assert "fetch(" not in interactions
    assert "No se renderizan acciones sin allowed_actions." in admin

    for forbidden_route in (
        "/api/debate/start",
        "/api/dispatch",
        "/api/runtime",
        "/api/execution",
    ):
        assert forbidden_route not in html
        assert forbidden_route not in widgets
        assert forbidden_route not in admin
        assert forbidden_route not in interactions


def test_readme_records_plan_without_legacy_or_external_dependency_activation():
    readme = _read(README)

    assert "Plan de siguiente bloque 1.5" in readme
    assert "modelo de lectura de payload/contract" in readme
    assert "benchmarks futuros" in readme
    assert "no se instalan" in readme
    assert "no reemplazan IA_CORE" in readme

    for legacy in ("SAAOP", "S.A.A.O.P.", "Loteria", "LoterÃ­a", "Tactical HUD"):
        assert legacy not in readme
