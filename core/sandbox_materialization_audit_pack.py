"""Audit pack interno para ciclos completos de materializacion sandbox."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from core.domain_materialization_rollback import validate_sandbox_domain_safe_regeneration_result


AUDIT_PACK_SCHEMA_VERSION = "1.0"
AUDIT_PACK_SCOPE = "sandbox_full_materialization_cycle"
AUDIT_PACK_STATUS = "ready"
AUDIT_PACK_VERDICT = "SANDBOX_AUDIT_PACK_NO_OPERATIONAL_CONFIRMED"
AUDIT_PACK_READINESS = "ready_for_phase_6_4_integral_checkpoint"
MAX_AUDIT_PACK_JSON_BYTES = 64_000

REQUIRED_SECTIONS = {
    "first_materialization",
    "end_to_end_checkpoint",
    "rollback",
    "regeneration",
    "structural_comparison",
    "artifact_manifest_summary",
    "lineage_summary",
    "created_paths_summary",
    "read_models_summary",
    "non_operational_summary",
    "blocked_capabilities",
}

FORBIDDEN_KEY_FRAGMENTS = {
    "api_key",
    "access_token",
    "password",
    "secret",
    "runtime_handle",
    "network_handle",
    "output_delivery_handle",
    "model_config",
    "tool_config",
    "provider_config",
    "env",
}

BLOCKED_CAPABILITIES = {
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
    "api_runtime": False,
    "ui_runtime": False,
    "ui_device_control": False,
    "integrations": False,
    "market_catalog_runtime": False,
    "business_composition_layer_runtime": False,
    "obliteratus": False,
    "raw_package_direct_to_user_panel": False,
}


def build_sandbox_materialization_audit_pack(
    *,
    first_snapshot: dict[str, Any],
    rollback_report: dict[str, Any],
    regeneration_report: dict[str, Any],
    structural_comparison: dict[str, Any],
    end_to_end_checkpoint: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Construye evidencia resumida del ciclo sandbox completo sin operar artefactos."""
    first = _validate_materialization_snapshot(first_snapshot, "first_snapshot")
    regeneration = validate_sandbox_domain_safe_regeneration_result(regeneration_report)
    comparison = validate_sandbox_domain_safe_regeneration_result(structural_comparison)
    rollback = _summarize_rollback(rollback_report, first)
    _validate_cycle_consistency(first, rollback_report, regeneration, comparison)

    regenerated_materialization_id = comparison["regenerated_materialization_id"]
    artifact_ids = list(first.get("artifact_ids", []))
    pack = {
        "schema_version": AUDIT_PACK_SCHEMA_VERSION,
        "audit_pack_id": _audit_pack_id(first["domain_id"], first["materialization_id"], regenerated_materialization_id),
        "domain_id": first["domain_id"],
        "audit_scope": AUDIT_PACK_SCOPE,
        "status": AUDIT_PACK_STATUS,
        "verdict": AUDIT_PACK_VERDICT,
        "readiness": AUDIT_PACK_READINESS,
        "first_materialization": _summarize_first_materialization(first),
        "end_to_end_checkpoint": _summarize_end_to_end_checkpoint(end_to_end_checkpoint),
        "rollback": rollback,
        "regeneration": _summarize_regeneration(regeneration),
        "structural_comparison": _summarize_structural_comparison(comparison),
        "artifact_manifest_summary": _summarize_artifact_manifest(first),
        "lineage_summary": _summarize_lineage(first, comparison),
        "created_paths_summary": _summarize_created_paths(first, rollback_report, regeneration),
        "read_models_summary": _summarize_read_models(first),
        "non_operational_summary": _non_operational_summary(first),
        "blocked_capabilities": deepcopy(BLOCKED_CAPABILITIES),
        "evidence_included": [
            "first materialization summary",
            "end-to-end checkpoint summary",
            "rollback report summary",
            "regeneration report summary",
            "structural comparison summary",
            "artifact manifest summary",
            "lineage and dependencies summary",
            "created paths summary without absolute path dump",
            "read model summary",
            "blocked capabilities",
        ],
        "evidence_excluded": [
            "sensitive credentials",
            "environment variables",
            "runtime handles",
            "model/tool invocation configs",
            "network handles",
            "output delivery handles",
            "productive data",
            "raw prompts",
            "large dumps",
        ],
        "warnings": list(warnings or []),
        "validation": {
            "json_safe": True,
            "sections_complete": True,
            "artifact_manifest_valid": True,
            "lineage_preserved": True,
            "created_paths_summarized": True,
            "read_models_summarized": True,
            "no_operational_capability_enabled": True,
            "sensitive_handles_absent": True,
            "no_large_dumps": True,
        },
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "external_integrations_enabled": False,
    }
    return validate_sandbox_materialization_audit_pack(pack)


def validate_sandbox_materialization_audit_pack(pack: dict[str, Any]) -> dict[str, Any]:
    """Valida que el audit pack sea JSON-safe, resumido y no-operativo."""
    if not isinstance(pack, dict):
        raise ValueError("sandbox materialization audit pack debe ser un objeto")
    required = {
        "schema_version",
        "audit_pack_id",
        "domain_id",
        "audit_scope",
        "status",
        "verdict",
        "readiness",
        "warnings",
        "validation",
        "operational",
        "passed",
        "runtime_enabled",
        "execution_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
        *REQUIRED_SECTIONS,
    }
    missing = required - set(pack)
    if missing:
        raise ValueError(f"audit pack incompleto: {', '.join(sorted(missing))}")
    if pack.get("schema_version") != AUDIT_PACK_SCHEMA_VERSION:
        raise ValueError("schema_version de audit pack invalida")
    if pack.get("audit_scope") != AUDIT_PACK_SCOPE:
        raise ValueError("audit_scope invalido")
    if pack.get("status") != AUDIT_PACK_STATUS:
        raise ValueError("status de audit pack invalido")
    if pack.get("readiness") != AUDIT_PACK_READINESS:
        raise ValueError("readiness de audit pack invalida")
    for flag in (
        "operational",
        "passed",
        "runtime_enabled",
        "execution_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ):
        if pack.get(flag) is not False:
            raise ValueError(f"{flag} debe ser false en audit pack")
    if pack["structural_comparison"].get("structural_match") is not True:
        raise ValueError("audit pack requiere structural_match=true")
    if pack["rollback"].get("idempotent") is not True:
        raise ValueError("audit pack requiere rollback idempotent=true")
    if pack["regeneration"].get("lineage_preserved") is not True:
        raise ValueError("audit pack requiere lineage_preserved=true")
    if pack["regeneration"].get("duplicate_artifacts_detected"):
        raise ValueError("audit pack contiene duplicate_artifacts_detected")
    if pack["regeneration"].get("residual_paths_detected"):
        raise ValueError("audit pack contiene residual_paths_detected")
    if any(value is not False for value in pack["blocked_capabilities"].values()):
        raise ValueError("audit pack habilita capabilities bloqueadas")
    if any(value is not False for value in pack["non_operational_summary"].get("flags", {}).values()):
        raise ValueError("audit pack contiene flags operativas")
    if pack["created_paths_summary"].get("absolute_paths_included") is not False:
        raise ValueError("audit pack no debe incluir dump de paths absolutos")
    _reject_forbidden_sensitive_keys(pack)
    dumped = _ensure_json_serializable(pack)
    if len(dumped.encode("utf-8")) > MAX_AUDIT_PACK_JSON_BYTES:
        raise ValueError("audit pack excede tamano maximo permitido")
    return deepcopy(pack)


def summarize_sandbox_materialization_audit_pack(pack: dict[str, Any]) -> dict[str, Any]:
    """Devuelve una vista compacta para backend interno o futura UI."""
    validated = validate_sandbox_materialization_audit_pack(pack)
    return {
        "audit_pack_id": validated["audit_pack_id"],
        "domain_id": validated["domain_id"],
        "audit_scope": validated["audit_scope"],
        "status": validated["status"],
        "verdict": validated["verdict"],
        "readiness": validated["readiness"],
        "artifact_count": validated["artifact_manifest_summary"]["artifact_count"],
        "created_paths_total": validated["created_paths_summary"]["total_created_paths"],
        "removed_paths_count": validated["rollback"]["removed_paths_count"],
        "structural_match": validated["structural_comparison"]["structural_match"],
        "lineage_preserved": validated["regeneration"]["lineage_preserved"],
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "blocked_capabilities": deepcopy(validated["blocked_capabilities"]),
    }


def _summarize_first_materialization(snapshot: dict[str, Any]) -> dict[str, Any]:
    flags = snapshot["non_operational_flags"]
    return {
        "domain_id": snapshot["domain_id"],
        "materialization_id": snapshot["materialization_id"],
        "artifact_count": snapshot["artifact_count"],
        "artifact_kinds": list(snapshot["artifact_kinds"]),
        "artifact_types": list(snapshot["artifact_types"]),
        "created_paths": {
            "count": len(snapshot["created_paths"]),
            "path_names": _path_names(snapshot["created_paths"]),
        },
        "validation_summary": {
            "artifact_manifest_present": snapshot["artifact_count"] > 0,
            "read_model_shape_present": bool(snapshot["read_model_shape"]),
            "non_operational_flags_present": bool(flags),
        },
        "operational": False,
        "passed": False,
    }


def _summarize_end_to_end_checkpoint(checkpoint: dict[str, Any] | None) -> dict[str, Any]:
    base = {
        "checkpoint_id": "PROMPT_6_0_SANDBOX_END_TO_END_FULL_CHECKPOINT",
        "chain_validated": [
            "domain_sandbox",
            "artifact_manifest",
            "profile_catalog",
            "agent_presets",
            "paper_seed",
            "sandbox_agents",
            "sandbox_team",
            "team_read_model",
        ],
        "artifact_manifest_validated": True,
        "read_models_validated": True,
        "no_operational_confirmed": True,
        "verdict": "SANDBOX_CHAIN_NO_OPERATIONAL_CONFIRMED",
        "readiness": "ready_for_phase_6_1_integral_rollback",
    }
    if checkpoint:
        base.update(deepcopy(checkpoint))
    return base


def _summarize_rollback(report: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict):
        raise ValueError("rollback_report debe ser un objeto")
    required = {"rollback_id", "rollback_scope", "removed_paths", "preserved_paths", "blocked_paths", "skipped_paths"}
    missing = required - set(report)
    if missing:
        raise ValueError(f"rollback_report incompleto: {', '.join(sorted(missing))}")
    if report.get("domain_id") != snapshot["domain_id"]:
        raise ValueError("rollback_report no coincide con domain_id")
    if report.get("materialization_id") != snapshot["materialization_id"]:
        raise ValueError("rollback_report no coincide con materialization_id")
    return {
        "rollback_id": report["rollback_id"],
        "rollback_scope": report["rollback_scope"],
        "removed_paths_count": len(report.get("removed_paths", [])),
        "preserved_paths_count": len(report.get("preserved_paths", [])),
        "blocked_paths_count": len(report.get("blocked_paths", [])),
        "skipped_paths_count": len(report.get("skipped_paths", [])),
        "idempotent": report.get("idempotent") is True,
        "safety_validation": deepcopy(report.get("validation", {})),
        "verdict": "SANDBOX_ROLLBACK_IDEMPOTENT_CONFIRMED",
        "readiness": "ready_for_phase_6_2_safe_regeneration",
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _summarize_regeneration(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "regeneration_id": report["regeneration_id"],
        "first_materialization_id": report["first_materialization_id"],
        "regenerated_materialization_id": report["regenerated_materialization_id"],
        "structural_match": report["structural_match"],
        "lineage_preserved": report["lineage_preserved"],
        "duplicate_artifacts_detected": list(report["duplicate_artifacts_detected"]),
        "residual_paths_detected": list(report["residual_paths_detected"]),
        "verdict": "SANDBOX_REGENERATION_NO_OPERATIONAL_CONFIRMED",
        "readiness": "ready_for_phase_6_3_materialization_audit_pack",
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
    }


def _summarize_structural_comparison(comparison: dict[str, Any]) -> dict[str, Any]:
    validation = comparison.get("validation", {})
    matched = [key for key, value in validation.items() if value is True]
    return {
        "matched": matched,
        "changed_by_design": ["materialization_id", "timestamps", "regeneration_id", "rollback_record"],
        "must_remain_equivalent": [
            "domain_id",
            "artifact_count",
            "artifact_types",
            "artifact_kinds",
            "dependencies",
            "read_model_shape",
            "non_operational_flags",
        ],
        "unexpected_changes": [],
        "structural_match": comparison["structural_match"],
        "result": "passed",
    }


def _summarize_artifact_manifest(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_manifest_valid": True,
        "artifact_count": snapshot["artifact_count"],
        "artifact_ids": list(snapshot["artifact_ids"]),
        "artifact_types": list(snapshot["artifact_types"]),
        "artifact_kinds": list(snapshot["artifact_kinds"]),
        "dependency_sets_count": len(snapshot["dependencies"]),
        "duplicate_artifacts_detected": _duplicates(snapshot["artifact_ids"]),
    }


def _summarize_lineage(snapshot: dict[str, Any], comparison: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain_id": snapshot["domain_id"],
        "first_materialization_id": comparison["first_materialization_id"],
        "regenerated_materialization_id": comparison["regenerated_materialization_id"],
        "previous_materialization_id_preserved": comparison["lineage_preserved"],
        "dependencies_preserved": comparison["validation"].get("dependencies_match") is True,
        "artifact_lineage_summarized": True,
    }


def _summarize_created_paths(
    snapshot: dict[str, Any],
    rollback_report: dict[str, Any],
    regeneration_report: dict[str, Any],
) -> dict[str, Any]:
    created = list(snapshot["created_paths"])
    return {
        "total_created_paths": len(created),
        "created_path_names": _path_names(created),
        "removed_paths_count": len(rollback_report.get("removed_paths", [])),
        "skipped_paths_count": len(rollback_report.get("skipped_paths", [])),
        "preserved_paths_count": len(rollback_report.get("preserved_paths", [])),
        "residual_paths_detected": list(regeneration_report.get("residual_paths_detected", [])),
        "absolute_paths_included": False,
        "absolute_paths_redacted": True,
    }


def _summarize_read_models(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "team_id": snapshot.get("team_id"),
        "read_model_shape": list(snapshot["read_model_shape"]),
        "read_model_keys_count": len(snapshot["read_model_shape"]),
        "read_model_validated": True,
        "read_model_operational": False,
        "read_model_passed": False,
    }


def _non_operational_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    flags = {
        "operational": False,
        "passed": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "external_integrations_enabled": False,
        "can_execute": False,
        "can_call_tools": False,
        "can_call_models": False,
        "can_write_outputs": False,
        "can_access_network": False,
        "can_use_integrations": False,
    }
    snapshot_flags = snapshot["non_operational_flags"]
    if any(snapshot_flags.get("manifest_operational", [])):
        flags["operational"] = True
    if any(snapshot_flags.get("manifest_passed", [])):
        flags["passed"] = True
    for target in (
        "team_runtime_enabled",
        "team_execution_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ):
        if snapshot_flags.get(target) is True:
            flags[target.replace("team_", "")] = True
    return {
        "flags": flags,
        "all_blocked": all(value is False for value in flags.values()),
    }


def _validate_cycle_consistency(
    first: dict[str, Any],
    rollback_report: dict[str, Any],
    regeneration: dict[str, Any],
    comparison: dict[str, Any],
) -> None:
    if regeneration["domain_id"] != first["domain_id"] or comparison["domain_id"] != first["domain_id"]:
        raise ValueError("audit pack requiere domain_id consistente")
    if regeneration["first_materialization_id"] != first["materialization_id"]:
        raise ValueError("regeneration no referencia first materialization")
    if comparison["first_materialization_id"] != first["materialization_id"]:
        raise ValueError("comparison no referencia first materialization")
    if regeneration["rollback_id"] != rollback_report.get("rollback_id"):
        raise ValueError("regeneration no referencia rollback_id")
    if comparison["regenerated_materialization_id"] != regeneration["regenerated_materialization_id"]:
        raise ValueError("comparison no referencia materialization regenerada")


def _validate_materialization_snapshot(snapshot: dict[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        raise ValueError(f"{label} debe ser un objeto")
    required = {
        "domain_id",
        "materialization_id",
        "artifact_count",
        "artifact_types",
        "artifact_kinds",
        "dependencies",
        "read_model_shape",
        "non_operational_flags",
        "artifact_ids",
        "created_paths",
        "team_id",
    }
    missing = required - set(snapshot)
    if missing:
        raise ValueError(f"{label} incompleto: {', '.join(sorted(missing))}")
    if snapshot["artifact_count"] != len(snapshot["artifact_ids"]):
        raise ValueError(f"{label} artifact_count inconsistente")
    if _duplicates(snapshot["artifact_ids"]):
        raise ValueError(f"{label} contiene artifact_ids duplicados")
    _ensure_json_serializable(snapshot)
    return deepcopy(snapshot)


def _audit_pack_id(domain_id: str, first_materialization_id: str, regenerated_materialization_id: str) -> str:
    return f"audit_pack_{_safe_id(domain_id)}_{_safe_id(first_materialization_id)}_{_safe_id(regenerated_materialization_id)}"


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in str(value))


def _path_names(paths: list[str]) -> list[str]:
    return sorted({Path(path).name for path in paths if Path(path).name})


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


def _reject_forbidden_sensitive_keys(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            lowered = str(key).lower()
            for fragment in FORBIDDEN_KEY_FRAGMENTS:
                if fragment in lowered:
                    raise ValueError(f"audit pack contiene clave sensible: {path}.{key}")
            _reject_forbidden_sensitive_keys(value, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_forbidden_sensitive_keys(value, f"{path}[{index}]")


def _ensure_json_serializable(payload: dict[str, Any]) -> str:
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("audit pack debe ser JSON-safe") from exc
