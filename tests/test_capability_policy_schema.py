import hashlib
from pathlib import Path

import pytest

from core.capability_policy_schema import (
    build_capability_policy,
    evaluate_capability_policy_status,
    validate_capability_policy,
    validate_capability_policy_for_subject,
    validate_team_policy_member_boundary,
)
from core.sandbox_agent_memory_contract import build_memory_contract
from core.sandbox_agent_schema import validate_sandbox_agent_schema
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_team_schema import validate_sandbox_team_schema
from tests.test_sandbox_agent_schema import _agent
from tests.test_sandbox_team_schema import _team


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"
MEMORY = ROOT / "memory"


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


def _policy(**overrides):
    payload = build_capability_policy(
        policy_id="policy_sandbox_growth_strategist_memory_declared",
        domain_id="sandbox_marketing_crm_automation",
        subject_type="agent",
        subject_id="sandbox_growth_strategist",
        capability_type="memory",
        capability_id="memory_sandbox_growth_strategist_declared",
        capability_category="documentary",
        policy_status="allowed_declared",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def _memory(**overrides):
    payload = build_memory_contract(
        memory_id="memory_sandbox_growth_strategist_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        memory_scope="agent",
        memory_type="documentary",
        persistence="none",
        storage_backend="none",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def _tool(**overrides):
    payload = build_tool_contract(
        tool_id="tool_sandbox_growth_strategist_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        tool_name="Future Internal Analysis Tool",
        tool_category="internal_future",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def test_valid_capability_policy_for_agent_passes():
    policy = validate_capability_policy_for_subject(
        _policy(),
        subject_type="agent",
        subject_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
    )

    assert policy["subject_type"] == "agent"
    assert policy["allowed_by_policy"] is True
    assert policy["runtime_enabled"] is False


def test_valid_capability_policy_for_team_passes():
    policy = validate_capability_policy_for_subject(
        _policy(
            policy_id="policy_sandbox_growth_team_tool_declared",
            subject_type="team",
            subject_id="sandbox_growth_team",
            capability_type="tool",
            capability_id="tool_sandbox_team_declared",
            capability_category="internal_future",
        ),
        subject_type="team",
        subject_id="sandbox_growth_team",
        domain_id="sandbox_marketing_crm_automation",
    )

    assert policy["subject_type"] == "team"
    assert policy["execution_allowed"] is False


def test_memory_declared_allowed_passes():
    policy = validate_capability_policy(_policy(capability_type="memory"))

    assert policy["policy_status"] == "allowed_declared"


def test_tool_declared_allowed_passes():
    policy = validate_capability_policy(
        _policy(
            policy_id="policy_sandbox_growth_strategist_tool_declared",
            capability_type="tool",
            capability_id="tool_sandbox_growth_strategist_declared",
            capability_category="internal_future",
        )
    )

    assert policy["capability_type"] == "tool"


def test_policy_declared_allowed_passes():
    policy = validate_capability_policy(
        _policy(
            policy_id="policy_sandbox_growth_strategist_policy_declared",
            capability_type="policy",
            capability_id="policy_sandbox_growth_strategist_policy_declared",
            capability_category="governance",
        )
    )

    assert policy["capability_type"] == "policy"


def test_runtime_enabled_fails():
    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_capability_policy(_policy(runtime_enabled=True))


def test_execution_allowed_fails():
    with pytest.raises(ValueError, match="execution_allowed=false"):
        validate_capability_policy(_policy(execution_allowed=True))


def test_external_access_fails():
    with pytest.raises(ValueError, match="external_access=false"):
        validate_capability_policy(_policy(external_access=True))


def test_forbidden_tool_fails_if_declared_as_allowed():
    with pytest.raises(ValueError, match="allowed_by_policy=true solo"):
        validate_capability_policy(
            _policy(
                capability_type="tool",
                capability_id="tool_sandbox_growth_strategist_declared",
                policy_status="forbidden",
                allowed_by_policy=True,
            )
        )


def test_future_requires_approval_passes_only_as_declarative():
    policy = validate_capability_policy(
        _policy(
            policy_status="future_requires_approval",
            allowed_by_policy=False,
            requires_approval=True,
            approval_status="future_required",
        )
    )

    assert policy["declared_only"] is True
    assert policy["requires_approval"] is True
    assert policy["runtime_enabled"] is False

    with pytest.raises(ValueError, match="future_requires_approval requiere"):
        validate_capability_policy(
            _policy(
                policy_status="future_requires_approval",
                allowed_by_policy=False,
                requires_approval=False,
                approval_status="not_required",
            )
        )


def test_self_approval_fails():
    with pytest.raises(ValueError, match="self_approval"):
        validate_capability_policy(
            _policy(
                capability_type="policy",
                capability_id="policy_sandbox_growth_strategist_policy_declared",
                capability_category="governance",
                restrictions=["self_approval"],
            )
        )


def test_team_capability_does_not_enable_members_automatically():
    policy = _policy(
        policy_id="policy_sandbox_growth_team_tool_declared",
        subject_type="team",
        subject_id="sandbox_growth_team",
        capability_type="tool",
        capability_id="tool_sandbox_team_declared",
        capability_category="internal_future",
    )

    validated = validate_team_policy_member_boundary(policy)

    assert validated["subject_type"] == "team"
    assert evaluate_capability_policy_status(
        capability_id="tool_sandbox_growth_strategist_declared",
        policies=[validated],
    )["policy_status"] == "missing"

    with pytest.raises(ValueError, match="no habilita automaticamente"):
        validate_team_policy_member_boundary(
            {
                **policy,
                "restrictions": [{"auto_enable_members": True}],
            }
        )


def test_agent_without_capabilities_still_valid():
    agent = _agent()
    agent.pop("capabilities")

    validated = validate_sandbox_agent_schema(agent)

    assert "capabilities" not in validated


def test_team_without_capabilities_still_valid():
    team = _team()
    team.pop("capabilities")

    validated = validate_sandbox_team_schema(team)

    assert "capabilities" not in validated


def test_agent_schema_accepts_declarative_policy_and_rejects_executable_capabilities():
    agent = _agent(
        capabilities={
            "memory": [_memory()],
            "tools": [_tool()],
            "policies": [_policy()],
        }
    )

    validated = validate_sandbox_agent_schema(agent)

    assert validated["capabilities"]["policies"][0]["allowed_by_policy"] is True

    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_sandbox_agent_schema(
            _agent(capabilities={"memory": [_memory(runtime_enabled=True)], "tools": []})
        )


def test_team_schema_accepts_declarative_policy_and_rejects_executable_capabilities():
    team_policy = _policy(
        policy_id="policy_sandbox_growth_team_tool_declared",
        subject_type="team",
        subject_id="sandbox_growth_team",
        capability_type="tool",
        capability_id="tool_sandbox_team_declared",
        capability_category="internal_future",
    )
    team = _team(capabilities={"memory": [], "tools": [_tool()], "policies": [team_policy]})

    validated = validate_sandbox_team_schema(team)

    assert validated["capabilities"]["policies"][0]["subject_type"] == "team"

    with pytest.raises(ValueError, match="execution_allowed=false"):
        validate_sandbox_team_schema(
            _team(capabilities={"memory": [], "tools": [], "policies": [{**team_policy, "execution_allowed": True}]})
        )


def test_capability_policy_does_not_create_memory_tools_runtime_or_legacy_files():
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    before_catalogs = _tree_hash(CATALOGS)
    before_memory = _tree_hash(MEMORY)
    before_papers = _papers_hash()

    validate_sandbox_agent_schema(
        _agent(
            capabilities={
                "memory": [_memory()],
                "tools": [_tool()],
                "policies": [_policy()],
            }
        )
    )
    validate_sandbox_team_schema(
        _team(
            capabilities={
                "memory": [],
                "tools": [],
                "policies": [
                    _policy(
                        policy_id="policy_sandbox_growth_team_tool_declared",
                        subject_type="team",
                        subject_id="sandbox_growth_team",
                        capability_type="tool",
                        capability_id="tool_sandbox_team_declared",
                        capability_category="internal_future",
                    )
                ],
            }
        )
    )

    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _tree_hash(MEMORY) == before_memory
    assert _papers_hash() == before_papers
