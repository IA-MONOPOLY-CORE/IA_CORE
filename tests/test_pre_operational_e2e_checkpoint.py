from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PRE_OPERATIONAL_E2E_CHECKPOINT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_pre_operational_e2e_checkpoint_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "PRE_OPERATIONAL_E2E_CHECKPOINT_PASSED" in text
    assert "PHASE_3_PRE_OPERATIONAL_CHAIN_READY" in text
    assert "ready_for_next_phase_planning" in text
    assert "PROMPT 3.12 — Planificación del próximo bloque operacional" in text


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
        "OPERATIONAL_READINESS_GATE_CONTRACT_E2E_PASSED",
        "PRE_OPERATIONAL_E2E_CHECKPOINT_PASSED",
        "PHASE_3_PRE_OPERATIONAL_CHAIN_READY",
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
        "ready_for_next_phase_planning",
    ]:
        assert readiness in text


def test_required_artifacts_exist():
    for relative in [
        "core/execution_intent.py",
        "core/execution_attempt.py",
        "core/execution_attempt_state_machine.py",
        "core/execution_result.py",
        "core/execution_result_projection.py",
        "core/operational_readiness_gate.py",
        "docs/LONG_TEST_SUITE_VALIDATION_POLICY.md",
    ]:
        assert (ROOT / relative).exists(), relative


def test_checkpoint_confirms_gate_contract_closed():
    text = _text()

    assert "Operational readiness gate existe como contrato, pero está cerrado." in text


def test_checkpoint_contains_module_inventory():
    text = _text()

    for module in [
        "execution_intent",
        "execution_attempt",
        "execution_attempt_state_machine",
        "execution_result",
        "execution_result_projection",
        "operational_readiness_gate",
        "execution_history_view",
        "internal_backend_read_model",
        "market_catalog",
    ]:
        assert module in text


def test_checkpoint_declares_disabled_capabilities():
    text = _text()

    for capability in [
        "runtime execution = disabled",
        "attempt factory = disabled",
        "attempt store writes = disabled",
        "lifecycle writes = disabled",
        "result store operativo = disabled",
        "result store writes = disabled",
        "ExecutionResult persistence = disabled",
        "result_id generator operativo = disabled",
        "history writes = disabled",
        "read model writes = disabled",
        "projection writes = disabled",
        "scheduler = disabled",
        "worker = disabled",
        "queue = disabled",
        "model invocation = disabled",
        "tool execution = disabled",
        "memory persistence = disabled",
        "external access = disabled",
        "API = disabled",
        "UI = disabled",
        "Market Catalog runtime = disabled",
        "Business Composition Layer runtime = disabled",
    ]:
        assert capability in text


def test_checkpoint_declares_ready_and_not_ready_boundaries():
    text = _text()

    for phrase in [
        "listo para planificación del próximo bloque operacional",
        "listo para diseñar próximos contratos",
        "listo para definir qué faltaría antes de runtime real",
        "listo para decidir si Fase 3 continúa o se cierra como pre-operational base",
        "no listo para runtime real",
        "no listo para ejecutar attempts",
        "no listo para abrir gate operacional",
    ]:
        assert phrase in text


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog sigue `planned_not_active`" in text
    assert "Business Composition Layer sigue futura/no operativa" in text


def test_no_operational_modules_were_created():
    for relative in [
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/history_writer.py",
        "core/read_model_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_attempt_factory_when_present_is_non_operational_contract():
    module_path = ROOT / "core" / "attempt_factory.py"
    if not module_path.exists():
        return

    text = module_path.read_text(encoding="utf-8")
    for required in [
        'ATTEMPT_FACTORY_CONTRACT_STATUS = "contract_only"',
        "ATTEMPT_FACTORY_ENABLED = False",
        "ATTEMPT_FACTORY_RUNTIME_ENABLED = False",
        "ATTEMPT_FACTORY_STORE_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_LIFECYCLE_WRITES_ENABLED = False",
        "ATTEMPT_FACTORY_RESULT_STORE_ENABLED = False",
        "ATTEMPT_FACTORY_SCHEDULER_ENABLED = False",
        "ATTEMPT_FACTORY_WORKER_ENABLED = False",
        "ATTEMPT_FACTORY_QUEUE_ENABLED = False",
    ]:
        assert required in text


def test_checkpoint_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
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
