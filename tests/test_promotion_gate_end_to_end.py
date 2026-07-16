import hashlib
import json
from pathlib import Path

from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _build_chain, _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"


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


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _target_requests(chain: dict, policy: dict) -> list[dict]:
    agent_id = chain["agent_ids"][0]
    return [
        {"target_type": "domain", "domain_dir": chain["domain_dir"]},
        {"target_type": "profile_catalog", "domain_dir": chain["domain_dir"]},
        {"target_type": "agent_preset", "domain_dir": chain["domain_dir"]},
        {"target_type": "paper_seed", "domain_dir": chain["domain_dir"]},
        {
            "target_type": "agent",
            "domain_dir": chain["domain_dir"],
            "target_id": agent_id,
        },
        {
            "target_type": "team",
            "domain_dir": chain["domain_dir"],
            "target_id": chain["team"]["team_id"],
        },
        {"target_type": "capability_policy", "target": policy},
    ]


def _evaluate(request: dict, requested_status: str) -> dict:
    return evaluate_promotion_gate(**request, requested_status=requested_status)


def _assert_evidence(report: dict) -> None:
    assert report["checks"]
    assert all(check["check"] for check in report["checks"])
    assert all(check["result"] for check in report["checks"])
    assert all(check["evidence"] for check in report["checks"])


def test_promotion_gate_evaluates_complete_chain_without_mutation(tmp_path):
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()
    chain = _build_chain(tmp_path)
    policy = _valid_policy()
    domain_dir = chain["domain_dir"]
    agent_id = chain["agent_ids"][0]
    team_id = chain["team"]["team_id"]
    manifest_path = domain_dir / "manifests" / "artifact_manifest.json"
    agent_path = domain_dir / "sandbox_agents" / f"{agent_id}.json"
    team_path = Path(chain["team"]["team_path"])

    before_sandbox = _tree_hash(domain_dir)
    before_manifest = _read_json(manifest_path)
    before_agent = _read_json(agent_path)
    before_team = _read_json(team_path)

    reports = []
    for request in _target_requests(chain, policy):
        for requested_status in ["validated", "candidate_for_activation"]:
            report = _evaluate(request, requested_status)
            reports.append(report)
            assert report["gate_result"] == "passed"
            assert report["requested_status"] == requested_status
            _assert_evidence(report)

    assert {report["target_type"] for report in reports} == {
        "domain",
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
        "team",
        "capability_policy",
    }
    assert _tree_hash(domain_dir) == before_sandbox
    assert _read_json(manifest_path) == before_manifest
    assert _read_json(agent_path)["lineage"] == before_agent["lineage"]
    assert _read_json(agent_path)["dependencies"] == before_agent["dependencies"]
    assert _read_json(agent_path)["sandbox_config"]["runtime_enabled"] is False
    assert _read_json(team_path)["dependencies"] == before_team["dependencies"]
    assert _read_json(team_path)["capabilities"] == before_team["capabilities"]
    assert _read_json(team_path)["coordination_model"]["execution_enabled"] is False
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers


def test_promotion_gate_blocks_active_for_complete_chain(tmp_path):
    chain = _build_chain(tmp_path)
    policy = _valid_policy()

    for request in _target_requests(chain, policy):
        report = _evaluate(request, "active")

        assert report["gate_result"] == "blocked"
        assert report["requested_status"] == "active"
        assert any("active" in blocker for blocker in report["blockers"])
        _assert_evidence(report)


def test_promotion_gate_blocks_runtime_execution_external_manifest_lineage_and_policy(tmp_path):
    chain = _build_chain(tmp_path)
    domain_dir = chain["domain_dir"]
    agent_id = chain["agent_ids"][0]
    team_path = Path(chain["team"]["team_path"])
    agent_path = domain_dir / "sandbox_agents" / f"{agent_id}.json"
    manifest_path = domain_dir / "manifests" / "artifact_manifest.json"

    agent = _read_json(agent_path)
    agent["sandbox_config"]["runtime_enabled"] = True
    agent_path.write_text(json.dumps(agent, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    runtime_report = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=domain_dir,
        target_id=agent_id,
        requested_status="validated",
    )
    assert runtime_report["gate_result"] == "blocked"
    assert "runtime_enabled" in " ".join(runtime_report["blockers"])

    agent["sandbox_config"]["runtime_enabled"] = False
    agent.pop("lineage")
    agent_path.write_text(json.dumps(agent, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lineage_report = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=domain_dir,
        target_id=agent_id,
        requested_status="validated",
    )
    assert lineage_report["gate_result"] == "blocked"
    assert "lineage" in " ".join(lineage_report["blockers"])

    team = _read_json(team_path)
    team["coordination_model"]["execution_enabled"] = True
    team_path.write_text(json.dumps(team, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    execution_report = evaluate_promotion_gate(
        target_type="team",
        domain_dir=domain_dir,
        target_id=chain["team"]["team_id"],
        requested_status="validated",
    )
    assert execution_report["gate_result"] == "blocked"
    assert "execution_enabled" in " ".join(execution_report["blockers"])

    external_report = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(external_access=True),
        requested_status="validated",
    )
    assert external_report["gate_result"] == "blocked"
    assert "external_access" in " ".join(external_report["blockers"])

    policy_report = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(capability_type="policy", restrictions=["self_approval"]),
        requested_status="validated",
    )
    assert policy_report["gate_result"] == "blocked"
    assert "self_approval" in " ".join(policy_report["blockers"])

    manifest = _read_json(manifest_path)
    manifest["artifacts"][1]["dependencies"] = ["missing_profile_catalog"]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_report = evaluate_promotion_gate(
        target_type="artifact",
        domain_dir=domain_dir,
        target_id="agent_presets_main",
        requested_status="validated",
    )
    assert manifest_report["gate_result"] == "blocked"
    assert "dependencia" in " ".join(manifest_report["blockers"]) or "dependencies" in " ".join(
        manifest_report["blockers"]
    )
