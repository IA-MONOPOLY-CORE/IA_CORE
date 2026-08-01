from pathlib import Path
import importlib

import core.runtime_execution_preparation_contract as contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_PACKAGE_AUDIT.md"


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


def test_package_audit_document_exists_and_declares_status():
    text = _text()
    for phrase in [
        "Runtime Execution Preparation Package Audit",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_AUDIT_COMPLETED",
        "RUNTIME_EXECUTION_PREPARATION_PACKAGE_BASELINE_VERIFIED",
        "ready_for_runtime_execution_preparation_package_contract",
        "PROMPT 4.3 — Contrato de Runtime Execution Preparation Package no-operativo",
    ]:
        assert phrase in text


def test_document_contains_definition_and_contract_41_relationship():
    text = _text()
    for phrase in [
        "Runtime Execution Preparation Package es la futura estructura no-operativa",
        "Runtime Execution Preparation Package no es Runtime Execution",
        "RuntimeExecutionPreparationPackage",
        "RuntimeExecutionPreparationDependency",
        "RuntimeExecutionPreparationBoundarySnapshot",
        "RuntimeExecutionPreparationMetadata",
        "RuntimeExecutionPreparationValidationResult",
        "RuntimeExecutionPreparationDecisionRecord",
        "RuntimeExecutionPreparationContractSnapshot",
        "build_runtime_execution_preparation_package()",
        "validate_runtime_execution_preparation_package()",
        "decide_runtime_execution_preparation()",
        "runtime_execution_preparation_to_dict()",
        "build_runtime_execution_preparation_contract_snapshot()",
        "estado actual",
        "que cubre",
        "Que no cubre",
        "Alcanza para contrato separado",
        "Riesgos",
        "Gaps",
        "Recomendacion",
    ]:
        assert phrase in text


def test_document_contains_future_contract_purpose_and_expected_recommendation():
    text = _text()
    for phrase in [
        "Si conviene formalizar Runtime Execution Preparation Package como contrato no-operativo separado",
        "claridad arquitectonica",
        "separacion entre contrato general y package",
        "validacion independiente",
        "extension futura",
        "testabilidad",
        "trazabilidad",
        "serializacion",
        "seguridad",
        "compatibilidad con attempts/results/history",
        "compatibilidad futura con human approval",
        "compatibilidad futura con dry-run handoff",
        "compatibilidad futura con runtime activation gate",
        "compatibilidad futura con observability/audit trail",
        "compatibilidad futura con UI/UX y paneles",
    ]:
        assert phrase in text


def test_document_contains_minimum_future_package_fields():
    text = _text()
    for field in [
        "package_id",
        "preparation_id",
        "intent_ref",
        "attempt_ref",
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
        "human_approval_ref",
        "kill_switch_ref",
        "rollback_ref",
        "dry_run_ref",
        "execution_scope",
        "execution_mode",
        "execution_risk_level",
        "required_dependencies",
        "optional_dependencies",
        "missing_required_dependencies",
        "missing_optional_dependencies",
        "blocked_capabilities",
        "forbidden_readiness",
        "metadata_sanitized",
        "package_status",
        "package_readiness",
        "package_validation",
        "package_decision",
        "prepared_snapshot",
        "serialization_version",
    ]:
        assert field in text
    assert "Todos los campos son conceptuales" in text
    assert "Ningun campo debe contener objetos vivos" in text


def test_document_contains_allowed_and_forbidden_states_and_readiness():
    text = _text()
    for state in [
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
        assert state in text
    for state in [
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
        assert state in text
    for readiness in [
        "ready_for_runtime_execution_preparation_package_contract",
        "ready_for_runtime_execution_preparation_package_contract_e2e",
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
        "package_runtime_enabled",
        "package_execution_enabled",
        "package_store_enabled",
    ]:
        assert readiness in text


def test_document_contains_matrix_with_50_dimensions():
    text = _text()
    for dimension in [
        "1. Package identity",
        "2. Preparation identity",
        "3. Intent reference",
        "4. Attempt reference",
        "5. Runtime Governance reference",
        "6. Runtime State reference",
        "7. Observability reference",
        "8. Runtime Activation Gate reference",
        "9. Security baseline reference",
        "10. Agent Permission reference",
        "11. Sandbox Boundary reference",
        "12. Tool Boundary reference",
        "13. Model Boundary reference",
        "14. Context Boundary reference",
        "15. Output Boundary reference",
        "16. Secrets Policy reference",
        "17. Prompt Injection Defense reference",
        "18. Human Approval reference",
        "19. Kill Switch reference",
        "20. Rollback reference",
        "21. Dry-run reference",
        "22. Required dependencies",
        "23. Optional dependencies",
        "24. Missing dependencies",
        "25. Blocked capabilities",
        "26. Forbidden readiness",
        "27. Metadata sanitizer",
        "28. Metadata blocked keys",
        "29. Execution scope",
        "30. Execution mode",
        "31. Risk level",
        "32. Status",
        "33. Readiness",
        "34. Validation",
        "35. Decision",
        "36. Snapshot",
        "37. JSON-safe serialization",
        "38. Determinism",
        "39. Side-effect free behavior",
        "40. No runtime activation",
        "41. No execution activation",
        "42. No dry-run real activation",
        "43. No tools/models/context/output",
        "44. No writes/stores/memory",
        "45. No network/browser/filesystem/env/secrets",
        "46. No UI/device/integrations",
        "47. Market Catalog boundary",
        "48. Business Composition Layer boundary",
        "49. OBLITERATUS exclusion",
        "50. Future UI/UX visibility boundary",
    ]:
        assert dimension in text
    for header in [
        "Cobertura actual",
        "Evidencia actual",
        "Archivo asociado",
        "Gap principal",
        "Riesgo",
        "Requisito minimo futuro",
    ]:
        assert header in text


def test_document_contains_metadata_ui_panel_gaps_risks_and_obliteratus():
    text = _text()
    for phrase in [
        "package_reason",
        "package_scope",
        "package_mode",
        "package_risk_level",
        "business_context_ref optional",
        "domain_ref optional",
        "agent_ref optional",
        "El Package nunca debe guardar valores de claves peligrosas",
        "Puede registrar nombres de claves bloqueadas, pero jamas sus valores",
        "El package puede alimentar paneles futuros solo mediante read models seguros",
        "El package no debe exponer metadata cruda",
        "El package no debe exponer secrets",
        "El package no debe exponer raw payloads",
        "El package no debe exponer prompts crudos",
        "El package no debe exponer tool/model responses",
        "El package no debe exponer internals de panel maestro a usuarios comunes",
        "El package debe respetar separacion futura entre Master Panel y User Panel",
        "La UI no es capa de seguridad; el backend debe filtrar y bloquear",
        "Master Panel puede ver trazabilidad tecnica autorizada",
        "User Panel solo debe ver estado resumido, resultado permitido y acciones autorizadas",
        "Un usuario comun nunca debe cargar, recibir ni consultar capacidades de panel maestro",
        "La separacion debe ser real por permisos, rutas, endpoints y backend filtering",
        "No existe contrato Package separado",
        "No existe modulo core/runtime_execution_preparation_package.py",
        "No existe Package read model",
        "No existe Package UI-safe view",
        "No existe Package handoff hacia human approval",
        "No existe Package handoff hacia dry-run",
        "No existe Package handoff hacia runtime activation gate",
        "No existe Package observability event contract",
        "No existe Package lifecycle contract",
        "No existe Package versioning contract",
        "No existe Package archival contract",
        "Estos gaps son esperados",
        "No deben resolverse en este prompt",
    ]:
        assert phrase in text
    for phrase in FORBIDDEN_DATA:
        assert phrase in text
    for risk in RISKS:
        assert risk in text
    for field in ["Descripcion", "Impacto", "Mitigacion existente", "Mitigacion faltante", "Recomendacion"]:
        assert field in text
    for phrase in [
        "OBLITERATUS no forma parte de Runtime Execution Preparation Package",
        "No es integration",
        "No es dependency",
        "No es adapter",
        "No es provider",
        "No es capability",
        "No es runtime",
        "No es execution source",
        "No es governance source",
        "No es state source",
        "No es observability source",
        "No es audit source",
        "No es package source",
        "No es package metadata source",
        "No es package decision source",
    ]:
        assert phrase in text


def test_no_package_module_or_operational_modules_created():
    assert not (ROOT / "core" / "runtime_execution_preparation_package.py").exists()
    allowed_preexisting = {
        "core/runtime_executor.py": "prepare-only",
    }
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


def test_runtime_execution_preparation_contract_flags_remain_closed():
    assert contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY is True
    assert contract.RUNTIME_EXECUTION_PREPARATION_OPERATIONAL is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_RUNTIME_ACTIVE is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_EXECUTION_ACTIVE is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_DRY_RUN_ACTIVE is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_TOOLS_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_MODELS_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_CONTEXT_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_OUTPUT_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_WRITES_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_STORES_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_MEMORY_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_NETWORK_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_BROWSER_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_FILESYSTEM_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_ENV_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_SECRETS_ENABLED is False
    assert contract.RUNTIME_EXECUTION_PREPARATION_INTEGRATIONS_ENABLED is False


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


FORBIDDEN_DATA = [
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

RISKS = [
    "Confundir Package con ejecucion",
    "Usar Package como bypass de Runtime Governance",
    "Usar Package como bypass de Runtime State",
    "Usar Package como bypass de Observability",
    "Usar Package como bypass de Runtime Activation Gate",
    "Usar Package como bypass de Human Approval",
    "Usar Package como bypass de Tool/Model/Context/Output boundaries",
    "Guardar metadata peligrosa",
    "Exponer Package crudo en UI",
    "Mezclar Master Panel y User Panel",
    "Usar Package para disparar runtime",
    "Usar Package para disparar dry-run real",
    "Crear stores/writers/readers antes de contrato",
    "Crear handoff operativo antes de contrato",
    "Incorporar OBLITERATUS como source/capability/integration",
]
