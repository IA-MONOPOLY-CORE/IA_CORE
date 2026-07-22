from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "EXECUTION_LIFECYCLE_IMPLEMENTATION_BOUNDARY_AUDIT.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"

READINESS = "EXECUTION_LIFECYCLE_READY_FOR_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION"
FUTURE_ALLOWED_FILE = "core/execution_lifecycle.py"
BLOCKED_FILES = {
    "core/execution_attempt_lifecycle.py",
    "core/execution_attempt_id.py",
    "core/execution_history_store.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
}
FUTURE_ALLOWED_FUNCTIONS = {
    "build_execution_lifecycle_entry",
    "append_execution_lifecycle_transition",
    "get_execution_lifecycle_entry",
    "list_execution_lifecycle_entries",
    "verify_execution_lifecycle_store",
    "replay_execution_lifecycle_idempotency",
    "compute_execution_lifecycle_entry_checksum",
    "canonicalize_execution_lifecycle_entry",
    "validate_execution_lifecycle_entry",
}
BLOCKED_FUNCTIONS = {
    "start_execution",
    "queue_execution",
    "run_execution",
    "complete_execution",
    "cancel_execution_real",
    "rollback_execution_real",
    "retry_execution_real",
    "invoke_model",
    "execute_tool",
    "persist_memory",
    "open_external_access",
    "start_scheduler",
    "start_worker",
    "dispatch_job",
    "process_queue",
}
IMPLEMENTABLE_STATES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
    "noop_idempotent",
}
BLOCKED_STATES = {
    "queued",
    "running",
    "completed",
    "cancelled",
    "rolled_back",
    "rolled_back_real",
    "aborted_real",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
IMPLEMENTABLE_TRANSITIONS = {
    "created -> preflight_passed",
    "created -> preflight_blocked",
    "created -> blocked",
    "created -> failed",
    "created -> not_applicable",
    "preflight_passed -> blocked",
    "preflight_blocked -> blocked",
    "blocked -> noop_idempotent",
    "failed -> noop_idempotent",
    "not_applicable -> noop_idempotent",
}
BLOCKED_TRANSITIONS = {
    "created -> queued",
    "preflight_passed -> queued",
    "queued -> running",
    "running -> completed",
    "running -> failed",
    "running -> cancelled",
    "running -> rolled_back",
    "completed -> rolled_back",
    "cancelled -> rolled_back",
    "any -> model_invoked",
    "any -> tool_executed",
    "any -> memory_persisted",
    "any -> external_accessed",
    "any -> scheduler_started",
    "any -> worker_started",
}
PAYLOAD_BLOCKED = {
    "execution_attempt_id",
    "attempt_id",
    "execution_payload",
    "execution_result",
    "execution_output",
    "agent_output",
    "team_output",
    "model_prompt_real",
    "model_response",
    "model_completion_real",
    "tool_call_real",
    "tool_result",
    "memory_write",
    "memory_read_result",
    "external_request",
    "external_response",
    "scheduler_job",
    "worker_task",
    "state_mutation",
    "artifact_mutation",
    "database_write_result",
    "network_response",
    "secret_value",
    "credential_value",
    "actual_output",
    "real_output",
    "live_response",
    "side_effect_result",
    "mutation_result",
}
ALLOWED_EVENTS = {
    "execution_lifecycle_transition_append_requested",
    "execution_lifecycle_transition_appended",
    "execution_lifecycle_transition_blocked",
    "execution_lifecycle_store_verified",
    "execution_lifecycle_idempotency_replayed",
    "execution_lifecycle_boundary_verified",
}
BLOCKED_EVENTS = {
    "execution_started",
    "execution_queued",
    "execution_running",
    "execution_completed",
    "execution_cancelled",
    "execution_rolled_back",
    "agent_execution_started",
    "team_execution_started",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
    "state_mutated",
    "artifact_mutated",
}


def _audit_text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_no_operational_lifecycle_attempt_id_history_or_queue_artifacts_exist():
    assert not (ROOT / "core" / "execution_lifecycle.py").exists()
    for relative in BLOCKED_FILES:
        assert not (ROOT / relative).exists(), relative


def test_future_file_policy_allows_only_execution_lifecycle_implementation():
    text = _audit_text()
    assert FUTURE_ALLOWED_FILE in text
    for relative in BLOCKED_FILES:
        assert relative in text


def test_future_store_policy_is_append_only_configurable_and_tmp_path_first():
    text = _audit_text()
    for phrase in [
        "execution_lifecycle_store",
        "append-only JSONL",
        "path configurable",
        "tests usando `tmp_path`",
        "sin escribir runtime real por defecto",
        "canonical serialization",
        "sha256 checksum",
        "`previous_entry_checksum`",
        "idempotency noop/conflict",
        "read-only get/list",
        "verify chain",
        "no overwrite",
        "no update",
        "no delete",
        "no truncate",
        "no replace",
    ]:
        assert phrase in text


def test_future_functions_allowed_and_operational_functions_blocked():
    text = _audit_text()
    for name in FUTURE_ALLOWED_FUNCTIONS | BLOCKED_FUNCTIONS:
        assert f"`{name}`" in text


def test_states_and_transitions_are_preflight_only():
    text = _audit_text()
    for state in IMPLEMENTABLE_STATES | BLOCKED_STATES:
        assert f"`{state}`" in text
    for transition in IMPLEMENTABLE_TRANSITIONS | BLOCKED_TRANSITIONS:
        assert f"`{transition}`" in text


def test_dependency_policy_requires_verified_contract_chain():
    text = _audit_text()
    for phrase in [
        "`execution_lifecycle_contract passed`",
        "`execution_attempt_store verified`",
        "`execution_attempt_store_contract passed`",
        "`attempt_ref` declarativo",
        "`dry_run_store verified`",
        "`dry_run_store_contract passed`",
        "`runtime_contract passed`",
        "`execution_contract passed`",
        "`runtime_executor_contract passed`",
        "`runtime_preparation prepared`",
        "`execution_runner_contract passed`",
        "`dry_run_contract passed`",
        "`audit_refs` presentes",
        "`observability_refs` presentes",
        "`correlation_id`",
        "`idempotency_key`",
    ]:
        assert phrase in text


def test_attempt_ref_id_policy_and_boundary_flags_are_locked_down():
    text = _audit_text()
    for phrase in [
        "`attempt_ref` declarativo obligatorio",
        "`attempt_ref` empieza con `preflight:`",
        "`attempt_ref_is_operational_id=false`",
        "`execution_attempt_id` operativo prohibido",
        "`attempt_id_generation=disabled`",
        "`attempt_id_persistence=disabled`",
        "`materialized_attempt_id=false`",
        "`execution_enabled=false`",
        "`agent_execution_enabled=false`",
        "`team_execution_enabled=false`",
        "`model_invocation_enabled=false`",
        "`tool_execution_enabled=false`",
        "`memory_persistence_enabled=false`",
        "`external_access_enabled=false`",
        "`scheduler_enabled=false`",
        "`worker_queue_enabled=false`",
        "`rollback_operational_enabled=false`",
        "`retry_operational_enabled=false`",
        "`cancel_operational_enabled=false`",
    ]:
        assert phrase in text


def test_payloads_and_events_boundaries_are_documented():
    text = _audit_text()
    for item in PAYLOAD_BLOCKED | ALLOWED_EVENTS | BLOCKED_EVENTS:
        assert f"`{item}`" in text


def test_no_existing_runtime_lifecycle_or_store_jsonl_paths():
    forbidden_paths = [
        "runtime/execution_lifecycle_store.jsonl",
        "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
        "storage/execution_lifecycle_store.jsonl",
        "data/execution_lifecycle_store.jsonl",
        "logs/execution_lifecycle_store.jsonl",
        "runtime/execution_attempts/execution_attempt_store.jsonl",
        "runtime/dry_runs/dry_run_store.jsonl",
    ]
    for relative in forbidden_paths:
        assert not (ROOT / relative).exists(), relative


def test_execution_attempt_store_and_runner_are_not_modified_by_future_boundary():
    attempt_store = (ROOT / "core" / "execution_attempt_store.py").read_text(encoding="utf-8")
    runner = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")
    assert "append_execution_lifecycle_transition" not in attempt_store
    assert "append_execution_lifecycle_transition" not in runner
    assert "execution_lifecycle_store" not in attempt_store
    assert "execution_lifecycle_store" not in runner


def test_readiness_and_next_prompt_are_coherent():
    text = _audit_text()
    book = BOOK_DOC.read_text(encoding="utf-8")
    assert READINESS in text
    assert "PROMPT 2.41 - Implementar execution_lifecycle preflight-transitions-only append-only" in text
    assert "PROMPT 2.40 - Auditoria de frontera de implementacion execution_lifecycle preflight-transitions-only" in book
    assert READINESS in book


def test_no_real_execution_external_ui_or_mutation_scope_is_opened():
    text = _audit_text()
    for phrase in [
        "No significa readiness para lifecycle operativo",
        "No se detecta `core/execution_lifecycle.py`",
        "no como `execution_lifecycle` operativo",
        "No deben disparar ejecucion ni modificar targets",
        "sin ejecucion real",
        "modelos/tools/memoria/external access",
        "scheduler/worker",
    ]:
        assert phrase in text
