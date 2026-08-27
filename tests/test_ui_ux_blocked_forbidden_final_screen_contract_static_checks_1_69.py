from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_BLOCKED_FORBIDDEN_FINAL_SCREEN_CONTRACT_1_69.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.70 - Checkpoint Blocked & Forbidden Final Screen Contract "
    "IA_CORE contract-aware sin runtime/no-execution"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_static_contract_markers_are_present():
    text = read(DOC)

    markers = [
        "final-documental",
        "not implemented",
        "Panel Maestro only",
        "No-Implementation Boundary",
        "No-Unlock Boundary",
        "Blocked/Forbidden Visibility Policy",
        "Blocked Capabilities Policy",
        "Forbidden Actions Policy",
        "Allowed Explanatory Data",
        "Forbidden Operational Data",
        "Allowed Local / Read-Only Controls",
        "Forbidden Controls",
        "Allowed States",
        "Forbidden States",
        "no route/hash",
        "no endpoint/API/router",
        "no fetch",
        "no User Panel",
        "no runtime/no-execution",
        "no unlock/no override/no bypass/no permission escalation",
        "No UI activa modificada",
    ]
    for marker in markers:
        assert marker in text


def test_static_checks_are_contextual_not_runtime_enforcement():
    text = read(DOC)

    assert "documental/acotada" in text
    assert "No hace red" not in text
    assert "no modifica UI activa" in text
    assert "no cambia HTML/CSS/JS operativo" in text
    assert "no instala dependencias" in text
    assert "no modifica GitHub Actions" in text
    assert "no invoca modelos/tools/integraciones" in text


def test_readme_cursor_points_to_1_70():
    root = read(README)
    web = read(WEB_README)
    bt = "`"

    assert (
        f"Next pending step: {bt}{NEXT_PROMPT}{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.71 - Consolidar siguiente bloque UI/UX post Blocked & Forbidden Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.72 - Auditar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.73 - Cerrar gaps menores Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.74 - Checkpoint Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.75 - Consolidar siguiente bloque UI/UX post Validation & Readiness Minor Gaps Closure IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.76 - Auditar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
        or f"Next pending step: {bt}PROMPT UI/UX 1.77 - Documentar Validation & Readiness Final Screen Contract IA_CORE contract-aware sin runtime/no-execution{bt}" in root
    )
    assert NEXT_PROMPT in web
    assert "Documentacion Blocked & Forbidden Final Screen Contract 1.69" in root
    assert "Documentacion Blocked & Forbidden Final Screen Contract 1.69" in web
    assert "push pospuesto" in root.lower()
    assert "push pospuesto" in web.lower()
