from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
PHASE_5 = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_5_TEAM_SANDBOX_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"

FORBIDDEN_OPERATIONAL_MODULES = (
    "core/runtime_execution_preparation_store.py",
    "core/runtime_execution_preparation_writer.py",
    "core/runtime_execution_preparation_reader.py",
    "core/runtime_execution_preparation_api.py",
    "core/runtime_execution_preparation_ui.py",
    "core/runtime_runner.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_dispatcher.py",
    "core/dry_run_executor.py",
    "core/tool_executor.py",
    "core/model_invoker.py",
    "core/context_injector.py",
    "core/output_delivery.py",
    "core/output_publisher.py",
    "core/browser_operator.py",
    "core/ui_tars_adapter.py",
    "core/hermes_adapter.py",
    "core/n8n_adapter.py",
    "core/home_assistant_adapter.py",
)


def test_next_architecture_block_plan_selects_phase_5_after_4_8():
    assert NEXT_ARCH.exists()
    text = NEXT_ARCH.read_text(encoding="utf-8")
    for token in (
        "NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED",
        "NEXT_ARCHITECTURE_BLOCK_SELECTED",
        "ready_for_phase_5_team_sandbox_schema",
        "PROMPT 4.8 cerrado",
        "61c4b15b",
        "PROMPT 5.0 — Schema de equipo real sandbox",
        "Fase 5 — Equipos reales sandbox",
        "Runtime Execution Preparation Block",
        "Backend Interno",
    ):
        assert token in text


def test_next_architecture_block_plan_keeps_runtime_and_integrations_blocked():
    text = NEXT_ARCH.read_text(encoding="utf-8")
    for token in (
        "runtime: bloqueado",
        "execution: bloqueada",
        "dry-run real: bloqueado",
        "UI/UX: fuera de alcance",
        "integraciones: bloqueadas",
        "OBLITERATUS: excluido",
        "Market Catalog runtime: bloqueado",
        "Business Composition Layer runtime: bloqueado",
        "No implementar Fase 5 en este prompt",
        "No crear equipos sandbox en este prompt",
    ):
        assert token in text
    forbidden_open_markers = (
        "runtime: abierto",
        "execution: abierta",
        "dry-run real: abierto",
        "integraciones: abiertas",
        "UI/UX como etapa actual",
    )
    for marker in forbidden_open_markers:
        assert marker not in text


def test_phase_5_team_sandbox_plan_exists_and_is_non_operational():
    assert PHASE_5.exists()
    text = PHASE_5.read_text(encoding="utf-8")
    for token in (
        "Fase 5 — Equipos reales sandbox",
        "sandbox",
        "no-operativa",
        "No habilita ejecución multiagente real",
        "PROMPT 5.0 — Schema de equipo real sandbox",
        "PROMPT 5.1 — Materializar equipo real desde team_template",
        "PROMPT 5.2 — Auditoría de equipo sandbox",
        "PROMPT 5.3 — Biblioteca interna/listado de equipos sandbox para futura UI",
        "ready_for_phase_5_team_sandbox_schema",
    ):
        assert token in text


def test_next_operational_plan_and_book_reflect_4_9_decision():
    operational = NEXT_OPERATIONAL.read_text(encoding="utf-8")
    book = BOOK.read_text(encoding="utf-8")
    for text in (operational, book):
        assert "PROMPT 4.9" in text
        assert "PROMPT 5.0 — Schema de equipo real sandbox" in text
        assert "ready_for_phase_5_team_sandbox_schema" in text
    assert "Runtime Execution Preparation ya cerró con 4.8" in operational
    assert "No operational runtime has been opened" in operational


def test_no_new_operational_modules_are_declared_as_implemented():
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
    text = NEXT_ARCH.read_text(encoding="utf-8")
    for relative in FORBIDDEN_OPERATIONAL_MODULES:
        assert f"{relative} implementado" not in text
