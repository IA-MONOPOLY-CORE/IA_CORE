import hashlib
from pathlib import Path

import pytest

from core.agent_lineage_schema import (
    build_agent_lineage,
    lineage_to_artifact_manifest_metadata,
    validate_agent_lineage,
)
from core.agent_preset_materializer import AGENT_PRESETS_ARTIFACT_ID
from core.artifact_manifest_schema import empty_artifact_manifest, validate_artifact_manifest
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID
from core.profile_catalog_materializer import PROFILE_CATALOG_ARTIFACT_ID
from core.sandbox_agent_schema import SANDBOX_AGENT_REQUIRED_DEPENDENCIES, sandbox_agent_to_artifact_record
from tests.test_sandbox_agent_schema import _agent, _artifact


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _origin(**overrides) -> dict:
    origin = {
        "profile_catalog_artifact_id": PROFILE_CATALOG_ARTIFACT_ID,
        "source_profile_id": "estratega_negocio_digital",
        "agent_presets_artifact_id": AGENT_PRESETS_ARTIFACT_ID,
        "preset_id": "sandbox_marketing_crm_automation_estratega_negocio_digital",
        "paper_seed_artifact_id": PAPER_SEED_ARTIFACT_ID,
        "paper_seed_id": "paper_seed_sandbox_marketing_crm_automation_estratega_negocio_digital",
    }
    origin.update(overrides)
    return origin


def _lineage(**overrides) -> dict:
    payload = build_agent_lineage(
        agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        origin=_origin(),
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    payload.update(overrides)
    return payload


def test_valid_lineage_passes():
    lineage = _lineage()

    validated = validate_agent_lineage(lineage)

    assert validated["agent_id"] == "sandbox_growth_strategist"
    assert validated["origin"]["source_profile_id"] == "estratega_negocio_digital"


def test_origin_must_be_complete():
    lineage = _lineage(origin=_origin(paper_seed_id=""))

    with pytest.raises(ValueError, match="paper_seed_id"):
        validate_agent_lineage(lineage)


def test_broken_references_fail():
    lineage = _lineage(origin=_origin(profile_catalog_artifact_id="wrong"))

    with pytest.raises(ValueError, match="profile_catalog"):
        validate_agent_lineage(lineage)


def test_history_must_be_valid_and_contain_current_version():
    lineage = _lineage(
        current_version="1.0.1",
        history=[
            {
                "event": "regenerated",
                "version": "1.0.0",
                "at": "2026-07-15T00:00:00",
            }
        ],
    )

    with pytest.raises(ValueError, match="current_version"):
        validate_agent_lineage(lineage)


def test_replacement_is_traceable():
    lineage = _lineage(replaced_by="sandbox_growth_strategist_v2")

    validated = validate_agent_lineage(lineage)

    assert validated["replaced_by"] == "sandbox_growth_strategist_v2"


def test_replacement_cannot_point_to_self():
    lineage = _lineage(replaced_by="sandbox_growth_strategist")

    with pytest.raises(ValueError, match="replaced_by"):
        validate_agent_lineage(lineage)


def test_compatibility_with_artifact_manifest():
    manifest = empty_artifact_manifest("sandbox_marketing_crm_automation")
    agent = _agent(status="materialized")
    agent_artifact = sandbox_agent_to_artifact_record(agent)
    agent_artifact["created_from"]["lineage"] = lineage_to_artifact_manifest_metadata(_lineage())
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
        agent_artifact,
    ]

    validated = validate_artifact_manifest(manifest)

    lineage_meta = validated["artifacts"][-1]["created_from"]["lineage"]
    assert lineage_meta["dependencies"] == SANDBOX_AGENT_REQUIRED_DEPENDENCIES
    assert lineage_meta["history_event_count"] == 1


def test_lineage_does_not_create_real_agents():
    before = _tree_hash(AGENTS)

    build_agent_lineage(
        agent_id="sandbox_growth_strategist",
        domain_id="sandbox_marketing_crm_automation",
        origin=_origin(),
    )

    assert _tree_hash(AGENTS) == before
