import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOC = ROOT / "docs" / "BACKEND_INTERNAL_PRE_OPERATIONAL_FINAL_AUDIT.md"
BOOK_DOC = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"


CHAIN = [
    "sandbox",
    "promotion",
    "active",
    "runtime_contract",
    "execution_contract",
    "runtime_executor_contract",
    "runtime_prepare",
    "execution_runner_contract",
    "dry_run_contract",
    "dry_run result-only",
    "dry_run_store",
    "execution_attempt_store",
    "execution_lifecycle",
    "execution_history_view",
    "internal_backend_read_model_contract",
    "internal_backend_read_model read-only",
]
BLOCKS = [
    "sandbox/materialization",
    "promotion",
    "active",
    "runtime contract",
    "execution contract",
    "runtime executor prepare-only",
    "execution runner contract",
    "dry-run result-only",
    "dry_run_store",
    "execution_attempt_store",
    "execution_lifecycle",
    "execution_history_view",
    "internal_backend_read_model",
    "audit/observability",
    "docs/tests",
]
GAP_TYPES = ["critical", "major", "minor", "deferred", "none"]
FORBIDDEN_PATHS = [
    "core/backend_read_model_store.py",
    "core/backend_status_api.py",
    "core/backend_dashboard_adapter.py",
    "ui/internal_backend_read_model",
    "core/scheduler_queue.py",
    "core/worker_queue.py",
]
CORE_UNMODIFIED = [
    "core/internal_backend_read_model.py",
    "core/execution_history_view.py",
    "core/execution_lifecycle.py",
    "core/execution_attempt_store.py",
    "core/dry_run_store.py",
    "core/execution_runner.py",
]


def _text() -> str:
    return AUDIT_DOC.read_text(encoding="utf-8")


def _git_status_for(paths: list[str]) -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--", *paths],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def test_final_audit_document_exists_and_verdict_is_ready():
    text = _text()

    assert AUDIT_DOC.exists()
    assert "BACKEND_INTERNAL_READY_FOR_INTEGRAL_CHECKPOINT" in text


def test_complete_chain_is_documented():
    text = _text()

    for item in CHAIN:
        assert item in text


def test_block_status_is_documented():
    text = _text()

    for block in BLOCKS:
        assert block in text
    for header in ["bloque", "estado", "archivo principal", "tests principales", "veredicto/readiness", "riesgos"]:
        assert header in text


def test_gaps_are_classified():
    text = _text()

    for gap_type in GAP_TYPES:
        assert gap_type in text
    for field in ["id", "tipo", "descripcion", "archivo relacionado", "riesgo", "recomendacion", "bloquea 2.50"]:
        assert field in text


def test_duplications_inconsistencies_and_risks_are_audited():
    text = _text()

    for item in [
        "nombres duplicados",
        "readiness duplicadas",
        "veredictos duplicados",
        "boundary flags inconsistentes",
        "suite pesada",
        "tests lentos acumulados",
        "drift documental",
        "contratos demasiado verbosos",
        "nombres largos",
        "dependencia excesiva de fixtures",
        "pre-operacional con operacional",
        "API/UI antes de tiempo",
    ]:
        assert item in text


def test_integral_checkpoint_scope_and_next_step_are_documented():
    text = _text()

    for item in [
        "validar cadena completa",
        "validar `agent/team`",
        "validar snapshot read-only final",
        "validar history view",
        "validar lifecycle/stores",
        "validar boundaries globales",
        "validar ausencia de features postergadas",
        "validar docs principales",
        "validar suite filtrada",
        "BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_PASSED",
        "PROMPT 2.50 - Checkpoint integral backend interno pre-operacional",
    ]:
        assert item in text


def test_key_checkpoints_stores_and_contracts_are_referenced():
    text = _text()

    for item in [
        "PASSED_INTERNAL_BACKEND_READ_MODEL_READ_ONLY_E2E",
        "PASSED_EXECUTION_HISTORY_VIEW_DERIVED_ONLY_E2E",
        "dry_run_store",
        "execution_attempt_store",
        "execution_lifecycle",
        "runtime_contract",
        "execution_contract",
        "internal_backend_read_model_contract",
    ]:
        assert item in text


def test_no_new_store_api_ui_scheduler_worker_or_execution_scope_exists():
    text = _text()

    for relative in FORBIDDEN_PATHS:
        assert not (ROOT / relative).exists(), relative
    for phrase in [
        "no crear store",
        "no crea API",
        "dashboard adapter",
        "scheduler/worker",
        "ejecucion real",
        "modelos/tools/memoria",
        "external access",
    ]:
        assert phrase in text


def test_core_implementation_files_are_not_modified_by_audit():
    for relative in CORE_UNMODIFIED:
        assert (ROOT / relative).exists(), relative
    assert _git_status_for(CORE_UNMODIFIED) == ""


def test_book_entry_references_prompt_249():
    book = BOOK_DOC.read_text(encoding="utf-8")

    assert "PROMPT 2.49 - Auditoria final de backend interno pre-operacional" in book
    assert "BACKEND_INTERNAL_READY_FOR_INTEGRAL_CHECKPOINT" in book
    assert "PROMPT 2.50 - Checkpoint integral backend interno pre-operacional" in book
