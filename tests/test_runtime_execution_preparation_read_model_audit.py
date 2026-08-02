from pathlib import Path
import importlib

import core.runtime_execution_preparation_package as package_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_AUDIT.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


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


def test_read_model_audit_document_exists_and_declares_status():
    text = _text()
    for phrase in [
        "Runtime Execution Preparation Read Model Audit",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_AUDIT_COMPLETED",
        "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_BASELINE_VERIFIED",
        "ready_for_runtime_execution_preparation_read_model_contract",
        "PROMPT 4.5 - Contrato de Runtime Execution Preparation Read Model no-operativo",
    ]:
        assert phrase in text


def test_document_contains_definition_and_package_contract_relationship():
    text = _text()
    for phrase in [
        "Runtime Execution Preparation Read Model es la futura estructura read-only/no-operativa",
        "Read Model no es Store",
        "Read Model no es Writer",
        "Read Model no es Runtime",
        "Read Model no es API",
        "Read Model no reemplaza Security Layer",
        "RuntimeExecutionPreparationPackageCore",
        "RuntimeExecutionPreparationPackageValidationResult",
        "RuntimeExecutionPreparationPackageDecisionRecord",
        "RuntimeExecutionPreparationPackageSafeView",
        "RuntimeExecutionPreparationPackageSnapshot",
        "RuntimeExecutionPreparationPackageContractSnapshot",
        "runtime_execution_preparation_package_to_dict()",
        "build_runtime_execution_preparation_package_safe_view()",
        "build_runtime_execution_preparation_package_contract_snapshot()",
        "estado actual",
        "Que puede exponerse",
        "Que no debe exponerse",
        "Solo Master Panel",
        "User Panel",
        "Backend filtering",
        "Riesgos",
        "Gaps",
        "Recomendacion",
    ]:
        assert phrase in text


def test_document_contains_purpose_and_expected_recommendation():
    text = _text()
    for phrase in [
        "lectura segura",
        "serializacion estable",
        "consumo por auditoria",
        "consumo por panel maestro",
        "consumo por panel usuario",
        "separacion de visibilidad",
        "compatibilidad con SafeView",
        "compatibilidad con Execution Intent",
        "compatibilidad con Attempt",
        "compatibilidad con Result/Projection/History",
        "compatibilidad futura con Human Approval",
        "compatibilidad futura con Observability/Audit Trail",
        "compatibilidad futura con UI/UX",
        "compatibilidad futura con Master Panel / User Panel",
        "trazabilidad sin exposicion sensible",
        "no side effects",
        "no writes",
        "Si conviene formalizar Runtime Execution Preparation Read Model como contrato no-operativo separado",
    ]:
        assert phrase in text


def test_document_contains_minimum_fields_and_view_rules():
    text = _text()
    for field in [
        "read_model_id",
        "package_id",
        "preparation_id",
        "intent_ref",
        "attempt_ref",
        "status",
        "readiness",
        "risk_level",
        "execution_scope",
        "execution_mode",
        "decision",
        "validation_status",
        "missing_required_dependencies",
        "missing_optional_dependencies",
        "blocked_capabilities",
        "warnings",
        "errors",
        "safe_summary",
        "master_panel_view",
        "user_panel_view",
        "visibility",
        "source_package_ref",
        "source_contract_ref",
        "serialization_version",
    ]:
        assert field in text
    for phrase in [
        "MASTER_PANEL_VIEW",
        "USER_PANEL_VIEW",
        "INTERNAL_AUDIT_VIEW",
        "La UI no es capa de seguridad",
        "El backend debe filtrar datos antes de construir cualquier view",
        "Ocultar botones no alcanza",
        "Un usuario comun nunca debe cargar, recibir ni consultar capacidades de panel maestro",
    ]:
        assert phrase in text


def test_document_contains_states_readiness_matrix_metadata_gaps_risks_and_obliteratus():
    text = _text()
    for state in [
        "read_model_uninitialized",
        "read_model_draft",
        "read_model_source_required",
        "read_model_projection_required",
        "read_model_visibility_required",
        "read_model_safe_view_required",
        "read_model_ready_simulated",
        "read_model_blocked",
        "read_model_invalid",
        "read_model_archived_simulated",
        "read_model_active",
        "read_model_running",
        "read_model_executing",
        "read_model_live",
        "read_model_enabled",
        "read_model_operational",
        "read_model_runtime_started",
        "read_model_execution_started",
        "read_model_dry_run_started",
        "read_model_tool_executing",
        "read_model_model_invoking",
        "read_model_context_injecting",
        "read_model_output_delivering",
        "read_model_writing",
        "read_model_store_mutating",
        "read_model_network_active",
        "read_model_browser_active",
        "read_model_filesystem_active",
        "read_model_env_active",
        "read_model_secret_active",
        "read_model_integration_active",
        "read_model_api_active",
        "read_model_ui_control_active",
        "ready_for_runtime_execution_preparation_read_model_contract",
        "ready_for_runtime_execution_preparation_read_model_contract_e2e",
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
        "ready_for_api",
        "ready_for_ui",
        "read_model_store_enabled",
        "read_model_writer_enabled",
        "read_model_api_enabled",
        "read_model_ui_enabled",
    ]:
        assert state in text
    for dimension in [
        "1. Read model identity",
        "2. Package reference",
        "3. Preparation reference",
        "4. Intent reference",
        "5. Attempt reference",
        "6. Status",
        "7. Readiness",
        "8. Risk level",
        "9. Execution scope",
        "10. Execution mode",
        "11. Decision",
        "12. Validation status",
        "13. Missing required dependencies",
        "14. Missing optional dependencies",
        "15. Blocked capabilities",
        "16. Warnings",
        "17. Errors",
        "18. Safe summary",
        "19. Master Panel View",
        "20. User Panel View",
        "21. Internal Audit View",
        "22. Visibility level",
        "23. Source package ref",
        "24. Source contract ref",
        "25. Serialization version",
        "26. SafeView dependency",
        "27. Metadata sanitization",
        "28. Raw payload exclusion",
        "29. Raw prompt exclusion",
        "30. Raw output exclusion",
        "31. Model/tool response exclusion",
        "32. Secrets/env/auth exclusion",
        "33. Personal data sanitization",
        "34. JSON-safe serialization",
        "35. Determinism",
        "36. No side effects",
        "37. No writes",
        "38. No stores",
        "39. No runtime activation",
        "40. No execution activation",
        "41. No dry-run activation",
        "42. No tool/model/context/output",
        "43. No network/browser/filesystem/env/secrets",
        "44. No UI/device control",
        "45. No integrations",
        "46. Backend filtering",
        "47. Master/User Panel separation",
        "48. Permission dependency",
        "49. Market Catalog boundary",
        "50. Business Composition Layer boundary",
        "51. OBLITERATUS exclusion",
    ]:
        assert dimension in text
    for phrase in [
        "read_model_reason",
        "read_model_scope",
        "created_by",
        "source",
        "tags",
        "notes",
        "package_ref",
        "contract_ref",
        "visibility",
        "master_panel_internal_capability",
        "admin_secret",
        "permission_bypass",
        "El Read Model nunca debe guardar valores de claves peligrosas",
        "Puede registrar nombres de claves bloqueadas, pero jamas sus valores",
        "No existe contrato Read Model separado",
        "No existe modulo core/runtime_execution_preparation_read_model.py",
        "No existe test Read Model independiente",
        "No existe Read Model E2E independiente",
        "No existe projection especifica del Package hacia Read Model",
        "No existe Master Panel view contract",
        "No existe User Panel view contract",
        "No existe Internal Audit view contract",
        "No existe permission-aware read filter",
        "No existe API-safe read model",
        "No existe UI-safe read model",
        "No existe read model versioning contract",
        "No existe archival/snapshot read model contract",
        "No existe read model relation with approval UI",
        "No existe read model relation with observability/audit trail events",
        "Estos gaps son esperados",
        "No deben resolverse en este prompt",
        "Confundir Read Model con Store",
        "Confundir Read Model con UI",
        "Confundir Read Model con API",
        "Usar Read Model para bypass de permisos",
        "Exponer internals del Master Panel al User Panel",
        "Exponer metadata cruda",
        "Exponer raw payloads",
        "Exponer raw prompts",
        "Exponer raw outputs",
        "Exponer model/tool responses",
        "Exponer secrets/env/auth",
        "Crear writer/store antes de contrato",
        "Crear endpoint/API antes de seguridad de lectura",
        "Crear UI antes de backend filtering",
        "Usar Read Model como disparador de runtime",
        "Incorporar OBLITERATUS como source/capability/integration",
        "OBLITERATUS no forma parte de Runtime Execution Preparation Read Model",
        "No es read model source",
        "No es read model metadata source",
        "No es read model view source",
        "No es audit source",
    ]:
        assert phrase in text


def test_no_read_model_module_or_forbidden_operational_modules_created():
    allowed_preexisting = {"core/runtime_executor.py": "prepare-only"}
    for relative in [
        "core/runtime_execution_preparation_read_model.py",
        "core/runtime_execution_preparation_projection.py",
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
    ]:
        candidate = ROOT / relative
        if relative in allowed_preexisting and candidate.exists():
            assert allowed_preexisting[relative] in candidate.read_text(encoding="utf-8").lower()
            continue
        assert not candidate.exists(), relative


def test_package_flags_remain_closed():
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY is True
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_OPERATIONAL is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_RUNTIME_ACTIVE is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_EXECUTION_ACTIVE is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_DRY_RUN_ACTIVE is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_TOOLS_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_MODELS_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTEXT_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_OUTPUT_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_WRITES_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_STORES_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_MEMORY_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_NETWORK_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_BROWSER_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_FILESYSTEM_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_ENV_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_SECRETS_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_UI_DEVICE_ENABLED is False
    assert package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_INTEGRATIONS_ENABLED is False


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
