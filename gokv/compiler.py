"""Deterministic, development-only compiler for GOKV Execution Packs."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from gokv.storage import VaultPaths, default_paths, iter_knowledge_items


EXECUTION_PACK_SCHEMA_VERSION = "gokv.execution_pack.v1"
COMPILER_VERSION = "gokv.compiler.v1"
PACK_MODES = frozenset({"PROMOTED_ONLY", "DEVELOPMENT_VALIDATED"})


def compile_execution_pack(
    request: Mapping[str, Any], paths: VaultPaths | None = None
) -> dict[str, Any]:
    """Compile a stable pack from explicit request data and vault records.

    The compiler only selects already-recorded knowledge. It never creates a
    knowledge item, promotes a lifecycle status, invokes a model, retrieves
    embeddings, or connects to product/runtime code.
    """

    normalized = _normalize_request(request)
    allowed_statuses = {
        "PROMOTED" if normalized["mode"] == "PROMOTED_ONLY" else "PROMOTED",
    }
    if normalized["mode"] == "DEVELOPMENT_VALIDATED":
        allowed_statuses.add("VALIDATED")

    selected = [
        item
        for item in iter_knowledge_items(paths or default_paths())
        if item["status"] in allowed_statuses and _matches(item, normalized)
    ]
    selected.sort(key=lambda item: item["knowledge_id"])
    ids = [item["knowledge_id"] for item in selected]
    pack_id = "gokv.pack." + sha256(
        json.dumps({"request": normalized, "knowledge_ids": ids}, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]

    pack = {
        "execution_pack_id": pack_id,
        "schema_version": EXECUTION_PACK_SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
        "mode": normalized["mode"],
        "mission_class": normalized["mission_class"],
        "task_type": normalized["task_type"],
        "scope": normalized["scope"],
        "risk_class": normalized["risk_class"],
        "required_capabilities": normalized["required_capabilities"],
        "agent_class": normalized["agent_class"],
        "model_size_class": normalized["model_size_class"],
        "tags": normalized["tags"],
        "allowed_statuses": sorted(allowed_statuses),
        "applicable_knowledge_ids": ids,
        "principles": _principles(selected),
        "procedures": _procedures(selected),
        "decision_rules": _rules(selected, "decision_rules"),
        "stop_conditions": _rules(selected, "stop_conditions"),
        "validation_rules": _rules(selected, "validation"),
        "failure_modes": _rules(selected, "failure_modes"),
        "recovery": _rules(selected, "recovery"),
        "output_contract": {
            "format": "structured_json",
            "runtime_enabled": False,
            "execution_enabled": False,
            "payload_enabled": False,
            "requires_explicit_human_approval": True,
        },
        "evidence_summary": {
            "item_count": len(selected),
            "evidence_ref_count": sum(len(item["evidence_refs"]) for item in selected),
            "source_commit_count": sum(len(item["source_commits"]) for item in selected),
            "source_checkpoint_count": sum(len(item["source_checkpoints"]) for item in selected),
            "measured_metrics_available": False,
            "notes": [
                "Selection is deterministic and development-time only.",
                "No candidate, deprecated, or replaced item is selected implicitly.",
            ],
        },
        "selection_policy": {
            "scope_compatibility": [normalized["scope"], "GLOBAL"],
            "privacy_compatibility": [normalized["privacy_class"], "global_public"],
            "excluded_statuses": ["CANDIDATE", "DEPRECATED", "REPLACED", "OBSERVED", "REVISED"],
        },
    }
    if "mission_type_aliases" in normalized:
        pack["mission_type_aliases"] = normalized["mission_type_aliases"]
    if "knowledge_id_allowlist" in normalized:
        pack["knowledge_id_allowlist"] = normalized["knowledge_id_allowlist"]
    return validate_execution_pack(pack)


def validate_execution_pack(pack: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the compiler output without activating it."""

    required = {
        "execution_pack_id",
        "schema_version",
        "compiler_version",
        "mode",
        "mission_class",
        "task_type",
        "scope",
        "risk_class",
        "required_capabilities",
        "agent_class",
        "model_size_class",
        "tags",
        "allowed_statuses",
        "applicable_knowledge_ids",
        "principles",
        "procedures",
        "decision_rules",
        "stop_conditions",
        "validation_rules",
        "failure_modes",
        "recovery",
        "output_contract",
        "evidence_summary",
        "selection_policy",
    }
    missing = required - set(pack)
    if missing:
        raise ValueError(f"execution_pack incompleto: {', '.join(sorted(missing))}")
    if pack["schema_version"] != EXECUTION_PACK_SCHEMA_VERSION:
        raise ValueError("schema_version de execution_pack invalida")
    if pack["compiler_version"] != COMPILER_VERSION:
        raise ValueError("compiler_version invalida")
    if pack["mode"] not in PACK_MODES:
        raise ValueError("mode de execution_pack invalido")
    if not isinstance(pack["execution_pack_id"], str) or not pack["execution_pack_id"].startswith("gokv.pack."):
        raise ValueError("execution_pack_id invalido")
    for field in (
        "required_capabilities",
        "tags",
        "allowed_statuses",
        "applicable_knowledge_ids",
    ):
        _require_string_list(pack[field], field)
    if pack["applicable_knowledge_ids"] != sorted(pack["applicable_knowledge_ids"]):
        raise ValueError("applicable_knowledge_ids debe estar ordenado")
    if any(status not in {"PROMOTED", "VALIDATED"} for status in pack["allowed_statuses"]):
        raise ValueError("allowed_statuses contiene un estado no compilable")
    if pack["mode"] == "PROMOTED_ONLY" and pack["allowed_statuses"] != ["PROMOTED"]:
        raise ValueError("PROMOTED_ONLY requiere solo PROMOTED")
    if pack["mode"] == "DEVELOPMENT_VALIDATED" and pack["allowed_statuses"] != ["PROMOTED", "VALIDATED"]:
        raise ValueError("DEVELOPMENT_VALIDATED requiere PROMOTED y VALIDATED")
    for field in (
        "principles",
        "procedures",
        "decision_rules",
        "stop_conditions",
        "validation_rules",
        "failure_modes",
        "recovery",
    ):
        if not isinstance(pack[field], list):
            raise ValueError(f"{field} debe ser una lista")
    contract = pack["output_contract"]
    if not isinstance(contract, dict) or contract != {
        "format": "structured_json",
        "runtime_enabled": False,
        "execution_enabled": False,
        "payload_enabled": False,
        "requires_explicit_human_approval": True,
    }:
        raise ValueError("output_contract invalido")
    summary = pack["evidence_summary"]
    if not isinstance(summary, dict) or summary.get("measured_metrics_available") is not False:
        raise ValueError("evidence_summary debe declarar metricas no medidas")
    return json.loads(json.dumps(pack, ensure_ascii=False))


def save_execution_pack(pack: Mapping[str, Any], paths: VaultPaths | None = None) -> Path:
    """Append one compiled pack to the development-only pack directory."""

    validated = validate_execution_pack(pack)
    vault = paths or default_paths()
    vault.ensure()
    destination = vault.packs_dir / f"{validated['execution_pack_id']}.json"
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise ValueError(f"execution_pack duplicado: {destination.stem}") from exc
    return destination


def _normalize_request(request: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(request, Mapping):
        raise ValueError("compile request debe ser un objeto")

    def text(name: str, default: str | None = None) -> str:
        value = request.get(name, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} debe ser texto no vacio")
        return value.strip()

    def strings(name: str) -> list[str]:
        value = request.get(name, [])
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            raise ValueError(f"{name} debe ser una lista de strings no vacios")
        return sorted(set(item.strip() for item in value))

    mode = text("mode", "PROMOTED_ONLY")
    if mode not in PACK_MODES:
        raise ValueError(f"mode invalido: {mode}")
    normalized = {
        "mission_class": text("mission_class"),
        "task_type": text("task_type", "general"),
        "scope": text("scope", "IA_CORE_BUILD"),
        "privacy_class": text("privacy_class", "ia_core_internal"),
        "risk_class": text("risk_class", "LOW"),
        "required_capabilities": strings("required_capabilities"),
        "agent_class": text("agent_class", "BUILD_AGENT"),
        "model_size_class": text("model_size_class", "SMALL"),
        "tags": strings("tags"),
        "mode": mode,
    }
    for optional_name in ("mission_type_aliases", "knowledge_id_allowlist"):
        if optional_name in request:
            values = strings(optional_name)
            if values:
                normalized[optional_name] = values
    return normalized


def _matches(item: Mapping[str, Any], request: Mapping[str, Any]) -> bool:
    if item["scope"] not in {request["scope"], "GLOBAL"}:
        return False
    if item["privacy_class"] not in {request["privacy_class"], "global_public"}:
        return False
    applicability = item.get("applicability", {})
    mission_types = set(applicability.get("mission_types", []))
    requested_missions = {request["mission_class"], *request.get("mission_type_aliases", [])}
    if mission_types and not requested_missions.intersection(mission_types) and "all_development" not in mission_types:
        return False
    scoped = set(applicability.get("scopes", []))
    if scoped and request["scope"] not in scoped and "GLOBAL" not in scoped:
        return False
    task_types = set(applicability.get("task_types", []))
    if task_types and request["task_type"] not in task_types:
        return False
    capabilities = set(applicability.get("capabilities", []))
    if request["required_capabilities"] and not set(request["required_capabilities"]).issubset(capabilities):
        return False
    if request["tags"] and not set(request["tags"]).intersection(item["tags"]):
        return False
    if request.get("knowledge_id_allowlist") and item["knowledge_id"] not in request["knowledge_id_allowlist"]:
        return False
    return True


def _principles(items: list[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {"knowledge_id": item["knowledge_id"], "summary": item["summary"]}
        for item in items
        if item["kind"] == "PRINCIPLE"
    ]


def _procedures(items: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"knowledge_id": item["knowledge_id"], "title": item["title"], "steps": item["procedure"]}
        for item in items
        if item["procedure"]
    ]


def _rules(items: list[Mapping[str, Any]], field: str) -> list[dict[str, Any]]:
    return [
        {"knowledge_id": item["knowledge_id"], "rules": item[field]}
        for item in items
        if item[field]
    ]


def _require_string_list(value: Any, field: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} debe ser una lista de strings")
