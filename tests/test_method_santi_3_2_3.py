"""Documentary guard for the additive Method Santi 3.2.3 update."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs" / "METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md"
PRIOR = ROOT / "docs" / "METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION.md"
INDEX = ROOT / "docs" / "FUTURE_PLATFORM_EXTENSION_INDEX.md"


def test_method_3_2_3_is_additive_and_not_product_authority():
    text = METHOD.read_text(encoding="utf-8")
    assert PRIOR.exists()
    for marker in (
        "additive, compatible evolution",
        "METHOD_SANTI_3_2_3_MATERIALIZED",
        "DEVELOPMENT_METHODOLOGY",
        "IA_CORE_PRODUCT_CAPABILITY: NO",
        "IA_CORE_RUNTIME_COMPONENT: NO",
        "COGNITIVE_KERNEL_FAMILY: NO",
        "COMMERCIAL_FEATURE: NO",
    ):
        assert marker in text


def test_method_3_2_3_contains_the_six_evidence_protocols():
    text = METHOD.read_text(encoding="utf-8")
    for protocol in (
        "THREE_CLOCK_MISSION_METRICS_V1",
        "PRE_LEVEL_B_HISTORICAL_IMPACT_GATE_V1",
        "ESTIMATE_CALIBRATION_PROTOCOL_V1",
        "FULL_REPORT_FIRST_PASS_POLICY_V1",
        "INTERRUPTION_RECOVERY_EVIDENCE_PROTOCOL_V1",
        "VALIDATION_COST_ACCOUNTING_V1",
    ):
        assert protocol in text


def test_method_3_2_3_preserves_safety_and_report_boundaries():
    text = METHOD.read_text(encoding="utf-8")
    for marker in (
        "Historical tests validate their own checkpoint contract",
        "does not add skips",
        "does not create product authority",
        "METHOD_UPDATE_IS_NOT_PRODUCT_CAPABILITY",
        "METHOD_UPDATE_IS_NOT_COGNITIVE_KERNEL_NODE",
        "METHOD_UPDATE_IS_NOT_RUNTIME",
    ):
        assert marker in text


def test_method_3_2_3_is_indexed_as_the_current_additive_method():
    index = INDEX.read_text(encoding="utf-8")
    assert "METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md" in index
    assert "METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION.md" in index
