from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RESULT_HISTORY_READ_MODEL_INTEGRATION_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_result_history_read_model_integration_audit_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "RESULT_HISTORY_READ_MODEL_INTEGRATION_AUDIT_COMPLETED" in text
    assert "RESULT_HISTORY_READ_MODEL_INTEGRATION_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_result_history_read_model_contract" in text
    assert "PROMPT 3.8 — Contrato de integración result/history/read model read-only" in text


def test_audit_contains_required_concepts():
    text = _text()

    for concept in [
        "ExecutionIntent",
        "execution_attempt_id",
        "ExecutionAttempt",
        "ExecutionAttempt state machine",
        "ExecutionResult",
        "Result Store",
        "Lifecycle event",
        "Dry-run output",
        "Execution history view",
        "Internal backend read model",
    ]:
        assert concept in text


def test_audit_answers_required_questions():
    text = _text()

    for phrase in [
        "Que debe aportar ExecutionResult a execution_history_view",
        "Que debe aportar ExecutionResult al internal_backend_read_model",
        "Que datos pertenecen al lifecycle",
        "Que datos pertenecen al dry-run",
        "Que no debe entrar todavia al read model",
    ]:
        assert phrase in text


def test_audit_contains_future_flows():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "ExecutionAttempt",
        "ExecutionAttempt state machine",
        "ExecutionResult",
        "Result Store",
        "Execution history view",
        "Internal backend read model",
        "dry_run_store",
    ]:
        assert phrase in text


def test_audit_contains_candidate_fields():
    text = _text()

    for field in [
        "intent_id",
        "attempt_id",
        "result_id",
        "attempt_state",
        "result_status",
        "result_type",
        "created_at",
        "updated_at",
        "completed_at",
        "summary",
        "warnings_count",
        "artifacts_count",
        "has_error",
        "is_runtime_backed",
        "is_dry_run",
        "source",
    ]:
        assert field in text


def test_audit_contains_required_risks():
    text = _text()

    for risk in [
        "history view consumiendo result no operativo",
        "read model consumiendo result no operativo",
        "dry-run confundido con resultado real",
        "result sin attempt valido",
        "attempt sin intent valido",
        "result duplicado",
        "estado de attempt desincronizado",
        "lifecycle event confundido con result",
        "datos sensibles",
        "outputs demasiado grandes",
        "activacion accidental de store writes",
        "activacion accidental de runtime",
    ]:
        assert risk in text


def test_audit_contains_required_boundaries():
    text = _text()

    for boundary in [
        "no integracion real result/history/read model",
        "no result store operativo",
        "no ExecutionResult persistence",
        "no result_id generator operativo",
        "no history writes",
        "no read model writes",
        "no store writes",
        "no lifecycle writes",
        "no runtime execution",
        "no scheduler",
        "no worker",
        "no queue",
        "no model invocation",
        "no tool execution",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
    ]:
        assert boundary in text


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog permanece planned_not_active" in text
    assert "Business Composition Layer permanece futura/no operativa" in text


def test_no_operational_integration_modules_were_created():
    for relative in [
        "core/result_history_integrator.py",
        "core/result_read_model_writer.py",
        "core/result_history_projection_writer.py",
        "core/result_store_writer.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "result_history_integration_enabled = true",
        "read_model_writes_enabled = true",
        "history_writes_enabled = true",
        "result_store_enabled = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
        "lifecycle_writes_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text
