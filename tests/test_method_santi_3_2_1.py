"""Contract guard for the additive Method Santi 3.2.1 evolution."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD_3_2 = ROOT / "docs" / "METHOD_SANTI_3_2_GOVERNED_CAPABILITY_EXPANSION.md"
METHOD_3_2_1 = ROOT / "docs" / "METHOD_SANTI_3_2_1_HERMETIC_VALIDATION_AND_COMMIT_ACCOUNTABILITY.md"


def test_method_3_2_1_is_additive_and_preserves_method_3_2():
    original = METHOD_3_2.read_text(encoding="utf-8")
    evolved = METHOD_3_2_1.read_text(encoding="utf-8")
    assert original
    assert "additive evolution" in evolved
    assert "does not replace the method" in evolved
    assert "runtime authority" in evolved


def test_method_3_2_1_requires_hermetic_validation_and_accountability():
    text = METHOD_3_2_1.read_text(encoding="utf-8")
    for rule in (
        "TEST_SAFETY_MUST_BE_ENFORCED_NOT_ASSUMED",
        "COLLECTION_MUST_BE_SIDE_EFFECT_FREE",
        "NO_PHANTOM_TEST_WRITES",
        "RESTORE_IS_NOT_HERMETICITY",
        "ONE_STATION_ONE_COMMIT",
        "EVERY_COMMIT_IS_ACCOUNTABLE",
        "REPAIR_PARITY_IS_EXPLICIT",
        "LEARNING_OR_REUSE_IS_MANDATORY",
        "VALIDATE_BEFORE_SCALING",
    ):
        assert rule in text


def test_method_3_2_1_keeps_stop_conditions_explicit():
    text = METHOD_3_2_1.read_text(encoding="utf-8")
    for forbidden_boundary in (
        "real provider",
        "network",
        "credential value",
        "runtime",
        "payload",
        "endpoint",
        "integration",
        "history rewrite",
        "silent skips",
    ):
        assert forbidden_boundary in text
