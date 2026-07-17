"""Schema y validacion de domain.json para dominios sandbox materializados."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import config
from core.artifact_state import ArtifactState, coerce_artifact_state
from core.domain_identity import domain_identity_keys, validate_unique_domain
from core.domain_registry import list_domains
from core.domain_state import DomainState, coerce_domain_state, validate_domain_state


SANDBOX_DOMAIN_SCHEMA_VERSION = "1.0"
SANDBOX_DOMAIN_TYPE = "sandbox"

REQUIRED_FIELDS = {
    "schema_version",
    "domain_id",
    "name",
    "description",
    "status",
    "domain_type",
    "source_request",
    "created_from",
    "materialization_id",
    "materialization_status",
    "artifact_state",
    "created_at",
    "updated_at",
    "human_review_required",
    "rollback_manifest",
    "validation",
    "warnings",
    "metadata",
}

ROLLBACK_REQUIRED_FIELDS = {
    "can_rollback",
    "created_paths",
    "modified_paths",
    "backup_paths",
    "notes",
}

ALLOWED_SANDBOX_STATES = {
    DomainState.MATERIALIZED,
    DomainState.VALIDATED,
    DomainState.CANDIDATE_FOR_ACTIVATION,
    DomainState.ARCHIVED,
    DomainState.BROKEN,
}

ALLOWED_CREATED_FROM_TYPES = {
    "preview",
    "manual_request",
    "test_fixture",
    "controlled_migration",
    "legacy_recovery",
}


def validate_sandbox_domain_schema(
    domain_data: dict[str, Any],
    *,
    existing_domains: list[dict[str, Any]] | None = None,
    allow_real_rollback_paths: bool = False,
) -> dict[str, Any]:
    """Valida un domain.json sandbox sin escribir ni registrar dominios."""
    if not isinstance(domain_data, dict):
        raise ValueError("domain.json sandbox debe ser un objeto")

    missing = REQUIRED_FIELDS - set(domain_data)
    if missing:
        raise ValueError(f"domain.json sandbox incompleto: {', '.join(sorted(missing))}")

    _ensure_json_serializable(domain_data)
    validated = deepcopy(domain_data)

    _validate_domain_id(validated)
    _validate_non_empty_text(validated.get("name"), "name")
    _validate_non_empty_text(validated.get("description"), "description")
    _validate_domain_type(validated)
    _validate_status(validated)
    _validate_artifact_state(validated)
    _validate_source_request(validated)
    _validate_created_from(validated)
    _validate_materialization_id(validated)
    _validate_rollback_manifest(
        validated,
        allow_real_rollback_paths=allow_real_rollback_paths,
    )
    _validate_human_review(validated)
    _validate_validation(validated)
    _validate_lists(validated)
    _validate_identity_uniqueness(validated, existing_domains=existing_domains)

    return validated


def is_valid_sandbox_domain(domain_data: dict[str, Any]) -> bool:
    try:
        validate_sandbox_domain_schema(domain_data)
    except (TypeError, ValueError):
        return False
    return True


def validate_sandbox_domain_file(
    path: str | Path,
    *,
    existing_domains: list[dict[str, Any]] | None = None,
    allow_real_rollback_paths: bool = False,
) -> dict[str, Any]:
    manifest_path = Path(path)
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"domain.json sandbox no es JSON valido: {exc}") from exc
    return validate_sandbox_domain_schema(
        data,
        existing_domains=existing_domains,
        allow_real_rollback_paths=allow_real_rollback_paths,
    )


def _validate_domain_id(domain_data: dict[str, Any]) -> None:
    domain_id = domain_data.get("domain_id")
    _validate_non_empty_text(domain_id, "domain_id")
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", str(domain_id)):
        raise ValueError("domain_id invalido: debe estar normalizado en snake_case")
    identity_record = {
        "id": domain_id,
        "nombre": domain_data.get("name"),
        "descripcion": domain_data.get("description"),
    }
    if not domain_identity_keys(identity_record):
        raise ValueError("domain_id invalido: no produce identidad de dominio")


def _validate_domain_type(domain_data: dict[str, Any]) -> None:
    if domain_data.get("domain_type") != SANDBOX_DOMAIN_TYPE:
        raise ValueError("domain_type invalido: debe ser sandbox")


def _validate_status(domain_data: dict[str, Any]) -> None:
    state = coerce_domain_state(domain_data.get("status"))
    if state is None:
        raise ValueError(f"status invalido: {domain_data.get('status')}")
    if state is DomainState.ACTIVE:
        validation = domain_data.get("validation")
        if not isinstance(validation, dict) or validation.get("passed") is not True:
            raise ValueError("status active requiere trazabilidad PASSED completa")
    if state not in ALLOWED_SANDBOX_STATES:
        raise ValueError(
            "status invalido para sandbox: use materialized, archived o broken"
        )

    state_payload = {
        "id": domain_data["domain_id"],
        "status": state.value,
        "visible_en_hud": False,
        "traceability": domain_data.get("created_from"),
    }
    if state is DomainState.BROKEN:
        state_payload["broken_reason"] = domain_data.get("validation", {}).get(
            "broken_reason",
            "Sandbox marcado como broken por validacion.",
        )
    validate_domain_state(state_payload)


def _validate_artifact_state(domain_data: dict[str, Any]) -> None:
    artifact_state = coerce_artifact_state(domain_data.get("artifact_state"))
    if artifact_state is None:
        raise ValueError(f"artifact_state invalido: {domain_data.get('artifact_state')}")
    if artifact_state is ArtifactState.ACTIVE:
        raise ValueError("artifact_state active no corresponde al schema sandbox inicial")
    if artifact_state not in {
        ArtifactState.MATERIALIZED,
        ArtifactState.VALIDATED,
        ArtifactState.CANDIDATE_FOR_ACTIVATION,
        ArtifactState.ARCHIVED,
        ArtifactState.BROKEN,
    }:
        raise ValueError("artifact_state invalido para sandbox materializado")
    if artifact_state.value != domain_data.get("status"):
        raise ValueError("artifact_state debe coincidir con status del dominio sandbox")


def _validate_source_request(domain_data: dict[str, Any]) -> None:
    source_request = domain_data.get("source_request")
    if not isinstance(source_request, dict) or not source_request:
        raise ValueError("source_request debe ser un objeto no vacio")


def _validate_created_from(domain_data: dict[str, Any]) -> None:
    created_from = domain_data.get("created_from")
    if not isinstance(created_from, dict) or not created_from:
        raise ValueError("created_from debe ser un objeto no vacio")
    source_type = created_from.get("type")
    if source_type not in ALLOWED_CREATED_FROM_TYPES:
        raise ValueError(
            "created_from.type invalido: use preview, manual_request, "
            "test_fixture, controlled_migration o legacy_recovery"
        )
    if source_type == "preview" and not created_from.get("preview_id"):
        raise ValueError("created_from preview requiere preview_id")


def _validate_materialization_id(domain_data: dict[str, Any]) -> None:
    _validate_non_empty_text(domain_data.get("materialization_id"), "materialization_id")
    if not re.fullmatch(r"[a-z0-9]+(?:[_-][a-z0-9]+)*", str(domain_data["materialization_id"])):
        raise ValueError("materialization_id invalido")
    _validate_non_empty_text(
        domain_data.get("materialization_status"),
        "materialization_status",
    )


def _validate_rollback_manifest(
    domain_data: dict[str, Any],
    *,
    allow_real_rollback_paths: bool,
) -> None:
    rollback = domain_data.get("rollback_manifest")
    if not isinstance(rollback, dict):
        raise ValueError("rollback_manifest debe ser un objeto")
    missing = ROLLBACK_REQUIRED_FIELDS - set(rollback)
    if missing:
        raise ValueError(
            f"rollback_manifest incompleto: {', '.join(sorted(missing))}"
        )
    if not isinstance(rollback.get("can_rollback"), bool):
        raise ValueError("rollback_manifest.can_rollback debe ser booleano")
    for field in ("created_paths", "modified_paths", "backup_paths", "notes"):
        if not isinstance(rollback.get(field), list):
            raise ValueError(f"rollback_manifest.{field} debe ser una lista")
    if not allow_real_rollback_paths:
        for field in ("created_paths", "modified_paths", "backup_paths"):
            for raw_path in rollback[field]:
                if _points_to_real_domains(raw_path):
                    raise ValueError(
                        f"rollback_manifest.{field} contiene path operativo real"
                    )


def _validate_human_review(domain_data: dict[str, Any]) -> None:
    if not isinstance(domain_data.get("human_review_required"), bool):
        raise ValueError("human_review_required debe estar presente como booleano")
    if domain_data["human_review_required"] is not True:
        raise ValueError("human_review_required debe ser true para sandbox inicial")


def _validate_validation(domain_data: dict[str, Any]) -> None:
    validation = domain_data.get("validation")
    if not isinstance(validation, dict):
        raise ValueError("validation debe ser un objeto")
    if validation.get("schema") != "sandbox_domain_schema":
        raise ValueError("validation.schema debe ser sandbox_domain_schema")
    if validation.get("schema_version") != SANDBOX_DOMAIN_SCHEMA_VERSION:
        raise ValueError("validation.schema_version invalida")
    if not isinstance(validation.get("validated"), bool):
        raise ValueError("validation.validated debe ser booleano")


def _validate_lists(domain_data: dict[str, Any]) -> None:
    if not isinstance(domain_data.get("warnings"), list):
        raise ValueError("warnings debe ser una lista")
    if not isinstance(domain_data.get("metadata"), dict):
        raise ValueError("metadata debe ser un objeto")
    _validate_non_empty_text(domain_data.get("created_at"), "created_at")
    _validate_non_empty_text(domain_data.get("updated_at"), "updated_at")


def _validate_identity_uniqueness(
    domain_data: dict[str, Any],
    *,
    existing_domains: list[dict[str, Any]] | None,
) -> None:
    candidate = {
        "id": domain_data["domain_id"],
        "nombre": domain_data["name"],
        "descripcion": domain_data["description"],
    }
    domains = list_domains(include_internal=True) if existing_domains is None else existing_domains
    validate_unique_domain(candidate, domains)


def _ensure_json_serializable(domain_data: dict[str, Any]) -> None:
    try:
        json.dumps(domain_data, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("domain.json sandbox debe ser serializable como JSON") from exc


def _validate_non_empty_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _points_to_real_domains(raw_path: Any) -> bool:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return False
    raw_text = raw_path.replace("\\", "/")
    domains_root = Path(config.DOMAINS_DIR).resolve()
    try:
        path = Path(raw_path)
        if path.is_absolute():
            resolved = path.resolve()
        else:
            resolved = (Path(config.ROOT_DIR) / path).resolve()
    except (OSError, RuntimeError, ValueError):
        resolved = None
    return (
        raw_text == "domains"
        or raw_text.startswith("domains/")
        or (resolved is not None and (resolved == domains_root or domains_root in resolved.parents))
    )
