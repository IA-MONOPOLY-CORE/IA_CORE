import json
from pathlib import Path

from core.backend_internal_dispatcher import (
    CONTROLLED_LIFECYCLE_SERVICE_IDS,
    CONTROLLED_WRITE_SERVICE_IDS,
    DISPATCH_READINESS,
    DISPATCH_SCHEMA_VERSION,
    DISPATCHABLE_SERVICE_IDS,
    build_internal_dispatch_error,
    build_internal_dispatch_result,
    dispatch_internal_request,
    is_service_blocked_by_dispatch_policy,
    is_service_dispatchable_now,
    validate_dispatch_policy,
)
from core.backend_internal_exposure_registry import build_internal_exposure_registry, validate_internal_exposure_registry
from core.backend_internal_request_envelope import build_internal_request_envelope, validate_internal_request_envelope
from core.backend_internal_ui_contract import build_backend_internal_ui_contract, validate_backend_internal_ui_contract
from core.backend_internal_ui_payloads import validate_backend_internal_ui_payload


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_DISPATCHER_8_3.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"

FORBIDDEN_FILES = (
    "core/backend_internal_confirmation_gate.py",
    "core/backend_internal_response_adapter.py",
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
        "confirmation_id": f"confirm_{service_id}_8_3",
    }


def _dispatchable_request(service_id: str) -> dict:
    payload = {"payload": {"status": "ready"}}
    if service_id == "internal_request_validation":
        payload = {
            "request_envelope": build_internal_request_envelope(
                request_id="nested_request_validation",
                service_id="stable_ui_payloads",
                caller_kind="internal_test",
                payload={"payload": {"status": "ready"}},
            )
        }
    return build_internal_request_envelope(
        request_id=f"req_{service_id}",
        service_id=service_id,
        caller_kind="internal_test",
        payload=payload,
    )


def _controlled_request(service_id: str) -> dict:
    payload = {"sandbox_root": _safe_root()}
    if service_id == "materialize_sandbox":
        payload["preview_payload"] = {"valid": True}
    else:
        payload["validation_payload"] = {"passed": True}
    if service_id == "delete_sandbox_domain":
        payload["allow_delete"] = True
    if service_id == "reset_sandbox_domain":
        payload["allow_reset"] = True
    return build_internal_request_envelope(
        request_id=f"req_{service_id}",
        service_id=service_id,
        caller_kind="internal_test",
        payload=payload,
        confirmation=_valid_confirmation(service_id),
    )


def test_dispatcher_module_policy_builders_and_result_schema_are_json_safe():
    request = _dispatchable_request("stable_ui_payloads")
    result = dispatch_internal_request({"request_envelope": request})

    assert result["schema_version"] == DISPATCH_SCHEMA_VERSION == "backend_internal_dispatch_result.v1"
    assert result["service"] == "internal_dispatcher"
    assert result["status"] == "dispatched"
    assert result["readiness"] == DISPATCH_READINESS == "ready_for_phase_8_4_confirmation_gate"
    assert result["dispatch_allowed"] is True
    assert result["dispatch_executed"] is True
    assert result["blocked_by_policy"] is False
    assert result["requires_confirmation_gate"] is False
    assert result["flags"]["runtime_enabled"] is False
    assert result["flags"]["execution_enabled"] is False
    assert result["flags"]["tools_enabled"] is False
    assert result["flags"]["models_enabled"] is False
    assert result["flags"]["integrations_enabled"] is False
    assert result["flags"]["public_endpoint"] is False
    assert result["flags"]["ui_visual"] is False
    assert result["flags"]["side_effects_performed"] is False
    assert validate_backend_internal_ui_payload(result["stable_ui_payload"]) == result["stable_ui_payload"]
    assert build_internal_dispatch_error("RUNTIME_BLOCKED", "blocked")["blocked"] is True
    assert build_internal_dispatch_result(
        request_envelope=request,
        target_service={"service_id": "stable_ui_payloads", "service_kind": "contract_payload_normalization"},
        status="blocked",
        dispatch_allowed=False,
        dispatch_executed=False,
        blocked_by_policy=True,
    )["flags"]["side_effects_performed"] is False
    json.dumps(result, ensure_ascii=False, sort_keys=True)


def test_dispatcher_validates_request_envelope_and_registry():
    registry = build_internal_exposure_registry()
    assert validate_internal_exposure_registry(registry) == registry

    request = _dispatchable_request("internal_exposure_registry")
    assert validate_internal_request_envelope(request)["valid"] is True
    result = dispatch_internal_request({"request_envelope": request})

    assert result["dispatch_allowed"] is True
    assert result["dispatch_executed"] is True
    assert result["target_service_id"] == "internal_exposure_registry"
    assert result["response_payload"]["schema_version"] == "backend_internal_exposure_registry.v1"


def test_invalid_missing_blocked_and_runtime_requests_fail_without_dispatch():
    invalid = dispatch_internal_request({"request_envelope": {}})
    assert invalid["dispatch_allowed"] is False
    assert invalid["dispatch_executed"] is False
    assert "REQUEST_VALIDATION_FAILED" in _codes(invalid)

    missing = dispatch_internal_request(
        {
            "request_envelope": build_internal_request_envelope(
                request_id="req_missing_service",
                service_id="missing_service",
                payload={},
            )
        }
    )
    assert {"REQUEST_VALIDATION_FAILED", "SERVICE_NOT_FOUND"} <= _codes(missing)

    blocked = dispatch_internal_request(
        {
            "request_envelope": build_internal_request_envelope(
                request_id="req_runtime_service",
                service_id="runtime_execution",
                payload={},
            )
        }
    )
    assert {"REQUEST_VALIDATION_FAILED", "SERVICE_BLOCKED"} <= _codes(blocked)

    runtime = _dispatchable_request("stable_ui_payloads")
    runtime["safety"]["runtime_allowed"] = True
    result = dispatch_internal_request({"request_envelope": runtime})
    assert {"REQUEST_VALIDATION_FAILED", "RUNTIME_BLOCKED"} <= _codes(result)


def test_dispatch_options_block_execution_tools_models_integrations_public_ui_and_domains():
    option_to_code = {
        "allow_runtime": "RUNTIME_BLOCKED",
        "allow_execution": "EXECUTION_BLOCKED",
        "allow_tools": "TOOLS_BLOCKED",
        "allow_models": "MODELS_BLOCKED",
        "allow_integrations": "INTEGRATIONS_BLOCKED",
        "allow_public_endpoint": "PUBLIC_ENDPOINT_BLOCKED",
        "allow_ui_runtime": "UI_RUNTIME_BLOCKED",
        "allow_operational_domains": "OPERATIONAL_DOMAINS_BLOCKED",
        "allow_side_effects": "SIDE_EFFECTS_BLOCKED",
    }
    for option, code in option_to_code.items():
        result = dispatch_internal_request(
            {
                "request_envelope": _dispatchable_request("stable_ui_payloads"),
                "dispatch_options": {option: True},
            }
        )
        assert result["dispatch_allowed"] is False
        assert result["dispatch_executed"] is False
        assert code in _codes(result)


def test_contractual_services_are_dispatchable_without_side_effects():
    for service_id in DISPATCHABLE_SERVICE_IDS:
        request = _dispatchable_request(service_id)
        policy = validate_dispatch_policy(request)
        result = dispatch_internal_request({"request_envelope": request})

        assert is_service_dispatchable_now(service_id) is True
        assert is_service_blocked_by_dispatch_policy(service_id) is False
        assert policy["dispatch_allowed"] is True
        assert result["dispatch_allowed"] is True
        assert result["dispatch_executed"] is True
        assert result["flags"]["side_effects_performed"] is False
        assert result["flags"]["agents_executed"] is False
        assert result["flags"]["models_invoked"] is False
        assert result["flags"]["tools_called"] is False
        assert result["flags"]["domains_operativo_touched"] is False


def test_controlled_write_and_lifecycle_require_confirmation_gate_and_are_not_executed():
    for service_id in (*CONTROLLED_WRITE_SERVICE_IDS, *CONTROLLED_LIFECYCLE_SERVICE_IDS):
        result = dispatch_internal_request({"request_envelope": _controlled_request(service_id)})

        assert result["dispatch_allowed"] is False
        assert result["dispatch_executed"] is False
        assert result["blocked_by_policy"] is True
        assert result["requires_confirmation_gate"] is True
        assert "CONFIRMATION_GATE_REQUIRED" in _codes(result)
        if service_id in CONTROLLED_WRITE_SERVICE_IDS:
            assert "CONTROLLED_WRITE_BLOCKED" in _codes(result)
        else:
            assert "CONTROLLED_LIFECYCLE_BLOCKED" in _codes(result)
        assert result["flags"]["side_effects_performed"] is False
        assert result["response_payload"] == {}


def test_read_only_domain_services_are_blocked_until_safe_adapters_are_defined():
    for service_id, payload in {
        "list_domains_status": {"sandbox_root": _safe_root()},
        "preview_materialization": {"sandbox_root": _safe_root(), "domain_request": {"domain_id": "demo"}},
        "validate_domain": {"sandbox_root": _safe_root(), "domain_id": "demo"},
    }.items():
        request = build_internal_request_envelope(
            request_id=f"req_{service_id}",
            service_id=service_id,
            caller_kind="internal_test",
            payload=payload,
        )
        result = dispatch_internal_request({"request_envelope": request})
        assert result["dispatch_allowed"] is False
        assert result["dispatch_executed"] is False
        assert "DISPATCH_POLICY_BLOCKED" in _codes(result)
        assert result["flags"]["side_effects_performed"] is False


def test_ui_contract_marks_dispatcher_and_policy_available_and_keeps_8_4_plus_planned():
    contract = build_backend_internal_ui_contract()
    assert validate_backend_internal_ui_contract(contract) == contract
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    dispatcher = available["internal_dispatcher_no_runtime"]
    assert dispatcher["available_now"] is True
    assert dispatcher["phase"] == "8.3"
    assert dispatcher["type"] == "contract/internal-dispatcher-no-runtime"
    assert dispatcher["dispatcher_created"] is True
    assert dispatcher["contractual_request_handling_enabled"] is True
    assert dispatcher["request_handling_enabled"] is False
    assert dispatcher["dispatch_policy_defined"] is True
    assert dispatcher["side_effects"] is False
    assert dispatcher["side_effects_performed"] is False
    assert dispatcher["public_endpoint"] is False
    assert dispatcher["runtime_enabled"] is False
    assert dispatcher["execution_enabled"] is False

    policy = available["internal_dispatch_policy"]
    assert policy["available_now"] is True
    assert policy["type"] == "contract/dispatch-policy"
    assert policy["dispatch_policy_defined"] is True
    assert policy["dispatcher_created"] is False
    assert policy["request_handling_enabled"] is False

    for name in ("confirmation_gate", "internal_response_adapter"):
        assert planned[name]["available_now"] is False
        assert planned[name]["dispatcher_created"] is False
        assert planned[name]["request_handling_enabled"] is False


def test_docs_plans_book_and_adr_record_prompt_8_3():
    for path in (DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_DISPATCHER_NO_RUNTIME_READY",
        "BACKEND_INTERNAL_DISPATCHER_NO_SIDE_EFFECTS_CONFIRMED",
        "BACKEND_INTERNAL_DISPATCHER_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_8_4_confirmation_gate",
        "PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle",
        "backend_internal_dispatch_result.v1",
        "backend_internal_ui_payload.v1",
        "Controlled-write bloqueado",
        "Controlled-lifecycle bloqueado",
        "Confirmation gate requerida",
        "No runtime",
        "No execution",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto",
        "BACKEND_INTERNAL_DISPATCHER_NO_RUNTIME_READY",
        "ready_for_phase_8_4_confirmation_gate",
        "internal_dispatcher_no_runtime",
        "internal_dispatch_policy",
        "controlled-write/lifecycle bloqueados",
        "no endpoints publicos",
        "no UI visual",
        "no runtime/execution/tools/models/integrations",
        "`domains/` operativo",
    ):
        assert token in combined


def test_no_operational_modules_ui_endpoints_domains_or_temp_artifacts_created():
    for relative in FORBIDDEN_FILES:
        assert not (ROOT / relative).exists(), relative
    assert DOMAINS.exists()
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
