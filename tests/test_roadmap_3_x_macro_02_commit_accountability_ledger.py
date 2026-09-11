"""Guard the complete, immutable accountability ledger for Macro 02."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_COMMIT_ACCOUNTABILITY_LEDGER.md"
BASE = "fbbc5372865467c4c5de3c09e580644971e2d163"
HEAD = "ad7a3dcac1959aba086c1098b126e8c97b9e32b8"

EXPECTED = [
    "eb3a02f72be320a75d5a7501f2c059dba8e0c548",
    "1c07393b21cd3b4965e956da519ddfa71ce3eaf3",
    "975a54e5624512450903d9b94c380cbe57bad0f0",
    "c520d2a072c1435118113f7411fd862b008d3194",
    "6622289f09e8af28845427d0984706267cdfc6c6",
    "75b0d1eed5b169bc8bdfe35d3f5b67f37b2778c3",
    "1fdf1c444a5985c01658d6125377a0835849491e",
    "888527c0a2d58198e10df80d1ccc90673c1692e9",
    "a6af100df13665efefedf81388da1ebe177e5480",
    "588aeaaf99fda6e0c84174be753b8dc11d09e548",
    "b1b15e0605fe5efe4fbdc9dd2123f3d43199dc9d",
    "c258700a894fdb7a7962b89ed57b165ca799d3b0",
    "378ebd557f3191675b8708a77461f187ccaa3330",
    "74f1a366e954dbc041c10c0ee17d65e041bb1421",
    "24b0fecc23148c325a3f5577559e689c6e1872e9",
    "61a0eab30e88f06254c66adc7ca5de8d744e09e8",
    "87f87820dfc555d9bb646e935ea01b15aebb0c5b",
    "555f0294a5aba4027757de2f2ea40425c06bb7f5",
    "df80a386e26992dff81e9845f56ee0fc3d193075",
    "ad7a3dcac1959aba086c1098b126e8c97b9e32b8",
]


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def test_range_contains_exactly_the_twenty_published_commits():
    actual = _git("rev-list", "--reverse", f"{BASE}..{HEAD}").splitlines()
    assert actual == EXPECTED
    assert len(actual) == 20


def test_ledger_has_every_commit_and_required_accountability_fields():
    text = LEDGER.read_text(encoding="utf-8")
    assert text.count("| `") >= 20
    for commit in EXPECTED:
        assert text.count(f"`{commit}`") >= 1
    for field in (
        "Station / coherent piece",
        "Files modified",
        "Contracts, tests, evidence, dependencies, rollback, and side effects",
        "Macro 02 correspondence",
        "STATION_COMMIT_PARITY_DEVIATION",
        "MATERIAL_AUTHORIZATION_MISMATCH",
    ):
        assert field in text


def test_history_is_not_rewritten_by_the_ledger_station():
    assert _git("rev-parse", "HEAD") == HEAD
    assert _git("rev-parse", f"{HEAD}^") == "df80a386e26992dff81e9845f56ee0fc3d193075"
