import importlib
from pathlib import Path

import core.runtime_execution_preparation_read_model as read_model_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_PROJECTION_AUDIT.md"


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


def test_projection_audit_document_exists_and_has_required_markers():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "Runtime Execution Preparation Projection Audit",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_AUDIT_COMPLETED",
        "RUNTIME_EXECUTION_PREPARATION_PROJECTION_BASELINE_VERIFIED",
        "ready_for_runtime_execution_preparation_projection_contract",
        "PROMPT 4.7 - Contrato de Runtime Execution Preparation Projection no-operativo",
    ]:
        assert token in text


def test_projection_audit_document_covers_required_sections():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "## Definition",
        "## Read Model Relationship",
        "## Package Relationship",
        "## Purpose Of The Future Projection Contract",
        "## Minimum Future Projection Fields",
        "## Future Projection Kinds",
        "## Future Projection States",
        "## Future Projection Readiness",
        "## Projection Audit Matrix",
        "## Allowed Projection Metadata",
        "## Forbidden Projection Data",
        "## Mandatory Gaps",
        "## Mandatory Risks",
        "## OBLITERATUS",
    ]:
        assert token in text


def test_projection_audit_document_covers_read_model_and_package_inputs():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "RuntimeExecutionPreparationReadModelCore",
        "RuntimeExecutionPreparationMasterPanelView",
        "RuntimeExecutionPreparationUserPanelView",
        "RuntimeExecutionPreparationInternalAuditView",
        "RuntimeExecutionPreparationReadModelValidationResult",
        "RuntimeExecutionPreparationReadModelDecisionRecord",
        "RuntimeExecutionPreparationReadModelSnapshot",
        "RuntimeExecutionPreparationReadModelContractSnapshot",
        "runtime_execution_preparation_read_model_to_dict()",
        "build_runtime_execution_preparation_read_model_snapshot()",
        "build_runtime_execution_preparation_read_model_contract_snapshot()",
        "RuntimeExecutionPreparationPackageCore",
        "RuntimeExecutionPreparationPackageValidationResult",
        "RuntimeExecutionPreparationPackageDecisionRecord",
        "RuntimeExecutionPreparationPackageSafeView",
        "RuntimeExecutionPreparationPackageSnapshot",
        "RuntimeExecutionPreparationPackageContractSnapshot",
        "runtime_execution_preparation_package_to_dict()",
        "build_runtime_execution_preparation_package_safe_view()",
        "build_runtime_execution_preparation_package_contract_snapshot()",
    ]:
        assert token in text


def test_projection_audit_document_covers_projection_fields_kinds_states_readiness_and_lists():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "projection_id",
        "read_model_id",
        "package_id",
        "preparation_id",
        "intent_ref",
        "attempt_ref",
        "projection_kind",
        "projection_status",
        "projection_readiness",
        "visibility",
        "risk_level",
        "execution_scope",
        "execution_mode",
        "decision",
        "validation_status",
        "dependency_summary",
        "boundary_summary",
        "blocked_capabilities_summary",
        "warning_summary",
        "error_summary",
        "safe_summary",
        "master_projection",
        "user_projection",
        "internal_audit_projection",
        "source_read_model_ref",
        "source_package_ref",
        "source_contract_refs",
        "serialization_version",
        "MASTER_PANEL_PROJECTION",
        "USER_PANEL_PROJECTION",
        "INTERNAL_AUDIT_PROJECTION",
        "SUMMARY_PROJECTION",
        "STATUS_ONLY_PROJECTION",
        "BLOCKED_PROJECTION",
        "projection_uninitialized",
        "projection_ready_simulated",
        "projection_invalid",
        "projection_active",
        "projection_operational",
        "ready_for_runtime_execution_preparation_projection_contract",
        "ready_for_runtime_execution_preparation_projection_contract_e2e",
        "projection_api_enabled",
        "projection_ui_enabled",
        "projection_reason",
        "projection_scope",
        "projection_kind",
        "read_model_ref",
        "package_ref",
        "contract_ref",
        "raw_master_panel_view",
        "raw_user_panel_view",
        "raw_internal_audit_view",
    ]:
        assert token in text


def test_projection_audit_document_contains_all_matrix_dimensions():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "1. Projection identity",
        "2. Read Model reference",
        "3. Package reference",
        "4. Preparation reference",
        "5. Intent reference",
        "6. Attempt reference",
        "7. Projection kind",
        "8. Projection status",
        "9. Projection readiness",
        "10. Visibility",
        "11. Risk level",
        "12. Execution scope",
        "13. Execution mode",
        "14. Decision",
        "15. Validation status",
        "16. Dependency summary",
        "17. Boundary summary",
        "18. Blocked capabilities summary",
        "19. Warning summary",
        "20. Error summary",
        "21. Safe summary",
        "22. Master projection",
        "23. User projection",
        "24. Internal audit projection",
        "25. Summary projection",
        "26. Status-only projection",
        "27. Blocked projection",
        "28. Source read model ref",
        "29. Source package ref",
        "30. Source contract refs",
        "31. Serialization version",
        "32. Metadata sanitization",
        "33. Raw payload exclusion",
        "34. Raw prompt exclusion",
        "35. Raw output exclusion",
        "36. Model/tool response exclusion",
        "37. Secrets/env/auth exclusion",
        "38. Personal data sanitization",
        "39. JSON-safe serialization",
        "40. Determinism",
        "41. No side effects",
        "42. No writes",
        "43. No stores",
        "44. No runtime activation",
        "45. No execution activation",
        "46. No dry-run activation",
        "47. No tool/model/context/output",
        "48. No network/browser/filesystem/env/secrets",
        "49. No API/UI/UI-device control",
        "50. No integrations",
        "51. Backend filtering",
        "52. Master/User Panel separation",
        "53. Permission dependency",
        "54. Market Catalog boundary",
        "55. Business Composition Layer boundary",
        "56. OBLITERATUS exclusion",
    ]:
        assert token in text


def test_projection_audit_document_contains_gaps_risks_and_obliteratus_exclusion():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "No separate Projection contract exists.",
        "No `core/runtime_execution_preparation_projection.py` module exists.",
        "No permission-aware projection filter exists.",
        "No API-safe projection exists.",
        "No UI-safe projection exists.",
        "Confusing Projection with Store.",
        "Confusing Projection with Writer.",
        "Confusing Projection with API.",
        "Confusing Projection with UI.",
        "Using Projection for permission bypass.",
        "Exposing Master Panel internals to User Panel.",
        "Projecting from Package to User Panel without Read Model filtering.",
        "OBLITERATUS does not form part of Runtime Execution Preparation Projection.",
        "It is not a projection source.",
        "It is not a projection metadata source.",
        "It is not a projection view source.",
    ]:
        assert token in text


def test_projection_and_other_forbidden_operational_modules_are_not_created():
    allowed_preexisting = {"core/runtime_executor.py": "prepare-only"}
    for relative in [
        "core/runtime_execution_preparation_projection.py",
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
        "core/runtime_executor.py",
    ]:
        candidate = ROOT / relative
        if relative in allowed_preexisting and candidate.exists():
            assert allowed_preexisting[relative] in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), relative


def test_read_model_and_package_flags_remain_default_deny():
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
    _assert_false_flags("core.runtime_execution_preparation_package")


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
