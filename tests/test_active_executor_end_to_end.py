import hashlib
import json
from copy import deepcopy
from pathlib import Path

from core.active_contract import evaluate_active_contract
from core.active_executor import dry_run_active_execution, execute_active, rollback_active_execution
from core.approval_workflow import build_approval_request_from_gate, record_approval_decision
from core.approval_workflow_schema import build_approval_decision
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.promotion_executor import execute_promotion
from core.promotion_gate import evaluate_promotion_gate
from tests.test_promotion_gate import _build_chain, _valid_policy


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        digest.update(b"missing")
        return digest.hexdigest()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _tree_inventory(root: Path) -> tuple[tuple[str, int], ...]:
    if not root.exists():
        return (("__missing__", 0),)
    return tuple(
        (path.relative_to(root).as_posix(), path.stat().st_size)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    )


def _papers_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(DOMAINS.glob("*/agents/papers/*.json")):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(str(path.stat().st_size).encode("utf-8"))
    return digest.hexdigest()


def _operational_snapshot() -> dict[str, object]:
    return {
        "domains": _tree_inventory(DOMAINS),
        "agents": _tree_inventory(AGENTS),
        "catalogs": _tree_inventory(CATALOGS),
        "global_papers": _papers_hash(),
    }


def _manifest(chain: dict) -> dict:
    return _read_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH)


def _write_manifest(chain: dict, manifest: dict) -> None:
    _write_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH, manifest)


def _manifest_without_statuses(chain: dict) -> dict:
    manifest = deepcopy(_manifest(chain))
    for artifact in manifest["artifacts"]:
        artifact["status"] = "<status>"
    return manifest


def _artifact(chain: dict, artifact_id: str) -> dict:
    matches = [item for item in _manifest(chain)["artifacts"] if item["artifact_id"] == artifact_id]
    assert len(matches) == 1
    return matches[0]


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
            "status": lambda: _artifact(chain, "profile_catalog_main")["status"],
        },
        {
            "target_type": "agent_preset",
            "target_id": None,
            "target": None,
            "status": lambda: _artifact(chain, "agent_presets_main")["status"],
        },
        {
            "target_type": "paper_seed",
            "target_id": None,
            "target": None,
            "status": lambda: _artifact(chain, "paper_seed_main")["status"],
        },
        {
            "target_type": "agent",
            "target_id": agent_id,
            "target": None,
            "status": lambda: _read_json(chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json")["status"],
        },
        {
            "target_type": "team",
            "target_id": team_id,
            "target": None,
            "status": lambda: _read_json(chain["domain_dir"] / "sandbox_teams" / f"{team_id}.json")["status"],
        },
        {
            "target_type": "capability_policy",
            "target_id": policy["policy_id"],
            "target": policy,
            "status": lambda: policy.get("promotion_status") or policy["policy_status"],
        },
    ]


def _candidate_approval_for(gate: dict) -> tuple[dict, dict]:
    request = build_approval_request_from_gate(
        gate,
        requested_by=f"requester_{gate['target_type']}_candidate",
    )
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by=f"reviewer_{gate['target_type']}_candidate",
        reason="Candidate evidence reviewed.",
    )
    return request, decision


def _active_approval(case: dict) -> dict:
    target_id = case["target_id"] or case["target_type"]
    return build_approval_decision(
        approval_decision_id=f"approval_decision_active_{case['target_type']}_{target_id}",
        approval_request_id=f"approval_request_active_{case['target_type']}_{target_id}",
        decision="approved_for_activation_candidate",
        decided_by="reviewer_active_executor",
        reason="Active executor E2E evidence reviewed.",
        evidence_reviewed={"target_type": case["target_type"], "target_id": target_id},
    )


def _active_audit(case: dict) -> dict:
    target_id = case["target_id"] or case["target_type"]
    return {
        "audit_event_id": f"audit_event_active_contract_{case['target_type']}_{target_id}",
        "event_type": "active_contract_reviewed",
        "target_type": case["target_type"],
        "target_id": target_id,
    }


def _promote_to_candidate(chain: dict, case: dict) -> None:
    gate = evaluate_promotion_gate(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"] if case["target_type"] != "capability_policy" else None,
        target_id=case["target_id"],
        target=case["target"],
        requested_status="candidate_for_activation",
    )
    request, decision = _candidate_approval_for(gate)
    result = execute_promotion(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        target=case["target"],
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="promotion_executor_service",
    )
    assert result["execution_result"] == "applied"


def _active_contract(chain: dict, case: dict, approval: dict, audit: dict, **overrides) -> dict:
    params = {
        "target_type": case["target_type"],
        "domain_dir": chain["domain_dir"],
        "target_id": case["target_id"],
        "target": case["target"],
        "approval_decision": approval,
        "audit_events": [audit],
    }
    params.update(overrides)
    return evaluate_active_contract(**params)


def _assert_runtime_boundary(chain: dict, policy: dict) -> None:
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


def test_active_executor_e2e_all_targets_execute_and_rollback_without_runtime(tmp_path):
    for target_type in [
        "domain",
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
        "team",
        "capability_policy",
    ]:
        chain = _build_chain(tmp_path / target_type)
        policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
        case = next(item for item in _target_cases(chain, policy) if item["target_type"] == target_type)
        _promote_to_candidate(chain, case)
        assert case["status"]() == "candidate_for_activation"

        approval = _active_approval(case)
        audit = _active_audit(case)
        contract = _active_contract(chain, case, approval, audit)
        before_hash = _tree_hash(chain["domain_dir"])
        before_manifest_shape = _manifest_without_statuses(chain)
        before_operational = _operational_snapshot()

        dry_run = dry_run_active_execution(
            target_type=case["target_type"],
            domain_dir=chain["domain_dir"],
            target_id=case["target_id"],
            target=case["target"],
            active_contract_result=contract,
            approval_decision=approval,
            audit_events=[audit],
            executed_by="active_executor_service",
        )
        assert dry_run["result_status"] == "dry_run_passed"
        assert _tree_hash(chain["domain_dir"]) == before_hash
        assert case["status"]() == "candidate_for_activation"

        execution = execute_active(
            target_type=case["target_type"],
            domain_dir=chain["domain_dir"],
            target_id=case["target_id"],
            target=case["target"],
            active_contract_result=contract,
            approval_decision=approval,
            audit_events=[audit],
            executed_by="active_executor_service",
        )
        assert execution["result_status"] == "passed"
        assert execution["evidence"]["audit_event"]["event_type"] == "active_executed"
        assert case["status"]() == "active"
        assert _manifest_without_statuses(chain) == before_manifest_shape
        _assert_runtime_boundary(chain, policy)
        assert _operational_snapshot() == before_operational

        rollback = rollback_active_execution(
            execution,
            domain_dir=chain["domain_dir"],
            target=case["target"],
            executed_by="active_executor_service",
        )
        assert rollback["result_status"] == "rolled_back"
        assert rollback["evidence"]["audit_event"]["event_type"] == "active_rollback_recorded"
        assert case["status"]() == "candidate_for_activation"
        assert _manifest_without_statuses(chain) == before_manifest_shape
        _assert_runtime_boundary(chain, policy)
        assert _operational_snapshot() == before_operational


def test_active_executor_e2e_blocks_non_candidate_statuses(tmp_path):
    for status in ["materialized", "validated", "active", "archived", "broken", "legacy"]:
        chain = _build_chain(tmp_path / status)
        policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
        case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
        team_path = chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"
        team = _read_json(team_path)
        team["status"] = status
        _write_json(team_path, team)
        approval = _active_approval(case)
        audit = _active_audit(case)

        result = execute_active(
            target_type="team",
            domain_dir=chain["domain_dir"],
            target_id=chain["team"]["team_id"],
            approval_decision=approval,
            audit_events=[audit],
            executed_by="active_executor_service",
        )

        assert result["result_status"] == "blocked"
        assert _read_json(team_path)["status"] == status


def test_active_executor_e2e_blocks_failed_contract_and_future_modes(tmp_path):
    chain = _build_chain(tmp_path)
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    _promote_to_candidate(chain, case)
    approval = _active_approval(case)
    audit = _active_audit(case)

    failed_contract = _active_contract(chain, case, approval, audit, active_mode="runtime_active_future")
    external_contract = _active_contract(chain, case, approval, audit, active_mode="external_active_future")

    runtime = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=failed_contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="active_executor_service",
    )
    external = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=external_contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="active_executor_service",
    )

    assert runtime["result_status"] == "blocked"
    assert external["result_status"] == "blocked"


def test_active_executor_e2e_blocks_invalid_approval_and_audit(tmp_path):
    chain = _build_chain(tmp_path)
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    _promote_to_candidate(chain, case)
    approval = _active_approval(case)
    audit = _active_audit(case)
    contract = _active_contract(chain, case, approval, audit)

    for decision_name in ["rejected", "needs_changes", "expired", "revoked"]:
        invalid_approval = deepcopy(approval)
        invalid_approval["decision"] = decision_name
        result = execute_active(
            target_type="team",
            domain_dir=chain["domain_dir"],
            target_id=chain["team"]["team_id"],
            active_contract_result=contract,
            approval_decision=invalid_approval,
            audit_events=[audit],
            executed_by="active_executor_service",
        )
        assert result["result_status"] == "blocked"

    other_approval = deepcopy(approval)
    other_approval["approval_decision_id"] = "approval_decision_other_target"
    wrong_decision = deepcopy(approval)
    wrong_decision["decision"] = "approved_for_validation"
    other_audit = {"audit_event_id": "audit_event_other_target", "event_type": "active_contract_reviewed"}

    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=None,
        audit_events=[audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"
    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=other_approval,
        audit_events=[audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"
    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=wrong_decision,
        audit_events=[audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"
    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=approval,
        audit_events=[],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"
    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        active_contract_result=contract,
        approval_decision=approval,
        audit_events=[other_audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"


def test_active_executor_e2e_blocks_runtime_execution_external_and_legacy_roots(tmp_path):
    before_operational = _operational_snapshot()
    chain = _build_chain(tmp_path)
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    _promote_to_candidate(chain, case)
    approval = _active_approval(case)
    audit = _active_audit(case)

    team_path = chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"
    team = _read_json(team_path)
    team["metadata"]["runtime_enabled"] = True
    _write_json(team_path, team)
    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        approval_decision=approval,
        audit_events=[audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"

    team["metadata"]["runtime_enabled"] = False
    team["coordination_model"]["execution_enabled"] = True
    _write_json(team_path, team)
    assert execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        approval_decision=approval,
        audit_events=[audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"

    external_policy = _valid_policy(
        domain_id=chain["domain"]["domain_id"],
        subject_id=chain["agent_ids"][0],
        external_access=True,
    )
    external_policy["promotion_status"] = "candidate_for_activation"
    assert execute_active(
        target_type="capability_policy",
        target=external_policy,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="active_executor_service",
    )["result_status"] == "blocked"

    assert _operational_snapshot() == before_operational
