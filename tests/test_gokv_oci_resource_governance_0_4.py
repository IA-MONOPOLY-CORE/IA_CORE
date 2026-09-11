from pathlib import Path

import pytest

from gokv.compiler import compile_execution_pack
from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]


def _request(**overrides):
    request = {
        "mission_class": "development_foundation",
        "task_type": "bootstrap",
        "scope": "IA_CORE_BUILD",
        "privacy_class": "ia_core_internal",
        "risk_class": "HIGH",
        "required_capabilities": [],
        "agent_class": "BUILD_AGENT",
        "model_size_class": "SMALL",
        "tags": ["gates"],
        "mode": "DEVELOPMENT_VALIDATED",
    }
    request.update(overrides)
    return request


def test_explicit_item_budget_is_deterministic_and_records_relevant_omissions():
    request = _request(
        resource_budget={
            "max_items": 1,
            "priority_knowledge_ids": ["internal_gates"],
        }
    )
    first = compile_execution_pack(request, default_paths(ROOT))
    second = compile_execution_pack(request, default_paths(ROOT))

    assert first == second
    assert first["resource_budget"]["explicit"] is True
    assert first["applicable_knowledge_ids"] == ["internal_gates"]
    assert first["evidence_summary"]["relevant_item_count"] == 2
    assert first["evidence_summary"]["omitted_relevant_items"] == [
        {
            "knowledge_id": "controlled_assembled_block_execution",
            "reason": "RESOURCE_BUDGET_MAX_ITEMS",
        }
    ]
    assert first["selection_policy"]["relevance_omission_requires_reason"] is True
    assert first["output_contract"]["runtime_enabled"] is False


def test_legacy_request_shape_and_pack_id_remain_unchanged_without_budget():
    pack = compile_execution_pack(_request(), default_paths(ROOT))

    assert "resource_budget" not in pack
    assert "relevant_item_count" not in pack["evidence_summary"]
    assert "relevance_omission_requires_reason" not in pack["selection_policy"]


def test_byte_budget_can_skip_an_item_without_silent_loss():
    pack = compile_execution_pack(
        _request(resource_budget={"max_serialized_bytes": 1}),
        default_paths(ROOT),
    )

    assert pack["applicable_knowledge_ids"] == []
    assert len(pack["evidence_summary"]["omitted_relevant_items"]) == 2
    assert {
        entry["reason"] for entry in pack["evidence_summary"]["omitted_relevant_items"]
    } == {"RESOURCE_BUDGET_MAX_SERIALIZED_BYTES"}


@pytest.mark.parametrize(
    "budget",
    [
        {"max_items": -1},
        {"max_serialized_bytes": True},
        {"priority_knowledge_ids": ["", 1]},
    ],
)
def test_invalid_resource_budget_is_rejected(budget):
    with pytest.raises(ValueError, match="resource_budget"):
        compile_execution_pack(_request(resource_budget=budget), default_paths(ROOT))
