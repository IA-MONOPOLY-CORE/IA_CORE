from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_NEXT_BLOCK_PLAN_1_59.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.60 - Auditar Final Screen Contract Readiness "
    "IA_CORE contract-aware sin runtime/no-execution"
)

SELECTED_BLOCK = "Final Screen Contract Readiness / Audit"

DRAFTS = [
    "Contract Overview Screen Draft",
    "Validation & Readiness Screen Draft",
    "Blocked & Forbidden Capabilities Screen Draft",
    "Request Contract Preview Screen Draft",
]

OPTIONS = [
    "Final Screen Contract Readiness / Audit",
    "Priority 1 Final Screen Contract Draft-to-Final Planning",
    "First Final Screen Contract Candidate",
    "Screen Contract Implementation Readiness",
    "Secondary Console Views / Detail Screens Planning",
    "Panel Maestro / User Panel Separation Next Layer",
    "UI Active Integration Readiness",
    "Visual Polish / Premium IA_CORE Layer",
    "External Benchmark Review",
    "GitHub Actions / CI Follow-up",
]

VERDICTS = [
    "UI_UX_NEXT_BLOCK_PLAN_1_59_COMPLETED",
    "POST_CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_STATE_REVIEWED",
    "CONTRACT_FIRST_SCREEN_CONTRACT_DRAFTS_CHECKPOINT_CONFIRMED",
    "REMOTE_RESTORE_POINT_EC8975B7_CONFIRMED",
    "PRIORITY_1_DRAFT_CONTRACTS_CONFIRMED",
    "FINAL_SCREEN_CONTRACTS_NOT_CREATED_CONFIRMED",
    "FUTURE_SCREENS_NOT_IMPLEMENTED_CONFIRMED",
    "USER_PANEL_NOT_IMPLEMENTED_CONFIRMED",
    "NEXT_BLOCK_OPTIONS_EVALUATED",
    "NEXT_BLOCK_SELECTED",
    "NEXT_BLOCK_SEQUENCE_DEFINED",
    "NO_UI_ACTIVE_CHANGE_CONFIRMED",
    "NO_RUNTIME_NO_EXECUTION_CONFIRMED",
    "NO_ENDPOINTS_NO_DEPENDENCIES_CONFIRMED",
    "PUSH_POSTPONED_UNTIL_NEXT_CHECKPOINT",
    "UI_READY_FOR_NEXT_BLOCK_AUDIT",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_document_exists_and_records_base_context():
    assert DOC.exists()
    text = read(DOC)

    markers = [
        "# UI/UX Next Block Plan 1.59 - Post Contract-First Screen Contract Drafts",
        "ec8975b7",
        "restore point remoto actual",
        "main",
        "origin https://github.com/IA-MONOPOLY-CORE/IA_CORE",
        "local sincronizado con `origin/main`",
        "working tree limpio",
        "Contract-First Screen Contract Drafts",
    ]
    for marker in markers:
        assert marker in text


def test_plan_confirms_closed_block_and_priority_1_drafts():
    text = read(DOC)

    markers = [
        "1.55 planifico",
        "1.56 audito",
        "1.57 documento",
        "1.58 cerro checkpoint",
        "GitHub actualizado hasta `ec8975b7`",
        "bloque `1.55 -> 1.58` queda cerrado",
        "Draft contracts Priority 1 existentes",
    ]
    for marker in markers:
        assert marker in text

    for draft in DRAFTS:
        assert draft in text


def test_plan_preserves_no_scope_and_identity():
    text = read(DOC)

    markers = [
        "Final screen contracts no creados",
        "Future screens no implementadas",
        "User Panel no implementado",
        "UI activa no modificada",
        "Sin endpoints nuevos",
        "Sin rutas nuevas",
        "Sin fetches nuevos",
        "Sin dependencias nuevas",
        "Sin cambios CI",
        "No-runtime/no-execution",
        "Sin dispatch",
        "Sin controlled execution",
        "Backend operativo untouched",
        "No tocar `core/`, `api.py`, `domains/` operativo, `tools`, modelos ni integraciones",
        "IA_CORE sigue como identidad activa",
        "SAAOP/Loteria/Tactical HUD/U-Score no son UI activa",
    ]
    for marker in markers:
        assert marker in text


def test_plan_evaluates_all_candidate_options_and_selects_one():
    text = read(DOC)

    assert "Opciones Candidatas Evaluadas" in text
    for option in OPTIONS:
        assert option in text

    assert f"Bloque seleccionado unico: `{SELECTED_BLOCK}`" in text
    assert text.count("Bloque seleccionado unico:") == 1
    assert "Por que ahora" in text
    assert "Por que no los otros bloques" in text
    assert "Opciones Postergadas" in text
    assert "Postergada" in text or "postergada" in text


def test_plan_defines_sequence_backup_policy_and_next_prompt():
    text = read(DOC)

    markers = [
        "Secuencia Tentativa",
        "PROMPT UI/UX 1.60 - Auditar Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.61 - Documentar Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution",
        "Politica De Backup",
        "1.59 es planificacion documental",
        "No hacer push por defecto",
        "ultimo restore point remoto sigue siendo `ec8975b7`",
        "proximo restore point remoto recomendado queda para el checkpoint del nuevo bloque, estimado en 1.62",
        NEXT_PROMPT,
        "No avanzar a 1.60",
    ]
    for marker in markers:
        assert marker in text


def test_plan_contains_expected_verdicts():
    text = read(DOC)

    for verdict in VERDICTS:
        assert verdict in text


def test_readmes_register_plan_and_cursor():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    current_after_1_60 = (
        "PROMPT UI/UX 1.61 - Documentar Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_61 = (
        "PROMPT UI/UX 1.62 - Checkpoint Final Screen Contract Readiness "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_62 = (
        "PROMPT UI/UX 1.63 - Consolidar siguiente bloque UI/UX post "
        "Final Screen Contract Readiness IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_63 = (
        "PROMPT UI/UX 1.64 - Auditar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_64 = (
        "PROMPT UI/UX 1.65 - Documentar Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_65 = (
        "PROMPT UI/UX 1.66 - Checkpoint Contract Overview Final Screen Contract "
        "IA_CORE contract-aware sin runtime/no-execution"
    )
    current_after_1_66 = (
        "PROMPT UI/UX 1.67 - Consolidar siguiente bloque UI/UX post Contract "
        "Overview Final Screen Contract IA_CORE contract-aware sin runtime/no-execution"
    )
    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_60}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_61}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_62}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_63}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_64}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_65}{bt}" in root
        or f"Next pending step: {bt}{current_after_1_66}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.68 - Auditar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.69 - Documentar Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )

    for text in (root, web):
        assert "planificacion 1.59" in text
        assert "bloque 1.55 -> 1.58 cerrado" in text
        assert SELECTED_BLOCK in text
        assert NEXT_PROMPT in text or current_after_1_63 in text
        assert "push pospuesto" in text.lower()
        assert "no-runtime/no-execution" in text
        assert "sin endpoints" in text
        assert "sin dependencias" in text
        assert "sin UI activa modificada" in text
        assert "sin User Panel" in text or "User Panel no implementado" in text
        assert "ec8975b7" in text
