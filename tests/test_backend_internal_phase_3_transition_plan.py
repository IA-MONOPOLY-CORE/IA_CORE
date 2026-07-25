import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_DOC = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
MARKET_DOC = ROOT / "docs" / "MARKET_CATALOG_PRODUCT_DECISION.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _text() -> str:
    return PLAN_DOC.read_text(encoding="utf-8")


def _git_status_for(paths: list[str]) -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--", *paths],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def test_phase_3_transition_plan_exists_and_is_ready():
    text = _text()

    assert PLAN_DOC.exists()
    assert "PHASE_3_TRANSITION_PLAN_READY" in text
    assert "ready_for_phase_3_operational_boundary_audit" in text
    assert "PROMPT 3.0 — Auditoría de frontera operacional" in text
    assert "BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_PASSED" in text
    assert "MARKET_CATALOG_REGISTERED_AS_PLANNED_DATABASE" in text


def test_market_catalog_and_business_composition_layer_are_future_only():
    text = _text()

    assert "planned_not_active" in text
    assert "Market Catalog runtime" in text
    assert "Business Composition Layer futura" in text
    assert "Business Composition Layer runtime" in text
    assert "fuera de la implementacion actual" in text


def test_plan_prohibits_automatic_activation_surfaces():
    text = _text()

    for phrase in [
        "no runtime operativo",
        "no ejecucion real",
        "no scheduler",
        "no worker",
        "no queue",
        "no model invocation",
        "no tool execution",
        "no memory persistence",
        "no external access",
        "no API publica",
        "no UI",
        "no Market Catalog runtime",
        "no Business Composition Layer runtime",
    ]:
        assert phrase in text


def test_tentative_phase_3_sequence_and_next_step_are_documented():
    text = _text()

    for prompt in [
        "PROMPT 3.0 — Auditoría de frontera operacional",
        "PROMPT 3.1 — Contrato de execution intent operativo",
        "PROMPT 3.2 — Auditoría de execution_attempt_id operativo",
        "PROMPT 3.3 — Schema de execution attempt operativo",
        "PROMPT 3.4 — State machine operacional contract-only",
        "PROMPT 3.5 — Result store boundary audit",
        "PROMPT 3.6 — Result store contract/read-only design",
        "PROMPT 3.7 — Operational readiness gate",
        "PROMPT 3.8 — E2E pre-operational-to-operational checkpoint",
    ]:
        assert prompt in text
    assert "sujeta a la auditoria de frontera operacional en 3.0" in text


def test_plan_has_no_contradictory_activation_states():
    text = _text()

    for forbidden in [
        "runtime_enabled = true",
        "business_composition_enabled = true",
        "market_catalog_active",
        "execution_enabled",
        "scheduler_enabled",
        "worker_enabled",
    ]:
        assert forbidden not in text


def test_market_catalog_generated_database_remains_planned_and_unmodified():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["status"] == "planned_not_active"
    assert catalog["runtime_enabled"] is False
    assert catalog["business_composition_enabled"] is False
    assert catalog["metadata"]["activation_status"] == "not_evaluated"
    assert _git_status_for(["data/market_catalog/market_catalog.generated.json"]) == ""


def test_book_checkpoint_and_market_docs_reference_transition():
    book = BOOK_DOC.read_text(encoding="utf-8")
    market_doc = MARKET_DOC.read_text(encoding="utf-8")

    assert "PROMPT 2.51 - Plan de transicion hacia Backend Interno Fase 3.x" in book
    assert "PROMPT 3.0 — Auditoría de frontera operacional" in book
    assert "Market Catalog queda como planned database no activa" in book
    assert "plan de transicion 2.51" in market_doc
