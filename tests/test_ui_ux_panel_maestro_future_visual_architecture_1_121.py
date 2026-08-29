from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_1_121.md"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_future_visual_architecture_document_is_complete():
    text = read(DOC)
    assert text.startswith("# UI/UX Panel Maestro Future Visual Architecture 1.121")
    assert "f3a2670" in text
    assert "01d09ce" in text
    for commit in ("8843b60", "03975b9"):
        assert commit in text

    for marker in (
        "Final Screen Contracts consolidado",
        "elementos inferiores bloqueados",
        "deuda UX futura",
        "Contract Overview",
        "Blocked & Forbidden",
        "Validation & Readiness",
        "Request Contract Preview",
        "DEFER_FINALIZATION",
        "No hay implementación",
        "no-runtime/no-execution",
    ):
        assert marker in text

    layers = (
        "Master Shell",
        "Overview Layer",
        "Contracts Layer",
        "Context Layer",
        "Evidence Layer",
        "Configuration Read-only Layer",
        "Future Work / Roadmap Layer",
    )
    for layer in layers:
        assert layer in text

    screens = (
        "Panel Maestro Overview",
        "Domains Context Screen",
        "Agents Context Screen",
        "Final Screen Contracts Screen",
        "Validation & Readiness Screen",
        "Blocked Capabilities Screen",
        "Request Contract Preview Screen",
        "Evidence & Details Screen",
        "Configuration Read-only Screen",
        "Roadmap / Future Work Screen",
        "Design System / Visual Tokens Screen",
    )
    for screen in screens:
        assert screen in text

    responsibilities = (
        "Overview no ejecuta",
        "Domains no crea dominio directo",
        "Agents no invoca modelos",
        "Contracts no activa capacidades",
        "Validation no aprueba ejecución",
        "Blocked no oculta bloqueos",
        "Request Preview no envía requests",
        "Evidence no muestra payload crudo",
        "Configuration no muta configuración",
        "Roadmap no presenta futuro como activo",
        "Design System no crea comportamiento",
    )
    for responsibility in responsibilities:
        assert responsibility in text

    for marker in (
        "CFG",
        "DOMAIN",
        "`+`",
        "RELEER PAYLOAD LOCAL",
        "VER DETALLE",
        "VER EVIDENCIA",
        "Tarjetas de agentes",
        "Indicadores de dominio",
        "Chips, labels y pills",
        "El `+` no debe existir como acción global ambigua",
        "elementos inferiores",
    ):
        assert marker in text

    for marker in (
        "no User Panel",
        "rutas/hash",
        "No se agregan endpoints, fetches",
        "Navegación futura",
        "índice documental",
        "progressive disclosure",
        "densidad visual",
        "copy",
        "IA_CORE",
        "SAAOP/Lotería",
    ):
        assert marker in text

    allowed_states = (
        "READ_ONLY",
        "BLOCKED_BY_CONTRACT",
        "DOCUMENTED",
        "PLANNED",
        "DEFERRED",
        "NEEDS_VALIDATION",
        "VALIDATED_DOCUMENTALLY",
        "FUTURE_ONLY",
        "NO_RUNTIME",
        "NO_EXECUTION",
    )
    prohibited_states = (
        "ACTIVE",
        "RUNNING",
        "LIVE",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "PROCESSING",
        "SENT",
        "ENQUEUED",
        "SCHEDULED",
        "READY_TO_RUN",
    )
    for state in allowed_states + prohibited_states:
        assert f"`{state}`" in text

    for marker in (
        "Preservar",
        "Absorber",
        "separar",
        "eliminar",
        "rediseñar",
        "Dependencias antes de implementación",
        "1.122",
        "1.123",
        "1.124",
        "1.125",
        "1.126",
        "Registro de riesgos",
        "Arquitectura antes de guardrails",
        "Rutas/hash",
        "User Panel",
        "fetches",
        "Pérdida de `DEFER_FINALIZATION`",
        "Blockers ocultos",
        "Éxito falso",
        "Ghost actions",
        "no push",
    ):
        assert marker in text

    decisions = (
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_READY_FOR_PRE_IMPLEMENTATION_GUARDRAILS",
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_READY_FOR_FIRST_BLOCK_PLANNING",
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_NEEDS_MORE_DETAIL",
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_BLOCKED_NEEDS_FIX",
        "PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_BLOCKED_CRITICAL",
    )
    selected = [decision for decision in decisions if decision in text]
    assert selected == [decisions[0]]
    assert text.count(decisions[0]) == 1
    assert "PROMPT UI/UX 1.122 - Guardrails pre-implementacion rediseño estructural Panel Maestro IA_CORE contract-aware sin runtime/no-execution" in text

    for path in (README, UI_README):
        assert "1.121" in read(path)


def test_current_ui_contract_and_lower_console_remain_unchanged_in_place():
    text = read(INDEX)
    for marker in (
        'data-contract-screen="FSC-CO-01"',
        'data-contract-screen="FSC-BF-02"',
        'data-contract-screen="FSC-VR-03"',
        'data-contract-screen="FSC-RCP-04"',
        "DEFER_FINALIZATION",
        "LOWER_CONSOLE_READ_ONLY",
        "data-contract-blocked",
        "RELEER PAYLOAD LOCAL",
        "Ver detalle",
        "Ver evidencia",
    ):
        assert marker in text
    assert "history.pushState" not in text
    assert "history.replaceState" not in text
    assert "location.hash" not in text
    assert "hashchange" not in text
