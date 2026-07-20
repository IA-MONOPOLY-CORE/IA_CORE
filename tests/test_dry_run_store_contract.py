import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.dry_run_store_contract import (
    DRY_RUN_STORE_CONTRACT_EVENTS,
    FORBIDDEN_DRY_RUN_STORE_EVENTS,
    build_append_only_contract,
    build_checksum_contract,
    build_payload_boundary_contract,
    validate_dry_run_store_contract,
)
from core.dry_run_store_schema import validate_dry_run_store_contract_report
from core.execution_runner import run_dry_run
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent


def _store_inputs(tmp_path: Path, target_type: str = "agent") -> tuple[dict, dict, dict, dict]:
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
    assert dry_run_contract["status"] == "passed"
    dry_run_result = run_dry_run(
        dry_run_contract_result=dry_run_contract,
        observability_context=kwargs["observability_context"],
        audit_store_path=kwargs["audit_store_path"],
    )
    assert dry_run_result["status"] == "simulated"
    return inputs, kwargs, dry_run_contract, dry_run_result


def _contract_kwargs(kwargs: dict, dry_run_contract: dict, dry_run_result: dict) -> dict:
    return {
        "dry_run_result": dry_run_result,
        "dry_run_contract_result": dry_run_contract,
        "execution_runner_contract_result": kwargs["execution_runner_contract_result"],
        "runtime_preparation": kwargs["runtime_prepare_result"],
        "audit_store_path": kwargs["audit_store_path"],
        "observability_context": kwargs["observability_context"],
        "capability_policy": dry_run_contract["capability_policy_ref"],
    }


def _assert_passed(report: dict, target_type: str) -> None:
    assert validate_dry_run_store_contract_report(report)
    assert report["status"] == "passed"
    assert report["mode"] == "dry_run_store_contract_only"
    assert report["storage_format"] == "append_only_jsonl"
    assert report["store_type"] == "dry_run_store"
    assert report["append_only"] is True
    assert report["target_type"] == target_type
    assert report["entry_contract"]
    assert report["append_only_contract"]["append_only"] is True
    assert report["idempotency_contract"]["idempotency_scope"]
    assert report["checksum_contract"]["checksum_algorithm"] == "sha256"
    assert report["reference_contract"]["required_refs"]
    assert report["payload_boundary_contract"]["model_response_allowed"] is False
    assert report["retention_contract"]["physical_delete_now_allowed"] is False
    assert report["audit_contract"]["audit_events_expected"] == sorted(DRY_RUN_STORE_CONTRACT_EVENTS)
    assert set(report["audit_contract"]["audit_events_forbidden"]) == FORBIDDEN_DRY_RUN_STORE_EVENTS
    assert report["observability_contract"]["correlation_id_required"] is True
    assert report["evidence"]
    assert report["boundary_summary"]
    assert report["readiness_summary"]
    assert report["store_summary"]["implementation_created"] is False
    assert report["blockers"] == []


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_dry_run_store_contract_passes_for_valid_agent_and_team_dry_run_result(tmp_path, target_type):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, target_type)

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result))

    _assert_passed(report, target_type)


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"mode": "dry_run_store_future"}, "invalid_mode"),
        ({"storage_format": "database_future"}, "invalid_storage_format"),
        ({"store_type": "execution_attempt_store"}, "invalid_store_type"),
        ({"target_type": "domain", "target_id": "domain"}, "invalid_target_type"),
        ({"dry_run_result": None}, "missing_dry_run_result"),
        ({"audit_store_path": None}, "missing_audit_store"),
        ({"observability_context": None}, "missing_observability_context"),
        ({"capability_policy": None}, "missing_capability_policy"),
    ],
)
def test_dry_run_store_contract_blocks_invalid_core_inputs(tmp_path, overrides, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    base = _contract_kwargs(kwargs, dry_run_contract, dry_run_result)

    report = validate_dry_run_store_contract(**{**base, **overrides})

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda result: result.update({"mode": "dry_run_only"}), "dry_run_result_not_result_only"),
        (lambda result: result.update({"status": "aborted"}), "dry_run_result_not_simulated_or_prepared"),
        (lambda result: result.update({"dry_run_id": ""}), "missing_dry_run_id"),
        (lambda result: result.update({"dry_run_contract_ref": {}}), "missing_dry_run_contract_ref"),
        (lambda result: result.update({"execution_runner_contract_ref": {}}), "missing_execution_runner_contract_ref"),
        (lambda result: result.update({"runtime_preparation_ref": {}}), "missing_runtime_preparation_ref"),
        (lambda result: result.update({"target_ref": {}}), "missing_target_ref"),
        (lambda result: result.update({"correlation_id": ""}), "missing_correlation_id"),
        (lambda result: result.update({"idempotency_key": ""}), "missing_idempotency_key"),
        (lambda result: result.update({"boundary_summary": {}}), "missing_boundary_summary"),
        (lambda result: result.update({"readiness_summary": {}}), "missing_readiness_summary"),
        (lambda result: result.update({"risk_summary": {}}), "missing_risk_summary"),
    ],
)
def test_dry_run_store_contract_blocks_invalid_dry_run_result_shape(tmp_path, mutator, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    mutated = deepcopy(dry_run_result)
    mutator(mutated)

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, mutated))

    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_dry_run_store_contract_blocks_unverified_audit_store(tmp_path):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    manifest_path = Path(kwargs["audit_store_path"]) / "store_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["event_count"] += 1
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result))

    assert report["status"] == "blocked"
    assert "audit_store_not_verified" in _codes(report)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("checksum_required", False, "checksum_missing"),
        ("entry_hash_required", False, "checksum_missing"),
        ("checksum_algorithm", "md5", "checksum_algorithm_not_allowed"),
        ("checksum_scope", [], "checksum_scope_missing"),
        ("canonical_serialization_policy", "", "non_canonical_serialization"),
        ("tamper_detection_required", False, "tamper_detection_missing"),
    ],
)
def test_dry_run_store_contract_blocks_invalid_checksum_policy(tmp_path, field, value, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    checksum = build_checksum_contract()
    checksum[field] = value

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result), checksum_contract=checksum)

    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_dry_run_store_contract_blocks_missing_checksum_policy(tmp_path):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result), checksum_contract={})

    assert report["status"] == "blocked"
    assert "missing_checksum_policy" in _codes(report)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("append_only", "not_append_only"),
        ("overwrite_allowed", "overwrite_not_allowed"),
        ("update_existing_allowed", "update_not_allowed"),
        ("delete_allowed", "delete_not_allowed"),
        ("physical_delete_allowed", "delete_not_allowed"),
        ("entry_replacement_allowed", "replace_not_allowed"),
        ("replace_allowed", "replace_not_allowed"),
    ],
)
def test_dry_run_store_contract_blocks_append_only_violations(tmp_path, field, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    append = build_append_only_contract()
    append[field] = False if field == "append_only" else True

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result), append_only_contract=append)

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_attempt_allowed", "execution_attempt_id_not_allowed"),
        ("execution_payload_allowed", "execution_payload_not_allowed"),
        ("agent_output_allowed", "agent_output_not_allowed"),
        ("team_output_allowed", "team_output_not_allowed"),
        ("model_response_allowed", "model_response_not_allowed"),
        ("model_prompt_allowed", "model_prompt_not_allowed"),
        ("model_completion_allowed", "model_completion_not_allowed"),
        ("tool_result_allowed", "tool_result_not_allowed"),
        ("tool_call_allowed", "tool_call_not_allowed"),
        ("memory_write_allowed", "memory_write_not_allowed"),
        ("memory_read_result_allowed", "memory_read_result_not_allowed"),
        ("external_response_allowed", "external_response_not_allowed"),
        ("external_request_allowed", "external_request_not_allowed"),
        ("scheduler_job_allowed", "scheduler_job_not_allowed"),
        ("worker_task_allowed", "worker_task_not_allowed"),
        ("state_mutation_allowed", "state_mutation_not_allowed"),
        ("artifact_mutation_allowed", "artifact_mutation_not_allowed"),
        ("secret_value_allowed", "secret_value_not_allowed"),
        ("credential_value_allowed", "credential_value_not_allowed"),
    ],
)
def test_dry_run_store_contract_blocks_payload_boundary_flags(tmp_path, field, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    payload_boundary = build_payload_boundary_contract()
    payload_boundary[field] = True

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result), payload_boundary_contract=payload_boundary)

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("execution_attempt_id", "execution_attempt_id_not_allowed"),
        ("execution_payload", "execution_payload_not_allowed"),
        ("execution_result", "execution_result_not_allowed"),
        ("agent_output", "agent_output_not_allowed"),
        ("team_output", "team_output_not_allowed"),
        ("model_response", "model_response_not_allowed"),
        ("model_prompt_real", "model_prompt_not_allowed"),
        ("model_completion_real", "model_completion_not_allowed"),
        ("tool_result", "tool_result_not_allowed"),
        ("tool_call_real", "tool_call_not_allowed"),
        ("memory_write", "memory_write_not_allowed"),
        ("memory_read_result", "memory_read_result_not_allowed"),
        ("external_response", "external_response_not_allowed"),
        ("external_request", "external_request_not_allowed"),
        ("scheduler_job", "scheduler_job_not_allowed"),
        ("worker_task", "worker_task_not_allowed"),
        ("state_mutation", "state_mutation_not_allowed"),
        ("artifact_mutation", "artifact_mutation_not_allowed"),
        ("secret_value", "secret_value_not_allowed"),
        ("credential_value", "credential_value_not_allowed"),
    ],
)
def test_dry_run_store_contract_blocks_forbidden_real_payload_fields(tmp_path, field, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    mutated = {**dry_run_result, field: {"real": True}}

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, mutated))

    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_dry_run_store_contract_blocks_cross_target_refs(tmp_path):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path / "agent", "agent")
    _team_inputs, team_kwargs, _team_contract, _team_result = _store_inputs(tmp_path / "team", "team")

    contract_kwargs = _contract_kwargs(kwargs, dry_run_contract, dry_run_result)
    contract_kwargs["execution_runner_contract_result"] = team_kwargs["execution_runner_contract_result"]
    report = validate_dry_run_store_contract(**contract_kwargs)

    assert report["status"] == "blocked"
    assert "cross_target_ref" in _codes(report)


@pytest.mark.parametrize(
    ("target_status", "code"),
    [
        ("candidate_for_activation", "target_not_active"),
        ("legacy", "legacy_target_not_allowed"),
        ("archived", "archived_target_not_allowed"),
        ("broken", "broken_target_not_allowed"),
    ],
)
def test_dry_run_store_contract_blocks_non_active_legacy_archived_and_broken_targets(tmp_path, target_status, code):
    _inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    mutated = deepcopy(dry_run_result)
    mutated["target_ref"]["status"] = target_status

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, mutated))

    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_dry_run_store_contract_does_not_create_store_jsonl_attempt_or_mutate_targets(tmp_path):
    inputs, kwargs, dry_run_contract, dry_run_result = _store_inputs(tmp_path, "agent")
    before_hash = _tree_hash(inputs["chain"]["domain_dir"])
    before_agent = deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"])))
    before_team = deepcopy(_read_json(_team_path(inputs["chain"])))
    before_operational = _operational_snapshot()
    runner_source = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, dry_run_result))

    assert report["status"] == "passed"
    assert not (ROOT / "core" / "dry_run_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not any(inputs["chain"]["domain_dir"].rglob("*.jsonl"))
    assert "execution_attempt_id" not in report
    assert _tree_hash(inputs["chain"]["domain_dir"]) == before_hash
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before_agent
    assert _read_json(_team_path(inputs["chain"])) == before_team
    assert _operational_snapshot() == before_operational
    assert (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8") == runner_source
