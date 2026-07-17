import hashlib
import json
from copy import deepcopy
from pathlib import Path

from core.active_contract import evaluate_active_contract
from core.approval_workflow_schema import build_approval_decision
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.promotion_executor import execute_promotion
from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _build_chain, _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"


def _tree_inventory(root: Path) -> tuple[tuple[str, int], ...]:
    return tuple(
        (path.relative_to(root).as_posix(), path.stat().st_size)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    )


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _manifest(chain: dict) -> dict:
    return _read_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH)


def _write_manifest(chain: dict, manifest: dict) -> None:
    _write_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH, manifest)


def _approval() -> dict:
    return build_approval_decision(
        approval_decision_id="approval_decision_active_contract",
        approval_request_id="approval_request_active_contract",
        decision="approved_for_activation_candidate",
        decided_by="reviewer_user",
        reason="Active contract evidence reviewed.",
        evidence_reviewed={"gate_result": "passed"},
    )


def _audit_events() -> list[dict]:
    return [{"audit_event_id": "audit_event_active_contract", "event_type": "active_contract_reviewed"}]


def _set_artifact_status(chain: dict, artifact_id: str, status: str) -> None:
    manifest = _manifest(chain)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            artifact["status"] = status
            _write_manifest(chain, manifest)
            return
    raise AssertionError(f"artifact not found: {artifact_id}")


def _prepare_candidate_team(chain: dict) -> dict:
    team_id = chain["team"]["team_id"]
    team_path = chain["domain_dir"] / "sandbox_teams" / f"{team_id}.json"
    team = _read_json(team_path)
    team["status"] = "candidate_for_activation"
    _write_json(team_path, team)
    _set_artifact_status(chain, f"team_{team_id}", "candidate_for_activation")
    return team


def _prepare_candidate_agent(chain: dict) -> dict:
    agent_id = chain["agent_ids"][0]
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
    agent = _read_json(agent_path)
    agent["status"] = "candidate_for_activation"
    _write_json(agent_path, agent)
    _set_artifact_status(chain, f"agent_{agent_id}", "candidate_for_activation")
    return agent


def _candidate_policy(chain: dict, **overrides) -> dict:
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    policy["promotion_status"] = "candidate_for_activation"
    policy.update(overrides)
    return policy


def _evaluate_team(chain: dict, **overrides) -> dict:
    params = {
        "target_type": "team",
        "domain_dir": chain["domain_dir"],
        "target_id": chain["team"]["team_id"],
        "approval_decision": _approval(),
        "audit_events": _audit_events(),
    }
    params.update(overrides)
    return evaluate_active_contract(**params)


def test_active_contract_valid_for_candidate_target(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)

    result = _evaluate_team(chain)

    assert result["contract_result"] == "passed"
    assert result["active_mode"] == "internal_active"
    assert result["runtime_enabled"] is False
    assert result["execution_enabled"] is False
    assert result["external_access"] is False


def test_active_contract_fails_if_materialized_or_validated_not_candidate(tmp_path):
    chain = _build_chain(tmp_path / "materialized")
    materialized = _evaluate_team(chain)
    assert materialized["contract_result"] == "blocked"
    assert "candidate_for_activation" in " ".join(materialized["blockers"])

    chain = _build_chain(tmp_path / "validated")
    team_id = chain["team"]["team_id"]
    team_path = chain["domain_dir"] / "sandbox_teams" / f"{team_id}.json"
    team = _read_json(team_path)
    team["status"] = "validated"
    _write_json(team_path, team)
    _set_artifact_status(chain, f"team_{team_id}", "validated")

    validated = _evaluate_team(chain)
    assert validated["contract_result"] == "blocked"
    assert "candidate_for_activation" in " ".join(validated["blockers"])


def test_active_contract_fails_without_approval_or_audit(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)

    no_approval = _evaluate_team(chain, approval_decision=None)
    no_audit = _evaluate_team(chain, audit_events=[])

    assert no_approval["contract_result"] == "blocked"
    assert "approval" in " ".join(no_approval["blockers"])
    assert no_audit["contract_result"] == "blocked"
    assert "audit" in " ".join(no_audit["blockers"])


def test_active_contract_fails_runtime_execution_and_external_access(tmp_path):
    chain = _build_chain(tmp_path / "runtime")
    team = _prepare_candidate_team(chain)
    team["metadata"]["runtime_enabled"] = True
    _write_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json", team)
    runtime = _evaluate_team(chain)
    assert runtime["contract_result"] == "blocked"
    assert "runtime_enabled" in " ".join(runtime["blockers"])

    chain = _build_chain(tmp_path / "execution")
    team = _prepare_candidate_team(chain)
    team["coordination_model"]["execution_enabled"] = True
    _write_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json", team)
    execution = _evaluate_team(chain)
    assert execution["contract_result"] == "blocked"
    assert "execution_enabled" in " ".join(execution["blockers"])

    chain = _build_chain(tmp_path / "external")
    policy = _candidate_policy(chain, external_access=True)
    external = evaluate_active_contract(
        target_type="capability_policy",
        target=policy,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )
    assert external["contract_result"] == "blocked"
    assert "external_access" in " ".join(external["blockers"])


def test_active_contract_fails_legacy_broken_and_archived(tmp_path):
    for status in ["legacy", "broken", "archived"]:
        chain = _build_chain(tmp_path / status)
        team = _prepare_candidate_team(chain)
        team["status"] = status
        _write_json(chain["domain_dir"] / "sandbox_teams" / f"{team['team_id']}.json", team)

        result = _evaluate_team(chain)

        assert result["contract_result"] == "blocked"
        assert status in " ".join(result["blockers"])


def test_active_contract_fails_manifest_and_dependencies_issues(tmp_path):
    chain = _build_chain(tmp_path / "manifest")
    _prepare_candidate_team(chain)
    manifest_path = chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest_path.write_text("{bad json", encoding="utf-8")
    manifest_result = _evaluate_team(chain)
    assert manifest_result["contract_result"] == "blocked"

    chain = _build_chain(tmp_path / "dependencies")
    _prepare_candidate_team(chain)
    manifest = _manifest(chain)
    manifest["artifacts"][-1]["dependencies"] = ["missing_agent"]
    _write_manifest(chain, manifest)
    dependency_result = _evaluate_team(chain)
    assert dependency_result["contract_result"] == "blocked"
    assert "dependencia" in " ".join(dependency_result["blockers"]) or "dependencies" in " ".join(dependency_result["blockers"])


def test_active_contract_fails_lineage_and_capability_policy_issues(tmp_path):
    chain = _build_chain(tmp_path / "lineage")
    agent = _prepare_candidate_agent(chain)
    agent.pop("lineage")
    agent_id = chain["agent_ids"][0]
    _write_json(chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json", agent)

    lineage = evaluate_active_contract(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )
    assert lineage["contract_result"] == "blocked"
    assert "lineage" in " ".join(lineage["blockers"])

    chain = _build_chain(tmp_path / "policy")
    policy = _candidate_policy(chain, restrictions=["self_approval"])
    invalid_policy = evaluate_active_contract(
        target_type="capability_policy",
        target=policy,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )
    assert invalid_policy["contract_result"] == "blocked"
    assert "capability_policy" in " ".join(invalid_policy["blockers"])


def test_active_contract_modes_future_runtime_and_external_block(tmp_path):
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)

    runtime = _evaluate_team(chain, active_mode="runtime_active_future")
    external = _evaluate_team(chain, active_mode="external_active_future")

    assert runtime["contract_result"] == "blocked"
    assert external["contract_result"] == "blocked"
    assert "active_mode" in " ".join(runtime["blockers"])
    assert "active_mode" in " ".join(external["blockers"])


def test_promotion_executor_still_blocks_active(tmp_path):
    chain = _build_chain(tmp_path)
    gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
    )

    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
        promotion_gate_result=gate,
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "blocked"


def test_active_contract_evaluator_does_not_mutate_state_runtime_or_legacy(tmp_path):
    before_domains = _tree_inventory(DOMAINS)
    before_agents = _tree_inventory(AGENTS)
    chain = _build_chain(tmp_path)
    _prepare_candidate_team(chain)
    before_sandbox = _tree_hash(chain["domain_dir"])
    before_manifest = deepcopy(_manifest(chain))

    result = _evaluate_team(chain)

    assert result["contract_result"] == "passed"
    assert _tree_hash(chain["domain_dir"]) == before_sandbox
    assert _manifest(chain) == before_manifest
    assert _tree_inventory(DOMAINS) == before_domains
    assert _tree_inventory(AGENTS) == before_agents
