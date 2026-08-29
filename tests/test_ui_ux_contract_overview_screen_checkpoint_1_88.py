from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_SCREEN_CHECKPOINT_1_88.md"


def read_doc():
    assert DOC.exists(), "Checkpoint 1.88 document is missing"
    return DOC.read_text(encoding="utf-8")


def test_checkpoint_document_exists_and_records_sequence():
    text = read_doc()
    markers = (
        "UI/UX Contract Overview Screen Checkpoint 1.88",
        "894d223",
        "d20a5d1",
        "9fb9d55",
        "1ceb9c6",
        "1.85",
        "1.86",
        "1.87",
        "1.88",
        "CONTRACT_OVERVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY",
        "CONTRACT_OVERVIEW_SCREEN_IMPLEMENTED_NEEDS_HARDENING",
        "CONTRACT_OVERVIEW_SCREEN_HARDENED_READY_FOR_HUMAN_VISUAL_REVIEW",
        "HUMAN_VISUAL_REVIEW_APPROVED",
    )
    assert all(marker in text for marker in markers)


def test_checkpoint_records_final_contract_overview_state():
    text = read_doc().lower()
    markers = (
        "contract overview screen",
        "fsc-co-01",
        "backend_internal_ui_payload.v1",
        "panel maestro",
        "documental",
        "read-only",
        "solo lectura",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "snapshot",
        "no log vivo",
        "no fake success",
        "no ghost actions",
        "no user panel",
        "no endpoint",
        "no fetch",
        "no rutas/hash",
        "ia_core",
        "saaop",
    )
    assert all(marker in text for marker in markers)
    assert "loteria" in text or "lotería" in text


def test_checkpoint_records_validation_and_restore_point_requirements():
    text = read_doc()
    markers = (
        "node checks",
        "git diff --check",
        "backend contract tests",
        "backup readiness",
        "tests 1.86 OK",
        "tests 1.87 OK",
        "tests 1.85 OK",
        "tests 1.84 OK",
        "tests 1.83 OK",
        "tests contrato 1.66 OK",
        "tests contrato 1.65 OK",
        "git push origin main",
        "main` sincronizada con `origin/main",
    )
    assert all(marker in text for marker in markers)


def test_checkpoint_preserves_scope_limits():
    text = read_doc()
    markers = (
        "No se implemento pantalla adicional",
        "No se modifico backend/runtime/endpoints/CI/dependencias",
        "No se limpio deuda residual",
        "No se corrigieron pyflakes",
        "No se avanzo a 1.89",
        "No se modifico UI activa",
        "No se creo User Panel",
        "No se crearon rutas/hash",
        "No se crearon endpoints",
        "No se crearon fetches",
        "No se activo runtime",
        "No se activo execution",
        "No se activo dispatch",
    )
    assert all(marker in text for marker in markers)


def test_checkpoint_points_to_next_prompt_without_implementing_it():
    text = read_doc()
    assert (
        "PROMPT UI/UX 1.89 - Planificar siguiente pantalla Final Screen Contract "
        "tras Contract Overview IA_CORE contract-aware sin runtime/no-execution"
    ) in text
    assert "Todavia no implementar Blocked & Forbidden directamente" in text
    assert "Contract Overview queda como baseline visual/contractual" in text



