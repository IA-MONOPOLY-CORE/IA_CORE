import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.agent_preset_materializer import materialize_agent_presets
from core.backend_internal_domain_status_service import (
    DOMAIN_BLOCKED_READINESS,
    DOMAIN_LISTABLE_READINESS,
    ERROR_CODES,
    FORBIDDEN_ACTIONS,
    SERVICE_NAME,
    SERVICE_READINESS,
    SERVICE_VERSION,
    build_domain_status_error,
    get_domain_status_summary,
    list_domains_status,
    validate_domain_status_payload,
)
from core.backend_internal_ui_contract import build_backend_internal_ui_contract
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog
from core.sandbox_agent_materializer import materialize_sandbox_agent
from core.sandbox_domain_schema import validate_sandbox_domain_schema
from core.sandbox_team_materializer import materialize_sandbox_team_from_template


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"
DOC = ROOT / "docs" / "BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_7_1.md"
PHASE_7_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md"
CONTRACT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_7_0.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
MODULE = ROOT / "core" / "backend_internal_domain_status_service.py"

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


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="domain status service 7.1",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )


def _schema_from_preview(preview: dict) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    return validate_sandbox_domain_schema(schema)


def _domain_only(tmp_path) -> dict:
    return materialize_sandbox_domain(
        _schema_from_preview(_preview()),
        sandbox_root=tmp_path / "sandboxes",
    )


def _team_template() -> dict:
    return {
        "schema_version": "1.0",
        "artifact_type": "derived_professional_team_template",
        "team_template": {
            "team_template_id": "sandbox_marketing_crm_automation_equipo_growth_ventas",
            "nombre": "Equipo de growth y ventas",
            "descripcion": "Plantilla derivada para listar estado interno.",
            "recommended_domain_profile_ids": [
                "perfil_estratega_growth",
                "perfil_especialista_conversion",
            ],
            "recommended_profile_ids": [
                "estratega_growth",
                "especialista_conversion",
            ],
            "required_team_roles": ["estratega", "especialista"],
            "expected_outputs": ["Plan comercial declarativo."],
            "generated_from": {"generator": "core.professional_team_template_generator"},
            "status": "derived",
            "warnings": [],
        },
    }


def _full_domain_with_team(tmp_path) -> dict:
    domain = _domain_only(tmp_path)
    domain_dir = Path(domain["domain_dir"])
    materialize_profile_catalog(domain_dir)
    presets = materialize_agent_presets(domain_dir)
    materialize_paper_seed(domain_dir)
    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    for preset in presets_payload["presets"]:
        materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
    materialize_sandbox_team_from_template(domain_dir, team_template=_team_template())
    return domain


def test_list_domains_status_requires_explicit_sandbox_root():
    payload = list_domains_status()

    assert payload["service"] == SERVICE_NAME
    assert payload["status"] == "blocked"
    assert payload["errors"][0]["error_code"] == "SANDBOX_ROOT_REQUIRED"
    assert payload["operational"] is False
    assert payload["runtime_enabled"] is False
    assert payload["execution_enabled"] is False


def test_missing_sandbox_root_returns_controlled_error(tmp_path):
    payload = list_domains_status(sandbox_root=tmp_path / "missing")

    assert payload["status"] == "blocked"
    assert payload["errors"][0]["error_code"] == "SANDBOX_ROOT_NOT_FOUND"
    assert payload["summary"]["domains_count"] == 0


def test_unsafe_sandbox_root_blocks_operational_domains():
    payload = list_domains_status(sandbox_root=DOMAINS)

    assert payload["status"] == "blocked"
    assert payload["errors"][0]["error_code"] == "UNSAFE_SANDBOX_ROOT"
    assert payload["domains"] == []


def test_empty_controlled_sandbox_root_is_json_safe(tmp_path):
    root = tmp_path / "sandboxes"
    root.mkdir()

    payload = validate_domain_status_payload(list_domains_status(sandbox_root=root))
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)

    assert encoded
    assert payload["service"] == SERVICE_NAME
    assert payload["service_version"] == SERVICE_VERSION
    assert payload["status"] == "ready"
    assert payload["readiness"] == SERVICE_READINESS
    assert payload["domains"] == []
    assert payload["summary"]["domains_count"] == 0
    assert payload["validation"]["read_only"] is True


def test_lists_materialized_sandbox_domain_with_minimum_payload(tmp_path):
    domain = _domain_only(tmp_path)

    payload = list_domains_status(sandbox_root=tmp_path / "sandboxes")
    item = payload["domains"][0]

    assert item["domain_id"] == domain["domain_id"]
    assert item["domain_name"]
    assert item["domain_status"] == "materialized"
    assert item["artifact_state"] == "materialized"
    assert item["readiness"] == DOMAIN_LISTABLE_READINESS
    assert item["artifact_count"] == 0
    assert item["artifact_kinds"] == []
    assert item["has_artifact_manifest"] is False
    assert item["has_profile_catalog"] is False
    assert item["has_agent_presets"] is False
    assert item["has_paper_seed"] is False
    assert item["has_sandbox_agents"] is False
    assert item["has_sandbox_team"] is False
    assert item["has_team_read_model"] is False
    assert item["has_audit_pack"] is False
    assert item["has_rollback_report"] is False
    assert item["has_regeneration_report"] is False
    assert item["warnings_count"] == 1
    assert item["errors_count"] == 0


def test_lists_artifacts_team_and_team_read_model_when_available(tmp_path):
    domain = _full_domain_with_team(tmp_path)

    payload = list_domains_status(sandbox_root=tmp_path / "sandboxes")
    item = payload["domains"][0]

    assert item["domain_id"] == domain["domain_id"]
    assert item["artifact_count"] >= 4
    assert "profile_catalog" in item["artifact_types"]
    assert "agent_preset" in item["artifact_types"]
    assert "paper_seed" in item["artifact_types"]
    assert "team" in item["artifact_types"]
    assert item["has_artifact_manifest"] is True
    assert item["has_profile_catalog"] is True
    assert item["has_agent_presets"] is True
    assert item["has_paper_seed"] is True
    assert item["has_sandbox_agents"] is True
    assert item["has_sandbox_team"] is True
    assert item["has_team_read_model"] is True
    assert item["blocked_capabilities"]
    assert set(item["blocked_capabilities"].values()) == {False}


def test_allowed_forbidden_and_next_actions_are_backend_defined(tmp_path):
    _full_domain_with_team(tmp_path)

    item = list_domains_status(sandbox_root=tmp_path / "sandboxes")["domains"][0]

    assert item["allowed_actions"] == ["view_status", "view_details"]
    assert "await_audit_pack" in item["next_actions"]
    assert "activate_runtime" in item["forbidden_actions"]
    assert "execute_agents" in item["forbidden_actions"]
    assert "invoke_models" in item["forbidden_actions"]
    assert "call_tools" in item["forbidden_actions"]
    assert "use_integrations" in item["forbidden_actions"]
    assert not set(item["allowed_actions"]) & {
        "materialize_without_preview",
        "rollback_without_confirmation",
        "delete_without_confirmation",
        "regenerate_without_rollback",
        "activate_runtime",
        "execute_agents",
    }


def test_service_is_read_only_and_creates_no_artifacts(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    domain = _full_domain_with_team(tmp_path)
    sandbox_root = tmp_path / "sandboxes"
    domain_dir = Path(domain["domain_dir"])
    before_sandbox = _snapshot_tree(sandbox_root)

    list_domains_status(sandbox_root=sandbox_root)
    get_domain_status_summary(domain_dir)

    assert _snapshot_tree(sandbox_root) == before_sandbox
    assert _tree_hash(DOMAINS) == before_domains
    assert not (domain_dir / "runtime").exists()
    assert not (domain_dir / "outputs").exists()
    assert not (domain_dir / "ui").exists()
    assert not (domain_dir / "integrations").exists()


def test_inconsistent_manifest_is_controlled_error(tmp_path):
    domain = _full_domain_with_team(tmp_path)
    manifest_path = Path(domain["domain_dir"]) / "manifests" / "artifact_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"][0]["dependencies"] = ["missing_dependency"]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    payload = list_domains_status(sandbox_root=tmp_path / "sandboxes")
    item = payload["domains"][0]

    assert item["readiness"] == DOMAIN_BLOCKED_READINESS
    assert item["errors_count"] == 1
    assert payload["errors"][0]["error_code"] == "INCONSISTENT_ARTIFACT_MANIFEST"


def test_invalid_audit_pack_is_controlled_warning_and_error(tmp_path):
    domain = _full_domain_with_team(tmp_path)
    audit_path = Path(domain["domain_dir"]) / "materialization_audit_pack.json"
    audit_path.write_text(json.dumps({"status": "broken"}, indent=2) + "\n", encoding="utf-8")

    payload = list_domains_status(sandbox_root=tmp_path / "sandboxes")
    item = payload["domains"][0]

    assert item["has_audit_pack"] is True
    assert item["errors_count"] == 1
    assert payload["errors"][0]["error_code"] == "INVALID_AUDIT_PACK"
    assert payload["warnings"][0]["error_code"] == "INVALID_AUDIT_PACK"


@pytest.mark.parametrize("field", ["operational", "runtime_enabled", "execution_enabled"])
def test_validator_rejects_operational_flags(field):
    payload = list_domains_status()
    payload[field] = True

    with pytest.raises(ValueError, match=field):
        validate_domain_status_payload(payload)


def test_validator_rejects_secret_like_field():
    payload = list_domains_status()
    payload["api_secret"] = "blocked"

    with pytest.raises(ValueError, match="sensible"):
        validate_domain_status_payload(payload)


def test_validator_rejects_destructive_allowed_action(tmp_path):
    _domain_only(tmp_path)
    payload = list_domains_status(sandbox_root=tmp_path / "sandboxes")
    payload["domains"][0]["allowed_actions"].append("delete_without_confirmation")

    with pytest.raises(ValueError, match="allowed_actions"):
        validate_domain_status_payload(payload)


def test_error_builder_uses_expected_shape_and_codes():
    error = build_domain_status_error("RUNTIME_BLOCKED", "runtime bloqueado")

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
    assert error["error_code"] in ERROR_CODES
    assert error["blocked"] is True


def test_contract_7_0_marks_list_domains_status_available_and_future_services_planned():
    contract = build_backend_internal_ui_contract()
    available = {service["name"]: service for service in contract["available_internal_services"]}
    planned = {service["name"]: service for service in contract["planned_internal_services"]}

    assert available["list_domains_status"]["available_now"] is True
    assert available["list_domains_status"]["type"] == "read-only"
    assert available["list_domains_status"]["destructive"] is False
    assert available["list_domains_status"]["requires_human_confirmation"] is False
    assert available["list_domains_status"]["public_endpoint"] is False
    assert available["list_domains_status"]["touches_visual_ui"] is False
    assert available["list_domains_status"]["runtime_enabled"] is False
    assert available["list_domains_status"]["execution_enabled"] is False
    assert available["preview_materialization"]["available_now"] is True
    assert available["materialize_sandbox"]["available_now"] is True
    assert available["materialize_sandbox"]["type"] == "controlled-write"
    assert available["materialize_sandbox"]["requires_human_confirmation"] is True
    for future in (
        "rollback_sandbox",
        "archive_domain",
        "delete_sandbox_domain",
        "reset_sandbox_domain",
    ):
        assert planned[future]["available_now"] is False


def test_service_does_not_access_env_network_models_tools_or_ui_runtime():
    source = MODULE.read_text(encoding="utf-8")

    assert "os.environ" not in source
    assert "requests." not in source
    assert "httpx." not in source
    assert "subprocess" not in source
    assert "openai" not in source.lower()
    assert "from core.model" not in source
    assert ".invoke_model" not in source
    assert "invoke_model(" not in source
    assert "from core.tool" not in source
    assert ".execute_tool" not in source
    assert "execute_tool(" not in source
    assert "frontend" not in source
    assert "FastAPI" not in source


def test_docs_plans_book_and_adr_record_prompt_7_1():
    for path in (DOC, PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR, MODULE):
        assert path.exists()

    doc = DOC.read_text(encoding="utf-8")
    for token in (
        "BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_READY",
        "BACKEND_INTERNAL_DOMAIN_STATUS_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_2_preview_materialization_service",
        "PROMPT 7.2 - Servicio interno preview_materialization",
        "sandbox_root explicito",
        "list_domains/status",
        "allowed_actions",
        "forbidden_actions",
        "SANDBOX_ROOT_REQUIRED",
        "UNSAFE_SANDBOX_ROOT",
        "no crea UI visual",
        "no crea endpoints publicos",
    ):
        assert token in doc

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PHASE_7_PLAN, CONTRACT_DOC, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR)
    )
    for token in (
        "PROMPT 7.1 - Servicio interno list_domains/status",
        "BACKEND_INTERNAL_DOMAIN_STATUS_SERVICE_READY",
        "BACKEND_INTERNAL_DOMAIN_STATUS_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_7_2_preview_materialization_service",
        "list_domains_status",
        "available_now=true",
        "PROMPT 7.2 - Servicio interno preview_materialization",
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


def test_prompt_7_1_does_not_create_operational_modules_or_temporals():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()


def test_payload_copy_validation_prevents_mutating_input_in_validator():
    payload = list_domains_status()
    original = deepcopy(payload)
    validated = validate_domain_status_payload(payload)

    assert validated == original
    assert validated is not payload
