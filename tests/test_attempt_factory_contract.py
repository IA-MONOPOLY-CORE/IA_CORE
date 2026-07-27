from pathlib import Path

import pytest

import core.attempt_factory as factory
from core.attempt_factory import (
    ATTEMPT_FACTORY_CONTRACT_STATUS,
    ATTEMPT_FACTORY_ENABLED,
    ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED,
    ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED,
    ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED,
    ATTEMPT_FACTORY_MEMORY_PERSISTENCE_ENABLED,
    ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED,
    ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED,
    ATTEMPT_FACTORY_QUEUE_ENABLED,
    ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED,
    ATTEMPT_FACTORY_RESULT_STORE_ENABLED,
    ATTEMPT_FACTORY_RUNTIME_ENABLED,
    ATTEMPT_FACTORY_SCHEDULER_ENABLED,
    ATTEMPT_FACTORY_STORE_WRITES_ENABLED,
    ATTEMPT_FACTORY_TOOL_EXECUTION_ENABLED,
    ATTEMPT_FACTORY_WORKER_ENABLED,
    build_attempt_contract_from_intent,
    build_attempt_factory_decision,
    get_attempt_factory_contract,
    serialize_attempt_factory_decision,
    validate_attempt_factory_decision,
)
from core.execution_intent import build_execution_intent
from core.operational_readiness_gate import build_operational_readiness_gate_decision


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_FACTORY_CONTRACT.md"


def _intent():
    return build_execution_intent(
        intent_id="intent_factory_contract",
        intent_type="agent_operation",
        source="tests",
        target_type="agent",
        target_id="agent_demo",
        mode="contract_validation",
        requested_by="tester",
        readiness="ready_for_attempt_design",
        status="validated",
    )


def _decision():
    return build_attempt_contract_from_intent(
        _intent(),
        requested_by="tester",
        source="tests",
        idempotency_key="idem-1",
        context_refs=["ctx:1"],
        preflight_flags={"contract_only": True},
    )


def test_attempt_factory_module_exists():
    assert (ROOT / "core" / "attempt_factory.py").exists()


def test_boundary_constants_are_contract_only_and_disabled():
    assert ATTEMPT_FACTORY_CONTRACT_STATUS == "contract_only"
    assert ATTEMPT_FACTORY_ENABLED is False

    for value in [
        ATTEMPT_FACTORY_RUNTIME_ENABLED,
        ATTEMPT_FACTORY_STORE_WRITES_ENABLED,
        ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED,
        ATTEMPT_FACTORY_RESULT_STORE_ENABLED,
        ATTEMPT_FACTORY_HISTORY_WRITES_ENABLED,
        ATTEMPT_FACTORY_READ_MODEL_WRITES_ENABLED,
        ATTEMPT_FACTORY_PROJECTION_WRITES_ENABLED,
        ATTEMPT_FACTORY_SCHEDULER_ENABLED,
        ATTEMPT_FACTORY_WORKER_ENABLED,
        ATTEMPT_FACTORY_QUEUE_ENABLED,
        ATTEMPT_FACTORY_MODEL_INVOCATION_ENABLED,
        ATTEMPT_FACTORY_TOOL_EXECUTION_ENABLED,
        ATTEMPT_FACTORY_MEMORY_PERSISTENCE_ENABLED,
        ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED,
    ]:
        assert value is False


def test_can_build_serialize_and_validate_contractual_decision():
    decision = _decision()
    payload = serialize_attempt_factory_decision(decision)
    validation = validate_attempt_factory_decision(decision)

    assert payload["decision"] == "created_contractually"
    assert payload["readiness"] == "ready_for_attempt_factory_e2e_checkpoint"
    assert payload["initial_state"] == "schema_validated"
    assert payload["attempt"] is not None
    assert validation["status"] == "validated"
    assert validation["verdict"] == "ATTEMPT_FACTORY_CONTRACT_READY"


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("factory_id", "", "missing_factory_id"),
        ("status", "unknown", "invalid_status"),
        ("decision", "unknown", "invalid_decision"),
        ("readiness", "unknown", "invalid_readiness"),
        ("initial_state", "unknown", "invalid_initial_state"),
        ("initial_state", "queued", "invalid_initial_state"),
        ("initial_state", "running", "invalid_initial_state"),
        ("readiness", "ready_for_runtime", "invalid_readiness"),
    ],
)
def test_rejects_invalid_top_level_fields(field, value, code):
    payload = serialize_attempt_factory_decision(_decision())
    payload[field] = value

    validation = validate_attempt_factory_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("runtime_enabled", True, "runtime_enabled_not_allowed"),
        ("operations_enabled", True, "operations_enabled_not_allowed"),
        ("attempt_factory_enabled", True, "attempt_factory_enabled_not_allowed"),
        ("gate_open", True, "gate_open_not_allowed"),
    ],
)
def test_rejects_forbidden_runtime_flags(field, value, code):
    payload = serialize_attempt_factory_decision(_decision())
    payload["metadata"][field] = value

    validation = validate_attempt_factory_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("blocking_reasons", {}, "invalid_blocking_reasons"),
        ("warnings", {}, "invalid_warnings"),
        ("lineage", [], "invalid_lineage"),
        ("metadata", [], "invalid_metadata"),
    ],
)
def test_rejects_invalid_container_types(field, value, code):
    payload = serialize_attempt_factory_decision(_decision())
    payload[field] = value

    validation = validate_attempt_factory_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == code for blocker in validation["blockers"])


def test_rejects_any_dangerous_capability_enabled():
    for name in get_attempt_factory_contract()["boundaries"]:
        payload = serialize_attempt_factory_decision(_decision())
        payload["metadata"][name] = True
        validation = validate_attempt_factory_decision(payload)

        assert validation["status"] == "blocked", name


def test_rejects_market_catalog_active():
    payload = serialize_attempt_factory_decision(_decision())
    payload["metadata"]["market_catalog_status"] = "active"

    validation = validate_attempt_factory_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "market_catalog_active_not_allowed" for blocker in validation["blockers"])


def test_rejects_business_composition_active():
    payload = serialize_attempt_factory_decision(_decision())
    payload["metadata"]["business_composition_enabled"] = True

    validation = validate_attempt_factory_decision(payload)

    assert validation["status"] == "blocked"
    assert any(blocker["code"] == "business_composition_enabled_not_allowed" for blocker in validation["blockers"])


def test_invalid_intent_returns_invalid_decision():
    invalid_intent = build_execution_intent(
        intent_id="intent_factory_invalid",
        intent_type="agent_operation",
        source="tests",
        target_type="agent",
        target_id="agent_demo",
        mode="contract_validation",
        requested_by="tester",
        readiness="ready_for_runtime",
        status="validated",
    )

    decision = build_attempt_contract_from_intent(invalid_intent)
    validation = validate_attempt_factory_decision(decision)

    assert decision.decision == "invalid"
    assert validation["status"] == "blocked"


def test_gate_blocked_returns_blocked_decision():
    gate = build_operational_readiness_gate_decision(decision="blocked", readiness="blocked")

    decision = build_attempt_contract_from_intent(_intent(), gate_decision=gate)

    assert decision.decision == "blocked"
    assert decision.attempt is None
    assert decision.blocking_reasons


def test_build_attempt_contract_from_intent_does_not_persist_or_write(tmp_path):
    watched = [
        ROOT / "core" / "execution_attempt_store.py",
        ROOT / "core" / "execution_lifecycle.py",
        ROOT / "core" / "execution_result_store.py",
        ROOT / "core" / "result_store.py",
        ROOT / "core" / "history_writer.py",
        ROOT / "core" / "read_model_writer.py",
        ROOT / "core" / "scheduler.py",
        ROOT / "core" / "worker.py",
        ROOT / "core" / "queue.py",
    ]
    before = {path: (path.exists(), path.stat().st_mtime_ns if path.exists() else None) for path in watched}

    decision = build_attempt_contract_from_intent(_intent(), idempotency_key="no-writes")

    after = {path: (path.exists(), path.stat().st_mtime_ns if path.exists() else None) for path in watched}
    assert decision.decision == "created_contractually"
    assert after == before


def test_no_runtime_or_external_public_api_is_exposed():
    forbidden = {
        "persist_attempt",
        "write_attempt_store",
        "write_lifecycle",
        "write_result_store",
        "write_history",
        "write_read_model",
        "create_scheduler",
        "create_worker",
        "create_queue",
        "invoke_model",
        "invoke_tool",
        "external_access",
        "execute_runtime",
    }

    assert forbidden.isdisjoint({name for name in dir(factory) if not name.startswith("_")})


def test_safe_initial_state_can_be_draft_or_schema_validated():
    schema_validated = build_attempt_contract_from_intent(_intent(), initial_state="schema_validated")
    draft = build_attempt_contract_from_intent(_intent(), initial_state="draft")

    assert schema_validated.initial_state == "schema_validated"
    assert draft.initial_state == "draft"
    assert validate_attempt_factory_decision(schema_validated)["status"] == "validated"
    assert validate_attempt_factory_decision(draft)["status"] == "validated"


def test_manual_blocked_decision_is_valid_contractual_output():
    decision = build_attempt_factory_decision(
        factory_id="attempt_factory_contract",
        status="blocked",
        decision="blocked",
        readiness="blocked",
        attempt_id=None,
        initial_state="blocked",
        execution_intent_ref="intent_factory_contract",
        blocking_reasons=[{"code": "blocked", "message": "blocked", "severity": "error"}],
        lineage={"intent_id": "intent_factory_contract"},
    )

    assert validate_attempt_factory_decision(decision)["status"] == "validated"


def test_contract_document_contains_required_markers():
    text = DOC.read_text(encoding="utf-8")

    for phrase in [
        "ATTEMPT_FACTORY_CONTRACT_READY",
        "ready_for_attempt_factory_e2e_checkpoint",
        "PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract",
        "contract-only",
        "non-operational",
        "in-memory only",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text
