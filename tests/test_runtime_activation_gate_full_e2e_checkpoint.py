from pathlib import Path

from core import runtime_activation_gate
from core.runtime_activation_gate import (
    FUTURE_CONDITIONS,
    RUNTIME_ACTIVATION_ENABLED,
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
    RUNTIME_UI_ENABLED,
    RUNTIME_UI_TARS_ENABLED,
    RUNTIME_WORKER_ENABLED,
    RUNTIME_WRITES_ENABLED,
    classify_runtime_activation_risk,
    classify_runtime_activation_signal,
    evaluate_runtime_activation_gate_contract,
    get_runtime_activation_gate_contract,
    serialize_runtime_activation_gate_decision,
    validate_runtime_activation_gate_decision,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_ACTIVATION_GATE_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _decision(signal: str, operation: str = "classify_runtime_activation_signal"):
    return evaluate_runtime_activation_gate_contract(
        activation_request_name=f"{signal}_candidate",
        activation_signal=signal,
        requested_operation=operation,
    )


def test_full_e2e_doc_exists_and_declares_status_verdict_readiness_and_next_step():
    assert DOC.exists()
    text = _text()
    for phrase in [
        "Runtime Activation Gate — Full E2E Checkpoint",
        "RUNTIME_ACTIVATION_GATE_FULL_E2E_PASSED",
        "RUNTIME_ACTIVATION_GATE_CHAIN_READY",
        "ready_for_security_layer_final_checkpoint",
        "PROMPT 3.31 — Security Layer final checkpoint pre-runtime",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_chain_and_simple_explanation():
    text = _text()
    for phrase in [
        "Security Surface Audit",
        "Agent Permission Contract",
        "Agent Permission Full E2E",
        "Secrets and Sensitive Data Policy",
        "Secrets Policy Full E2E",
        "Prompt Injection Defense Policy",
        "Prompt Injection Defense Full E2E",
        "Sandbox Boundary Policy",
        "Sandbox Boundary Full E2E",
        "Tool Boundary Policy",
        "Tool Boundary Full E2E",
        "Model Invocation Boundary Policy",
        "Model Invocation Boundary Full E2E",
        "Context Boundary Policy",
        "Context Boundary Full E2E",
        "Output Boundary Policy",
        "Output Boundary Full E2E",
        "Runtime Activation Gate Policy",
        "Runtime activation signal classification",
        "Runtime activation risk classification",
        "Runtime activation gate decision",
        "closed/planning_only/requires_future_contracts/requires_human_approval/blocked/invalid",
        "no runtime activation",
        "no runtime execution",
        "no future integrations active",
        "Runtime activation gate no es runtime",
        "Una senal puede existir conceptualmente",
        "Puede clasificarse por tipo y riesgo",
        "Puede indicar planificacion",
        "Puede indicar contratos futuros faltantes",
        "Puede requerir aprobacion humana",
        "Puede quedar bloqueada",
        "Pero no abre runtime",
        "No inicia runner",
        "No inicia scheduler",
        "No inicia worker",
        "No inicia queue",
        "No ejecuta tools",
        "No invoca modelos",
        "No inyecta contexto",
        "No entrega salidas",
        "No escribe stores",
        "No actualiza memoria",
        "No llama APIs",
        "No usa red",
        "No lee secretos",
        "No activa integraciones",
        "No ejecuta acciones irreversibles",
        "ready no significa runtime abierto",
        "E2E passed no significa runtime abierto",
        "Full E2E passed no significa runtime abierto",
        "Chain ready no significa runtime abierto",
        "Approval conceptual no significa runtime abierto",
    ]:
        assert phrase in text


def test_full_e2e_doc_contains_required_verifications_boundaries_and_scenarios():
    text = _text()
    for phrase in [
        "Existe Runtime Activation Gate Policy",
        "Existe Runtime Activation Gate E2E",
        "contract_only",
        "pre-runtime",
        "activation-gate-only",
        "deny-by-default",
        "boundary-aware",
        "permission-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "sandbox-aware",
        "tool-boundary-aware",
        "model-invocation-aware",
        "context-boundary-aware",
        "output-boundary-aware",
        "runtime runner real",
        "scheduler real",
        "worker real",
        "queue real",
        "orchestrator real",
        "executor real",
        "dispatcher real",
        "clipboard access",
        "planning_signal",
        "contract_ready_signal",
        "e2e_passed_signal",
        "full_e2e_passed_signal",
        "boundary_chain_ready_signal",
        "human_review_signal",
        "approval_signal",
        "security_policy_signal",
        "sandbox_policy_signal",
        "tool_policy_signal",
        "model_policy_signal",
        "context_policy_signal",
        "output_policy_signal",
        "runtime_candidate_signal",
        "runtime_activation_request",
        "runtime_activation_decision",
        "low/medium/high/critical",
        "condiciones futuras no cumplidas",
        "planning_signal no activa runtime",
        "requires_future_contracts no inicia runner",
        "requires_human_approval no despacha jobs",
        "allowed_to_access_secrets=True",
        "Agent Permission boundary",
        "Secrets Policy boundary",
        "Prompt Injection Defense boundary",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Output Boundary",
        "Operational Readiness Gate boundary",
        "Market Catalog sigue `planned_not_active`",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es runtime provider/integration/dependency/adapter/capability",
        "security layer final checkpoint",
        "Escenario | Activation signal | Operation | Decision | Future contracts | Human approval | Runtime | Execute | Runner | Scheduler | Worker | Queue | Tool | Model | Context | Output | Writes | Network | Secrets | Resultado esperado",
        "allowed_to_activate_runtime True forzado",
        "runtime_activation_enabled true forzado",
        "ui_tars_enabled true forzado",
        "market_catalog_active forzado",
        "OBLITERATUS como runtime provider/source/integration",
    ]:
        assert phrase in text


def test_doc_declares_all_future_conditions_and_runtime_boundary_constants_false():
    text = _text()
    for condition in FUTURE_CONDITIONS:
        assert f"{condition} = False" in text
    for constant in [
        "RUNTIME_ACTIVATION_GATE_STATUS = contract_only",
        "RUNTIME_ACTIVATION_ENABLED = False",
        "RUNTIME_EXECUTION_ENABLED = False",
        "RUNTIME_RUNNER_ENABLED = False",
        "RUNTIME_SCHEDULER_ENABLED = False",
        "RUNTIME_WORKER_ENABLED = False",
        "RUNTIME_QUEUE_ENABLED = False",
        "RUNTIME_ORCHESTRATOR_ENABLED = False",
        "RUNTIME_EXECUTOR_ENABLED = False",
        "RUNTIME_DISPATCHER_ENABLED = False",
        "RUNTIME_BACKGROUND_JOBS_ENABLED = False",
        "RUNTIME_AUTONOMY_ENABLED = False",
        "RUNTIME_CONTINUOUS_LOOP_ENABLED = False",
        "RUNTIME_TOOL_EXECUTION_ENABLED = False",
        "RUNTIME_MODEL_INVOCATION_ENABLED = False",
        "RUNTIME_CONTEXT_INJECTION_ENABLED = False",
        "RUNTIME_OUTPUT_DELIVERY_ENABLED = False",
        "RUNTIME_OUTPUT_PUBLISHING_ENABLED = False",
        "RUNTIME_WRITES_ENABLED = False",
        "RUNTIME_STORES_ENABLED = False",
        "RUNTIME_MEMORY_PERSISTENCE_ENABLED = False",
        "RUNTIME_EXTERNAL_ACCESS_ENABLED = False",
        "RUNTIME_NETWORK_ENABLED = False",
        "RUNTIME_API_ENABLED = False",
        "RUNTIME_UI_ENABLED = False",
        "RUNTIME_BROWSER_ENABLED = False",
        "RUNTIME_FILESYSTEM_ENABLED = False",
        "RUNTIME_COMMAND_EXECUTION_ENABLED = False",
        "RUNTIME_SHELL_ENABLED = False",
        "RUNTIME_PROCESS_SPAWN_ENABLED = False",
        "RUNTIME_ENV_ACCESS_ENABLED = False",
        "RUNTIME_SECRET_ACCESS_ENABLED = False",
        "RUNTIME_HOST_ACCESS_ENABLED = False",
        "RUNTIME_DEVICE_ACCESS_ENABLED = False",
        "RUNTIME_CLIPBOARD_ENABLED = False",
        "RUNTIME_UI_TARS_ENABLED = False",
        "RUNTIME_HERMES_ENABLED = False",
        "RUNTIME_N8N_ENABLED = False",
        "RUNTIME_HOME_ASSISTANT_ENABLED = False",
        "RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED = False",
        "RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False",
    ]:
        assert constant in text


def test_runtime_activation_gate_imports_keep_all_runtime_flags_disabled():
    assert RUNTIME_ACTIVATION_GATE_STATUS == "contract_only"
    flags = [
        RUNTIME_ACTIVATION_ENABLED,
        RUNTIME_EXECUTION_ENABLED,
        RUNTIME_RUNNER_ENABLED,
        RUNTIME_SCHEDULER_ENABLED,
        RUNTIME_WORKER_ENABLED,
        RUNTIME_QUEUE_ENABLED,
        RUNTIME_ORCHESTRATOR_ENABLED,
        RUNTIME_EXECUTOR_ENABLED,
        RUNTIME_DISPATCHER_ENABLED,
        RUNTIME_BACKGROUND_JOBS_ENABLED,
        RUNTIME_AUTONOMY_ENABLED,
        RUNTIME_CONTINUOUS_LOOP_ENABLED,
        RUNTIME_TOOL_EXECUTION_ENABLED,
        RUNTIME_MODEL_INVOCATION_ENABLED,
        RUNTIME_CONTEXT_INJECTION_ENABLED,
        RUNTIME_OUTPUT_DELIVERY_ENABLED,
        RUNTIME_OUTPUT_PUBLISHING_ENABLED,
        RUNTIME_WRITES_ENABLED,
        RUNTIME_STORES_ENABLED,
        RUNTIME_MEMORY_PERSISTENCE_ENABLED,
        RUNTIME_EXTERNAL_ACCESS_ENABLED,
        RUNTIME_NETWORK_ENABLED,
        RUNTIME_API_ENABLED,
        RUNTIME_UI_ENABLED,
        RUNTIME_BROWSER_ENABLED,
        RUNTIME_FILESYSTEM_ENABLED,
        RUNTIME_COMMAND_EXECUTION_ENABLED,
        RUNTIME_SHELL_ENABLED,
        RUNTIME_PROCESS_SPAWN_ENABLED,
        RUNTIME_ENV_ACCESS_ENABLED,
        RUNTIME_SECRET_ACCESS_ENABLED,
        RUNTIME_HOST_ACCESS_ENABLED,
        RUNTIME_DEVICE_ACCESS_ENABLED,
        RUNTIME_CLIPBOARD_ENABLED,
        RUNTIME_UI_TARS_ENABLED,
        RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED,
        RUNTIME_HOME_ASSISTANT_ENABLED,
        RUNTIME_MARKET_CATALOG_RUNTIME_ENABLED,
        RUNTIME_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    ]
    assert all(flag is False for flag in flags)


def test_signal_and_risk_classification_cover_full_chain_without_activation():
    for signal in runtime_activation_gate.ACTIVATION_SIGNALS:
        classification = classify_runtime_activation_signal(signal)
        assert classification.known is True
        assert classification.blocked_by_default is True
    observed_risks = {
        classify_runtime_activation_risk(signal, operation).risk_level
        for signal, operation in [
            ("planning_signal", "classify_runtime_activation_signal"),
            ("boundary_chain_ready_signal", "classify_runtime_activation_signal"),
            ("human_review_signal", "classify_runtime_activation_signal"),
            ("runtime_activation_request", "activate_runtime"),
        ]
    }
    assert runtime_activation_gate.RISK_LEVELS == {"low", "medium", "high", "critical"}
    assert {"low", "high", "critical"}.issubset(observed_risks)


def test_gate_decisions_never_enable_runtime_execution_or_side_effects():
    expected = {
        "planning_signal": "planning_only",
        "contract_ready_signal": "planning_only",
        "e2e_passed_signal": "requires_future_contracts",
        "full_e2e_passed_signal": "requires_future_contracts",
        "boundary_chain_ready_signal": "requires_future_contracts",
        "human_review_signal": "requires_human_approval",
        "approval_signal": "requires_human_approval",
        "runtime_candidate_signal": "requires_future_contracts",
        "runtime_activation_request": "blocked",
        "runtime_activation_decision": "blocked",
    }
    for signal, decision_name in expected.items():
        decision = _decision(signal)
        assert decision.decision == decision_name
        assert decision.allowed_to_activate_runtime is False
        assert decision.allowed_to_execute is False
        assert decision.allowed_to_start_runner is False
        assert decision.allowed_to_start_scheduler is False
        assert decision.allowed_to_start_worker is False
        assert decision.allowed_to_start_queue is False
        assert decision.allowed_to_dispatch is False
        assert decision.allowed_to_execute_tool is False
        assert decision.allowed_to_invoke_model is False
        assert decision.allowed_to_inject_context is False
        assert decision.allowed_to_deliver_output is False
        assert decision.allowed_to_write is False
        assert decision.allowed_to_persist is False
        assert decision.allowed_to_use_network is False
        assert decision.allowed_to_access_secrets is False
        assert validate_runtime_activation_gate_decision(decision)["status"] == "validated"


def test_forbidden_operations_are_blocked_full_e2e():
    for operation in runtime_activation_gate.FORBIDDEN_ACTIONS:
        decision = _decision("planning_signal", operation=operation)
        assert decision.decision == "blocked"
        assert decision.allowed_to_activate_runtime is False
        assert decision.allowed_to_execute is False
        assert validate_runtime_activation_gate_decision(decision)["status"] == "validated"


def test_forced_allow_flags_and_runtime_metadata_are_rejected():
    base = serialize_runtime_activation_gate_decision(_decision("planning_signal"))
    for flag in [
        "allowed_to_activate_runtime",
        "allowed_to_execute",
        "allowed_to_start_runner",
        "allowed_to_start_scheduler",
        "allowed_to_start_worker",
        "allowed_to_start_queue",
        "allowed_to_dispatch",
        "allowed_to_execute_tool",
        "allowed_to_invoke_model",
        "allowed_to_inject_context",
        "allowed_to_deliver_output",
        "allowed_to_write",
        "allowed_to_persist",
        "allowed_to_use_network",
        "allowed_to_access_secrets",
    ]:
        mutated = dict(base)
        mutated[flag] = True
        assert validate_runtime_activation_gate_decision(mutated)["status"] == "blocked"
    for flag in runtime_activation_gate.FORBIDDEN_TRUE_FLAGS:
        mutated = dict(base)
        mutated["metadata"] = {**base["metadata"], flag: True}
        assert validate_runtime_activation_gate_decision(mutated)["status"] == "blocked"
    for forbidden_value in ["market_catalog_active", "business_composition_enabled", "runtime_open", "runtime_active", "OBLITERATUS"]:
        mutated = dict(base)
        mutated["metadata"] = {"state": forbidden_value}
        assert validate_runtime_activation_gate_decision(mutated)["status"] == "blocked"


def test_contract_and_full_checkpoint_point_to_security_layer_final_checkpoint():
    contract = get_runtime_activation_gate_contract()
    assert contract["status"] == "contract_only"
    assert contract["readiness"] == "ready_for_runtime_activation_gate_e2e_checkpoint"
    assert contract["next_step"] == "PROMPT 3.30.1 - Checkpoint E2E de runtime activation gate"
    assert all(value is False for value in contract["future_conditions"].values())
    text = _text()
    assert "ready_for_security_layer_final_checkpoint" in text
    assert "PROMPT 3.31 — Security Layer final checkpoint pre-runtime" in text


def test_no_new_operational_runtime_modules_exist():
    for path in [
        "core/runtime_runner.py",
        "core/runtime_scheduler.py",
        "core/runtime_worker.py",
        "core/runtime_queue.py",
        "core/runtime_orchestrator.py",

        "core/runtime_dispatcher.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_injector.py",
        "core/output_delivery.py",
        "core/output_publisher.py",
        "core/command_executor.py",
        "core/shell.py",
        "core/subprocess_runner.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / path).exists()


def test_full_e2e_doc_has_no_contradictory_runtime_states():
    text = _text().lower()
    for phrase in [
        "runtime_activation_enabled = true",
        "runtime_execution_enabled = true",
        "runtime_runner_enabled = true",
        "runtime_scheduler_enabled = true",
        "runtime_worker_enabled = true",
        "runtime_queue_enabled = true",
        "runtime_orchestrator_enabled = true",
        "runtime_executor_enabled = true",
        "runtime_dispatcher_enabled = true",
        "runtime_background_jobs_enabled = true",
        "runtime_autonomy_enabled = true",
        "runtime_continuous_loop_enabled = true",
        "runtime_tool_execution_enabled = true",
        "runtime_model_invocation_enabled = true",
        "runtime_context_injection_enabled = true",
        "runtime_output_delivery_enabled = true",
        "runtime_output_publishing_enabled = true",
        "runtime_writes_enabled = true",
        "runtime_stores_enabled = true",
        "runtime_memory_persistence_enabled = true",
        "runtime_network_enabled = true",
        "runtime_api_enabled = true",
        "runtime_secret_access_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime`",
        "runtime_open",
        "runtime_active",
    ]:
        assert phrase not in text
