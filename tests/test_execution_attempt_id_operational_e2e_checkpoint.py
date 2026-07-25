import json
from pathlib import Path

from core.execution_intent import (
    EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED,
    EXECUTION_INTENT_EXECUTION_ENABLED,
    EXECUTION_INTENT_RUNTIME_ENABLED,
)


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DOC = ROOT / "docs" / "EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_CHECKPOINT.md"
OPERATIONAL_AUDIT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_OPERATIONAL_BOUNDARY_AUDIT.md"
INTENT_DOC = ROOT / "docs" / "EXECUTION_INTENT_CONTRACT.md"
ATTEMPT_ID_AUDIT_DOC = ROOT / "docs" / "EXECUTION_ATTEMPT_ID_OPERATIONAL_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return CHECKPOINT_DOC.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_declares_e2e_passed():
    text = _text()

    assert CHECKPOINT_DOC.exists()
    assert "EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_PASSED" in text
    for prompt in [
        "PROMPT 3.0 — Auditoría de frontera operacional",
        "PROMPT 3.1 — Contrato de execution intent operativo",
        "PROMPT 3.2 — Auditoría de execution_attempt_id operativo",
        "PROMPT 3.3 — Schema de execution attempt operativo",
    ]:
        assert prompt in text


def test_checkpoint_contains_validated_verdicts_and_readiness():
    text = _text()

    for verdict in [
        "OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "EXECUTION_INTENT_CONTRACT_READY",
        "EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN",
    ]:
        assert verdict in text
    for readiness in [
        "ready_for_execution_intent_contract",
        "ready_for_execution_attempt_id_audit",
        "ready_for_execution_attempt_schema",
    ]:
        assert readiness in text


def test_previous_contract_documents_exist_and_keep_expected_markers():
    assert OPERATIONAL_AUDIT_DOC.exists()
    assert INTENT_DOC.exists()
    assert ATTEMPT_ID_AUDIT_DOC.exists()

    intent_text = INTENT_DOC.read_text(encoding="utf-8")
    attempt_audit_text = ATTEMPT_ID_AUDIT_DOC.read_text(encoding="utf-8")

    assert "EXECUTION_INTENT_CONTRACT_READY" in intent_text
    assert "ready_for_execution_attempt_id_audit" in intent_text
    assert "EXECUTION_ATTEMPT_ID_AUDIT_COMPLETED" in attempt_audit_text
    assert "ready_for_execution_attempt_schema" in attempt_audit_text


def test_execution_intent_remains_contract_only():
    assert EXECUTION_INTENT_RUNTIME_ENABLED is False
    assert EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED is False
    assert EXECUTION_INTENT_EXECUTION_ENABLED is False


def test_market_catalog_database_remains_non_active():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert catalog["metadata"]["activation_status"] == "not_evaluated"


def test_checkpoint_did_not_create_operational_execution_modules():
    for relative in [
        "core/execution_attempt.py",
        "core/execution_attempt_factory.py",
        "core/execution_attempt_id.py",
        "core/execution_result_store.py",
        "core/result_store.py",
        "core/runtime_runner.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_checkpoint_prohibits_activation_surfaces():
    text = _text()

    for phrase in [
        "ExecutionAttempt operativo",
        "execution_attempt_id generator operativo",
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
        "Market Catalog runtime",
        "Business Composition Layer runtime",
    ]:
        assert phrase in text


def test_checkpoint_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "execution_enabled = true",
        "attempt_creation_enabled = true",
        "runtime_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text

