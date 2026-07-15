import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core import domain_registry
from core.domain_materializer import (
    MATERIALIZATION_MANIFEST,
    materialize_sandbox_domain,
    validate_materialized_sandbox_domain,
)
from core.domain_state import DomainState


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


def test_valid_schema_materializes_sandbox_structure(tmp_path):
    result = materialize_sandbox_domain(
        _schema(),
        sandbox_root=tmp_path / "sandboxes",
        execution_metadata={"test": "valid_schema"},
    )

    domain_dir = Path(result["domain_dir"])

    assert result["success"] is True
    assert domain_dir.is_dir()
    assert (domain_dir / "domain.json").is_file()
    assert (domain_dir / MATERIALIZATION_MANIFEST).is_file()
    assert result["domain"]["status"] == "materialized"
    assert result["domain"]["artifact_state"] == "materialized"
    assert result["domain"]["human_review_required"] is True


def test_invalid_schema_fails_before_writing(tmp_path):
    root = tmp_path / "sandboxes"
    invalid = _schema(source_request={})

    with pytest.raises(ValueError, match="source_request"):
        materialize_sandbox_domain(invalid, sandbox_root=root)

    assert not root.exists()


def test_materialization_creates_domain_json_and_manifest(tmp_path):
    result = materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")

    domain_json = Path(result["domain_json_path"])
    manifest_path = Path(result["manifest_path"])
    domain = json.loads(domain_json.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert domain["domain_id"] == "sandbox_marketing_crm_automation"
    assert manifest["domain_id"] == domain["domain_id"]
    assert manifest["materialization_id"] == domain["materialization_id"]


def test_materialization_id_is_generated(tmp_path):
    result = materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")

    assert result["materialization_id"].startswith("mat_sandbox_marketing_crm_automation_")
    assert result["materialization_id"] != "mat_fixture_pending"
    assert result["domain"]["materialization_id"] == result["materialization_id"]


def test_materializer_never_writes_to_real_domains(tmp_path):
    before = _domains_hash()

    result = materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")

    assert _domains_hash() == before
    assert not (DOMAINS / result["domain_id"]).exists()
    assert result["domain_id"] not in {
        domain["id"] for domain in domain_registry.list_domains(include_internal=True)
    }


def test_materializer_does_not_create_active_state(tmp_path):
    result = materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")

    assert result["domain"]["status"] == DomainState.MATERIALIZED.value
    assert result["domain"]["status"] != DomainState.ACTIVE.value
    assert result["manifest"]["post_validation"]["required"] is True


def test_materializer_populates_rollback_manifest(tmp_path):
    result = materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")
    rollback = result["domain"]["rollback_manifest"]

    assert rollback["can_rollback"] is True
    assert result["domain_dir"] in rollback["created_paths"]
    assert result["domain_json_path"] in rollback["created_paths"]
    assert result["manifest_path"] in rollback["created_paths"]
    assert rollback["modified_paths"] == []
    assert rollback["backup_paths"] == []


def test_materializer_blocks_duplicate_ids_in_sandbox_root(tmp_path):
    root = tmp_path / "sandboxes"
    materialize_sandbox_domain(_schema(), sandbox_root=root)

    with pytest.raises(ValueError, match="dominios duplicados"):
        materialize_sandbox_domain(_schema(), sandbox_root=root)


def test_materializer_blocks_legacy_equivalent_domain(tmp_path):
    legacy_like = _schema(
        domain_id="loteria",
        name="Loteria / IA_CORE",
        description="Intento de recuperar legacy sin flujo formal.",
    )

    with pytest.raises(ValueError, match="dominios duplicados"):
        materialize_sandbox_domain(legacy_like, sandbox_root=tmp_path / "sandboxes")


def test_materializer_blocks_real_domains_root():
    with pytest.raises(ValueError, match="domains/ operativo"):
        materialize_sandbox_domain(_schema(), sandbox_root=DOMAINS)


def test_materializer_blocks_paths_outside_allowed_sandbox(tmp_path):
    outside = deepcopy(_schema())
    outside["domain_id"] = "../escape"

    with pytest.raises(ValueError, match="domain_id invalido"):
        materialize_sandbox_domain(outside, sandbox_root=tmp_path / "sandboxes")


def test_post_materialization_validation_checks_structure(tmp_path):
    result = materialize_sandbox_domain(_schema(), sandbox_root=tmp_path / "sandboxes")

    validation = validate_materialized_sandbox_domain(result["domain_dir"])

    assert validation["success"] is True
    assert validation["domain"]["domain_id"] == result["domain_id"]
    assert validation["manifest"]["materialization_id"] == result["materialization_id"]
