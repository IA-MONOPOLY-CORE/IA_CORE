import json
from pathlib import Path

import pytest

from core.artifact_manifest_schema import empty_artifact_manifest, validate_artifact_manifest
from core.artifact_state import (
    ArtifactState,
    can_activate,
    is_operational,
    is_valid_transition,
    require_valid_transition,
)
from core.capability_policy_schema import build_capability_policy, validate_capability_policy
from core.domain_state import DomainState, is_domain_active, is_valid_domain_transition, restore_domain
from core.sandbox_agent_memory_contract import build_memory_contract, validate_memory_contract
from core.sandbox_agent_tool_contract import build_tool_contract, validate_tool_contract
from core.sandbox_agent_schema import validate_sandbox_agent_schema
from core.sandbox_domain_schema import validate_sandbox_domain_schema
from core.sandbox_team_schema import validate_sandbox_team_schema
from tests.test_sandbox_agent_schema import _agent, _artifact
from tests.test_sandbox_domain_schema import _valid_domain
from tests.test_sandbox_team_schema import _team


ROOT = Path(__file__).parent.parent
AUDIT_DOC = ROOT / "docs" / "STATE_TRANSITION_AUDIT_BEFORE_PROMOTION_GATE.md"


def test_artifact_states_are_compatible_with_sandbox_artifacts():
    manifest = empty_artifact_manifest("sandbox_marketing_crm_automation")
    manifest["artifacts"] = [
        _artifact("profile_catalog_main", "profile_catalog", dependencies=[]),
        _artifact(
            "agent_presets_main",
            "agent_preset",
            dependencies=["profile_catalog_main"],
        ),
    ]

    validated = validate_artifact_manifest(manifest)

    assert validated["artifacts"][0]["status"] == ArtifactState.MATERIALIZED.value
    assert is_operational(ArtifactState.MATERIALIZED) is False


def test_domain_states_do_not_contradict_artifact_states_for_sandbox():
    domain = validate_sandbox_domain_schema(_valid_domain())

    assert domain["status"] == DomainState.MATERIALIZED.value
    assert domain["artifact_state"] == ArtifactState.MATERIALIZED.value

    with pytest.raises(ValueError, match="artifact_state debe coincidir"):
        validate_sandbox_domain_schema(
            _valid_domain(
                status=DomainState.MATERIALIZED.value,
                artifact_state=ArtifactState.ARCHIVED.value,
            )
        )


def test_sandbox_agent_blocks_active():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_agent_schema(_agent(status=ArtifactState.ACTIVE.value))


def test_sandbox_team_blocks_active():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_team_schema(_team(status=ArtifactState.ACTIVE.value))


def test_capability_policy_blocks_runtime_execution_and_external_access():
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

    assert policy["runtime_enabled"] is False
    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_capability_policy({**policy, "runtime_enabled": True})
    with pytest.raises(ValueError, match="execution_allowed=false"):
        validate_capability_policy({**policy, "execution_allowed": True})
    with pytest.raises(ValueError, match="external_access=false"):
        validate_capability_policy({**policy, "external_access": True})


def test_memory_and_tool_contracts_block_runtime():
    memory = build_memory_contract(
        memory_id="memory_sandbox_growth_strategist_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        created_at="2026-07-16T00:00:00",
        updated_at="2026-07-16T00:00:00",
    )
    tool = build_tool_contract(
        tool_id="tool_sandbox_growth_strategist_declared",
        owner_agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        tool_name="Future Internal Analysis Tool",
        created_at="2026-07-16T00:00:00",
        updated_at="2026-07-16T00:00:00",
    )

    with pytest.raises(ValueError, match="runtime_enabled=false"):
        validate_memory_contract({**memory, "runtime_enabled": True})
    with pytest.raises(ValueError, match="execution_allowed=true"):
        validate_tool_contract({**tool, "execution_allowed": True})


def test_artifact_manifest_rejects_invalid_states():
    manifest = empty_artifact_manifest("sandbox_marketing_crm_automation")
    artifact = _artifact("profile_catalog_main", "profile_catalog", dependencies=[])
    artifact["status"] = "promoted"
    manifest["artifacts"] = [artifact]

    with pytest.raises(ValueError, match="status de artefacto invalido"):
        validate_artifact_manifest(manifest)


def test_no_implicit_transition_to_active_for_sandbox_contracts():
    assert is_valid_transition(ArtifactState.MATERIALIZED, ArtifactState.ACTIVE) is True
    assert can_activate(ArtifactState.MATERIALIZED, has_traceability=True) is False
    assert can_activate(ArtifactState.CANDIDATE_FOR_ACTIVATION, has_traceability=True) is True
    assert is_operational(ArtifactState.MATERIALIZED, has_traceability=True) is False

    with pytest.raises(ValueError, match="active"):
        validate_sandbox_domain_schema(
            _valid_domain(status=DomainState.ACTIVE.value, artifact_state=ArtifactState.ACTIVE.value)
        )


def test_legacy_does_not_appear_as_active():
    legacy_domain = {"id": "loteria", "legacy": True, "visible_en_hud": False}

    assert is_domain_active(legacy_domain) is False
    assert is_valid_domain_transition(DomainState.LEGACY, DomainState.ACTIVE) is False


def test_restore_domain_never_restores_directly_to_active(tmp_path):
    domain_root = tmp_path / "domains"
    domain_dir = domain_root / "sandbox_marketing_crm_automation"
    domain_dir.mkdir(parents=True)
    domain = {
        "id": "sandbox_marketing_crm_automation",
        "status": DomainState.ARCHIVED.value,
        "visible_en_hud": False,
        "traceability": {"source": "test"},
        "domain_state_history": [{"from": "materialized", "to": "archived"}],
    }
    (domain_dir / "domain.json").write_text(json.dumps(domain), encoding="utf-8")

    with pytest.raises(ValueError, match="no activa dominios"):
        restore_domain(
            "sandbox_marketing_crm_automation",
            domains_dir=domain_root,
            target_state=DomainState.ACTIVE,
        )


def test_broken_cannot_be_candidate_for_promotion_or_active():
    assert is_valid_transition(ArtifactState.BROKEN, ArtifactState.ACTIVE) is False
    with pytest.raises(ValueError, match="Transicion de artefacto invalida"):
        require_valid_transition(ArtifactState.BROKEN, ArtifactState.ACTIVE)
    assert is_valid_transition(ArtifactState.BROKEN, ArtifactState.CANDIDATE_FOR_ACTIVATION) is False


def test_archived_cannot_execute_or_be_operational():
    assert is_operational(ArtifactState.ARCHIVED, has_traceability=True) is False
    assert is_valid_transition(ArtifactState.ARCHIVED, ArtifactState.ACTIVE) is False

    team = _team(status=ArtifactState.MATERIALIZED.value)
    team["coordination_model"]["execution_enabled"] = True
    with pytest.raises(ValueError, match="execution_enabled=false"):
        validate_sandbox_team_schema(team)


def test_future_transitions_are_documented_but_not_implemented():
    text = AUDIT_DOC.read_text(encoding="utf-8")

    assert "validated" in {state.value for state in ArtifactState}
    assert "candidate_for_activation" in {state.value for state in ArtifactState}
    assert "materialized -> validated" in text
    assert "active promotion" in text
