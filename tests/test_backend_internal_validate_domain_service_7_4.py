import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.backend_internal_materialize_sandbox_service import (
    build_materialize_sandbox_request,
    materialize_sandbox,
)
from core.backend_internal_preview_materialization_service import preview_materialization
from core.backend_internal_ui_contract import build_backend_internal_ui_contract
from core.backend_internal_validate_domain_service import (
    FORBIDDEN_ACTIONS,
    SERVICE_NAME,
    SERVICE_READINESS,
    SERVICE_VERSION,
    build_validate_domain_error,
    build_validate_domain_request,
    validate_domain,
    validate_domain_validation_payload,
    validate_validate_domain_request,
)


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_7_4.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
CONTRACT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_validate_domain_service.py"

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


def _domain_request(domain_id: str = "validate_marketing_contenidos") -> dict:
    return {
        "domain_id": domain_id,
        "domain_name": "Validate marketing contenidos",
        "domain_description": "Dominio sandbox validado por backend interno.",
        "domain_type": "sandbox",
        "source": "test_fixture",
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "business_scale": "pyme",
        "objective": "validacion backend interno 7.4",
        "complexity_level": "media",
        "max_profiles": 2,
        "max_presets": 2,
    }


def _preview(root: Path, *, domain_id: str = "validate_marketing_contenidos") -> dict:
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


def _confirmation() -> dict:
    return {
        "confirmed": True,
        "confirmation_scope": "materialize_sandbox",
        "human_confirmation_required": True,
        "confirmed_by": "test_or_internal_caller",
        "confirmation_id": "confirm_validate_domain_7_4",
    }


def _materialized(root: Path, *, domain_id: str = "validate_marketing_contenidos") -> dict:
    preview_payload = _preview(root, domain_id=domain_id)
    request = build_materialize_sandbox_request(
        preview_payload=preview_payload,
        sandbox_root=root,
        confirmation=_confirmation(),
    )
    result = materialize_sandbox(request)
    assert result["status"] == "materialized"
    return result


def _validate_request(root: Path, materialized: dict | None = None) -> dict:
    materialized = materialized or _materialized(root)
    return build_validate_domain_request(
        sandbox_root=root,
        domain_id=materialized["domain_id"],
        materialization_id=materialized["materialization_id"],
    )


def test_validate_domain_exists_and_requires_inputs(tmp_path):
    assert SERVICE_NAME == "validate_domain"
    assert SERVICE_VERSION == "0.1"

    missing_request = validate_domain(None)
    assert missing_request["status"] == "blocked"
    assert missing_request["errors"][0]["error_code"] == "VALIDATION_REQUEST_REQUIRED"

    root = tmp_path / "sandboxes"
    root.mkdir()
    missing_root = validate_domain({"domain_id": "missing_domain"})
    assert missing_root["errors"][0]["error_code"] == "SANDBOX_ROOT_REQUIRED"

    missing_domain = validate_domain({"sandbox_root": str(root)})
    assert missing_domain["errors"][0]["error_code"] == "DOMAIN_ID_REQUIRED"


def test_validate_domain_validates_materialized_sandbox_without_writes(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    root = tmp_path / "sandboxes"
    materialized = _materialized(root)
    before = _tree_hash(root)

    payload = validate_domain(_validate_request(root, materialized))

    assert validate_domain_validation_payload(payload) == payload
    assert _tree_hash(root) == before
    assert _tree_hash(DOMAINS) == before_domains
    assert payload["service"] == SERVICE_NAME
    assert payload["status"] == "validated"
    assert payload["readiness"] == SERVICE_READINESS
    assert payload["domain_id"] == materialized["domain_id"]
    assert payload["materialization_id"] == materialized["materialization_id"]
    assert payload["validation_scope"] == "sandbox_domain_materialization"
    assert payload["valid"] is True
    assert payload["operational"] is False
    assert payload["passed"] is False
    assert payload["runtime_enabled"] is False
    assert payload["execution_enabled"] is False
    assert payload["writes_performed"] is False
    assert payload["materialization_performed"] is False
    assert payload["rollback_performed"] is False
    assert payload["regeneration_performed"] is False

    assert payload["domain_validation"]["schema_valid"] is True
    assert payload["artifact_manifest_validation"]["present"] is True
    assert payload["created_paths_validation"]["all_paths_inside_sandbox_root"] is True
    assert payload["lineage_validation"]["dependencies_coherent"] is True
    assert {item["artifact_kind"] for item in payload["artifact_validations"]} >= {
        "profile_catalog",
        "agent_presets",
        "paper_seed",
        "sandbox_agents",
        "sandbox_team",
    }
    assert payload["read_models_validation"]["valid"] is True
    assert payload["rollback_readiness"]["ready"] is True
    assert payload["rollback_readiness"]["executed"] is False
    assert payload["audit_pack_validation"]["optional"] is True
    json.dumps(payload, ensure_ascii=False)


def test_validate_domain_actions_and_error_contract_are_conservative(tmp_path):
    root = tmp_path / "sandboxes"
    payload = validate_domain(_validate_request(root))

    assert not {"execute", "activate_runtime", "invoke_models", "call_tools", "delete_without_confirmation"} & set(payload["allowed_actions"])
    assert {"activate_runtime", "execute_agents", "invoke_models", "call_tools", "use_integrations"} <= set(payload["forbidden_actions"])
    assert set(FORBIDDEN_ACTIONS) <= set(payload["forbidden_actions"])

    error = build_validate_domain_error("RUNTIME_BLOCKED", "runtime bloqueado")
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
    assert error["blocked"] is True


def test_validate_domain_blocks_unsafe_roots_and_path_traversal(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()

    assert validate_domain({"sandbox_root": str(DOMAINS), "domain_id": "valid_domain"})["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    assert validate_domain({"sandbox_root": str(ROOT), "domain_id": "valid_domain"})["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    assert validate_domain({"sandbox_root": str(tmp_path / "missing"), "domain_id": "valid_domain"})["errors"][0]["error_code"] == "SANDBOX_ROOT_NOT_FOUND"
    assert validate_domain({"sandbox_root": str(root), "domain_id": "../escape"})["errors"][0]["error_code"] == "INVALID_VALIDATE_DOMAIN_REQUEST"


def test_validate_domain_handles_domain_and_materialization_mismatch(tmp_path):
    root = tmp_path / "sandboxes"
    _materialized(root)

    missing = validate_domain(build_validate_domain_request(sandbox_root=root, domain_id="missing_domain"))
    assert missing["status"] == "blocked"
    assert missing["errors"][0]["error_code"] == "DOMAIN_NOT_FOUND"

    wrong_materialization = validate_domain(
        build_validate_domain_request(
            sandbox_root=root,
            domain_id="validate_marketing_contenidos",
            materialization_id="mat_wrong",
        )
    )
    assert wrong_materialization["valid"] is False
    assert any(error["error_code"] == "DOMAIN_ID_MISMATCH" for error in wrong_materialization["errors"])


def test_validate_domain_handles_missing_or_inconsistent_manifest(tmp_path):
    root = tmp_path / "sandboxes"
    materialized = _materialized(root)
    domain_dir = root / materialized["domain_id"]

    manifest_path = domain_dir / "manifests" / "artifact_manifest.json"
    original = manifest_path.read_text(encoding="utf-8")
    manifest_path.unlink()
    missing = validate_domain(_validate_request(root, materialized))
    assert any(error["error_code"] == "MISSING_ARTIFACT_MANIFEST" for error in missing["errors"])

    manifest_path.write_text(original, encoding="utf-8")
    manifest = json.loads(original)
    manifest["domain_id"] = "other_domain"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    inconsistent = validate_domain(_validate_request(root, materialized))
    assert any(error["error_code"] == "INCONSISTENT_ARTIFACT_MANIFEST" for error in inconsistent["errors"])


def test_validate_domain_handles_unsafe_created_paths_and_invalid_read_model(tmp_path):
    root = tmp_path / "sandboxes"
    materialized = _materialized(root)
    domain_dir = root / materialized["domain_id"]
    materialization_manifest_path = domain_dir / "materialization_manifest.json"
    manifest = json.loads(materialization_manifest_path.read_text(encoding="utf-8"))
    manifest["created_paths"].append(str(ROOT / "core" / "unsafe.py"))
    materialization_manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    unsafe = validate_domain(_validate_request(root, materialized))
    assert any(error["error_code"] == "UNSAFE_CREATED_PATH" for error in unsafe["errors"])

    team_path = next((domain_dir / "sandbox_teams").glob("*.json"))
    team = json.loads(team_path.read_text(encoding="utf-8"))
    team["execution_policy"]["execution_enabled"] = True
    team_path.write_text(json.dumps(team), encoding="utf-8")
    invalid = validate_domain(_validate_request(root, materialized))
    assert any(error["error_code"] == "INVALID_READ_MODEL" for error in invalid["errors"])


@pytest.mark.parametrize(
    "field",
    [
        "operational",
        "runtime_enabled",
        "execution_enabled",
        "writes_performed",
        "materialization_performed",
        "rollback_performed",
        "regeneration_performed",
    ],
)
def test_validate_domain_payload_validator_rejects_operational_flags(tmp_path, field):
    root = tmp_path / "sandboxes"
    payload = validate_domain(_validate_request(root))
    broken = deepcopy(payload)
    broken[field] = True

    with pytest.raises(ValueError):
        validate_domain_validation_payload(broken)


def test_validate_domain_payload_validator_blocks_secret_like_fields(tmp_path):
    root = tmp_path / "sandboxes"
    payload = validate_domain(_validate_request(root))
    broken = deepcopy(payload)
    broken["api_secret"] = "blocked"

    with pytest.raises(ValueError):
        validate_domain_validation_payload(broken)

    request = build_validate_domain_request(sandbox_root=root, domain_id="missing_domain")
    request["api_secret"] = "blocked"
    result = validate_domain(request)
    assert result["errors"][0]["error_code"] == "SECRET_LIKE_FIELD_BLOCKED"


def test_validate_domain_request_validator_is_read_only(tmp_path):
    root = tmp_path / "sandboxes"
    materialized = _materialized(root)
    request = _validate_request(root, materialized)
    before = _tree_hash(root)

    validated = validate_validate_domain_request(request)

    assert validated["sandbox_root"] == str(root.resolve())
    assert validated["domain_id"] == materialized["domain_id"]
    assert _tree_hash(root) == before


def test_contract_marks_validate_available_and_future_services_planned():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert available["list_domains_status"]["available_now"] is True
    assert available["preview_materialization"]["available_now"] is True
    assert available["materialize_sandbox"]["available_now"] is True
    assert available["validate_domain"]["available_now"] is True
    assert available["validate_domain"]["type"] == "read-only-validation"
    assert available["validate_domain"]["side_effects"] is False
    assert available["validate_domain"]["requires_human_confirmation"] is False
    assert available["validate_domain"]["destructive"] is False
    assert available["validate_domain"]["public_endpoint"] is False
    assert available["validate_domain"]["touches_visual_ui"] is False
    assert available["validate_domain"]["runtime_enabled"] is False
    assert available["validate_domain"]["execution_enabled"] is False
    assert available["validate_domain"]["writes_performed"] is False
    assert available["validate_domain"]["materialization_performed"] is False
    for future in ("rollback_sandbox", "archive_domain", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert planned[future]["available_now"] is False


def test_service_source_has_no_runtime_model_tool_ui_env_or_write_calls():
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
    assert ".unlink(" not in source
    assert "rollback_sandbox_domain_integral(" not in source
    assert "rollback_domain_materialization(" not in source


def test_docs_plans_book_and_adr_record_validate_domain_7_4():
    docs = [DOC, PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR]
    for path in docs:
        assert path.exists(), path
    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_READY",
        "BACKEND_INTERNAL_VALIDATE_DOMAIN_READ_ONLY_CONFIRMED",
        "BACKEND_INTERNAL_VALIDATE_DOMAIN_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_5_rollback_archive_delete_reset_service",
        "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
        "read-only",
        "no escribe",
        "no materializa",
        "no hace rollback",
    ):
        assert token in doc

    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs[1:])
    for token in (
        "PROMPT 7.4 - Servicio interno validate_domain",
        "BACKEND_INTERNAL_VALIDATE_DOMAIN_SERVICE_READY",
        "ready_for_phase_7_5_rollback_archive_delete_reset_service",
        "validate_domain",
        "read-only-validation",
        "available_now=true",
        "PROMPT 7.5 - Servicio interno rollback/archive/delete/reset",
    ):
        assert token in combined


def test_no_operational_modules_or_temp_artifacts_were_created():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (ROOT / "memoria_agentes" / "test_agent").exists()
    assert not (ROOT / "memoria_agentes" / "test_agent_context").exists()
