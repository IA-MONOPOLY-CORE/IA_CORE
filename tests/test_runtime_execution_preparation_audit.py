from pathlib import Path
import importlib

from core.market_catalog import (
    MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED,
    MARKET_CATALOG_RUNTIME_ENABLED,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_AUDIT.md"
PHASE4_DOC = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_4_RUNTIME_EXECUTION_PREPARATION_PLAN.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def _assert_false_flags(module_name: str) -> None:
    module = importlib.import_module(module_name)
    flags = [
        getattr(module, name)
        for name in dir(module)
        if name.isupper() and (name.endswith("_ENABLED") or name.endswith("_OPERATIONAL"))
    ]
    assert flags, module_name
    assert flags == [False] * len(flags), module_name


def test_audit_document_exists_and_declares_status():
    text = _text()
    for phrase in [
        "Runtime Execution Preparation Audit",
        "RUNTIME_EXECUTION_PREPARATION_AUDIT_COMPLETED",
        "RUNTIME_EXECUTION_PREPARATION_BASELINE_VERIFIED",
        "ready_for_runtime_execution_preparation_contract",
        "PROMPT 4.1 — Contrato de Runtime Execution Preparation no-operativo",
    ]:
        assert phrase in text


def test_definition_is_non_operational():
    text = _text()
    for phrase in [
        "Runtime Execution Preparation es la futura capa no-operativa",
        "Runtime Execution Preparation no es Runtime Execution",
        "Runtime Execution Preparation no activa runtime",
        "Runtime Execution Preparation no ejecuta dry-run real",
        "Runtime Execution Preparation no crea runner",
        "Runtime Execution Preparation no crea scheduler",
        "Runtime Execution Preparation no crea worker",
        "Runtime Execution Preparation no crea queue",
        "Runtime Execution Preparation no crea executor",
        "Runtime Execution Preparation no invoca tools",
        "Runtime Execution Preparation no invoca modelos",
        "Runtime Execution Preparation no inyecta contexto",
        "Runtime Execution Preparation no entrega outputs",
        "Runtime Execution Preparation no escribe stores operativos",
    ]:
        assert phrase in text


def test_sources_package_states_readiness_and_matrix_are_documented():
    text = _text()
    for phrase in REQUIRED_SOURCES:
        assert phrase in text
    for phrase in PACKAGE_COMPONENTS:
        assert phrase in text
    for phrase in CONCEPTUAL_STATES:
        assert phrase in text
    for phrase in FORBIDDEN_STATES:
        assert phrase in text
    for phrase in [
        "ready_for_runtime_execution_preparation_contract",
        "ready_for_runtime_execution_preparation_contract_e2e",
        "ready_for_runtime",
        "ready_for_runtime_activation",
        "ready_for_execution",
        "ready_for_dry_run_execution",
        "runtime_execution_preparation_operational",
    ]:
        assert phrase in text
    for index in range(1, 45):
        assert f"| {index}. " in text


def test_metadata_forbidden_data_gaps_risks_and_recommendation_are_documented():
    text = _text()
    for phrase in METADATA_FIELDS:
        assert phrase in text
    for phrase in FORBIDDEN_DATA:
        assert phrase in text
    for phrase in GAPS:
        assert phrase in text
    for phrase in RISKS:
        assert phrase in text
    assert "PROMPT 4.1 — Contrato de Runtime Execution Preparation no-operativo" in text
    assert "ser contract-only" in text
    assert "no tener side effects" in text


def test_forbidden_modules_blockers_and_no_contract_yet():
    text = _text()
    for path in FORBIDDEN_MODULES:
        assert path in text
    for blocker in BLOCKERS:
        assert blocker in text
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
    assert not (ROOT / "core" / "runtime_execution_preparation_contract.py").exists()


def test_core_contracts_and_boundaries_remain_blocked():
    for module_name in [
        "core.runtime_governance_contract",
        "core.runtime_state_contract",
        "core.observability_contract",
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


def test_market_catalog_business_composition_and_obliteratus_remain_excluded():
    text = _text()
    assert MARKET_CATALOG_RUNTIME_ENABLED is False
    assert MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED is False
    for phrase in [
        "Market Catalog planned_not_active",
        "Market Catalog runtime",
        "Business Composition Layer future/not runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS no forma parte de Runtime Execution Preparation",
        "No es execution source",
        "No es integration",
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
    ]:
        assert phrase in text


def test_phase4_plan_document_is_created_and_non_operational():
    assert PHASE4_DOC.exists()
    text = PHASE4_DOC.read_text(encoding="utf-8")
    for phrase in [
        "PHASE_4_RUNTIME_EXECUTION_PREPARATION_STARTED",
        "RUNTIME_EXECUTION_PREPARATION_AUDIT_COMPLETED",
        "ready_for_runtime_execution_preparation_contract",
        "PROMPT 4.1 — Contrato de Runtime Execution Preparation no-operativo",
        "Phase 3 transitioned to Phase 4 through PROMPT 4.0",
        "Phase 4 starts with Runtime Execution Preparation Audit",
        "No runtime activation occurred",
    ]:
        assert phrase in text


REQUIRED_SOURCES = [
    "Next Architecture Block Planning 3.49",
    "Runtime Governance Block Integral Checkpoint",
    "Runtime Governance Contract",
    "Runtime Governance Contract Full E2E",
    "Runtime State Contract",
    "Runtime State Contract Full E2E",
    "Observability Contract",
    "Observability Contract Full E2E",
    "Runtime Activation Gate",
    "Operational Readiness Gate",
    "Dry-run Execution Contract",
    "Dry-run Execution Contract Full E2E",
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
    "Human Approval Gate Plan",
    "Kill Switch / Rollback Contract",
    "Security Layer Final Checkpoint",
    "Agent Permission Contract",
    "Secrets Policy",
    "Prompt Injection Defense",
    "Sandbox Boundary",
    "Tool Boundary",
    "Model Invocation Boundary",
    "Context Boundary",
    "Output Boundary",
    "Observability / Audit Trail Post-Security Audit",
    "Market Catalog planned_not_active",
    "Business Composition Layer future/not runtime",
]

PACKAGE_COMPONENTS = [
    "preparation_id",
    "intent_ref",
    "attempt_ref optional",
    "runtime_governance_ref",
    "runtime_state_ref",
    "observability_ref",
    "runtime_activation_gate_ref",
    "security_baseline_ref",
    "agent_permission_ref",
    "sandbox_boundary_ref",
    "tool_boundary_ref",
    "model_boundary_ref",
    "context_boundary_ref",
    "output_boundary_ref",
    "secrets_policy_ref",
    "prompt_injection_defense_ref",
    "human_approval_ref optional",
    "kill_switch_ref",
    "rollback_ref",
    "dry_run_ref optional",
    "execution_scope",
    "execution_mode",
    "execution_risk_level",
    "required_dependencies",
    "missing_dependencies",
    "blocked_capabilities",
    "forbidden_readiness",
    "metadata_sanitized",
    "prepared_snapshot",
]

CONCEPTUAL_STATES = [
    "runtime_execution_preparation_uninitialized",
    "runtime_execution_preparation_governance_required",
    "runtime_execution_preparation_state_required",
    "runtime_execution_preparation_observability_required",
    "runtime_execution_preparation_security_required",
    "runtime_execution_preparation_intent_required",
    "runtime_execution_preparation_attempt_required",
    "runtime_execution_preparation_boundaries_required",
    "runtime_execution_preparation_human_approval_required",
    "runtime_execution_preparation_kill_switch_required",
    "runtime_execution_preparation_rollback_required",
    "runtime_execution_preparation_dry_run_required",
    "runtime_execution_preparation_ready_simulated",
    "runtime_execution_preparation_blocked",
    "runtime_execution_preparation_invalid",
    "runtime_execution_preparation_archived_simulated",
]

FORBIDDEN_STATES = [
    "runtime_execution_preparation_active",
    "runtime_execution_preparation_running",
    "runtime_execution_preparation_executing",
    "runtime_execution_preparation_live",
    "runtime_execution_preparation_open",
    "runtime_execution_preparation_enabled",
    "runtime_execution_preparation_operational",
    "runtime_execution_preparation_runtime_started",
    "runtime_execution_preparation_dry_run_started",
    "runtime_execution_preparation_tool_executing",
    "runtime_execution_preparation_model_invoking",
    "runtime_execution_preparation_context_injecting",
    "runtime_execution_preparation_output_delivering",
    "runtime_execution_preparation_writing",
    "runtime_execution_preparation_store_mutating",
    "runtime_execution_preparation_network_active",
    "runtime_execution_preparation_api_active",
    "runtime_execution_preparation_browser_active",
    "runtime_execution_preparation_filesystem_active",
    "runtime_execution_preparation_env_active",
    "runtime_execution_preparation_secret_active",
    "runtime_execution_preparation_integration_active",
]

METADATA_FIELDS = [
    "runtime_execution_preparation_id",
    "intent_id",
    "attempt_id optional",
    "runtime_gate_ref",
    "preparation_reason",
    "preparation_scope",
    "preparation_mode",
    "preparation_risk_level",
]

FORBIDDEN_DATA = [
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "credential",
    "credentials",
    "private_key",
    "raw_payload",
    "payload",
    "raw_output",
    "output",
    "file_content",
    "env",
    "environment",
    "cookie",
    "authorization",
    "bearer",
    "raw_prompt",
    "prompt",
    "raw_completion",
    "completion",
    "model_response",
    "tool_response",
    "external_response",
    "browser_content",
    "filesystem_content",
    "personal_data_unsanitized",
]

GAPS = [
    "No existe Runtime Execution Preparation Contract.",
    "No existe Runtime Execution Preparation E2E.",
    "No existe preparation package schema.",
    "No existe preparation snapshot contract.",
    "No existe preparation dependency validator.",
    "No existe preparation metadata sanitizer propio.",
    "No existe preparation readiness validator.",
    "No existe preparation risk classifier.",
    "No existe preparation boundary aggregator.",
    "No existe preparation audit reference contract.",
    "No existe preparation handoff hacia dry-run.",
    "No existe preparation handoff hacia human approval.",
    "No existe preparation handoff hacia runtime activation gate.",
    "No existe preparation read model/projection.",
]

RISKS = [
    "Confundir preparación de ejecución con ejecución real.",
    "Crear runner/scheduler/worker/queue/executor antes de contrato.",
    "Habilitar dry-run real desde preparación.",
    "Habilitar tools/modelos/context/output desde preparación.",
    "Usar preparation package como bypass de Runtime Governance.",
    "Usar preparation package como bypass de Runtime State.",
    "Usar preparation package como bypass de Observability.",
    "Usar preparation package como bypass de Human Approval.",
    "Usar preparation package como bypass de Kill Switch/Rollback.",
    "Usar preparation package como bypass de Runtime Activation Gate.",
    "Guardar metadata peligrosa.",
    "Guardar raw payloads/raw outputs/prompts/model responses.",
    "Habilitar writes/stores/memory/network/browser/secrets.",
    "Activar integraciones desde preparation.",
    "Incorporar OBLITERATUS como execution source por accidente.",
]

FORBIDDEN_MODULES = [
    "core/runtime_execution_preparation_contract.py",
    "core/runtime_execution_preparation.py",
    "core/runtime_execution_preparation_package.py",
    "core/runtime_execution_preparation_snapshot.py",
    "core/runtime_execution_preparation_validator.py",
    "core/runtime_execution_preparation_store.py",
    "core/runtime_execution_preparation_writer.py",
    "core/runtime_execution_preparation_reader.py",
    "core/runtime_execution_preparation_handoff.py",
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

BLOCKERS = [
    "runtime execution preparation contract activo",
    "runtime execution preparation operativo",
    "runtime execution preparation package operativo",
    "runtime execution preparation snapshot operativo",
    "runtime execution preparation validator operativo",
    "runtime execution preparation store operativo",
    "runtime execution preparation writer operativo",
    "runtime execution preparation reader operativo",
    "runtime execution preparation handoff operativo",
    "runtime execution",
    "runtime activation",
    "runtime controller",
    "runtime manager",
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
    "runtime governance operativo",
    "runtime governance activation",
    "runtime governance execution",
    "runtime state operativo",
    "runtime state activation",
    "runtime state mutation real",
    "runtime state store operativo",
    "runtime state writer operativo",
    "runtime state reader operativo",
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
    "log write real",
    "event publish real",
    "store write real",
    "store mutation real",
    "human approval operativo",
    "approval gate active",
    "approval workflow real",
    "approval UI real",
    "approval API real",
    "approval endpoint real",
    "approval store operativo",
    "automatic approval",
    "permission escalation",
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
