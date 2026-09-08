import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_BACKEND_SURFACE_CENSUS.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_backend_surface_census.json"


def test_n0_surface_census_gate_is_read_only_and_reproducible():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N0_BACKEND_SURFACE_CENSUS_PASSED" in DOC.read_text(encoding="utf-8")
    assert data["read_only"] is True
    assert data["baseline_commit"] == "82d309f00ab99dfa9eb100e5594bf1d8d0559f5a"
    assert data["repository_counts"]["all_files"] == 1598
    assert data["repository_counts"]["non_test_python_files"] == 217
    assert data["static_candidates"]["write_side_effect_paths"] == 60
    assert data["static_candidates"]["network_capable_references"] == 9
    assert data["product_change"] is False
    assert data["runtime_started"] is False
    assert data["provider_called"] is False
    assert data["network_called"] is False
    assert data["forbidden_actions_performed"] == []

