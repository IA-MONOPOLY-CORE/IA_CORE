"""Servicio interno validate_domain read-only para futura UI.

El servicio valida una materializacion sandbox existente sin escribir,
reparar, regenerar, ejecutar rollback ni activar runtime.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.agent_preset_materializer import validate_materialized_agent_presets
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.backend_internal_ui_contract import build_backend_internal_ui_forbidden_capabilities
from core.domain_materialization_rollback import (
    build_sandbox_domain_integral_rollback_plan,
    validate_sandbox_domain_integral_rollback_plan,
)
from core.domain_materializer import MATERIALIZATION_MANIFEST, validate_materialized_sandbox_domain
from core.paper_seed_materializer import validate_materialized_paper_seed
from core.profile_catalog_materializer import validate_materialized_profile_catalog
from core.sandbox_agent_materializer import validate_materialized_sandbox_agent
from core.sandbox_team_materializer import validate_materialized_sandbox_team
from core.sandbox_team_read_model import list_sandbox_teams, validate_sandbox_team_read_model


SERVICE_NAME = "validate_domain"
SERVICE_VERSION = "0.1"
SERVICE_STATUS = "validated"
SERVICE_VERDICT = "BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_READY"
SERVICE_READ_ONLY_VERDICT = "BACKEND_INTERNAL_VALIDATE_DOMAIN_READ_ONLY_CONFIRMED"
SERVICE_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_VALIDATE_DOMAIN_NO_OPERATIONAL_CONFIRMED"
SERVICE_READINESS = "ready_for_phase_7_5_rollback_archive_delete_reset_service"
VALIDATION_SCOPE = "sandbox_domain_materialization"
MAX_PAYLOAD_JSON_BYTES = 128_000

ALLOWED_ACTIONS = (
    "view_validation_report",
    "view_status",
    "view_details",
    "view_audit_pack_summary",
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
FORBIDDEN_TRUE_KEYS = {
    "operational",
    "runtime_enabled",
    "execution_enabled",
    "dry_run_real_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "external_integrations_enabled",
    "can_execute",
    "can_call_tools",
    "can_call_models",
    "can_write_outputs",
    "can_access_network",
    "can_use_integrations",
    "writes_performed",
    "materialization_performed",
    "rollback_performed",
    "regeneration_performed",
}


def validate_domain(request: dict[str, Any] | None) -> dict[str, Any]:
    """Valida una materializacion sandbox existente sin mutar archivos."""
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if not isinstance(request, dict):
        errors.append(build_validate_domain_error("VALIDATION_REQUEST_REQUIRED", "request requerido"))
        return validate_domain_validation_payload(_blocked_payload(errors=errors, warnings=warnings))

    try:
        validated_request = validate_validate_domain_request(request)
    except ValueError as exc:
        errors.append(_error_from_exception(exc))
        return validate_domain_validation_payload(_blocked_payload(errors=errors, warnings=warnings))

    sandbox_root = Path(validated_request["sandbox_root"]).resolve()
    domain_id = validated_request["domain_id"]
    materialization_id = validated_request.get("materialization_id") or ""
    options = validated_request["validation_options"]
    domain_dir = _safe_child(sandbox_root, domain_id)
    if not domain_dir.is_dir():
        errors.append(build_validate_domain_error("DOMAIN_NOT_FOUND", "dominio sandbox no encontrado", field="domain_id"))
        return validate_domain_validation_payload(
            _result_payload(
                sandbox_root=sandbox_root,
                domain_id=domain_id,
                materialization_id=materialization_id,
                valid=False,
                errors=errors,
                warnings=warnings,
            )
        )

    result = _validate_materialized_domain(
        sandbox_root=sandbox_root,
        domain_dir=domain_dir,
        domain_id=domain_id,
        materialization_id=materialization_id,
        options=options,
        errors=errors,
        warnings=warnings,
    )
    result_materialization_id = result.pop("materialization_id", "") or materialization_id
    payload = _result_payload(
        sandbox_root=sandbox_root,
        domain_id=domain_id,
        materialization_id=result_materialization_id,
        valid=not errors,
        errors=errors,
        warnings=warnings,
        **result,
    )
    return validate_domain_validation_payload(payload)


def build_validate_domain_request(
    *,
    sandbox_root: str | Path,
    domain_id: str,
    materialization_id: str | None = None,
    validation_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construye una request JSON-safe para validate_domain."""
    request = {
        "sandbox_root": str(sandbox_root),
        "domain_id": domain_id,
        "materialization_id": materialization_id or "",
        "validation_options": {
            "include_artifact_manifest": True,
            "include_lineage": True,
            "include_created_paths": True,
            "include_read_models": True,
            "include_rollback_readiness": True,
            "include_audit_pack": True,
            "strict": True,
            **(validation_options or {}),
        },
    }
    _reject_sensitive_keys(request)
    _ensure_json_safe(request)
    return request


def validate_validate_domain_request(request: dict[str, Any]) -> dict[str, Any]:
    """Valida la request de validate_domain sin leer artefactos de dominio."""
    if not isinstance(request, dict):
        raise ValueError("VALIDATION_REQUEST_REQUIRED: request debe ser objeto")
    _reject_sensitive_keys(request)
    _ensure_json_safe(request)
    root = _resolve_sandbox_root(request.get("sandbox_root"))
    domain_id = _validate_domain_id(request.get("domain_id"))
    materialization_id = str(request.get("materialization_id") or "").strip()
    if materialization_id and any(part == ".." for part in Path(materialization_id).parts):
        raise ValueError("INVALID_VALIDATE_DOMAIN_REQUEST: materialization_id inseguro")
    options = _validation_options(request.get("validation_options"))
    return {
        "sandbox_root": str(root),
        "domain_id": domain_id,
        "materialization_id": _safe_text(materialization_id),
        "validation_options": options,
    }


def validate_domain_validation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida el payload de salida read-only y JSON-safe."""
    if not isinstance(payload, dict):
        raise ValueError("validate_domain payload debe ser objeto")
    required = {
        "service",
        "service_version",
        "status",
        "readiness",
        "domain_id",
        "materialization_id",
        "validation_scope",
        "domain_validation",
        "artifact_manifest_validation",
        "created_paths_validation",
        "lineage_validation",
        "artifact_validations",
        "read_models_validation",
        "rollback_readiness",
        "audit_pack_validation",
        "warnings",
        "errors",
        "blocked_capabilities",
        "allowed_actions",
        "forbidden_actions",
        "validation",
        "valid",
        "operational",
        "passed",
        "runtime_enabled",
        "execution_enabled",
        "writes_performed",
        "materialization_performed",
        "rollback_performed",
        "regeneration_performed",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"validate_domain payload incompleto: {', '.join(sorted(missing))}")
    if payload.get("service") != SERVICE_NAME:
        raise ValueError("service invalido")
    if payload.get("service_version") != SERVICE_VERSION:
        raise ValueError("service_version invalida")
    if payload.get("readiness") != SERVICE_READINESS:
        raise ValueError("readiness invalida")
    if payload.get("validation_scope") != VALIDATION_SCOPE:
        raise ValueError("validation_scope invalido")
    if payload.get("operational") is not False:
        raise ValueError("operational debe ser false")
    if payload.get("passed") is not False:
        raise ValueError("passed debe ser false")
    for field in (
        "runtime_enabled",
        "execution_enabled",
        "writes_performed",
        "materialization_performed",
        "rollback_performed",
        "regeneration_performed",
    ):
        if payload.get(field) is not False:
            raise ValueError(f"{field} debe ser false")
    if payload.get("valid") is True and payload.get("errors"):
        raise ValueError("valid=true no puede incluir errores")
    _validate_actions(payload)
    _reject_sensitive_keys(payload)
    _reject_forbidden_true_flags(payload)
    encoded = _ensure_json_safe(payload)
    if len(encoded.encode("utf-8")) > MAX_PAYLOAD_JSON_BYTES:
        raise ValueError("validate_domain payload excede tamano maximo")
    return deepcopy(payload)


def build_validate_domain_error(
    error_code: str,
    message: str,
    *,
    field: str = "",
    severity: str = "error",
    recoverable: bool = True,
    blocked: bool = True,
) -> dict[str, Any]:
    """Construye un error seguro para futura UI."""
    code = error_code if error_code in ERROR_CODES else "INVALID_VALIDATE_DOMAIN_REQUEST"
    return {
        "error_code": code,
        "message": _safe_text(message),
        "severity": severity if severity in {"info", "warning", "error", "critical"} else "error",
        "field": _safe_text(field),
        "recoverable": bool(recoverable),
        "user_action": _user_action_for(code),
        "developer_hint": _developer_hint_for(code),
        "blocked": bool(blocked),
    }


def _validate_materialized_domain(
    *,
    sandbox_root: Path,
    domain_dir: Path,
    domain_id: str,
    materialization_id: str,
    options: dict[str, bool],
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    domain_validation: dict[str, Any] = {
        "domain_exists": domain_dir.is_dir(),
        "schema_valid": False,
        "domain_id_matches": False,
        "materialization_id_matches": materialization_id == "",
        "status_allowed": False,
        "artifact_state_allowed": False,
        "non_operational_confirmed": False,
    }
    artifact_manifest_validation: dict[str, Any] = {
        "present": False,
        "json_safe": False,
        "domain_id_matches": False,
        "materialization_id_matches": materialization_id == "",
        "artifact_count": 0,
        "artifact_ids": [],
        "artifact_types": [],
        "artifacts_coherent": False,
    }
    created_paths_validation: dict[str, Any] = {
        "present": False,
        "paths_count": 0,
        "all_paths_inside_sandbox_root": False,
        "operational_domains_blocked": True,
        "repo_roots_blocked": True,
        "unsafe_paths": [],
    }
    lineage_validation: dict[str, Any] = {
        "created_from_present": False,
        "lineage_entries_count": 0,
        "dependencies_declared": False,
        "dependencies_coherent": False,
    }
    artifact_validations: list[dict[str, Any]] = []
    read_models_validation: dict[str, Any] = {
        "included": bool(options["include_read_models"]),
        "valid": False,
        "teams_count": 0,
        "json_safe": False,
        "non_operational_confirmed": False,
    }
    rollback_readiness: dict[str, Any] = {
        "included": bool(options["include_rollback_readiness"]),
        "ready": False,
        "rollback_scope": "sandbox_domain_integral",
        "rollback_plan_available": False,
        "requires_future_confirmation": True,
        "executed": False,
        "planned_paths_count": 0,
        "all_paths_inside_sandbox_root": False,
    }
    audit_pack_validation: dict[str, Any] = {
        "included": bool(options["include_audit_pack"]),
        "present": False,
        "valid": False,
        "optional": True,
    }

    materialization_manifest: dict[str, Any] = {}
    artifact_manifest: dict[str, Any] = {}
    try:
        base = validate_materialized_sandbox_domain(domain_dir)
        domain = base["domain"]
        materialization_manifest = base["manifest"]
        actual_materialization_id = domain.get("materialization_id") or materialization_manifest.get("materialization_id") or ""
        domain_validation.update(
            {
                "schema_valid": True,
                "domain_id_matches": domain.get("domain_id") == domain_id,
                "materialization_id_matches": not materialization_id or actual_materialization_id == materialization_id,
                "status_allowed": domain.get("status") != "active",
                "artifact_state_allowed": domain.get("artifact_state") != "active",
                "non_operational_confirmed": _non_operational_domain(domain),
            }
        )
        if not domain_validation["domain_id_matches"]:
            errors.append(build_validate_domain_error("DOMAIN_ID_MISMATCH", "domain_id no coincide", field="domain_id"))
        if not domain_validation["materialization_id_matches"]:
            errors.append(
                build_validate_domain_error(
                    "DOMAIN_ID_MISMATCH",
                    "materialization_id no coincide",
                    field="materialization_id",
                )
            )
        if not domain_validation["non_operational_confirmed"]:
            errors.append(build_validate_domain_error("RUNTIME_BLOCKED", "dominio declara capacidades operativas", recoverable=False))
    except FileNotFoundError as exc:
        errors.append(build_validate_domain_error("DOMAIN_NOT_FOUND", str(exc), field="domain_id"))
        return _validation_result(
            materialization_id=materialization_id,
            domain_validation=domain_validation,
            artifact_manifest_validation=artifact_manifest_validation,
            created_paths_validation=created_paths_validation,
            lineage_validation=lineage_validation,
            artifact_validations=artifact_validations,
            read_models_validation=read_models_validation,
            rollback_readiness=rollback_readiness,
            audit_pack_validation=audit_pack_validation,
        )
    except ValueError as exc:
        errors.append(build_validate_domain_error("INVALID_DOMAIN_SCHEMA", str(exc), field="domain"))

    manifest_path = _safe_child(domain_dir, MATERIALIZATION_MANIFEST)
    artifact_manifest_path = _safe_child(domain_dir, Path("manifests") / "artifact_manifest.json")
    if options["include_artifact_manifest"]:
        try:
            artifact_manifest = validate_artifact_manifest_file(artifact_manifest_path)
            artifact_ids = [artifact["artifact_id"] for artifact in artifact_manifest.get("artifacts", [])]
            artifact_manifest_validation.update(
                {
                    "present": True,
                    "json_safe": True,
                    "domain_id_matches": artifact_manifest.get("domain_id") == domain_id,
                    "materialization_id_matches": _artifact_manifest_matches_materialization(
                        artifact_manifest,
                        materialization_manifest.get("materialization_id") or materialization_id,
                    ),
                    "artifact_count": len(artifact_manifest.get("artifacts") or []),
                    "artifact_ids": artifact_ids,
                    "artifact_types": [artifact.get("artifact_type") for artifact in artifact_manifest.get("artifacts") or []],
                    "artifacts_coherent": True,
                }
            )
            if not artifact_manifest_validation["domain_id_matches"]:
                errors.append(build_validate_domain_error("INCONSISTENT_ARTIFACT_MANIFEST", "artifact_manifest no coincide con domain_id"))
            if not artifact_manifest_validation["materialization_id_matches"]:
                errors.append(build_validate_domain_error("INCONSISTENT_ARTIFACT_MANIFEST", "artifact_manifest no coincide con materialization_id"))
        except FileNotFoundError:
            errors.append(build_validate_domain_error("MISSING_ARTIFACT_MANIFEST", "artifact_manifest no encontrado"))
        except ValueError as exc:
            errors.append(build_validate_domain_error("INCONSISTENT_ARTIFACT_MANIFEST", str(exc)))

    if options["include_created_paths"]:
        created_paths = list(materialization_manifest.get("created_paths") or [])
        created_paths_validation["present"] = bool(created_paths)
        created_paths_validation["paths_count"] = len(created_paths)
        unsafe = _unsafe_created_paths(created_paths, sandbox_root=sandbox_root)
        created_paths_validation["unsafe_paths"] = unsafe
        created_paths_validation["all_paths_inside_sandbox_root"] = not unsafe and bool(created_paths)
        if not created_paths:
            errors.append(build_validate_domain_error("MISSING_CREATED_PATHS", "materialization_manifest sin created_paths"))
        if unsafe:
            errors.append(build_validate_domain_error("UNSAFE_CREATED_PATH", "created_paths contiene rutas inseguras", recoverable=False))

    if options["include_lineage"] and artifact_manifest:
        dependencies = _dependency_pairs(artifact_manifest)
        lineage_validation.update(
            {
                "created_from_present": all(bool(artifact.get("created_from")) for artifact in artifact_manifest.get("artifacts") or []),
                "lineage_entries_count": sum(1 for artifact in artifact_manifest.get("artifacts") or [] if artifact.get("created_from")),
                "dependencies_declared": bool(dependencies),
                "dependencies_coherent": _dependencies_coherent(artifact_manifest),
                "dependencies": dependencies,
            }
        )
        if not lineage_validation["created_from_present"] or not lineage_validation["dependencies_coherent"]:
            errors.append(build_validate_domain_error("INCONSISTENT_ARTIFACT_MANIFEST", "lineage/dependencies inconsistentes"))

    artifact_validations.extend(_validate_expected_artifacts(domain_dir, artifact_manifest, errors=errors))

    if options["include_read_models"]:
        try:
            read_model = list_sandbox_teams(domain_dir)
            for team in read_model.get("teams") or []:
                validate_sandbox_team_read_model(team)
            read_models_validation.update(
                {
                    "valid": True,
                    "teams_count": read_model.get("teams_count", 0),
                    "json_safe": True,
                    "non_operational_confirmed": read_model.get("operational") is False and read_model.get("passed") is False,
                    "read_model": read_model.get("read_model"),
                    "verdict": read_model.get("verdict"),
                    "readiness": read_model.get("readiness"),
                }
            )
            if not read_models_validation["non_operational_confirmed"]:
                errors.append(build_validate_domain_error("INVALID_READ_MODEL", "read model declara operacion real", recoverable=False))
        except (OSError, ValueError) as exc:
            errors.append(build_validate_domain_error("INVALID_READ_MODEL", str(exc)))

    if options["include_rollback_readiness"] and manifest_path.is_file():
        try:
            plan = build_sandbox_domain_integral_rollback_plan(
                manifest_path=manifest_path,
                sandbox_root=sandbox_root,
            )
            plan = validate_sandbox_domain_integral_rollback_plan(plan)
            rollback_readiness.update(
                {
                    "ready": True,
                    "rollback_scope": plan.get("rollback_scope"),
                    "rollback_plan_available": True,
                    "planned_paths_count": len(plan.get("planned_paths") or []),
                    "all_paths_inside_sandbox_root": plan.get("validation", {}).get("all_paths_inside_sandbox_root") is True,
                    "operational_domains_blocked": plan.get("validation", {}).get("operational_domains_blocked") is True,
                    "repo_roots_blocked": plan.get("validation", {}).get("repo_roots_blocked") is True,
                }
            )
        except (OSError, ValueError) as exc:
            errors.append(build_validate_domain_error("ROLLBACK_NOT_READY", str(exc)))

    audit_pack_path = _safe_child(domain_dir, Path("audit_pack") / "materialization_audit_pack.json")
    if options["include_audit_pack"]:
        audit_pack_validation["present"] = audit_pack_path.is_file()
        if audit_pack_path.is_file():
            try:
                audit_pack = json.loads(audit_pack_path.read_text(encoding="utf-8"))
                _ensure_json_safe(audit_pack)
                audit_pack_validation["valid"] = isinstance(audit_pack, dict)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                errors.append(build_validate_domain_error("INVALID_AUDIT_PACK", str(exc)))
        else:
            warnings.append(
                build_validate_domain_error(
                    "INVALID_AUDIT_PACK",
                    "audit pack no existe; es opcional para validate_domain 7.4",
                    severity="warning",
                    blocked=False,
                )
            )

    return _validation_result(
        materialization_id=materialization_manifest.get("materialization_id") or materialization_id,
        domain_validation=domain_validation,
        artifact_manifest_validation=artifact_manifest_validation,
        created_paths_validation=created_paths_validation,
        lineage_validation=lineage_validation,
        artifact_validations=artifact_validations,
        read_models_validation=read_models_validation,
        rollback_readiness=rollback_readiness,
        audit_pack_validation=audit_pack_validation,
    )


def _validate_expected_artifacts(
    domain_dir: Path,
    artifact_manifest: dict[str, Any],
    *,
    errors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    validators = (
        ("profile_catalog", "profile_catalog_main", validate_materialized_profile_catalog),
        ("agent_presets", "agent_presets_main", validate_materialized_agent_presets),
        ("paper_seed", "paper_seed_main", validate_materialized_paper_seed),
    )
    for artifact_kind, artifact_id, validator in validators:
        validations.append(_artifact_validation_entry(domain_dir, artifact_kind, artifact_id, validator, errors))

    agent_files = sorted((domain_dir / "sandbox_agents").glob("*.json")) if (domain_dir / "sandbox_agents").is_dir() else []
    if not agent_files:
        errors.append(build_validate_domain_error("MISSING_EXPECTED_ARTIFACT", "sandbox_agents no encontrado", field="sandbox_agents"))
        validations.append({"artifact_kind": "sandbox_agents", "present": False, "valid": False, "count": 0})
    else:
        valid_agents = 0
        for path in agent_files:
            if path.parent.name == "history":
                continue
            try:
                validate_materialized_sandbox_agent(domain_dir, agent_id=path.stem)
                valid_agents += 1
            except (OSError, ValueError) as exc:
                errors.append(build_validate_domain_error("MISSING_EXPECTED_ARTIFACT", str(exc), field="sandbox_agents"))
        validations.append({"artifact_kind": "sandbox_agents", "present": True, "valid": valid_agents == len(agent_files), "count": valid_agents})

    team_files = sorted(
        path
        for path in (domain_dir / "sandbox_teams").glob("*.json")
        if not path.name.endswith(".manifest.json")
    ) if (domain_dir / "sandbox_teams").is_dir() else []
    if not team_files:
        errors.append(build_validate_domain_error("MISSING_EXPECTED_ARTIFACT", "sandbox_team no encontrado", field="sandbox_team"))
        validations.append({"artifact_kind": "sandbox_team", "present": False, "valid": False, "count": 0})
    else:
        valid_teams = 0
        for path in team_files:
            try:
                validate_materialized_sandbox_team(domain_dir, team_id=path.stem)
                valid_teams += 1
            except (OSError, ValueError) as exc:
                errors.append(build_validate_domain_error("MISSING_EXPECTED_ARTIFACT", str(exc), field="sandbox_team"))
        validations.append({"artifact_kind": "sandbox_team", "present": True, "valid": valid_teams == len(team_files), "count": valid_teams})

    expected_ids = {"profile_catalog_main", "agent_presets_main", "paper_seed_main"}
    actual_ids = {artifact.get("artifact_id") for artifact in artifact_manifest.get("artifacts") or []}
    if artifact_manifest and not expected_ids <= actual_ids:
        errors.append(build_validate_domain_error("MISSING_EXPECTED_ARTIFACT", "artifact_manifest no contiene artefactos base"))
    return validations


def _artifact_validation_entry(
    domain_dir: Path,
    artifact_kind: str,
    artifact_id: str,
    validator: Any,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    try:
        validation = validator(domain_dir)
        artifact = validation.get("artifact") or {}
        return {
            "artifact_kind": artifact_kind,
            "artifact_id": artifact_id,
            "present": True,
            "valid": artifact.get("artifact_id") == artifact_id,
            "artifact_type": artifact.get("artifact_type"),
            "dependencies": list(artifact.get("dependencies") or []),
            "operational": artifact.get("operational") is True,
            "passed": artifact.get("passed") is True,
        }
    except (OSError, ValueError) as exc:
        errors.append(build_validate_domain_error("MISSING_EXPECTED_ARTIFACT", str(exc), field=artifact_kind))
        return {"artifact_kind": artifact_kind, "artifact_id": artifact_id, "present": False, "valid": False}


def _result_payload(
    *,
    sandbox_root: Path | str = "",
    domain_id: str = "",
    materialization_id: str = "",
    valid: bool,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
    domain_validation: dict[str, Any] | None = None,
    artifact_manifest_validation: dict[str, Any] | None = None,
    created_paths_validation: dict[str, Any] | None = None,
    lineage_validation: dict[str, Any] | None = None,
    artifact_validations: list[dict[str, Any]] | None = None,
    read_models_validation: dict[str, Any] | None = None,
    rollback_readiness: dict[str, Any] | None = None,
    audit_pack_validation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "status": SERVICE_STATUS if valid else "blocked",
        "verdict": SERVICE_VERDICT if valid else "BACKEND_INTERNAL_VALIDATE_DOMAIN_BLOCKED",
        "read_only_verdict": SERVICE_READ_ONLY_VERDICT,
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "domain_id": domain_id,
        "materialization_id": materialization_id,
        "sandbox_root": str(sandbox_root),
        "validation_scope": VALIDATION_SCOPE,
        "domain_validation": domain_validation or {},
        "artifact_manifest_validation": artifact_manifest_validation or {},
        "created_paths_validation": created_paths_validation or {},
        "lineage_validation": lineage_validation or {},
        "artifact_validations": artifact_validations or [],
        "read_models_validation": read_models_validation or {},
        "rollback_readiness": rollback_readiness or {},
        "audit_pack_validation": audit_pack_validation or {},
        "warnings": warnings,
        "errors": errors,
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": list(ALLOWED_ACTIONS),
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "next_actions": ["request_rollback_next_step"] if valid else ["review_validation_errors"],
        "validation": {
            "request_valid": not any(error["error_code"] in {"VALIDATION_REQUEST_REQUIRED", "INVALID_VALIDATE_DOMAIN_REQUEST"} for error in errors),
            "sandbox_root_explicit": bool(str(sandbox_root)),
            "sandbox_root_controlled": bool(str(sandbox_root)),
            "domain_checked": bool(domain_validation),
            "artifact_manifest_checked": bool(artifact_manifest_validation),
            "created_paths_checked": bool(created_paths_validation),
            "lineage_checked": bool(lineage_validation),
            "read_models_checked": bool(read_models_validation),
            "rollback_readiness_checked": bool(rollback_readiness),
            "json_safe": True,
            "read_only": True,
            "no_write": True,
            "no_materialization": True,
            "no_rollback": True,
            "no_regeneration": True,
            "no_runtime": True,
            "no_execution": True,
            "no_tools_or_models": True,
            "no_integrations": True,
        },
        "valid": valid,
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "writes_performed": False,
        "materialization_performed": False,
        "rollback_performed": False,
        "regeneration_performed": False,
    }


def _blocked_payload(*, errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> dict[str, Any]:
    return _result_payload(valid=False, errors=errors, warnings=warnings)


def _validation_result(**kwargs: Any) -> dict[str, Any]:
    return kwargs


def _resolve_sandbox_root(raw: Any) -> Path:
    if raw in (None, ""):
        raise ValueError("SANDBOX_ROOT_REQUIRED: sandbox_root explicito requerido")
    text = str(raw)
    if any(part == ".." for part in Path(text).parts):
        raise ValueError("PATH_TRAVERSAL_BLOCKED: sandbox_root contiene path traversal")
    root = Path(text).resolve()
    reason = _unsafe_root_reason(root)
    if reason:
        raise ValueError(f"UNSAFE_SANDBOX_ROOT: {reason}")
    if not root.exists() or not root.is_dir():
        raise ValueError("SANDBOX_ROOT_NOT_FOUND: sandbox_root no existe o no es directorio")
    return root


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


def _validate_domain_id(raw: Any) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("DOMAIN_ID_REQUIRED: domain_id requerido")
    value = raw.strip()
    if any(part == ".." for part in Path(value).parts):
        raise ValueError("INVALID_VALIDATE_DOMAIN_REQUEST: domain_id contiene traversal")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError("INVALID_VALIDATE_DOMAIN_REQUEST: domain_id debe ser snake_case")
    return value


def _validation_options(raw: Any) -> dict[str, bool]:
    source = raw if isinstance(raw, dict) else {}
    return {
        "include_artifact_manifest": source.get("include_artifact_manifest") is not False,
        "include_lineage": source.get("include_lineage") is not False,
        "include_created_paths": source.get("include_created_paths") is not False,
        "include_read_models": source.get("include_read_models") is not False,
        "include_rollback_readiness": source.get("include_rollback_readiness") is not False,
        "include_audit_pack": source.get("include_audit_pack") is not False,
        "strict": source.get("strict") is not False,
    }


def _safe_child(root: Path, relative: str | Path) -> Path:
    if any(part == ".." for part in Path(relative).parts):
        raise ValueError("PATH_TRAVERSAL_BLOCKED: path contiene traversal")
    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError("UNSAFE_CREATED_PATH: path escapa del sandbox_root")
    return target


def _unsafe_created_paths(paths: list[Any], *, sandbox_root: Path) -> list[str]:
    unsafe: list[str] = []
    repo_root = Path(__file__).resolve().parents[1]
    domains_root = (repo_root / "domains").resolve()
    forbidden_parts = {".git", "core", "docs", "tests"}
    for raw_path in paths:
        text = str(raw_path)
        if any(part == ".." for part in Path(text).parts):
            unsafe.append(_safe_text(text))
            continue
        path = Path(text).resolve()
        if path != sandbox_root and sandbox_root not in path.parents:
            unsafe.append(_safe_text(text))
            continue
        if path == domains_root or domains_root in path.parents:
            unsafe.append(_safe_text(text))
            continue
        if repo_root in path.parents and set(path.parts) & forbidden_parts:
            unsafe.append(_safe_text(text))
    return unsafe


def _non_operational_domain(domain: dict[str, Any]) -> bool:
    if domain.get("status") == "active" or domain.get("artifact_state") == "active":
        return False
    metadata = domain.get("metadata") or {}
    validation = domain.get("validation") or {}
    if metadata.get("operational") is True:
        return False
    if validation.get("passed") is True:
        return False
    return True


def _artifact_manifest_matches_materialization(artifact_manifest: dict[str, Any], materialization_id: str) -> bool:
    if not materialization_id:
        return True
    artifacts = artifact_manifest.get("artifacts") or []
    return all(
        artifact.get("created_from", {}).get("materialization_id") in {None, "", materialization_id}
        or artifact.get("materialization_id") in {None, "", materialization_id}
        for artifact in artifacts
    )


def _dependency_pairs(artifact_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "artifact_id": artifact.get("artifact_id"),
            "depends_on": list(artifact.get("dependencies") or []),
        }
        for artifact in artifact_manifest.get("artifacts") or []
    ]


def _dependencies_coherent(artifact_manifest: dict[str, Any]) -> bool:
    artifact_ids = {artifact.get("artifact_id") for artifact in artifact_manifest.get("artifacts") or []}
    return all(set(artifact.get("dependencies") or []) <= artifact_ids for artifact in artifact_manifest.get("artifacts") or [])


def _validate_actions(payload: dict[str, Any]) -> None:
    prohibited_allowed = {
        "execute",
        "activate_runtime",
        "execute_agents",
        "invoke_models",
        "call_tools",
        "delete_without_confirmation",
        "rollback_without_confirmation",
    }
    allowed = set(payload.get("allowed_actions") or [])
    if allowed & prohibited_allowed:
        raise ValueError("allowed_actions contiene acciones prohibidas")
    required_forbidden = {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"}
    if not required_forbidden <= set(payload.get("forbidden_actions") or []):
        raise ValueError("forbidden_actions incompleto")


def _reject_sensitive_keys(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            lowered = key_text.lower()
            if key_text not in ALLOWED_SENSITIVE_DECLARATION_KEYS and any(fragment in lowered for fragment in SENSITIVE_KEY_FRAGMENTS):
                raise ValueError(f"campo sensible bloqueado en {path}.{key_text}")
            _reject_sensitive_keys(value, f"{path}.{key_text}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_sensitive_keys(value, f"{path}[{index}]")


def _reject_forbidden_true_flags(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            if key_text in FORBIDDEN_TRUE_KEYS and value is True:
                raise ValueError(f"flag operativo prohibido en {path}.{key_text}")
            _reject_forbidden_true_flags(value, f"{path}.{key_text}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_forbidden_true_flags(value, f"{path}[{index}]")


def _ensure_json_safe(payload: Any) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("PAYLOAD_NOT_JSON_SAFE: payload no serializable") from exc


def _error_from_exception(exc: Exception) -> dict[str, Any]:
    message = str(exc)
    prefix = message.split(":", 1)[0]
    code = prefix if prefix in ERROR_CODES else "INVALID_VALIDATE_DOMAIN_REQUEST"
    if "SANDBOX_ROOT_REQUIRED" in message:
        code = "SANDBOX_ROOT_REQUIRED"
    elif "SANDBOX_ROOT_NOT_FOUND" in message:
        code = "SANDBOX_ROOT_NOT_FOUND"
    elif "UNSAFE_SANDBOX_ROOT" in message:
        code = "UNSAFE_SANDBOX_ROOT"
    elif "DOMAIN_ID_REQUIRED" in message:
        code = "DOMAIN_ID_REQUIRED"
    elif "PATH_TRAVERSAL_BLOCKED" in message:
        code = "UNSAFE_CREATED_PATH"
    elif "SECRET" in message or "sensible" in message:
        code = "SECRET_LIKE_FIELD_BLOCKED"
    elif "PAYLOAD_NOT_JSON_SAFE" in message:
        code = "PAYLOAD_NOT_JSON_SAFE"
    return build_validate_domain_error(code, message, recoverable=code not in {"SECRET_LIKE_FIELD_BLOCKED", "UNSAFE_SANDBOX_ROOT"})


def _safe_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "unknown"


def _safe_text(value: Any) -> str:
    text = str(value)
    return text.replace("\r", " ").replace("\n", " ")[:240]


def _user_action_for(code: str) -> str:
    return {
        "VALIDATION_REQUEST_REQUIRED": "Enviar request de validacion.",
        "SANDBOX_ROOT_REQUIRED": "Seleccionar sandbox_root controlado.",
        "SANDBOX_ROOT_NOT_FOUND": "Verificar que el sandbox exista.",
        "DOMAIN_ID_REQUIRED": "Enviar domain_id.",
        "DOMAIN_NOT_FOUND": "Revisar dominio sandbox seleccionado.",
        "MISSING_ARTIFACT_MANIFEST": "Revisar materializacion previa.",
        "ROLLBACK_NOT_READY": "Solicitar revision antes de rollback futuro.",
    }.get(code, "Revisar payload y reintentar.")


def _developer_hint_for(code: str) -> str:
    return {
        "UNSAFE_SANDBOX_ROOT": "sandbox_root no debe apuntar a repo, domains ni carpetas internas.",
        "UNSAFE_CREATED_PATH": "created_paths deben resolver bajo sandbox_root.",
        "SECRET_LIKE_FIELD_BLOCKED": "Eliminar campos secret/env/token/runtime handles.",
        "WRITE_OPERATION_BLOCKED": "validate_domain es read-only.",
    }.get(code, "Error controlado de validate_domain 7.4.")
