import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.backend_internal_materialize_sandbox_service import (
    FORBIDDEN_ACTIONS,
    SERVICE_NAME,
    SERVICE_READINESS,
    SERVICE_VERSION,
    build_materialize_sandbox_error,
    build_materialize_sandbox_request,
    materialize_sandbox,
    validate_materialize_sandbox_request,
    validate_materialize_sandbox_result,
    validate_preview_for_materialization,
)
from core.backend_internal_preview_materialization_service import preview_materialization
from core.backend_internal_ui_contract import build_backend_internal_ui_contract


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_7_3.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
CONTRACT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_materialize_sandbox_service.py"

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


def _domain_request(domain_id: str = "materialize_marketing_contenidos") -> dict:
    return {
        "domain_id": domain_id,
        "domain_name": "Materialize marketing contenidos",
        "domain_description": "Dominio sandbox materializado por backend interno.",
        "domain_type": "sandbox",
        "source": "test_fixture",
        "area_id": "marketing_publicidad",
        "niche_ids": ["contenidos_redes"],
        "business_scale": "pyme",
        "objective": "materializacion backend interno 7.3",
        "complexity_level": "media",
        "max_profiles": 2,
        "max_presets": 2,
    }


def _preview(root: Path, *, domain_id: str = "materialize_marketing_contenidos") -> dict:
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


def _confirmation(**overrides) -> dict:
    payload = {
        "confirmed": True,
        "confirmation_scope": "materialize_sandbox",
        "human_confirmation_required": True,
        "confirmed_by": "test_or_internal_caller",
        "confirmation_id": "confirm_materialize_sandbox_7_3",
    }
    payload.update(overrides)
    return payload


def _request(root: Path, **overrides) -> dict:
    preview_payload = overrides.pop("preview_payload", _preview(root))
    payload = build_materialize_sandbox_request(
        preview_payload=preview_payload,
        sandbox_root=root,
        confirmation=overrides.pop("confirmation", _confirmation()),
        materialization_options=overrides.pop("materialization_options", None),
    )
    payload.update(overrides)
    return payload


def test_materialize_sandbox_exists_and_requires_inputs(tmp_path):
    assert SERVICE_NAME == "materialize_sandbox"
    assert SERVICE_VERSION == "0.1"

    missing_request = materialize_sandbox(None)
    assert missing_request["status"] == "blocked"
    assert missing_request["errors"][0]["error_code"] == "PREVIEW_REQUIRED"

    root = tmp_path / "sandboxes"
    root.mkdir()
    missing_preview = materialize_sandbox({"sandbox_root": str(root), "confirmation": _confirmation()})
    assert missing_preview["errors"][0]["error_code"] == "PREVIEW_REQUIRED"

    preview_payload = _preview(root)
    missing_root = materialize_sandbox({"preview_payload": preview_payload, "confirmation": _confirmation()})
    assert missing_root["errors"][0]["error_code"] == "SANDBOX_ROOT_REQUIRED"


def test_materialize_sandbox_requires_explicit_confirmation(tmp_path):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)

    missing = materialize_sandbox({"preview_payload": preview_payload, "sandbox_root": str(root)})
    assert missing["errors"][0]["error_code"] == "CONFIRMATION_REQUIRED"

    wrong_scope = _request(root, preview_payload=preview_payload, confirmation=_confirmation(confirmation_scope="other"))
    assert materialize_sandbox(wrong_scope)["errors"][0]["error_code"] == "INVALID_CONFIRMATION_SCOPE"

    not_confirmed = _request(root, preview_payload=preview_payload, confirmation=_confirmation(confirmed=False))
    assert materialize_sandbox(not_confirmed)["errors"][0]["error_code"] == "CONFIRMATION_REQUIRED"


@pytest.mark.parametrize(
    "field,error_code",
    [
        ("writes_performed", "PREVIEW_ALREADY_MATERIALIZED"),
        ("materialization_performed", "PREVIEW_ALREADY_MATERIALIZED"),
        ("operational", "INVALID_PREVIEW_PAYLOAD"),
        ("runtime_enabled", "RUNTIME_BLOCKED"),
        ("execution_enabled", "EXECUTION_BLOCKED"),
    ],
)
def test_materialize_sandbox_rejects_invalid_preview_flags(tmp_path, field, error_code):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)
    preview_payload[field] = True

    result = materialize_sandbox(_request(root, preview_payload=preview_payload))

    assert result["status"] == "blocked"
    assert result["errors"][0]["error_code"] == error_code
    assert result["writes_performed"] is False
    assert result["materialization_performed"] is False


def test_materialize_sandbox_rejects_blocking_preview_errors(tmp_path):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)
    preview_payload["status"] = "blocked"
    preview_payload["errors"] = [build_materialize_sandbox_error("INVALID_PREVIEW_PAYLOAD", "bloqueante")]

    result = materialize_sandbox(_request(root, preview_payload=preview_payload))

    assert result["status"] == "blocked"
    assert result["errors"][0]["error_code"] in {"INVALID_PREVIEW_PAYLOAD", "PREVIEW_HAS_BLOCKING_ERRORS"}


def test_materialize_sandbox_rejects_unsafe_roots_and_paths(tmp_path):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)

    assert materialize_sandbox(_request(root, sandbox_root=str(DOMAINS), preview_payload=preview_payload))["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    assert materialize_sandbox(_request(root, sandbox_root=str(ROOT), preview_payload=preview_payload))["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    missing_root = tmp_path / "missing"
    assert materialize_sandbox(_request(root, sandbox_root=str(missing_root), preview_payload=preview_payload))["errors"][0]["error_code"] == "SANDBOX_ROOT_NOT_FOUND"

    traversal_preview = deepcopy(preview_payload)
    traversal_preview["planned_paths"][0]["relative_path"] = "../escape"
    assert materialize_sandbox(_request(root, preview_payload=traversal_preview))["errors"][0]["error_code"] == "PATH_TRAVERSAL_BLOCKED"

    domains_preview = deepcopy(preview_payload)
    domains_preview["planned_paths"][0]["relative_path"] = "domains/loteria"
    assert materialize_sandbox(_request(root, preview_payload=domains_preview))["errors"][0]["error_code"] == "DOMAINS_OPERATIVE_PATH_BLOCKED"


def test_materialize_sandbox_rejects_preview_for_other_sandbox_root(tmp_path):
    first_root = tmp_path / "sandboxes_a"
    second_root = tmp_path / "sandboxes_b"
    second_root.mkdir()
    preview_payload = _preview(first_root)

    request = _request(first_root, preview_payload=preview_payload, sandbox_root=str(second_root))
    result = materialize_sandbox(request)

    assert result["status"] == "blocked"
    assert result["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"


def test_materialize_sandbox_validates_request_without_writes(tmp_path):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)
    before = _tree_hash(root)
    validated = validate_materialize_sandbox_request(_request(root, preview_payload=preview_payload))

    assert validated["sandbox_root"] == str(root.resolve())
    assert validated["confirmation"]["confirmation_scope"] == "materialize_sandbox"
    assert _tree_hash(root) == before
    assert validate_preview_for_materialization(preview_payload, sandbox_root=root)["preview_payload"]


def test_materialize_sandbox_materializes_complete_controlled_chain(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)

    result = materialize_sandbox(_request(root, preview_payload=preview_payload))

    assert validate_materialize_sandbox_result(result) == result
    assert result["service"] == SERVICE_NAME
    assert result["status"] == "materialized"
    assert result["readiness"] == SERVICE_READINESS
    assert result["domain_id"] == "materialize_marketing_contenidos"
    assert result["materialization_id"].startswith("mat_materialize_marketing_contenidos_")
    assert result["writes_performed"] is True
    assert result["materialization_performed"] is True
    assert result["operational"] is False
    assert result["passed"] is False
    assert result["runtime_enabled"] is False
    assert result["execution_enabled"] is False

    domain_dir = root / result["domain_id"]
    assert (domain_dir / "domain.json").is_file()
    assert (domain_dir / "materialization_manifest.json").is_file()
    assert (domain_dir / "manifests" / "artifact_manifest.json").is_file()
    assert (domain_dir / "profile_catalog" / "profile_catalog.json").is_file()
    assert (domain_dir / "agent_presets" / "agent_presets.json").is_file()
    assert (domain_dir / "paper_seed" / "paper_seed.json").is_file()
    assert list((domain_dir / "sandbox_agents").glob("*.json"))
    assert (domain_dir / "sandbox_teams" / f"{result['domain_id']}_team.json").is_file()

    created = {Path(path).as_posix() for path in result["created_paths"]}
    assert f"{result['domain_id']}/domain.json" in created
    assert any(path.endswith("manifests/artifact_manifest.json") for path in created)
    assert any(path.endswith("profile_catalog/profile_catalog.json") for path in created)
    assert any(path.endswith("agent_presets/agent_presets.json") for path in created)
    assert any(path.endswith("paper_seed/paper_seed.json") for path in created)
    assert any("/sandbox_agents/" in path for path in created)
    assert any("/sandbox_teams/" in path for path in created)

    assert result["artifact_summary"]["artifact_count"] >= 6
    assert {"profile_catalog", "agent_preset", "paper_seed", "agent", "team"} <= set(result["artifact_summary"]["artifact_types"])
    assert result["artifact_summary"]["non_operational"] is True
    assert result["artifact_summary"]["passed_false"] is True
    assert result["artifact_manifest"]["domain_id"] == result["domain_id"]
    assert result["lineage_summary"]["preview_id"] == preview_payload["domain_preview"]["preview_id"]
    assert result["dependencies_summary"]["dependencies_declared"] is True
    assert result["read_models_summary"]["read_model"] == "sandbox_team_internal_listing"
    assert result["read_models_summary"]["teams_count"] == 1
    assert result["rollback_prepared"] is True
    assert result["rollback_scope"] == "sandbox_domain_integral"
    assert result["rollback_plan_available"] is True
    assert result["rollback_plan_summary"]["planned_paths_count"] >= len(result["created_paths"])
    assert result["rollback_plan_summary"]["all_paths_inside_sandbox_root"] is True
    assert result["rollback_plan_summary"]["operational_domains_blocked"] is True
    assert _tree_hash(DOMAINS) == before_domains


def test_materialize_sandbox_actions_and_error_contract_are_conservative(tmp_path):
    root = tmp_path / "sandboxes"
    result = materialize_sandbox(_request(root))

    for allowed in (
        "view_status",
        "view_details",
        "view_audit_pack_summary",
        "request_validation_next_step",
        "request_rollback_next_step",
    ):
        assert allowed in result["allowed_actions"]
    for disallowed in ("execute", "activate_runtime", "invoke_models", "call_tools", "delete_without_confirmation"):
        assert disallowed not in result["allowed_actions"]
    for forbidden in FORBIDDEN_ACTIONS:
        assert forbidden in result["forbidden_actions"]

    error = build_materialize_sandbox_error("RUNTIME_BLOCKED", "runtime bloqueado")
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


def test_materialize_sandbox_result_is_json_safe_and_blocks_secrets(tmp_path):
    root = tmp_path / "sandboxes"
    result = materialize_sandbox(_request(root))
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True)

    assert encoded
    for forbidden in ("api_key", "password", "runtime_handle", "tool_config", "model_config"):
        assert forbidden not in encoded.lower()

    broken = deepcopy(result)
    broken["api_secret"] = "blocked"
    with pytest.raises(ValueError, match="sensible"):
        validate_materialize_sandbox_result(broken)


def test_materialize_sandbox_blocks_overwrite_by_default(tmp_path):
    root = tmp_path / "sandboxes"
    preview_payload = _preview(root)
    first = materialize_sandbox(_request(root, preview_payload=preview_payload))
    assert first["status"] == "materialized"

    second_preview = _preview(root)
    result = materialize_sandbox(_request(root, preview_payload=second_preview))
    assert result["status"] == "blocked"
    assert result["errors"][0]["error_code"] == "OVERWRITE_BLOCKED"


def test_contract_marks_materialize_available_and_future_services_planned():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert available["list_domains_status"]["available_now"] is True
    assert available["preview_materialization"]["available_now"] is True
    assert available["materialize_sandbox"]["available_now"] is True
    assert available["materialize_sandbox"]["type"] == "controlled-write"
    assert available["materialize_sandbox"]["side_effects"] is True
    assert available["materialize_sandbox"]["requires_human_confirmation"] is True
    assert available["materialize_sandbox"]["requires_valid_preview"] is True
    assert available["materialize_sandbox"]["prepares_rollback"] is True
    assert available["materialize_sandbox"]["public_endpoint"] is False
    assert available["materialize_sandbox"]["touches_visual_ui"] is False
    assert available["materialize_sandbox"]["runtime_enabled"] is False
    assert available["materialize_sandbox"]["execution_enabled"] is False
    assert available["materialize_sandbox"]["touches_operational_domains"] is False
    assert available["validate_domain"]["available_now"] is True
    assert available["validate_domain"]["type"] == "read-only-validation"
    assert available["validate_domain"]["side_effects"] is False

    for lifecycle in ("rollback_sandbox", "archive_sandbox_domain", "delete_sandbox_domain", "reset_sandbox_domain"):
        assert available[lifecycle]["available_now"] is True
        assert available[lifecycle]["requires_human_confirmation"] is True
        assert available[lifecycle]["requires_validation_payload"] is True
        assert available[lifecycle]["requires_safe_sandbox_root"] is True
    assert planned["stable_ui_payloads"]["available_now"] is False


def test_service_source_has_no_runtime_model_tool_ui_or_env_access():
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


def test_docs_plans_book_and_adr_record_prompt_7_3():
    for path in (DOC, PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR, MODULE):
        assert path.exists()

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_READY",
        "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_CONTROLLED_WRITE_CONFIRMED",
        "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_4_validate_domain_service",
        "PROMPT 7.4 - Servicio interno validate_domain",
        "preview_materialization",
        "confirmation",
        "rollback_prepared=true",
        "controlled-write",
        "no crea UI visual",
        "no crea endpoints publicos",
    ):
        assert token in doc

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR)
    )
    for token in (
        "PROMPT 7.3 - Servicio interno materialize_sandbox",
        "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_SERVICE_READY",
        "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_CONTROLLED_WRITE_CONFIRMED",
        "BACKEND_INTERNAL_MATERIALIZE_SANDBOX_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_4_validate_domain_service",
        "materialize_sandbox",
        "controlled-write",
        "available_now=true",
        "requires_valid_preview=true",
        "prepares_rollback=true",
        "PROMPT 7.4 - Servicio interno validate_domain",
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


def test_prompt_7_3_does_not_create_operational_modules_or_temporals():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
