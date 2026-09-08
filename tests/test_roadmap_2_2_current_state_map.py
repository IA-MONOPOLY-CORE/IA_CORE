from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_2_2_CURRENT_STATE_MAP.md"


def test_current_state_map_gate_and_backend_entry_condition_exist():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_2_2_CURRENT_STATE_MAP_PASSED" in text
    assert "BACKEND_ENTRY_CONDITION = READ_ONLY_INVENTORY_FIRST" in text
    assert "CAN_START_ROADMAP_3_X = YES" in text
    assert "REAL_CONTROLLED" in text
    assert "REAL_SANDBOX" in text
    assert "REAL_READ_ONLY" in text
    assert "UNKNOWN_REQUIRES_AUDIT" in text


def test_current_state_map_has_required_table_columns_and_rows():
    text = DOC.read_text(encoding="utf-8")
    header = "| component | classification | evidence | current truth | risk | debt | audit required in 3.x | priority |"
    assert header in text
    rows = [line for line in text.splitlines() if line.startswith("| ") and line.count("|") == 9]
    assert len(rows) >= 25
    for category in (
        "DOCUMENTED_ONLY",
        "TEST_ONLY",
        "FIXTURE_ONLY",
        "LEGACY",
        "FUTURE",
    ):
        assert category in text


def test_state_map_preserves_read_only_and_no_activation_boundary():
    text = DOC.read_text(encoding="utf-8")
    assert "must not implement or enable" in text
    assert "runtime, execution, API expansion, provider calls or operational writes" in text
