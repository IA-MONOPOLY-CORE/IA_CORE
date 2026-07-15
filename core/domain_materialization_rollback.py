"""Rollback seguro de materializaciones sandbox."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from core.domain_materializer import MATERIALIZATION_MANIFEST, MATERIALIZATION_SCHEMA_VERSION


ROLLBACK_RECORDS_DIR = "_rollback_records"
ROLLBACK_SCHEMA_VERSION = "1.0"


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
    domains_root = Path(config.DOMAINS_DIR).resolve()
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
