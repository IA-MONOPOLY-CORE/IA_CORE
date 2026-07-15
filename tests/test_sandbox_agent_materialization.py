import hashlib
import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID, materialize_agent_presets
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID, materialize_paper_seed
from core.profile_catalog_materializer import (
    PROFILE_CATALOG_ARTIFACT_ID,
    materialize_profile_catalog,
)
from core.sandbox_agent_materializer import (
    materialize_sandbox_agent,
    rollback_sandbox_agent,
    validate_materialized_sandbox_agent,
)


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
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


def _domain_with_seed(tmp_path) -> dict:
    preview = _preview()
    domain = materialize_sandbox_domain(
        _schema_from_preview(preview),
        sandbox_root=tmp_path / "sandboxes",
    )
    materialize_profile_catalog(domain["domain_dir"])
    materialize_agent_presets(domain["domain_dir"])
    materialize_paper_seed(domain["domain_dir"])
    return domain


def test_materializes_agent_with_valid_dependencies(tmp_path):
    domain = _domain_with_seed(tmp_path)

    result = materialize_sandbox_agent(domain["domain_dir"])

    agent_path = Path(result["agent_path"])
    payload = json.loads(agent_path.read_text(encoding="utf-8"))
    assert agent_path.is_file()
    assert payload["agent_id"] == result["agent_id"]
    assert payload["status"] == "materialized"
    assert payload["sandbox_config"]["runtime_enabled"] is False


def test_artifact_manifest_is_updated(tmp_path):
    domain = _domain_with_seed(tmp_path)

    result = materialize_sandbox_agent(domain["domain_dir"])

    artifact_types = [artifact["artifact_type"] for artifact in result["artifact_manifest"]["artifacts"]]
    assert artifact_types == ["profile_catalog", "agent_preset", "paper_seed", "agent"]


def test_agent_id_is_generated(tmp_path):
    domain = _domain_with_seed(tmp_path)

    result = materialize_sandbox_agent(domain["domain_dir"])

    assert result["agent_id"].startswith("sandbox_")
    assert result["artifact_id"] == f"agent_{result['agent_id']}"


def test_lineage_is_registered(tmp_path):
    domain = _domain_with_seed(tmp_path)

    result = materialize_sandbox_agent(domain["domain_dir"])

    assert result["lineage"]["agent_id"] == result["agent_id"]
    assert result["artifact"]["created_from"]["lineage"]["agent_id"] == result["agent_id"]
    assert result["lineage"]["history"][0]["event"] == "materialized"


def test_does_not_create_runtime_agent(tmp_path):
    before = _tree_hash(AGENTS)
    domain = _domain_with_seed(tmp_path)

    materialize_sandbox_agent(domain["domain_dir"])

    assert _tree_hash(AGENTS) == before


def test_does_not_touch_legacy_agents(tmp_path):
    before = _tree_hash(AGENTS)
    domain = _domain_with_seed(tmp_path)

    validate_materialized_sandbox_agent(
        domain["domain_dir"],
        agent_id=materialize_sandbox_agent(domain["domain_dir"])["agent_id"],
    )

    assert _tree_hash(AGENTS) == before


def test_rollback_removes_agent(tmp_path):
    domain = _domain_with_seed(tmp_path)
    result = materialize_sandbox_agent(domain["domain_dir"])
    agent_path = Path(result["agent_path"])

    rollback = rollback_sandbox_agent(domain["domain_dir"], agent_id=result["agent_id"])

    assert rollback["status"] == "rolled_back"
    assert not agent_path.exists()
    assert not (Path(domain["domain_dir"]) / "sandbox_agents").exists()


def test_rollback_preserves_dependencies(tmp_path):
    domain = _domain_with_seed(tmp_path)
    result = materialize_sandbox_agent(domain["domain_dir"])
    profile_path = Path(domain["domain_dir"]) / "profile_catalog" / "profile_catalog.json"
    presets_path = Path(domain["domain_dir"]) / "agent_presets" / "agent_presets.json"
    paper_seed_path = Path(domain["domain_dir"]) / "paper_seed" / "paper_seed.json"

    rollback = rollback_sandbox_agent(domain["domain_dir"], agent_id=result["agent_id"])

    assert profile_path.is_file()
    assert presets_path.is_file()
    assert paper_seed_path.is_file()
    assert [artifact["artifact_type"] for artifact in rollback["artifact_manifest"]["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
        "paper_seed",
    ]


def test_regeneration_updates_version_and_history(tmp_path):
    domain = _domain_with_seed(tmp_path)
    first = materialize_sandbox_agent(domain["domain_dir"])

    second = materialize_sandbox_agent(domain["domain_dir"], regenerate=True)

    assert first["agent_id"] == second["agent_id"]
    assert first["version"] == "1.0.0"
    assert second["version"] == "1.0.1"
    assert second["lineage"]["current_version"] == "1.0.1"
    assert [event["event"] for event in second["lineage"]["history"]] == [
        "materialized",
        "regenerated",
    ]


def test_duplicate_agent_is_blocked_without_regeneration(tmp_path):
    domain = _domain_with_seed(tmp_path)
    materialize_sandbox_agent(domain["domain_dir"])

    with pytest.raises(FileExistsError, match="agent_id ya existe"):
        materialize_sandbox_agent(domain["domain_dir"])


def test_agent_state_is_materialized_not_active(tmp_path):
    domain = _domain_with_seed(tmp_path)

    result = materialize_sandbox_agent(domain["domain_dir"])
    validation = validate_materialized_sandbox_agent(domain["domain_dir"], agent_id=result["agent_id"])

    assert validation["agent"]["status"] == "materialized"
    assert validation["agent"]["metadata"]["operational"] is False
    assert validation["agent"]["metadata"]["active"] is False
    assert validation["artifact"]["status"] == "materialized"


def test_traceability_is_complete(tmp_path):
    domain = _domain_with_seed(tmp_path)

    result = materialize_sandbox_agent(
        domain["domain_dir"],
        execution_metadata={"prompt": "2.4"},
    )

    assert result["artifact"]["dependencies"] == [
        PROFILE_CATALOG_ARTIFACT_ID,
        AGENT_PRESETS_ARTIFACT_ID,
        PAPER_SEED_ARTIFACT_ID,
    ]
    assert result["agent"]["profile_reference"]["profile_catalog_artifact_id"] == (
        PROFILE_CATALOG_ARTIFACT_ID
    )
    assert result["agent"]["preset_reference"]["agent_presets_artifact_id"] == (
        AGENT_PRESETS_ARTIFACT_ID
    )
    assert result["agent"]["paper_reference"]["paper_seed_artifact_id"] == PAPER_SEED_ARTIFACT_ID
    assert result["artifact"]["created_from"]["execution_metadata"] == {"prompt": "2.4"}
