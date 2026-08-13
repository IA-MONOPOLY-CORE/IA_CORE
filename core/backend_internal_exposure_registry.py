"""Registry interno de exposicion controlada para futura UI.

Este modulo declara un service map contractual/read-only. No ejecuta servicios,
no enruta requests, no crea handlers, no crea endpoints y no activa runtime.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any


SCHEMA_VERSION = "backend_internal_exposure_registry.v1"
REGISTRY_ID = "backend_internal_controlled_exposure_registry"
REGISTRY_STATUS = "ready"
REGISTRY_READINESS = "ready_for_phase_8_2_internal_request_envelope"
REGISTRY_VERDICT = "BACKEND_INTERNAL_EXPOSURE_REGISTRY_READY"
REGISTRY_NO_DISPATCHER_VERDICT = "BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_DISPATCHER_CONFIRMED"
REGISTRY_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_OPERATIONAL_CONFIRMED"
RESPONSE_SCHEMA_VERSION = "backend_internal_ui_payload.v1"
MAX_REGISTRY_JSON_BYTES = 96_000

EXPECTED_EXPOSABLE_SERVICES = (
    "list_domains_status",
    "preview_materialization",
    "materialize_sandbox",
    "validate_domain",
    "rollback_sandbox",
    "archive_sandbox_domain",
    "delete_sandbox_domain",
    "reset_sandbox_domain",
    "stable_ui_payloads",
    "internal_exposure_registry",
    "internal_request_validation",
    "internal_dispatcher_no_runtime",
)

EXPECTED_BLOCKED_SERVICES = (
    "runtime_execution",
    "agent_execution",
    "model_invocation",
    "tool_invocation",
    "external_integrations",
    "network_browser_automation",
    "public_endpoints",
    "ui_visual_runtime",
    "ui_device_control",
    "market_catalog_runtime",
    "business_composition_layer_runtime",
    "obliteratus",
    "domains_operativo",
    "raw_package_direct_to_user_panel",
    "scheduler_worker_queue",
    "orchestrator_dispatcher_event_bus",
)

GLOBAL_BLOCKED_CAPABILITIES = {
    "runtime": True,
    "execution": True,
    "tools": True,
    "models": True,
    "integrations": True,
    "network": True,
    "public_endpoints": True,
    "ui_runtime": True,
    "operational_domains": True,
    "secrets": True,
}

GLOBAL_FORBIDDEN_ACTIONS = (
    "activate_runtime",
    "execute_agents",
    "invoke_models",
    "call_tools",
    "use_integrations",
    "open_public_endpoint",
    "open_ui_runtime",
    "control_ui_device",
    "access_network",
    "access_secrets",
    "touch_operational_domains",
    "mutate_registry_from_ui",
    "infer_permissions_in_ui",
)

SERVICE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "list_domains_status": {
        "service_name": "list_domains_status",
        "service_kind": "read_only_status",
        "source_prompt": "PROMPT 7.1 - Servicio interno list_domains/status",
        "source_module": "core.backend_internal_domain_status_service",
        "source_doc": "docs/BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_7_1.md",
        "source_tests": ["tests/test_backend_internal_domain_status_service_7_1.py"],
        "input_contract": {
            "required": ["sandbox_root"],
            "optional": [],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": True,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_show": ["view_status", "view_details"], "backend_decides": True},
        "security_notes": ["read-only listing", "domains operativo bloqueado"],
    },
    "preview_materialization": {
        "service_name": "preview_materialization",
        "service_kind": "read_only_preview",
        "source_prompt": "PROMPT 7.2 - Servicio interno preview_materialization",
        "source_module": "core.backend_internal_preview_materialization_service",
        "source_doc": "docs/BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_7_2.md",
        "source_tests": ["tests/test_backend_internal_preview_materialization_service_7_2.py"],
        "input_contract": {
            "required": ["domain_request", "sandbox_root"],
            "optional": ["preview_options"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": True,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_show": ["view_preview", "view_planned_artifacts"], "backend_decides": True},
        "security_notes": ["no-write preview", "planned paths relativos"],
    },
    "materialize_sandbox": {
        "service_name": "materialize_sandbox",
        "service_kind": "controlled_write",
        "source_prompt": "PROMPT 7.3 - Servicio interno materialize_sandbox",
        "source_module": "core.backend_internal_materialize_sandbox_service",
        "source_doc": "docs/BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_7_3.md",
        "source_tests": ["tests/test_backend_internal_materialize_sandbox_service_7_3.py"],
        "input_contract": {
            "required": ["preview_payload", "sandbox_root", "confirmation"],
            "optional": ["materialization_options"],
            "requires_preview_payload": True,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": True,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": True,
        "side_effects": True,
        "destructive": False,
        "allowed_actions_policy": {"may_request": ["materialize_sandbox"], "backend_decides": True},
        "security_notes": ["preview valido obligatorio", "allow_overwrite=false"],
    },
    "validate_domain": {
        "service_name": "validate_domain",
        "service_kind": "read_only_validation",
        "source_prompt": "PROMPT 7.4 - Servicio interno validate_domain",
        "source_module": "core.backend_internal_validate_domain_service",
        "source_doc": "docs/BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_7_4.md",
        "source_tests": ["tests/test_backend_internal_validate_domain_service_7_4.py"],
        "input_contract": {
            "required": ["sandbox_root", "domain_id"],
            "optional": ["materialization_id", "validation_options"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": True,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_show": ["view_validation_report"], "backend_decides": True},
        "security_notes": ["read-only validation", "created_paths inside sandbox"],
    },
    "rollback_sandbox": {
        "service_name": "rollback_sandbox",
        "service_kind": "controlled_lifecycle",
        "source_prompt": "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
        "source_module": "core.backend_internal_domain_lifecycle_service",
        "source_doc": "docs/BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5.md",
        "source_tests": ["tests/test_backend_internal_domain_lifecycle_service_7_5.py"],
        "input_contract": {
            "required": ["validation_payload", "sandbox_root", "confirmation"],
            "optional": ["options"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": True,
        "requires_validation_payload": True,
        "requires_safe_sandbox_root": True,
        "side_effects": True,
        "destructive": True,
        "allowed_actions_policy": {"may_request": ["rollback_sandbox"], "backend_decides": True},
        "security_notes": ["rollback readiness obligatorio", "paths declarados por manifest"],
    },
    "archive_sandbox_domain": {
        "service_name": "archive_sandbox_domain",
        "service_kind": "controlled_lifecycle",
        "source_prompt": "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
        "source_module": "core.backend_internal_domain_lifecycle_service",
        "source_doc": "docs/BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5.md",
        "source_tests": ["tests/test_backend_internal_domain_lifecycle_service_7_5.py"],
        "input_contract": {
            "required": ["validation_payload", "sandbox_root", "confirmation"],
            "optional": ["options"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": True,
        "requires_validation_payload": True,
        "requires_safe_sandbox_root": True,
        "side_effects": True,
        "destructive": False,
        "allowed_actions_policy": {"may_request": ["archive_sandbox_domain"], "backend_decides": True},
        "security_notes": ["archive dentro de sandbox", "no borra definitivamente"],
    },
    "delete_sandbox_domain": {
        "service_name": "delete_sandbox_domain",
        "service_kind": "controlled_lifecycle",
        "source_prompt": "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
        "source_module": "core.backend_internal_domain_lifecycle_service",
        "source_doc": "docs/BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5.md",
        "source_tests": ["tests/test_backend_internal_domain_lifecycle_service_7_5.py"],
        "input_contract": {
            "required": ["validation_payload", "sandbox_root", "confirmation", "allow_delete"],
            "optional": ["options"],
            "requires_preview_payload": False,
            "requires_allow_delete": True,
            "requires_allow_reset": False,
        },
        "requires_confirmation": True,
        "requires_validation_payload": True,
        "requires_safe_sandbox_root": True,
        "side_effects": True,
        "destructive": True,
        "allowed_actions_policy": {"may_request": ["delete_sandbox_domain"], "backend_decides": True},
        "security_notes": ["allow_delete=true obligatorio", "target declarado dentro sandbox"],
    },
    "reset_sandbox_domain": {
        "service_name": "reset_sandbox_domain",
        "service_kind": "controlled_lifecycle",
        "source_prompt": "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
        "source_module": "core.backend_internal_domain_lifecycle_service",
        "source_doc": "docs/BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5.md",
        "source_tests": ["tests/test_backend_internal_domain_lifecycle_service_7_5.py"],
        "input_contract": {
            "required": ["validation_payload", "sandbox_root", "confirmation", "allow_reset"],
            "optional": ["options"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": True,
        },
        "requires_confirmation": True,
        "requires_validation_payload": True,
        "requires_safe_sandbox_root": True,
        "side_effects": True,
        "destructive": True,
        "allowed_actions_policy": {"may_request": ["reset_sandbox_domain"], "backend_decides": True},
        "security_notes": ["allow_reset=true obligatorio", "no regenera automaticamente"],
    },
    "stable_ui_payloads": {
        "service_name": "stable_ui_payloads",
        "service_kind": "contract_payload_normalization",
        "source_prompt": "PROMPT 7.6 - Payloads estables para futura UI",
        "source_module": "core.backend_internal_ui_payloads",
        "source_doc": "docs/BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6.md",
        "source_tests": ["tests/test_backend_internal_ui_payloads_7_6.py"],
        "input_contract": {
            "required": ["payload"],
            "optional": [],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": False,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_normalize": ["backend_internal_ui_payload.v1"], "backend_decides": True},
        "security_notes": ["JSON-safe", "sanitiza paths absolutos sensibles"],
    },
    "internal_exposure_registry": {
        "service_name": "internal_exposure_registry",
        "service_kind": "contract_internal_exposure_registry",
        "source_prompt": "PROMPT 8.1 - Internal exposure registry / service map",
        "source_module": "core.backend_internal_exposure_registry",
        "source_doc": "docs/BACKEND_INTERNAL_EXPOSURE_REGISTRY_8_1.md",
        "source_tests": ["tests/test_backend_internal_exposure_registry_8_1.py"],
        "input_contract": {
            "required": [],
            "optional": ["include_blocked_services"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": False,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_show": ["view_service_map"], "backend_decides": True},
        "security_notes": ["service map contractual", "no ejecuta servicios"],
    },
    "internal_request_validation": {
        "service_name": "internal_request_validation",
        "service_kind": "contract_request_validation",
        "source_prompt": "PROMPT 8.2 - Internal request envelope y request validation",
        "source_module": "core.backend_internal_request_envelope",
        "source_doc": "docs/BACKEND_INTERNAL_REQUEST_ENVELOPE_8_2.md",
        "source_tests": ["tests/test_backend_internal_request_envelope_8_2.py"],
        "input_contract": {
            "required": ["request_envelope"],
            "optional": [],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": False,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_validate": ["backend_internal_ui_request.v1"], "backend_decides": True},
        "security_notes": ["request validation contractual", "no enruta ni ejecuta"],
    },
    "internal_dispatcher_no_runtime": {
        "service_name": "internal_dispatcher_no_runtime",
        "service_kind": "contract_internal_dispatcher",
        "source_prompt": "PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto",
        "source_module": "core.backend_internal_dispatcher",
        "source_doc": "docs/BACKEND_INTERNAL_DISPATCHER_8_3.md",
        "source_tests": ["tests/test_backend_internal_dispatcher_8_3.py"],
        "input_contract": {
            "required": ["request_envelope"],
            "optional": ["dispatch_options"],
            "requires_preview_payload": False,
            "requires_allow_delete": False,
            "requires_allow_reset": False,
        },
        "requires_confirmation": False,
        "requires_validation_payload": False,
        "requires_safe_sandbox_root": False,
        "side_effects": False,
        "destructive": False,
        "allowed_actions_policy": {"may_dispatch_contract_only": ["safe_contract_services"], "backend_decides": True},
        "security_notes": ["dispatcher contractual", "no runtime", "no side effects"],
    },
}


def build_internal_exposure_registry() -> dict[str, Any]:
    """Construye el registry contractual sin ejecutar servicios ni leer recursos externos."""
    exposable = [_service_entry(service_id, SERVICE_DEFINITIONS[service_id]) for service_id in EXPECTED_EXPOSABLE_SERVICES]
    blocked = [_blocked_service_entry(service_id) for service_id in EXPECTED_BLOCKED_SERVICES]
    registry = {
        "schema_version": SCHEMA_VERSION,
        "registry_id": REGISTRY_ID,
        "status": REGISTRY_STATUS,
        "verdict": REGISTRY_VERDICT,
        "no_dispatcher_verdict": REGISTRY_NO_DISPATCHER_VERDICT,
        "non_operational_verdict": REGISTRY_NO_OPERATIONAL_VERDICT,
        "readiness": REGISTRY_READINESS,
        "source_phase": "phase_8_controlled_internal_exposure",
        "depends_on": ["backend_internal_ui_contract", RESPONSE_SCHEMA_VERSION],
        "exposable_services": exposable,
        "blocked_services": blocked,
        "service_groups": {
            "read_only": ["list_domains_status", "preview_materialization", "validate_domain", "stable_ui_payloads"],
            "contract": [
                "internal_exposure_registry",
                "internal_request_validation",
                "internal_dispatcher_no_runtime",
            ],
            "controlled_write": ["materialize_sandbox"],
            "controlled_lifecycle": [
                "rollback_sandbox",
                "archive_sandbox_domain",
                "delete_sandbox_domain",
                "reset_sandbox_domain",
            ],
        },
        "global_blocked_capabilities": deepcopy(GLOBAL_BLOCKED_CAPABILITIES),
        "global_forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
        "validation": {
            "json_safe": True,
            "no_duplicate_services": True,
            "backend_authority": True,
            "ui_may_infer_permissions": False,
            "dispatcher_created": False,
            "request_handling_enabled": False,
            "services_execute_from_registry": False,
            "response_schema_version": RESPONSE_SCHEMA_VERSION,
        },
        "warnings": [],
        "errors": [],
        "flags": _non_operational_flags(),
    }
    return validate_internal_exposure_registry(registry)


def validate_internal_exposure_registry(registry: dict[str, Any]) -> dict[str, Any]:
    """Valida el registry sin side effects."""
    if not isinstance(registry, dict):
        raise ValueError("internal exposure registry debe ser objeto")
    required = {
        "schema_version",
        "registry_id",
        "status",
        "readiness",
        "depends_on",
        "exposable_services",
        "blocked_services",
        "service_groups",
        "global_blocked_capabilities",
        "global_forbidden_actions",
        "validation",
        "warnings",
        "errors",
        "flags",
    }
    missing = required - set(registry)
    if missing:
        raise ValueError(f"internal exposure registry incompleto: {', '.join(sorted(missing))}")
    if registry["schema_version"] != SCHEMA_VERSION:
        raise ValueError("schema_version invalida")
    if registry["registry_id"] != REGISTRY_ID:
        raise ValueError("registry_id invalido")
    if registry["status"] != REGISTRY_STATUS:
        raise ValueError("status invalido")
    if registry["readiness"] != REGISTRY_READINESS:
        raise ValueError("readiness invalida")
    _validate_root_flags(registry["flags"])
    _validate_global_policy(registry)
    _validate_exposable_services(registry["exposable_services"])
    _validate_blocked_services(registry["blocked_services"], registry["exposable_services"])
    _validate_registry_validation(registry["validation"])
    encoded = _ensure_json_safe(registry)
    if len(encoded.encode("utf-8")) > MAX_REGISTRY_JSON_BYTES:
        raise ValueError("internal exposure registry excede tamano maximo")
    return deepcopy(registry)


def list_exposable_services() -> list[dict[str, Any]]:
    """Lista servicios exponibles declarados, sin ejecutarlos."""
    return deepcopy(build_internal_exposure_registry()["exposable_services"])


def get_exposable_service(service_id: str) -> dict[str, Any] | None:
    """Devuelve una entrada exponible por id o None si no existe/no es exponible."""
    target = str(service_id or "")
    for service in build_internal_exposure_registry()["exposable_services"]:
        if service["service_id"] == target:
            return deepcopy(service)
    return None


def list_blocked_services() -> list[dict[str, Any]]:
    """Lista servicios explicitamente no exponibles."""
    return deepcopy(build_internal_exposure_registry()["blocked_services"])


def is_service_exposable(service_id: str) -> bool:
    """Indica si un service_id esta en el mapa exponible."""
    return get_exposable_service(service_id) is not None


def validate_exposure_service_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Valida una entrada de servicio exponible."""
    if not isinstance(entry, dict):
        raise ValueError("service entry debe ser objeto")
    required = {
        "service_id",
        "service_name",
        "service_kind",
        "available_now",
        "exposable",
        "source_prompt",
        "source_module",
        "source_doc",
        "source_tests",
        "input_contract",
        "response_schema_version",
        "requires_confirmation",
        "requires_validation_payload",
        "requires_safe_sandbox_root",
        "side_effects",
        "destructive",
        "allowed_actions_policy",
        "forbidden_actions",
        "blocked_capabilities",
        "security_notes",
        "ui_boundary",
        "flags",
    }
    missing = required - set(entry)
    if missing:
        raise ValueError(f"service entry incompleto: {', '.join(sorted(missing))}")
    if entry["service_id"] not in EXPECTED_EXPOSABLE_SERVICES:
        raise ValueError("service_id no permitido")
    if entry["available_now"] is not True or entry["exposable"] is not True:
        raise ValueError("servicio exponible debe estar available_now=true y exposable=true")
    if entry["response_schema_version"] != RESPONSE_SCHEMA_VERSION:
        raise ValueError("response_schema_version invalido")
    if not entry["source_module"] or not entry["source_doc"] or not entry["source_tests"]:
        raise ValueError("service entry requiere module/doc/tests")
    _validate_root_flags(entry["flags"])
    if any(value is not True for value in entry["blocked_capabilities"].values()):
        raise ValueError("blocked_capabilities usa true = blocked")
    if not set(GLOBAL_FORBIDDEN_ACTIONS) <= set(entry["forbidden_actions"]):
        raise ValueError("forbidden_actions incompleto")
    boundary = entry["ui_boundary"]
    if boundary.get("backend_authority") is not True:
        raise ValueError("backend_authority debe ser true")
    if boundary.get("ui_may_infer_permissions") is not False or boundary.get("ui_may_execute") is not False:
        raise ValueError("UI no puede inferir permisos ni ejecutar")
    if entry["destructive"] is True and entry["requires_confirmation"] is not True:
        raise ValueError("servicio destructive requiere confirmacion")
    if entry["service_kind"] == "controlled_lifecycle" and entry["requires_validation_payload"] is not True:
        raise ValueError("servicio lifecycle requiere validation_payload")
    input_contract = entry["input_contract"]
    if entry["service_id"] == "delete_sandbox_domain" and input_contract.get("requires_allow_delete") is not True:
        raise ValueError("delete_sandbox_domain requiere allow_delete")
    if entry["service_id"] == "reset_sandbox_domain" and input_contract.get("requires_allow_reset") is not True:
        raise ValueError("reset_sandbox_domain requiere allow_reset")
    _ensure_json_safe(entry)
    return deepcopy(entry)


def build_exposure_registry_error(error_code: str, message: str, *, field: str = "") -> dict[str, Any]:
    """Construye error controlado para validaciones futuras del registry."""
    return {
        "error_code": str(error_code or "INVALID_EXPOSURE_REGISTRY"),
        "message": str(message or "internal exposure registry invalido")[:240],
        "severity": "error",
        "field": str(field or ""),
        "recoverable": True,
        "blocked": True,
    }


def _service_entry(service_id: str, definition: dict[str, Any]) -> dict[str, Any]:
    entry = {
        "service_id": service_id,
        "service_name": definition["service_name"],
        "service_kind": definition["service_kind"],
        "available_now": True,
        "exposable": True,
        "source_prompt": definition["source_prompt"],
        "source_module": definition["source_module"],
        "source_doc": definition["source_doc"],
        "source_tests": list(definition["source_tests"]),
        "input_contract": deepcopy(definition["input_contract"]),
        "response_schema_version": RESPONSE_SCHEMA_VERSION,
        "requires_confirmation": definition["requires_confirmation"],
        "requires_validation_payload": definition["requires_validation_payload"],
        "requires_safe_sandbox_root": definition["requires_safe_sandbox_root"],
        "side_effects": definition["side_effects"],
        "destructive": definition["destructive"],
        "allowed_actions_policy": deepcopy(definition["allowed_actions_policy"]),
        "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
        "blocked_capabilities": deepcopy(GLOBAL_BLOCKED_CAPABILITIES),
        "security_notes": list(definition["security_notes"]),
        "ui_boundary": {
            "backend_authority": True,
            "ui_may_infer_permissions": False,
            "ui_may_execute": False,
        },
        "flags": _non_operational_flags(),
    }
    return validate_exposure_service_entry(entry)


def _blocked_service_entry(service_id: str) -> dict[str, Any]:
    return {
        "service_id": service_id,
        "blocked": True,
        "available_now": False,
        "reason": f"{service_id} no es exponible en Fase 8.1",
        "blocked_capabilities": deepcopy(GLOBAL_BLOCKED_CAPABILITIES),
        "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
    }


def _non_operational_flags() -> dict[str, bool]:
    return {
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tools_enabled": False,
        "models_enabled": False,
        "integrations_enabled": False,
        "ui_visual": False,
        "public_endpoint": False,
        "dispatcher_created": False,
        "request_handling_enabled": False,
    }


def _validate_root_flags(flags: dict[str, Any]) -> None:
    if not isinstance(flags, dict):
        raise ValueError("flags debe ser objeto")
    required = set(_non_operational_flags())
    missing = required - set(flags)
    if missing:
        raise ValueError(f"flags incompleto: {', '.join(sorted(missing))}")
    for key in required:
        if flags.get(key) is not False:
            raise ValueError(f"{key} debe ser false")


def _validate_global_policy(registry: dict[str, Any]) -> None:
    blocked = registry["global_blocked_capabilities"]
    if set(GLOBAL_BLOCKED_CAPABILITIES) - set(blocked):
        raise ValueError("global_blocked_capabilities incompleto")
    if any(value is not True for value in blocked.values()):
        raise ValueError("global_blocked_capabilities usa true = blocked")
    if not set(GLOBAL_FORBIDDEN_ACTIONS) <= set(registry["global_forbidden_actions"]):
        raise ValueError("global_forbidden_actions incompleto")


def _validate_exposable_services(services: list[dict[str, Any]]) -> None:
    if not isinstance(services, list) or not services:
        raise ValueError("exposable_services requerido")
    ids = [service.get("service_id") for service in services if isinstance(service, dict)]
    if len(ids) != len(set(ids)):
        raise ValueError("servicios exponibles duplicados")
    if set(ids) != set(EXPECTED_EXPOSABLE_SERVICES):
        raise ValueError("servicios exponibles incompletos")
    for service in services:
        validate_exposure_service_entry(service)


def _validate_blocked_services(blocked_services: list[dict[str, Any]], exposable_services: list[dict[str, Any]]) -> None:
    if not isinstance(blocked_services, list) or not blocked_services:
        raise ValueError("blocked_services requerido")
    exposable_ids = {service["service_id"] for service in exposable_services}
    ids = set()
    for service in blocked_services:
        if not isinstance(service, dict):
            raise ValueError("blocked service debe ser objeto")
        service_id = service.get("service_id")
        ids.add(service_id)
        if service.get("blocked") is not True:
            raise ValueError("blocked service debe declarar blocked=true")
        if service.get("available_now") is not False:
            raise ValueError("blocked service debe declarar available_now=false")
        if service_id in exposable_ids:
            raise ValueError("blocked service no puede ser exponible")
        if any(value is not True for value in service.get("blocked_capabilities", {}).values()):
            raise ValueError("blocked service capabilities deben usar true=blocked")
        if not set(GLOBAL_FORBIDDEN_ACTIONS) <= set(service.get("forbidden_actions") or []):
            raise ValueError("blocked service forbidden_actions incompleto")
    if set(EXPECTED_BLOCKED_SERVICES) - ids:
        raise ValueError("blocked_services incompleto")


def _validate_registry_validation(validation: dict[str, Any]) -> None:
    required_truthy = {"json_safe", "no_duplicate_services", "backend_authority"}
    for key in required_truthy:
        if validation.get(key) is not True:
            raise ValueError(f"validation.{key} debe ser true")
    for key in ("ui_may_infer_permissions", "dispatcher_created", "request_handling_enabled", "services_execute_from_registry"):
        if validation.get(key) is not False:
            raise ValueError(f"validation.{key} debe ser false")
    if validation.get("response_schema_version") != RESPONSE_SCHEMA_VERSION:
        raise ValueError("validation.response_schema_version invalido")


def _ensure_json_safe(payload: Any) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("internal exposure registry no es JSON-safe") from exc
