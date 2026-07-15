import hashlib
from pathlib import Path

import pytest

from core.sandbox_agent_memory_contract import (
    build_memory_contract,
    validate_memory_contract,
)
from core.sandbox_agent_schema import validate_sandbox_agent_schema
from core.sandbox_agent_tool_contract import build_tool_contract, validate_tool_contract
from tests.test_sandbox_agent_schema import _agent


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


def test_valid_memory_contract_passes():
    memory = validate_memory_contract(_memory())

    assert memory["declared_only"] is True
    assert memory["runtime_enabled"] is False
    assert memory["storage_backend"] == "none"


def test_valid_tool_contract_passes():
    tool = validate_tool_contract(_tool())

    assert tool["declared_only"] is True
    assert tool["runtime_enabled"] is False
    assert tool["execution_allowed"] is False
    assert tool["external_access"] is False


def test_memory_runtime_enabled_true_fails():
    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_memory_contract(_memory(runtime_enabled=True))


def test_tool_execution_allowed_true_fails():
    with pytest.raises(ValueError, match="execution_allowed=true"):
        validate_tool_contract(_tool(execution_allowed=True))


def test_tool_external_access_true_fails():
    with pytest.raises(ValueError, match="external_access=true"):
        validate_tool_contract(_tool(external_access=True))


def test_non_declarative_capability_fails():
    with pytest.raises(ValueError, match="declared_only=true"):
        validate_memory_contract(_memory(declared_only=False))

    with pytest.raises(ValueError, match="status declared"):
        validate_tool_contract(_tool(status="active"))

    with pytest.raises(ValueError, match="enabled=true"):
        validate_tool_contract(_tool(enabled=True))


def test_sandbox_agent_without_capabilities_still_passes():
    agent = _agent()
    agent.pop("capabilities")

    validated = validate_sandbox_agent_schema(agent)

    assert "capabilities" not in validated


def test_sandbox_agent_with_declarative_capabilities_passes():
    agent = _agent(
        capabilities={
            "memory": [_memory()],
            "tools": [_tool()],
        }
    )

    validated = validate_sandbox_agent_schema(agent)

    assert validated["capabilities"]["memory"][0]["declared_only"] is True
    assert validated["capabilities"]["tools"][0]["execution_allowed"] is False


def test_sandbox_agent_blocks_runtime_capabilities():
    agent = _agent(
        capabilities={
            "memory": [_memory(runtime_enabled=True)],
            "tools": [],
        }
    )

    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_sandbox_agent_schema(agent)

    agent = _agent(
        capabilities={
            "memory": [],
            "tools": [_tool(external_access=True)],
        }
    )

    with pytest.raises(ValueError, match="external_access=true"):
        validate_sandbox_agent_schema(agent)


def test_contracts_do_not_create_memory_tools_runtime_or_legacy_files():
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    validate_sandbox_agent_schema(
        _agent(
            capabilities={
                "memory": [_memory()],
                "tools": [_tool()],
            }
        )
    )

    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers
