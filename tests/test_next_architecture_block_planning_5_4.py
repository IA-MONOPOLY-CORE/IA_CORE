from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_6_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_6_SANDBOX_E2E_ROLLBACK_REGENERATION_BLOCK_PLAN.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"

FORBIDDEN_NEW_OPERATIONAL_MODULES = (
    "core/sandbox_e2e_runner.py",
    "core/sandbox_runtime_runner.py",
    "core/team_runtime_executor.py",
    "core/team_orchestrator.py",
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
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase_6_plan_exists_and_selects_next_block():
    assert PHASE_6_PLAN.exists()
    text = _text(PHASE_6_PLAN)
    for token in (
        "NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED",
        "NEXT_ARCHITECTURE_BLOCK_SELECTED",
        "ready_for_phase_6_sandbox_e2e_checkpoint",
        "Fase 6",
        "end-to-end",
        "rollback",
        "regeneracion",
        "PROMPT 6.0 - Validacion end-to-end sandbox completa",
        "PROMPT 6.0 — Validación end-to-end sandbox completa",
    ):
        assert token in text


def test_phase_6_plan_classifies_existing_reusable_pieces():
    text = _text(PHASE_6_PLAN)
    for token in (
        "core/sandbox_lifecycle_validation.py",
        "core/domain_materialization_rollback.py",
        "tests/test_sandbox_lifecycle.py",
        "tests/test_domain_materialization_rollback.py",
        "tests/test_sandbox_chain_checkpoint.py",
        "tests/test_sandbox_chain_maximum_checkpoint.py",
        "tests/test_sandbox_chain_with_team_checkpoint.py",
        "docs/SANDBOX_TEAM_CHAIN_CHECKPOINT.md",
        "vigente reutilizable",
        "parcial a extender",
        "historico compatible",
        "fixture/benchmark largo",
    ):
        assert token in text


def test_next_plans_and_book_reflect_phase_6_selection():
    for path in (NEXT_ARCH, NEXT_OPERATIONAL, BOOK):
        text = _text(path)
        assert "PROMPT 5.4" in text
        assert "Fase 6" in text
        assert "ready_for_phase_6_sandbox_e2e_checkpoint" in text
        assert "PROMPT 6.0 - Validacion end-to-end sandbox completa" in text


def test_blocked_capabilities_remain_explicitly_blocked():
    combined = "\n".join(_text(path) for path in (PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "Runtime",
        "runtime",
        "execution",
        "dry-run real",
        "tools",
        "modelos",
        "contexto",
        "outputs",
        "writes",
        "stores",
        "memory",
        "memoria operativa",
        "API",
        "UI",
        "integraciones",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
        "raw Package directo a User Panel",
        "permanecen bloqueados",
    ):
        assert token in combined


def test_phase_6_is_not_implemented_by_this_prompt():
    text = _text(PHASE_6_PLAN)
    for token in (
        "No implementar runtime real",
        "No ejecutar agentes ni equipos",
        "No crear un segundo `sandbox_chain` paralelo",
        "No crear UI, endpoints publicos ni integraciones",
        "Fase 6 no abre runtime",
    ):
        assert token in text
    for relative in FORBIDDEN_NEW_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative


def test_existing_chain_checkpoint_is_reused_before_new_flow():
    text = _text(PHASE_6_PLAN) + "\n" + _text(ADR)
    assert "reutilizar" in text
    assert "tests/test_sandbox_chain_with_team_checkpoint.py" in text
    assert "no duplicar" in text or "duplicar `sandbox_chain`" in text
    assert "ADR-046" in text
