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
from core.backend_internal_response_adapter import adapt_dispatch_result, adapt_registry_response
from core.backend_internal_ui_contract import (
    build_backend_internal_ui_contract,
    validate_backend_internal_ui_contract,
)
from core.backend_internal_ui_payloads import (
    build_backend_internal_ui_payload,
    validate_backend_internal_ui_payload,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BACKEND_INTERNAL_FUTURE_UI_CONTRACT_PLAN_8_7.md"
CHECKPOINT_8_6 = ROOT / "docs" / "BACKEND_INTERNAL_EXPOSURE_AUDIT_CHECKPOINT_8_6.md"
DOC_8_5 = ROOT / "docs" / "BACKEND_INTERNAL_RESPONSE_ADAPTER_8_5.md"
DOC_8_4 = ROOT / "docs" / "BACKEND_INTERNAL_CONFIRMATION_GATE_8_4.md"
DOC_8_3 = ROOT / "docs" / "BACKEND_INTERNAL_DISPATCHER_8_3.md"
DOC_8_2 = ROOT / "docs" / "BACKEND_INTERNAL_REQUEST_ENVELOPE_8_2.md"
DOC_8_1 = ROOT / "docs" / "BACKEND_INTERNAL_EXPOSURE_REGISTRY_8_1.md"
PLAN_8_0 = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md"
DOC_7_6 = ROOT / "docs" / "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6.md"
DOC_7_7 = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_CHECKPOINT_7_7.md"
DOC_7_0 = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MEMORY = ROOT / "memoria_agentes"

FORBIDDEN_UI_OR_RUNTIME_FILES = (
    "src/components",
    "src/pages",
    "app",
    "pages",
    "core/backend_internal_ui_router.py",
    "core/backend_internal_ui_api.py",
    "core/backend_internal_public_endpoint.py",
    "core/backend_internal_controlled_execution_adapter.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/integration_runtime.py",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _safe_root() -> dict:
    return {"declared": True, "root_kind": "controlled_sandbox", "path_policy": "manifest_bound"}


def _request(service_id: str = "internal_exposure_registry", payload: dict | None = None) -> dict:
    return build_internal_request_envelope(
        request_id=f"req_{service_id}_8_7",
        service_id=service_id,
        caller_kind="internal_test",
        payload=payload or {"payload": {"status": "ready"}},
    )


def test_plan_8_7_exists_and_references_required_chain_docs():
    assert DOC.exists()
    text = _text(DOC)

    for token in (
        "PROMPT 8.7 - Plan de futura UI visual sobre contrato estable",
        "PROMPT 8.6 - Exposure audit checkpoint",
        "internal_response_adapter",
        "internal_confirmation_gate",
        "internal_dispatcher_no_runtime",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "backend_internal_ui_payload.v1",
        "BACKEND_INTERNAL_FUTURE_UI_CONTRACT_PLAN_READY",
        "ready_for_ui_ux_book_continuation",
    ):
        assert token in text

    for path in (CHECKPOINT_8_6, DOC_8_5, DOC_8_4, DOC_8_3, DOC_8_2, DOC_8_1, PLAN_8_0, DOC_7_6, DOC_7_7, DOC_7_0):
        assert path.exists()


def test_plan_defines_backend_authority_and_ui_no_inference_boundary():
    text = _text(DOC)
    for token in (
        "Backend decide",
        "La UI futura solo renderiza",
        "La UI no puede inferir",
        "permisos",
        "readiness",
        "capabilities",
        "path safety",
        "lifecycle safety",
        "operational state",
        "no debe derivar permisos",
    ):
        assert token in text


def test_plan_defines_action_forbidden_and_blocked_capabilities_rendering():
    text = _text(DOC)
    for token in (
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "true = capability blocked",
        "action no declarada como allowed no se muestra como activa",
        "action forbidden nunca se muestra activa",
        "action controlled-write/lifecycle nunca se dispara sin request envelope",
    ):
        assert token in text

    payload = build_backend_internal_ui_payload(
        service="internal_exposure_registry",
        service_kind="contract",
        status="ready",
        readiness="ready_for_ui_ux_book_continuation",
        request_id="req_ui_contract_8_7",
        allowed_actions=["view_service_map"],
        forbidden_actions=["activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"],
        blocked_capabilities=GLOBAL_BLOCKED_CAPABILITIES,
    )
    validated = validate_backend_internal_ui_payload(payload)
    assert validated["allowed_actions"][0]["action"] == "view_service_map"
    assert all(value is True for value in validated["blocked_capabilities"].values())
    assert not {"activate_runtime", "execute_agents"} & {item["action"] for item in validated["allowed_actions"]}


def test_plan_defines_state_readiness_confirmation_and_error_warning_contracts():
    text = _text(DOC)
    for token in (
        "State/Readiness Rendering",
        "draft",
        "preview_ready",
        "not_available",
        "active",
        "running",
        "production_ready",
        "Confirmation UX Contract",
        "confirmation.confirmed=true",
        "confirmation_scope",
        "allow_delete=true",
        "allow_reset=true",
        "Error/Warning UX Contract",
        "no mostrar tracebacks crudos",
    ):
        assert token in text

    gate = validate_confirmation_gate(
        {
            "request_envelope": build_internal_request_envelope(
                request_id="req_materialize_8_7",
                service_id="materialize_sandbox",
                caller_kind="internal_test",
                payload={
                    "sandbox_root": _safe_root(),
                    "preview_payload": {"preview_id": "preview_8_7"},
                },
                confirmation={
                    "confirmed": True,
                    "human_confirmation_required": True,
                    "confirmation_scope": "materialize_sandbox",
                    "confirmed_by": "internal_test",
                    "confirmation_id": "confirm_materialize_8_7",
                },
            ),
            "gate_options": {"allow_controlled_write": True},
        }
    )
    assert gate["confirmation_gate_passed"] is True
    assert gate["dispatch_executed"] is False


def test_plan_blocks_ui_frontend_endpoints_runtime_agents_integrations_and_domains():
    text = _text(DOC)
    for token in (
        "No se implementa UI visual",
        "No se crean frontend",
        "No Endpoint/API/Router",
        "No Runtime/Execution/Tools/Models/Integrations",
        "activar runtime",
        "ejecutar agentes",
        "invocar modelos",
        "llamar tools",
        "tocar integraciones",
        "network automation",
        "env/secrets",
        "`domains/` operativo",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
        "raw Package directo al User Panel",
    ):
        assert token in text

    for relative in FORBIDDEN_UI_OR_RUNTIME_FILES:
        assert not (ROOT / relative).exists(), relative


def test_contract_7_0_and_phase_8_modules_remain_coherent_for_future_ui():
    contract = build_backend_internal_ui_contract()
    validate_backend_internal_ui_contract(contract)
    available = {service["name"]: service for service in contract["available_internal_services"]}

    for name in (
        "stable_ui_payloads",
        "internal_exposure_registry",
        "internal_request_envelope",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "stable_response_adapter",
    ):
        assert available[name]["available_now"] is True
        assert available[name]["runtime_enabled"] is False
        assert available[name]["execution_enabled"] is False
        assert available[name]["public_endpoint"] is False
        assert available[name]["touches_visual_ui"] is False
        assert available[name]["touches_operational_domains"] is False

    registry_payload = adapt_registry_response(build_internal_exposure_registry())
    assert registry_payload["schema_version"] == "backend_internal_ui_payload.v1"
    assert registry_payload["flags"]["ui_visual"] is False
    assert all(value is True for value in registry_payload["blocked_capabilities"].values())


def test_request_envelope_rejects_ui_attempt_to_unlock_blocked_capabilities():
    unsafe = _request("stable_ui_payloads", payload={"payload": {"status": "ready"}})
    unsafe["safety"]["runtime_allowed"] = True
    unsafe["safety"]["execution_allowed"] = True
    unsafe["safety"]["tools_allowed"] = True
    unsafe["safety"]["models_allowed"] = True
    unsafe["safety"]["integrations_allowed"] = True
    unsafe["safety"]["operational_domains_allowed"] = True

    result = validate_internal_request_envelope(unsafe)
    codes = {error["error_code"] for error in result["errors"]}
    assert result["valid"] is False
    assert {
        "RUNTIME_REQUEST_BLOCKED",
        "EXECUTION_REQUEST_BLOCKED",
        "TOOLS_REQUEST_BLOCKED",
        "MODELS_REQUEST_BLOCKED",
        "INTEGRATIONS_REQUEST_BLOCKED",
        "OPERATIONAL_DOMAINS_REQUEST_BLOCKED",
    } <= codes


def test_dispatch_and_response_adapter_remain_no_runtime_for_future_ui():
    dispatch = dispatch_internal_request({"request_envelope": _request("internal_exposure_registry")})
    payload = adapt_dispatch_result(dispatch)

    assert dispatch["dispatch_allowed"] is True
    assert dispatch["dispatch_executed"] is True
    assert payload["schema_version"] == "backend_internal_ui_payload.v1"
    assert payload["meta"]["adapter_dispatched_request"] is False
    assert payload["meta"]["adapter_executed_service"] is False
    assert payload["summary"]["side_effects_performed"] is False
    assert json.loads(json.dumps(payload, ensure_ascii=False, sort_keys=True)) == payload


def test_plan_documents_ui_ux_continuation_and_prompt_0_5_3():
    text = _text(DOC)
    for token in (
        "Relacion Con Libro UI/UX",
        "Prompt 0 cerrado",
        "Prompt 0.5.1 cerrado",
        "Prompt 0.5.2 cerrado",
        "Prompt 0.5.3 - reconstruir Widgets",
        "presets automaticos por combinacion",
        "PROMPT UI/UX 0.5.3 - Reconstruir Widgets con datos reales sobre contrato backend estable",
    ):
        assert token in text


def test_next_plans_book_and_adr_record_prompt_8_7_without_ui_implementation():
    for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists()

    combined = "\n".join(_text(path) for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.7 - Plan de futura UI visual sobre contrato estable",
        "BACKEND_INTERNAL_FUTURE_UI_CONTRACT_PLAN_READY",
        "BACKEND_INTERNAL_UI_BOUNDARY_CONFIRMED",
        "BACKEND_INTERNAL_UI_NO_INFERENCE_CONFIRMED",
        "BACKEND_INTERNAL_PHASE_8_READY_FOR_UI_UX_CONTINUATION",
        "ready_for_ui_ux_book_continuation",
        "PROMPT UI/UX 0.5.3 - Reconstruir Widgets con datos reales sobre contrato backend estable",
        "no UI visual",
        "no endpoint publico",
        "no API/router HTTP",
        "no runtime",
        "no execution",
        "no tools/modelos/integraciones",
        "`domains/` operativo",
        "ADR-065",
    ):
        assert token in combined


def test_no_temp_artifacts_remain():
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
