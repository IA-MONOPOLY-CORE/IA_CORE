import dataclasses
import importlib
import json
from pathlib import Path

import pytest

import core.runtime_execution_preparation_contract as contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_CONTRACT.md"
MODULE_PATH = ROOT / "core" / "runtime_execution_preparation_contract.py"


def _metadata(**overrides):
    data = {
        "preparation_reason": "unit test",
        "preparation_scope": "future execution preparation",
        "preparation_mode": "contract_only",
        "preparation_risk_level": "low",
        "created_by": "pytest",
        "source": "tests",
        "tags": ["contract", "safe"],
        "notes": ["no execution"],
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
        "preparation_id": "prep_1",
        "intent_ref": "intent_1",
        "attempt_ref": "attempt_1",
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
    }
    data.update(overrides)
    return contract.build_runtime_execution_preparation_package(**data)


def test_module_exists_and_imports():
    assert importlib.import_module("core.runtime_execution_preparation_contract")
    assert MODULE_PATH.exists()


def test_flags_are_ready_and_non_operational():
    assert contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY is True
    for flag_name in [
        "RUNTIME_EXECUTION_PREPARATION_OPERATIONAL",
        "RUNTIME_EXECUTION_PREPARATION_RUNTIME_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_EXECUTION_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_DRY_RUN_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_TOOLS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_MODELS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_CONTEXT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_OUTPUT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_WRITES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_STORES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_MEMORY_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_NETWORK_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_BROWSER_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_FILESYSTEM_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_ENV_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_SECRETS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_INTEGRATIONS_ENABLED",
    ]:
        assert getattr(contract, flag_name) is False


def test_dataclasses_are_frozen():
    for cls_name in [
        "RuntimeExecutionPreparationPolicy",
        "RuntimeExecutionPreparationMetadata",
        "RuntimeExecutionPreparationDependency",
        "RuntimeExecutionPreparationBoundarySnapshot",
        "RuntimeExecutionPreparationPackage",
        "RuntimeExecutionPreparationValidationResult",
        "RuntimeExecutionPreparationDecisionRecord",
        "RuntimeExecutionPreparationContractSnapshot",
    ]:
        cls = getattr(contract, cls_name)
        assert dataclasses.is_dataclass(cls)
        assert cls.__dataclass_params__.frozen is True


def test_enums_allowed_states_readiness_and_forbidden_sets():
    for state in [
        "runtime_execution_preparation_uninitialized",
        "runtime_execution_preparation_governance_required",
        "runtime_execution_preparation_state_required",
        "runtime_execution_preparation_observability_required",
        "runtime_execution_preparation_security_required",
        "runtime_execution_preparation_intent_required",
        "runtime_execution_preparation_attempt_required",
        "runtime_execution_preparation_boundaries_required",
        "runtime_execution_preparation_ready_simulated",
        "runtime_execution_preparation_blocked",
        "runtime_execution_preparation_invalid",
        "runtime_execution_preparation_archived_simulated",
    ]:
        assert state in contract.ALLOWED_STATUSES
    assert contract.ALLOWED_READINESS == (
        "ready_for_runtime_execution_preparation_contract",
        "ready_for_runtime_execution_preparation_contract_e2e",
    )
    for forbidden in [
        "runtime_execution_preparation_active",
        "runtime_execution_preparation_running",
        "runtime_execution_preparation_executing",
        "runtime_execution_preparation_live",
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
    ]:
        assert forbidden in contract.FORBIDDEN_STATUSES
    for readiness in [
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
        "runtime_execution_enabled",
        "runtime_execution_preparation_operational",
    ]:
        assert readiness in contract.FORBIDDEN_READINESS


def test_metadata_safe_is_kept_and_dangerous_values_are_blocked():
    metadata = contract.sanitize_runtime_execution_preparation_metadata(
        {
            "preparation_reason": "safe reason",
            "created_by": "tester",
            "tags": ["a", "b"],
            "api_key": "SHOULD_NOT_SURVIVE",
            "raw_prompt": "SHOULD_NOT_SURVIVE",
            "model_response": "SHOULD_NOT_SURVIVE",
        }
    )
    as_dict = contract.runtime_execution_preparation_to_dict(metadata)
    dumped = json.dumps(as_dict)
    assert metadata.preparation_reason == "safe reason"
    assert metadata.created_by == "tester"
    assert metadata.tags == ("a", "b")
    assert set(metadata.blocked_keys) == {"api_key", "raw_prompt", "model_response"}
    assert "SHOULD_NOT_SURVIVE" not in dumped
    for key in [
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
    ]:
        assert key in contract.FORBIDDEN_METADATA_KEYS


def test_policy_default_deny_and_operational_policy_fails_validation():
    policy = contract.build_runtime_execution_preparation_policy()
    assert policy.contract_ready is True
    for field in dataclasses.fields(policy):
        if field.name != "contract_ready":
            assert getattr(policy, field.name) is False
    unsafe_policy = dataclasses.replace(policy, runtime_execution_enabled=True)
    result = contract.validate_runtime_execution_preparation_package(_package(), unsafe_policy)
    assert result.is_valid is False
    assert "operational_policy_flag_enabled:runtime_execution_enabled" in result.errors


def test_complete_safe_package_validates_and_decision_is_simulated_only():
    package = _package()
    result = contract.validate_runtime_execution_preparation_package(package)
    decision = contract.decide_runtime_execution_preparation(result)
    assert result.is_valid is True
    assert result.status == contract.RuntimeExecutionPreparationStatus.READY_SIMULATED
    assert decision.decision == contract.RuntimeExecutionPreparationDecision.ALLOW_SIMULATED_PREPARATION
    assert decision.allowed is True
    assert decision.simulated_preparation_allowed is True
    assert decision.runtime_execution_allowed is False
    assert decision.runtime_activation_allowed is False
    assert decision.dry_run_execution_allowed is False
    assert decision.tool_execution_allowed is False
    assert decision.model_invocation_allowed is False
    assert decision.context_injection_allowed is False
    assert decision.output_delivery_allowed is False
    assert decision.writes_allowed is False
    assert decision.stores_allowed is False


@pytest.mark.parametrize(
    "field",
    [
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
def test_missing_required_refs_fail(field):
    package = _package(**{field: ""})
    result = contract.validate_runtime_execution_preparation_package(package)
    assert result.is_valid is False
    assert f"missing_required_ref:{field}" in result.errors


def test_missing_main_boundaries_fail():
    package = _package(prepared_snapshot=_snapshot(tool_boundary_ok=False, context_boundary_ok=False))
    result = contract.validate_runtime_execution_preparation_package(package)
    assert result.is_valid is False
    assert "missing_boundary:tool_boundary" in result.errors
    assert "missing_boundary:context_boundary" in result.errors


def test_forbidden_readiness_and_capability_shape_fail():
    bad_readiness = _package(readiness="ready_for_runtime")
    result = contract.validate_runtime_execution_preparation_package(bad_readiness)
    assert result.is_valid is False
    assert "ready_for_runtime" in result.forbidden_readiness_detected
    bad_capability = _package(blocked_capabilities=("runtime_execution",))
    capability_result = contract.validate_runtime_execution_preparation_package(bad_capability)
    assert capability_result.is_valid is False
    assert "blocked_capabilities_must_match_default_deny" in capability_result.errors


def test_to_dict_snapshot_json_safe_and_deterministic():
    package = _package()
    validation = contract.validate_runtime_execution_preparation_package(package)
    decision = contract.decide_runtime_execution_preparation(validation)
    snapshot = contract.build_runtime_execution_preparation_contract_snapshot(
        package=package,
        validation=validation,
        decision=decision,
    )
    first = contract.runtime_execution_preparation_to_dict(snapshot)
    second = contract.runtime_execution_preparation_to_dict(snapshot)
    assert first == second
    json.dumps(first, sort_keys=True)
    assert first["contract_status"] == "RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY"
    assert first["decision"]["runtime_execution_allowed"] is False


def test_no_side_effect_imports_or_env_secret_access():
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in [
        "import subprocess",
        "import socket",
        "import requests",
        "import http.client",
        "import urllib",
        "from pathlib",
        "os.environ",
        "getenv",
        "Path(",
        "open(",
        "datetime.now",
        "uuid4",
    ]:
        assert forbidden not in source


def test_no_files_stores_logs_or_events_created(tmp_path):
    before = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    package = _package()
    validation = contract.validate_runtime_execution_preparation_package(package)
    contract.decide_runtime_execution_preparation(validation)
    contract.runtime_execution_preparation_to_dict(package)
    after = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert before == after


def test_obliteratus_is_excluded_from_all_runtime_roles():
    assert contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    blocked = set(contract.BLOCKED_CAPABILITIES)
    assert "obliteratus_integration" in blocked
    for statement in contract.OBLITERATUS_EXCLUSION_STATEMENTS:
        assert "OBLITERATUS" in statement
    snapshot = contract.runtime_execution_preparation_to_dict(
        contract.build_runtime_execution_preparation_contract_snapshot()
    )
    dumped = json.dumps(snapshot)
    assert "OBLITERATUS" not in dumped


def test_contract_document_exists_and_contains_required_markers():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY",
        "RUNTIME_EXECUTION_PREPARATION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_runtime_execution_preparation_contract_e2e",
        "PROMPT 4.1.1 — Checkpoint E2E Runtime Execution Preparation Contract",
    ]:
        assert phrase in text




