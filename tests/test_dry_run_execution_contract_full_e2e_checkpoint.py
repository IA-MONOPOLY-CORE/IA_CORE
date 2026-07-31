import json
from pathlib import Path

import pytest

import core.dry_run_execution_contract as contract
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_HERMES_ENABLED,
    RUNTIME_HOME_ASSISTANT_ENABLED,
    RUNTIME_MEMORY_PERSISTENCE_ENABLED,
    RUNTIME_MODEL_INVOCATION_ENABLED,
    RUNTIME_N8N_ENABLED,
    RUNTIME_NETWORK_ENABLED,
    RUNTIME_OUTPUT_DELIVERY_ENABLED,
    RUNTIME_QUEUE_ENABLED,
    RUNTIME_RUNNER_ENABLED,
    RUNTIME_SCHEDULER_ENABLED,
    RUNTIME_SECRET_ACCESS_ENABLED,
    RUNTIME_STORES_ENABLED,
    RUNTIME_TOOL_EXECUTION_ENABLED,
    RUNTIME_UI_TARS_ENABLED,
    RUNTIME_WORKER_ENABLED,
    RUNTIME_WRITES_ENABLED,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "DRY_RUN_EXECUTION_CONTRACT_FULL_E2E_CHECKPOINT.md"


def _request() -> contract.DryRunExecutionRequest:
    return contract.create_dry_run_execution_request(
        request_id="dry_run_e2e_req",
        intent_id="intent_e2e",
        attempt_id="attempt_e2e",
        requested_by="e2e_test",
        reason="validate dry-run contract full e2e",
        simulation_scope=("request", "policy", "projection"),
        metadata={"source": "full_e2e", "safe": {"kind": "contract_only"}},
    )


def test_dry_run_execution_contract_full_e2e_document_exists_and_declares_status():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Dry-run Execution Contract Full E2E Checkpoint",
        "DRY_RUN_EXECUTION_CONTRACT_FULL_E2E_PASSED",
        "DRY_RUN_EXECUTION_CONTRACT_CHAIN_READY",
        "ready_for_observability_audit_trail_planning",
        "PROMPT 3.37 — Auditoría de observability/audit trail post-security",
        "1. Purpose",
        "2. Scope",
        "3. E2E flow",
        "4. Happy path validation",
        "5. Blocked metadata validation",
        "6. Forbidden operational states validation",
        "7. Serialization validation",
        "8. Determinism validation",
        "9. No side effects validation",
        "10. Runtime Activation Gate validation",
        "11. Forbidden modules validation",
        "12. Non-operational guarantees",
        "13. Result",
        "14. Next prompt",
    ]:
        assert phrase in text


def test_happy_path_request_decision_result_serialization_e2e():
    request = _request()
    decision = contract.evaluate_dry_run_execution_request(request)
    result = contract.build_dry_run_execution_contract_result(request)
    serialized = contract.serialize_dry_run_execution_contract_result(result)

    assert request.request_id
    assert request.intent_id
    assert request.requested_by
    assert request.reason
    assert request.simulation_scope
    assert decision.no_activation_confirmed is True
    assert decision.allowed is True
    assert decision.conceptual_state in contract.DRY_RUN_ALLOWED_CONCEPTUAL_STATES
    assert decision.conceptual_state not in contract.DRY_RUN_FORBIDDEN_OPERATIONAL_STATES
    assert "allowed_true_is_representability_only" in decision.warnings
    assert result.contract_status == "DRY_RUN_EXECUTION_CONTRACT_READY"
    assert result.readiness == "ready_for_dry_run_execution_contract_e2e"
    assert result.next_step == "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract"
    assert isinstance(serialized, dict)
    json.dumps(serialized, sort_keys=True)


def test_all_activation_flags_remain_false_e2e():
    result = contract.build_dry_run_execution_contract_result(_request())
    for flag in [
        result.runtime_activation_enabled,
        result.runtime_execution_enabled,
        result.dry_run_execution_enabled,
        result.tool_execution_enabled,
        result.model_invocation_enabled,
        result.context_injection_enabled,
        result.output_delivery_enabled,
        result.writes_enabled,
        result.stores_enabled,
        result.external_access_enabled,
    ]:
        assert flag is False


def test_empty_scope_is_blocked_e2e():
    with pytest.raises(ValueError, match="simulation_scope"):
        contract.create_dry_run_execution_request(
            request_id="dry_run_empty_scope",
            intent_id="intent_e2e",
            requested_by="e2e_test",
            reason="blocked",
            simulation_scope=(),
            metadata={},
        )


@pytest.mark.parametrize("key", ["secret", "token", "api_key", "password", "credential", "env", "private_key"])
def test_suspicious_metadata_is_blocked_e2e(key):
    with pytest.raises(ValueError):
        contract.create_dry_run_execution_request(
            request_id=f"dry_run_{key}",
            intent_id="intent_e2e",
            requested_by="e2e_test",
            reason="blocked metadata",
            simulation_scope=("request",),
            metadata={key: "blocked"},
        )


@pytest.mark.parametrize("key", ["raw_output", "tool_payload", "model_prompt", "context_payload", "output_payload"])
def test_raw_payload_metadata_is_blocked_e2e(key):
    with pytest.raises(ValueError):
        contract.create_dry_run_execution_request(
            request_id=f"dry_run_{key}",
            intent_id="intent_e2e",
            requested_by="e2e_test",
            reason="blocked payload",
            simulation_scope=("request",),
            metadata={key: "blocked"},
        )


@pytest.mark.parametrize("key", ["filesystem_path", "external_url", "provider_client", "runtime_executor"])
def test_operational_metadata_is_blocked_e2e(key):
    with pytest.raises(ValueError):
        contract.create_dry_run_execution_request(
            request_id=f"dry_run_{key}",
            intent_id="intent_e2e",
            requested_by="e2e_test",
            reason="blocked operational metadata",
            simulation_scope=("request",),
            metadata={key: "blocked"},
        )


@pytest.mark.parametrize(
    "state",
    ["queued", "running", "succeeded", "failed", "runtime_open", "runtime_active", "execution_enabled", "dry_run_execution_enabled", "operations_enabled", "gate_open"],
)
def test_forbidden_operational_states_are_not_allowed_e2e(state):
    decision = contract.evaluate_dry_run_execution_request(_request(), conceptual_state=state)
    assert decision.allowed is False
    assert decision.conceptual_state == "dry_run_blocked"
    assert decision.blocked_reasons


def test_serialization_safety_e2e():
    serialized = contract.serialize_dry_run_execution_contract_result(
        contract.build_dry_run_execution_contract_result(_request())
    )
    metadata_json = json.dumps(serialized["request"]["metadata"], sort_keys=True).lower()
    for forbidden in ["raw_output", "secret", "tool_payload", "model_prompt", "context_payload", "output_payload"]:
        assert forbidden not in metadata_json


def test_security_baseline_present_e2e():
    decision = contract.evaluate_dry_run_execution_request(_request())
    assert "Security Layer" in decision.security_baseline
    assert "Runtime Activation Gate" in decision.security_baseline


def test_repeated_deterministic_evaluation_e2e():
    request = _request()
    first_decision = contract.evaluate_dry_run_execution_request(request)
    second_decision = contract.evaluate_dry_run_execution_request(request)
    assert first_decision == second_decision

    first_payload = contract.serialize_dry_run_execution_contract_result(contract.build_dry_run_execution_contract_result(request))
    second_payload = contract.serialize_dry_run_execution_contract_result(contract.build_dry_run_execution_contract_result(request))
    assert first_payload == second_payload


def test_no_side_effects_e2e():
    before = {
        path: path.stat().st_mtime_ns
        for path in [
            ROOT / "core" / "dry_run_store.py",
            ROOT / "core" / "attempt_store.py",
            ROOT / "core" / "lifecycle_store.py",
        ]
        if path.exists()
    }
    contract.serialize_dry_run_execution_contract_result(contract.build_dry_run_execution_contract_result(_request()))
    after = {path: path.stat().st_mtime_ns for path in before}
    assert before == after


def test_no_forbidden_operational_modules_exist_e2e():
    for path in [
        "core/dry_run_executor.py",
        "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py",
        "core/dry_run_scheduler.py",
        "core/dry_run_worker.py",
        "core/dry_run_queue.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/orchestrator.py",
        "core/executor.py",
        "core/dispatcher.py",
        "core/background_jobs.py",
        "core/autonomous_loop.py",
        "core/execution_planner.py",
        "core/execution_dispatcher.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/context_injector.py",
        "core/prompt_assembler.py",
        "core/retrieval_engine.py",
        "core/rag_engine.py",
        "core/output_writer.py",
        "core/output_publisher.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists(), path


def test_runtime_activation_gate_and_contract_flags_stay_closed_e2e():
    runtime_flags = [
        RUNTIME_ACTIVATION_ENABLED,
        RUNTIME_EXECUTION_ENABLED,
        RUNTIME_RUNNER_ENABLED,
        RUNTIME_SCHEDULER_ENABLED,
        RUNTIME_WORKER_ENABLED,
        RUNTIME_QUEUE_ENABLED,
        RUNTIME_TOOL_EXECUTION_ENABLED,
        RUNTIME_MODEL_INVOCATION_ENABLED,
        RUNTIME_CONTEXT_INJECTION_ENABLED,
        RUNTIME_OUTPUT_DELIVERY_ENABLED,
        RUNTIME_WRITES_ENABLED,
        RUNTIME_STORES_ENABLED,
        RUNTIME_MEMORY_PERSISTENCE_ENABLED,
        RUNTIME_NETWORK_ENABLED,
        RUNTIME_API_ENABLED,
        RUNTIME_SECRET_ACCESS_ENABLED,
        RUNTIME_UI_TARS_ENABLED,
        RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED,
        RUNTIME_HOME_ASSISTANT_ENABLED,
    ]
    contract_flags = [
        contract.DRY_RUN_EXECUTION_OPERATIONAL,
        contract.DRY_RUN_EXECUTION_ENABLED,
        contract.DRY_RUN_EXECUTOR_ENABLED,
        contract.DRY_RUN_RUNNER_ENABLED,
        contract.DRY_RUN_DISPATCHER_ENABLED,
        contract.DRY_RUN_SCHEDULER_ENABLED,
        contract.DRY_RUN_WORKER_ENABLED,
        contract.DRY_RUN_QUEUE_ENABLED,
        contract.DRY_RUN_TOOL_EXECUTION_ENABLED,
        contract.DRY_RUN_MODEL_INVOCATION_ENABLED,
        contract.DRY_RUN_CONTEXT_INJECTION_ENABLED,
        contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED,
        contract.DRY_RUN_OUTPUT_PUBLISHING_ENABLED,
        contract.DRY_RUN_WRITES_ENABLED,
        contract.DRY_RUN_STORES_ENABLED,
        contract.DRY_RUN_MEMORY_PERSISTENCE_ENABLED,
        contract.DRY_RUN_NETWORK_ENABLED,
        contract.DRY_RUN_API_ENABLED,
        contract.DRY_RUN_BROWSER_ENABLED,
        contract.DRY_RUN_FILESYSTEM_ENABLED,
        contract.DRY_RUN_ENV_ACCESS_ENABLED,
        contract.DRY_RUN_SECRET_ACCESS_ENABLED,
        contract.DRY_RUN_UI_TARS_ENABLED,
        contract.DRY_RUN_HERMES_ENABLED,
        contract.DRY_RUN_N8N_ENABLED,
        contract.DRY_RUN_HOME_ASSISTANT_ENABLED,
    ]
    assert runtime_flags == [False] * len(runtime_flags)
    assert contract_flags == [False] * len(contract_flags)


def test_document_contains_explicit_prohibitions_e2e():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "dry-run execution activation",
        "runtime activation",
        "runtime execution",
        "dry-run executor",
        "dry-run runner",
        "dry-run dispatcher",
        "dry-run scheduler",
        "dry-run worker",
        "dry-run queue",
        "tool execution",
        "model invocation",
        "context injection",
        "output delivery",
        "writes reales",
        "stores operativos",
        "memory persistence",
        "API calls",
        "network",
        "browser",
        "real filesystem reads",
        "env access",
        "secret access",
        "UI-TARS runtime",
        "Hermes runtime",
        "n8n real workflows",
        "Home Assistant real actions",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS integration",
    ]:
        assert phrase in text
