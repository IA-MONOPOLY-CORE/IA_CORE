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
from core.execution_runner import RESULT_ONLY_MODE, prepare_dry_run, run_dry_run
from core.execution_runner_dry_run_contract import validate_execution_runner_dry_run_contract
from tests.test_dry_run_store_contract import _contract_kwargs
from tests.test_execution_runner_contract import _codes
from tests.test_execution_runner_dry_run_contract import _prepared_dry_run_kwargs
from tests.test_runtime_contract_end_to_end import _agent_path, _operational_snapshot, _read_json, _team_path, _tree_hash


ROOT = Path(__file__).parent.parent
FORBIDDEN_STORAGE_PATTERNS = ("*.jsonl",)
FORBIDDEN_DOMAIN_DIRS = (
    "dry_run_store",
    "execution_attempt_store",
    "execution_attempts",
    "storage",
    "data",
    "logs",
    "ui",
    "integrations",
    "scheduler",
    "worker_queue",
)
REQUIRED_DRY_RUN_RESULT_FIELDS = [
    "dry_run_id",
    "target_ref",
    "contract_refs",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "simulated_plan",
    "simulated_steps",
    "input_expectations",
    "output_expectations",
    "risk_summary",
    "boundary_summary",
    "readiness_summary",
    "audit_events",
    "observability_events",
    "blocked_side_effects",
    "idempotency_key",
    "correlation_id",
]
REAL_PAYLOAD_FIELDS = [
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
]
PAYLOAD_BOUNDARY_FLAGS = [
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
]


def _runner_kwargs(kwargs: dict, dry_run_contract: dict) -> dict:
    return {
        "dry_run_contract_result": dry_run_contract,
        "observability_context": kwargs["observability_context"],
        "audit_store_path": kwargs["audit_store_path"],
        "actor": "dry_run_store_contract_e2e",
        "reason": "dry run store contract e2e",
    }


def _snapshot(inputs: dict) -> dict:
    return {
        "domain_hash": _tree_hash(inputs["chain"]["domain_dir"]),
        "agent": deepcopy(_read_json(_agent_path(inputs["chain"], inputs["agent_id"]))),
        "team": deepcopy(_read_json(_team_path(inputs["chain"]))),
        "operational": _operational_snapshot(),
        "core_execution_runner": (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8"),
    }


def _assert_no_persistence_or_mutation(inputs: dict, before: dict) -> None:
    domain_dir = inputs["chain"]["domain_dir"]
    assert _tree_hash(domain_dir) == before["domain_hash"]
    assert _read_json(_agent_path(inputs["chain"], inputs["agent_id"])) == before["agent"]
    assert _read_json(_team_path(inputs["chain"])) == before["team"]
    assert _operational_snapshot() == before["operational"]
    assert (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8") == before["core_execution_runner"]
    assert (ROOT / "core" / "dry_run_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    for dirname in FORBIDDEN_DOMAIN_DIRS:
        assert not (domain_dir / dirname).exists()
    for pattern in FORBIDDEN_STORAGE_PATTERNS:
        assert not list(domain_dir.rglob(pattern))


def _build_e2e(tmp_path: Path, target_type: str) -> tuple[dict, dict, dict, dict, dict]:
    inputs, kwargs = _prepared_dry_run_kwargs(tmp_path, target_type)
    before = _snapshot(inputs)
    dry_run_contract = validate_execution_runner_dry_run_contract(**kwargs)
    prepared = prepare_dry_run(**_runner_kwargs(kwargs, dry_run_contract))
    simulated = run_dry_run(prepared_result=prepared, actor="dry_run_store_contract_e2e", reason="simulate dry run store contract e2e")
    return inputs, kwargs, dry_run_contract, prepared, simulated, before


def _assert_dry_run_result(result: dict, prepared: dict, dry_run_contract: dict, kwargs: dict, target_type: str) -> None:
    assert prepared["status"] == "prepared"
    assert result["status"] == "simulated"
    assert result["mode"] == RESULT_ONLY_MODE
    assert result["target_type"] == target_type
    assert result["target_id"] == kwargs["target_id"]
    for field in REQUIRED_DRY_RUN_RESULT_FIELDS:
        assert result[field] not in (None, "", {}, [])
    assert result["target_ref"]["status"] == "active"
    assert result["contract_refs"]["runtime_contract_ref"] == dry_run_contract["runtime_contract_ref"]
    assert result["contract_refs"]["execution_contract_ref"] == dry_run_contract["execution_contract_ref"]
    assert result["contract_refs"]["runtime_executor_contract_ref"] == dry_run_contract["runtime_executor_contract_ref"]
    assert result["runtime_preparation_ref"] == dry_run_contract["runtime_preparation_ref"]
    assert result["execution_runner_contract_ref"] == dry_run_contract["execution_runner_contract_ref"]
    assert result["dry_run_contract_ref"]["contract_id"] == dry_run_contract["contract_id"]
    assert all(value is False for value in result["boundary_summary"].values())
    assert "execution_attempt_id" not in result


def _assert_store_contract(report: dict, target_type: str) -> None:
    assert report["status"] == "passed"
    assert report["mode"] == "dry_run_store_contract_only"
    assert report["store_type"] == "dry_run_store"
    assert report["storage_format"] == "append_only_jsonl"
    assert report["append_only"] is True
    assert report["target_type"] == target_type
    assert report["entry_contract"]["entry_type"] == "dry_run_result_only"
    assert report["append_only_contract"]["append_only"] is True
    assert report["append_only_contract"]["overwrite_allowed"] is False
    assert report["append_only_contract"]["delete_allowed"] is False
    assert report["idempotency_contract"]["idempotency_required"] is True
    assert report["idempotency_contract"]["duplicate_different_payload_policy"] == "blocked"
    assert report["checksum_contract"]["checksum_required"] is True
    assert report["checksum_contract"]["checksum_algorithm"] == "sha256"
    assert report["checksum_contract"]["canonical_serialization_policy"] == "json_sort_keys_utf8_no_mutation"
    assert report["checksum_contract"]["tamper_detection_required"] is True
    assert report["reference_contract"]["cross_target_refs_blocked"] is True
    assert report["payload_boundary_contract"]["execution_attempt_allowed"] is False
    assert report["payload_boundary_contract"]["model_response_allowed"] is False
    assert report["payload_boundary_contract"]["tool_result_allowed"] is False
    assert report["payload_boundary_contract"]["memory_write_allowed"] is False
    assert report["retention_contract"]["physical_delete_now_allowed"] is False
    assert report["audit_contract"]["audit_store_verified"] is True
    assert report["observability_contract"]["correlation_id_required"] is True
    assert report["store_summary"]["implementation_created"] is False
    assert report["store_summary"]["jsonl_written"] is False
    assert report["store_summary"]["storage_real_created"] is False
    assert report["store_summary"]["execution_attempt_id_created"] is False
    assert report["boundary_summary"]["append_only"] is True
    assert report["boundary_summary"]["payloads_real_allowed"] is False
    assert report["boundary_summary"]["store_implementation_created"] is False
    assert report["boundary_summary"]["execution_attempt_store_created"] is False
    assert report["readiness_summary"]["ready_for_contract_only"] is True
    assert report["readiness_summary"]["ready_for_implementation"] is False
    assert report["evidence"]
    assert report["blockers"] == []
    assert set(report["audit_contract"]["audit_events_expected"]) == DRY_RUN_STORE_CONTRACT_EVENTS
    assert set(report["audit_contract"]["audit_events_forbidden"]) == FORBIDDEN_DRY_RUN_STORE_EVENTS


@pytest.mark.parametrize("target_type", ["agent", "team"])
def test_dry_run_store_contract_e2e_passes_for_agent_and_team_result_only_chain(tmp_path, target_type):
    inputs, kwargs, dry_run_contract, prepared, simulated, before = _build_e2e(tmp_path, target_type)

    assert kwargs["runtime_contract_result"]["contract_result"] == "passed"
    assert kwargs["execution_contract_result"]["contract_result"] == "passed"
    assert kwargs["runtime_executor_contract_result"]["blockers"] == []
    assert kwargs["runtime_prepare_result"]["status"] == "prepared"
    assert kwargs["execution_runner_contract_result"]["status"] == "passed"
    assert dry_run_contract["status"] == "passed"
    assert dry_run_contract["target_ref"]["status"] == "active"
    _assert_dry_run_result(simulated, prepared, dry_run_contract, kwargs, target_type)

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, simulated))

    _assert_store_contract(report, target_type)
    assert "execution_attempt_id" not in report
    _assert_no_persistence_or_mutation(inputs, before)


@pytest.mark.parametrize(
    ("mutator", "code"),
    [
        (lambda result: result.update({"mode": "dry_run_only"}), "dry_run_result_not_result_only"),
        (lambda result: result.update({"status": "aborted"}), "dry_run_result_not_simulated_or_prepared"),
        (lambda result: result.update({"dry_run_id": ""}), "missing_dry_run_id"),
        (lambda result: result.update({"target_ref": {}}), "missing_target_ref"),
        (lambda result: result.update({"correlation_id": ""}), "missing_correlation_id"),
        (lambda result: result.update({"idempotency_key": ""}), "missing_idempotency_key"),
        (lambda result: result.update({"boundary_summary": {}}), "missing_boundary_summary"),
        (lambda result: result.update({"readiness_summary": {}}), "missing_readiness_summary"),
        (lambda result: result.update({"risk_summary": {}}), "missing_risk_summary"),
        (lambda result: result.update({"dry_run_contract_ref": {}}), "missing_dry_run_contract_ref"),
        (lambda result: result.update({"execution_runner_contract_ref": {}}), "missing_execution_runner_contract_ref"),
        (lambda result: result.update({"runtime_preparation_ref": {}}), "missing_runtime_preparation_ref"),
    ],
)
def test_dry_run_store_contract_e2e_blocks_invalid_result_and_refs(tmp_path, mutator, code):
    _inputs, kwargs, dry_run_contract, _prepared, simulated, _before = _build_e2e(tmp_path, "agent")
    mutated = deepcopy(simulated)
    mutator(mutated)

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, mutated))

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"dry_run_result": None}, "missing_dry_run_result"),
        ({"audit_store_path": None}, "missing_audit_store"),
        ({"observability_context": None}, "missing_observability_context"),
        ({"capability_policy": None}, "missing_capability_policy"),
        ({"target_type": "team"}, "cross_target_ref"),
        ({"target_id": "other_target"}, "cross_target_ref"),
        ({"correlation_id": "other_correlation"}, "cross_target_ref"),
    ],
)
def test_dry_run_store_contract_e2e_blocks_missing_or_crossed_inputs(tmp_path, overrides, code):
    _inputs, kwargs, dry_run_contract, _prepared, simulated, _before = _build_e2e(tmp_path, "agent")

    report = validate_dry_run_store_contract(**{**_contract_kwargs(kwargs, dry_run_contract, simulated), **overrides})

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"mode": "dry_run_store_future"}, "invalid_mode"),
        ({"storage_format": "database_future"}, "invalid_storage_format"),
        ({"append_only_contract": {**build_append_only_contract(), "append_only": False}}, "not_append_only"),
        ({"append_only_contract": {**build_append_only_contract(), "overwrite_allowed": True}}, "overwrite_not_allowed"),
        ({"append_only_contract": {**build_append_only_contract(), "update_existing_allowed": True}}, "update_not_allowed"),
        ({"append_only_contract": {**build_append_only_contract(), "delete_allowed": True}}, "delete_not_allowed"),
        ({"append_only_contract": {**build_append_only_contract(), "replace_allowed": True}}, "replace_not_allowed"),
        ({"append_only_contract": {**build_append_only_contract(), "physical_delete_allowed": True}}, "delete_not_allowed"),
        ({"append_only_contract": {**build_append_only_contract(), "mutable_entry_allowed": True}}, "mutable_entry_not_allowed"),
    ],
)
def test_dry_run_store_contract_e2e_blocks_invalid_store_policy(tmp_path, overrides, code):
    _inputs, kwargs, dry_run_contract, _prepared, simulated, _before = _build_e2e(tmp_path, "agent")

    report = validate_dry_run_store_contract(**{**_contract_kwargs(kwargs, dry_run_contract, simulated), **overrides})

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(
    ("checksum", "code"),
    [
        ({}, "missing_checksum_policy"),
        ({**build_checksum_contract(), "checksum_algorithm": "md5"}, "checksum_algorithm_not_allowed"),
        ({**build_checksum_contract(), "checksum_required": False}, "checksum_missing"),
        ({**build_checksum_contract(), "checksum_scope": []}, "checksum_scope_missing"),
        ({**build_checksum_contract(), "tamper_detection_required": False}, "tamper_detection_missing"),
        ({**build_checksum_contract(), "canonical_serialization_policy": ""}, "non_canonical_serialization"),
    ],
)
def test_dry_run_store_contract_e2e_blocks_invalid_checksum_policy(tmp_path, checksum, code):
    _inputs, kwargs, dry_run_contract, _prepared, simulated, _before = _build_e2e(tmp_path, "agent")

    report = validate_dry_run_store_contract(
        **_contract_kwargs(kwargs, dry_run_contract, simulated),
        checksum_contract=checksum,
    )

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(("field", "code"), REAL_PAYLOAD_FIELDS)
def test_dry_run_store_contract_e2e_blocks_forbidden_real_payload_fields(tmp_path, field, code):
    _inputs, kwargs, dry_run_contract, _prepared, simulated, _before = _build_e2e(tmp_path, "agent")
    mutated = {**simulated, field: {"real": True}}

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, mutated))

    assert report["status"] == "blocked"
    assert code in _codes(report)


@pytest.mark.parametrize(("field", "code"), PAYLOAD_BOUNDARY_FLAGS)
def test_dry_run_store_contract_e2e_blocks_payload_boundary_flags(tmp_path, field, code):
    _inputs, kwargs, dry_run_contract, _prepared, simulated, _before = _build_e2e(tmp_path, "agent")
    payload_boundary = build_payload_boundary_contract()
    payload_boundary[field] = True

    report = validate_dry_run_store_contract(
        **_contract_kwargs(kwargs, dry_run_contract, simulated),
        payload_boundary_contract=payload_boundary,
    )

    assert report["status"] == "blocked"
    assert code in _codes(report)


def test_dry_run_store_contract_e2e_declares_events_and_does_not_write_store(tmp_path):
    inputs, kwargs, dry_run_contract, _prepared, simulated, before = _build_e2e(tmp_path, "agent")

    report = validate_dry_run_store_contract(**_contract_kwargs(kwargs, dry_run_contract, simulated))

    assert set(report["audit_contract"]["audit_events_expected"]) == DRY_RUN_STORE_CONTRACT_EVENTS
    assert set(report["audit_contract"]["audit_events_forbidden"]) == FORBIDDEN_DRY_RUN_STORE_EVENTS
    exposed_events = set(report["audit_contract"]["audit_events_expected"]) | set(report["audit_contract"]["audit_events_forbidden"])
    assert DRY_RUN_STORE_CONTRACT_EVENTS <= exposed_events
    assert FORBIDDEN_DRY_RUN_STORE_EVENTS <= exposed_events
    assert report["store_summary"]["jsonl_written"] is False
    assert report["store_summary"]["storage_real_created"] is False
    assert report["store_summary"]["execution_attempt_id_created"] is False
    _assert_no_persistence_or_mutation(inputs, before)
