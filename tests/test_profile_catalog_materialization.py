import hashlib
import json
from pathlib import Path

import pytest

from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materialization_rollback import rollback_domain_materialization
from core.domain_materializer import materialize_sandbox_domain
from core.profile_catalog_materializer import (
    PROFILE_CATALOG_ARTIFACT_ID,
    materialize_profile_catalog,
    validate_materialized_profile_catalog,
)


ROOT = Path(__file__).parent.parent
CATALOGS = ROOT / "catalogs"
DOMAINS = ROOT / "domains"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )


def _schema_from_preview(preview: dict) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    return schema


def _materialized_domain(tmp_path) -> dict:
    preview = _preview()
    return materialize_sandbox_domain(
        _schema_from_preview(preview),
        sandbox_root=tmp_path / "sandboxes",
    )


def test_valid_sandbox_receives_profile_catalog(tmp_path):
    domain = _materialized_domain(tmp_path)

    result = materialize_profile_catalog(domain["domain_dir"])

    profile_path = Path(result["profile_catalog_path"])
    payload = json.loads(profile_path.read_text(encoding="utf-8"))
    assert profile_path.is_file()
    assert payload["artifact_type"] == "derived_domain_profile_catalog"
    assert payload["sandbox_artifact"]["artifact_id"] == PROFILE_CATALOG_ARTIFACT_ID
    assert payload["profiles"]


def test_artifact_manifest_is_created_and_updated(tmp_path):
    domain = _materialized_domain(tmp_path)

    result = materialize_profile_catalog(domain["domain_dir"])

    manifest_path = Path(result["artifact_manifest_path"])
    assert manifest_path.is_file()
    assert result["artifact_manifest"]["domain_id"] == domain["domain_id"]
    assert result["artifact_manifest"]["artifacts"][0]["artifact_type"] == "profile_catalog"


def test_artifact_id_is_generated_for_profile_catalog(tmp_path):
    domain = _materialized_domain(tmp_path)

    result = materialize_profile_catalog(domain["domain_dir"])

    artifact = result["artifact_manifest"]["artifacts"][0]
    assert artifact["artifact_id"] == PROFILE_CATALOG_ARTIFACT_ID
    assert result["artifact_id"] == PROFILE_CATALOG_ARTIFACT_ID


def test_global_catalogs_are_not_modified(tmp_path):
    before = _tree_hash(CATALOGS)
    domain = _materialized_domain(tmp_path)

    materialize_profile_catalog(domain["domain_dir"])

    assert _tree_hash(CATALOGS) == before


def test_operational_domains_are_not_modified(tmp_path):
    before = _tree_hash(DOMAINS)
    domain = _materialized_domain(tmp_path)

    materialize_profile_catalog(domain["domain_dir"])

    assert _tree_hash(DOMAINS) == before
    assert not (DOMAINS / domain["domain_id"]).exists()


def test_full_sandbox_rollback_eliminates_profile_catalog_artifact(tmp_path):
    domain = _materialized_domain(tmp_path)
    result = materialize_profile_catalog(domain["domain_dir"])
    profile_path = Path(result["profile_catalog_path"])

    rollback = rollback_domain_materialization(manifest_path=domain["manifest_path"])

    assert rollback["status"] == "rolled_back"
    assert not profile_path.exists()
    assert not Path(domain["domain_dir"]).exists()


def test_regeneration_requires_explicit_flag_and_generates_new_version(tmp_path):
    domain = _materialized_domain(tmp_path)
    first = materialize_profile_catalog(domain["domain_dir"])

    second = materialize_profile_catalog(domain["domain_dir"], regenerate=True)

    assert first["version"] == "1.0.0"
    assert second["version"] == "1.0.1"
    assert second["regenerated"] is True
    assert second["artifact"]["history"][0]["previous_version"] == "1.0.0"
    history_path = Path(second["artifact"]["history"][0]["archived_profile_catalog_path"])
    assert history_path.is_file()


def test_duplicate_profile_catalog_is_blocked_without_regeneration(tmp_path):
    domain = _materialized_domain(tmp_path)
    materialize_profile_catalog(domain["domain_dir"])

    with pytest.raises(FileExistsError, match="profile_catalog ya existe"):
        materialize_profile_catalog(domain["domain_dir"])


def test_materialized_state_is_correct_and_not_active(tmp_path):
    domain = _materialized_domain(tmp_path)

    result = materialize_profile_catalog(domain["domain_dir"])
    validation = validate_materialized_profile_catalog(domain["domain_dir"])

    assert result["status"] == "materialized"
    assert validation["artifact"]["status"] == "materialized"
    assert validation["artifact"]["operational"] is False
    assert validation["profile_catalog"]["sandbox_artifact"]["active"] is False


def test_traceability_is_complete(tmp_path):
    domain = _materialized_domain(tmp_path)

    result = materialize_profile_catalog(
        domain["domain_dir"],
        execution_metadata={"prompt": "2.0"},
    )
    artifact = result["artifact"]

    assert artifact["created_from"]["materialization_id"] == domain["materialization_id"]
    assert artifact["created_from"]["domain_id"] == domain["domain_id"]
    assert artifact["created_from"]["generator"].endswith("generate_profile_catalog_for_domain")
    assert artifact["created_from"]["execution_metadata"] == {"prompt": "2.0"}
    assert artifact["rollback_info"]["safe_remove"] is True
    assert artifact["rollback_info"]["created_paths"]
    assert result["materialization_manifest"]["rollback_manifest"]["created_paths"]
