import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.backend_internal_domain_lifecycle_service import (
    ARCHIVE_ACTION,
    DELETE_ACTION,
    RESET_ACTION,
    ROLLBACK_ACTION,
    archive_sandbox_domain,
    build_domain_lifecycle_request,
    delete_sandbox_domain,
    reset_sandbox_domain,
    rollback_sandbox,
)
from core.backend_internal_domain_status_service import list_domains_status
from core.backend_internal_materialize_sandbox_service import (
    build_materialize_sandbox_request,
    materialize_sandbox,
)
from core.backend_internal_preview_materialization_service import preview_materialization
from core.backend_internal_ui_contract import build_backend_internal_ui_contract
from core.backend_internal_ui_payloads import (
    SCHEMA_VERSION,
    SERVICE_JSON_SAFE_VERDICT,
    SERVICE_NO_OPERATIONAL_VERDICT,
    SERVICE_READINESS,
    SERVICE_VERDICT,
    assert_backend_internal_json_safe,
    build_backend_internal_ui_payload,
    normalize_backend_internal_action,
    normalize_backend_internal_error,
    normalize_backend_internal_warning,
    normalize_blocked_capabilities,
    to_stable_ui_payload_from_domain_status,
    to_stable_ui_payload_from_lifecycle,
    to_stable_ui_payload_from_materialization,
    to_stable_ui_payload_from_preview,
    to_stable_ui_payload_from_validation,
    validate_backend_internal_ui_payload,
)
from core.backend_internal_validate_domain_service import (
    build_validate_domain_request,
    validate_domain,
)


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
CONTRACT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_ui_payloads.py"

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


def _domain_request(domain_id: str) -> dict:
    return {
        "domain_id": domain_id,
        "domain_name": f"Stable UI {domain_id}",
        "domain_description": "Dominio sandbox para payloads estables 7.6.",
        "domain_type": "sandbox",
        "source": "test_fixture",
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "business_scale": "pyme",
        "objective": "payload estable backend interno 7.6",
        "complexity_level": "media",
        "max_profiles": 2,
        "max_presets": 2,
    }


def _preview(root: Path, domain_id: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    return preview_materialization(
        {
            "domain_request": _domain_request(domain_id),
            "sandbox_root": str(root),
            "preview_options": {
                "include_team_preview": True,
                "include_audit_pack_preview": True,
                "include_paths_preview": True,
                "include_manifest_preview": True,
            },
        }
    )


def _materialize_confirmation() -> dict:
    return {
        "confirmed": True,
        "confirmation_scope": "materialize_sandbox",
        "human_confirmation_required": True,
        "confirmed_by": "test_or_internal_caller",
        "confirmation_id": "confirm_materialize_for_payloads_7_6",
    }


def _lifecycle_confirmation(action: str) -> dict:
    return {
        "confirmed": True,
        "confirmation_scope": action,
        "human_confirmation_required": True,
        "confirmed_by": "test_or_internal_caller",
        "confirmation_id": f"confirm_{action}_7_6",
    }


def _materialized(root: Path, domain_id: str) -> dict:
    preview_payload = _preview(root, domain_id)
    result = materialize_sandbox(
        build_materialize_sandbox_request(
            preview_payload=preview_payload,
            sandbox_root=root,
            confirmation=_materialize_confirmation(),
        )
    )
    assert result["status"] == "materialized"
    return result


def _validated(root: Path, materialized: dict) -> dict:
    payload = validate_domain(
        build_validate_domain_request(
            sandbox_root=root,
            domain_id=materialized["domain_id"],
            materialization_id=materialized["materialization_id"],
        )
    )
    assert payload["valid"] is True
    return payload


def _lifecycle_request(action: str, root: Path, validation_payload: dict, options: dict | None = None) -> dict:
    return build_domain_lifecycle_request(
        action=action,
        sandbox_root=root,
        domain_id=validation_payload["domain_id"],
        materialization_id=validation_payload["materialization_id"],
        validation_payload=validation_payload,
        confirmation=_lifecycle_confirmation(action),
        options=options,
    )


def _assert_envelope(payload: dict, *, service_kind: str) -> None:
    validated = validate_backend_internal_ui_payload(payload)
    assert validated == payload
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["service"]
    assert payload["service_kind"] == service_kind
    assert payload["status"]
    assert payload["readiness"]
    for field in (
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
    ):
        assert field in payload
    assert all(value is False for value in payload["flags"].values())
    assert all(value is True for value in payload["blocked_capabilities"].values())
    assert {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"} <= {
        item["action"] for item in payload["forbidden_actions"]
    }
    assert not {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"} & {
        item["action"] for item in payload["allowed_actions"]
    }
    assert_backend_internal_json_safe(payload)


def test_builder_validator_and_envelope_required_fields():
    payload = build_backend_internal_ui_payload(
        service="stable_ui_payloads",
        service_kind="contract",
        status="ready",
        readiness=SERVICE_READINESS,
        domain={"domain_id": "demo_domain"},
        materialization={"materialization_id": "mat_demo", "created_paths_count": 1, "artifact_count": 2},
        summary={"verdict": SERVICE_VERDICT},
        data={"json_safe_verdict": SERVICE_JSON_SAFE_VERDICT},
        validation={"no_operational_verdict": SERVICE_NO_OPERATIONAL_VERDICT},
        allowed_actions=["view_status"],
        forbidden_actions=["activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"],
        blocked_capabilities={"runtime": False, "execution": False},
        meta={"compatibility": "contract"},
    )

    _assert_envelope(payload, service_kind="contract")
    assert payload["domain"]["domain_id"] == "demo_domain"
    assert payload["materialization"]["sandbox_root_policy"] == "explicit_controlled_sandbox_root"


def test_status_service_kind_and_json_safety_rejections():
    payload = build_backend_internal_ui_payload(
        service="stable_ui_payloads",
        service_kind="contract",
        status="ready",
        readiness=SERVICE_READINESS,
        forbidden_actions=["activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"],
    )

    broken_status = deepcopy(payload)
    broken_status["status"] = "running"
    with pytest.raises(ValueError, match="status"):
        validate_backend_internal_ui_payload(broken_status)

    broken_kind = deepcopy(payload)
    broken_kind["service_kind"] = "runtime"
    with pytest.raises(ValueError, match="service_kind"):
        validate_backend_internal_ui_payload(broken_kind)

    broken_json = deepcopy(payload)
    broken_json["data"]["bad"] = {b"not-json"}
    with pytest.raises(ValueError, match="JSON-safe"):
        assert_backend_internal_json_safe(broken_json)


def test_error_warning_action_and_blocked_capability_normalizers():
    error = normalize_backend_internal_error(
        {"error_code": "RUNTIME_BLOCKED", "message": "runtime bloqueado", "recoverable": False, "user_action": "ver estado"},
        service="validate_domain",
    )
    warning = normalize_backend_internal_warning({"error_code": "READINESS_NOT_MET", "message": "faltan artefactos"}, service="list_domains_status")
    action = normalize_backend_internal_action("delete_sandbox_domain")
    forbidden = normalize_backend_internal_action("activate_runtime", forbidden=True)
    blocked = normalize_blocked_capabilities({"runtime": False, "execution": False})

    assert set(error) == {"code", "message", "severity", "service", "field", "recoverable", "ui_hint", "sensitive"}
    assert error["severity"] == "error"
    assert warning["severity"] == "warning"
    assert set(action) == {"action", "label", "kind", "requires_confirmation", "destructive", "available_now", "reason"}
    assert action["destructive"] is True
    assert action["requires_confirmation"] is True
    assert forbidden["available_now"] is False
    assert all(blocked.values())


def test_destructive_allowed_action_requires_confirmation_and_operational_allowed_actions_fail():
    with pytest.raises(ValueError, match="confirmacion"):
        normalize_backend_internal_action(
            {
                "action": "delete_sandbox_domain",
                "destructive": True,
                "requires_confirmation": False,
                "available_now": True,
            }
        )
    with pytest.raises(ValueError, match="operativa"):
        normalize_backend_internal_action("activate_runtime")


def test_secret_traceback_absolute_path_and_sensitive_payloads_fail():
    with pytest.raises(ValueError, match="SECRET_LIKE_FIELD_BLOCKED"):
        build_backend_internal_ui_payload(
            service="stable_ui_payloads",
            service_kind="contract",
            status="ready",
            readiness=SERVICE_READINESS,
            data={"api_secret": "blocked"},
            forbidden_actions=["activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"],
        )
    with pytest.raises(ValueError, match="traceback"):
        normalize_backend_internal_error({"message": "Traceback (most recent call last): boom"}, service="x")
    with pytest.raises(ValueError, match="path absoluto"):
        normalize_backend_internal_error({"message": "C:\\IA_CORE\\secret.txt"}, service="x")


def test_adapters_for_domain_status_preview_materialization_and_validation(tmp_path):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root, "stable_payload_preview")
    materialized = materialize_sandbox(
        build_materialize_sandbox_request(
            preview_payload=preview_payload,
            sandbox_root=root,
            confirmation=_materialize_confirmation(),
        )
    )
    validation_payload = _validated(root, materialized)
    status_payload = list_domains_status(sandbox_root=root)

    _assert_envelope(to_stable_ui_payload_from_domain_status(status_payload), service_kind="read_only_status")
    _assert_envelope(to_stable_ui_payload_from_preview(preview_payload), service_kind="read_only_preview")
    _assert_envelope(to_stable_ui_payload_from_materialization(materialized), service_kind="controlled_write")
    _assert_envelope(to_stable_ui_payload_from_validation(validation_payload), service_kind="read_only_validation")


def test_lifecycle_adapters_for_rollback_archive_delete_and_reset(tmp_path):
    rollback_root = tmp_path / "rollback"
    rollback_materialized = _materialized(rollback_root, "stable_payload_rollback")
    rollback_validation = _validated(rollback_root, rollback_materialized)
    rollback_payload = rollback_sandbox(_lifecycle_request(ROLLBACK_ACTION, rollback_root, rollback_validation))
    _assert_envelope(to_stable_ui_payload_from_lifecycle(rollback_payload), service_kind="controlled_lifecycle")

    archive_root = tmp_path / "archive"
    archive_materialized = _materialized(archive_root, "stable_payload_archive")
    archive_validation = _validated(archive_root, archive_materialized)
    archive_payload = archive_sandbox_domain(_lifecycle_request(ARCHIVE_ACTION, archive_root, archive_validation))
    _assert_envelope(to_stable_ui_payload_from_lifecycle(archive_payload), service_kind="controlled_lifecycle")

    delete_root = tmp_path / "delete"
    delete_materialized = _materialized(delete_root, "stable_payload_delete")
    delete_validation = _validated(delete_root, delete_materialized)
    delete_payload = delete_sandbox_domain(_lifecycle_request(DELETE_ACTION, delete_root, delete_validation, {"allow_delete": True}))
    _assert_envelope(to_stable_ui_payload_from_lifecycle(delete_payload), service_kind="controlled_lifecycle")

    reset_root = tmp_path / "reset"
    reset_materialized = _materialized(reset_root, "stable_payload_reset")
    reset_validation = _validated(reset_root, reset_materialized)
    reset_payload = reset_sandbox_domain(_lifecycle_request(RESET_ACTION, reset_root, reset_validation, {"allow_reset": True}))
    _assert_envelope(to_stable_ui_payload_from_lifecycle(reset_payload), service_kind="controlled_lifecycle")


def test_contract_marks_stable_payloads_available_and_keeps_services_available():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert available["stable_ui_payloads"]["available_now"] is True
    assert available["stable_ui_payloads"]["type"] == "contract/payload-normalization"
    assert available["stable_ui_payloads"]["side_effects"] is False
    assert available["stable_ui_payloads"]["requires_human_confirmation"] is False
    assert available["stable_ui_payloads"]["destructive"] is False
    for service_name in (
        "list_domains_status",
        "preview_materialization",
        "materialize_sandbox",
        "validate_domain",
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
    ):
        assert available[service_name]["available_now"] is True
    assert planned["backend_internal_ui_contract_checkpoint"]["available_now"] is False


def test_source_has_no_runtime_model_tool_ui_env_network_or_filesystem_writes():
    source = MODULE.read_text(encoding="utf-8")

    assert "os.environ" not in source
    assert "requests." not in source
    assert "httpx." not in source
    assert "subprocess" not in source
    assert "openai" not in source.lower()
    assert ".invoke_model" not in source
    assert "invoke_model(" not in source
    assert ".execute_tool" not in source
    assert "execute_tool(" not in source
    assert "FastAPI" not in source
    assert ".write_text(" not in source
    assert ".mkdir(" not in source
    assert "materialize_sandbox(" not in source
    assert "rollback_sandbox(" not in source


def test_docs_plans_book_and_adr_record_prompt_7_6():
    docs = [DOC, PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR]
    for path in docs:
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_READY",
        "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_JSON_SAFE_CONFIRMED",
        "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_7_backend_internal_ui_contract_checkpoint",
        "PROMPT 7.7 - Checkpoint integral contrato backend interno para UI",
        "backend_internal_ui_payload.v1",
        "true = blocked",
        "stable_ui_payloads",
        "no crea UI visual",
        "no crea endpoints publicos",
        "no toca domains operativo",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs[1:])
    for token in (
        "PROMPT 7.6 - Payloads estables para futura UI",
        "BACKEND_INTERNAL_STABLE_UI_PAYLOADS_READY",
        "ready_for_phase_7_7_backend_internal_ui_contract_checkpoint",
        "stable_ui_payloads",
        "backend_internal_ui_payload.v1",
        "PROMPT 7.7 - Checkpoint integral contrato backend interno para UI",
    ):
        assert token in combined


def test_no_operational_modules_domains_or_temp_artifacts_were_created():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert DOMAINS.exists()
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
