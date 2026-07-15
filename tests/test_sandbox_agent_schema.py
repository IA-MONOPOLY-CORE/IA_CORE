import hashlib
import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.artifact_manifest_schema import empty_artifact_manifest, validate_artifact_manifest
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID
from core.profile_catalog_materializer import PROFILE_CATALOG_ARTIFACT_ID
from core.sandbox_agent_schema import (
    SANDBOX_AGENT_REQUIRED_DEPENDENCIES,
    build_sandbox_agent_schema,
    sandbox_agent_to_artifact_record,
    validate_sandbox_agent_schema,
)


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _agent(**overrides) -> dict:
    payload = build_sandbox_agent_schema(
        agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        profile_reference={
            "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
            "source_profile_id": "estratega_negocio_digital",
        },
        preset_reference={
            "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
            "preset_id": "sandbox_marketing_crm_automation_estratega_negocio_digital",
        },
        paper_reference={
            "paper_seed_artifact_id": PAPER_SEED_ARTIFACT_ID,
            "paper_seed_id": "paper_seed_sandbox_marketing_crm_automation_estratega_negocio_digital",
        },
        role={"role_id": "estratega"},
        specialization={"specialization_id": "negocio_digital"},
        model_policy_reference="balanced_reasoning",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def _artifact(artifact_id: str, artifact_type: str, dependencies=None):
    dependencies = list(dependencies or [])
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "name": artifact_id.replace("_", " ").title(),
        "version": "1.0.0",
        "status": "materialized",
        "created_from": {"source_type": "test"},
        "created_by": "tests/test_sandbox_agent_schema.py",
        "dependencies": dependencies,
        "created_at": "2026-07-15T00:00:00",
        "updated_at": "2026-07-15T00:00:00",
        "rollback_info": {
            "created_paths": [],
            "depends_on": dependencies,
            "safe_remove": True,
        },
    }


def test_valid_schema_passes():
    agent = _agent()

    validated = validate_sandbox_agent_schema(agent)

    assert validated["agent_id"] == "sandbox_growth_strategist"
    assert validated["dependencies"] == SANDBOX_AGENT_REQUIRED_DEPENDENCIES


def test_missing_profile_reference_fails():
    agent = _agent()
    agent.pop("profile_reference")

    with pytest.raises(ValueError, match="profile_reference"):
        validate_sandbox_agent_schema(agent)


def test_missing_preset_reference_fails():
    agent = _agent()
    agent.pop("preset_reference")

    with pytest.raises(ValueError, match="preset_reference"):
        validate_sandbox_agent_schema(agent)


def test_missing_paper_reference_fails():
    agent = _agent()
    agent.pop("paper_reference")

    with pytest.raises(ValueError, match="paper_reference"):
        validate_sandbox_agent_schema(agent)


def test_invalid_or_active_status_fails():
    with pytest.raises(ValueError, match="active"):
        validate_sandbox_agent_schema(_agent(status="active"))

    with pytest.raises(ValueError, match="status"):
        validate_sandbox_agent_schema(_agent(status="invented"))


def test_inconsistent_dependencies_fail():
    agent = _agent(dependencies=[PROFILE_CATALOG_ARTIFACT_ID])

    with pytest.raises(ValueError, match="dependencies"):
        validate_sandbox_agent_schema(agent)


def test_schema_does_not_create_real_agents():
    before = _tree_hash(AGENTS)

    build_sandbox_agent_schema(
        agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        profile_reference={
            "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
            "source_profile_id": "estratega_negocio_digital",
        },
        preset_reference={
            "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
            "preset_id": "sandbox_marketing_crm_automation_estratega_negocio_digital",
        },
        paper_reference={
            "paper_seed_artifact_id": PAPER_SEED_ARTIFACT_ID,
            "paper_seed_id": "paper_seed_sandbox_marketing_crm_automation_estratega_negocio_digital",
        },
        role={"role_id": "estratega"},
        specialization={"specialization_id": "negocio_digital"},
        model_policy_reference="balanced_reasoning",
    )

    assert _tree_hash(AGENTS) == before


def test_validation_does_not_modify_legacy_agents():
    before = _tree_hash(AGENTS)

    validate_sandbox_agent_schema(_agent())

    assert _tree_hash(AGENTS) == before


def test_serialization_is_valid_json():
    agent = _agent()

    payload = json.loads(json.dumps(agent, ensure_ascii=False))

    assert payload["schema_version"] == "1.0"
    assert payload["metadata"]["creates_agent"] is False


def test_future_artifact_manifest_compatibility():
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
        sandbox_agent_to_artifact_record(_agent(status="materialized")),
    ]

    validated = validate_artifact_manifest(manifest)

    assert validated["artifacts"][-1]["artifact_type"] == "agent"
    assert validated["artifacts"][-1]["dependencies"] == SANDBOX_AGENT_REQUIRED_DEPENDENCIES
