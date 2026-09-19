from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs/METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING.md"


def test_method_324_is_additive_development_method_only():
    text = METHOD.read_text(encoding="utf-8")
    for marker in (
        "METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING",
        "CANONICAL_EVIDENCE_GATE_V1",
        "FUNCTIONAL_PUBLICATION_FETCH_VERIFIED_TIME",
        "DOCUMENTARY_CONTENT_FINALIZED_TIME",
        "DOCUMENTARY_LOCK_FETCH_VERIFIED_TIME",
        "OPERATOR_VISIBLE_COMPLETION_TIME",
        "PUBLICATION_METADATA_MUST_NOT_CHASE_ITS_OWN_HEAD",
        "METHOD_UPDATE_IS_NOT_PRODUCT_CAPABILITY",
        "METHOD_UPDATE_IS_NOT_RUNTIME",
        "METHOD_UPDATE_IS_NOT_AUTHORITY",
        "METHOD_UPDATE_IS_NOT_GOKV_PROMOTION",
        "UNKNOWN_IS_VALID_EVIDENCE",
    ):
        assert marker in text


def test_method_324_contains_no_product_authority_or_runtime_activation():
    text = METHOD.read_text(encoding="utf-8").lower()
    assert "ia_core_product_capability: no" in text
    assert "ia_core_runtime_component: no" in text
    assert "cognitive_kernel_family: no" in text
    assert "commercial_feature: no" in text
    assert "oauth" not in text
    assert "jwt" not in text
