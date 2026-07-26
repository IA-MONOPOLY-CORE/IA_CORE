import json
from copy import deepcopy
from pathlib import Path

from core.execution_attempt import build_execution_attempt_schema, serialize_execution_attempt_schema
from core.execution_attempt_state_machine import (
    EXECUTION_ATTEMPT_STATE_MACHINE_EXECUTION_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_EXTERNAL_ACCESS_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_LIFECYCLE_WRITES_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_MEMORY_PERSISTENCE_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_MODEL_INVOCATION_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_QUEUE_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_RESULT_STORE_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_RUNTIME_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_SCHEDULER_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_STATUS,
    EXECUTION_ATTEMPT_STATE_MACHINE_STORE_WRITES_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_TOOL_EXECUTION_ENABLED,
    EXECUTION_ATTEMPT_STATE_MACHINE_WORKER_ENABLED,
    get_allowed_execution_attempt_states,
    get_allowed_execution_attempt_transitions,
    get_future_reserved_execution_attempt_states,
    get_terminal_execution_attempt_states,
    is_terminal_execution_attempt_state,
    is_valid_execution_attempt_state,
    is_valid_execution_attempt_transition,
    serialize_execution_attempt_state_machine_contract,
    validate_execution_attempt_state_machine_transition,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _attempt(state: str = "draft"):
    schema_status = state if state in {"draft", "schema_validated", "blocked"} else "schema_validated"
    lifecycle_state = "blocked" if state == "blocked" else "preflight_only" if state == "preflight_ready" else "not_started"
    return build_execution_attempt_schema(
        attempt_id="attempt_intent_agent_audit_001_0001_ab12cd34",
        intent_id="intent_agent_audit_001",
        intent_type="agent_operation",
        target_type="agent",
        target_id="agent-1",
        mode="contract_validation",
        requested_by="system",
        status=schema_status,
        lifecycle_state=lifecycle_state,
        readiness="ready_for_state_machine_design",
        metadata={"state_machine_state": state},
    )


def _codes(result: dict) -> set[str]:
    return {blocker["code"] for blocker in result["blockers"]}


def test_state_machine_module_and_boundary_flags_exist():
    assert (ROOT / "core" / "execution_attempt_state_machine.py").exists()
    assert EXECUTION_ATTEMPT_STATE_MACHINE_STATUS == "contract_only"
    assert EXECUTION_ATTEMPT_STATE_MACHINE_RUNTIME_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_STORE_WRITES_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_LIFECYCLE_WRITES_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_RESULT_STORE_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_EXECUTION_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_SCHEDULER_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_WORKER_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_QUEUE_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_MODEL_INVOCATION_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_TOOL_EXECUTION_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_MEMORY_PERSISTENCE_ENABLED is False
    assert EXECUTION_ATTEMPT_STATE_MACHINE_EXTERNAL_ACCESS_ENABLED is False


def test_allowed_future_and_terminal_states_are_declared():
    assert set(get_allowed_execution_attempt_states()) == {"draft", "schema_validated", "preflight_ready", "blocked", "cancelled"}
    assert set(get_future_reserved_execution_attempt_states()) == {
        "queued",
        "running",
        "succeeded",
        "failed",
        "partially_succeeded",
        "retrying",
        "expired",
    }
    assert set(get_terminal_execution_attempt_states()) == {"blocked", "cancelled"}
    assert is_terminal_execution_attempt_state("blocked") is True
    assert is_terminal_execution_attempt_state("cancelled") is True


def test_allowed_transitions_are_valid():
    assert is_valid_execution_attempt_transition("draft", "schema_validated") is True
    assert is_valid_execution_attempt_transition("schema_validated", "preflight_ready") is True
    assert is_valid_execution_attempt_transition("draft", "blocked") is True
    assert is_valid_execution_attempt_transition("preflight_ready", "cancelled") is True
    transitions = get_allowed_execution_attempt_transitions()
    assert transitions["draft"] == ("schema_validated", "blocked", "cancelled")


def test_future_runtime_transitions_are_rejected():
    for from_state, to_state in [
        ("draft", "running"),
        ("schema_validated", "running"),
        ("preflight_ready", "queued"),
        ("preflight_ready", "succeeded"),
    ]:
        assert is_valid_execution_attempt_transition(from_state, to_state) is False
        result = validate_execution_attempt_state_machine_transition(_attempt(from_state), to_state)
        assert result["status"] == "blocked"


def test_transitions_from_terminal_states_are_rejected():
    for from_state in ["blocked", "cancelled"]:
        result = validate_execution_attempt_state_machine_transition(_attempt(from_state), "draft")
        assert result["status"] == "blocked"
        assert "terminal_state_transition_not_allowed" in _codes(result)


def test_unknown_states_are_rejected():
    assert is_valid_execution_attempt_state("unknown") is False

    payload = serialize_execution_attempt_schema(_attempt("draft"))
    payload["metadata"]["state_machine_state"] = "unknown"
    result = validate_execution_attempt_state_machine_transition(payload, "schema_validated")
    assert "from_state_invalid" in _codes(result)

    result = validate_execution_attempt_state_machine_transition(_attempt("draft"), "unknown")
    assert "to_state_invalid" in _codes(result)


def test_transition_validation_does_not_mutate_attempt_or_refs():
    attempt = serialize_execution_attempt_schema(_attempt("draft"))
    before = deepcopy(attempt)
    result = validate_execution_attempt_state_machine_transition(attempt, "schema_validated")

    assert result["status"] == "validated"
    assert attempt == before
    assert result["mutated"] is False
    assert attempt["result_ref"] is None
    assert attempt["error_ref"] is None


def test_schema_is_validated_first():
    payload = serialize_execution_attempt_schema(_attempt("draft"))
    payload["attempt_id"] = ""

    result = validate_execution_attempt_state_machine_transition(payload, "schema_validated")

    assert result["status"] == "blocked"
    assert "missing_attempt_id" in _codes(result)


def test_state_machine_does_not_write_stores_or_lifecycle_events(tmp_path):
    paths = [
        ROOT / "runtime" / "execution_attempts" / "execution_attempt_store.jsonl",
        ROOT / "runtime" / "execution_lifecycle" / "execution_lifecycle_store.jsonl",
        ROOT / "runtime" / "execution_results" / "execution_result_store.jsonl",
        tmp_path / "execution_attempt_store.jsonl",
        tmp_path / "execution_lifecycle_store.jsonl",
        tmp_path / "execution_result_store.jsonl",
    ]
    before = {path: path.exists() for path in paths}
    validate_execution_attempt_state_machine_transition(_attempt("draft"), "schema_validated")
    after = {path: path.exists() for path in paths}

    assert before == after


def test_state_machine_contract_serialization_keeps_boundaries_disabled():
    contract = serialize_execution_attempt_state_machine_contract()
    boundaries = contract["boundaries"]

    assert contract["verdict"] == "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY"
    assert contract["readiness"] == "ready_for_result_store_boundary_audit"
    for value in boundaries.values():
        assert value is False


def test_market_catalog_and_business_composition_remain_non_operational():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert catalog["metadata"]["activation_status"] == "not_evaluated"


def test_state_machine_document_declares_readiness_and_boundaries():
    text = DOC.read_text(encoding="utf-8")

    assert "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY" in text
    assert "ready_for_result_store_boundary_audit" in text
    assert "PROMPT 3.5 — Auditoría de result store boundary" in text
    for phrase in [
        "contract-only",
        "read-only",
        "no runtime execution",
        "no factory active",
        "no store writes",
        "no lifecycle writes",
        "no result store",
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
