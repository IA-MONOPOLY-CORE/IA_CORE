"""Deterministic validation for the inert IA_CORE cognitive kernel graph.

The kernel graph is a development-time contract over the existing GOKV
foundation. Loading or validating it has no runtime, provider, permission,
tenant, model, network, or persistence side effects.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any, Mapping


KERNEL_SCHEMA_VERSION = "ia_core.cognitive_kernel.g0.v1"
KERNEL_MODE = "INERT_DEVELOPMENT_FOUNDATION"
FAMILY_IDS = frozenset({"GOKV", "DOOL", "OCI"})
GENERATION_IDS = (
    "G0_DEVELOPMENT_ORIGIN",
    "G1_BETA_OPERATIONAL_LEARNING",
    "G2_FIELD_OPERATIONAL_LEARNING",
    "GN_CONTINUOUS_EVOLUTION",
)
RELATION_TYPES = frozenset(
    {
        "derived_from",
        "confirms",
        "contradicts",
        "limits",
        "supersedes",
        "compatible_with",
        "tested_by",
        "inheritable_by",
        "requires",
        "improves",
        "degrades",
    }
)
PROVENANCE_CLASSES = frozenset(
    {"OBSERVED", "INFERRED", "OWNER_DIRECTED", "UNKNOWN", "EXTERNAL_EVIDENCE_REQUIRED"}
)
G0_STATUSES = frozenset({"OBSERVED", "CONTRACTED", "VALIDATED"})
FUTURE_STATUSES = frozenset({"CONTRACTED_NOT_MATERIALIZED"})
NODE_KINDS = frozenset(
    {
        "FAMILY_CONTRACT",
        "KNOWLEDGE_FOUNDATION",
        "DEVELOPMENT_LEARNING",
        "INHERITANCE_COMPILER",
        "OWNER_DIRECTION",
        "GENERATION_PLACEHOLDER",
    }
)
EDGE_STATUSES = frozenset({"CONTRACTED", "VALIDATED"})
CONFIDENTIALITY_CLASSES = frozenset({"global_inheritable", "ia_core_internal"})
ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def load_kernel_graph(path: Path) -> dict[str, Any]:
    """Load and validate one graph without writing or activating anything."""

    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    return validate_kernel_graph(value)


def validate_kernel_graph(graph: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the complete G0 graph and return a defensive copy."""

    if not isinstance(graph, Mapping):
        raise ValueError("kernel graph debe ser un objeto")
    required = {
        "schema_version",
        "kernel_id",
        "kernel_mode",
        "kernel_formula",
        "families",
        "generations",
        "relation_types",
        "invariants",
        "runtime_boundary",
        "nodes",
        "edges",
    }
    missing = required - set(graph)
    if missing:
        raise ValueError(f"kernel graph incompleto: {', '.join(sorted(missing))}")
    if graph["schema_version"] != KERNEL_SCHEMA_VERSION:
        raise ValueError("kernel schema_version invalida")
    _validate_id(graph["kernel_id"], "kernel_id")
    if graph["kernel_mode"] != KERNEL_MODE:
        raise ValueError("kernel mode invalido")
    _validate_string_list(graph["kernel_formula"], "kernel_formula")
    if graph["kernel_formula"] != [
        "IDENTITY",
        "CONTRACTS",
        "TYPED_CONNECTIONS",
        "GOVERNANCE",
        "INHERITANCE",
        "FEEDBACK",
    ]:
        raise ValueError("kernel_formula invalida")
    _validate_families(graph["families"])
    _validate_generations(graph["generations"])
    _validate_relation_types(graph["relation_types"])
    _validate_string_list(graph["invariants"], "invariants")
    _validate_runtime_boundary(graph["runtime_boundary"])

    nodes = _validate_nodes(graph["nodes"])
    node_ids = {node["node_id"] for node in nodes}
    _validate_edges(graph["edges"], node_ids)
    return deepcopy(dict(graph))


def _validate_families(value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError("families debe ser una lista")
    seen: set[str] = set()
    for family in value:
        if not isinstance(family, Mapping):
            raise ValueError("family debe ser un objeto")
        required = {"family_id", "orientation", "status", "contract_refs"}
        if not required <= set(family):
            raise ValueError("family incompleta")
        family_id = family["family_id"]
        if family_id not in FAMILY_IDS or family_id in seen:
            raise ValueError("family_id duplicado o invalido")
        seen.add(family_id)
        if family["orientation"] != "HORIZONTAL_PEER":
            raise ValueError("las familias GOKV/DOOL/OCI deben ser pares horizontales")
        if family["status"] not in {"CURRENT_CONTRACTED", "CURRENT_VALIDATED"}:
            raise ValueError("status de family invalido")
        _validate_nonempty_string_list(family["contract_refs"], "family.contract_refs")
    if seen != FAMILY_IDS:
        raise ValueError("el catalogo debe contener exactamente GOKV, DOOL y OCI")


def _validate_generations(value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError("generations debe ser una lista")
    seen: set[str] = set()
    for generation in value:
        if not isinstance(generation, Mapping):
            raise ValueError("generation debe ser un objeto")
        required = {"generation_id", "evidence_state", "materialization"}
        if not required <= set(generation):
            raise ValueError("generation incompleta")
        generation_id = generation["generation_id"]
        if generation_id not in GENERATION_IDS or generation_id in seen:
            raise ValueError("generation_id duplicado o invalido")
        seen.add(generation_id)
        if generation_id == "G0_DEVELOPMENT_ORIGIN":
            expected = ("REAL_EVIDENCE_ONLY", "ALLOWED_INERT_NODES")
        else:
            expected = ("NO_OPERATIONAL_EVIDENCE", "CONTRACTED_NOT_MATERIALIZED")
        if (generation["evidence_state"], generation["materialization"]) != expected:
            raise ValueError("estado de generation incompatible con su alcance")
    if tuple(generation["generation_id"] for generation in value) != GENERATION_IDS:
        raise ValueError("generations deben conservar el orden G0, G1, G2, Gn")


def _validate_relation_types(value: Any) -> None:
    _validate_string_list(value, "relation_types")
    if set(value) != RELATION_TYPES or len(value) != len(RELATION_TYPES):
        raise ValueError("relation_types debe contener el catalogo tipado exacto")


def _validate_runtime_boundary(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("runtime_boundary debe ser un objeto")
    expected = {
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
    if dict(value) != expected:
        raise ValueError("runtime_boundary debe permanecer completamente inerte")


def _validate_nodes(value: Any) -> list[Mapping[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ValueError("nodes debe ser una lista no vacia")
    seen: set[str] = set()
    nodes: list[Mapping[str, Any]] = []
    for node in value:
        if not isinstance(node, Mapping):
            raise ValueError("node debe ser un objeto")
        required = {
            "node_id",
            "family",
            "generation",
            "kind",
            "status",
            "scope",
            "provenance",
            "evidence_refs",
            "compatibility",
            "confidentiality_class",
            "created_at",
            "supersedes",
            "inheritance",
        }
        if not required <= set(node):
            raise ValueError("node incompleto")
        node_id = node["node_id"]
        _validate_id(node_id, "node_id")
        if node_id in seen:
            raise ValueError("node_id duplicado")
        seen.add(node_id)
        if node["family"] not in FAMILY_IDS:
            raise ValueError("node family invalida: el kernel no es una cuarta familia")
        if node["generation"] not in GENERATION_IDS:
            raise ValueError("node generation invalida")
        if node["kind"] not in NODE_KINDS:
            raise ValueError("node kind invalido")
        if node["generation"] == "G0_DEVELOPMENT_ORIGIN":
            if node["status"] not in G0_STATUSES:
                raise ValueError("G0 requiere status observado, contratado o validado")
            if not node["evidence_refs"]:
                raise ValueError("cada nodo G0 requiere evidencia real")
        else:
            if node["status"] not in FUTURE_STATUSES:
                raise ValueError("G1/G2/Gn solo pueden ser placeholders contratados")
            if node["evidence_refs"] != []:
                raise ValueError("G1/G2/Gn no pueden contener evidencia operativa ficticia")
            if node["kind"] != "GENERATION_PLACEHOLDER":
                raise ValueError("los nodos futuros deben ser placeholders")
        _validate_text(node["scope"], "node.scope")
        _validate_provenance(node["provenance"])
        _validate_evidence_refs(node["evidence_refs"])
        _validate_compatibility(node["compatibility"])
        if node["confidentiality_class"] not in CONFIDENTIALITY_CLASSES:
            raise ValueError("confidentiality_class no heredable o no reconocida")
        _validate_timestamp(node["created_at"], "node.created_at")
        _validate_id_list(node["supersedes"], "node.supersedes")
        _validate_inheritance(node["inheritance"])
        nodes.append(node)
    for node in nodes:
        if node["node_id"] in node["supersedes"]:
            raise ValueError("un nodo no puede supersederse a si mismo")
    return nodes


def _validate_edges(value: Any, node_ids: set[str]) -> None:
    if not isinstance(value, list):
        raise ValueError("edges debe ser una lista")
    seen: set[str] = set()
    for edge in value:
        if not isinstance(edge, Mapping):
            raise ValueError("edge debe ser un objeto")
        required = {
            "edge_id",
            "from_node",
            "to_node",
            "relation_type",
            "status",
            "evidence_refs",
            "constraints",
            "created_at",
        }
        if not required <= set(edge):
            raise ValueError("edge incompleta")
        _validate_id(edge["edge_id"], "edge_id")
        if edge["edge_id"] in seen:
            raise ValueError("edge_id duplicado")
        seen.add(edge["edge_id"])
        if edge["from_node"] not in node_ids or edge["to_node"] not in node_ids:
            raise ValueError("edge referencia un nodo inexistente")
        if edge["from_node"] == edge["to_node"]:
            raise ValueError("edge no puede ser reflexiva")
        if edge["relation_type"] not in RELATION_TYPES:
            raise ValueError("relation_type invalido")
        if edge["status"] not in EDGE_STATUSES:
            raise ValueError("edge status invalido")
        _validate_evidence_refs(edge["evidence_refs"])
        if not isinstance(edge["constraints"], Mapping):
            raise ValueError("edge.constraints debe ser un objeto")
        if edge["constraints"].get("cross_tenant") is not False:
            raise ValueError("las edges G0 no pueden habilitar cruce de tenant")
        _validate_timestamp(edge["created_at"], "edge.created_at")


def _validate_provenance(value: Any) -> None:
    if not isinstance(value, Mapping) or not {"classification", "sources", "claim"} <= set(value):
        raise ValueError("provenance incompleta")
    if value["classification"] not in PROVENANCE_CLASSES:
        raise ValueError("provenance classification invalida")
    _validate_nonempty_string_list(value["sources"], "provenance.sources")
    _validate_text(value["claim"], "provenance.claim")


def _validate_evidence_refs(value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError("evidence_refs debe ser una lista")
    for reference in value:
        if not isinstance(reference, Mapping):
            raise ValueError("evidence_ref debe ser un objeto")
        required = {"evidence_id", "kind", "ref", "claim", "classification"}
        if not required <= set(reference):
            raise ValueError("evidence_ref incompleta")
        _validate_id(reference["evidence_id"], "evidence_id")
        if reference["kind"] not in {"commit", "checkpoint", "test", "document", "metric"}:
            raise ValueError("evidence_ref.kind invalido")
        _validate_text(reference["ref"], "evidence_ref.ref")
        _validate_text(reference["claim"], "evidence_ref.claim")
        if reference["classification"] not in PROVENANCE_CLASSES:
            raise ValueError("evidence_ref.classification invalida")


def _validate_compatibility(value: Any) -> None:
    if not isinstance(value, Mapping) or not {"status", "compatible_with", "excluded"} <= set(value):
        raise ValueError("compatibility incompleta")
    if value["status"] not in {"CURRENT_COMPATIBLE", "FUTURE_CONTRACTED"}:
        raise ValueError("compatibility.status invalido")
    _validate_string_list(value["compatible_with"], "compatibility.compatible_with")
    _validate_string_list(value["excluded"], "compatibility.excluded")


def _validate_inheritance(value: Any) -> None:
    if not isinstance(value, Mapping) or not {"eligible", "requires", "excludes"} <= set(value):
        raise ValueError("inheritance incompleta")
    if not isinstance(value["eligible"], bool):
        raise ValueError("inheritance.eligible debe ser booleano")
    _validate_string_list(value["requires"], "inheritance.requires")
    _validate_string_list(value["excludes"], "inheritance.excludes")
    if value["eligible"] and not any(
        marker in " ".join(value["excludes"]).lower()
        for marker in ("raw secret", "plaintext", "tenant content", "private prompt", "chain-of-thought")
    ):
        raise ValueError("nodo heredable debe declarar exclusiones de contenido protegido")


def _validate_id_list(value: Any, field: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field} debe ser una lista")
    for item in value:
        _validate_id(item, field)


def _validate_nonempty_string_list(value: Any, field: str) -> None:
    _validate_string_list(value, field)
    if not value:
        raise ValueError(f"{field} no puede estar vacia")


def _validate_string_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field} debe ser una lista de strings")


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise ValueError(f"{field} invalido")


def _validate_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} debe ser texto no vacio")


def _validate_timestamp(value: Any, field: str) -> None:
    _validate_text(value, field)
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} debe ser ISO-8601") from exc
