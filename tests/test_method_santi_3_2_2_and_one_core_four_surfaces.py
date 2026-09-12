"""Contract checks for the additive Method Santi 3.2.2 documentary block."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs" / "METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION.md"
DOCTRINE = ROOT / "docs" / "IA_CORE_ONE_CORE_FOUR_SURFACES_DOCTRINE.md"
PRINT_READY = ROOT / "docs" / "generated" / "METHOD_SANTI_3_2_2_ONE_CORE_FOUR_SURFACES_PRINT_READY.html"
INDEX = ROOT / "docs" / "FUTURE_PLATFORM_EXTENSION_INDEX.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_method_3_2_2_is_additive_and_contains_the_governed_rules():
    text = read(METHOD)
    assert "additive evolution of Method Santi 3.2.1" in text
    for marker in (
        "METHOD_SANTI_3_2_2_MATERIALIZED",
        "Mission scale",
        "ONE_STATION_ONE_COMMIT",
        "EVERY_COMMIT_IS_ACCOUNTABLE",
        "Dynamic frontier engineering",
        "FRONTIER_AT_MISSION_START",
        "IA_CORE does not depend on changing language-model weights",
        "GOKV preserves governed knowledge",
        "DOOL preserves development-origin observations",
        "OCI delivers knowledge pertinent",
        "There is no artificial quota",
        "Governed continuity across chats, agents and projects",
        "Full report by default",
        "PUSH_ONLY_AT_PUBLISHABLE_CHECKPOINT",
        "REMOTE_VERIFICATION_IS_PART_OF_PUBLICATION",
        "Historical tests validate their own checkpoint contract",
        "TEST_SAFETY_MUST_BE_ENFORCED_NOT_ASSUMED",
    ):
        assert marker in text


def test_method_3_2_2_keeps_boundaries_and_handoff_complete():
    text = read(METHOD)
    for marker in (
        "real provider",
        "network",
        "credential",
        "runtime",
        "payload",
        "endpoint",
        "integration",
        "automatic",
        "HUMAN_DECISION_REQUIRED",
        "The print-ready companion",
        "No deterministic local PDF renderer was available",
    ):
        assert marker in text


def test_one_core_four_surfaces_is_the_single_future_doctrine():
    text = read(DOCTRINE)
    for marker in (
        "ONE_CORE_FOUR_SURFACES_DOCTRINE_DOCUMENTED",
        "un solo núcleo canónico",
        "IA_CORE PLATFORM",
        "IA_CORE OS DESKTOP/SERVER",
        "IA_CORE MOBILE",
        "IA_CORE MOBILE OS / MOBILE ENVIRONMENT",
        "IA_CORE CANONICAL CORE",
        "GOKV, DOOL, and OCI",
        "ONE_CORE_FOUR_SURFACES",
        "NO_INDEPENDENT_PRODUCT_FORKS",
        "SHARED_INTELLIGENCE_ENVIRONMENT_SPECIFIC_EXECUTION",
        "PRESERVE_FUTURE_ARCHITECTURAL_OPTIONALITY",
        "INTEGRATE_WHAT_WORKS_REPLACE_WHAT_FAILS_CREATE_WHAT_IS_MISSING",
        "EARNED_IRREPLACEABILITY",
        "HUMAN_AMPLIFICATION_WITH_SELECTIVE_SUBSTITUTION",
        "does not create an installable OS",
    ):
        assert marker in text


def test_index_links_the_canonical_documents_without_repeating_the_doctrine():
    text = read(INDEX)
    assert "METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION.md" in text
    assert "IA_CORE_ONE_CORE_FOUR_SURFACES_DOCTRINE.md" in text
    assert "METHOD_SANTI_3_2_2_ONE_CORE_FOUR_SURFACES_PRINT_READY.html" in text
    assert "single canonical doctrine" in text


def test_print_ready_fallback_is_static_and_complete():
    text = read(PRINT_READY)
    for marker in (
        "Method Santi 3.2.2 and One Core, Four Surfaces",
        "Version:",
        "2026-09-12",
        "Method Santi 3.2.2",
        "Dynamic frontiers",
        "Learning and continuity",
        "ONE CORE, FOUR SURFACES",
        "IA_CORE PLATFORM",
        "IA_CORE OS DESKTOP/SERVER",
        "IA_CORE MOBILE",
        "IA_CORE MOBILE OS / MOBILE ENVIRONMENT",
        "METHOD_SANTI_3_2_2_MATERIALIZED",
        "ONE_CORE_FOUR_SURFACES_DOCTRINE_DOCUMENTED",
        "print-ready fallback",
    ):
        assert marker in text
    assert "<script" not in text.lower()
    assert "fetch(" not in text.lower()
