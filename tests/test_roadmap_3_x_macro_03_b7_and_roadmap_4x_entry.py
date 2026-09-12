from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B7 = ROOT / "docs/ROADMAP_3_X_MACRO_03_B7_CLOSURE_READINESS_MATRIX.md"
ENTRY = ROOT / "docs/ROADMAP_4_X_ENTRY_CONTRACT.md"


def test_b7_matrix_has_all_required_rows_and_explicit_outcome():
    text = B7.read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*(\d+)\s*\|", text, re.MULTILINE)
    assert rows == [str(index) for index in range(1, 17)]
    assert "B7_READY_FOR_DIRECTION_ACCEPTANCE" in text
    assert "ROADMAP_3_X_CLOSED` is **not declared**" in text
    assert "Minimal Direction decision" in text
    assert "36 routes individually" in text


def test_b7_preserves_external_and_human_boundaries():
    text = B7.read_text(encoding="utf-8")
    for marker in (
        "EXTERNAL_EVIDENCE_PENDING",
        "DIRECTION_DECISION_PENDING",
        "production readiness",
        "canonical coverage",
        "No adapter",
        "provider",
        "secret values",
        "Roadmap 4.x",
    ):
        assert marker.lower() in text.lower()


def test_roadmap_4x_entry_is_partial_candidate_only():
    text = ENTRY.read_text(encoding="utf-8")
    for marker in (
        "PARTIAL_BLOCKED_BY_B7_DIRECTION_ACCEPTANCE_AND_EXTERNAL_EVIDENCE",
        "NEXT_MACRO_MISSION_CANDIDATE",
        "ARCHITECT_SELECTS_ONE_F004_FAMILY_REMEDIATION_BLOCK_AFTER_B7_ACCEPTANCE",
        "maximum first coherent block is **one family**",
        "does not choose P1 through P9",
        "not executed",
        "No human decision is needed to keep the current repository read-only",
    ):
        assert marker.lower() in text.lower()


def test_roadmap_4x_entry_preserves_prohibited_runtime_boundary():
    text = ENTRY.read_text(encoding="utf-8").lower()
    for marker in (
        "payload v2",
        "new endpoints",
        "runtime",
        "execution",
        "providers",
        "secret values",
        "product forks",
        "no reset",
    ):
        assert marker in text
