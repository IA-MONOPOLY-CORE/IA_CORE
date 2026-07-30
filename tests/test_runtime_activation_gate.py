from pathlib import Path

from core import agent_permission_contract, context_boundary, model_invocation_boundary, output_boundary, prompt_injection_defense, sandbox_boundary, secrets_policy, tool_boundary
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_ACTIVATION_GATE_READY,
    RUNTIME_ACTIVATION_GATE_STATUS,
    RUNTIME_API_ENABLED,
    RUNTIME_AUTONOMY_ENABLED,
    RUNTIME_BACKGROUND_JOBS_ENABLED,
    RUNTIME_BROWSER_ENABLED,
    RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    RUNTIME_CLIPBOARD_ENABLED,
    RUNTIME_COMMAND_EXECUTION_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_CONTINUOUS_LOOP_ENABLED,
    RUNTIME_DEVICE_ACCESS_ENABLED,
    RUNTIME_DISPATCHER_ENABLED,
    RUNTIME_ENV_ACCESS_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_EXECUTOR_ENABLED,
    RUNTIME_EXTERNAL_ACCESS_ENABLED,
    RUNTIME_FILESYSTEM_ENABLED,
    RUNTIME_HERMES_ENABLED,
    RUNTIME_HOME_ASSISTANT_ENABLED,
    RUNTIME_HOST_ACCESS_ENABLED,
    RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
    RUNTIME_MEMORY_PERSISTENCE_ENABLED,
    RUNTIME_MODEL_INVOCATION_ENABLED,
    RUNTIME_N8N_ENABLED,
    RUNTIME_NETWORK_ENABLED,
    RUNTIME_ORCHESTRATOR_ENABLED,
    RUNTIME_OUTPUT_DELIVERY_ENABLED,
    RUNTIME_OUTPUT_PUBLISHING_ENABLED,
    RUNTIME_PROCESS_SPAWN_ENABLED,
    RUNTIME_QUEUE_ENABLED,
    RUNTIME_RUNNER_ENABLED,
    RUNTIME_SCHEDULER_ENABLED,
    RUNTIME_SECRET_ACCESS_ENABLED,
    RUNTIME_SHELL_ENABLED,
    RUNTIME_STORES_ENABLED,
    RUNTIME_TOOL_EXECUTION_ENABLED,
    RUNTIME_UI_TARS_ENABLED,
    RUNTIME_WORKER_ENABLED,
    RUNTIME_WRITES_ENABLED,
    classify_runtime_activation_signal,
    evaluate_runtime_activation_gate_contract,
    get_runtime_activation_gate_contract,
    serialize_runtime_activation_gate_decision,
    validate_runtime_activation_gate_decision,
)

ROOT = Path(__file__).resolve().parents[1]


def _decision(signal: str, operation: str = "classify_runtime_activation_signal"):
    return evaluate_runtime_activation_gate_contract(
        activation_request_name=f"{signal}_candidate",
        activation_signal=signal,
        requested_operation=operation,
    )


def test_module_exists_and_status_constants_are_contract_only():
    assert (ROOT / "core" / "runtime_activation_gate.py").exists()
    assert RUNTIME_ACTIVATION_GATE_STATUS == "contract_only"
    assert RUNTIME_ACTIVATION_GATE_READY is True


def test_all_runtime_flags_are_disabled():
    flags = [
        RUNTIME_ACTIVATION_ENABLED, RUNTIME_EXECUTION_ENABLED, RUNTIME_RUNNER_ENABLED, RUNTIME_SCHEDULER_ENABLED,
        RUNTIME_WORKER_ENABLED, RUNTIME_QUEUE_ENABLED, RUNTIME_ORCHESTRATOR_ENABLED, RUNTIME_EXECUTOR_ENABLED,
        RUNTIME_DISPATCHER_ENABLED, RUNTIME_BACKGROUND_JOBS_ENABLED, RUNTIME_AUTONOMY_ENABLED, RUNTIME_CONTINUOUS_LOOP_ENABLED,
        RUNTIME_TOOL_EXECUTION_ENABLED, RUNTIME_MODEL_INVOCATION_ENABLED, RUNTIME_CONTEXT_INJECTION_ENABLED,
        RUNTIME_OUTPUT_DELIVERY_ENABLED, RUNTIME_OUTPUT_PUBLISHING_ENABLED, RUNTIME_WRITES_ENABLED, RUNTIME_STORES_ENABLED,
        RUNTIME_MEMORY_PERSISTENCE_ENABLED, RUNTIME_EXTERNAL_ACCESS_ENABLED, RUNTIME_NETWORK_ENABLED, RUNTIME_API_ENABLED,
        RUNTIME_BROWSER_ENABLED, RUNTIME_FILESYSTEM_ENABLED, RUNTIME_COMMAND_EXECUTION_ENABLED, RUNTIME_SHELL_ENABLED,
        RUNTIME_PROCESS_SPAWN_ENABLED, RUNTIME_ENV_ACCESS_ENABLED, RUNTIME_SECRET_ACCESS_ENABLED, RUNTIME_HOST_ACCESS_ENABLED,
        RUNTIME_DEVICE_ACCESS_ENABLED, RUNTIME_CLIPBOARD_ENABLED, RUNTIME_UI_TARS_ENABLED, RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED, RUNTIME_HOME_ASSISTANT_ENABLED, RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
        RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert all(flag is False for flag in flags)


def test_classifies_all_runtime_activation_signals():
    for signal in [
        "planning_signal", "contract_ready_signal", "e2e_passed_signal", "full_e2e_passed_signal",
        "boundary_chain_ready_signal", "human_review_signal", "approval_signal", "security_policy_signal",
        "sandbox_policy_signal", "tool_policy_signal", "model_policy_signal", "context_policy_signal",
        "output_policy_signal", "runtime_candidate_signal", "runtime_activation_request", "runtime_activation_decision",
    ]:
        classification = classify_runtime_activation_signal(signal)
        assert classification.known is True
        assert classification.activation_signal == signal


def test_expected_gate_decisions_never_activate_runtime():
    cases = {
        "planning_signal": {"planning_only"},
        "contract_ready_signal": {"planning_only"},
        "security_policy_signal": {"planning_only"},
        "e2e_passed_signal": {"requires_future_contracts"},
        "full_e2e_passed_signal": {"requires_future_contracts"},
        "boundary_chain_ready_signal": {"requires_future_contracts"},
        "runtime_candidate_signal": {"requires_future_contracts"},
        "human_review_signal": {"requires_human_approval"},
        "approval_signal": {"requires_human_approval"},
        "runtime_activation_request": {"blocked"},
        "runtime_activation_decision": {"blocked"},
    }
    for signal, expected in cases.items():
        decision = _decision(signal)
        assert decision.decision in expected
        assert decision.allowed_to_activate_runtime is False
        assert decision.allowed_to_execute is False
        assert decision.allowed_to_start_runner is False
        assert decision.allowed_to_dispatch is False
        assert decision.allowed_to_execute_tool is False
        assert decision.allowed_to_invoke_model is False
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_deliver_output is False
        assert validate_runtime_activation_gate_decision(decision)["status"] == "validated"


def test_forbidden_operations_are_blocked_without_runtime():
    for operation in [
        "activate_runtime", "open_runtime_gate", "start_runtime_runner", "start_scheduler", "start_worker", "start_queue",
        "start_orchestrator", "start_executor", "dispatch_job", "enqueue_job", "run_background_job",
        "start_autonomous_loop", "execute_tool", "invoke_model", "inject_context", "deliver_output", "publish_output",
        "write_file", "write_store", "update_memory", "call_api", "network_request", "open_browser", "read_real_file",
        "write_real_file", "read_env", "read_secret", "run_command", "open_shell", "spawn_process", "control_ui",
        "control_device", "trigger_workflow", "perform_irreversible_action",
    ]:
        decision = _decision("planning_signal", operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_activate_runtime is False
        assert validate_runtime_activation_gate_decision(decision)["status"] == "validated"


def test_validation_rejects_allow_flags_and_runtime_true_flags():
    base = serialize_runtime_activation_gate_decision(_decision("planning_signal"))
    for flag in [
        "allowed_to_activate_runtime", "allowed_to_execute", "allowed_to_start_runner", "allowed_to_start_scheduler",
        "allowed_to_start_worker", "allowed_to_start_queue", "allowed_to_dispatch", "allowed_to_execute_tool",
        "allowed_to_invoke_model", "allowed_to_inject_context", "allowed_to_deliver_output", "allowed_to_write",
        "allowed_to_persist", "allowed_to_use_network", "allowed_to_access_secrets",
    ]:
        mutated = dict(base)
        mutated[flag] = True
        assert validate_runtime_activation_gate_decision(mutated)["status"] == "blocked"
    for flag in [
        "runtime_activation_enabled", "runtime_execution_enabled", "runtime_runner_enabled", "runtime_scheduler_enabled",
        "runtime_worker_enabled", "runtime_queue_enabled", "runtime_orchestrator_enabled", "runtime_executor_enabled",
        "runtime_dispatcher_enabled", "runtime_background_jobs_enabled", "runtime_autonomy_enabled", "runtime_continuous_loop_enabled",
        "runtime_tool_execution_enabled", "runtime_model_invocation_enabled", "runtime_context_injection_enabled",
        "runtime_output_delivery_enabled", "runtime_output_publishing_enabled", "runtime_writes_enabled", "runtime_stores_enabled",
        "runtime_memory_persistence_enabled", "runtime_network_enabled", "runtime_api_enabled", "runtime_secret_access_enabled",
        "ui_tars_enabled", "hermes_enabled", "n8n_enabled", "home_assistant_enabled",
    ]:
        mutated = dict(base)
        mutated["metadata"] = {**base["metadata"], flag: True}
        assert validate_runtime_activation_gate_decision(mutated)["status"] == "blocked"
    for forbidden in ["market_catalog_active", "business_composition_enabled", "runtime_open", "runtime_active", "OBLITERATUS"]:
        mutated = dict(base)
        mutated["metadata"] = {"state": forbidden}
        assert validate_runtime_activation_gate_decision(mutated)["status"] == "blocked"


def test_future_conditions_are_all_missing_and_required():
    contract = get_runtime_activation_gate_contract()
    assert contract["future_conditions"]
    assert all(value is False for value in contract["future_conditions"].values())
    assert set(contract["missing_future_conditions"]) == set(contract["future_conditions"])
    decision = _decision("boundary_chain_ready_signal")
    assert decision.missing_future_conditions


def test_previous_boundaries_remain_contractual():
    contract = get_runtime_activation_gate_contract()
    assert contract["verdict"] == "RUNTIME_ACTIVATION_GATE_READY"
    assert contract["readiness"] == "ready_for_runtime_activation_gate_e2e_checkpoint"
    assert contract["next_step"] == "PROMPT 3.30.1 - Checkpoint E2E de runtime activation gate"
    assert agent_permission_contract.AGENT_PERMISSION_CONTRACT_STATUS == "contract_only"
    assert secrets_policy.SECRETS_POLICY_STATUS == "contract_only"
    assert prompt_injection_defense.PROMPT_INJECTION_DEFENSE_STATUS == "contract_only"
    assert sandbox_boundary.SANDBOX_BOUNDARY_STATUS == "contract_only"
    assert tool_boundary.TOOL_BOUNDARY_STATUS == "contract_only"
    assert model_invocation_boundary.MODEL_INVOCATION_BOUNDARY_STATUS == "contract_only"
    assert context_boundary.CONTEXT_BOUNDARY_STATUS == "contract_only"
    assert output_boundary.OUTPUT_BOUNDARY_STATUS == "contract_only"
    assert contract["operational_readiness_gate_boundary"] == "closed"


def test_policy_document_contains_required_readiness_and_next_step():
    text = (ROOT / "docs" / "RUNTIME_ACTIVATION_GATE_POLICY.md").read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_ACTIVATION_GATE_READY", "ready_for_runtime_activation_gate_e2e_checkpoint",
        "PROMPT 3.30.1 - Checkpoint E2E de runtime activation gate", "no runtime activation",
        "no runtime execution", "no runtime runner", "no scheduler", "no worker", "no queue", "no orchestrator",
        "no executor", "no dispatcher", "no background jobs", "no autonomy", "no continuous loop",
        "Market Catalog remains planned_not_active", "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text
