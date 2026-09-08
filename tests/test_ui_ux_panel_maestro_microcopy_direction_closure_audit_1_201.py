"""N2 decision-closure audit for the UI/UX 1.200 direction contract."""

from collections import Counter
from pathlib import Path
import subprocess

from ui_ux_panel_maestro_microcopy_1_200_support import (
    EXPECTED_GEOMETRY_CSS,
    allowlist_counts,
    baseline_bytes,
    load_allowlist,
)


ROOT = Path(__file__).resolve().parents[1]
CURRENT = "a2afc307d7278657a324efba345c04e28c39525a"
DECISIONS = {
    "PKG_B_EDITORIAL_STYLE": "B",
    "PKG_B_CONSISTENCY_RULE": "A",
    "PKG_B_GEOMETRY_REMEDIATION": "B",
    "PKG_C_CONTEXTUAL_VARIANTS": "A",
    "PKG_C_CONTRACT_SENSITIVE": "A",
    "PKG_C_ACTION_PERMISSION": "A",
    "PKG_C_AMBIGUOUS_ROLE": "A",
    "PKG_D_CONTRACT_VOCABULARY": "A",
}


def _unchanged(*paths):
    return subprocess.run(
        ["git", "diff", "--quiet", "4618c59", CURRENT, "--", *paths],
        cwd=ROOT,
        check=False,
    ).returncode == 0


def test_n2_all_eight_direction_decisions_are_closed_without_unmapped_units():
    items = load_allowlist()["items"]
    packages = {item["direction_package"] for item in items}
    assert packages - {"LEVEL_A_INHERITED"} == set(DECISIONS)
    assert "LEVEL_A_INHERITED" in packages
    assert all(item["microcopy_id"] and item["decision_unit_id"] for item in items)
    assert all(item["direction_package"] in DECISIONS or item["direction_package"] == "LEVEL_A_INHERITED" for item in items)
    assert all(item["approved_decision"] in {"A", "B", "INHERITED_KEEP"} for item in items)
    assert not (set(DECISIONS) - packages)


def test_n2_editorial_geometry_and_level_d_results_match_the_closed_contract():
    counts = allowlist_counts()
    assert counts["ALLOWED_EDITORIAL_CHANGE"] == 295
    assert counts["ALLOWED_GEOMETRY_CHANGE"] == 15
    assert counts["KEEP_LEVEL_D"] == 692

    items = load_allowlist()["items"]
    editorial = [item for item in items if item["change_class"] == "ALLOWED_EDITORIAL_CHANGE"]
    geometry = [item for item in items if item["change_class"] == "ALLOWED_GEOMETRY_CHANGE"]
    level_d = [item for item in items if item["change_class"] == "KEEP_LEVEL_D"]
    assert {item["approved_decision"] for item in editorial} == {"B"}
    assert {item["approved_decision"] for item in geometry} == {"B"}
    assert {item["approved_decision"] for item in level_d} == {"A"}
    assert all(item["current_text_is_preserved"] is False for item in editorial)
    assert all(item["current_text_is_preserved"] for item in level_d)
    assert _unchanged("ui/web/index.html", "ui/web/i18n_es.json")

    baseline = baseline_bytes("ui/web/styles.css").replace(b"\r\n", b"\n").decode()
    current = (ROOT / "ui" / "web" / "styles.css").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert current == baseline + EXPECTED_GEOMETRY_CSS


def test_n2_no_contract_change_or_direction_widening_is_observable():
    assert _unchanged(
        "ui/web/index.html",
        "ui/web/i18n_es.json",
        "api.py",
        "core/backend_internal_ui_payloads.py",
    )
    counts = Counter(item["change_class"] for item in load_allowlist()["items"])
    assert counts["ALLOWED_EDITORIAL_CHANGE"] == 295
    assert counts["ALLOWED_GEOMETRY_CHANGE"] == 15
