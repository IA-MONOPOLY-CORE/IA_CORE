import pytest

from core.artifact_state import ArtifactState, is_operational
from core.capability_policy_schema import build_capability_policy, validate_capability_policy
from core.domain_state import DomainState, is_domain_active, is_valid_domain_transition
from core.promotion_executor import execute_promotion
from core.promotion_gate import evaluate_promotion_gate
from core.sandbox_agent_schema import validate_sandbox_agent_schema
from core.sandbox_domain_schema import validate_sandbox_domain_schema
from core.sandbox_team_schema import validate_sandbox_team_schema
from tests.test_promotion_gate import _build_chain, _valid_policy
from tests.test_sandbox_agent_schema import _agent
from tests.test_sandbox_domain_schema import _valid_domain
from tests.test_sandbox_team_schema import _team


def _policy(**overrides):
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


def test_promotion_gate_blocks_active(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_promotion_gate(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=chain["team"]["team_id"],
        requested_status="active",
    )

    assert result["gate_result"] == "blocked"
    assert "active" in " ".join(result["blockers"])


def test_promotion_executor_blocks_active(tmp_path):
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
    assert "active" in " ".join(result["blockers"])


def test_capability_policy_cannot_enable_runtime_execution_or_external_access():
    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_capability_policy(_policy(runtime_enabled=True))
    with pytest.raises(ValueError, match="execution_allowed=false"):
        validate_capability_policy(_policy(execution_allowed=True))
    with pytest.raises(ValueError, match="external_access=false"):
        validate_capability_policy(_policy(external_access=True))


def test_agent_team_and_domain_active_are_not_allowed_by_sandbox_contracts():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_agent_schema(_agent(status=ArtifactState.ACTIVE.value))
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_team_schema(_team(status=ArtifactState.ACTIVE.value))
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_domain_schema(
            _valid_domain(
                status=DomainState.ACTIVE.value,
                artifact_state=ArtifactState.ACTIVE.value,
            )
        )


def test_runtime_execution_and_external_access_boundaries_still_block(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id = chain["agent_ids"][0]
    agent_path = chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"
    agent = agent_path.read_text(encoding="utf-8")
    agent_path.write_text(agent.replace('"runtime_enabled": false', '"runtime_enabled": true', 1), encoding="utf-8")

    runtime_gate = evaluate_promotion_gate(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        requested_status="validated",
    )

    assert runtime_gate["gate_result"] == "blocked"
    assert "runtime_enabled" in " ".join(runtime_gate["blockers"])

    execution_team = _team()
    execution_team["coordination_model"]["execution_enabled"] = True
    with pytest.raises(ValueError, match="execution_enabled=false"):
        validate_sandbox_team_schema(execution_team)

    external_gate = evaluate_promotion_gate(
        target_type="capability_policy",
        target=_valid_policy(external_access=True),
        requested_status="validated",
    )
    assert external_gate["gate_result"] == "blocked"
    assert "external_access" in " ".join(external_gate["blockers"])


def test_legacy_broken_and_archived_cannot_be_active():
    legacy_domain = {"id": "legacy_domain", "legacy": True, "visible_en_hud": False}
    broken_domain = {
        "id": "broken_domain",
        "status": DomainState.BROKEN.value,
        "broken_reason": "test",
        "visible_en_hud": False,
    }
    archived_domain = {
        "id": "archived_domain",
        "status": DomainState.ARCHIVED.value,
        "visible_en_hud": False,
    }

    assert is_domain_active(legacy_domain) is False
    assert is_domain_active(broken_domain) is False
    assert is_domain_active(archived_domain) is False
    assert is_valid_domain_transition(DomainState.LEGACY, DomainState.ACTIVE) is False
    assert is_valid_domain_transition(DomainState.BROKEN, DomainState.ACTIVE) is False
    assert is_valid_domain_transition(DomainState.ARCHIVED, DomainState.ACTIVE) is False


def test_candidate_and_validated_do_not_equal_active():
    assert is_operational(ArtifactState.VALIDATED, has_traceability=True) is False
    assert is_operational(ArtifactState.CANDIDATE_FOR_ACTIVATION, has_traceability=True) is False
    assert is_operational(ArtifactState.ACTIVE, has_traceability=True) is True
    assert ArtifactState.VALIDATED.value != ArtifactState.ACTIVE.value
    assert ArtifactState.CANDIDATE_FOR_ACTIVATION.value != ArtifactState.ACTIVE.value
