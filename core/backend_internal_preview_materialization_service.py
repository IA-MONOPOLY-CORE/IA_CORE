"""Servicio interno preview_materialization no-write para futura UI.

El servicio envuelve el preview de dominio existente y calcula artefactos,
paths, manifests y readiness planeados sin crear archivos ni directorios.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import config
from core.backend_internal_ui_contract import build_backend_internal_ui_forbidden_capabilities
from core.domain_materialization_preview import build_domain_materialization_preview


SERVICE_NAME = "preview_materialization"
SERVICE_VERSION = "0.1"
SERVICE_STATUS = "ready"
SERVICE_VERDICT = "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_READY"
SERVICE_NO_WRITE_VERDICT = "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_WRITE_CONFIRMED"
SERVICE_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED"
SERVICE_READINESS = "ready_for_phase_7_3_materialize_sandbox_service"
MAX_PREVIEW_PAYLOAD_JSON_BYTES = 96_000

ALLOWED_ACTIONS = (
    "view_preview",
    "view_planned_artifacts",
    "view_planned_paths",
    "view_warnings",
    "request_materialization_next_step",
)
FORBIDDEN_ACTIONS = (
    "execute_preview",
    "persist_preview",
    "activate_runtime",
    "execute_agents",
    "invoke_models",
    "call_tools",
    "use_integrations",
    "write_operational_outputs",
    "mutate_manifest_directly",
    "materialize_without_confirmation",
    "rollback_without_materialization",
    "delete_without_confirmation",
    "regenerate_without_rollback",
    "open_ui_runtime",
)
ERROR_CODES = (
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
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "MATERIALIZATION_NOT_PERFORMED",
    "WRITE_OPERATION_BLOCKED",
    "READINESS_NOT_MET",
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
ALLOWED_POLICY_KEYS = {
    "SECRET_LIKE_FIELD_BLOCKED",
}
FORBIDDEN_OPERATIONAL_KEYS = {
    "operational",
    "runtime_enabled",
    "execution_enabled",
    "writes_performed",
    "materialization_performed",
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
}


def preview_materialization(request: dict[str, Any] | None) -> dict[str, Any]:
    """Construye preview interno no-write a partir de una request explicita."""
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not isinstance(request, dict):
        errors.append(build_preview_materialization_error("DOMAIN_REQUEST_REQUIRED", "request requerido"))
        return validate_materialization_preview_payload(_blocked_payload(errors=errors, warnings=warnings))

    try:
        _reject_sensitive_keys(request)
        _ensure_json_safe(request)
    except ValueError as exc:
        errors.append(build_preview_materialization_error("SECRET_LIKE_FIELD_BLOCKED", str(exc)))
        return validate_materialization_preview_payload(_blocked_payload(errors=errors, warnings=warnings))

    root_result = _resolve_sandbox_root(request.get("sandbox_root"))
    if root_result.get("error"):
        errors.append(root_result["error"])
        return validate_materialization_preview_payload(_blocked_payload(errors=errors, warnings=warnings))
    sandbox_root = root_result["root"]

    domain_request_result = _validate_domain_request(request.get("domain_request"))
    if domain_request_result.get("error"):
        errors.append(domain_request_result["error"])
        return validate_materialization_preview_payload(_blocked_payload(errors=errors, warnings=warnings))
    domain_request = domain_request_result["domain_request"]

    options = _preview_options(request.get("preview_options"))
    warnings.extend(_unsupported_artifact_warnings(options["requested_artifact_kinds"]))
    preview = build_materialization_preview(domain_request=domain_request)
    domain_id = domain_request["domain_id"]
    planned_paths = _planned_paths(domain_id, include_paths_preview=options["include_paths_preview"])
    path_errors = _validate_planned_paths(planned_paths)
    errors.extend(path_errors)
    planned_artifacts = _planned_artifacts(
        domain_id,
        preview=preview,
        include_team_preview=options["include_team_preview"],
        include_audit_pack_preview=options["include_audit_pack_preview"],
    )
    planned_manifests = _planned_manifests(domain_id, planned_artifacts, include_manifest_preview=options["include_manifest_preview"])
    payload = {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "status": SERVICE_STATUS if not errors else "blocked",
        "verdict": SERVICE_VERDICT if not errors else "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_BLOCKED",
        "no_write_verdict": SERVICE_NO_WRITE_VERDICT,
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "domain_preview": _domain_preview(domain_request, preview),
        "planned_artifacts": planned_artifacts,
        "planned_paths": planned_paths,
        "planned_manifests": planned_manifests,
        "planned_lineage": _planned_lineage(domain_request, preview),
        "planned_dependencies": _planned_dependencies(planned_artifacts),
        "planned_read_models": _planned_read_models(domain_id, planned_artifacts),
        "planned_audit_pack": _planned_audit_pack(domain_id, options),
        "warnings": warnings,
        "errors": errors,
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": list(ALLOWED_ACTIONS),
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "next_actions": ["request_materialization_next_step"] if not errors else ["review_preview_errors"],
        "validation": {
            "domain_request_valid": not errors,
            "sandbox_root_explicit": True,
            "sandbox_root_controlled": True,
            "planned_paths_safe": not path_errors,
            "json_safe": True,
            "read_only_preview": True,
            "no_side_effects": True,
            "no_write": True,
            "no_materialization": True,
            "backend_authoritative": True,
        },
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "writes_performed": False,
        "materialization_performed": False,
    }
    return validate_materialization_preview_payload(payload)


def build_materialization_preview(*, domain_request: dict[str, Any]) -> dict[str, Any]:
    """Reutiliza el preview canonico existente sin escribir artefactos."""
    return build_domain_materialization_preview(
        domain_id=domain_request["domain_id"],
        area_id=domain_request["area_id"],
        niche_ids=domain_request.get("niche_ids") or [],
        business_scale=domain_request.get("business_scale"),
        objective=domain_request.get("objective"),
        complexity_level=domain_request.get("complexity_level"),
        max_profiles=domain_request.get("max_profiles"),
        max_presets=domain_request.get("max_presets"),
    )


def validate_materialization_preview_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida payload de preview sin side effects."""
    if not isinstance(payload, dict):
        raise ValueError("preview materialization payload debe ser objeto")
    required = {
        "service",
        "service_version",
        "status",
        "readiness",
        "domain_preview",
        "planned_artifacts",
        "planned_paths",
        "planned_manifests",
        "planned_lineage",
        "planned_dependencies",
        "planned_read_models",
        "planned_audit_pack",
        "warnings",
        "errors",
        "blocked_capabilities",
        "allowed_actions",
        "forbidden_actions",
        "next_actions",
        "validation",
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "writes_performed",
        "materialization_performed",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"preview materialization payload incompleto: {', '.join(sorted(missing))}")
    if payload.get("service") != SERVICE_NAME:
        raise ValueError("service invalido")
    if payload.get("service_version") != SERVICE_VERSION:
        raise ValueError("service_version invalida")
    if payload.get("readiness") != SERVICE_READINESS:
        raise ValueError("readiness invalida")
    for field in ("planned_artifacts", "planned_paths", "planned_manifests", "planned_dependencies", "planned_read_models", "warnings", "errors", "allowed_actions", "forbidden_actions", "next_actions"):
        if not isinstance(payload.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    for field in ("domain_preview", "planned_lineage", "planned_audit_pack", "blocked_capabilities", "validation"):
        if not isinstance(payload.get(field), dict):
            raise ValueError(f"{field} debe ser objeto")
    for field in ("operational", "runtime_enabled", "execution_enabled", "writes_performed", "materialization_performed"):
        if payload.get(field) is not False:
            raise ValueError(f"{field} debe ser false")
    _reject_sensitive_keys(payload)
    _reject_recursive_enabled_operation(payload)
    _validate_actions(payload)
    _validate_artifacts(payload["planned_artifacts"])
    _validate_paths(payload["planned_paths"])
    _validate_manifests(payload["planned_manifests"])
    if any(value is not False for value in payload["blocked_capabilities"].values()):
        raise ValueError("blocked_capabilities debe mantener todo false")
    dumped = _ensure_json_safe(payload)
    if len(dumped.encode("utf-8")) > MAX_PREVIEW_PAYLOAD_JSON_BYTES:
        raise ValueError("preview materialization payload excede tamano maximo")
    return deepcopy(payload)


def build_preview_materialization_error(
    error_code: str,
    message: str,
    *,
    severity: str = "error",
    field: str = "",
    recoverable: bool = True,
) -> dict[str, Any]:
    """Construye error legible para futura UI."""
    if error_code not in ERROR_CODES:
        error_code = "INVALID_DOMAIN_REQUEST"
    return {
        "error_code": error_code,
        "message": _safe_message(message),
        "severity": severity,
        "field": field,
        "recoverable": recoverable,
        "user_action": "revisar la solicitud de preview indicada por backend",
        "developer_hint": "mantener preview como simulacion no-write",
        "blocked": severity in {"error", "critical"},
    }


def _blocked_payload(*, errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "status": "blocked",
        "verdict": "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_BLOCKED",
        "no_write_verdict": SERVICE_NO_WRITE_VERDICT,
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "domain_preview": {},
        "planned_artifacts": [],
        "planned_paths": [],
        "planned_manifests": [],
        "planned_lineage": {},
        "planned_dependencies": [],
        "planned_read_models": [],
        "planned_audit_pack": {},
        "warnings": warnings,
        "errors": errors,
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": ["view_warnings"],
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "next_actions": ["review_preview_errors"],
        "validation": {
            "domain_request_valid": False,
            "sandbox_root_explicit": False,
            "sandbox_root_controlled": False,
            "planned_paths_safe": False,
            "json_safe": True,
            "read_only_preview": True,
            "no_side_effects": True,
            "no_write": True,
            "no_materialization": True,
            "backend_authoritative": True,
        },
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "writes_performed": False,
        "materialization_performed": False,
    }


def _validate_domain_request(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict) or not raw:
        return {"error": build_preview_materialization_error("DOMAIN_REQUEST_REQUIRED", "domain_request requerido", field="domain_request")}
    domain_id = str(raw.get("domain_id") or "").strip()
    if not domain_id:
        return {"error": build_preview_materialization_error("INVALID_DOMAIN_ID", "domain_id requerido", field="domain_request.domain_id")}
    if ".." in domain_id or "/" in domain_id or "\\" in domain_id:
        return {"error": build_preview_materialization_error("PATH_TRAVERSAL_BLOCKED", "domain_id contiene traversal o separadores", field="domain_request.domain_id", recoverable=False)}
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", domain_id):
        return {"error": build_preview_materialization_error("INVALID_DOMAIN_ID", "domain_id debe estar en snake_case", field="domain_request.domain_id")}
    domain_type = raw.get("domain_type", "sandbox")
    if domain_type != "sandbox":
        return {"error": build_preview_materialization_error("INVALID_DOMAIN_REQUEST", "domain_type debe ser sandbox", field="domain_request.domain_type")}
    area_id = str(raw.get("area_id") or "").strip()
    if not area_id:
        return {"error": build_preview_materialization_error("INVALID_DOMAIN_REQUEST", "area_id requerido para preview canonico", field="domain_request.area_id")}
    domain_name = str(raw.get("domain_name") or raw.get("name") or domain_id.replace("_", " ")).strip()
    domain_description = str(raw.get("domain_description") or raw.get("description") or "Preview sandbox no operativo.").strip()
    return {
        "domain_request": {
            "domain_id": domain_id,
            "domain_name": domain_name,
            "domain_description": domain_description,
            "domain_type": "sandbox",
            "source": str(raw.get("source") or "user_request_or_fixture"),
            "area_id": area_id,
            "niche_ids": list(raw.get("niche_ids") or []),
            "business_scale": raw.get("business_scale"),
            "objective": raw.get("objective"),
            "complexity_level": raw.get("complexity_level"),
            "max_profiles": raw.get("max_profiles"),
            "max_presets": raw.get("max_presets"),
        }
    }


def _preview_options(raw: Any) -> dict[str, bool]:
    source = raw if isinstance(raw, dict) else {}
    return {
        "include_team_preview": source.get("include_team_preview") is not False,
        "include_audit_pack_preview": source.get("include_audit_pack_preview") is not False,
        "include_paths_preview": source.get("include_paths_preview") is not False,
        "include_manifest_preview": source.get("include_manifest_preview") is not False,
        "requested_artifact_kinds": list(source.get("requested_artifact_kinds") or []),
    }


def _unsupported_artifact_warnings(requested: list[Any]) -> list[dict[str, Any]]:
    supported = {
        "sandbox_domain",
        "artifact_manifest",
        "profile_catalog",
        "agent_presets",
        "paper_seed",
        "sandbox_agents",
        "sandbox_team",
        "sandbox_team_read_model",
        "materialization_audit_pack",
    }
    warnings = []
    for item in requested:
        artifact = str(item)
        if artifact not in supported:
            warnings.append(
                build_preview_materialization_error(
                    "READINESS_NOT_MET",
                    f"planned artifact no soportado en preview: {artifact}",
                    severity="warning",
                    field="preview_options.requested_artifact_kinds",
                    recoverable=True,
                )
            )
    return warnings


def _resolve_sandbox_root(raw: Any) -> dict[str, Any]:
    if raw in (None, ""):
        return {"error": build_preview_materialization_error("SANDBOX_ROOT_REQUIRED", "sandbox_root explicito requerido", field="sandbox_root")}
    text = str(raw)
    if ".." in Path(text).parts:
        return {"error": build_preview_materialization_error("PATH_TRAVERSAL_BLOCKED", "sandbox_root contiene path traversal", field="sandbox_root", recoverable=False)}
    root = Path(text).resolve()
    reason = _unsafe_root_reason(root)
    if reason:
        return {"error": build_preview_materialization_error("UNSAFE_SANDBOX_ROOT", reason, field="sandbox_root", recoverable=False)}
    if not root.exists() or not root.is_dir():
        return {"error": build_preview_materialization_error("SANDBOX_ROOT_NOT_FOUND", "sandbox_root no existe o no es directorio", field="sandbox_root")}
    return {"root": root}


def _unsafe_root_reason(root: Path) -> str | None:
    repo_root = Path(__file__).resolve().parents[1]
    domains_root = Path(config.DOMAINS_DIR).resolve()
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


def _domain_preview(domain_request: dict[str, Any], preview: dict[str, Any]) -> dict[str, Any]:
    return {
        "preview_id": preview["preview_id"],
        "domain_id": domain_request["domain_id"],
        "domain_name": domain_request["domain_name"],
        "domain_description": domain_request["domain_description"],
        "domain_type": "sandbox",
        "artifact_state": "derived_preview",
        "validation_status": preview["validation_status"],
        "source": domain_request["source"],
        "warnings_count": len(preview.get("warnings") or []),
        "gaps_count": len(preview.get("gaps") or []),
        "risks_count": len(preview.get("risks") or []),
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _planned_artifacts(
    domain_id: str,
    *,
    preview: dict[str, Any],
    include_team_preview: bool,
    include_audit_pack_preview: bool,
) -> list[dict[str, Any]]:
    base = [
        ("sandbox_domain", "domain", "sandbox_domain", "domain.json", []),
        ("artifact_manifest", "manifest", "artifact_manifest", "manifests/artifact_manifest.json", ["sandbox_domain"]),
        ("profile_catalog", "profile_catalog", "derived_domain_profile_catalog", "profile_catalog/profile_catalog.json", ["sandbox_domain"]),
        ("agent_presets", "agent_preset", "derived_domain_agent_presets", "agent_presets/agent_presets.json", ["profile_catalog"]),
        ("paper_seed", "paper_seed", "derived_paper_seed", "paper_seed/paper_seed.json", ["profile_catalog", "agent_presets"]),
        ("sandbox_agents", "agent", "sandbox_agent", "sandbox_agents/<agent_id>.json", ["profile_catalog", "agent_presets", "paper_seed"]),
    ]
    if include_team_preview and preview.get("derived_outputs", {}).get("team_template"):
        base.append(("sandbox_team", "team", "sandbox_team", "sandbox_teams/<team_id>.json", ["sandbox_agents"]))
        base.append(("sandbox_team_read_model", "read_model", "sandbox_team_internal_listing", "read_models/sandbox_team_listing.json", ["sandbox_team"]))
    if include_audit_pack_preview:
        base.append(("materialization_audit_pack", "audit_pack", "sandbox_materialization_audit_pack", "audit/materialization_audit_pack.json", ["artifact_manifest", "sandbox_team_read_model"]))
    return [
        {
            "artifact_id": f"preview_{domain_id}_{artifact_id}",
            "artifact_type": artifact_type,
            "artifact_kind": artifact_kind,
            "planned_path": planned_path,
            "source": "preview_materialization",
            "created_from": {
                "type": "preview",
                "preview_only": True,
                "materialization_id_policy": "generated_on_materialization",
            },
            "dependencies": dependencies,
            "operational": False,
            "passed": False,
            "runtime_enabled": False,
            "execution_enabled": False,
        }
        for artifact_id, artifact_type, artifact_kind, planned_path, dependencies in base
    ]


def _planned_paths(domain_id: str, *, include_paths_preview: bool) -> list[dict[str, Any]]:
    if not include_paths_preview:
        return []
    relatives = [
        domain_id,
        f"{domain_id}/domain.json",
        f"{domain_id}/materialization_manifest.json",
        f"{domain_id}/manifests",
        f"{domain_id}/manifests/artifact_manifest.json",
        f"{domain_id}/profile_catalog/profile_catalog.json",
        f"{domain_id}/agent_presets/agent_presets.json",
        f"{domain_id}/paper_seed/paper_seed.json",
        f"{domain_id}/sandbox_agents",
        f"{domain_id}/sandbox_teams",
        f"{domain_id}/read_models/sandbox_team_listing.json",
        f"{domain_id}/audit/materialization_audit_pack.json",
    ]
    return [
        {
            "path_kind": "directory" if not Path(relative).suffix else "file",
            "relative_path": relative,
            "operation": "would_create",
            "safe": True,
            "under_sandbox_root": True,
        }
        for relative in relatives
    ]


def _planned_manifests(domain_id: str, artifacts: list[dict[str, Any]], *, include_manifest_preview: bool) -> list[dict[str, Any]]:
    if not include_manifest_preview:
        return []
    return [
        {
            "manifest_kind": "materialization_manifest",
            "artifact_id": f"preview_{domain_id}_sandbox_domain",
            "artifact_type": "manifest",
            "artifact_kind": "materialization_manifest",
            "domain_id": domain_id,
            "materialization_id_policy": "generated_on_materialization",
            "operational": False,
            "passed": False,
        },
        {
            "manifest_kind": "artifact_manifest",
            "artifact_id": f"preview_{domain_id}_artifact_manifest",
            "artifact_type": "manifest",
            "artifact_kind": "artifact_manifest",
            "domain_id": domain_id,
            "materialization_id_policy": "generated_on_materialization",
            "planned_artifact_count": len(artifacts),
            "operational": False,
            "passed": False,
        },
    ]


def _planned_lineage(domain_request: dict[str, Any], preview: dict[str, Any]) -> dict[str, Any]:
    return {
        "preview_id": preview["preview_id"],
        "domain_id": domain_request["domain_id"],
        "source": domain_request["source"],
        "source_request": {
            "area_id": domain_request["area_id"],
            "niche_ids": list(domain_request.get("niche_ids") or []),
            "business_scale": domain_request.get("business_scale"),
            "objective": domain_request.get("objective"),
        },
        "materialization_id_policy": "generated_on_materialization",
        "lineage_status": "preview_only",
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _planned_dependencies(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "artifact_id": artifact["artifact_id"],
            "depends_on": list(artifact["dependencies"]),
            "declarative": True,
            "resolved_on_materialization": True,
        }
        for artifact in artifacts
    ]


def _planned_read_models(domain_id: str, artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    kinds = {artifact["artifact_kind"] for artifact in artifacts}
    if "sandbox_team_internal_listing" not in kinds:
        return []
    return [
        {
            "read_model": "sandbox_team_internal_listing",
            "domain_id": domain_id,
            "source": "core.sandbox_team_read_model.list_sandbox_teams",
            "available_after_materialization": True,
            "preview_only": True,
            "operational": False,
        }
    ]


def _planned_audit_pack(domain_id: str, options: dict[str, bool]) -> dict[str, Any]:
    if not options["include_audit_pack_preview"]:
        return {"planned": False, "reason": "include_audit_pack_preview=false"}
    return {
        "planned": True,
        "domain_id": domain_id,
        "source": "core.sandbox_materialization_audit_pack",
        "available_after_materialization_rollback_regeneration": True,
        "preview_only": True,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _validate_planned_paths(paths: list[dict[str, Any]]) -> list[dict[str, Any]]:
    errors = []
    for path in paths:
        relative = str(path.get("relative_path") or "")
        if ".." in Path(relative).parts:
            errors.append(build_preview_materialization_error("PATH_TRAVERSAL_BLOCKED", "planned_path contiene traversal", field="planned_paths", recoverable=False))
        if relative.startswith("/") or re.match(r"^[a-zA-Z]:", relative):
            errors.append(build_preview_materialization_error("UNSAFE_PLANNED_PATH", "planned_path no debe ser absoluto", field="planned_paths", recoverable=False))
        if relative.replace("\\", "/").startswith("domains/"):
            errors.append(build_preview_materialization_error("DOMAINS_OPERATIVE_PATH_BLOCKED", "planned_path apunta a domains operativo", field="planned_paths", recoverable=False))
    return errors


def _validate_actions(payload: dict[str, Any]) -> None:
    forbidden = {"materialize", "execute", "rollback", "delete", "regenerate", "persist_preview", "execute_preview"}
    for action in payload["allowed_actions"]:
        if action in forbidden or any(action.startswith(prefix) for prefix in forbidden):
            raise ValueError("allowed_actions contiene accion destructiva u operativa")
    if not set(FORBIDDEN_ACTIONS) <= set(payload["forbidden_actions"]):
        raise ValueError("forbidden_actions incompleto")


def _validate_artifacts(artifacts: list[dict[str, Any]]) -> None:
    for artifact in artifacts:
        for field in ("artifact_id", "artifact_type", "artifact_kind", "planned_path", "source", "created_from", "dependencies"):
            if field not in artifact:
                raise ValueError(f"planned_artifact incompleto: {field}")
        for flag in ("operational", "passed", "runtime_enabled", "execution_enabled"):
            if artifact.get(flag) is not False:
                raise ValueError(f"planned_artifact {artifact['artifact_id']} {flag} debe ser false")


def _validate_paths(paths: list[dict[str, Any]]) -> None:
    for item in paths:
        if item.get("operation") != "would_create":
            raise ValueError("planned_paths solo puede usar operation=would_create")
        if item.get("safe") is not True or item.get("under_sandbox_root") is not True:
            raise ValueError("planned_path inseguro")
        relative = str(item.get("relative_path") or "")
        if not relative:
            raise ValueError("planned_path sin relative_path")
        if _validate_planned_paths([item]):
            raise ValueError("planned_path inseguro")


def _validate_manifests(manifests: list[dict[str, Any]]) -> None:
    for manifest in manifests:
        for field in ("manifest_kind", "artifact_id", "artifact_type", "artifact_kind", "domain_id", "materialization_id_policy"):
            if field not in manifest:
                raise ValueError(f"planned_manifest incompleto: {field}")
        if manifest.get("materialization_id_policy") != "generated_on_materialization":
            raise ValueError("planned_manifest materialization_id_policy invalida")
        if manifest.get("operational") is not False or manifest.get("passed") is not False:
            raise ValueError("planned_manifest debe ser no operativo")


def _reject_sensitive_keys(value: Any, path: str = "") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if (
                key not in ALLOWED_POLICY_KEYS
                and not path.startswith("blocked_capabilities")
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


def _ensure_json_safe(payload: Any) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("preview materialization payload no es JSON-safe") from exc


def _safe_message(message: str) -> str:
    text = str(message).replace("\\", "/")
    repo_root = str(Path(__file__).resolve().parents[1]).replace("\\", "/")
    if repo_root in text:
        text = text.replace(repo_root, "<repo>")
    return text
