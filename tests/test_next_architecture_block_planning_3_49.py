from pathlib import Path
import importlib

import core.observability_contract as observability
import core.runtime_governance_contract as governance
import core.runtime_state_contract as runtime_state
from core.market_catalog import MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED, MARKET_CATALOG_RUNTIME_ENABLED


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLANNING_3_49.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def _assert_false_flags(module_name: str) -> None:
    module = importlib.import_module(module_name)
    false_flags = [
        getattr(module, name)
        for name in dir(module)
        if name.isupper() and (name.endswith("_ENABLED") or name.endswith("_OPERATIONAL"))
    ]
    assert false_flags, module_name
    assert false_flags == [False] * len(false_flags), module_name


def test_document_exists_and_declares_selected_path():
    text = _text()
    for phrase in [
        "Next Architecture Block Planning",
        "NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED",
        "NEXT_ARCHITECTURE_BLOCK_SELECTED",
        "PHASE_4_RUNTIME_EXECUTION_PREPARATION_SELECTED",
        "ready_for_phase_4_0",
        "PROMPT 4.0 — Auditoría de Runtime Execution Preparation",
    ]:
        assert phrase in text
    assert "NEXT_ARCHITECTURE_BLOCK_PLANNING_REQUIRES_INTERMEDIATE_CHECKPOINT" in text
    assert "PROMPT 3.49.1 — Checkpoint intermedio previo a 4.0" in text
    assert "no declara `NEXT_ARCHITECTURE_BLOCK_PLANNING_REQUIRES_INTERMEDIATE_CHECKPOINT`" in text


def test_document_contains_required_baseline():
    text = _text()
    for phrase in [
        "Security Layer final checkpoint",
        "Post-Security Block integral checkpoint",
        "Runtime Governance Block integral checkpoint",
        "Runtime Governance Contract + E2E",
        "Runtime State Contract + E2E",
        "Observability Contract + E2E",
        "Runtime Activation Gate",
        "Operational Readiness Gate",
        "Dry-run Execution Contract + E2E",
        "Kill Switch / Rollback Contract",
        "Human Approval Gate Plan",
        "Output Boundary",
        "Context Boundary",
        "Model Invocation Boundary",
        "Tool Boundary",
        "Sandbox Boundary",
        "Prompt Injection Defense",
        "Secrets Policy",
        "Agent Permission Contract",
        "Execution Intent",
        "Execution Attempt",
        "Attempt Factory",
        "Attempt Store write-safe",
        "Lifecycle Writer",
        "Execution Result",
        "Execution Result Projection",
        "Execution History View",
        "Internal Backend Read Model",
        "Market Catalog planned_not_active",
        "Business Composition Layer future/not runtime",
    ]:
        assert phrase in text


def test_document_contains_candidates_and_selection_criteria():
    text = _text()
    for phrase in [
        "Runtime Execution / Dry-run Runtime Block",
        "Human Approval Contract Block",
        "Audit Trail / Observability Runtime Preparation Block",
        "Runtime Activation Preparation Block",
        "Integration Governance Block",
        "Tool Execution Preparation Block",
        "Model Invocation Runtime Preparation Block",
        "Output Delivery Preparation Block",
        "Memory / Store Governance Block",
        "UI / Operator Experience Runtime Control Block",
        "selected",
        "deferred",
        "blocked",
        "future-only",
        "active runtime real prematuramente",
        "active tools/modelos/context/output sin aprobacion",
        "escriba stores operativos sin contrato",
        "requiera integraciones reales",
        "dependa de UI-TARS/Hermes/n8n/Home Assistant",
        "convierta Observability en runtime antes de tiempo",
        "use OBLITERATUS",
        "saltee human approval",
        "saltee kill switch/rollback",
        "saltee audit trail",
        "saltee Runtime Activation Gate",
    ]:
        assert phrase in text


def test_document_contains_expected_decision_and_no_runtime_rule():
    text = _text()
    for phrase in [
        "PHASE 4 — Runtime Execution Preparation Block",
        "PROMPT 4.0 — Auditoría de Runtime Execution Preparation",
        "4.0 NO debe activar runtime real",
        "4.0 NO debe ejecutar dry-run real",
        "4.0 NO debe crear runner/scheduler/worker/queue/executor operativo",
        "4.0 debe empezar con auditoria",
        "4.0 debe consumir como baseline Runtime Governance, Runtime State y Observability",
        "No hace falta `PROMPT 3.49.1 — Checkpoint intermedio previo a 4.0`",
    ]:
        assert phrase in text


def test_document_contains_all_blockers_and_forbidden_modules():
    text = _text()
    for phrase in BLOCKERS:
        assert phrase in text
    for module in FORBIDDEN_MODULES:
        assert module in text


def test_contract_flags_remain_false():
    assert governance.RUNTIME_GOVERNANCE_CONTRACT_READY is True
    assert runtime_state.RUNTIME_STATE_CONTRACT_READY is True
    assert observability.OBSERVABILITY_CONTRACT_READY is True
    for module_name in [
        "core.runtime_governance_contract",
        "core.runtime_state_contract",
        "core.observability_contract",
    ]:
        _assert_false_flags(module_name)


def test_runtime_gate_dry_run_kill_switch_and_boundaries_remain_blocked():
    for module_name in [
        "core.runtime_activation_gate",
        "core.dry_run_execution_contract",
        "core.kill_switch_rollback_contract",
        "core.output_boundary",
        "core.context_boundary",
        "core.model_invocation_boundary",
        "core.tool_boundary",
        "core.sandbox_boundary",
        "core.prompt_injection_defense",
        "core.secrets_policy",
        "core.agent_permission_contract",
    ]:
        _assert_false_flags(module_name)


def test_no_forbidden_operational_modules_created_except_allowed_preexisting():
    allowed_preexisting = {
        "core/runtime_executor.py": "prepare-only",
        "core/approval_workflow.py": "Helpers no mutantes",
    }
    for path in FORBIDDEN_MODULES:
        candidate = ROOT / path
        if path in allowed_preexisting and candidate.exists():
            assert allowed_preexisting[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_market_catalog_and_business_composition_remain_non_runtime():
    text = _text()
    assert MARKET_CATALOG_RUNTIME_ENABLED is False
    assert MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED is False
    assert "Market Catalog planned_not_active" in text
    assert "Market Catalog runtime" in text
    assert "Business Composition Layer future/not runtime" in text
    assert "Business Composition Layer runtime" in text
    assert "Business Composition Layer future-only o planned_not_active" not in text


def test_obliteratus_exclusion_is_explicit_for_next_block():
    text = _text()
    for phrase in [
        "OBLITERATUS no forma parte del siguiente bloque arquitectónico",
        "No es integración",
        "No es integracion",
        "No es dependency",
        "No es adapter",
        "No es provider",
        "No es capability",
        "No es runtime",
        "No es roadmap operativo",
        "No es governance source",
        "No es state source",
        "No es observability source",
        "No es event source",
        "No es audit source",
        "No es execution source",
        "tool",
        "model",
        "workflow",
        "execution",
    ]:
        assert phrase in text


BLOCKERS = [
    "runtime governance operativo",
    "runtime governance activation",
    "runtime governance execution",
    "runtime state operativo",
    "runtime state activation",
    "runtime state mutation real",
    "runtime state store operativo",
    "runtime state writer operativo",
    "runtime state reader operativo",
    "runtime state transition real",
    "runtime state event bus",
    "observability operativo",
    "observability runtime",
    "audit trail operativo",
    "logger operativo",
    "event log operativo",
    "event bus operativo",
    "telemetry real",
    "metrics collector",
    "tracing real",
    "dashboard operativo",
    "immutable audit log operativo",
    "correlation ledger runtime",
    "side-effect ledger operativo",
    "redaction engine operativo",
    "log write real",
    "event publish real",
    "store write real",
    "store mutation real",
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
    "runtime event schema operativo",
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
    "manifest mutation",
    "database rollback",
    "memory rollback",
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
]


FORBIDDEN_MODULES = [
    "core/runtime_execution.py",
    "core/runtime_executor.py",
    "core/runtime_runner.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_dispatcher.py",
    "core/runtime_controller.py",
    "core/runtime_manager.py",
    "core/runtime_event_bus.py",
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
    "core/observability_event.py",
    "core/observability_event_schema.py",
    "core/observability_snapshot.py",
    "core/observability_store.py",
    "core/observability_writer.py",
    "core/observability_reader.py",
    "core/observability_logger.py",
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
    "core/redaction_engine.py",
    "core/ui_tars_adapter.py",
    "core/hermes_adapter.py",
    "core/n8n_adapter.py",
    "core/home_assistant_adapter.py",
]
