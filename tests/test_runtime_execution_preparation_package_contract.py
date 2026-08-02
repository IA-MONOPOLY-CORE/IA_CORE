import dataclasses
import importlib
import json
from pathlib import Path

import pytest

import core.runtime_execution_preparation_contract as parent_contract
import core.runtime_execution_preparation_package as package_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT.md"
MODULE_PATH = ROOT / "core" / "runtime_execution_preparation_package.py"


def _metadata(**overrides):
    data = {
        "package_reason": "unit test",
        "package_scope": "future package",
        "package_mode": "contract_only",
        "package_risk_level": "low",
        "created_by": "pytest",
        "source": "tests",
        "tags": ("package", "safe"),
        "notes": ("no runtime",),
        "business_context_ref": "business_context",
        "domain_ref": "domain_ref",
        "agent_ref": "agent_ref",
    }
    data.update(overrides)
    return package_contract.sanitize_runtime_execution_preparation_package_metadata(data)


def _dependency_set(**overrides):
    data = {
        "preparation_id": "prep_1",
        "intent_ref": "intent_1",
        "attempt_ref": "attempt_1",
        "runtime_governance_ref": "runtime_governance_contract",
        "runtime_state_ref": "runtime_state_contract",
        "observability_ref": "observability_contract",
        "runtime_activation_gate_ref": "runtime_activation_gate_closed",
        "security_baseline_ref": "security_layer_final",
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
    }
    data.update(overrides)
    return package_contract.build_runtime_execution_preparation_package_dependency_set(**data)


def _boundary_set(**overrides):
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
        "master_user_panel_separation_ok": True,
        "ui_safe_visibility_ok": True,
    }
    data.update(overrides)
    return package_contract.build_runtime_execution_preparation_package_boundary_set(**data)


def _package(**overrides):
    data = {
        "package_id": "pkg_1",
        "dependency_set": _dependency_set(),
        "boundary_set": _boundary_set(),
        "execution_scope": "future_simulated_scope",
        "execution_mode": package_contract.RuntimeExecutionPreparationPackageMode.CONTRACT_ONLY,
        "execution_risk_level": package_contract.RuntimeExecutionPreparationPackageRiskLevel.LOW,
        "metadata": _metadata(),
    }
    data.update(overrides)
    return package_contract.build_runtime_execution_preparation_package(**data)


def _assert_decision_never_operational(decision):
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
        "memory_allowed",
        "network_allowed",
        "browser_allowed",
        "filesystem_allowed",
        "env_allowed",
        "secrets_allowed",
        "ui_device_allowed",
        "integrations_allowed",
    ]:
        assert getattr(decision, field) is False


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


def test_module_imports_and_references_parent_contract_safely():
    module = importlib.import_module("core.runtime_execution_preparation_package")
    assert module.parent_contract is parent_contract
    assert module.PARENT_CONTRACT_REF == "core.runtime_execution_preparation_contract"
    assert parent_contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY is True


def test_flags_are_ready_and_non_operational():
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY is True
    for flag_name in [
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_OPERATIONAL",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_RUNTIME_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_EXECUTION_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_DRY_RUN_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_TOOLS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_MODELS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTEXT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_OUTPUT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_WRITES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_STORES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_MEMORY_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_NETWORK_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_BROWSER_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_FILESYSTEM_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_ENV_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_SECRETS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_UI_DEVICE_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_INTEGRATIONS_ENABLED",
    ]:
        assert getattr(package_contract, flag_name) is False


def test_dataclasses_are_frozen():
    for cls_name in [
        "RuntimeExecutionPreparationPackagePolicy",
        "RuntimeExecutionPreparationPackageMetadata",
        "RuntimeExecutionPreparationPackageDependencySet",
        "RuntimeExecutionPreparationPackageBoundarySet",
        "RuntimeExecutionPreparationPackageCore",
        "RuntimeExecutionPreparationPackageValidationResult",
        "RuntimeExecutionPreparationPackageDecisionRecord",
        "RuntimeExecutionPreparationPackageSnapshot",
        "RuntimeExecutionPreparationPackageContractSnapshot",
        "RuntimeExecutionPreparationPackageSafeView",
    ]:
        cls = getattr(package_contract, cls_name)
        assert dataclasses.is_dataclass(cls)
        assert cls.__dataclass_params__.frozen is True


def test_enums_statuses_readiness_and_capabilities_are_declared():
    for status in [
        "package_uninitialized",
        "package_draft",
        "package_dependencies_required",
        "package_boundaries_required",
        "package_metadata_invalid",
        "package_readiness_invalid",
        "package_policy_invalid",
        "package_blocked",
        "package_ready_simulated",
        "package_archived_simulated",
        "package_invalid",
    ]:
        assert status in package_contract.ALLOWED_STATUSES
    for status in [
        "package_active",
        "package_running",
        "package_executing",
        "package_live",
        "package_enabled",
        "package_operational",
        "package_runtime_started",
        "package_execution_started",
        "package_dry_run_started",
        "package_tool_executing",
        "package_model_invoking",
        "package_context_injecting",
        "package_output_delivering",
        "package_writing",
        "package_store_mutating",
        "package_network_active",
        "package_browser_active",
        "package_filesystem_active",
        "package_env_active",
        "package_secret_active",
        "package_integration_active",
    ]:
        assert status in package_contract.FORBIDDEN_STATUSES
    assert package_contract.ALLOWED_READINESS == (
        "ready_for_runtime_execution_preparation_package_contract",
        "ready_for_runtime_execution_preparation_package_contract_e2e",
    )
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
        "package_operational",
        "package_runtime_enabled",
        "package_execution_enabled",
        "package_store_enabled",
    ]:
        assert readiness in package_contract.FORBIDDEN_READINESS
    for capability in [
        "runtime_execution",
        "runtime_activation",
        "dry_run_execution",
        "runner",
        "scheduler",
        "worker",
        "queue",
        "executor",
        "orchestrator",
        "dispatcher",
        "event_bus",
        "tool_execution",
        "model_invocation",
        "context_injection",
        "output_delivery",
        "writes",
        "stores",
        "memory",
        "network",
        "api",
        "browser",
        "filesystem",
        "env",
        "secrets",
        "ui_control",
        "device_control",
        "integrations",
        "market_catalog_runtime",
        "business_composition_runtime",
        "obliteratus_integration",
        "master_panel_capabilities_for_user_panel",
        "raw_internal_visibility",
    ]:
        assert capability in package_contract.BLOCKED_CAPABILITIES


def test_metadata_safe_is_kept_and_dangerous_values_are_blocked():
    metadata = package_contract.sanitize_runtime_execution_preparation_package_metadata(
        {
            "package_reason": "safe",
            "business_context_ref": "biz",
            "domain_ref": "domain",
            "agent_ref": "agent",
            "api_key": "SHOULD_NOT_SURVIVE",
            "raw_prompt": "SHOULD_NOT_SURVIVE",
            "model_response": "SHOULD_NOT_SURVIVE",
        }
    )
    dumped = json.dumps(package_contract.runtime_execution_preparation_package_to_dict(metadata), sort_keys=True)
    assert metadata.package_reason == "safe"
    assert metadata.business_context_ref == "biz"
    assert metadata.domain_ref == "domain"
    assert metadata.agent_ref == "agent"
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
        assert key in package_contract.FORBIDDEN_METADATA_KEYS


def test_policy_default_deny_and_operational_policy_fails_validation():
    policy = package_contract.build_runtime_execution_preparation_package_policy()
    assert policy.contract_ready is True
    for field in dataclasses.fields(policy):
        if field.name != "contract_ready":
            assert getattr(policy, field.name) is False
    unsafe_policy = dataclasses.replace(policy, runtime_execution_enabled=True)
    result = package_contract.validate_runtime_execution_preparation_package_contract(_package(), unsafe_policy)
    assert result.is_valid is False
    assert "operational_policy_flag_enabled:runtime_execution_enabled" in result.policy_violations


def test_dependency_set_required_optional_and_missing_detection():
    deps = _dependency_set()
    assert deps.required_dependencies() == package_contract.REQUIRED_DEPENDENCY_FIELDS
    assert deps.optional_dependencies() == package_contract.OPTIONAL_DEPENDENCY_FIELDS
    assert deps.missing_required_dependencies() == ()
    assert deps.missing_optional_dependencies() == ()
    incomplete = _dependency_set(intent_ref="", dry_run_ref=None)
    assert "intent_ref" in incomplete.missing_required_dependencies()
    assert "dry_run_ref" in incomplete.missing_optional_dependencies()


def test_boundary_set_complete_and_incomplete_detection():
    complete = _boundary_set()
    assert complete.missing_critical_boundaries() == ()
    incomplete = _boundary_set(tool_boundary_ok=False, master_user_panel_separation_ok=False)
    assert "tool_boundary" in incomplete.missing_critical_boundaries()
    assert "master_user_panel_separation" in incomplete.missing_critical_boundaries()


def test_complete_safe_package_validates_true():
    package = _package()
    result = package_contract.validate_runtime_execution_preparation_package_contract(package)
    assert result.is_valid is True
    assert result.status == package_contract.RuntimeExecutionPreparationPackageStatus.PACKAGE_READY_SIMULATED
    assert result.missing_required_dependencies == ()
    assert result.missing_optional_dependencies == ()


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
def test_package_missing_required_dependencies_fails(field):
    deps = _dependency_set(**{field: ""})
    result = package_contract.validate_runtime_execution_preparation_package_contract(
        _package(dependency_set=deps)
    )
    assert result.is_valid is False
    assert f"missing_required_ref:{field}" in result.errors


def test_package_without_package_id_fails():
    result = package_contract.validate_runtime_execution_preparation_package_contract(_package(package_id=""))
    assert result.is_valid is False
    assert "missing_required_ref:package_id" in result.errors


def test_package_with_forbidden_readiness_status_capability_metadata_and_boundaries_fails():
    readiness = package_contract.validate_runtime_execution_preparation_package_contract(
        _package(package_readiness="ready_for_runtime")
    )
    assert readiness.is_valid is False
    assert "ready_for_runtime" in readiness.forbidden_readiness_detected

    bad_status_package = dataclasses.replace(_package(), package_status="package_active")
    status = package_contract.validate_runtime_execution_preparation_package_contract(bad_status_package)
    assert status.is_valid is False
    assert "package_active" in status.forbidden_status_detected

    capability = package_contract.validate_runtime_execution_preparation_package_contract(
        _package(blocked_capabilities=("runtime_execution",))
    )
    assert capability.is_valid is False
    assert "blocked_capabilities_must_match_default_deny" in capability.errors

    metadata = package_contract.validate_runtime_execution_preparation_package_contract(
        _package(metadata=_metadata(api_key="SHOULD_NOT_SURVIVE"))
    )
    assert metadata.is_valid is False
    assert metadata.metadata_blocked_keys == ("api_key",)
    assert "SHOULD_NOT_SURVIVE" not in json.dumps(
        package_contract.runtime_execution_preparation_package_to_dict(metadata),
        sort_keys=True,
    )

    boundary = package_contract.validate_runtime_execution_preparation_package_contract(
        _package(boundary_set=_boundary_set(model_boundary_ok=False))
    )
    assert boundary.is_valid is False
    assert "model_boundary" in boundary.boundary_violations

    panel = package_contract.validate_runtime_execution_preparation_package_contract(
        _package(boundary_set=_boundary_set(master_user_panel_separation_ok=False))
    )
    assert panel.is_valid is False
    assert "master_user_panel_separation_violated" in panel.ui_visibility_violations

    raw_ui_policy = dataclasses.replace(
        package_contract.build_runtime_execution_preparation_package_policy(),
        user_panel_raw_internal_exposure_enabled=True,
    )
    raw_ui = package_contract.validate_runtime_execution_preparation_package_contract(_package(), raw_ui_policy)
    assert raw_ui.is_valid is False
    assert "operational_policy_flag_enabled:user_panel_raw_internal_exposure_enabled" in raw_ui.policy_violations


def test_decision_positive_and_negative_never_allow_operational_axes():
    valid = package_contract.validate_runtime_execution_preparation_package_contract(_package())
    allowed = package_contract.decide_runtime_execution_preparation_package(valid)
    assert allowed.decision == package_contract.RuntimeExecutionPreparationPackageDecision.ALLOW_SIMULATED_PACKAGE
    assert allowed.allowed is True
    assert allowed.simulated_package_allowed is True
    _assert_decision_never_operational(allowed)

    cases = [
        package_contract.validate_runtime_execution_preparation_package_contract(_package(dependency_set=_dependency_set(intent_ref=""))),
        package_contract.validate_runtime_execution_preparation_package_contract(_package(boundary_set=_boundary_set(tool_boundary_ok=False))),
        package_contract.validate_runtime_execution_preparation_package_contract(_package(metadata=_metadata(api_key="x"))),
        package_contract.validate_runtime_execution_preparation_package_contract(
            _package(),
            dataclasses.replace(package_contract.build_runtime_execution_preparation_package_policy(), stores_enabled=True),
        ),
        package_contract.validate_runtime_execution_preparation_package_contract(_package(package_readiness="ready_for_runtime")),
    ]
    allowed_negative = {
        package_contract.RuntimeExecutionPreparationPackageDecision.BLOCK_PACKAGE,
        package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_DEPENDENCIES,
        package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_BOUNDARIES,
        package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_METADATA_SANITIZATION,
        package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_POLICY_DEFAULT_DENY,
        package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_UI_SAFE_VIEW,
        package_contract.RuntimeExecutionPreparationPackageDecision.INVALID,
    }
    for case in cases:
        decision = package_contract.decide_runtime_execution_preparation_package(case)
        assert decision.decision in allowed_negative
        assert decision.allowed is False
        _assert_decision_never_operational(decision)


def test_safe_views_do_not_expose_metadata_or_internals():
    package = _package()
    validation = package_contract.validate_runtime_execution_preparation_package_contract(package)
    user_view = package_contract.build_runtime_execution_preparation_package_safe_view(
        package,
        validation,
        package_contract.RuntimeExecutionPreparationPackageVisibility.USER_PANEL_SAFE,
    )
    master_view = package_contract.build_runtime_execution_preparation_package_safe_view(
        package,
        validation,
        package_contract.RuntimeExecutionPreparationPackageVisibility.MASTER_PANEL_SAFE,
    )
    for view in [user_view, master_view]:
        dumped = json.dumps(package_contract.runtime_execution_preparation_package_to_dict(view), sort_keys=True)
        assert "metadata" not in dumped
        assert "raw_prompt" not in dumped
        assert "raw_output" not in dumped
        assert "model_response" not in dumped
        assert "tool_response" not in dumped
    assert user_view.visibility == package_contract.RuntimeExecutionPreparationPackageVisibility.USER_PANEL_SAFE
    assert "user_panel_view_reduced" in user_view.warnings
    assert master_view.visibility == package_contract.RuntimeExecutionPreparationPackageVisibility.MASTER_PANEL_SAFE


def test_to_dict_snapshot_json_safe_and_deterministic():
    package = _package()
    validation = package_contract.validate_runtime_execution_preparation_package_contract(package)
    decision = package_contract.decide_runtime_execution_preparation_package(validation)
    safe_view = package_contract.build_runtime_execution_preparation_package_safe_view(
        package,
        validation,
        package_contract.RuntimeExecutionPreparationPackageVisibility.INTERNAL_ONLY,
    )
    snapshot = package_contract.build_runtime_execution_preparation_package_contract_snapshot(
        package=package,
        validation=validation,
        decision=decision,
        safe_view=safe_view,
    )
    first = package_contract.runtime_execution_preparation_package_to_dict(snapshot)
    second = package_contract.runtime_execution_preparation_package_to_dict(snapshot)
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
        "package",
        "validation",
        "decision",
        "safe_view",
        "parent_contract_ref",
    ]:
        assert field in first


def test_no_side_effects_or_dangerous_imports():
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
        "import browser",
        "import network",
    ]:
        assert forbidden not in source
    before = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    package = _package()
    validation = package_contract.validate_runtime_execution_preparation_package_contract(package)
    decision = package_contract.decide_runtime_execution_preparation_package(validation)
    package_contract.runtime_execution_preparation_package_to_dict(
        package_contract.build_runtime_execution_preparation_package_contract_snapshot(
            package=package,
            validation=validation,
            decision=decision,
        )
    )
    after = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert before == after


def test_obliteratus_excluded_from_package_roles():
    assert package_contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    assert "obliteratus_integration" in package_contract.BLOCKED_CAPABILITIES
    for statement in package_contract.OBLITERATUS_EXCLUSION_STATEMENTS:
        assert "OBLITERATUS" in statement
    snapshot = package_contract.runtime_execution_preparation_package_to_dict(
        package_contract.build_runtime_execution_preparation_package_contract_snapshot()
    )
    assert "OBLITERATUS" not in json.dumps(snapshot, sort_keys=True)


def test_contract_document_exists_and_contains_required_markers():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_runtime_execution_preparation_package_contract_e2e",
        "PROMPT 4.3.1 — Checkpoint E2E Runtime Execution Preparation Package Contract",
    ]:
        assert phrase in text


def test_previous_contracts_and_boundaries_remain_blocked():
    for module_name in [
        "core.runtime_execution_preparation_contract",
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


def test_no_forbidden_operational_modules_created():
    allowed_preexisting = {"core/runtime_executor.py": "prepare-only"}
    for relative in [
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
        "core/dry_run_executor.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/context_injector.py",
        "core/output_delivery.py",
        "core/output_publisher.py",
        "core/browser_operator.py",
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
