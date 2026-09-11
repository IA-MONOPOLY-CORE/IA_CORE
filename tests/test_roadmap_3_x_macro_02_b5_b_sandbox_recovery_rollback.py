from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_B5_B_SANDBOX_RECOVERY_ROLLBACK.md"
ROLLBACK = ROOT / "core" / "domain_materialization_rollback.py"
BOUNDARY = ROOT / "core" / "sandbox_boundary.py"
LIFECYCLE = ROOT / "core" / "sandbox_lifecycle_validation.py"
CHECKPOINT_TEST = ROOT / "tests" / "test_sandbox_integral_rollback_6_1.py"


def test_b5_b_declares_recovery_obligations_and_preserves_sandbox_boundary():
    doc = DOC.read_text(encoding="utf-8")

    for path in (ROLLBACK, BOUNDARY, LIFECYCLE, CHECKPOINT_TEST):
        assert path.is_file(), path
    for marker in (
        "sandbox root containment",
        "path traversal and symlink escape",
        "materialization lineage",
        "rollback",
        "archive",
        "restore",
        "reset/delete",
        "partial failure",
        "idempotency",
        "already_rolled_back_integral",
        "tmp_path",
        "operational=false",
        "runtime_enabled=false",
        "execution_enabled=false",
    ):
        assert marker in doc


def test_b5_b_does_not_upgrade_unknown_archive_or_restore_into_product_capability():
    doc = DOC.read_text(encoding="utf-8")

    assert "not demonstrated; remains blocked" in doc
    assert "independent product restore is absent" in doc
    assert "does not add archive/restore APIs" in doc
    assert "product data migration" in doc
