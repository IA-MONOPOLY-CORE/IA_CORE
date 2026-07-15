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


ROOT = Path(__file__).parent.parent
CATALOGS = ROOT / "catalogs"
DOMAINS = ROOT / "domains"
AGENTS = ROOT / "agents"
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
        objective="checkpoint minimo controlado",
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


def test_minimum_controlled_sandbox_chain_and_rollbacks(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    root = tmp_path / "sandboxes"
    preview = _preview()
    domain = materialize_sandbox_domain(_schema_from_preview(preview), sandbox_root=root)
    domain_dir = Path(domain["domain_dir"])

    profile = materialize_profile_catalog(domain_dir)
    presets = materialize_agent_presets(domain_dir)
    paper_seed = materialize_paper_seed(domain_dir)
    agent = materialize_sandbox_agent(domain_dir)

    manifest = validate_artifact_manifest_file(agent["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
    ]
    assert agent["lineage"]["origin"]["source_profile_id"]
    assert agent["agent"]["status"] == "materialized"
    assert agent["agent"]["sandbox_config"]["runtime_enabled"] is False
    assert all(artifact["status"] != "active" for artifact in manifest["artifacts"])

    rollback_sandbox_agent(domain_dir, agent_id=agent["agent_id"])
    manifest = validate_artifact_manifest_file(agent["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
        "paper_seed",
    ]
    assert not Path(agent["agent_path"]).exists()
    assert Path(paper_seed["paper_seed_path"]).is_file()

    rollback_paper_seed(domain_dir)
    manifest = validate_artifact_manifest_file(agent["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == [
        "profile_catalog",
        "agent_preset",
    ]
    assert Path(presets["agent_presets_path"]).is_file()

    rollback_agent_presets(domain_dir)
    manifest = validate_artifact_manifest_file(agent["artifact_manifest_path"])
    assert [artifact["artifact_type"] for artifact in manifest["artifacts"]] == ["profile_catalog"]
    assert Path(profile["profile_catalog_path"]).is_file()

    rollback_profile_catalog(domain_dir)
    manifest = validate_artifact_manifest_file(agent["artifact_manifest_path"])
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
