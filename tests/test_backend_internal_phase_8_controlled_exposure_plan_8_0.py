from pathlib import Path

from core.backend_internal_ui_contract import build_backend_internal_ui_contract


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md"
CHECKPOINT_7_7 = ROOT / "docs" / "BACKEND_INTERNAL_UI_CONTRACT_CHECKPOINT_7_7.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
DOMAINS = ROOT / "domains"
MEMORY = ROOT / "memoria_agentes"

EXPECTED_CANDIDATE_SERVICES = {
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

FORBIDDEN_FUNCTIONAL_FILES = (
    "core/backend_internal_ui_request.py",
    "core/backend_internal_ui_dispatcher.py",
    "core/backend_internal_confirmation_gate.py",
    "core/backend_internal_exposure_adapter.py",
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


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase_8_plan_exists_and_inherits_closed_phase_7():
    assert PLAN.exists()
    assert CHECKPOINT_7_7.exists()
    text = _text(PLAN)

    for token in (
        "Fase 7 cerrada",
        "BACKEND_INTERNAL_UI_CONTRACT_PHASE_7_CHECKPOINT_PASSED",
        "ready_for_next_backend_internal_architecture_block",
        "backend_internal_ui_payload.v1",
        "tests/test_backend_internal_ui_contract_checkpoint_7_7.py",
    ):
        assert token in text


def test_plan_defines_controlled_internal_exposure_and_negative_scope():
    text = _text(PLAN)

    assert "Exposicion interna controlada = capa backend interna" in text
    for token in (
        "no es frontend",
        "no es UI visual",
        "no es API publica",
        "no es endpoint publico",
        "no es router HTTP",
        "no es runtime",
        "no es execution runner",
        "no es ejecucion de agentes",
        "no es invocacion de modelos/tools",
        "no es integracion externa",
        "no es User Panel real",
        "no es puente a produccion",
        "no es permiso para tocar `domains/` operativo",
    ):
        assert token in text


def test_plan_defines_backend_ui_boundary_and_backend_authority():
    text = _text(PLAN)

    for token in (
        "Backend conserva autoridad",
        "permisos",
        "readiness",
        "validacion",
        "blocked capabilities",
        "allowed_actions",
        "forbidden_actions",
        "errores",
        "path safety",
        "confirmaciones requeridas",
        "lifecycle rules",
        "UI futura solo consume",
        "La UI futura no infiere",
        "activar runtime",
        "tocar integraciones",
    ):
        assert token in text


def test_plan_lists_and_classifies_candidate_phase_7_services():
    text = _text(PLAN)
    contract = build_backend_internal_ui_contract()
    available = {service["name"] for service in contract["available_internal_services"]}

    assert EXPECTED_CANDIDATE_SERVICES <= available
    for service in EXPECTED_CANDIDATE_SERVICES:
        assert service in text
    for token in (
        "read_only_status",
        "read_only_preview",
        "read_only_validation",
        "controlled_write",
        "controlled_lifecycle",
        "available_now=true",
        "side_effects",
        "destructive",
        "path safety",
        "forbidden capabilities",
        "tests existentes",
    ):
        assert token in text


def test_plan_lists_blocked_non_exposable_services_and_capabilities():
    text = _text(PLAN)

    for token in (
        "runtime execution",
        "agent execution",
        "model invocation",
        "tool invocation",
        "external integrations",
        "network/browser automation",
        "public endpoints",
        "UI device control",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
        "`domains/` operativo",
        "raw Package direct to User Panel",
        "cualquier servicio no implementado/testeado",
    ):
        assert token in text


def test_plan_defines_phase_8_architecture_request_response_confirmations_and_stages():
    text = _text(PLAN)

    for token in (
        "PROMPT 8.1 - Internal exposure registry / service map",
        "PROMPT 8.2 - Internal request envelope y request validation",
        "PROMPT 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto",
        "PROMPT 8.4 - Confirmation gate para controlled-write/lifecycle",
        "PROMPT 8.5 - Internal response adapter usando stable_ui_payloads",
        "PROMPT 8.6 - Exposure audit checkpoint",
        "PROMPT 8.7 - Plan de futura UI visual sobre contrato estable",
        "backend_internal_ui_request.v1",
        '"schema_version": "backend_internal_ui_request.v1"',
        '"runtime_allowed": false',
        '"execution_allowed": false',
        '"tools_allowed": false',
        '"models_allowed": false',
        '"integrations_allowed": false',
        "La response envelope confirmada es `backend_internal_ui_payload.v1`",
        "`delete_sandbox_domain` requiere confirmacion fuerte y `allow_delete=true`",
        "`reset_sandbox_domain` requiere confirmacion fuerte y `allow_reset=true`",
    ):
        assert token in text


def test_plan_defines_prompt_restrictions_tests_closure_verdict_and_readiness():
    text = _text(PLAN)

    for token in (
        "git status --short",
        "HEAD esperado",
        "tests focales",
        "regresion 7.7/7.6/7.0",
        "git diff --check",
        "commit",
        "working tree final limpio",
        "tests/test_runtime_execution_preparation_block_integral_checkpoint.py",
        "BACKEND_INTERNAL_PHASE_8_CONTROLLED_EXPOSURE_PLAN_READY",
        "BACKEND_INTERNAL_PHASE_8_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_8_1_internal_exposure_registry",
        "PROMPT 8.1 - Internal exposure registry / service map",
        "Criterio De Cierre De Fase 8",
    ):
        assert token in text


def test_next_plans_book_and_adr_record_prompt_8_0():
    for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR):
        assert path.exists()

    combined = "\n".join(_text(path) for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR))
    for token in (
        "PROMPT 8.0 - Planificacion del bloque de exposicion interna controlada para futura UI",
        "Fase 8 - Exposicion interna controlada para futura UI",
        "BACKEND_INTERNAL_PHASE_8_CONTROLLED_EXPOSURE_PLAN_READY",
        "BACKEND_INTERNAL_PHASE_8_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_8_1_internal_exposure_registry",
        "PROMPT 8.1 - Internal exposure registry / service map",
        "no UI visual",
        "no endpoint publico",
        "runtime",
        "execution",
        "tools",
        "modelos",
        "integraciones",
        "`domains/` operativo",
    ):
        assert token in combined


def test_prompt_8_0_does_not_create_functional_exposure_ui_endpoint_or_temp_artifacts():
    for relative in FORBIDDEN_FUNCTIONAL_FILES:
        assert not (ROOT / relative).exists(), relative
    assert DOMAINS.exists()
    assert not (ROOT / ".tmp").exists()
    assert not (MEMORY / "test_agent").exists()
    assert not (MEMORY / "test_agent_context").exists()
