import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RESULT_STORE_BOUNDARY_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_result_store_boundary_audit_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "RESULT_STORE_BOUNDARY_AUDIT_COMPLETED" in text
    assert "RESULT_STORE_BOUNDARY_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_result_store_contract" in text
    assert "PROMPT 3.6 — Contrato de result store operativo read-only" in text


def test_audit_defines_required_concepts():
    text = _text()

    for concept in [
        "ExecutionIntent",
        "execution_attempt_id",
        "ExecutionAttempt",
        "ExecutionAttempt state machine",
        "ExecutionResult",
        "Result Store",
    ]:
        assert concept in text


def test_audit_answers_required_questions():
    text = _text()

    for phrase in [
        "Que es un resultado",
        "Que NO es un resultado",
        "Diferencia entre ExecutionAttempt y ExecutionResult",
        "Diferencia entre lifecycle event y result",
        "Diferencia entre dry_run output y result",
    ]:
        assert phrase in text


def test_audit_contains_candidate_result_fields():
    text = _text()

    for field in [
        "result_id",
        "attempt_id",
        "intent_id",
        "status",
        "result_type",
        "created_at",
        "completed_at",
        "output_ref",
        "error_ref",
        "summary",
        "metrics",
        "artifacts",
        "warnings",
        "metadata",
        "constraints",
    ]:
        assert field in text


def test_audit_contains_required_risks():
    text = _text()

    for risk in [
        "resultados sin attempt valido",
        "resultados sin intent valido",
        "resultados duplicados",
        "dry_run confundidos con ejecucion real",
        "datos sensibles",
        "outputs demasiado grandes",
        "outputs no serializables",
        "falta de trazabilidad",
        "activacion accidental de runtime",
        "activacion accidental de modelos/tools",
    ]:
        assert risk in text


def test_audit_contains_required_boundaries():
    text = _text()

    for boundary in [
        "no result store operativo",
        "no ExecutionResult operativo",
        "no result_id generator operativo",
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


def test_market_catalog_and_business_composition_boundaries_are_preserved():
    text = _text()
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert "Market Catalog permanece planned_not_active" in text
    assert "Business Composition Layer permanece futura/no operativa" in text


def test_no_operational_result_store_modules_were_created():
    for relative in [
        "core/result_store.py",
        "core/execution_result.py",
        "core/result_store_writer.py",
        "core/result_id_generator.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "result_store_enabled = true",
        "execution_result_enabled = true",
        "store_writes_enabled = true",
        "runtime_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "model_invocation_enabled = true",
        "tool_execution_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text

