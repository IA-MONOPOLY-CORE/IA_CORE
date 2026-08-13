import json
from pathlib import Path

import pytest

from core import (
    backend_internal_domain_lifecycle_service as lifecycle_service,
    backend_internal_domain_status_service as status_service,
    backend_internal_materialize_sandbox_service as materialize_service,
    backend_internal_preview_materialization_service as preview_service,
    backend_internal_ui_payloads as payloads,
    backend_internal_validate_domain_service as validate_service,
)
from core.backend_internal_ui_contract import (
    ERROR_CODES,
    build_backend_internal_ui_contract,
    validate_backend_internal_ui_contract,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"

CHECKPOINT_DOC = DOCS / "BACKEND_INTERNAL_UI_CONTRACT_CHECKPOINT_7_7.md"
PHASE_7_PLAN = DOCS / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
NEXT_ARCH = DOCS / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = DOCS / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = DOCS / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"

DOCS_7_0_TO_7_6 = (
    DOCS / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md",
    DOCS / "BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_7_1.md",
    DOCS / "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_7_2.md",
    DOCS / "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_7_3.md",
    DOCS / "BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_7_4.md",
    DOCS / "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5.md",
    DOCS / "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6.md",
)

AVAILABLE_SERVICES = {
    "list_domains_status",
    "preview_materialization",
    "materialize_sandbox",
    "validate_domain",
    "rollback_sandbox",
    "archive_sandbox_domain",
    "delete_sandbox_domain",
    "reset_sandbox_domain",
    "stable_ui_payloads",
}

EXPECTED_SERVICE_TYPES = {
    "list_domains_status": "read-only",
    "preview_materialization": "read-only-preview",
    "materialize_sandbox": "controlled-write",
    "validate_domain": "read-only-validation",
    "rollback_sandbox": "destructive-controlled",
    "archive_sandbox_domain": "controlled-write",
    "delete_sandbox_domain": "destructive-controlled",
    "reset_sandbox_domain": "destructive-controlled",
    "stable_ui_payloads": "contract/payload-normalization",
}

EXPECTED_STABLE_KINDS = {
    "list_domains_status": "read_only_status",
    "preview_materialization": "read_only_preview",
    "materialize_sandbox": "controlled_write",
    "validate_domain": "read_only_validation",
    "rollback_sandbox": "controlled_lifecycle",
    "archive_sandbox_domain": "controlled_lifecycle",
    "delete_sandbox_domain": "controlled_lifecycle",
    "reset_sandbox_domain": "controlled_lifecycle",
    "stable_ui_payloads": "contract",
}

OPERATIONAL_ACTIONS = {
    "activate_runtime",
    "execute",
    "execute_agents",
    "invoke_model",
    "invoke_models",
    "call_tool",
    "call_tools",
    "use_integrations",
    "open_ui_runtime",
}

REQUIRED_FORBIDDEN_ACTIONS = {
    "activate_runtime",
    "execute_agents",
    "invoke_models",
    "call_tools",
    "use_integrations",
}

CRITICAL_ERROR_CODES = {
    "SANDBOX_ROOT_REQUIRED",
    "UNSAFE_SANDBOX_ROOT",
    "INVALID_DOMAIN_ID",
    "PREVIEW_REQUIRED",
    "INVALID_PREVIEW_PAYLOAD",
    "CONFIRMATION_REQUIRED",
    "INVALID_CONFIRMATION_SCOPE",
    "MISSING_ARTIFACT_MANIFEST",
    "INCONSISTENT_ARTIFACT_MANIFEST",
    "MISSING_CREATED_PATHS",
    "UNSAFE_CREATED_PATH",
    "PATH_TRAVERSAL_BLOCKED",
    "DOMAINS_OPERATIVE_PATH_BLOCKED",
    "REPO_ROOT_PATH_BLOCKED",
    "OVERWRITE_BLOCKED",
    "RUNTIME_BLOCKED",
    "EXECUTION_BLOCKED",
    "TOOLS_BLOCKED",
    "MODELS_BLOCKED",
    "INTEGRATIONS_BLOCKED",
    "PAYLOAD_NOT_JSON_SAFE",
    "SECRET_LIKE_FIELD_BLOCKED",
    "TRACEBACK_BLOCKED",
    "ABSOLUTE_PATH_BLOCKED",
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


def _available() -> dict[str, dict]:
    contract = validate_backend_internal_ui_contract(build_backend_internal_ui_contract())
    return {service["name"]: service for service in contract["available_internal_services"]}


def _planned() -> dict[str, dict]:
    contract = validate_backend_internal_ui_contract(build_backend_internal_ui_contract())
    return {service["name"]: service for service in contract["planned_internal_services"]}


def _assert_non_operational_flags(mapping: dict) -> None:
    for key in (
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "tools_enabled",
        "models_enabled",
        "integrations_enabled",
        "ui_visual",
        "public_endpoint",
    ):
        if key in mapping:
            assert mapping[key] is False


def _assert_stable_envelope(envelope: dict, *, service: str) -> None:
    validated = payloads.validate_backend_internal_ui_payload(envelope)
    assert validated == envelope
    assert envelope["schema_version"] == payloads.SCHEMA_VERSION
    assert envelope["schema_version"] == "backend_internal_ui_payload.v1"
    assert envelope["service"] == service
    assert envelope["service_kind"] == EXPECTED_STABLE_KINDS[service]
    assert set(
        [
            "schema_version",
            "service",
            "service_version",
            "service_kind",
            "status",
            "readiness",
            "domain",
            "materialization",
            "summary",
            "data",
            "warnings",
            "errors",
            "validation",
            "allowed_actions",
            "forbidden_actions",
            "blocked_capabilities",
            "meta",
            "flags",
        ]
    ) <= set(envelope)
    assert all(value is False for value in envelope["flags"].values())
    assert all(value is True for value in envelope["blocked_capabilities"].values())
    assert REQUIRED_FORBIDDEN_ACTIONS <= {item["action"] for item in envelope["forbidden_actions"]}
    assert not OPERATIONAL_ACTIONS & {item["action"] for item in envelope["allowed_actions"]}
    payloads.assert_backend_internal_json_safe(envelope)


def test_contract_and_services_7_1_to_7_6_are_importable_and_available():
    available = _available()
    planned = _planned()

    assert AVAILABLE_SERVICES <= set(available)
    for name in AVAILABLE_SERVICES:
        service = available[name]
        assert service["available_now"] is True
        assert service["type"] == EXPECTED_SERVICE_TYPES[name]
        assert service["touches_runtime"] is False
        assert service["touches_visual_ui"] is False
        assert service["touches_integrations"] is False
        assert service["touches_operational_domains"] is False
        assert service["can_touch_operational_domains"] is False
        assert service["public_endpoint"] is False
        assert service["runtime_enabled"] is False
        assert service["execution_enabled"] is False
    assert planned["backend_internal_ui_contract_checkpoint"]["available_now"] is False
    assert all(service["available_now"] is False for service in planned.values())


def test_no_operational_capabilities_public_endpoint_or_visual_ui_are_declared():
    contract = build_backend_internal_ui_contract()
    validate_backend_internal_ui_contract(contract)

    for key in (
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "dry_run_real_enabled",
        "ui_visual_enabled",
        "public_endpoints_enabled",
        "integrations_enabled",
    ):
        assert contract[key] is False
    assert all(value is False for value in contract["blocked_capabilities"].values())
    assert contract["non_operational_guarantees"]["no_runtime_activation"] is True
    assert contract["non_operational_guarantees"]["no_execution_activation"] is True
    assert contract["non_operational_guarantees"]["no_tools_or_models"] is True
    assert contract["non_operational_guarantees"]["no_network_browser_env_or_secrets"] is True
    assert contract["ui_boundaries"]["visual_ui_created"] is False
    assert contract["ui_boundaries"]["public_endpoints_created"] is False


def test_read_only_controlled_write_and_lifecycle_boundaries_are_explicit():
    available = _available()

    assert available["list_domains_status"]["side_effects"] is False
    assert available["preview_materialization"]["side_effects"] is False
    assert available["validate_domain"]["side_effects"] is False
    assert available["stable_ui_payloads"]["side_effects"] is False
    assert available["materialize_sandbox"]["side_effects"] is True
    assert available["materialize_sandbox"]["requires_valid_preview"] is True
    assert available["materialize_sandbox"]["requires_human_confirmation"] is True
    assert available["materialize_sandbox"]["destructive"] is False

    for name in ("rollback_sandbox", "archive_sandbox_domain", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert available[name]["requires_human_confirmation"] is True
        assert available[name]["requires_validation_payload"] is True
        assert available[name]["requires_safe_sandbox_root"] is True
        assert available[name]["side_effects"] is True
    assert available["archive_sandbox_domain"]["destructive"] is False
    for name in ("rollback_sandbox", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert available[name]["destructive"] is True


def test_services_return_or_validate_blocked_payloads_without_operational_flags():
    samples = [
        status_service.list_domains_status(sandbox_root=None),
        preview_service.preview_materialization(None),
        materialize_service.materialize_sandbox(None),
        validate_service.validate_domain(None),
        lifecycle_service.rollback_sandbox(None),
        lifecycle_service.archive_sandbox_domain(None),
        lifecycle_service.delete_sandbox_domain(None),
        lifecycle_service.reset_sandbox_domain(None),
    ]

    assert samples
    for sample in samples:
        assert sample["status"] == "blocked"
        _assert_non_operational_flags(sample)
        assert not OPERATIONAL_ACTIONS & set(sample.get("allowed_actions") or [])
        if sample.get("forbidden_actions"):
            assert REQUIRED_FORBIDDEN_ACTIONS <= set(sample["forbidden_actions"])
        if "blocked_capabilities" in sample:
            assert all(value is False for value in sample["blocked_capabilities"].values())
        json.dumps(sample, ensure_ascii=False, sort_keys=True)

    for module in (status_service, preview_service, materialize_service, validate_service, lifecycle_service):
        assert REQUIRED_FORBIDDEN_ACTIONS <= set(module.FORBIDDEN_ACTIONS)


def test_stable_payload_envelope_validates_representative_payload_for_each_service():
    raw_payloads = {
        "list_domains_status": status_service.list_domains_status(sandbox_root=None),
        "preview_materialization": preview_service.preview_materialization(None),
        "materialize_sandbox": materialize_service.materialize_sandbox(None),
        "validate_domain": validate_service.validate_domain(None),
        "rollback_sandbox": lifecycle_service.rollback_sandbox(None),
        "archive_sandbox_domain": lifecycle_service.archive_sandbox_domain(None),
        "delete_sandbox_domain": lifecycle_service.delete_sandbox_domain(None),
        "reset_sandbox_domain": lifecycle_service.reset_sandbox_domain(None),
    }
    adapters = {
        "list_domains_status": payloads.to_stable_ui_payload_from_domain_status,
        "preview_materialization": payloads.to_stable_ui_payload_from_preview,
        "materialize_sandbox": payloads.to_stable_ui_payload_from_materialization,
        "validate_domain": payloads.to_stable_ui_payload_from_validation,
        "rollback_sandbox": payloads.to_stable_ui_payload_from_lifecycle,
        "archive_sandbox_domain": payloads.to_stable_ui_payload_from_lifecycle,
        "delete_sandbox_domain": payloads.to_stable_ui_payload_from_lifecycle,
        "reset_sandbox_domain": payloads.to_stable_ui_payload_from_lifecycle,
    }

    for service, raw in raw_payloads.items():
        envelope = adapters[service](raw)
        _assert_stable_envelope(envelope, service=service)

    own = payloads.build_backend_internal_ui_payload(
        service="stable_ui_payloads",
        service_kind="contract",
        status="ready",
        readiness=payloads.SERVICE_READINESS,
        allowed_actions=["view_status"],
        forbidden_actions=sorted(REQUIRED_FORBIDDEN_ACTIONS),
        summary={"verdict": payloads.SERVICE_VERDICT},
        validation={"json_safe": True, "no_operational": True},
    )
    _assert_stable_envelope(own, service="stable_ui_payloads")


def test_payload_rejects_operational_status_kind_actions_secrets_tracebacks_and_paths():
    base = payloads.build_backend_internal_ui_payload(
        service="stable_ui_payloads",
        service_kind="contract",
        status="ready",
        readiness=payloads.SERVICE_READINESS,
        forbidden_actions=sorted(REQUIRED_FORBIDDEN_ACTIONS),
    )

    bad_status = dict(base)
    bad_status["status"] = "running"
    with pytest.raises(ValueError, match="status"):
        payloads.validate_backend_internal_ui_payload(bad_status)

    bad_kind = dict(base)
    bad_kind["service_kind"] = "runtime"
    with pytest.raises(ValueError, match="service_kind"):
        payloads.validate_backend_internal_ui_payload(bad_kind)

    with pytest.raises(ValueError, match="operativa"):
        payloads.normalize_backend_internal_action("activate_runtime")
    with pytest.raises(ValueError, match="SECRET_LIKE_FIELD_BLOCKED"):
        payloads.build_backend_internal_ui_payload(
            service="stable_ui_payloads",
            service_kind="contract",
            status="ready",
            readiness=payloads.SERVICE_READINESS,
            data={"api_secret": "blocked"},
            forbidden_actions=sorted(REQUIRED_FORBIDDEN_ACTIONS),
        )
    with pytest.raises(ValueError, match="traceback"):
        payloads.normalize_backend_internal_error({"message": "Traceback (most recent call last): boom"})
    with pytest.raises(ValueError, match="path absoluto"):
        payloads.normalize_backend_internal_error({"message": "C:\\IA_CORE\\secret.txt"})


def test_error_contract_covers_critical_7_x_errors():
    contract = build_backend_internal_ui_contract()
    declared = {error["error_code"] for error in contract["error_contract"]["expected_errors"]}

    assert CRITICAL_ERROR_CODES <= declared
    assert CRITICAL_ERROR_CODES <= set(ERROR_CODES)


def test_docs_plans_book_and_adr_confirm_phase_7_checkpoint():
    for path in (*DOCS_7_0_TO_7_6, CHECKPOINT_DOC, PHASE_7_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists(), path

    checkpoint = CHECKPOINT_DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_UI_CONTRACT_PHASE_7_CHECKPOINT_PASSED",
        "BACKEND_INTERNAL_UI_CONTRACT_SERVICES_CONFIRMED",
        "BACKEND_INTERNAL_UI_CONTRACT_NO_OPERATIONAL_CONFIRMED",
        "BACKEND_INTERNAL_UI_CONTRACT_READY_FOR_NEXT_BLOCK",
        "ready_for_next_backend_internal_architecture_block",
        "PROMPT 8.0 - Planificacion del bloque de exposicion interna controlada para futura UI",
        "backend_internal_ui_payload.v1",
        "true = blocked",
        "no crea UI visual",
        "no crea endpoints publicos",
        "domains/ operativo bloqueado",
    ):
        assert token in checkpoint

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (PHASE_7_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 7.7 - Checkpoint integral contrato backend interno para UI",
        "Fase 7 cerrada",
        "BACKEND_INTERNAL_UI_CONTRACT_PHASE_7_CHECKPOINT_PASSED",
        "ready_for_next_backend_internal_architecture_block",
        "Fase 8 - Exposicion interna controlada para futura UI",
        "PROMPT 8.0 - Planificacion del bloque de exposicion interna controlada para futura UI",
        "runtime",
        "execution",
        "tools",
        "modelos",
        "integraciones",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
    ):
        assert token in combined


def test_no_domains_operational_ui_endpoint_runtime_or_temp_artifacts_created():
    assert DOMAINS.exists()
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
