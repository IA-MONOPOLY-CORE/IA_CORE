import hashlib
import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import (
    AGENT_PRESETS_ARTIFACT_ID,
    materialize_agent_presets,
    rollback_agent_presets,
    validate_materialized_agent_presets,
)
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.profile_catalog_materializer import (
    PROFILE_CATALOG_ARTIFACT_ID,
    materialize_profile_catalog,
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


def _domain_with_profile_catalog(tmp_path) -> dict:
    domain = _materialized_domain(tmp_path)
    materialize_profile_catalog(domain["domain_dir"])
    return domain


def test_requires_profile_catalog(tmp_path):
    domain = _materialized_domain(tmp_path)

    with pytest.raises(FileNotFoundError, match="artifact_manifest"):
        materialize_agent_presets(domain["domain_dir"])


def test_valid_sandbox_materializes_agent_presets(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)

    result = materialize_agent_presets(domain["domain_dir"])

    presets_path = Path(result["agent_presets_path"])
    payload = json.loads(presets_path.read_text(encoding="utf-8"))
    assert presets_path.is_file()
    assert payload["artifact_type"] == "derived_domain_agent_presets"
    assert payload["sandbox_artifact"]["artifact_id"] == AGENT_PRESETS_ARTIFACT_ID
    assert payload["presets"]


def test_artifact_manifest_is_updated(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)

    result = materialize_agent_presets(domain["domain_dir"])

    artifact_types = [artifact["artifact_type"] for artifact in result["artifact_manifest"]["artifacts"]]
    assert artifact_types == ["profile_catalog", "agent_preset"]


def test_artifact_id_is_generated(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)

    result = materialize_agent_presets(domain["domain_dir"])

    assert result["artifact_id"] == AGENT_PRESETS_ARTIFACT_ID
    assert result["artifact"]["artifact_id"] == AGENT_PRESETS_ARTIFACT_ID
    first_preset = json.loads(Path(result["agent_presets_path"]).read_text(encoding="utf-8"))[
        "presets"
    ][0]
    assert first_preset["artifact_id"].startswith("agent_preset_")


def test_profile_catalog_dependency_is_registered(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)

    result = materialize_agent_presets(domain["domain_dir"])
    payload = json.loads(Path(result["agent_presets_path"]).read_text(encoding="utf-8"))

    assert result["artifact"]["dependencies"] == [PROFILE_CATALOG_ARTIFACT_ID]
    assert result["artifact"]["rollback_info"]["depends_on"] == [PROFILE_CATALOG_ARTIFACT_ID]
    assert payload["presets"][0]["dependencies"] == [PROFILE_CATALOG_ARTIFACT_ID]
    assert (
        payload["presets"][0]["profile_reference"]["profile_catalog_artifact_id"]
        == PROFILE_CATALOG_ARTIFACT_ID
    )


def test_global_catalogs_are_not_modified(tmp_path):
    before = _tree_hash(CATALOGS)
    domain = _domain_with_profile_catalog(tmp_path)

    materialize_agent_presets(domain["domain_dir"])

    assert _tree_hash(CATALOGS) == before


def test_operational_domains_are_not_modified(tmp_path):
    before = _tree_hash(DOMAINS)
    domain = _domain_with_profile_catalog(tmp_path)

    materialize_agent_presets(domain["domain_dir"])

    assert _tree_hash(DOMAINS) == before
    assert not (DOMAINS / domain["domain_id"]).exists()


def test_agent_presets_rollback_removes_presets(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)
    result = materialize_agent_presets(domain["domain_dir"])
    presets_path = Path(result["agent_presets_path"])

    rollback = rollback_agent_presets(domain["domain_dir"])

    assert rollback["status"] == "rolled_back"
    assert not presets_path.exists()
    assert not (Path(domain["domain_dir"]) / "agent_presets").exists()


def test_agent_presets_rollback_preserves_profile_catalog(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)
    materialize_agent_presets(domain["domain_dir"])
    profile_path = Path(domain["domain_dir"]) / "profile_catalog" / "profile_catalog.json"

    rollback = rollback_agent_presets(domain["domain_dir"])

    assert profile_path.is_file()
    assert [artifact["artifact_type"] for artifact in rollback["artifact_manifest"]["artifacts"]] == [
        "profile_catalog"
    ]


def test_regeneration_creates_new_version_and_keeps_dependency(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)
    first = materialize_agent_presets(domain["domain_dir"])

    second = materialize_agent_presets(domain["domain_dir"], regenerate=True)

    assert first["version"] == "1.0.0"
    assert second["version"] == "1.0.1"
    assert second["artifact"]["dependencies"] == [PROFILE_CATALOG_ARTIFACT_ID]
    assert second["artifact"]["history"][0]["previous_version"] == "1.0.0"
    assert Path(second["artifact"]["history"][0]["archived_agent_presets_path"]).is_file()


def test_duplicate_agent_presets_is_blocked_without_regeneration(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)
    materialize_agent_presets(domain["domain_dir"])

    with pytest.raises(FileExistsError, match="agent_presets ya existe"):
        materialize_agent_presets(domain["domain_dir"])


def test_materialized_state_is_correct_and_not_active(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)

    result = materialize_agent_presets(domain["domain_dir"])
    validation = validate_materialized_agent_presets(domain["domain_dir"])

    payload = json.loads(Path(result["agent_presets_path"]).read_text(encoding="utf-8"))
    assert validation["artifact"]["status"] == "materialized"
    assert validation["artifact"]["operational"] is False
    assert payload["presets"][0]["status"] == "materialized"
    assert payload["presets"][0]["activo"] is False


def test_traceability_is_complete(tmp_path):
    domain = _domain_with_profile_catalog(tmp_path)

    result = materialize_agent_presets(
        domain["domain_dir"],
        execution_metadata={"prompt": "2.1"},
    )
    artifact = result["artifact"]

    assert artifact["created_from"]["materialization_id"] == domain["materialization_id"]
    assert artifact["created_from"]["domain_id"] == domain["domain_id"]
    assert artifact["created_from"]["profile_catalog_artifact_id"] == PROFILE_CATALOG_ARTIFACT_ID
    assert artifact["created_from"]["generator"].endswith("generate_agent_presets_for_profile_catalog")
    assert artifact["created_from"]["execution_metadata"] == {"prompt": "2.1"}
    assert artifact["rollback_info"]["safe_remove"] is True
    assert artifact["rollback_info"]["created_paths"]
