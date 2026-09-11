from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_LOTERIA_P3_CAPABILITY_EXTRACTION.md"


FILES = (
    "domains/loteria/validation_loteria.py",
    "domains/loteria/scoring.py",
    "domains/loteria/uscore_calculator.py",
    "domains/loteria/evolution_loteria.py",
    "domains/loteria/memoria_loteria.py",
    "domains/loteria/database_loteria.py",
)


def test_loteria_p3_extracts_all_requested_capability_families_without_movement():
    doc = DOC.read_text(encoding="utf-8")

    for relative in FILES:
        assert (ROOT / relative).is_file(), relative
    for family in ("validation", "ranking", "evolution", "learning", "evidence", "reveal", "lifecycle"):
        assert f"| {family} |" in doc
    for classification in (
        "LOTTERY_SPECIFIC",
        "GLOBAL_CONTRACT_WITH_DOMAIN_ADAPTER",
        "BLOCKED_BY_OWNER_OR_BOUNDARY",
    ):
        assert classification in doc


def test_loteria_p3_preserves_contract_and_runtime_boundaries():
    doc = DOC.read_text(encoding="utf-8")

    for marker in (
        "No capability is classified as `CANONICAL_DUPLICATE`",
        "No capability is promoted to global runtime behavior",
        "No UI, endpoint, backend, payload, provider, execution, or integration change",
        "owner, authorization, retention, rollback, and route coverage",
        "runtime learning is not enabled",
    ):
        assert marker in doc
