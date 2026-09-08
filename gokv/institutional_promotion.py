"""Development-only, explicitly authorized GOKV lifecycle promotion."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from gokv.promotion import validate_promotion_assessment
from gokv.schema import transition_knowledge_item, validate_knowledge_item
from gokv.storage import VaultPaths, default_paths, rebuild_index, iter_knowledge_items


AUTHORIZATION_SCHEMA_VERSION = "gokv.promotion_authorization.v1"
PROMOTION_EVENT_SCHEMA_VERSION = "gokv.promotion_event.v1"
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_WILDCARDS = {"*", "all", "all_validated", "promotion_ready", "validated", "promoted"}
_PRESERVED_FIELDS = (
    "knowledge_id",
    "schema_version",
    "knowledge_version",
    "kind",
    "title",
    "summary",
    "scope",
    "applicability",
    "preconditions",
    "procedure",
    "decision_rules",
    "stop_conditions",
    "validation",
    "failure_modes",
    "recovery",
    "evidence_refs",
    "source_commits",
    "source_checkpoints",
    "metrics_refs",
    "confidence",
    "privacy_class",
    "tags",
    "created_at",
    "supersedes",
    "superseded_by",
    "learning_origin",
    "lineage",
)


def validate_promotion_authorization(authorization: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "authorization_id",
        "schema_version",
        "authorized_by",
        "authorization_type",
        "source_context",
        "source_assessment",
        "decision_timestamp",
        "authorized_knowledge_ids",
        "explicitly_deferred_knowledge_ids",
        "direction_approval_ids",
        "scope_constraints",
        "provenance_constraints",
        "automatic_promotion",
        "product_changes_authorized",
        "ui_ux_1_202_execution_authorized",
        "pre_promotion_gate",
        "notes",
    }
    if not isinstance(authorization, Mapping) or not required <= set(authorization):
        raise ValueError("promotion authorization incompleta")
    if authorization["schema_version"] != AUTHORIZATION_SCHEMA_VERSION:
        raise ValueError("promotion authorization schema invalido")
    _validate_id(authorization["authorization_id"], "authorization_id")
    for field in ("source_context", "source_assessment"):
        _validate_text(authorization[field], field)
    _validate_timestamp(authorization["decision_timestamp"], "decision_timestamp")
    if authorization["authorized_by"] != "DIRECTION":
        raise ValueError("authorized_by debe ser DIRECTION")
    if authorization["authorization_type"] != "KNOWLEDGE_PROMOTION":
        raise ValueError("authorization_type invalido")
    for field in (
        "authorized_knowledge_ids",
        "explicitly_deferred_knowledge_ids",
        "direction_approval_ids",
    ):
        _validate_id_list(authorization[field], field, allow_empty=field != "authorized_knowledge_ids")
        if len(authorization[field]) != len(set(authorization[field])):
            raise ValueError(f"{field} contiene IDs duplicados")
        if any(value.lower() in _WILDCARDS for value in authorization[field]):
            raise ValueError(f"{field} no puede usar wildcard")
    authorized = set(authorization["authorized_knowledge_ids"])
    deferred = set(authorization["explicitly_deferred_knowledge_ids"])
    directional = set(authorization["direction_approval_ids"])
    if authorized & deferred:
        raise ValueError("un ID no puede estar autorizado y diferido")
    if not directional <= authorized:
        raise ValueError("direction_approval_ids debe estar dentro de authorized_knowledge_ids")
    scope = authorization["scope_constraints"]
    if scope != {
        "required_scope": "IA_CORE_BUILD",
        "preserve_scope": True,
        "allow_scope_widening": False,
    }:
        raise ValueError("scope_constraints invalidas")
    provenance = authorization["provenance_constraints"]
    if provenance != {
        "required_learning_origin": "DEVELOPMENT_ORIGIN",
        "preserve_learning_origin": True,
        "allow_origin_change": False,
    }:
        raise ValueError("provenance_constraints invalidas")
    for field in (
        "automatic_promotion",
        "product_changes_authorized",
        "ui_ux_1_202_execution_authorized",
    ):
        if authorization[field] is not False:
            raise ValueError(f"{field} debe ser false")
    gate = authorization["pre_promotion_gate"]
    required_gate = {
        "gate_id",
        "authorized_promotion_ids",
        "promotion_ready_ids",
        "unknown_authorized_ids",
        "authorized_not_ready",
        "ready_not_authorized",
        "conflicting_evidence",
        "missing_evidence",
        "conditioned_autonomy_readiness",
        "conditioned_autonomy_decision",
        "status",
    }
    if not isinstance(gate, Mapping) or not required_gate <= set(gate):
        raise ValueError("pre_promotion_gate incompleto")
    if gate["gate_id"] != "N0_GOKV_FIRST_INSTITUTIONAL_PROMOTION_GATE_PASSED" or gate["status"] != "PASSED":
        raise ValueError("N0 gate invalido")
    if gate["authorized_promotion_ids"] != len(authorized) or gate["promotion_ready_ids"] != len(authorized):
        raise ValueError("N0 gate no coincide con la autorizacion")
    for field in ("unknown_authorized_ids", "authorized_not_ready", "ready_not_authorized", "conflicting_evidence", "missing_evidence"):
        if gate[field] != 0:
            raise ValueError(f"N0 gate reporta {field}")
    if gate["conditioned_autonomy_readiness"] != "DIRECTION_APPROVAL_REQUIRED":
        raise ValueError("conditioned_autonomy readiness invalido")
    if gate["conditioned_autonomy_decision"] != "KEEP_VALIDATED":
        raise ValueError("conditioned_autonomy decision invalida")
    if not isinstance(authorization["notes"], list) or not all(isinstance(value, str) for value in authorization["notes"]):
        raise ValueError("notes debe ser una lista de strings")
    return deepcopy(dict(authorization))


def validate_transition_preserves_contract(before: Mapping[str, Any], after: Mapping[str, Any]) -> None:
    before_item = validate_knowledge_item(dict(before))
    after_item = validate_knowledge_item(dict(after))
    for field in _PRESERVED_FIELDS:
        if before_item[field] != after_item[field]:
            raise ValueError(f"promotion no puede mutar {field}")
    if before_item["status"] != "VALIDATED" or after_item["status"] != "PROMOTED":
        raise ValueError("promotion debe ser VALIDATED -> PROMOTED")
    if before_item["updated_at"] == after_item["updated_at"]:
        raise ValueError("promotion debe registrar updated_at")


def build_promotion_event(
    *,
    event_id: str,
    authorization: Mapping[str, Any],
    assessment: Mapping[str, Any],
    transitions: list[Mapping[str, Any]],
    created_at: str | None = None,
) -> dict[str, Any]:
    _validate_id(event_id, "event_id")
    event = {
        "event_id": event_id,
        "schema_version": PROMOTION_EVENT_SCHEMA_VERSION,
        "event_type": "FIRST_INSTITUTIONAL_KNOWLEDGE_PROMOTION",
        "authorization_id": authorization["authorization_id"],
        "source_assessment": authorization["source_assessment"],
        "automatic_promotion": False,
        "product_changes_authorized": False,
        "created_at": created_at or _now(),
        "transitions": [deepcopy(dict(transition)) for transition in transitions],
    }
    return validate_promotion_event(event)


def validate_promotion_event(event: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "event_id",
        "schema_version",
        "event_type",
        "authorization_id",
        "source_assessment",
        "automatic_promotion",
        "product_changes_authorized",
        "created_at",
        "transitions",
    }
    if not isinstance(event, Mapping) or not required <= set(event):
        raise ValueError("promotion event incompleto")
    _validate_id(event["event_id"], "event_id")
    _validate_id(event["authorization_id"], "authorization_id")
    _validate_text(event["source_assessment"], "source_assessment")
    _validate_timestamp(event["created_at"], "created_at")
    if event["schema_version"] != PROMOTION_EVENT_SCHEMA_VERSION:
        raise ValueError("promotion event schema invalido")
    if event["event_type"] != "FIRST_INSTITUTIONAL_KNOWLEDGE_PROMOTION":
        raise ValueError("event_type invalido")
    if event["automatic_promotion"] is not False or event["product_changes_authorized"] is not False:
        raise ValueError("promotion event policy invalida")
    if not isinstance(event["transitions"], list) or not event["transitions"]:
        raise ValueError("promotion event transitions invalida")
    for transition in event["transitions"]:
        required_transition = {
            "knowledge_id",
            "kind",
            "status_before",
            "promotion_readiness",
            "authorized",
            "evidence_refs",
            "source_checkpoints",
            "source_commits",
            "scope_before",
            "scope_after",
            "origin_before",
            "origin_after",
            "privacy_before",
            "privacy_after",
            "lineage_preserved",
            "status_after",
        }
        if not isinstance(transition, Mapping) or not required_transition <= set(transition):
            raise ValueError("promotion transition incompleta")
        _validate_id(transition["knowledge_id"], "transition.knowledge_id")
        if transition["status_before"] != "VALIDATED" or transition["status_after"] != "PROMOTED":
            raise ValueError("promotion transition lifecycle invalido")
        if transition["promotion_readiness"] != "PROMOTION_READY" or transition["authorized"] is not True:
            raise ValueError("promotion transition governance invalida")
        for field in ("evidence_refs", "source_checkpoints", "source_commits"):
            _validate_id_list(transition[field], f"transition.{field}", allow_empty=False)
        if transition["scope_before"] != transition["scope_after"] or transition["scope_after"] != "IA_CORE_BUILD":
            raise ValueError("promotion transition scope invalido")
        if transition["origin_before"] != "DEVELOPMENT_ORIGIN" or transition["origin_before"] != transition["origin_after"]:
            raise ValueError("promotion transition provenance invalida")
        if transition["privacy_before"] != transition["privacy_after"]:
            raise ValueError("promotion transition privacy mutada")
        if transition["lineage_preserved"] is not True:
            raise ValueError("promotion transition lineage no preservada")
    return deepcopy(dict(event))


def promote_authorized_items(
    authorization: Mapping[str, Any],
    assessment: Mapping[str, Any],
    *,
    paths: VaultPaths | None = None,
    requested_ids: list[str] | None = None,
    event_id: str = "first_institutional_promotion_0_3",
) -> dict[str, Any]:
    """Execute an explicit, preflighted promotion transaction for listed IDs."""

    auth = validate_promotion_authorization(authorization)
    validated_assessment = validate_promotion_assessment(assessment)
    vault = paths or default_paths()
    current_items = iter_knowledge_items(vault)
    by_id = {item["knowledge_id"]: item for item in current_items}
    authorized_ids = list(auth["authorized_knowledge_ids"])
    requested = list(requested_ids if requested_ids is not None else authorized_ids)
    _validate_id_list(requested, "requested_ids", allow_empty=False)
    if requested != authorized_ids or set(requested) != set(authorized_ids):
        raise ValueError("requested_ids debe coincidir exactamente con la autorizacion")
    unknown = set(authorized_ids) - set(by_id)
    if unknown:
        raise ValueError(f"authorized IDs desconocidos: {sorted(unknown)}")
    decisions = {decision["knowledge_id"]: decision for decision in validated_assessment["decisions"]}
    transitions: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for knowledge_id in authorized_ids:
        item = by_id[knowledge_id]
        decision = decisions.get(knowledge_id)
        if decision is None:
            raise ValueError(f"assessment sin decision para {knowledge_id}")
        _validate_item_against_assessment(item, decision, validated_assessment, vault)
        if decision["promotion_readiness"] != "PROMOTION_READY":
            if not (decision["promotion_readiness"] == "DIRECTION_APPROVAL_REQUIRED" and knowledge_id in auth["direction_approval_ids"]):
                raise ValueError(f"{knowledge_id} no esta PROMOTION_READY")
            raise ValueError(f"{knowledge_id} requiere una autorizacion direccional especifica no disponible en este mecanismo")
        if item["status"] != "VALIDATED":
            raise ValueError(f"{knowledge_id} no esta VALIDATED")
        if item["scope"] != auth["scope_constraints"]["required_scope"]:
            raise ValueError(f"{knowledge_id} scope fuera de autorizacion")
        if item["learning_origin"] != auth["provenance_constraints"]["required_learning_origin"]:
            raise ValueError(f"{knowledge_id} provenance fuera de autorizacion")
        updated = transition_knowledge_item(item, "PROMOTED")
        validate_transition_preserves_contract(item, updated)
        transition = {
            "knowledge_id": knowledge_id,
            "kind": item["kind"],
            "status_before": item["status"],
            "promotion_readiness": decision["promotion_readiness"],
            "authorized": True,
            "evidence_refs": _effective_evidence_ids(item, decision, vault),
            "source_checkpoints": _effective_checkpoints(item, decision, vault),
            "source_commits": _effective_commits(item, decision, vault),
            "scope_before": item["scope"],
            "scope_after": updated["scope"],
            "origin_before": item["learning_origin"],
            "origin_after": updated["learning_origin"],
            "privacy_before": item["privacy_class"],
            "privacy_after": updated["privacy_class"],
            "lineage_preserved": item["lineage"] == updated["lineage"],
            "status_after": updated["status"],
        }
        transitions.append((item, updated, transition))
    event = build_promotion_event(
        event_id=event_id,
        authorization=auth,
        assessment=validated_assessment,
        transitions=[transition for _, _, transition in transitions],
    )
    event_path = vault.events_dir / "promotions" / f"{event_id}.json"
    if event_path.exists():
        raise ValueError(f"promotion event duplicado: {event_id}")
    _commit_transaction(vault, transitions, event_path, event)
    return event


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON debe ser un objeto: {path}")
    return value


def _validate_item_against_assessment(
    item: Mapping[str, Any],
    decision: Mapping[str, Any],
    assessment: Mapping[str, Any],
    vault: VaultPaths,
) -> None:
    if decision["status"] != item["status"]:
        raise ValueError(f"assessment stale para {item['knowledge_id']}: status")
    assessed_at = assessment["assessed_at"]
    if _parse_timestamp(item["updated_at"]) > _parse_timestamp(assessed_at):
        raise ValueError(f"assessment stale para {item['knowledge_id']}: updated_at")
    if decision.get("learning_origin") != item["learning_origin"]:
        raise ValueError(f"assessment stale para {item['knowledge_id']}: provenance")
    if decision.get("readiness_after", decision["promotion_readiness"]) != decision["promotion_readiness"]:
        raise ValueError(f"assessment readiness inconsistente para {item['knowledge_id']}")
    if not all(decision.get("criteria", {}).values()):
        raise ValueError(f"assessment criteria incompletos para {item['knowledge_id']}")
    evidence_ids = _effective_evidence_ids(item, decision, vault)
    checkpoints = _effective_checkpoints(item, decision, vault)
    commits = _effective_commits(item, decision, vault)
    expected_evidence = decision.get("evidence_count", decision.get("evidence_after"))
    expected_checkpoints = decision.get("source_checkpoint_count_after", decision.get("source_checkpoint_count"))
    expected_commits = decision.get("source_commit_count_after", decision.get("source_commit_count"))
    if expected_evidence != len(evidence_ids):
        raise ValueError(f"missing evidence para {item['knowledge_id']}")
    if expected_checkpoints != len(checkpoints) or expected_commits != len(commits):
        raise ValueError(f"assessment stale para {item['knowledge_id']}: source thresholds")
    if len(evidence_ids) < 2 or len(checkpoints) < 2 or len(commits) < 2:
        raise ValueError(f"promotion evidence threshold insuficiente para {item['knowledge_id']}")
    if any(entry["relation"] == "CONTRADICT" for entry in item["lineage"]):
        raise ValueError(f"conflicting evidence para {item['knowledge_id']}")


def _effective_evidence_ids(item: Mapping[str, Any], decision: Mapping[str, Any], vault: VaultPaths) -> list[str]:
    ids = [entry["evidence_id"] for entry in item["evidence_refs"]]
    for entry in _overlay_entries(decision, item["knowledge_id"], vault):
        ids.append(entry["evidence_id"])
    if len(ids) != len(set(ids)):
        raise ValueError(f"evidence duplicada para {item['knowledge_id']}")
    return sorted(ids)


def _effective_checkpoints(item: Mapping[str, Any], decision: Mapping[str, Any], vault: VaultPaths) -> list[str]:
    values = list(item["source_checkpoints"])
    for overlay in _overlay_for_decision(decision, vault):
        values.append(overlay["source_checkpoint"])
    return sorted(set(values))


def _effective_commits(item: Mapping[str, Any], decision: Mapping[str, Any], vault: VaultPaths) -> list[str]:
    values = list(item["source_commits"])
    for entry in _overlay_entries(decision, item["knowledge_id"], vault):
        values.extend(entry["source_commits"])
    return sorted(set(values))


def _overlay_for_decision(decision: Mapping[str, Any], vault: VaultPaths) -> list[dict[str, Any]]:
    overlay_id = decision.get("evidence_overlay_ref")
    if not overlay_id:
        return []
    matches = []
    for path in (vault.events_dir / "evidence").glob("*.json"):
        value = load_json(path)
        if value.get("overlay_id") == overlay_id:
            matches.append(value)
    if len(matches) != 1:
        raise ValueError(f"evidence overlay no resuelto: {overlay_id}")
    overlay = matches[0]
    if overlay.get("provenance") != "DEVELOPMENT_ORIGIN" or overlay.get("append_only") is not True:
        raise ValueError("evidence overlay no preserva provenance/append_only")
    if not isinstance(overlay.get("evidence_refs"), list):
        raise ValueError("evidence overlay invalido")
    return [overlay]


def _overlay_entries(decision: Mapping[str, Any], knowledge_id: str, vault: VaultPaths) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for overlay in _overlay_for_decision(decision, vault):
        for entry in overlay["evidence_refs"]:
            if entry.get("knowledge_id") == knowledge_id:
                if not entry.get("source_refs") or not entry.get("source_commits"):
                    raise ValueError(f"evidence overlay incompleto para {knowledge_id}")
                entries.append(entry)
    return entries


def _commit_transaction(
    vault: VaultPaths,
    transitions: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]],
    event_path: Path,
    event: Mapping[str, Any],
) -> None:
    snapshots = {vault.items_dir / f"{before['knowledge_id']}.json": _read_bytes(vault.items_dir / f"{before['knowledge_id']}.json") for before, _, _ in transitions}
    registry_snapshot = _read_bytes(vault.registry_path)
    replaced_paths: list[Path] = []
    try:
        for before, after, _ in transitions:
            path = vault.items_dir / f"{before['knowledge_id']}.json"
            _atomic_write_json(path, after)
            replaced_paths.append(path)
        rebuild_index(vault)
        _write_json_exclusive(event_path, event)
    except Exception:
        for path, content in snapshots.items():
            _atomic_write_bytes(path, content)
        _atomic_write_bytes(vault.registry_path, registry_snapshot)
        if event_path.exists() and event_path not in snapshots:
            try:
                event_path.unlink()
            except OSError:
                pass
        raise


def _write_json_exclusive(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    _atomic_write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.gokv-tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _validate_id_list(value: Any, field: str, *, allow_empty: bool) -> None:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValueError(f"{field} debe ser una lista no vacia")
    for entry in value:
        _validate_id(entry, field)


def _validate_id(value: Any, field: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise ValueError(f"{field} invalido")


def _validate_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} invalido")


def _validate_timestamp(value: Any, field: str) -> None:
    _validate_text(value, field)
    _parse_timestamp(value)


def _parse_timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{value} no es ISO-8601") from exc


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
