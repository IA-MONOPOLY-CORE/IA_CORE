from pathlib import Path

import core.dry_run_execution_contract as dry_run_contract
import core.kill_switch_rollback_contract as kill_switch_contract
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
DOC = ROOT / "docs" / "RUNTIME_GOVERNANCE_PRE_OPERATIONAL_AUDIT.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_runtime_governance_audit_document_status():
    text = _text()
    for phrase in [
        "RUNTIME_GOVERNANCE_AUDIT_COMPLETED",
        "RUNTIME_GOVERNANCE_BASELINE_VERIFIED",
        "ready_for_runtime_governance_contract",
        "PROMPT 3.43 — Contrato de Runtime Governance no-operativo",
    ]:
        assert phrase in text


def test_definition_is_pre_operational_only():
    text = _text()
    for phrase in [
        "Runtime Governance es la capa futura de gobierno",
        "Runtime Governance no es Runtime Activation",
        "Runtime Governance no ejecuta",
        "Runtime Governance no crea runner",
        "Runtime Governance no crea scheduler",
        "Runtime Governance no crea worker",
        "Runtime Governance no crea queue",
        "Runtime Governance no crea executor",
        "Runtime Governance no invoca tools",
        "Runtime Governance no invoca modelos",
        "Runtime Governance no inyecta contexto",
        "Runtime Governance no entrega outputs",
        "Runtime Governance no escribe stores operativos",
    ]:
        assert phrase in text


def test_governance_sources_are_listed():
    text = _text()
    for phrase in [
        "Security Layer Final Checkpoint",
        "Post-Security Block Integral Checkpoint",
        "Next Architecture Block Plan",
        "Runtime Foundation Plan",
        "Dry-run Execution Architecture Audit",
        "Dry-run Execution Contract",
        "Dry-run Execution Contract Full E2E",
        "Observability / Audit Trail Post-Security Audit",
        "Kill Switch / Rollback Contract",
        "Human Approval Gate Plan",
        "Runtime Activation Gate",
        "Operational Readiness Gate",
        "Execution Intent Contract",
        "Execution Attempt ID audit",
        "Execution Attempt schema",
        "Execution Attempt State Machine",
        "Attempt Factory contract",
        "Attempt Store write-safe contract",
        "Lifecycle Writer contract",
        "Execution Result contract",
        "Execution Result Projection",
        "Execution History View",
        "Internal Backend Read Model",
        "Attempt Store",
        "Lifecycle Store",
        "Dry Run Store",
        "Agent Permission Contract",
        "Secrets Policy",
        "Prompt Injection Defense",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Output Boundary",
    ]:
        assert phrase in text


def test_runtime_governance_matrix_is_listed():
    text = _text()
    for phrase in [
        "Runtime activation governance",
        "Runtime execution governance",
        "Runtime state governance",
        "Dry-run governance",
        "Attempt governance",
        "Lifecycle governance",
        "Result governance",
        "Projection/read model governance",
        "Tool execution governance",
        "Model invocation governance",
        "Context injection governance",
        "Output delivery governance",
        "Writes/stores governance",
        "Memory persistence governance",
        "Network/API/browser governance",
        "Filesystem/env/secrets governance",
        "Human approval governance",
        "Kill switch governance",
        "Rollback governance",
        "Observability/audit trail governance",
        "Side-effect governance",
        "Integration governance",
        "UI/runtime bridge governance",
        "Market Catalog runtime governance",
        "Business Composition Layer runtime governance",
        "Cobertura actual",
        "Requisito minimo futuro",
    ]:
        assert phrase in text


def test_readiness_valid_and_forbidden_are_listed():
    text = _text()
    for phrase in [
        "ready_for_runtime_governance_audit",
        "ready_for_runtime_governance_contract",
        "ready_for_runtime",
        "ready_for_runtime_activation",
        "ready_for_execution",
        "ready_for_dry_run_execution",
        "ready_for_tool_execution",
        "ready_for_model_invocation",
        "ready_for_context_injection",
        "ready_for_output_delivery",
        "ready_for_writes",
        "ready_for_stores",
        "runtime_open",
        "runtime_active",
        "runtime_enabled",
        "execution_enabled",
        "operations_enabled",
        "gate_open",
        "approval_enabled",
        "human_approval_operational",
        "kill_switch_enabled",
        "rollback_enabled",
        "observability_runtime_enabled",
    ]:
        assert phrase in text


def test_required_gaps_are_acknowledged():
    text = _text()
    for phrase in [
        "No existe Runtime Governance contract",
        "No existe Runtime Governance E2E",
        "No existe Runtime State contract",
        "No existe Runtime State E2E",
        "No existe Observability contract no-operativo",
        "No existe Human Approval contract no-operativo",
        "No existe Kill Switch / Rollback E2E",
        "No existe runtime event schema",
        "No existe side-effect governance contract",
        "No existe integration governance contract",
        "No existe UI/runtime bridge governance",
        "No existe Market Catalog runtime governance",
        "No existe Business Composition Layer runtime governance",
        "Estos gaps son esperados",
        "No deben resolverse en este prompt",
    ]:
        assert phrase in text


def test_required_risks_are_documented():
    text = _text()
    for phrase in [
        "Confundir Runtime Governance con Runtime Activation",
        "Crear Runtime Governance operativo antes del contrato",
        "Usar governance como bypass de Runtime Activation Gate",
        "Reinterpretar READY/E2E/CHAIN como permiso operativo",
        "Crear Runtime State sin reglas de transición",
        "Permitir dry-run execution como ejecución real",
        "Permitir approval simulado como approval real",
        "Permitir kill switch/rollback sin audit trail E2E",
        "Crear observability runtime antes de contrato",
        "Crear tool/model/context/output governance incompleta",
        "Crear writes/stores governance sin rollback",
        "Crear integrations governance antes de boundaries",
        "Activar Market Catalog/BCL runtime sin governance",
        "Registrar secretos/raw payloads en governance metadata",
        "Incorporar OBLITERATUS como governance source por accidente",
        "Mitigacion existente",
        "Mitigacion faltante",
        "Recomendacion",
    ]:
        assert phrase in text


def test_forbidden_modules_and_blockers_are_listed():
    text = _text()
    for phrase in [
        "core/runtime_governance.py",
        "core/runtime_governance_contract.py",
        "core/runtime_state.py",
        "core/runtime_state_contract.py",
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
        "runtime governance operativo",
        "runtime governance contract activo",
        "runtime state operativo",
        "runtime activation",
        "runtime execution",
        "dry-run execution activation",
        "human approval operativo",
        "kill switch operativo",
        "rollback operativo",
        "observability runtime",
        "tool execution",
        "model invocation",
        "context injection",
        "output delivery",
        "writes reales",
        "stores operativos",
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
        dry_run_contract.DRY_RUN_OUTPUT_PUBLISHING_ENABLED,
        dry_run_contract.DRY_RUN_WRITES_ENABLED,
        dry_run_contract.DRY_RUN_STORES_ENABLED,
        dry_run_contract.DRY_RUN_MEMORY_PERSISTENCE_ENABLED,
        dry_run_contract.DRY_RUN_NETWORK_ENABLED,
        dry_run_contract.DRY_RUN_API_ENABLED,
        dry_run_contract.DRY_RUN_BROWSER_ENABLED,
        dry_run_contract.DRY_RUN_FILESYSTEM_ENABLED,
        dry_run_contract.DRY_RUN_ENV_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_SECRET_ACCESS_ENABLED,
        dry_run_contract.DRY_RUN_UI_TARS_ENABLED,
        dry_run_contract.DRY_RUN_HERMES_ENABLED,
        dry_run_contract.DRY_RUN_N8N_ENABLED,
        dry_run_contract.DRY_RUN_HOME_ASSISTANT_ENABLED,
    ]
    assert flags == [False] * len(flags)


def test_kill_switch_rollback_contract_flags_remain_false():
    assert kill_switch_contract.KILL_SWITCH_ROLLBACK_OPERATIONAL is False
    for flag in [
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
        kill_switch_contract.KILL_SWITCH_SECRET_ACCESS_ENABLED,
        kill_switch_contract.KILL_SWITCH_UI_TARS_ENABLED,
        kill_switch_contract.KILL_SWITCH_HERMES_ENABLED,
        kill_switch_contract.KILL_SWITCH_N8N_ENABLED,
        kill_switch_contract.KILL_SWITCH_HOME_ASSISTANT_ENABLED,
    ]:
        assert flag is False


def test_no_operational_modules_were_created_unless_preexisting_non_operational():
    allowed = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
        "core/runtime_governance_contract.py": "Non-operational Runtime Governance contract",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in [
        "core/runtime_governance.py",
        "core/runtime_governance_contract.py",
        "core/runtime_state.py",
        "core/runtime_state_contract.py",
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
        "core/human_approval_store.py",
        "core/human_approval_audit.py",
        "core/approval_request.py",
        "core/approval_decision.py",
        "core/approval_workflow.py",
        "core/approval_ui.py",
        "core/approval_api.py",
        "core/approval_endpoint.py",
        "core/approval_runtime.py",
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
            text = candidate.read_text(encoding="utf-8").lower()
            assert allowed[path].lower() in text
            continue
        assert not candidate.exists(), path


def test_obliteratus_is_excluded_from_runtime_governance():
    text = _text()
    for phrase in [
        "OBLITERATUS no forma parte de Runtime Governance",
        "No es fuente de gobierno",
        "No es integración",
        "No es dependency",
        "No es adapter",
        "No es provider",
        "No es capability",
        "No es runtime",
        "No es roadmap operativo",
        "No debe aparecer como fuente de logs, aprobación, rollback, kill switch, dry-run, runtime, tool, model, integration, workflow ni governance",
    ]:
        assert phrase in text
