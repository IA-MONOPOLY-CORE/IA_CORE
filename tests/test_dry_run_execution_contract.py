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
DOC = ROOT / "docs" / "DRY_RUN_EXECUTION_CONTRACT.md"


def _valid_request() -> contract.DryRunExecutionRequest:
    return contract.create_dry_run_execution_request(
        request_id="dry_run_req_1",
        intent_id="intent_1",
        attempt_id=None,
        requested_by="tester",
        reason="contract validation",
        simulation_scope=("intent", "policy", "result_projection"),
        metadata={"source": "unit_test", "nested": {"safe": True}},
    )


def test_dry_run_execution_contract_constants_are_non_operational():
    assert contract.DRY_RUN_EXECUTION_CONTRACT_READY is True
    for flag in [
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
        contract.DRY_RUN_WRITES_ENABLED,
        contract.DRY_RUN_STORES_ENABLED,
        contract.DRY_RUN_MEMORY_PERSISTENCE_ENABLED,
        contract.DRY_RUN_NETWORK_ENABLED,
        contract.DRY_RUN_API_ENABLED,
        contract.DRY_RUN_SECRET_ACCESS_ENABLED,
        contract.DRY_RUN_UI_TARS_ENABLED,
        contract.DRY_RUN_HERMES_ENABLED,
        contract.DRY_RUN_N8N_ENABLED,
        contract.DRY_RUN_HOME_ASSISTANT_ENABLED,
    ]:
        assert flag is False


def test_dry_run_execution_contract_declares_states():
    assert set(contract.DRY_RUN_ALLOWED_CONCEPTUAL_STATES) == {
        "dry_run_draft",
        "dry_run_planned",
        "dry_run_preflight_validated",
        "dry_run_policy_checked",
        "dry_run_blocked",
        "dry_run_simulated",
        "dry_run_result_projected",
        "dry_run_cancelled",
        "dry_run_invalid",
    }
    for state in [
        "queued",
        "running",
        "succeeded",
        "failed",
        "runtime_open",
        "runtime_active",
        "execution_enabled",
        "dry_run_execution_enabled",
        "operations_enabled",
        "gate_open",
    ]:
        assert state in contract.DRY_RUN_FORBIDDEN_OPERATIONAL_STATES


def test_create_valid_dry_run_execution_request_is_serializable():
    request = _valid_request()
    assert isinstance(request, contract.DryRunExecutionRequest)
    payload = {
        "request_id": request.request_id,
        "intent_id": request.intent_id,
        "attempt_id": request.attempt_id,
        "requested_by": request.requested_by,
        "reason": request.reason,
        "simulation_scope": list(request.simulation_scope),
        "metadata": dict(request.metadata),
    }
    json.dumps(payload, sort_keys=True)


@pytest.mark.parametrize(
    "field,kwargs",
    [
        ("request_id", {"request_id": ""}),
        ("intent_id", {"intent_id": ""}),
        ("requested_by", {"requested_by": ""}),
        ("reason", {"reason": ""}),
        ("simulation_scope", {"simulation_scope": ()}),
    ],
)
def test_create_dry_run_execution_request_rejects_empty_required_fields(field, kwargs):
    data = {
        "request_id": "dry_run_req_1",
        "intent_id": "intent_1",
        "requested_by": "tester",
        "reason": "contract validation",
        "simulation_scope": ("intent",),
        "metadata": {},
    }
    data.update(kwargs)
    with pytest.raises(ValueError, match=field):
        contract.create_dry_run_execution_request(**data)


@pytest.mark.parametrize(
    "key",
    [
        "secret",
        "token",
        "api_key",
        "password",
        "credential",
        "env",
        "private_key",
        "raw_output",
        "tool_payload",
        "model_prompt",
        "context_payload",
        "output_payload",
        "filesystem_path",
        "external_url",
        "provider_client",
        "runtime_executor",
    ],
)
def test_create_dry_run_execution_request_blocks_suspicious_metadata(key):
    with pytest.raises(ValueError):
        contract.create_dry_run_execution_request(
            request_id="dry_run_req_1",
            intent_id="intent_1",
            requested_by="tester",
            reason="contract validation",
            simulation_scope=("intent",),
            metadata={key: "blocked"},
        )


def test_evaluate_dry_run_execution_request_returns_non_activating_decision():
    request = _valid_request()
    decision = contract.evaluate_dry_run_execution_request(request)
    assert isinstance(decision, contract.DryRunExecutionDecision)
    assert decision.no_activation_confirmed is True
    assert decision.conceptual_state in contract.DRY_RUN_ALLOWED_CONCEPTUAL_STATES
    assert decision.conceptual_state not in {"queued", "running", "succeeded", "failed"}
    assert decision.allowed is True
    assert "allowed_true_is_representability_only" in decision.warnings
    assert "Security Layer" in decision.security_baseline


def test_evaluate_dry_run_execution_request_blocks_operational_state():
    request = _valid_request()
    decision = contract.evaluate_dry_run_execution_request(request, conceptual_state="queued")
    assert decision.allowed is False
    assert decision.conceptual_state == "dry_run_blocked"
    assert decision.blocked_reasons


def test_build_dry_run_execution_contract_result_has_closed_flags():
    result = contract.build_dry_run_execution_contract_result(_valid_request())
    assert isinstance(result, contract.DryRunExecutionContractResult)
    assert result.contract_status == "DRY_RUN_EXECUTION_CONTRACT_READY"
    assert result.readiness == "ready_for_dry_run_execution_contract_e2e"
    assert result.next_step == "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract"
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


def test_serialize_dry_run_execution_contract_result_is_safe_json():
    result = contract.build_dry_run_execution_contract_result(_valid_request())
    payload = contract.serialize_dry_run_execution_contract_result(result)
    json.dumps(payload, sort_keys=True)
    serialized = json.dumps(payload["request"]["metadata"], sort_keys=True).lower()
    for forbidden in [
        "raw_output",
        "secret",
        "tool_payload",
        "model_prompt",
        "context_payload",
        "output_payload",
    ]:
        assert forbidden not in serialized


def test_dry_run_execution_contract_document_exists_and_declares_status():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Dry-run Execution Contract",
        "DRY_RUN_EXECUTION_CONTRACT_READY",
        "DRY_RUN_EXECUTION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_dry_run_execution_contract_e2e",
        "PROMPT 3.36.1 — Checkpoint E2E de dry-run execution contract",
    ]:
        assert phrase in text


def test_dry_run_execution_contract_document_contains_explicit_prohibitions():
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
        "runtime runner",
        "scheduler",
        "worker",
        "queue",
        "orchestrator",
        "executor",
        "dispatcher",
        "background jobs",
        "autonomy",
        "continuous loop",
        "tool execution",
        "model invocation",
        "context injection",
        "prompt assembly runtime",
        "retrieval runtime",
        "RAG runtime",
        "output delivery",
        "output publishing",
        "writes reales",
        "stores operativos",
        "memory persistence",
        "external access",
        "API calls",
        "network",
        "browser",
        "command execution",
        "shell",
        "process spawn",
        "real filesystem reads",
        "real filesystem writes",
        "env access",
        "secret access",
        "host access",
        "device access",
        "clipboard access",
        "UI control",
        "device control",
        "UI-TARS runtime",
        "Hermes runtime",
        "n8n real workflows",
        "Home Assistant real actions",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS integration",
    ]:
        assert phrase in text


def test_no_operational_modules_were_created_by_dry_run_execution_contract():
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


def test_runtime_activation_gate_flags_remain_false_for_dry_run_execution_contract():
    flags = [
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
    assert flags == [False] * len(flags)
