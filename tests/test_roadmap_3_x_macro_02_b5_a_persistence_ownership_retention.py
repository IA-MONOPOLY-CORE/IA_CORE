from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_B5_A_PERSISTENCE_OWNERSHIP_RETENTION.md"


FAMILIES = (
    "settings", "memory", "evidence", "logs", "metrics", "domains", "agents",
    "presets", "papers", "teams", "validation", "evolution", "learning",
)


def test_b5_a_covers_each_requested_persistence_family_and_boundary():
    doc = DOC.read_text(encoding="utf-8")

    for family in FAMILIES:
        assert f"| {family} |" in doc
    for marker in (
        "Owner and root classification",
        "Sensitivity",
        "Retention / write mode",
        "Tenant or deploy semantics",
        "Secret policy",
        "Consumer and recovery",
        "OWNER_PROBABLE_NOT_CONTRACTUAL",
        "append-only",
        "No product store was opened or modified",
    ):
        assert marker in doc


def test_b5_a_keeps_gokv_and_sandbox_distinct_from_product_persistence():
    doc = DOC.read_text(encoding="utf-8")

    assert "GOKV `knowledge/global_operational/`" in doc
    assert "controlled sandbox" in doc
    assert "they are not product persistence" in doc
    assert "No SQLite connection" in doc
    assert "No row upgrades a probable owner to a contractual owner" in doc
