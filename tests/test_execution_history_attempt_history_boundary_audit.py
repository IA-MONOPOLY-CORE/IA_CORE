from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "EXECUTION_HISTORY_ATTEMPT_HISTORY_BOUNDARY_AUDIT.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"

READINESS = "HISTORY_READY_FOR_DERIVED_VIEW_CONTRACT_ONLY"
NEXT_PROMPT = "PROMPT 2.43 - Disenar execution_history_view_contract derived-only preflight-only sin store"
FORBIDDEN_FILES = {
    "core/execution_history_store.py",
    "core/execution_attempt_history.py",
    "core/attempt_history.py",
    "core/execution_result_store.py",
    "core/execution_attempt_id.py",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
}
RUNTIME_JSONL = {
    "runtime/execution_lifecycle/execution_lifecycle_store.jsonl",
    "runtime/execution_attempts/execution_attempt_store.jsonl",
    "runtime/dry_runs/dry_run_store.jsonl",
    "runtime/execution_history/execution_history_store.jsonl",
    "storage/execution_history_store.jsonl",
    "data/execution_history_store.jsonl",
    "logs/execution_history_store.jsonl",
}
PRIMARY_STORES = {
    "core/dry_run_store.py",
    "core/execution_attempt_store.py",
    "core/execution_lifecycle.py",
}
DERIVED_INPUTS = {
    "`dry_run_store verified`",
    "`execution_attempt_store verified`",
    "`execution_lifecycle_store verified`",
    "`audit_store refs`",
    "`observability refs`",
    "`correlation_id`",
    "`attempt_ref declarativo`",
    "`target_ref`",
}
BOUNDARY_FLAGS = {
    "`execution_enabled=false`",
    "`agent_execution_enabled=false`",
    "`team_execution_enabled=false`",
    "`model_invocation_enabled=false`",
    "`tool_execution_enabled=false`",
    "`memory_persistence_enabled=false`",
    "`external_access_enabled=false`",
    "`scheduler_enabled=false`",
    "`worker_queue_enabled=false`",
    "`result_persistence_enabled=false`",
    "`execution_history_store_enabled=false`",
    "`execution_attempt_id_enabled=false`",
}
PROHIBITED_OUTPUTS = {
    "`execution_result`",
    "`execution_output`",
    "`agent_output`",
    "`team_output`",
    "`model_response`",
    "`tool_result`",
    "`memory_payload`",
    "`external_response`",
    "`secret_value`",
    "`credential_value`",
    "`actual_output`",
    "`real_output`",
}


def _audit_text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_forbidden_history_attempt_result_and_id_modules_do_not_exist():
    for relative in FORBIDDEN_FILES:
        assert not (ROOT / relative).exists(), relative


def test_primary_stores_exist_and_history_store_does_not():
    for relative in PRIMARY_STORES:
        assert (ROOT / relative).exists(), relative
    assert not (ROOT / "core" / "execution_history_store.py").exists()


def test_audit_recommends_derived_view_contract_before_new_store():
    text = _audit_text()
    assert READINESS in text
    assert "Opcion C primero: `history_view derived-only contract`" in text
    assert "sin store propio" in text
    assert "sin JSONL propio" in text
    assert "no store nuevo" in text
    assert NEXT_PROMPT in text


def test_glossary_and_concept_table_cover_required_history_terms():
    text = _audit_text()
    for term in [
        "`dry_run_store`",
        "`execution_attempt_store preflight-only`",
        "`execution_lifecycle_store`",
        "`attempt_history`",
        "`execution_history`",
        "`execution_result_history`",
        "`execution_result_store`",
        "`execution_attempt_id operativo`",
    ]:
        assert term in text
    for header in ["Concepto", "Que guarda", "Fuente", "Es derivado o primario", "Puede existir ahora", "Riesgo", "Estado actual"]:
        assert header in text


def test_history_view_depends_on_verified_stores_refs_and_declarative_attempt_ref():
    text = _audit_text()
    for phrase in DERIVED_INPUTS:
        assert phrase in text
    for phrase in [
        "`execution_lifecycle_contract passed`",
        "`execution_attempt_store_contract passed`",
        "`dry_run_store_contract passed`",
        "runtime/execution contracts passed",
    ]:
        assert phrase in text


def test_history_view_blocks_execution_attempt_id_attempt_real_and_result_history():
    text = _audit_text()
    for phrase in [
        "no debe crear `execution_attempt_id` operativo",
        "no debe crear execution attempt real",
        "no debe crear execution result history",
        "sin `execution_attempt_id` operativo",
        "sin ejecucion real",
    ]:
        assert phrase in text


def test_boundary_policy_and_payload_outputs_remain_blocked():
    text = _audit_text()
    for phrase in BOUNDARY_FLAGS | PROHIBITED_OUTPUTS:
        assert phrase in text
    for phrase in ["`queued/running/completed` reales", "scheduler/worker queue", "modelos/tools/memoria", "external access"]:
        assert phrase in text


def test_no_history_or_runtime_jsonl_exists():
    for relative in RUNTIME_JSONL:
        assert not (ROOT / relative).exists(), relative


def test_no_core_lifecycle_attempt_store_or_runner_changes_required_by_boundary():
    text = _audit_text()
    assert "No se detecta implementacion operativa" in text
    assert "No significa readiness para `execution_history_store`" in text
    assert (ROOT / "core" / "execution_lifecycle.py").exists()
    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert (ROOT / "core" / "execution_runner.py").exists()


def test_risks_are_documented_and_book_is_updated():
    text = _audit_text()
    book = BOOK_DOC.read_text(encoding="utf-8")
    for phrase in [
        "duplicar stores primarios",
        "crear `history_store` demasiado pronto",
        "crear `result_store` camuflado",
        "introducir `execution_attempt_id` operativo",
        "confundir lifecycle history con execution result",
        "guardar payloads reales por accidente",
    ]:
        assert phrase in text
    assert "PROMPT 2.42 - Auditoria de frontera execution history / attempt history contract" in book
    assert READINESS in book
