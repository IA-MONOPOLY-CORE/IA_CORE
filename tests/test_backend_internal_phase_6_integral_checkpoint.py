from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT.md"
PHASE_6_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_6_SANDBOX_E2E_ROLLBACK_REGENERATION_BLOCK_PLAN.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"


FORBIDDEN_OPERATIONAL_MODULES = (
    "core/sandbox_execution_runner.py",
    "core/sandbox_runtime_runner.py",
    "core/team_runtime_executor.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_dispatcher.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/context_injection_runtime.py",
    "core/output_delivery_runtime.py",
    "core/ui_runtime.py",
    "core/integration_runtime.py",
    "core/backend_ui_endpoint.py",
    "core/backend_ui_api.py",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase_6_integral_checkpoint_document_exists_and_closes_chain():
    assert CHECKPOINT.exists()
    text = _text(CHECKPOINT)
    for token in (
        "BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT_PASSED",
        "SANDBOX_E2E_ROLLBACK_REGENERATION_AUDIT_PACK_CONFIRMED",
        "ready_for_phase_7_backend_internal_ui_contract",
        "PROMPT 6.0 - Validacion end-to-end sandbox completa",
        "SANDBOX_END_TO_END_FULL_CHECKPOINT_PASSED",
        "PROMPT 6.1 - Rollback integral de dominio sandbox completo",
        "SANDBOX_INTEGRAL_ROLLBACK_PASSED",
        "PROMPT 6.2 - Regeneracion segura sandbox completa",
        "SANDBOX_SAFE_REGENERATION_PASSED",
        "PROMPT 6.3 - Audit pack y trazabilidad de materializacion sandbox",
        "SANDBOX_MATERIALIZATION_AUDIT_PACK_READY",
    ):
        assert token in text


def test_phase_6_integral_checkpoint_covers_evidence_sections():
    text = _text(CHECKPOINT)
    for token in (
        "E2E sandbox completo",
        "Rollback Validado",
        "Regeneracion Validada",
        "Audit Pack Validado",
        "artifact_manifest",
        "lineage",
        "created_paths",
        "read model",
        "JSON-safe",
        "blocked_capabilities",
        "domains/` operativo no se toca",
        ".tmp/",
        "memoria_agentes/test_agent",
        "memoria_agentes/test_agent_context",
    ):
        assert token in text


def test_integral_non_operational_boundaries_are_explicit():
    text = _text(CHECKPOINT)
    for token in (
        "runtime real",
        "execution real",
        "dry-run real operativo",
        "tools",
        "model invocation",
        "context injection operativo",
        "output delivery",
        "writes/stores/memory operativos",
        "network/browser",
        "API runtime",
        "UI runtime",
        "UI visual real",
        "integraciones",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
        "raw Package directo al User Panel",
        "Permanecen bloqueados",
    ):
        assert token in text


def test_next_plans_and_book_select_phase_7_without_implementing_it():
    combined = "\n".join(_text(path) for path in (PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "PROMPT 6.4",
        "BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT_PASSED",
        "SANDBOX_E2E_ROLLBACK_REGENERATION_AUDIT_PACK_CONFIRMED",
        "ready_for_phase_7_backend_internal_ui_contract",
        "Fase 7 - Contrato backend interno para UI",
        "PROMPT 7.0 - Contrato backend interno para UI",
        "no crea UI",
        "no crea endpoints publicos",
        "no activa runtime",
        "no ejecuta agentes",
        "no toca integraciones",
    ):
        assert token in combined


def test_phase_6_checkpoint_has_no_operational_activation_language():
    text = _text(CHECKPOINT).lower()
    forbidden = (
        "runtime_enabled=true",
        "execution_enabled=true",
        "operational=true",
        "tools habilitados",
        "modelos habilitados",
        "ui implementada",
        "integraciones activas",
        "obliteratus permitido",
        "ready_for_runtime_activation",
        "ready_for_execution",
        "runtime activo",
        "ejecucion real habilitada",
    )
    for token in forbidden:
        assert token not in text


def test_phase_6_checkpoint_does_not_create_forbidden_operational_modules_or_temporals():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    assert not (ROOT / ".tmp").exists()
    assert not (ROOT / "memoria_agentes" / "test_agent").exists()
    assert not (ROOT / "memoria_agentes" / "test_agent_context").exists()


def test_architecture_decision_records_phase_6_integral_close():
    text = _text(ADR)
    for token in (
        "ADR-050",
        "Fase 6 cierra el ciclo sandbox E2E rollback regeneracion auditoria sin operacion real",
        "docs/BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT.md",
        "Fase 7 - Contrato backend interno para UI",
        "no queda implementada",
        "permanecen bloqueados",
    ):
        assert token in text
