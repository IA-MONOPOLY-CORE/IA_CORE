import json
from pathlib import Path

from fastapi.testclient import TestClient

import api
from core import domain_registry


ROOT = Path(__file__).parent.parent
LEGACY_DOMAINS = ROOT / "docs" / "legacy" / "domains"
OLD_DOMAIN = ROOT / "domains" / "loteria"
UI_CREATED_DOMAIN = ROOT / "domains" / "loteria_analisis_de_juegos_de_azar"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_domain_cleanup_manifest_and_snapshots_exist():
    expected = [
        LEGACY_DOMAINS / "loteria_domain_cleanup_manifest.md",
        LEGACY_DOMAINS / "loteria_domain_inventory.md",
        LEGACY_DOMAINS / "loteria_legacy_domain_snapshot.json",
        LEGACY_DOMAINS / "loteria_ui_created_domain_snapshot.json",
    ]

    assert [path for path in expected if not path.exists()] == []


def test_old_loteria_domain_is_legacy_not_active():
    domain = _load(OLD_DOMAIN / "domain.json")

    assert domain["id"] == "loteria"
    assert domain["nombre"] == "Loteria / IA_CORE"
    assert domain["visible_en_hud"] is False
    assert domain["status"] == "legacy"
    assert domain["legacy"] is True


def test_ui_created_loteria_domain_is_not_operational_folder():
    assert not UI_CREATED_DOMAIN.exists()


def test_loteria_domains_are_not_in_active_registry():
    active_ids = {domain["id"] for domain in domain_registry.list_domains()}
    active_names = {domain["nombre"] for domain in domain_registry.list_domains()}

    assert "loteria" not in active_ids
    assert "loteria_analisis_de_juegos_de_azar" not in active_ids
    assert "Loteria / IA_CORE" not in active_names
    assert "Lotería — Análisis de Juegos de Azar" not in active_names


def test_loteria_domains_are_not_returned_to_ui_selector():
    payload = TestClient(api.app).get("/api/domains/list").json()
    domain_ids = {domain["id"] for domain in payload["domains"]}
    names = {domain["nombre"] for domain in payload["domains"]}

    assert payload["success"] is True
    assert "loteria" not in domain_ids
    assert "loteria_analisis_de_juegos_de_azar" not in domain_ids
    assert "Loteria / IA_CORE" not in names
    assert "Lotería — Análisis de Juegos de Azar" not in names


def test_no_active_orphan_assets_for_cleaned_loteria_domains():
    assert list((OLD_DOMAIN / "agents" / "config").glob("*.json")) == []
    assert list((OLD_DOMAIN / "agents" / "papers").glob("*.json")) == []
    assert not UI_CREATED_DOMAIN.exists()


def test_other_domain_folders_were_not_removed():
    assert (ROOT / "domains" / "demo_generico" / "domain.json").exists()
    assert (ROOT / "domains" / "codex_qa_prompt_2_20260707").exists()


def test_ui_created_domain_snapshot_preserves_original_manifest():
    snapshot = _load(LEGACY_DOMAINS / "loteria_ui_created_domain_snapshot.json")

    assert snapshot["id"] == "loteria_analisis_de_juegos_de_azar"
    assert snapshot["area_profesional_id"] == "oficios_otros"
    assert snapshot["nicho_id"] == "analisis_loteria_juegos_azar"
