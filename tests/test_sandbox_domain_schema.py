import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core import domain_registry
from core.artifact_state import ArtifactState
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_state import DomainState
from core.sandbox_domain_schema import (
    SANDBOX_DOMAIN_SCHEMA_VERSION,
    is_valid_sandbox_domain,
    validate_sandbox_domain_file,
    validate_sandbox_domain_schema,
)


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"


def _domains_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in DOMAINS.rglob("*") if item.is_file()):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _valid_domain(**overrides):
    domain = {
        "schema_version": SANDBOX_DOMAIN_SCHEMA_VERSION,
        "domain_id": "sandbox_marketing_crm_automation",
        "name": "Sandbox Marketing CRM Automation",
        "description": "Dominio sandbox para validar materializacion controlada.",
        "status": DomainState.MATERIALIZED.value,
        "domain_type": "sandbox",
        "source_request": {
            "area_id": "marketing_publicidad",
            "niche_id": "contenidos_redes",
            "objective": "validar schema sandbox sin materializar dominio real",
            "business_scale": "pyme",
        },
        "created_from": {
            "type": "test_fixture",
            "source": "tests/test_sandbox_domain_schema.py",
        },
        "materialization_id": "mat_test_20260714_001",
        "materialization_status": "schema_validated",
        "artifact_state": ArtifactState.MATERIALIZED.value,
        "created_at": "2026-07-14T00:00:00",
        "updated_at": "2026-07-14T00:00:00",
        "human_review_required": True,
        "rollback_manifest": {
            "can_rollback": True,
            "created_paths": [],
            "modified_paths": [],
            "backup_paths": [],
            "notes": [],
        },
        "validation": {
            "schema": "sandbox_domain_schema",
            "schema_version": SANDBOX_DOMAIN_SCHEMA_VERSION,
            "validated": True,
            "passed": False,
            "rules": [
                "domain_state",
                "artifact_state",
                "domain_identity",
                "rollback_manifest",
            ],
        },
        "warnings": [],
        "metadata": {
            "book_prompt": "1.0",
            "operational": False,
        },
    }
    domain.update(overrides)
    return domain


def test_valid_fixture_passes():
    validated = validate_sandbox_domain_schema(_valid_domain())

    assert validated["domain_id"] == "sandbox_marketing_crm_automation"
    assert is_valid_sandbox_domain(validated) is True


def test_missing_required_fields_fail():
    domain = _valid_domain()
    domain.pop("source_request")

    with pytest.raises(ValueError, match="source_request"):
        validate_sandbox_domain_schema(domain)


def test_domain_type_must_be_sandbox():
    with pytest.raises(ValueError, match="domain_type"):
        validate_sandbox_domain_schema(_valid_domain(domain_type="production"))


def test_invalid_status_fails():
    with pytest.raises(ValueError, match="status invalido"):
        validate_sandbox_domain_schema(_valid_domain(status="unknown"))


def test_active_status_without_passed_traceability_fails():
    with pytest.raises(ValueError, match="active requiere trazabilidad PASSED"):
        validate_sandbox_domain_schema(
            _valid_domain(status="active", artifact_state="active")
        )


def test_empty_source_request_fails():
    with pytest.raises(ValueError, match="source_request"):
        validate_sandbox_domain_schema(_valid_domain(source_request={}))


def test_empty_materialization_id_fails():
    with pytest.raises(ValueError, match="materialization_id"):
        validate_sandbox_domain_schema(_valid_domain(materialization_id=""))


def test_missing_rollback_manifest_fails():
    domain = _valid_domain()
    domain.pop("rollback_manifest")

    with pytest.raises(ValueError, match="rollback_manifest"):
        validate_sandbox_domain_schema(domain)


def test_missing_human_review_required_fails():
    domain = _valid_domain()
    domain.pop("human_review_required")

    with pytest.raises(ValueError, match="human_review_required"):
        validate_sandbox_domain_schema(domain)


def test_missing_created_from_fails():
    domain = _valid_domain()
    domain.pop("created_from")

    with pytest.raises(ValueError, match="created_from"):
        validate_sandbox_domain_schema(domain)


def test_non_json_serializable_payload_fails():
    domain = _valid_domain(metadata={"bad": {"not", "json"}})

    with pytest.raises(ValueError, match="serializable"):
        validate_sandbox_domain_schema(domain)


def test_validator_does_not_write_domains_or_register_domain():
    before = _domains_hash()

    validated = validate_sandbox_domain_schema(_valid_domain())

    assert _domains_hash() == before
    assert not (DOMAINS / validated["domain_id"]).exists()
    assert validated["domain_id"] not in {
        domain["id"] for domain in domain_registry.list_domains(include_internal=True)
    }


def test_validator_respects_domain_state_contract():
    with pytest.raises(ValueError, match="artifact_state debe coincidir"):
        validate_sandbox_domain_schema(
            _valid_domain(status="materialized", artifact_state="archived")
        )


def test_validator_respects_artifact_state_contract():
    with pytest.raises(ValueError, match="artifact_state"):
        validate_sandbox_domain_schema(
            _valid_domain(status="materialized", artifact_state="ready_to_materialize")
        )


def test_legacy_cannot_pass_as_sandbox_active():
    legacy = _valid_domain(
        domain_id="loteria",
        name="Loteria / IA_CORE",
        status="active",
        artifact_state="active",
        validation={**_valid_domain()["validation"], "passed": False},
    )

    with pytest.raises(ValueError, match="active requiere trazabilidad PASSED"):
        validate_sandbox_domain_schema(legacy)


def test_fixture_file_validates_from_tmp_path(tmp_path):
    manifest_path = tmp_path / "domain.json"
    manifest_path.write_text(
        json.dumps(_valid_domain(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    validated = validate_sandbox_domain_file(manifest_path)

    assert validated["domain_type"] == "sandbox"
    assert not (DOMAINS / validated["domain_id"]).exists()


def test_real_domains_paths_in_rollback_are_blocked_for_fixture():
    domain = _valid_domain()
    domain["rollback_manifest"] = deepcopy(domain["rollback_manifest"])
    domain["rollback_manifest"]["created_paths"] = ["domains/sandbox_marketing_crm_automation"]

    with pytest.raises(ValueError, match="path operativo real"):
        validate_sandbox_domain_schema(domain)


def test_schema_accepts_metadata_from_preview_without_materializing():
    preview = build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )
    domain = _valid_domain(
        source_request=preview["domain_request"],
        created_from={
            "type": "preview",
            "preview_id": preview["preview_id"],
            "artifact_state": preview["artifact_state"],
        },
    )

    validated = validate_sandbox_domain_schema(domain)

    assert validated["created_from"]["preview_id"] == preview["preview_id"]
    assert not (DOMAINS / validated["domain_id"]).exists()
