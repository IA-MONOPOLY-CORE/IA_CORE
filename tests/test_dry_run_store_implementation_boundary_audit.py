from pathlib import Path

from core.dry_run_store_contract import (
    FORBIDDEN_ENTRY_FIELDS,
    build_append_only_contract,
    build_checksum_contract,
    build_payload_boundary_contract,
)
from core.dry_run_store_schema import BLOCKED_STORAGE_FORMATS


ROOT = Path(__file__).parent.parent
AUDIT_DOC = ROOT / "docs" / "DRY_RUN_STORE_IMPLEMENTATION_BOUNDARY_AUDIT.md"


def _doc() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_no_execution_attempt_store_or_runtime_storage_exists_after_dry_run_store_implementation():
    assert (ROOT / "core" / "dry_run_store.py").exists()
    assert (ROOT / "core" / "execution_attempt_store.py").exists()
    assert not (ROOT / "core" / "execution_attempt_id.py").exists()
    assert not (ROOT / "core" / "execution_attempt_lifecycle.py").exists()
    assert not (ROOT / "runtime" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert not (ROOT / "data" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert not (ROOT / ".audit" / "dry_run_store.jsonl").exists()
    assert not (ROOT / "var" / "dry_runs" / "dry_run_store.jsonl").exists()
    assert not list(ROOT.rglob("dry_run_store*.jsonl"))
    assert not list(ROOT.rglob("execution_attempt_store*.jsonl"))


def test_boundary_audit_declares_contract_e2e_is_not_store_implementation():
    text = _doc()
    assert "PASSED_DRY_RUN_STORE_CONTRACT_E2E" not in text or "no crea" in text
    assert "DRY_RUN_STORE_READY_FOR_APPEND_ONLY_IMPLEMENTATION" in text
    assert "EXECUTION_ATTEMPT_STORE_NOT_READY" in text
    assert "core/dry_run_store.py" in text
    assert "Ese archivo no se crea en este prompt" in text
    assert "runtime/dry_runs/dry_run_store.jsonl" in text


def test_future_store_requires_passed_contract_result_only_append_only_jsonl_checksum_and_ids():
    text = _doc()
    for expected in [
        "dry_run_store_contract_not_passed",
        "missing_dry_run_store_contract",
        "missing_dry_run_result",
        "dry_run_result_not_result_only",
        "append-only",
        "JSONL",
        "sha256",
        "missing_idempotency_key",
        "missing_correlation_id",
        "append_only_jsonl",
    ]:
        assert expected in text
    assert BLOCKED_STORAGE_FORMATS == {
        "append_only_json",
        "database_future",
        "in_memory_only",
        "audit_store_only",
        "execution_attempt_store_future",
    }


def test_future_store_append_only_policy_blocks_overwrite_update_delete_replace_truncate():
    append_contract = build_append_only_contract()
    text = _doc()
    assert append_contract["append_only"] is True
    assert append_contract["overwrite_allowed"] is False
    assert append_contract["update_existing_allowed"] is False
    assert append_contract["delete_allowed"] is False
    assert append_contract["replace_allowed"] is False
    for blocked in ["overwrite", "update", "delete", "truncate", "replace", "compact without policy"]:
        assert blocked in text


def test_future_store_checksum_policy_is_canonical_tamper_evident_and_chained():
    checksum_contract = build_checksum_contract()
    text = _doc()
    assert checksum_contract["checksum_required"] is True
    assert checksum_contract["checksum_algorithm"] == "sha256"
    assert checksum_contract["entry_hash_required"] is True
    assert checksum_contract["tamper_detection_required"] is True
    for expected in [
        "orden estable de claves",
        "UTF-8",
        "sin entry_checksum",
        "previous_entry_checksum",
        "checksum mismatch",
        "lineas corruptas",
        "payload prohibido",
    ]:
        assert expected in text


def test_future_store_idempotency_scope_and_conflict_policy_are_declared():
    text = _doc()
    for expected in [
        "target_type",
        "target_id",
        "correlation_id",
        "idempotency_key",
        "dry_run_id",
        "dry_run_contract_ref",
        "noop_idempotent",
        "blocked_conflict",
        "scope faltante",
    ]:
        assert expected in text


def test_future_store_blocks_attempt_execution_payloads_external_ui_scheduler_worker_and_mutation():
    payload_boundary = build_payload_boundary_contract()
    text = _doc()
    assert "execution_attempt_id" in FORBIDDEN_ENTRY_FIELDS
    assert payload_boundary["execution_attempt_allowed"] is False
    assert payload_boundary["model_response_allowed"] is False
    assert payload_boundary["tool_result_allowed"] is False
    assert payload_boundary["memory_write_allowed"] is False
    for expected in [
        "execution_attempt_id_not_allowed",
        "execution_payload_not_allowed",
        "agent_output_not_allowed",
        "team_output_not_allowed",
        "model_response_not_allowed",
        "tool_result_not_allowed",
        "memory_payload_not_allowed",
        "external_response_not_allowed",
        "scheduler_job_not_allowed",
        "worker_task_not_allowed",
        "mutation_not_allowed",
        "execution_attempt_store_not_allowed",
        "UI",
        "integraciones",
        "scheduler",
        "worker queue",
        "lifecycle",
    ]:
        assert expected in text


def test_future_store_relationships_with_audit_store_and_execution_attempt_store_are_separate():
    text = _doc()
    assert "no reemplaza `audit_store`" in text
    assert "Ambos deben compartir `correlation_id`" in text
    assert "no crea `execution_attempt_id`" in text
    assert "no tiene lifecycle de ejecucion" in text
    assert "execution_attempt_store` requiere auditoria y contrato posterior" in text
