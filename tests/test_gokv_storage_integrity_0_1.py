"""N3 storage, registry and integrity tests for GOKV 0.1."""

from pathlib import Path

import pytest

from gokv.schema import build_knowledge_item
from gokv.storage import (
    DuplicateKnowledgeError,
    VaultIntegrityError,
    VaultPaths,
    list_promoted,
    rebuild_index,
    save_knowledge_item,
    validate_vault,
)


def evidence():
    return [{"evidence_id": "storage_test", "kind": "test", "ref": "tests/storage.py", "claim": "storage passed"}]


def make_item(knowledge_id: str, status: str = "CANDIDATE"):
    return build_knowledge_item(
        knowledge_id=knowledge_id,
        kind="PROCEDURE",
        title=knowledge_id,
        summary="Storage test item.",
        status=status,
        evidence_refs=evidence(),
        source_commits=["7cb7134"],
        source_checkpoints=["gokv_0_1"],
        confidence={"level": "MEDIUM", "rationale": "test fixture"},
    )


def paths(tmp_path: Path) -> VaultPaths:
    return VaultPaths(tmp_path / "vault")


def test_n3_append_only_storage_and_registry_roundtrip(tmp_path):
    vault = paths(tmp_path)
    save_knowledge_item(make_item("first_item"), vault)
    save_knowledge_item(make_item("second_item"), vault)
    registry = rebuild_index(vault)
    assert registry["counts"]["total"] == 2
    assert validate_vault(vault)["valid"] is True
    assert list_promoted(vault) == []


def test_n3_duplicate_ids_cannot_overwrite_history(tmp_path):
    vault = paths(tmp_path)
    save_knowledge_item(make_item("same_item"), vault)
    with pytest.raises(DuplicateKnowledgeError):
        save_knowledge_item(make_item("same_item"), vault)


def test_n3_corrupt_item_and_stale_registry_are_rejected(tmp_path):
    vault = paths(tmp_path)
    save_knowledge_item(make_item("valid_item"), vault)
    rebuild_index(vault)
    (vault.items_dir / "valid_item.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(VaultIntegrityError):
        validate_vault(vault)


def test_n3_relationships_and_registry_are_exact(tmp_path):
    vault = paths(tmp_path)
    item = make_item("reference_item")
    item["supersedes"] = ["missing_item"]
    save_knowledge_item(item, vault)
    with pytest.raises(VaultIntegrityError, match="inexistentes"):
        rebuild_index(vault)
