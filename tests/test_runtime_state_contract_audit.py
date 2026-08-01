from pathlib import Path

import core.dry_run_execution_contract as dry_run_contract
import core.kill_switch_rollback_contract as kill_switch_contract
import core.runtime_governance_contract as runtime_governance_contract
from core.runtime_activation_gate import (
    RUNTIME_ACTIVATION_ENABLED,
    RUNTIME_API_ENABLED,
    RUNTIME_BROWSER_ENABLED,
    RUNTIME_CONTEXT_INJECTION_ENABLED,
    RUNTIME_ENV_ACCESS_ENABLED,
    RUNTIME_EXECUTION_ENABLED,
    RUNTIME_FILESYSTEM_ENABLED,
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
DOC = ROOT / "docs" / "RUNTIME_STATE_CONTRACT_AUDIT.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_runtime_state_contract_audit_document_status():
    text = _text()
    for phrase in [
        "RUNTIME_STATE_CONTRACT_AUDIT_COMPLETED",
        "RUNTIME_STATE_BASELINE_VERIFIED",
        "ready_for_runtime_state_contract",
        "PROMPT 3.45 — Contrato de Runtime State no-operativo",
    ]:
        assert phrase in text


def test_definition_is_pre_contract_only():
    text = _text()
    for phrase in [
        "Runtime State es la representacion futura, controlada y no-operativa del estado de un runtime",
        "Runtime State no es Runtime Activation",
        "Runtime State no ejecuta",
        "Runtime State no inicia procesos",
        "Runtime State no crea runner",
        "Runtime State no crea scheduler",
        "Runtime State no crea worker",
        "Runtime State no crea queue",
        "Runtime State no crea executor",
        "Runtime State no invoca tools",
        "Runtime State no invoca modelos",
        "Runtime State no inyecta contexto",
        "Runtime State no entrega outputs",
        "Runtime State no escribe stores operativos",
    ]:
        assert phrase in text


def test_audited_sources_are_listed():
    text = _text()
    for phrase in [
        "Runtime Governance Contract",
        "Runtime Governance Contract Full E2E Checkpoint",
        "Runtime Governance Pre-operational Audit",
        "Runtime Activation Gate",
        "Runtime Foundation Plan",
        "Dry-run Execution Contract",
        "Dry-run Execution Contract Full E2E",
        "Execution Intent Contract",
        "Execution Attempt schema",
        "Execution Attempt State Machine",
        "Attempt Factory contract",
        "Attempt Store write-safe contract",
        "Lifecycle Writer contract",
        "Execution Result contract",
        "Execution Result Projection",
        "Execution History View",
        "Internal Backend Read Model",
        "Observability / Audit Trail Post-Security Audit",
        "Kill Switch / Rollback Contract",
        "Human Approval Gate Plan",
        "Security Layer Final Checkpoint",
        "Post-Security Block Integral Checkpoint",
        "Agent Permission Contract",
        "Secrets Policy",
        "Prompt Injection Defense",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Output Boundary",
        "Archivo/modulo/documento asociado",
        "Riesgo operativo",
        "Falta antes del contrato",
        "Recomendacion",
    ]:
        assert phrase in text


def test_conceptual_and_forbidden_states_are_listed():
    text = _text()
    for phrase in [
        "runtime_state_uninitialized",
        "runtime_state_governance_pending",
        "runtime_state_security_blocked",
        "runtime_state_policy_blocked",
        "runtime_state_ready_simulated",
        "runtime_state_dry_run_required",
        "runtime_state_human_approval_required",
        "runtime_state_audit_trail_required",
        "runtime_state_kill_switch_required",
        "runtime_state_rollback_required",
        "runtime_state_blocked",
        "runtime_state_invalid",
        "runtime_state_archived_simulated",
        "No activan runtime",
        "No habilitan ejecucion",
    ]:
        assert phrase in text
    for phrase in [
        "runtime_state_active",
        "runtime_state_running",
        "runtime_state_executing",
        "runtime_state_live",
        "runtime_state_open",
        "runtime_state_enabled",
        "runtime_state_operational",
        "runtime_state_tool_executing",
        "runtime_state_model_invoking",
        "runtime_state_context_injecting",
        "runtime_state_output_delivering",
        "runtime_state_writing",
        "runtime_state_persisting_memory",
        "runtime_state_network_active",
        "runtime_state_api_active",
        "runtime_state_browser_active",
        "runtime_state_filesystem_active",
        "runtime_state_env_active",
        "runtime_state_secret_active",
        "runtime_state_ui_control_active",
        "runtime_state_device_control_active",
        "runtime_state_integration_active",
        "runtime_state_market_catalog_active",
        "runtime_state_business_composition_active",
    ]:
        assert phrase in text


def test_conceptual_and_forbidden_transitions_are_listed():
    text = _text()
    for phrase in [
        "uninitialized -> governance_pending",
        "governance_pending -> security_blocked",
        "governance_pending -> policy_blocked",
        "governance_pending -> ready_simulated",
        "ready_simulated -> dry_run_required",
        "ready_simulated -> human_approval_required",
        "ready_simulated -> audit_trail_required",
        "ready_simulated -> kill_switch_required",
        "ready_simulated -> rollback_required",
        "any -> blocked",
        "any -> invalid",
        "any -> archived_simulated",
        "No activan workers/queues/executors",
    ]:
        assert phrase in text
    for phrase in [
        "ready_simulated -> runtime_active",
        "ready_simulated -> runtime_running",
        "ready_simulated -> runtime_executing",
        "ready_simulated -> tool_executing",
        "ready_simulated -> model_invoking",
        "ready_simulated -> context_injecting",
        "ready_simulated -> output_delivering",
        "ready_simulated -> writes_enabled",
        "ready_simulated -> stores_enabled",
        "ready_simulated -> memory_persistence_enabled",
        "ready_simulated -> network_enabled",
        "ready_simulated -> api_enabled",
        "ready_simulated -> browser_enabled",
        "ready_simulated -> filesystem_enabled",
        "ready_simulated -> env_access_enabled",
        "ready_simulated -> secret_access_enabled",
        "ready_simulated -> ui_control_enabled",
        "ready_simulated -> device_control_enabled",
        "ready_simulated -> integration_enabled",
        "any -> runtime_active",
        "any -> runtime_execution",
        "any -> operations_enabled",
        "any -> gate_open",
    ]:
        assert phrase in text


def test_runtime_state_matrix_is_complete():
    text = _text()
    for phrase in [
        "State identity",
        "State ownership",
        "State scope",
        "State governance dependency",
        "State security dependency",
        "State approval dependency",
        "State audit dependency",
        "State kill switch dependency",
        "State rollback dependency",
        "State dry-run dependency",
        "State attempt dependency",
        "State lifecycle dependency",
        "State result dependency",
        "State projection/read model dependency",
        "State side-effect guarantee",
        "State metadata sanitization",
        "State transition validity",
        "State forbidden readiness",
        "State forbidden capability",
        "State serialization",
        "State determinism",
        "State archival",
        "State reset/rollback simulation",
        "State integration boundary",
        "State OBLITERATUS exclusion",
        "Cobertura actual",
        "Requisito minimo futuro",
    ]:
        assert phrase in text


def test_metadata_gaps_risks_and_recommendation_are_listed():
    text = _text()
    for phrase in [
        "runtime_state_id",
        "runtime_governance_ref",
        "runtime_gate_ref",
        "security_baseline_ref",
        "intent_id optional",
        "attempt_id optional",
        "lifecycle_ref optional",
        "result_ref optional",
        "projection_ref optional",
        "dry_run_ref optional",
        "human_approval_ref optional",
        "audit_trail_ref optional",
        "kill_switch_ref optional",
        "rollback_ref optional",
        "state_reason",
        "state_scope",
        "state_risk_level",
        "state_created_at_controlled optional",
        "metadata_sanitized",
        "No debe contener secrets",
        "No debe contener raw_payload",
        "No debe contener raw_output",
        "No debe contener file_content",
        "No debe contener env",
        "No debe contener tokens/passwords/credentials",
    ]:
        assert phrase in text
    for phrase in [
        "No existe Runtime State contract",
        "No existe Runtime State E2E",
        "No existe runtime state transition validator",
        "No existe runtime state snapshot contract",
        "No existe runtime state serialization contract",
        "No existe runtime state metadata sanitizer propio",
        "No existe runtime state archive/reset simulation contract",
        "No existe runtime state dependency checker",
        "No existe runtime state integration boundary",
        "No existe runtime state side-effect ledger contract",
        "Estos gaps son esperados",
        "No deben resolverse en este prompt",
    ]:
        assert phrase in text
    for phrase in [
        "Confundir Runtime State con Runtime Activation",
        "Confundir ready_simulated con ready_for_runtime",
        "Crear estados activos antes del contrato",
        "Crear transiciones que habiliten ejecucion real",
        "Permitir state mutation operativa",
        "Escribir Runtime State en stores operativos",
        "Registrar secretos o payloads reales en metadata",
        "Permitir transicion a tool/model/context/output real",
        "Permitir transicion a writes/stores/network/secrets",
        "Permitir integracion runtime por estado",
        "Usar Runtime State como bypass de Runtime Governance",
        "Usar Runtime State como bypass de Human Approval",
        "Usar Runtime State como bypass de Kill Switch/Rollback",
        "Usar Runtime State como bypass de Audit Trail",
        "Incorporar OBLITERATUS como runtime state source por accidente",
        "Mitigacion existente",
        "Mitigacion faltante",
        "Recomendacion",
    ]:
        assert phrase in text
    assert "PROMPT 3.45 — Contrato de Runtime State no-operativo" in text


def test_forbidden_modules_and_explicit_blockers_are_listed():
    text = _text()
    for phrase in [
        "core/runtime_state.py",
        "core/runtime_state_contract.py",
        "core/runtime_state_machine.py",
        "core/runtime_state_validator.py",
        "core/runtime_state_snapshot.py",
        "core/runtime_state_store.py",
        "core/runtime_state_writer.py",
        "core/runtime_state_reader.py",
        "core/runtime_state_transition.py",
        "core/runtime_state_event.py",
        "core/runtime_state_event_bus.py",
        "core/runtime_governance.py",
        "core/runtime_controller.py",
        "core/runtime_manager.py",
        "core/runtime_runner.py",
        "core/runtime_scheduler.py",
        "core/runtime_worker.py",
        "core/runtime_queue.py",
        "core/runtime_executor.py",
        "core/runtime_orchestrator.py",
        "core/runtime_dispatcher.py",
        "core/runtime_event_schema.py",
        "core/runtime_event_bus.py",
        "core/human_approval_gate.py",
        "core/human_approval_contract.py",
        "core/approval_workflow.py",
        "core/kill_switch.py",
        "core/rollback_controller.py",
        "core/audit_trail.py",
        "core/event_bus.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert phrase in text
    for phrase in [
        "runtime state operativo",
        "runtime state contract activo",
        "runtime state machine operativa",
        "runtime state mutation real",
        "runtime state store operativo",
        "runtime state writer operativo",
        "runtime state reader operativo",
        "runtime state transition real",
        "runtime state event bus",
        "runtime governance operativo",
        "runtime governance activation",
        "runtime governance execution",
        "runtime controller",
        "runtime manager",
        "runtime activation",
        "runtime execution",
        "runtime runner",
        "runtime scheduler",
        "runtime worker",
        "runtime queue",
        "runtime executor",
        "dry-run execution activation",
        "dry-run executor",
        "human approval operativo",
        "approval gate active",
        "approval workflow real",
        "kill switch operativo",
        "rollback operativo",
        "observability runtime",
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


def test_no_operational_modules_were_created_unless_preexisting_non_operational():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
        "core/runtime_governance_contract.py": "Non-operational Runtime Governance contract",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in [
        "core/runtime_state.py",
        "core/runtime_state_contract.py",
        "core/runtime_state_machine.py",
        "core/runtime_state_validator.py",
        "core/runtime_state_snapshot.py",
        "core/runtime_state_store.py",
        "core/runtime_state_writer.py",
        "core/runtime_state_reader.py",
        "core/runtime_state_transition.py",
        "core/runtime_state_event.py",
        "core/runtime_state_event_bus.py",
        "core/runtime_governance.py",
        "core/runtime_controller.py",
        "core/runtime_manager.py",
        "core/runtime_runner.py",
        "core/runtime_scheduler.py",
        "core/runtime_worker.py",
        "core/runtime_queue.py",
        "core/runtime_executor.py",
        "core/runtime_orchestrator.py",
        "core/runtime_dispatcher.py",
        "core/runtime_event_schema.py",
        "core/runtime_event_bus.py",
        "core/human_approval_gate.py",
        "core/human_approval_contract.py",
        "core/approval_workflow.py",
        "core/kill_switch.py",
        "core/rollback_controller.py",
        "core/audit_trail.py",
        "core/event_bus.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        candidate = ROOT / path
        if path in allowed and candidate.exists():
            assert allowed[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_runtime_governance_contract_flags_remain_false():
    for flag in [
        runtime_governance_contract.RUNTIME_GOVERNANCE_OPERATIONAL,
        runtime_governance_contract.RUNTIME_GOVERNANCE_ACTIVATION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_EXECUTION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_CONTROLLER_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_MANAGER_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_STATE_MUTATION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_EVENT_BUS_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_DRY_RUN_EXECUTION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_TOOL_EXECUTION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_MODEL_INVOCATION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_CONTEXT_INJECTION_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_OUTPUT_DELIVERY_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_WRITES_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_STORES_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_MEMORY_PERSISTENCE_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_NETWORK_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_API_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_BROWSER_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_FILESYSTEM_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_ENV_ACCESS_ENABLED,
        runtime_governance_contract.RUNTIME_GOVERNANCE_SECRET_ACCESS_ENABLED,
        runtime_governance_contract.OBLITERATUS_RUNTIME_GOVERNANCE_ENABLED,
    ]:
        assert flag is False


def test_runtime_activation_gate_flags_remain_false():
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
        RUNTIME_BROWSER_ENABLED,
        RUNTIME_FILESYSTEM_ENABLED,
        RUNTIME_ENV_ACCESS_ENABLED,
        RUNTIME_SECRET_ACCESS_ENABLED,
        RUNTIME_UI_TARS_ENABLED,
        RUNTIME_HERMES_ENABLED,
        RUNTIME_N8N_ENABLED,
        RUNTIME_HOME_ASSISTANT_ENABLED,
    ]
    assert flags == [False] * len(flags)


def test_dry_run_execution_contract_flags_remain_false():
    flags = [
        dry_run_contract.DRY_RUN_EXECUTION_OPERATIONAL,
        dry_run_contract.DRY_RUN_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_EXECUTOR_ENABLED,
        dry_run_contract.DRY_RUN_RUNNER_ENABLED,
        dry_run_contract.DRY_RUN_DISPATCHER_ENABLED,
        dry_run_contract.DRY_RUN_SCHEDULER_ENABLED,
        dry_run_contract.DRY_RUN_WORKER_ENABLED,
        dry_run_contract.DRY_RUN_QUEUE_ENABLED,
        dry_run_contract.DRY_RUN_TOOL_EXECUTION_ENABLED,
        dry_run_contract.DRY_RUN_MODEL_INVOCATION_ENABLED,
        dry_run_contract.DRY_RUN_CONTEXT_INJECTION_ENABLED,
        dry_run_contract.DRY_RUN_OUTPUT_DELIVERY_ENABLED,
        dry_run_contract.DRY_RUN_WRITES_ENABLED,
        dry_run_contract.DRY_RUN_STORES_ENABLED,
        dry_run_contract.DRY_RUN_MEMORY_PERSISTENCE_ENABLED,
        dry_run_contract.DRY_RUN_NETWORK_ENABLED,
        dry_run_contract.DRY_RUN_API_ENABLED,
        dry_run_contract.DRY_RUN_BROWSER_ENABLED,
        dry_run_contract.DRY_RUN_FILESYSTEM_ENABLED,
        dry_run_contract.DRY_RUN_ENV_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED,
    ]
    assert flags == [False] * len(flags)


def test_kill_switch_rollback_contract_flags_remain_false():
    flags = [
        kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL,
        kill_switch_contract.KILL_SWITCH_ENABLED,
        kill_switch_contract.ROLLBACK_ENABLED,
        kill_switch_contract.KILL_SWITCH_EXECUTION_ENABLED,
        kill_switch_contract.ROLLBACK_EXECUTION_ENABLED,
        kill_switch_contract.PROCESS_TERMINATION_ENABLED,
        kill_switch_contract.JOB_CANCELLATION_ENABLED,
        kill_switch_contract.QUEUE_DRAIN_ENABLED,
        kill_switch_contract.WORKER_STOP_ENABLED,
        kill_switch_contract.SCHEDULER_STOP_ENABLED,
        kill_switch_contract.RUNNER_STOP_ENABLED,
        kill_switch_contract.EXECUTOR_STOP_ENABLED,
        kill_switch_contract.ROLLBACK_FILESYSTEM_ENABLED,
        kill_switch_contract.ROLLBACK_GIT_ENABLED,
        kill_switch_contract.ROLLBACK_STORE_MUTATION_ENABLED,
        kill_switch_contract.ROLLBACK_MANIFEST_MUTATION_ENABLED,
        kill_switch_contract.ROLLBACK_DATABASE_ENABLED,
        kill_switch_contract.ROLLBACK_MEMORY_ENABLED,
        kill_switch_contract.KILL_SWITCH_TOOL_EXECUTION_ENABLED,
        kill_switch_contract.KILL_SWITCH_MODEL_INVOCATION_ENABLED,
        kill_switch_contract.KILL_SWITCH_CONTEXT_INJECTION_ENABLED,
        kill_switch_contract.KILL_SWITCH_OUTPUT_DELIVERY_ENABLED,
        kill_switch_contract.KILL_SWITCH_NETWORK_ENABLED,
        kill_switch_contract.KILL_SWITCH_API_ENABLED,
        kill_switch_contract.KILL_SWITCH_BROWSER_ENABLED,
        kill_switch_contract.KILL_SWITCH_FILESYSTEM_ENABLED,
        kill_switch_contract.KILL_SWITCH_ENV_ACCESS_ENABLED,
        kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED,
    ]
    assert flags == [False] * len(flags)


def test_obliteratus_is_excluded_from_runtime_state_roles():
    text = _text()
    for phrase in [
        "OBLITERATUS no forma parte de Runtime State",
        "No es fuente de estado",
        "No es integracion",
        "No es dependency",
        "No es adapter",
        "No es provider",
        "No es capability",
        "No es runtime",
        "No es roadmap operativo",
        "No debe aparecer como fuente de logs, aprobacion, rollback, kill switch, dry-run, runtime, tool, model, integration, workflow, governance ni state",
        "runtime state source",
        "governance source",
        "state source",
        "runtime provider",
    ]:
        assert phrase in text
