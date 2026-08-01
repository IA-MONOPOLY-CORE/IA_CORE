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
DOC = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_next_architecture_block_plan_document_exists_and_declares_status():
    text = _text()
    for phrase in [
        "NEXT_ARCHITECTURE_BLOCK_PLAN_READY",
        "POST_SECURITY_BLOCK_CONSUMED_AS_BASELINE",
        "ready_for_runtime_governance_audit",
        "PROMPT 3.42 — Auditoría de Runtime Governance pre-operational",
    ]:
        assert phrase in text


def test_document_declares_recommended_block_and_not_runtime():
    text = _text()
    for phrase in [
        "Runtime Governance Block — Pre-operational",
        "Runtime Governance no significa runtime",
        "No significa activación",
        "No significa ejecución",
        "No significa runner",
        "No significa scheduler",
        "No significa worker",
        "No significa queue",
        "No significa executor",
        "No significa tool execution",
        "No significa model invocation",
        "No significa context injection",
        "No significa output delivery",
    ]:
        assert phrase in text


def test_document_contains_possible_blocks_evaluated():
    text = _text()
    for phrase in [
        "Runtime Governance Block — Pre-operational",
        "Runtime State Contract Block",
        "Observability Contract Block",
        "Human Approval Contract Block",
        "Kill Switch / Rollback E2E Block",
        "Dry-run Integration Block",
        "Execution Planner Contract Block",
        "Tool Executor Future Contract Block",
        "Model Provider Future Contract Block",
        "Context Builder Future Contract Block",
        "Output Delivery Future Contract Block",
        "UI/UX Runtime Bridge Planning Block",
        "Market Catalog / Business Composition Layer future block",
        "External Integrations Future Block: UI-TARS, Hermes, n8n, Home Assistant",
        "Ahora: Runtime Governance Block — Pre-operational",
        "Después: Runtime State Contract / Observability Contract / Human Approval Contract",
        "Futuro: Tool/Model/Context/Output/Integrations/UI runtime bridges",
    ]:
        assert phrase in text


def test_document_contains_tentative_sequence():
    text = _text()
    for phrase in [
        "PROMPT 3.42 — Auditoría de Runtime Governance pre-operational",
        "PROMPT 3.43 — Contrato de Runtime Governance no-operativo",
        "PROMPT 3.43.1 — Checkpoint E2E de Runtime Governance contract",
        "PROMPT 3.44 — Auditoría de Runtime State Contract",
        "PROMPT 3.45 — Contrato de Runtime State no-operativo",
        "PROMPT 3.45.1 — Checkpoint E2E de Runtime State contract",
        "PROMPT 3.46 — Auditoría de Observability Contract",
        "PROMPT 3.47 — Contrato de Observability no-operativo",
        "PROMPT 3.48 — Checkpoint integral Runtime Governance block",
        "Este orden es tentativo",
        "Ningún paso de este bloque activa runtime",
        "Ningún paso de este bloque ejecuta tools/modelos/context/output",
        "Ningún paso de este bloque habilita writes/stores operativos",
    ]:
        assert phrase in text


def test_document_contains_consumed_baseline_and_rules():
    text = _text()
    for phrase in [
        "Security Layer final checkpoint",
        "Post-Security block integral checkpoint",
        "Runtime Foundation plan",
        "Dry-run execution contract + E2E",
        "Observability/audit trail audit",
        "Kill switch/rollback future-only contract",
        "Human Approval Gate plan",
        "Ninguna pieza del próximo bloque puede contradecir estos checkpoints",
        "Ninguna pieza del próximo bloque puede reinterpretar READY/E2E/CHAIN como permiso operativo",
        "Ninguna pieza del próximo bloque puede abrir runtime",
        "Ninguna pieza del próximo bloque puede saltarse Security Layer",
    ]:
        assert phrase in text


def test_document_contains_forbidden_readiness():
    text = _text()
    for phrase in [
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


def test_document_contains_forbidden_modules():
    text = _text()
    for phrase in [
        "core/runtime_governance.py",
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
        "core/rollback_executor.py",
        "core/process_killer.py",
        "core/job_canceller.py",
        "core/queue_drain.py",
        "core/worker_stop.py",
        "core/scheduler_stop.py",
        "core/runner_stop.py",
        "core/executor_stop.py",
        "core/filesystem_rollback.py",
        "core/git_rollback.py",
        "core/store_rollback.py",
        "core/database_rollback.py",
        "core/memory_rollback.py",
        "core/audit_trail.py",
        "core/audit_logger.py",
        "core/event_log.py",
        "core/event_bus.py",
        "core/telemetry.py",
        "core/metrics_collector.py",
        "core/tracing.py",
        "core/dashboard.py",
        "core/correlation_ledger.py",
        "core/immutable_audit_log.py",
        "core/side_effect_ledger.py",
        "core/dry_run_executor.py",
        "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py",
        "core/dry_run_scheduler.py",
        "core/dry_run_worker.py",
        "core/dry_run_queue.py",
        "core/tool_executor.py",
        "core/tool_registry.py",
        "core/tool_adapter.py",
        "core/model_invoker.py",
        "core/model_router.py",
        "core/model_executor.py",
        "core/inference_runner.py",
        "core/context_builder.py",
        "core/context_injector.py",
        "core/prompt_assembler.py",
        "core/retrieval_engine.py",
        "core/rag_engine.py",
        "core/output_writer.py",
        "core/output_publisher.py",
        "core/output_notifier.py",
        "core/output_delivery.py",
        "core/message_sender.py",
        "core/email_sender.py",
        "core/webhook_client.py",
        "core/provider_client.py",
        "core/browser_operator.py",
        "core/sandbox_runner.py",
        "core/command_executor.py",
        "core/shell.py",
        "core/subprocess_runner.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert phrase in text


def test_document_contains_explicit_blockers():
    text = _text()
    for phrase in [
        "runtime governance operativo",
        "runtime state operativo",
        "runtime controller",
        "runtime manager",
        "runtime activation",
        "runtime execution",
        "runtime runner",
        "runtime scheduler",
        "runtime worker",
        "runtime queue",
        "runtime executor",
        "runtime orchestrator",
        "runtime dispatcher",
        "runtime event bus",
        "dry-run execution activation",
        "dry-run executor",
        "dry-run runner",
        "dry-run dispatcher",
        "dry-run scheduler",
        "dry-run worker",
        "dry-run queue",
        "human approval operativo",
        "approval gate active",
        "approval workflow real",
        "approval UI real",
        "approval API real",
        "approval endpoint real",
        "approval store operativo",
        "automatic approval",
        "permission escalation",
        "runtime approval real",
        "execution approval real",
        "tool execution approval real",
        "model invocation approval real",
        "output delivery approval real",
        "writes approval real",
        "stores approval real",
        "integration approval real",
        "kill switch operativo",
        "rollback operativo",
        "process termination",
        "job cancellation",
        "queue drain",
        "worker stop",
        "scheduler stop",
        "runner stop",
        "executor stop",
        "filesystem rollback",
        "git rollback",
        "store mutation",
        "manifest mutation",
        "database rollback",
        "memory rollback",
        "observability runtime",
        "audit trail operativo",
        "event log operativo",
        "event bus",
        "telemetry real",
        "metrics collector",
        "tracing real",
        "dashboard operativo",
        "immutable audit log operativo",
        "correlation ledger runtime",
        "side-effect ledger operativo",
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


def test_document_contains_required_risks():
    text = _text()
    for phrase in [
        "Elegir un bloque demasiado operativo antes de gobernanza",
        "Confundir Runtime Governance con Runtime Activation",
        "Confundir Runtime State Contract con runtime real",
        "Crear observability runtime antes de definir gobernanza",
        "Crear human approval operativo antes de contrato",
        "Crear kill switch operativo antes de audit trail completo",
        "Crear dry-run executor antes de runtime governance",
        "Crear tool/model/context/output contracts antes de readiness governance",
        "Abrir integrations antes de UI/runtime boundaries",
        "Habilitar Market Catalog/BCL runtime antes de gobierno runtime",
        "Reinterpretar READY/E2E/CHAIN como permiso operativo",
        "Incorporar OBLITERATUS por accidente",
        "Mitigacion existente",
        "Mitigacion faltante",
        "Recomendacion",
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
    allowed_preexisting_non_operational = {
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/runtime_executor.py": "prepare-only",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
    }
    for path in [
        "core/runtime_governance.py",
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
        "core/rollback_executor.py",
        "core/process_killer.py",
        "core/job_canceller.py",
        "core/queue_drain.py",
        "core/worker_stop.py",
        "core/scheduler_stop.py",
        "core/runner_stop.py",
        "core/executor_stop.py",
        "core/filesystem_rollback.py",
        "core/git_rollback.py",
        "core/store_rollback.py",
        "core/database_rollback.py",
        "core/memory_rollback.py",
        "core/audit_trail.py",
        "core/audit_logger.py",
        "core/event_log.py",
        "core/event_bus.py",
        "core/telemetry.py",
        "core/metrics_collector.py",
        "core/tracing.py",
        "core/dashboard.py",
        "core/correlation_ledger.py",
        "core/immutable_audit_log.py",
        "core/side_effect_ledger.py",
        "core/dry_run_executor.py",
        "core/dry_run_runner.py",
        "core/dry_run_dispatcher.py",
        "core/dry_run_scheduler.py",
        "core/dry_run_worker.py",
        "core/dry_run_queue.py",
        "core/tool_executor.py",
        "core/tool_registry.py",
        "core/tool_adapter.py",
        "core/model_invoker.py",
        "core/model_router.py",
        "core/model_executor.py",
        "core/inference_runner.py",
        "core/context_builder.py",
        "core/context_injector.py",
        "core/prompt_assembler.py",
        "core/retrieval_engine.py",
        "core/rag_engine.py",
        "core/output_writer.py",
        "core/output_publisher.py",
        "core/output_notifier.py",
        "core/output_delivery.py",
        "core/message_sender.py",
        "core/email_sender.py",
        "core/webhook_client.py",
        "core/provider_client.py",
        "core/browser_operator.py",
        "core/sandbox_runner.py",
        "core/command_executor.py",
        "core/shell.py",
        "core/subprocess_runner.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        candidate = ROOT / path
        if path in allowed_preexisting_non_operational and candidate.exists():
            text = candidate.read_text(encoding="utf-8").lower()
            assert allowed_preexisting_non_operational[path].lower() in text
            continue
        assert not candidate.exists(), path


def test_obliteratus_is_explicitly_excluded_from_operational_roadmap():
    text = _text()
    for phrase in [
        "OBLITERATUS no forma parte de IA_CORE",
        "No es integración",
        "No es dependency",
        "No es adapter",
        "No es provider",
        "No es capability",
        "No es runtime",
        "No es roadmap operativo",
        "No debe aparecer como fuente de logs, aprobación, rollback, kill switch, dry-run, runtime, tool, model, integration ni workflow",
    ]:
        assert phrase in text
