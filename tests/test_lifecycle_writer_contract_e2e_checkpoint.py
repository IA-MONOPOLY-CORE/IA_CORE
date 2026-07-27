from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LIFECYCLE_WRITER_CONTRACT_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_lifecycle_writer_contract_e2e_checkpoint_exists_and_passed():
    text = _text()
    assert DOC.exists()
    assert "LIFECYCLE_WRITER_CONTRACT_E2E_PASSED" in text
    assert "PROMPT 3.17 — Auditoría de lifecycle writer boundary" in text
    assert "PROMPT 3.18 — Contrato de lifecycle writer no-operativo" in text
    assert "PROMPT 3.18.1 — Checkpoint E2E de lifecycle writer" in text


def test_checkpoint_contains_connected_statuses():
    text = _text()
    for phrase in [
        "LIFECYCLE_WRITER_BOUNDARY_AUDIT_COMPLETED",
        "LIFECYCLE_WRITER_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "LIFECYCLE_WRITER_CONTRACT_READY",
        "ready_for_lifecycle_writer_contract",
        "ready_for_lifecycle_writer_e2e_checkpoint",
    ]:
        assert phrase in text


def test_checkpoint_confirms_non_operational_boundaries():
    text = _text()
    for phrase in [
        "contract-only",
        "lifecycle-simulated",
        "non-operational",
        "no real lifecycle writes",
        "no lifecycle events reales",
        "no lifecycle_store writes",
        "no attempt store writes",
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
        "lifecycle_writer_enabled = true",
        "lifecycle_writes_enabled = true",
        "lifecycle_events_enabled = true",
        "lifecycle_store_writes_enabled = true",
        "emitted = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
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
