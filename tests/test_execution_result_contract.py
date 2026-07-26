import json
from pathlib import Path

from core.execution_attempt import build_execution_attempt_schema
from core.execution_result import (
    EXECUTION_RESULT_CONTRACT_STATUS,
    EXECUTION_RESULT_EXECUTION_ENABLED,
    EXECUTION_RESULT_EXTERNAL_ACCESS_ENABLED,
    EXECUTION_RESULT_ID_GENERATOR_ENABLED,
    EXECUTION_RESULT_LIFECYCLE_WRITES_ENABLED,
    EXECUTION_RESULT_MEMORY_PERSISTENCE_ENABLED,
    EXECUTION_RESULT_MODEL_INVOCATION_ENABLED,
    EXECUTION_RESULT_QUEUE_ENABLED,
    EXECUTION_RESULT_RUNTIME_ENABLED,
    EXECUTION_RESULT_SCHEDULER_ENABLED,
    EXECUTION_RESULT_STORE_ENABLED,
    EXECUTION_RESULT_STORE_WRITES_ENABLED,
    EXECUTION_RESULT_TOOL_EXECUTION_ENABLED,
    EXECUTION_RESULT_WORKER_ENABLED,
    build_execution_result_contract,
    build_result_contract_from_attempt,
    serialize_execution_result_contract,
    validate_execution_result_contract,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EXECUTION_RESULT_CONTRACT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _valid_result():
    return build_execution_result_contract(
        result_id="result_attempt_intent_agent_audit_001_0001_ab12cd34_0001",
        attempt_id="attempt_intent_agent_audit_001_0001_ab12cd34",
        intent_id="intent_agent_audit_001",
        status="schema_validated",
        result_type="contract_validation",
        summary="contract placeholder",
    )


def _valid_attempt():
    return build_execution_attempt_schema(
        attempt_id="attempt_intent_agent_audit_001_0001_ab12cd34",
        intent_id="intent_agent_audit_001",
        intent_type="agent_operation",
        target_type="agent",
        target_id="agent-1",
        mode="contract_validation",
        requested_by="system",
        status="schema_validated",
        lifecycle_state="not_started",
        readiness="ready_for_state_machine_design",
        metadata={"state_machine_state": "schema_validated"},
    )


def _payload():
    return serialize_execution_result_contract(_valid_result())


def _codes(result: dict) -> set[str]:
    return {blocker["code"] for blocker in result["blockers"]}


def test_execution_result_contract_module_and_boundaries_exist():
    assert (ROOT / "core" / "execution_result.py").exists()
    assert EXECUTION_RESULT_CONTRACT_STATUS == "read_only_contract"
    assert EXECUTION_RESULT_STORE_ENABLED is False
    assert EXECUTION_RESULT_STORE_WRITES_ENABLED is False
    assert EXECUTION_RESULT_ID_GENERATOR_ENABLED is False
    assert EXECUTION_RESULT_RUNTIME_ENABLED is False
    assert EXECUTION_RESULT_EXECUTION_ENABLED is False
    assert EXECUTION_RESULT_LIFECYCLE_WRITES_ENABLED is False
    assert EXECUTION_RESULT_SCHEDULER_ENABLED is False
    assert EXECUTION_RESULT_WORKER_ENABLED is False
    assert EXECUTION_RESULT_QUEUE_ENABLED is False
    assert EXECUTION_RESULT_MODEL_INVOCATION_ENABLED is False
    assert EXECUTION_RESULT_TOOL_EXECUTION_ENABLED is False
    assert EXECUTION_RESULT_MEMORY_PERSISTENCE_ENABLED is False
    assert EXECUTION_RESULT_EXTERNAL_ACCESS_ENABLED is False


def test_build_serialize_and_validate_valid_contract():
    result = _valid_result()
    payload = serialize_execution_result_contract(result)
    validation = validate_execution_result_contract(result)

    assert payload["result_id"] == "result_attempt_intent_agent_audit_001_0001_ab12cd34_0001"
    assert payload["output_ref"] is None
    assert payload["error_ref"] is None
    assert validation["status"] == "validated"
    assert validation["verdict"] == "EXECUTION_RESULT_CONTRACT_READY"
    assert validation["readiness"] == "ready_for_result_history_read_model_integration_audit"


def test_rejects_required_empty_fields():
    for field, code in [
        ("result_id", "missing_result_id"),
        ("attempt_id", "missing_attempt_id"),
        ("intent_id", "missing_intent_id"),
        ("created_at", "missing_created_at"),
    ]:
        payload = _payload()
        payload[field] = ""
        assert code in _codes(validate_execution_result_contract(payload))


def test_rejects_unknown_status_result_type_and_future_statuses():
    payload = _payload()
    payload["status"] = "unknown"
    assert "invalid_status" in _codes(validate_execution_result_contract(payload))

    payload = _payload()
    payload["status"] = "succeeded"
    codes = _codes(validate_execution_result_contract(payload))
    assert "invalid_status" in codes
    assert "future_result_status_not_allowed" in codes

    payload = _payload()
    payload["result_type"] = "real_output"
    assert "invalid_result_type" in _codes(validate_execution_result_contract(payload))


def test_rejects_output_and_error_refs():
    payload = _payload()
    payload["output_ref"] = "output-1"
    assert "output_ref_not_allowed" in _codes(validate_execution_result_contract(payload))

    payload = _payload()
    payload["error_ref"] = "error-1"
    assert "error_ref_not_allowed" in _codes(validate_execution_result_contract(payload))


def test_rejects_invalid_collection_types():
    for field, value, code in [
        ("metrics", [], "invalid_metrics"),
        ("artifacts", {}, "invalid_artifacts"),
        ("warnings", {}, "invalid_warnings"),
        ("metadata", [], "invalid_metadata"),
        ("summary", [], "invalid_summary"),
    ]:
        payload = _payload()
        payload[field] = value
        assert code in _codes(validate_execution_result_contract(payload))


def test_rejects_any_operational_constraint_true():
    expected = {
        "allow_runtime_execution": "runtime_execution_not_allowed",
        "allow_external_access": "external_access_not_allowed",
        "allow_model_invocation": "model_invocation_not_allowed",
        "allow_tool_execution": "tool_execution_not_allowed",
        "allow_memory_persistence": "memory_persistence_not_allowed",
        "allow_store_write": "store_write_not_allowed",
        "allow_lifecycle_write": "lifecycle_write_not_allowed",
        "allow_result_store_write": "result_store_write_not_allowed",
    }
    for field, code in expected.items():
        payload = _payload()
        payload["constraints"][field] = True
        assert code in _codes(validate_execution_result_contract(payload))


def test_build_result_contract_from_attempt_requires_explicit_result_id():
    try:
        build_result_contract_from_attempt(_valid_attempt(), result_id="")
    except ValueError as exc:
        assert str(exc) == "result_id_required"
    else:
        raise AssertionError("expected result_id_required")


def test_build_result_contract_from_attempt_validates_attempt_and_keeps_refs_empty():
    result = build_result_contract_from_attempt(
        _valid_attempt(),
        result_id="result_attempt_intent_agent_audit_001_0001_ab12cd34_0001",
    )
    payload = serialize_execution_result_contract(result)

    assert payload["attempt_id"] == "attempt_intent_agent_audit_001_0001_ab12cd34"
    assert payload["intent_id"] == "intent_agent_audit_001"
    assert payload["status"] == "schema_validated"
    assert payload["output_ref"] is None
    assert payload["error_ref"] is None
    assert validate_execution_result_contract(payload)["status"] == "validated"


def test_build_result_contract_from_attempt_rejects_invalid_attempt():
    attempt = _valid_attempt().to_dict()
    attempt["attempt_id"] = ""

    try:
        build_result_contract_from_attempt(attempt, result_id="result-1")
    except ValueError as exc:
        assert str(exc) == "execution_attempt_schema_not_validated"
    else:
        raise AssertionError("expected invalid attempt rejection")


def test_contract_does_not_write_stores_create_events_files_or_runtime(tmp_path):
    paths = [
        ROOT / "runtime" / "execution_results" / "execution_result_store.jsonl",
        ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl",
        tmp_path / "execution_result_store.jsonl",
        tmp_path / "execution_lifecycle_store.jsonl",
    ]
    before = {path: path.exists() for path in paths}
    validate_execution_result_contract(_valid_result())
    build_result_contract_from_attempt(_valid_attempt(), result_id="result_attempt_intent_agent_audit_001_0001_ab12cd34_0001")
    after = {path: path.exists() for path in paths}

    assert before == after
    assert EXECUTION_RESULT_RUNTIME_ENABLED is False


def test_market_catalog_and_business_composition_remain_non_operational():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False


def test_execution_result_contract_document_declares_readiness_and_boundaries():
    text = DOC.read_text(encoding="utf-8")

    assert "EXECUTION_RESULT_CONTRACT_READY" in text
    assert "ready_for_result_history_read_model_integration_audit" in text
    assert "PROMPT 3.7 — Auditoría de integración result/history/read model" in text
    for phrase in [
        "read-only contract",
        "no operational result store",
        "no ExecutionResult persistence",
        "no result_id generator",
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
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text

