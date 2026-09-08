import json
from pathlib import Path

import pytest

from gokv.compiler import compile_execution_pack, validate_execution_pack
from gokv.storage import default_paths


FIXTURES = Path(__file__).parent / "fixtures" / "gokv"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_compiler_is_deterministic_and_validated_mode_selects_only_compatible_items():
    request = _fixture("fixture_a_ui_ux.json")
    first = compile_execution_pack(request, default_paths(Path.cwd()))
    second = compile_execution_pack(request, default_paths(Path.cwd()))

    assert first == second
    assert first["mode"] == "DEVELOPMENT_VALIDATED"
    assert first["applicable_knowledge_ids"] == [
        "contract_over_ui_inference",
        "preserve_contract_until_explicit_change",
        "true_hard_frontier",
    ]
    assert first["output_contract"]["runtime_enabled"] is False
    assert first["output_contract"]["execution_enabled"] is False
    assert first["output_contract"]["payload_enabled"] is False
    validate_execution_pack(first)


def test_promoted_only_selects_only_currently_promoted_records():
    pack = compile_execution_pack(_fixture("fixture_b_default_promoted_only.json"), default_paths(Path.cwd()))

    assert pack["allowed_statuses"] == ["PROMOTED"]
    assert pack["applicable_knowledge_ids"] == [
        "evidence_before_closure",
        "focal_group_canonical_deep_test_policy",
        "real_diff_over_planned_commit_name",
        "station_local_commits",
        "true_hard_frontier",
    ]
    assert pack["evidence_summary"]["item_count"] == 5


def test_tag_filter_is_explicit_and_stable():
    pack = compile_execution_pack(_fixture("fixture_c_tag_filter.json"), default_paths(Path.cwd()))

    assert pack["applicable_knowledge_ids"] == [
        "controlled_assembled_block_execution",
        "internal_gates",
    ]
    assert pack["tags"] == ["gates"]


def test_required_capability_without_evidence_selects_nothing():
    pack = compile_execution_pack(_fixture("fixture_d_capability_mismatch.json"), default_paths(Path.cwd()))

    assert pack["applicable_knowledge_ids"] == []


def test_invalid_mode_and_tampered_contract_are_rejected():
    with pytest.raises(ValueError, match="mode invalido"):
        compile_execution_pack({"mission_class": "ui_ux", "mode": "AUTONOMOUS"})

    pack = compile_execution_pack(_fixture("fixture_a_ui_ux.json"), default_paths(Path.cwd()))
    pack["output_contract"]["execution_enabled"] = True
    with pytest.raises(ValueError, match="output_contract invalido"):
        validate_execution_pack(pack)
