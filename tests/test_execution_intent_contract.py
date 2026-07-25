import subprocess
from copy import deepcopy
from pathlib import Path

from core.execution_intent import (
    EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED,
    EXECUTION_INTENT_CONTRACT_STATUS,
    EXECUTION_INTENT_EXECUTION_ENABLED,
    EXECUTION_INTENT_EXTERNAL_ACCESS_ENABLED,
    EXECUTION_INTENT_MEMORY_PERSISTENCE_ENABLED,
    EXECUTION_INTENT_MODEL_INVOCATION_ENABLED,
    EXECUTION_INTENT_RUNTIME_ENABLED,
    EXECUTION_INTENT_SCHEDULER_ENABLED,
    EXECUTION_INTENT_TOOL_EXECUTION_ENABLED,
    EXECUTION_INTENT_WORKER_ENABLED,
    build_execution_intent,
    serialize_execution_intent,
    validate_execution_intent,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EXECUTION_INTENT_CONTRACT.md"
CATALOG_PATH = "data/market_catalog/market_catalog.generated.json"


def _valid_intent():
    return build_execution_intent(
        intent_id="intent_agent_audit_001",
        intent_type="agent_operation",
        source="operational_boundary_audit",
        target_type="agent",
        target_id="agent-1",
        mode="contract_validation",
        requested_by="system",
        readiness="ready_for_attempt_design",
        status="validated",
    )


def _codes(result: dict) -> set[str]:
    return {blocker["code"] for blocker in result["blockers"]}


def _git_status_for(paths: list[str]) -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--", *paths],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def test_execution_intent_module_and_boundaries_exist():
    assert (ROOT / "core/execution_intent.py").exists()
    assert EXECUTION_INTENT_CONTRACT_STATUS == "contract_only"
    assert EXECUTION_INTENT_RUNTIME_ENABLED is False
    assert EXECUTION_INTENT_ATTEMPT_CREATION_ENABLED is False
    assert EXECUTION_INTENT_EXECUTION_ENABLED is False
    assert EXECUTION_INTENT_SCHEDULER_ENABLED is False
    assert EXECUTION_INTENT_WORKER_ENABLED is False
    assert EXECUTION_INTENT_MODEL_INVOCATION_ENABLED is False
    assert EXECUTION_INTENT_TOOL_EXECUTION_ENABLED is False
    assert EXECUTION_INTENT_MEMORY_PERSISTENCE_ENABLED is False
    assert EXECUTION_INTENT_EXTERNAL_ACCESS_ENABLED is False


def test_build_serialize_and_validate_valid_contract_only_intent():
    intent = _valid_intent()
    payload = serialize_execution_intent(intent)
    result = validate_execution_intent(intent)

    assert payload["intent_id"] == "intent_agent_audit_001"
    assert payload["constraints"]["allow_runtime_execution"] is False
    assert result["status"] == "validated"
    assert result["verdict"] == "EXECUTION_INTENT_CONTRACT_READY"
    assert result["readiness"] == "ready_for_execution_attempt_id_audit"


def test_rejects_empty_intent_id():
    payload = serialize_execution_intent(_valid_intent())
    payload["intent_id"] = ""

    assert "missing_intent_id" in _codes(validate_execution_intent(payload))


def test_rejects_unknown_intent_type():
    payload = serialize_execution_intent(_valid_intent())
    payload["intent_type"] = "unknown"

    assert "invalid_intent_type" in _codes(validate_execution_intent(payload))


def test_rejects_unknown_target_type():
    payload = serialize_execution_intent(_valid_intent())
    payload["target"]["target_type"] = "unknown"

    assert "invalid_target_type" in _codes(validate_execution_intent(payload))


def test_rejects_empty_target_id():
    payload = serialize_execution_intent(_valid_intent())
    payload["target"]["target_id"] = ""

    assert "missing_target_id" in _codes(validate_execution_intent(payload))


def test_rejects_unknown_mode_status_and_readiness():
    payload = serialize_execution_intent(_valid_intent())
    payload["mode"] = "execute_now"
    payload["status"] = "running"
    payload["readiness"] = "ready_for_runtime"
    codes = _codes(validate_execution_intent(payload))

    assert "invalid_mode" in codes
    assert "invalid_status" in codes
    assert "invalid_readiness" in codes


def test_rejects_any_operational_constraint_true():
    base = serialize_execution_intent(_valid_intent())
    for field, code in [
        ("allow_runtime_execution", "runtime_execution_not_allowed"),
        ("allow_attempt_creation", "attempt_creation_not_allowed"),
        ("allow_scheduler", "scheduler_not_allowed"),
        ("allow_worker", "worker_not_allowed"),
        ("allow_model_invocation", "model_invocation_not_allowed"),
        ("allow_tool_execution", "tool_execution_not_allowed"),
        ("allow_memory_persistence", "memory_persistence_not_allowed"),
        ("allow_external_access", "external_access_not_allowed"),
    ]:
        payload = deepcopy(base)
        payload["constraints"][field] = True
        assert code in _codes(validate_execution_intent(payload))


def test_market_catalog_review_requires_planned_not_active_catalog():
    intent = build_execution_intent(
        intent_id="intent_market_review_001",
        intent_type="market_catalog_review",
        source="phase_3_contract",
        target_type="market",
        target_id="market_abadia",
        mode="audit_only",
        requested_by="system",
        metadata={"market_catalog_status": "planned_not_active", "market_catalog_runtime_enabled": False},
    )

    assert validate_execution_intent(intent)["status"] == "validated"

    payload = serialize_execution_intent(intent)
    payload["metadata"]["market_catalog_status"] = "active"
    assert "market_catalog_not_planned" in _codes(validate_execution_intent(payload))


def test_business_composition_review_requires_future_non_operational_layer():
    intent = build_execution_intent(
        intent_id="intent_bcl_review_001",
        intent_type="business_composition_review",
        source="phase_3_contract",
        target_type="business_composition_candidate",
        target_id="candidate-1",
        mode="audit_only",
        requested_by="system",
        metadata={"business_composition_layer_operational": False},
    )

    assert validate_execution_intent(intent)["status"] == "validated"

    payload = serialize_execution_intent(intent)
    payload["metadata"]["business_composition_layer_operational"] = True
    assert "business_composition_layer_not_allowed" in _codes(validate_execution_intent(payload))


def test_contract_does_not_create_attempts_or_operational_stores():
    for relative in [
        "core/execution_attempt_id.py",
        "core/execution_result_store.py",
        "core/scheduler_queue.py",
        "core/worker_queue.py",
    ]:
        assert not (ROOT / relative).exists(), relative


def test_contract_does_not_modify_market_catalog_database():
    before = (ROOT / CATALOG_PATH).read_text(encoding="utf-8")
    validate_execution_intent(_valid_intent())
    after = (ROOT / CATALOG_PATH).read_text(encoding="utf-8")

    assert before == after
    assert _git_status_for([CATALOG_PATH]) == ""


def test_execution_intent_contract_document_declares_readiness_and_boundaries():
    text = DOC.read_text(encoding="utf-8")

    assert "EXECUTION_INTENT_CONTRACT_READY" in text
    assert "ready_for_execution_attempt_id_audit" in text
    assert "PROMPT 3.2 — Auditoría de execution_attempt_id operativo" in text
    for phrase in [
        "runtime execution",
        "attempt creation",
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
        assert phrase in text
