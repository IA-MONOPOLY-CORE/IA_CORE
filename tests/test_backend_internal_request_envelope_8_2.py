import json
from pathlib import Path

from core.backend_internal_exposure_registry import build_internal_exposure_registry, validate_internal_exposure_registry
from core.backend_internal_request_envelope import (
    ALLOWED_CALLER_KINDS,
    BLOCKED_CALLER_KINDS,
    REQUEST_READINESS,
    SCHEMA_VERSION,
    build_internal_request_envelope,
    build_internal_request_error,
    is_request_blocked,
    is_request_for_exposable_service,
    normalize_internal_request_error,
    validate_internal_request_envelope,
    validate_request_against_exposure_registry,
)
from core.backend_internal_ui_contract import build_backend_internal_ui_contract, validate_backend_internal_ui_contract


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_REQUEST_ENVELOPE_8_2.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"

FORBIDDEN_FILES = (
    "core/backend_internal_ui_dispatcher.py",
    "core/backend_internal_confirmation_gate.py",
    "core/backend_internal_response_adapter.py",
    "core/backend_internal_ui_router.py",
    "core/backend_internal_ui_api.py",
    "core/backend_internal_public_endpoint.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_dispatcher.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/integration_runtime.py",
)


def _codes(result: dict) -> set[str]:
    return {error["error_code"] for error in result["errors"]}


def _safe_root() -> dict:
    return {"declared": True, "root_kind": "controlled_sandbox", "path_policy": "manifest_bound"}


def _valid_confirmation(service_id: str) -> dict:
    return {
        "confirmed": True,
        "confirmation_scope": service_id,
        "human_confirmation_required": True,
        "confirmed_by": "internal_test",
        "confirmation_id": f"confirm_{service_id}_001",
    }


def test_request_envelope_builder_validator_schema_and_json_safety():
    request = build_internal_request_envelope(
        request_id="req_8_2_001",
        service_id="stable_ui_payloads",
        caller_kind="internal_test",
        payload={"payload": {"status": "ready"}},
    )
    result = validate_internal_request_envelope(request)

    assert request["schema_version"] == SCHEMA_VERSION == "backend_internal_ui_request.v1"
    assert request["request_id"] == "req_8_2_001"
    assert request["service_id"] == "stable_ui_payloads"
    assert set(["caller", "payload", "confirmation", "safety", "meta"]) <= set(request)
    assert request["meta"]["intended_response_schema"] == "backend_internal_ui_payload.v1"
    assert request["meta"]["dispatcher_created"] is False
    assert request["meta"]["request_handling_enabled"] is False
    assert result["valid"] is True
    assert result["readiness"] == REQUEST_READINESS == "ready_for_phase_8_3_internal_dispatcher_no_runtime"
    assert result["dispatcher_created"] is False
    assert result["request_handling_enabled"] is False
    assert result["operational"] is False
    json.dumps(request, ensure_ascii=False, sort_keys=True)
    json.dumps(result, ensure_ascii=False, sort_keys=True)


def test_allowed_and_blocked_caller_kinds_are_enforced():
    for caller_kind in ALLOWED_CALLER_KINDS:
        request = build_internal_request_envelope(
            request_id=f"req_{caller_kind}",
            service_id="stable_ui_payloads",
            caller_kind=caller_kind,
            payload={"payload": {"status": "ready"}},
        )
        assert validate_internal_request_envelope(request)["valid"] is True

    for caller_kind in BLOCKED_CALLER_KINDS:
        request = build_internal_request_envelope(
            request_id=f"req_{caller_kind}",
            service_id="stable_ui_payloads",
            caller_kind=caller_kind,
            payload={"payload": {"status": "ready"}},
        )
        result = validate_internal_request_envelope(request)
        assert result["valid"] is False
        assert {"INVALID_CALLER_KIND", "UNTRUSTED_CALLER"} & _codes(result)

    trusted = build_internal_request_envelope(
        request_id="req_trusted_ui",
        service_id="stable_ui_payloads",
        caller_kind="internal_ui_future",
        payload={"payload": {"status": "ready"}},
    )
    trusted["caller"]["trusted"] = True
    assert "UNTRUSTED_CALLER" in _codes(validate_internal_request_envelope(trusted))


def test_registry_service_checks_pass_for_exposable_and_fail_for_missing_or_blocked():
    registry = build_internal_exposure_registry()
    assert validate_internal_exposure_registry(registry) == registry

    request = build_internal_request_envelope(
        request_id="req_registry_ok",
        service_id="stable_ui_payloads",
        caller_kind="backend_internal",
        payload={"payload": {"status": "ready"}},
    )
    assert is_request_for_exposable_service(request) is True
    assert is_request_blocked(request) is False
    assert validate_request_against_exposure_registry(request)["valid"] is True

    missing = build_internal_request_envelope(
        request_id="req_missing",
        service_id="missing_service",
        payload={},
    )
    assert "SERVICE_NOT_FOUND" in _codes(validate_internal_request_envelope(missing))

    blocked = build_internal_request_envelope(
        request_id="req_runtime",
        service_id="runtime_execution",
        payload={},
    )
    result = validate_internal_request_envelope(blocked)
    assert result["valid"] is False
    assert "SERVICE_BLOCKED" in _codes(result)


def test_safety_block_rejects_runtime_execution_tools_models_integrations_public_ui_and_operational_domains():
    flag_to_error = {
        "runtime_allowed": "RUNTIME_REQUEST_BLOCKED",
        "execution_allowed": "EXECUTION_REQUEST_BLOCKED",
        "tools_allowed": "TOOLS_REQUEST_BLOCKED",
        "models_allowed": "MODELS_REQUEST_BLOCKED",
        "integrations_allowed": "INTEGRATIONS_REQUEST_BLOCKED",
        "public_endpoint_allowed": "PUBLIC_ENDPOINT_REQUEST_BLOCKED",
        "ui_runtime_allowed": "UI_RUNTIME_REQUEST_BLOCKED",
        "operational_domains_allowed": "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
    }
    for flag, code in flag_to_error.items():
        request = build_internal_request_envelope(
            request_id=f"req_{flag}",
            service_id="stable_ui_payloads",
            payload={"payload": {"status": "ready"}},
            safety={flag: True},
        )
        result = validate_internal_request_envelope(request)
        assert result["valid"] is False
        assert code in _codes(result)
        assert result["dispatcher_created"] is False
        assert result["request_handling_enabled"] is False


def test_safe_sandbox_root_and_confirmation_are_enforced():
    without_root = build_internal_request_envelope(
        request_id="req_without_root",
        service_id="list_domains_status",
        caller_kind="internal_test",
        payload={},
    )
    assert "SAFE_SANDBOX_ROOT_REQUIRED" in _codes(validate_internal_request_envelope(without_root))

    without_confirmation = build_internal_request_envelope(
        request_id="req_without_confirmation",
        service_id="materialize_sandbox",
        caller_kind="internal_test",
        payload={"sandbox_root": _safe_root(), "preview_payload": {"valid": True}},
    )
    result = validate_internal_request_envelope(without_confirmation)
    assert "CONFIRMATION_REQUIRED" in _codes(result)

    valid = build_internal_request_envelope(
        request_id="req_materialize_ok",
        service_id="materialize_sandbox",
        caller_kind="internal_test",
        payload={"sandbox_root": _safe_root(), "preview_payload": {"valid": True}},
        confirmation=_valid_confirmation("materialize_sandbox"),
    )
    assert validate_internal_request_envelope(valid)["valid"] is True


def test_lifecycle_validation_payload_preview_and_allow_flags_are_enforced():
    lifecycle = build_internal_request_envelope(
        request_id="req_rollback_missing_validation",
        service_id="rollback_sandbox",
        caller_kind="internal_test",
        payload={"sandbox_root": _safe_root()},
        confirmation=_valid_confirmation("rollback_sandbox"),
    )
    assert "VALIDATION_PAYLOAD_REQUIRED" in _codes(validate_internal_request_envelope(lifecycle))

    delete = build_internal_request_envelope(
        request_id="req_delete_missing_allow",
        service_id="delete_sandbox_domain",
        caller_kind="internal_test",
        payload={"sandbox_root": _safe_root(), "validation_payload": {"passed": True}},
        confirmation=_valid_confirmation("delete_sandbox_domain"),
    )
    assert "ALLOW_DELETE_REQUIRED" in _codes(validate_internal_request_envelope(delete))

    reset = build_internal_request_envelope(
        request_id="req_reset_missing_allow",
        service_id="reset_sandbox_domain",
        caller_kind="internal_test",
        payload={"sandbox_root": _safe_root(), "validation_payload": {"passed": True}},
        confirmation=_valid_confirmation("reset_sandbox_domain"),
    )
    assert "ALLOW_RESET_REQUIRED" in _codes(validate_internal_request_envelope(reset))

    materialize = build_internal_request_envelope(
        request_id="req_materialize_missing_preview",
        service_id="materialize_sandbox",
        caller_kind="internal_test",
        payload={"sandbox_root": _safe_root()},
        confirmation=_valid_confirmation("materialize_sandbox"),
    )
    assert "PREVIEW_PAYLOAD_REQUIRED" in _codes(validate_internal_request_envelope(materialize))

    valid_delete = build_internal_request_envelope(
        request_id="req_delete_ok",
        service_id="delete_sandbox_domain",
        caller_kind="internal_test",
        payload={
            "sandbox_root": _safe_root(),
            "validation_payload": {"passed": True},
            "options": {"allow_delete": True},
        },
        confirmation=_valid_confirmation("delete_sandbox_domain"),
    )
    assert validate_internal_request_envelope(valid_delete)["valid"] is True


def test_forbidden_action_secret_traceback_absolute_path_and_dispatcher_meta_are_blocked():
    forbidden = build_internal_request_envelope(
        request_id="req_forbidden_action",
        service_id="stable_ui_payloads",
        action="activate_runtime",
        payload={"payload": {"status": "ready"}},
    )
    assert "FORBIDDEN_ACTION_REQUESTED" in _codes(validate_internal_request_envelope(forbidden))

    secret = build_internal_request_envelope(
        request_id="req_secret",
        service_id="stable_ui_payloads",
        payload={"api_key": "blocked"},
    )
    assert "SECRET_LIKE_FIELD_BLOCKED" in _codes(validate_internal_request_envelope(secret))

    traceback = build_internal_request_envelope(
        request_id="req_traceback",
        service_id="stable_ui_payloads",
        payload={"error": "Traceback (most recent call last): File \"x.py\", line 1"},
    )
    assert "TRACEBACK_BLOCKED" in _codes(validate_internal_request_envelope(traceback))

    absolute = build_internal_request_envelope(
        request_id="req_absolute",
        service_id="stable_ui_payloads",
        payload={"path": "C:\\IA_CORE\\domains\\real"},
    )
    assert "ABSOLUTE_PATH_BLOCKED" in _codes(validate_internal_request_envelope(absolute))

    dispatcher = build_internal_request_envelope(
        request_id="req_dispatcher",
        service_id="stable_ui_payloads",
        payload={"payload": {"status": "ready"}},
        meta={"dispatcher_created": True, "request_handling_enabled": True},
    )
    result = validate_internal_request_envelope(dispatcher)
    assert {"DISPATCHER_NOT_AVAILABLE", "REQUEST_HANDLING_NOT_ENABLED"} <= _codes(result)


def test_error_contract_and_validation_result_are_stable_and_non_operational():
    error = build_internal_request_error("SERVICE_NOT_FOUND", "missing", field="service_id")
    assert normalize_internal_request_error(error) == error
    assert error["blocked"] is True
    assert error["recoverable"] is True

    invalid = validate_internal_request_envelope({})
    assert invalid["valid"] is False
    assert invalid["schema_version"] == "backend_internal_ui_request.v1"
    assert invalid["validation_schema_version"] == "backend_internal_ui_request_validation.v1"
    assert invalid["dispatcher_created"] is False
    assert invalid["request_handling_enabled"] is False
    assert invalid["operational"] is False
    assert invalid["runtime_enabled"] is False
    assert invalid["execution_enabled"] is False
    assert invalid["tools_enabled"] is False
    assert invalid["models_enabled"] is False
    assert invalid["integrations_enabled"] is False
    assert invalid["public_endpoint"] is False
    assert invalid["ui_visual"] is False
    json.dumps(invalid, ensure_ascii=False, sort_keys=True)


def test_ui_contract_marks_8_2_available_and_keeps_8_3_plus_planned():
    contract = build_backend_internal_ui_contract()
    assert validate_backend_internal_ui_contract(contract) == contract
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    for name in ("internal_request_envelope", "internal_request_validation"):
        assert available[name]["available_now"] is True
        assert available[name]["phase"] == "8.2"
        assert available[name]["side_effects"] is False
        assert available[name]["public_endpoint"] is False
        assert available[name]["touches_visual_ui"] is False
        assert available[name]["runtime_enabled"] is False
        assert available[name]["execution_enabled"] is False
        assert available[name]["dispatcher_created"] is False
        assert available[name]["request_handling_enabled"] is False

    assert available["internal_request_envelope"]["type"] == "contract/request-envelope"
    assert available["internal_request_validation"]["type"] == "contract/request-validation"
    for name in ("internal_dispatcher_no_runtime", "confirmation_gate", "internal_response_adapter"):
        assert planned[name]["available_now"] is False
        assert planned[name]["dispatcher_created"] is False
        assert planned[name]["request_handling_enabled"] is False


def test_docs_plans_book_and_adr_record_prompt_8_2():
    for path in (DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_REQUEST_ENVELOPE_READY",
        "BACKEND_INTERNAL_REQUEST_VALIDATION_READY",
        "BACKEND_INTERNAL_REQUEST_VALIDATION_NO_DISPATCHER_CONFIRMED",
        "BACKEND_INTERNAL_REQUEST_VALIDATION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_8_3_internal_dispatcher_no_runtime",
        "PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto",
        "backend_internal_ui_request.v1",
        "backend_internal_ui_payload.v1",
        "No dispatcher",
        "No request handling",
        "No ejecucion de servicios",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.2 - Internal request envelope y request validation",
        "BACKEND_INTERNAL_REQUEST_ENVELOPE_READY",
        "BACKEND_INTERNAL_REQUEST_VALIDATION_READY",
        "ready_for_phase_8_3_internal_dispatcher_no_runtime",
        "internal_request_envelope",
        "internal_request_validation",
        "no dispatcher",
        "no request handling",
        "no routing",
        "no UI visual",
        "no endpoints publicos",
        "`domains/` operativo",
    ):
        assert token in combined


def test_no_dispatcher_ui_endpoint_domains_or_temp_artifacts_created():
    for relative in FORBIDDEN_FILES:
        assert not (ROOT / relative).exists(), relative
    assert DOMAINS.exists()
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
