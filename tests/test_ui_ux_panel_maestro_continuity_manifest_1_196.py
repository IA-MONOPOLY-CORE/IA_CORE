"""N1 closed-path continuity manifest tests for UI/UX 1.196."""

from pathlib import Path

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CONTINUITY_MANIFEST_1_196.md"


def test_manifest_has_exact_baseline_stations_and_protected_surfaces():
    content = DOC.read_text(encoding="utf-8")
    assert "357a08d" in content
    assert "N1" in content and "N10" in content
    assert "no glob" in content.lower()
    assert "microcopy contractual transversal" in content.lower()
    assert len(continuity.STATION_PATHS) == 10
    assert set(continuity.STATION_MESSAGES) == {f"N{i}" for i in range(1, 11)}
    assert "ui/web/index.html" in continuity.PRODUCT_READ_ONLY
    assert "core/backend_internal_ui_payloads.py" in continuity.PRODUCT_READ_ONLY


def test_manifest_rejects_product_and_unknown_paths():
    for path in (
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/i18n_es.json",
        "api.py",
        "backend/new_endpoint.py",
        "runtime/new_runtime.py",
    ):
        try:
            continuity.assert_rejects_paths({path})
        except AssertionError:
            pass
        else:
            raise AssertionError(path)
    continuity.assert_no_permissive_manifest_source()


def test_n1_current_paths_and_protected_product_are_closed():
    continuity.assert_current_station_is_exact("N1")

