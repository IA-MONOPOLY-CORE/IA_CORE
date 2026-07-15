import hashlib
import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID, materialize_agent_presets
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import (
    PAPER_SEED_ARTIFACT_ID,
    materialize_paper_seed,
    rollback_paper_seed,
    validate_materialized_paper_seed,
)
from core.profile_catalog_materializer import (
    PROFILE_CATALOG_ARTIFACT_ID,
    materialize_profile_catalog,
)


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _papers_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(DOMAINS.glob("*/agents/papers/*.json")):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
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


def _domain_with_presets(tmp_path) -> dict:
    domain = _materialized_domain(tmp_path)
    materialize_profile_catalog(domain["domain_dir"])
    materialize_agent_presets(domain["domain_dir"])
    return domain


def test_valid_sandbox_materializes_paper_seed(tmp_path):
    domain = _domain_with_presets(tmp_path)

    result = materialize_paper_seed(domain["domain_dir"])

    paper_path = Path(result["paper_seed_path"])
    payload = json.loads(paper_path.read_text(encoding="utf-8"))
    assert paper_path.is_file()
    assert payload["artifact_type"] == "sandbox_paper_seed_collection"
    assert payload["sandbox_artifact"]["artifact_id"] == PAPER_SEED_ARTIFACT_ID
    assert payload["paper_seeds"]


def test_artifact_manifest_is_updated(tmp_path):
    domain = _domain_with_presets(tmp_path)

    result = materialize_paper_seed(domain["domain_dir"])

    artifact_types = [artifact["artifact_type"] for artifact in result["artifact_manifest"]["artifacts"]]
    assert artifact_types == ["profile_catalog", "agent_preset", "paper_seed"]


def test_artifact_id_is_generated(tmp_path):
    domain = _domain_with_presets(tmp_path)

    result = materialize_paper_seed(domain["domain_dir"])
    first_seed = json.loads(Path(result["paper_seed_path"]).read_text(encoding="utf-8"))[
        "paper_seeds"
    ][0]

    assert result["artifact_id"] == PAPER_SEED_ARTIFACT_ID
    assert result["artifact"]["artifact_id"] == PAPER_SEED_ARTIFACT_ID
    assert first_seed["artifact_id"].startswith("paper_seed_")


def test_dependencies_are_registered(tmp_path):
    domain = _domain_with_presets(tmp_path)

    result = materialize_paper_seed(domain["domain_dir"])
    payload = json.loads(Path(result["paper_seed_path"]).read_text(encoding="utf-8"))

    expected = [PROFILE_CATALOG_ARTIFACT_ID, AGENT_PRESETS_ARTIFACT_ID]
    assert result["artifact"]["dependencies"] == expected
    assert result["artifact"]["rollback_info"]["depends_on"] == expected
    assert payload["paper_seeds"][0]["dependencies"] == expected
    assert payload["paper_seeds"][0]["preset_reference"]["agent_presets_artifact_id"] == (
        AGENT_PRESETS_ARTIFACT_ID
    )


def test_global_papers_are_not_modified(tmp_path):
    before = _papers_hash()
    domain = _domain_with_presets(tmp_path)

    materialize_paper_seed(domain["domain_dir"])

    assert _papers_hash() == before


def test_operational_domains_are_not_modified(tmp_path):
    before = _tree_hash(DOMAINS)
    domain = _domain_with_presets(tmp_path)

    materialize_paper_seed(domain["domain_dir"])

    assert _tree_hash(DOMAINS) == before
    assert not (DOMAINS / domain["domain_id"]).exists()


def test_paper_seed_rollback_removes_only_paper_seed(tmp_path):
    domain = _domain_with_presets(tmp_path)
    result = materialize_paper_seed(domain["domain_dir"])
    paper_path = Path(result["paper_seed_path"])

    rollback = rollback_paper_seed(domain["domain_dir"])

    assert rollback["status"] == "rolled_back"
    assert not paper_path.exists()
    assert not (Path(domain["domain_dir"]) / "paper_seed").exists()


def test_paper_seed_rollback_preserves_dependencies(tmp_path):
    domain = _domain_with_presets(tmp_path)
    materialize_paper_seed(domain["domain_dir"])
    profile_path = Path(domain["domain_dir"]) / "profile_catalog" / "profile_catalog.json"
    presets_path = Path(domain["domain_dir"]) / "agent_presets" / "agent_presets.json"

    rollback = rollback_paper_seed(domain["domain_dir"])

    assert profile_path.is_file()
    assert presets_path.is_file()
    assert [artifact["artifact_type"] for artifact in rollback["artifact_manifest"]["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
    ]


def test_regeneration_creates_new_version_and_keeps_dependencies(tmp_path):
    domain = _domain_with_presets(tmp_path)
    first = materialize_paper_seed(domain["domain_dir"])

    second = materialize_paper_seed(domain["domain_dir"], regenerate=True)

    expected = [PROFILE_CATALOG_ARTIFACT_ID, AGENT_PRESETS_ARTIFACT_ID]
    assert first["version"] == "1.0.0"
    assert second["version"] == "1.0.1"
    assert second["artifact"]["dependencies"] == expected
    assert second["artifact"]["history"][0]["previous_version"] == "1.0.0"
    assert Path(second["artifact"]["history"][0]["archived_paper_seed_path"]).is_file()


def test_duplicate_paper_seed_is_blocked_without_regeneration(tmp_path):
    domain = _domain_with_presets(tmp_path)
    materialize_paper_seed(domain["domain_dir"])

    with pytest.raises(FileExistsError, match="paper_seed ya existe"):
        materialize_paper_seed(domain["domain_dir"])


def test_materialized_state_is_correct_and_not_active(tmp_path):
    domain = _domain_with_presets(tmp_path)

    result = materialize_paper_seed(domain["domain_dir"])
    validation = validate_materialized_paper_seed(domain["domain_dir"])
    payload = json.loads(Path(result["paper_seed_path"]).read_text(encoding="utf-8"))

    assert validation["artifact"]["status"] == "materialized"
    assert validation["artifact"]["operational"] is False
    assert payload["paper_seeds"][0]["status"] == "materialized"
    assert payload["paper_seeds"][0]["active"] is False


def test_traceability_is_complete(tmp_path):
    domain = _domain_with_presets(tmp_path)

    result = materialize_paper_seed(
        domain["domain_dir"],
        execution_metadata={"prompt": "2.2"},
    )
    artifact = result["artifact"]
    payload = json.loads(Path(result["paper_seed_path"]).read_text(encoding="utf-8"))
    first_seed = payload["paper_seeds"][0]

    assert artifact["created_from"]["materialization_id"] == domain["materialization_id"]
    assert artifact["created_from"]["domain_id"] == domain["domain_id"]
    assert artifact["created_from"]["profile_catalog_artifact_id"] == PROFILE_CATALOG_ARTIFACT_ID
    assert artifact["created_from"]["agent_presets_artifact_id"] == AGENT_PRESETS_ARTIFACT_ID
    assert artifact["created_from"]["execution_metadata"] == {"prompt": "2.2"}
    assert first_seed["profile_reference"]["profile_catalog_artifact_id"] == PROFILE_CATALOG_ARTIFACT_ID
    assert first_seed["preset_reference"]["agent_presets_artifact_id"] == AGENT_PRESETS_ARTIFACT_ID
