import json
from pathlib import Path

from core.execution_attempt import (
    EXECUTION_ATTEMPT_EXECUTION_ENABLED,
    EXECUTION_ATTEMPT_FACTORY_ENABLED,
    EXECUTION_ATTEMPT_QUEUE_ENABLED,
    EXECUTION_ATTEMPT_RESULT_STORE_ENABLED,
    EXECUTION_ATTEMPT_RUNTIME_ENABLED,
    EXECUTION_ATTEMPT_SCHEDULER_ENABLED,
    EXECUTION_ATTEMPT_STORE_WRITES_ENABLED,
    EXECUTION_ATTEMPT_WORKER_ENABLED,
)


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DOC = ROOT / "docs" / "EXECUTION_ATTEMPT_SCHEMA_E2E_CHECKPOINT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return CHECKPOINT_DOC.read_text(encoding="utf-8")


def test_schema_e2e_checkpoint_exists_and_declares_chain():
    text = _text()

    assert CHECKPOINT_DOC.exists()
    assert "EXECUTION_ATTEMPT_SCHEMA_E2E_PASSED" in text
    for prompt in [
        "PROMPT 3.0 — Auditoría de frontera operacional",
        "PROMPT 3.1 — Contrato de execution intent operativo",
        "PROMPT 3.2 — Auditoría de execution_attempt_id operativo",
        "PROMPT 3.2.1 — Checkpoint E2E de execution_attempt_id operativo",
        "PROMPT 3.3 — Schema de execution attempt operativo",
        "PROMPT 3.4 — State machine operacional contract-only",
    ]:
        assert prompt in text


def test_schema_e2e_checkpoint_contains_verdicts_and_readiness():
    text = _text()

    for verdict in [
        "OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "EXECUTION_INTENT_CONTRACT_READY",
        "EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN",
        "EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_PASSED",
        "EXECUTION_ATTEMPT_SCHEMA_READY",
    ]:
        assert verdict in text
    for readiness in [
        "ready_for_execution_intent_contract",
        "ready_for_execution_attempt_id_audit",
        "ready_for_execution_attempt_schema",
        "ready_for_operational_state_machine_contract",
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


def test_runtime_factory_store_and_execution_boundaries_remain_disabled():
    assert EXECUTION_ATTEMPT_RUNTIME_ENABLED is False
    assert EXECUTION_ATTEMPT_FACTORY_ENABLED is False
    assert EXECUTION_ATTEMPT_STORE_WRITES_ENABLED is False
    assert EXECUTION_ATTEMPT_RESULT_STORE_ENABLED is False
    assert EXECUTION_ATTEMPT_EXECUTION_ENABLED is False
    assert EXECUTION_ATTEMPT_SCHEDULER_ENABLED is False
    assert EXECUTION_ATTEMPT_WORKER_ENABLED is False
    assert EXECUTION_ATTEMPT_QUEUE_ENABLED is False

    text = _text()
    for phrase in [
        "factory activa",
        "store writes",
        "result store",
        "runtime execution",
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


def test_schema_e2e_checkpoint_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "runtime_enabled = true",
        "factory_enabled = true",
        "store_writes_enabled = true",
        "result_store_enabled = true",
        "execution_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text
