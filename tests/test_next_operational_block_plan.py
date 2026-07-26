from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_next_operational_block_plan_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "NEXT_OPERATIONAL_BLOCK_PLAN_READY" in text
    assert "PHASE_3_READY_FOR_NEXT_OPERATIONAL_BLOCK" in text
    assert "ready_for_next_operational_block_first_audit" in text
    assert "PROMPT 3.13 — Auditoría de attempt factory boundary" in text


def test_plan_contains_completed_chain():
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
        "Operational readiness gate contract",
        "Pre-operational E2E checkpoint",
    ]:
        assert phrase in text


def test_plan_contains_simple_summary():
    assert "El sistema todavia no ejecuta nada real" in _text()


def test_plan_contains_required_inventory():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "ExecutionAttempt",
        "ExecutionResult",
        "ExecutionResult projection",
        "Operational readiness gate",
        "Long suite validation policy",
        "Market Catalog",
        "Business Composition Layer",
    ]:
        assert phrase in text


def test_plan_contains_open_gaps():
    text = _text()

    for phrase in [
        "No existe attempt factory operativa",
        "No existe result store operativo",
        "No existe lifecycle writer operativo",
        "No existe scheduler",
        "No existe worker",
        "No existe queue",
        "No existe runtime runner",
        "No existe permission model operativo",
        "No existe rollback operativo",
        "No existe apertura controlada del gate",
    ]:
        assert phrase in text


def test_plan_contains_options_and_recommendation():
    text = _text()

    for phrase in [
        "Attempt factory boundary",
        "Result store write-safe boundary",
        "Lifecycle writer boundary",
        "Scheduler/worker/queue boundary",
    ]:
        assert phrase in text

    assert "La recomendacion es avanzar con:" in text
    assert "Attempt factory boundary" in text


def test_plan_contains_next_sequence():
    text = _text()

    for prompt in [
        "PROMPT 3.13 — Auditoría de attempt factory boundary",
        "PROMPT 3.14 — Contrato de attempt factory no-operativa",
        "PROMPT 3.14.1 — Checkpoint E2E de attempt factory contract",
        "PROMPT 3.15 — Auditoría de attempt store write-safe boundary",
        "PROMPT 3.16 — Contrato de attempt store write-safe",
        "PROMPT 3.17 — Auditoría de lifecycle writer boundary",
        "PROMPT 3.18 — Contrato de lifecycle writer no-operativo",
        "PROMPT 3.19 — Checkpoint E2E operational-block foundation",
    ]:
        assert prompt in text


def test_plan_contains_next_prompt_expected_state():
    text = _text()

    for phrase in [
        "ATTEMPT_FACTORY_BOUNDARY_AUDIT_COMPLETED",
        "ATTEMPT_FACTORY_BOUNDARY_READY_FOR_CONTRACT_DESIGN",
        "ready_for_attempt_factory_contract",
    ]:
        assert phrase in text


def test_plan_declares_blocked_capabilities():
    text = _text()

    for phrase in [
        "runtime execution sigue bloqueado",
        "attempt factory activa sigue bloqueada",
        "attempt store writes siguen bloqueados",
        "lifecycle writes siguen bloqueados",
        "result store operativo sigue bloqueado",
        "history writes siguen bloqueados",
        "read model writes siguen bloqueados",
        "scheduler sigue bloqueado",
        "worker sigue bloqueado",
        "queue sigue bloqueada",
        "model invocation sigue bloqueado",
        "tool execution sigue bloqueado",
        "external access sigue bloqueado",
    ]:
        assert phrase in text


def test_market_catalog_and_business_composition_remain_inactive():
    text = _text()
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")

    assert "planned_not_active" in catalog_text
    assert "Market Catalog permanece planned_not_active" in text
    assert "Business Composition Layer permanece futura/no operativa" in text
    assert "No participa en attempt factory" in text
    assert "No activa Business Composition Layer" in text
    assert "No activa runtime" in text


def test_no_operational_modules_were_created():
    for relative in [
        "core/attempt_factory.py",
        "core/runtime_runner.py",
        "core/result_store_writer.py",
        "core/lifecycle_writer.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_plan_has_no_contradictory_states():
    text = _text()

    for forbidden in [
        "runtime_enabled = true",
        "attempt_factory_enabled = true",
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
