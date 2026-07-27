from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_attempt_store_write_safe_contract_e2e_checkpoint_exists_and_passed():
    text = _text()
    assert DOC.exists()
    assert "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_E2E_PASSED" in text
    assert "PROMPT 3.15 — Auditoría de attempt store write-safe boundary" in text
    assert "PROMPT 3.16 — Contrato de attempt store write-safe" in text
    assert "PROMPT 3.16.1 — Checkpoint E2E de attempt store write-safe" in text


def test_checkpoint_contains_connected_statuses():
    text = _text()
    for phrase in [
        "ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_AUDIT_COMPLETED",
        "ATTEMPT_STORE_WRITE_SAFE_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "ATTEMPT_STORE_WRITE_SAFE_CONTRACT_READY",
        "ready_for_attempt_store_write_safe_contract",
        "ready_for_attempt_store_write_safe_e2e_checkpoint",
    ]:
        assert phrase in text


def test_checkpoint_confirms_non_operational_boundaries():
    text = _text()
    for phrase in [
        "contract-only",
        "write-safe simulated",
        "non-operational",
        "no real persistence",
        "no attempt store writes",
        "no lifecycle writes",
        "no lifecycle events",
        "no result store writes",
        "no history writes",
        "no read model writes",
        "no runtime execution",
        "no scheduler",
        "no worker",
        "no queue",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text


def test_checkpoint_has_no_contradictory_enabled_states():
    text = _text()
    for forbidden in [
        "attempt_store_enabled = true",
        "attempt_store_writes_enabled = true",
        "attempt_persistence_enabled = true",
        "persisted = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
        "lifecycle_writes_enabled = true",
        "result_store_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert forbidden not in text
