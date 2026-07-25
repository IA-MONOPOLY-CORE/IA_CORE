import json
from copy import deepcopy
from pathlib import Path

from core.execution_attempt import (
    EXECUTION_ATTEMPT_EXECUTION_ENABLED,
    EXECUTION_ATTEMPT_EXTERNAL_ACCESS_ENABLED,
    EXECUTION_ATTEMPT_FACTORY_ENABLED,
    EXECUTION_ATTEMPT_MEMORY_PERSISTENCE_ENABLED,
    EXECUTION_ATTEMPT_MODEL_INVOCATION_ENABLED,
    EXECUTION_ATTEMPT_QUEUE_ENABLED,
    EXECUTION_ATTEMPT_RESULT_STORE_ENABLED,
    EXECUTION_ATTEMPT_RUNTIME_ENABLED,
    EXECUTION_ATTEMPT_SCHEDULER_ENABLED,
    EXECUTION_ATTEMPT_SCHEMA_STATUS,
    EXECUTION_ATTEMPT_STORE_WRITES_ENABLED,
    EXECUTION_ATTEMPT_TOOL_EXECUTION_ENABLED,
    EXECUTION_ATTEMPT_WORKER_ENABLED,
    build_attempt_schema_from_intent,
    build_execution_attempt_schema,
    serialize_execution_attempt_schema,
    validate_execution_attempt_schema,
)
from core.execution_intent import build_execution_intent


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DOC = ROOT / "docs" / "EXECUTION_ATTEMPT_SCHEMA.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


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
    )


def _payload():
    return serialize_execution_attempt_schema(_valid_attempt())


def _codes(result: dict) -> set[str]:
    return {blocker["code"] for blocker in result["blockers"]}


def test_execution_attempt_schema_module_and_boundaries_exist():
    assert (ROOT / "core" / "execution_attempt.py").exists()
    assert EXECUTION_ATTEMPT_SCHEMA_STATUS == "schema_only"
    assert EXECUTION_ATTEMPT_RUNTIME_ENABLED is False
    assert EXECUTION_ATTEMPT_FACTORY_ENABLED is False
    assert EXECUTION_ATTEMPT_STORE_WRITES_ENABLED is False
    assert EXECUTION_ATTEMPT_RESULT_STORE_ENABLED is False
    assert EXECUTION_ATTEMPT_EXECUTION_ENABLED is False
    assert EXECUTION_ATTEMPT_SCHEDULER_ENABLED is False
    assert EXECUTION_ATTEMPT_WORKER_ENABLED is False
    assert EXECUTION_ATTEMPT_QUEUE_ENABLED is False
    assert EXECUTION_ATTEMPT_MODEL_INVOCATION_ENABLED is False
    assert EXECUTION_ATTEMPT_TOOL_EXECUTION_ENABLED is False
    assert EXECUTION_ATTEMPT_MEMORY_PERSISTENCE_ENABLED is False
    assert EXECUTION_ATTEMPT_EXTERNAL_ACCESS_ENABLED is False


def test_build_serialize_and_validate_valid_schema():
    attempt = _valid_attempt()
    payload = serialize_execution_attempt_schema(attempt)
    result = validate_execution_attempt_schema(attempt)

    assert payload["attempt_id"] == "attempt_intent_agent_audit_001_0001_ab12cd34"
    assert payload["result_ref"] is None
    assert payload["error_ref"] is None
    assert result["status"] == "validated"
    assert result["verdict"] == "EXECUTION_ATTEMPT_SCHEMA_READY"
    assert result["readiness"] == "ready_for_operational_state_machine_contract"


def test_rejects_missing_and_invalid_attempt_id():
    payload = _payload()
    payload["attempt_id"] = ""
    assert "missing_attempt_id" in _codes(validate_execution_attempt_schema(payload))

    payload = _payload()
    payload["attempt_id"] = "invalid"
    assert "invalid_attempt_id_format" in _codes(validate_execution_attempt_schema(payload))


def test_rejects_attempt_id_that_does_not_match_intent_id():
    payload = _payload()
    payload["attempt_id"] = "attempt_other_intent_0001_ab12cd34"

    assert "attempt_id_intent_mismatch" in _codes(validate_execution_attempt_schema(payload))


def test_rejects_missing_or_unknown_intent_and_target_fields():
    cases = [
        ("intent_id", "", "missing_intent_id"),
        ("intent_type", "unknown", "invalid_intent_type"),
        ("target.target_type", "unknown", "invalid_target_type"),
        ("target.target_id", "", "missing_target_id"),
    ]
    for field_path, value, code in cases:
        payload = _payload()
        if "." in field_path:
            parent, child = field_path.split(".")
            payload[parent][child] = value
        else:
            payload[field_path] = value
        assert code in _codes(validate_execution_attempt_schema(payload))


def test_rejects_unknown_mode_status_lifecycle_state_and_readiness():
    cases = [
        ("mode", "execute_now", "invalid_mode"),
        ("status", "running", "invalid_status"),
        ("lifecycle_state", "completed", "invalid_lifecycle_state"),
        ("readiness", "ready_for_runtime", "invalid_readiness"),
    ]
    for field, value, code in cases:
        payload = _payload()
        payload[field] = value
        assert code in _codes(validate_execution_attempt_schema(payload))


def test_rejects_result_ref_and_error_ref():
    payload = _payload()
    payload["result_ref"] = {"result_id": "result-1"}
    assert "result_ref_not_allowed" in _codes(validate_execution_attempt_schema(payload))

    payload = _payload()
    payload["error_ref"] = {"error_id": "error-1"}
    assert "error_ref_not_allowed" in _codes(validate_execution_attempt_schema(payload))


def test_rejects_any_operational_constraint_true():
    expected = {
        "allow_runtime_execution": "runtime_execution_not_allowed",
        "allow_store_write": "store_write_not_allowed",
        "allow_result_store_write": "result_store_write_not_allowed",
        "allow_scheduler": "scheduler_not_allowed",
        "allow_worker": "worker_not_allowed",
        "allow_queue": "queue_not_allowed",
        "allow_model_invocation": "model_invocation_not_allowed",
        "allow_tool_execution": "tool_execution_not_allowed",
        "allow_memory_persistence": "memory_persistence_not_allowed",
        "allow_external_access": "external_access_not_allowed",
    }
    for field, code in expected.items():
        payload = _payload()
        payload["constraints"][field] = True
        assert code in _codes(validate_execution_attempt_schema(payload))


def test_market_catalog_target_must_remain_planned_not_active():
    payload = _payload()
    payload["intent_type"] = "market_catalog_review"
    payload["target"] = {"target_type": "market", "target_id": "market_abadia"}
    payload["metadata"] = {"market_catalog_status": "planned_not_active", "market_catalog_runtime_enabled": False}
    payload["attempt_id"] = "attempt_intent_agent_audit_001_0001_ab12cd34"
    assert validate_execution_attempt_schema(payload)["status"] == "validated"

    broken = deepcopy(payload)
    broken["metadata"]["market_catalog_status"] = "active"
    assert "market_catalog_not_planned" in _codes(validate_execution_attempt_schema(broken))


def test_business_composition_target_must_remain_non_operational():
    payload = _payload()
    payload["intent_type"] = "business_composition_review"
    payload["target"] = {"target_type": "business_composition_candidate", "target_id": "candidate-1"}
    payload["metadata"] = {"business_composition_layer_operational": False}
    assert validate_execution_attempt_schema(payload)["status"] == "validated"

    broken = deepcopy(payload)
    broken["metadata"]["business_composition_layer_operational"] = True
    assert "business_composition_layer_not_allowed" in _codes(validate_execution_attempt_schema(broken))


def test_schema_does_not_write_stores_create_lifecycle_events_or_results(tmp_path):
    forbidden_paths = [
        ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl",
        ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl",
        ROOT / "runtime" / "execution_results" / "execution_result_store.jsonl",
        tmp_path / "execution_attempt_store.jsonl",
        tmp_path / "execution_lifecycle_store.jsonl",
        tmp_path / "execution_result_store.jsonl",
    ]
    before = {path: path.exists() for path in forbidden_paths}

    validate_execution_attempt_schema(_valid_attempt())

    after = {path: path.exists() for path in forbidden_paths}
    assert before == after


def test_build_attempt_schema_from_intent_validates_intent_without_generating_id():
    intent = build_execution_intent(
        intent_id="intent_agent_audit_001",
        intent_type="agent_operation",
        source="execution_attempt_schema_test",
        target_type="agent",
        target_id="agent-1",
        mode="contract_validation",
        requested_by="system",
        readiness="ready_for_attempt_design",
        status="validated",
    )

    attempt = build_attempt_schema_from_intent(
        intent,
        attempt_id="attempt_intent_agent_audit_001_0001_ab12cd34",
        sequence=1,
    )
    payload = serialize_execution_attempt_schema(attempt)

    assert payload["intent_id"] == "intent_agent_audit_001"
    assert payload["status"] == "schema_validated"
    assert payload["readiness"] == "ready_for_state_machine_design"
    assert validate_execution_attempt_schema(payload)["status"] == "validated"


def test_build_attempt_schema_from_intent_rejects_invalid_intent():
    intent = build_execution_intent(
        intent_id="",
        intent_type="agent_operation",
        source="execution_attempt_schema_test",
        target_type="agent",
        target_id="agent-1",
        mode="contract_validation",
        requested_by="system",
    )

    try:
        build_attempt_schema_from_intent(intent, attempt_id="attempt_intent_agent_audit_001_0001_ab12cd34")
    except ValueError as exc:
        assert str(exc) == "execution_intent_not_validated"
    else:
        raise AssertionError("expected invalid intent to be rejected")


def test_market_catalog_database_remains_planned_not_active():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert catalog["metadata"]["activation_status"] == "not_evaluated"


def test_execution_attempt_schema_document_declares_readiness_and_boundaries():
    text = SCHEMA_DOC.read_text(encoding="utf-8")

    assert "EXECUTION_ATTEMPT_SCHEMA_READY" in text
    assert "ready_for_operational_state_machine_contract" in text
    assert "PROMPT 3.4 — State machine operacional contract-only" in text
    for phrase in [
        "schema-only",
        "no runtime execution",
        "no factory active",
        "no store writes",
        "no result store",
        "no lifecycle writes",
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
        assert phrase in text

