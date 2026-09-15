from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from gokv.kernel import load_kernel_graph, validate_kernel_graph


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json"
SCHEMA = ROOT / "knowledge" / "global_operational" / "schema" / "cognitive_kernel_g0.schema.json"
SECURITY_IDS = {
    "gokv_g0_defensive_knowledge_contract": "GOKV",
    "dool_g0_security_control_learning": "DOOL",
    "oci_g0_necessary_sufficient_security_composition": "OCI",
}


def graph() -> dict:
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def node(value: dict, node_id: str) -> dict:
    return next(item for item in value["nodes"] if item["node_id"] == node_id)


def test_security_g0_positive_path_is_canonical_and_inert():
    value = load_kernel_graph(GRAPH)
    assert len(value["nodes"]) == 13
    assert len(value["edges"]) == 10
    assert {node["node_id"]: node["family"] for node in value["nodes"] if node["node_id"] in SECURITY_IDS} == SECURITY_IDS
    assert all(
        next(node for node in value["nodes"] if node["node_id"] == node_id)["generation"]
        == "G0_DEVELOPMENT_ORIGIN"
        for node_id in SECURITY_IDS
    )
    assert value["security_contract"]["native_operating_plane"] is True
    assert value["security_contract"]["offensive_artifact_production"] is False
    assert value["security_contract"]["future_cyber_range_state"] == "FUTURE_CONCEPT_PRESERVED_NOT_SCHEDULED_NOT_IMPLEMENTED"
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


def test_security_g0_contracts_and_edges_are_complete():
    value = graph()
    invariants = set(value["invariants"])
    assert {
        "SECURITY_IS_A_NATIVE_OPERATING_PLANE",
        "SECURITY_BY_DESIGN_NOT_SECURITY_AS_AN_ADD_ON",
        "DEFENSE_IN_DEPTH_OVER_SINGLE_PRODUCT_DEPENDENCE",
        "AI_ASSISTS_SECURITY_DETERMINISTIC_CONTROLS_ENFORCE_IT",
        "SECURITY_STRENGTH_MUST_BE_MEASURED_NOT_MARKETED",
        "UNTRUSTED_SECURITY_REPOSITORIES_ARE_EVIDENCE_NOT_AUTHORITY",
        "NO_OFFENSIVE_ARTIFACT_REACHES_PRODUCTION_UNSANDBOXED",
        "NO_EXTERNAL_SECURITY_CORPUS_IS_AUTO_PROMOTED",
        "EVERY_NEW_ENTITY_INHERITS_VALIDATED_DEFENSIVE_LEARNING",
        "DOMAIN_MODULES_HAVE_PARITY_NO_DOMAIN_HAS_INHERENT_PLATFORM_PRIVILEGE",
    } <= invariants
    edge_types = {(edge["from_node"], edge["to_node"], edge["relation_type"]) for edge in value["edges"]}
    assert ("gokv_g0_defensive_knowledge_contract", "gokv_family_contract", "derived_from") in edge_types
    assert ("dool_g0_security_control_learning", "dool_g0_method_learning", "derived_from") in edge_types
    assert ("oci_g0_necessary_sufficient_security_composition", "gokv_g0_defensive_knowledge_contract", "requires") in edge_types
    assert ("dool_g0_security_control_learning", "oci_g0_necessary_sufficient_security_composition", "inheritable_by") in edge_types
    assert all(edge["constraints"]["cross_tenant"] is False for edge in value["edges"])
    oci = next(node for node in value["nodes"] if node["node_id"] == "oci_g0_necessary_sufficient_security_composition")
    assert "NECESSARY_AND_SUFFICIENT_INHERITANCE" in oci["inheritance"]["requires"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value["security_contract"].update({"native_operating_plane": False}), "security_contract"),
        (lambda value: value["invariants"].remove("SECURITY_IS_A_NATIVE_OPERATING_PLANE"), "invariantes de seguridad"),
        (lambda value: node(value, "gokv_g0_defensive_knowledge_contract").update({"family": "KERNEL"}), "family invalida"),
        (lambda value: node(value, "oci_g0_necessary_sufficient_security_composition")["inheritance"]["requires"].remove("NECESSARY_AND_SUFFICIENT_INHERITANCE"), "necesaria y suficiente"),
        (lambda value: node(value, "gokv_g0_defensive_knowledge_contract").update({"evidence_refs": []}), "cada nodo G0 requiere evidencia real"),
        (lambda value: value["runtime_boundary"].update({"provider_calls_allowed": True}), "inerte"),
        (lambda value: value["security_contract"].update({"offensive_artifact_production": True}), "security_contract"),
        (lambda value: node(value, "gokv_g0_defensive_knowledge_contract")["inheritance"].update({"excludes": []}), "exclusiones"),
    ],
)
def test_adversarial_security_mutations_fail_closed(mutation, message):
    value = deepcopy(graph())
    mutation(value)
    with pytest.raises(ValueError, match=message):
        validate_kernel_graph(value)


def test_malformed_json_and_schema_mutations_fail_closed(tmp_path):
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        load_kernel_graph(malformed)
    value = deepcopy(graph())
    value["schema_version"] = "wrong.schema.v0"
    with pytest.raises(ValueError, match="schema_version"):
        validate_kernel_graph(value)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["$id"] == "ia_core.cognitive_kernel.g0.v1"


def test_future_and_offensive_boundaries_remain_non_materialized():
    value = graph()
    future = [node for node in value["nodes"] if node["generation"] != "G0_DEVELOPMENT_ORIGIN"]
    assert future
    assert all(node["evidence_refs"] == [] for node in future)
    assert all(node["kind"] == "GENERATION_PLACEHOLDER" for node in future)
    assert not any("offensive" in json.dumps(node).lower() for node in future)
    assert "FUTURE_CONCEPT_PRESERVED_NOT_SCHEDULED_NOT_IMPLEMENTED" in json.dumps(value["security_contract"])
