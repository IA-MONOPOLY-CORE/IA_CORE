import hashlib
import json
from pathlib import Path

from core.agent_preset_materializer import materialize_agent_presets, rollback_agent_presets
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materialization_rollback import rollback_domain_materialization
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed, rollback_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog, rollback_profile_catalog
from core.sandbox_agent_materializer import materialize_sandbox_agent, rollback_sandbox_agent
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_team_materializer import (
    materialize_sandbox_team,
    regenerate_sandbox_team,
    rollback_sandbox_team,
    validate_materialized_sandbox_team,
)


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"
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
        objective="team chain checkpoint",
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


def _coordination(agent_ids: list[str]) -> dict:
    return {
        "coordination_type": "single_coordinator",
        "coordinator_agent_id": agent_ids[0],
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": ["Checkpoint declarativo; no ejecuta coordinacion."],
        "suggested_order": list(agent_ids),
        "restrictions": ["Sin debate runtime.", "Sin pipeline ejecutable."],
    }


def _capabilities(domain_id: str, owner_agent_id: str) -> dict:
    tool = build_tool_contract(
        tool_id="tool_team_checkpoint_declared",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        tool_name="Future Team Checkpoint Tool",
        tool_category="internal_future",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    return {
        "memory": [],
        "tools": [tool],
        "policies": [
            {
                "policy_id": "policy_team_checkpoint_declared",
                "status": "declared",
                "declared_only": True,
                "runtime_enabled": False,
                "execution_enabled": False,
                "external_access": False,
            }
        ],
    }


def test_full_sandbox_chain_with_team_checkpoint(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    root = tmp_path / "sandboxes"
    domain = materialize_sandbox_domain(_schema_from_preview(_preview()), sandbox_root=root)
    domain_dir = Path(domain["domain_dir"])

    profile = materialize_profile_catalog(domain_dir)
    presets = materialize_agent_presets(domain_dir)
    paper_seed = materialize_paper_seed(domain_dir)
    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
        for preset in presets_payload["presets"]
    ]
    agent_ids = [agent["agent_id"] for agent in agents]
    team = materialize_sandbox_team(
        domain_dir,
        team_id="checkpoint_team",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )

    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    artifact_types = [artifact["artifact_type"] for artifact in manifest["artifacts"]]
    assert artifact_types == ["profile_catalog", "agent_preset", "paper_seed", "agent", "agent", "team"]
    assert Path(profile["profile_catalog_path"]).is_file()
    assert Path(presets["agent_presets_path"]).is_file()
    assert Path(paper_seed["paper_seed_path"]).is_file()
    assert all(Path(agent["agent_path"]).is_file() for agent in agents)
    assert Path(team["team_path"]).is_file()

    team_validation = validate_materialized_sandbox_team(domain_dir, team_id=team["team_id"])
    team_artifact = team_validation["artifact"]
    assert team_artifact["artifact_type"] == "team"
    assert team_artifact["dependencies"][:3] == [
        "profile_catalog_main",
        "agent_presets_main",
        "paper_seed_main",
    ]
    assert team_artifact["dependencies"][3:] == [f"agent_{agent_id}" for agent_id in agent_ids]
    assert team_validation["team"]["dependencies"] == [f"agent_{agent_id}" for agent_id in agent_ids]

    for agent in agents:
        assert agent["lineage"]["origin"]["source_profile_id"]
        assert agent["agent"]["status"] == "materialized"
        assert agent["agent"]["sandbox_config"]["runtime_enabled"] is False
    assert team_validation["team"]["status"] == "materialized"
    assert team_validation["team"]["metadata"]["runtime_enabled"] is False
    assert team_validation["team"]["metadata"]["execution_enabled"] is False
    assert team_validation["team"]["coordination_model"]["runtime_enabled"] is False
    assert team_validation["team"]["coordination_model"]["execution_enabled"] is False
    assert team_validation["team"]["capabilities"]["tools"][0]["execution_allowed"] is False
    assert team_validation["team"]["capabilities"]["tools"][0]["external_access"] is False
    assert team_validation["team"]["capabilities"]["policies"][0]["external_access"] is False
    assert all(artifact["status"] != "active" for artifact in manifest["artifacts"])

    regenerated = regenerate_sandbox_team(
        domain_dir,
        team_id=team["team_id"],
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
        purpose="Checkpoint team regenerado sin runtime.",
    )
    assert regenerated["team_id"] == team["team_id"]
    assert regenerated["version"] == "1.0.1"
    assert [member["agent_id"] for member in regenerated["team"]["member_agents"]] == agent_ids
    assert regenerated["artifact"]["dependencies"][3:] == [f"agent_{agent_id}" for agent_id in agent_ids]
    assert [event["event"] for event in regenerated["team"]["history"]] == [
        "materialized",
        "regenerated",
    ]
    assert regenerated["team"]["metadata"]["runtime_enabled"] is False

    team_rollback = rollback_sandbox_team(domain_dir, team_id=team["team_id"])
    assert team_rollback["status"] == "rolled_back"
    assert not Path(regenerated["team_path"]).exists()
    assert all(Path(agent["agent_path"]).is_file() for agent in agents)
    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    assert "team" not in [artifact["artifact_type"] for artifact in manifest["artifacts"]]

    for agent in reversed(agents):
        rollback_sandbox_agent(domain_dir, agent_id=agent["agent_id"])
    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
        "paper_seed",
    ]
    assert Path(paper_seed["paper_seed_path"]).is_file()

    rollback_paper_seed(domain_dir)
    rollback_agent_presets(domain_dir)
    rollback_profile_catalog(domain_dir)
    manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    assert manifest["artifacts"] == []

    total = rollback_domain_materialization(manifest_path=domain["manifest_path"])
    assert total["status"] == "rolled_back"
    assert not domain_dir.exists()
    assert not list(root.glob("*/domain.json"))
    assert list((root / "_rollback_records").glob("*.json"))

    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers
