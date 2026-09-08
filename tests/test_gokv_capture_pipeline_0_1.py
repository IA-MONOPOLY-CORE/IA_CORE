"""N4 capture pipeline and metric tests for GOKV 0.1."""

from pathlib import Path

import pytest

from gokv.capture import (
    append_execution_metric,
    append_learning_event,
    build_execution_metric,
    build_learning_event,
)
from gokv.storage import VaultPaths


def vault(tmp_path: Path) -> VaultPaths:
    return VaultPaths(tmp_path / "vault")


def event():
    return build_learning_event(
        event_id="event_one",
        source_prompt="PROMPT GOKV 0.1",
        source_phase="N4",
        source_checkpoint="n4_checkpoint",
        start_commit="7cb7134",
        end_commit=None,
        model=None,
        effort=None,
        mission_type="development_foundation",
        planned_stations=8,
        completed_stations=4,
        result="observed",
    )


def metric():
    return build_execution_metric(
        metric_id="metric_one",
        model=None,
        effort=None,
        task_type="development_foundation",
        measurement_quality="NOT_AVAILABLE",
        notes=["quota not supplied by operator"],
    )


def test_n4_machine_readable_capture_schemas_exist():
    root = Path(__file__).resolve().parents[1] / "knowledge/global_operational/schema"
    assert (root / "learning_event.schema.json").is_file()
    assert (root / "execution_metric.schema.json").is_file()
    assert event()["schema_version"] == "gokv.learning_event.v1"
    assert metric()["measurement_quality"] == "NOT_AVAILABLE"


def test_n4_append_is_safe_and_does_not_promote_knowledge(tmp_path):
    paths = vault(tmp_path)
    event_path = append_learning_event(event(), paths)
    metric_path = append_execution_metric(metric(), paths)
    assert event_path.is_file() and metric_path.is_file()
    with pytest.raises(ValueError, match="registro duplicado"):
        append_learning_event(event(), paths)
    assert not list(paths.items_dir.glob("*.json"))


def test_n4_unknown_measurements_are_valid_without_invention():
    unknown = build_execution_metric(
        metric_id="unknown_metric",
        model=None,
        effort=None,
        task_type="development_foundation",
        duration=None,
        station_count=None,
        operator_interventions=None,
        retries=None,
        rollbacks=None,
        result=None,
        measurement_quality="NOT_AVAILABLE",
    )
    assert unknown["quota_5h_start"] is None
    assert unknown["quota_weekly_delta"] is None


def test_n4_invalid_measurement_quality_and_station_counts_fail():
    with pytest.raises(ValueError, match="measurement_quality invalida"):
        build_execution_metric(
            metric_id="bad_metric",
            model=None,
            effort=None,
            task_type="development_foundation",
            measurement_quality="INVENTED",
        )
    with pytest.raises(ValueError, match="completed_stations"):
        build_learning_event(
            event_id="bad_event",
            source_prompt="prompt",
            source_phase="N4",
            source_checkpoint=None,
            start_commit=None,
            end_commit=None,
            model=None,
            effort=None,
            mission_type="development_foundation",
            planned_stations=2,
            completed_stations=3,
            result="observed",
        )
