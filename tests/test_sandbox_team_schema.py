import hashlib
import json
from pathlib import Path

import pytest

from core.artifact_manifest_schema import empty_artifact_manifest, validate_artifact_manifest
from core.sandbox_agent_memory_contract import build_memory_contract
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_team_schema import (
    build_sandbox_team_schema,
    is_valid_sandbox_team,
    sandbox_team_to_artifact_record,
    validate_sandbox_team_file,
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
    assert team["team_type"] == "sandbox"
    assert team["status"] == "materialized"
    assert team["artifact_state"] == "materialized"
    assert team["description"]
    assert team["members"][0]["role_id"] == "estratega"
    assert team["permissions"]["can_execute"] is False
    assert team["execution_policy"]["runtime_enabled"] is False
    assert team["dependencies"] == [
        "agent_sandbox_growth_strategist",
        "agent_sandbox_quality_reviewer",
    ]


def test_missing_required_fields_fail_with_clear_error():
    team = _team()
    team.pop("description")

    with pytest.raises(ValueError, match="description"):
        validate_sandbox_team_schema(team)


def test_team_type_must_be_sandbox():
    team = _team(team_type="derived_team_template")

    with pytest.raises(ValueError, match="team_type"):
        validate_sandbox_team_schema(team)


def test_team_requires_members():
    with pytest.raises(ValueError, match="members"):
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


def test_member_requires_role_id():
    team = _team()
    team["members"][0].pop("role_id")

    with pytest.raises(ValueError, match="role_id"):
        validate_sandbox_team_schema(team)


def test_member_requires_responsibility():
    team = _team(member_agents=[_member(responsibility="")])

    with pytest.raises(ValueError, match="responsibility"):
        validate_sandbox_team_schema(team)


def test_member_requires_responsibilities():
    team = _team()
    team["members"][0]["responsibilities"] = []

    with pytest.raises(ValueError, match="responsibilities"):
        validate_sandbox_team_schema(team)


def test_duplicate_members_fail():
    team = _team(member_agents=[_member(), _member()])

    with pytest.raises(ValueError, match="duplicado"):
        validate_sandbox_team_schema(team)


def test_active_fails():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_team_schema(_team(status="active"))


def test_artifact_state_active_fails():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_team_schema(_team(artifact_state="active"))


def test_runtime_enabled_fails():
    with pytest.raises(ValueError, match="runtime_enabled=true"):
        validate_sandbox_team_schema(_team(runtime_enabled=True))


def test_execution_enabled_fails():
    with pytest.raises(ValueError, match="execution_enabled=true"):
        validate_sandbox_team_schema(_team(execution_enabled=True))


def test_execution_policy_is_required_and_default_denied():
    team = _team()
    team.pop("execution_policy")
    with pytest.raises(ValueError, match="execution_policy"):
        validate_sandbox_team_schema(team)

    for field in [
        "execution_enabled",
        "runtime_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ]:
        team = _team()
        team["execution_policy"][field] = True
        with pytest.raises(ValueError, match=field):
            validate_sandbox_team_schema(team)

    team = _team()
    team["execution_policy"]["human_approval_required"] = False
    with pytest.raises(ValueError, match="human_approval_required"):
        validate_sandbox_team_schema(team)


def test_sensitive_permissions_are_blocked():
    for field in [
        "can_execute",
        "can_call_tools",
        "can_call_models",
        "can_write_outputs",
        "can_access_network",
        "can_use_integrations",
    ]:
        team = _team()
        team["permissions"][field] = True
        with pytest.raises(ValueError, match=field):
            validate_sandbox_team_schema(team)


def test_source_lineage_fields_are_required():
    for field in ["source_team_template", "materialization_id", "artifact_id", "created_from"]:
        team = _team()
        team.pop(field)
        with pytest.raises(ValueError, match=field):
            validate_sandbox_team_schema(team)


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


def test_json_non_serializable_fails():
    team = _team()
    team["metadata"]["bad"] = {object()}

    with pytest.raises(ValueError, match="serializable"):
        validate_sandbox_team_schema(team)


def test_validate_sandbox_team_file_reads_json_without_writes(tmp_path):
    path = tmp_path / "team.json"
    path.write_text("{}\n", encoding="utf-8")
    before = path.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="incompleto"):
        validate_sandbox_team_file(path)

    assert path.read_text(encoding="utf-8") == before

    path.write_text(json.dumps(_team(), ensure_ascii=False), encoding="utf-8")
    assert validate_sandbox_team_file(path)["team_id"] == "sandbox_growth_team"


def test_team_template_derived_is_not_sandbox_team():
    template = {
        "schema_version": "1.0",
        "artifact_type": "derived_professional_team_template",
        "team_template_id": "equipo_growth_ventas",
        "members": [],
    }

    assert is_valid_sandbox_team(template) is False
    with pytest.raises(ValueError, match="sandbox team incompleto"):
        validate_sandbox_team_schema(template)


def test_valid_team_can_keep_null_agent_reference():
    member = {
        "member_id": "sandbox_strategy_member",
        "role_id": "estratega",
        "role_name": "Estratega",
        "specialization_id": "negocio_digital",
        "specialization_name": "Negocio Digital",
        "agent_reference": None,
        "responsibilities": ["Define estrategia sin agente materializado todavia."],
        "inputs": [],
        "outputs": [],
        "status": "materialized",
        "artifact_state": "materialized",
    }
    coordination = {
        "coordination_type": "none",
        "coordinator_agent_id": None,
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": [],
        "suggested_order": ["sandbox_strategy_member"],
        "restrictions": ["Sin ejecucion."],
    }

    team = build_sandbox_team_schema(
        team_id="sandbox_unbound_team",
        domain_id="sandbox_marketing_crm_automation",
        name="Sandbox Unbound Team",
        purpose="Equipo declarativo sin agente materializado.",
        member_agents=[_member()],
        members=[member],
        coordination_model=coordination,
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )

    assert team["members"][0]["agent_reference"] is None
    assert team["dependencies"] == []


def test_schema_is_compatible_with_artifact_and_domain_states():
    team = _team(status="validated", artifact_state="candidate_for_activation")

    validated = validate_sandbox_team_schema(team)

    assert validated["status"] == "validated"
    assert validated["artifact_state"] == "candidate_for_activation"


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
    assert validated["artifacts"][-1]["created_from"]["artifact_kind"] == "sandbox_team"
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


def test_team_schema_does_not_register_operational_team():
    team = validate_sandbox_team_schema(_team())
    artifact = sandbox_team_to_artifact_record(team)

    assert artifact["operational"] is False
    assert artifact["passed"] is False
    assert team["metadata"]["operational"] is False
    assert team["metadata"]["creates_runtime_team"] is False
