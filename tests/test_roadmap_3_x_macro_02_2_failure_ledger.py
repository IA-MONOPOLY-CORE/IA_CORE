"""Baseline accountability checks for Roadmap 3.x Macro 02.2."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_2_FAILURE_ACCOUNTABILITY_LEDGER.md"


def _text() -> str:
    return LEDGER.read_text(encoding="utf-8")


def test_failure_ledger_records_the_reproducible_baseline():
    text = _text()
    assert "ROADMAP_3X_MACRO_02_2_HISTORICAL_TEST_CONTRACT_CONVERGENCE_AND_DOCTRINE_CONSOLIDATION" in text
    assert "6905 tests collected" in text
    assert "6774 passed, 125 failed, 6 skipped, 5 warnings" in text
    assert "ia-core-macro-02-2-baseline.txt" in text


def test_failure_ledger_has_one_row_per_failed_node_and_no_silent_disposition():
    text = _text()
    rows = re.findall(r"^\| (\d+) \| `tests/[^`]+::test_[^`]+` \| `[^`]+` \| `[^`]+` \| .+ \| .+ \| `RESOLVED_HISTORICAL_CHECKPOINT` \|$", text, re.MULTILINE)
    assert len(rows) == 125
    assert [int(row) for row in rows] == list(range(1, 126))
    for forbidden in ("skip", "xfail", "delete", "bulk-regenerat"):
        assert forbidden in text.lower()
    assert "PENDING_HISTORICAL_ADAPTATION" not in text
    assert "HISTORICAL_SUITE_TRUTH_CONVERGED" in text
    assert "UNKNOWN_TRUE_FRONTIER" not in text


def test_failure_ledger_root_cause_counts_are_explicit():
    text = _text()
    assert "| `GOKV_GENERATION_HISTORY` | 10 |" in text
    assert "| `ROADMAP_CHECKPOINT_DIFF` | 4 |" in text
    assert "| `UI_UX_HISTORICAL_SURFACE` | 88 |" in text
    assert "| `MICROCOPY_FROZEN_BASELINE` | 21 |" in text
    assert "| `UI_UX_HISTORICAL_SURFACE` (continuity probes) | 2 |" in text
