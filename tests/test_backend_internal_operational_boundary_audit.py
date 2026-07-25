import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_OPERATIONAL_BOUNDARY_AUDIT.md"
TRANSITION_DOC = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def test_operational_boundary_audit_document_exists_and_is_ready():
    text = _text()

    assert AUDIT_DOC.exists()
    assert "OPERATIONAL_BOUNDARY_AUDIT_COMPLETED" in text
    assert "OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN" in text
    assert "ready_for_execution_intent_contract" in text
    assert "PROMPT 3.1 — Contrato de execution intent operativo" in text


def test_audit_defines_required_operational_concepts():
    text = _text()

    for concept in [
        "execution",
        "execution intent",
        "execution attempt",
        "execution_attempt_id",
        "operational state",
        "result",
        "result store",
        "lifecycle event",
        "history event",
        "readiness gate",
        "runtime boundary",
    ]:
        assert concept in text


def test_pre_operational_vs_operational_is_explicit():
    text = _text()

    assert "Pre-operacional" in text
    assert "Operacional" in text
    for item in ["preview", "dry-run", "preflight attempt", "history derived-only", "read model read-only"]:
        assert item in text
    for item in ["intent real", "attempt operativo", "resultado persistido", "errores operativos"]:
        assert item in text


def test_market_catalog_and_business_composition_boundaries_are_preserved():
    text = _text()

    assert "Market Catalog Boundary" in text
    assert "planned_not_active" in text
    assert "no participa en execution intent" in text
    assert "no participa en execution attempt" in text
    assert "no participa en result store" in text
    assert "Business Composition Layer sigue futura/no operativa" in text


def test_audit_prohibits_operational_activation_surfaces():
    text = _text()

    for phrase in [
        "runtime operativo",
        "execution real",
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


def test_gap_classification_is_documented():
    text = _text()

    assert "Critical gaps" in text
    assert "Major gaps" in text
    assert "Minor gaps" in text
    assert "Deferred items" in text
    assert "none." in text


def test_audit_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "runtime_enabled = true",
        "execution_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text


def test_market_catalog_database_remains_planned_not_active():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert catalog["metadata"]["activation_status"] == "not_evaluated"


def test_phase_3_transition_plan_still_exists_and_keeps_readiness():
    text = TRANSITION_DOC.read_text(encoding="utf-8")

    assert "PHASE_3_TRANSITION_PLAN_READY" in text
    assert "ready_for_phase_3_operational_boundary_audit" in text
