from pathlib import Path

import pytest

from core.execution_result import build_execution_result_contract
import core.execution_result_projection as projection


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EXECUTION_RESULT_PROJECTION_CONTRACT.md"
CATALOG_PATH = ROOT / "data" / "market_catalog" / "market_catalog.generated.json"


def _valid_result():
    return build_execution_result_contract(
        result_id="result_001",
        attempt_id="attempt_intent_demo_1_abcd1234",
        intent_id="intent_demo",
        status="schema_validated",
        result_type="contract_validation",
        summary="safe summary",
        warnings=["warn"],
        artifacts=[{"artifact_id": "artifact_1"}],
    )


def _codes(result):
    return {blocker["code"] for blocker in result["blockers"]}


def test_projection_module_exists_and_boundaries_are_declared():
    assert (ROOT / "core" / "execution_result_projection.py").exists()
    assert projection.EXECUTION_RESULT_PROJECTION_STATUS == "read_only_contract"
    assert projection.EXECUTION_RESULT_PROJECTION_ENABLED is True
    assert projection.get_execution_result_projection_contract()["projection_enabled_scope"] == "pure_read_only_in_memory_transformation"


def test_projection_boundary_flags_disable_writes_and_runtime():
    for name in [
        "EXECUTION_RESULT_PROJECTION_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_HISTORY_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_READ_MODEL_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_RESULT_STORE_ENABLED",
        "EXECUTION_RESULT_PROJECTION_RESULT_STORE_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_RUNTIME_ENABLED",
        "EXECUTION_RESULT_PROJECTION_EXECUTION_ENABLED",
        "EXECUTION_RESULT_PROJECTION_LIFECYCLE_WRITES_ENABLED",
        "EXECUTION_RESULT_PROJECTION_SCHEDULER_ENABLED",
        "EXECUTION_RESULT_PROJECTION_WORKER_ENABLED",
        "EXECUTION_RESULT_PROJECTION_QUEUE_ENABLED",
        "EXECUTION_RESULT_PROJECTION_MODEL_INVOCATION_ENABLED",
        "EXECUTION_RESULT_PROJECTION_TOOL_EXECUTION_ENABLED",
        "EXECUTION_RESULT_PROJECTION_MEMORY_PERSISTENCE_ENABLED",
        "EXECUTION_RESULT_PROJECTION_EXTERNAL_ACCESS_ENABLED",
    ]:
        assert getattr(projection, name) is False


def test_project_execution_result_for_history_returns_safe_projection():
    original = _valid_result()
    before = original.to_dict()

    projected = projection.project_execution_result_for_history(original)

    assert original.to_dict() == before
    assert projected == {
        "projection_type": "execution_result_history_projection",
        "intent_id": "intent_demo",
        "attempt_id": "attempt_intent_demo_1_abcd1234",
        "result_id": "result_001",
        "result_status": "schema_validated",
        "result_type": "contract_validation",
        "created_at": before["created_at"],
        "completed_at": None,
        "summary": "safe summary",
        "warnings_count": 1,
        "artifacts_count": 1,
        "has_error": False,
        "is_runtime_backed": False,
        "is_dry_run": False,
        "source": "execution_result_contract",
        "read_only": True,
    }
    assert projection.validate_execution_result_projection(projected)["status"] == "validated"


def test_project_execution_result_for_read_model_returns_safe_projection():
    original = _valid_result()
    before = original.to_dict()

    projected = projection.project_execution_result_for_read_model(original)

    assert original.to_dict() == before
    assert projected["projection_type"] == "execution_result_read_model_projection"
    assert projected["intent_id"] == "intent_demo"
    assert projected["attempt_id"] == "attempt_intent_demo_1_abcd1234"
    assert projected["result_id"] == "result_001"
    assert projected["status"] == "schema_validated"
    assert projected["result_type"] == "contract_validation"
    assert projected["summary"] == "safe summary"
    assert projected["has_warnings"] is True
    assert projected["warnings_count"] == 1
    assert projected["artifacts_count"] == 1
    assert projected["has_error"] is False
    assert projected["is_runtime_backed"] is False
    assert projected["is_dry_run"] is False
    assert projected["source"] == "execution_result_contract"
    assert projected["safe_for_internal_backend_read_model"] is True
    assert projected["read_only"] is True
    assert projection.validate_execution_result_projection(projected)["status"] == "validated"


def test_projection_functions_validate_execution_result_first():
    invalid = _valid_result().to_dict()
    invalid["result_id"] = ""

    with pytest.raises(ValueError, match="execution_result_contract_not_validated"):
        projection.project_execution_result_for_history(invalid)
    with pytest.raises(ValueError, match="execution_result_contract_not_validated"):
        projection.project_execution_result_for_read_model(invalid)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("projection_type", "unknown", "invalid_projection_type"),
        ("intent_id", "", "missing_intent_id"),
        ("attempt_id", "", "missing_attempt_id"),
        ("result_id", "", "missing_result_id"),
        ("warnings_count", -1, "negative_warnings_count"),
        ("artifacts_count", -1, "negative_artifacts_count"),
        ("is_runtime_backed", True, "runtime_backed_not_allowed"),
        ("read_only", False, "read_only_required"),
        ("output_ref", {"path": "x"}, "output_ref_not_allowed"),
        ("error_ref", {"path": "x"}, "error_ref_not_allowed"),
        ("metadata", {"raw": True}, "metadata_not_allowed"),
        ("runtime_enabled", True, "runtime_enabled_not_allowed"),
        ("history_writes_enabled", True, "history_writes_enabled_not_allowed"),
    ],
)
def test_validate_projection_rejects_unsafe_values(field, value, code):
    payload = projection.project_execution_result_for_history(_valid_result())
    payload[field] = value

    result = projection.validate_execution_result_projection(payload)

    assert result["status"] == "blocked"
    assert code in _codes(result)


def test_serialize_projection_returns_copy():
    payload = projection.project_execution_result_for_history(_valid_result())
    serialized = projection.serialize_execution_result_projection(payload)

    assert serialized == payload
    assert serialized is not payload


def test_no_public_write_sync_or_persist_functions_exist():
    forbidden = {
        "write_execution_result_to_history",
        "write_execution_result_to_read_model",
        "persist_execution_result_projection",
        "save_execution_result_projection",
        "apply_execution_result_projection",
        "sync_execution_result_to_history",
        "sync_execution_result_to_read_model",
    }
    public_names = {name for name in dir(projection) if not name.startswith("_")}

    assert forbidden.isdisjoint(public_names)


def test_market_catalog_and_business_composition_remain_inactive():
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")
    contract = projection.get_execution_result_projection_contract()

    assert "planned_not_active" in catalog_text
    assert contract["boundaries"]["market_catalog_runtime_enabled"] is False
    assert contract["boundaries"]["business_composition_layer_runtime_enabled"] is False


def test_projection_contract_document_contains_required_markers():
    text = DOC.read_text(encoding="utf-8")

    for phrase in [
        "EXECUTION_RESULT_PROJECTION_CONTRACT_READY",
        "EXECUTION_RESULT_PROJECTION_E2E_PASSED",
        "ready_for_result_projection_e2e_checkpoint",
        "PROMPT 3.8.1 — Checkpoint E2E de projection result/history/read model",
        "read-only contract",
        "pure projection only",
        "no result store operativo",
        "no history writes",
        "no read model writes",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text
