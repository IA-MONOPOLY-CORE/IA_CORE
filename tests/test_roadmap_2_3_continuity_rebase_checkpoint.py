import json
from pathlib import Path

from gokv.inheritance import validate_development_oci_pack
from gokv.manifest import validate_next_mission_inheritance_manifest


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs/ROADMAP_2_X_CONTINUITY_REBASE_CHECKPOINT.md"
HANDOFF = ROOT / "docs/ROADMAP_3_0_BACKEND_ELITE_AUDIT_HANDOFF.md"
MANIFEST = ROOT / "knowledge/global_operational/packs/next_mission_manifest_roadmap_3_0_backend_elite_read_only_inventory.json"
PACK = ROOT / "knowledge/global_operational/packs/oci/gokv.pack.419ba7a247ea447f_roadmap_2_x_continuity_rebase_after_ui_ux_current_line_closure.json"
README = ROOT / "README.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_checkpoint_and_backend_handoff_gates_are_closed():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    assert "ROADMAP_2_3_CONTINUITY_REBASE_CHECKPOINT_PASSED" in checkpoint
    assert "ROADMAP_2_X_CONTINUITY_REBASE_PASSED" in checkpoint
    assert "BACKEND_3_X_ENTRY_READY" in handoff
    assert "not executed" in handoff


def test_next_manifest_and_oci_pack_validate_without_product_authority():
    manifest = validate_next_mission_inheritance_manifest(_load(MANIFEST))
    pack = validate_development_oci_pack(_load(PACK))
    assert manifest["mission_id"] == "roadmap_3_0_backend_elite_read_only_inventory"
    assert manifest["execution_pack_id"] == "gokv.pack.419ba7a247ea447f"
    assert manifest["mode"] == "PROMOTED_ONLY"
    assert manifest["validated_items_selected"] == []
    assert manifest["candidate_items_selected"] == []
    assert pack["execution_pack_id"] == "gokv.pack.419ba7a247ea447f"
    assert pack["allowed_statuses"] == ["PROMOTED"]
    assert pack["output_contract"]["runtime_enabled"] is False
    assert pack["output_contract"]["execution_enabled"] is False


def test_checkpoint_preserves_the_product_boundary():
    checkpoint = CHECKPOINT.read_text(encoding="utf-8")
    for marker in (
        "Product diff throughout 2.x: `EMPTY`",
        "must not modify UI",
        "runtime, execution, providers",
        "operational writes",
    ):
        assert marker in checkpoint


def test_readme_exposes_the_current_roadmap_cursor_without_erasing_history():
    readme = README.read_text(encoding="utf-8")
    assert "Cursor vigente Roadmap 2.x" in readme
    assert "roadmap_3_0_backend_elite_read_only_inventory" in readme
    assert "Cursor vigente UI/UX 1.188" in readme
