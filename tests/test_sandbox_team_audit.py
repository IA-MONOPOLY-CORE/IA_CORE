import hashlib
import json
from pathlib import Path

import pytest

from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.sandbox_team_materializer import (
    materialize_sandbox_team_from_template,
    validate_materialized_sandbox_team,
)


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"
AUDIT_DOC = ROOT / "docs" / "SANDBOX_TEAM_AUDIT.md"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="team audit",
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


def _domain_only(tmp_path) -> dict:
    return materialize_sandbox_domain(
        _schema_from_preview(_preview()),
        sandbox_root=tmp_path / "sandboxes",
    )


def _team_template(**overrides) -> dict:
    payload = {
        "schema_version": "1.0",
        "artifact_type": "derived_professional_team_template",
        "team_template": {
            "team_template_id": "sandbox_marketing_crm_automation_equipo_growth_ventas",
            "nombre": "Equipo de growth y ventas",
            "descripcion": "Plantilla derivada para aumentar ventas y conversion.",
            "recommended_domain_profile_ids": [
                "perfil_estratega_growth",
                "perfil_especialista_conversion",
            ],
            "recommended_profile_ids": [
                "estratega_growth",
                "especialista_conversion",
            ],
            "required_team_roles": ["estratega", "especialista"],
            "expected_outputs": ["Plan comercial declarativo."],
            "generated_from": {
                "generator": "core.professional_team_template_generator",
                "profile_catalog": "derived_profile_catalog",
                "agent_presets": "derived_domain_agent_presets",
            },
            "status": "derived",
            "warnings": [],
        },
    }
    payload["team_template"].update(overrides)
    return payload


def _materialized_team(tmp_path) -> tuple[dict, dict]:
    domain = _domain_only(tmp_path)
    result = materialize_sandbox_team_from_template(
        domain["domain_dir"],
        team_template=_team_template(),
    )
    return domain, result


def _write_json(path: str | Path, payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _audit_result(result: dict) -> dict:
    team = result["team"]
    team_manifest = result["team_manifest"]
    artifact = result["artifact"]
    assert Path(result["team_path"]).is_file()
    assert Path(result["team_manifest_path"]).is_file()
    assert Path(result["artifact_manifest_path"]).is_file()
    assert team["team_id"] == team_manifest["team_id"]
    assert team["artifact_id"] == team_manifest["artifact_id"] == artifact["artifact_id"]
    assert team["domain_id"] == team_manifest["domain_id"] == result["artifact_manifest"]["domain_id"]
    assert team["materialization_id"] == team_manifest["materialization_id"]
    assert artifact["artifact_type"] == "team"
    assert artifact["created_from"]["artifact_kind"] == "sandbox_team"
    assert team_manifest["artifact_kind"] == "sandbox_team"
    assert artifact["created_from"]["source_team_template"] == team["source_team_template"]
    assert artifact["dependencies"] == team["dependencies"] == team_manifest["dependencies"]
    assert artifact["operational"] is False
    assert artifact["passed"] is False
    for member in team["members"]:
        assert member["member_id"]
        assert member["role_id"]
        assert member["role_name"]
        assert member["responsibilities"]
        assert isinstance(member["inputs"], list)
        assert isinstance(member["outputs"], list)
        assert member["status"] != "active"
        assert member["artifact_state"] != "active"
    for field in [
        "execution_enabled",
        "runtime_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ]:
        assert team["execution_policy"][field] is False
        assert team_manifest[field] is False
    for field in [
        "can_execute",
        "can_call_tools",
        "can_call_models",
        "can_write_outputs",
        "can_access_network",
        "can_use_integrations",
    ]:
        assert team["permissions"][field] is False
    return {
        "status": "SANDBOX_TEAM_AUDIT_PASSED",
        "verdict": "SANDBOX_TEAM_DECLARATIVE_NO_OPERATIONAL_CONFIRMED",
        "readiness": "ready_for_phase_5_3_internal_team_listing",
    }


def test_materialized_sandbox_team_passes_audit(tmp_path):
    _domain, result = _materialized_team(tmp_path)

    audit = _audit_result(result)
    validation = validate_materialized_sandbox_team(_domain["domain_dir"], team_id=result["team_id"])

    assert validation["success"] is True
    assert audit["status"] == "SANDBOX_TEAM_AUDIT_PASSED"
    assert audit["readiness"] == "ready_for_phase_5_3_internal_team_listing"


def test_team_manifest_and_artifact_manifest_are_coherent(tmp_path):
    _domain, result = _materialized_team(tmp_path)

    team = json.loads(Path(result["team_path"]).read_text(encoding="utf-8"))
    manifest = json.loads(Path(result["team_manifest_path"]).read_text(encoding="utf-8"))
    artifact = result["artifact_manifest"]["artifacts"][0]

    assert manifest["team_id"] == team["team_id"]
    assert manifest["created_from"]["team_template_id"] == team["source_team_template"]["team_template_id"]
    assert artifact["created_from"]["team_id"] == team["team_id"]
    assert artifact["created_from"]["materialization_id"] == team["materialization_id"]
    assert artifact["created_from"]["source_team_template"] == team["source_team_template"]
    assert artifact["dependencies"] == manifest["dependencies"] == team["dependencies"]


def test_artifact_type_team_and_artifact_kind_sandbox_team_are_unambiguous(tmp_path):
    _domain, result = _materialized_team(tmp_path)

    assert result["artifact"]["artifact_type"] == "team"
    assert result["artifact"]["created_from"]["artifact_kind"] == "sandbox_team"
    assert result["team_manifest"]["artifact_type"] == "team"
    assert result["team_manifest"]["artifact_kind"] == "sandbox_team"
    assert result["team"]["metadata"]["manifest_artifact_type"] == "team"
    assert result["team"]["metadata"]["artifact_type"] == "sandbox_team"


def test_members_are_declarative_and_null_agent_reference_creates_no_agent(tmp_path):
    before_agents = _tree_hash(AGENTS)
    domain, result = _materialized_team(tmp_path)
    domain_dir = Path(domain["domain_dir"])

    assert [member["agent_reference"] for member in result["team"]["members"]] == [None, None]
    assert not (domain_dir / "sandbox_agents").exists()
    assert result["team"]["dependencies"] == []
    assert _tree_hash(AGENTS) == before_agents


def test_operational_statuses_are_rejected_by_audit_validation(tmp_path):
    domain, result = _materialized_team(tmp_path)
    team_path = Path(result["team_path"])

    for field in ["status", "artifact_state"]:
        team = json.loads(team_path.read_text(encoding="utf-8"))
        team[field] = "active"
        _write_json(team_path, team)
        with pytest.raises(ValueError, match="active"):
            validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])
        team[field] = "materialized"
        _write_json(team_path, team)


def test_execution_policy_true_flags_are_rejected_by_audit_validation(tmp_path):
    domain, result = _materialized_team(tmp_path)
    team_path = Path(result["team_path"])

    for field in [
        "execution_enabled",
        "runtime_enabled",
        "tool_execution_enabled",
        "model_invocation_enabled",
        "external_integrations_enabled",
    ]:
        team = json.loads(team_path.read_text(encoding="utf-8"))
        team["execution_policy"][field] = True
        _write_json(team_path, team)
        with pytest.raises(ValueError, match=field):
            validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])
        team["execution_policy"][field] = False
        _write_json(team_path, team)


def test_sensitive_permissions_true_flags_are_rejected_by_audit_validation(tmp_path):
    domain, result = _materialized_team(tmp_path)
    team_path = Path(result["team_path"])

    for field in [
        "can_execute",
        "can_call_tools",
        "can_call_models",
        "can_write_outputs",
        "can_access_network",
        "can_use_integrations",
    ]:
        team = json.loads(team_path.read_text(encoding="utf-8"))
        team["permissions"][field] = True
        _write_json(team_path, team)
        with pytest.raises(ValueError, match=field):
            validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])
        team["permissions"][field] = False
        _write_json(team_path, team)


def test_missing_required_team_lineage_and_responsibilities_fail(tmp_path):
    domain, result = _materialized_team(tmp_path)
    team_path = Path(result["team_path"])

    cases = [
        ("source_team_template", lambda team: team.pop("source_team_template")),
        ("artifact_id", lambda team: team.pop("artifact_id")),
        ("responsibilities", lambda team: team["members"][0].update({"responsibilities": []})),
    ]
    for expected, mutate in cases:
        team = json.loads(team_path.read_text(encoding="utf-8"))
        mutate(team)
        _write_json(team_path, team)
        with pytest.raises(ValueError, match=expected):
            validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])
        _write_json(team_path, result["team"])


def test_missing_team_manifest_fails_for_template_materialization(tmp_path):
    domain, result = _materialized_team(tmp_path)
    Path(result["team_manifest_path"]).unlink()

    with pytest.raises(FileNotFoundError):
        validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])


def test_inconsistent_team_manifest_fails(tmp_path):
    domain, result = _materialized_team(tmp_path)
    manifest_path = Path(result["team_manifest_path"])

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifact_kind"] = "team"
    _write_json(manifest_path, manifest)

    with pytest.raises(ValueError, match="artifact_kind"):
        validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])


def test_inconsistent_artifact_manifest_fails(tmp_path):
    domain, result = _materialized_team(tmp_path)
    artifact_manifest_path = Path(result["artifact_manifest_path"])

    manifest = json.loads(artifact_manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"][0]["created_from"]["artifact_kind"] = "team"
    _write_json(artifact_manifest_path, manifest)

    with pytest.raises(ValueError, match="artifact_kind"):
        validate_materialized_sandbox_team(domain["domain_dir"], team_id=result["team_id"])


def test_materialization_does_not_create_runtime_outputs_or_touch_operational_roots(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    domain, result = _materialized_team(tmp_path)
    domain_dir = Path(domain["domain_dir"])

    assert not (domain_dir / "runtime").exists()
    assert not (domain_dir / "outputs").exists()
    assert not (domain_dir / "execution_outputs").exists()
    assert not (domain_dir / "stores").exists()
    assert not (domain_dir / "memory").exists()
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    for key in ["team_path", "team_manifest_path", "artifact_manifest_path"]:
        assert str(Path(result[key]).resolve()).startswith(str(tmp_path.resolve()))


def test_audit_document_declares_passed_non_operational_readiness():
    text = AUDIT_DOC.read_text(encoding="utf-8")

    for token in [
        "SANDBOX_TEAM_AUDIT_PASSED",
        "SANDBOX_TEAM_DECLARATIVE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_5_3_internal_team_listing",
        "artifact_type: team",
        "artifact_kind: sandbox_team",
        "No crea agentes",
        "No activa runtime",
    ]:
        assert token in text
