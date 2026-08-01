from pathlib import Path
import importlib
import json
import os

import pytest

import core.observability_contract as observability
import core.runtime_governance_contract as governance
import core.runtime_state_contract as runtime_state


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_GOVERNANCE_BLOCK_INTEGRAL_CHECKPOINT.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def _json_safe(payload):
    json.dumps(payload, sort_keys=True)


def _state_metadata(**overrides):
    data = {
        "runtime_state_id": "runtime_state_block_checkpoint",
        "runtime_governance_ref": "runtime_governance_contract",
        "runtime_gate_ref": "runtime_gate_closed",
        "security_baseline_ref": "security_layer_final",
        "state_reason": "integral checkpoint",
        "state_scope": "future_runtime",
        "state_risk_level": runtime_state.RuntimeStateRiskLevel.MEDIUM,
        "metadata_sanitized": {"purpose": "integral_checkpoint"},
        "intent_id": "intent_checkpoint",
        "attempt_id": "attempt_checkpoint",
        "lifecycle_ref": "lifecycle_checkpoint",
        "result_ref": "result_checkpoint",
        "projection_ref": "projection_checkpoint",
        "dry_run_ref": "dry_run_contract",
        "human_approval_ref": "human_approval_plan",
        "audit_trail_ref": "audit_trail_future",
        "kill_switch_ref": "kill_switch_contract",
        "rollback_ref": "rollback_contract",
    }
    data.update(overrides)
    return runtime_state.build_runtime_state_metadata(**data)


def _observability_metadata(**overrides):
    data = {
        "observability_event_id": "observability_event_block_checkpoint",
        "correlation_id": "correlation_block_checkpoint",
        "causation_id": "causation_block_checkpoint",
        "event_type": observability.ObservabilityEventType.CONTRACT_INITIALIZED,
        "event_source": "tests.test_runtime_governance_block_integral_checkpoint",
        "event_scope": "future_runtime",
        "actor_ref": "actor_checkpoint",
        "runtime_governance_ref": "runtime_governance_contract",
        "runtime_state_ref": "runtime_state_contract",
        "runtime_gate_ref": "runtime_gate_closed",
        "security_baseline_ref": "security_layer_final",
        "policy_check_ref": "policy_check_sanitized",
        "dry_run_ref": "dry_run_contract",
        "attempt_id": "attempt_checkpoint",
        "lifecycle_ref": "lifecycle_checkpoint",
        "result_ref": "result_checkpoint",
        "projection_ref": "projection_checkpoint",
        "human_approval_ref": "human_approval_plan",
        "kill_switch_ref": "kill_switch_contract",
        "rollback_ref": "rollback_contract",
        "event_reason": "integral checkpoint",
        "event_risk_level": observability.ObservabilityRiskLevel.MEDIUM,
        "metadata_sanitized": {"purpose": "integral_checkpoint"},
    }
    data.update(overrides)
    return observability.build_observability_metadata(**data)


def test_document_exists_and_declares_integral_status():
    text = _text()
    for phrase in [
        "Runtime Governance Block Integral Checkpoint",
        "RUNTIME_GOVERNANCE_BLOCK_INTEGRAL_CHECKPOINT_PASSED",
        "RUNTIME_GOVERNANCE_BLOCK_CHAIN_READY",
        "ready_for_next_architecture_block_planning",
        "PROMPT 3.49 — Planificación siguiente bloque arquitectónico",
    ]:
        assert phrase in text


def test_document_contains_component_states_and_readiness_chain():
    text = _text()
    for phrase in [
        "RUNTIME_GOVERNANCE_CONTRACT_READY",
        "RUNTIME_GOVERNANCE_NO_OPERATIONAL_CONFIRMED",
        "RUNTIME_GOVERNANCE_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_GOVERNANCE_CONTRACT_CHAIN_READY",
        "RUNTIME_STATE_CONTRACT_AUDIT_COMPLETED",
        "RUNTIME_STATE_BASELINE_VERIFIED",
        "RUNTIME_STATE_CONTRACT_READY",
        "RUNTIME_STATE_NO_OPERATIONAL_CONFIRMED",
        "RUNTIME_STATE_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_STATE_CONTRACT_CHAIN_READY",
        "OBSERVABILITY_CONTRACT_AUDIT_COMPLETED",
        "OBSERVABILITY_CONTRACT_BASELINE_VERIFIED",
        "OBSERVABILITY_CONTRACT_READY",
        "OBSERVABILITY_NO_OPERATIONAL_CONFIRMED",
        "OBSERVABILITY_CONTRACT_FULL_E2E_PASSED",
        "OBSERVABILITY_CONTRACT_CHAIN_READY",
        "ready_for_runtime_governance_contract",
        "ready_for_runtime_governance_contract_e2e",
        "ready_for_runtime_state_contract_audit",
        "ready_for_runtime_state_contract",
        "ready_for_runtime_state_contract_e2e",
        "ready_for_observability_contract_audit",
        "ready_for_observability_contract",
        "ready_for_observability_contract_e2e",
        "ready_for_runtime_governance_block_integral_checkpoint",
        "ready_for_next_architecture_block_planning",
    ]:
        assert phrase in text


def test_document_contains_all_integral_scope_items_and_matrix_dimensions():
    text = _text()
    for phrase in [
        "Runtime Governance Audit",
        "Runtime Governance Contract",
        "Runtime Governance Contract E2E",
        "Runtime State Contract Audit",
        "Runtime State Contract",
        "Runtime State Contract E2E",
        "Observability Contract Audit",
        "Observability Contract",
        "Observability Contract E2E",
        "Conexion con Runtime Activation Gate",
        "Conexion con Security Layer",
        "Conexion con Dry-run Contract",
        "Conexion con Human Approval Plan",
        "Conexion con Kill Switch/Rollback Contract",
        "Conexion con Output Boundary",
        "Conexion con Context/Model/Tool/Sandbox boundaries",
        "Conexion con Secrets Policy",
        "Conexion con Prompt Injection Defense",
        "Conexion con attempts/lifecycle/results/projections/read models",
        "Ausencia total de runtime operativo",
        "Ausencia total de side effects reales",
        "Ausencia total de integraciones activas",
        "Exclusion de OBLITERATUS",
    ]:
        assert phrase in text
    for dimension in [
        "1. Governance contract status",
        "2. Governance E2E status",
        "3. Runtime State audit status",
        "4. Runtime State contract status",
        "5. Runtime State E2E status",
        "6. Observability audit status",
        "7. Observability contract status",
        "8. Observability E2E status",
        "9. Default-deny consistency",
        "10. Allowed conceptual states/events",
        "11. Forbidden operational states/events",
        "12. Forbidden readiness",
        "13. Blocked capabilities",
        "14. Metadata sanitization",
        "15. Secret/raw payload/raw output exclusion",
        "16. JSON-safe serialization",
        "17. Determinism",
        "18. No side effects",
        "19. No runtime activation",
        "20. No runtime execution",
        "21. No dry-run activation",
        "22. No human approval runtime",
        "23. No kill switch/rollback runtime",
        "24. No observability runtime",
        "25. No logs/event bus/telemetry",
        "26. No tools/models/context/output",
        "27. No writes/stores/memory",
        "28. No network/API/browser",
        "29. No filesystem/env/secrets",
        "30. No UI/device control",
        "31. No integrations",
        "32. Market Catalog remains planned/not runtime",
        "33. Business Composition Layer remains future/not runtime",
        "34. OBLITERATUS exclusion",
        "35. Documentation chain",
        "36. Test chain",
        "37. Long suite validation policy",
        "38. Next block readiness",
        "Estado | Evidencia | Archivos asociados | Riesgo residual | Decision",
    ]:
        assert dimension in text


def test_document_contains_integral_blockers_and_forbidden_modules():
    text = _text()
    for phrase in [
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
    ]:
        assert phrase in text
    for module in FORBIDDEN_MODULES:
        assert module in text


def test_contract_imports_status_verdict_readiness_and_flags_are_safe():
    before = set(os.listdir(ROOT))
    modules = [
        importlib.import_module("core.runtime_governance_contract"),
        importlib.import_module("core.runtime_state_contract"),
        importlib.import_module("core.observability_contract"),
    ]
    after = set(os.listdir(ROOT))
    assert before == after
    assert governance.RUNTIME_GOVERNANCE_CONTRACT_READY is True
    assert runtime_state.RUNTIME_STATE_CONTRACT_READY is True
    assert observability.OBSERVABILITY_CONTRACT_READY is True
    statuses = [
        governance.runtime_governance_contract_status(),
        runtime_state.runtime_state_contract_status(),
        observability.observability_contract_status(),
    ]
    for status in statuses:
        _json_safe(status)
        assert status["operational"] is False
        assert "status" in status
        assert "verdict" in status
        assert "readiness" in status
    for module in modules:
        false_flags = [
            getattr(module, name)
            for name in dir(module)
            if name.isupper() and (name.endswith("_ENABLED") or name.endswith("_OPERATIONAL"))
        ]
        assert false_flags
        assert false_flags == [False] * len(false_flags)


def test_contract_snapshots_are_json_safe_and_deterministic():
    governance_one = governance.runtime_governance_to_dict(governance.build_runtime_governance_snapshot())
    governance_two = governance.runtime_governance_to_dict(governance.build_runtime_governance_snapshot())
    state_one = runtime_state.runtime_state_to_dict(runtime_state.build_runtime_state_contract_snapshot())
    state_two = runtime_state.runtime_state_to_dict(runtime_state.build_runtime_state_contract_snapshot())
    obs_one = observability.observability_to_dict(observability.build_observability_contract_snapshot())
    obs_two = observability.observability_to_dict(observability.build_observability_contract_snapshot())
    assert governance_one == governance_two
    assert state_one == state_two
    assert obs_one == obs_two
    for payload in [governance_one, state_one, obs_one]:
        _json_safe(payload)
        assert payload["operational"] is False
    assert runtime_state.runtime_state_allowed_states() == runtime_state.runtime_state_allowed_states()
    assert runtime_state.runtime_state_forbidden_states() == runtime_state.runtime_state_forbidden_states()
    assert runtime_state.runtime_state_allowed_transitions() == runtime_state.runtime_state_allowed_transitions()
    assert observability.observability_allowed_event_types() == observability.observability_allowed_event_types()
    assert observability.observability_forbidden_event_types() == observability.observability_forbidden_event_types()
    assert observability.observability_forbidden_data_keys() == observability.observability_forbidden_data_keys()


def test_pure_helpers_do_not_create_files_or_mutate_inputs():
    before_root = set(os.listdir(ROOT))
    before_cwd = Path.cwd()
    source_metadata = {"purpose": "no_side_effects", "items": ["a", {"b": 1}]}
    state_metadata = _state_metadata(metadata_sanitized=source_metadata)
    obs_metadata = _observability_metadata(metadata_sanitized=source_metadata)
    obs_event = observability.build_observability_event_record(obs_metadata)
    governance.runtime_governance_contract_status()
    runtime_state.build_runtime_state_snapshot(runtime_state.RuntimeStateValue.READY_SIMULATED, state_metadata)
    observability.build_observability_snapshot(
        [obs_event],
        snapshot_id="snapshot_block_checkpoint",
        correlation_id=obs_metadata.correlation_id,
        policy_ref="observability_policy",
        security_baseline_ref=obs_metadata.security_baseline_ref,
        runtime_governance_ref=obs_metadata.runtime_governance_ref,
        runtime_state_ref=obs_metadata.runtime_state_ref,
        metadata_sanitized={"snapshot": "safe"},
    )
    assert source_metadata == {"purpose": "no_side_effects", "items": ["a", {"b": 1}]}
    assert set(os.listdir(ROOT)) == before_root
    assert Path.cwd() == before_cwd


@pytest.mark.parametrize("key", runtime_state.DANGEROUS_METADATA_KEYS[:8])
def test_runtime_state_dangerous_metadata_is_blocked(key):
    with pytest.raises(ValueError):
        _state_metadata(metadata_sanitized={key: "blocked"})


@pytest.mark.parametrize("key", observability.FORBIDDEN_DATA_KEYS[:10])
def test_observability_dangerous_metadata_is_blocked(key):
    with pytest.raises(ValueError):
        _observability_metadata(metadata_sanitized={key: "blocked"})


def test_forbidden_readiness_remains_blocked():
    governance_policy = governance.build_default_runtime_governance_policy()
    state_policy = runtime_state.build_default_runtime_state_policy()
    observability_policy = observability.build_default_observability_policy()
    assert "ready_for_runtime" in governance_policy.forbidden_readiness
    assert "ready_for_runtime" in state_policy.forbidden_readiness
    assert "ready_for_runtime" in observability_policy.forbidden_readiness
    state_request = runtime_state.RuntimeStateTransitionRequest(
        request_id="state_forbidden_readiness",
        current_state=runtime_state.RuntimeStateValue.GOVERNANCE_PENDING,
        requested_transition=runtime_state.RuntimeStateTransition.GOVERNANCE_PENDING_TO_READY_SIMULATED,
        requested_state=runtime_state.RuntimeStateValue.READY_SIMULATED,
        requested_by="checkpoint",
        reason="forbidden readiness check",
        metadata=_state_metadata(),
        security_baseline_ref="security_layer_final",
        runtime_gate_ref="runtime_gate_closed",
        requested_readiness="ready_for_runtime",
    )
    state_decision = runtime_state.evaluate_runtime_state_transition(state_request)
    assert runtime_state.RuntimeStateBlockReason.FORBIDDEN_READINESS.value in state_decision.block_reasons
    obs_decision = observability.evaluate_observability_event(_observability_metadata(), requested_readiness="ready_for_runtime")
    assert observability.ObservabilityBlockReason.FORBIDDEN_READINESS.value in obs_decision.block_reasons
    assert obs_decision.readiness.value == "ready_for_observability_contract_e2e"


def test_forbidden_modules_were_not_created_except_allowed_preexisting_non_operational():
    allowed_preexisting = {
        "core/runtime_executor.py": "prepare-only",
        "core/approval_workflow.py": "Helpers no mutantes",
        "core/observability.py": "Helpers no mutantes",
        "core/runtime_state_contract.py": "Non-operational Runtime State contract",
        "core/observability_contract.py": "Non-operational Observability contract",
    }
    for path in FORBIDDEN_MODULES:
        candidate = ROOT / path
        if path in allowed_preexisting and candidate.exists():
            assert allowed_preexisting[path].lower() in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), path


def test_external_boundary_flags_remain_blocked():
    modules = [
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
    ]
    for module_name in modules:
        module = importlib.import_module(module_name)
        false_flags = [
            getattr(module, name)
            for name in dir(module)
            if name.isupper() and (name.endswith("_ENABLED") or name.endswith("_OPERATIONAL"))
        ]
        assert false_flags, module_name
        assert false_flags == [False] * len(false_flags), module_name


def test_observability_helper_remains_preexisting_non_mutant():
    helper = ROOT / "core" / "observability.py"
    assert helper.exists()
    text = helper.read_text(encoding="utf-8")
    assert "Helpers no mutantes" in text
    forbidden_runtime_phrases = [
        "OBSERVABILITY_RUNTIME_ENABLED = True",
        "EVENT_BUS_ENABLED = True",
        "TELEMETRY_ENABLED = True",
        "LOG_WRITE_ENABLED = True",
        "STORE_WRITE_ENABLED = True",
    ]
    for phrase in forbidden_runtime_phrases:
        assert phrase not in text


def test_obliteratus_exclusion_is_explicit_and_not_operational():
    text = _text()
    for phrase in [
        "OBLITERATUS no forma parte del Runtime Governance Block",
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
        "tool",
        "model",
        "workflow",
    ]:
        assert phrase in text


FORBIDDEN_MODULES = [
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
    "core/runtime_state.py",
    "core/runtime_state_machine.py",
    "core/runtime_state_validator.py",
    "core/runtime_state_store.py",
    "core/runtime_state_writer.py",
    "core/runtime_state_reader.py",
    "core/runtime_state_transition.py",
    "core/runtime_state_event.py",
    "core/runtime_state_event_bus.py",
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
]
