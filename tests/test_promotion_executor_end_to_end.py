import hashlib
import json
from copy import deepcopy
from pathlib import Path

from core.approval_workflow import (
    build_approval_request_from_gate,
    build_audit_event_for_approval_decision,
    build_audit_event_for_approval_request,
    record_approval_decision,
)
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.promotion_executor import (
    dry_run_promotion,
    execute_promotion,
    rollback_promotion_execution,
)
from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _build_chain, _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"

DECISION_BY_STATUS = {
    "validated": "approved_for_validation",
    "candidate_for_activation": "approved_for_activation_candidate",
}


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        digest.update(b"missing")
        return digest.hexdigest()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _papers_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(DOMAINS.glob("*/agents/papers/*.json")):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(str(path.stat().st_size).encode("utf-8"))
    return digest.hexdigest()


def _tree_inventory(root: Path) -> tuple[tuple[str, int], ...]:
    if not root.exists():
        return (("__missing__", 0),)
    return tuple(
        (path.relative_to(root).as_posix(), path.stat().st_size)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    )


def _operational_snapshot() -> dict[str, str]:
    return {
        "domains": repr(_tree_inventory(DOMAINS)),
        "agents": repr(_tree_inventory(AGENTS)),
        "catalogs": repr(_tree_inventory(CATALOGS)),
        "global_papers": _papers_hash(),
    }


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _manifest(chain: dict) -> dict:
    return _read_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH)


def _manifest_artifact(chain: dict, artifact_id: str) -> dict:
    matches = [
        artifact
        for artifact in _manifest(chain)["artifacts"]
        if artifact["artifact_id"] == artifact_id
    ]
    assert len(matches) == 1
    return matches[0]


def _sandbox_files(chain: dict) -> list[str]:
    return sorted(
        path.relative_to(chain["domain_dir"]).as_posix()
        for path in chain["domain_dir"].rglob("*")
        if path.is_file()
    )


def _approval_for(gate: dict, requested_status: str) -> tuple[dict, dict, dict, dict]:
    request = build_approval_request_from_gate(
        gate,
        requested_by=f"requester_{gate['target_type']}_{requested_status}",
    )
    decision = record_approval_decision(
        request,
        decision=DECISION_BY_STATUS[requested_status],
        decided_by=f"reviewer_{gate['target_type']}_{requested_status}",
        reason="Evidence reviewed for E2E checkpoint.",
    )
    request_audit = build_audit_event_for_approval_request(request)
    decision_audit = build_audit_event_for_approval_decision(request, decision)
    return request, decision, request_audit, decision_audit


def _target_cases(chain: dict, policy: dict) -> list[dict]:
    agent_id = chain["agent_ids"][0]
    team_id = chain["team"]["team_id"]
    return [
        {
            "target_type": "domain",
            "target_id": None,
            "target": None,
            "status": lambda: _read_json(chain["domain_dir"] / "domain.json")["status"],
        },
        {
            "target_type": "profile_catalog",
            "target_id": None,
            "target": None,
            "status": lambda: _manifest_artifact(chain, "profile_catalog_main")["status"],
        },
        {
            "target_type": "agent_preset",
            "target_id": None,
            "target": None,
            "status": lambda: _manifest_artifact(chain, "agent_presets_main")["status"],
        },
        {
            "target_type": "paper_seed",
            "target_id": None,
            "target": None,
            "status": lambda: _manifest_artifact(chain, "paper_seed_main")["status"],
        },
        {
            "target_type": "agent",
            "target_id": agent_id,
            "target": None,
            "status": lambda: _read_json(
                chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
            )["status"],
        },
        {
            "target_type": "team",
            "target_id": team_id,
            "target": None,
            "status": lambda: _read_json(
                chain["domain_dir"] / "sandbox_teams" / f"{team_id}.json"
            )["status"],
        },
        {
            "target_type": "capability_policy",
            "target_id": policy["policy_id"],
            "target": policy,
            "status": lambda: policy.get("promotion_status") or policy["policy_status"],
        },
    ]


def _gate_for(case: dict, chain: dict, requested_status: str) -> dict:
    return evaluate_promotion_gate(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"] if case["target_type"] != "capability_policy" else None,
        target_id=case["target_id"],
        target=case["target"],
        requested_status=requested_status,
    )


def _assert_runtime_boundaries(chain: dict, policy: dict) -> None:
    for agent_id in chain["agent_ids"]:
        agent = _read_json(chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json")
        assert agent["sandbox_config"]["runtime_enabled"] is False
        assert agent["sandbox_config"]["operational"] is False
    team = _read_json(chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json")
    assert team["metadata"]["runtime_enabled"] is False
    assert team["metadata"]["execution_enabled"] is False
    assert team["coordination_model"]["runtime_enabled"] is False
    assert team["coordination_model"]["execution_enabled"] is False
    assert team["capabilities"]["tools"][0]["execution_allowed"] is False
    assert team["capabilities"]["tools"][0]["external_access"] is False
    assert policy["runtime_enabled"] is False
    assert policy["execution_allowed"] is False
    assert policy["external_access"] is False


def _assert_lineage_dependencies_capabilities(chain: dict) -> None:
    manifest = _manifest(chain)
    artifact_ids = {artifact["artifact_id"] for artifact in manifest["artifacts"]}
    for artifact in manifest["artifacts"]:
        assert set(artifact["dependencies"]).issubset(artifact_ids)
    for agent_id in chain["agent_ids"]:
        agent = _read_json(chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json")
        assert agent["lineage"]["origin"]["source_profile_id"]
    team = _read_json(chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json")
    assert team["dependencies"] == [f"agent_{agent_id}" for agent_id in chain["agent_ids"]]
    assert team["capabilities"]["tools"]
    assert team["capabilities"]["policies"]


def _run_full_flow_for_target(tmp_path: Path, target_type: str, requested_status: str) -> None:
    chain = _build_chain(tmp_path)
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == target_type)
    previous_status = case["status"]()
    before_sandbox_hash = _tree_hash(chain["domain_dir"])
    before_manifest = deepcopy(_manifest(chain))
    before_files = _sandbox_files(chain)
    before_operational = _operational_snapshot()

    gate = _gate_for(case, chain, requested_status)
    assert gate["gate_result"] == "passed"
    request, decision, request_audit, decision_audit = _approval_for(gate, requested_status)
    assert request_audit["event_type"] == "approval_requested"
    assert decision_audit["event_type"] == "approval_decision_recorded"

    dry_run = dry_run_promotion(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        target=case["target"],
        requested_status=requested_status,
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert dry_run["execution_result"] == "dry_run_passed"
    assert dry_run["dry_run"] is True
    assert dry_run["evidence"]["promotion_gate"]["gate_result"] == "passed"
    assert case["status"]() == previous_status
    assert _tree_hash(chain["domain_dir"]) == before_sandbox_hash
    assert _manifest(chain) == before_manifest
    assert _sandbox_files(chain) == before_files
    _assert_runtime_boundaries(chain, policy)
    _assert_lineage_dependencies_capabilities(chain)
    assert _operational_snapshot() == before_operational

    execution = execute_promotion(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        target=case["target"],
        requested_status=requested_status,
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )

    assert execution["execution_result"] == "applied"
    assert execution["applied_status"] == requested_status
    assert execution["evidence"]["audit_event"]["event_type"] == "promotion_executed"
    assert execution["evidence"]["audit_event"]["immutable"] is True
    assert execution["evidence"]["audit_event"]["runtime_related"] is False
    assert case["status"]() == requested_status
    assert _sandbox_files(chain) == before_files
    _assert_runtime_boundaries(chain, policy)
    _assert_lineage_dependencies_capabilities(chain)
    assert _operational_snapshot() == before_operational

    rollback = rollback_promotion_execution(
        execution,
        domain_dir=chain["domain_dir"],
        target=case["target"],
        executed_by="executor_service",
    )

    assert rollback["status"] == "rolled_back"
    assert rollback["audit_event"]["event_type"] == "promotion_rollback_recorded"
    assert rollback["audit_event"]["immutable"] is True
    assert case["status"]() == previous_status
    assert _manifest(chain) == before_manifest
    assert _sandbox_files(chain) == before_files
    _assert_runtime_boundaries(chain, policy)
    _assert_lineage_dependencies_capabilities(chain)
    assert _operational_snapshot() == before_operational


def test_executor_e2e_validated_for_complete_sandbox_chain_targets(tmp_path):
    for target_type in [
        "domain",
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
        "team",
        "capability_policy",
    ]:
        _run_full_flow_for_target(tmp_path / target_type, target_type, "validated")


def test_executor_e2e_candidate_for_activation_for_representative_targets(tmp_path):
    for target_type in ["domain", "agent", "team", "capability_policy"]:
        _run_full_flow_for_target(
            tmp_path / target_type,
            target_type,
            "candidate_for_activation",
        )


def test_executor_e2e_blocks_active_for_complete_chain(tmp_path):
    chain = _build_chain(tmp_path)
    case = next(item for item in _target_cases(chain, _valid_policy()) if item["target_type"] == "team")
    before = _tree_hash(chain["domain_dir"])
    gate = _gate_for(case, chain, "active")

    result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        requested_status="active",
        promotion_gate_result=gate,
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )

    assert result["execution_result"] == "blocked"
    assert "active" in " ".join(result["blockers"])
    assert _tree_hash(chain["domain_dir"]) == before


def test_executor_e2e_blocks_invalid_approvals(tmp_path):
    chain = _build_chain(tmp_path)
    case = next(item for item in _target_cases(chain, _valid_policy()) if item["target_type"] == "team")
    gate = _gate_for(case, chain, "validated")
    before = _tree_hash(chain["domain_dir"])

    for decision_name in ["rejected", "needs_changes", "expired", "revoked"]:
        request, decision, _request_audit, _decision_audit = _approval_for(gate, "validated")
        decision["decision"] = decision_name
        result = execute_promotion(
            target_type="team",
            domain_dir=chain["domain_dir"],
            target_id=case["target_id"],
            requested_status="validated",
            promotion_gate_result=gate,
            approval_request=request,
            approval_decision=decision,
            executed_by="executor_service",
        )
        assert result["execution_result"] == "blocked"

    request, decision, _request_audit, _decision_audit = _approval_for(gate, "validated")
    request["target_id"] = "other_team"
    other_target = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        requested_status="validated",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )
    assert other_target["execution_result"] == "blocked"

    request, decision, _request_audit, _decision_audit = _approval_for(gate, "validated")
    wrong_status = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )
    assert wrong_status["execution_result"] == "blocked"
    assert _tree_hash(chain["domain_dir"]) == before


def test_executor_e2e_blocks_invalid_gate_runtime_and_legacy_boundaries(tmp_path):
    chain = _build_chain(tmp_path)
    case = next(item for item in _target_cases(chain, _valid_policy()) if item["target_type"] == "team")
    gate = _gate_for(case, chain, "validated")
    request, decision, _request_audit, _decision_audit = _approval_for(gate, "validated")

    failed_gate = dict(gate)
    failed_gate["gate_result"] = "failed"
    failed_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        requested_status="validated",
        promotion_gate_result=failed_gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )
    assert failed_result["execution_result"] == "blocked"

    blocked_gate = dict(gate)
    blocked_gate["gate_result"] = "blocked"
    blocked_gate["blockers"] = ["manifest inconsistente"]
    blocked_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        requested_status="validated",
        promotion_gate_result=blocked_gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )
    assert blocked_result["execution_result"] == "blocked"

    manifest_path = chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest = _manifest(chain)
    manifest["artifacts"][1]["dependencies"] = ["missing_profile_catalog"]
    _write_json(manifest_path, manifest)
    inconsistent_gate = evaluate_promotion_gate(
        target_type="agent_preset",
        domain_dir=chain["domain_dir"],
        requested_status="validated",
    )
    assert inconsistent_gate["gate_result"] == "blocked"
    inconsistent_result = execute_promotion(
        target_type="agent_preset",
        domain_dir=chain["domain_dir"],
        requested_status="validated",
        promotion_gate_result=inconsistent_gate,
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )
    assert inconsistent_result["execution_result"] == "blocked"
    chain = _build_chain(tmp_path / "runtime_boundaries")

    agent_id = chain["agent_ids"][0]
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
    agent = _read_json(agent_path)
    agent["sandbox_config"]["runtime_enabled"] = True
    _write_json(agent_path, agent)
    runtime_gate = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        requested_status="validated",
    )
    assert runtime_gate["gate_result"] == "blocked"

    team_path = chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"
    team = _read_json(team_path)
    team["coordination_model"]["execution_enabled"] = True
    _write_json(team_path, team)
    execution_gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="validated",
    )
    assert execution_gate["gate_result"] == "blocked"

    external_policy = _valid_policy(external_access=True)
    external_gate = evaluate_promotion_gate(
        target_type="capability_policy",
        target=external_policy,
        requested_status="validated",
    )
    assert external_gate["gate_result"] == "blocked"

    for status in ["legacy", "broken", "archived"]:
        domain_path = chain["domain_dir"] / "domain.json"
        domain = _read_json(domain_path)
        domain["status"] = status
        domain["artifact_state"] = status
        _write_json(domain_path, domain)
        legacy_result = execute_promotion(
            target_type="domain",
            domain_dir=chain["domain_dir"],
            requested_status="validated",
            approval_request=None,
            approval_decision=None,
            executed_by="executor_service",
        )
        assert legacy_result["execution_result"] == "blocked"
