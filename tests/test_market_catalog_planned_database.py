import subprocess
from pathlib import Path

from core.market_catalog import (
    MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED,
    MARKET_CATALOG_RUNTIME_ENABLED,
    MARKET_CATALOG_STATUS,
    MARKET_CATALOG_UI_ENABLED,
)
from core.market_catalog.loader import find_market_by_normalized_name, get_market_by_id, list_markets, load_market_catalog
from core.market_catalog.schema import ACTIVATION_STATUS, EMPTY_MAPPING_FIELDS, validate_market_catalog_entry


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"
FORBIDDEN_PATHS = [
    "core/backend_read_model_store.py",
    "core/backend_status_api.py",
    "core/backend_dashboard_adapter.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
    "ui/market_catalog",
    "runtime/market_catalog",
]


def _catalog():
    return load_market_catalog(CATALOG_PATH)


def _git_status_for(paths: list[str]) -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--", *paths],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def test_market_catalog_module_is_planned_not_active():
    assert MARKET_CATALOG_STATUS == "planned_not_active"
    assert MARKET_CATALOG_RUNTIME_ENABLED is False
    assert MARKET_CATALOG_UI_ENABLED is False
    assert MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED is False


def test_generated_catalog_exists_and_has_valid_structure():
    catalog = _catalog()

    assert CATALOG_PATH.exists()
    assert catalog.catalog_name == "Market Catalog / Catálogo de Mercados"
    assert catalog.status == "planned_not_active"
    assert catalog.runtime_enabled is False
    assert catalog.ui_enabled is False
    assert catalog.business_composition_enabled is False
    assert catalog.source_file_name == "1.1-Lista de 3859 nichos.docx"
    assert catalog.total_raw_entries == 3859
    assert catalog.total_normalized_entries == len(catalog.entries)
    assert catalog.total_normalized_entries >= 3000
    assert catalog.duplicates_removed == 6
    assert catalog.metadata["discarded_lines_count"] == 2
    assert catalog.metadata["count_note"]


def test_market_ids_and_normalized_names_are_unique_and_non_empty():
    catalog = _catalog()
    market_ids = [entry.market_id for entry in catalog.entries]
    normalized_names = [entry.normalized_name for entry in catalog.entries]

    assert len(market_ids) == len(set(market_ids))
    assert len(normalized_names) == len(set(normalized_names))
    assert all(entry.raw_name and entry.display_name and entry.normalized_name for entry in catalog.entries)


def test_entries_are_planned_not_active_and_unmapped_by_default():
    catalog = _catalog()

    for entry in catalog.entries:
        payload = entry.to_dict()
        assert validate_market_catalog_entry(payload)
        assert entry.status == "planned_not_active"
        assert entry.activation_status == ACTIVATION_STATUS
        assert entry.business_composition_ready is False
        for field in EMPTY_MAPPING_FIELDS:
            assert payload[field] == []
        assert all(value is None for value in payload["scoring"].values())


def test_loader_is_read_only_and_returns_copies():
    catalog = _catalog()
    first = catalog.entries[0]
    by_id = get_market_by_id(catalog, first.market_id)
    by_name = find_market_by_normalized_name(catalog, first.normalized_name)
    listed = list_markets(catalog)

    assert by_id == first.to_dict()
    assert by_name == first.to_dict()
    listed[0]["display_name"] = "mutated"
    assert list_markets(catalog)[0]["display_name"] == first.display_name
    assert get_market_by_id(catalog, "missing-market") is None
    assert find_market_by_normalized_name(catalog, "missing market") is None


def test_external_catalog_does_not_modify_internal_active_assets_or_runtime():
    assert _git_status_for(["catalogs", "domains", "runtime", "api.py"]) == ""
    for relative in FORBIDDEN_PATHS:
        assert not (ROOT / relative).exists(), relative


def test_catalog_boundaries_are_documented_in_generated_metadata():
    catalog = _catalog()

    assert catalog.metadata["activation_status"] == "not_evaluated"
    assert catalog.metadata["runtime_boundary"] == "not_active_no_runtime_no_ui_no_business_composition"
    assert catalog.metadata["duplicate_lines"]
    assert catalog.metadata["discarded_lines"]
