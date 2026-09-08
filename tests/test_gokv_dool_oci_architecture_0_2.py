from pathlib import Path

from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]


def test_dool_oci_architecture_defines_the_new_boundary_without_runtime_claims():
    document = (ROOT / "docs" / "GOKV_DOOL_OCI_ARCHITECTURE_0_2.md").read_text(encoding="utf-8")

    assert "N1_GOKV_DOOL_OCI_ARCHITECTURE_PASSED" in document
    assert "DEVELOPMENT_ORIGIN" in document
    assert "FIELD_OPERATION" in document
    assert "EACH_STAGE_BUILDS_THE_SYSTEM_AND_INCREASES_THE_CAPABILITY_OF_THE_NEXT" in document
    assert "DEVELOPMENT_TIME_OCI_V1" in document
    assert "UI/UX 1.200 execution" in document


def test_dool_oci_audit_preserves_gokv_01_inventory():
    validation = validate_vault(default_paths(ROOT))

    assert validation["valid"] is True
    assert validation["item_count"] == 23
    assert validation["status_counts"] == {"CANDIDATE": 7, "PROMOTED": 7, "VALIDATED": 9}
