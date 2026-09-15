from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from gokv.kernel import (
    FAMILY_IDS,
    GENERATION_IDS,
    KERNEL_SCHEMA_VERSION,
    RELATION_TYPES,
    load_kernel_graph,
    validate_kernel_graph,
)


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json"
SCHEMA_PATH = ROOT / "knowledge" / "global_operational" / "schema" / "cognitive_kernel_g0.schema.json"


def graph() -> dict:
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def test_g0_graph_is_canonical_inert_and_complete():
    value = load_kernel_graph(GRAPH_PATH)

    assert value["schema_version"] == KERNEL_SCHEMA_VERSION
    assert {family["family_id"] for family in value["families"]} == FAMILY_IDS
    assert [generation["generation_id"] for generation in value["generations"]] == list(GENERATION_IDS)
    assert set(value["relation_types"]) == RELATION_TYPES
    assert value["kernel_mode"] == "INERT_DEVELOPMENT_FOUNDATION"
    assert value["runtime_boundary"] == {
        "runtime_enabled": False,
        "provider_calls_allowed": False,
        "external_calls_allowed": False,
        "permission_grants": False,
        "automatic_promotion": False,
        "tenant_reads": False,
        "raw_secret_reads": False,
        "model_training": False,
        "payload_enabled": False,
    }


def test_g0_nodes_have_evidence_and_future_generations_have_none():
    value = graph()
    nodes = value["nodes"]
    assert all(node["evidence_refs"] for node in nodes if node["generation"] == "G0_DEVELOPMENT_ORIGIN")
    assert all(node["evidence_refs"] == [] for node in nodes if node["generation"] != "G0_DEVELOPMENT_ORIGIN")
    assert all(node["kind"] == "GENERATION_PLACEHOLDER" for node in nodes if node["generation"] != "G0_DEVELOPMENT_ORIGIN")
    assert all(node["family"] in FAMILY_IDS for node in nodes)
    assert not any(node["family"] in {"KERNEL", "COGNITIVE_KERNEL"} for node in nodes)


def test_edges_are_typed_non_orphaned_and_non_cross_tenant():
    value = graph()
    node_ids = {node["node_id"] for node in value["nodes"]}
    assert value["edges"]
    assert all(edge["from_node"] in node_ids and edge["to_node"] in node_ids for edge in value["edges"])
    assert all(edge["from_node"] != edge["to_node"] for edge in value["edges"])
    assert all(edge["constraints"]["cross_tenant"] is False for edge in value["edges"])


def test_schema_is_parseable_and_graph_validation_is_defensive():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$id"] == KERNEL_SCHEMA_VERSION
    value = graph()
    validated = validate_kernel_graph(value)
    validated["nodes"].clear()
    assert value["nodes"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value["families"].append({"family_id": "KERNEL", "orientation": "HORIZONTAL_PEER", "status": "CURRENT_CONTRACTED", "contract_refs": ["x"]}), "family_id"),
        (lambda value: value["nodes"][0].update({"node_id": "duplicate_node"}) or value["nodes"][1].update({"node_id": "duplicate_node"}), "node_id"),
        (lambda value: value["edges"][0].update({"to_node": "missing_node"}), "inexistente"),
        (lambda value: value["nodes"][0].update({"evidence_refs": []}), "evidencia real"),
        (lambda value: value["nodes"][-1].update({"evidence_refs": [{"evidence_id": "fake", "kind": "document", "ref": "fake", "claim": "fake", "classification": "OBSERVED"}]}), "ficticia"),
        (lambda value: value["runtime_boundary"].update({"runtime_enabled": True}), "inerte"),
        (lambda value: value["nodes"][0].update({"confidentiality_class": "enterprise_confidential"}), "confidentiality_class"),
    ],
)
def test_invalid_graphs_fail_closed(mutation, message):
    value = deepcopy(graph())
    mutation(value)
    with pytest.raises(ValueError, match=message):
        validate_kernel_graph(value)
