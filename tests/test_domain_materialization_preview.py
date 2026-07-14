import hashlib
import json
from pathlib import Path

import pytest

from core.artifact_state import ArtifactState
from core.domain_materialization_preview import (
    build_domain_materialization_preview,
    mark_preview_broken,
    mark_preview_ready_to_materialize,
    validate_domain_materialization_preview,
)


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"


def _domains_hash():
    files = sorted(path for path in DOMAINS.rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _preview():
    return build_domain_materialization_preview(
        domain_id="preview_marketing_contenidos",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        complexity_level="media",
        max_profiles=5,
        max_presets=4,
    )


def test_valid_preview_generates_expected_payload_shape():
    preview = _preview()

    assert preview["artifact_type"] == "domain_materialization_preview"
    assert preview["preview_id"].startswith("preview_")
    assert preview["artifact_state"] == ArtifactState.DERIVED_PREVIEW.value
    assert preview["operational"] is False
    assert preview["modifies_domains"] is False
    assert preview["creates_domain"] is False
    assert preview["creates_agents"] is False
    assert preview["creates_papers"] is False
    assert preview["creates_presets"] is False
    assert preview["domain_request"]["area_id"] == "marketing_publicidad"
    assert preview["domain_request"]["niche_ids"] == ["contenidos_redes"]
    assert preview["source"]["source_of_truth"] == "catalogs/professional_profiles.json"
    assert set(preview["derived_outputs"]) == {
        "profile_catalog",
        "agent_presets",
        "team_template",
        "model_recommendations",
        "paper_seeds",
        "end_to_end",
    }


def test_preview_payload_is_json_serializable():
    preview = _preview()

    serialized = json.dumps(preview, ensure_ascii=False, sort_keys=True)

    assert json.loads(serialized)["preview_id"] == preview["preview_id"]


def test_preview_includes_warnings_gaps_risks_and_required_actions():
    preview = _preview()

    assert isinstance(preview["warnings"], list)
    assert isinstance(preview["gaps"], list)
    assert isinstance(preview["risks"], list)
    assert preview["required_actions"]
    assert all(action["operational"] is False for action in preview["required_actions"])
    assert preview["validation_status"] in {
        "valid_preview",
        "review_recommended",
        "needs_review",
    }


def test_preview_composes_existing_derived_generators():
    preview = _preview()

    profile_catalog = preview["derived_outputs"]["profile_catalog"]["payload"]
    agent_presets = preview["derived_outputs"]["agent_presets"]["payload"]
    team_template = preview["derived_outputs"]["team_template"]["payload"]
    paper_seeds = preview["derived_outputs"]["paper_seeds"]["payload"]

    assert profile_catalog["artifact_type"] == "derived_domain_profile_catalog"
    assert profile_catalog["profiles"]
    assert agent_presets["artifact_type"] == "derived_domain_agent_presets"
    assert agent_presets["presets"]
    assert team_template["status"] == "derived"
    assert paper_seeds


def test_preview_does_not_write_domains_or_create_operational_assets():
    before = _domains_hash()

    preview = _preview()

    assert _domains_hash() == before
    assert preview["modifies_domains"] is False
    assert preview["creates_agents"] is False
    assert preview["creates_papers"] is False
    assert preview["creates_presets"] is False


def test_all_derived_outputs_are_non_operational_preview_wrappers():
    preview = _preview()

    for output in preview["derived_outputs"].values():
        assert output["artifact_state"] == ArtifactState.DERIVED_PREVIEW.value
        assert output["operational"] is False
        assert output["payload"]


def test_invalid_preview_state_fails():
    preview = _preview()
    preview["artifact_state"] = ArtifactState.ACTIVE.value

    with pytest.raises(ValueError, match="estado de preview invalido"):
        validate_domain_materialization_preview(preview)


def test_missing_traceability_fails():
    preview = _preview()
    preview["source"] = {}

    with pytest.raises(ValueError, match="origen trazable"):
        validate_domain_materialization_preview(preview)


def test_operational_flags_fail_validation():
    preview = _preview()
    preview["creates_agents"] = True

    with pytest.raises(ValueError, match="creates_agents"):
        validate_domain_materialization_preview(preview)


def test_preview_can_be_marked_ready_without_becoming_operational():
    preview = _preview()

    ready = mark_preview_ready_to_materialize(preview)

    assert ready["artifact_state"] == ArtifactState.READY_TO_MATERIALIZE.value
    assert ready["validation_status"] == "ready_to_materialize"
    assert ready["operational"] is False
    assert ready["modifies_domains"] is False


def test_preview_can_be_marked_broken_with_reason():
    preview = _preview()

    broken = mark_preview_broken(preview, reason="Falta aprobacion humana")

    assert broken["artifact_state"] == ArtifactState.BROKEN.value
    assert broken["validation_status"] == "broken"
    assert any(gap.get("type") == "broken_preview" for gap in broken["gaps"])
