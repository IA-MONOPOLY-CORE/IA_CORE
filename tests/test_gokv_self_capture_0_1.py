import json
from pathlib import Path

from gokv.capture import validate_execution_metric, validate_learning_event
from gokv.compiler import compile_execution_pack
from gokv.storage import default_paths, iter_knowledge_items


def test_first_self_capture_event_metric_and_pack_round_trip():
    paths = default_paths(Path.cwd())
    event_path = paths.events_dir / "gokv_0_1_first_self_capture.json"
    metric_path = paths.metrics_dir / "gokv_0_1_first_self_capture_metric.json"
    pack_path = paths.packs_dir / "gokv.pack.3d734103e4e0731d.json"

    event = json.loads(event_path.read_text(encoding="utf-8"))
    metric = json.loads(metric_path.read_text(encoding="utf-8"))
    stored_pack = json.loads(pack_path.read_text(encoding="utf-8"))

    assert validate_learning_event(event)["end_commit"] == "e2684ee"
    assert event["planned_stations"] == 8
    assert event["completed_stations"] == 6
    assert event["candidate_knowledge_ids"] == []
    assert event["metrics_refs"] == ["gokv_0_1_first_self_capture_metric"]

    assert validate_execution_metric(metric)["measurement_quality"] == "NOT_AVAILABLE"
    assert metric["station_count"] == 6
    assert metric["duration"] is None
    assert metric["quota_5h_start"] is None
    assert metric["quota_weekly_start"] is None

    request = {
        "mission_class": "development_foundation",
        "task_type": "bootstrap",
        "scope": "IA_CORE_BUILD",
        "risk_class": "HIGH",
        "required_capabilities": [],
        "agent_class": "BUILD_AGENT",
        "model_size_class": "SMALL",
        "tags": ["gates"],
        "mode": "DEVELOPMENT_VALIDATED",
    }
    assert stored_pack == compile_execution_pack(request, paths)
    assert stored_pack["applicable_knowledge_ids"] == [
        "controlled_assembled_block_execution",
        "internal_gates",
    ]
    assert stored_pack["output_contract"]["runtime_enabled"] is False
    assert stored_pack["output_contract"]["execution_enabled"] is False
    assert stored_pack["output_contract"]["payload_enabled"] is False


def test_self_capture_did_not_create_knowledge_after_gokv_03_promotion():
    items = list(iter_knowledge_items(default_paths(Path.cwd())))

    assert len(items) == 23
    assert sum(item["status"] == "PROMOTED" for item in items) == 7
    assert not any(item["knowledge_id"] == "gokv_0_1_first_self_capture" for item in items)
