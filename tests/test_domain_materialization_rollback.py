import hashlib
import json
from pathlib import Path

import pytest

from core import domain_registry
from core.domain_materialization_rollback import rollback_domain_materialization
from core.domain_materializer import materialize_sandbox_domain


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"


def _domains_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in DOMAINS.rglob("*") if item.is_file()):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _schema(**overrides) -> dict:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    data.update(overrides)
    return data


def _materialize(tmp_path):
    return materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")


def test_valid_materialization_can_be_rolled_back(tmp_path):
    result = _materialize(tmp_path)

    rollback = rollback_domain_materialization(manifest_path=result["manifest_path"])

    assert rollback["success"] is True
    assert rollback["status"] == "rolled_back"
    assert not Path(result["domain_dir"]).exists()
    assert Path(rollback["rollback_record_path"]).is_file()


def test_rollback_leaves_no_created_files(tmp_path):
    result = _materialize(tmp_path)
    created_paths = list(result["manifest"]["created_paths"])

    rollback_domain_materialization(manifest_path=result["manifest_path"])

    assert all(not Path(path).exists() for path in created_paths)


def test_manifest_is_required(tmp_path):
    with pytest.raises(FileNotFoundError, match="Manifest de materializacion no encontrado"):
        rollback_domain_materialization(manifest_path=tmp_path / "missing_manifest.json")


def test_corrupt_manifest_fails(tmp_path):
    manifest = tmp_path / "sandboxes" / "bad" / "materialization_manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text("{ not json", encoding="utf-8")

    with pytest.raises(ValueError, match="corrupto"):
        rollback_domain_materialization(manifest_path=manifest)


def test_paths_outside_sandbox_are_blocked(tmp_path):
    result = _materialize(tmp_path)
    manifest_path = Path(result["manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["created_paths"].append(str(tmp_path.parent / "escape.txt"))
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="fuera del sandbox"):
        rollback_domain_materialization(manifest_path=manifest_path)


def test_operational_domains_are_protected(tmp_path):
    result = _materialize(tmp_path)
    manifest_path = Path(result["manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["created_paths"] = [str(DOMAINS / "loteria")]
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="fuera del sandbox|domains/ operativo"):
        rollback_domain_materialization(manifest_path=manifest_path)
    assert (DOMAINS / "loteria").exists()


def test_repeated_rollback_is_idempotent(tmp_path):
    result = _materialize(tmp_path)

    first = rollback_domain_materialization(manifest_path=result["manifest_path"])
    second = rollback_domain_materialization(manifest_path=result["manifest_path"])
    third = rollback_domain_materialization(
        materialization_id=result["materialization_id"],
        sandbox_root=tmp_path / "sandboxes",
    )

    assert first["status"] == "rolled_back"
    assert second["status"] == "already_rolled_back"
    assert third["status"] == "already_rolled_back"


def test_unknown_materialization_id_fails(tmp_path):
    with pytest.raises(FileNotFoundError, match="Materializacion no encontrada"):
        rollback_domain_materialization(
            materialization_id="mat_missing",
            sandbox_root=tmp_path / "sandboxes",
        )


def test_rollback_does_not_touch_legacy_or_register_active_domains(tmp_path):
    before = _domains_hash()
    result = _materialize(tmp_path)

    rollback_domain_materialization(manifest_path=result["manifest_path"])

    assert _domains_hash() == before
    assert (DOMAINS / "loteria").exists()
    assert result["domain_id"] not in {
        domain["id"] for domain in domain_registry.list_domains(include_internal=True)
    }


def test_rollback_keeps_traceability_record(tmp_path):
    result = _materialize(tmp_path)

    rollback = rollback_domain_materialization(manifest_path=result["manifest_path"])
    record = json.loads(Path(rollback["rollback_record_path"]).read_text(encoding="utf-8"))

    assert record["materialization_id"] == result["materialization_id"]
    assert record["domain_id"] == result["domain_id"]
    assert record["status"] == "rolled_back"
    assert record["created_paths"] == result["manifest"]["created_paths"]
    assert record["deleted_paths"]
