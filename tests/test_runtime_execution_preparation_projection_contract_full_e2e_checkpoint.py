import dataclasses
import importlib
import json
from pathlib import Path

import core.runtime_execution_preparation_contract as parent_contract
import core.runtime_execution_preparation_package as package_contract
import core.runtime_execution_preparation_projection as projection_contract
import core.runtime_execution_preparation_read_model as read_model_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_FULL_E2E_CHECKPOINT.md"
MODULE = ROOT / "core" / "runtime_execution_preparation_projection.py"


FORBIDDEN_SECRET_VALUES = ("SECRET_VALUE", "TOKEN_VALUE", "RAW_PAYLOAD_VALUE", "RAW_OUTPUT_VALUE")
FORBIDDEN_VIEW_FRAGMENTS = (
    "secret",
    "raw_payload",
    "raw_prompt",
    "raw_output",
    "model_response",
    "tool_response",
    "api_key",
    "authorization",
    "bearer",
    "token",
    "cookie",
    "env",
    "raw_package_contract",
    "raw_read_model_contract",
)
PREVIOUS_CONTRACTS_AND_BOUNDARIES = (
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
)


def _metadata(**overrides):
    data = {
        "projection_reason": "full e2e checkpoint",
        "projection_scope": "projection contract",
        "projection_kind": "summary_projection",
        "created_by": "pytest",
        "source": "runtime_execution_preparation_projection_contract_full_e2e",
        "tags": ("projection", "safe", "e2e"),
        "notes": ("read only", "no runtime"),
        "read_model_ref": "read_model_1",
        "package_ref": "package_1",
        "contract_ref": "projection_contract",
        "visibility": "internal_only",
    }
    data.update(overrides)
    return projection_contract.sanitize_runtime_execution_preparation_projection_metadata(data)


def _source_ref(**overrides):
    data = {
        "projection_id": "projection_1",
        "read_model_id": "read_model_1",
        "package_id": "package_1",
        "preparation_id": "preparation_1",
        "intent_ref": "intent_1",
        "attempt_ref": "attempt_1",
        "source_read_model_ref": "core.runtime_execution_preparation_read_model",
        "source_package_ref": "core.runtime_execution_preparation_package",
        "source_contract_refs": (
            "core.runtime_execution_preparation_projection",
            "core.runtime_execution_preparation_read_model",
            "core.runtime_execution_preparation_package",
            "core.runtime_execution_preparation_contract",
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


def _views(active=None):
    projection = active or _projection()
    master = projection_contract.build_runtime_execution_preparation_master_panel_projection(
        projection,
        technical_refs=("source_read_model_ref", "source_package_ref", "parent_preparation_contract_ref"),
    )
    user = projection_contract.build_runtime_execution_preparation_user_panel_projection(projection)
    audit = projection_contract.build_runtime_execution_preparation_internal_audit_projection(
        projection,
        sanitized_refs=("source_read_model_ref", "source_package_ref", "parent_preparation_contract_ref"),
    )
    summary = projection_contract.build_runtime_execution_preparation_summary_projection(projection)
    status_only = projection_contract.build_runtime_execution_preparation_status_only_projection(projection)
    blocked = projection_contract.build_runtime_execution_preparation_blocked_projection(projection, "contract_only")
    return master, user, audit, summary, status_only, blocked


def _validation(active=None, policy=None, views=None):
    projection = active or _projection()
    master, user, audit, summary, status_only, blocked = views or _views(projection)
    return projection_contract.validate_runtime_execution_preparation_projection(
        projection,
        policy=policy,
        master_projection=master,
        user_projection=user,
        internal_audit_projection=audit,
        summary_projection=summary,
        status_only_projection=status_only,
        blocked_projection=blocked,
    )


def _decision(active=None, policy=None, views=None):
    return projection_contract.decide_runtime_execution_preparation_projection(
        _validation(active=active, policy=policy, views=views),
        policy=policy,
    )


def _snapshot_bundle():
    source = _source_ref()
    active = _projection(source_ref=source)
    master, user, audit, summary, status_only, blocked = _views(active)
    validation = _validation(active, views=(master, user, audit, summary, status_only, blocked))
    decision = projection_contract.decide_runtime_execution_preparation_projection(validation)
    snapshot = projection_contract.build_runtime_execution_preparation_projection_snapshot(
        projection=active,
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
        projection=active,
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
    return source, active, (master, user, audit, summary, status_only, blocked), validation, decision, snapshot, contract_snapshot


def _to_dict(value):
    return projection_contract.runtime_execution_preparation_projection_to_dict(value)


def _dump(value):
    return json.dumps(_to_dict(value), sort_keys=True)


def _assert_no_operational_decision_fields(decision):
    for field in (
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
    ):
        assert getattr(decision, field) is False


def _assert_module_boolean_blocks(module_name):
    module = importlib.import_module(module_name)
    booleans = {
        name: getattr(module, name)
        for name in dir(module)
        if name.isupper()
        and isinstance(getattr(module, name), bool)
        and (
            name.endswith("_OPERATIONAL")
            or name.endswith("_ACTIVE")
            or name.endswith("_ENABLED")
            or name.endswith("_ALLOWED")
        )
    }
    assert booleans, module_name
    assert all(value is False for value in booleans.values()), booleans


def test_e2e_imports_projection_and_parent_contracts_safely():
    module = importlib.import_module("core.runtime_execution_preparation_projection")
    assert module is projection_contract
    assert projection_contract.read_model_contract is read_model_contract
    assert projection_contract.package_contract is package_contract
    assert projection_contract.parent_contract is parent_contract
    assert projection_contract.PARENT_READ_MODEL_CONTRACT_REF == "core.runtime_execution_preparation_read_model"
    assert projection_contract.PARENT_PACKAGE_CONTRACT_REF == "core.runtime_execution_preparation_package"
    assert projection_contract.PARENT_PREPARATION_CONTRACT_REF == "core.runtime_execution_preparation_contract"


def test_e2e_projection_flags_and_policy_are_default_deny():
    assert projection_contract.RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_READY is True
    for name in (
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
    ):
        assert getattr(projection_contract, name) is False
    policy = projection_contract.build_runtime_execution_preparation_projection_policy()
    assert policy.read_only_enabled is True
    assert policy.contract_ready is True
    for field, value in dataclasses.asdict(policy).items():
        if field not in {"contract_ready", "read_only_enabled"}:
            assert value is False, field


def test_e2e_parent_contracts_remain_default_deny():
    for module_name in (
        "core.runtime_execution_preparation_read_model",
        "core.runtime_execution_preparation_package",
        "core.runtime_execution_preparation_contract",
    ):
        _assert_module_boolean_blocks(module_name)


def test_e2e_metadata_safe_values_survive_and_dangerous_values_are_blocked_without_values():
    metadata = _metadata(projection_reason="safe reason", tags=("alpha", "beta"))
    assert metadata.projection_reason == "safe reason"
    assert metadata.tags == ("alpha", "beta")
    dangerous = projection_contract.sanitize_runtime_execution_preparation_projection_metadata(
        {
            "secret": "SECRET_VALUE",
            "api_key": "TOKEN_VALUE",
            "raw_payload": "RAW_PAYLOAD_VALUE",
            "raw_output": "RAW_OUTPUT_VALUE",
            "projection_reason": "still safe",
        }
    )
    assert set(dangerous.blocked_keys) >= {"secret", "api_key", "raw_payload", "raw_output"}
    dumped = _dump(dangerous)
    for value in FORBIDDEN_SECRET_VALUES:
        assert value not in dumped
    for key in (
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
    ):
        assert key in projection_contract.FORBIDDEN_METADATA_KEYS


def test_e2e_source_refs_complete_and_all_required_missing_refs_fail():
    complete = _source_ref()
    assert complete.missing_critical_source_refs() == ()
    for field in projection_contract.REQUIRED_SOURCE_REF_FIELDS:
        incomplete = _source_ref(**{field: ""})
        assert field in incomplete.missing_critical_source_refs()
        result = _validation(_projection(source_ref=incomplete))
        assert result.is_valid is False
        assert f"missing_source_ref:{field}" in result.errors


def test_e2e_projection_core_views_and_validation_are_safe():
    source, active, views, validation, decision, snapshot, contract_snapshot = _snapshot_bundle()
    master, user, audit, summary, status_only, blocked = views
    assert active.projection_id == source.projection_id
    assert active.projection_readiness == "ready_for_runtime_execution_preparation_projection_contract_e2e"
    assert validation.is_valid is True
    assert validation.errors == ()
    assert decision.decision == projection_contract.RuntimeExecutionPreparationProjectionDecision.ALLOW_READ_ONLY_PROJECTION
    assert decision.read_only_projection_allowed is True
    _assert_no_operational_decision_fields(decision)
    assert master.technical_refs
    assert user.safe_summary == active.safe_summary
    assert audit.sanitized_refs
    assert set(_to_dict(summary)) == {"projection_id", "package_id", "status", "readiness", "risk_level", "safe_summary", "visibility"}
    assert set(_to_dict(status_only)) == {"projection_id", "package_id", "status", "readiness", "risk_level", "visibility"}
    assert not any(key.startswith("allowed") for key in _to_dict(blocked))
    json.dumps(_to_dict(snapshot), sort_keys=True)
    json.dumps(_to_dict(contract_snapshot), sort_keys=True)


def test_e2e_forbidden_readiness_status_metadata_and_policy_fail():
    readiness = _validation(_projection(projection_readiness="ready_for_runtime"))
    assert readiness.is_valid is False
    assert "ready_for_runtime" in readiness.forbidden_readiness_detected
    status = _validation(dataclasses.replace(_projection(), projection_status="projection_active"))
    assert status.is_valid is False
    assert "projection_active" in status.forbidden_status_detected
    metadata = _validation(_projection(metadata=_metadata(api_key="SECRET_VALUE")))
    assert metadata.is_valid is False
    assert "api_key" in metadata.metadata_blocked_keys
    for field in ("writes_enabled", "permission_bypass_enabled", "raw_package_to_user_projection_enabled"):
        unsafe_policy = dataclasses.replace(
            projection_contract.build_runtime_execution_preparation_projection_policy(),
            **{field: True},
        )
        result = _validation(policy=unsafe_policy)
        assert result.is_valid is False
        assert f"operational_policy_flag_enabled:{field}" in result.policy_violations
        assert _decision(policy=unsafe_policy).decision == (
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_POLICY_DEFAULT_DENY
        )


def test_e2e_user_projection_never_exposes_master_internals_or_raw_parent_contracts():
    active = _projection()
    _, user, _, _, _, _ = _views(active)
    user_dict = _to_dict(user)
    forbidden_user_keys = {
        "metadata",
        "technical_refs",
        "master_panel",
        "security_internal",
        "raw_package_contract",
        "raw_read_model_contract",
    }
    assert forbidden_user_keys.isdisjoint(user_dict)
    user_dump = json.dumps(user_dict, sort_keys=True).lower()
    for fragment in FORBIDDEN_VIEW_FRAGMENTS:
        assert fragment not in user_dump


def test_e2e_all_projection_views_block_raw_sensitive_fragments():
    active = _projection(metadata=_metadata(notes=("safe note",)))
    for view in _views(active):
        dumped = json.dumps(_to_dict(view), sort_keys=True).lower()
        for fragment in FORBIDDEN_VIEW_FRAGMENTS:
            assert fragment not in dumped


def test_e2e_decision_negative_paths_are_closed_and_non_operational():
    unsafe_user_model = _projection()
    master, _, audit, summary, status_only, blocked = _views(unsafe_user_model)
    unsafe_user = dataclasses.replace(
        projection_contract.build_runtime_execution_preparation_user_panel_projection(unsafe_user_model),
        safe_summary="raw_package_contract",
    )
    cases = (
        (
            _validation(_projection(source_ref=_source_ref(projection_id=""))),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_SOURCE_REFS,
        ),
        (
            projection_contract.validate_runtime_execution_preparation_projection(_projection()),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_READ_MODEL_FILTER,
        ),
        (
            _validation(_projection(metadata=_metadata(api_key="SECRET_VALUE"))),
            projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_METADATA_SANITIZATION,
        ),
        (
            _validation(
                policy=dataclasses.replace(
                    projection_contract.build_runtime_execution_preparation_projection_policy(),
                    writes_enabled=True,
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
    )
    allowed_negative = {
        projection_contract.RuntimeExecutionPreparationProjectionDecision.BLOCK_PROJECTION,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_SOURCE_REFS,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_READ_MODEL_FILTER,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_METADATA_SANITIZATION,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_POLICY_DEFAULT_DENY,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.REQUIRE_VISIBILITY_FILTERING,
        projection_contract.RuntimeExecutionPreparationProjectionDecision.INVALID,
    }
    for validation, expected in cases:
        decision = projection_contract.decide_runtime_execution_preparation_projection(validation)
        assert decision.decision == expected
        assert decision.decision in allowed_negative
        assert decision.allowed is False
        _assert_no_operational_decision_fields(decision)


def test_e2e_serializer_snapshot_contract_snapshot_are_json_safe_and_deterministic():
    _, active, _, _, _, snapshot, contract_snapshot = _snapshot_bundle()
    custom = {
        "enum": projection_contract.RuntimeExecutionPreparationProjectionKind.SUMMARY_PROJECTION,
        "dataclass": active,
        "tuple": ("a", "b"),
        "frozenset": frozenset(("b", "a")),
        "list": [active],
        "dict": {"policy": projection_contract.build_runtime_execution_preparation_projection_policy()},
    }
    custom_dict = _to_dict(custom)
    json.dumps(custom_dict, sort_keys=True)
    snapshot_dict = _to_dict(snapshot)
    contract_dict = _to_dict(contract_snapshot)
    json.dumps(snapshot_dict, sort_keys=True)
    json.dumps(contract_dict, sort_keys=True)
    assert snapshot_dict == _to_dict(snapshot)
    assert contract_dict == _to_dict(contract_snapshot)
    for field in (
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
    ):
        assert field in contract_dict


def test_e2e_pure_calls_do_not_create_files_or_use_dangerous_runtime_modules():
    before = {path.relative_to(ROOT).as_posix() for path in (ROOT / "core").iterdir()}
    for _ in range(2):
        _snapshot_bundle()
    after = {path.relative_to(ROOT).as_posix() for path in (ROOT / "core").iterdir()}
    assert after == before
    source = MODULE.read_text(encoding="utf-8").lower()
    for forbidden in ("subprocess", "socket", "requests", "httpx", "os.environ", "getenv", "open(", "write_text"):
        assert forbidden not in source


def test_e2e_previous_contracts_and_boundaries_remain_blocked():
    for module_name in PREVIOUS_CONTRACTS_AND_BOUNDARIES:
        module = importlib.import_module(module_name)
        ready_flags = [getattr(module, name) for name in dir(module) if name.isupper() and name.endswith("_READY")]
        assert ready_flags or module_name in {"core.runtime_execution_preparation_contract"}
        _assert_module_boolean_blocks(module_name)


def test_e2e_operational_modules_are_not_created_and_runtime_executor_is_prepare_only():
    forbidden_modules = (
        "core/runtime_execution_preparation_store.py",
        "core/runtime_execution_preparation_writer.py",
        "core/runtime_execution_preparation_reader.py",
        "core/runtime_execution_preparation_api.py",
        "core/runtime_execution_preparation_ui.py",
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
    )
    for relative in forbidden_modules:
        assert not (ROOT / relative).exists(), relative
    runtime_executor = ROOT / "core" / "runtime_executor.py"
    if runtime_executor.exists():
        assert "prepare-only" in runtime_executor.read_text(encoding="utf-8").lower()


def test_e2e_market_business_runtime_and_obliteratus_are_excluded():
    contract_dict = _to_dict(projection_contract.build_runtime_execution_preparation_projection_contract_snapshot())
    assert "market_catalog_runtime" in contract_dict["blocked_capabilities"]
    assert "business_composition_runtime" in contract_dict["blocked_capabilities"]
    assert "obliteratus_integration" in contract_dict["blocked_capabilities"]
    assert projection_contract.EXCLUDED_EXTERNAL_CONCEPTS == frozenset({"OBLITERATUS"})
    joined = "\n".join(projection_contract.OBLITERATUS_EXCLUSION_STATEMENTS).lower()
    for role in (
        "integration",
        "dependency",
        "adapter",
        "provider",
        "capability",
        "runtime",
        "execution source",
        "package source",
        "read model source",
        "projection source",
        "projection view source",
        "audit source",
    ):
        assert f"not an {role}" in joined or f"not a {role}" in joined


def test_e2e_checkpoint_document_exists_and_contains_required_tokens():
    text = DOC.read_text(encoding="utf-8")
    for token in (
        "Runtime Execution Preparation Projection Contract Full E2E Checkpoint",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_FULL_E2E_PASSED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_CHAIN_READY",
        "ready_for_runtime_execution_preparation_block_integral_checkpoint",
        "PROMPT 4.8 — Checkpoint integral Runtime Execution Preparation Block",
        "E2E valida que Runtime Execution Preparation Projection Contract opera como contrato puro/read-only/no-operativo",
        "raw Package direct to User Panel remain blocked",
    ):
        assert token in text
