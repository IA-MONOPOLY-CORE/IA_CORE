import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_RUNTIME_EXECUTION_GRAPH.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_runtime_execution_graph.json"


def test_n3_runtime_graph_distinguishes_legacy_execution_from_disabled_3x_runtime():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N3_RUNTIME_EXECUTION_GRAPH_PASSED" in DOC.read_text(encoding="utf-8")
    assert len(data["runtime_flags_false"]) >= 10
    assert data["attempt_factory_flags_false"] is True
    assert data["execution_runner_is_dry_run_contract"] is True
    assert data["active_executor_present_but_gated"] is True
    assert data["dedicated_runtime_operationally_enabled"] is False
    assert data["legacy_application_execution_path_present"] is True
    assert data["queue_worker_scheduler_observed"] is False
    assert data["runtime_started_by_audit"] is False
    assert data["execution_started_by_audit"] is False
    assert data["model_invoked"] is False

