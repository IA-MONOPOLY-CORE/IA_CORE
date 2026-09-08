import json
import subprocess
from pathlib import Path

from gokv.supplements import validate_operator_measurement_supplement


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_2_0_CONTINUITY_PREFLIGHT.md"
SUPPLEMENT = ROOT / "knowledge/global_operational/events/supplements/roadmap_2_x_operator_measurement_supplement.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_preflight_gate_and_zero_blocking_mismatch_are_recorded():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_2_0_CONTINUITY_PREFLIGHT_PASSED" in text
    assert "BLOCKING_CONTINUITY_MISMATCH = 0" in text
    assert "NON_BLOCKING_DOCUMENTATION_DRIFT" in text
    assert "HISTORICAL_ONLY" in text


def test_preflight_document_preserves_its_historical_entry_truth():
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    assert branch == "main"
    text = DOC.read_text(encoding="utf-8")
    assert "| HEAD | `eb00a47871d8c1cbb0597d13379901f114ff240f`" in text
    assert "| origin/main | `eb00a47871d8c1cbb0597d13379901f114ff240f`" in text
    assert "| Ahead/behind | `0/0`" in text


def test_roadmap_operator_supplement_is_valid_and_preserves_reset_ambiguity():
    supplement = validate_operator_measurement_supplement(_load(SUPPLEMENT))
    assert supplement["original_event_id"] == "ui_ux_1_204_integral_closure_and_handoff_learning_event"
    assert supplement["planned_stations"] == 4
    assert supplement["completed_stations"] == 0
    assert supplement["quota_5h_start_remaining"] == 75
    assert supplement["quota_5h_end_remaining"] == 98
    assert supplement["quota_5h_delta"] == 0
    assert any("NOT_RECONSTRUCTABLE_EXACTLY" in note for note in supplement["notes"])
    assert supplement["quota_weekly_delta"] == 1
