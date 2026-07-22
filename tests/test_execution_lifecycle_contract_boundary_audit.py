from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "EXECUTION_LIFECYCLE_CONTRACT_BOUNDARY_AUDIT.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"

READINESS_VERDICT = "LIFECYCLE_READY_FOR_CONTRACT_ONLY"

FUTURE_CONCEPTUAL_STATES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "queued_future",
    "running_future",
    "completed_future",
    "failed_future",
    "cancelled_future",
    "aborted_future",
    "rolled_back_future",
    "noop_idempotent",
    "blocked",
}
FIRST_CONTRACT_ALLOWED_STATES = {
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
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
    "scheduler_started",
    "worker_started",
}
ALLOWED_TRANSITIONS = {
    ("created", "preflight_passed"),
    ("created", "preflight_blocked"),
    ("created", "blocked"),
    ("created", "failed"),
    ("preflight_passed", "blocked"),
    ("preflight_blocked", "blocked"),
    ("blocked", "noop_idempotent"),
    ("failed", "noop_idempotent"),
}
BLOCKED_TRANSITIONS = {
    ("preflight_passed", "queued"),
    ("queued", "running"),
    ("running", "completed"),
    ("running", "failed"),
    ("running", "cancelled"),
    ("running", "rolled_back"),
    ("completed", "rolled_back"),
}
REQUIREMENT_CATEGORIES = {
    "REQUIRED_BEFORE_LIFECYCLE_CONTRACT",
    "REQUIRED_BEFORE_LIFECYCLE_IMPLEMENTATION",
    "REQUIRED_BEFORE_QUEUED_RUNNING_STATES",
    "REQUIRED_BEFORE_AGENT_TEAM_EXECUTION",
    "REQUIRED_BEFORE_MODEL_INVOCATION",
    "REQUIRED_BEFORE_TOOL_EXECUTION",
    "REQUIRED_BEFORE_MEMORY_PERSISTENCE",
    "REQUIRED_BEFORE_EXTERNAL_ACCESS",
    "REQUIRED_BEFORE_SCHEDULER_QUEUE",
    "NOT_REQUIRED_YET",
}
FUTURE_BLOCKERS = {
    "missing_execution_attempt_store_preflight_e2e",
    "missing_attempt_ref",
    "attempt_ref_materialized_as_execution_attempt_id",
    "execution_attempt_id_operational_not_allowed",
    "missing_lifecycle_state_schema",
    "invalid_lifecycle_state",
    "queued_state_not_allowed",
    "running_state_not_allowed",
    "completed_state_not_allowed",
    "cancelled_state_not_allowed",
    "rolled_back_state_not_allowed",
    "model_invoked_state_not_allowed",
    "tool_executed_state_not_allowed",
    "memory_persisted_state_not_allowed",
    "external_accessed_state_not_allowed",
    "scheduler_started_state_not_allowed",
    "worker_started_state_not_allowed",
    "invalid_transition",
    "queued_transition_not_allowed",
    "running_transition_not_allowed",
    "completed_transition_not_allowed",
    "retry_policy_not_ready",
    "cancel_policy_not_ready",
    "rollback_policy_not_ready",
    "scheduler_boundary_missing",
    "worker_queue_boundary_missing",
    "model_boundary_missing",
    "tool_boundary_missing",
    "memory_boundary_missing",
    "external_access_boundary_missing",
    "execution_payload_not_allowed",
    "execution_result_not_allowed",
    "agent_output_not_allowed",
    "team_output_not_allowed",
    "model_response_not_allowed",
    "tool_result_not_allowed",
    "memory_payload_not_allowed",
    "external_response_not_allowed",
    "state_mutation_not_allowed",
    "artifact_mutation_not_allowed",
    "secret_value_not_allowed",
    "credential_value_not_allowed",
}


def _audit_text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_readiness_verdict_is_contract_only():
    text = _audit_text()
    assert READINESS_VERDICT in text
    assert "preflight-transitions-only" in text
    assert "No ejecuta nada" in text or "no ejecuta nada" in text


def test_forbidden_lifecycle_modules_do_not_exist():
    assert (ROOT / "core" / "execution_lifecycle.py").exists()
    forbidden = [
        "core/execution_attempt_lifecycle.py",
        "core/execution_attempt_id.py",
        "core/execution_history_store.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
    ]
    for relative in forbidden:
        assert not (ROOT / relative).exists(), relative
    assert (ROOT / "core" / "execution_lifecycle_schema.py").exists()
    assert (ROOT / "core" / "execution_lifecycle_contract.py").exists()


def test_attempt_store_e2e_checkpoint_is_required_and_passed():
    checkpoint = (ROOT / "docs" / "EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E_CHECKPOINT.md").read_text(encoding="utf-8")
    assert "PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E" in checkpoint
    assert "attempt_ref" in checkpoint
    assert "declarativo" in checkpoint
    assert "sin `execution_attempt_id` operativo" in checkpoint


def test_state_sets_keep_future_states_separate_from_first_contract():
    assert {"queued_future", "running_future", "completed_future"} <= FUTURE_CONCEPTUAL_STATES
    assert FIRST_CONTRACT_ALLOWED_STATES <= FUTURE_CONCEPTUAL_STATES | {"not_applicable", "failed"}
    assert {"queued", "running", "completed", "model_invoked", "tool_executed"} <= BLOCKED_STATES
    assert {"memory_persisted", "external_accessed", "scheduler_started", "worker_started"} <= BLOCKED_STATES


def test_audit_doc_lists_allowed_and_blocked_states():
    text = _audit_text()
    for state in FIRST_CONTRACT_ALLOWED_STATES | BLOCKED_STATES:
        assert f"`{state}`" in text


def test_transition_sets_are_preflight_only():
    assert ("created", "preflight_passed") in ALLOWED_TRANSITIONS
    assert ("created", "preflight_blocked") in ALLOWED_TRANSITIONS
    assert ("queued", "running") in BLOCKED_TRANSITIONS
    assert ("running", "completed") in BLOCKED_TRANSITIONS
    assert not any(origin == "running" for origin, _ in ALLOWED_TRANSITIONS)
    assert not any(target == "queued" for _, target in ALLOWED_TRANSITIONS)


def test_audit_doc_lists_transition_boundaries():
    text = _audit_text()
    for origin, target in ALLOWED_TRANSITIONS | BLOCKED_TRANSITIONS:
        assert f"`{origin} -> {target}`" in text


def test_requirement_categories_are_complete():
    text = _audit_text()
    for category in REQUIREMENT_CATEGORIES:
        assert f"`{category}`" in text


def test_future_requirements_cover_retry_cancel_rollback_and_boundaries():
    text = _audit_text()
    for phrase in [
        "retry policy",
        "cancel policy",
        "rollback policy",
        "scheduler boundary",
        "worker boundary",
        "model boundary contract",
        "tool boundary contract",
        "memory boundary contract",
        "external access boundary contract",
    ]:
        assert phrase in text


def test_future_blockers_are_declared():
    text = _audit_text()
    for blocker in FUTURE_BLOCKERS:
        assert f"`{blocker}`" in text


def test_payload_and_mutation_boundaries_are_declared():
    text = _audit_text()
    for blocker in [
        "execution_payload_not_allowed",
        "execution_result_not_allowed",
        "agent_output_not_allowed",
        "team_output_not_allowed",
        "model_response_not_allowed",
        "tool_result_not_allowed",
        "memory_payload_not_allowed",
        "external_response_not_allowed",
        "state_mutation_not_allowed",
        "artifact_mutation_not_allowed",
        "secret_value_not_allowed",
        "credential_value_not_allowed",
    ]:
        assert f"`{blocker}`" in text


def test_attempt_store_and_runner_are_not_connected_to_execution_lifecycle():
    for relative in ["core/execution_attempt_store.py", "core/execution_runner.py"]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "execution_lifecycle" not in text
        assert "append_execution_lifecycle" not in text
        assert "core.execution_lifecycle" not in text


def test_no_real_execution_or_external_artifacts_are_created():
    forbidden = [
        "core/execution_history_store.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
        "core/model_invocation_log.py",
        "core/tool_execution_log.py",
        "core/external_access_log.py",
    ]
    for relative in forbidden:
        assert not (ROOT / relative).exists(), relative


def test_book_registers_prompt_238_boundary_audit():
    text = BOOK_DOC.read_text(encoding="utf-8")
    assert "PROMPT 2.38 - Auditoria de frontera execution lifecycle contract" in text
    assert READINESS_VERDICT in text
    assert "docs/EXECUTION_LIFECYCLE_CONTRACT_BOUNDARY_AUDIT.md" in text
    assert "tests/test_execution_lifecycle_contract_boundary_audit.py" in text


def test_next_prompt_is_239_contract_only_design():
    text = _audit_text()
    assert "PROMPT 2.39" in text
    assert "execution_lifecycle_contract preflight-transitions-only sin implementation" in text
