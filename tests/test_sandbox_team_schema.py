import hashlib
from pathlib import Path

import pytest

from core.artifact_manifest_schema import empty_artifact_manifest, validate_artifact_manifest
from core.sandbox_agent_memory_contract import build_memory_contract
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_team_schema import (
    build_sandbox_team_schema,
    sandbox_team_to_artifact_record,
    validate_sandbox_team_schema,
)
from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID
from core.profile_catalog_materializer import PROFILE_CATALOG_ARTIFACT_ID
from tests.test_sandbox_agent_schema import _agent, _artifact, sandbox_agent_to_artifact_record


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


def _member(agent_id="sandbox_growth_strategist", **overrides):
    payload = {
        "agent_id": agent_id,
        "role": "estratega",
        "specialization": "negocio_digital",
        "responsibility": "Define hipotesis y criterios de priorizacion.",
        "required": True,
        "source_reference": {
            "artifact_id": f"agent_{agent_id}",
            "artifact_type": "agent",
        },
        "status": "materialized",
    }
    payload.update(overrides)
    return payload


def _coordination(**overrides):
    payload = {
        "coordination_type": "single_coordinator",
        "coordinator_agent_id": "sandbox_growth_strategist",
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": ["El coordinador sintetiza, no ejecuta agentes."],
        "suggested_order": ["sandbox_growth_strategist", "sandbox_quality_reviewer"],
        "restrictions": ["No debate runtime en esta fase."],
    }
    payload.update(overrides)
    return payload


def _memory(**overrides):
    payload = build_memory_contract(
        memory_id="memory_sandbox_team_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        memory_scope="team",
        memory_type="shared_future",
        persistence="none",
        storage_backend="none",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def _tool(**overrides):
    payload = build_tool_contract(
        tool_id="tool_sandbox_team_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        tool_name="Future Team Review Tool",
        tool_category="internal_future",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def _policy(**overrides):
    payload = {
        "policy_id": "policy_team_capabilities_declared",
        "status": "declared",
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "external_access": False,
    }
    payload.update(overrides)
    return payload


def _team(**overrides):
    payload = build_sandbox_team_schema(
        team_id="sandbox_growth_team",
        domain_id="sandbox_marketing_crm_automation",
        name="Sandbox Growth Team",
        purpose="Coordinar analisis y revision sin ejecucion runtime.",
        member_agents=[
            _member(),
            _member(
                "sandbox_quality_reviewer",
                role="validador",
                specialization="calidad",
                responsibility="Revisa consistencia y riesgos del entregable.",
            ),
        ],
        coordination_model=_coordination(),
        capabilities={"memory": [], "tools": [], "policies": []},
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def test_valid_team_contract_passes():
    team = validate_sandbox_team_schema(_team())

    assert team["team_id"] == "sandbox_growth_team"
    assert team["status"] == "materialized"
    assert team["dependencies"] == [
        "agent_sandbox_growth_strategist",
        "agent_sandbox_quality_reviewer",
    ]


def test_team_requires_members():
    with pytest.raises(ValueError, match="member_agents"):
        build_sandbox_team_schema(
            team_id="sandbox_empty_team",
            domain_id="sandbox_marketing_crm_automation",
            name="Empty Team",
            purpose="Debe fallar.",
            member_agents=[],
        )


def test_member_requires_agent_id():
    team = _team(member_agents=[_member(agent_id="")])

    with pytest.raises(ValueError, match="agent_id"):
        validate_sandbox_team_schema(team)


def test_member_requires_responsibility():
    team = _team(member_agents=[_member(responsibility="")])

    with pytest.raises(ValueError, match="responsibility"):
        validate_sandbox_team_schema(team)


def test_duplicate_members_fail():
    team = _team(member_agents=[_member(), _member()])

    with pytest.raises(ValueError, match="duplicado"):
        validate_sandbox_team_schema(team)


def test_active_fails():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_team_schema(_team(status="active"))


def test_runtime_enabled_fails():
    with pytest.raises(ValueError, match="runtime_enabled=true"):
        validate_sandbox_team_schema(_team(runtime_enabled=True))


def test_execution_enabled_fails():
    with pytest.raises(ValueError, match="execution_enabled=true"):
        validate_sandbox_team_schema(_team(execution_enabled=True))


def test_declarative_coordination_model_passes():
    team = _team(coordination_model=_coordination(coordination_type="parallel_review"))

    validated = validate_sandbox_team_schema(team)

    assert validated["coordination_model"]["coordination_type"] == "parallel_review"
    assert validated["coordination_model"]["runtime_enabled"] is False


def test_executable_coordination_model_fails():
    team = _team(coordination_model=_coordination(executable=True))

    with pytest.raises(ValueError, match="executable=true"):
        validate_sandbox_team_schema(team)


def test_declarative_capabilities_pass():
    team = _team(
        capabilities={
            "memory": [_memory()],
            "tools": [_tool()],
            "policies": [_policy()],
        }
    )

    validated = validate_sandbox_team_schema(team)

    assert validated["capabilities"]["memory"][0]["memory_scope"] == "team"
    assert validated["capabilities"]["tools"][0]["execution_allowed"] is False
    assert validated["capabilities"]["policies"][0]["declared_only"] is True


def test_executable_capabilities_fail():
    team = _team(capabilities={"memory": [], "tools": [_tool(external_access=True)], "policies": []})

    with pytest.raises(ValueError, match="external_access=true"):
        validate_sandbox_team_schema(team)

    team = _team(capabilities={"memory": [], "tools": [], "policies": [_policy(execution_enabled=True)]})

    with pytest.raises(ValueError, match="execution_enabled=false"):
        validate_sandbox_team_schema(team)


def test_future_artifact_manifest_compatibility():
    agent_a = sandbox_agent_to_artifact_record(_agent(status="materialized"))
    agent_b_payload = _agent(
        agent_id="sandbox_quality_reviewer",
        role={"role_id": "validador"},
        specialization={"specialization_id": "calidad"},
        status="materialized",
    )
    agent_b = sandbox_agent_to_artifact_record(agent_b_payload)
    manifest = empty_artifact_manifest("sandbox_marketing_crm_automation")
    manifest["artifacts"] = [
        _artifact(PROFILE_CATALOG_ARTIFACT_ID, "profile_catalog"),
        _artifact(
            AGENT_PRESETS_ARTIFACT_ID,
            "agent_preset",
            dependencies=[PROFILE_CATALOG_ARTIFACT_ID],
        ),
        _artifact(
            PAPER_SEED_ARTIFACT_ID,
            "paper_seed",
            dependencies=[PROFILE_CATALOG_ARTIFACT_ID, AGENT_PRESETS_ARTIFACT_ID],
        ),
        agent_a,
        agent_b,
        sandbox_team_to_artifact_record(_team()),
    ]

    validated = validate_artifact_manifest(manifest)

    assert validated["artifacts"][-1]["artifact_type"] == "team"
    assert validated["artifacts"][-1]["dependencies"] == [
        "agent_sandbox_growth_strategist",
        "agent_sandbox_quality_reviewer",
    ]


def test_team_schema_does_not_create_runtime_or_legacy_files():
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    validate_sandbox_team_schema(_team())

    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers
