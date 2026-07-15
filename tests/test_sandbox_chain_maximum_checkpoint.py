import hashlib
import json
from pathlib import Path

import pytest

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
MAX_MATERIALIZED_DOMAINS = 12


def _load_catalog(name: str):
    data = json.loads((CATALOGS / name).read_text(encoding="utf-8"))
    return data["profiles"] if isinstance(data, dict) and "profiles" in data else data


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


def _schema_from_preview(preview: dict, *, index: int, area_id: str, niche_id: str) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["domain_id"] = preview["domain_request"]["domain_id"]
    schema["name"] = f"Sandbox Checkpoint {index:03d} {niche_id}"
    schema["description"] = f"Dominio sandbox checkpoint para {area_id}/{niche_id}."
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    return schema


def test_maximum_current_sandbox_surface_checkpoint(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    areas = [area for area in _load_catalog("areas.json") if area.get("activo", True)]
    niches = [niche for niche in _load_catalog("niches.json") if niche.get("activo", True)]
    profiles = _load_catalog("professional_profiles.json")
    roles = [role for role in _load_catalog("roles.json") if role.get("activo", True)]
    specializations = [
        spec for spec in _load_catalog("specializations.json") if spec.get("activo", True)
    ]
    pairs = sorted((niche["area_id"], niche["id"]) for niche in niches)

    assert len(areas) == 30
    assert len(niches) == 200
    assert len(profiles) == 106
    assert len(roles) == 20
    assert len(specializations) == 80
    assert len(pairs) == 200

    root = tmp_path / "maximum_sandboxes"
    totals = {
        "domains_attempted": 0,
        "domains_materialized": 0,
        "duplicates_blocked": 0,
        "profile_catalogs": 0,
        "profiles": 0,
        "presets": 0,
        "paper_seed_collections": 0,
        "paper_seeds": 0,
        "agents": 0,
        "regenerations": 0,
        "selective_rollbacks": 0,
        "total_rollbacks": 0,
    }
    materializations = []

    for index, (area_id, niche_id) in enumerate(pairs[:MAX_MATERIALIZED_DOMAINS], start=1):
        domain_id = f"sandbox_checkpoint_{index:03d}_{niche_id}"
        preview = build_domain_materialization_preview(
            domain_id=domain_id,
            area_id=area_id,
            niche_ids=[niche_id],
            business_scale="pyme",
            objective="maximum checkpoint",
            complexity_level="media",
        )
        schema = _schema_from_preview(preview, index=index, area_id=area_id, niche_id=niche_id)
        totals["domains_attempted"] += 1
        domain = materialize_sandbox_domain(schema, sandbox_root=root)
        totals["domains_materialized"] += 1

        with pytest.raises((FileExistsError, ValueError)):
            materialize_sandbox_domain(schema, sandbox_root=root)
        totals["duplicates_blocked"] += 1

        profile = materialize_profile_catalog(domain["domain_dir"])
        totals["profile_catalogs"] += 1
        profile_payload = json.loads(Path(profile["profile_catalog_path"]).read_text(encoding="utf-8"))
        totals["profiles"] += len(profile_payload["profiles"])

        presets = materialize_agent_presets(domain["domain_dir"])
        presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
        totals["presets"] += len(presets_payload["presets"])

        paper = materialize_paper_seed(domain["domain_dir"])
        paper_payload = json.loads(Path(paper["paper_seed_path"]).read_text(encoding="utf-8"))
        totals["paper_seed_collections"] += 1
        totals["paper_seeds"] += len(paper_payload["paper_seeds"])

        agents = []
        for preset in presets_payload["presets"]:
            agent = materialize_sandbox_agent(domain["domain_dir"], preset_id=preset["preset_id"])
            agents.append(agent)
            totals["agents"] += 1
            assert agent["agent"]["status"] == "materialized"
            assert agent["agent"]["sandbox_config"]["runtime_enabled"] is False
            with pytest.raises(FileExistsError):
                materialize_sandbox_agent(domain["domain_dir"], preset_id=preset["preset_id"])
            totals["duplicates_blocked"] += 1

        if index == 1 and agents:
            materialize_profile_catalog(domain["domain_dir"], regenerate=True)
            materialize_agent_presets(domain["domain_dir"], regenerate=True)
            materialize_paper_seed(domain["domain_dir"], regenerate=True)
            materialize_sandbox_agent(
                domain["domain_dir"],
                preset_id=presets_payload["presets"][0]["preset_id"],
                regenerate=True,
            )
            totals["regenerations"] += 4

        manifest = validate_artifact_manifest_file(agents[-1]["artifact_manifest_path"])
        assert all(artifact["status"] != "active" for artifact in manifest["artifacts"])
        materializations.append((domain, profile, presets, paper, agents))

    assert totals["domains_attempted"] == MAX_MATERIALIZED_DOMAINS
    assert totals["domains_materialized"] == MAX_MATERIALIZED_DOMAINS
    assert totals["profile_catalogs"] == MAX_MATERIALIZED_DOMAINS
    assert totals["presets"] == totals["paper_seeds"] == totals["agents"]
    assert totals["agents"] > 0
    assert totals["regenerations"] == 4

    for domain, _profile, _presets, _paper, agents in reversed(materializations):
        for agent in reversed(agents):
            rollback_sandbox_agent(domain["domain_dir"], agent_id=agent["agent_id"])
            totals["selective_rollbacks"] += 1
        rollback_paper_seed(domain["domain_dir"])
        rollback_agent_presets(domain["domain_dir"])
        rollback_profile_catalog(domain["domain_dir"])
        totals["selective_rollbacks"] += 3
        manifest = validate_artifact_manifest_file(Path(domain["domain_dir"]) / "manifests" / "artifact_manifest.json")
        assert manifest["artifacts"] == []
        total = rollback_domain_materialization(manifest_path=domain["manifest_path"])
        assert total["status"] == "rolled_back"
        totals["total_rollbacks"] += 1

    assert totals["total_rollbacks"] == MAX_MATERIALIZED_DOMAINS
    assert not list(root.glob("*/domain.json"))
    assert list((root / "_rollback_records").glob("*.json"))
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers
