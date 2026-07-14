import json
from pathlib import Path

import pytest

from core.domain_registry import list_domains
from core.domain_state import (
    DOMAIN_STATE_DESCRIPTIONS,
    VALID_DOMAIN_TRANSITIONS,
    DomainState,
    archive_domain,
    delete_domain_safely,
    is_domain_active,
    is_domain_visible_as_active,
    is_valid_domain_transition,
    reset_domain,
    restore_domain,
    validate_domain_state,
)


ROOT = Path(__file__).parent.parent


def _write_domain(root: Path, domain_id: str, **overrides):
    domain_dir = root / domain_id
    (domain_dir / "agents" / "config").mkdir(parents=True)
    (domain_dir / "agents" / "papers").mkdir(parents=True)
    manifest = {
        "schema_version": 1,
        "id": domain_id,
        "nombre": domain_id.replace("_", " ").title(),
        "descripcion": "Dominio de test.",
        "instrucciones": "Instrucciones de test.",
        "tema_id": "corporativo",
        "creado_en": "2026-07-13T00:00:00",
        **overrides,
    }
    (domain_dir / "domain.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def _load(root: Path, domain_id: str):
    return json.loads((root / domain_id / "domain.json").read_text(encoding="utf-8"))


def test_domain_states_are_defined_and_documented():
    assert {state.value for state in DomainState} == {
        "empty",
        "draft",
        "preview",
        "materialized",
        "active",
        "archived",
        "legacy",
        "broken",
    }
    assert set(DOMAIN_STATE_DESCRIPTIONS) == set(DomainState)
    assert all(description for description in DOMAIN_STATE_DESCRIPTIONS.values())


def test_validate_domain_state_accepts_valid_states(tmp_path):
    for state in DomainState:
        extras = {"status": state.value, "visible_en_hud": False}
        if state is DomainState.ACTIVE:
            extras["visible_en_hud"] = True
        if state is DomainState.LEGACY:
            extras["legacy"] = True
        if state is DomainState.BROKEN:
            extras["broken_reason"] = "schema invalido"
        domain = _write_domain(tmp_path, f"domain_{state.value}", **extras)

        assert validate_domain_state(domain) is state


def test_validate_domain_state_rejects_invalid_state():
    domain = {
        "id": "x",
        "nombre": "X",
        "status": "proposed",
        "creado_en": "2026-07-13T00:00:00",
    }

    with pytest.raises(ValueError, match="Estado de dominio invalido"):
        validate_domain_state(domain)


def test_non_active_states_cannot_be_visible_as_active():
    domain = {
        "id": "archivo",
        "nombre": "Archivo",
        "status": "archived",
        "visible_en_hud": True,
        "creado_en": "2026-07-13T00:00:00",
    }

    with pytest.raises(ValueError, match="no puede estar visible"):
        validate_domain_state(domain)


def test_legacy_cannot_transition_directly_to_active():
    assert not is_valid_domain_transition(DomainState.LEGACY, DomainState.ACTIVE)


def test_archive_domain_retires_from_active_flow_without_deleting(tmp_path):
    _write_domain(tmp_path, "ventas", status="active", visible_en_hud=True)

    archived = archive_domain("ventas", domains_dir=tmp_path, reason="Cierre controlado")

    assert archived["status"] == "archived"
    assert archived["visible_en_hud"] is False
    assert archived["archived"] is True
    assert (tmp_path / "ventas" / "domain.json").exists()
    assert list_domains(tmp_path) == []
    assert list_domains(tmp_path, include_internal=True)[0]["id"] == "ventas"


def test_restore_domain_returns_archived_domain_to_materialized_not_active(tmp_path):
    _write_domain(tmp_path, "ventas", status="active", visible_en_hud=True)
    archive_domain("ventas", domains_dir=tmp_path)

    restored = restore_domain("ventas", domains_dir=tmp_path)

    assert restored["status"] == "materialized"
    assert restored["visible_en_hud"] is False
    assert not is_domain_visible_as_active(restored)
    assert list_domains(tmp_path) == []


def test_restore_domain_refuses_direct_active_restore(tmp_path):
    _write_domain(tmp_path, "ventas", status="active", visible_en_hud=True)
    archive_domain("ventas", domains_dir=tmp_path)

    with pytest.raises(ValueError, match="no activa dominios"):
        restore_domain("ventas", domains_dir=tmp_path, target_state=DomainState.ACTIVE)


def test_reset_domain_keeps_manifest_and_moves_to_empty(tmp_path):
    _write_domain(tmp_path, "ventas", status="materialized", visible_en_hud=False)

    reset = reset_domain("ventas", domains_dir=tmp_path)

    assert reset["status"] == "empty"
    assert reset["visible_en_hud"] is False
    assert (tmp_path / "ventas" / "domain.json").exists()
    assert reset["domain_state_history"][-1]["to"] == "empty"


def test_delete_domain_safely_requires_archived_and_confirmation(tmp_path):
    _write_domain(tmp_path, "ventas", status="active", visible_en_hud=True)

    with pytest.raises(ValueError, match="confirm=True"):
        delete_domain_safely("ventas", domains_dir=tmp_path)
    with pytest.raises(ValueError, match="requiere dominio archived"):
        delete_domain_safely("ventas", domains_dir=tmp_path, confirm=True)

    archive_domain("ventas", domains_dir=tmp_path)
    deleted = delete_domain_safely("ventas", domains_dir=tmp_path, confirm=True)

    assert deleted["deleted"] is True
    assert not (tmp_path / "ventas").exists()


def test_delete_domain_safely_never_deletes_legacy(tmp_path):
    _write_domain(
        tmp_path,
        "loteria",
        status="legacy",
        legacy=True,
        visible_en_hud=False,
    )

    with pytest.raises(ValueError, match="legacy"):
        delete_domain_safely("loteria", domains_dir=tmp_path, confirm=True)
    assert (tmp_path / "loteria" / "domain.json").exists()


def test_validate_domain_state_detects_broken_without_reason():
    domain = {
        "id": "roto",
        "nombre": "Roto",
        "status": "broken",
        "visible_en_hud": False,
        "creado_en": "2026-07-13T00:00:00",
    }

    with pytest.raises(ValueError, match="broken_reason"):
        validate_domain_state(domain)


def test_archived_and_legacy_domains_do_not_appear_active(tmp_path):
    _write_domain(tmp_path, "activo", status="active", visible_en_hud=True)
    _write_domain(tmp_path, "archivo", status="archived", visible_en_hud=False)
    _write_domain(tmp_path, "legacy", status="legacy", legacy=True, visible_en_hud=False)

    assert [domain["id"] for domain in list_domains(tmp_path)] == ["activo"]
    assert {domain["id"] for domain in list_domains(tmp_path, include_internal=True)} == {
        "activo",
        "archivo",
        "legacy",
    }


def test_loteria_legacy_domain_is_not_active_in_repo():
    domain = json.loads((ROOT / "domains" / "loteria" / "domain.json").read_text(encoding="utf-8"))

    assert validate_domain_state(domain) is DomainState.LEGACY
    assert not is_domain_active(domain)
    assert not is_domain_visible_as_active(domain)


def test_expected_transitions_are_declared():
    assert DomainState.ACTIVE in VALID_DOMAIN_TRANSITIONS[DomainState.MATERIALIZED]
    assert DomainState.ARCHIVED in VALID_DOMAIN_TRANSITIONS[DomainState.ACTIVE]
    assert DomainState.MATERIALIZED in VALID_DOMAIN_TRANSITIONS[DomainState.ARCHIVED]
    assert DomainState.ACTIVE not in VALID_DOMAIN_TRANSITIONS[DomainState.LEGACY]
