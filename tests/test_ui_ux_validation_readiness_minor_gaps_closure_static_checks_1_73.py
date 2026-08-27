from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_VALIDATION_READINESS_MINOR_GAPS_CLOSURE_1_73.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps "
    "Closure IA_CORE contract-aware sin runtime/no-execution"
)

FINAL_CONTRACT_GLOB = "UI_UX_VALIDATION_READINESS_FINAL_SCREEN_CONTRACT_*.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_no_validation_readiness_final_contract_document_was_created():
    final_contracts = list((ROOT / "docs").glob(FINAL_CONTRACT_GLOB))
    assert final_contracts == []


def test_closure_declares_no_final_contract_screen_user_panel_or_ui_active_change():
    text = read(DOC).lower()

    markers = [
        "no crea `validation & readiness final screen contract`",
        "no ejecuta final contract audit",
        "no crea pantalla",
        "no modifica ui activa",
        "no crea user panel",
        "validation & readiness final screen contract` no creado todavia",
        "final contract audit no ejecutado",
        "ui activa no modificada",
        "user panel no implementado",
    ]
    for marker in markers:
        assert marker in text


def test_closure_declares_no_endpoints_fetches_runtime_execution_or_ci():
    text = read(DOC).lower()

    markers = [
        "no crea rutas/hash/endpoints/fetches",
        "no agrega dependencias",
        "no modifica ci",
        "no activa runtime/execution/dispatch/controlled execution",
        "no endpoint/fetch",
        "no route/hash",
        "no router",
        "no runtime/execution/dispatch/controlled execution",
        "no unlock/override/bypass/permission escalation",
    ]
    for marker in markers:
        assert marker in text


def test_allowed_and_forbidden_states_are_contextual():
    text = read(DOC)

    allowed = [
        "read-only",
        "documented",
        "draft",
        "candidate",
        "not implemented",
        "planned",
        "blocked",
        "forbidden",
        "unavailable",
        "no_payload",
        "invalid",
        "pending documental no-running",
        "passed documental",
        "failed documental",
        "ready contractual no-permission",
        "ready_for_final_contract_audit_next",
    ]
    for marker in allowed:
        assert marker in text

    forbidden_sentence = (
        "Estados prohibidos como UI validos: active, running, live, operational, "
        "executing, dispatching, submitted, processing, activated, operating, queued, "
        "in progress as runtime, unlockable, overridable, pending permission y escalation pending."
    )
    assert forbidden_sentence in text
    assert "Solo pueden aparecer en contexto de prohibicion documental." in text


def test_no_ready_as_executable_or_valid_as_safe_to_execute():
    text = read(DOC)

    markers = [
        "`ready` no significa ejecutable ahora",
        "`ready` no significa permiso",
        "no habilita submit/execute/dispatch",
        "`validation.valid` es resultado declarado por contrato",
        "no live validation",
        "Sin safe-to-execute derivado de validacion",
        "valid=true como safe-to-execute | Mitigado",
    ]
    for marker in markers:
        assert marker in text


def test_readme_cursors_point_to_1_74_checkpoint():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
    for text in (root, web):
        assert "UI/UX avanzado hasta 1.73" in text
        assert "gaps menores Validation & Readiness cerrados" in text
        assert "READY_FOR_FINAL_CONTRACT_AUDIT_NEXT" in text
        assert "no final contract" in text
        assert "no pantalla" in text
        assert "no UI activa" in text
        assert "User Panel no implementado" in text
        assert "no-runtime/no-execution" in text
        assert "push pospuesto" in text.lower()
        assert NEXT_PROMPT in text
