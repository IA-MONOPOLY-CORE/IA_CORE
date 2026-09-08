import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_3_0_BACKEND_CROSS_LAYER_RISK_UNKNOWN_MATRIX.md"
FIXTURE = ROOT / "tests/fixtures/roadmap_3_0_backend_cross_layer_risk_unknown_matrix.json"


def test_n7_cross_layer_matrix_preserves_unknowns_and_does_not_infer_activation():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "ROADMAP_3_0_N7_CROSS_LAYER_MATRIX_PASSED" in DOC.read_text(encoding="utf-8")
    assert data["classifications"]["REAL_ACTIVE"] == []
    assert data["write_path_total"] == 60
    assert data["execution_path_total"] == 1
    assert data["network_path_total"] == 9
    assert data["provider_total"] == 3
    assert data["security_boundary_total"] == 10
    assert data["unguarded_boundary_total"] == 4
    assert data["unknown_boundary_total"] == 6
    assert data["p0_count"] == 0
    assert data["p1_count"] == 3
    assert data["side_effect_performed"] is False
    assert data["product_change"] is False

