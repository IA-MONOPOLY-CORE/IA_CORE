import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DOC = ROOT / "docs" / "RESULT_STORE_BOUNDARY_AUDIT_E2E_CHECKPOINT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return CHECKPOINT_DOC.read_text(encoding="utf-8")


def test_result_store_boundary_audit_e2e_exists_and_declares_chain():
    text = _text()

    assert CHECKPOINT_DOC.exists()
    assert "RESULT_STORE_BOUNDARY_AUDIT_E2E_PASSED" in text
    for prompt in [
        "PROMPT 3.0 — Auditoría de frontera operacional",
        "PROMPT 3.1 — Contrato de execution intent operativo",
        "PROMPT 3.2 — Auditoría de execution_attempt_id operativo",
        "PROMPT 3.2.1 — Checkpoint E2E de execution_attempt_id operativo",
        "PROMPT 3.3 — Schema de execution attempt operativo",
        "PROMPT 3.4 — State machine operacional contract-only",
        "PROMPT 3.5 — Auditoría de result store boundary",
        "PROMPT 3.6 — Contrato de result store operativo read-only",
    ]:
        assert prompt in text


def test_result_store_boundary_audit_e2e_contains_verdicts_and_readiness():
    text = _text()

    for verdict in [
        "OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "EXECUTION_INTENT_CONTRACT_READY",
        "EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN",
        "EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_PASSED",
        "EXECUTION_ATTEMPT_SCHEMA_READY",
        "EXECUTION_ATTEMPT_SCHEMA_E2E_PASSED",
        "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY",
        "EXECUTION_ATTEMPT_STATE_MACHINE_E2E_PASSED",
        "RESULT_STORE_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
    ]:
        assert verdict in text
    for readiness in [
        "ready_for_execution_intent_contract",
        "ready_for_execution_attempt_id_audit",
        "ready_for_execution_attempt_schema",
        "ready_for_operational_state_machine_contract",
        "ready_for_result_store_boundary_audit",
        "ready_for_result_store_contract",
    ]:
        assert readiness in text


def test_market_catalog_and_business_composition_remain_non_operational():
    text = _text()
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert "Market Catalog sigue `planned_not_active`" in text
    assert "Business Composition Layer sigue futura/no operativa" in text


def test_result_store_boundary_e2e_keeps_runtime_and_writes_disabled():
    text = _text()

    for phrase in [
        "No se activo result store",
        "ExecutionResult operativo",
        "result_id generator",
        "runtime",
        "store writes",
        "lifecycle writes",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "memory persistence",
        "external access",
        "API",
        "UI",
    ]:
        assert phrase in text


def test_result_store_boundary_e2e_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "result_store_enabled = true",
        "execution_result_enabled = true",
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
