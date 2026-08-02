import dataclasses
import importlib
import json
from pathlib import Path

import pytest

import core.runtime_execution_preparation_contract as parent_contract
import core.runtime_execution_preparation_package as package_contract
import core.runtime_execution_preparation_read_model as read_model_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_FULL_E2E_CHECKPOINT.md"
MODULE_PATH = ROOT / "core" / "runtime_execution_preparation_read_model.py"


def _metadata(**overrides):
    data = {
        "read_model_reason": "full e2e",
        "read_model_scope": "contract",
        "created_by": "pytest",
        "source": "runtime_execution_preparation_read_model_contract_full_e2e",
        "tags": ("read_model", "e2e"),
        "notes": ("read only", "non operational"),
        "package_ref": "pkg_full_e2e",
        "contract_ref": "read_model_contract",
        "visibility": "internal_only",
    }
    data.update(overrides)
    return read_model_contract.sanitize_runtime_execution_preparation_read_model_metadata(data)


def _source_ref(**overrides):
    data = {
        "package_id": "pkg_full_e2e",
        "preparation_id": "prep_full_e2e",
        "intent_ref": "intent_full_e2e",
        "attempt_ref": "attempt_full_e2e",
        "source_package_ref": "core.runtime_execution_preparation_package",
        "source_contract_ref": "core.runtime_execution_preparation_read_model",
        "safe_view_ref": "safe_view_full_e2e",
        "parent_contract_ref": "core.runtime_execution_preparation_contract",
    }
    data.update(overrides)
    return read_model_contract.build_runtime_execution_preparation_read_model_source_ref(**data)


def _read_model(**overrides):
    data = {
        "read_model_id": "read_model_full_e2e",
        "source_ref": _source_ref(),
        "execution_scope": "future_safe_projection",
        "execution_mode": "contract_only",
        "readiness": "ready_for_runtime_execution_preparation_read_model_contract_e2e",
        "metadata": _metadata(),
    }
    data.update(overrides)
    return read_model_contract.build_runtime_execution_preparation_read_model(**data)


def _views(model=None):
    active = model or _read_model()
    master = read_model_contract.build_runtime_execution_preparation_master_panel_view(
        active,
        technical_refs=("source_package_ref", "source_contract_ref"),
    )
    user = read_model_contract.build_runtime_execution_preparation_user_panel_view(active)
    audit = read_model_contract.build_runtime_execution_preparation_internal_audit_view(
        active,
        sanitized_refs=("package_ref", "contract_ref"),
    )
    return master, user, audit


def _validation(model=None, policy=None, views=None):
    active = model or _read_model()
    master, user, audit = views or _views(active)
    return read_model_contract.validate_runtime_execution_preparation_read_model(
        active,
        policy=policy,
        master_view=master,
        user_view=user,
        audit_view=audit,
    )


def _dump(value):
    return json.dumps(read_model_contract.runtime_execution_preparation_read_model_to_dict(value), sort_keys=True)


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
        "api_allowed",
        "ui_allowed",
        "permission_bypass_allowed",
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


def test_imports_and_parent_contracts_are_safe():
    module = importlib.import_module("core.runtime_execution_preparation_read_model")
    assert module.package_contract is package_contract
    assert module.parent_contract is parent_contract
    assert module.PARENT_PACKAGE_CONTRACT_REF == "core.runtime_execution_preparation_package"
    assert module.PARENT_PREPARATION_CONTRACT_REF == "core.runtime_execution_preparation_contract"
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY is True
    assert parent_contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY is True


def test_read_model_flags_are_ready_and_default_deny():
    assert read_model_contract.RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_READY is True
    for name in [
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_OPERATIONAL",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_RUNTIME_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_EXECUTION_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_DRY_RUN_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_TOOLS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_MODELS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTEXT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_OUTPUT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_WRITES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_STORES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_MEMORY_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_NETWORK_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_BROWSER_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_FILESYSTEM_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_ENV_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_SECRETS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_API_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_UI_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_UI_DEVICE_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_INTEGRATIONS_ENABLED",
    ]:
        assert getattr(read_model_contract, name) is False


def test_policy_is_read_only_and_blocks_every_operational_axis():
    policy = read_model_contract.build_runtime_execution_preparation_read_model_policy()
    assert policy.contract_ready is True
    assert policy.read_only_enabled is True
    for field in dataclasses.fields(policy):
        if field.name not in {"contract_ready", "read_only_enabled"}:
            assert getattr(policy, field.name) is False
    expected_operational_fields = {
        "read_model_operational_enabled",
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
        "api_enabled",
        "ui_enabled",
        "ui_device_enabled",
        "integrations_enabled",
        "master_panel_internal_exposure_enabled",
        "user_panel_raw_internal_exposure_enabled",
        "permission_bypass_enabled",
    }
    assert expected_operational_fields <= {field.name for field in dataclasses.fields(policy)}


def test_parent_package_and_preparation_flags_remain_default_deny():
    _assert_false_flags("core.runtime_execution_preparation_package")
    _assert_false_flags("core.runtime_execution_preparation_contract")


def test_metadata_safe_values_survive_and_dangerous_values_are_blocked():
    metadata = read_model_contract.sanitize_runtime_execution_preparation_read_model_metadata(
        {
            "read_model_reason": "safe reason",
            "package_ref": "pkg_safe",
            "contract_ref": "contract_safe",
            "api_key": "SECRET_VALUE",
            "raw_prompt": "RAW_PROMPT_VALUE",
            "raw_output": "RAW_OUTPUT_VALUE",
            "model_response": "MODEL_RESPONSE_VALUE",
            "tool_response": "TOOL_RESPONSE_VALUE",
            "permission_bypass": "BYPASS_VALUE",
        }
    )
    assert metadata.read_model_reason == "safe reason"
    assert metadata.package_ref == "pkg_safe"
    assert metadata.contract_ref == "contract_safe"
    assert set(metadata.blocked_keys) == {
        "api_key",
        "raw_prompt",
        "raw_output",
        "model_response",
        "tool_response",
        "permission_bypass",
    }
    dumped = _dump(metadata)
    for value in [
        "SECRET_VALUE",
        "RAW_PROMPT_VALUE",
        "RAW_OUTPUT_VALUE",
        "MODEL_RESPONSE_VALUE",
        "TOOL_RESPONSE_VALUE",
        "BYPASS_VALUE",
    ]:
        assert value not in dumped
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
        "master_panel_internal_capability",
        "admin_secret",
        "permission_bypass",
    ]:
        assert key in read_model_contract.FORBIDDEN_METADATA_KEYS


def test_source_ref_complete_and_incomplete_validation():
    assert _source_ref().missing_critical_source_refs() == ()
    incomplete = _source_ref(
        package_id="",
        preparation_id="",
        intent_ref="",
        source_package_ref="",
        source_contract_ref="",
    )
    assert set(incomplete.missing_critical_source_refs()) == {
        "package_id",
        "preparation_id",
        "intent_ref",
        "source_package_ref",
        "source_contract_ref",
    }


def test_complete_read_model_views_and_validation_are_safe():
    model = _read_model()
    master, user, audit = _views(model)
    result = _validation(model, views=(master, user, audit))
    assert result.is_valid is True
    assert result.readiness in read_model_contract.ALLOWED_READINESS
    assert result.readiness == "ready_for_runtime_execution_preparation_read_model_contract_e2e"
    assert result.status == read_model_contract.RuntimeExecutionPreparationReadModelStatus.READ_MODEL_READY_SIMULATED
    assert result.missing_source_refs == ()
    assert result.view_violations == ()
    assert model.blocked_capabilities == read_model_contract.BLOCKED_CAPABILITIES
    assert master.visibility == read_model_contract.RuntimeExecutionPreparationReadModelVisibility.MASTER_PANEL_VIEW
    assert user.visibility == read_model_contract.RuntimeExecutionPreparationReadModelVisibility.USER_PANEL_VIEW
    assert audit.visibility == read_model_contract.RuntimeExecutionPreparationReadModelVisibility.INTERNAL_AUDIT_VIEW


@pytest.mark.parametrize(
    ("model", "error"),
    [
        (_read_model(read_model_id=""), "missing_required_ref:read_model_id"),
        (_read_model(source_ref=_source_ref(package_id="")), "missing_source_ref:package_id"),
        (_read_model(source_ref=_source_ref(preparation_id="")), "missing_source_ref:preparation_id"),
        (_read_model(source_ref=_source_ref(intent_ref="")), "missing_source_ref:intent_ref"),
        (_read_model(source_ref=_source_ref(source_package_ref="")), "missing_source_ref:source_package_ref"),
        (_read_model(source_ref=_source_ref(source_contract_ref="")), "missing_source_ref:source_contract_ref"),
    ],
)
def test_missing_required_core_and_source_refs_fail(model, error):
    result = _validation(model)
    assert result.is_valid is False
    assert error in result.errors


def test_forbidden_readiness_status_metadata_policy_and_permission_bypass_fail():
    readiness = _validation(_read_model(readiness="ready_for_runtime"))
    assert readiness.is_valid is False
    assert readiness.forbidden_readiness_detected == ("ready_for_runtime",)

    bad_status = dataclasses.replace(_read_model(), status="read_model_active")
    status = _validation(bad_status)
    assert status.is_valid is False
    assert status.forbidden_status_detected == ("read_model_active",)

    metadata = _validation(_read_model(metadata=_metadata(api_key="SECRET_VALUE")))
    assert metadata.is_valid is False
    assert metadata.metadata_blocked_keys == ("api_key",)

    unsafe_policy = dataclasses.replace(
        read_model_contract.build_runtime_execution_preparation_read_model_policy(),
        runtime_execution_enabled=True,
    )
    policy = _validation(policy=unsafe_policy)
    assert policy.is_valid is False
    assert "operational_policy_flag_enabled:runtime_execution_enabled" in policy.policy_violations

    bypass_policy = dataclasses.replace(
        read_model_contract.build_runtime_execution_preparation_read_model_policy(),
        permission_bypass_enabled=True,
    )
    bypass = _validation(policy=bypass_policy)
    assert bypass.is_valid is False
    assert "operational_policy_flag_enabled:permission_bypass_enabled" in bypass.policy_violations


def test_views_do_not_expose_raw_sensitive_or_user_forbidden_internals():
    model = _read_model(
        metadata=_metadata(
            api_key="SECRET_VALUE",
            raw_payload="RAW_PAYLOAD_VALUE",
            raw_prompt="RAW_PROMPT_VALUE",
            raw_output="RAW_OUTPUT_VALUE",
            model_response="MODEL_RESPONSE_VALUE",
            tool_response="TOOL_RESPONSE_VALUE",
            authorization="AUTH_VALUE",
            bearer="BEARER_VALUE",
        )
    )
    master, user, audit = _views(model)
    for view in [master, user]:
        dumped = _dump(view)
        for token in [
            "SECRET_VALUE",
            "RAW_PAYLOAD_VALUE",
            "RAW_PROMPT_VALUE",
            "RAW_OUTPUT_VALUE",
            "MODEL_RESPONSE_VALUE",
            "TOOL_RESPONSE_VALUE",
            "AUTH_VALUE",
            "BEARER_VALUE",
            "raw_payload",
            "raw_prompt",
            "raw_output",
            "model_response",
            "tool_response",
            "authorization",
            "bearer",
            "personal_data_unsanitized",
        ]:
            assert token not in dumped
    user_dump = _dump(user)
    for token in [
        "metadata",
        "technical_refs",
        "master_panel",
        "admin",
        "security_internal",
        "permission_internal",
        "intent_internal",
        "attempt_internal",
    ]:
        assert token not in user_dump
    audit_dump = _dump(audit)
    for raw_value in [
        "SECRET_VALUE",
        "RAW_PAYLOAD_VALUE",
        "RAW_PROMPT_VALUE",
        "RAW_OUTPUT_VALUE",
        "MODEL_RESPONSE_VALUE",
        "TOOL_RESPONSE_VALUE",
        "AUTH_VALUE",
        "BEARER_VALUE",
    ]:
        assert raw_value not in audit_dump
    assert set(audit.blocked_keys) == {
        "api_key",
        "raw_payload",
        "raw_prompt",
        "raw_output",
        "model_response",
        "tool_response",
        "authorization",
        "bearer",
    }


def test_unsafe_user_view_requires_visibility_filtering():
    model = _read_model()
    master, _, audit = _views(model)
    unsafe_user = dataclasses.replace(
        read_model_contract.build_runtime_execution_preparation_user_panel_view(model),
        safe_summary="technical_refs master_panel security_internal raw_prompt",
    )
    result = _validation(model, views=(master, unsafe_user, audit))
    assert result.is_valid is False
    assert any("user_panel_view_contains_forbidden_fragment" in item for item in result.view_violations)
    decision = read_model_contract.decide_runtime_execution_preparation_read_model(result)
    assert decision.decision == read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_VISIBILITY_FILTERING
    _assert_decision_never_operational(decision)


def test_decisions_positive_and_negative_never_enable_operations():
    valid = _validation()
    allowed = read_model_contract.decide_runtime_execution_preparation_read_model(valid)
    assert allowed.decision == read_model_contract.RuntimeExecutionPreparationReadModelDecision.ALLOW_READ_ONLY_MODEL
    assert allowed.allowed is True
    assert allowed.read_only_model_allowed is True
    _assert_decision_never_operational(allowed)

    unsafe_user_model = _read_model()
    master, _, audit = _views(unsafe_user_model)
    unsafe_user = dataclasses.replace(
        read_model_contract.build_runtime_execution_preparation_user_panel_view(unsafe_user_model),
        safe_summary="raw_prompt",
    )
    negative_cases = [
        (
            _validation(_read_model(source_ref=_source_ref(package_id=""))),
            read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_SOURCE_REFS,
        ),
        (
            read_model_contract.validate_runtime_execution_preparation_read_model(_read_model()),
            read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_SAFE_VIEW,
        ),
        (
            _validation(_read_model(metadata=_metadata(api_key="x"))),
            read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_METADATA_SANITIZATION,
        ),
        (
            _validation(
                policy=dataclasses.replace(
                    read_model_contract.build_runtime_execution_preparation_read_model_policy(),
                    stores_enabled=True,
                )
            ),
            read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_POLICY_DEFAULT_DENY,
        ),
        (
            _validation(unsafe_user_model, views=(master, unsafe_user, audit)),
            read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_VISIBILITY_FILTERING,
        ),
        (
            _validation(_read_model(readiness="ready_for_runtime")),
            read_model_contract.RuntimeExecutionPreparationReadModelDecision.INVALID,
        ),
    ]
    allowed_negative = {
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.BLOCK_READ_MODEL,
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_SOURCE_REFS,
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_SAFE_VIEW,
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_METADATA_SANITIZATION,
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_POLICY_DEFAULT_DENY,
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.REQUIRE_VISIBILITY_FILTERING,
        read_model_contract.RuntimeExecutionPreparationReadModelDecision.INVALID,
    }
    for validation, expected_decision in negative_cases:
        decision = read_model_contract.decide_runtime_execution_preparation_read_model(validation)
        assert decision.decision == expected_decision
        assert decision.decision in allowed_negative
        assert decision.allowed is False
        _assert_decision_never_operational(decision)


def test_to_dict_handles_json_safe_shapes():
    payload = {
        "enum": read_model_contract.RuntimeExecutionPreparationReadModelDecision.ALLOW_READ_ONLY_MODEL,
        "dataclass": _metadata(),
        "tuple": ("a", "b"),
        "frozenset": frozenset({"x", "y"}),
        "list": [1, 2],
        "dict": {"nested": _source_ref()},
    }
    converted = read_model_contract.runtime_execution_preparation_read_model_to_dict(payload)
    assert converted["enum"] == "allow_read_only_model"
    assert sorted(converted["frozenset"]) == ["x", "y"]
    json.dumps(converted, sort_keys=True)


def test_snapshots_and_contract_snapshots_are_complete_json_safe_and_deterministic():
    source = _source_ref()
    model = _read_model(source_ref=source)
    master, user, audit = _views(model)
    validation = _validation(model, views=(master, user, audit))
    decision = read_model_contract.decide_runtime_execution_preparation_read_model(validation)
    snapshot = read_model_contract.build_runtime_execution_preparation_read_model_snapshot(
        read_model=model,
        master_panel_view=master,
        user_panel_view=user,
        internal_audit_view=audit,
        validation=validation,
        decision=decision,
        source_refs=source,
    )
    contract_snapshot = read_model_contract.build_runtime_execution_preparation_read_model_contract_snapshot(
        read_model=model,
        master_panel_view=master,
        user_panel_view=user,
        internal_audit_view=audit,
        validation=validation,
        decision=decision,
        source_refs=source,
    )
    snapshot_dict = read_model_contract.runtime_execution_preparation_read_model_to_dict(snapshot)
    first = read_model_contract.runtime_execution_preparation_read_model_to_dict(contract_snapshot)
    second = read_model_contract.runtime_execution_preparation_read_model_to_dict(contract_snapshot)
    assert first == second
    json.dumps(snapshot_dict, sort_keys=True)
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
        "read_model",
        "master_panel_view",
        "user_panel_view",
        "internal_audit_view",
        "validation",
        "decision",
        "source_refs",
        "parent_package_contract_ref",
        "parent_preparation_contract_ref",
    ]:
        assert field in first


def test_pure_calls_have_no_side_effects_logs_stores_or_events():
    before = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    source = _source_ref()
    model = _read_model(source_ref=source)
    master, user, audit = _views(model)
    validation = _validation(model, views=(master, user, audit))
    decision = read_model_contract.decide_runtime_execution_preparation_read_model(validation)
    read_model_contract.runtime_execution_preparation_read_model_to_dict(
        read_model_contract.build_runtime_execution_preparation_read_model_contract_snapshot(
            read_model=model,
            master_panel_view=master,
            user_panel_view=user,
            internal_audit_view=audit,
            validation=validation,
            decision=decision,
            source_refs=source,
        )
    )
    after = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert before == after


def test_module_source_does_not_use_runtime_or_external_execution_capabilities():
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in [
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
        "tool_executor",
        "model_invoker",
        "browser_operator",
        "ui_tars_adapter",
    ]:
        assert forbidden not in source


def test_previous_contracts_and_boundaries_remain_blocked():
    for module_name in [
        "core.runtime_execution_preparation_read_model",
        "core.runtime_execution_preparation_package",
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


def test_forbidden_operational_modules_are_not_created():
    allowed_preexisting = {
        "core/runtime_execution_preparation_projection.py": "contract-only",
        "core/runtime_executor.py": "prepare-only",
    }
    for relative in [
        "core/runtime_execution_preparation_projection.py",
        "core/runtime_execution_preparation_store.py",
        "core/runtime_execution_preparation_writer.py",
        "core/runtime_execution_preparation_reader.py",
        "core/runtime_execution_preparation_api.py",
        "core/runtime_execution_preparation_ui.py",
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


def test_market_catalog_bcl_and_obliteratus_remain_blocked_or_excluded():
    assert "market_catalog_runtime" in read_model_contract.BLOCKED_CAPABILITIES
    assert "business_composition_runtime" in read_model_contract.BLOCKED_CAPABILITIES
    assert "obliteratus_integration" in read_model_contract.BLOCKED_CAPABILITIES
    assert read_model_contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    snapshot = read_model_contract.runtime_execution_preparation_read_model_to_dict(
        read_model_contract.build_runtime_execution_preparation_read_model_contract_snapshot()
    )
    dumped = json.dumps(snapshot, sort_keys=True)
    assert "OBLITERATUS" not in dumped
    assert "obliteratus_integration" in dumped


def test_e2e_document_exists_and_contains_required_markers():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_CHAIN_READY",
        "ready_for_runtime_execution_preparation_projection_audit",
        "PROMPT 4.6 - Auditoria de Runtime Execution Preparation Projection",
    ]:
        assert token in text
