"""Servicio interno read-only list_domains/status para futura UI.

El servicio lista dominios sandbox desde un ``sandbox_root`` explicito y
controlado. No lee ``domains/`` operativo por defecto, no escribe archivos,
no materializa, no ejecuta rollback/regeneracion y no abre endpoints/UI.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import config
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.backend_internal_ui_contract import build_backend_internal_ui_forbidden_capabilities
from core.domain_materializer import MATERIALIZATION_MANIFEST, validate_materialized_sandbox_domain
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.sandbox_materialization_audit_pack import validate_sandbox_materialization_audit_pack
from core.sandbox_team_read_model import list_sandbox_teams


SERVICE_NAME = "list_domains_status"
SERVICE_VERSION = "0.1"
SERVICE_STATUS = "ready"
SERVICE_VERDICT = "BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_READY"
SERVICE_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_DOMAIN_STATUS_NO_OPERATIONAL_CONFIRMED"
SERVICE_READINESS = "ready_for_phase_7_2_preview_materialization_service"
DOMAIN_LISTABLE_READINESS = "ready_for_internal_listing"
DOMAIN_BLOCKED_READINESS = "blocked_by_validation"
MAX_STATUS_PAYLOAD_JSON_BYTES = 64_000

ALLOWED_ACTIONS = ("view_status", "view_details", "view_audit_pack_summary")
FORBIDDEN_ACTIONS = (
    "activate_runtime",
    "execute_agents",
    "invoke_models",
    "call_tools",
    "use_integrations",
    "write_operational_outputs",
    "mutate_manifest_directly",
    "materialize_without_preview",
    "rollback_without_confirmation",
    "delete_without_confirmation",
    "regenerate_without_rollback",
    "open_ui_runtime",
)
ERROR_CODES = (
    "SANDBOX_ROOT_REQUIRED",
    "SANDBOX_ROOT_NOT_FOUND",
    "UNSAFE_SANDBOX_ROOT",
    "INVALID_DOMAIN_STATUS_PAYLOAD",
    "MISSING_ARTIFACT_MANIFEST",
    "INCONSISTENT_ARTIFACT_MANIFEST",
    "INVALID_AUDIT_PACK",
    "READ_MODEL_UNAVAILABLE",
    "DOMAIN_STATUS_NOT_LISTABLE",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "SECRET_LIKE_FIELD_BLOCKED",
    "PAYLOAD_NOT_JSON_SAFE",
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
    "env",
    "secrets",
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


def list_domains_status(*, sandbox_root: str | Path | None = None) -> dict[str, Any]:
    """Lista estado de dominios sandbox desde una raiz explicita."""
    root_result = _resolve_sandbox_root(sandbox_root)
    if root_result.get("error"):
        return validate_domain_status_payload(
            _root_payload(
                sandbox_root="",
                status="blocked",
                domains=[],
                errors=[root_result["error"]],
                warnings=[],
            )
        )

    root = root_result["root"]
    domains: list[dict[str, Any]] = []
    root_errors: list[dict[str, Any]] = []
    root_warnings: list[dict[str, Any]] = []

    for domain_dir in _iter_sandbox_domain_dirs(root):
        item = get_domain_status_summary(domain_dir)
        domains.append(item)
        root_errors.extend(item.get("errors") or [])
        root_warnings.extend(item.get("warnings") or [])

    return validate_domain_status_payload(
        _root_payload(
            sandbox_root=str(root),
            status=SERVICE_STATUS,
            domains=domains,
            errors=root_errors,
            warnings=root_warnings,
        )
    )


def get_domain_status_summary(domain_dir: str | Path) -> dict[str, Any]:
    """Construye un summary seguro de un dominio sandbox materializado."""
    target = Path(domain_dir).resolve()
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    domain: dict[str, Any] = {}
    manifest: dict[str, Any] = {}
    artifact_kinds: list[str] = []
    artifact_types: list[str] = []

    try:
        validation = validate_materialized_sandbox_domain(target)
        domain = validation["domain"]
    except Exception as exc:  # noqa: BLE001 - se transforma en error contract
        errors.append(build_domain_status_error("DOMAIN_STATUS_NOT_LISTABLE", str(exc), field="domain.json"))
        domain = _load_domain_fallback(target)

    manifest_path = target / ARTIFACT_MANIFEST_RELATIVE_PATH
    if manifest_path.is_file():
        try:
            manifest = validate_artifact_manifest_file(manifest_path)
            artifact_types = [artifact["artifact_type"] for artifact in manifest["artifacts"]]
            artifact_kinds = [
                artifact.get("created_from", {}).get("artifact_kind") or artifact["artifact_type"]
                for artifact in manifest["artifacts"]
            ]
        except Exception as exc:  # noqa: BLE001 - se transforma en error contract
            errors.append(
                build_domain_status_error(
                    "INCONSISTENT_ARTIFACT_MANIFEST",
                    str(exc),
                    field="manifests/artifact_manifest.json",
                )
            )
    else:
        warnings.append(
            build_domain_status_error(
                "MISSING_ARTIFACT_MANIFEST",
                "artifact_manifest ausente para el dominio sandbox",
                severity="warning",
                field="manifests/artifact_manifest.json",
                recoverable=True,
            )
        )

    team_listing = (
        _team_listing_summary(target, errors)
        if manifest
        else {
            "has_sandbox_team": _has_sandbox_team_files(target),
            "has_team_read_model": False,
        }
    )
    audit_summary = _audit_pack_status(target, errors, warnings)
    has_rollback_report = _has_matching_json(target.parent / "_rollback_records", "*rollback*.json")
    has_regeneration_report = _has_matching_json(target, "*regeneration*.json")
    allowed_actions = ["view_status"]
    if domain:
        allowed_actions.append("view_details")
    if audit_summary["has_audit_pack"] and audit_summary["audit_pack_valid"]:
        allowed_actions.append("view_audit_pack_summary")

    item = {
        "domain_id": str(domain.get("domain_id") or target.name),
        "domain_name": str(domain.get("name") or target.name),
        "domain_status": str(domain.get("status") or "invalid"),
        "artifact_state": str(domain.get("artifact_state") or "invalid"),
        "readiness": DOMAIN_BLOCKED_READINESS if errors else DOMAIN_LISTABLE_READINESS,
        "artifact_count": len(manifest.get("artifacts") or []),
        "artifact_kinds": sorted(set(artifact_kinds)),
        "artifact_types": sorted(set(artifact_types)),
        "has_artifact_manifest": bool(manifest),
        "has_profile_catalog": "profile_catalog" in artifact_types or (target / "profile_catalog" / "profile_catalog.json").is_file(),
        "has_agent_presets": "agent_preset" in artifact_types or (target / "agent_presets" / "agent_presets.json").is_file(),
        "has_paper_seed": "paper_seed" in artifact_types or (target / "paper_seed" / "paper_seed.json").is_file(),
        "has_sandbox_agents": _has_sandbox_agents(target),
        "has_sandbox_team": team_listing["has_sandbox_team"],
        "has_team_read_model": team_listing["has_team_read_model"],
        "has_audit_pack": audit_summary["has_audit_pack"],
        "has_rollback_report": has_rollback_report,
        "has_regeneration_report": has_regeneration_report,
        "warnings_count": len(warnings),
        "errors_count": len(errors),
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": allowed_actions,
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "next_actions": _next_actions(errors, audit_summary),
        "errors": errors,
        "warnings": warnings,
        "validation": {
            "domain_json_present": (target / "domain.json").is_file(),
            "materialization_manifest_present": (target / MATERIALIZATION_MANIFEST).is_file(),
            "artifact_manifest_valid": bool(manifest),
            "team_read_model_available": team_listing["has_team_read_model"],
            "audit_pack_valid": audit_summary["audit_pack_valid"],
            "backend_authoritative": True,
            "json_safe": True,
            "read_only": True,
        },
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }
    _validate_domain_item(item)
    return item


def validate_domain_status_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida payload root de list_domains/status sin side effects."""
    if not isinstance(payload, dict):
        raise ValueError("domain status payload debe ser un objeto")
    required = {
        "service",
        "service_version",
        "status",
        "readiness",
        "domains",
        "summary",
        "warnings",
        "errors",
        "validation",
        "operational",
        "runtime_enabled",
        "execution_enabled",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"domain status payload incompleto: {', '.join(sorted(missing))}")
    if payload.get("service") != SERVICE_NAME:
        raise ValueError("service invalido")
    if payload.get("service_version") != SERVICE_VERSION:
        raise ValueError("service_version invalida")
    if payload.get("readiness") != SERVICE_READINESS:
        raise ValueError("readiness invalida")
    for field in ("domains", "warnings", "errors"):
        if not isinstance(payload.get(field), list):
            raise ValueError(f"{field} debe ser lista")
    if not isinstance(payload.get("summary"), dict) or not isinstance(payload.get("validation"), dict):
        raise ValueError("summary y validation deben ser objetos")
    for field in ("operational", "runtime_enabled", "execution_enabled"):
        if payload.get(field) is not False:
            raise ValueError(f"{field} debe ser false")
    _reject_sensitive_keys(payload)
    _reject_recursive_enabled_operation(payload)
    for domain in payload["domains"]:
        _validate_domain_item(domain)
    dumped = _ensure_json_safe(payload)
    if len(dumped.encode("utf-8")) > MAX_STATUS_PAYLOAD_JSON_BYTES:
        raise ValueError("domain status payload excede tamano maximo")
    return deepcopy(payload)


def build_domain_status_error(
    error_code: str,
    message: str,
    *,
    severity: str = "error",
    field: str = "",
    recoverable: bool = True,
) -> dict[str, Any]:
    """Construye error legible y JSON-safe para futura UI."""
    if error_code not in ERROR_CODES:
        error_code = "INVALID_DOMAIN_STATUS_PAYLOAD"
    error = {
        "error_code": error_code,
        "message": _safe_message(message),
        "severity": severity,
        "field": field,
        "recoverable": recoverable,
        "user_action": "revisar el estado informado por backend interno",
        "developer_hint": "mantener la decision en backend; la UI solo muestra este error",
        "blocked": severity in {"error", "critical"},
    }
    _ensure_json_safe(error)
    return error


def _root_payload(
    *,
    sandbox_root: str,
    status: str,
    domains: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "status": status,
        "verdict": SERVICE_VERDICT if not errors else "BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_BLOCKED",
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "sandbox_root": sandbox_root,
        "domains": domains,
        "summary": {
            "domains_count": len(domains),
            "listable_domains_count": sum(1 for domain in domains if domain["errors_count"] == 0),
            "blocked_domains_count": sum(1 for domain in domains if domain["errors_count"] > 0),
            "artifact_count": sum(domain["artifact_count"] for domain in domains),
            "domains_with_audit_pack": sum(1 for domain in domains if domain["has_audit_pack"]),
            "domains_with_team_read_model": sum(1 for domain in domains if domain["has_team_read_model"]),
            "warnings_count": len(warnings),
            "errors_count": len(errors),
            "backend_authoritative": True,
            "future_ui_must_not_infer_next_actions": True,
        },
        "warnings": warnings,
        "errors": errors,
        "validation": {
            "sandbox_root_explicit": bool(sandbox_root),
            "sandbox_root_controlled": status != "blocked",
            "json_safe": True,
            "read_only": True,
            "no_side_effects": True,
            "no_operational_capability_enabled": True,
        },
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _resolve_sandbox_root(sandbox_root: str | Path | None) -> dict[str, Any]:
    if sandbox_root in (None, ""):
        return {
            "error": build_domain_status_error(
                "SANDBOX_ROOT_REQUIRED",
                "sandbox_root explicito requerido",
                field="sandbox_root",
            )
        }
    root = Path(sandbox_root).resolve()
    unsafe_reason = _unsafe_root_reason(root)
    if unsafe_reason:
        return {
            "error": build_domain_status_error(
                "UNSAFE_SANDBOX_ROOT",
                unsafe_reason,
                field="sandbox_root",
                recoverable=False,
            )
        }
    if not root.exists() or not root.is_dir():
        return {
            "error": build_domain_status_error(
                "SANDBOX_ROOT_NOT_FOUND",
                "sandbox_root no existe o no es directorio",
                field="sandbox_root",
            )
        }
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


def _iter_sandbox_domain_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path.resolve()
        for path in root.iterdir()
        if path.is_dir() and path.name != "_rollback_records" and (path / "domain.json").is_file()
    )


def _team_listing_summary(domain_dir: Path, errors: list[dict[str, Any]]) -> dict[str, bool]:
    has_team = any((domain_dir / "sandbox_teams").glob("*.json")) if (domain_dir / "sandbox_teams").exists() else False
    if not has_team:
        return {"has_sandbox_team": False, "has_team_read_model": False}
    try:
        listing = list_sandbox_teams(domain_dir)
        return {
            "has_sandbox_team": listing.get("teams_count", 0) > 0,
            "has_team_read_model": listing.get("read_model") == "sandbox_team_internal_listing",
        }
    except Exception as exc:  # noqa: BLE001 - se transforma en error contract
        errors.append(build_domain_status_error("READ_MODEL_UNAVAILABLE", str(exc), field="sandbox_teams"))
        return {"has_sandbox_team": True, "has_team_read_model": False}


def _audit_pack_status(
    domain_dir: Path,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> dict[str, bool]:
    matches = sorted(domain_dir.glob("*audit_pack*.json"))
    if not matches:
        audit_dir = domain_dir / "audit"
        matches = sorted(audit_dir.glob("*audit_pack*.json")) if audit_dir.exists() else []
    if not matches:
        return {"has_audit_pack": False, "audit_pack_valid": False}
    try:
        payload = json.loads(matches[0].read_text(encoding="utf-8"))
        validate_sandbox_materialization_audit_pack(payload)
        return {"has_audit_pack": True, "audit_pack_valid": True}
    except Exception as exc:  # noqa: BLE001 - se transforma en error contract
        warning = build_domain_status_error(
            "INVALID_AUDIT_PACK",
            str(exc),
            severity="warning",
            field="audit_pack",
            recoverable=True,
        )
        warnings.append(warning)
        errors.append(warning)
        return {"has_audit_pack": True, "audit_pack_valid": False}


def _has_matching_json(root: Path, pattern: str) -> bool:
    if not root.exists() or not root.is_dir():
        return False
    return any(path.is_file() for path in root.glob(pattern))


def _has_sandbox_agents(domain_dir: Path) -> bool:
    agents_dir = domain_dir / "sandbox_agents"
    if not agents_dir.exists() or not agents_dir.is_dir():
        return False
    return any(path.is_file() and path.suffix == ".json" for path in agents_dir.glob("*.json"))


def _has_sandbox_team_files(domain_dir: Path) -> bool:
    teams_dir = domain_dir / "sandbox_teams"
    if not teams_dir.exists() or not teams_dir.is_dir():
        return False
    return any(path.is_file() and path.suffix == ".json" for path in teams_dir.glob("*.json"))


def _next_actions(errors: list[dict[str, Any]], audit_summary: dict[str, bool]) -> list[str]:
    if errors:
        return ["review_validation_errors"]
    actions = ["view_status", "view_details"]
    if audit_summary["has_audit_pack"] and audit_summary["audit_pack_valid"]:
        actions.append("view_audit_pack_summary")
    else:
        actions.append("await_audit_pack")
    return actions


def _load_domain_fallback(domain_dir: Path) -> dict[str, Any]:
    path = domain_dir / "domain.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _validate_domain_item(item: dict[str, Any]) -> None:
    required = {
        "domain_id",
        "domain_name",
        "domain_status",
        "artifact_state",
        "readiness",
        "artifact_count",
        "artifact_kinds",
        "has_artifact_manifest",
        "has_profile_catalog",
        "has_agent_presets",
        "has_paper_seed",
        "has_sandbox_agents",
        "has_sandbox_team",
        "has_team_read_model",
        "has_audit_pack",
        "has_rollback_report",
        "has_regeneration_report",
        "warnings_count",
        "errors_count",
        "blocked_capabilities",
        "allowed_actions",
        "forbidden_actions",
        "next_actions",
        "operational",
        "passed",
        "runtime_enabled",
        "execution_enabled",
    }
    missing = required - set(item)
    if missing:
        raise ValueError(f"domain status item incompleto: {', '.join(sorted(missing))}")
    for field in ("domain_id", "domain_name", "domain_status", "artifact_state", "readiness"):
        if not isinstance(item.get(field), str) or not item[field].strip():
            raise ValueError(f"{field} requerido")
    if item["domain_status"] in {"active", "running", "live", "operational"}:
        raise ValueError("domain_status operativo prohibido")
    if item["artifact_state"] in {"active", "running", "live", "operational"}:
        raise ValueError("artifact_state operativo prohibido")
    if not isinstance(item.get("artifact_count"), int) or item["artifact_count"] < 0:
        raise ValueError("artifact_count invalido")
    if not isinstance(item.get("artifact_kinds"), list):
        raise ValueError("artifact_kinds debe ser lista")
    if not isinstance(item.get("allowed_actions"), list) or not isinstance(item.get("forbidden_actions"), list):
        raise ValueError("acciones deben ser listas")
    destructive = {
        "materialize_without_preview",
        "rollback_without_confirmation",
        "delete_without_confirmation",
        "regenerate_without_rollback",
        "activate_runtime",
        "execute_agents",
        "invoke_models",
        "call_tools",
        "use_integrations",
        "write_operational_outputs",
        "open_ui_runtime",
    }
    if set(item["allowed_actions"]) & destructive:
        raise ValueError("allowed_actions contiene accion destructiva u operativa")
    if not destructive <= set(item["forbidden_actions"]):
        raise ValueError("forbidden_actions incompleto")
    if any(value is not False for value in item["blocked_capabilities"].values()):
        raise ValueError("blocked_capabilities debe mantener todo false")
    for field in ("operational", "passed", "runtime_enabled", "execution_enabled"):
        if item.get(field) is not False:
            raise ValueError(f"{field} debe ser false")


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


def _ensure_json_safe(payload: dict[str, Any]) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("domain status payload no es JSON-safe") from exc


def _safe_message(message: str) -> str:
    text = str(message).replace("\\", "/")
    repo_root = str(Path(__file__).resolve().parents[1]).replace("\\", "/")
    if repo_root in text:
        text = text.replace(repo_root, "<repo>")
    return text
