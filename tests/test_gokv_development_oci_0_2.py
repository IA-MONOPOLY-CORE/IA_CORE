import json
from pathlib import Path

import pytest

from gokv.compiler import compile_execution_pack
from gokv.inheritance import (
    AUTHORITY_PRECEDENCE,
    append_knowledge_conflict_event,
    append_oci_consumption_result,
    build_knowledge_conflict_event,
    build_oci_consumption_result,
    compile_development_oci_pack,
    validate_development_oci_pack,
)
from gokv.storage import VaultPaths, default_paths


ROOT = Path(__file__).resolve().parents[1]


def request():
    return {
        "mission_id": "gokv_0_2_n5_self_inspection",
        "mission_class": "development_foundation",
        "task_type": "bootstrap",
        "scope": "IA_CORE_BUILD",
        "risk_class": "HIGH",
        "required_capabilities": [],
        "agent_class": "BUILD_AGENT",
        "model_size_class": "SMALL",
        "tags": ["gates"],
        "mode": "DEVELOPMENT_VALIDATED",
    }


def test_development_oci_pack_is_explicit_and_current_contract_wins():
    pack = compile_development_oci_pack(request(), default_paths(ROOT))

    assert pack["inheritance_mode"] == "DEVELOPMENT_TIME_OCI_V1"
    assert pack["authority_precedence"] == AUTHORITY_PRECEDENCE
    assert pack["conflict_policy"]["id"] == "CURRENT_CONTRACT_WINS"
    assert pack["conflict_policy"]["silent_application"] is False
    assert pack["operational_guidance_only"] is True
    assert validate_development_oci_pack(pack)["mission_id"] == "gokv_0_2_n5_self_inspection"
    stored_pack = json.loads(
        (ROOT / "knowledge/global_operational/packs/oci/gokv.pack.3d734103e4e0731d_gokv_0_2_n5_self_inspection.json").read_text(encoding="utf-8")
    )
    stored_result = json.loads(
        (ROOT / "knowledge/global_operational/events/oci_consumption/gokv_0_2_n5_consumption.json").read_text(encoding="utf-8")
    )
    assert stored_pack == pack
    assert stored_result["result"] == "INSPECTION_ONLY"


def test_oci_requires_explicit_development_validated_mode():
    invalid = request()
    invalid["mode"] = "PROMOTED_ONLY"
    with pytest.raises(ValueError, match="DEVELOPMENT_VALIDATED"):
        compile_development_oci_pack(invalid, default_paths(ROOT))


def test_consumption_result_records_observable_use_without_inventing_savings():
    pack = compile_development_oci_pack(request(), default_paths(ROOT))
    result = build_oci_consumption_result(
        consumption_id="gokv_0_2_n5_consumption",
        pack=pack,
        mission_id=request()["mission_id"],
        knowledge_items_applied=[],
        knowledge_items_unused=pack["applicable_knowledge_ids"],
        result="INSPECTION_ONLY",
        created_at="2026-09-08T00:00:00+00:00",
    )

    assert result["pack_item_count"] == len(pack["applicable_knowledge_ids"])
    assert result["pack_size_bytes"] > 0
    assert result["knowledge_items_applied"] == []
    assert "reasoning_saved" not in result


def test_conflict_event_excludes_knowledge_and_is_append_only(tmp_path):
    paths = VaultPaths(tmp_path / "vault")
    event = build_knowledge_conflict_event(
        event_id="conflict_fixture",
        mission_id="mission_fixture",
        knowledge_id="conditioned_autonomy",
        conflict_field="allowed_action",
        current_contract_reference="current_contract_fixture",
        created_at="2026-09-08T00:00:00+00:00",
    )
    destination = append_knowledge_conflict_event(event, paths)
    assert json.loads(destination.read_text(encoding="utf-8"))["knowledge_applied"] is False
    with pytest.raises(ValueError, match="duplicado"):
        append_knowledge_conflict_event(event, paths)

    pack = compile_development_oci_pack(request(), default_paths(ROOT))
    result = build_oci_consumption_result(
        consumption_id="consumption_fixture",
        pack=pack,
        mission_id=request()["mission_id"],
        knowledge_items_conflicted=["conditioned_autonomy"],
    )
    assert append_oci_consumption_result(result, paths).is_file()


def test_optional_compiler_allowlist_keeps_shadow_selection_minimal():
    pack = compile_execution_pack(
        {
            **request(),
            "knowledge_id_allowlist": ["internal_gates"],
        },
        default_paths(ROOT),
    )
    assert pack["applicable_knowledge_ids"] == ["internal_gates"]
