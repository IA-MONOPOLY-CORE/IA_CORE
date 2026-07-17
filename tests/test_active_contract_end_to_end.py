import hashlib
import json
from copy import deepcopy
from pathlib import Path

from core.active_contract import evaluate_active_contract
from core.approval_workflow import (
    build_approval_request_from_gate,
    build_audit_event_for_approval_decision,
    record_approval_decision,
)
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


def _manifest_artifact(chain: dict, artifact_id: str) -> dict:
    matches = [item for item in _manifest(chain)["artifacts"] if item["artifact_id"] == artifact_id]
    assert len(matches) == 1
    return matches[0]


def _approval_for(gate: dict) -> tuple[dict, dict, dict]:
    request = build_approval_request_from_gate(
        gate,
        requested_by=f"requester_{gate['target_type']}_candidate",
    )
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by=f"reviewer_{gate['target_type']}_candidate",
        reason="Candidate evidence reviewed for active contract E2E.",
    )
    decision_audit = build_audit_event_for_approval_decision(request, decision)
    return request, decision, decision_audit


def _contract_decision() -> dict:
    return build_approval_decision(
        approval_decision_id="approval_decision_active_contract_e2e",
        approval_request_id="approval_request_active_contract_e2e",
        decision="approved_for_activation_candidate",
        decided_by="reviewer_active_contract",
        reason="Active contract E2E evidence reviewed.",
        evidence_reviewed={"gate_result": "passed"},
    )


def _policy(chain: dict, **overrides) -> dict:
    policy = _valid_policy(domain_id=chain["domain"]["domain_id"], subject_id=chain["agent_ids"][0])
    policy.update(overrides)
    return policy


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


def _promote_to_candidate(chain: dict, case: dict) -> tuple[dict, dict]:
    gate = evaluate_promotion_gate(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"] if case["target_type"] != "capability_policy" else None,
        target_id=case["target_id"],
        target=case["target"],
        requested_status="candidate_for_activation",
    )
    assert gate["gate_result"] == "passed"
    request, decision, decision_audit = _approval_for(gate)
    execution = execute_promotion(
        target_type=case["target_type"],
        domain_dir=chain["domain_dir"],
        target_id=case["target_id"],
        target=case["target"],
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="executor_service",
    )
    assert execution["execution_result"] == "applied"
    assert execution["applied_status"] == "candidate_for_activation"
    return decision, execution["evidence"]["audit_event"] or decision_audit


def _evaluate_contract(chain: dict, case: dict, decision: dict, audit_event: dict, **overrides) -> dict:
    params = {
        "target_type": case["target_type"],
        "domain_dir": chain["domain_dir"],
        "target_id": case["target_id"],
        "target": case["target"],
        "approval_decision": decision,
        "audit_events": [audit_event],
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


def test_active_contract_e2e_internal_active_for_complete_candidate_chain(tmp_path):
    chain = _build_chain(tmp_path)
    policy = _policy(chain)
    cases = _target_cases(chain, policy)
    approvals: dict[str, tuple[dict, dict]] = {}

    for case in cases:
        decision, audit_event = _promote_to_candidate(chain, case)
        assert case["status"]() == "candidate_for_activation"
        approvals[case["target_type"]] = (decision, audit_event)

    before_sandbox = _tree_hash(chain["domain_dir"])
    before_manifest = deepcopy(_manifest(chain))
    before_operational = _operational_snapshot()
    domain_payload = _read_json(chain["domain_dir"] / "domain.json")
    assert domain_payload.get("visible_en_hud") is not True

    for case in cases:
        decision, audit_event = approvals[case["target_type"]]
        result = _evaluate_contract(chain, case, decision, audit_event)
        assert result["contract_result"] == "passed"
        assert result["active_mode"] == "internal_active"
        assert result["current_status"] == "candidate_for_activation"
        assert result["runtime_enabled"] is False
        assert result["execution_enabled"] is False
        assert result["external_access"] is False

    assert _tree_hash(chain["domain_dir"]) == before_sandbox
    assert _manifest(chain) == before_manifest
    assert _operational_snapshot() == before_operational
    assert _read_json(chain["domain_dir"] / "domain.json").get("visible_en_hud") is not True
    _assert_runtime_boundary(chain, policy)


def test_active_contract_e2e_blocks_future_active_modes(tmp_path):
    chain = _build_chain(tmp_path)
    policy = _policy(chain)
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    decision, audit_event = _promote_to_candidate(chain, case)

    runtime = _evaluate_contract(chain, case, decision, audit_event, active_mode="runtime_active_future")
    external = _evaluate_contract(chain, case, decision, audit_event, active_mode="external_active_future")

    assert runtime["contract_result"] == "blocked"
    assert external["contract_result"] == "blocked"
    assert "active_mode" in " ".join(runtime["blockers"])
    assert "active_mode" in " ".join(external["blockers"])


def test_active_contract_e2e_blocks_non_candidate_statuses(tmp_path):
    for status in ["materialized", "validated", "archived", "broken", "legacy"]:
        chain = _build_chain(tmp_path / status)
        case = next(item for item in _target_cases(chain, _policy(chain)) if item["target_type"] == "team")
        team_path = chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"
        team = _read_json(team_path)
        team["status"] = status
        _write_json(team_path, team)

        result = _evaluate_contract(
            chain,
            case,
            _contract_decision(),
            {"audit_event_id": "audit_event_active_contract"},
        )

        assert result["contract_result"] == "blocked"
        assert "candidate_for_activation" in " ".join(result["blockers"]) or status in " ".join(result["blockers"])


def test_active_contract_e2e_blocks_runtime_execution_external_and_missing_evidence(tmp_path):
    chain = _build_chain(tmp_path)
    policy = _policy(chain)
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    decision, audit_event = _promote_to_candidate(chain, case)

    no_approval = _evaluate_contract(chain, case, None, audit_event)
    no_audit = _evaluate_contract(chain, case, decision, audit_event, audit_events=[])
    assert no_approval["contract_result"] == "blocked"
    assert no_audit["contract_result"] == "blocked"

    team_path = chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"
    team = _read_json(team_path)
    team["metadata"]["runtime_enabled"] = True
    _write_json(team_path, team)
    runtime = _evaluate_contract(chain, case, decision, audit_event)
    assert runtime["contract_result"] == "blocked"
    assert "runtime_enabled" in " ".join(runtime["blockers"])

    team["metadata"]["runtime_enabled"] = False
    team["coordination_model"]["execution_enabled"] = True
    _write_json(team_path, team)
    execution = _evaluate_contract(chain, case, decision, audit_event)
    assert execution["contract_result"] == "blocked"
    assert "execution_enabled" in " ".join(execution["blockers"])

    external_policy = policy.copy()
    external_policy["promotion_status"] = "candidate_for_activation"
    external_policy["external_access"] = True
    external = evaluate_active_contract(
        target_type="capability_policy",
        target=external_policy,
        approval_decision=decision,
        audit_events=[audit_event],
    )
    assert external["contract_result"] == "blocked"
    assert "external_access" in " ".join(external["blockers"])


def test_active_contract_e2e_blocks_manifest_dependencies_lineage_policy_and_executor_active(tmp_path):
    chain = _build_chain(tmp_path / "manifest")
    policy = _policy(chain)
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    decision, audit_event = _promote_to_candidate(chain, case)
    manifest_path = chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest_path.write_text("{bad json", encoding="utf-8")
    manifest_result = _evaluate_contract(chain, case, decision, audit_event)
    assert manifest_result["contract_result"] == "blocked"

    chain = _build_chain(tmp_path / "dependencies")
    policy = _policy(chain)
    case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "team")
    decision, audit_event = _promote_to_candidate(chain, case)
    manifest = _manifest(chain)
    manifest["artifacts"][-1]["dependencies"] = ["missing_agent"]
    _write_manifest(chain, manifest)
    dependency_result = _evaluate_contract(chain, case, decision, audit_event)
    assert dependency_result["contract_result"] == "blocked"

    chain = _build_chain(tmp_path / "lineage")
    policy = _policy(chain)
    agent_case = next(item for item in _target_cases(chain, policy) if item["target_type"] == "agent")
    decision, audit_event = _promote_to_candidate(chain, agent_case)
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{chain['agent_ids'][0]}.json"
    agent = _read_json(agent_path)
    agent.pop("lineage")
    _write_json(agent_path, agent)
    lineage_result = _evaluate_contract(chain, agent_case, decision, audit_event)
    assert lineage_result["contract_result"] == "blocked"
    assert "lineage" in " ".join(lineage_result["blockers"])

    chain = _build_chain(tmp_path / "policy")
    invalid_policy = _policy(chain, restrictions=["self_approval"])
    invalid_policy["promotion_status"] = "candidate_for_activation"
    policy_result = evaluate_active_contract(
        target_type="capability_policy",
        target=invalid_policy,
        approval_decision=decision,
        audit_events=[audit_event],
    )
    assert policy_result["contract_result"] == "blocked"

    active_gate = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
    )
    active_result = execute_promotion(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
        promotion_gate_result=active_gate,
        approval_request=None,
        approval_decision=None,
        executed_by="executor_service",
    )
    assert active_result["execution_result"] == "blocked"
