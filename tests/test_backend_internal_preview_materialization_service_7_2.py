import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.backend_internal_preview_materialization_service import (
    FORBIDDEN_ACTIONS,
    SERVICE_NAME,
    SERVICE_READINESS,
    SERVICE_VERSION,
    build_materialization_preview,
    build_preview_materialization_error,
    preview_materialization,
    validate_materialization_preview_payload,
)
from core.backend_internal_ui_contract import build_backend_internal_ui_contract


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_7_2.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
CONTRACT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_preview_materialization_service.py"

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


def _snapshot_tree(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def _request(root: Path, **overrides) -> dict:
    domain_request = {
        "domain_id": "preview_marketing_contenidos",
        "domain_name": "Preview marketing contenidos",
        "domain_description": "Dominio sandbox de preview no operativo.",
        "domain_type": "sandbox",
        "source": "test_fixture",
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "business_scale": "pyme",
        "objective": "preview backend interno",
        "complexity_level": "media",
        "max_profiles": 2,
        "max_presets": 2,
    }
    domain_request.update(overrides.pop("domain_request", {}))
    payload = {
        "domain_request": domain_request,
        "sandbox_root": str(root),
        "preview_options": {
            "include_team_preview": True,
            "include_audit_pack_preview": True,
            "include_paths_preview": True,
            "include_manifest_preview": True,
        },
    }
    payload.update(overrides)
    return payload


def test_preview_materialization_exists_and_requires_inputs(tmp_path):
    missing_request = preview_materialization(None)
    assert missing_request["status"] == "blocked"
    assert missing_request["errors"][0]["error_code"] == "DOMAIN_REQUEST_REQUIRED"

    root = tmp_path / "sandboxes"
    root.mkdir()
    missing_domain = preview_materialization({"sandbox_root": str(root)})
    assert missing_domain["errors"][0]["error_code"] == "DOMAIN_REQUEST_REQUIRED"

    missing_root = preview_materialization({"domain_request": _request(root)["domain_request"]})
    assert missing_root["errors"][0]["error_code"] == "SANDBOX_ROOT_REQUIRED"


def test_preview_materialization_payload_is_json_safe_and_no_operational(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)

    assert payload["service"] == SERVICE_NAME
    assert payload["service_version"] == SERVICE_VERSION
    assert payload["status"] == "ready"
    assert payload["readiness"] == SERVICE_READINESS
    assert payload["sandbox_root"] == str(root.resolve())
    assert payload["domain_request"]["domain_id"] == "preview_marketing_contenidos"
    assert payload["domain_preview"]
    assert payload["planned_artifacts"]
    assert payload["planned_paths"]
    assert payload["planned_manifests"]
    assert payload["planned_lineage"]
    assert payload["planned_dependencies"]
    assert payload["planned_read_models"]
    assert payload["planned_audit_pack"]
    assert payload["warnings"] == []
    assert payload["errors"] == []
    assert payload["validation"]["json_safe"] is True
    assert payload["operational"] is False
    assert payload["runtime_enabled"] is False
    assert payload["execution_enabled"] is False
    assert payload["writes_performed"] is False
    assert payload["materialization_performed"] is False
    assert encoded


def test_preview_reuses_canonical_domain_preview_without_writes(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    request = _request(root)
    before_domains = _tree_hash(DOMAINS)
    before_sandbox = _snapshot_tree(root)

    preview = build_materialization_preview(domain_request=request["domain_request"])
    payload = preview_materialization(request)

    assert preview["artifact_type"] == "domain_materialization_preview"
    assert payload["domain_preview"]["preview_id"] == preview["preview_id"]
    assert _tree_hash(DOMAINS) == before_domains
    assert _snapshot_tree(root) == before_sandbox
    assert not (root / request["domain_request"]["domain_id"]).exists()


def test_planned_artifacts_are_supported_preview_only_and_non_operational(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    kinds = {artifact["artifact_kind"] for artifact in payload["planned_artifacts"]}

    assert {
        "sandbox_domain",
        "artifact_manifest",
        "derived_domain_profile_catalog",
        "derived_domain_agent_presets",
        "derived_paper_seed",
        "sandbox_agent",
        "sandbox_team",
        "sandbox_team_internal_listing",
        "sandbox_materialization_audit_pack",
    } <= kinds
    for artifact in payload["planned_artifacts"]:
        assert artifact["artifact_id"].startswith("preview_")
        assert artifact["planned_path"]
        assert artifact["created_from"]["preview_only"] is True
        assert artifact["operational"] is False
        assert artifact["passed"] is False
        assert artifact["runtime_enabled"] is False
        assert artifact["execution_enabled"] is False


def test_planned_paths_are_relative_safe_and_not_created(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    before_sandbox = _snapshot_tree(root)

    payload = preview_materialization(_request(root))

    assert _snapshot_tree(root) == before_sandbox
    for item in payload["planned_paths"]:
        assert item["operation"] == "would_create"
        assert item["safe"] is True
        assert item["under_sandbox_root"] is True
        relative = item["relative_path"]
        assert not Path(relative).is_absolute()
        assert ".." not in Path(relative).parts
        assert not relative.replace("\\", "/").startswith("domains/")
        assert not (root / relative).exists()


def test_planned_manifests_lineage_dependencies_are_declarative(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))

    for manifest in payload["planned_manifests"]:
        assert manifest["materialization_id_policy"] == "generated_on_materialization"
        assert manifest["operational"] is False
        assert manifest["passed"] is False
    assert payload["planned_lineage"]["lineage_status"] == "preview_only"
    assert payload["planned_lineage"]["materialization_id_policy"] == "generated_on_materialization"
    assert payload["planned_lineage"]["operational"] is False
    assert payload["planned_dependencies"]
    assert all(dependency["declarative"] is True for dependency in payload["planned_dependencies"])


def test_allowed_forbidden_and_next_actions_are_conservative(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))

    assert payload["allowed_actions"] == [
        "view_preview",
        "view_planned_artifacts",
        "view_planned_paths",
        "view_warnings",
        "request_materialization_next_step",
    ]
    assert payload["next_actions"] == ["request_materialization_next_step"]
    for forbidden in (
        "execute_preview",
        "persist_preview",
        "activate_runtime",
        "execute_agents",
        "invoke_models",
        "call_tools",
        "use_integrations",
        "write_operational_outputs",
        "materialize_without_confirmation",
        "rollback_without_materialization",
        "delete_without_confirmation",
        "regenerate_without_rollback",
    ):
        assert forbidden in payload["forbidden_actions"]
    assert not any(action in payload["allowed_actions"] for action in ("materialize", "execute", "rollback", "delete", "regenerate"))


def test_service_blocks_unsafe_roots_and_path_traversal(tmp_path):
    assert preview_materialization(_request(DOMAINS))["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    assert preview_materialization(_request(ROOT))["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    assert preview_materialization(_request(ROOT / "core"))["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    missing = tmp_path / "missing"
    assert preview_materialization(_request(missing))["errors"][0]["error_code"] == "SANDBOX_ROOT_NOT_FOUND"

    root = tmp_path / "sandboxes"
    root.mkdir()
    request = _request(root, domain_request={"domain_id": "../bad"})
    assert preview_materialization(request)["errors"][0]["error_code"] == "PATH_TRAVERSAL_BLOCKED"


def test_invalid_domain_request_is_controlled(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    invalid_type = _request(root, domain_request={"domain_type": "active"})
    assert preview_materialization(invalid_type)["errors"][0]["error_code"] == "INVALID_DOMAIN_REQUEST"

    missing_area = _request(root, domain_request={"area_id": ""})
    assert preview_materialization(missing_area)["errors"][0]["error_code"] == "INVALID_DOMAIN_REQUEST"


def test_unsupported_planned_artifact_is_controlled_warning(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    request = _request(root)
    request["preview_options"]["requested_artifact_kinds"] = ["unsupported_runtime_worker"]

    payload = preview_materialization(request)

    assert payload["warnings"][0]["error_code"] == "READINESS_NOT_MET"
    assert "unsupported_runtime_worker" in payload["warnings"][0]["message"]
    assert payload["status"] == "ready"


@pytest.mark.parametrize(
    "field",
    ["operational", "runtime_enabled", "execution_enabled", "writes_performed", "materialization_performed"],
)
def test_validator_rejects_operational_or_write_flags(tmp_path, field):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    payload[field] = True

    with pytest.raises(ValueError, match=field):
        validate_materialization_preview_payload(payload)


def test_validator_rejects_secret_like_field(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    payload["api_secret"] = "blocked"

    with pytest.raises(ValueError, match="sensible"):
        validate_materialization_preview_payload(payload)


def test_validator_rejects_destructive_allowed_action(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    payload["allowed_actions"].append("materialize")

    with pytest.raises(ValueError, match="allowed_actions"):
        validate_materialization_preview_payload(payload)


def test_validator_rejects_unsafe_planned_path(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    payload["planned_paths"][0]["relative_path"] = "../escape"

    with pytest.raises(ValueError, match="planned_path"):
        validate_materialization_preview_payload(payload)


def test_request_with_secret_like_field_is_blocked(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    request = _request(root)
    request["domain_request"]["api_secret"] = "blocked"

    payload = preview_materialization(request)

    assert payload["status"] == "blocked"
    assert payload["errors"][0]["error_code"] == "SECRET_LIKE_FIELD_BLOCKED"


def test_error_builder_uses_expected_shape():
    error = build_preview_materialization_error("RUNTIME_BLOCKED", "runtime bloqueado")

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


def test_contract_marks_preview_available_and_future_services_planned():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert available["list_domains_status"]["available_now"] is True
    assert available["preview_materialization"]["available_now"] is True
    assert available["preview_materialization"]["type"] == "read-only-preview"
    assert available["preview_materialization"]["side_effects"] is False
    assert available["preview_materialization"]["writes_performed"] is False
    assert available["preview_materialization"]["materialization_performed"] is False
    assert available["preview_materialization"]["public_endpoint"] is False
    assert available["preview_materialization"]["touches_visual_ui"] is False
    assert available["preview_materialization"]["runtime_enabled"] is False
    assert available["preview_materialization"]["execution_enabled"] is False
    assert available["materialize_sandbox"]["available_now"] is True
    assert available["materialize_sandbox"]["type"] == "controlled-write"
    assert available["materialize_sandbox"]["requires_human_confirmation"] is True
    for lifecycle in (
        "rollback_sandbox",
        "archive_sandbox_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
    ):
        assert available[lifecycle]["available_now"] is True
        assert available[lifecycle]["requires_human_confirmation"] is True
        assert available[lifecycle]["requires_validation_payload"] is True
        assert available[lifecycle]["requires_safe_sandbox_root"] is True
    assert available["stable_ui_payloads"]["available_now"] is True
    assert planned["backend_internal_ui_contract_checkpoint"]["available_now"] is False


def test_service_does_not_access_env_network_models_tools_or_ui_runtime():
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


def test_docs_plans_book_and_adr_record_prompt_7_2():
    for path in (DOC, PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR, MODULE):
        assert path.exists()

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_READY",
        "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_WRITE_CONFIRMED",
        "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_3_materialize_sandbox_service",
        "PROMPT 7.3 - Servicio interno materialize_sandbox",
        "preview_materialization",
        "planned_artifacts",
        "planned_paths",
        "planned_manifests",
        "DOMAIN_REQUEST_REQUIRED",
        "WRITE_OPERATION_BLOCKED",
        "no crea UI visual",
        "no crea endpoints publicos",
    ):
        assert token in doc

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR)
    )
    for token in (
        "PROMPT 7.2 - Servicio interno preview_materialization",
        "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_SERVICE_READY",
        "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_WRITE_CONFIRMED",
        "BACKEND_INTERNAL_PREVIEW_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_3_materialize_sandbox_service",
        "preview_materialization",
        "available_now=true",
        "PROMPT 7.3 - Servicio interno materialize_sandbox",
        "list_domains_status",
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
    ):
        assert token in combined


def test_prompt_7_2_does_not_create_operational_modules_or_temporals():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()


def test_payload_copy_validation_prevents_mutating_input(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()
    payload = preview_materialization(_request(root))
    original = deepcopy(payload)
    validated = validate_materialization_preview_payload(payload)

    assert validated == original
    assert validated is not payload
