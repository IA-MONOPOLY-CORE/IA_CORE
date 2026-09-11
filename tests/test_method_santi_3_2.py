from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs" / "METHOD_SANTI_3_2_GOVERNED_CAPABILITY_EXPANSION.md"
METHOD_3_0 = ROOT / "docs" / "METHOD_SANTI_3_0_VERIFIED_ADAPTIVE_PROJECT_DIRECTION_ENGINEERING.md"
METHOD_AUDIT = ROOT / "docs" / "ROADMAP_2_1_METHOD_APPLIED_AUDIT.md"


def test_method_santi_3_2_is_additive_and_preserves_authority_layers():
    text = METHOD.read_text(encoding="utf-8")
    assert "METHOD SANTI 3.2" in text
    assert "METHOD_SANTI_3_0" in text
    assert "Applied Method inventory 2.1" in text
    assert "Standalone Method Santi 3.1: not present" in text
    assert "Current source, contracts, tests and published checkpoints win" in text
    assert METHOD_3_0.exists()
    assert METHOD_AUDIT.exists()


def test_method_santi_3_2_contains_the_governance_expansion_rules():
    text = METHOD.read_text(encoding="utf-8")
    required = (
        "Known Map Refinement",
        "Governed Surface Throughput",
        "Block, station and commit",
        "Ambiguity-proportional prompting",
        "Repository field recommendation loop",
        "Cumulative frontier preparation",
        "Progressive frontier compression",
        "Relevance-complete, scope-bounded inheritance",
        "Mandatory learning lifecycle",
        "Domain capability extraction",
        "Capability map model",
        "Scale neutrality",
        "Human and AI team authority",
        "Autonomy by maturity",
    )
    for section in required:
        assert section in text


def test_method_santi_3_2_keeps_non_operational_boundaries_explicit():
    text = METHOD.read_text(encoding="utf-8")
    for boundary in (
        "does not open runtime",
        "Promotion is never automatic",
        "does not rewrite historical checkpoints",
        "legacy HTTP routes",
        "product stores",
        "B-7",
    ):
        assert boundary in text


def test_method_santi_3_2_declares_station_commit_model():
    text = METHOD.read_text(encoding="utf-8")
    assert "Each station produces exactly one non-empty commit" in text
    assert "ONE COMMIT PER STATION" in text
    assert "METHOD_SANTI_3_2_MATERIALIZED" in text
