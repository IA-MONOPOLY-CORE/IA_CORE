from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_1_83.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
NEXT_PROMPT = (
    "PROMPT UI/UX 1.84 - Checkpoint guardrails pre-implementacion "
    "Contract Overview Screen IA_CORE contract-aware sin runtime/no-execution"
)
DECISION = "CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY"


def read(path):
    return path.read_text(encoding="utf-8")


def test_guardrails_document_exists_and_records_base_context():
    text = read(DOC)
    markers = (
        "UI/UX Contract Overview Pre-Implementation Guardrails 1.83",
        "476831e",
        "UI_UX_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_CHECKPOINT_1_82",
        "FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED",
        "EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN",
        "Contract Overview",
        "Blocked & Forbidden",
        "Validation & Readiness",
        "Panel Maestro",
        "FSC-CO-01",
    )
    assert all(marker in text for marker in markers)


def test_required_guardrail_sections_are_present():
    text = read(DOC)
    headings = (
        "## Objetivo",
        "## Estado recibido",
        "## Alcance",
        "## Fuera de alcance obligatorio",
        "## Datos permitidos",
        "## Datos prohibidos",
        "## Estados visuales permitidos",
        "## Estados operativos prohibidos",
        "## Acciones visuales permitidas",
        "## Acciones prohibidas",
        "## Elementos visuales minimos futuros",
        "## Pruebas minimas futuras",
        "## Criterios de entrada",
        "## Criterios de salida",
        "## Registro de riesgos",
        "## Decision",
        "## Siguiente bloque",
    )
    assert all(heading in text for heading in headings)


def test_contract_boundaries_and_no_runtime_limits_are_explicit():
    text = read(DOC)
    markers = (
        "No se implemento pantalla.",
        "No se modifico UI activa.",
        "No se creo componente nuevo.",
        "No se creo User Panel.",
        "No se crearon rutas/hash.",
        "No se crearon endpoints.",
        "No se crearon fetches.",
        "No se activo runtime.",
        "No se activo execution.",
        "No se activo dispatch.",
        "No se toco backend.",
        "backend_internal_ui_payload.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "ready-no-permission",
        "validation",
        "No es User Panel",
        "SAAOP/Loteria",
        "snapshot documental",
    )
    assert all(marker in text for marker in markers)


def test_single_decision_and_exact_next_prompt_are_present():
    text = read(DOC)
    assert text.count(DECISION) == 2
    assert NEXT_PROMPT in text


def test_no_scope_markers_are_complete():
    text = read(DOC)
    markers = (
        "No se tocaron backend/runtime/endpoints/CI/dependencias.",
        "No se limpio deuda residual.",
        "No se corrigieron pyflakes.",
        "No se modifico CI/dependencias.",
        "No se hizo push.",
        "No se avanzo a 1.84.",
    )
    assert all(marker in text for marker in markers)


def test_readmes_register_the_1_83_guardrails_checkpoint():
    for path in (README, WEB_README):
        text = read(path)
        markers = (
            "UI/UX preparado hasta 1.83",
            "guardrails pre-implementacion Contract Overview",
            DECISION,
            NEXT_PROMPT,
            "no implementa pantalla",
            "sin UI activa modificada",
            "sin componente nuevo",
            "User Panel no implementado",
            "sin rutas/hash",
            "sin backend/runtime/endpoints/CI/dependencias",
            "no push",
        )
        assert all(marker in text for marker in markers), path
