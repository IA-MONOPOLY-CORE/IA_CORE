import hashlib
import inspect
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import api
from core import domain_registry
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_state import (
    DomainState,
    archive_domain,
    delete_domain_safely,
    restore_domain,
)


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"


def _domains_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in DOMAINS.rglob("*") if item.is_file()):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _write_domain(root: Path, domain_id: str, *, status: str | None = None, **extra) -> dict:
    domain_dir = root / domain_id
    domain_dir.mkdir(parents=True)
    manifest = {
        "schema_version": 1,
        "id": domain_id,
        "nombre": domain_id.replace("_", " ").title(),
        "descripcion": "Fixture aislado.",
        "instrucciones": "Fixture aislado.",
        "tema_id": "corporativo",
        "creado_en": "2026-07-14T00:00:00",
        **extra,
    }
    if status is not None:
        manifest["status"] = status
    (domain_dir / "domain.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="preview_marketing_contenidos",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="growth",
        complexity_level="media",
        max_profiles=3,
        max_presets=2,
    )


def test_alternative_fixture_route_rejects_duplicate_domain_ids(tmp_path):
    domain_registry.create_domain(
        name="Auditoria de Ventas",
        description="Fixture aislado.",
        instructions="Fixture aislado.",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )

    with pytest.raises(ValueError, match="dominios duplicados"):
        domain_registry.create_domain(
            name="Auditoria de Ventas",
            description="Fixture duplicado.",
            instructions="Fixture duplicado.",
            theme_id="corporativo",
            domains_dir=tmp_path,
        )


def test_alternative_fixture_route_rejects_equivalent_domain_names(tmp_path):
    domain_registry.create_domain(
        name="Loteria",
        description="Fixture aislado.",
        instructions="Fixture aislado.",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )

    with pytest.raises(ValueError, match="dominios duplicados"):
        domain_registry.create_domain(
            name="Loteria - Analisis de Juegos de Azar",
            description="Fixture equivalente.",
            instructions="Fixture equivalente.",
            theme_id="corporativo",
            domains_dir=tmp_path,
        )


def test_list_domains_hides_non_operational_and_invalid_states_by_default(tmp_path):
    _write_domain(tmp_path, "activo", status="active")
    for state in ("legacy", "archived", "broken", "preview", "materialized", "unknown"):
        extra = {"broken_reason": "Fixture roto."} if state == "broken" else {}
        if state == "legacy":
            extra["legacy"] = True
        _write_domain(tmp_path, state, status=state, **extra)

    visible = {domain["id"] for domain in domain_registry.list_domains(tmp_path)}
    internal = {domain["id"] for domain in domain_registry.list_domains(tmp_path, include_internal=True)}

    assert visible == {"activo"}
    assert {"legacy", "archived", "broken", "preview", "materialized", "unknown"} <= internal


def test_preview_does_not_create_domain_folder_or_register_domain():
    before = _domains_hash()

    preview = _preview()

    assert _domains_hash() == before
    assert preview["creates_domain"] is False
    assert preview["modifies_domains"] is False
    assert preview["domain_request"]["domain_id"] not in {
        domain["id"] for domain in domain_registry.list_domains(include_internal=True)
    }
    assert not (DOMAINS / preview["domain_request"]["domain_id"]).exists()


def test_real_create_domain_endpoint_is_blocked_and_does_not_write_domains():
    domain_id = "bypass_prompt_0_4"
    target = DOMAINS / domain_id
    assert not target.exists()

    response = TestClient(api.app).post(
        "/api/domains/create",
        json={
            "nombre": "Bypass Prompt 0 4",
            "descripcion": "Intento de bypass.",
            "instrucciones": "No debe materializar.",
            "tema_id": "corporativo",
        },
    )

    assert response.status_code == 409
    assert "Creacion directa de dominios bloqueada" in response.json()["detail"]
    assert not target.exists()


def test_test_fixtures_do_not_leave_residue_in_real_domains(tmp_path):
    before = _domains_hash()

    domain_registry.create_domain(
        name="Fixture Temporal Seguro",
        description="Fixture aislado.",
        instructions="Fixture aislado.",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )

    assert _domains_hash() == before
    assert not (DOMAINS / "fixture_temporal_seguro").exists()


def test_legacy_domain_cannot_be_reactivated_without_formal_flow(tmp_path):
    _write_domain(tmp_path, "loteria", status="legacy", legacy=True, visible_en_hud=False)

    with pytest.raises(ValueError, match="legacy no puede pasar a active"):
        restore_domain("loteria", domains_dir=tmp_path, target_state=DomainState.ACTIVE)


def test_restore_domain_does_not_return_directly_to_active(tmp_path):
    _write_domain(tmp_path, "ventas", status="active")
    archive_domain("ventas", domains_dir=tmp_path)

    with pytest.raises(ValueError, match="restore_domain no activa dominios"):
        restore_domain("ventas", domains_dir=tmp_path, target_state=DomainState.ACTIVE)


def test_delete_domain_safely_requires_conditions(tmp_path):
    _write_domain(tmp_path, "ventas", status="active")

    with pytest.raises(ValueError, match="confirm=True"):
        delete_domain_safely("ventas", domains_dir=tmp_path)

    with pytest.raises(ValueError, match="requiere dominio archived"):
        delete_domain_safely("ventas", domains_dir=tmp_path, confirm=True)


def test_valid_documented_route_uses_central_validators():
    source = inspect.getsource(domain_registry.create_domain)

    assert "validate_domain_catalog_selection" in source
    assert "validate_unique_domain" in source
    assert "list_domains(domains_dir, include_internal=True)" in source
    assert "_load_archived_domain_records(domains_dir)" in source
