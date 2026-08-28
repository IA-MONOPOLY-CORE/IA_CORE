import dataclasses
import importlib
import json
from pathlib import Path

import pytest

import core.runtime_execution_preparation_package as package_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_FULL_E2E_CHECKPOINT.md"
MODULE_PATH = ROOT / "core" / "runtime_execution_preparation_package.py"


PACKAGE_OPERATIONAL_FLAGS = [
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
]

POLICY_BLOCK_FIELDS = [
    "package_operational_enabled",
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
    "ui_device_enabled",
    "integrations_enabled",
    "master_panel_exposure_enabled",
    "user_panel_raw_internal_exposure_enabled",
    "automatic_approval_enabled",
]

FORBIDDEN_METADATA_KEYS = [
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

PREVIOUS_CONTRACTS_AND_BOUNDARIES = [
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
]

FORBIDDEN_OPERATIONAL_MODULES = [
    "core/runtime_execution_preparation_store.py",
    "core/runtime_execution_preparation_writer.py",
    "core/runtime_execution_preparation_reader.py",
    "core/runtime_execution_preparation_handoff.py",
    "core/runtime_execution.py",
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
]


def _metadata(**overrides):
    data = {
        "package_reason": "full e2e",
        "package_scope": "runtime execution preparation package checkpoint",
        "package_mode": "contract_only",
        "package_risk_level": "low",
        "created_by": "pytest",
        "source": "checkpoint",
        "tags": ("package", "e2e"),
        "notes": ("no runtime", "no execution"),
        "business_context_ref": "business_context",
        "domain_ref": "domain_ref",
        "agent_ref": "agent_ref",
    }
    data.update(overrides)
    return package_contract.sanitize_runtime_execution_preparation_package_metadata(data)


def _dependency_set(**overrides):
    data = {
        "preparation_id": "prep_full_e2e",
        "intent_ref": "intent_full_e2e",
        "attempt_ref": "attempt_full_e2e",
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
        "package_id": "pkg_full_e2e",
        "dependency_set": _dependency_set(),
        "boundary_set": _boundary_set(),
        "execution_scope": "future_simulated_scope",
        "execution_mode": package_contract.RuntimeExecutionPreparationPackageMode.CONTRACT_ONLY,
        "execution_risk_level": package_contract.RuntimeExecutionPreparationPackageRiskLevel.LOW,
        "metadata": _metadata(),
        "package_readiness": (
            package_contract.RuntimeExecutionPreparationPackageReadiness
            .READY_FOR_RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_E2E
        ),
    }
    data.update(overrides)
    return package_contract.build_runtime_execution_preparation_package(**data)


def _validation(package=None, policy=None):
    return package_contract.validate_runtime_execution_preparation_package_contract(
        package or _package(),
        policy=policy,
    )


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


def _assert_all_operational_flags_false(module_name):
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


def _assert_dump_excludes_sensitive_values(value):
    dumped = json.dumps(package_contract.runtime_execution_preparation_package_to_dict(value), sort_keys=True)
    for token in [
        "SECRET_VALUE",
        "RAW_PAYLOAD_VALUE",
        "RAW_PROMPT_VALUE",
        "RAW_OUTPUT_VALUE",
        "MODEL_RESPONSE_VALUE",
        "TOOL_RESPONSE_VALUE",
        "MASTER_PANEL_INTERNAL",
    ]:
        assert token not in dumped
    return dumped


def test_imports_package_and_parent_contract_safely():
    module = importlib.import_module("core.runtime_execution_preparation_package")
    parent = importlib.import_module("core.runtime_execution_preparation_contract")
    assert module is package_contract
    assert module.parent_contract is parent
    assert module.PARENT_CONTRACT_REF == "core.runtime_execution_preparation_contract"
    assert parent.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY is True
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY is True


def test_package_and_parent_operational_flags_remain_false():
    for flag_name in PACKAGE_OPERATIONAL_FLAGS:
        assert getattr(package_contract, flag_name) is False
    for module_name in ["core.runtime_execution_preparation_package", *PREVIOUS_CONTRACTS_AND_BOUNDARIES]:
        _assert_all_operational_flags_false(module_name)


def test_policy_is_default_deny_and_blocks_all_operational_axes():
    policy = package_contract.build_runtime_execution_preparation_package_policy()
    assert policy.contract_ready is True
    for field in POLICY_BLOCK_FIELDS:
        assert getattr(policy, field) is False

    unsafe = dataclasses.replace(policy, runtime_execution_enabled=True)
    result = _validation(policy=unsafe)
    assert result.is_valid is False
    assert "operational_policy_flag_enabled:runtime_execution_enabled" in result.policy_violations
    decision = package_contract.decide_runtime_execution_preparation_package(result, unsafe)
    assert decision.decision == package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_POLICY_DEFAULT_DENY
    _assert_decision_never_operational(decision)


def test_metadata_safe_values_survive_and_dangerous_values_are_blocked_without_values():
    metadata = package_contract.sanitize_runtime_execution_preparation_package_metadata(
        {
            "package_reason": "safe reason",
            "package_scope": "safe scope",
            "tags": ("safe", "checkpoint"),
            "notes": ["kept"],
            "api_key": "SECRET_VALUE",
            "raw_payload": "RAW_PAYLOAD_VALUE",
            "raw_prompt": "RAW_PROMPT_VALUE",
            "raw_output": "RAW_OUTPUT_VALUE",
            "model_response": "MODEL_RESPONSE_VALUE",
            "tool_response": "TOOL_RESPONSE_VALUE",
        }
    )
    assert metadata.package_reason == "safe reason"
    assert metadata.package_scope == "safe scope"
    assert metadata.tags == ("safe", "checkpoint")
    assert metadata.notes == ("kept",)
    assert set(metadata.blocked_keys) == {
        "api_key",
        "raw_payload",
        "raw_prompt",
        "raw_output",
        "model_response",
        "tool_response",
    }
    dumped = _assert_dump_excludes_sensitive_values(metadata)
    assert "safe reason" in dumped
    for key in FORBIDDEN_METADATA_KEYS:
        assert key in package_contract.FORBIDDEN_METADATA_KEYS


def test_dependency_sets_complete_incomplete_and_optional_warnings():
    complete = _dependency_set()
    assert complete.required_dependencies() == package_contract.REQUIRED_DEPENDENCY_FIELDS
    assert complete.optional_dependencies() == package_contract.OPTIONAL_DEPENDENCY_FIELDS
    assert complete.missing_required_dependencies() == ()
    assert complete.missing_optional_dependencies() == ()

    incomplete = _dependency_set(preparation_id="", intent_ref="", dry_run_ref=None)
    assert set(incomplete.missing_required_dependencies()) == {"preparation_id", "intent_ref"}
    assert "dry_run_ref" in incomplete.missing_optional_dependencies()

    optional_missing_package = _package(dependency_set=_dependency_set(dry_run_ref=None))
    result = _validation(optional_missing_package)
    assert result.is_valid is True
    assert "missing_optional_ref:dry_run_ref" in result.warnings
    decision = package_contract.decide_runtime_execution_preparation_package(result)
    assert decision.decision == package_contract.RuntimeExecutionPreparationPackageDecision.ALLOW_SIMULATED_PACKAGE
    _assert_decision_never_operational(decision)


def test_boundary_sets_complete_incomplete_and_ui_violations():
    complete = _boundary_set()
    assert complete.missing_critical_boundaries() == ()

    incomplete = _boundary_set(
        sandbox_boundary_ok=False,
        tool_boundary_ok=False,
        model_boundary_ok=False,
        context_boundary_ok=False,
        output_boundary_ok=False,
        master_user_panel_separation_ok=False,
        ui_safe_visibility_ok=False,
    )
    assert set(incomplete.missing_critical_boundaries()) >= {
        "sandbox_boundary",
        "tool_boundary",
        "model_boundary",
        "context_boundary",
        "output_boundary",
        "master_user_panel_separation",
        "ui_safe_visibility",
    }
    result = _validation(_package(boundary_set=incomplete))
    assert result.is_valid is False
    assert "master_user_panel_separation_violated" in result.ui_visibility_violations
    assert "ui_safe_visibility_violated" in result.ui_visibility_violations


def test_complete_package_validates_as_safe_contract_only():
    package = _package()
    result = _validation(package)
    assert result.is_valid is True
    assert result.status == package_contract.RuntimeExecutionPreparationPackageStatus.PACKAGE_READY_SIMULATED
    assert result.readiness in (
        package_contract.RuntimeExecutionPreparationPackageReadiness
        .READY_FOR_RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT,
        package_contract.RuntimeExecutionPreparationPackageReadiness
        .READY_FOR_RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_E2E,
    )
    assert result.missing_required_dependencies == ()
    assert result.blocked_capabilities == package_contract.BLOCKED_CAPABILITIES
    decision = package_contract.decide_runtime_execution_preparation_package(result)
    assert decision.decision == package_contract.RuntimeExecutionPreparationPackageDecision.ALLOW_SIMULATED_PACKAGE
    assert decision.allowed is True
    assert decision.simulated_package_allowed is True
    _assert_decision_never_operational(decision)


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
def test_package_missing_required_dependency_fails(field):
    result = _validation(_package(dependency_set=_dependency_set(**{field: ""})))
    assert result.is_valid is False
    assert f"missing_required_ref:{field}" in result.errors
    decision = package_contract.decide_runtime_execution_preparation_package(result)
    assert decision.decision == package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_DEPENDENCIES
    _assert_decision_never_operational(decision)


def test_package_without_package_id_fails():
    result = _validation(_package(package_id=""))
    assert result.is_valid is False
    assert "missing_required_ref:package_id" in result.errors
    decision = package_contract.decide_runtime_execution_preparation_package(result)
    assert decision.decision in {
        package_contract.RuntimeExecutionPreparationPackageDecision.INVALID,
        package_contract.RuntimeExecutionPreparationPackageDecision.BLOCK_PACKAGE,
    }
    _assert_decision_never_operational(decision)


def test_forbidden_readiness_status_capability_metadata_policy_and_boundaries_fail():
    readiness = _validation(_package(package_readiness="ready_for_runtime"))
    assert readiness.is_valid is False
    assert "ready_for_runtime" in readiness.forbidden_readiness_detected

    bad_status_package = dataclasses.replace(_package(), package_status="package_active")
    status = _validation(bad_status_package)
    assert status.is_valid is False
    assert "package_active" in status.forbidden_status_detected

    capability = _validation(_package(blocked_capabilities=("runtime_execution",)))
    assert capability.is_valid is False
    assert "blocked_capabilities_must_match_default_deny" in capability.errors

    metadata = _validation(_package(metadata=_metadata(api_key="SECRET_VALUE")))
    assert metadata.is_valid is False
    assert metadata.metadata_blocked_keys == ("api_key",)
    _assert_dump_excludes_sensitive_values(metadata)

    unsafe_policy = dataclasses.replace(
        package_contract.build_runtime_execution_preparation_package_policy(),
        stores_enabled=True,
    )
    policy = _validation(policy=unsafe_policy)
    assert policy.is_valid is False
    assert "operational_policy_flag_enabled:stores_enabled" in policy.policy_violations

    boundary = _validation(_package(boundary_set=_boundary_set(secrets_policy_ok=False)))
    assert boundary.is_valid is False
    assert "secrets_policy" in boundary.boundary_violations

    master_user = _validation(_package(boundary_set=_boundary_set(master_user_panel_separation_ok=False)))
    assert master_user.is_valid is False
    assert "master_user_panel_separation_violated" in master_user.ui_visibility_violations

    raw_user_policy = dataclasses.replace(
        package_contract.build_runtime_execution_preparation_package_policy(),
        user_panel_raw_internal_exposure_enabled=True,
    )
    raw_user = _validation(policy=raw_user_policy)
    assert raw_user.is_valid is False
    assert (
        "operational_policy_flag_enabled:user_panel_raw_internal_exposure_enabled"
        in raw_user.policy_violations
    )


def test_negative_decisions_cover_dependencies_boundaries_metadata_policy_ui_and_invalid():
    cases = [
        (
            _validation(_package(dependency_set=_dependency_set(intent_ref=""))),
            package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_DEPENDENCIES,
        ),
        (
            _validation(_package(boundary_set=_boundary_set(tool_boundary_ok=False))),
            package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_BOUNDARIES,
        ),
        (
            _validation(_package(metadata=_metadata(api_key="SECRET_VALUE"))),
            package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_METADATA_SANITIZATION,
        ),
        (
            _validation(
                policy=dataclasses.replace(
                    package_contract.build_runtime_execution_preparation_package_policy(),
                    model_invocation_enabled=True,
                )
            ),
            package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_POLICY_DEFAULT_DENY,
        ),
        (
            _validation(_package(boundary_set=_boundary_set(ui_safe_visibility_ok=False))),
            package_contract.RuntimeExecutionPreparationPackageDecision.REQUIRE_UI_SAFE_VIEW,
        ),
        (
            _validation(_package(package_readiness="ready_for_runtime")),
            package_contract.RuntimeExecutionPreparationPackageDecision.INVALID,
        ),
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
    for result, expected in cases:
        decision = package_contract.decide_runtime_execution_preparation_package(result)
        assert decision.decision == expected
        assert decision.decision in allowed_negative
        assert decision.allowed is False
        _assert_decision_never_operational(decision)


def test_safe_views_are_reduced_serializable_and_non_operational():
    package = _package(metadata=_metadata(api_key="SECRET_VALUE", raw_prompt="RAW_PROMPT_VALUE"))
    result = _validation(package)
    views = {
        visibility: package_contract.build_runtime_execution_preparation_package_safe_view(
            package,
            result,
            visibility,
        )
        for visibility in package_contract.RuntimeExecutionPreparationPackageVisibility
    }
    for visibility, view in views.items():
        assert view.visibility == visibility
        dumped = _assert_dump_excludes_sensitive_values(view)
        assert "metadata" not in dumped
        assert "api_key" not in dumped
        assert "raw_prompt" not in dumped
        assert "raw_output" not in dumped
        assert "model_response" not in dumped
        assert "tool_response" not in dumped
        json.dumps(package_contract.runtime_execution_preparation_package_to_dict(view), sort_keys=True)
    assert "user_panel_view_reduced" in views[
        package_contract.RuntimeExecutionPreparationPackageVisibility.USER_PANEL_SAFE
    ].warnings
    assert views[package_contract.RuntimeExecutionPreparationPackageVisibility.BLOCKED].summary == (
        "Package visibility blocked."
    )


def test_snapshot_to_dict_is_complete_json_safe_and_deterministic():
    package = _package()
    validation = _validation(package)
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
    assert first["parent_contract_ref"] == "core.runtime_execution_preparation_contract"

    json_safe = package_contract.runtime_execution_preparation_package_to_dict(
        {
            "enum": package_contract.RuntimeExecutionPreparationPackageDecision.ALLOW_SIMULATED_PACKAGE,
            "dataclass": validation,
            "tuple": ("a", "b"),
            "frozenset": frozenset({"c", "d"}),
            "list": [package_contract.RuntimeExecutionPreparationPackageRiskLevel.LOW],
            "dict": {"status": package_contract.RuntimeExecutionPreparationPackageStatus.PACKAGE_READY_SIMULATED},
        }
    )
    json.dumps(json_safe, sort_keys=True)


def test_pure_calls_do_not_create_files_logs_stores_or_events():
    before = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    package = _package()
    validation = _validation(package)
    decision = package_contract.decide_runtime_execution_preparation_package(validation)
    safe_view = package_contract.build_runtime_execution_preparation_package_safe_view(
        package,
        validation,
        package_contract.RuntimeExecutionPreparationPackageVisibility.MASTER_PANEL_SAFE,
    )
    snapshot = package_contract.build_runtime_execution_preparation_package_contract_snapshot(
        package=package,
        validation=validation,
        decision=decision,
        safe_view=safe_view,
    )
    package_contract.runtime_execution_preparation_package_to_dict(snapshot)
    package_contract.get_runtime_execution_preparation_package_contract_status()
    after = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert before == after


def test_module_source_has_no_real_execution_io_network_env_or_secret_access():
    source = MODULE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = [
        "import subprocess",
        "from subprocess",
        "import socket",
        "from socket",
        "import requests",
        "import httpx",
        "import urllib",
        "import webbrowser",
        "from pathlib",
        "os.environ",
        "getenv",
        "open(",
        "Path(",
        "write_text",
        "emit",
        "publish",
        "tool_executor",
        "model_invoker",
        "browser_operator",
        "ui_tars_adapter",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_previous_contracts_boundaries_and_operational_modules_remain_blocked():
    for module_name in PREVIOUS_CONTRACTS_AND_BOUNDARIES:
        _assert_all_operational_flags_false(module_name)

    runtime_executor = ROOT / "core" / "runtime_executor.py"
    if runtime_executor.exists():
        assert "prepare-only" in runtime_executor.read_text(encoding="utf-8").lower()

    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative


def test_market_catalog_business_composition_runtime_and_obliteratus_remain_blocked():
    assert "market_catalog_runtime" in package_contract.BLOCKED_CAPABILITIES
    assert "business_composition_runtime" in package_contract.BLOCKED_CAPABILITIES
    assert "obliteratus_integration" in package_contract.BLOCKED_CAPABILITIES
    assert package_contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    for statement in package_contract.OBLITERATUS_EXCLUSION_STATEMENTS:
        assert "OBLITERATUS" in statement
        assert "not" in statement or "excluded" in statement
    snapshot = package_contract.runtime_execution_preparation_package_to_dict(
        package_contract.build_runtime_execution_preparation_package_contract_snapshot()
    )
    dumped = json.dumps(snapshot, sort_keys=True)
    assert "OBLITERATUS" not in dumped
    assert "obliteratus_integration" in dumped


def test_e2e_document_exists_and_contains_required_markers():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "Runtime Execution Preparation Package Contract Full E2E Checkpoint",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_CHAIN_READY",
        "ready_for_runtime_execution_preparation_read_model_audit",
        "PROMPT 4.4 - Auditoria de Runtime Execution Preparation Read Model",
    ]:
        assert token in text
