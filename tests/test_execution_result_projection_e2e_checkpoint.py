from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EXECUTION_RESULT_PROJECTION_E2E_CHECKPOINT.md"
PROJECTION_MODULE = ROOT / "core" / "execution_result_projection.py"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_execution_result_projection_e2e_checkpoint_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "EXECUTION_RESULT_PROJECTION_E2E_PASSED" in text
    assert "EXECUTION_RESULT_PROJECTION_READY_FOR_OPERATIONAL_READINESS_GATE_AUDIT" in text
    assert "ready_for_operational_readiness_gate_audit" in text
    assert "PROMPT 3.9 — Auditoría de operational readiness gate" in text


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
    ]:
        assert readiness in text


def test_required_artifacts_exist():
    for relative in [
        "core/execution_result.py",
        "core/execution_result_projection.py",
        "docs/EXECUTION_RESULT_CONTRACT.md",
        "docs/EXECUTION_RESULT_PROJECTION_CONTRACT.md",
        "docs/LONG_TEST_SUITE_VALIDATION_POLICY.md",
    ]:
        assert (ROOT / relative).exists(), relative


def test_projection_module_boundaries_remain_false():
    text = PROJECTION_MODULE.read_text(encoding="utf-8")

    for constant in [
        "EXECUTION_RESULT_PROJECTION_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_HISTORY_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_READ_MODEL_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_RESULT_STORE_ENABLED",
        "EXECUTION_RESULT_PROJECTION_RUNTIME_ENABLED",
        "EXECUTION_RESULT_PROJECTION_EXECUTION_ENABLED",
        "EXECUTION_RESULT_PROJECTION_LIFECYCLE_WRITES_ENABLED",
    ]:
        assert f"{constant} = False" in text


def test_projection_module_exposes_no_write_sync_persist_functions():
    text = PROJECTION_MODULE.read_text(encoding="utf-8")

    for forbidden in [
        "def write_execution_result_to_history",
        "def write_execution_result_to_read_model",
        "def persist_execution_result_projection",
        "def save_execution_result_projection",
        "def apply_execution_result_projection",
        "def sync_execution_result_to_history",
        "def sync_execution_result_to_read_model",
    ]:
        assert forbidden not in text


def test_checkpoint_mentions_excluded_fields_and_read_only_runtime_flags():
    text = _text()

    for phrase in [
        "raw outputs",
        "output_ref",
        "error_ref",
        "metadata completa",
        "payloads grandes",
        "refs sensibles",
        "is_runtime_backed permanece False",
        "read_only permanece True",
    ]:
        assert phrase in text


def test_checkpoint_preserves_market_catalog_and_bcl_boundaries():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog permanece planned_not_active" in text
    assert "Business Composition Layer permanece futura/no operativa" in text


def test_checkpoint_confirms_no_real_integration_or_runtime():
    text = _text()

    for boundary in [
        "no integracion real result/history/read model",
        "no projection writes",
        "no history writes",
        "no read model writes",
        "no result store operativo",
        "no ExecutionResult persistence",
        "no result_id generator operativo",
        "no runtime execution",
        "no store writes",
        "no lifecycle writes",
        "no scheduler",
        "no worker",
        "no queue",
        "no model invocation",
        "no tool execution",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
    ]:
        assert boundary in text


def test_checkpoint_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "projection_writes_enabled = true",
        "history_writes_enabled = true",
        "read_model_writes_enabled = true",
        "result_store_enabled = true",
        "runtime_enabled = true",
        "store_writes_enabled = true",
        "lifecycle_writes_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text
