from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "OPERATIONAL_READINESS_GATE_CONTRACT_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_operational_readiness_gate_contract_e2e_checkpoint_exists():
    text = _text()

    assert DOC.exists()
    assert "OPERATIONAL_READINESS_GATE_CONTRACT_E2E_PASSED" in text
    assert "PROMPT 3.11 — Checkpoint E2E pre-operational" in text


def test_checkpoint_contains_complete_prompt_chain():
    text = _text()

    for prompt in [
        "PROMPT 3.0 — Auditoría de frontera operacional",
        "PROMPT 3.1 — Contrato de execution intent operativo",
        "PROMPT 3.2 — Auditoría de execution_attempt_id operativo",
        "PROMPT 3.2.1 — Checkpoint E2E de execution_attempt_id operativo",
        "PROMPT 3.3 — Schema de execution attempt operativo",
        "PROMPT 3.4 — State machine operacional contract-only",
        "PROMPT 3.5 — Auditoría de result store boundary",
        "PROMPT 3.6 — Contrato de result store operativo read-only",
        "PROMPT 3.6.1 — Normalización de suite filtrada por bloques",
        "PROMPT 3.7 — Auditoría de integración result/history/read model",
        "PROMPT 3.8 — Contrato de integración result/history/read model read-only",
        "PROMPT 3.8.1 — Checkpoint E2E de projection result/history/read model",
        "PROMPT 3.9 — Auditoría de operational readiness gate",
        "PROMPT 3.10 — Contrato de operational readiness gate",
        "PROMPT 3.11 — Checkpoint E2E pre-operational",
    ]:
        assert prompt in text


def test_checkpoint_contains_required_verdicts():
    text = _text()

    for verdict in [
        "OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "EXECUTION_INTENT_CONTRACT_READY",
        "EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN",
        "EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_PASSED",
        "EXECUTION_ATTEMPT_SCHEMA_READY",
        "EXECUTION_ATTEMPT_SCHEMA_E2E_PASSED",
        "EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY",
        "EXECUTION_ATTEMPT_STATE_MACHINE_E2E_PASSED",
        "RESULT_STORE_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "RESULT_STORE_BOUNDARY_AUDIT_E2E_PASSED",
        "EXECUTION_RESULT_CONTRACT_READY",
        "EXECUTION_RESULT_CONTRACT_E2E_PASSED",
        "LONG_TEST_SUITE_VALIDATION_POLICY_READY",
        "RESULT_HISTORY_READ_MODEL_INTEGRATION_AUDIT_COMPLETED",
        "RESULT_HISTORY_READ_MODEL_INTEGRATION_AUDIT_E2E_PASSED",
        "RESULT_HISTORY_READ_MODEL_INTEGRATION_READY_FOR_CONTRACT_DESIGN",
        "EXECUTION_RESULT_PROJECTION_CONTRACT_READY",
        "EXECUTION_RESULT_PROJECTION_E2E_PASSED",
        "EXECUTION_RESULT_PROJECTION_READY_FOR_OPERATIONAL_READINESS_GATE_AUDIT",
        "OPERATIONAL_READINESS_GATE_AUDIT_COMPLETED",
        "OPERATIONAL_READINESS_GATE_AUDIT_E2E_PASSED",
        "OPERATIONAL_READINESS_GATE_READY_FOR_CONTRACT_DESIGN",
        "OPERATIONAL_READINESS_GATE_CONTRACT_READY",
    ]:
        assert verdict in text


def test_checkpoint_contains_required_readiness_chain():
    text = _text()

    for readiness in [
        "ready_for_execution_intent_contract",
        "ready_for_execution_attempt_id_audit",
        "ready_for_execution_attempt_schema",
        "ready_for_operational_state_machine_contract",
        "ready_for_result_store_boundary_audit",
        "ready_for_result_store_contract",
        "ready_for_result_history_read_model_integration_audit",
        "ready_for_result_history_read_model_contract",
        "ready_for_result_projection_e2e_checkpoint",
        "ready_for_operational_readiness_gate_audit",
        "ready_for_operational_readiness_gate_contract",
        "ready_for_pre_operational_e2e_checkpoint",
    ]:
        assert readiness in text


def test_checkpoint_preserves_market_catalog_and_bcl_boundaries():
    text = _text()

    assert "Market Catalog sigue `planned_not_active`" in text
    assert "Business Composition Layer sigue futura/no operativa" in text


def test_checkpoint_confirms_no_operational_activation():
    text = _text()

    for boundary in [
        "No se activo gate real",
        "runtime",
        "attempt factory",
        "store writes",
        "lifecycle writes",
        "result store",
        "history writes",
        "read model writes",
        "projection writes",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "memory persistence",
        "external access",
        "API",
        "UI",
    ]:
        assert boundary in text


def test_checkpoint_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "operational_readiness_gate_enabled = true",
        "runtime_enabled = true",
        "attempt_factory_enabled = true",
        "store_writes_enabled = true",
        "lifecycle_writes_enabled = true",
        "result_store_enabled = true",
        "history_writes_enabled = true",
        "read_model_writes_enabled = true",
        "projection_writes_enabled = true",
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
