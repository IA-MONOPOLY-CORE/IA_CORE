import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.active_contract import evaluate_active_contract
from core.active_executor import execute_active, rollback_active_execution
from core.approval_workflow_schema import build_approval_decision
from core.capability_policy_schema import build_capability_policy, validate_capability_policy
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.promotion_executor import execute_promotion
from core.promotion_gate import evaluate_promotion_gate
from core.sandbox_agent_memory_contract import build_memory_contract, validate_memory_contract
from core.sandbox_agent_tool_contract import build_tool_contract, validate_tool_contract
from tests.test_promotion_gate import _build_chain


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _approval() -> dict:
    return build_approval_decision(
        approval_decision_id="approval_decision_runtime_boundary",
        approval_request_id="approval_request_runtime_boundary",
        decision="approved_for_activation_candidate",
        decided_by="runtime_boundary_reviewer",
        reason="Runtime boundary evidence reviewed.",
        evidence_reviewed={"runtime_boundary": "blocked"},
        decided_at="2026-07-17T00:00:00",
    )


def _audit_events() -> list[dict]:
    return [
        {
            "audit_event_id": "audit_event_runtime_boundary",
            "event_type": "runtime_boundary_reviewed",
            "result": "recorded",
        }
    ]


def _manifest_path(domain_dir: Path) -> Path:
    return domain_dir / ARTIFACT_MANIFEST_RELATIVE_PATH


def _set_manifest_artifact_status(domain_dir: Path, artifact_id: str, status: str) -> None:
    manifest_path = _manifest_path(domain_dir)
    manifest = _read_json(manifest_path)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            artifact["status"] = status
            break
    else:
        raise AssertionError(f"missing artifact {artifact_id}")
    _write_json(manifest_path, manifest)


def _set_domain_status(domain_dir: Path, status: str) -> None:
    domain_path = domain_dir / "domain.json"
    domain = _read_json(domain_path)
    domain["status"] = status
    domain["artifact_state"] = status
    _write_json(domain_path, domain)


def _set_agent_status(domain_dir: Path, agent_id: str, status: str) -> None:
    agent_path = domain_dir / "sandbox_agents" / f"{agent_id}.json"
    agent = _read_json(agent_path)
    agent["status"] = status
    _write_json(agent_path, agent)
    _set_manifest_artifact_status(domain_dir, f"agent_{agent_id}", status)


def _set_team_status(domain_dir: Path, team_id: str, status: str) -> None:
    team_path = domain_dir / "sandbox_teams" / f"{team_id}.json"
    team = _read_json(team_path)
    team["status"] = status
    _write_json(team_path, team)
    _set_manifest_artifact_status(domain_dir, f"team_{team_id}", status)


def _team_path(domain_dir: Path, team_id: str) -> Path:
    return domain_dir / "sandbox_teams" / f"{team_id}.json"


def _agent_path(domain_dir: Path, agent_id: str) -> Path:
    return domain_dir / "sandbox_agents" / f"{agent_id}.json"


def _contract_for_team(domain_dir: Path, team_id: str, **overrides) -> dict:
    return evaluate_active_contract(
        target_type="team",
        domain_dir=domain_dir,
        target_id=team_id,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        **overrides,
    )


def _execute_team(domain_dir: Path, team_id: str, contract: dict | None = None) -> dict:
    return execute_active(
        target_type="team",
        domain_dir=domain_dir,
        target_id=team_id,
        active_contract_result=contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="runtime_boundary_test",
    )


def _assert_blocked_by(result: dict, expected: str) -> None:
    assert result.get("contract_result") == "blocked" or result.get("result_status") == "blocked"
    assert expected in " ".join(result["blockers"])


def _build_runtime_policy(**overrides) -> dict:
    policy = build_capability_policy(
        policy_id="policy_runtime_boundary_declared",
        domain_id="sandbox_marketing_crm_automation",
        subject_type="agent",
        subject_id="sandbox_growth_strategist",
        capability_type="tool",
        capability_id="tool_runtime_boundary_declared",
        capability_category="internal_future",
        policy_status="allowed_declared",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )
    policy["promotion_status"] = "candidate_for_activation"
    policy.update(overrides)
    return policy


def test_runtime_execution_and_external_flags_block_contract_and_executor(tmp_path):
    chain = _build_chain(tmp_path)
    domain_dir = chain["domain_dir"]
    team_id = chain["team"]["team_id"]
    _set_team_status(domain_dir, team_id, "candidate_for_activation")
    team_path = _team_path(domain_dir, team_id)
    base_team = _read_json(team_path)

    runtime_team = deepcopy(base_team)
    runtime_team["metadata"]["runtime_enabled"] = True
    _write_json(team_path, runtime_team)
    runtime_contract = _contract_for_team(domain_dir, team_id)
    runtime_execution = _execute_team(domain_dir, team_id, runtime_contract)
    _assert_blocked_by(runtime_contract, "runtime_enabled=true bloqueado")
    _assert_blocked_by(runtime_execution, "runtime_enabled=true bloqueado")

    execution_team = deepcopy(base_team)
    execution_team["coordination_model"]["execution_enabled"] = True
    _write_json(team_path, execution_team)
    execution_contract = _contract_for_team(domain_dir, team_id)
    execution_report = _execute_team(domain_dir, team_id, execution_contract)
    _assert_blocked_by(execution_contract, "execution_enabled=true bloqueado")
    _assert_blocked_by(execution_report, "execution_enabled=true bloqueado")

    external_policy = _build_runtime_policy(external_access=True)
    external_contract = evaluate_active_contract(
        target_type="capability_policy",
        target=external_policy,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )
    external_report = execute_active(
        target_type="capability_policy",
        target=external_policy,
        active_contract_result=external_contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="runtime_boundary_test",
    )
    _assert_blocked_by(external_contract, "external_access=true bloqueado")
    _assert_blocked_by(external_report, "external_access=true bloqueado")


@pytest.mark.parametrize("active_mode", ["runtime_active_future", "external_active_future"])
def test_future_active_modes_remain_blocked(tmp_path, active_mode):
    chain = _build_chain(tmp_path)
    domain_dir = chain["domain_dir"]
    team_id = chain["team"]["team_id"]
    _set_team_status(domain_dir, team_id, "candidate_for_activation")

    contract = _contract_for_team(domain_dir, team_id, active_mode=active_mode)
    report = _execute_team(domain_dir, team_id, contract)

    _assert_blocked_by(contract, f"active_mode bloqueado en esta fase: {active_mode}")
    _assert_blocked_by(report, "active_contract no passed")
    assert report["runtime_enabled"] is False
    assert report["execution_enabled"] is False
    assert report["external_access"] is False


def test_internal_active_for_domain_agent_and_team_does_not_enable_runtime(tmp_path):
    chain = _build_chain(tmp_path)
    domain_dir = chain["domain_dir"]
    agent_id = chain["agent_ids"][0]
    team_id = chain["team"]["team_id"]

    _set_domain_status(domain_dir, "candidate_for_activation")
    domain_contract = evaluate_active_contract(
        target_type="domain",
        domain_dir=domain_dir,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )
    domain_report = execute_active(
        target_type="domain",
        domain_dir=domain_dir,
        active_contract_result=domain_contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="runtime_boundary_test",
    )
    assert domain_report["result_status"] == "passed"
    domain = _read_json(domain_dir / "domain.json")
    assert domain["status"] == "active"
    assert "runtime_enabled" not in domain
    rollback_active_execution(domain_report, domain_dir=domain_dir, executed_by="runtime_boundary_test")
    assert _read_json(domain_dir / "domain.json")["status"] == "candidate_for_activation"

    _set_agent_status(domain_dir, agent_id, "candidate_for_activation")
    agent_contract = evaluate_active_contract(
        target_type="agent",
        domain_dir=domain_dir,
        target_id=agent_id,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )
    agent_report = execute_active(
        target_type="agent",
        domain_dir=domain_dir,
        target_id=agent_id,
        active_contract_result=agent_contract,
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="runtime_boundary_test",
    )
    assert agent_report["result_status"] == "passed"
    agent = _read_json(_agent_path(domain_dir, agent_id))
    assert agent["status"] == "active"
    assert agent["sandbox_config"]["runtime_enabled"] is False
    assert agent["sandbox_config"]["operational"] is False
    rollback_active_execution(agent_report, domain_dir=domain_dir, executed_by="runtime_boundary_test")

    _set_team_status(domain_dir, team_id, "candidate_for_activation")
    team_contract = _contract_for_team(domain_dir, team_id)
    team_report = _execute_team(domain_dir, team_id, team_contract)
    assert team_report["result_status"] == "passed"
    team = _read_json(_team_path(domain_dir, team_id))
    assert team["status"] == "active"
    assert team["metadata"]["runtime_enabled"] is False
    assert team["coordination_model"]["runtime_enabled"] is False
    assert team["coordination_model"]["execution_enabled"] is False
    rollback_active_execution(team_report, domain_dir=domain_dir, executed_by="runtime_boundary_test")
    team_after_rollback = _read_json(_team_path(domain_dir, team_id))
    assert team_after_rollback["status"] == "candidate_for_activation"
    assert team_after_rollback["metadata"]["runtime_enabled"] is False


def test_capability_policy_tool_and_memory_contracts_remain_declarative():
    policy = _build_runtime_policy()
    validated_policy = validate_capability_policy(policy)
    assert validated_policy["runtime_enabled"] is False
    assert validated_policy["execution_allowed"] is False
    assert validated_policy["external_access"] is False

    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_capability_policy({**policy, "runtime_enabled": True})
    with pytest.raises(ValueError, match="execution_allowed=false"):
        validate_capability_policy({**policy, "execution_allowed": True})
    with pytest.raises(ValueError, match="external_access=false"):
        validate_capability_policy({**policy, "external_access": True})

    memory = build_memory_contract(
        memory_id="memory_runtime_boundary_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        memory_scope="agent",
        memory_type="documentary",
        persistence="none",
        storage_backend="none",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )
    assert memory["runtime_enabled"] is False
    assert memory["persistence"] == "none"
    assert memory["storage_backend"] == "none"
    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_memory_contract({**memory, "runtime_enabled": True})

    tool = build_tool_contract(
        tool_id="tool_runtime_boundary_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        tool_name="Runtime Boundary Declared Tool",
        tool_category="internal_future",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )
    assert tool["runtime_enabled"] is False
    assert tool["execution_allowed"] is False
    assert tool["external_access"] is False
    with pytest.raises(ValueError, match="execution_allowed=true"):
        validate_tool_contract({**tool, "execution_allowed": True})
    with pytest.raises(ValueError, match="external_access=true"):
        validate_tool_contract({**tool, "external_access": True})


def test_promotion_executor_and_non_operational_states_cannot_enable_runtime(tmp_path):
    chain = _build_chain(tmp_path)
    domain_dir = chain["domain_dir"]
    team_id = chain["team"]["team_id"]
    team_path = _team_path(domain_dir, team_id)

    active_attempt = execute_promotion(
        target_type="team",
        domain_dir=domain_dir,
        target_id=team_id,
        requested_status="active",
        executed_by="runtime_boundary_test",
    )
    assert active_attempt["execution_result"] == "blocked"
    assert "requested_status active o invalido bloqueado" in " ".join(active_attempt["blockers"])

    for status in ["legacy", "broken", "archived"]:
        team = _read_json(team_path)
        team["status"] = status
        team["metadata"]["runtime_enabled"] = True
        _write_json(team_path, team)
        _set_manifest_artifact_status(domain_dir, f"team_{team_id}", status)

        gate = evaluate_promotion_gate(
            target_type="team",
            domain_dir=domain_dir,
            target_id=team_id,
            requested_status="validated",
        )
        contract = _contract_for_team(domain_dir, team_id)
        report = _execute_team(domain_dir, team_id, contract)

        assert gate["gate_result"] == "blocked"
        assert contract["contract_result"] == "blocked"
        assert report["result_status"] == "blocked"
        assert "runtime_enabled=true bloqueado" in " ".join(report["blockers"])
        assert f"current_status bloqueado: {status}" in " ".join(report["blockers"])
