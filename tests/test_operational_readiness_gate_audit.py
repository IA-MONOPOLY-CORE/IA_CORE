from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "OPERATIONAL_READINESS_GATE_AUDIT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_operational_readiness_gate_audit_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "OPERATIONAL_READINESS_GATE_AUDIT_COMPLETED" in text
    assert "OPERATIONAL_READINESS_GATE_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_operational_readiness_gate_contract" in text
    assert "PROMPT 3.10 — Contrato de operational readiness gate" in text


def test_audit_contains_required_chain():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "execution_attempt_id",
        "ExecutionAttempt schema",
        "ExecutionAttempt state machine",
        "Result Store boundary",
        "ExecutionResult contract",
        "Result/history/read model integration audit",
        "ExecutionResult projection contract",
        "Operational readiness gate audit",
    ]:
        assert phrase in text


def test_audit_contains_inventory_and_classifications():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "ExecutionAttempt",
        "ExecutionResult",
        "ExecutionResult projection",
        "Long suite validation policy",
        "Market Catalog",
        "Business Composition Layer",
        "audit_only",
        "contract_only",
        "schema_only",
        "read_only_contract",
        "read_only_projection",
        "e2e_checkpoint",
        "planned_not_active",
        "future_non_operational",
    ]:
        assert phrase in text


def test_audit_answers_required_questions():
    text = _text()

    for phrase in [
        "Que significa operational-ready",
        "Que NO significa operational-ready",
        "Contratos operativos vs ejecucion real",
        "Condiciones minimas del readiness gate",
        "runtime",
        "store writes",
        "lifecycle writes",
        "result store writes",
        "history/read model writes",
        "preflight_ready",
        "queued",
        "projection writes",
    ]:
        assert phrase in text


def test_audit_contains_candidate_gate_conditions():
    text = _text()

    for field in [
        "intent_contract_ready",
        "attempt_id_audit_ready",
        "attempt_schema_ready",
        "attempt_state_machine_ready",
        "result_boundary_audit_ready",
        "execution_result_contract_ready",
        "result_projection_contract_ready",
        "history_read_model_integration_audit_ready",
        "long_suite_policy_ready",
        "runtime_enabled",
        "store_writes_enabled",
        "lifecycle_writes_enabled",
        "result_store_enabled",
        "history_writes_enabled",
        "read_model_writes_enabled",
        "market_catalog_active",
        "business_composition_active",
    ]:
        assert field in text


def test_audit_contains_required_risks():
    text = _text()

    for risk in [
        "activar runtime sin gate",
        "queued/running sin scheduler controlado",
        "store writes sin rollback",
        "lifecycle writes sin sincronizacion",
        "result store writes sin politica",
        "history/read model writes sin projection auditada",
        "dry-run con resultado real",
        "read-only projection con integracion real",
        "Market Catalog como negocio activo",
        "Business Composition Layer sin contrato",
        "modelos/tools sin permisos",
        "external access sin politica",
        "estados inconsistentes",
        "resultados sin lineage",
    ]:
        assert risk in text


def test_audit_contains_required_boundaries():
    text = _text()

    for boundary in [
        "no operational readiness gate real",
        "no runtime execution",
        "no attempt factory",
        "no attempt store writes",
        "no lifecycle writes",
        "no result store operativo",
        "no ExecutionResult persistence",
        "no result_id generator operativo",
        "no history writes",
        "no read model writes",
        "no projection writes",
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


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog permanece planned_not_active" in text
    assert "Business Composition Layer permanece futura/no operativa" in text


def test_no_operational_gate_modules_were_created():
    for relative in [
        "core/operational_readiness_gate.py",
        "core/runtime_runner.py",
        "core/attempt_factory.py",
        "core/result_store_writer.py",
        "core/history_writer.py",
        "core/read_model_writer.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_enabled_states():
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
        '"market_catalog_active": true',
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text
