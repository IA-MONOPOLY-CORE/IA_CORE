"""Servicios internos lifecycle controlados para dominios sandbox.

Implementa rollback/archive/delete/reset como acciones separadas, con
validacion previa, confirmacion explicita y paths limitados al sandbox.
"""

from __future__ import annotations

import json
import re
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from core.backend_internal_ui_contract import build_backend_internal_ui_forbidden_capabilities
from core.domain_materialization_rollback import (
    ROLLBACK_RECORDS_DIR,
    build_sandbox_domain_integral_rollback_plan,
    rollback_sandbox_domain_integral,
    validate_sandbox_domain_integral_rollback_plan,
)
from core.domain_materializer import MATERIALIZATION_MANIFEST


SERVICE_NAME = "domain_lifecycle"
SERVICE_VERSION = "0.1"
SERVICE_VERDICT = "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_READY"
SERVICE_CONTROLLED_ACTIONS_VERDICT = "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_CONTROLLED_ACTIONS_CONFIRMED"
SERVICE_NO_OPERATIONAL_VERDICT = "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_NO_OPERATIONAL_CONFIRMED"
SERVICE_READINESS = "ready_for_phase_7_6_stable_ui_payloads"
LIFECYCLE_RECORDS_DIR = "_lifecycle_records"
ARCHIVES_DIR = "_archives"
MAX_PAYLOAD_JSON_BYTES = 128_000

ROLLBACK_ACTION = "rollback_sandbox"
ARCHIVE_ACTION = "archive_sandbox_domain"
DELETE_ACTION = "delete_sandbox_domain"
RESET_ACTION = "reset_sandbox_domain"
ALLOWED_ACTIONS = (ROLLBACK_ACTION, ARCHIVE_ACTION, DELETE_ACTION, RESET_ACTION)
DESTRUCTIVE_ACTIONS = {ROLLBACK_ACTION, DELETE_ACTION, RESET_ACTION}

FORBIDDEN_ACTIONS = (
    "execute_agents",
    "activate_runtime",
    "invoke_models",
    "call_tools",
    "use_integrations",
    "open_ui_runtime",
    "mutate_manifest_directly",
    "delete_without_confirmation",
    "rollback_without_confirmation",
    "reset_without_confirmation",
)
ERROR_CODES = (
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
    "PATH_TRAVERSAL_BLOCKED",
    "DOMAINS_OPERATIVE_PATH_BLOCKED",
    "REPO_ROOT_PATH_BLOCKED",
    "OVERWRITE_BLOCKED",
    "ROLLBACK_NOT_READY",
    "ROLLBACK_FAILED",
    "ARCHIVE_NOT_SUPPORTED",
    "ARCHIVE_FAILED",
    "DELETE_NOT_ALLOWED",
    "DELETE_FAILED",
    "RESET_NOT_ALLOWED",
    "RESET_FAILED",
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


def rollback_sandbox(request: dict[str, Any] | None) -> dict[str, Any]:
    """Ejecuta rollback integral seguro de un dominio sandbox."""
    prepared = _prepare_request(request, expected_action=ROLLBACK_ACTION)
    if prepared.get("payload"):
        return prepared["payload"]
    root: Path = prepared["sandbox_root"]
    domain_id = prepared["domain_id"]
    materialization_id = prepared["materialization_id"]
    manifest_path = _domain_dir(root, domain_id) / MATERIALIZATION_MANIFEST

    try:
        if manifest_path.exists():
            plan = _build_integral_plan(manifest_path=manifest_path, root=root)
            _ensure_no_undeclared_paths(_domain_dir(root, domain_id), declared_paths=plan["planned_paths"], root=root)
        result = rollback_sandbox_domain_integral(manifest_path=manifest_path, sandbox_root=root)
        status = "already_rolled_back" if result.get("status") == "already_rolled_back_integral" else "rolled_back"
        return validate_domain_lifecycle_result(
            _result_payload(
                action=ROLLBACK_ACTION,
                status=status,
                root=root,
                domain_id=result.get("domain_id") or domain_id,
                materialization_id=result.get("materialization_id") or materialization_id,
                affected_paths=_relative_paths(result.get("removed_paths") or result.get("deleted_paths") or [], root=root),
                preserved_paths=_relative_paths(result.get("preserved_paths") or [], root=root),
                skipped_paths=_relative_paths(result.get("skipped_paths") or result.get("already_missing") or [], root=root),
                rollback_records=_rollback_record_summary(result, root=root),
                writes_performed=status == "rolled_back",
                destructive_operation_performed=status == "rolled_back" and bool(result.get("removed_paths") or result.get("deleted_paths")),
            )
        )
    except Exception as exc:
        return _blocked_result(ROLLBACK_ACTION, root, domain_id, materialization_id, _error_from_exception(exc, fallback="ROLLBACK_FAILED"))


def archive_sandbox_domain(request: dict[str, Any] | None) -> dict[str, Any]:
    """Archiva un dominio sandbox moviendolo dentro del sandbox controlado."""
    prepared = _prepare_request(request, expected_action=ARCHIVE_ACTION)
    if prepared.get("payload"):
        return prepared["payload"]
    root: Path = prepared["sandbox_root"]
    domain_id = prepared["domain_id"]
    materialization_id = prepared["materialization_id"]
    source = _domain_dir(root, domain_id)
    archive_dir = _archive_dir(root, domain_id, materialization_id)

    if archive_dir.exists() and not source.exists():
        record = _load_optional_json(archive_dir / "archive_record.json")
        return validate_domain_lifecycle_result(
            _result_payload(
                action=ARCHIVE_ACTION,
                status="already_archived",
                root=root,
                domain_id=domain_id,
                materialization_id=materialization_id,
                preserved_paths=[_relative_path(archive_dir, root=root)],
                archive_record=_archive_record_summary(record, archive_dir=archive_dir, root=root),
                writes_performed=False,
                destructive_operation_performed=False,
            )
        )
    if not source.is_dir():
        return _blocked_result(
            ARCHIVE_ACTION,
            root,
            domain_id,
            materialization_id,
            build_domain_lifecycle_error("DOMAIN_NOT_FOUND", "dominio sandbox no encontrado", field="domain_id"),
        )

    try:
        plan = _build_integral_plan(manifest_path=source / MATERIALIZATION_MANIFEST, root=root)
        _ensure_no_undeclared_paths(source, declared_paths=plan["planned_paths"], root=root)
        if archive_dir.exists():
            raise FileExistsError("archive target ya existe")
        _safe_child(root, ARCHIVES_DIR).mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(archive_dir))
        archived_paths = [_relative_path(path, root=root) for path in _walk_paths(archive_dir)]
        record = {
            "archive_id": _operation_id(ARCHIVE_ACTION, domain_id, materialization_id),
            "action": ARCHIVE_ACTION,
            "status": "archived",
            "domain_id": domain_id,
            "materialization_id": materialization_id,
            "archived_at": _now(),
            "archive_dir": _relative_path(archive_dir, root=root),
            "source_domain_dir": domain_id,
            "archived_paths": archived_paths,
            "reason": _safe_text(prepared["options"].get("reason") or "archive_sandbox_domain 7.5"),
            "operational": False,
            "runtime_enabled": False,
            "execution_enabled": False,
        }
        record_path = archive_dir / "archive_record.json"
        record["archived_paths"] = sorted(set([*record["archived_paths"], _relative_path(record_path, root=root)]))
        _write_json(record_path, record)
        return validate_domain_lifecycle_result(
            _result_payload(
                action=ARCHIVE_ACTION,
                status="archived",
                root=root,
                domain_id=domain_id,
                materialization_id=materialization_id,
                affected_paths=[domain_id, _relative_path(archive_dir, root=root)],
                preserved_paths=[_relative_path(archive_dir, root=root), _relative_path(record_path, root=root)],
                archive_record=_archive_record_summary(record, archive_dir=archive_dir, root=root),
                writes_performed=True,
                destructive_operation_performed=False,
            )
        )
    except Exception as exc:
        return _blocked_result(ARCHIVE_ACTION, root, domain_id, materialization_id, _error_from_exception(exc, fallback="ARCHIVE_FAILED"))


def delete_sandbox_domain(request: dict[str, Any] | None) -> dict[str, Any]:
    """Elimina un sandbox solo con confirmacion fuerte y paths declarados."""
    prepared = _prepare_request(request, expected_action=DELETE_ACTION)
    if prepared.get("payload"):
        return prepared["payload"]
    root: Path = prepared["sandbox_root"]
    domain_id = prepared["domain_id"]
    materialization_id = prepared["materialization_id"]
    options = prepared["options"]
    if options.get("allow_delete") is not True:
        return _blocked_result(
            DELETE_ACTION,
            root,
            domain_id,
            materialization_id,
            build_domain_lifecycle_error("DELETE_NOT_ALLOWED", "delete requiere allow_delete=true", field="options.allow_delete"),
        )
    return _delete_or_reset_target(
        action=DELETE_ACTION,
        root=root,
        domain_id=domain_id,
        materialization_id=materialization_id,
        already_status="already_deleted",
        done_status="deleted",
    )


def reset_sandbox_domain(request: dict[str, Any] | None) -> dict[str, Any]:
    """Deja el sandbox limpio sin regenerar ni materializar automaticamente."""
    prepared = _prepare_request(request, expected_action=RESET_ACTION)
    if prepared.get("payload"):
        return prepared["payload"]
    root: Path = prepared["sandbox_root"]
    domain_id = prepared["domain_id"]
    materialization_id = prepared["materialization_id"]
    options = prepared["options"]
    if options.get("allow_reset") is not True:
        return _blocked_result(
            RESET_ACTION,
            root,
            domain_id,
            materialization_id,
            build_domain_lifecycle_error("RESET_NOT_ALLOWED", "reset requiere allow_reset=true", field="options.allow_reset"),
        )
    return _delete_or_reset_target(
        action=RESET_ACTION,
        root=root,
        domain_id=domain_id,
        materialization_id=materialization_id,
        already_status="already_reset",
        done_status="reset",
    )


def build_domain_lifecycle_request(
    *,
    action: str,
    sandbox_root: str | Path,
    domain_id: str,
    materialization_id: str = "",
    validation_payload: dict[str, Any] | None = None,
    confirmation: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construye una request explicita para acciones lifecycle sandbox."""
    request = {
        "action": action,
        "sandbox_root": str(sandbox_root),
        "domain_id": domain_id,
        "materialization_id": materialization_id,
        "validation_payload": deepcopy(validation_payload or {}),
        "confirmation": deepcopy(confirmation)
        if confirmation is not None
        else {
            "confirmed": True,
            "confirmation_scope": action,
            "human_confirmation_required": True,
            "confirmed_by": "internal_backend",
            "confirmation_id": f"confirm_{_safe_id(action)}_{_safe_id(domain_id)}",
        },
        "options": {
            "dry_run": False,
            "preserve_rollback_records": True,
            "archive_before_delete": True,
            "allow_delete": False,
            "allow_reset": False,
            **(options or {}),
        },
    }
    _reject_sensitive_keys(request)
    _ensure_json_safe(request)
    return request


def validate_domain_lifecycle_request(request: dict[str, Any]) -> dict[str, Any]:
    """Valida request sin ejecutar la accion lifecycle."""
    if not isinstance(request, dict):
        raise ValueError("LIFECYCLE_ACTION_REQUIRED: request debe ser objeto")
    _reject_sensitive_keys(request)
    _ensure_json_safe(request)
    action = _validate_action(request.get("action"))
    root = _resolve_sandbox_root(request.get("sandbox_root"))
    domain_id = _validate_domain_id(request.get("domain_id"))
    materialization_id = _safe_text(str(request.get("materialization_id") or ""))
    validation_payload = _validate_previous_validation(request.get("validation_payload"), action=action, domain_id=domain_id, materialization_id=materialization_id)
    if not materialization_id:
        materialization_id = validation_payload.get("materialization_id", "")
    confirmation = _validate_confirmation(request.get("confirmation"), action=action)
    options = _lifecycle_options(request.get("options"))
    return {
        "action": action,
        "sandbox_root": str(root),
        "domain_id": domain_id,
        "materialization_id": materialization_id,
        "validation_payload": validation_payload,
        "confirmation": confirmation,
        "options": options,
    }


def validate_domain_lifecycle_result(payload: dict[str, Any]) -> dict[str, Any]:
    """Valida resultado lifecycle JSON-safe y no-operativo."""
    if not isinstance(payload, dict):
        raise ValueError("domain lifecycle result debe ser objeto")
    required = {
        "service",
        "service_version",
        "action",
        "status",
        "readiness",
        "domain_id",
        "materialization_id",
        "lifecycle_operation_id",
        "affected_paths",
        "preserved_paths",
        "blocked_paths",
        "skipped_paths",
        "rollback_records",
        "archive_record",
        "delete_record",
        "reset_record",
        "warnings",
        "errors",
        "blocked_capabilities",
        "allowed_actions",
        "forbidden_actions",
        "validation",
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "writes_performed",
        "destructive_operation_performed",
    }
    missing = required - set(payload)
    if missing:
        raise ValueError(f"domain lifecycle result incompleto: {', '.join(sorted(missing))}")
    if payload.get("service") != SERVICE_NAME:
        raise ValueError("service invalido")
    if payload.get("service_version") != SERVICE_VERSION:
        raise ValueError("service_version invalida")
    if payload.get("action") not in ALLOWED_ACTIONS:
        raise ValueError("action invalida")
    if payload.get("readiness") != SERVICE_READINESS:
        raise ValueError("readiness invalida")
    for field in ("operational", "runtime_enabled", "execution_enabled"):
        if payload.get(field) is not False:
            raise ValueError(f"{field} debe ser false")
    if payload.get("action") == ARCHIVE_ACTION and payload.get("destructive_operation_performed") is not False:
        raise ValueError("archive no debe declarar destructive_operation_performed")
    _validate_actions(payload)
    _reject_sensitive_keys(payload)
    encoded = _ensure_json_safe(payload)
    if len(encoded.encode("utf-8")) > MAX_PAYLOAD_JSON_BYTES:
        raise ValueError("domain lifecycle result excede tamano maximo")
    return deepcopy(payload)


def build_domain_lifecycle_error(
    error_code: str,
    message: str,
    *,
    field: str = "",
    severity: str = "error",
    recoverable: bool = True,
    blocked: bool = True,
) -> dict[str, Any]:
    """Construye un error seguro para futura UI."""
    code = error_code if error_code in ERROR_CODES else "INVALID_LIFECYCLE_ACTION"
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


def _prepare_request(request: dict[str, Any] | None, *, expected_action: str) -> dict[str, Any]:
    if not isinstance(request, dict):
        return {"payload": _blocked_result(expected_action, "", "", "", build_domain_lifecycle_error("LIFECYCLE_ACTION_REQUIRED", "request requerido"))}
    try:
        validated = validate_domain_lifecycle_request(request)
    except ValueError as exc:
        action = request.get("action") if isinstance(request.get("action"), str) else expected_action
        return {"payload": _blocked_result(action, "", "", "", _error_from_exception(exc, fallback="INVALID_LIFECYCLE_ACTION"))}
    if validated["action"] != expected_action:
        return {
            "payload": _blocked_result(
                expected_action,
                validated["sandbox_root"],
                validated["domain_id"],
                validated["materialization_id"],
                build_domain_lifecycle_error("INVALID_LIFECYCLE_ACTION", "accion no coincide con wrapper", field="action"),
            )
        }
    return {
        **validated,
        "sandbox_root": Path(validated["sandbox_root"]).resolve(),
    }


def _delete_or_reset_target(
    *,
    action: str,
    root: Path,
    domain_id: str,
    materialization_id: str,
    already_status: str,
    done_status: str,
) -> dict[str, Any]:
    target_info = _find_lifecycle_target(root, domain_id, materialization_id)
    record_path = _lifecycle_record_path(root, action, materialization_id)
    if target_info is None:
        if record_path.is_file():
            record = _load_optional_json(record_path)
            return validate_domain_lifecycle_result(
                _result_payload(
                    action=action,
                    status=already_status,
                    root=root,
                    domain_id=domain_id,
                    materialization_id=materialization_id,
                    skipped_paths=list(record.get("affected_paths", [])),
                    delete_record=_record_summary(record, root=root) if action == DELETE_ACTION else {},
                    reset_record=_record_summary(record, root=root) if action == RESET_ACTION else {},
                    writes_performed=False,
                    destructive_operation_performed=False,
                )
            )
        return _blocked_result(action, root, domain_id, materialization_id, build_domain_lifecycle_error("DOMAIN_NOT_FOUND", "dominio sandbox no encontrado"))

    target = target_info["path"]
    try:
        declared_paths = target_info["declared_paths"]
        _ensure_no_undeclared_paths(target, declared_paths=declared_paths, root=root)
        record = {
            "operation_id": _operation_id(action, domain_id, materialization_id),
            "action": action,
            "status": "in_progress",
            "domain_id": domain_id,
            "materialization_id": materialization_id,
            "target": _relative_path(target, root=root),
            "affected_paths": [_relative_path(path, root=root) for path in _walk_paths(target)],
            "started_at": _now(),
            "completed_at": None,
            "operational": False,
            "runtime_enabled": False,
            "execution_enabled": False,
        }
        record_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(record_path, record)
        _safe_remove_tree(target, root=root)
        record["status"] = done_status
        record["completed_at"] = _now()
        record["record_path"] = _relative_path(record_path, root=root)
        _write_json(record_path, record)
        return validate_domain_lifecycle_result(
            _result_payload(
                action=action,
                status=done_status,
                root=root,
                domain_id=domain_id,
                materialization_id=materialization_id,
                affected_paths=record["affected_paths"],
                preserved_paths=[_relative_path(record_path, root=root)],
                delete_record=_record_summary(record, root=root) if action == DELETE_ACTION else {},
                reset_record=_record_summary(record, root=root) if action == RESET_ACTION else {},
                writes_performed=True,
                destructive_operation_performed=True,
            )
        )
    except Exception as exc:
        return _blocked_result(action, root, domain_id, materialization_id, _error_from_exception(exc, fallback="DELETE_FAILED" if action == DELETE_ACTION else "RESET_FAILED"))


def _result_payload(
    *,
    action: str,
    status: str,
    root: str | Path,
    domain_id: str,
    materialization_id: str,
    affected_paths: list[str] | None = None,
    preserved_paths: list[str] | None = None,
    blocked_paths: list[str] | None = None,
    skipped_paths: list[str] | None = None,
    rollback_records: dict[str, Any] | None = None,
    archive_record: dict[str, Any] | None = None,
    delete_record: dict[str, Any] | None = None,
    reset_record: dict[str, Any] | None = None,
    warnings: list[dict[str, Any]] | None = None,
    errors: list[dict[str, Any]] | None = None,
    writes_performed: bool = False,
    destructive_operation_performed: bool = False,
) -> dict[str, Any]:
    root_text = str(root)
    has_errors = bool(errors)
    return {
        "service": SERVICE_NAME,
        "service_version": SERVICE_VERSION,
        "action": action,
        "status": "blocked" if has_errors else status,
        "verdict": "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_BLOCKED" if has_errors else SERVICE_VERDICT,
        "controlled_actions_verdict": SERVICE_CONTROLLED_ACTIONS_VERDICT,
        "non_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT,
        "readiness": SERVICE_READINESS,
        "domain_id": domain_id,
        "materialization_id": materialization_id,
        "lifecycle_operation_id": _operation_id(action, domain_id, materialization_id),
        "sandbox_root": root_text,
        "affected_paths": affected_paths or [],
        "preserved_paths": preserved_paths or [],
        "blocked_paths": blocked_paths or [],
        "skipped_paths": skipped_paths or [],
        "rollback_records": rollback_records or {},
        "archive_record": archive_record or {},
        "delete_record": delete_record or {},
        "reset_record": reset_record or {},
        "warnings": warnings or [],
        "errors": errors or [],
        "blocked_capabilities": build_backend_internal_ui_forbidden_capabilities(),
        "allowed_actions": _allowed_actions_for(action, status, has_errors=has_errors),
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "validation": {
            "action_valid": action in ALLOWED_ACTIONS,
            "sandbox_root_explicit": bool(root_text),
            "sandbox_root_controlled": bool(root_text),
            "validation_payload_required": True,
            "confirmation_explicit": True,
            "paths_checked": True,
            "domains_operational_untouched": True,
            "repo_root_protected": True,
            "no_runtime": True,
            "no_execution": True,
            "no_tools_or_models": True,
            "no_integrations": True,
            "json_safe": True,
        },
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "writes_performed": bool(writes_performed),
        "destructive_operation_performed": bool(destructive_operation_performed),
    }


def _blocked_result(
    action: str,
    root: str | Path,
    domain_id: str,
    materialization_id: str,
    error: dict[str, Any],
) -> dict[str, Any]:
    return validate_domain_lifecycle_result(
        _result_payload(
            action=action if action in ALLOWED_ACTIONS else ROLLBACK_ACTION,
            status="blocked",
            root=root,
            domain_id=domain_id,
            materialization_id=materialization_id,
            blocked_paths=[],
            errors=[error],
            writes_performed=False,
            destructive_operation_performed=False,
        )
    )


def _validate_action(raw: Any) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("LIFECYCLE_ACTION_REQUIRED: action requerida")
    action = raw.strip()
    if action not in ALLOWED_ACTIONS:
        raise ValueError("INVALID_LIFECYCLE_ACTION: action no permitida")
    return action


def _resolve_sandbox_root(raw: Any) -> Path:
    if raw in (None, ""):
        raise ValueError("SANDBOX_ROOT_REQUIRED: sandbox_root explicito requerido")
    text = str(raw)
    if any(part == ".." for part in Path(text).parts):
        raise ValueError("PATH_TRAVERSAL_BLOCKED: sandbox_root contiene traversal")
    root = Path(text).resolve()
    reason = _unsafe_root_reason(root)
    if reason:
        raise ValueError(f"UNSAFE_SANDBOX_ROOT: {reason}")
    if not root.exists() or not root.is_dir():
        raise ValueError("SANDBOX_ROOT_NOT_FOUND: sandbox_root no existe")
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
        raise ValueError("PATH_TRAVERSAL_BLOCKED: domain_id contiene traversal")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError("DOMAIN_ID_REQUIRED: domain_id debe ser snake_case")
    return value


def _validate_previous_validation(
    raw: Any,
    *,
    action: str,
    domain_id: str,
    materialization_id: str,
) -> dict[str, Any]:
    if not isinstance(raw, dict) or not raw:
        raise ValueError("VALIDATION_PAYLOAD_REQUIRED: validation_payload requerido")
    if raw.get("service") != "validate_domain":
        raise ValueError("INVALID_VALIDATION_PAYLOAD: service debe ser validate_domain")
    if raw.get("valid") is not True:
        raise ValueError("VALIDATION_NOT_PASSED: validation_payload.valid debe ser true")
    if raw.get("domain_id") != domain_id:
        raise ValueError("INVALID_VALIDATION_PAYLOAD: validation_payload.domain_id no coincide")
    payload_materialization_id = str(raw.get("materialization_id") or "")
    if materialization_id and payload_materialization_id and materialization_id != payload_materialization_id:
        raise ValueError("MATERIALIZATION_ID_MISMATCH: materialization_id no coincide")
    if action in DESTRUCTIVE_ACTIONS and raw.get("rollback_readiness", {}).get("ready") is not True:
        raise ValueError("ROLLBACK_NOT_READY: validation_payload no declara rollback readiness")
    return deepcopy(raw)


def _validate_confirmation(raw: Any, *, action: str) -> dict[str, Any]:
    if not isinstance(raw, dict) or not raw:
        raise ValueError("CONFIRMATION_REQUIRED: confirmacion requerida")
    if raw.get("confirmed") is not True:
        raise ValueError("CONFIRMATION_REQUIRED: confirmation.confirmed debe ser true")
    if raw.get("confirmation_scope") != action:
        raise ValueError("INVALID_CONFIRMATION_SCOPE: confirmation_scope no coincide con action")
    if raw.get("human_confirmation_required") is not True:
        raise ValueError("CONFIRMATION_REQUIRED: human_confirmation_required debe ser true")
    confirmed_by = str(raw.get("confirmed_by") or "").strip()
    confirmation_id = str(raw.get("confirmation_id") or "").strip()
    if not confirmed_by or not confirmation_id:
        raise ValueError("CONFIRMATION_REQUIRED: confirmed_by y confirmation_id requeridos")
    return {
        "confirmed": True,
        "confirmation_scope": action,
        "human_confirmation_required": True,
        "confirmed_by": _safe_text(confirmed_by),
        "confirmation_id": _safe_id(confirmation_id),
    }


def _lifecycle_options(raw: Any) -> dict[str, Any]:
    source = raw if isinstance(raw, dict) else {}
    return {
        "dry_run": source.get("dry_run") is True,
        "preserve_rollback_records": source.get("preserve_rollback_records") is not False,
        "archive_before_delete": source.get("archive_before_delete") is not False,
        "allow_delete": source.get("allow_delete") is True,
        "allow_reset": source.get("allow_reset") is True,
        "reason": _safe_text(source.get("reason") or ""),
    }


def _build_integral_plan(*, manifest_path: Path, root: Path) -> dict[str, Any]:
    if not manifest_path.is_file():
        raise FileNotFoundError("materialization_manifest no encontrado")
    plan = build_sandbox_domain_integral_rollback_plan(manifest_path=manifest_path, sandbox_root=root)
    return validate_sandbox_domain_integral_rollback_plan(plan)


def _ensure_no_undeclared_paths(target: Path, *, declared_paths: list[str], root: Path) -> None:
    target = target.resolve()
    _require_inside_root(target, root)
    declared = {str(Path(path).resolve()) for path in declared_paths}
    if str(target) not in declared:
        declared.add(str(target))
    undeclared = []
    for path in _walk_paths(target):
        _require_inside_root(path, root)
        _reject_repo_operational_path(path)
        if str(path.resolve()) not in declared:
            undeclared.append(path)
    if undeclared:
        names = ", ".join(_relative_path(path, root=root) for path in undeclared[:5])
        raise ValueError(f"UNDECLARED_PATH_BLOCKED: paths no declarados: {names}")


def _find_lifecycle_target(root: Path, domain_id: str, materialization_id: str) -> dict[str, Any] | None:
    active = _domain_dir(root, domain_id)
    if active.is_dir():
        plan = _build_integral_plan(manifest_path=active / MATERIALIZATION_MANIFEST, root=root)
        return {"path": active, "declared_paths": plan["planned_paths"], "source": "active"}
    archive = _archive_dir(root, domain_id, materialization_id)
    record_path = archive / "archive_record.json"
    if archive.is_dir() and record_path.is_file():
        record = _load_optional_json(record_path)
        declared = [str((root / path).resolve()) for path in record.get("archived_paths", [])]
        declared.append(str(archive.resolve()))
        return {"path": archive, "declared_paths": declared, "source": "archive"}
    return None


def _safe_remove_tree(target: Path, *, root: Path) -> None:
    target = target.resolve()
    _require_inside_root(target, root)
    if target == root:
        raise ValueError("REPO_ROOT_PATH_BLOCKED: no se puede borrar sandbox_root")
    _reject_repo_operational_path(target)
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


def _domain_dir(root: Path, domain_id: str) -> Path:
    return _safe_child(root, domain_id)


def _archive_dir(root: Path, domain_id: str, materialization_id: str) -> Path:
    safe_name = f"{_safe_id(domain_id)}__{_safe_id(materialization_id or 'unknown')}"
    return _safe_child(root, Path(ARCHIVES_DIR) / safe_name)


def _lifecycle_record_path(root: Path, action: str, materialization_id: str) -> Path:
    return _safe_child(root, Path(LIFECYCLE_RECORDS_DIR) / f"{_safe_id(action)}__{_safe_id(materialization_id or 'unknown')}.json")


def _safe_child(root: Path, relative: str | Path) -> Path:
    if Path(relative).is_absolute():
        raise ValueError("UNSAFE_CREATED_PATH: path absoluto no permitido")
    if any(part == ".." for part in Path(relative).parts):
        raise ValueError("PATH_TRAVERSAL_BLOCKED: path contiene traversal")
    target = (root / relative).resolve()
    _require_inside_root(target, root)
    _reject_repo_operational_path(target)
    return target


def _require_inside_root(path: Path, root: Path) -> None:
    path = path.resolve()
    root = root.resolve()
    if path != root and root not in path.parents:
        raise ValueError("UNSAFE_CREATED_PATH: path fuera de sandbox_root")


def _reject_repo_operational_path(path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    domains_root = (repo_root / "domains").resolve()
    path = path.resolve()
    if path == repo_root:
        raise ValueError("REPO_ROOT_PATH_BLOCKED: repo root protegido")
    if path == domains_root or domains_root in path.parents:
        raise ValueError("DOMAINS_OPERATIVE_PATH_BLOCKED: domains operativo protegido")
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return
    protected = {".git", "core", "docs", "tests"}
    if set(relative.parts) & protected:
        raise ValueError("REPO_ROOT_PATH_BLOCKED: ruta interna del repo protegida")


def _walk_paths(root: Path) -> list[Path]:
    root = root.resolve()
    paths = [root]
    if not root.exists():
        return paths
    stack = [root]
    while stack:
        current = stack.pop()
        if current.is_dir():
            for child in sorted(current.iterdir(), key=lambda item: item.name):
                paths.append(child.resolve())
                if child.is_dir():
                    stack.append(child)
    return sorted(paths, key=lambda path: len(path.parts), reverse=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _rollback_record_summary(result: dict[str, Any], *, root: Path) -> dict[str, Any]:
    record_path = result.get("rollback_record_path")
    return {
        "rollback_id": result.get("rollback_id", ""),
        "rollback_scope": result.get("rollback_scope", "sandbox_domain_integral"),
        "status": result.get("status", ""),
        "record_path": _relative_path(record_path, root=root) if record_path else "",
        "records_dir": ROLLBACK_RECORDS_DIR,
        "preserved": bool(record_path),
    }


def _archive_record_summary(record: dict[str, Any], *, archive_dir: Path, root: Path) -> dict[str, Any]:
    return {
        "archive_id": record.get("archive_id", ""),
        "status": record.get("status", "already_archived"),
        "archive_dir": _relative_path(archive_dir, root=root),
        "archived_paths_count": len(record.get("archived_paths") or []),
        "record_path": _relative_path(archive_dir / "archive_record.json", root=root),
    }


def _record_summary(record: dict[str, Any], *, root: Path) -> dict[str, Any]:
    return {
        "operation_id": record.get("operation_id", ""),
        "action": record.get("action", ""),
        "status": record.get("status", ""),
        "record_path": record.get("record_path", ""),
        "affected_paths_count": len(record.get("affected_paths") or []),
        "target": record.get("target", ""),
    }


def _relative_paths(paths: list[Any], *, root: Path) -> list[str]:
    return [_relative_path(path, root=root) for path in paths]


def _relative_path(path: Any, *, root: Path) -> str:
    target = Path(str(path)).resolve()
    if target == root:
        return "."
    if root in target.parents:
        return target.relative_to(root).as_posix()
    return _safe_text(Path(str(path)).name)


def _allowed_actions_for(action: str, status: str, *, has_errors: bool) -> list[str]:
    if has_errors:
        return ["view_status"]
    if action == ROLLBACK_ACTION:
        return ["view_status", "view_lifecycle_report", "request_preview_next_step", "request_materialization_next_step"]
    if action == ARCHIVE_ACTION:
        return ["view_status", "view_archive_record", "request_delete_next_step"]
    if action == DELETE_ACTION:
        return ["view_lifecycle_report", "request_preview_next_step"]
    if action == RESET_ACTION:
        return ["view_status", "request_preview_next_step"]
    return ["view_status"]


def _validate_actions(payload: dict[str, Any]) -> None:
    forbidden_allowed = {
        "execute_agents",
        "activate_runtime",
        "invoke_models",
        "call_tools",
        "use_integrations",
        "open_ui_runtime",
        "mutate_manifest_directly",
        "delete_without_confirmation",
        "rollback_without_confirmation",
        "reset_without_confirmation",
    }
    if set(payload.get("allowed_actions") or []) & forbidden_allowed:
        raise ValueError("allowed_actions contiene acciones prohibidas")
    required = {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"}
    if not required <= set(payload.get("forbidden_actions") or []):
        raise ValueError("forbidden_actions incompleto")


def _reject_sensitive_keys(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            lowered = key_text.lower()
            if key_text not in ALLOWED_SENSITIVE_DECLARATION_KEYS and any(fragment in lowered for fragment in SENSITIVE_KEY_FRAGMENTS):
                raise ValueError(f"SECRET_LIKE_FIELD_BLOCKED: campo sensible bloqueado en {path}.{key_text}")
            _reject_sensitive_keys(value, f"{path}.{key_text}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_sensitive_keys(value, f"{path}[{index}]")


def _ensure_json_safe(payload: Any) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("PAYLOAD_NOT_JSON_SAFE: payload no serializable") from exc


def _error_from_exception(exc: Exception, *, fallback: str) -> dict[str, Any]:
    message = str(exc)
    code = message.split(":", 1)[0]
    if code not in ERROR_CODES:
        code = fallback
    if "artifact_manifest" in message and "no encontrado" in message:
        code = "MISSING_ARTIFACT_MANIFEST"
    elif "created_paths" in message and "sin" in message:
        code = "MISSING_CREATED_PATHS"
    elif "UNDECLARED_PATH_BLOCKED" in message:
        code = "UNDECLARED_PATH_BLOCKED"
    elif "fuera de sandbox" in message or "UNSAFE_CREATED_PATH" in message:
        code = "UNSAFE_CREATED_PATH"
    elif "domains" in message:
        code = "DOMAINS_OPERATIVE_PATH_BLOCKED"
    elif "repo root" in message or "repo protegida" in message:
        code = "REPO_ROOT_PATH_BLOCKED"
    elif "ya existe" in message:
        code = "OVERWRITE_BLOCKED"
    elif "SECRET_LIKE_FIELD_BLOCKED" in message:
        code = "SECRET_LIKE_FIELD_BLOCKED"
    elif "PAYLOAD_NOT_JSON_SAFE" in message:
        code = "PAYLOAD_NOT_JSON_SAFE"
    return build_domain_lifecycle_error(code, message, recoverable=code not in {"SECRET_LIKE_FIELD_BLOCKED", "DOMAINS_OPERATIVE_PATH_BLOCKED", "REPO_ROOT_PATH_BLOCKED"})


def _operation_id(action: str, domain_id: str, materialization_id: str) -> str:
    return f"{_safe_id(action)}_{_safe_id(domain_id)}_{_safe_id(materialization_id or 'unknown')}"


def _safe_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", str(value).strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "unknown"


def _safe_text(value: Any) -> str:
    return str(value).replace("\r", " ").replace("\n", " ")[:240]


def _now() -> str:
    return datetime.now().isoformat()


def _user_action_for(code: str) -> str:
    return {
        "CONFIRMATION_REQUIRED": "Confirmar la accion solicitada.",
        "INVALID_CONFIRMATION_SCOPE": "Usar confirmation_scope igual a la accion.",
        "VALIDATION_PAYLOAD_REQUIRED": "Ejecutar validate_domain antes de la accion.",
        "VALIDATION_NOT_PASSED": "Resolver errores de validacion antes de continuar.",
        "DELETE_NOT_ALLOWED": "Enviar allow_delete=true si corresponde.",
        "RESET_NOT_ALLOWED": "Enviar allow_reset=true si corresponde.",
        "UNDECLARED_PATH_BLOCKED": "Revisar residuos no declarados.",
    }.get(code, "Revisar request lifecycle y reintentar.")


def _developer_hint_for(code: str) -> str:
    return {
        "UNDECLARED_PATH_BLOCKED": "No se borran/mueven paths fuera de manifests/created_paths.",
        "UNSAFE_SANDBOX_ROOT": "sandbox_root no debe apuntar a repo, domains ni carpetas internas.",
        "ROLLBACK_FAILED": "Revisar materialization_manifest y artifact_manifest.",
        "ARCHIVE_FAILED": "Revisar target de archivo y overwrite.",
    }.get(code, "Error controlado de domain lifecycle 7.5.")
