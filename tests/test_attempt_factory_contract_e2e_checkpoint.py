from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ATTEMPT_FACTORY_CONTRACT_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_attempt_factory_contract_e2e_checkpoint_exists_and_passed():
    text = _text()

    assert DOC.exists()
    assert "ATTEMPT_FACTORY_CONTRACT_E2E_PASSED" in text
    assert "PROMPT 3.13 — Auditoría de attempt factory boundary" in text
    assert "PROMPT 3.14 — Contrato de attempt factory no-operativa" in text
    assert "PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract" in text


def test_checkpoint_contains_connected_states():
    text = _text()

    for phrase in [
        "ATTEMPT_FACTORY_BOUNDARY_AUDIT_COMPLETED",
        "ATTEMPT_FACTORY_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "ready_for_attempt_factory_contract",
        "ATTEMPT_FACTORY_CONTRACT_READY",
        "ready_for_attempt_factory_e2e_checkpoint",
    ]:
        assert phrase in text


def test_checkpoint_contains_full_chain():
    text = _text()

    for phrase in [
        "3.0 operational boundary audit",
        "3.1 execution intent contract",
        "3.2 execution_attempt_id audit",
        "3.3 execution attempt schema",
        "3.4 execution attempt state machine",
        "3.9 operational readiness gate audit",
        "3.10 operational readiness gate contract",
        "3.11 pre-operational E2E checkpoint",
        "3.12 next operational block plan",
        "3.13 attempt factory boundary audit",
        "3.14 attempt factory non-operational contract",
    ]:
        assert phrase in text


def test_checkpoint_confirms_non_operational_boundaries():
    text = _text()

    for phrase in [
        "contract-only",
        "non-operational",
        "in-memory only",
        "no active attempt factory",
        "no persisted attempts",
        "no runtime execution",
        "no store writes",
        "no lifecycle writes",
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
        "attempt_factory_enabled = true",
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
        "queued/running enabled",
    ]:
        assert forbidden not in text
