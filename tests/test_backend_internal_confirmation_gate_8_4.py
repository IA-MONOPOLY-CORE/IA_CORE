import json
from copy import deepcopy
from pathlib import Path

from core.backend_internal_confirmation_gate import (
    GATE_READINESS,
    GATE_SCHEMA_VERSION,
    build_confirmation_gate_error,
    get_required_confirmation_scope,
    is_confirmation_required_for_service,
    validate_confirmation_gate,
    validate_confirmation_scope,
)
from core.backend_internal_dispatcher import dispatch_internal_request
from core.backend_internal_request_envelope import build_internal_request_envelope
from core.backend_internal_ui_contract import build_backend_internal_ui_contract, validate_backend_internal_ui_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BACKEND_INTERNAL_CONFIRMATION_GATE_8_4.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"

FORBIDDEN_RUNTIME_FILES = (
    "core/backend_internal_controlled_execution_adapter.py",
    "core/backend_internal_ui_router.py",
    "core/backend_internal_ui_api.py",
    "core/backend_internal_public_endpoint.py",
    "core/backend_ui_endpoint.py",
    "core/backend_ui_api.py",
    "core/ui_runtime.py",
    "core/frontend_runtime.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/context_injection_runtime.py",
    "core/output_delivery_runtime.py",
    "core/integration_runtime.py",
)


def _safe_root() -> dict:
    return {"declared": True, "root_kind": "controlled_sandbox", "path_policy": "manifest_bound"}


def _valid_confirmation(service_id: str) -> dict:
    return {
        "confirmed": True,
        "confirmation_scope": service_id,
        "human_confirmation_required": True,
        "confirmed_by": "internal_test",
        "confirmation_id": f"confirm_{service_id}_8_4",
    }


def _materialize_request(**overrides: dict) -> dict:
    payload = {
        "sandbox_root": _safe_root(),
        "preview_payload": {
            "preview_id": "preview_8_4",
            "planned_artifacts": ["domain.json", "artifact_manifest.json"],
        },
    }
    payload.update(overrides)
    return build_internal_request_envelope(
        request_id="req_materialize_8_4",
        service_id="materialize_sandbox",
        caller_kind="internal_test",
        payload=payload,
        confirmation=_valid_confirmation("materialize_sandbox"),
    )


def _lifecycle_request(service_id: str, **overrides: dict) -> dict:
    payload = {
        "sandbox_root": _safe_root(),
        "validation_payload": {
            "validation_id": "validation_8_4",
            "passed": True,
            "readiness": "ready_for_lifecycle",
        },
    }
    if service_id == "delete_sandbox_domain":
        payload["allow_delete"] = True
    if service_id == "reset_sandbox_domain":
        payload["allow_reset"] = True
    payload.update(overrides)
    return build_internal_request_envelope(
        request_id=f"req_{service_id}_8_4",
        service_id=service_id,
        caller_kind="internal_test",
        payload=payload,
        confirmation=_valid_confirmation(service_id),
    )


def _gate_codes(result: dict) -> set[str]:
    return {error["code"] for error in result["errors"]}


def test_read_only_and_contract_services_pass_without_confirmation_or_side_effects():
    for service_id in (
        "list_domains_status",
        "preview_materialization",
        "validate_domain",
        "stable_ui_payloads",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
    ):
        payload = {"sandbox_root": _safe_root()} if service_id in {"list_domains_status", "preview_materialization", "validate_domain"} else {}
        if service_id == "preview_materialization":
            payload["domain_request"] = {"domain_id": "demo"}
        if service_id == "validate_domain":
            payload["domain_id"] = "demo"
        if service_id == "internal_request_validation":
            payload["request_envelope"] = build_internal_request_envelope(
                request_id="nested_8_4",
                service_id="stable_ui_payloads",
                caller_kind="internal_test",
                payload={"payload": {"status": "ready"}},
            )
        if service_id == "internal_dispatcher_no_runtime":
            payload["request_envelope"] = build_internal_request_envelope(
                request_id="nested_dispatch_8_4",
                service_id="stable_ui_payloads",
                caller_kind="internal_test",
                payload={"payload": {"status": "ready"}},
            )

        request = build_internal_request_envelope(
            request_id=f"req_{service_id}_8_4",
            service_id=service_id,
            caller_kind="internal_test",
            payload=payload,
        )
        result = validate_confirmation_gate({"request_envelope": request})

        assert result["schema_version"] == GATE_SCHEMA_VERSION
        assert result["confirmation_required"] is False
        assert result["confirmation_gate_passed"] is True
        assert result["requires_confirmation_gate"] is False
        assert result["dispatch_executed"] is False
        assert result["side_effects_performed"] is False
        assert result["runtime_enabled"] is False
        assert result["execution_enabled"] is False
        assert result["tools_enabled"] is False
        assert result["models_enabled"] is False
        assert result["integrations_enabled"] is False
        assert result["readiness"] == GATE_READINESS == "ready_for_phase_8_5_internal_response_adapter"
        json.dumps(result, ensure_ascii=False, sort_keys=True)


def test_materialize_gate_requires_confirmation_preview_safe_root_and_allow_controlled_write():
    blocked = validate_confirmation_gate(
        {
            "request_envelope": _materialize_request(preview_payload=None),
            "gate_options": {"allow_controlled_write": False},
        }
    )

    assert blocked["confirmation_gate_passed"] is False
    assert "CONTROLLED_WRITE_NOT_ALLOWED" in _gate_codes(blocked)
    assert "PREVIEW_PAYLOAD_REQUIRED" in _gate_codes(blocked)
    assert blocked["dispatch_executed"] is False

    passed = validate_confirmation_gate(
        {
            "request_envelope": _materialize_request(),
            "gate_options": {"allow_controlled_write": True},
        }
    )

    assert passed["confirmation_gate_passed"] is True
    assert passed["confirmation_required"] is True
    assert passed["confirmation_valid"] is True
    assert passed["confirmation_scope"] == "materialize_sandbox"
    assert passed["dispatch_allowed_by_gate"] is True
    assert passed["dispatch_executed"] is False
    assert passed["ready_for_controlled_execution_adapter"] is False
    assert passed["flags"]["controlled_write_executed"] is False


def test_lifecycle_gate_requires_validation_payload_and_specific_delete_reset_flags():
    delete_passed = validate_confirmation_gate(
        {
            "request_envelope": _lifecycle_request("delete_sandbox_domain"),
            "gate_options": {"allow_lifecycle": True},
        }
    )
    assert delete_passed["confirmation_gate_passed"] is True
    assert delete_passed["allow_delete_present"] is True
    assert delete_passed["dispatch_executed"] is False

    reset_blocked = validate_confirmation_gate(
        {
            "request_envelope": _lifecycle_request("reset_sandbox_domain", allow_reset=False),
            "gate_options": {"allow_lifecycle": True},
        }
    )
    assert reset_blocked["confirmation_gate_passed"] is False
    assert "ALLOW_RESET_REQUIRED" in _gate_codes(reset_blocked)
    assert reset_blocked["dispatch_executed"] is False


def test_all_lifecycle_services_pass_gate_with_validation_payload_and_are_not_executed():
    for service_id in (
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
    ):
        result = validate_confirmation_gate(
            {
                "request_envelope": _lifecycle_request(service_id),
                "gate_options": {"allow_lifecycle": True},
            }
        )

        assert result["confirmation_required"] is True
        assert result["confirmation_gate_passed"] is True
        assert result["validation_payload_present"] is True
        assert result["dispatch_allowed_by_gate"] is True
        assert result["dispatch_executed"] is False
        assert result["side_effects_performed"] is False
        assert result["flags"]["controlled_lifecycle_executed"] is False
        if service_id == "delete_sandbox_domain":
            assert result["allow_delete_present"] is True
        if service_id == "reset_sandbox_domain":
            assert result["allow_reset_present"] is True


def test_confirmation_block_invalid_cases_are_rejected_with_specific_codes():
    base = _materialize_request()
    cases = (
        ({"confirmation": None}, {"CONFIRMATION_REQUIRED", "CONFIRMATION_MISSING"}),
        ({"confirmed": False}, {"CONFIRMATION_NOT_CONFIRMED"}),
        ({"human_confirmation_required": False}, {"HUMAN_CONFIRMATION_REQUIRED"}),
        ({"confirmation_scope": ""}, {"CONFIRMATION_SCOPE_REQUIRED"}),
        ({"confirmation_scope": "rollback_sandbox"}, {"INVALID_CONFIRMATION_SCOPE"}),
        ({"confirmed_by": ""}, {"CONFIRMED_BY_REQUIRED"}),
        ({"confirmation_id": ""}, {"CONFIRMATION_ID_REQUIRED"}),
    )

    for overrides, expected_codes in cases:
        request = deepcopy(base)
        if "confirmation" in overrides and overrides["confirmation"] is None:
            request.pop("confirmation")
        else:
            request["confirmation"].update(overrides)
        result = validate_confirmation_gate(
            {
                "request_envelope": request,
                "gate_options": {"allow_controlled_write": True},
            }
        )

        assert result["confirmation_gate_passed"] is False
        assert expected_codes <= _gate_codes(result)
        assert result["dispatch_executed"] is False


def test_action_scope_mismatch_secret_payload_runtime_flags_and_domains_operativo_are_blocked():
    action_mismatch = _materialize_request()
    action_mismatch["action"] = "execute_materialization"
    result = validate_confirmation_gate(
        {
            "request_envelope": action_mismatch,
            "gate_options": {"allow_controlled_write": True},
        }
    )
    assert result["confirmation_gate_passed"] is False
    assert "INVALID_CONFIRMATION_SCOPE" in _gate_codes(result)

    secret_payload = _materialize_request(access_token="blocked")
    result = validate_confirmation_gate(
        {
            "request_envelope": secret_payload,
            "gate_options": {"allow_controlled_write": True},
        }
    )
    assert result["confirmation_gate_passed"] is False
    assert "SECRET_LIKE_FIELD_BLOCKED" in _gate_codes(result)

    runtime_payload = _materialize_request(
        runtime_enabled=True,
        execution_enabled=True,
        tools_enabled=True,
        models_enabled=True,
        integrations_enabled=True,
    )
    result = validate_confirmation_gate(
        {
            "request_envelope": runtime_payload,
            "gate_options": {"allow_controlled_write": True},
        }
    )
    assert result["confirmation_gate_passed"] is False
    assert {
        "RUNTIME_BLOCKED",
        "EXECUTION_BLOCKED",
        "TOOLS_BLOCKED",
        "MODELS_BLOCKED",
        "INTEGRATIONS_BLOCKED",
    } <= _gate_codes(result)

    domains_payload = _materialize_request(target_path="domains/production_domain")
    result = validate_confirmation_gate(
        {
            "request_envelope": domains_payload,
            "gate_options": {"allow_controlled_write": True},
        }
    )
    assert result["confirmation_gate_passed"] is False
    assert "OPERATIONAL_DOMAINS_BLOCKED" in _gate_codes(result)


def test_confirmation_scope_helpers_and_error_builder_are_stable():
    confirmation = _valid_confirmation("materialize_sandbox")

    assert is_confirmation_required_for_service("materialize_sandbox") is True
    assert is_confirmation_required_for_service("stable_ui_payloads") is False
    assert get_required_confirmation_scope("materialize_sandbox") == "materialize_sandbox"
    assert get_required_confirmation_scope("stable_ui_payloads") == ""
    assert validate_confirmation_scope(confirmation, "materialize_sandbox") is True
    assert validate_confirmation_scope(confirmation, "rollback_sandbox") is False

    error = build_confirmation_gate_error("UNKNOWN_CODE", "message", "field")
    assert error["code"] == "INVALID_CONFIRMATION_GATE_REQUEST"
    assert error["message"] == "message"
    assert error["field"] == "field"


def test_runtime_execution_tools_models_integrations_stay_blocked_even_when_requested():
    result = validate_confirmation_gate(
        {
            "request_envelope": _materialize_request(),
            "gate_options": {
                "allow_controlled_write": True,
                "allow_runtime": True,
                "allow_execution": True,
                "allow_tools": True,
                "allow_models": True,
                "allow_integrations": True,
            },
        }
    )

    assert result["confirmation_gate_passed"] is False
    assert {
        "RUNTIME_BLOCKED",
        "EXECUTION_BLOCKED",
        "TOOLS_BLOCKED",
        "MODELS_BLOCKED",
        "INTEGRATIONS_BLOCKED",
    } <= _gate_codes(result)
    assert result["runtime_enabled"] is False
    assert result["execution_enabled"] is False
    assert result["tools_enabled"] is False
    assert result["models_enabled"] is False
    assert result["integrations_enabled"] is False


def test_dispatcher_invokes_confirmation_gate_without_executing_controlled_services():
    passed = dispatch_internal_request(
        {
            "request_envelope": _materialize_request(),
            "dispatch_options": {"allow_controlled_write": True},
        }
    )

    assert passed["status"] == "gate_passed"
    assert passed["dispatch_allowed"] is True
    assert passed["dispatch_executed"] is False
    assert passed["blocked_by_policy"] is False
    assert passed["requires_confirmation_gate"] is False
    assert passed["confirmation_gate_passed"] is True
    assert passed["ready_for_controlled_execution_adapter"] is False
    assert passed["confirmation_gate_result"]["confirmation_gate_passed"] is True
    assert passed["flags"]["side_effects_performed"] is False
    assert passed["flags"]["agents_executed"] is False
    assert passed["flags"]["models_invoked"] is False
    assert passed["flags"]["tools_called"] is False
    assert passed["flags"]["domains_operativo_touched"] is False

    blocked = dispatch_internal_request({"request_envelope": _materialize_request()})
    assert blocked["dispatch_allowed"] is False
    assert blocked["dispatch_executed"] is False
    assert blocked["requires_confirmation_gate"] is True
    assert blocked["confirmation_gate_passed"] is False

    lifecycle = dispatch_internal_request(
        {
            "request_envelope": _lifecycle_request("rollback_sandbox"),
            "dispatch_options": {"allow_lifecycle": True},
        }
    )
    assert lifecycle["status"] == "gate_passed"
    assert lifecycle["dispatch_allowed"] is True
    assert lifecycle["dispatch_executed"] is False
    assert lifecycle["confirmation_gate_passed"] is True
    assert lifecycle["flags"]["side_effects_performed"] is False
    assert lifecycle["flags"]["agents_executed"] is False
    assert lifecycle["flags"]["models_invoked"] is False
    assert lifecycle["flags"]["tools_called"] is False


def test_ui_contract_marks_confirmation_gate_and_response_adapter_available():
    contract = build_backend_internal_ui_contract()
    assert validate_backend_internal_ui_contract(contract) == contract
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    gate = available["internal_confirmation_gate"]
    assert gate["available_now"] is True
    assert gate["phase"] == "8.4"
    assert gate["type"] == "contract/confirmation-gate"
    assert gate["side_effects"] is False
    assert gate["side_effects_performed"] is False
    assert gate["service_execution_enabled"] is False
    assert gate["public_endpoint"] is False
    assert gate["runtime_enabled"] is False
    assert gate["execution_enabled"] is False
    assert gate["requires_human_confirmation"] is False
    assert available["confirmation_gate_validation"]["type"] == "contract/confirmation-gate-validation"
    assert available["internal_response_adapter"]["phase"] == "8.5"
    assert available["internal_response_adapter"]["available_now"] is True
    assert available["internal_response_adapter"]["type"] == "contract/response-adapter"
    assert available["internal_response_adapter"]["service_execution_enabled"] is False
    assert available["stable_response_adapter"]["phase"] == "8.5"
    assert available["stable_response_adapter"]["available_now"] is True
    assert planned["exposure_audit_checkpoint"]["phase"] == "8.6"
    assert planned["exposure_audit_checkpoint"]["available_now"] is False


def test_docs_plans_book_and_adr_record_prompt_8_4():
    for path in (DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_CONFIRMATION_GATE_READY",
        "BACKEND_INTERNAL_CONFIRMATION_GATE_NO_EXECUTION_CONFIRMED",
        "BACKEND_INTERNAL_CONFIRMATION_GATE_NO_OPERATIONAL_CONFIRMED",
        "backend_internal_confirmation_gate_result.v1",
        "ready_for_phase_8_5_internal_response_adapter",
        "PROMPT 8.5 - Internal response adapter usando stable_ui_payloads",
        "No runtime",
        "No execution",
        "No UI",
        "No integrations",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle",
        "BACKEND_INTERNAL_CONFIRMATION_GATE_READY",
        "ready_for_phase_8_5_internal_response_adapter",
        "PROMPT 8.5 - Internal response adapter usando stable_ui_payloads",
    ):
        assert token in combined


def test_prompt_8_4_does_not_create_runtime_ui_or_endpoint_modules():
    for relative in FORBIDDEN_RUNTIME_FILES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
