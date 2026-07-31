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
DOC = ROOT / "docs" / "POST_SECURITY_BLOCK_INTEGRAL_CHECKPOINT.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_integral_checkpoint_document_exists_and_declares_status():
    text = _text()
    for phrase in [
        "POST_SECURITY_BLOCK_INTEGRAL_CHECKPOINT_PASSED",
        "POST_SECURITY_BLOCK_CHAIN_READY",
        "ready_for_next_architecture_block_planning",
        "PROMPT 3.41 — Planificación del siguiente bloque arquitectónico",
    ]:
        assert phrase in text


def test_document_contains_required_statuses():
    text = _text()
    for phrase in [
        "SECURITY_LAYER_FINAL_CHECKPOINT_PASSED",
        "SECURITY_LAYER_PRE_RUNTIME_CHAIN_READY",
        "POST_SECURITY_LAYER_BLOCK_PLAN_READY",
        "SECURITY_LAYER_CONSUMED_AS_PRE_RUNTIME_BASELINE",
        "POST_SECURITY_LAYER_ARCHITECTURE_AUDIT_COMPLETED",
        "POST_SECURITY_LAYER_ARCHITECTURE_BASELINE_VERIFIED",
        "RUNTIME_FOUNDATION_PLAN_READY",
        "RUNTIME_FOUNDATION_NO_ACTIVATION_CONFIRMED",
        "DRY_RUN_EXECUTION_ARCHITECTURE_AUDIT_COMPLETED",
        "DRY_RUN_EXECUTION_ARCHITECTURE_BASELINE_VERIFIED",
        "DRY_RUN_EXECUTION_CONTRACT_READY",
        "DRY_RUN_EXECUTION_NO_OPERATIONAL_CONFIRMED",
        "DRY_RUN_EXECUTION_CONTRACT_FULL_E2E_PASSED",
        "DRY_RUN_EXECUTION_CONTRACT_CHAIN_READY",
        "OBSERVABILITY_AUDIT_TRAIL_AUDIT_COMPLETED",
        "OBSERVABILITY_AUDIT_TRAIL_BASELINE_VERIFIED",
        "KILL_SWITCH_ROLLBACK_CONTRACT_READY",
        "KILL_SWITCH_ROLLBACK_NO_OPERATIONAL_CONFIRMED",
        "HUMAN_APPROVAL_GATE_PLAN_READY",
        "HUMAN_APPROVAL_GATE_NO_OPERATIONAL_CONFIRMED",
        "POST_SECURITY_BLOCK_INTEGRAL_CHECKPOINT_PASSED",
        "POST_SECURITY_BLOCK_CHAIN_READY",
    ]:
        assert phrase in text


def test_document_contains_integral_chain():
    text = _text()
    for phrase in [
        "3.31 Security Layer final checkpoint pre-runtime",
        "→ 3.32 Post-Security Layer block plan",
        "→ 3.33 Post-Security Layer architecture audit",
        "→ 3.34 Runtime Foundation plan without activation",
        "→ 3.35 Dry-run execution architecture audit",
        "→ 3.36 Dry-run execution non-operational contract",
        "→ 3.36.1 Dry-run execution contract full E2E checkpoint",
        "→ 3.37 Observability/audit trail post-security audit",
        "→ 3.38 Kill switch/rollback future-only contract",
        "→ 3.39 Human Approval Gate future-only plan",
        "→ 3.40 Post-Security block integral checkpoint",
        "pre-runtime",
        "contract-only where applicable",
        "future-only where applicable",
        "no-operational",
        "security-layer-dependent",
        "no side effects",
        "no runtime activation",
        "no dry-run activation",
        "no external integrations",
    ]:
        assert phrase in text


def test_document_contains_built_or_documented_pieces():
    text = _text()
    for phrase in [
        "1. Security Layer final baseline",
        "2. Post-Security block plan",
        "3. Post-Security architecture audit",
        "4. Runtime Foundation plan sin activación",
        "5. Dry-run execution architecture audit",
        "6. Dry-run execution contract no-operativo",
        "7. Dry-run execution contract full E2E",
        "8. Observability/audit trail post-security audit",
        "9. Kill switch/rollback future-only contract",
        "10. Human Approval Gate future-only plan",
        "Documento/modulo/test asociado",
        "Estado",
        "Veredicto",
        "Readiness",
        "Activa runtime",
        "Efectos reales",
        "Dependencia Security Layer",
        "Proximo uso futuro",
    ]:
        assert phrase in text


def test_document_contains_all_final_blockers():
    text = _text()
    for phrase in [
        "runtime activation",
        "runtime execution",
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
        "approval buttons reales",
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
        "runtime event schema operativo",
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


def test_no_operational_modules_were_created_unless_preexisting_non_mutating():
    allowed_preexisting_non_operational = {
        "core/approval_workflow.py": "Helpers no mutantes",
    }
    for path in [
        "core/human_approval_gate.py",
        "core/human_approval_contract.py",
        "core/human_approval_store.py",
        "core/human_approval_audit.py",
        "core/approval_request.py",
        "core/approval_decision.py",
        "core/approval_workflow.py",
        "core/approval_notifier.py",
        "core/approval_ui.py",
        "core/approval_api.py",
        "core/approval_endpoint.py",
        "core/approval_button.py",
        "core/approval_policy.py",
        "core/approval_runtime.py",
        "core/permission_escalation.py",
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
        "core/manifest_mutator.py",
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
        "core/runtime_event_schema.py",
        "core/side_effect_ledger.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/orchestrator.py",
        "core/executor.py",
        "core/dispatcher.py",
        "core/background_jobs.py",
        "core/autonomous_loop.py",
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
            text = candidate.read_text(encoding="utf-8")
            assert allowed_preexisting_non_operational[path] in text
            continue
        assert not candidate.exists(), path


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


def test_document_does_not_declare_active_or_ready_runtime_states():
    text = _text().lower()
    forbidden_active_forms = [
        "estado: ready_for_runtime",
        "readiness: ready_for_runtime",
        "estado: ready_for_execution",
        "readiness: ready_for_execution",
        "estado: runtime_open",
        "estado: runtime_active",
        "runtime_enabled = true",
        "execution_enabled = true",
        "operations_enabled = true",
        "gate_open = true",
        "dry_run_execution_enabled = true",
        "kill_switch_enabled = true",
        "rollback_enabled = true",
        "approval_enabled = true",
        "human_approval_operational = true",
        "tool_execution_enabled = true",
        "model_invocation_enabled = true",
        "context_injection_enabled = true",
        "output_delivery_enabled = true",
        "writes_enabled = true",
        "stores_enabled = true",
        "network_enabled = true",
        "api_enabled = true",
        "secret_access_enabled = true",
        "estado: integration_approved",
        "market_catalog_active = true",
        "business_composition_enabled = true",
    ]
    for phrase in forbidden_active_forms:
        assert phrase not in text
