"""Git-backed, development-only storage and integrity checks for GOKV."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from gokv.schema import SCHEMA_VERSION, validate_knowledge_item


REGISTRY_SCHEMA_VERSION = "gokv.registry.v1"


class VaultIntegrityError(ValueError):
    """Raised when the Git-backed vault is inconsistent or corrupted."""


class DuplicateKnowledgeError(VaultIntegrityError):
    """Raised when an append-only knowledge ID already exists."""


@dataclass(frozen=True)
class VaultPaths:
    root: Path

    @property
    def schema_dir(self) -> Path:
        return self.root / "schema"

    @property
    def items_dir(self) -> Path:
        return self.root / "items"

    @property
    def events_dir(self) -> Path:
        return self.root / "events"

    @property
    def metrics_dir(self) -> Path:
        return self.root / "metrics"

    @property
    def packs_dir(self) -> Path:
        return self.root / "packs"

    @property
    def registry_path(self) -> Path:
        return self.root / "registry.json"

    def ensure(self) -> None:
        for directory in (self.root, self.items_dir, self.events_dir, self.metrics_dir, self.packs_dir):
            directory.mkdir(parents=True, exist_ok=True)


def default_paths(repo_root: Path | None = None) -> VaultPaths:
    root = Path(repo_root or Path(__file__).resolve().parents[1])
    return VaultPaths(root / "knowledge" / "global_operational")


def save_knowledge_item(item: dict[str, Any], paths: VaultPaths | None = None) -> Path:
    vault = paths or default_paths()
    validated = validate_knowledge_item(item)
    vault.ensure()
    destination = vault.items_dir / f"{validated['knowledge_id']}.json"
    if destination.exists():
        raise DuplicateKnowledgeError(f"knowledge_id ya existe: {validated['knowledge_id']}")
    _write_json_exclusive(destination, validated)
    return destination


def load_knowledge_item(knowledge_id: str, paths: VaultPaths | None = None) -> dict[str, Any]:
    vault = paths or default_paths()
    path = vault.items_dir / f"{knowledge_id}.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    return validate_knowledge_item(_read_json(path))


def iter_knowledge_items(paths: VaultPaths | None = None) -> list[dict[str, Any]]:
    vault = paths or default_paths()
    if not vault.items_dir.exists():
        return []
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(vault.items_dir.glob("*.json")):
        item = validate_knowledge_item(_read_json(path))
        if path.stem != item["knowledge_id"]:
            raise VaultIntegrityError(f"filename no coincide con knowledge_id: {path.name}")
        if item["knowledge_id"] in seen:
            raise VaultIntegrityError(f"knowledge_id duplicado: {item['knowledge_id']}")
        seen.add(item["knowledge_id"])
        items.append(item)
    return items


def rebuild_index(paths: VaultPaths | None = None) -> dict[str, Any]:
    vault = paths or default_paths()
    vault.ensure()
    items = iter_knowledge_items(vault)
    ids = {item["knowledge_id"] for item in items}
    _validate_relationships(items, ids)
    registry = _build_registry(items)
    _write_json(vault.registry_path, registry)
    return registry


def validate_vault(paths: VaultPaths | None = None) -> dict[str, Any]:
    vault = paths or default_paths()
    vault.ensure()
    items = iter_knowledge_items(vault)
    ids = {item["knowledge_id"] for item in items}
    _validate_relationships(items, ids)
    if not vault.registry_path.is_file():
        raise VaultIntegrityError("registry.json ausente")
    registry = _read_json(vault.registry_path)
    _validate_registry(registry, items)
    return {
        "valid": True,
        "schema_version": SCHEMA_VERSION,
        "registry_schema_version": REGISTRY_SCHEMA_VERSION,
        "item_count": len(items),
        "status_counts": dict(Counter(item["status"] for item in items)),
    }


def show_item(knowledge_id: str, paths: VaultPaths | None = None) -> dict[str, Any]:
    return load_knowledge_item(knowledge_id, paths)


def list_promoted(paths: VaultPaths | None = None) -> list[dict[str, Any]]:
    return [item for item in iter_knowledge_items(paths) if item["status"] == "PROMOTED"]


def _build_registry(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": REGISTRY_SCHEMA_VERSION,
        "knowledge_schema_version": SCHEMA_VERSION,
        "items": {
            item["knowledge_id"]: {
                "path": f"items/{item['knowledge_id']}.json",
                "knowledge_version": item["knowledge_version"],
                "kind": item["kind"],
                "status": item["status"],
                "scope": item["scope"],
                "privacy_class": item["privacy_class"],
                "learning_origin": item["learning_origin"],
                "tags": item["tags"],
            }
            for item in items
        },
        "counts": {
            "total": len(items),
            "by_status": dict(Counter(item["status"] for item in items)),
            "by_kind": dict(Counter(item["kind"] for item in items)),
        },
    }


def _validate_registry(registry: Any, items: list[dict[str, Any]]) -> None:
    if not isinstance(registry, dict):
        raise VaultIntegrityError("registry debe ser un objeto")
    if registry.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise VaultIntegrityError("schema_version de registry invalida")
    if registry.get("knowledge_schema_version") != SCHEMA_VERSION:
        raise VaultIntegrityError("knowledge_schema_version de registry invalida")
    expected = _build_registry(items)
    if registry != expected:
        raise VaultIntegrityError("registry desactualizado: ejecutar rebuild_index")


def _validate_relationships(items: list[dict[str, Any]], ids: set[str]) -> None:
    for item in items:
        for field in ("supersedes", "superseded_by"):
            missing = set(item[field]) - ids
            if missing:
                raise VaultIntegrityError(f"{field} referencia IDs inexistentes: {sorted(missing)}")


def _read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise VaultIntegrityError(f"JSON invalido o ilegible: {path}") from exc


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _write_json_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
    except FileExistsError as exc:
        raise DuplicateKnowledgeError(f"archivo ya existe: {path}") from exc
