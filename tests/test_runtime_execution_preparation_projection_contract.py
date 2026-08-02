import dataclasses
import importlib
import json
from pathlib import Path

import core.runtime_execution_preparation_contract as parent_contract
import core.runtime_execution_preparation_package as package_contract
import core.runtime_execution_preparation_projection as projection_contract
import core.runtime_execution_preparation_read_model as read_model_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT.md"
MODULE_PATH = ROOT / "core" / "runtime_execution_preparation_projection.py"


def _metadata(**overrides):
    data = {
        "projection_reason": "unit test",
        "projection_scope": "contract",
        "projection_kind": "summary_projection",
        "created_by": "pytest",
        "source": "tests",
        "tags": ("projection", "safe"),
        "notes": ("read only",),
        "read_model_ref": "read_model_1",
        "package_ref": "pkg_1",
        "contract_ref": "projection_contract",
        "visibility": "internal_only",
    }
    data.update(overrides)
    return projection_contract.sanitize_runtime_execution_preparation_projection_metadata(data)


def _source_ref(**overrides):
    data = {
        "projection_id": "projection_1",
        "read_model_id": "read_model_1",
        "package_id": "pkg_1",
        "preparation_id": "prep_1",
        "intent_ref": "intent_1",
        "attempt_ref": "attempt_1",
        "source_read_model_ref": "core.runtime_execution_preparation_read_model",
        "source_package_ref": "core.runtime_execution_preparation_package",
        "source_contract_refs": (
            "core.runtime_execution_preparation_projection",
            "core.runtime_execution_preparation_read_model",
            "core.runtime_execution_preparation_package",
        ),
        "parent_read_model_contract_ref": "core.runtime_execution_preparation_read_model",
        "parent_package_contract_ref": "core.runtime_execution_preparation_package",
        "parent_preparation_contract_ref": "core.runtime_execution_preparation_contract",
    }
    data.update(overrides)
    return projection_contract.build_runtime_execution_preparation_projection_source_ref(**data)


def _projection(**overrides):
    data = {
        "source_ref": _source_ref(),
        "projection_kind": "summary_projection",
        "projection_readiness": "ready_for_runtime_execution_preparation_projection_contract_e2e",
        "visibility": "internal_only",
        "metadata": _metadata(),
    }
    data.update(overrides)
    return projection_contract.build_runtime_execution_preparation_projection(**data)


def _views(projection=None):
    active = projection or _projection()
    master = projection_contract.build_runtime_execution_preparation_master_panel_projection(
        active,
        technical_refs=("source_read_model_ref", "source_package_ref"),
    )
    user = projection_contract.build_runtime_execution_preparation_user_panel_projection(active)
    audit = projection_contract.build_runtime_execution_preparation_internal_audit_projection(
        active,
        sanitized_refs=("source_read_model_ref", "source_package_ref"),
    )
    summary = projection_contract.build_runtime_execution_preparation_summary_projection(active)
    status_only = projection_contract.build_runtime_execution_preparation_status_only_projection(active)
    blocked = projection_contract.build_runtime_execution_preparation_blocked_projection(active, "contract_only")
    return master, user, audit, summary, status_only, blocked


def _validation(projection=None, policy=None, views=None):
    active = projection or _projection()
    master, user, audit, summary, status_only, blocked = views or _views(active)
    return projection_contract.validate_runtime_execution_preparation_projection(
        active,
        policy=policy,
        master_projection=master,
        user_projection=user,
        internal_audit_projection=audit,
        summary_projection=summary,
        status_only_projection=status_only,
        blocked_projection=blocked,
    )


def _dump(value):
    return json.dumps(projection_contract.runtime_execution_preparation_projection_to_dict(value), sort_keys=True)


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
        "raw_package_to_user_projection_allowed",
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


def test_module_imports_and_references_previous_contracts_safely():
    module = importlib.import_module("core.runtime_execution_preparation_projection")
    assert module.read_model_contract is read_model_contract
    assert module.package_contract is package_contract
    assert module.parent_contract is parent_contract
    assert module.PARENT_READ_MODEL_CONTRACT_REF == "core.runtime_execution_preparation_read_model"
    assert module.PARENT_PACKAGE_CONTRACT_REF == "core.runtime_execution_preparation_package"
    assert module.PARENT_PREPARATION_CONTRACT_REF == "core.runtime_execution_preparation_contract"


def test_flags_are_ready_read_only_and_non_operational():
    assert projection_contract.RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_READY is True
    for name in [
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_OPERATIONAL",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_RUNTIME_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_EXECUTION_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_DRY_RUN_ACTIVE",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_TOOLS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_MODELS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTEXT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_OUTPUT_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_WRITES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_STORES_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_MEMORY_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_NETWORK_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_BROWSER_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_FILESYSTEM_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_ENV_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_SECRETS_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_API_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_UI_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_UI_DEVICE_ENABLED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_INTEGRATIONS_ENABLED",
    ]:
        assert getattr(projection_contract, name) is False


def test_dataclasses_are_frozen():
    for name in [
        "RuntimeExecutionPreparationProjectionPolicy",
        "RuntimeExecutionPreparationProjectionMetadata",
        "RuntimeExecutionPreparationProjectionSourceRef",
        "RuntimeExecutionPreparationProjectionCore",
        "RuntimeExecutionPreparationMasterPanelProjection",
        "RuntimeExecutionPreparationUserPanelProjection",
        "RuntimeExecutionPreparationInternalAuditProjection",
        "RuntimeExecutionPreparationSummaryProjection",
        "RuntimeExecutionPreparationStatusOnlyProjection",
        "RuntimeExecutionPreparationBlockedProjection",
        "RuntimeExecutionPreparationProjectionValidationResult",
        "RuntimeExecutionPreparationProjectionDecisionRecord",
        "RuntimeExecutionPreparationProjectionSnapshot",
        "RuntimeExecutionPreparationProjectionContractSnapshot",
    ]:
        cls = getattr(projection_contract, name)
        assert dataclasses.is_dataclass(cls)
        assert cls.__dataclass_params__.frozen is True


def test_enums_allowed_forbidden_readiness_kinds_visibility_and_capabilities():
    for status in [
        "projection_uninitialized",
        "projection_draft",
        "projection_source_required",
        "projection_read_model_required",
        "projection_package_required",
        "projection_visibility_required",
        "projection_filtering_required",
        "projection_ready_simulated",
        "projection_blocked",
        "projection_invalid",
        "projection_archived_simulated",
    ]:
        assert status in projection_contract.ALLOWED_STATUSES
    for status in [
        "projection_active",
        "projection_running",
        "projection_executing",
        "projection_operational",
        "projection_api_active",
        "projection_ui_control_active",
    ]:
        assert status in projection_contract.FORBIDDEN_STATUSES
    assert projection_contract.ALLOWED_READINESS == (
        "ready_for_runtime_execution_preparation_projection_contract",
        "ready_for_runtime_execution_preparation_projection_contract_e2e",
    )
    for readiness in [
        "ready_for_runtime",
        "ready_for_execution",
        "ready_for_dry_run_execution",
        "ready_for_api",
        "ready_for_ui",
        "projection_operational",
        "projection_store_enabled",
        "projection_writer_enabled",
        "projection_api_enabled",
        "projection_ui_enabled",
    ]:
        assert readiness in projection_contract.FORBIDDEN_READINESS
    assert projection_contract.PROJECTION_KINDS == (
        "master_panel_projection",
        "user_panel_projection",
        "internal_audit_projection",
        "summary_projection",
        "status_only_projection",
        "blocked_projection",
    )
    for visibility in ["master_panel", "user_panel", "internal_audit", "summary_only", "status_only", "internal_only", "blocked"]:
        assert visibility in [item.value for item in projection_contract.RuntimeExecutionPreparationProjectionVisibility]
    for capability in [
        "runtime_execution",
        "runtime_activation",
        "dry_run_execution",
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
        "ui",
        "ui_control",
        "device_control",
        "integrations",
        "market_catalog_runtime",
        "business_composition_runtime",
        "obliteratus_integration",
        "master_panel_internal_capability_exposure",
        "user_panel_raw_internal_exposure",
        "permission_bypass",
        "raw_package_to_user_projection",
    ]:
        assert capability in projection_contract.BLOCKED_CAPABILITIES


def test_metadata_safe_values_survive_and_dangerous_values_are_blocked():
    metadata = projection_contract.sanitize_runtime_execution_preparation_projection_metadata(
        {
            "projection_reason": "safe",
            "read_model_ref": "read_model",
            "package_ref": "package",
            "contract_ref": "contract",
            "api_key": "SECRET_VALUE",
            "raw_prompt": "RAW_PROMPT_VALUE",
            "raw_output": "RAW_OUTPUT_VALUE",
            "model_response": "MODEL_RESPONSE_VALUE",
            "raw_master_panel_view": "MASTER_VALUE",
            "permission_bypass": "BYPASS_VALUE",
        }
    )
    dumped = _dump(metadata)
    assert metadata.projection_reason == "safe"
    assert metadata.read_model_ref == "read_model"
    assert metadata.package_ref == "package"
    assert set(metadata.blocked_keys) == {
        "api_key",
        "raw_prompt",
        "raw_output",
        "model_response",
        "raw_master_panel_view",
        "permission_bypass",
    }
    for value in ["SECRET_VALUE", "RAW_PROMPT_VALUE", "RAW_OUTPUT_VALUE", "MODEL_RESPONSE_VALUE", "MASTER_VALUE", "BYPASS_VALUE"]:
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
        "raw_master_panel_view",
        "raw_user_panel_view",
        "raw_internal_audit_view",
    ]:
        assert key in projection_contract.FORBIDDEN_METADATA_KEYS


def test_policy_default_deny_and_operational_policy_fails():
    policy = projection_contract.build_runtime_execution_preparation_projection_policy()
    assert policy.contract_ready is True
    assert policy.read_only_enabled is True
    for field in dataclasses.fields(policy):
        if field.name not in {"contract_ready", "read_only_enabled"}:
            assert getattr(policy, field.name) is False
    unsafe = dataclasses.replace(policy, writes_enabled=True)
    result = _validation(policy=unsafe)
    assert result.is_valid is False
    assert "operational_policy_flag_enabled:writes_enabled" in result.policy_violations
    bypass = dataclasses.replace(policy, permission_bypass_enabled=True)
    bypass_result = _validation(policy=bypass)
    assert bypass_result.is_valid is False
    assert "operational_policy_flag_enabled:permission_bypass_enabled" in bypass_result.policy_violations
    raw_package = dataclasses.replace(policy, raw_package_to_user_projection_enabled=True)
    raw_package_result = _validation(policy=raw_package)
    assert raw_package_result.is_valid is False
    assert "operational_policy_flag_enabled:raw_package_to_user_projection_enabled" in raw_package_result.policy_violations


def test_source_ref_complete_and_incomplete_detection():
    complete = _source_ref()
    assert complete.missing_critical_source_refs() == ()
    incomplete = _source_ref(
        projection_id="",
        read_model_id="",
        package_id="",
        preparation_id="",
        intent_ref="",
        source_read_model_ref="",
        source_package_ref="",
        parent_read_model_contract_ref="",
        parent_package_contract_ref="",
        parent_preparation_contract_ref="",
    )
    assert set(incomplete.missing_critical_source_refs()) == {
        "projection_id",
        "read_model_id",
        "package_id",
        "preparation_id",
        "intent_ref",
        "source_read_model_ref",
        "source_package_ref",
        "parent_read_model_contract_ref",
        "parent_package_contract_ref",
        "parent_preparation_contract_ref",
    }


def test_complete_projection_views_and_validation_are_safe():
    projection = _projection()
    master, user, audit, summary, status_only, blocked = _views(projection)
    result = _validation(projection, views=(master, user, audit, summary, status_only, blocked))
    assert result.is_valid is True
    assert result.readiness in projection_contract.ALLOWED_READINESS
    assert result.status == projection_contract.RuntimeExecutionPreparationProjectionStatus.PROJECTION_READY_SIMULATED
    assert result.missing_source_refs == ()
    assert result.projection_violations == ()


def test_missing_required_core_and_source_refs_fail():
    cases = [
        (_projection(source_ref=_source_ref(projection_id="")), "missing_source_ref:projection_id"),
        (_projection(source_ref=_source_ref(read_model_id="")), "missing_source_ref:read_model_id"),
        (_projection(source_ref=_source_ref(package_id="")), "missing_source_ref:package_id"),
        (_projection(source_ref=_source_ref(preparation_id="")), "missing_source_ref:preparation_id"),
        (_projection(source_ref=_source_ref(intent_ref="")), "missing_source_ref:intent_ref"),
        (_projection(source_ref=_source_ref(source_read_model_ref="")), "missing_source_ref:source_read_model_ref"),
        (_projection(source_ref=_source_ref(source_package_ref="")), "missing_source_ref:source_package_ref"),
        (
            _projection(source_ref=_source_ref(parent_read_model_contract_ref="")),
            "missing_source_ref:parent_read_model_contract_ref",
        ),
        (
            _projection(source_ref=_source_ref(parent_package_contract_ref="")),
            "missing_source_ref:parent_package_contract_ref",
        ),
        (
            _projection(source_ref=_source_ref(parent_preparation_contract_ref="")),
            "missing_source_ref:parent_preparation_contract_ref",
        ),
    ]
    for projection, error in cases:
        result = _validation(projection)
        assert result.is_valid is False
        assert error in result.errors


def test_forbidden_readiness_status_metadata_policy_and_views_fail():
    readiness = _validation(_projection(projection_readiness="ready_for_runtime"))
    assert readiness.is_valid is False
    assert "ready_for_runtime" in readiness.forbidden_readiness_detected

    bad_status = dataclasses.replace(_projection(), projection_status="projection_active")
    status = _validation(bad_status)
    assert status.is_valid is False
    assert "projection_active" in status.forbidden_status_detected

    metadata = _validation(_projection(metadata=_metadata(api_key="SECRET_VALUE")))
    assert metadata.is_valid is False
    assert metadata.metadata_blocked_keys == ("api_key",)

    model = _projection()
    master, _, audit, summary, status_only, blocked = _views(model)
    unsafe_user = dataclasses.replace(
        projection_contract.build_runtime_execution_preparation_user_panel_projection(model),
        safe_summary="technical_refs master_panel security_internal raw_package_contract raw_read_model_contract raw_prompt",
    )
    unsafe_view = _validation(model, views=(master, unsafe_user, audit, summary, status_only, blocked))
    assert unsafe_view.is_valid is False
    assert any("user_panel_projection_contains_forbidden_fragment" in item for item in unsafe_view.projection_violations)


def test_projection_views_do_not_expose_raw_or_sensitive_values():
    projection = _projection(
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
    master, user, audit, summary, status_only, blocked = _views(projection)
    for view in [master, user, summary, status_only, blocked]:
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
        "raw_package_contract",
        "raw_read_model_contract",
    ]:
        assert token not in user_dump
    audit_dump = _dump(audit)
    for raw_value in ["SECRET_VALUE", "RAW_PAYLOAD_VALUE", "RAW_PROMPT_VALUE", "RAW_OUTPUT_VALUE", "MODEL_RESPONSE_VALUE"]:
        assert raw_value not in audit_dump
    assert "raw_prompt" in audit.blocked_keys


def test_minimal_projection_shapes_and_blocked_projection_do_not_enable_actions():
    projection = _projection()
    _, user, _, summary, status_only, blocked = _views(projection)
    assert set(dataclasses.asdict(summary)) == {
        "projection_id",
        "package_id",
        "status",
        "readiness",
        "risk_level",
        "safe_summary",
        "visibility",
    }
    assert set(dataclasses.asdict(status_only)) == {
        "projection_id",
        "package_id",
        "status",
        "readiness",
        "risk_level",
        "visibility",
    }
    assert "blocked_reason" in dataclasses.asdict(blocked)
    assert "technical_refs" not in dataclasses.asdict(user)
    assert "metadata" not in dataclasses.asdict(user)
    assert "read_model_id" not in dataclasses.asdict(user)


def test_decisions_positive_and_negative_never_allow_operational_axes():
    valid = _validation()
    allowed = projection_contract.decide_runtime_execution_preparation_projection(valid)
    assert allowed.decision == projection_contract.RuntimeExecutionPreparationProjectionDecision.ALLOW_READ_ONLY_PROJECTION
    assert allowed.allowed is True
    assert allowed.read_only_projection_allowed is True
    _assert_decision_never_operational(allowed)

    unsafe_user_model = _projection()
    master, _, audit, summary, status_only, blocked = _views(unsafe_user_model)
    unsafe_user = dataclasses.replace(
        projection_contract.build_runtime_execution_preparation_user_panel_projection(unsafe_user_model),
        safe_summary="raw_prompt",
    )
    negative_cases = [
        (
            _validation(_projection(source_ref=_source_ref(projection_id=""))),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_SOURCE_REFS,
        ),
        (
            projection_contract.validate_runtime_execution_preparation_projection(_projection()),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_READ_MODEL_FILTER,
        ),
        (
            _validation(_projection(metadata=_metadata(api_key="x"))),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_METADATA_SANITIZATION,
        ),
        (
            _validation(
                policy=dataclasses.replace(
                    projection_contract.build_runtime_execution_preparation_projection_policy(),
                    stores_enabled=True,
                )
            ),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_POLICY_DEFAULT_DENY,
        ),
        (
            _validation(unsafe_user_model, views=(master, unsafe_user, audit, summary, status_only, blocked)),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_VISIBILITY_FILTERING,
        ),
        (
            _validation(_projection(projection_readiness="ready_for_runtime")),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.INVALID,
        ),
    ]
    allowed_negative = {
        projection_contract.RuntimeExecutionPreparationProjectionDecision.BLOCK_PROJECTION,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_SOURCE_REFS,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_READ_MODEL_FILTER,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_METADATA_SANITIZATION,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_POLICY_DEFAULT_DENY,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_VISIBILITY_FILTERING,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.INVALID,
    }
    for validation, expected_decision in negative_cases:
        decision = projection_contract.decide_runtime_execution_preparation_projection(validation)
        assert decision.decision == expected_decision
        assert decision.decision in allowed_negative
        assert decision.allowed is False
        _assert_decision_never_operational(decision)


def test_to_dict_snapshots_json_safe_and_deterministic():
    source = _source_ref()
    projection = _projection(source_ref=source)
    master, user, audit, summary, status_only, blocked = _views(projection)
    validation = _validation(projection, views=(master, user, audit, summary, status_only, blocked))
    decision = projection_contract.decide_runtime_execution_preparation_projection(validation)
    snapshot = projection_contract.build_runtime_execution_preparation_projection_snapshot(
        projection=projection,
        master_panel_projection=master,
        user_panel_projection=user,
        internal_audit_projection=audit,
        summary_projection=summary,
        status_only_projection=status_only,
        blocked_projection=blocked,
        validation=validation,
        decision=decision,
        source_refs=source,
    )
    contract_snapshot = projection_contract.build_runtime_execution_preparation_projection_contract_snapshot(
        projection=projection,
        master_panel_projection=master,
        user_panel_projection=user,
        internal_audit_projection=audit,
        summary_projection=summary,
        status_only_projection=status_only,
        blocked_projection=blocked,
        validation=validation,
        decision=decision,
        source_refs=source,
    )
    first = projection_contract.runtime_execution_preparation_projection_to_dict(contract_snapshot)
    second = projection_contract.runtime_execution_preparation_projection_to_dict(contract_snapshot)
    assert first == second
    json.dumps(projection_contract.runtime_execution_preparation_projection_to_dict(snapshot), sort_keys=True)
    json.dumps(first, sort_keys=True)
    for field in [
        "contract_status",
        "policy",
        "allowed_statuses",
        "forbidden_statuses",
        "allowed_readiness",
        "forbidden_readiness",
        "projection_kinds",
        "blocked_capabilities",
        "forbidden_metadata_keys",
        "projection",
        "master_panel_projection",
        "user_panel_projection",
        "internal_audit_projection",
        "summary_projection",
        "status_only_projection",
        "blocked_projection",
        "validation",
        "decision",
        "source_refs",
        "parent_read_model_contract_ref",
        "parent_package_contract_ref",
        "parent_preparation_contract_ref",
    ]:
        assert field in first


def test_no_side_effects_or_dangerous_imports():
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
    before = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    projection = _projection()
    master, user, audit, summary, status_only, blocked = _views(projection)
    validation = _validation(projection, views=(master, user, audit, summary, status_only, blocked))
    decision = projection_contract.decide_runtime_execution_preparation_projection(validation)
    projection_contract.runtime_execution_preparation_projection_to_dict(
        projection_contract.build_runtime_execution_preparation_projection_contract_snapshot(
            projection=projection,
            master_panel_projection=master,
            user_panel_projection=user,
            internal_audit_projection=audit,
            summary_projection=summary,
            status_only_projection=status_only,
            blocked_projection=blocked,
            validation=validation,
            decision=decision,
            source_refs=_source_ref(),
        )
    )
    after = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert before == after


def test_obliteratus_excluded_from_projection_roles():
    assert projection_contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    assert "obliteratus_integration" in projection_contract.BLOCKED_CAPABILITIES
    for statement in projection_contract.OBLITERATUS_EXCLUSION_STATEMENTS:
        assert "OBLITERATUS" in statement
    snapshot = projection_contract.runtime_execution_preparation_projection_to_dict(
        projection_contract.build_runtime_execution_preparation_projection_contract_snapshot()
    )
    dumped = json.dumps(snapshot, sort_keys=True)
    assert "OBLITERATUS" not in dumped
    assert "obliteratus_integration" in dumped


def test_contract_document_exists_and_contains_required_markers():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_READY",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_runtime_execution_preparation_projection_contract_e2e",
        "PROMPT 4.7.1 - Checkpoint E2E Runtime Execution Preparation Projection Contract",
        "Master Panel / User Panel Boundary",
        "UI No Es Capa De Seguridad",
    ]:
        assert phrase in text


def test_previous_contracts_and_boundaries_remain_blocked():
    for module_name in [
        "core.runtime_execution_preparation_projection",
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


def test_no_forbidden_operational_modules_created():
    allowed_preexisting = {"core/runtime_executor.py": "prepare-only"}
    for relative in [
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
