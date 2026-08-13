import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.backend_internal_domain_lifecycle_service import (
    ARCHIVE_ACTION,
    DELETE_ACTION,
    FORBIDDEN_ACTIONS,
    RESET_ACTION,
    ROLLBACK_ACTION,
    SERVICE_CONTROLLED_ACTIONS_VERDICT,
    SERVICE_NAME,
    SERVICE_NO_OPERATIONAL_VERDICT,
    SERVICE_READINESS,
    SERVICE_VERSION,
    build_domain_lifecycle_error,
    build_domain_lifecycle_request,
    archive_sandbox_domain,
    delete_sandbox_domain,
    reset_sandbox_domain,
    rollback_sandbox,
    validate_domain_lifecycle_request,
    validate_domain_lifecycle_result,
)
from core.backend_internal_materialize_sandbox_service import (
    build_materialize_sandbox_request,
    materialize_sandbox,
)
from core.backend_internal_preview_materialization_service import preview_materialization
from core.backend_internal_ui_contract import build_backend_internal_ui_contract
from core.backend_internal_validate_domain_service import (
    build_validate_domain_request,
    validate_domain,
)


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_7_5.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
CONTRACT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_domain_lifecycle_service.py"

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


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return ""
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _domain_request(domain_id: str) -> dict:
    return {
        "domain_id": domain_id,
        "domain_name": f"Lifecycle {domain_id}",
        "domain_description": "Dominio sandbox para lifecycle interno 7.5.",
        "domain_type": "sandbox",
        "source": "test_fixture",
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "business_scale": "pyme",
        "objective": "lifecycle backend interno 7.5",
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
        "confirmation_id": "confirm_materialize_for_lifecycle_7_5",
    }


def _lifecycle_confirmation(action: str, **overrides) -> dict:
    payload = {
        "confirmed": True,
        "confirmation_scope": action,
        "human_confirmation_required": True,
        "confirmed_by": "test_or_internal_caller",
        "confirmation_id": f"confirm_{action}_7_5",
    }
    payload.update(overrides)
    return payload


def _materialized(root: Path, domain_id: str) -> dict:
    preview_payload = _preview(root, domain_id)
    request = build_materialize_sandbox_request(
        preview_payload=preview_payload,
        sandbox_root=root,
        confirmation=_materialize_confirmation(),
    )
    result = materialize_sandbox(request)
    assert result["status"] == "materialized"
    return result


def _validated(root: Path, materialized: dict) -> dict:
    request = build_validate_domain_request(
        sandbox_root=root,
        domain_id=materialized["domain_id"],
        materialization_id=materialized["materialization_id"],
    )
    result = validate_domain(request)
    assert result["status"] == "validated"
    assert result["valid"] is True
    return result


def _validated_domain(root: Path, domain_id: str) -> tuple[dict, dict]:
    materialized = _materialized(root, domain_id)
    return materialized, _validated(root, materialized)


def _request(action: str, root: Path, validation_payload: dict, **overrides) -> dict:
    payload = build_domain_lifecycle_request(
        action=action,
        sandbox_root=root,
        domain_id=validation_payload["domain_id"],
        materialization_id=validation_payload["materialization_id"],
        validation_payload=validation_payload,
        confirmation=overrides.pop("confirmation", _lifecycle_confirmation(action)),
        options=overrides.pop("options", None),
    )
    payload.update(overrides)
    return payload


def _assert_non_operational(payload: dict) -> None:
    assert validate_domain_lifecycle_result(payload) == payload
    assert payload["service"] == SERVICE_NAME
    assert payload["service_version"] == SERVICE_VERSION
    assert payload["controlled_actions_verdict"] == SERVICE_CONTROLLED_ACTIONS_VERDICT
    assert payload["non_operational_verdict"] == SERVICE_NO_OPERATIONAL_VERDICT
    assert payload["readiness"] == SERVICE_READINESS
    assert payload["operational"] is False
    assert payload["runtime_enabled"] is False
    assert payload["execution_enabled"] is False
    assert {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"} <= set(payload["forbidden_actions"])
    assert not {
        "execute_agents",
        "activate_runtime",
        "invoke_models",
        "call_tools",
        "use_integrations",
        "open_ui_runtime",
        "delete_without_confirmation",
        "rollback_without_confirmation",
        "reset_without_confirmation",
    } & set(payload["allowed_actions"])
    json.dumps(payload, ensure_ascii=False, sort_keys=True)


def test_lifecycle_services_exist_and_require_inputs(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()

    for action, func in (
        (ROLLBACK_ACTION, rollback_sandbox),
        (ARCHIVE_ACTION, archive_sandbox_domain),
        (DELETE_ACTION, delete_sandbox_domain),
        (RESET_ACTION, reset_sandbox_domain),
    ):
        missing = func(None)
        assert missing["status"] == "blocked"
        assert missing["errors"][0]["error_code"] == "LIFECYCLE_ACTION_REQUIRED"

        missing_root = func({"action": action, "domain_id": "missing_domain"})
        assert missing_root["errors"][0]["error_code"] == "SANDBOX_ROOT_REQUIRED"

        missing_domain = func({"action": action, "sandbox_root": str(root)})
        assert missing_domain["errors"][0]["error_code"] == "DOMAIN_ID_REQUIRED"

        missing_validation = func(
            {
                "action": action,
                "sandbox_root": str(root),
                "domain_id": "missing_domain",
                "confirmation": _lifecycle_confirmation(action),
            }
        )
        assert missing_validation["errors"][0]["error_code"] == "VALIDATION_PAYLOAD_REQUIRED"


def test_lifecycle_rejects_confirmation_scope_unsafe_roots_and_traversal(tmp_path):
    root = tmp_path / "sandboxes"
    _, validation_payload = _validated_domain(root, "lifecycle_rejects")
    wrong_scope = _request(
        ROLLBACK_ACTION,
        root,
        validation_payload,
        confirmation=_lifecycle_confirmation(ROLLBACK_ACTION, confirmation_scope="other"),
    )
    assert rollback_sandbox(wrong_scope)["errors"][0]["error_code"] == "INVALID_CONFIRMATION_SCOPE"

    unsafe_domains = _request(ROLLBACK_ACTION, root, validation_payload)
    unsafe_domains["sandbox_root"] = str(DOMAINS)
    assert rollback_sandbox(unsafe_domains)["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"

    unsafe_root = _request(ROLLBACK_ACTION, root, validation_payload)
    unsafe_root["sandbox_root"] = str(ROOT)
    assert rollback_sandbox(unsafe_root)["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"

    traversal = _request(ROLLBACK_ACTION, root, validation_payload)
    traversal["domain_id"] = "../escape"
    assert rollback_sandbox(traversal)["errors"][0]["error_code"] == "PATH_TRAVERSAL_BLOCKED"


def test_lifecycle_rejects_secret_like_fields_and_invalid_validation(tmp_path):
    root = tmp_path / "sandboxes"
    _, validation_payload = _validated_domain(root, "lifecycle_secret_invalid")

    with pytest.raises(ValueError, match="SECRET_LIKE_FIELD_BLOCKED"):
        build_domain_lifecycle_request(
            action=ROLLBACK_ACTION,
            sandbox_root=root,
            domain_id=validation_payload["domain_id"],
            materialization_id=validation_payload["materialization_id"],
            validation_payload=validation_payload,
            confirmation=_lifecycle_confirmation(ROLLBACK_ACTION),
            options={"api_secret": "blocked"},
        )

    invalid_service = _request(ROLLBACK_ACTION, root, validation_payload)
    invalid_service["validation_payload"] = {"service": "other", "valid": True}
    assert rollback_sandbox(invalid_service)["errors"][0]["error_code"] == "INVALID_VALIDATION_PAYLOAD"

    not_valid = _request(ROLLBACK_ACTION, root, validation_payload)
    not_valid["validation_payload"] = deepcopy(validation_payload)
    not_valid["validation_payload"]["valid"] = False
    assert rollback_sandbox(not_valid)["errors"][0]["error_code"] == "VALIDATION_NOT_PASSED"

    mismatch = _request(ROLLBACK_ACTION, root, validation_payload)
    mismatch["materialization_id"] = "mat_other"
    assert rollback_sandbox(mismatch)["errors"][0]["error_code"] == "MATERIALIZATION_ID_MISMATCH"


def test_rollback_sandbox_uses_integral_rollback_and_is_idempotent(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    root = tmp_path / "sandboxes"
    materialized, validation_payload = _validated_domain(root, "lifecycle_rollback")
    domain_dir = root / materialized["domain_id"]
    outside = root / "outside_sentinel.txt"
    outside.write_text("preserve", encoding="utf-8")

    result = rollback_sandbox(_request(ROLLBACK_ACTION, root, validation_payload))

    _assert_non_operational(result)
    assert result["action"] == ROLLBACK_ACTION
    assert result["status"] == "rolled_back"
    assert result["writes_performed"] is True
    assert result["destructive_operation_performed"] is True
    assert not domain_dir.exists()
    assert outside.read_text(encoding="utf-8") == "preserve"
    assert result["rollback_records"]["record_path"].startswith("_rollback_records/")
    assert _tree_hash(DOMAINS) == before_domains

    second = rollback_sandbox(_request(ROLLBACK_ACTION, root, validation_payload))

    _assert_non_operational(second)
    assert second["status"] == "already_rolled_back"
    assert second["writes_performed"] is False
    assert second["destructive_operation_performed"] is False
    assert outside.exists()
    assert _tree_hash(DOMAINS) == before_domains


def test_archive_sandbox_domain_archives_without_delete_and_is_idempotent(tmp_path):
    root = tmp_path / "sandboxes"
    materialized, validation_payload = _validated_domain(root, "lifecycle_archive")
    domain_dir = root / materialized["domain_id"]

    result = archive_sandbox_domain(_request(ARCHIVE_ACTION, root, validation_payload))

    _assert_non_operational(result)
    assert result["action"] == ARCHIVE_ACTION
    assert result["status"] == "archived"
    assert result["writes_performed"] is True
    assert result["destructive_operation_performed"] is False
    assert not domain_dir.exists()
    archive_dir = root / "_archives" / f"{materialized['domain_id']}__{materialized['materialization_id']}"
    assert archive_dir.is_dir()
    assert (archive_dir / "archive_record.json").is_file()
    assert result["archive_record"]["archive_dir"].startswith("_archives/")

    second = archive_sandbox_domain(_request(ARCHIVE_ACTION, root, validation_payload))

    _assert_non_operational(second)
    assert second["status"] == "already_archived"
    assert second["writes_performed"] is False
    assert archive_dir.is_dir()


def test_delete_sandbox_domain_requires_allow_delete_and_blocks_residues(tmp_path):
    root = tmp_path / "sandboxes"
    materialized, validation_payload = _validated_domain(root, "lifecycle_delete_blocked")

    blocked = delete_sandbox_domain(_request(DELETE_ACTION, root, validation_payload))
    assert blocked["status"] == "blocked"
    assert blocked["errors"][0]["error_code"] == "DELETE_NOT_ALLOWED"

    residue = root / materialized["domain_id"] / "undeclared.txt"
    residue.write_text("block", encoding="utf-8")
    allowed = _request(DELETE_ACTION, root, validation_payload, options={"allow_delete": True})
    result = delete_sandbox_domain(allowed)

    assert result["status"] == "blocked"
    assert result["errors"][0]["error_code"] == "UNDECLARED_PATH_BLOCKED"
    assert residue.exists()


def test_delete_sandbox_domain_deletes_only_safe_sandbox_and_is_idempotent(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    root = tmp_path / "sandboxes"
    materialized, validation_payload = _validated_domain(root, "lifecycle_delete")
    domain_dir = root / materialized["domain_id"]
    outside = root / "outside_sentinel.txt"
    outside.write_text("preserve", encoding="utf-8")

    result = delete_sandbox_domain(_request(DELETE_ACTION, root, validation_payload, options={"allow_delete": True}))

    _assert_non_operational(result)
    assert result["status"] == "deleted"
    assert result["writes_performed"] is True
    assert result["destructive_operation_performed"] is True
    assert not domain_dir.exists()
    assert outside.exists()
    assert result["delete_record"]["record_path"].startswith("_lifecycle_records/")
    assert _tree_hash(DOMAINS) == before_domains

    second = delete_sandbox_domain(_request(DELETE_ACTION, root, validation_payload, options={"allow_delete": True}))

    _assert_non_operational(second)
    assert second["status"] == "already_deleted"
    assert second["writes_performed"] is False
    assert second["destructive_operation_performed"] is False
    assert outside.exists()


def test_reset_sandbox_domain_requires_allow_reset_and_does_not_regenerate(tmp_path):
    root = tmp_path / "sandboxes"
    materialized, validation_payload = _validated_domain(root, "lifecycle_reset")
    domain_dir = root / materialized["domain_id"]

    blocked = reset_sandbox_domain(_request(RESET_ACTION, root, validation_payload))
    assert blocked["status"] == "blocked"
    assert blocked["errors"][0]["error_code"] == "RESET_NOT_ALLOWED"

    result = reset_sandbox_domain(_request(RESET_ACTION, root, validation_payload, options={"allow_reset": True}))

    _assert_non_operational(result)
    assert result["status"] == "reset"
    assert result["writes_performed"] is True
    assert result["destructive_operation_performed"] is True
    assert not domain_dir.exists()
    assert result["reset_record"]["record_path"].startswith("_lifecycle_records/")
    assert not (root / materialized["domain_id"] / "domain.json").exists()


def test_payload_flags_allowed_forbidden_and_json_safety(tmp_path):
    root = tmp_path / "sandboxes"
    _, validation_payload = _validated_domain(root, "lifecycle_payload_flags")
    result = archive_sandbox_domain(_request(ARCHIVE_ACTION, root, validation_payload))

    _assert_non_operational(result)
    assert result["allowed_actions"] == ["view_status", "view_archive_record", "request_delete_next_step"]
    assert set(FORBIDDEN_ACTIONS) <= set(result["forbidden_actions"])
    for forbidden in ("api_key", "password", "runtime_handle", "tool_config", "model_config"):
        assert forbidden not in json.dumps(result, ensure_ascii=False).lower()

    error = build_domain_lifecycle_error("RUNTIME_BLOCKED", "runtime bloqueado")
    assert set(error) == {
        "error_code",
        "message",
        "severity",
        "field",
        "recoverable",
        "user_action",
        "developer_hint",
        "blocked",
    }


def test_request_validator_is_side_effect_free(tmp_path):
    root = tmp_path / "sandboxes"
    _, validation_payload = _validated_domain(root, "lifecycle_request_validator")
    before = _tree_hash(root)

    validated = validate_domain_lifecycle_request(_request(ARCHIVE_ACTION, root, validation_payload))

    assert validated["action"] == ARCHIVE_ACTION
    assert validated["domain_id"] == validation_payload["domain_id"]
    assert _tree_hash(root) == before


def test_contract_marks_7_5_available_and_7_6_planned():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

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
        assert available[service_name]["runtime_enabled"] is False
        assert available[service_name]["execution_enabled"] is False
        assert available[service_name]["touches_operational_domains"] is False

    assert available["archive_sandbox_domain"]["destructive"] is False
    for service_name in ("rollback_sandbox", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert available[service_name]["destructive"] is True
    for service_name in ("rollback_sandbox", "archive_sandbox_domain", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert available[service_name]["requires_human_confirmation"] is True
        assert available[service_name]["requires_validation_payload"] is True
        assert available[service_name]["requires_safe_sandbox_root"] is True
        assert available[service_name]["side_effects"] is True
    assert available["stable_ui_payloads"]["available_now"] is True
    assert planned["backend_internal_ui_contract_checkpoint"]["available_now"] is False


def test_service_source_has_no_runtime_model_tool_ui_env_or_network_access():
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


def test_docs_plans_book_and_adr_record_prompt_7_5():
    docs = [DOC, PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR]
    for path in docs:
        assert path.exists(), path

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_READY",
        "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_CONTROLLED_ACTIONS_CONFIRMED",
        "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_6_stable_ui_payloads",
        "PROMPT 7.6 - Payloads estables para futura UI",
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
        "validation_payload",
        "confirmation_scope",
        "sandbox_root seguro",
        "no crea UI visual",
        "no crea endpoints publicos",
        "no toca domains operativo",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs[1:])
    for token in (
        "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
        "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_SERVICE_READY",
        "BACKEND_INTERNAL_DOMAIN_LIFECYCLE_CONTROLLED_ACTIONS_CONFIRMED",
        "ready_for_phase_7_6_stable_ui_payloads",
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
        "PROMPT 7.6 - Payloads estables para futura UI",
    ):
        assert token in combined


def test_no_operational_modules_or_temp_artifacts_were_created():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
