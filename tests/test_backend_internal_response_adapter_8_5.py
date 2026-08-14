import json
from pathlib import Path

from core.backend_internal_confirmation_gate import validate_confirmation_gate
from core.backend_internal_dispatcher import dispatch_internal_request, validate_dispatch_policy
from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    GLOBAL_FORBIDDEN_ACTIONS,
    build_internal_exposure_registry,
)
from core.backend_internal_request_envelope import (
    build_internal_request_envelope,
    validate_internal_request_envelope,
)
from core.backend_internal_response_adapter import (
    ADAPTER_READINESS,
    ALLOWED_SOURCE_SCHEMAS,
    CONFIRMATION_GATE_SCHEMA_VERSION,
    DISPATCH_POLICY_SCHEMA_VERSION,
    DISPATCH_SCHEMA_VERSION,
    REGISTRY_SCHEMA_VERSION,
    REQUEST_VALIDATION_SCHEMA_VERSION,
    UI_PAYLOAD_SCHEMA_VERSION,
    adapt_confirmation_gate_result,
    adapt_dispatch_policy_result,
    adapt_dispatch_result,
    adapt_internal_response_to_ui_payload,
    adapt_registry_response,
    adapt_request_validation_response,
    adapt_stable_ui_payload_response,
    build_response_adapter_error,
    validate_adapted_internal_response,
)
from core.backend_internal_ui_contract import (
    build_backend_internal_ui_contract,
    validate_backend_internal_ui_contract,
)
from core.backend_internal_ui_payloads import build_backend_internal_ui_payload


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BACKEND_INTERNAL_RESPONSE_ADAPTER_8_5.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MEMORY = ROOT / "memoria_agentes"

FORBIDDEN_OPERATIONAL_FILES = (
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
        "confirmation_id": f"confirm_{service_id}_8_5",
    }


def _contract_request(service_id: str = "stable_ui_payloads") -> dict:
    payload = {"payload": {"status": "ready"}}
    if service_id == "internal_request_validation":
        payload = {
            "request_envelope": build_internal_request_envelope(
                request_id="nested_8_5",
                service_id="stable_ui_payloads",
                caller_kind="internal_test",
                payload={"payload": {"status": "ready"}},
            )
        }
    return build_internal_request_envelope(
        request_id=f"req_{service_id}_8_5",
        service_id=service_id,
        caller_kind="internal_test",
        payload=payload,
    )


def _materialize_request() -> dict:
    return build_internal_request_envelope(
        request_id="req_materialize_8_5",
        service_id="materialize_sandbox",
        caller_kind="internal_test",
        payload={
            "sandbox_root": _safe_root(),
            "preview_payload": {"preview_id": "preview_8_5", "planned_artifacts": ["domain.json"]},
        },
        confirmation=_valid_confirmation("materialize_sandbox"),
    )


def _assert_stable_payload(payload: dict) -> dict:
    validated = validate_adapted_internal_response(payload)
    assert validated["schema_version"] == "backend_internal_ui_payload.v1"
    assert json.loads(json.dumps(validated, ensure_ascii=False, sort_keys=True)) == validated
    assert all(value is False for value in validated["flags"].values())
    assert validated["flags"]["runtime_enabled"] is False
    assert validated["flags"]["execution_enabled"] is False
    assert validated["flags"]["tools_enabled"] is False
    assert validated["flags"]["models_enabled"] is False
    assert validated["flags"]["integrations_enabled"] is False
    assert validated["flags"]["ui_visual"] is False
    assert validated["flags"]["public_endpoint"] is False
    assert set(validated["blocked_capabilities"]) == set(GLOBAL_BLOCKED_CAPABILITIES)
    assert all(value is True for value in validated["blocked_capabilities"].values())
    assert {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"} <= {
        action["action"] for action in validated["forbidden_actions"]
    }
    return validated


def _codes(payload: dict) -> set[str]:
    return {error["code"] for error in payload["errors"]}


def test_response_adapter_module_functions_and_allowed_schemas_exist():
    assert callable(adapt_internal_response_to_ui_payload)
    assert callable(adapt_registry_response)
    assert callable(adapt_request_validation_response)
    assert callable(adapt_dispatch_result)
    assert callable(adapt_confirmation_gate_result)
    assert callable(adapt_dispatch_policy_result)
    assert callable(adapt_stable_ui_payload_response)
    assert callable(validate_adapted_internal_response)
    assert callable(build_response_adapter_error)
    assert {
        REGISTRY_SCHEMA_VERSION,
        REQUEST_VALIDATION_SCHEMA_VERSION,
        DISPATCH_SCHEMA_VERSION,
        DISPATCH_POLICY_SCHEMA_VERSION,
        CONFIRMATION_GATE_SCHEMA_VERSION,
        UI_PAYLOAD_SCHEMA_VERSION,
    } <= set(ALLOWED_SOURCE_SCHEMAS)


def test_registry_response_is_adapted_to_stable_ui_payload():
    registry = build_internal_exposure_registry()
    payload = adapt_registry_response(registry)
    validated = _assert_stable_payload(payload)

    assert validated["service"] == "internal_exposure_registry"
    assert validated["service_kind"] == "contract"
    assert validated["readiness"] == registry["readiness"]
    assert validated["summary"]["exposable_services_count"] == len(registry["exposable_services"])
    assert validated["summary"]["blocked_services_count"] == len(registry["blocked_services"])
    assert validated["data"]["registry"]["schema_version"] == REGISTRY_SCHEMA_VERSION
    assert validated["blocked_capabilities"] == GLOBAL_BLOCKED_CAPABILITIES


def test_request_validation_response_is_adapted_to_stable_ui_payload():
    validation = validate_internal_request_envelope(_contract_request("stable_ui_payloads"))
    payload = adapt_request_validation_response(validation)
    validated = _assert_stable_payload(payload)

    assert validated["service"] == "stable_ui_payloads"
    assert validated["status"] == "ready"
    assert validated["validation"]["valid"] is True
    assert validated["data"]["request"]["service_id"] == "stable_ui_payloads"
    assert validated["meta"]["dispatcher_created"] is False
    assert validated["meta"]["request_handling_enabled"] is False


def test_dispatch_result_and_policy_are_adapted_without_extra_dispatch():
    request = _contract_request("internal_exposure_registry")
    dispatch = dispatch_internal_request({"request_envelope": request})
    payload = adapt_dispatch_result(dispatch)
    validated = _assert_stable_payload(payload)

    assert dispatch["dispatch_allowed"] is True
    assert dispatch["dispatch_executed"] is True
    assert validated["service"] == "internal_dispatcher_no_runtime"
    assert validated["validation"]["dispatch_allowed"] is True
    assert validated["validation"]["dispatch_executed"] is True
    assert validated["data"]["target_service_id"] == "internal_exposure_registry"
    assert validated["data"]["response_payload"]["schema_version"] == REGISTRY_SCHEMA_VERSION
    assert validated["meta"]["adapter_dispatched_request"] is False
    assert validated["meta"]["adapter_executed_service"] is False

    policy = validate_dispatch_policy(request)
    policy_payload = adapt_internal_response_to_ui_payload(
        {
            "source_result": policy,
            "source_schema_version": DISPATCH_POLICY_SCHEMA_VERSION,
            "source_service": "internal_dispatch_policy",
        }
    )
    policy_validated = _assert_stable_payload(policy_payload)
    assert policy_validated["service"] == "internal_dispatch_policy"
    assert policy_validated["validation"]["dispatch_allowed"] is True


def test_confirmation_gate_result_is_adapted_without_invoking_gate_as_execution():
    gate_result = validate_confirmation_gate(
        {
            "request_envelope": _materialize_request(),
            "gate_options": {"allow_controlled_write": True},
        }
    )
    payload = adapt_confirmation_gate_result(gate_result)
    validated = _assert_stable_payload(payload)

    assert gate_result["confirmation_gate_passed"] is True
    assert gate_result["dispatch_executed"] is False
    assert validated["service"] == "internal_confirmation_gate"
    assert validated["validation"]["confirmation_gate_passed"] is True
    assert validated["validation"]["payload_requirements"]["requires_preview_payload"] is True
    assert validated["validation"]["payload_requirements"]["preview_payload_present"] is True
    assert validated["summary"]["dispatch_executed"] is False
    assert validated["summary"]["side_effects_performed"] is False
    assert validated["meta"]["adapter_invoked_confirmation_gate"] is False
    assert validated["meta"]["service_execution_not_performed"] is True


def test_adapter_supports_wrapper_input_and_existing_stable_ui_payloads():
    registry_payload = adapt_internal_response_to_ui_payload(
        {
            "source_result": build_internal_exposure_registry(),
            "source_schema_version": REGISTRY_SCHEMA_VERSION,
            "source_service": "internal_exposure_registry",
            "adapter_options": {"include_raw_payload": True, "sanitize_errors": True},
        }
    )
    assert _assert_stable_payload(registry_payload)["service"] == "internal_exposure_registry"

    stable = build_backend_internal_ui_payload(
        service="stable_ui_payloads",
        service_kind="contract",
        status="ready",
        readiness=ADAPTER_READINESS,
        data={"already_stable": True},
        forbidden_actions=list(GLOBAL_FORBIDDEN_ACTIONS),
        blocked_capabilities=GLOBAL_BLOCKED_CAPABILITIES,
    )
    assert adapt_internal_response_to_ui_payload(stable) == stable


def test_unknown_non_json_safe_secret_traceback_and_path_sources_fail_controlled():
    unknown = adapt_internal_response_to_ui_payload({"schema_version": "unknown.v1", "status": "ready"})
    assert unknown["status"] == "invalid"
    assert "UNKNOWN_SOURCE_SCHEMA" in _codes(unknown)

    non_json = adapt_internal_response_to_ui_payload({"schema_version": REGISTRY_SCHEMA_VERSION, "callable": object()})
    assert non_json["status"] == "invalid"
    assert "SOURCE_PAYLOAD_NOT_JSON_SAFE" in _codes(non_json)

    secret = adapt_internal_response_to_ui_payload({"schema_version": REGISTRY_SCHEMA_VERSION, "api_key": "blocked"})
    assert secret["status"] == "invalid"
    assert "SECRET_LIKE_FIELD_BLOCKED" in _codes(secret)

    traceback = adapt_internal_response_to_ui_payload(
        {"schema_version": REGISTRY_SCHEMA_VERSION, "errors": [{"message": "Traceback (most recent call last): File x"}]}
    )
    assert traceback["status"] == "invalid"
    assert "TRACEBACK_BLOCKED" in _codes(traceback)

    path = adapt_internal_response_to_ui_payload({"schema_version": REGISTRY_SCHEMA_VERSION, "path": "C:\\IA_CORE\\domains\\real"})
    assert path["status"] == "invalid"
    assert "SENSITIVE_PATH_BLOCKED" in _codes(path)

    for payload in (unknown, non_json, secret, traceback, path):
        validated = _assert_stable_payload(payload)
        assert validated["readiness"] == ADAPTER_READINESS


def test_adapter_normalizes_errors_warnings_and_forbidden_actions():
    payload = adapt_dispatch_policy_result(
        {
            "dispatch_allowed": False,
            "requires_confirmation_gate": True,
            "target_service_id": "materialize_sandbox",
            "target_service_kind": "controlled_write",
            "errors": [{"error_code": "DISPATCH_POLICY_BLOCKED", "message": "blocked", "field": "service_id"}],
            "warnings": ["policy warning"],
            "forbidden_actions": list(GLOBAL_FORBIDDEN_ACTIONS),
            "blocked_capabilities": dict(GLOBAL_BLOCKED_CAPABILITIES),
        }
    )
    validated = _assert_stable_payload(payload)

    assert validated["status"] == "blocked"
    assert validated["errors"][0]["code"] == "DISPATCH_POLICY_BLOCKED"
    assert validated["errors"][0]["severity"] == "error"
    assert validated["errors"][0]["sensitive"] is False
    assert validated["warnings"][0]["severity"] == "warning"
    assert validated["warnings"][0]["sensitive"] is False
    assert all(action["available_now"] is False for action in validated["forbidden_actions"])


def test_adapter_does_not_import_or_create_operational_execution_boundaries():
    source = (ROOT / "core" / "backend_internal_response_adapter.py").read_text(encoding="utf-8")
    forbidden_source_tokens = (
        "from core.backend_internal_materialize_sandbox_service",
        "from core.backend_internal_domain_lifecycle_service",
        "from core.backend_internal_dispatcher import dispatch_internal_request",
        "from core.backend_internal_confirmation_gate import validate_confirmation_gate",
        "requests.",
        "subprocess",
        "open(",
        "Path.write_text",
        "Path.unlink",
    )
    for token in forbidden_source_tokens:
        assert token not in source

    assert (ROOT / "domains").exists()
    for relative in FORBIDDEN_OPERATIONAL_FILES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()


def test_ui_contract_marks_response_adapters_available_and_future_execution_ui_endpoints_planned_only():
    contract = build_backend_internal_ui_contract()
    assert validate_backend_internal_ui_contract(contract) == contract
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    for name in ("internal_response_adapter", "stable_response_adapter"):
        service = available[name]
        assert service["available_now"] is True
        assert service["phase"] == "8.5"
        assert service["type"] == "contract/response-adapter"
        assert service["side_effects"] is False
        assert service["service_execution_enabled"] is False
        assert service["dispatcher_created"] is False
        assert service["request_handling_enabled"] is False
        assert service["public_endpoint"] is False
        assert service["touches_visual_ui"] is False
        assert service["runtime_enabled"] is False
        assert service["execution_enabled"] is False

    assert planned["exposure_audit_checkpoint"]["available_now"] is False
    assert planned["exposure_audit_checkpoint"]["phase"] == "8.6"
    unavailable_names = {"controlled_execution_adapter", "backend_internal_ui", "public_endpoint", "ui_runtime"}
    assert not unavailable_names & set(available)


def test_docs_plans_book_and_adr_record_prompt_8_5():
    for path in (DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_RESPONSE_ADAPTER_READY",
        "BACKEND_INTERNAL_RESPONSE_ADAPTER_STABLE_PAYLOAD_CONFIRMED",
        "BACKEND_INTERNAL_RESPONSE_ADAPTER_NO_EXECUTION_CONFIRMED",
        "BACKEND_INTERNAL_RESPONSE_ADAPTER_NO_OPERATIONAL_CONFIRMED",
        "backend_internal_ui_payload.v1",
        "backend_internal_exposure_registry.v1",
        "backend_internal_ui_request_validation.v1",
        "backend_internal_dispatch_result.v1",
        "backend_internal_confirmation_gate_result.v1",
        "ready_for_phase_8_6_exposure_audit_checkpoint",
        "PROMPT 8.6 - Exposure audit checkpoint",
        "No runtime",
        "No execution",
        "No UI visual",
        "No endpoints publicos",
        "No integrations",
        "`domains/` operativo",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.5 - Internal response adapter usando stable_ui_payloads",
        "BACKEND_INTERNAL_RESPONSE_ADAPTER_READY",
        "ready_for_phase_8_6_exposure_audit_checkpoint",
        "internal_response_adapter",
        "stable_response_adapter",
        "PROMPT 8.6 - Exposure audit checkpoint",
        "no endpoints publicos",
        "no UI visual",
        "no runtime/execution/tools/models/integrations",
        "`domains/` operativo",
    ):
        assert token in combined
