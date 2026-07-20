from pathlib import Path


ROOT = Path(__file__).parent.parent

READINESS_VERDICT = "ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY"
NEXT_PROMPT = "PROMPT 2.35 - Disenar execution_attempt_store_contract preflight-only sin implementation"

FUTURE_ALLOWED_FIELDS = {
    "execution_attempt_id",
    "attempt_type",
    "attempt_mode",
    "target_ref",
    "dry_run_ref",
    "dry_run_store_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "runtime_preparation_ref",
    "execution_contract_ref",
    "runtime_contract_ref",
    "status",
    "lifecycle_state",
    "created_at",
    "actor",
    "reason",
    "correlation_id",
    "idempotency_key",
    "preflight_summary",
    "readiness_summary",
    "boundary_summary",
    "risk_summary",
    "blocked_capabilities",
    "audit_refs",
    "observability_refs",
    "warnings",
    "blockers",
    "evidence",
    "checksum",
    "previous_entry_checksum",
}

REQUIRED_FUTURE_REFS = {
    "dry_run_ref",
    "dry_run_store_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
    "runtime_preparation_ref",
    "execution_contract_ref",
    "runtime_contract_ref",
    "correlation_id",
    "idempotency_key",
    "audit_refs",
    "observability_refs",
}

PRE_EXECUTION_STATES = {
    "created",
    "preflight_passed",
    "preflight_blocked",
    "blocked",
    "failed",
    "not_applicable",
}

BLOCKED_STATES = {
    "queued_future",
    "running_future",
    "completed_future",
    "model_invoked",
    "tool_executed",
    "memory_persisted",
    "external_accessed",
}

FORBIDDEN_PAYLOAD_FIELDS = {
    "real_execution_payload",
    "agent_output_real",
    "team_output_real",
    "model_prompt_real",
    "model_response_real",
    "tool_call_real",
    "tool_result_real",
    "memory_write_real",
    "memory_read_result_real",
    "external_request",
    "external_response",
    "scheduler_job",
    "worker_task",
    "state_mutation_result",
    "artifact_mutation_result",
    "secret_value",
    "credential_value",
}

FUTURE_BLOCKERS = {
    "missing_attempt_id_policy",
    "missing_attempt_lifecycle_policy",
    "missing_dry_run_ref",
    "dry_run_store_not_verified",
    "missing_execution_runner_contract_ref",
    "missing_runtime_preparation_ref",
    "missing_execution_contract_ref",
    "missing_runtime_contract_ref",
    "missing_correlation_id",
    "missing_idempotency_key",
    "missing_audit_refs",
    "missing_observability_refs",
    "invalid_attempt_mode",
    "invalid_lifecycle_state",
    "execution_payload_not_allowed",
    "agent_output_not_allowed",
    "team_output_not_allowed",
    "model_prompt_not_allowed",
    "model_response_not_allowed",
    "tool_call_not_allowed",
    "tool_result_not_allowed",
    "memory_write_not_allowed",
    "memory_read_result_not_allowed",
    "external_request_not_allowed",
    "external_response_not_allowed",
    "scheduler_job_not_allowed",
    "worker_task_not_allowed",
    "state_mutation_not_allowed",
    "artifact_mutation_not_allowed",
    "secret_value_not_allowed",
    "credential_value_not_allowed",
    "running_state_not_allowed",
    "completed_state_not_allowed",
    "model_invoked_state_not_allowed",
    "tool_executed_state_not_allowed",
    "execution_lifecycle_not_ready",
    "scheduler_boundary_missing",
    "worker_queue_boundary_missing",
    "model_boundary_missing",
    "tool_boundary_missing",
    "memory_boundary_missing",
    "external_access_boundary_missing",
}


def _doc_text() -> str:
    return (ROOT / "docs" / "EXECUTION_ATTEMPT_STORE_BOUNDARY_AUDIT.md").read_text(encoding="utf-8")


def test_no_operational_execution_attempt_store_or_aliases_exist():
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "execution_history_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "attempt_lifecycle.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "scheduler_queue.py").exists()
    assert not (ROOT / "core" / "worker_queue.py").exists()
    assert not list((ROOT / "core").glob("*execution_attempt*.jsonl"))


def test_dry_run_store_append_only_e2e_passed_does_not_imply_attempt_store():
    checkpoint = (ROOT / "docs" / "DRY_RUN_STORE_APPEND_ONLY_E2E_CHECKPOINT.md").read_text(encoding="utf-8")

    assert "PASSED_DRY_RUN_STORE_APPEND_ONLY_E2E" in checkpoint
    assert (ROOT / "core" / "dry_run_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_store.py").exists()
    assert "execution_attempt_id" in checkpoint
    assert "- no `execution_attempt_id`;" in checkpoint


def test_future_attempt_store_is_distinct_from_dry_run_store():
    text = _doc_text()

    assert "`execution_attempt_store` registra intentos" in text
    assert "`dry_run_store` registra simulaciones" in text
    assert "No debe transformar dry-run en ejecucion" in text
    assert "ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY" in text


def test_future_attempt_store_requires_dry_run_refs_audit_observability_and_idempotency():
    assert {"dry_run_ref", "dry_run_store_ref"} <= REQUIRED_FUTURE_REFS
    assert {"audit_refs", "observability_refs"} <= REQUIRED_FUTURE_REFS
    assert {"correlation_id", "idempotency_key"} <= REQUIRED_FUTURE_REFS
    assert "dry_run_store_not_verified" in FUTURE_BLOCKERS
    assert "missing_correlation_id" in FUTURE_BLOCKERS
    assert "missing_idempotency_key" in FUTURE_BLOCKERS
    assert "missing_audit_refs" in FUTURE_BLOCKERS
    assert "missing_observability_refs" in FUTURE_BLOCKERS


def test_future_attempt_store_blocks_real_payloads_outputs_models_tools_memory_external_queue_and_mutation():
    expected = {
        "real_execution_payload",
        "agent_output_real",
        "team_output_real",
        "model_prompt_real",
        "model_response_real",
        "tool_call_real",
        "tool_result_real",
        "memory_write_real",
        "memory_read_result_real",
        "external_request",
        "external_response",
        "scheduler_job",
        "worker_task",
        "state_mutation_result",
        "artifact_mutation_result",
        "secret_value",
        "credential_value",
    }

    assert expected <= FORBIDDEN_PAYLOAD_FIELDS
    assert "execution_payload_not_allowed" in FUTURE_BLOCKERS
    assert "agent_output_not_allowed" in FUTURE_BLOCKERS
    assert "team_output_not_allowed" in FUTURE_BLOCKERS
    assert "model_prompt_not_allowed" in FUTURE_BLOCKERS
    assert "model_response_not_allowed" in FUTURE_BLOCKERS
    assert "tool_call_not_allowed" in FUTURE_BLOCKERS
    assert "tool_result_not_allowed" in FUTURE_BLOCKERS
    assert "memory_write_not_allowed" in FUTURE_BLOCKERS
    assert "memory_read_result_not_allowed" in FUTURE_BLOCKERS
    assert "external_request_not_allowed" in FUTURE_BLOCKERS
    assert "external_response_not_allowed" in FUTURE_BLOCKERS
    assert "scheduler_job_not_allowed" in FUTURE_BLOCKERS
    assert "worker_task_not_allowed" in FUTURE_BLOCKERS
    assert "state_mutation_not_allowed" in FUTURE_BLOCKERS
    assert "artifact_mutation_not_allowed" in FUTURE_BLOCKERS
    assert "secret_value_not_allowed" in FUTURE_BLOCKERS
    assert "credential_value_not_allowed" in FUTURE_BLOCKERS


def test_future_attempt_store_allows_only_preflight_concept_and_blocks_execution_states():
    assert {"created", "preflight_passed", "preflight_blocked", "blocked"} <= PRE_EXECUTION_STATES
    assert "running_future" in BLOCKED_STATES
    assert "completed_future" in BLOCKED_STATES
    assert "model_invoked" in BLOCKED_STATES
    assert "tool_executed" in BLOCKED_STATES
    assert "running_state_not_allowed" in FUTURE_BLOCKERS
    assert "completed_state_not_allowed" in FUTURE_BLOCKERS
    assert "model_invoked_state_not_allowed" in FUTURE_BLOCKERS
    assert "tool_executed_state_not_allowed" in FUTURE_BLOCKERS


def test_no_core_runner_or_store_contract_boundary_was_crossed():
    dry_run_store = (ROOT / "core" / "dry_run_store.py").read_text(encoding="utf-8")
    execution_runner = (ROOT / "core" / "execution_runner.py").read_text(encoding="utf-8")

    assert "execution_attempt_store_not_allowed" in dry_run_store
    assert "execution_attempt_store_enabled" in execution_runner
    assert "model_invoked" not in dry_run_store
    assert "tool_executed" not in dry_run_store
    assert not (ROOT / "runtime" / "execution_attempt_store.jsonl").exists()
    assert not (ROOT / "runtime" / "execution_attempts").exists()


def test_audit_document_covers_required_questions_and_next_step():
    text = _doc_text()

    for marker in [
        "## 1. Resumen Ejecutivo",
        "## 2. Definicion de execution_attempt_store",
        "## 3. Que NO Es execution_attempt_store",
        "## 4. Diferencia Con dry_run_store",
        "## 5. Que Podria Guardar Inicialmente execution_attempt_store",
        "## 6. Que NO Puede Guardar Todavia",
        "## 7. Lifecycle Futuro",
        "## 8. Riesgos de Disenar execution_attempt_store",
        "## 9. Requisitos Antes Del Contrato",
        "## 10. Readiness",
        "## 11. Relacion Con dry_run_store",
        "## 12. Relacion Con audit_store/observability",
        "## 13. Blockers Futuros Obligatorios",
        "## 14. Proximo Paso Recomendado",
        "## 15. Auditoria Arquitectonica Final",
    ]:
        assert marker in text

    assert READINESS_VERDICT in text
    assert NEXT_PROMPT in text


def test_future_allowed_fields_are_preflight_only_and_do_not_execute_anything():
    assert REQUIRED_FUTURE_REFS <= FUTURE_ALLOWED_FIELDS
    assert "preflight_summary" in FUTURE_ALLOWED_FIELDS
    assert "readiness_summary" in FUTURE_ALLOWED_FIELDS
    assert "boundary_summary" in FUTURE_ALLOWED_FIELDS
    assert "risk_summary" in FUTURE_ALLOWED_FIELDS
    assert "blocked_capabilities" in FUTURE_ALLOWED_FIELDS
    assert "model_response_real" not in FUTURE_ALLOWED_FIELDS
    assert "tool_call_real" not in FUTURE_ALLOWED_FIELDS
    assert "memory_write_real" not in FUTURE_ALLOWED_FIELDS
    assert "scheduler_job" not in FUTURE_ALLOWED_FIELDS
    assert "worker_task" not in FUTURE_ALLOWED_FIELDS


def test_no_targets_global_legacy_or_ui_integration_runtime_attempt_paths_exist():
    for forbidden in [
        ROOT / "domains" / "execution_attempts",
        ROOT / "domains" / "execution_attempt_store",
        ROOT / "memoria_agentes" / "execution_attempts",
        ROOT / "memory" / "execution_attempts",
        ROOT / "ui" / "execution_attempt_store",
        ROOT / "integrations" / "execution_attempt_store",
    ]:
        assert not forbidden.exists()
