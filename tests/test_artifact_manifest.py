import hashlib
from pathlib import Path

import pytest

from core.artifact_manifest_schema import (
    ALLOWED_ARTIFACT_TYPES,
    empty_artifact_manifest,
    validate_artifact_manifest,
)


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"


def _domains_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in DOMAINS.rglob("*") if item.is_file()):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _artifact(artifact_id: str, artifact_type: str, *, dependencies=None, rollback_depends=None):
    dependencies = list(dependencies or [])
    rollback_depends = list(rollback_depends if rollback_depends is not None else dependencies)
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "name": artifact_id.replace("_", " ").title(),
        "version": "1.0.0",
        "status": "materialized",
        "created_from": {
            "source_type": "sandbox_materialization",
            "materialization_id": "mat_test",
        },
        "created_by": "tests/test_artifact_manifest.py",
        "dependencies": dependencies,
        "created_at": "2026-07-15T00:00:00",
        "updated_at": "2026-07-15T00:00:00",
        "rollback_info": {
            "created_paths": [],
            "depends_on": rollback_depends,
            "safe_remove": True,
        },
    }


def _manifest(*artifacts):
    return {
        "artifact_manifest_version": "1.0",
        "domain_id": "sandbox_marketing_crm_automation",
        "artifacts": list(artifacts),
    }


def test_empty_manifest_is_valid():
    manifest = empty_artifact_manifest("sandbox_marketing_crm_automation")

    validated = validate_artifact_manifest(manifest)

    assert validated["artifacts"] == []


def test_valid_artifact_passes():
    artifact = _artifact("profile_catalog_main", "profile_catalog")

    validated = validate_artifact_manifest(_manifest(artifact))

    assert validated["artifacts"][0]["artifact_id"] == "profile_catalog_main"


def test_missing_artifact_id_fails():
    artifact = _artifact("profile_catalog_main", "profile_catalog")
    artifact.pop("artifact_id")

    with pytest.raises(ValueError, match="artifact_id"):
        validate_artifact_manifest(_manifest(artifact))


def test_invalid_artifact_type_fails():
    artifact = _artifact("unknown_artifact", "unknown")

    with pytest.raises(ValueError, match="artifact_type invalido"):
        validate_artifact_manifest(_manifest(artifact))


def test_invalid_status_fails():
    artifact = _artifact("profile_catalog_main", "profile_catalog")
    artifact["status"] = "invented"

    with pytest.raises(ValueError, match="status de artefacto invalido"):
        validate_artifact_manifest(_manifest(artifact))


def test_missing_dependency_fails():
    preset = _artifact("sales_agent_preset", "agent_preset", dependencies=["missing_catalog"])

    with pytest.raises(ValueError, match="dependencia inexistente"):
        validate_artifact_manifest(_manifest(preset))


def test_missing_rollback_info_fails():
    artifact = _artifact("profile_catalog_main", "profile_catalog")
    artifact.pop("rollback_info")

    with pytest.raises(ValueError, match="rollback_info"):
        validate_artifact_manifest(_manifest(artifact))


def test_validator_does_not_create_artifacts_or_write_domains():
    before = _domains_hash()

    validate_artifact_manifest(_manifest(_artifact("profile_catalog_main", "profile_catalog")))

    assert _domains_hash() == before
    assert not (DOMAINS / "sandbox_marketing_crm_automation" / "profile_catalog").exists()


def test_allowed_artifact_types_are_declared():
    assert ALLOWED_ARTIFACT_TYPES == {
        "profile_catalog",
        "agent_preset",
        "paper_seed",
        "agent",
        "team",
        "memory",
        "model_recommendation",
    }


def test_future_dependency_chain_can_be_represented():
    profile_catalog = _artifact("profile_catalog_main", "profile_catalog")
    preset = _artifact(
        "customer_support_preset",
        "agent_preset",
        dependencies=["profile_catalog_main"],
    )
    agent = _artifact(
        "customer_support_agent",
        "agent",
        dependencies=["customer_support_preset"],
    )
    team = _artifact(
        "support_team",
        "team",
        dependencies=["customer_support_agent"],
    )

    validated = validate_artifact_manifest(_manifest(profile_catalog, preset, agent, team))

    assert [item["artifact_id"] for item in validated["artifacts"]] == [
        "profile_catalog_main",
        "customer_support_preset",
        "customer_support_agent",
        "support_team",
    ]
