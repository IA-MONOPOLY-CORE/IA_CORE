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
DOC = ROOT / "docs" / "HUMAN_APPROVAL_GATE_PLAN.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_human_approval_gate_plan_document_exists_and_declares_status():
    text = _text()
    for phrase in [
        "HUMAN_APPROVAL_GATE_PLAN_READY",
        "HUMAN_APPROVAL_GATE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_post_security_block_checkpoint",
        "PROMPT 3.40 — Checkpoint integral post-security block",
    ]:
        assert phrase in text


def test_document_contains_human_approval_gate_definition():
    text = _text()
    for phrase in [
        "Human Approval Gate es la capacidad futura de requerir autorización humana explícita",
        "verificable",
        "auditable",
        "antes de permitir acciones sensibles",
    ]:
        assert phrase in text


def test_document_contains_future_actions_requiring_approval():
    text = _text()
    for phrase in [
        "Runtime activation",
        "Runtime execution",
        "Dry-run execution activation",
        "Tool execution",
        "Model invocation",
        "Context injection",
        "Output delivery/publishing",
        "Writes reales",
        "Stores operativos",
        "Memory persistence",
        "Network/API/browser access",
        "Filesystem/env/secrets access",
        "Kill switch operativo",
        "Rollback operativo",
        "Worker/scheduler/runner/queue operations",
        "External integrations: UI-TARS, Hermes, n8n, Home Assistant",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "Any irreversible or externally visible action",
    ]:
        assert phrase in text


def test_document_contains_conceptual_approval_request_shape():
    text = _text()
    for phrase in [
        "approval_request_id",
        "requested_by",
        "requested_at_future_controlled",
        "action_type",
        "target_scope",
        "target_ids",
        "reason",
        "risk_level",
        "security_baseline_ref",
        "policy_check_ref",
        "dry_run_ref optional",
        "kill_switch_ref optional",
        "rollback_manifest_ref optional",
        "audit_trail_ref",
        "expected_side_effects",
        "reversibility",
        "expires_at_future_controlled",
        "metadata_sanitized",
        "No debe implementarse como modulo operativo todavia",
        "No debe escribirse en stores operativos",
        "No debe activar aprobacion real",
        "No debe habilitar runtime",
    ]:
        assert phrase in text


def test_document_contains_conceptual_decisions_and_rules():
    text = _text()
    for phrase in [
        "approval_requested",
        "approval_policy_checked",
        "approval_blocked",
        "approval_granted_simulated",
        "approval_denied_simulated",
        "approval_expired_simulated",
        "approval_revoked_simulated",
        "approval_invalid",
        "approval_granted_simulated no habilita ejecucion real",
        "Ninguna decision conceptual abre runtime",
        "Ninguna decision conceptual ejecuta tools",
        "Ninguna decision conceptual invoca modelos",
        "Ninguna decision conceptual escribe stores",
        "Ninguna decision conceptual activa integraciones",
    ]:
        assert phrase in text


def test_document_contains_minimum_human_evidence():
    text = _text()
    for phrase in [
        "acción solicitada",
        "actor/requested_by",
        "razón",
        "target_scope",
        "target_ids",
        "impacto esperado",
        "riesgo",
        "reversibilidad",
        "contrato aplicable",
        "Security Layer baseline",
        "policy check",
        "dry-run result si existe",
        "kill switch/rollback dependency si aplica",
        "audit trail reference",
        "datos sanitizados",
        "secretos ausentes",
        "raw outputs ausentes",
        "payloads reales ausentes",
        "estado actual del runtime gate",
        "consecuencias de aprobar",
        "consecuencias de rechazar",
    ]:
        assert phrase in text


def test_document_contains_required_dependencies():
    text = _text()
    for phrase in [
        "Security Surface Audit",
        "Agent Permission Contract",
        "Secrets Policy",
        "Prompt Injection Defense",
        "Sandbox Boundary",
        "Tool Boundary",
        "Model Invocation Boundary",
        "Context Boundary",
        "Output Boundary",
        "Runtime Activation Gate",
        "Security Layer Final Checkpoint",
        "Dry-run Execution Contract",
        "Dry-run Execution Contract Full E2E",
        "Observability / Audit Trail Post-Security Audit",
        "Kill Switch / Rollback Contract",
    ]:
        assert phrase in text


def test_document_contains_specific_risks():
    text = _text()
    for phrase in [
        "Aprobar una acción sin evidencia suficiente",
        "Aprobar runtime creyendo que es solo planificación",
        "Aprobar dry-run creyendo que no tiene efectos, pero habilitar efectos reales",
        "Aprobar tool execution sin boundary",
        "Aprobar model invocation sin boundary",
        "Aprobar output delivery sin revisar exposición externa",
        "Aprobar writes/stores sin rollback",
        "Aprobar rollback sin manifest",
        "Aprobar kill switch sin audit trail",
        "Aprobar integraciones externas sin aislamiento",
        "Registrar secretos o payloads reales en approval metadata",
        "Confundir aprobación simulada con aprobación real",
        "Permitir aprobación automática sin humano",
        "Permitir aprobación vencida o revocada",
        "Usar Human Approval Gate como bypass de Security Layer",
        "Incorporar OBLITERATUS como flujo aprobable por accidente",
        "Mitigacion existente",
        "Mitigacion faltante",
        "Recomendacion",
    ]:
        assert phrase in text


def test_document_contains_forbidden_states():
    text = _text()
    for phrase in [
        "approval_gate_active",
        "approval_enabled",
        "human_approval_operational",
        "approval_granted_real",
        "approval_applied",
        "runtime_approved",
        "execution_approved",
        "tool_execution_approved",
        "model_invocation_approved",
        "output_delivery_approved",
        "writes_approved",
        "stores_approved",
        "integration_approved",
        "ready_for_runtime",
        "ready_for_execution",
        "runtime_open",
        "runtime_active",
        "operations_enabled",
        "gate_open",
    ]:
        assert phrase in text


def test_document_contains_explicit_prohibitions():
    text = _text()
    for phrase in [
        "human approval operativo",
        "approval gate active",
        "approval workflow real",
        "approval UI real",
        "approval API real",
        "approval endpoint real",
        "approval buttons reales",
        "approval store operativo",
        "permission escalation",
        "automatic approval",
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


def test_no_human_approval_operational_modules_were_created():
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
        "core/model_invoker.py",
        "core/context_builder.py",
        "core/output_delivery.py",
        "core/kill_switch.py",
        "core/rollback_controller.py",
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



