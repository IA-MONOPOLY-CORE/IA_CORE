import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.sandbox_team_materializer import materialize_sandbox_team_from_template
from core.sandbox_team_read_model import (
    READ_MODEL_READINESS,
    READ_MODEL_VERDICT,
    TEAM_LISTABLE_READINESS,
    get_sandbox_team_summary,
    list_sandbox_teams,
    validate_sandbox_team_read_model,
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


def _snapshot_tree(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="team read model",
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
            "generated_from": {"generator": "core.professional_team_template_generator"},
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


def _dumped(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).lower()


def test_materialized_sandbox_team_appears_in_internal_listing(tmp_path):
    domain, result = _materialized_team(tmp_path)

    listing = list_sandbox_teams(domain["domain_dir"])

    assert listing["status"] == "listed"
    assert listing["verdict"] == READ_MODEL_VERDICT
    assert listing["readiness"] == READ_MODEL_READINESS
    assert listing["teams_count"] == 1
    assert listing["teams"][0]["team_id"] == result["team_id"]
    assert listing["teams"][0]["domain_id"] == domain["domain_id"]


def test_payload_is_json_safe_and_has_required_ids(tmp_path):
    domain, result = _materialized_team(tmp_path)

    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])
    encoded = json.dumps(summary, ensure_ascii=False, sort_keys=True)

    assert encoded
    assert summary["team_id"]
    assert summary["domain_id"]
    assert summary["artifact_id"]
    assert summary["materialization_id"]
    assert summary["created_at"]
    assert summary["updated_at"]


def test_artifact_type_and_kind_are_represented_without_ambiguity(tmp_path):
    domain, result = _materialized_team(tmp_path)

    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])

    assert summary["artifact_type"] == "team"
    assert summary["artifact_kind"] == "sandbox_team"
    assert summary["metadata"]["artifact_type"] == "sandbox_team"
    assert summary["metadata"]["manifest_artifact_type"] == "team"


def test_members_summary_is_declarative_and_compact(tmp_path):
    domain, result = _materialized_team(tmp_path)

    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])

    assert summary["members_count"] == len(summary["members_summary"]) == 2
    for member in summary["members_summary"]:
        assert set(member) == {
            "member_id",
            "role_id",
            "role_name",
            "specialization_id",
            "specialization_name",
            "has_agent_reference",
            "responsibilities_count",
            "status",
            "artifact_state",
        }
        assert member["has_agent_reference"] is False
        assert member["responsibilities_count"] == 1
        assert "responsibilities" not in member
        assert "agent_reference" not in member


def test_permissions_and_execution_policy_summaries_are_default_deny(tmp_path):
    domain, result = _materialized_team(tmp_path)

    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])

    assert summary["permissions_summary"] == {
        "can_access_network": False,
        "can_call_models": False,
        "can_call_tools": False,
        "can_execute": False,
        "can_use_integrations": False,
        "can_write_outputs": False,
    }
    assert summary["execution_policy_summary"] == {
        "execution_enabled": False,
        "runtime_enabled": False,
        "tool_execution_enabled": False,
        "model_invocation_enabled": False,
        "external_integrations_enabled": False,
        "human_approval_required": True,
    }


def test_readiness_and_flags_do_not_suggest_real_operation(tmp_path):
    domain, result = _materialized_team(tmp_path)

    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])

    assert summary["operational"] is False
    assert summary["passed"] is False
    assert summary["readiness"] == TEAM_LISTABLE_READINESS
    assert "ready_for_runtime" not in summary["readiness"]
    assert "ready_for_execution" not in summary["readiness"]


@pytest.mark.parametrize("field", ["execution_enabled", "runtime_enabled"])
def test_operational_execution_flags_fail_controlled(tmp_path, field):
    domain, result = _materialized_team(tmp_path)
    team_path = Path(result["team_path"])
    team = json.loads(team_path.read_text(encoding="utf-8"))
    team["execution_policy"][field] = True
    _write_json(team_path, team)

    with pytest.raises(ValueError, match=field):
        list_sandbox_teams(domain["domain_dir"])


def test_sensitive_permission_true_fails_controlled(tmp_path):
    domain, result = _materialized_team(tmp_path)
    team_path = Path(result["team_path"])
    team = json.loads(team_path.read_text(encoding="utf-8"))
    team["permissions"]["can_execute"] = True
    _write_json(team_path, team)

    with pytest.raises(ValueError, match="can_execute"):
        get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])


def test_missing_or_inconsistent_artifact_manifest_fails(tmp_path):
    domain, result = _materialized_team(tmp_path)
    artifact_manifest_path = Path(result["artifact_manifest_path"])
    artifact_manifest_path.unlink()
    with pytest.raises(FileNotFoundError):
        list_sandbox_teams(domain["domain_dir"])

    _write_json(artifact_manifest_path, result["artifact_manifest"])
    manifest = json.loads(artifact_manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"][0]["created_from"]["artifact_kind"] = "team"
    _write_json(artifact_manifest_path, manifest)
    with pytest.raises(ValueError, match="artifact_kind"):
        list_sandbox_teams(domain["domain_dir"])


def test_read_model_payload_does_not_expose_sensitive_or_runtime_config(tmp_path):
    domain, result = _materialized_team(tmp_path)

    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])
    dumped = _dumped(summary)

    for forbidden in [
        "api_key",
        "secret",
        "token",
        "password",
        "credential",
        "runtime_handle",
        "tool_config",
        "model_config",
        "member_agents",
        "raw_prompt",
    ]:
        assert forbidden not in dumped
    assert '"agent_reference"' not in dumped
    assert '"has_agent_reference"' in dumped


def test_listing_is_read_only_and_creates_no_artifacts(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    domain, result = _materialized_team(tmp_path)
    domain_dir = Path(domain["domain_dir"])
    before_sandbox = _snapshot_tree(domain_dir)

    list_sandbox_teams(domain["domain_dir"])
    get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])

    assert _snapshot_tree(domain_dir) == before_sandbox
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    assert not (domain_dir / "runtime").exists()
    assert not (domain_dir / "sandbox_agents").exists()
    assert not (domain_dir / "outputs").exists()


def test_listing_blocks_operational_domains_root(tmp_path):
    with pytest.raises(ValueError, match="domains/ operativo"):
        list_sandbox_teams(DOMAINS)


def test_validate_sandbox_team_read_model_detects_broken_payload(tmp_path):
    domain, result = _materialized_team(tmp_path)
    summary = get_sandbox_team_summary(domain["domain_dir"], team_id=result["team_id"])

    broken = deepcopy(summary)
    broken["operational"] = True
    with pytest.raises(ValueError, match="operational"):
        validate_sandbox_team_read_model(broken)

    broken = deepcopy(summary)
    broken["members_count"] = 99
    with pytest.raises(ValueError, match="members_count"):
        validate_sandbox_team_read_model(broken)

    broken = deepcopy(summary)
    broken["metadata"]["api_key"] = "nope"
    with pytest.raises(ValueError, match="api_key"):
        validate_sandbox_team_read_model(broken)


def test_future_ui_can_consume_without_critical_logic_or_actions(tmp_path):
    domain, result = _materialized_team(tmp_path)

    listing = list_sandbox_teams(domain["domain_dir"])
    ui_payload = listing["teams"][0]

    assert ui_payload["name"]
    assert ui_payload["status"] == "materialized"
    assert ui_payload["source_team_template"]["team_template_id"]
    assert ui_payload["members_summary"]
    assert ui_payload["readiness"] == TEAM_LISTABLE_READINESS
    for forbidden_action in ["activate", "execute", "materialize", "mutate", "endpoint", "integration"]:
        assert forbidden_action not in ui_payload


def test_listing_leaves_no_artifacts_outside_tmp_path(tmp_path):
    domain, result = _materialized_team(tmp_path)

    listing = list_sandbox_teams(domain["domain_dir"])

    assert str(Path(listing["domain_dir"]).resolve()).startswith(str(tmp_path.resolve()))
    assert str(Path(result["team_path"]).resolve()).startswith(str(tmp_path.resolve()))
