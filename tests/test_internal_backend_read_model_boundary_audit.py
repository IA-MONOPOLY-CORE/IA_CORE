from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "INTERNAL_BACKEND_READ_MODEL_BOUNDARY_AUDIT.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"

READINESS = "READ_MODEL_READY_FOR_CONTRACT_ONLY"
FUTURE_ALLOWED_FILES = {
    "core/internal_backend_read_model_schema.py",
    "core/internal_backend_read_model_contract.py",
    "tests/test_internal_backend_read_model_contract.py",
    "tests/test_internal_backend_read_model_contract_end_to_end.py",
    "docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT.md",
}
POSTPONED_FILES = {
    "core/backend_read_model_store.py",
    "core/backend_status_api.py",
    "core/backend_dashboard_adapter.py",
}
AUDITED_CORE_UNCHANGED = {
    "core/execution_history_view.py",
    "core/execution_lifecycle.py",
    "core/execution_attempt_store.py",
    "core/dry_run_store.py",
    "core/execution_runner.py",
}
FUTURE_SOURCES = {
    "domain state",
    "artifact state",
    "sandbox materialization preview",
    "sandbox materialization result",
    "promotion gate result",
    "promotion executor result",
    "active contract result",
    "active executor result",
    "runtime contract result",
    "execution contract result",
    "runtime executor contract result",
    "runtime preparation result",
    "execution runner contract result",
    "dry-run contract result",
    "dry-run result-only",
    "dry_run_store verified entries",
    "execution_attempt_store verified entries",
    "execution_lifecycle verified entries",
    "execution_history_view derived view",
    "audit refs",
    "observability refs",
    "capability policy refs",
}
FIELDS = {
    "snapshot_id",
    "schema_version",
    "read_model_mode",
    "generated_at",
    "target_type",
    "target_id",
    "target_ref",
    "domain_ref",
    "sandbox_summary",
    "promotion_summary",
    "active_summary",
    "runtime_contract_summary",
    "execution_contract_summary",
    "runtime_preparation_summary",
    "execution_runner_summary",
    "dry_run_summary",
    "dry_run_store_summary",
    "execution_attempt_store_summary",
    "execution_lifecycle_summary",
    "execution_history_summary",
    "audit_summary",
    "observability_summary",
    "capability_policy_summary",
    "readiness_summary",
    "blockers",
    "warnings",
    "evidence",
}
PERMITTED_OUTPUTS = {
    "summaries",
    "derived_status",
    "readiness",
    "blockers",
    "warnings",
    "evidence",
    "refs",
    "counts",
    "timestamps",
    "contract verdicts",
    "boundary summaries",
}
FORBIDDEN_OUTPUTS = {
    "raw execution payloads",
    "model responses",
    "tool results",
    "memory payloads",
    "credentials",
    "secrets",
    "external responses",
    "mutation results",
    "live execution outputs",
    "large raw JSONL bodies",
    "unredacted artifacts",
}
RISKS = {
    "convertir read model en API prematura",
    "mezclar read-only con mutacion",
    "duplicar stores",
    "exponer payloads reales",
    "crear snapshots persistidos antes de tiempo",
    "leer archivos sueltos sin contrato",
    "hacer que UI dependa de estructuras internas inestables",
    "mezclar readiness con ejecucion real",
    "abrir endpoints antes de cerrar contrato",
}


def _audit_text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_audit_document_exists_and_readiness_is_contract_only():
    text = _audit_text()

    assert AUDIT_DOC.exists()
    assert READINESS in text
    assert "READ_MODEL_READY_FOR_IMPLEMENTATION" in text
    assert "contrato de read model interno" in text


def test_future_sources_allowed_are_documented():
    text = _audit_text()

    for source in FUTURE_SOURCES:
        assert source in text


def test_future_allowed_contract_files_are_documented_and_contract_layer_created():
    text = _audit_text()

    for relative in FUTURE_ALLOWED_FILES:
        assert relative in text
    for relative in [
        "core/internal_backend_read_model_schema.py",
        "core/internal_backend_read_model_contract.py",
        "tests/test_internal_backend_read_model_contract.py",
        "tests/test_internal_backend_read_model_contract_end_to_end.py",
        "docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT.md",
    ]:
        assert (ROOT / relative).exists(), relative


def test_read_only_implementation_is_created_but_store_api_and_dashboard_are_not_created():
    text = _audit_text()

    assert "core/internal_backend_read_model.py" in text
    assert (ROOT / "core/internal_backend_read_model.py").exists()
    for relative in POSTPONED_FILES:
        assert relative in text
        assert not (ROOT / relative).exists(), relative


def test_candidate_fields_outputs_and_non_read_model_outputs_are_documented():
    text = _audit_text()

    for item in FIELDS | PERMITTED_OUTPUTS | FORBIDDEN_OUTPUTS:
        assert item in text


def test_risks_and_next_prompt_are_documented():
    text = _audit_text()
    book = BOOK_DOC.read_text(encoding="utf-8")

    for risk in RISKS:
        assert risk in text
    assert "PROMPT 2.47 - Disenar internal_backend_read_model_contract read-only" in text
    assert "PROMPT 2.46 - Auditoria de frontera de read model interno" in book
    assert READINESS in book


def test_no_core_execution_or_history_modules_are_modified_by_audit_scope():
    for relative in AUDITED_CORE_UNCHANGED:
        assert (ROOT / relative).exists(), relative
    assert (ROOT / "core" / "internal_backend_read_model.py").exists()
    assert (ROOT / "core" / "internal_backend_read_model_contract.py").exists()


def test_no_new_store_api_ui_execution_scheduler_or_external_scope_is_created():
    text = _audit_text()
    for phrase in [
        "no store nuevo",
        "no API nueva",
        "no UI",
        "no ejecucion real",
        "no scheduler/worker",
        "no modelos/tools/memoria",
        "no external access",
        "no mutacion",
        "no payloads reales",
        "no snapshots persistidos",
    ]:
        assert phrase in text
    for relative in [
        "core/backend_read_model_store.py",
        "core/backend_status_api.py",
        "core/backend_dashboard_adapter.py",
        "ui/internal_backend_read_model",
        "runtime/internal_backend_read_model",
    ]:
        assert not (ROOT / relative).exists(), relative
