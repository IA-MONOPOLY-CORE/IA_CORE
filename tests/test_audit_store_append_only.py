import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

import core.audit_store as audit_store
from core.audit_store import (
    append_audit_event,
    create_audit_store,
    read_audit_events,
    summarize_audit_store,
    verify_audit_store,
)
from core.observability_schema import build_observability_event


ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"
AGENTS = ROOT / "agents"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _event(event_id: str = "event_audit_store_one", **overrides) -> dict:
    payload = build_observability_event(
        event_id=event_id,
        correlation_id="correlation_audit_store_flow",
        causation_id="causation_audit_store_flow",
        event_type="runtime_contract_evaluated",
        actor="audit_store_test_service",
        actor_type="test",
        source_module="tests.test_audit_store_append_only",
        target_type="team",
        target_id="sandbox_audit_store_team",
        domain_id="sandbox_audit_store_domain",
        operation="audit_store_append_only",
        operation_phase="runtime_contract",
        result_status="passed",
        requested_status="declarative_runtime_contract",
        previous_status="active",
        next_status="active",
        mutation_scope="none",
        runtime_flags={"runtime_enabled": False, "runtime_allowed": False},
        execution_flags={"execution_enabled": False, "execution_allowed": False},
        external_access_flags={"external_access": False, "external_access_enabled": False},
        tool_memory_flags={"tool_execution_enabled": False, "memory_persistence_enabled": False},
        evidence_refs={"runtime_contract_id": "runtime_contract_audit_store_team"},
        contract_refs={"runtime_contract_id": "runtime_contract_audit_store_team"},
        audit_refs={"audit_event_id": "audit_event_audit_store_team"},
    )
    payload.update(overrides)
    return payload


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _event_paths(store_path: Path) -> list[Path]:
    return sorted((store_path / "events").glob("*.json"))


def test_create_audit_store_generates_valid_manifest(tmp_path):
    store_path = tmp_path / "audit_store"

    manifest = create_audit_store(store_path, audit_store_id="audit_store_test")

    assert (store_path / "store_manifest.json").is_file()
    assert (store_path / "events").is_dir()
    assert manifest["append_only"] is True
    assert manifest["immutable_records"] is True
    assert manifest["event_count"] == 0
    assert manifest["first_event_at"] is None
    assert verify_audit_store(store_path)["verified"] is True


def test_append_read_verify_and_summarize_preserve_chain_and_flags(tmp_path):
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_test")

    first = append_audit_event(store_path, _event("event_audit_store_one"))
    second = append_audit_event(store_path, _event("event_audit_store_two", result_status="blocked", blockers=["blocked_by_test"]))

    paths = _event_paths(store_path)
    assert [path.name[:8] for path in paths] == ["00000001", "00000002"]
    assert _read_json(store_path / "store_manifest.json")["event_count"] == 2
    assert first["sequence_number"] == 1
    assert second["sequence_number"] == 2
    assert second["previous_event_checksum"] == first["checksum"]

    events = read_audit_events(store_path)
    assert [event["sequence_number"] for event in events] == [1, 2]
    assert {event["correlation_id"] for event in events} == {"correlation_audit_store_flow"}
    assert events[0]["runtime_flags"]["runtime_enabled"] is False
    assert events[0]["execution_flags"]["execution_enabled"] is False
    assert events[0]["external_access_flags"]["external_access"] is False
    assert events[0]["tool_memory_flags"]["tool_execution_enabled"] is False
    assert events[0]["tool_memory_flags"]["memory_persistence_enabled"] is False

    verification = verify_audit_store(store_path)
    assert verification["event_count"] == 2
    assert verification["last_event_checksum"] == second["checksum"]

    summary = summarize_audit_store(store_path)
    assert summary["events_total"] == 2
    assert summary["events_by_type"]["runtime_contract_evaluated"] == 2
    assert summary["blocked_operations_total"] == 1
    assert summary["audit_store"]["verified"] is True


def test_verify_fails_when_event_is_modified(tmp_path):
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_test")
    append_audit_event(store_path, _event("event_audit_store_one"))

    event_path = _event_paths(store_path)[0]
    event = _read_json(event_path)
    event["target_id"] = "sandbox_audit_store_tampered_team"
    _write_json(event_path, event)

    with pytest.raises(ValueError, match="event checksum"):
        verify_audit_store(store_path)


def test_verify_fails_when_event_is_deleted_or_sequence_reordered(tmp_path):
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_test")
    append_audit_event(store_path, _event("event_audit_store_one"))
    append_audit_event(store_path, _event("event_audit_store_two"))

    _event_paths(store_path)[0].unlink()
    with pytest.raises(ValueError, match="event_count|sequence"):
        verify_audit_store(store_path)

    store_path = tmp_path / "audit_store_reorder"
    create_audit_store(store_path, audit_store_id="audit_store_reorder_test")
    append_audit_event(store_path, _event("event_audit_store_one"))
    append_audit_event(store_path, _event("event_audit_store_two"))
    second = _event_paths(store_path)[1]
    second.rename(second.with_name(second.name.replace("00000002", "00000003")))

    with pytest.raises(ValueError, match="sequence"):
        verify_audit_store(store_path)


def test_verify_fails_when_manifest_is_inconsistent(tmp_path):
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_test")
    append_audit_event(store_path, _event("event_audit_store_one"))

    manifest_path = store_path / "store_manifest.json"
    manifest = _read_json(manifest_path)
    manifest["event_count"] = 99
    _write_json(manifest_path, manifest)
    with pytest.raises(ValueError, match="event_count"):
        verify_audit_store(store_path)

    manifest["event_count"] = 1
    manifest["last_event_checksum"] = "bad_checksum"
    _write_json(manifest_path, manifest)
    with pytest.raises(ValueError, match="last_event_checksum"):
        verify_audit_store(store_path)


def test_invalid_event_does_not_write_partial_file(tmp_path):
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_test")
    invalid = _event("event_audit_store_invalid")
    invalid["evidence_refs"] = {}

    with pytest.raises(ValueError, match="evidence_refs"):
        append_audit_event(store_path, invalid)

    assert _event_paths(store_path) == []
    assert _read_json(store_path / "store_manifest.json")["event_count"] == 0


def test_append_does_not_overwrite_existing_event_file(tmp_path):
    store_path = tmp_path / "audit_store"
    create_audit_store(store_path, audit_store_id="audit_store_test")
    reserved_path = store_path / "events" / "00000001_event_audit_store_one.json"
    reserved_payload = {"reserved": True}
    _write_json(reserved_path, reserved_payload)

    with pytest.raises(FileExistsError):
        append_audit_event(store_path, _event("event_audit_store_one"))

    assert _read_json(reserved_path) == reserved_payload
    assert _read_json(store_path / "store_manifest.json")["event_count"] == 0


def test_no_public_delete_helper_and_no_operational_side_effects(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    store_path = tmp_path / "audit_store"
    event = _event("event_audit_store_one")
    original = deepcopy(event)

    create_audit_store(store_path, audit_store_id="audit_store_test")
    append_audit_event(store_path, event)

    assert event == original
    assert not hasattr(audit_store, "delete_audit_event")
    assert not hasattr(audit_store, "update_audit_event")
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert not (store_path / "ui").exists()
    assert not (store_path / "integrations").exists()
