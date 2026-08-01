import dataclasses
import importlib
import json
from pathlib import Path

import pytest

import core.runtime_execution_preparation_contract as contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_CONTRACT_FULL_E2E_CHECKPOINT.md"
MODULE_PATH = ROOT / "core" / "runtime_execution_preparation_contract.py"


def _metadata(**overrides):
    data = {
        "preparation_reason": "full e2e checkpoint",
        "preparation_scope": "future_runtime_execution_preparation",
        "preparation_mode": "contract_only",
        "preparation_risk_level": "low",
        "created_by": "pytest",
        "source": "tests.test_runtime_execution_preparation_contract_full_e2e_checkpoint",
        "tags": ("e2e", "safe"),
        "notes": ("non-operational",),
    }
    data.update(overrides)
    return contract.sanitize_runtime_execution_preparation_metadata(data)


def _snapshot(**overrides):
    data = {
        "security_baseline_ok": True,
        "agent_permission_ok": True,
        "sandbox_boundary_ok": True,
        "tool_boundary_ok": True,
        "model_boundary_ok": True,
        "context_boundary_ok": True,
        "output_boundary_ok": True,
        "secrets_policy_ok": True,
        "prompt_injection_defense_ok": True,
        "runtime_governance_ok": True,
        "runtime_state_ok": True,
        "observability_ok": True,
        "runtime_activation_gate_ok": True,
        "human_approval_ok": True,
        "kill_switch_ok": True,
        "rollback_ok": True,
        "dry_run_ok": True,
    }
    data.update(overrides)
    return contract.build_runtime_execution_preparation_boundary_snapshot(**data)


def _package(**overrides):
    data = {
        "preparation_id": "prep_full_e2e",
        "intent_ref": "intent_contract_ref",
        "attempt_ref": "attempt_contract_ref",
        "runtime_governance_ref": "runtime_governance_contract",
        "runtime_state_ref": "runtime_state_contract",
        "observability_ref": "observability_contract",
        "runtime_activation_gate_ref": "runtime_activation_gate_closed",
        "security_baseline_ref": "security_layer_final_checkpoint",
        "agent_permission_ref": "agent_permission_contract",
        "sandbox_boundary_ref": "sandbox_boundary",
        "tool_boundary_ref": "tool_boundary",
        "model_boundary_ref": "model_boundary",
        "context_boundary_ref": "context_boundary",
        "output_boundary_ref": "output_boundary",
        "secrets_policy_ref": "secrets_policy",
        "prompt_injection_defense_ref": "prompt_injection_defense",
        "human_approval_ref": "human_approval_plan",
        "kill_switch_ref": "kill_switch_contract",
        "rollback_ref": "rollback_contract",
        "dry_run_ref": "dry_run_contract",
        "execution_scope": "future_simulated_scope",
        "execution_mode": contract.RuntimeExecutionPreparationMode.CONTRACT_ONLY,
        "execution_risk_level": contract.RuntimeExecutionPreparationRiskLevel.LOW,
        "metadata": _metadata(),
        "prepared_snapshot": _snapshot(),
        "readiness": contract.RuntimeExecutionPreparationReadiness.READY_FOR_RUNTIME_EXECUTION_PREPARATION_CONTRACT_E2E,
    }
    data.update(overrides)
    return contract.build_runtime_execution_preparation_package(**data)


def _assert_no_runtime_flags(record):
    for field in [
        "runtime_execution_allowed",
        "runtime_activation_allowed",
        "dry_run_execution_allowed",
        "tool_execution_allowed",
        "model_invocation_allowed",
        "context_injection_allowed",
        "output_delivery_allowed",
        "writes_allowed",
        "stores_allowed",
    ]:
        assert getattr(record, field) is False


def _assert_false_flags(module_name: str) -> None:
    module = importlib.import_module(module_name)
    flags = [
        getattr(module, name)
        for name in dir(module)
        if name.isupper()
        and isinstance(getattr(module, name), bool)
        and (name.endswith("_ENABLED") or name.endswith("_OPERATIONAL") or name.endswith("_ACTIVE"))
    ]
    assert flags, module_name
    assert flags == [False] * len(flags), module_name


def test_module_imports_and_global_flags_remain_closed():
    assert importlib.import_module("core.runtime_execution_preparation_contract")
    assert contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY is True
    _assert_false_flags("core.runtime_execution_preparation_contract")


def test_policy_default_deny_blocks_every_operational_axis():
    policy = contract.build_runtime_execution_preparation_policy()
    assert policy.contract_ready is True
    for field_name in [
        "runtime_activation_enabled",
        "runtime_execution_enabled",
        "dry_run_execution_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "context_injection_enabled",
        "output_delivery_enabled",
        "writes_enabled",
        "stores_enabled",
        "memory_enabled",
        "network_enabled",
        "browser_enabled",
        "filesystem_enabled",
        "env_enabled",
        "secrets_enabled",
        "integrations_enabled",
        "automatic_approval_enabled",
        "kill_switch_operational_enabled",
        "rollback_operational_enabled",
    ]:
        assert getattr(policy, field_name) is False


def test_metadata_sanitizer_preserves_safe_data_and_blocks_dangerous_values():
    metadata = contract.sanitize_runtime_execution_preparation_metadata(
        {
            "preparation_reason": "safe",
            "preparation_scope": "scope",
            "created_by": "tester",
            "tags": ["a", "b"],
            "api_key": "LEAK_ME_NOT",
            "password": "LEAK_ME_NOT",
            "raw_prompt": "LEAK_ME_NOT",
            "tool_response": "LEAK_ME_NOT",
        }
    )
    serialized = json.dumps(contract.runtime_execution_preparation_to_dict(metadata), sort_keys=True)
    assert metadata.preparation_reason == "safe"
    assert metadata.preparation_scope == "scope"
    assert metadata.created_by == "tester"
    assert metadata.tags == ("a", "b")
    assert set(metadata.blocked_keys) == {"api_key", "password", "raw_prompt", "tool_response"}
    assert "LEAK_ME_NOT" not in serialized
    for key in [
        "secret",
        "api_key",
        "token",
        "password",
        "credential",
        "private_key",
        "raw_payload",
        "payload",
        "raw_output",
        "output",
        "file_content",
        "env",
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
    ]:
        assert key in contract.FORBIDDEN_METADATA_KEYS


def test_dependencies_can_be_built_for_every_required_kind():
    dependencies = [
        contract.build_runtime_execution_preparation_dependency(
            kind=kind,
            ref=f"{kind.value}_ref",
            required=kind
            not in {
                contract.RuntimeExecutionPreparationDependencyKind.ATTEMPT_REFERENCE,
                contract.RuntimeExecutionPreparationDependencyKind.HUMAN_APPROVAL,
                contract.RuntimeExecutionPreparationDependencyKind.KILL_SWITCH,
                contract.RuntimeExecutionPreparationDependencyKind.ROLLBACK,
                contract.RuntimeExecutionPreparationDependencyKind.DRY_RUN,
            },
        )
        for kind in contract.RuntimeExecutionPreparationDependencyKind
    ]
    assert {dependency.kind for dependency in dependencies} == set(contract.RuntimeExecutionPreparationDependencyKind)
    assert all(dependency.present for dependency in dependencies)
    assert any(not dependency.required for dependency in dependencies)


def test_boundary_snapshot_complete_and_incomplete_detection():
    complete = _snapshot()
    assert complete.missing_required() == ()
    assert complete.missing_optional() == ()
    incomplete = _snapshot(tool_boundary_ok=False, model_boundary_ok=False, dry_run_ok=False)
    assert incomplete.missing_required() == ("tool_boundary", "model_boundary")
    assert incomplete.missing_optional() == ("dry_run",)


def test_complete_safe_package_validates_positive_with_safe_readiness():
    package = _package()
    validation = contract.validate_runtime_execution_preparation_package(package)
    assert validation.is_valid is True
    assert package.readiness == contract.RuntimeExecutionPreparationReadiness.READY_FOR_RUNTIME_EXECUTION_PREPARATION_CONTRACT_E2E
    assert validation.status == contract.RuntimeExecutionPreparationStatus.READY_SIMULATED
    status = contract.get_runtime_execution_preparation_contract_status()
    assert status["runtime_active"] is False
    assert status["execution_active"] is False
    assert status["dry_run_active"] is False
    assert status["tools_enabled"] is False
    assert status["models_enabled"] is False
    assert status["context_enabled"] is False
    assert status["output_enabled"] is False
    assert status["writes_enabled"] is False
    assert status["stores_enabled"] is False
    assert status["memory_enabled"] is False
    assert status["network_enabled"] is False
    assert status["browser_enabled"] is False
    assert status["filesystem_enabled"] is False
    assert status["env_enabled"] is False
    assert status["secrets_enabled"] is False
    assert status["integrations_enabled"] is False


@pytest.mark.parametrize(
    "field",
    [
        "preparation_id",
        "intent_ref",
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
    ],
)
def test_package_missing_required_refs_fails(field):
    result = contract.validate_runtime_execution_preparation_package(_package(**{field: ""}))
    assert result.is_valid is False
    assert f"missing_required_ref:{field}" in result.errors


def test_package_with_forbidden_readiness_capability_metadata_policy_and_status_fails():
    forbidden_readiness = contract.validate_runtime_execution_preparation_package(
        _package(readiness="ready_for_runtime")
    )
    assert forbidden_readiness.is_valid is False
    assert "ready_for_runtime" in forbidden_readiness.forbidden_readiness_detected

    operational_capability = contract.validate_runtime_execution_preparation_package(
        _package(blocked_capabilities=("runtime_execution",))
    )
    assert operational_capability.is_valid is False
    assert "blocked_capabilities_must_match_default_deny" in operational_capability.errors

    dangerous_metadata = contract.validate_runtime_execution_preparation_package(
        _package(metadata=_metadata(api_key="LEAK_ME_NOT"))
    )
    assert dangerous_metadata.is_valid is False
    assert dangerous_metadata.metadata_blocked_keys == ("api_key",)
    assert "LEAK_ME_NOT" not in json.dumps(contract.runtime_execution_preparation_to_dict(dangerous_metadata))

    unsafe_policy = dataclasses.replace(
        contract.build_runtime_execution_preparation_policy(),
        runtime_execution_enabled=True,
    )
    policy_result = contract.validate_runtime_execution_preparation_package(_package(), unsafe_policy)
    assert policy_result.is_valid is False
    assert "operational_policy_flag_enabled:runtime_execution_enabled" in policy_result.errors

    operational_status_package = dataclasses.replace(
        _package(),
        status="runtime_execution_preparation_active",
    )
    status_result = contract.validate_runtime_execution_preparation_package(operational_status_package)
    assert status_result.is_valid is False
    assert "forbidden_status:runtime_execution_preparation_active" in status_result.errors


def test_decision_records_allow_only_simulated_preparation_or_blocking_decisions():
    valid = contract.validate_runtime_execution_preparation_package(_package())
    decision = contract.decide_runtime_execution_preparation(valid)
    assert decision.decision == contract.RuntimeExecutionPreparationDecision.ALLOW_SIMULATED_PREPARATION
    assert decision.allowed is True
    assert decision.simulated_preparation_allowed is True
    _assert_no_runtime_flags(decision)

    invalid = contract.validate_runtime_execution_preparation_package(_package(intent_ref=""))
    blocked = contract.decide_runtime_execution_preparation(invalid)
    assert blocked.decision in {
        contract.RuntimeExecutionPreparationDecision.INVALID,
        contract.RuntimeExecutionPreparationDecision.BLOCK_PREPARATION,
        contract.RuntimeExecutionPreparationDecision.REQUIRE_DEPENDENCIES,
    }
    assert blocked.allowed is False
    _assert_no_runtime_flags(blocked)


def test_snapshot_json_safe_contains_required_fields_and_is_deterministic():
    package = _package()
    validation = contract.validate_runtime_execution_preparation_package(package)
    decision = contract.decide_runtime_execution_preparation(validation)
    first = contract.runtime_execution_preparation_to_dict(
        contract.build_runtime_execution_preparation_contract_snapshot(
            package=package,
            validation=validation,
            decision=decision,
        )
    )
    second = contract.runtime_execution_preparation_to_dict(
        contract.build_runtime_execution_preparation_contract_snapshot(
            package=package,
            validation=validation,
            decision=decision,
        )
    )
    assert first == second
    json.dumps(first, sort_keys=True)
    for field in [
        "contract_status",
        "policy",
        "allowed_statuses",
        "forbidden_statuses",
        "allowed_readiness",
        "forbidden_readiness",
        "blocked_capabilities",
        "forbidden_metadata_keys",
        "dependencies",
        "package",
        "validation",
        "decision",
    ]:
        assert field in first

    mixed = {
        "enum": contract.RuntimeExecutionPreparationMode.CONTRACT_ONLY,
        "dataclass": package.metadata,
        "tuple": ("a", "b"),
        "frozenset": frozenset({"c"}),
        "list": [contract.RuntimeExecutionPreparationRiskLevel.LOW],
        "dict": {"status": contract.RuntimeExecutionPreparationStatus.READY_SIMULATED},
    }
    json.dumps(contract.runtime_execution_preparation_to_dict(mixed), sort_keys=True)


def test_pure_contract_calls_create_no_files_logs_stores_or_events():
    before = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    package = _package()
    validation = contract.validate_runtime_execution_preparation_package(package)
    decision = contract.decide_runtime_execution_preparation(validation)
    contract.runtime_execution_preparation_to_dict(
        contract.build_runtime_execution_preparation_contract_snapshot(
            package=package,
            validation=validation,
            decision=decision,
        )
    )
    after = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert before == after


def test_module_does_not_import_or_use_real_execution_interfaces():
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in [
        "import subprocess",
        "import socket",
        "import requests",
        "import httpx",
        "import urllib",
        "from pathlib",
        "os.environ",
        "getenv",
        "open(",
        "Path(",
        "import browser_operator",
        "import network",
        "import secret_access",
        "import runtime_runner",
        "import tool_executor",
        "import model_invoker",
        "import context_injector",
        "import output_delivery",
    ]:
        assert forbidden not in source


def test_previous_contracts_and_boundaries_remain_blocked():
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


def test_no_new_forbidden_operational_modules_exist():
    allowed_preexisting = {
        "core/runtime_executor.py": "prepare-only",
    }
    for relative in [
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
        "core/model_invoker.py",
        "core/context_injector.py",
        "core/output_delivery.py",
        "core/output_publisher.py",
        "core/output_writer.py",
        "core/message_sender.py",
        "core/webhook_client.py",
        "core/provider_client.py",
        "core/browser_operator.py",
        "core/sandbox_runner.py",
        "core/command_executor.py",
        "core/shell.py",
        "core/subprocess_runner.py",
        "core/runtime_execution_preparation_store.py",
        "core/runtime_execution_preparation_writer.py",
        "core/runtime_execution_preparation_reader.py",
        "core/runtime_execution_preparation_handoff.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        candidate = ROOT / relative
        if relative in allowed_preexisting and candidate.exists():
            assert allowed_preexisting[relative] in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), relative


def test_obliteratus_excluded_from_runtime_execution_preparation_chain():
    assert contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    assert "obliteratus_integration" in contract.BLOCKED_CAPABILITIES
    for statement in contract.OBLITERATUS_EXCLUSION_STATEMENTS:
        assert "OBLITERATUS" in statement
    snapshot = contract.runtime_execution_preparation_to_dict(
        contract.build_runtime_execution_preparation_contract_snapshot()
    )
    assert "OBLITERATUS" not in json.dumps(snapshot, sort_keys=True)


def test_checkpoint_document_exists_and_declares_full_e2e_status():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "Runtime Execution Preparation Contract Full E2E Checkpoint",
        "RUNTIME_EXECUTION_PREPARATION_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_EXECUTION_PREPARATION_CONTRACT_CHAIN_READY",
        "ready_for_runtime_execution_preparation_package_audit",
        "PROMPT 4.2 — Auditoría de Runtime Execution Preparation Package",
        "Runtime Execution Preparation sigue no-operativo",
        "OBLITERATUS queda excluido",
    ]:
        assert phrase in text
