from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "EXECUTION_HISTORY_VIEW_IMPLEMENTATION_BOUNDARY_AUDIT.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"

READINESS = "HISTORY_VIEW_READY_FOR_DERIVED_ONLY_IMPLEMENTATION"
FUTURE_ALLOWED_FILE = "core/execution_history_view.py"
FORBIDDEN_FILES = {
    "core/execution_history_store.py",
    "core/attempt_history.py",
    "core/execution_attempt_history.py",
    "core/execution_result_store.py",
    "core/execution_attempt_id.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
}
UNCHANGED_CORE_FILES = {
    "core/execution_history_view_contract.py",
    "core/execution_lifecycle.py",
    "core/execution_attempt_store.py",
    "core/dry_run_store.py",
    "core/execution_runner.py",
}
FUTURE_ALLOWED_FUNCTIONS = {
    "build_execution_history_view",
    "derive_execution_history_timeline",
    "derive_preflight_status",
    "derive_transition_history",
    "derive_store_verification_summary",
    "derive_boundary_summary",
    "derive_risk_summary",
    "validate_execution_history_view",
}
BLOCKED_FUNCTIONS = {
    "append_execution_history",
    "write_execution_history",
    "persist_execution_history",
    "create_execution_history_store",
    "append_execution_result",
    "write_execution_result",
    "create_execution_attempt_id",
    "start_execution",
    "queue_execution",
    "run_execution",
    "complete_execution",
    "invoke_model",
    "execute_tool",
    "persist_memory",
    "open_external_access",
    "start_scheduler",
    "start_worker",
    "dispatch_job",
    "process_queue",
}
REQUIRED_INPUTS = {
    "dry_run_store_entries",
    "dry_run_store_verified=true",
    "execution_attempt_store_entries",
    "execution_attempt_store_verified=true",
    "execution_lifecycle_store_entries",
    "execution_lifecycle_store_verified=true",
    "execution_history_view_contract passed",
    "attempt_ref",
    "target_ref",
    "correlation_id",
    "idempotency_key",
    "audit_refs",
    "observability_refs",
    "capability_policy_ref",
    "runtime_contract_ref",
    "execution_contract_ref",
    "runtime_executor_contract_ref",
    "runtime_preparation_ref",
    "execution_runner_contract_ref",
    "dry_run_contract_ref",
}
ALLOWED_OUTPUTS = {
    "summary",
    "timeline",
    "preflight_status",
    "transition_history",
    "store_verification_summary",
    "boundary_summary",
    "risk_summary",
    "evidence",
    "warnings",
    "blockers",
}
PROHIBITED_OUTPUTS = {
    "execution_result",
    "execution_output",
    "execution_history_payload",
    "execution_result_history",
    "agent_output",
    "team_output",
    "model_response",
    "tool_result",
    "memory_payload",
    "external_response",
    "secret_value",
    "credential_value",
    "actual_output",
    "real_output",
    "live_response",
    "side_effect_result",
    "mutation_result",
}
BOUNDARY_FLAGS = {
    "execution_enabled=false",
    "agent_execution_enabled=false",
    "team_execution_enabled=false",
    "model_invocation_enabled=false",
    "tool_execution_enabled=false",
    "memory_persistence_enabled=false",
    "external_access_enabled=false",
    "scheduler_enabled=false",
    "worker_queue_enabled=false",
    "history_store_enabled=false",
    "execution_history_store_enabled=false",
    "attempt_history_store_enabled=false",
    "execution_result_store_enabled=false",
    "result_persistence_enabled=false",
    "jsonl_history_enabled=false",
    "execution_attempt_id_enabled=false",
}
FORBIDDEN_RUNTIME_JSONL = {
    "runtime/dry_runs/dry_run_store.jsonl",
    "runtime/execution_attempts/execution_attempt_store.jsonl",
    "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
    "runtime/execution_history/execution_history_store.jsonl",
    "runtime/execution_history/history.jsonl",
    "runtime/execution_results/execution_result_store.jsonl",
    "storage/execution_history_store.jsonl",
    "data/execution_history_store.jsonl",
    "logs/execution_history_store.jsonl",
}


def _audit_text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_execution_history_view_file_exists_only_as_allowed_derived_view_implementation():
    assert (ROOT / FUTURE_ALLOWED_FILE).exists()


def test_forbidden_history_attempt_result_id_and_queue_modules_do_not_exist():
    for relative in FORBIDDEN_FILES:
        assert not (ROOT / relative).exists(), relative


def test_future_allowed_file_policy_allows_only_history_view_implementation():
    text = _audit_text()
    assert FUTURE_ALLOWED_FILE in text
    for relative in FORBIDDEN_FILES:
        assert relative in text
    assert "`core/execution_history_view.py` creado como vista in-memory" in text


def test_no_store_or_jsonl_policy_is_explicit():
    text = _audit_text()
    for phrase in [
        "sin store propio",
        "sin JSONL propio",
        "sin history path",
        "sin result path",
        "sin append",
        "sin persistencia",
        "sin escritura runtime",
        "no crear parent dirs",
        "no crear archivos",
        "no escribir JSONL",
        "no overwrite",
        "no update",
        "no delete",
        "no truncate",
        "no replace",
    ]:
        assert phrase in text


def test_future_functions_allowed_and_blocked_are_documented():
    text = _audit_text()
    for name in FUTURE_ALLOWED_FUNCTIONS | BLOCKED_FUNCTIONS:
        assert f"`{name}`" in text


def test_required_inputs_allowed_outputs_and_prohibited_outputs_are_documented():
    text = _audit_text()
    for item in REQUIRED_INPUTS | ALLOWED_OUTPUTS | PROHIBITED_OUTPUTS:
        assert f"`{item}`" in text


def test_dependency_policy_requires_verified_stores_contracts_and_matching_refs():
    text = _audit_text()
    for phrase in [
        "stores primarios verified",
        "contract passed",
        "`dry_run_store verified`",
        "`execution_attempt_store verified`",
        "`execution_lifecycle_store verified`",
        "`execution_history_view_contract passed`",
        "`attempt_ref` coincide",
        "`target_ref` coincide",
        "`correlation_id` coincide",
        "`idempotency_key` coincide",
        "`audit_refs` presentes",
        "`observability_refs` presentes",
        "`capability_policy_ref` presente",
    ]:
        assert phrase in text


def test_attempt_ref_attempt_id_execution_scheduler_worker_and_history_boundaries_are_locked():
    text = _audit_text()
    for phrase in [
        "`attempt_ref` declarativo",
        "`attempt_ref` empieza con `preflight:`",
        "`attempt_ref_is_operational_id=false`",
        "`execution_attempt_id_enabled=false`",
        "`attempt_id_generation=disabled`",
        "`attempt_id_persistence=disabled`",
        "`materialized_attempt_id=false`",
        "`scheduler_enabled=false`",
        "`worker_queue_enabled=false`",
        "`history_store_enabled=false`",
        "`execution_history_store_enabled=false`",
        "`attempt_history_store_enabled=false`",
        "`execution_result_store_enabled=false`",
    ]:
        assert phrase in text
    for flag in BOUNDARY_FLAGS:
        assert f"`{flag}`" in text


def test_real_execution_agent_team_model_tool_memory_external_ui_mutation_are_blocked():
    text = _audit_text()
    for phrase in [
        "no execution attempt real",
        "no scheduler/worker queue",
        "no `queued/running/completed` reales",
        "no ejecucion real",
        "no agent/team execution",
        "no modelos/tools/memoria",
        "no external access",
        "no UI/integraciones",
        "no mutacion target",
        "no payloads reales prohibidos",
    ]:
        assert phrase in text


def test_no_history_result_or_runtime_jsonl_exists():
    for relative in FORBIDDEN_RUNTIME_JSONL:
        assert not (ROOT / relative).exists(), relative


def test_no_legacy_global_contamination_from_history_view_boundary():
    assert not (ROOT / "storage" / "execution_history_store.jsonl").exists()
    assert not (ROOT / "data" / "execution_history_store.jsonl").exists()
    assert not (ROOT / "logs" / "execution_history_store.jsonl").exists()
    for relative in UNCHANGED_CORE_FILES:
        assert (ROOT / relative).exists(), relative


def test_readiness_risks_next_prompt_and_book_entry_are_coherent():
    text = _audit_text()
    book = BOOK_DOC.read_text(encoding="utf-8")
    assert READINESS in text
    assert "PROMPT 2.45 - Implementar execution_history_view derived-only preflight-only sin store" in text
    assert "PROMPT 2.45.1 - Checkpoint E2E execution_history_view derived-only preflight-only" in text
    for risk in [
        "convertir view en store",
        "duplicar datos de stores primarios",
        "crear JSONL history por conveniencia",
        "guardar result payload camuflado como summary",
        "crear `execution_attempt_id` para indexar history",
        "interpretar `completed` como estado real",
        "leer/escribir runtime real en tests",
        "mezclar `audit_store` con `history_store`",
        "abrir puerta a UI antes de cerrar backend boundary",
    ]:
        assert risk in text
    assert "PROMPT 2.44 - Auditoria de frontera de implementacion derived history view sin store" in book
    assert READINESS in book


def test_audited_references_are_contract_docs_tests_or_blockers_not_operational_history_store():
    text = _audit_text()
    assert "`core/execution_history_view.py` creado como vista in-memory" in text
    assert "documentacion, tests, contratos, blockers, politicas `false` y riesgos futuros" in text
