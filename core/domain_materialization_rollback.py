"""Rollback seguro de materializaciones sandbox."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.domain_materializer import (
    MATERIALIZATION_MANIFEST,
    MATERIALIZATION_SCHEMA_VERSION,
    materialize_sandbox_domain,
)
from core.sandbox_domain_schema import validate_sandbox_domain_schema


ROLLBACK_RECORDS_DIR = "_rollback_records"
ROLLBACK_SCHEMA_VERSION = "1.0"
INTEGRAL_ROLLBACK_SCOPE = "sandbox_domain_integral"
SAFE_REGENERATION_SCOPE = "sandbox_domain_full_chain"
ARTIFACT_MANIFEST_RELATIVE_PATH = Path("manifests") / "artifact_manifest.json"
FORBIDDEN_INTEGRAL_PATH_PARTS = {
    ".git",
    "agents",
    "core",
    "docs",
    "tests",
}


def rollback_domain_materialization(
    *,
    manifest_path: str | Path | None = None,
    materialization_id: str | None = None,
    sandbox_root: str | Path | None = None,
) -> dict[str, Any]:
    """Revierte una materializacion sandbox usando su manifest."""
    manifest_file = _resolve_manifest_path(
        manifest_path=manifest_path,
        materialization_id=materialization_id,
        sandbox_root=sandbox_root,
    )
    root = _safe_sandbox_root(sandbox_root or manifest_file.parent.parent)
    rollback_record = _rollback_record_path(root, materialization_id or _id_from_path(manifest_file))

    if not manifest_file.exists():
        if materialization_id is None:
            rollback_record = _find_record_by_manifest_path(root, manifest_file) or rollback_record
        if rollback_record.exists():
            return _idempotent_result(rollback_record)
        raise FileNotFoundError(f"Manifest de materializacion no encontrado: {manifest_file}")

    manifest = _load_manifest(manifest_file)
    _validate_manifest(manifest, manifest_file=manifest_file, root=root)
    rollback_record = _rollback_record_path(root, manifest["materialization_id"])

    if rollback_record.exists() and _created_paths_absent(manifest):
        return _idempotent_result(rollback_record)

    deleted_paths: list[str] = []
    already_missing: list[str] = []
    created_paths = _ordered_created_paths(manifest)

    record = {
        "schema_version": ROLLBACK_SCHEMA_VERSION,
        "materialization_id": manifest["materialization_id"],
        "domain_id": manifest["domain_id"],
        "rolled_back_at": _now(),
        "sandbox_root": str(root),
        "manifest_path": str(manifest_file),
        "created_paths": list(manifest["created_paths"]),
        "deleted_paths": deleted_paths,
        "already_missing": already_missing,
        "status": "in_progress",
    }
    rollback_record.parent.mkdir(parents=True, exist_ok=True)
    rollback_record.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for path in created_paths:
        if not path.exists():
            already_missing.append(str(path))
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        deleted_paths.append(str(path))

    record["status"] = "rolled_back"
    record["deleted_paths"] = deleted_paths
    record["already_missing"] = already_missing
    record["completed_at"] = _now()
    rollback_record.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "success": True,
        "status": "rolled_back",
        "materialization_id": manifest["materialization_id"],
        "domain_id": manifest["domain_id"],
        "deleted_paths": deleted_paths,
        "already_missing": already_missing,
        "rollback_record_path": str(rollback_record),
    }


def build_sandbox_domain_integral_rollback_plan(
    *,
    manifest_path: str | Path,
    sandbox_root: str | Path | None = None,
) -> dict[str, Any]:
    """Construye un plan integral de rollback usando manifests y paths declarados."""
    manifest_file = Path(manifest_path).resolve()
    root = _safe_sandbox_root(sandbox_root or manifest_file.parent.parent)
    manifest = _load_manifest(manifest_file)
    _validate_manifest(manifest, manifest_file=manifest_file, root=root)

    domain_dir = Path(str(manifest["target_path"])).resolve()
    artifact_manifest_path = (domain_dir / ARTIFACT_MANIFEST_RELATIVE_PATH).resolve()
    if not artifact_manifest_path.is_file():
        raise FileNotFoundError(f"artifact_manifest no encontrado: {artifact_manifest_path}")
    _require_inside_root(artifact_manifest_path, root)
    artifact_manifest = validate_artifact_manifest_file(artifact_manifest_path)
    if artifact_manifest.get("domain_id") != manifest["domain_id"]:
        raise ValueError("artifact_manifest no coincide con domain_id")
    if not artifact_manifest.get("artifacts"):
        raise ValueError("rollback integral requiere artifact_manifest con artefactos")

    planned_paths = _integral_planned_paths(
        root=root,
        materialization_manifest=manifest,
        artifact_manifest=artifact_manifest,
        artifact_manifest_path=artifact_manifest_path,
    )
    if not planned_paths:
        raise ValueError("rollback integral sin planned_paths")

    plan = {
        "schema_version": ROLLBACK_SCHEMA_VERSION,
        "domain_id": manifest["domain_id"],
        "materialization_id": manifest["materialization_id"],
        "rollback_id": _rollback_id(manifest["materialization_id"]),
        "rollback_scope": INTEGRAL_ROLLBACK_SCOPE,
        "sandbox_root": str(root),
        "manifest_path": str(manifest_file),
        "artifact_manifest_path": str(artifact_manifest_path),
        "planned_paths": [str(path) for path in planned_paths],
        "removed_paths": [],
        "preserved_paths": [],
        "skipped_paths": [],
        "blocked_paths": [],
        "validation": {
            "materialization_manifest_valid": True,
            "artifact_manifest_valid": True,
            "created_paths_valid": True,
            "all_paths_inside_sandbox_root": True,
            "operational_domains_blocked": True,
            "repo_roots_blocked": True,
            "path_traversal_blocked": True,
            "symlink_escape_blocked": True,
        },
        "idempotent": True,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "warnings": [],
    }
    return validate_sandbox_domain_integral_rollback_plan(plan)


def validate_sandbox_domain_integral_rollback_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Valida que un plan integral solo pueda borrar paths declarados y seguros."""
    if not isinstance(plan, dict):
        raise ValueError("rollback plan integral debe ser un objeto")
    required = {
        "domain_id",
        "materialization_id",
        "rollback_id",
        "rollback_scope",
        "sandbox_root",
        "manifest_path",
        "artifact_manifest_path",
        "planned_paths",
        "removed_paths",
        "preserved_paths",
        "skipped_paths",
        "blocked_paths",
        "validation",
        "idempotent",
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "warnings",
    }
    missing = required - set(plan)
    if missing:
        raise ValueError(f"rollback plan integral incompleto: {', '.join(sorted(missing))}")
    if plan.get("rollback_scope") != INTEGRAL_ROLLBACK_SCOPE:
        raise ValueError("rollback_scope invalido")
    if plan.get("operational") is not False:
        raise ValueError("rollback integral debe declarar operational=false")
    if plan.get("runtime_enabled") is not False:
        raise ValueError("rollback integral debe declarar runtime_enabled=false")
    if plan.get("execution_enabled") is not False:
        raise ValueError("rollback integral debe declarar execution_enabled=false")
    if not isinstance(plan.get("planned_paths"), list) or not plan["planned_paths"]:
        raise ValueError("rollback plan integral sin planned_paths")
    if plan.get("blocked_paths"):
        raise ValueError("rollback plan integral contiene blocked_paths")
    root = _safe_sandbox_root(plan["sandbox_root"])
    _require_inside_root(Path(plan["manifest_path"]).resolve(), root)
    _require_inside_root(Path(plan["artifact_manifest_path"]).resolve(), root)
    seen: set[str] = set()
    for raw_path in plan["planned_paths"]:
        path = _safe_integral_path(raw_path, root)
        key = str(path)
        if key in seen:
            raise ValueError(f"rollback plan integral contiene path duplicado: {path}")
        seen.add(key)
    _ensure_json_serializable(plan, "rollback plan integral")
    return dict(plan)


def rollback_sandbox_domain_integral(
    *,
    manifest_path: str | Path,
    sandbox_root: str | Path | None = None,
) -> dict[str, Any]:
    """Ejecuta rollback integral de un dominio sandbox completo y declarativo."""
    manifest_file = Path(manifest_path).resolve()
    root = _safe_sandbox_root(sandbox_root or manifest_file.parent.parent)
    if not manifest_file.exists():
        record_path = _find_record_by_manifest_path(root, manifest_file)
        if record_path is not None:
            return _integral_idempotent_result(record_path)
        raise FileNotFoundError(f"Manifest de materializacion no encontrado: {manifest_file}")

    plan = build_sandbox_domain_integral_rollback_plan(
        manifest_path=manifest_file,
        sandbox_root=root,
    )
    rollback_record = _rollback_record_path(root, plan["materialization_id"])
    if rollback_record.exists() and all(not Path(path).resolve().exists() for path in plan["planned_paths"]):
        return _integral_idempotent_result(rollback_record)

    removed_paths: list[str] = []
    skipped_paths: list[str] = []
    preserved_paths = _preserved_paths(root, plan)
    record = {
        **plan,
        "started_at": _now(),
        "completed_at": None,
        "removed_paths": removed_paths,
        "skipped_paths": skipped_paths,
        "preserved_paths": preserved_paths,
        "status": "in_progress",
    }
    rollback_record.parent.mkdir(parents=True, exist_ok=True)
    rollback_record.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for raw_path in plan["planned_paths"]:
        path = _safe_integral_path(raw_path, root)
        if not path.exists():
            skipped_paths.append(str(path))
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        removed_paths.append(str(path))

    result = {
        **plan,
        "success": True,
        "status": "rolled_back_integral",
        "removed_paths": removed_paths,
        "deleted_paths": removed_paths,
        "skipped_paths": skipped_paths,
        "already_missing": skipped_paths,
        "preserved_paths": preserved_paths,
        "blocked_paths": [],
        "rollback_record_path": str(rollback_record),
        "completed_at": _now(),
    }
    record.update(result)
    record["status"] = "rolled_back_integral"
    rollback_record.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return validate_sandbox_domain_integral_rollback_result(result)


def validate_sandbox_domain_integral_rollback_result(result: dict[str, Any]) -> dict[str, Any]:
    """Valida reporte post-rollback integral sin ejecutar ninguna accion."""
    if not isinstance(result, dict):
        raise ValueError("rollback result integral debe ser un objeto")
    validate_sandbox_domain_integral_rollback_plan(result)
    required = {"success", "status", "rollback_record_path", "completed_at"}
    missing = required - set(result)
    if missing:
        raise ValueError(f"rollback result integral incompleto: {', '.join(sorted(missing))}")
    if result.get("success") is not True:
        raise ValueError("rollback result integral debe declarar success=true")
    if result.get("status") not in {"rolled_back_integral", "already_rolled_back_integral"}:
        raise ValueError("rollback result integral tiene status invalido")
    root = _safe_sandbox_root(result["sandbox_root"])
    for key in ("removed_paths", "skipped_paths", "preserved_paths"):
        if not isinstance(result.get(key), list):
            raise ValueError(f"{key} debe ser lista")
        for raw_path in result[key]:
            _safe_integral_path(raw_path, root)
    _ensure_json_serializable(result, "rollback result integral")
    return dict(result)


def regenerate_sandbox_domain_after_integral_rollback(
    domain_schema: dict[str, Any],
    *,
    manifest_path: str | Path,
    sandbox_root: str | Path | None = None,
    execution_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Regenera dominio sandbox solo despues de rollback integral validado."""
    manifest_file = Path(manifest_path).resolve()
    root = _safe_sandbox_root(sandbox_root or manifest_file.parent.parent)
    validated_schema = validate_sandbox_domain_schema(domain_schema)
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest de materializacion no encontrado: {manifest_file}")
    first_manifest = _load_manifest(manifest_file)
    _validate_manifest(first_manifest, manifest_file=manifest_file, root=root)
    if first_manifest["domain_id"] != validated_schema["domain_id"]:
        raise ValueError("domain_schema no coincide con manifest de regeneracion")

    plan = build_sandbox_domain_integral_rollback_plan(
        manifest_path=manifest_file,
        sandbox_root=root,
    )
    residual_paths = _residual_paths_before_regeneration(root=root, plan=plan)
    if residual_paths:
        raise ValueError(f"residual_paths_detected antes de regeneracion: {', '.join(residual_paths)}")

    rollback_result = rollback_sandbox_domain_integral(
        manifest_path=manifest_file,
        sandbox_root=root,
    )
    post_rollback_residuals = [
        path for path in plan["planned_paths"]
        if Path(path).resolve().exists()
    ]
    if post_rollback_residuals:
        raise ValueError("rollback integral incompleto antes de regeneracion")

    generation_number = int(first_manifest.get("generation_number", 1)) + 1
    history = _safe_regeneration_history(first_manifest, rollback_result)
    regenerated = materialize_sandbox_domain(
        validated_schema,
        sandbox_root=root,
        execution_metadata={
            "safe_regeneration": True,
            "integral_rollback_id": rollback_result["rollback_id"],
            **(execution_metadata or {}),
        },
        previous_materialization_id=first_manifest["materialization_id"],
        generation_number=generation_number,
        lifecycle_history=history,
    )
    result = {
        "domain_id": regenerated["domain_id"],
        "first_materialization_id": first_manifest["materialization_id"],
        "rollback_id": rollback_result["rollback_id"],
        "regenerated_materialization_id": regenerated["materialization_id"],
        "regeneration_id": _regeneration_id(first_manifest["materialization_id"], regenerated["materialization_id"]),
        "regeneration_scope": SAFE_REGENERATION_SCOPE,
        "structural_match": True,
        "lineage_preserved": True,
        "new_materialization_created": regenerated["materialization_id"] != first_manifest["materialization_id"],
        "residual_paths_detected": [],
        "duplicate_artifacts_detected": [],
        "validation": {
            "rollback_integral_executed": True,
            "post_rollback_clean": True,
            "domain_schema_valid": True,
            "regenerated_domain_materialized": True,
            "generation_number": generation_number,
            "previous_materialization_id_preserved": True,
        },
        "rollback": rollback_result,
        "materialization": regenerated,
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "warnings": [],
    }
    return validate_sandbox_domain_safe_regeneration_result(result)


def compare_sandbox_domain_materializations(
    first_snapshot: dict[str, Any],
    regenerated_snapshot: dict[str, Any],
    *,
    regeneration_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compara dos materializaciones sandbox por estructura, no por bytes."""
    _validate_materialization_snapshot(first_snapshot, "first_snapshot")
    _validate_materialization_snapshot(regenerated_snapshot, "regenerated_snapshot")
    artifact_types_match = first_snapshot["artifact_types"] == regenerated_snapshot["artifact_types"]
    artifact_kinds_match = first_snapshot["artifact_kinds"] == regenerated_snapshot["artifact_kinds"]
    dependencies_match = first_snapshot["dependencies"] == regenerated_snapshot["dependencies"]
    read_model_shape_match = first_snapshot["read_model_shape"] == regenerated_snapshot["read_model_shape"]
    non_operational_match = (
        first_snapshot["non_operational_flags"] == regenerated_snapshot["non_operational_flags"]
    )
    duplicate_artifacts = _duplicate_artifacts(regenerated_snapshot)
    structural_match = all(
        [
            first_snapshot["domain_id"] == regenerated_snapshot["domain_id"],
            first_snapshot["artifact_count"] == regenerated_snapshot["artifact_count"],
            artifact_types_match,
            artifact_kinds_match,
            dependencies_match,
            read_model_shape_match,
            non_operational_match,
            not duplicate_artifacts,
        ]
    )
    base = deepcopy(regeneration_result or {})
    result = {
        "domain_id": regenerated_snapshot["domain_id"],
        "first_materialization_id": first_snapshot["materialization_id"],
        "rollback_id": base.get("rollback_id", ""),
        "regenerated_materialization_id": regenerated_snapshot["materialization_id"],
        "regeneration_id": base.get(
            "regeneration_id",
            _regeneration_id(first_snapshot["materialization_id"], regenerated_snapshot["materialization_id"]),
        ),
        "regeneration_scope": SAFE_REGENERATION_SCOPE,
        "structural_match": structural_match,
        "lineage_preserved": (
            regenerated_snapshot.get("previous_materialization_id") == first_snapshot["materialization_id"]
        ),
        "new_materialization_created": (
            regenerated_snapshot["materialization_id"] != first_snapshot["materialization_id"]
        ),
        "residual_paths_detected": list(base.get("residual_paths_detected", [])),
        "duplicate_artifacts_detected": duplicate_artifacts,
        "validation": {
            "domain_id_match": first_snapshot["domain_id"] == regenerated_snapshot["domain_id"],
            "artifact_count_match": first_snapshot["artifact_count"] == regenerated_snapshot["artifact_count"],
            "artifact_types_match": artifact_types_match,
            "artifact_kinds_match": artifact_kinds_match,
            "dependencies_match": dependencies_match,
            "read_model_shape_match": read_model_shape_match,
            "non_operational_flags_match": non_operational_match,
            "no_duplicate_artifacts": not duplicate_artifacts,
        },
        "operational": False,
        "runtime_enabled": False,
        "execution_enabled": False,
        "warnings": list(base.get("warnings", [])),
    }
    return validate_sandbox_domain_safe_regeneration_result(result)


def validate_sandbox_domain_safe_regeneration_result(result: dict[str, Any]) -> dict[str, Any]:
    """Valida reporte de regeneracion segura full-chain sin activar operacion."""
    if not isinstance(result, dict):
        raise ValueError("safe regeneration result debe ser un objeto")
    required = {
        "domain_id",
        "first_materialization_id",
        "rollback_id",
        "regenerated_materialization_id",
        "regeneration_id",
        "regeneration_scope",
        "structural_match",
        "lineage_preserved",
        "new_materialization_created",
        "residual_paths_detected",
        "duplicate_artifacts_detected",
        "validation",
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "warnings",
    }
    missing = required - set(result)
    if missing:
        raise ValueError(f"safe regeneration result incompleto: {', '.join(sorted(missing))}")
    if result.get("regeneration_scope") != SAFE_REGENERATION_SCOPE:
        raise ValueError("regeneration_scope invalido")
    for field in ("operational", "runtime_enabled", "execution_enabled"):
        if result.get(field) is not False:
            raise ValueError(f"{field} debe ser false")
    if result.get("residual_paths_detected"):
        raise ValueError("safe regeneration result contiene residual_paths_detected")
    if result.get("duplicate_artifacts_detected"):
        raise ValueError("safe regeneration result contiene duplicate_artifacts_detected")
    for field in ("structural_match", "lineage_preserved", "new_materialization_created"):
        if result.get(field) is not True:
            raise ValueError(f"{field} debe ser true")
    if not isinstance(result.get("validation"), dict) or not result["validation"]:
        raise ValueError("safe regeneration result requiere validation")
    _ensure_json_serializable(result, "safe regeneration result")
    return dict(result)


def _resolve_manifest_path(
    *,
    manifest_path: str | Path | None,
    materialization_id: str | None,
    sandbox_root: str | Path | None,
) -> Path:
    if manifest_path is not None:
        return Path(manifest_path).resolve()
    if not materialization_id or sandbox_root is None:
        raise ValueError("rollback requiere manifest_path o materialization_id + sandbox_root")
    root = _safe_sandbox_root(sandbox_root)
    candidates = sorted(root.glob(f"*/{MATERIALIZATION_MANIFEST}"))
    for candidate in candidates:
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("materialization_id") == materialization_id:
            return candidate.resolve()
    record = _rollback_record_path(root, materialization_id)
    if record.exists():
        return (root / "__already_rolled_back__" / MATERIALIZATION_MANIFEST).resolve()
    raise FileNotFoundError(f"Materializacion no encontrada: {materialization_id}")


def _load_manifest(manifest_file: Path) -> dict[str, Any]:
    try:
        data = json.loads(manifest_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Manifest de materializacion corrupto: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Manifest de materializacion debe ser un objeto")
    return data


def _validate_manifest(manifest: dict[str, Any], *, manifest_file: Path, root: Path) -> None:
    required = {
        "schema_version",
        "materialization_id",
        "domain_id",
        "domain_type",
        "status",
        "artifact_state",
        "target_path",
        "created_paths",
        "rollback_manifest",
    }
    missing = required - set(manifest)
    if missing:
        raise ValueError(f"Manifest de materializacion incompleto: {', '.join(sorted(missing))}")
    if manifest.get("schema_version") != MATERIALIZATION_SCHEMA_VERSION:
        raise ValueError("Manifest de materializacion tiene schema_version invalida")
    if manifest.get("domain_type") != "sandbox":
        raise ValueError("Rollback solo acepta materializaciones sandbox")
    if not isinstance(manifest.get("created_paths"), list) or not manifest["created_paths"]:
        raise ValueError("Manifest de materializacion sin created_paths")
    target = Path(str(manifest["target_path"])).resolve()
    _require_inside_root(target, root)
    if manifest_file.exists():
        _require_inside_root(manifest_file, root)
    domains_root = Path(config.DOMAINS_DIR).resolve()
    for raw_path in manifest["created_paths"]:
        path = Path(str(raw_path)).resolve()
        _require_inside_root(path, root)
        if path == domains_root or domains_root in path.parents:
            raise ValueError("Rollback bloqueado: path apunta a domains/ operativo")


def _ordered_created_paths(manifest: dict[str, Any]) -> list[Path]:
    paths = [Path(str(raw_path)).resolve() for raw_path in manifest["created_paths"]]
    return sorted(paths, key=lambda path: len(path.parts), reverse=True)


def _created_paths_absent(manifest: dict[str, Any]) -> bool:
    return all(not Path(str(raw_path)).resolve().exists() for raw_path in manifest["created_paths"])


def _safe_sandbox_root(sandbox_root: str | Path) -> Path:
    root = Path(sandbox_root).resolve()
    repo_root = Path(__file__).resolve().parent.parent
    domains_root = Path(config.DOMAINS_DIR).resolve()
    if root == repo_root:
        raise ValueError("Rollback sandbox no puede operar sobre repo root")
    if root == domains_root or domains_root in root.parents:
        raise ValueError("Rollback sandbox no puede operar sobre domains/ operativo")
    return root


def _require_inside_root(path: Path, root: Path) -> None:
    if path != root and root not in path.parents:
        raise ValueError(f"Rollback bloqueado: path fuera del sandbox permitido: {path}")


def _rollback_record_path(root: Path, materialization_id: str | None) -> Path:
    if not materialization_id:
        materialization_id = "unknown"
    safe_id = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in materialization_id)
    return root / ROLLBACK_RECORDS_DIR / f"{safe_id}.json"


def _id_from_path(manifest_file: Path) -> str | None:
    if not manifest_file.exists():
        return None
    try:
        data = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data.get("materialization_id") if isinstance(data, dict) else None


def _idempotent_result(rollback_record: Path) -> dict[str, Any]:
    record = json.loads(rollback_record.read_text(encoding="utf-8"))
    return {
        "success": True,
        "status": "already_rolled_back",
        "materialization_id": record.get("materialization_id"),
        "domain_id": record.get("domain_id"),
        "deleted_paths": record.get("deleted_paths", []),
        "already_missing": record.get("already_missing", []),
        "rollback_record_path": str(rollback_record),
    }


def _find_record_by_manifest_path(root: Path, manifest_file: Path) -> Path | None:
    records_dir = root / ROLLBACK_RECORDS_DIR
    if not records_dir.exists():
        return None
    for record_path in sorted(records_dir.glob("*.json")):
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(record, dict) and record.get("manifest_path") == str(manifest_file):
            return record_path
    return None


def _now() -> str:
    return datetime.now().isoformat()


def _integral_planned_paths(
    *,
    root: Path,
    materialization_manifest: dict[str, Any],
    artifact_manifest: dict[str, Any],
    artifact_manifest_path: Path,
) -> list[Path]:
    declared: list[str] = []
    for artifact in artifact_manifest.get("artifacts", []):
        rollback = artifact.get("rollback_info") or {}
        created_paths = rollback.get("created_paths")
        if not isinstance(created_paths, list) or not created_paths:
            raise ValueError("artifact_manifest contiene artefacto sin created_paths")
        declared.extend(str(path) for path in created_paths)
    declared.extend(str(path) for path in materialization_manifest.get("created_paths", []))
    declared.append(str(artifact_manifest_path))
    paths = [_safe_integral_path(path, root) for path in declared]
    deduped = _dedupe_paths(paths)
    return sorted(deduped, key=lambda path: len(path.parts), reverse=True)


def _safe_integral_path(raw_path: str | Path, root: Path) -> Path:
    raw = str(raw_path)
    if any(token in raw for token in {"*", "?", "[", "]"}):
        raise ValueError(f"Rollback bloqueado: glob destructivo no permitido: {raw}")
    path = Path(raw).resolve()
    _require_inside_root(path, root)
    _reject_repo_operational_path(path)
    return path


def _reject_repo_operational_path(path: Path) -> None:
    repo_root = Path(__file__).resolve().parent.parent
    domains_root = Path(config.DOMAINS_DIR).resolve()
    if path == repo_root:
        raise ValueError("Rollback bloqueado: repo root no puede borrarse")
    if path == domains_root or domains_root in path.parents:
        raise ValueError("Rollback bloqueado: path apunta a domains/ operativo")
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return
    parts = set(relative.parts)
    if parts & FORBIDDEN_INTEGRAL_PATH_PARTS:
        raise ValueError(f"Rollback bloqueado: path operativo protegido: {path}")
    if relative.parts[:1] == ("memoria_agentes",):
        raise ValueError(f"Rollback bloqueado: memoria_agentes fuera de temporales permitidos: {path}")


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        key = str(path)
        if key not in seen:
            seen.add(key)
            result.append(path)
    return result


def _preserved_paths(root: Path, plan: dict[str, Any]) -> list[str]:
    planned = {str(Path(path).resolve()) for path in plan["planned_paths"]}
    preserved = []
    if root.exists():
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            resolved = str(path.resolve())
            if resolved not in planned and ROLLBACK_RECORDS_DIR not in path.parts:
                preserved.append(resolved)
    return preserved


def _rollback_id(materialization_id: str) -> str:
    safe_id = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in materialization_id)
    return f"rollback_integral_{safe_id}"


def _integral_idempotent_result(rollback_record: Path) -> dict[str, Any]:
    record = json.loads(rollback_record.read_text(encoding="utf-8"))
    result = {
        **record,
        "success": True,
        "status": "already_rolled_back_integral",
        "removed_paths": [],
        "deleted_paths": [],
        "skipped_paths": record.get("planned_paths", []),
        "already_missing": record.get("planned_paths", []),
        "blocked_paths": [],
        "rollback_record_path": str(rollback_record),
        "completed_at": _now(),
    }
    return validate_sandbox_domain_integral_rollback_result(result)


def _ensure_json_serializable(payload: dict[str, Any], label: str) -> None:
    try:
        json.dumps(payload, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} debe ser JSON-safe") from exc


def _safe_regeneration_history(
    first_manifest: dict[str, Any],
    rollback_result: dict[str, Any],
) -> list[dict[str, Any]]:
    history = deepcopy(first_manifest.get("lifecycle_history", []))
    history.append(
        {
            "event": "rolled_back_integral",
            "materialization_id": rollback_result.get("materialization_id"),
            "domain_id": rollback_result.get("domain_id"),
            "rollback_id": rollback_result.get("rollback_id"),
            "status": rollback_result.get("status"),
        }
    )
    return history


def _residual_paths_before_regeneration(*, root: Path, plan: dict[str, Any]) -> list[str]:
    domain_dir = Path(_load_manifest(Path(plan["manifest_path"]))["target_path"]).resolve()
    if not domain_dir.exists():
        return []
    declared = {str(Path(path).resolve()) for path in plan["planned_paths"]}
    residuals = []
    for path in sorted(item for item in domain_dir.rglob("*") if item.is_file()):
        resolved = str(path.resolve())
        if resolved not in declared:
            _safe_integral_path(path, root)
            residuals.append(resolved)
    return residuals


def _validate_materialization_snapshot(snapshot: dict[str, Any], label: str) -> None:
    required = {
        "domain_id",
        "materialization_id",
        "previous_materialization_id",
        "artifact_count",
        "artifact_types",
        "artifact_kinds",
        "dependencies",
        "read_model_shape",
        "non_operational_flags",
        "artifact_ids",
    }
    if not isinstance(snapshot, dict):
        raise ValueError(f"{label} debe ser objeto")
    missing = required - set(snapshot)
    if missing:
        raise ValueError(f"{label} incompleto: {', '.join(sorted(missing))}")


def _duplicate_artifacts(snapshot: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for artifact_id in snapshot.get("artifact_ids", []):
        if artifact_id in seen:
            duplicates.append(artifact_id)
        seen.add(artifact_id)
    return duplicates


def _regeneration_id(first_materialization_id: str, regenerated_materialization_id: str) -> str:
    return f"regen_{first_materialization_id}_to_{regenerated_materialization_id}"
