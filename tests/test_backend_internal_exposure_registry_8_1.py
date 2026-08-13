import json
from pathlib import Path

import pytest

from core.backend_internal_exposure_registry import (
    GLOBAL_BLOCKED_CAPABILITIES,
    GLOBAL_FORBIDDEN_ACTIONS,
    REGISTRY_READINESS,
    RESPONSE_SCHEMA_VERSION,
    SCHEMA_VERSION,
    build_internal_exposure_registry,
    get_exposable_service,
    is_service_exposable,
    list_blocked_services,
    list_exposable_services,
    validate_exposure_service_entry,
    validate_internal_exposure_registry,
)
from core.backend_internal_ui_contract import build_backend_internal_ui_contract


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_EXPOSURE_REGISTRY_8_1.md"
PLAN_8_0 = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"

EXPECTED_EXPOSABLE = {
    "list_domains_status": "read_only_status",
    "preview_materialization": "read_only_preview",
    "materialize_sandbox": "controlled_write",
    "validate_domain": "read_only_validation",
    "rollback_sandbox": "controlled_lifecycle",
    "archive_sandbox_domain": "controlled_lifecycle",
    "delete_sandbox_domain": "controlled_lifecycle",
    "reset_sandbox_domain": "controlled_lifecycle",
    "stable_ui_payloads": "contract_payload_normalization",
}

EXPECTED_BLOCKED = {
    "runtime_execution",
    "agent_execution",
    "model_invocation",
    "tool_invocation",
    "external_integrations",
    "network_browser_automation",
    "public_endpoints",
    "ui_visual_runtime",
    "ui_device_control",
    "market_catalog_runtime",
    "business_composition_layer_runtime",
    "obliteratus",
    "domains_operativo",
    "raw_package_direct_to_user_panel",
    "scheduler_worker_queue",
    "orchestrator_dispatcher_event_bus",
}

FORBIDDEN_FILES = (
    "core/backend_internal_ui_dispatcher.py",
    "core/backend_internal_ui_request.py",
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
    "core/runtime_dispatcher.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/integration_runtime.py",
)


def _registry() -> dict:
    registry = build_internal_exposure_registry()
    assert validate_internal_exposure_registry(registry) == registry
    return registry


def test_registry_builder_validator_schema_readiness_and_json_safety():
    registry = _registry()

    assert registry["schema_version"] == SCHEMA_VERSION == "backend_internal_exposure_registry.v1"
    assert registry["registry_id"] == "backend_internal_controlled_exposure_registry"
    assert registry["status"] == "ready"
    assert registry["readiness"] == REGISTRY_READINESS == "ready_for_phase_8_2_internal_request_envelope"
    assert registry["depends_on"] == ["backend_internal_ui_contract", RESPONSE_SCHEMA_VERSION]
    assert registry["flags"]["dispatcher_created"] is False
    assert registry["flags"]["request_handling_enabled"] is False
    json.dumps(registry, ensure_ascii=False, sort_keys=True)


def test_registry_lists_expected_exposable_services_without_duplicates():
    registry = _registry()
    services = registry["exposable_services"]
    service_ids = [service["service_id"] for service in services]

    assert len(service_ids) == len(set(service_ids))
    assert set(service_ids) == set(EXPECTED_EXPOSABLE)
    for service in services:
        assert service["service_kind"] == EXPECTED_EXPOSABLE[service["service_id"]]
        assert service["available_now"] is True
        assert service["exposable"] is True
        assert service["response_schema_version"] == "backend_internal_ui_payload.v1"
        assert service["source_module"].startswith("core.")
        assert service["source_doc"].startswith("docs/")
        assert service["source_tests"] and all(path.startswith("tests/") for path in service["source_tests"])
        assert validate_exposure_service_entry(service) == service


def test_exposable_services_have_non_operational_flags_and_global_blocks():
    for service in _registry()["exposable_services"]:
        assert all(value is False for value in service["flags"].values())
        assert service["flags"]["public_endpoint"] is False
        assert service["flags"]["ui_visual"] is False
        assert service["flags"]["runtime_enabled"] is False
        assert service["flags"]["execution_enabled"] is False
        assert service["flags"]["tools_enabled"] is False
        assert service["flags"]["models_enabled"] is False
        assert service["flags"]["integrations_enabled"] is False
        assert service["blocked_capabilities"] == GLOBAL_BLOCKED_CAPABILITIES
        assert all(value is True for value in service["blocked_capabilities"].values())
        assert set(GLOBAL_FORBIDDEN_ACTIONS) <= set(service["forbidden_actions"])
        assert service["ui_boundary"]["backend_authority"] is True
        assert service["ui_boundary"]["ui_may_infer_permissions"] is False
        assert service["ui_boundary"]["ui_may_execute"] is False


def test_confirmation_validation_payload_allow_delete_and_allow_reset_requirements():
    services = {service["service_id"]: service for service in _registry()["exposable_services"]}

    assert services["list_domains_status"]["requires_safe_sandbox_root"] is True
    assert services["preview_materialization"]["requires_safe_sandbox_root"] is True
    assert services["validate_domain"]["requires_safe_sandbox_root"] is True
    assert services["stable_ui_payloads"]["requires_safe_sandbox_root"] is False
    assert services["materialize_sandbox"]["requires_confirmation"] is True
    assert services["materialize_sandbox"]["input_contract"]["requires_preview_payload"] is True

    for service_id in ("rollback_sandbox", "archive_sandbox_domain", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert services[service_id]["service_kind"] == "controlled_lifecycle"
        assert services[service_id]["requires_confirmation"] is True
        assert services[service_id]["requires_validation_payload"] is True
        assert services[service_id]["requires_safe_sandbox_root"] is True
        assert services[service_id]["side_effects"] is True

    for service_id in ("rollback_sandbox", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert services[service_id]["destructive"] is True
    assert services["archive_sandbox_domain"]["destructive"] is False
    assert services["delete_sandbox_domain"]["input_contract"]["requires_allow_delete"] is True
    assert services["reset_sandbox_domain"]["input_contract"]["requires_allow_reset"] is True


def test_blocked_services_are_not_exposable_and_default_denied():
    registry = _registry()
    exposable_ids = {service["service_id"] for service in registry["exposable_services"]}
    blocked = registry["blocked_services"]

    assert {service["service_id"] for service in blocked} == EXPECTED_BLOCKED
    assert not EXPECTED_BLOCKED & exposable_ids
    for service in blocked:
        assert service["blocked"] is True
        assert service["available_now"] is False
        assert service["reason"]
        assert service["blocked_capabilities"] == GLOBAL_BLOCKED_CAPABILITIES
        assert set(GLOBAL_FORBIDDEN_ACTIONS) <= set(service["forbidden_actions"])


def test_query_helpers_are_read_only_and_return_controlled_results():
    services = list_exposable_services()
    blocked = list_blocked_services()

    assert len(services) == len(EXPECTED_EXPOSABLE)
    assert len(blocked) == len(EXPECTED_BLOCKED)
    assert get_exposable_service("list_domains_status")["service_kind"] == "read_only_status"
    assert get_exposable_service("missing_service") is None
    assert is_service_exposable("stable_ui_payloads") is True
    assert is_service_exposable("runtime_execution") is False

    services[0]["service_id"] = "mutated"
    assert get_exposable_service("list_domains_status")["service_id"] == "list_domains_status"


def test_validator_rejects_duplicates_operational_flags_dispatcher_and_bad_lifecycle_rules():
    registry = _registry()
    duplicate = dict(registry)
    duplicate["exposable_services"] = [*registry["exposable_services"], registry["exposable_services"][0]]
    with pytest.raises(ValueError, match="duplicados"):
        validate_internal_exposure_registry(duplicate)

    operational = _registry()
    operational["exposable_services"][0]["flags"]["runtime_enabled"] = True
    with pytest.raises(ValueError, match="runtime_enabled"):
        validate_internal_exposure_registry(operational)

    dispatcher = _registry()
    dispatcher["flags"]["dispatcher_created"] = True
    with pytest.raises(ValueError, match="dispatcher_created"):
        validate_internal_exposure_registry(dispatcher)

    lifecycle = _registry()
    rollback = next(service for service in lifecycle["exposable_services"] if service["service_id"] == "rollback_sandbox")
    rollback["requires_validation_payload"] = False
    with pytest.raises(ValueError, match="validation_payload"):
        validate_internal_exposure_registry(lifecycle)


def test_ui_contract_marks_registry_available_and_keeps_future_8_x_planned():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert available["internal_exposure_registry"]["available_now"] is True
    assert available["internal_exposure_registry"]["type"] == "contract/internal-exposure-registry"
    assert available["internal_exposure_registry"]["side_effects"] is False
    assert available["internal_exposure_registry"]["public_endpoint"] is False
    assert available["internal_exposure_registry"]["touches_visual_ui"] is False
    assert available["internal_exposure_registry"]["runtime_enabled"] is False
    assert available["internal_exposure_registry"]["execution_enabled"] is False
    assert available["internal_exposure_registry"]["dispatcher_created"] is False
    assert available["internal_exposure_registry"]["request_handling_enabled"] is False

    for future in ("internal_request_envelope", "internal_request_validation", "internal_dispatcher_no_runtime", "confirmation_gate"):
        assert planned[future]["available_now"] is False
        assert planned[future]["dispatcher_created"] is False
        assert planned[future]["request_handling_enabled"] is False


def test_docs_plans_book_and_adr_record_prompt_8_1():
    for path in (DOC, PLAN_8_0, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_EXPOSURE_REGISTRY_READY",
        "BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_DISPATCHER_CONFIRMED",
        "BACKEND_INTERNAL_EXPOSURE_REGISTRY_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_8_2_internal_request_envelope",
        "PROMPT 8.2 - Internal request envelope y request validation",
        "backend_internal_exposure_registry.v1",
        "backend_internal_ui_payload.v1",
        "true = capability blocked",
        "No dispatcher",
        "No request handling",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.1 - Internal exposure registry / service map",
        "BACKEND_INTERNAL_EXPOSURE_REGISTRY_READY",
        "ready_for_phase_8_2_internal_request_envelope",
        "internal_exposure_registry",
        "service map",
        "no dispatcher",
        "no request handling",
        "no UI visual",
        "no endpoints publicos",
        "`domains/` operativo",
    ):
        assert token in combined


def test_no_ui_endpoint_dispatcher_runtime_agents_models_tools_or_temp_artifacts_created():
    for relative in FORBIDDEN_FILES:
        assert not (ROOT / relative).exists(), relative
    assert DOMAINS.exists()
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
