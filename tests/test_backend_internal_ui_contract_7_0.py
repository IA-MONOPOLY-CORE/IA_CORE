import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.backend_internal_ui_contract import (
    CONTRACT_ID,
    CONTRACT_NO_OPERATIONAL_VERDICT,
    CONTRACT_READINESS,
    CONTRACT_READY_VERDICT,
    CONTRACT_SCOPE,
    build_backend_internal_ui_capabilities,
    build_backend_internal_ui_contract,
    build_backend_internal_ui_error_contract,
    build_backend_internal_ui_forbidden_capabilities,
    summarize_backend_internal_ui_contract,
    validate_backend_internal_ui_contract,
)


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_ui_contract.py"


VISIBLE_ENTITIES = {
    "sandbox_domain",
    "artifact_manifest",
    "profile_catalog",
    "agent_presets",
    "paper_seed",
    "sandbox_agents",
    "sandbox_team",
    "sandbox_team_read_model",
    "materialization_audit_pack",
    "rollback_report",
    "regeneration_report",
    "readiness",
    "validation_error",
}

PLANNED_SERVICES = {
    "get_domain_detail",
    "get_sandbox_team_listing",
    "get_materialization_audit_pack",
    "backend_internal_ui_contract_checkpoint",
}

EXPECTED_ERRORS = {
    "DIRTY_WORKING_TREE",
    "UNEXPECTED_HEAD",
    "INVALID_DOMAIN_PAYLOAD",
    "INVALID_SANDBOX_SCHEMA",
    "MISSING_ARTIFACT_MANIFEST",
    "INCONSISTENT_ARTIFACT_MANIFEST",
    "UNSAFE_PATH",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "UI_ACTION_NOT_IMPLEMENTED",
    "OPERATIONAL_WRITE_BLOCKED",
    "SECRET_LIKE_FIELD_BLOCKED",
    "PAYLOAD_NOT_JSON_SAFE",
    "READINESS_NOT_MET",
}

FORBIDDEN_OPERATIONAL_MODULES = (
    "core/backend_ui_endpoint.py",
    "core/backend_ui_api.py",
    "core/ui_runtime.py",
    "core/frontend_runtime.py",
    "core/sandbox_execution_runner.py",
    "core/sandbox_runtime_runner.py",
    "core/team_runtime_executor.py",
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


def _dumped(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def test_backend_internal_ui_contract_builds_and_is_json_safe():
    contract = build_backend_internal_ui_contract()
    encoded = _dumped(contract)

    assert contract["contract_id"] == CONTRACT_ID
    assert contract["contract_version"] == "0.1"
    assert contract["contract_scope"] == CONTRACT_SCOPE
    assert contract["status"] == "ready"
    assert contract["verdict"] == CONTRACT_READY_VERDICT
    assert contract["non_operational_verdict"] == CONTRACT_NO_OPERATIONAL_VERDICT
    assert contract["readiness"] == CONTRACT_READINESS
    assert encoded
    assert len(encoded.encode("utf-8")) <= 96_000


def test_services_are_declared_without_overstating_availability():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert set(available) == {
        "get_backend_internal_ui_contract",
        "validate_backend_internal_ui_contract",
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
    }
    assert PLANNED_SERVICES <= set(planned)
    for service in planned.values():
        assert service["available_now"] is False
        assert service["touches_runtime"] is False
        assert service["touches_visual_ui"] is False
        assert service["touches_integrations"] is False
        assert service["can_touch_operational_domains"] is False
        assert service["public_endpoint"] is False
        assert service["ui_action_implemented"] is False
        assert service["runtime_enabled"] is False
        assert service["execution_enabled"] is False
    for service in planned.values():
        if service["destructive"]:
            assert service["requires_human_confirmation"] is True
    assert available["materialize_sandbox"]["type"] == "controlled-write"
    assert available["materialize_sandbox"]["side_effects"] is True
    assert available["materialize_sandbox"]["requires_human_confirmation"] is True
    assert available["materialize_sandbox"]["requires_valid_preview"] is True
    assert available["materialize_sandbox"]["prepares_rollback"] is True
    assert available["validate_domain"]["type"] == "read-only-validation"
    assert available["validate_domain"]["side_effects"] is False
    assert available["validate_domain"]["requires_human_confirmation"] is False
    assert available["validate_domain"]["destructive"] is False
    assert available["archive_sandbox_domain"]["type"] == "controlled-write"
    assert available["archive_sandbox_domain"]["requires_human_confirmation"] is True
    assert available["archive_sandbox_domain"]["requires_validation_payload"] is True
    assert available["archive_sandbox_domain"]["requires_safe_sandbox_root"] is True
    assert available["archive_sandbox_domain"]["destructive"] is False
    for lifecycle in ("rollback_sandbox", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert available[lifecycle]["type"] == "destructive-controlled"
        assert available[lifecycle]["requires_human_confirmation"] is True
        assert available[lifecycle]["requires_validation_payload"] is True
        assert available[lifecycle]["requires_safe_sandbox_root"] is True
        assert available[lifecycle]["destructive"] is True
        assert available[lifecycle]["touches_operational_domains"] is False
    assert available["stable_ui_payloads"]["type"] == "contract/payload-normalization"
    assert available["stable_ui_payloads"]["side_effects"] is False
    assert available["stable_ui_payloads"]["requires_human_confirmation"] is False
    assert available["stable_ui_payloads"]["destructive"] is False
    assert available["internal_exposure_registry"]["type"] == "contract/internal-exposure-registry"
    assert available["internal_exposure_registry"]["side_effects"] is False
    assert available["internal_exposure_registry"]["requires_human_confirmation"] is False
    assert available["internal_exposure_registry"]["destructive"] is False
    assert available["internal_exposure_registry"]["dispatcher_created"] is False
    assert available["internal_exposure_registry"]["request_handling_enabled"] is False
    assert available["internal_request_envelope"]["type"] == "contract/request-envelope"
    assert available["internal_request_validation"]["type"] == "contract/request-validation"
    for name in ("internal_request_envelope", "internal_request_validation"):
        assert available[name]["side_effects"] is False
        assert available[name]["requires_human_confirmation"] is False
        assert available[name]["destructive"] is False
        assert available[name]["dispatcher_created"] is False
        assert available[name]["request_handling_enabled"] is False
    assert available["internal_dispatcher_no_runtime"]["type"] == "contract/internal-dispatcher-no-runtime"
    assert available["internal_dispatcher_no_runtime"]["dispatcher_created"] is True
    assert available["internal_dispatcher_no_runtime"]["contractual_request_handling_enabled"] is True
    assert available["internal_dispatcher_no_runtime"]["request_handling_enabled"] is False
    assert available["internal_dispatcher_no_runtime"]["side_effects_performed"] is False
    assert available["internal_dispatch_policy"]["type"] == "contract/dispatch-policy"
    assert available["internal_dispatch_policy"]["dispatch_policy_defined"] is True
    assert available["internal_dispatch_policy"]["request_handling_enabled"] is False


def test_entities_states_readiness_and_errors_are_explicit():
    contract = build_backend_internal_ui_contract()
    entities = {entity["entity"] for entity in contract["entities"]}

    assert VISIBLE_ENTITIES <= entities
    assert "runtime" not in entities
    assert "execution_runner" not in entities
    for entity in contract["entities"]:
        assert entity["runtime_entity"] is False
        assert entity["minimal_payload_fields"]

    permitted = set(contract["states"]["permitted"])
    prohibited = set(contract["states"]["prohibited"])
    assert {"draft", "preview_ready", "sandbox_materialized", "sandbox_audited", "blocked"} <= permitted
    assert {"active", "running", "live", "operational"} <= prohibited
    assert not permitted & {"active", "running", "live", "operational"}
    assert CONTRACT_READINESS in contract["readiness_values"]
    assert "ready_for_runtime" not in contract["readiness_values"]
    assert EXPECTED_ERRORS <= {
        error["error_code"]
        for error in contract["error_contract"]["expected_errors"]
    }


def test_permissions_and_capabilities_are_default_deny():
    contract = build_backend_internal_ui_contract()
    permissions = contract["permissions"]
    blocked = contract["blocked_capabilities"]

    assert build_backend_internal_ui_capabilities()["can_read_backend_contract"] is True
    assert build_backend_internal_ui_forbidden_capabilities()["runtime"] is False
    for key in (
        "can_infer_critical_logic",
        "can_invent_states",
        "can_resolve_permissions",
        "can_mutate_manifests",
        "can_trigger_runtime",
        "can_execute_agents",
        "can_invoke_models",
        "can_call_tools",
        "can_touch_integrations",
        "can_write_operational_domains",
    ):
        assert permissions[key] is False
    assert all(value is False for value in blocked.values())
    assert contract["operational"] is False
    assert contract["runtime_enabled"] is False
    assert contract["execution_enabled"] is False
    assert contract["dry_run_real_enabled"] is False
    assert contract["ui_visual_enabled"] is False
    assert contract["public_endpoints_enabled"] is False
    assert contract["integrations_enabled"] is False


def test_payload_safety_and_summary_hide_operational_material():
    contract = build_backend_internal_ui_contract()
    safety = contract["payload_safety"]
    summary = summarize_backend_internal_ui_contract(contract)

    for field in (
        "json_serializable",
        "no_sets_bytes_functions_or_path_objects",
        "no_secret_like_fields",
        "no_env_fields",
        "no_runtime_handles",
        "no_model_or_tool_invocation_configs",
        "no_large_dumps",
        "no_productive_data",
    ):
        assert safety[field] is True
    assert summary["future_ui_must_not_infer_critical_logic"] is True
    assert summary["operational"] is False
    assert summary["runtime_enabled"] is False
    assert summary["execution_enabled"] is False


def test_error_contract_shape_is_ui_legible_and_backend_owned():
    errors = build_backend_internal_ui_error_contract()
    assert set(errors["shape"]) == {
        "error_code",
        "message",
        "severity",
        "field",
        "recoverable",
        "user_action",
        "developer_hint",
        "blocked",
    }
    assert set(errors["allowed_severities"]) == {"info", "warning", "error", "critical"}
    for error in errors["expected_errors"]:
        assert set(error) == set(errors["shape"])
        assert error["blocked"] is True


@pytest.mark.parametrize("flag", ["operational", "runtime_enabled", "execution_enabled"])
def test_operational_flags_true_fail_controlled(flag):
    contract = build_backend_internal_ui_contract()
    contract[flag] = True

    with pytest.raises(ValueError, match=flag):
        validate_backend_internal_ui_contract(contract)


def test_secret_like_key_fails_controlled():
    contract = build_backend_internal_ui_contract()
    contract["api_secret"] = "blocked"

    with pytest.raises(ValueError, match="sensible"):
        validate_backend_internal_ui_contract(contract)


def test_destructive_service_available_without_human_confirmation_fails():
    contract = build_backend_internal_ui_contract()
    service = deepcopy(contract["planned_internal_services"][0])
    service.update(
        {
            "name": "future_destructive_review",
            "type": "destructive-controlled",
            "available_now": False,
            "destructive": True,
            "requires_human_confirmation": False,
        }
    )
    contract["planned_internal_services"] = [service]

    with pytest.raises(ValueError, match="confirmacion humana"):
        validate_backend_internal_ui_contract(contract)


def test_ui_action_implemented_in_7_0_fails():
    contract = build_backend_internal_ui_contract()
    contract["available_internal_services"][0]["ui_action_implemented"] = True

    with pytest.raises(ValueError, match="accion UI"):
        validate_backend_internal_ui_contract(contract)


def test_active_integration_fails():
    contract = build_backend_internal_ui_contract()
    contract["integration_active"] = True

    with pytest.raises(ValueError, match="integration_active"):
        validate_backend_internal_ui_contract(contract)


def test_non_json_safe_payload_fails():
    contract = build_backend_internal_ui_contract()
    contract["warnings"] = {b"not-json-safe"}

    with pytest.raises(ValueError, match="JSON-safe"):
        validate_backend_internal_ui_contract(contract)


def test_docs_plans_book_and_adr_record_prompt_7_0():
    for path in (DOC, PHASE_7_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR, MODULE):
        assert path.exists()

    contract_doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_UI_CONTRACT_READY",
        "BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_1_list_domains_status_service",
        "PROMPT 7.1 - Servicio interno list_domains/status",
        "sandbox_domain",
        "sandbox_team_read_model",
        "materialization_audit_pack",
        "DIRTY_WORKING_TREE",
        "SECRET_LIKE_FIELD_BLOCKED",
        "no crea UI visual",
        "no crea endpoints publicos",
    ):
        assert token in contract_doc

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PHASE_7_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR)
    )
    for token in (
        "Fase 7 - Contrato backend interno para UI",
        "PROMPT 7.0 - Contrato backend interno para UI",
        "PROMPT 7.1 - Servicio interno list_domains/status",
        "BACKEND_INTERNAL_UI_CONTRACT_READY",
        "BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_1_list_domains_status_service",
        "runtime",
        "execution",
        "dry-run real",
        "tools",
        "modelos",
        "UI visual",
        "endpoints publicos",
        "integraciones",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
        "raw Package directo al User Panel",
    ):
        assert token in combined


def test_prompt_7_0_does_not_create_runtime_modules_or_temporals():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()


def test_domains_operational_tree_is_not_part_of_7_0_contract_actions():
    contract = build_backend_internal_ui_contract()
    for service in [*contract["available_internal_services"], *contract["planned_internal_services"]]:
        assert service["can_touch_operational_domains"] is False
    assert DOMAINS.exists()
