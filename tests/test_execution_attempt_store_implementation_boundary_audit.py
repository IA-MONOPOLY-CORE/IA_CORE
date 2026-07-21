from pathlib import Path


ROOT = Path(__file__).parent.parent

FUTURE_ALLOWED_FILE = "core/execution_attempt_store.py"
RECOMMENDED_STORAGE_PATH = "runtime/execution_attempts/execution_attempt_store.jsonl"
READINESS_VERDICT = "EXECUTION_ATTEMPT_STORE_READY_FOR_PREFLIGHT_ONLY_IMPLEMENTATION"

FUTURE_PREFLIGHT_FUNCTIONS = {
    "build_execution_attempt_preflight_entry",
    "append_execution_attempt_preflight",
    "get_execution_attempt_preflight",
    "list_execution_attempt_preflights",
    "verify_execution_attempt_store",
    "replay_execution_attempt_preflight_idempotency",
    "compute_execution_attempt_entry_checksum",
    "canonicalize_execution_attempt_store_entry",
    "validate_execution_attempt_store_entry",
}

PROHIBITED_FUNCTIONS = {
    "create_execution_attempt",
    "start_execution_attempt",
    "run_execution_attempt",
    "queue_execution_attempt",
    "complete_execution_attempt",
    "fail_execution_attempt",
    "cancel_execution_attempt",
    "rollback_execution_attempt",
    "execute_agent",
    "execute_team",
    "invoke_model",
    "execute_tool",
    "persist_memory",
    "enqueue_job",
    "start_worker",
}

ATTEMPT_REF_POLICY = {
    "attempt_ref_allowed": True,
    "attempt_ref_example": "preflight:<target_type>:<target_id>:<correlation_id>:<idempotency_key>",
    "execution_attempt_id_operational_allowed": False,
    "attempt_id_generation": "disabled",
    "attempt_id_persistence": "disabled",
    "materialized_attempt_id": False,
}

ALLOWED_STATUSES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
    "noop_idempotent",
}

BLOCKED_STATUSES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back_real",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}

REQUIRED_DRY_RUN_DEPENDENCIES = {
    "execution_attempt_store_contract_passed",
    "dry_run_store_ref",
    "dry_run_store_verified",
    "dry_run_ref",
    "dry_run_result_mode_dry_run_result_only",
    "dry_run_result_status_simulated",
    "dry_run_store_checksum_ref",
    "dry_run_store_verified_report",
}

IDEMPOTENCY_SCOPE = {
    "target_type",
    "target_id",
    "attempt_ref",
    "correlation_id",
    "idempotency_key",
    "dry_run_ref",
    "dry_run_store_checksum_ref",
    "execution_attempt_store_contract_ref",
}

CANONICAL_CHECKSUM_POLICY = {
    "sort_keys": True,
    "separators": "compact",
    "encoding": "utf-8",
    "pretty_print": False,
    "line_ending": "\n",
    "checksum_algorithm": "sha256",
    "entry_checksum_required": True,
    "previous_entry_checksum_required": True,
    "tamper_detection_required": True,
}

FUTURE_ALLOWED_OPERATIONS = {
    "append_preflight_record",
    "read_by_attempt_ref",
    "list_read_only",
    "verify_store",
    "idempotency_replay",
}

PROHIBITED_OPERATIONS = {
    "overwrite",
    "update",
    "delete",
    "truncate",
    "replace",
    "compact_without_policy",
    "create_execution_attempt_id_operational",
    "start_attempt",
    "queue_attempt",
    "run_attempt",
    "complete_attempt",
    "write_execution_payload",
    "write_real_outputs",
    "write_model_tool_memory_external_payloads",
    "mutate_target",
}

PROHIBITED_PAYLOADS = {
    "execution_payload",
    "execution_result",
    "agent_output",
    "team_output",
    "model_prompt",
    "model_response",
    "tool_call",
    "tool_result",
    "memory_payload",
    "external_request",
    "external_response",
    "scheduler_job",
    "worker_task",
    "state_mutation",
    "artifact_mutation",
    "secret_value",
    "credential_value",
}

FUTURE_BLOCKERS = {
    "missing_execution_attempt_store_contract",
    "execution_attempt_store_contract_not_passed",
    "missing_attempt_ref",
    "attempt_ref_materialized_as_execution_attempt_id",
    "attempt_id_generation_enabled",
    "attempt_id_persistence_enabled",
    "materialized_attempt_id",
    "missing_dry_run_ref",
    "missing_dry_run_store_ref",
    "dry_run_store_not_verified",
    "dry_run_store_checksum_missing",
    "dry_run_store_checksum_mismatch",
    "dry_run_result_not_result_only",
    "dry_run_result_not_simulated",
    "missing_runtime_contract_ref",
    "missing_execution_contract_ref",
    "missing_runtime_executor_contract_ref",
    "missing_runtime_preparation_ref",
    "missing_execution_runner_contract_ref",
    "missing_dry_run_contract_ref",
    "missing_dry_run_store_contract_ref",
    "missing_audit_refs",
    "missing_observability_refs",
    "missing_capability_policy_ref",
    "missing_correlation_id",
    "missing_idempotency_key",
    "invalid_status",
    "running_status_not_allowed",
    "completed_status_not_allowed",
    "queued_status_not_allowed",
    "execution_payload_not_allowed",
    "execution_result_not_allowed",
    "agent_output_not_allowed",
    "team_output_not_allowed",
    "model_prompt_not_allowed",
    "model_response_not_allowed",
    "tool_call_not_allowed",
    "tool_result_not_allowed",
    "memory_payload_not_allowed",
    "external_request_not_allowed",
    "external_response_not_allowed",
    "scheduler_job_not_allowed",
    "worker_task_not_allowed",
    "state_mutation_not_allowed",
    "artifact_mutation_not_allowed",
    "secret_value_not_allowed",
    "credential_value_not_allowed",
    "overwrite_not_allowed",
    "update_not_allowed",
    "delete_not_allowed",
    "truncate_not_allowed",
    "replace_not_allowed",
    "execution_lifecycle_not_ready",
    "execution_runner_not_allowed_to_persist_attempts_yet",
}


def _doc_text() -> str:
    return (ROOT / "docs" / "EXECUTION_ATTEMPT_STORE_IMPLEMENTATION_BOUNDARY_AUDIT.md").read_text(encoding="utf-8")


def test_no_operational_execution_attempt_store_or_attempt_artifacts_exist():
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not (ROOT / "runtime" / "execution_attempts").exists()
    assert not list((ROOT / "runtime").glob("**/*execution_attempt*.jsonl"))


def test_future_file_and_functions_are_preflight_only_not_execution():
    assert FUTURE_ALLOWED_FILE == "core/execution_attempt_store.py"
    assert "append_execution_attempt_preflight" in FUTURE_PREFLIGHT_FUNCTIONS
    assert all("preflight" in name or name in {"verify_execution_attempt_store", "compute_execution_attempt_entry_checksum", "canonicalize_execution_attempt_store_entry", "validate_execution_attempt_store_entry"} for name in FUTURE_PREFLIGHT_FUNCTIONS)
    assert "run_execution_attempt" in PROHIBITED_FUNCTIONS
    assert FUTURE_PREFLIGHT_FUNCTIONS.isdisjoint(PROHIBITED_FUNCTIONS)


def test_storage_is_configurable_testable_and_tmp_path_required_for_future_tests():
    text = _doc_text()
    assert RECOMMENDED_STORAGE_PATH in text
    assert "configurable/testable" in text
    assert "tmp_path" in text
    assert "No se escribe JSONL real de attempts" not in text


def test_attempt_ref_policy_does_not_materialize_operational_attempt_id():
    assert ATTEMPT_REF_POLICY["attempt_ref_allowed"] is True
    assert ATTEMPT_REF_POLICY["attempt_ref_example"].startswith("preflight:")
    assert ATTEMPT_REF_POLICY["execution_attempt_id_operational_allowed"] is False
    assert ATTEMPT_REF_POLICY["attempt_id_generation"] == "disabled"
    assert ATTEMPT_REF_POLICY["attempt_id_persistence"] == "disabled"
    assert ATTEMPT_REF_POLICY["materialized_attempt_id"] is False


def test_preflight_statuses_allowed_and_execution_lifecycle_statuses_blocked():
    assert {"created", "preflight_passed", "preflight_blocked", "noop_idempotent"} <= ALLOWED_STATUSES
    assert {"running", "completed", "model_invoked", "tool_executed", "memory_persisted"} <= BLOCKED_STATUSES
    assert ALLOWED_STATUSES.isdisjoint(BLOCKED_STATUSES)


def test_dry_run_store_dependency_and_reference_only_policy_defined():
    assert {
        "execution_attempt_store_contract_passed",
        "dry_run_store_ref",
        "dry_run_store_verified",
        "dry_run_ref",
        "dry_run_result_mode_dry_run_result_only",
        "dry_run_result_status_simulated",
        "dry_run_store_checksum_ref",
    } <= REQUIRED_DRY_RUN_DEPENDENCIES
    text = _doc_text()
    assert "Debe referenciar, no copiar payloads" in text
    assert "No convierte dry-run en ejecucion" in text


def test_idempotency_and_checksum_policies_are_defined():
    assert {
        "target_type",
        "target_id",
        "attempt_ref",
        "correlation_id",
        "idempotency_key",
        "dry_run_ref",
        "dry_run_store_checksum_ref",
        "execution_attempt_store_contract_ref",
    } <= IDEMPOTENCY_SCOPE
    assert CANONICAL_CHECKSUM_POLICY["sort_keys"] is True
    assert CANONICAL_CHECKSUM_POLICY["checksum_algorithm"] == "sha256"
    assert CANONICAL_CHECKSUM_POLICY["entry_checksum_required"] is True
    assert CANONICAL_CHECKSUM_POLICY["previous_entry_checksum_required"] is True
    assert CANONICAL_CHECKSUM_POLICY["tamper_detection_required"] is True


def test_allowed_and_prohibited_operations_are_separated():
    assert {"append_preflight_record", "read_by_attempt_ref", "list_read_only", "verify_store", "idempotency_replay"} <= FUTURE_ALLOWED_OPERATIONS
    assert {"overwrite", "update", "delete", "truncate", "replace", "run_attempt", "mutate_target"} <= PROHIBITED_OPERATIONS
    assert FUTURE_ALLOWED_OPERATIONS.isdisjoint(PROHIBITED_OPERATIONS)


def test_payloads_real_execution_and_external_boundaries_remain_prohibited():
    assert {"execution_payload", "execution_result", "agent_output", "team_output"} <= PROHIBITED_PAYLOADS
    assert {"model_prompt", "model_response", "tool_call", "tool_result", "memory_payload"} <= PROHIBITED_PAYLOADS
    assert {"external_request", "external_response", "scheduler_job", "worker_task"} <= PROHIBITED_PAYLOADS
    assert {"state_mutation", "artifact_mutation", "secret_value", "credential_value"} <= PROHIBITED_PAYLOADS


def test_future_blockers_cover_dependencies_payloads_lifecycle_and_mutation():
    expected = {
        "missing_execution_attempt_store_contract",
        "execution_attempt_store_contract_not_passed",
        "missing_attempt_ref",
        "attempt_ref_materialized_as_execution_attempt_id",
        "dry_run_store_not_verified",
        "dry_run_store_checksum_missing",
        "running_status_not_allowed",
        "completed_status_not_allowed",
        "queued_status_not_allowed",
        "execution_payload_not_allowed",
        "model_response_not_allowed",
        "tool_result_not_allowed",
        "memory_payload_not_allowed",
        "external_response_not_allowed",
        "scheduler_job_not_allowed",
        "worker_task_not_allowed",
        "state_mutation_not_allowed",
        "artifact_mutation_not_allowed",
        "overwrite_not_allowed",
        "replace_not_allowed",
        "execution_runner_not_allowed_to_persist_attempts_yet",
    }
    assert expected <= FUTURE_BLOCKERS


def test_existing_dry_run_store_and_execution_runner_remain_unchanged_boundaries():
    dry_run_store_text = (ROOT / "core" / "dry_run_store.py").read_text(encoding="utf-8")
    execution_runner_text = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")
    assert "execution_attempt_store_not_allowed" in dry_run_store_text
    assert "execution_attempt_store_enabled" in execution_runner_text
    assert "append_execution_attempt_preflight" not in dry_run_store_text
    assert "create_execution_attempt" not in execution_runner_text


def test_no_real_execution_agent_team_model_tool_memory_external_ui_or_mutation_is_enabled():
    text = _doc_text()
    for forbidden in [
        "sin ejecucion real",
        "sin lifecycle real",
        "sin `execution_attempt_id` operativo",
        "No seria ejecucion",
        "write model/tool/memory/external payloads",
        "mutate target",
    ]:
        assert forbidden in text
    assert not (ROOT / "ui" / "execution_attempt_store").exists()
    assert not (ROOT / "integrations" / "execution_attempt_store").exists()


def test_readiness_verdict_and_next_step_are_documented():
    text = _doc_text()
    assert READINESS_VERDICT in text
    assert "implementar `execution_attempt_store` preflight-only en prompt dedicado" in text
    assert "No implica readiness para lifecycle real" in text

