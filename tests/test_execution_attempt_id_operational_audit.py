import json
from pathlib import Path

from core.execution_intent import (
    EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED,
    EXECUTION_INTENT_EXECUTION_ENABLED,
    EXECUTION_INTENT_RUNTIME_ENABLED,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "EXECUTION_ATTEMPT_ID_OPERATIONAL_AUDIT.md"
INTENT_DOC = ROOT / "docs" / "EXECUTION_INTENT_CONTRACT.md"
OPERATIONAL_AUDIT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_OPERATIONAL_BOUNDARY_AUDIT.md"
PLAN_DOC = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_execution_attempt_id_audit_document_exists_and_is_ready():
    text = _text()

    assert AUDIT_DOC.exists()
    assert "EXECUTION_ATTEMPT_ID_AUDIT_COMPLETED" in text
    assert "EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN" in text
    assert "ready_for_execution_attempt_schema" in text
    assert "PROMPT 3.3 — Schema de execution attempt operativo" in text


def test_audit_defines_intent_attempt_and_attempt_id():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "ExecutionAttempt",
        "execution_attempt_id",
        "intencion validada de querer ejecutar algo",
        "instancia operativa futura",
        "identificador unico, estable, trazable y no ambiguo",
    ]:
        assert phrase in text


def test_audit_explains_intent_to_attempt_relationship():
    text = _text()

    assert "Relacion intent -> attempt" in text
    assert "Un ExecutionIntent validado puede habilitar" in text
    assert "Un ExecutionAttempt debe referenciar exactamente un ExecutionIntent" in text
    assert "Un execution_attempt_id no debe existir como ejecucion real" in text


def test_audit_declares_required_id_guarantees():
    text = _text()

    for guarantee in [
        "unicidad",
        "estabilidad",
        "trazabilidad",
        "no ambiguedad",
        "idempotencia",
        "compatibilidad con stores futuros",
        "compatibilidad con lifecycle/history",
        "serializacion segura",
    ]:
        assert guarantee in text


def test_audit_recommends_format_and_ownership():
    text = _text()

    assert "attempt_<intent_id>_<sequence>_<short_hash>" in text
    assert "Formato recomendado" in text
    assert "Ownership" in text
    assert "attempt factory / attempt builder controlado" in text
    assert "No ExecutionIntent" in text
    assert "No Market Catalog" in text
    assert "No UI" in text
    assert "No API directa" in text


def test_audit_maps_future_store_interactions():
    text = _text()

    for component in [
        "attempt_store",
        "lifecycle_store",
        "dry_run_store",
        "execution_history_view",
        "internal_backend_read_model",
        "result_store",
    ]:
        assert component in text
    for column in ["Estado actual", "Relacion futura esperada", "Riesgo", "Accion recomendada"]:
        assert column in text


def test_market_catalog_and_business_composition_boundaries_are_preserved():
    text = _text()

    assert "Market Catalog Boundary" in text
    assert "planned_not_active" in text
    assert "No crea execution_attempt_id" in text
    assert "No participa en attempt factory" in text
    assert "No participa en lifecycle/result/history operativo" in text
    assert "Business Composition Layer sigue futura/no operativa" in text
    assert "No crea ExecutionAttempt" in text


def test_audit_prohibits_activation_surfaces():
    text = _text()

    for phrase in [
        "execution attempt operativo",
        "execution_attempt_id generator operativo",
        "runtime execution",
        "result store",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "memory persistence",
        "external access",
        "API",
        "UI",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
    ]:
        assert phrase in text


def test_execution_intent_remains_contract_only():
    assert EXECUTION_INTENT_RUNTIME_ENABLED is False
    assert EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED is False
    assert EXECUTION_INTENT_EXECUTION_ENABLED is False


def test_market_catalog_generated_database_remains_planned_not_active():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert catalog["metadata"]["activation_status"] == "not_evaluated"


def test_no_operational_attempt_generator_or_runtime_modules_exist():
    for relative in [
        "core/execution_attempt_id.py",
        "core/execution_result_store.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_audit_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "execution_enabled = true",
        "attempt_creation_enabled = true",
        "runtime_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text


def test_related_docs_reference_prompt_3_2_result():
    assert "PROMPT 3.2 result" in INTENT_DOC.read_text(encoding="utf-8")
    assert "profundiza la frontera entre `ExecutionIntent` y futuro `ExecutionAttempt`" in OPERATIONAL_AUDIT_DOC.read_text(encoding="utf-8")
    assert "PROMPT 3.2 - Auditoria de execution_attempt_id operativo" in PLAN_DOC.read_text(encoding="utf-8")
    assert "PROMPT 3.2 - Auditoria de execution_attempt_id operativo" in BOOK_DOC.read_text(encoding="utf-8")
