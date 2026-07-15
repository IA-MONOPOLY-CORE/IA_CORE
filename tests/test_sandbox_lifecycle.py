import hashlib
import json
from pathlib import Path

import pytest

from core import domain_registry
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materialization_rollback import rollback_domain_materialization
from core.sandbox_lifecycle_validation import (
    regenerate_sandbox_domain,
    validate_sandbox_lifecycle,
)


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"


def _domains_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in DOMAINS.rglob("*") if item.is_file()):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )


def _schema_from_preview(preview: dict, **overrides) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    schema.update(overrides)
    return schema


def test_preview_valid_starts_lifecycle(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview)

    result = validate_sandbox_lifecycle(
        preview=preview,
        domain_schema=schema,
        sandbox_root=tmp_path / "sandboxes",
    )

    assert result["success"] is True
    assert result["preview_id"] == preview["preview_id"]
    assert result["clean"] is True


def test_materialization_and_post_validation_are_correct(tmp_path):
    preview = _preview()
    result = validate_sandbox_lifecycle(
        preview=preview,
        domain_schema=_schema_from_preview(preview),
        sandbox_root=tmp_path / "sandboxes",
        cleanup=False,
    )

    materialization = result["materialization"]
    assert Path(materialization["domain_json_path"]).is_file()
    assert Path(materialization["manifest_path"]).is_file()
    assert result["post_validation"]["success"] is True
    assert result["post_validation"]["domain"]["status"] == "materialized"
    rollback_domain_materialization(manifest_path=materialization["manifest_path"])


def test_rollback_returns_to_clean_state(tmp_path):
    preview = _preview()
    result = validate_sandbox_lifecycle(
        preview=preview,
        domain_schema=_schema_from_preview(preview),
        sandbox_root=tmp_path / "sandboxes",
    )

    assert result["rollback"]["status"] == "rolled_back"
    assert not Path(result["materialization"]["domain_dir"]).exists()


def test_regeneration_rolls_back_existing_and_creates_new_generation(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview)
    root = tmp_path / "sandboxes"
    first = validate_sandbox_lifecycle(
        preview=preview,
        domain_schema=schema,
        sandbox_root=root,
        cleanup=False,
    )["materialization"]

    regenerated = regenerate_sandbox_domain(schema, sandbox_root=root)

    assert regenerated["previous_materialization_id"] == first["materialization_id"]
    assert regenerated["materialization_id"] != first["materialization_id"]
    assert regenerated["generation_number"] == 2
    assert regenerated["rollback"]["status"] == "rolled_back"
    assert Path(regenerated["materialization"]["domain_dir"]).is_dir()


def test_second_regeneration_does_not_create_duplicates_and_keeps_history(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview)
    root = tmp_path / "sandboxes"
    validate_sandbox_lifecycle(preview=preview, domain_schema=schema, sandbox_root=root, cleanup=False)
    second = regenerate_sandbox_domain(schema, sandbox_root=root)
    third = regenerate_sandbox_domain(schema, sandbox_root=root)

    assert third["generation_number"] == 3
    assert third["materialization_id"] != second["materialization_id"]
    assert third["previous_materialization_id"] == second["materialization_id"]
    events = [item["event"] for item in third["history"]]
    assert events.count("materialized") == 3
    assert events.count("rolled_back") == 2
    assert len(list(root.glob("*/domain.json"))) == 1


def test_lifecycle_never_touches_domains_or_legacy(tmp_path):
    before = _domains_hash()
    preview = _preview()
    schema = _schema_from_preview(preview)
    root = tmp_path / "sandboxes"

    validate_sandbox_lifecycle(preview=preview, domain_schema=schema, sandbox_root=root)

    assert _domains_hash() == before
    assert (DOMAINS / "loteria").exists()
    assert schema["domain_id"] not in {
        domain["id"] for domain in domain_registry.list_domains(include_internal=True)
    }


def test_lifecycle_leaves_no_temporary_residue_after_cleanup(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview)
    root = tmp_path / "sandboxes"

    result = validate_sandbox_lifecycle(preview=preview, domain_schema=schema, sandbox_root=root)

    assert not Path(result["materialization"]["domain_dir"]).exists()
    assert list((root / "_rollback_records").glob("*.json"))
    assert not list(root.glob("*/domain.json"))


def test_final_states_are_not_active(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview)
    regenerated = regenerate_sandbox_domain(schema, sandbox_root=tmp_path / "sandboxes")

    domain = regenerated["post_validation"]["domain"]
    assert domain["status"] == "materialized"
    assert domain["artifact_state"] == "materialized"
    assert domain["validation"]["passed"] is False


def test_corrupt_manifest_fails_regeneration_controlled(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview)
    root = tmp_path / "sandboxes"
    domain_dir = root / schema["domain_id"]
    domain_dir.mkdir(parents=True)
    (domain_dir / "materialization_manifest.json").write_text("{ not json", encoding="utf-8")

    with pytest.raises(ValueError, match="Manifest corrupto"):
        regenerate_sandbox_domain(schema, sandbox_root=root)


def test_invalid_schema_fails_before_materialization(tmp_path):
    preview = _preview()
    schema = _schema_from_preview(preview, source_request={})

    with pytest.raises(ValueError, match="source_request"):
        validate_sandbox_lifecycle(
            preview=preview,
            domain_schema=schema,
            sandbox_root=tmp_path / "sandboxes",
        )

    assert not (tmp_path / "sandboxes").exists()
