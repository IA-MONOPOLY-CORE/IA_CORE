import hashlib
import json
from pathlib import Path

from core.agent_preset_materializer import materialize_agent_presets
from core.capability_policy_schema import build_capability_policy
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH, materialize_profile_catalog
from core.promotion_gate import evaluate_promotion_gate
from core.sandbox_agent_materializer import materialize_sandbox_agent
from core.sandbox_team_materializer import materialize_sandbox_team
from tests.test_sandbox_chain_with_team_checkpoint import _capabilities, _coordination


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
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
        objective="promotion gate",
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


def _build_chain(tmp_path: Path) -> dict:
    domain = materialize_sandbox_domain(
        _schema_from_preview(_preview()),
        sandbox_root=tmp_path / "sandboxes",
    )
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
        team_id="promotion_team",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )
    return {
        "domain": domain,
        "domain_dir": domain_dir,
        "profile": profile,
        "presets": presets,
        "paper_seed": paper_seed,
        "agents": agents,
        "agent_ids": agent_ids,
        "team": team,
    }


def _valid_policy(**overrides):
    policy = build_capability_policy(
        policy_id="policy_sandbox_growth_strategist_tool_declared",
        domain_id="sandbox_marketing_crm_automation",
        subject_type="agent",
        subject_id="sandbox_growth_strategist",
        capability_type="tool",
        capability_id="tool_sandbox_growth_strategist_declared",
        capability_category="internal_future",
        policy_status="allowed_declared",
        created_at="2026-07-16T00:00:00",
        updated_at="2026-07-16T00:00:00",
    )
    policy.update(overrides)
    return policy


def test_promotion_gate_evaluates_materialized_domain(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="domain",
        domain_dir=chain["domain_dir"],
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert result["requested_status"] == "validated"
    assert any(check["check"] == "minimum_chain" for check in result["checks"])


def test_promotion_gate_evaluates_profile_catalog(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="profile_catalog",
        domain_dir=chain["domain_dir"],
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert result["target_id"] == "profile_catalog_main"


def test_promotion_gate_evaluates_agent_presets(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="agent_preset",
        domain_dir=chain["domain_dir"],
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert result["target_id"] == "agent_presets_main"


def test_promotion_gate_evaluates_paper_seed(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="paper_seed",
        domain_dir=chain["domain_dir"],
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert result["target_id"] == "paper_seed_main"


def test_promotion_gate_evaluates_sandbox_agent(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id = chain["agent_ids"][0]

    result = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert any(check["check"] == "lineage" for check in result["checks"])


def test_promotion_gate_evaluates_sandbox_team(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert any(check["check"] == "team_members" for check in result["checks"])


def test_promotion_gate_evaluates_capability_policy():
    result = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(),
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert result["capability_policy_result"] == "passed"


def test_candidate_for_activation_can_pass(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="candidate_for_activation",
    )

    assert result["gate_result"] == "passed"
    assert result["requested_status"] == "candidate_for_activation"


def test_active_request_always_blocks(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="profile_catalog",
        domain_dir=chain["domain_dir"],
        requested_status="active",
    )

    assert result["gate_result"] == "blocked"
    assert "active" in " ".join(result["blockers"])


def test_broken_archived_and_legacy_block():
    broken = evaluate_promotion_gate(
        target_type="artifact",
        target={"artifact_id": "profile_catalog_main", "status": "broken"},
        requested_status="validated",
    )
    archived = evaluate_promotion_gate(
        target_type="artifact",
        target={"artifact_id": "profile_catalog_main", "status": "archived"},
        requested_status="validated",
    )
    legacy = evaluate_promotion_gate(
        target_type="artifact",
        target={"artifact_id": "profile_catalog_main", "status": "legacy"},
        requested_status="validated",
    )

    assert broken["gate_result"] == "blocked"
    assert archived["gate_result"] == "blocked"
    assert legacy["gate_result"] == "blocked"


def test_runtime_enabled_blocks_agent(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id = chain["agent_ids"][0]
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
    agent = json.loads(agent_path.read_text(encoding="utf-8"))
    agent["sandbox_config"]["runtime_enabled"] = True
    agent_path.write_text(json.dumps(agent, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        requested_status="validated",
    )

    assert result["gate_result"] == "blocked"
    assert any("runtime_enabled" in blocker for blocker in result["blockers"])


def test_execution_enabled_blocks_team(tmp_path):
    chain = _build_chain(tmp_path)
    team_path = Path(chain["team"]["team_path"])
    team = json.loads(team_path.read_text(encoding="utf-8"))
    team["coordination_model"]["execution_enabled"] = True
    team_path.write_text(json.dumps(team, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
    )

    assert result["gate_result"] == "blocked"
    assert "execution_enabled" in " ".join(result["blockers"])


def test_external_access_blocks_capability_policy():
    result = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(external_access=True),
        requested_status="validated",
    )

    assert result["gate_result"] == "blocked"
    assert "external_access" in " ".join(result["blockers"])


def test_invalid_capability_policy_blocks():
    result = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(capability_type="policy", restrictions=["self_approval"]),
        requested_status="validated",
    )

    assert result["gate_result"] == "blocked"
    assert "self_approval" in " ".join(result["blockers"])


def test_agent_without_valid_lineage_blocks(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id = chain["agent_ids"][0]
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
    agent = json.loads(agent_path.read_text(encoding="utf-8"))
    agent.pop("lineage")
    agent_path.write_text(json.dumps(agent, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        requested_status="validated",
    )

    assert result["gate_result"] == "blocked"
    assert "lineage" in " ".join(result["blockers"])


def test_manifest_inconsistent_blocks(tmp_path):
    chain = _build_chain(tmp_path)
    manifest_path = chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"][1]["dependencies"] = ["missing_profile_catalog"]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = evaluate_promotion_gate(
        target_type="artifact",
        domain_dir=chain["domain_dir"],
        target_id="agent_presets_main",
        requested_status="validated",
    )

    assert result["gate_result"] == "blocked"
    assert "dependencia" in " ".join(result["blockers"]) or "dependencies" in " ".join(result["blockers"])


def test_evaluation_does_not_mutate_target_or_operational_roots(tmp_path):
    chain = _build_chain(tmp_path)
    before_sandbox = _tree_hash(chain["domain_dir"])
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)

    result = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
    )

    assert result["gate_result"] == "passed"
    assert _tree_hash(chain["domain_dir"]) == before_sandbox
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
