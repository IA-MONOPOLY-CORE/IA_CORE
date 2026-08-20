import json
from pathlib import Path

from core.backend_internal_confirmation_gate import validate_confirmation_gate
from core.backend_internal_dispatcher import dispatch_internal_request
from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    build_internal_exposure_registry,
)
from core.backend_internal_request_envelope import (
    build_internal_request_envelope,
    validate_internal_request_envelope,
)
from core.backend_internal_response_adapter import (
    adapt_confirmation_gate_result,
    adapt_dispatch_result,
    adapt_internal_response_to_ui_payload,
    adapt_registry_response,
    adapt_request_validation_response,
)
from core.backend_internal_ui_contract import (
    build_backend_internal_ui_contract,
    validate_backend_internal_ui_contract,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BACKEND_INTERNAL_EXPOSURE_AUDIT_CHECKPOINT_8_6.md"
PLAN_8_0 = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md"
DOC_8_1 = ROOT / "docs" / "BACKEND_INTERNAL_EXPOSURE_REGISTRY_8_1.md"
DOC_8_2 = ROOT / "docs" / "BACKEND_INTERNAL_REQUEST_ENVELOPE_8_2.md"
DOC_8_3 = ROOT / "docs" / "BACKEND_INTERNAL_DISPATCHER_8_3.md"
DOC_8_4 = ROOT / "docs" / "BACKEND_INTERNAL_CONFIRMATION_GATE_8_4.md"
DOC_8_5 = ROOT / "docs" / "BACKEND_INTERNAL_RESPONSE_ADAPTER_8_5.md"
DOC_7_6 = ROOT / "docs" / "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6.md"
DOC_7_7 = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_CHECKPOINT_7_7.md"
DOC_7_0 = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MEMORY = ROOT / "memoria_agentes"
DOMAINS = ROOT / "domains"

MODULES_8_1_TO_8_5 = (
    ROOT / "core" / "backend_internal_exposure_registry.py",
    ROOT / "core" / "backend_internal_request_envelope.py",
    ROOT / "core" / "backend_internal_dispatcher.py",
    ROOT / "core" / "backend_internal_confirmation_gate.py",
    ROOT / "core" / "backend_internal_response_adapter.py",
)

TESTS_8_1_TO_8_5 = (
    ROOT / "tests" / "test_backend_internal_exposure_registry_8_1.py",
    ROOT / "tests" / "test_backend_internal_request_envelope_8_2.py",
    ROOT / "tests" / "test_backend_internal_dispatcher_8_3.py",
    ROOT / "tests" / "test_backend_internal_confirmation_gate_8_4.py",
    ROOT / "tests" / "test_backend_internal_response_adapter_8_5.py",
)

FORBIDDEN_OPERATIONAL_FILES = (
    "core/backend_internal_controlled_execution_adapter.py",
    "core/backend_internal_public_endpoint.py",
    "core/backend_internal_private_http_endpoint.py",
    "core/backend_internal_ui_router.py",
    "core/backend_internal_ui_api.py",
    "core/backend_ui_endpoint.py",
    "core/backend_ui_api.py",
    "core/ui_runtime.py",
    "core/frontend_runtime.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_dispatcher.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/context_injection_runtime.py",
    "core/output_delivery_runtime.py",
    "core/integration_runtime.py",
)

AVAILABLE_NOW = {
    "list_domains_status",
    "preview_materialization",
    "materialize_sandbox",
    "validate_domain",
    "rollback_sandbox",
    "archive_sandbox_domain",
    "delete_sandbox_domain",
    "reset_sandbox_domain",
    "stable_ui_payloads",
    "internal_exposure_registry",
    "internal_request_envelope",
    "internal_request_validation",
    "internal_dispatcher_no_runtime",
    "internal_dispatch_policy",
    "internal_confirmation_gate",
    "confirmation_gate_validation",
    "internal_response_adapter",
    "stable_response_adapter",
}

PLANNED_OR_BLOCKED = {
    "controlled_execution_adapter",
    "public_endpoints",
    "ui_visual_runtime",
    "runtime_execution",
    "agent_execution",
    "model_invocation",
    "tool_invocation",
    "external_integrations",
    "network_browser_automation",
    "market_catalog_runtime",
    "business_composition_layer_runtime",
    "obliteratus",
    "raw_package_direct_to_user_panel",
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _safe_root() -> dict:
    return {"declared": True, "root_kind": "controlled_sandbox", "path_policy": "manifest_bound"}


def _confirmation(service_id: str) -> dict:
    return {
        "confirmed": True,
        "confirmation_scope": service_id,
        "human_confirmation_required": True,
        "confirmed_by": "internal_test",
        "confirmation_id": f"confirm_{service_id}_8_6",
    }


def _request(service_id: str = "stable_ui_payloads", payload: dict | None = None) -> dict:
    return build_internal_request_envelope(
        request_id=f"req_{service_id}_8_6",
        service_id=service_id,
        caller_kind="internal_test",
        payload=payload or {"payload": {"status": "ready"}},
    )


def _materialize_request() -> dict:
    return build_internal_request_envelope(
        request_id="req_materialize_8_6",
        service_id="materialize_sandbox",
        caller_kind="internal_test",
        payload={
            "sandbox_root": _safe_root(),
            "preview_payload": {"preview_id": "preview_8_6", "planned_artifacts": ["domain.json"]},
        },
        confirmation=_confirmation("materialize_sandbox"),
    )


def _assert_stable_non_operational_payload(payload: dict) -> dict:
    assert payload["schema_version"] == "backend_internal_ui_payload.v1"
    assert json.loads(json.dumps(payload, ensure_ascii=False, sort_keys=True)) == payload
    assert all(value is False for value in payload["flags"].values())
    assert payload["flags"]["runtime_enabled"] is False
    assert payload["flags"]["execution_enabled"] is False
    assert payload["flags"]["tools_enabled"] is False
    assert payload["flags"]["models_enabled"] is False
    assert payload["flags"]["integrations_enabled"] is False
    assert payload["flags"]["ui_visual"] is False
    assert payload["flags"]["public_endpoint"] is False
    assert payload["blocked_capabilities"] == GLOBAL_BLOCKED_CAPABILITIES
    assert all(value is True for value in payload["blocked_capabilities"].values())
    return payload


def test_checkpoint_document_exists_and_records_required_verdicts():
    assert DOC.exists()
    text = _text(DOC)

    for token in (
        "PROMPT 8.6 - Exposure audit checkpoint",
        "BACKEND_INTERNAL_EXPOSURE_AUDIT_CHECKPOINT_PASSED",
        "BACKEND_INTERNAL_EXPOSURE_CHAIN_CONFIRMED",
        "BACKEND_INTERNAL_EXPOSURE_NO_OPERATIONAL_CONFIRMED",
        "BACKEND_INTERNAL_EXPOSURE_READY_FOR_NEXT_BLOCK",
        "ready_for_phase_8_7_future_ui_contract_plan",
        "PROMPT 8.7 - Plan de futura UI visual sobre contrato estable",
    ):
        assert token in text


def test_modules_docs_and_focal_tests_for_8_1_to_8_5_exist():
    for path in (
        PLAN_8_0,
        DOC_8_1,
        DOC_8_2,
        DOC_8_3,
        DOC_8_4,
        DOC_8_5,
        DOC_7_6,
        DOC_7_7,
        DOC_7_0,
        *MODULES_8_1_TO_8_5,
        *TESTS_8_1_TO_8_5,
    ):
        assert path.exists(), str(path)


def test_registry_request_dispatch_gate_adapter_chain_is_real_and_json_safe():
    registry = build_internal_exposure_registry()
    registry_payload = _assert_stable_non_operational_payload(adapt_registry_response(registry))
    assert registry_payload["service"] == "internal_exposure_registry"

    validation = validate_internal_request_envelope(_request("stable_ui_payloads"))
    assert validation["valid"] is True
    validation_payload = _assert_stable_non_operational_payload(adapt_request_validation_response(validation))
    assert validation_payload["service"] == "stable_ui_payloads"

    dispatch = dispatch_internal_request({"request_envelope": _request("internal_exposure_registry")})
    dispatch_payload = _assert_stable_non_operational_payload(adapt_dispatch_result(dispatch))
    assert dispatch["dispatch_allowed"] is True
    assert dispatch["dispatch_executed"] is True
    assert dispatch_payload["meta"]["adapter_dispatched_request"] is False
    assert dispatch_payload["meta"]["adapter_executed_service"] is False

    gate = validate_confirmation_gate(
        {
            "request_envelope": _materialize_request(),
            "gate_options": {"allow_controlled_write": True},
        }
    )
    assert gate["confirmation_gate_passed"] is True
    assert gate["dispatch_executed"] is False
    gate_payload = _assert_stable_non_operational_payload(adapt_confirmation_gate_result(gate))
    assert gate_payload["summary"]["side_effects_performed"] is False
    assert gate_payload["meta"]["service_execution_not_performed"] is True

    wrapped = adapt_internal_response_to_ui_payload(
        {
            "source_result": registry,
            "source_schema_version": "backend_internal_exposure_registry.v1",
            "source_service": "internal_exposure_registry",
        }
    )
    _assert_stable_non_operational_payload(wrapped)


def test_contract_available_now_and_planned_services_are_coherent():
    contract = build_backend_internal_ui_contract()
    validate_backend_internal_ui_contract(contract)

    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert AVAILABLE_NOW <= set(available)
    for name in AVAILABLE_NOW:
        service = available[name]
        assert service["available_now"] is True
        assert service["runtime_enabled"] is False
        assert service["execution_enabled"] is False
        assert service["touches_integrations"] is False
        assert service["public_endpoint"] is False
        assert service["touches_visual_ui"] is False
        assert service["touches_operational_domains"] is False

    assert planned["exposure_audit_checkpoint"]["available_now"] is False
    assert "controlled_execution_adapter" not in available
    assert not PLANNED_OR_BLOCKED & set(available)


def test_registry_declares_exposable_and_blocked_services():
    registry = build_internal_exposure_registry()
    exposable = {service["service_id"]: service for service in registry["exposable_services"]}
    blocked = {service["service_id"]: service for service in registry["blocked_services"]}

    assert {
        "list_domains_status",
        "preview_materialization",
        "materialize_sandbox",
        "validate_domain",
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
        "stable_ui_payloads",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
    } <= set(exposable)
    assert {
        "runtime_execution",
        "agent_execution",
        "model_invocation",
        "tool_invocation",
        "external_integrations",
        "public_endpoints",
        "ui_visual_runtime",
        "market_catalog_runtime",
        "business_composition_layer_runtime",
        "obliteratus",
        "domains_operativo",
    } <= set(blocked)
    assert registry["global_blocked_capabilities"] == GLOBAL_BLOCKED_CAPABILITIES


def test_request_validation_blocks_blocked_services_and_operational_flags():
    blocked_request = _request("runtime_execution")
    result = validate_internal_request_envelope(blocked_request)
    assert result["valid"] is False
    assert {error["error_code"] for error in result["errors"]} & {"SERVICE_BLOCKED", "RUNTIME_REQUEST_BLOCKED"}

    unsafe = _request(
        "stable_ui_payloads",
        payload={
            "payload": {"status": "ready"},
            "runtime_enabled": True,
            "execution_enabled": True,
            "tools_enabled": True,
            "models_enabled": True,
            "integrations_enabled": True,
            "touches_operational_domains": True,
        },
    )
    unsafe_result = validate_internal_request_envelope(unsafe)
    assert unsafe_result["valid"] is False
    codes = {error["error_code"] for error in unsafe_result["errors"]}
    assert {
        "RUNTIME_REQUEST_BLOCKED",
        "EXECUTION_REQUEST_BLOCKED",
        "TOOLS_REQUEST_BLOCKED",
        "MODELS_REQUEST_BLOCKED",
        "INTEGRATIONS_REQUEST_BLOCKED",
        "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
    } <= codes


def test_dispatcher_blocks_controlled_write_and_lifecycle_by_default():
    materialize = dispatch_internal_request({"request_envelope": _materialize_request()})
    assert materialize["dispatch_allowed"] is False
    assert materialize["dispatch_executed"] is False
    assert materialize["blocked_by_policy"] is True
    assert materialize["requires_confirmation_gate"] is True

    rollback = build_internal_request_envelope(
        request_id="req_rollback_8_6",
        service_id="rollback_sandbox",
        caller_kind="internal_test",
        payload={
            "sandbox_root": _safe_root(),
            "validation_payload": {"rollback_ready": True, "domain_id": "demo"},
        },
        confirmation=_confirmation("rollback_sandbox"),
    )
    lifecycle = dispatch_internal_request({"request_envelope": rollback})
    assert lifecycle["dispatch_allowed"] is False
    assert lifecycle["dispatch_executed"] is False
    assert lifecycle["requires_confirmation_gate"] is True


def test_docs_and_plans_record_8_6_without_opening_runtime_or_ui():
    for path in (DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK):
        assert path.exists()

    combined = "\n".join(_text(path) for path in (DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "PROMPT 8.6 - Exposure audit checkpoint",
        "BACKEND_INTERNAL_EXPOSURE_AUDIT_CHECKPOINT_PASSED",
        "BACKEND_INTERNAL_EXPOSURE_CHAIN_CONFIRMED",
        "BACKEND_INTERNAL_EXPOSURE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_8_7_future_ui_contract_plan",
        "PROMPT 8.7 - Plan de futura UI visual sobre contrato estable",
        "no runtime",
        "no execution",
        "no UI visual",
        "no endpoints publicos",
        "no API/router HTTP",
        "no tools/modelos/integraciones",
        "`domains/` operativo",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
    ):
        assert token in combined


def test_checkpoint_references_adrs_and_prior_docs():
    text = _text(DOC)
    for token in (
        "ADR-059",
        "ADR-060",
        "ADR-061",
        "ADR-062",
        "ADR-063",
        "ADR-064",
        "docs/BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md",
        "docs/BACKEND_INTERNAL_EXPOSURE_REGISTRY_8_1.md",
        "docs/BACKEND_INTERNAL_REQUEST_ENVELOPE_8_2.md",
        "docs/BACKEND_INTERNAL_DISPATCHER_8_3.md",
        "docs/BACKEND_INTERNAL_CONFIRMATION_GATE_8_4.md",
        "docs/BACKEND_INTERNAL_RESPONSE_ADAPTER_8_5.md",
    ):
        assert token in text

    adr_text = _text(ADR)
    for token in ("ADR-059", "ADR-060", "ADR-061", "ADR-062", "ADR-063", "ADR-064"):
        assert token in adr_text


def test_no_operational_runtime_endpoint_ui_integration_or_temp_artifacts_created():
    for relative in FORBIDDEN_OPERATIONAL_FILES:
        assert not (ROOT / relative).exists(), relative

    assert DOMAINS.exists()
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
