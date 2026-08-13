"""Servicio interno materialize_sandbox controlled-write para futura UI.

El servicio exige preview valido, sandbox_root seguro y confirmacion explicita
antes de reutilizar la cadena sandbox completa validada en Fase 6.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from core.backend_internal_preview_materialization_service import (
    validate_materialization_preview_payload,
)
from core.backend_internal_ui_contract import build_backend_internal_ui_forbidden_capabilities


SERVICE_NAME = "materialize_sandbox"
SERVICE_VERSION = "0.1"
SERVICE_STATUS = "materialized"
SERVICE_VERDICT = "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_READY"
SERVICE_CONTROLLED_WRITE_VERDICT = "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_CONTROLLED_WRITE_CONFIRMED"
SERVICE_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_NO_OPERATIONAL_CONFIRMED"
SERVICE_READINESS = "ready_for_phase_7_4_validate_domain_service"
MAX_RESULT_JSON_BYTES = 128_000

ALLOWED_ACTIONS = (
    "view_status",
    "view_details",
    "view_audit_pack_summary",
    "request_validation_next_step",
    "request_rollback_next_step",
)
FORBIDDEN_ACTIONS = (
    "activate_runtime",
    "execute_agents",
    "invoke_models",
    "call_tools",
    "use_integrations",
    "write_operational_outputs",
    "mutate_manifest_directly",
    "delete_without_confirmation",
    "rollback_without_confirmation",
    "regenerate_without_rollback",
    "open_ui_runtime",
)
ERROR_CODES = (
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
    "SECRET_LIKE_FIELD_BLOCKED",
}
FORBIDDEN_OPERATIONAL_TRUE_KEYS = {
    "operational",
    "passed",
    "runtime_enabled",
    "execution_enabled",
    "dry_run_real_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "context_injection_enabled",
    "output_delivery_enabled",
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
    "market_catalog_runtime_enabled",
    "business_composition_layer_runtime_enabled",
    "obliteratus_enabled",
    "raw_package_direct_to_user_panel_enabled",
    "active",
}


def materialize_sandbox(request: dict[str, Any] | None) -> dict[str, Any]:
    """Materializa una cadena sandbox completa con confirmacion explicita."""
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not isinstance(request, dict):
        errors.append(build_materialize_sandbox_error("PREVIEW_REQUIRED", "request requerido"))
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))

    try:
        _reject_sensitive_keys(request)
        _ensure_json_safe(request)
    except ValueError as exc:
        errors.append(build_materialize_sandbox_error("SECRET_LIKE_FIELD_BLOCKED", str(exc), recoverable=False))
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))

    root_result = _resolve_sandbox_root(request.get("sandbox_root"))
    if root_result.get("error"):
        errors.append(root_result["error"])
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))
    sandbox_root = root_result["root"]

    options = _materialization_options(request.get("materialization_options"))
    if options["allow_overwrite"]:
        errors.append(
            build_materialize_sandbox_error(
                "OVERWRITE_BLOCKED",
                "allow_overwrite=true no esta habilitado para materialize_sandbox",
                field="materialization_options.allow_overwrite",
                recoverable=False,
            )
        )
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))
    if not options["prepare_rollback"]:
        errors.append(
            build_materialize_sandbox_error(
                "ROLLBACK_PREPARATION_FAILED",
                "prepare_rollback=true es obligatorio",
                field="materialization_options.prepare_rollback",
                recoverable=False,
            )
        )
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))

    confirmation_result = _validate_confirmation(request.get("confirmation"))
    if confirmation_result.get("error"):
        errors.append(confirmation_result["error"])
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))
    confirmation = confirmation_result["confirmation"]

    preview_result = validate_preview_for_materialization(
        request.get("preview_payload"),
        sandbox_root=sandbox_root,
        allow_overwrite=options["allow_overwrite"],
    )
    if preview_result.get("error"):
        errors.append(preview_result["error"])
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))
    preview_payload = preview_result["preview_payload"]

    try:
        materialization = _materialize_full_chain(
            preview_payload=preview_payload,
            sandbox_root=sandbox_root,
            confirmation=confirmation,
            options=options,
        )
        result = _build_materialized_payload(
            preview_payload=preview_payload,
            sandbox_root=sandbox_root,
            confirmation=confirmation,
            options=options,
            materialization=materialization,
            warnings=warnings,
        )
    except FileExistsError as exc:
        errors.append(build_materialize_sandbox_error("OVERWRITE_BLOCKED", str(exc), recoverable=False))
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))
    except ValueError as exc:
        errors.append(_error_from_exception(exc))
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))
    except OSError as exc:
        errors.append(build_materialize_sandbox_error("MATERIALIZATION_FAILED", str(exc), recoverable=False))
        return validate_materialize_sandbox_result(_blocked_payload(errors=errors, warnings=warnings))

    return validate_materialize_sandbox_result(result)


def build_materialize_sandbox_request(
    *,
    preview_payload: dict[str, Any],
    sandbox_root: str | Path,
    confirmation: dict[str, Any] | None = None,
    materialization_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construye una request explicita y JSON-safe para materialize_sandbox."""
    request = {
        "preview_payload": deepcopy(preview_payload),
        "sandbox_root": str(sandbox_root),
        "confirmation": deepcopy(confirmation)
        if confirmation is not None
        else {
            "confirmed": True,
            "confirmation_scope": SERVICE_NAME,
            "human_confirmation_required": True,
            "confirmed_by": "internal_backend",
            "confirmation_id": f"confirm_{_safe_id(preview_payload.get('domain_preview', {}).get('preview_id', 'manual'))}",
        },
        "materialization_options": {
            "prepare_rollback": True,
            "build_read_models": True,
            "build_audit_pack_if_supported": False,
            "allow_overwrite": False,
            **(materialization_options or {}),
        },
    }
    _reject_sensitive_keys(request)
    _ensure_json_safe(request)
    return request


def validate_materialize_sandbox_request(request: dict[str, Any]) -> dict[str, Any]:
    """Valida request sin escribir archivos ni materializar."""
    if not isinstance(request, dict):
        raise ValueError("materialize_sandbox request debe ser objeto")
    _reject_sensitive_keys(request)
    _ensure_json_safe(request)
    root_result = _resolve_sandbox_root(request.get("sandbox_root"))
    if root_result.get("error"):
        raise ValueError(root_result["error"]["message"])
    options = _materialization_options(request.get("materialization_options"))
    if options["allow_overwrite"]:
        raise ValueError("allow_overwrite no esta habilitado")
    if not options["prepare_rollback"]:
        raise ValueError("prepare_rollback requerido")
    confirmation_result = _validate_confirmation(request.get("confirmation"))
    if confirmation_result.get("error"):
        raise ValueError(confirmation_result["error"]["message"])
    preview_result = validate_preview_for_materialization(
        request.get("preview_payload"),
        sandbox_root=root_result["root"],
        allow_overwrite=options["allow_overwrite"],
    )
    if preview_result.get("error"):
        raise ValueError(preview_result["error"]["message"])
    return {
        "preview_payload": preview_result["preview_payload"],
        "sandbox_root": str(root_result["root"]),
        "confirmation": confirmation_result["confirmation"],
        "materialization_options": options,
    }


def validate_preview_for_materialization(
    preview_payload: Any,
    *,
    sandbox_root: str | Path,
    allow_overwrite: bool = False,
) -> dict[str, Any]:
    """Valida que un preview 7.2 sea apto para escritura sandbox 7.3."""
    if not isinstance(preview_payload, dict):
        return {"error": build_materialize_sandbox_error("PREVIEW_REQUIRED", "preview_payload requerido", field="preview_payload")}
    try:
        _reject_sensitive_keys(preview_payload)
        _ensure_json_safe(preview_payload)
    except ValueError as exc:
        return {"error": build_materialize_sandbox_error("SECRET_LIKE_FIELD_BLOCKED", str(exc), field="preview_payload", recoverable=False)}

    for field in ("writes_performed", "materialization_performed"):
        if preview_payload.get(field) is True:
            return {
                "error": build_materialize_sandbox_error(
                    "PREVIEW_ALREADY_MATERIALIZED",
                    f"preview_payload.{field} no puede ser true",
                    field=f"preview_payload.{field}",
                    recoverable=False,
                )
            }
    if preview_payload.get("operational") is True:
        return {"error": build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", "preview operational=true bloqueado", field="preview_payload.operational", recoverable=False)}
    if preview_payload.get("runtime_enabled") is True:
        return {"error": build_materialize_sandbox_error("RUNTIME_BLOCKED", "preview runtime_enabled=true bloqueado", field="preview_payload.runtime_enabled", recoverable=False)}
    if preview_payload.get("execution_enabled") is True:
        return {"error": build_materialize_sandbox_error("EXECUTION_BLOCKED", "preview execution_enabled=true bloqueado", field="preview_payload.execution_enabled", recoverable=False)}

    root = Path(sandbox_root).resolve()
    raw_path_error = _validate_planned_paths_against_root(
        preview_payload.get("planned_paths") or [],
        root=root,
        allow_overwrite=allow_overwrite,
    )
    if raw_path_error:
        return {"error": raw_path_error}

    try:
        validated = validate_materialization_preview_payload(preview_payload)
    except ValueError as exc:
        return {"error": build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", str(exc), field="preview_payload", recoverable=False)}

    if validated.get("status") == "blocked" or any(error.get("blocked") is True for error in validated.get("errors", [])):
        return {"error": build_materialize_sandbox_error("PREVIEW_HAS_BLOCKING_ERRORS", "preview_payload contiene errores bloqueantes", field="preview_payload.errors")}
    if validated.get("service") != "preview_materialization":
        return {"error": build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", "preview_payload.service invalido", field="preview_payload.service", recoverable=False)}
    for field in ("planned_artifacts", "planned_paths", "planned_manifests"):
        if not validated.get(field):
            return {"error": build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", f"preview_payload sin {field}", field=f"preview_payload.{field}", recoverable=False)}

    preview_root = str(validated.get("sandbox_root") or "").strip()
    if not preview_root:
        return {"error": build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", "preview_payload sin sandbox_root trazable", field="preview_payload.sandbox_root", recoverable=False)}
    if Path(preview_root).resolve() != root:
        return {"error": build_materialize_sandbox_error("UNSAFE_SANDBOX_ROOT", "preview_payload fue construido para otro sandbox_root", field="preview_payload.sandbox_root", recoverable=False)}

    path_error = _validate_planned_paths_against_root(
        validated["planned_paths"],
        root=root,
        allow_overwrite=allow_overwrite,
    )
    if path_error:
        return {"error": path_error}
    return {"preview_payload": validated}


def validate_materialize_sandbox_result(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida payload JSON-safe del servicio controlled-write."""
    if not isinstance(payload, dict):
        raise ValueError("materialize_sandbox result debe ser objeto")
    required = {
        "service",
        "service_version",
        "status",
        "readiness",
        "domain_id",
        "materialization_id",
        "sandbox_root",
        "created_paths",
        "artifact_manifest",
        "artifact_summary",
        "lineage_summary",
        "dependencies_summary",
        "read_models_summary",
        "rollback_prepared",
        "rollback_scope",
        "rollback_plan_available",
        "rollback_plan_summary",
        "warnings",
        "errors",
        "blocked_capabilities",
        "allowed_actions",
        "forbidden_actions",
        "validation",
        "operational",
        "passed",
        "runtime_enabled",
        "execution_enabled",
        "writes_performed",
        "materialization_performed",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"materialize_sandbox result incompleto: {', '.join(sorted(missing))}")
    if payload.get("service") != SERVICE_NAME:
        raise ValueError("service invalido")
    if payload.get("service_version") != SERVICE_VERSION:
        raise ValueError("service_version invalida")
    if payload.get("readiness") != SERVICE_READINESS:
        raise ValueError("readiness invalida")
    for field in ("created_paths", "warnings", "errors", "allowed_actions", "forbidden_actions"):
        if not isinstance(payload.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    for field in ("artifact_manifest", "artifact_summary", "lineage_summary", "dependencies_summary", "read_models_summary", "rollback_plan_summary", "blocked_capabilities", "validation"):
        if not isinstance(payload.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    if payload.get("operational") is not False:
        raise ValueError("operational debe ser false")
    if payload.get("passed") is not False:
        raise ValueError("passed debe ser false")
    if payload.get("runtime_enabled") is not False:
        raise ValueError("runtime_enabled debe ser false")
    if payload.get("execution_enabled") is not False:
        raise ValueError("execution_enabled debe ser false")
    if any(value is not False for value in payload["blocked_capabilities"].values()):
        raise ValueError("blocked_capabilities debe mantener todo false")
    _validate_actions(payload)
    _reject_sensitive_keys(payload)
    _reject_recursive_forbidden_true_flags(payload)
    dumped = _ensure_json_safe(payload)
    if len(dumped.encode("utf-8")) > MAX_RESULT_JSON_BYTES:
        raise ValueError("materialize_sandbox result excede tamano maximo")

    if payload["status"] == "materialized":
        if payload.get("writes_performed") is not True:
            raise ValueError("writes_performed debe ser true para status materialized")
        if payload.get("materialization_performed") is not True:
            raise ValueError("materialization_performed debe ser true para status materialized")
        if payload.get("rollback_prepared") is not True or payload.get("rollback_plan_available") is not True:
            raise ValueError("rollback debe quedar preparado")
        if not payload.get("domain_id") or not payload.get("materialization_id"):
            raise ValueError("materializacion requiere domain_id y materialization_id")
        if not payload.get("created_paths"):
            raise ValueError("materializacion requiere created_paths")
        if payload.get("errors"):
            raise ValueError("materializacion no puede contener errores")
    elif payload["status"] == "blocked":
        if payload.get("writes_performed") is not False:
            raise ValueError("blocked no puede declarar writes_performed=true")
        if payload.get("materialization_performed") is not False:
            raise ValueError("blocked no puede declarar materialization_performed=true")
    else:
        raise ValueError("status invalido")
    return deepcopy(payload)


def build_materialize_sandbox_error(
    error_code: str,
    message: str,
    *,
    severity: str = "error",
    field: str = "",
    recoverable: bool = True,
) -> dict[str, Any]:
    """Construye errores legibles para futura UI sin exponer datos sensibles."""
    if error_code not in ERROR_CODES:
        error_code = "MATERIALIZATION_FAILED"
    return {
        "error_code": error_code,
        "message": _safe_message(message),
        "severity": severity,
        "field": field,
        "recoverable": recoverable,
        "user_action": "revisar preview, confirmacion y sandbox_root indicados por backend",
        "developer_hint": "mantener materializacion limitada a sandbox controlado",
        "blocked": severity in {"error", "critical"},
    }


def _materialize_full_chain(
    *,
    preview_payload: dict[str, Any],
    sandbox_root: Path,
    confirmation: dict[str, Any],
    options: dict[str, bool],
) -> dict[str, Any]:
    from core.agent_preset_materializer import materialize_agent_presets
    from core.artifact_manifest_schema import validate_artifact_manifest_file
    from core.domain_materialization_rollback import (
        build_sandbox_domain_integral_rollback_plan,
        validate_sandbox_domain_integral_rollback_plan,
    )
    from core.domain_materializer import materialize_sandbox_domain
    from core.paper_seed_materializer import materialize_paper_seed
    from core.profile_catalog_materializer import materialize_profile_catalog
    from core.sandbox_agent_materializer import materialize_sandbox_agent
    from core.sandbox_team_materializer import materialize_sandbox_team
    from core.sandbox_team_read_model import list_sandbox_teams

    domain_schema = _domain_schema_from_preview(preview_payload)
    execution_metadata = {
        "backend_internal_service": SERVICE_NAME,
        "preview_id": preview_payload["domain_preview"]["preview_id"],
        "confirmation_id": confirmation["confirmation_id"],
        "confirmation_scope": confirmation["confirmation_scope"],
        "controlled_write": True,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }

    domain = materialize_sandbox_domain(
        domain_schema,
        sandbox_root=sandbox_root,
        execution_metadata=execution_metadata,
    )
    domain_dir = Path(domain["domain_dir"]).resolve()
    profile = materialize_profile_catalog(domain_dir, execution_metadata=execution_metadata)
    presets = materialize_agent_presets(domain_dir, execution_metadata=execution_metadata)
    paper_seed = materialize_paper_seed(domain_dir, execution_metadata=execution_metadata)

    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(
            domain_dir,
            preset_id=preset["preset_id"],
            execution_metadata=execution_metadata,
        )
        for preset in presets_payload.get("presets", [])
    ]
    agent_ids = [agent["agent_id"] for agent in agents]
    team = materialize_sandbox_team(
        domain_dir,
        team_id=f"{domain['domain_id']}_team",
        agent_ids=agent_ids,
        execution_metadata=execution_metadata,
    )

    read_model = list_sandbox_teams(domain_dir) if options["build_read_models"] else {"teams_count": 0, "teams": []}
    artifact_manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    rollback_plan = build_sandbox_domain_integral_rollback_plan(
        manifest_path=domain["manifest_path"],
        sandbox_root=sandbox_root,
    )
    rollback_plan = validate_sandbox_domain_integral_rollback_plan(rollback_plan)

    return {
        "domain": domain,
        "profile_catalog": profile,
        "agent_presets": presets,
        "paper_seed": paper_seed,
        "sandbox_agents": agents,
        "sandbox_team": team,
        "read_model": read_model,
        "artifact_manifest": artifact_manifest,
        "rollback_plan": rollback_plan,
    }


def _build_materialized_payload(
    *,
    preview_payload: dict[str, Any],
    sandbox_root: Path,
    confirmation: dict[str, Any],
    options: dict[str, bool],
    materialization: dict[str, Any],
    warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    domain = materialization["domain"]
    manifest = materialization["artifact_manifest"]
    rollback_plan = materialization["rollback_plan"]
    final_materialization_manifest = materialization["sandbox_team"]["materialization_manifest"]
    created_paths = _relative_created_paths(
        list(final_materialization_manifest.get("created_paths") or []),
        root=sandbox_root,
    )
    artifact_manifest = _sanitize_artifact_manifest(manifest, root=sandbox_root)
    artifacts = artifact_manifest.get("artifacts", [])
    result = {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "status": SERVICE_STATUS,
        "verdict": SERVICE_VERDICT,
        "controlled_write_verdict": SERVICE_CONTROLLED_WRITE_VERDICT,
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "domain_id": domain["domain_id"],
        "materialization_id": domain["materialization_id"],
        "sandbox_root": str(sandbox_root),
        "created_paths": created_paths,
        "artifact_manifest": artifact_manifest,
        "artifact_summary": _artifact_summary(artifacts),
        "lineage_summary": _lineage_summary(preview_payload, domain, artifacts),
        "dependencies_summary": _dependencies_summary(artifacts),
        "read_models_summary": _read_model_summary(materialization["read_model"]),
        "rollback_prepared": True,
        "rollback_scope": rollback_plan["rollback_scope"],
        "rollback_plan_available": True,
        "rollback_plan_summary": _rollback_plan_summary(rollback_plan),
        "warnings": warnings,
        "errors": [],
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": list(ALLOWED_ACTIONS),
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "next_actions": ["request_validation_next_step"],
        "validation": {
            "preview_valid": True,
            "confirmation_explicit": True,
            "sandbox_root_explicit": True,
            "sandbox_root_controlled": True,
            "planned_paths_safe": True,
            "artifact_manifest_valid": True,
            "rollback_plan_valid": True,
            "read_models_built": options["build_read_models"],
            "json_safe": True,
            "controlled_write": True,
            "writes_limited_to_sandbox_root": True,
            "domains_operational_untouched": True,
            "no_runtime": True,
            "no_execution": True,
            "no_tools_or_models": True,
            "no_integrations": True,
        },
        "confirmation_summary": {
            "confirmed": confirmation["confirmed"],
            "confirmation_scope": confirmation["confirmation_scope"],
            "human_confirmation_required": confirmation["human_confirmation_required"],
            "confirmed_by": confirmation["confirmed_by"],
            "confirmation_id": confirmation["confirmation_id"],
        },
        "materialization_options": deepcopy(options),
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "writes_performed": True,
        "materialization_performed": True,
    }
    return result


def _blocked_payload(
    *,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "status": "blocked",
        "verdict": "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_BLOCKED",
        "controlled_write_verdict": SERVICE_CONTROLLED_WRITE_VERDICT,
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "domain_id": "",
        "materialization_id": "",
        "sandbox_root": "",
        "created_paths": [],
        "artifact_manifest": {},
        "artifact_summary": {},
        "lineage_summary": {},
        "dependencies_summary": {},
        "read_models_summary": {},
        "rollback_prepared": False,
        "rollback_scope": "sandbox_domain_integral",
        "rollback_plan_available": False,
        "rollback_plan_summary": {},
        "warnings": warnings,
        "errors": errors,
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": ["view_status"],
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "next_actions": ["review_materialization_errors"],
        "validation": {
            "preview_valid": False,
            "confirmation_explicit": False,
            "sandbox_root_explicit": False,
            "sandbox_root_controlled": False,
            "planned_paths_safe": False,
            "artifact_manifest_valid": False,
            "rollback_plan_valid": False,
            "read_models_built": False,
            "json_safe": True,
            "controlled_write": False,
            "writes_limited_to_sandbox_root": False,
            "domains_operational_untouched": True,
            "no_runtime": True,
            "no_execution": True,
            "no_tools_or_models": True,
            "no_integrations": True,
        },
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "writes_performed": False,
        "materialization_performed": False,
    }


def _domain_schema_from_preview(preview_payload: dict[str, Any]) -> dict[str, Any]:
    domain_request = deepcopy(preview_payload.get("domain_request") or {})
    domain_preview = preview_payload["domain_preview"]
    domain_id = domain_preview["domain_id"]
    now = _now()
    source_request = {
        "area_id": domain_request.get("area_id") or preview_payload.get("planned_lineage", {}).get("source_request", {}).get("area_id"),
        "niche_ids": list(domain_request.get("niche_ids") or preview_payload.get("planned_lineage", {}).get("source_request", {}).get("niche_ids") or []),
        "objective": domain_request.get("objective") or preview_payload.get("planned_lineage", {}).get("source_request", {}).get("objective"),
        "business_scale": domain_request.get("business_scale"),
        "complexity_level": domain_request.get("complexity_level"),
        "max_profiles": domain_request.get("max_profiles"),
        "max_presets": domain_request.get("max_presets"),
    }
    return {
        "schema_version": "1.0",
        "domain_id": domain_id,
        "name": domain_request.get("domain_name") or domain_preview.get("domain_name") or domain_id.replace("_", " ").title(),
        "description": domain_request.get("domain_description") or domain_preview.get("domain_description") or "Dominio sandbox materializado por backend interno.",
        "status": "materialized",
        "domain_type": "sandbox",
        "source_request": {key: value for key, value in source_request.items() if value not in (None, "", [])},
        "created_from": {
            "type": "preview",
            "preview_id": domain_preview["preview_id"],
            "artifact_state": domain_preview.get("artifact_state", "derived_preview"),
            "service": "preview_materialization",
        },
        "materialization_id": f"mat_pending_{_safe_id(domain_id)}",
        "materialization_status": "preview_confirmed",
        "artifact_state": "materialized",
        "created_at": now,
        "updated_at": now,
        "human_review_required": True,
        "rollback_manifest": {
            "can_rollback": True,
            "created_paths": [],
            "modified_paths": [],
            "backup_paths": [],
            "notes": ["materialize_sandbox 7.3 prepara rollback integral; no activa runtime."],
        },
        "validation": {
            "schema": "sandbox_domain_schema",
            "schema_version": "1.0",
            "validated": True,
            "passed": False,
            "rules": ["preview_required", "explicit_confirmation", "safe_sandbox_root"],
        },
        "warnings": [],
        "metadata": {
            "backend_internal_service": SERVICE_NAME,
            "operational": False,
            "runtime_enabled": False,
            "execution_enabled": False,
        },
    }


def _materialization_options(raw: Any) -> dict[str, bool]:
    source = raw if isinstance(raw, dict) else {}
    return {
        "prepare_rollback": source.get("prepare_rollback") is not False,
        "build_read_models": source.get("build_read_models") is not False,
        "build_audit_pack_if_supported": source.get("build_audit_pack_if_supported") is True,
        "allow_overwrite": source.get("allow_overwrite") is True,
    }


def _validate_confirmation(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict) or not raw:
        return {"error": build_materialize_sandbox_error("CONFIRMATION_REQUIRED", "confirmacion explicita requerida", field="confirmation")}
    if raw.get("confirmed") is not True:
        return {"error": build_materialize_sandbox_error("CONFIRMATION_REQUIRED", "confirmation.confirmed debe ser true", field="confirmation.confirmed")}
    if raw.get("confirmation_scope") != SERVICE_NAME:
        return {"error": build_materialize_sandbox_error("INVALID_CONFIRMATION_SCOPE", "confirmation_scope debe ser materialize_sandbox", field="confirmation.confirmation_scope", recoverable=False)}
    if raw.get("human_confirmation_required") is not True:
        return {"error": build_materialize_sandbox_error("CONFIRMATION_REQUIRED", "human_confirmation_required debe ser true", field="confirmation.human_confirmation_required")}
    confirmed_by = str(raw.get("confirmed_by") or "").strip()
    confirmation_id = str(raw.get("confirmation_id") or "").strip()
    if not confirmed_by or not confirmation_id:
        return {"error": build_materialize_sandbox_error("CONFIRMATION_REQUIRED", "confirmed_by y confirmation_id requeridos", field="confirmation")}
    return {
        "confirmation": {
            "confirmed": True,
            "confirmation_scope": SERVICE_NAME,
            "human_confirmation_required": True,
            "confirmed_by": _safe_text(confirmed_by),
            "confirmation_id": _safe_id(confirmation_id),
        }
    }


def _resolve_sandbox_root(raw: Any) -> dict[str, Any]:
    if raw in (None, ""):
        return {"error": build_materialize_sandbox_error("SANDBOX_ROOT_REQUIRED", "sandbox_root explicito requerido", field="sandbox_root")}
    text = str(raw)
    if any(part == ".." for part in Path(text).parts):
        return {"error": build_materialize_sandbox_error("PATH_TRAVERSAL_BLOCKED", "sandbox_root contiene path traversal", field="sandbox_root", recoverable=False)}
    root = Path(text).resolve()
    reason = _unsafe_root_reason(root)
    if reason:
        return {"error": build_materialize_sandbox_error("UNSAFE_SANDBOX_ROOT", reason, field="sandbox_root", recoverable=False)}
    if not root.exists() or not root.is_dir():
        return {"error": build_materialize_sandbox_error("SANDBOX_ROOT_NOT_FOUND", "sandbox_root no existe o no es directorio", field="sandbox_root")}
    return {"root": root}


def _unsafe_root_reason(root: Path) -> str | None:
    repo_root = Path(__file__).resolve().parents[1]
    domains_root = (repo_root / "domains").resolve()
    forbidden_roots = [
        repo_root,
        domains_root,
        repo_root / ".git",
        repo_root / "core",
        repo_root / "docs",
        repo_root / "tests",
        repo_root / "agents",
        repo_root / "memory",
        repo_root / "memoria_agentes",
    ]
    for forbidden in forbidden_roots:
        forbidden = forbidden.resolve()
        if root == forbidden or forbidden in root.parents:
            if forbidden == domains_root:
                return "sandbox_root no puede apuntar a domains/ operativo"
            return "sandbox_root no puede apuntar al repo o zonas internas no sandbox"
    return None


def _validate_planned_paths_against_root(
    paths: list[dict[str, Any]],
    *,
    root: Path,
    allow_overwrite: bool,
) -> dict[str, Any] | None:
    if not isinstance(paths, list) or not paths:
        return build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", "planned_paths requerido", field="preview_payload.planned_paths", recoverable=False)
    domains_root = (Path(__file__).resolve().parents[1] / "domains").resolve()
    forbidden_repo_parts = {".git", "core", "docs", "tests"}
    for item in paths:
        relative = str(item.get("relative_path") or "")
        if not relative:
            return build_materialize_sandbox_error("UNSAFE_PLANNED_PATH", "planned_path sin relative_path", field="preview_payload.planned_paths", recoverable=False)
        if any(part == ".." for part in Path(relative).parts):
            return build_materialize_sandbox_error("PATH_TRAVERSAL_BLOCKED", "planned_path contiene traversal", field="preview_payload.planned_paths", recoverable=False)
        if Path(relative).is_absolute() or re.match(r"^[a-zA-Z]:", relative):
            return build_materialize_sandbox_error("UNSAFE_PLANNED_PATH", "planned_path no debe ser absoluto", field="preview_payload.planned_paths", recoverable=False)
        if relative.replace("\\", "/").startswith("domains/"):
            return build_materialize_sandbox_error("DOMAINS_OPERATIVE_PATH_BLOCKED", "planned_path apunta a domains operativo", field="preview_payload.planned_paths", recoverable=False)
        target = (root / relative).resolve()
        if target != root and root not in target.parents:
            return build_materialize_sandbox_error("UNSAFE_PLANNED_PATH", "planned_path escapa del sandbox_root", field="preview_payload.planned_paths", recoverable=False)
        if target == domains_root or domains_root in target.parents:
            return build_materialize_sandbox_error("DOMAINS_OPERATIVE_PATH_BLOCKED", "planned_path apunta a domains operativo", field="preview_payload.planned_paths", recoverable=False)
        if set(target.parts) & forbidden_repo_parts and Path(__file__).resolve().parents[1] in target.parents:
            return build_materialize_sandbox_error("UNSAFE_PLANNED_PATH", "planned_path apunta a zona interna del repo", field="preview_payload.planned_paths", recoverable=False)
        if target.exists() and not allow_overwrite:
            return build_materialize_sandbox_error("OVERWRITE_BLOCKED", "planned_path ya existe y allow_overwrite=false", field="preview_payload.planned_paths", recoverable=False)
    return None


def _sanitize_artifact_manifest(manifest: dict[str, Any], *, root: Path) -> dict[str, Any]:
    sanitized = deepcopy(manifest)
    for artifact in sanitized.get("artifacts", []):
        rollback = artifact.get("rollback_info") or {}
        rollback["created_paths"] = _relative_created_paths(rollback.get("created_paths") or [], root=root)
        artifact["rollback_info"] = rollback
    return sanitized


def _relative_created_paths(paths: list[Any], *, root: Path) -> list[str]:
    relatives = []
    for raw_path in paths:
        path = Path(str(raw_path)).resolve()
        if path == root or root in path.parents:
            relatives.append(path.relative_to(root).as_posix())
    return list(dict.fromkeys(relatives))


def _artifact_summary(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    types = [artifact.get("artifact_type") for artifact in artifacts]
    kinds = [artifact.get("created_from", {}).get("artifact_kind") or artifact.get("artifact_type") for artifact in artifacts]
    return {
        "artifact_count": len(artifacts),
        "artifact_ids": [artifact.get("artifact_id") for artifact in artifacts],
        "artifact_types": types,
        "artifact_kinds": kinds,
        "non_operational": all(artifact.get("operational") is False for artifact in artifacts),
        "passed_false": all(artifact.get("passed") is False for artifact in artifacts),
    }


def _lineage_summary(
    preview_payload: dict[str, Any],
    domain: dict[str, Any],
    artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "preview_id": preview_payload["domain_preview"]["preview_id"],
        "domain_id": domain["domain_id"],
        "materialization_id": domain["materialization_id"],
        "source": preview_payload["domain_preview"].get("source"),
        "artifact_lineage_count": sum(1 for artifact in artifacts if artifact.get("created_from")),
        "lineage_traced": True,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _dependencies_summary(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "dependency_sets_count": len([artifact for artifact in artifacts if artifact.get("dependencies")]),
        "dependencies": [
            {
                "artifact_id": artifact.get("artifact_id"),
                "depends_on": list(artifact.get("dependencies") or []),
            }
            for artifact in artifacts
        ],
        "dependencies_declared": True,
    }


def _read_model_summary(read_model: dict[str, Any]) -> dict[str, Any]:
    return {
        "read_model": read_model.get("read_model", "sandbox_team_internal_listing"),
        "status": read_model.get("status", "listed"),
        "verdict": read_model.get("verdict"),
        "readiness": read_model.get("readiness"),
        "teams_count": read_model.get("teams_count", 0),
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "built": True,
    }


def _rollback_plan_summary(plan: dict[str, Any]) -> dict[str, Any]:
    path_names = sorted({Path(path).name for path in plan.get("planned_paths", []) if Path(path).name})
    return {
        "rollback_id": plan.get("rollback_id"),
        "rollback_scope": plan.get("rollback_scope"),
        "planned_paths_count": len(plan.get("planned_paths") or []),
        "path_names": path_names,
        "blocked_paths_count": len(plan.get("blocked_paths") or []),
        "idempotent": plan.get("idempotent") is True,
        "all_paths_inside_sandbox_root": plan.get("validation", {}).get("all_paths_inside_sandbox_root") is True,
        "operational_domains_blocked": plan.get("validation", {}).get("operational_domains_blocked") is True,
        "repo_roots_blocked": plan.get("validation", {}).get("repo_roots_blocked") is True,
    }


def _validate_actions(payload: dict[str, Any]) -> None:
    prohibited_allowed = {
        "execute",
        "activate_runtime",
        "execute_agents",
        "invoke_models",
        "call_tools",
        "delete_without_confirmation",
        "rollback_without_confirmation",
        "regenerate_without_rollback",
    }
    if any(action in prohibited_allowed for action in payload["allowed_actions"]):
        raise ValueError("allowed_actions contiene accion prohibida")
    if not set(FORBIDDEN_ACTIONS) <= set(payload["forbidden_actions"]):
        raise ValueError("forbidden_actions incompleto")


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


def _reject_recursive_forbidden_true_flags(value: Any, path: str = "") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_OPERATIONAL_TRUE_KEYS and nested is True:
                raise ValueError(f"{path + '.' if path else ''}{key} debe ser false")
            _reject_recursive_forbidden_true_flags(nested, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _reject_recursive_forbidden_true_flags(nested, f"{path}[{index}]")


def _ensure_json_safe(payload: Any) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("payload no es JSON-safe") from exc


def _error_from_exception(exc: ValueError) -> dict[str, Any]:
    message = str(exc)
    lowered = message.lower()
    if "artifact_manifest" in lowered:
        return build_materialize_sandbox_error("ARTIFACT_MANIFEST_WRITE_FAILED", message, recoverable=False)
    if "rollback" in lowered:
        return build_materialize_sandbox_error("ROLLBACK_PREPARATION_FAILED", message, recoverable=False)
    if "domains/" in lowered or "domains operativo" in lowered:
        return build_materialize_sandbox_error("DOMAINS_OPERATIVE_PATH_BLOCKED", message, recoverable=False)
    if "runtime" in lowered:
        return build_materialize_sandbox_error("RUNTIME_BLOCKED", message, recoverable=False)
    if "execution" in lowered or "ejecucion" in lowered:
        return build_materialize_sandbox_error("EXECUTION_BLOCKED", message, recoverable=False)
    return build_materialize_sandbox_error("MATERIALIZATION_FAILED", message, recoverable=False)


def _safe_message(message: str) -> str:
    text = str(message).replace("\\", "/")
    repo_root = str(Path(__file__).resolve().parents[1]).replace("\\", "/")
    if repo_root in text:
        text = text.replace(repo_root, "<repo>")
    return _safe_text(text)


def _safe_text(value: str) -> str:
    return re.sub(r"[\r\n\t]+", " ", str(value)).strip()


def _safe_id(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(value)).strip("_").lower()
    return safe or "manual"


def _now() -> str:
    return datetime.now().isoformat()
