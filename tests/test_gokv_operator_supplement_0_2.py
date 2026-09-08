import json
from pathlib import Path

import pytest

from gokv.capture import validate_learning_event
from gokv.supplements import (
    append_operator_measurement_supplement,
    build_operator_measurement_supplement,
    validate_operator_measurement_supplement,
)
from gokv.storage import VaultPaths


ROOT = Path(__file__).resolve().parents[1]


def _supplement():
    return build_operator_measurement_supplement(
        supplement_id="gokv_0_1_operator_measurement_supplement",
        original_event_id="gokv_0_1_first_self_capture",
        model="GPT-5.6 Luna",
        effort="Muy Alto",
        visible_duration="31m39s",
        quota_5h_start_remaining=100,
        quota_5h_end_remaining=95,
        quota_5h_delta=5,
        quota_weekly_start_remaining=100,
        quota_weekly_end_remaining=99,
        quota_weekly_delta=1,
        planned_stations=8,
        completed_stations=8,
        commit_count=8,
        result="PASS",
        reported_at="2026-09-08T00:00:00+00:00",
        notes=["Operator supplied after the original capture."],
    )


def test_operator_supplement_links_original_and_preserves_source_quality(tmp_path):
    paths = VaultPaths(tmp_path / "vault")
    paths.ensure()
    original_path = paths.events_dir / "gokv_0_1_first_self_capture.json"
    original_path.write_text(
        (ROOT / "knowledge/global_operational/events/gokv_0_1_first_self_capture.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    original_before = original_path.read_bytes()
    original = json.loads(original_before)
    supplement = _supplement()

    assert validate_learning_event(original)["duration"] is None
    assert validate_operator_measurement_supplement(supplement)["source"] == "OPERATOR_REPORTED"
    destination = append_operator_measurement_supplement(supplement, paths)

    assert destination.is_file()
    assert original_path.read_bytes() == original_before
    stored = json.loads(destination.read_text(encoding="utf-8"))
    assert stored["original_event_id"] == "gokv_0_1_first_self_capture"
    assert stored["quota_5h_delta"] == 5
    assert stored["quota_weekly_delta"] == 1
    assert "tokens" not in stored
    assert "dollars" not in stored
    assert "cost" not in stored


def test_operator_supplement_is_append_only_and_rejects_invalid_source(tmp_path):
    paths = VaultPaths(tmp_path / "vault")
    paths.ensure()
    (paths.events_dir / "gokv_0_1_first_self_capture.json").write_text(
        (ROOT / "knowledge/global_operational/events/gokv_0_1_first_self_capture.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    append_operator_measurement_supplement(_supplement(), paths)
    with pytest.raises(ValueError, match="supplement duplicado"):
        append_operator_measurement_supplement(_supplement(), paths)

    invalid = _supplement()
    invalid["source"] = "MEASURED"
    with pytest.raises(ValueError, match="OPERATOR_REPORTED"):
        validate_operator_measurement_supplement(invalid)
