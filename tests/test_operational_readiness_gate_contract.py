from pathlib import Path

import pytest

from core.operational_readiness_gate import (
    OPERATIONAL_READINESS_GATE_CONTRACT_STATUS,
    OPERATIONAL_READINESS_GATE_ENABLED,
    build_operational_readiness_gate_decision,
    evaluate_operational_readiness_contracts,
    get_operational_readiness_gate_contract,
    serialize_operational_readiness_gate_decision,
    validate_operational_readiness_gate_decision,
)
import core.operational_readiness_gate as gate


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "OPERATIONAL_READINESS_GATE_CONTRACT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _codes(result):
    return {blocker["code"] for blocker in result["blockers"]}


def _valid_payload():
    return serialize_operational_readiness_gate_decision(build_operational_readiness_gate_decision())


def test_gate_module_exists_and_boundary_constants_are_declared():
    assert (ROOT / "core" / "operational_readiness_gate.py").exists()
    assert OPERATIONAL_READINESS_GATE_CONTRACT_STATUS == "contract_only"
    assert OPERATIONAL_READINESS_GATE_ENABLED is False


def test_gate_boundary_flags_are_false():
    for name in [
        "OPERATIONAL_READINESS_GATE_RUNTIME_ENABLED",
        "OPERATIONAL_READINESS_GATE_ATTEMPT_FACTORY_ENABLED",
        "OPERATIONAL_READINESS_GATE_ATTEMPT_STORE_WRITES_ENABLED",
        "OPERATIONAL_READINESS_GATE_LIFECYCLE_WRITES_ENABLED",
        "OPERATIONAL_READINESS_GATE_RESULT_STORE_ENABLED",
        "OPERATIONAL_READINESS_GATE_RESULT_STORE_WRITES_ENABLED",
        "OPERATIONAL_READINESS_GATE_HISTORY_WRITES_ENABLED",
        "OPERATIONAL_READINESS_GATE_READ_MODEL_WRITES_ENABLED",
        "OPERATIONAL_READINESS_GATE_PROJECTION_WRITES_ENABLED",
        "OPERATIONAL_READINESS_GATE_SCHEDULER_ENABLED",
        "OPERATIONAL_READINESS_GATE_WORKER_ENABLED",
        "OPERATIONAL_READINESS_GATE_QUEUE_ENABLED",
        "OPERATIONAL_READINESS_GATE_MODEL_INVOCATION_ENABLED",
        "OPERATIONAL_READINESS_GATE_TOOL_EXECUTION_ENABLED",
        "OPERATIONAL_READINESS_GATE_MEMORY_PERSISTENCE_ENABLED",
        "OPERATIONAL_READINESS_GATE_EXTERNAL_ACCESS_ENABLED",
    ]:
        assert getattr(gate, name) is False


def test_can_build_serialize_and_validate_decision():
    decision = build_operational_readiness_gate_decision()
    payload = serialize_operational_readiness_gate_decision(decision)
    validation = validate_operational_readiness_gate_decision(payload)

    assert payload["decision"] == "ready_for_next_contract"
    assert payload["readiness"] == "ready_for_pre_operational_e2e_checkpoint"
    assert validation["status"] == "validated"
    assert validation["verdict"] == "OPERATIONAL_READINESS_GATE_CONTRACT_READY"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("gate_id", "", "missing_gate_id"),
        ("status", "unknown", "invalid_status"),
        ("decision", "unknown", "invalid_decision"),
        ("readiness", "unknown", "invalid_readiness"),
        ("checked_at", "", "missing_checked_at"),
        ("contracts", [], "invalid_contracts"),
        ("disabled_capabilities", [], "invalid_disabled_capabilities"),
        ("blocking_reasons", {}, "invalid_blocking_reasons"),
        ("warnings", {}, "invalid_warnings"),
        ("metadata", [], "invalid_metadata"),
        ("decision", "ready_for_runtime", "invalid_decision"),
    ],
)
def test_validate_rejects_invalid_decision_shapes(field, value, code):
    payload = _valid_payload()
    payload[field] = value

    result = validate_operational_readiness_gate_decision(payload)

    assert result["status"] == "blocked"
    assert code in _codes(result)


@pytest.mark.parametrize(
    ("path", "value", "code"),
    [
        (("disabled_capabilities", "runtime_execution"), False, "runtime_execution_not_disabled"),
        (("metadata", "gate_open"), True, "gate_open_not_allowed"),
        (("metadata", "operations_enabled"), True, "operations_enabled_not_allowed"),
        (("metadata", "runtime_enabled"), True, "runtime_enabled_not_allowed"),
        (("metadata", "market_catalog_active"), True, "market_catalog_active_not_allowed"),
        (("metadata", "business_composition_active"), True, "business_composition_active_not_allowed"),
        (("metadata", "market_catalog_status"), "active", "market_catalog_active_not_allowed"),
        (("metadata", "business_composition_layer_status"), "operational", "business_composition_active_not_allowed"),
    ],
)
def test_validate_rejects_operational_activation(path, value, code):
    payload = _valid_payload()
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value

    result = validate_operational_readiness_gate_decision(payload)

    assert result["status"] == "blocked"
    assert code in _codes(result)


def test_evaluate_operational_readiness_contracts_returns_safe_decision():
    decision = evaluate_operational_readiness_contracts()
    payload = serialize_operational_readiness_gate_decision(decision)
    validation = validate_operational_readiness_gate_decision(payload)

    assert payload["decision"] == "ready_for_next_contract"
    assert payload["readiness"] == "ready_for_pre_operational_e2e_checkpoint"
    assert payload["metadata"]["system_ready_for_runtime"] is False
    assert payload["metadata"]["system_ready_for_operational_gate_opening"] is False
    assert validation["status"] == "validated"


def test_contract_exposes_required_contracts_and_disabled_capabilities():
    contract = get_operational_readiness_gate_contract()

    for name in [
        "execution_intent",
        "execution_attempt_schema",
        "execution_attempt_state_machine",
        "execution_result_contract",
        "execution_result_projection",
        "long_suite_validation_policy",
    ]:
        assert name in contract["required_contracts"]
    for capability in [
        "runtime_execution",
        "attempt_factory",
        "attempt_store_writes",
        "lifecycle_writes",
        "result_store_writes",
        "history_writes",
        "read_model_writes",
        "projection_writes",
        "scheduler",
        "worker",
        "queue",
        "model_invocation",
        "tool_execution",
        "memory_persistence",
        "external_access",
    ]:
        assert capability in contract["required_disabled_capabilities"]


def test_gate_does_not_write_or_create_runtime_artifacts(tmp_path):
    before = {path: path.exists() for path in [
        ROOT / "runtime",
        ROOT / "core" / "execution_result_store.py",
        ROOT / "core" / "runtime_runner.py",
        ROOT / "core" / "attempt_factory.py",
        ROOT / "core" / "history_writer.py",
        ROOT / "core" / "read_model_writer.py",
    ]}

    decision = evaluate_operational_readiness_contracts()
    validate_operational_readiness_gate_decision(decision)

    after = {path: path.exists() for path in before}
    assert after == before


def test_gate_does_not_create_results_lifecycle_or_persisted_projections():
    forbidden = {
        "create_lifecycle_event",
        "create_execution_result",
        "persist_projection",
        "write_store",
        "execute_runtime",
        "invoke_model",
        "invoke_tool",
        "external_access",
    }
    public_names = {name for name in dir(gate) if not name.startswith("_")}

    assert forbidden.isdisjoint(public_names)


def test_market_catalog_and_business_composition_remain_inactive():
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")
    contract = get_operational_readiness_gate_contract()

    assert "planned_not_active" in catalog_text
    assert contract["boundaries"]["market_catalog_runtime_enabled"] is False
    assert contract["boundaries"]["business_composition_layer_runtime_enabled"] is False


def test_contract_document_contains_required_markers():
    text = DOC.read_text(encoding="utf-8")

    for phrase in [
        "OPERATIONAL_READINESS_GATE_CONTRACT_READY",
        "ready_for_pre_operational_e2e_checkpoint",
        "PROMPT 3.11 — Checkpoint E2E pre-operational",
        "contract-only",
        "read-only",
        "no operational gate enabled",
        "no runtime execution",
        "no attempt factory",
        "no store writes",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text
