import hashlib
import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import materialize_agent_presets
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog
from core.sandbox_agent_materializer import materialize_sandbox_agent
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_team_materializer import (
    materialize_sandbox_team_from_template,
    materialize_sandbox_team,
    regenerate_sandbox_team,
    rollback_sandbox_team,
    validate_materialized_sandbox_team,
)


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"


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


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="team materialization",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )


def _schema_from_preview(preview: dict) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    return schema


def _domain_with_agents(tmp_path) -> tuple[dict, list[dict]]:
    preview = _preview()
    domain = materialize_sandbox_domain(
        _schema_from_preview(preview),
        sandbox_root=tmp_path / "sandboxes",
    )
    materialize_profile_catalog(domain["domain_dir"])
    presets = materialize_agent_presets(domain["domain_dir"])
    materialize_paper_seed(domain["domain_dir"])
    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(domain["domain_dir"], preset_id=preset["preset_id"])
        for preset in presets_payload["presets"]
    ]
    return domain, agents


def _domain_only(tmp_path) -> dict:
    preview = _preview()
    return materialize_sandbox_domain(
        _schema_from_preview(preview),
        sandbox_root=tmp_path / "sandboxes",
    )


def _team_template(**overrides):
    payload = {
        "schema_version": "1.0",
        "artifact_type": "derived_professional_team_template",
        "team_template": {
            "team_template_id": "sandbox_marketing_crm_automation_equipo_growth_ventas",
            "nombre": "Equipo de growth y ventas",
            "descripcion": "Plantilla derivada para aumentar ventas y conversion.",
            "objetivo": "Aumentar ventas sin ejecutar agentes.",
            "recommended_domain_profile_ids": [
                "perfil_estratega_growth",
                "perfil_especialista_conversion",
            ],
            "recommended_profile_ids": [
                "estratega_growth",
                "especialista_conversion",
            ],
            "recommended_preset_ids": [
                "preset_estratega_growth",
                "preset_especialista_conversion",
            ],
            "required_team_roles": ["estratega", "especialista"],
            "optional_team_roles": ["validador"],
            "expected_outputs": ["Plan comercial declarativo."],
            "source": "derived_profile_catalog_and_agent_presets",
            "generated_from": {
                "generator": "core.professional_team_template_generator",
                "profile_catalog": "derived_profile_catalog",
                "agent_presets": "derived_domain_agent_presets",
            },
            "status": "derived",
            "activo": True,
            "warnings": [],
            "risks": ["No ejecutar sin aprobacion futura."],
        },
    }
    payload["team_template"].update(overrides)
    return payload


def _coordination(agent_ids: list[str], **overrides):
    payload = {
        "coordination_type": "single_coordinator",
        "coordinator_agent_id": agent_ids[0],
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": ["Coordina solo de forma declarativa."],
        "suggested_order": list(agent_ids),
        "restrictions": ["Sin debate runtime.", "Sin pipeline ejecutable."],
    }
    payload.update(overrides)
    return payload


def _capabilities(domain_id: str, owner_agent_id: str, **tool_overrides):
    tool = build_tool_contract(
        tool_id="tool_sandbox_team_declared",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        tool_name="Future Team Tool",
        tool_category="internal_future",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    tool.update(tool_overrides)
    return {"memory": [], "tools": [tool], "policies": []}


def test_materializes_team_with_valid_sandbox_agents(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)

    result = materialize_sandbox_team(domain["domain_dir"], agent_ids=[agent["agent_id"] for agent in agents])

    team_path = Path(result["team_path"])
    assert team_path.is_file()
    assert result["team"]["status"] == "materialized"
    assert result["team"]["metadata"]["runtime_enabled"] is False
    assert result["team"]["metadata"]["execution_enabled"] is False
    assert [member["agent_id"] for member in result["team"]["member_agents"]] == [
        agent["agent_id"] for agent in agents
    ]


def test_team_requires_members(tmp_path):
    domain, _agents = _domain_with_agents(tmp_path)

    with pytest.raises(ValueError, match="al menos un agente"):
        materialize_sandbox_team(domain["domain_dir"], agent_ids=[])


def test_members_require_existing_agents(tmp_path):
    domain, _agents = _domain_with_agents(tmp_path)

    with pytest.raises(FileNotFoundError, match="inexistente"):
        materialize_sandbox_team(domain["domain_dir"], agent_ids=["sandbox_missing_agent"])


def test_duplicate_members_are_blocked(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)

    with pytest.raises(ValueError, match="duplicado"):
        materialize_sandbox_team(
            domain["domain_dir"],
            agent_ids=[agents[0]["agent_id"], agents[0]["agent_id"]],
        )


def test_artifact_manifest_is_updated_with_team(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)

    result = materialize_sandbox_team(domain["domain_dir"], agent_ids=[agent["agent_id"] for agent in agents])

    artifact = result["artifact_manifest"]["artifacts"][-1]
    assert artifact["artifact_type"] == "team"
    assert artifact["artifact_id"] == f"team_{result['team_id']}"
    assert artifact["status"] == "materialized"
    assert artifact["dependencies"][:3] == [
        "profile_catalog_main",
        "agent_presets_main",
        "paper_seed_main",
    ]
    assert artifact["dependencies"][3:] == [f"agent_{agent['agent_id']}" for agent in agents]


def test_active_runtime_and_execution_are_blocked(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)
    agent_ids = [agent["agent_id"] for agent in agents]
    agent_payload = json.loads(Path(agents[0]["agent_path"]).read_text(encoding="utf-8"))
    agent_payload["status"] = "active"
    Path(agents[0]["agent_path"]).write_text(
        json.dumps(agent_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="active"):
        materialize_sandbox_team(
            domain["domain_dir"],
            agent_ids=agent_ids,
            team_id="active_member_team",
        )

    agent_payload["status"] = "materialized"
    Path(agents[0]["agent_path"]).write_text(
        json.dumps(agent_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="runtime_enabled=false"):
        materialize_sandbox_team(
            domain["domain_dir"],
            agent_ids=agent_ids,
            team_id="runtime_team",
            coordination_model=_coordination(agent_ids, runtime_enabled=True),
        )

    with pytest.raises(ValueError, match="execution_enabled=false"):
        materialize_sandbox_team(
            domain["domain_dir"],
            agent_ids=agent_ids,
            team_id="execution_team",
            coordination_model=_coordination(agent_ids, execution_enabled=True),
        )


def test_executable_coordination_is_blocked(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)
    agent_ids = [agent["agent_id"] for agent in agents]

    with pytest.raises(ValueError, match="pipeline_enabled=true"):
        materialize_sandbox_team(
            domain["domain_dir"],
            agent_ids=agent_ids,
            coordination_model=_coordination(agent_ids, pipeline_enabled=True),
        )


def test_declarative_capabilities_pass_and_executable_capabilities_fail(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)
    agent_ids = [agent["agent_id"] for agent in agents]

    result = materialize_sandbox_team(
        domain["domain_dir"],
        agent_ids=agent_ids,
        capabilities=_capabilities(result_domain_id := domain["domain_id"], agent_ids[0]),
    )
    assert result["team"]["capabilities"]["tools"][0]["execution_allowed"] is False

    with pytest.raises(ValueError, match="external_access=true"):
        materialize_sandbox_team(
            domain["domain_dir"],
            agent_ids=agent_ids,
            team_id="bad_capability_team",
            capabilities=_capabilities(result_domain_id, agent_ids[0], external_access=True),
        )


def test_rollback_removes_team_and_preserves_agents(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)
    result = materialize_sandbox_team(domain["domain_dir"], agent_ids=[agent["agent_id"] for agent in agents])
    team_path = Path(result["team_path"])
    agent_paths = [Path(agent["agent_path"]) for agent in agents]

    rollback = rollback_sandbox_team(domain["domain_dir"], team_id=result["team_id"])

    assert rollback["status"] == "rolled_back"
    assert not team_path.exists()
    assert all(path.is_file() for path in agent_paths)
    assert "team" not in [artifact["artifact_type"] for artifact in rollback["artifact_manifest"]["artifacts"]]


def test_regeneration_increments_version_and_history(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)
    agent_ids = [agent["agent_id"] for agent in agents]
    first = materialize_sandbox_team(domain["domain_dir"], agent_ids=agent_ids)

    second = regenerate_sandbox_team(
        domain["domain_dir"],
        team_id=first["team_id"],
        agent_ids=agent_ids,
        purpose="Equipo regenerado sin runtime.",
    )

    assert first["team_id"] == second["team_id"]
    assert first["version"] == "1.0.0"
    assert second["version"] == "1.0.1"
    assert [event["event"] for event in second["team"]["history"]] == [
        "materialized",
        "regenerated",
    ]
    assert second["artifact"]["dependencies"][3:] == [f"agent_{agent_id}" for agent_id in agent_ids]


def test_validate_materialized_team(tmp_path):
    domain, agents = _domain_with_agents(tmp_path)
    result = materialize_sandbox_team(domain["domain_dir"], agent_ids=[agent["agent_id"] for agent in agents])

    validation = validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])

    assert validation["team"]["team_id"] == result["team_id"]
    assert validation["artifact"]["artifact_type"] == "team"


def test_team_materialization_does_not_touch_legacy_or_global_files(tmp_path):
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()
    domain, agents = _domain_with_agents(tmp_path)

    materialize_sandbox_team(domain["domain_dir"], agent_ids=[agent["agent_id"] for agent in agents])

    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _papers_hash() == before_papers


def test_materializes_declarative_team_from_team_template(tmp_path):
    domain = _domain_only(tmp_path)

    result = materialize_sandbox_team_from_template(
        domain["domain_dir"],
        team_template=_team_template(),
    )

    team_path = Path(result["team_path"])
    manifest_path = Path(result["team_manifest_path"])
    assert team_path.is_file()
    assert manifest_path.is_file()
    assert result["team"]["team_type"] == "sandbox"
    assert result["team"]["status"] == "materialized"
    assert result["team"]["artifact_state"] == "materialized"
    assert result["team"]["source_team_template"]["team_template_id"] == (
        "sandbox_marketing_crm_automation_equipo_growth_ventas"
    )
    assert result["team"]["created_from"]["source_type"] == "team_template"
    assert [member["agent_reference"] for member in result["team"]["members"]] == [None, None]
    assert result["team"]["execution_policy"]["execution_enabled"] is False
    assert result["team"]["execution_policy"]["runtime_enabled"] is False
    assert result["team"]["execution_policy"]["tool_execution_enabled"] is False
    assert result["team"]["execution_policy"]["model_invocation_enabled"] is False
    assert result["team"]["execution_policy"]["external_integrations_enabled"] is False
    assert result["team"]["permissions"]["can_execute"] is False
    assert result["team_manifest"]["team_id"] == result["team"]["team_id"]
    assert result["team_manifest"]["domain_id"] == result["team"]["domain_id"]
    assert result["team_manifest"]["artifact_id"] == result["team"]["artifact_id"]
    assert result["team_manifest"]["materialization_id"] == result["team"]["materialization_id"]
    assert result["artifact"]["artifact_type"] == "team"
    assert result["artifact"]["created_from"]["artifact_kind"] == "sandbox_team"
    assert result["artifact"]["dependencies"] == []
    assert result["validation"]["team"]["team_id"] == result["team_id"]


def test_template_materialization_uses_tmp_sandbox_and_does_not_create_agents_or_runtime(tmp_path):
    before_agents = _tree_hash(AGENTS)
    before_domains = _tree_hash(DOMAINS)
    domain = _domain_only(tmp_path)

    result = materialize_sandbox_team_from_template(domain["domain_dir"], team_template=_team_template())
    domain_dir = Path(domain["domain_dir"])

    assert not (domain_dir / "sandbox_agents").exists()
    assert not (domain_dir / "runtime").exists()
    assert result["artifact"]["operational"] is False
    assert result["artifact"]["passed"] is False
    assert result["team"]["metadata"]["active"] is False
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(DOMAINS) == before_domains
    assert str(Path(result["team_path"]).resolve()).startswith(str(tmp_path.resolve()))


def test_template_materialization_blocks_operational_template_flags(tmp_path):
    domain = _domain_only(tmp_path)

    for field in [
        "execution_enabled",
        "runtime_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
        "can_execute",
        "can_call_tools",
        "can_call_models",
    ]:
        with pytest.raises(ValueError, match=field):
            materialize_sandbox_team_from_template(
                domain["domain_dir"],
                team_template=_team_template(**{field: True}),
                team_id=f"bad_{field}",
            )


def test_template_materialization_requires_lineage_and_ids(tmp_path):
    domain = _domain_only(tmp_path)

    for field in ["team_template_id", "descripcion"]:
        template = _team_template()
        template["team_template"].pop(field)
        with pytest.raises(ValueError, match="team_template"):
            materialize_sandbox_team_from_template(domain["domain_dir"], team_template=template)

    bad_template = _team_template()
    bad_template["artifact_type"] = "sandbox_team"
    with pytest.raises(ValueError, match="derivado"):
        materialize_sandbox_team_from_template(domain["domain_dir"], team_template=bad_template)


def test_template_materialization_blocks_operational_and_invalid_paths(tmp_path):
    domain = _domain_only(tmp_path)

    with pytest.raises(ValueError, match="domains/ operativo"):
        materialize_sandbox_team_from_template(DOMAINS, team_template=_team_template())

    with pytest.raises(FileNotFoundError):
        materialize_sandbox_team_from_template(
            tmp_path / "not_a_materialized_sandbox",
            team_template=_team_template(),
        )

    materialize_sandbox_team_from_template(domain["domain_dir"], team_template=_team_template())
    with pytest.raises(FileExistsError, match="team_id ya existe"):
        materialize_sandbox_team_from_template(domain["domain_dir"], team_template=_team_template())


def test_template_materialization_preserves_artifact_type_decision(tmp_path):
    domain = _domain_only(tmp_path)

    result = materialize_sandbox_team_from_template(domain["domain_dir"], team_template=_team_template())

    assert result["artifact"]["artifact_type"] == "team"
    assert result["team_manifest"]["artifact_type"] == "team"
    assert result["artifact"]["created_from"]["artifact_kind"] == "sandbox_team"
    assert result["team_manifest"]["artifact_kind"] == "sandbox_team"


def test_validate_materialized_team_detects_inconsistent_team_manifest(tmp_path):
    domain = _domain_only(tmp_path)
    result = materialize_sandbox_team_from_template(domain["domain_dir"], team_template=_team_template())
    manifest_path = Path(result["team_manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["team_id"] = "wrong_team"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="team_id"):
        validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])


def test_validate_materialized_team_detects_invalid_team_json(tmp_path):
    domain = _domain_only(tmp_path)
    result = materialize_sandbox_team_from_template(domain["domain_dir"], team_template=_team_template())
    team_path = Path(result["team_path"])
    team = json.loads(team_path.read_text(encoding="utf-8"))
    team["execution_policy"]["runtime_enabled"] = True
    team_path.write_text(json.dumps(team, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="runtime_enabled"):
        validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])
