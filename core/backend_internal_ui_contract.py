"""Contrato backend interno para futura UI.

El modulo define una frontera JSON-safe, no-operativa y sin side effects para
que una UI futura pueda consumir estados sandbox sin inferir logica critica.
No crea servicios runtime, endpoints, frontend, integraciones ni writes.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any


CONTRACT_ID = "backend_internal_ui_contract_7_0"
CONTRACT_VERSION = "0.1"
CONTRACT_SCOPE = "backend_internal_ui"
CONTRACT_STATUS = "ready"
CONTRACT_READY_VERDICT = "BACKEND_INTERNAL_UI_CONTRACT_READY"
CONTRACT_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_phase_7_1_list_domains_status_service"
MAX_CONTRACT_JSON_BYTES = 64_000

VISIBLE_ENTITIES = (
    "sandbox_domain",
    "artifact_manifest",
    "profile_catalog",
    "agent_presets",
    "paper_seed",
    "sandbox_agents",
    "sandbox_team",
    "sandbox_team_read_model",
    "materialization_audit_pack",
    "rollback_report",
    "regeneration_report",
    "readiness",
    "validation_error",
)

PERMITTED_STATES = (
    "draft",
    "preview_ready",
    "sandbox_materialized",
    "sandbox_validated",
    "sandbox_audited",
    "rollback_ready",
    "rolled_back",
    "regeneration_ready",
    "regenerated",
    "audit_pack_ready",
    "invalid",
    "blocked",
    "pending",
)

PROHIBITED_STATES = (
    "active",
    "running",
    "live",
    "operational",
    "executing",
    "production_ready",
)

READINESS_VALUES = (
    "ready_for_internal_listing",
    "ready_for_preview",
    "ready_for_materialization",
    "ready_for_validation",
    "ready_for_phase_7_4_validate_domain_service",
    "ready_for_phase_7_5_rollback_archive_delete_reset_service",
    "ready_for_phase_7_6_stable_ui_payloads",
    "ready_for_rollback",
    "ready_for_regeneration",
    "ready_for_audit_pack",
    "ready_for_ui_contract",
    CONTRACT_READINESS,
    "not_ready",
    "blocked_by_validation",
    "blocked_by_permissions",
    "blocked_by_runtime_boundary",
)

ERROR_CODES = (
    "DIRTY_WORKING_TREE",
    "UNEXPECTED_HEAD",
    "INVALID_DOMAIN_PAYLOAD",
    "INVALID_SANDBOX_SCHEMA",
    "MISSING_ARTIFACT_MANIFEST",
    "INCONSISTENT_ARTIFACT_MANIFEST",
    "UNSAFE_PATH",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "UI_ACTION_NOT_IMPLEMENTED",
    "OPERATIONAL_WRITE_BLOCKED",
    "SECRET_LIKE_FIELD_BLOCKED",
    "PAYLOAD_NOT_JSON_SAFE",
    "READINESS_NOT_MET",
    "SANDBOX_ROOT_REQUIRED",
    "SANDBOX_ROOT_NOT_FOUND",
    "UNSAFE_SANDBOX_ROOT",
    "INVALID_DOMAIN_STATUS_PAYLOAD",
    "INVALID_AUDIT_PACK",
    "READ_MODEL_UNAVAILABLE",
    "DOMAIN_STATUS_NOT_LISTABLE",
    "DOMAIN_REQUEST_REQUIRED",
    "INVALID_DOMAIN_REQUEST",
    "INVALID_DOMAIN_ID",
    "UNSAFE_PLANNED_PATH",
    "PATH_TRAVERSAL_BLOCKED",
    "DOMAINS_OPERATIVE_PATH_BLOCKED",
    "PREVIEW_NOT_JSON_SAFE",
    "MATERIALIZATION_NOT_PERFORMED",
    "WRITE_OPERATION_BLOCKED",
    "PREVIEW_REQUIRED",
    "INVALID_PREVIEW_PAYLOAD",
    "PREVIEW_HAS_BLOCKING_ERRORS",
    "PREVIEW_ALREADY_MATERIALIZED",
    "CONFIRMATION_REQUIRED",
    "INVALID_CONFIRMATION_SCOPE",
    "OVERWRITE_BLOCKED",
    "ARTIFACT_MANIFEST_WRITE_FAILED",
    "MATERIALIZATION_FAILED",
    "ROLLBACK_PREPARATION_FAILED",
    "VALIDATION_REQUEST_REQUIRED",
    "INVALID_VALIDATE_DOMAIN_REQUEST",
    "DOMAIN_ID_REQUIRED",
    "DOMAIN_NOT_FOUND",
    "DOMAIN_ID_MISMATCH",
    "INVALID_DOMAIN_SCHEMA",
    "MISSING_CREATED_PATHS",
    "UNSAFE_CREATED_PATH",
    "MISSING_EXPECTED_ARTIFACT",
    "INVALID_READ_MODEL",
    "ROLLBACK_NOT_READY",
    "ROLLBACK_NOT_PERFORMED",
    "REGENERATION_NOT_PERFORMED",
    "LIFECYCLE_ACTION_REQUIRED",
    "INVALID_LIFECYCLE_ACTION",
    "VALIDATION_PAYLOAD_REQUIRED",
    "INVALID_VALIDATION_PAYLOAD",
    "VALIDATION_NOT_PASSED",
    "MATERIALIZATION_ID_MISMATCH",
    "UNDECLARED_PATH_BLOCKED",
    "REPO_ROOT_PATH_BLOCKED",
    "ROLLBACK_FAILED",
    "ARCHIVE_NOT_SUPPORTED",
    "ARCHIVE_FAILED",
    "DELETE_NOT_ALLOWED",
    "DELETE_FAILED",
    "RESET_NOT_ALLOWED",
    "RESET_FAILED",
)

SENSITIVE_KEY_FRAGMENTS = (
    "api_key",
    "access_token",
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "env",
    "environment",
    "model_config",
    "model_provider_config",
    "network_handle",
    "output_delivery_handle",
    "password",
    "provider_config",
    "raw_prompt",
    "raw_payload",
    "runtime_handle",
    "secret",
    "token",
    "tool_config",
    "tool_runtime",
)

ALLOWED_SENSITIVE_DECLARATION_KEYS = {
    "env",
    "secrets",
    "no_env_fields",
    "no_secret_like_fields",
    "no_network_browser_env_or_secrets",
    "SECRET_LIKE_FIELD_BLOCKED",
}

FORBIDDEN_OPERATIONAL_KEYS = {
    "operational",
    "runtime_enabled",
    "execution_enabled",
    "dry_run_real_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "context_injection_enabled",
    "output_delivery_enabled",
    "writes_enabled",
    "stores_enabled",
    "memory_enabled",
    "network_enabled",
    "browser_enabled",
    "filesystem_runtime_enabled",
    "api_runtime_enabled",
    "ui_runtime_enabled",
    "ui_visual_enabled",
    "public_endpoints_enabled",
    "integrations_enabled",
    "integration_active",
    "market_catalog_runtime_enabled",
    "business_composition_layer_runtime_enabled",
    "obliteratus_enabled",
    "raw_package_direct_to_user_panel_enabled",
}


def build_backend_internal_ui_capabilities() -> dict[str, bool]:
    """Devuelve capacidades de inspeccion permitidas para futura UI."""
    return {
        "can_read_backend_contract": True,
        "can_read_sandbox_status_payloads": True,
        "can_read_json_safe_summaries": True,
        "can_display_backend_errors": True,
        "can_infer_critical_logic": False,
        "can_invent_states": False,
        "can_resolve_permissions": False,
        "can_mutate_manifests": False,
        "can_trigger_runtime": False,
        "can_execute_agents": False,
        "can_invoke_models": False,
        "can_call_tools": False,
        "can_touch_integrations": False,
        "can_write_operational_domains": False,
        "can_use_raw_package_direct_to_user_panel": False,
    }


def build_backend_internal_ui_forbidden_capabilities() -> dict[str, bool]:
    """Declara todas las capacidades operativas que 7.0 mantiene bloqueadas."""
    return {
        "runtime": False,
        "execution": False,
        "dry_run_real": False,
        "tools": False,
        "models": False,
        "context_injection": False,
        "output_delivery": False,
        "writes": False,
        "stores": False,
        "memory": False,
        "network": False,
        "browser": False,
        "filesystem_runtime": False,
        "env": False,
        "secrets": False,
        "api_runtime": False,
        "ui_runtime": False,
        "ui_visual": False,
        "ui_device_control": False,
        "public_endpoints": False,
        "integrations": False,
        "market_catalog_runtime": False,
        "business_composition_layer_runtime": False,
        "obliteratus": False,
        "raw_package_direct_to_user_panel": False,
    }


def build_backend_internal_ui_error_contract() -> dict[str, Any]:
    """Contrato de errores legibles para futura UI."""
    shape = {
        "error_code": "",
        "message": "",
        "severity": "info|warning|error|critical",
        "field": "",
        "recoverable": True,
        "user_action": "",
        "developer_hint": "",
        "blocked": True,
    }
    return {
        "shape": shape,
        "allowed_severities": ["info", "warning", "error", "critical"],
        "expected_errors": [
            {
                "error_code": code,
                "message": _default_error_message(code),
                "severity": "error",
                "field": "",
                "recoverable": code
                not in {
                    "RUNTIME_BLOCKED",
                    "EXECUTION_BLOCKED",
                    "TOOLS_BLOCKED",
                    "MODELS_BLOCKED",
                    "INTEGRATIONS_BLOCKED",
                    "OPERATIONAL_WRITE_BLOCKED",
                },
                "user_action": "revisar el estado indicado por backend interno",
                "developer_hint": "mantener la decision en backend; la UI solo muestra el bloqueo",
                "blocked": True,
            }
            for code in ERROR_CODES
        ],
    }


def build_backend_internal_ui_contract() -> dict[str, Any]:
    """Construye el contrato base in-memory para futura UI."""
    capabilities = build_backend_internal_ui_capabilities()
    blocked = build_backend_internal_ui_forbidden_capabilities()
    contract = {
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "contract_scope": CONTRACT_SCOPE,
        "status": CONTRACT_STATUS,
        "verdict": CONTRACT_READY_VERDICT,
        "non_operational_verdict": CONTRACT_NO_OPERATIONAL_VERDICT,
        "readiness": CONTRACT_READINESS,
        "available_internal_services": _available_internal_services(),
        "planned_internal_services": _planned_internal_services(),
        "entities": _visible_entities(),
        "states": {
            "permitted": list(PERMITTED_STATES),
            "prohibited": list(PROHIBITED_STATES),
        },
        "readiness_values": list(READINESS_VALUES),
        "error_contract": build_backend_internal_ui_error_contract(),
        "permissions": capabilities,
        "blocked_capabilities": blocked,
        "non_operational_guarantees": _non_operational_guarantees(blocked),
        "payload_safety": _payload_safety(),
        "ui_boundaries": _ui_boundaries(),
        "source_blocks": _source_blocks(),
        "warnings": [],
        "validation": {
            "json_safe": True,
            "no_side_effects": True,
            "no_operational_capability_enabled": True,
            "future_ui_must_not_infer_critical_logic": True,
            "availability_is_not_overstated": True,
            "destructive_services_require_human_confirmation": True,
        },
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "dry_run_real_enabled": False,
        "ui_visual_enabled": False,
        "public_endpoints_enabled": False,
        "integrations_enabled": False,
    }
    return validate_backend_internal_ui_contract(contract)


def validate_backend_internal_ui_contract(contract: dict[str, Any]) -> dict[str, Any]:
    """Valida el contrato sin escribir, ejecutar ni acceder a recursos externos."""
    if not isinstance(contract, dict):
        raise ValueError("backend internal ui contract debe ser un objeto")

    required = {
        "contract_id",
        "contract_version",
        "contract_scope",
        "status",
        "verdict",
        "non_operational_verdict",
        "readiness",
        "available_internal_services",
        "planned_internal_services",
        "entities",
        "states",
        "readiness_values",
        "error_contract",
        "permissions",
        "blocked_capabilities",
        "non_operational_guarantees",
        "payload_safety",
        "ui_boundaries",
        "source_blocks",
        "warnings",
        "validation",
        "operational",
        "runtime_enabled",
        "execution_enabled",
    }
    missing = required - set(contract)
    if missing:
        raise ValueError(f"backend internal ui contract incompleto: {', '.join(sorted(missing))}")

    if contract.get("contract_id") != CONTRACT_ID:
        raise ValueError("contract_id invalido")
    if contract.get("contract_version") != CONTRACT_VERSION:
        raise ValueError("contract_version invalida")
    if contract.get("contract_scope") != CONTRACT_SCOPE:
        raise ValueError("contract_scope debe ser backend_internal_ui")
    if contract.get("status") != CONTRACT_STATUS:
        raise ValueError("status debe ser ready")
    if contract.get("verdict") != CONTRACT_READY_VERDICT:
        raise ValueError("verdict invalido")
    if contract.get("non_operational_verdict") != CONTRACT_NO_OPERATIONAL_VERDICT:
        raise ValueError("non_operational_verdict invalido")
    if contract.get("readiness") != CONTRACT_READINESS:
        raise ValueError("readiness invalida")

    _reject_sensitive_keys(contract)
    _validate_operational_flags(contract)
    _validate_services(contract)
    _validate_entities(contract)
    _validate_states(contract)
    _validate_readiness(contract)
    _validate_error_contract(contract)
    _validate_permissions(contract)
    _validate_blocked_capabilities(contract)
    _validate_payload_safety(contract)
    dumped = _ensure_json_safe(contract)
    if len(dumped.encode("utf-8")) > MAX_CONTRACT_JSON_BYTES:
        raise ValueError("backend internal ui contract excede tamano maximo")
    return deepcopy(contract)


def summarize_backend_internal_ui_contract(contract: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resumen seguro para documentacion, tests o futura introspeccion interna."""
    validated = validate_backend_internal_ui_contract(contract or build_backend_internal_ui_contract())
    return {
        "contract_id": validated["contract_id"],
        "contract_version": validated["contract_version"],
        "contract_scope": validated["contract_scope"],
        "status": validated["status"],
        "verdict": validated["verdict"],
        "non_operational_verdict": validated["non_operational_verdict"],
        "readiness": validated["readiness"],
        "entities_count": len(validated["entities"]),
        "available_services_count": len(validated["available_internal_services"]),
        "planned_services_count": len(validated["planned_internal_services"]),
        "future_ui_must_not_infer_critical_logic": True,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "blocked_capabilities": deepcopy(validated["blocked_capabilities"]),
    }


def _available_internal_services() -> list[dict[str, Any]]:
    return [
        _service(
            name="get_backend_internal_ui_contract",
            phase="7.0",
            service_type="read-only",
            available_now=True,
            payload_expected="backend_internal_ui_contract",
            expected_errors=["PAYLOAD_NOT_JSON_SAFE", "SECRET_LIKE_FIELD_BLOCKED"],
        ),
        _service(
            name="validate_backend_internal_ui_contract",
            phase="7.0",
            service_type="read-only",
            available_now=True,
            payload_expected="backend_internal_ui_contract",
            expected_errors=[
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "INTEGRATIONS_BLOCKED",
            ],
        ),
        _service(
            name="list_domains_status",
            phase="7.1",
            service_type="read-only",
            available_now=True,
            payload_expected="domain_status_listing",
            expected_errors=[
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "INVALID_DOMAIN_STATUS_PAYLOAD",
                "MISSING_ARTIFACT_MANIFEST",
                "INCONSISTENT_ARTIFACT_MANIFEST",
                "INVALID_AUDIT_PACK",
                "READ_MODEL_UNAVAILABLE",
                "DOMAIN_STATUS_NOT_LISTABLE",
                "PAYLOAD_NOT_JSON_SAFE",
            ],
        ),
        _service(
            name="preview_materialization",
            phase="7.2",
            service_type="read-only-preview",
            available_now=True,
            payload_expected="preview_materialization_payload",
            expected_errors=[
                "DOMAIN_REQUEST_REQUIRED",
                "INVALID_DOMAIN_REQUEST",
                "INVALID_DOMAIN_ID",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "UNSAFE_PLANNED_PATH",
                "PATH_TRAVERSAL_BLOCKED",
                "DOMAINS_OPERATIVE_PATH_BLOCKED",
                "PREVIEW_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "MATERIALIZATION_NOT_PERFORMED",
                "WRITE_OPERATION_BLOCKED",
                "READINESS_NOT_MET",
            ],
        ),
        _service(
            name="materialize_sandbox",
            phase="7.3",
            service_type="controlled-write",
            available_now=True,
            payload_expected="materialize_sandbox_request",
            expected_errors=[
                "PREVIEW_REQUIRED",
                "INVALID_PREVIEW_PAYLOAD",
                "PREVIEW_HAS_BLOCKING_ERRORS",
                "PREVIEW_ALREADY_MATERIALIZED",
                "CONFIRMATION_REQUIRED",
                "INVALID_CONFIRMATION_SCOPE",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "UNSAFE_PLANNED_PATH",
                "PATH_TRAVERSAL_BLOCKED",
                "DOMAINS_OPERATIVE_PATH_BLOCKED",
                "OVERWRITE_BLOCKED",
                "ARTIFACT_MANIFEST_WRITE_FAILED",
                "MATERIALIZATION_FAILED",
                "ROLLBACK_PREPARATION_FAILED",
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "TOOLS_BLOCKED",
                "MODELS_BLOCKED",
                "INTEGRATIONS_BLOCKED",
            ],
            requires_human_confirmation=True,
            side_effects=True,
            requires_valid_preview=True,
            prepares_rollback=True,
        ),
        _service(
            name="validate_domain",
            phase="7.4",
            service_type="read-only-validation",
            available_now=True,
            payload_expected="domain_validation_payload",
            expected_errors=[
                "VALIDATION_REQUEST_REQUIRED",
                "INVALID_VALIDATE_DOMAIN_REQUEST",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "DOMAIN_ID_REQUIRED",
                "DOMAIN_NOT_FOUND",
                "DOMAIN_ID_MISMATCH",
                "INVALID_DOMAIN_SCHEMA",
                "MISSING_ARTIFACT_MANIFEST",
                "INCONSISTENT_ARTIFACT_MANIFEST",
                "MISSING_CREATED_PATHS",
                "UNSAFE_CREATED_PATH",
                "MISSING_EXPECTED_ARTIFACT",
                "INVALID_READ_MODEL",
                "INVALID_AUDIT_PACK",
                "ROLLBACK_NOT_READY",
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "TOOLS_BLOCKED",
                "MODELS_BLOCKED",
                "INTEGRATIONS_BLOCKED",
                "WRITE_OPERATION_BLOCKED",
                "MATERIALIZATION_NOT_PERFORMED",
                "ROLLBACK_NOT_PERFORMED",
                "REGENERATION_NOT_PERFORMED",
            ],
        ),
        _service(
            name="rollback_sandbox",
            phase="7.5",
            service_type="destructive-controlled",
            available_now=True,
            payload_expected="domain_lifecycle_request",
            expected_errors=[
                "LIFECYCLE_ACTION_REQUIRED",
                "INVALID_LIFECYCLE_ACTION",
                "VALIDATION_PAYLOAD_REQUIRED",
                "INVALID_VALIDATION_PAYLOAD",
                "VALIDATION_NOT_PASSED",
                "CONFIRMATION_REQUIRED",
                "INVALID_CONFIRMATION_SCOPE",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "DOMAIN_ID_REQUIRED",
                "DOMAIN_NOT_FOUND",
                "MATERIALIZATION_ID_MISMATCH",
                "MISSING_ARTIFACT_MANIFEST",
                "INCONSISTENT_ARTIFACT_MANIFEST",
                "MISSING_CREATED_PATHS",
                "UNSAFE_CREATED_PATH",
                "UNDECLARED_PATH_BLOCKED",
                "DOMAINS_OPERATIVE_PATH_BLOCKED",
                "REPO_ROOT_PATH_BLOCKED",
                "ROLLBACK_NOT_READY",
                "ROLLBACK_FAILED",
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "TOOLS_BLOCKED",
                "MODELS_BLOCKED",
                "INTEGRATIONS_BLOCKED",
            ],
            destructive=True,
            requires_human_confirmation=True,
            side_effects=True,
            requires_validation_payload=True,
            requires_safe_sandbox_root=True,
        ),
        _service(
            name="archive_sandbox_domain",
            phase="7.5",
            service_type="controlled-write",
            available_now=True,
            payload_expected="domain_lifecycle_request",
            expected_errors=[
                "LIFECYCLE_ACTION_REQUIRED",
                "INVALID_LIFECYCLE_ACTION",
                "VALIDATION_PAYLOAD_REQUIRED",
                "INVALID_VALIDATION_PAYLOAD",
                "VALIDATION_NOT_PASSED",
                "CONFIRMATION_REQUIRED",
                "INVALID_CONFIRMATION_SCOPE",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "DOMAIN_ID_REQUIRED",
                "DOMAIN_NOT_FOUND",
                "MATERIALIZATION_ID_MISMATCH",
                "MISSING_ARTIFACT_MANIFEST",
                "MISSING_CREATED_PATHS",
                "UNDECLARED_PATH_BLOCKED",
                "DOMAINS_OPERATIVE_PATH_BLOCKED",
                "REPO_ROOT_PATH_BLOCKED",
                "OVERWRITE_BLOCKED",
                "ARCHIVE_FAILED",
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "TOOLS_BLOCKED",
                "MODELS_BLOCKED",
                "INTEGRATIONS_BLOCKED",
            ],
            destructive=False,
            requires_human_confirmation=True,
            side_effects=True,
            requires_validation_payload=True,
            requires_safe_sandbox_root=True,
        ),
        _service(
            name="delete_sandbox_domain",
            phase="7.5",
            service_type="destructive-controlled",
            available_now=True,
            payload_expected="domain_lifecycle_request",
            expected_errors=[
                "LIFECYCLE_ACTION_REQUIRED",
                "INVALID_LIFECYCLE_ACTION",
                "VALIDATION_PAYLOAD_REQUIRED",
                "INVALID_VALIDATION_PAYLOAD",
                "VALIDATION_NOT_PASSED",
                "CONFIRMATION_REQUIRED",
                "INVALID_CONFIRMATION_SCOPE",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "DOMAIN_ID_REQUIRED",
                "DOMAIN_NOT_FOUND",
                "MATERIALIZATION_ID_MISMATCH",
                "MISSING_ARTIFACT_MANIFEST",
                "MISSING_CREATED_PATHS",
                "UNSAFE_CREATED_PATH",
                "UNDECLARED_PATH_BLOCKED",
                "DOMAINS_OPERATIVE_PATH_BLOCKED",
                "REPO_ROOT_PATH_BLOCKED",
                "DELETE_NOT_ALLOWED",
                "DELETE_FAILED",
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "TOOLS_BLOCKED",
                "MODELS_BLOCKED",
                "INTEGRATIONS_BLOCKED",
            ],
            destructive=True,
            requires_human_confirmation=True,
            side_effects=True,
            requires_validation_payload=True,
            requires_safe_sandbox_root=True,
        ),
        _service(
            name="reset_sandbox_domain",
            phase="7.5",
            service_type="destructive-controlled",
            available_now=True,
            payload_expected="domain_lifecycle_request",
            expected_errors=[
                "LIFECYCLE_ACTION_REQUIRED",
                "INVALID_LIFECYCLE_ACTION",
                "VALIDATION_PAYLOAD_REQUIRED",
                "INVALID_VALIDATION_PAYLOAD",
                "VALIDATION_NOT_PASSED",
                "CONFIRMATION_REQUIRED",
                "INVALID_CONFIRMATION_SCOPE",
                "SANDBOX_ROOT_REQUIRED",
                "SANDBOX_ROOT_NOT_FOUND",
                "UNSAFE_SANDBOX_ROOT",
                "DOMAIN_ID_REQUIRED",
                "DOMAIN_NOT_FOUND",
                "MATERIALIZATION_ID_MISMATCH",
                "MISSING_ARTIFACT_MANIFEST",
                "MISSING_CREATED_PATHS",
                "UNSAFE_CREATED_PATH",
                "UNDECLARED_PATH_BLOCKED",
                "DOMAINS_OPERATIVE_PATH_BLOCKED",
                "REPO_ROOT_PATH_BLOCKED",
                "RESET_NOT_ALLOWED",
                "RESET_FAILED",
                "PAYLOAD_NOT_JSON_SAFE",
                "SECRET_LIKE_FIELD_BLOCKED",
                "RUNTIME_BLOCKED",
                "EXECUTION_BLOCKED",
                "TOOLS_BLOCKED",
                "MODELS_BLOCKED",
                "INTEGRATIONS_BLOCKED",
            ],
            destructive=True,
            requires_human_confirmation=True,
            side_effects=True,
            requires_validation_payload=True,
            requires_safe_sandbox_root=True,
        ),
    ]


def _planned_internal_services() -> list[dict[str, Any]]:
    return [
        _service("get_domain_detail", "7.1", "read-only", False, "sandbox_domain_detail", ["INVALID_DOMAIN_PAYLOAD"]),
        _service("get_sandbox_team_listing", "7.1", "read-only", False, "sandbox_team_listing", ["MISSING_ARTIFACT_MANIFEST"]),
        _service("get_materialization_audit_pack", "7.1", "read-only", False, "materialization_audit_pack_summary", ["READINESS_NOT_MET"]),
        _service(
            "stable_ui_payloads",
            "7.6",
            "read-only-contract",
            False,
            "stable_ui_payload_contract",
            ["READINESS_NOT_MET", "PAYLOAD_NOT_JSON_SAFE"],
        ),
    ]


def _service(
    name: str,
    phase: str,
    service_type: str,
    available_now: bool,
    payload_expected: str,
    expected_errors: list[str],
    *,
    destructive: bool = False,
    requires_human_confirmation: bool = False,
    side_effects: bool = False,
    requires_valid_preview: bool = False,
    prepares_rollback: bool = False,
    requires_validation_payload: bool = False,
    requires_safe_sandbox_root: bool = False,
) -> dict[str, Any]:
    return {
        "name": name,
        "phase": phase,
        "type": service_type,
        "available_now": available_now,
        "requires_human_confirmation": requires_human_confirmation,
        "destructive": destructive,
        "touches_runtime": False,
        "touches_visual_ui": False,
        "touches_integrations": False,
        "touches_operational_domains": False,
        "can_touch_operational_domains": False,
        "public_endpoint": False,
        "ui_action_implemented": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "side_effects": side_effects,
        "writes_performed": False,
        "materialization_performed": False,
        "requires_valid_preview": requires_valid_preview,
        "prepares_rollback": prepares_rollback,
        "requires_validation_payload": requires_validation_payload,
        "requires_safe_sandbox_root": requires_safe_sandbox_root,
        "payload_expected": payload_expected,
        "expected_errors": expected_errors,
    }


def _visible_entities() -> list[dict[str, Any]]:
    payload_fields = {
        "sandbox_domain": ["domain_id", "name", "status", "artifact_state", "readiness"],
        "artifact_manifest": ["artifact_count", "artifact_types", "lineage_valid", "dependencies_valid"],
        "profile_catalog": ["profiles_count", "coverage_summary", "status", "readiness"],
        "agent_presets": ["presets_count", "profile_refs_valid", "status", "readiness"],
        "paper_seed": ["paper_seed_count", "source_presets_count", "status", "readiness"],
        "sandbox_agents": ["agents_count", "roles_summary", "status", "readiness"],
        "sandbox_team": ["team_id", "domain_id", "name", "status", "members_count", "readiness"],
        "sandbox_team_read_model": ["teams_count", "read_model", "verdict", "readiness"],
        "materialization_audit_pack": ["audit_pack_id", "domain_id", "status", "verdict", "readiness"],
        "rollback_report": ["rollback_id", "domain_id", "removed_paths_count", "idempotent", "readiness"],
        "regeneration_report": ["regeneration_id", "domain_id", "lineage_preserved", "readiness"],
        "readiness": ["value", "source", "blocked", "blockers_count"],
        "validation_error": ["error_code", "message", "severity", "field", "recoverable", "blocked"],
    }
    return [
        {
            "entity": entity,
            "visible_to_future_ui": True,
            "runtime_entity": False,
            "minimal_payload_fields": payload_fields[entity],
            "forbidden_fields": [
                "secret-like keys",
                "environment variables",
                "runtime handles",
                "model/tool invocation configs",
                "raw prompts",
                "large dumps",
                "productive data",
            ],
        }
        for entity in VISIBLE_ENTITIES
    ]


def _non_operational_guarantees(blocked: dict[str, bool]) -> dict[str, Any]:
    return {
        "all_blocked_capabilities_false": all(value is False for value in blocked.values()),
        "no_runtime_activation": True,
        "no_execution_activation": True,
        "no_dry_run_real": True,
        "no_tools_or_models": True,
        "no_context_or_output_delivery": True,
        "no_writes_stores_or_memory": True,
        "no_network_browser_env_or_secrets": True,
        "no_visual_ui_or_public_endpoints": True,
        "no_integrations": True,
        "no_market_catalog_runtime": True,
        "no_business_composition_layer_runtime": True,
        "no_obliteratus": True,
        "no_raw_package_direct_to_user_panel": True,
    }


def _payload_safety() -> dict[str, Any]:
    return {
        "json_serializable": True,
        "no_sets_bytes_functions_or_path_objects": True,
        "no_secret_like_fields": True,
        "no_env_fields": True,
        "no_runtime_handles": True,
        "no_model_or_tool_invocation_configs": True,
        "no_large_dumps": True,
        "no_productive_data": True,
        "max_json_bytes": MAX_CONTRACT_JSON_BYTES,
    }


def _ui_boundaries() -> dict[str, Any]:
    return {
        "visual_ui_created": False,
        "frontend_created": False,
        "public_endpoints_created": False,
        "ui_runtime_created": False,
        "ui_device_control_enabled": False,
        "future_ui_is_consumer_only": True,
        "backend_remains_source_of_truth": True,
        "future_ui_must_not_infer_readiness": True,
        "future_ui_must_not_invent_states": True,
        "future_ui_must_not_bypass_backend_permissions": True,
    }


def _source_blocks() -> list[dict[str, str]]:
    return [
        {
            "source": "docs/BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT.md",
            "classification": "documento antecedente vigente reutilizable",
        },
        {
            "source": "core/sandbox_materialization_audit_pack.py",
            "classification": "vigente reutilizable para audit pack summary",
        },
        {
            "source": "core/sandbox_team_read_model.py",
            "classification": "vigente reutilizable para internal listing",
        },
        {
            "source": "core/internal_backend_read_model.py",
            "classification": "parcial a extender para frontera UI futura",
        },
    ]


def _validate_operational_flags(contract: dict[str, Any]) -> None:
    for field in FORBIDDEN_OPERATIONAL_KEYS:
        if contract.get(field) is True:
            raise ValueError(f"{field} debe ser false")
    _reject_recursive_enabled_operation(contract)


def _validate_services(contract: dict[str, Any]) -> None:
    available = contract.get("available_internal_services")
    planned = contract.get("planned_internal_services")
    if not isinstance(available, list) or not available:
        raise ValueError("available_internal_services requerido")
    if not isinstance(planned, list) or not planned:
        raise ValueError("planned_internal_services requerido")
    for service in [*available, *planned]:
        if not isinstance(service, dict) or not service.get("name"):
            raise ValueError("servicio interno invalido")
        if service.get("touches_runtime") is not False:
            raise ValueError(f"{service['name']} toca runtime")
        if service.get("touches_visual_ui") is not False:
            raise ValueError(f"{service['name']} toca UI visual")
        if service.get("touches_integrations") is not False:
            raise ValueError(f"{service['name']} toca integraciones")
        if service.get("touches_operational_domains") is not False:
            raise ValueError(f"{service['name']} toca domains operativo")
        if service.get("can_touch_operational_domains") is not False:
            raise ValueError(f"{service['name']} toca domains operativo")
        if service.get("public_endpoint") is not False:
            raise ValueError(f"{service['name']} expone endpoint publico")
        if service.get("ui_action_implemented") is not False:
            raise ValueError(f"{service['name']} implementa accion UI en 7.0")
        if service.get("runtime_enabled") is not False:
            raise ValueError(f"{service['name']} habilita runtime")
        if service.get("execution_enabled") is not False:
            raise ValueError(f"{service['name']} habilita execution")
        controlled_available_now = {
            "materialize_sandbox",
            "rollback_sandbox",
            "archive_sandbox_domain",
            "delete_sandbox_domain",
            "reset_sandbox_domain",
        }
        if (
            service.get("type") in {"controlled-write", "destructive-controlled"}
            and service.get("available_now") is True
            and service.get("name") not in controlled_available_now
        ):
            raise ValueError(f"{service['name']} no puede estar disponible en 7.0")
        if service.get("name") == "materialize_sandbox" and service.get("available_now") is True:
            if service.get("type") != "controlled-write":
                raise ValueError("materialize_sandbox debe ser controlled-write")
            if service.get("requires_human_confirmation") is not True:
                raise ValueError("materialize_sandbox requiere confirmacion humana")
            if service.get("requires_valid_preview") is not True:
                raise ValueError("materialize_sandbox requiere preview valido")
            if service.get("prepares_rollback") is not True:
                raise ValueError("materialize_sandbox requiere rollback preparado")
            if service.get("side_effects") is not True:
                raise ValueError("materialize_sandbox debe declarar side_effects=true")
            if service.get("destructive") is not False:
                raise ValueError("materialize_sandbox no debe ser destructivo")
        if service.get("destructive") is True and service.get("requires_human_confirmation") is not True:
            raise ValueError(f"{service['name']} destructivo requiere confirmacion humana")
        if service.get("name") in {"rollback_sandbox", "archive_sandbox_domain", "delete_sandbox_domain", "reset_sandbox_domain"}:
            if service.get("available_now") is not True:
                raise ValueError(f"{service['name']} debe estar disponible despues de 7.5")
            if service.get("phase") != "7.5":
                raise ValueError(f"{service['name']} debe pertenecer a fase 7.5")
            if service.get("requires_human_confirmation") is not True:
                raise ValueError(f"{service['name']} requiere confirmacion humana")
            if service.get("requires_validation_payload") is not True:
                raise ValueError(f"{service['name']} requiere validation_payload")
            if service.get("requires_safe_sandbox_root") is not True:
                raise ValueError(f"{service['name']} requiere sandbox_root seguro")
            if service.get("side_effects") is not True:
                raise ValueError(f"{service['name']} debe declarar side_effects=true")
            if service.get("touches_operational_domains") is not False:
                raise ValueError(f"{service['name']} no debe tocar domains operativo")
            if service.get("writes_performed") is not False:
                raise ValueError(f"{service['name']} no debe predeclarar writes_performed")
            if service.get("name") == "archive_sandbox_domain":
                if service.get("type") != "controlled-write":
                    raise ValueError("archive_sandbox_domain debe ser controlled-write")
                if service.get("destructive") is not False:
                    raise ValueError("archive_sandbox_domain no debe ser destructivo")
            else:
                if service.get("type") != "destructive-controlled":
                    raise ValueError(f"{service['name']} debe ser destructive-controlled")
                if service.get("destructive") is not True:
                    raise ValueError(f"{service['name']} debe ser destructivo")

    available_names = {service["name"] for service in available}
    allowed_now = {
        "get_backend_internal_ui_contract",
        "validate_backend_internal_ui_contract",
        "list_domains_status",
        "preview_materialization",
        "materialize_sandbox",
        "validate_domain",
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
    }
    if not available_names <= allowed_now:
        raise ValueError("7.0 declara como disponible un servicio no implementado")


def _validate_entities(contract: dict[str, Any]) -> None:
    entities = contract.get("entities")
    if not isinstance(entities, list):
        raise ValueError("entities debe ser lista")
    names = {entity.get("entity") for entity in entities if isinstance(entity, dict)}
    missing = set(VISIBLE_ENTITIES) - names
    if missing:
        raise ValueError(f"entities incompletas: {', '.join(sorted(missing))}")
    forbidden_runtime_entities = {"runtime", "execution_runner", "scheduler", "worker", "queue", "orchestrator"}
    if names & forbidden_runtime_entities:
        raise ValueError("entities contiene runtime operativo")
    for entity in entities:
        if entity.get("runtime_entity") is not False:
            raise ValueError(f"{entity.get('entity')} no puede ser runtime_entity")
        if not entity.get("minimal_payload_fields"):
            raise ValueError(f"{entity.get('entity')} sin payload minimo")


def _validate_states(contract: dict[str, Any]) -> None:
    states = contract.get("states")
    if not isinstance(states, dict):
        raise ValueError("states debe ser objeto")
    permitted = set(states.get("permitted") or [])
    prohibited = set(states.get("prohibited") or [])
    if not set(PERMITTED_STATES) <= permitted:
        raise ValueError("states.permitted incompleto")
    if not set(PROHIBITED_STATES) <= prohibited:
        raise ValueError("states.prohibited incompleto")
    if permitted & set(PROHIBITED_STATES):
        raise ValueError("states.permitted contiene estado operativo prohibido")


def _validate_readiness(contract: dict[str, Any]) -> None:
    values = set(contract.get("readiness_values") or [])
    if CONTRACT_READINESS not in values:
        raise ValueError("readiness_values no incluye readiness de 7.0")
    if any(value in values for value in ("ready_for_runtime", "ready_for_execution", "production_ready")):
        raise ValueError("readiness_values sugiere operacion real")


def _validate_error_contract(contract: dict[str, Any]) -> None:
    error_contract = contract.get("error_contract")
    if not isinstance(error_contract, dict):
        raise ValueError("error_contract debe ser objeto")
    shape = error_contract.get("shape")
    expected = error_contract.get("expected_errors")
    if not isinstance(shape, dict) or not isinstance(expected, list):
        raise ValueError("error_contract incompleto")
    required_shape = {
        "error_code",
        "message",
        "severity",
        "field",
        "recoverable",
        "user_action",
        "developer_hint",
        "blocked",
    }
    if required_shape - set(shape):
        raise ValueError("error_contract.shape incompleto")
    codes = {error.get("error_code") for error in expected if isinstance(error, dict)}
    missing = set(ERROR_CODES) - codes
    if missing:
        raise ValueError(f"error_contract sin errores esperados: {', '.join(sorted(missing))}")


def _validate_permissions(contract: dict[str, Any]) -> None:
    permissions = contract.get("permissions")
    if not isinstance(permissions, dict):
        raise ValueError("permissions debe ser objeto")
    for field in (
        "can_infer_critical_logic",
        "can_invent_states",
        "can_resolve_permissions",
        "can_mutate_manifests",
        "can_trigger_runtime",
        "can_execute_agents",
        "can_invoke_models",
        "can_call_tools",
        "can_touch_integrations",
        "can_write_operational_domains",
        "can_use_raw_package_direct_to_user_panel",
    ):
        if permissions.get(field) is not False:
            raise ValueError(f"permissions.{field} debe ser false")


def _validate_blocked_capabilities(contract: dict[str, Any]) -> None:
    blocked = contract.get("blocked_capabilities")
    if not isinstance(blocked, dict) or not blocked:
        raise ValueError("blocked_capabilities requerido")
    if any(value is not False for value in blocked.values()):
        raise ValueError("blocked_capabilities debe mantener todo false")
    guarantees = contract.get("non_operational_guarantees")
    if not isinstance(guarantees, dict) or guarantees.get("all_blocked_capabilities_false") is not True:
        raise ValueError("non_operational_guarantees incompleto")


def _validate_payload_safety(contract: dict[str, Any]) -> None:
    safety = contract.get("payload_safety")
    if not isinstance(safety, dict):
        raise ValueError("payload_safety debe ser objeto")
    for field in (
        "json_serializable",
        "no_sets_bytes_functions_or_path_objects",
        "no_secret_like_fields",
        "no_env_fields",
        "no_runtime_handles",
        "no_model_or_tool_invocation_configs",
        "no_large_dumps",
        "no_productive_data",
    ):
        if safety.get(field) is not True:
            raise ValueError(f"payload_safety.{field} debe ser true")


def _reject_sensitive_keys(value: Any, path: str = "") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if (
                key not in ALLOWED_SENSITIVE_DECLARATION_KEYS
                and not path.startswith(("blocked_capabilities", "payload_safety", "non_operational_guarantees"))
                and any(fragment in lowered for fragment in SENSITIVE_KEY_FRAGMENTS)
            ):
                raise ValueError(f"campo sensible bloqueado: {path + '.' if path else ''}{key}")
            _reject_sensitive_keys(nested, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_sensitive_keys(nested, f"{path}[{index}]")


def _reject_recursive_enabled_operation(value: Any, path: str = "") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_OPERATIONAL_KEYS and nested is True:
                raise ValueError(f"{path + '.' if path else ''}{key} debe ser false")
            _reject_recursive_enabled_operation(nested, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_recursive_enabled_operation(nested, f"{path}[{index}]")


def _ensure_json_safe(contract: dict[str, Any]) -> str:
    try:
        return json.dumps(contract, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("backend internal ui contract no es JSON-safe") from exc


def _default_error_message(code: str) -> str:
    return code.lower().replace("_", " ")
