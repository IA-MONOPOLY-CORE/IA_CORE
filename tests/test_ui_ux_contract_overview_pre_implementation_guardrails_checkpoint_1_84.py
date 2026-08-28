from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_CHECKPOINT_1_84.md"
NEXT_PROMPT = (
    "PROMPT UI/UX 1.85 - Preparar plan de implementacion controlada de "
    "Contract Overview Screen IA_CORE contract-aware sin runtime/no-execution"
)


def test_checkpoint_document_contains_required_contract_and_history_markers():
    text = DOC.read_text(encoding="utf-8")
    markers = (
        "UI/UX Contract Overview Pre-Implementation Guardrails Checkpoint 1.84",
        "cd855a2",
        "476831e",
        "1.82",
        "1.83",
        "1.84",
        "FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED",
        "CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY",
        "FSC-CO-01",
        "backend_internal_ui_payload.v1",
        "Panel Maestro",
        "vista documental",
        "solo lectura",
        "no User Panel",
        "no runtime",
        "no execution",
        "ready-no-permission",
        "allowed_actions",
        "no son botones de ejecucion",
        "forbidden_actions",
        "blockers",
        "snapshot documental",
        "no log vivo",
        "empty state honesto",
        "Loteria",
        "SAAOP",
        "12 riesgos",
        "P0",
        "P1",
        "P2",
        "30 passed",
        "4 checks",
        "no pantalla",
        "no UI activa",
        "no componente nuevo",
        "no rutas/hash",
        "no endpoints",
        "no fetches",
        "no backend operativo",
        "no CI",
        "no dependencias",
        "no deuda residual",
        "no pyflakes",
        NEXT_PROMPT,
    )
    assert DOC.exists()
    normalized = text.lower()
    assert all(marker.lower() in normalized for marker in markers)


def test_checkpoint_explicitly_preserves_non_implementation_boundaries():
    text = DOC.read_text(encoding="utf-8")
    markers = (
        "La pantalla no fue implementada",
        "la UI activa no fue modificada",
        "no se creo componente nuevo",
        "no se creo User Panel",
        "no se crearon rutas/hash",
        "no se tocaron backend/runtime/endpoints/CI/dependencias",
        "no se limpio deuda residual",
        "no se corrigieron pyflakes",
        "no secrets",
        "no se implemento pantalla",
        "no se modifico UI activa",
        "no se crearon endpoints",
        "no se crearon fetches",
        "no se activo runtime",
        "no se activo execution",
        "no se activo dispatch",
    )
    normalized = text.lower()
    assert all(marker.lower() in normalized for marker in markers)


def test_checkpoint_records_git_push_gate_and_future_scope():
    text = DOC.read_text(encoding="utf-8")
    markers = (
        "working tree limpio",
        "ahead de `origin/main` por 1 commit",
        "docs(ui): cerrar checkpoint guardrails contract overview",
        "nuevo restore point remoto",
        "git status",
        "no implementacion directa",
        "User Panel sigue fuera de alcance",
        "runtime/endpoints siguen prohibidos",
    )
    normalized = text.lower()
    assert all(marker.lower() in normalized for marker in markers)
