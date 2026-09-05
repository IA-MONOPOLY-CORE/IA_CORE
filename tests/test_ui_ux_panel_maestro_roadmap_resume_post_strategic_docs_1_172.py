from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_ROADMAP_RESUME_POST_STRATEGIC_DOCS_1_172.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"


ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_ROADMAP_RESUME_POST_STRATEGIC_DOCS_1_172.md",
    "tests/test_ui_ux_panel_maestro_roadmap_resume_post_strategic_docs_1_172.py",
}


FUTURE_CAPABILITIES = [
    "integraciones reales",
    "usuarios reales",
    "auth real",
    "Owner Console real",
    "Client Edition real",
    "Financial Mirror real",
    "Tax Mirror real",
    "Legal real",
    "Security runtime real",
    "chat interno real",
    "modulos enterprise reales",
    "multi-tenant real",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).strip()


def changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return tracked | untracked


def test_resume_document_exists():
    assert DOC.is_file()


def test_resume_document_has_required_markers():
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro IA_CORE",
        "Roadmap Resume Post Strategic Docs 1.172",
        "81dc766",
        "5fc5d35",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
        "STRATEGIC_FUTURE_ENTERPRISE_ARCHITECTURE_DOCUMENTED",
        "UI_UX_ROADMAP_RESUMED_POST_STRATEGIC_DOCS",
        "no-runtime",
        "no-execution",
        "sin runtime",
        "sin execution",
        "contract-aware",
        "UI ghost",
        "acciones falsas",
        "datos decorativos",
    ]:
        assert marker in text


def test_strategic_docs_do_not_enable_current_capabilities():
    text = normalized(read(DOC))
    assert "strategic docs 1.0 no habilita como capacidad actual" in text
    for capability in FUTURE_CAPABILITIES:
        assert normalized(capability) in text


def test_next_prompt_is_declared_without_execution():
    assert (
        "PROMPT UI/UX 1.173 — Auditar cursor real del roadmap UI/UX Panel Maestro IA_CORE y seleccionar próximo bloque visual contract-aware sin runtime/no-execution"
        in read(DOC)
    )
    assert "sin ejecutarlo" in normalized(read(DOC))


def test_readmes_record_cursor_1_172():
    root_text = read(README)
    for marker in [
        "UI/UX 1.172",
        "STRATEGIC DOCS 1.0",
        "no-runtime",
        "no-execution",
    ]:
        assert marker in root_text

    web_text = read(WEB_README)
    for marker in [
        "UI/UX 1.172",
        "no UI activa modificada",
        "contract-aware",
        "no-runtime/no-execution",
    ]:
        assert marker in web_text


CLAUSE_BOUNDARY = re.compile(r"[.!?;]\s+|\bpero\b|\baunque\b|\bsin embargo\b", re.I)
CURRENT_CLAIM = re.compile(
    r"\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?"
    r"(?:ejecuta|opera|administra|factura|declara|paga|conecta|envia|envía|"
    r"responde|controla|recupera|instala|activa)\b"
    r"|\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?(?:tiene|dispone de|ofrece)\s+"
    r"(?:integraciones reales|usuarios reales|auth real|owner console real|"
    r"client edition real|financial mirror real|tax mirror real|legal real|"
    r"security runtime real|chat interno real|modulos enterprise reales|"
    r"multi-tenant real|runtime real|execution real)\b"
    r"|\b(?:owner console|client edition|financial mirror|tax mirror|legal|"
    r"security runtime|chat interno|multi-tenant)\s+"
    r"(?:(?:actualmente|hoy|ya)\s+)?(?:es|esta|está)\s+"
    r"(?:operativo|operativa|real|activo|activa|disponible|implementado|implementada)\b",
    re.I,
)
NON_CURRENT_CONTEXT = re.compile(
    r"^(?:no\b|sin\b|prohibido\b|no se debe\b|no debe\b|no afirmar\b|"
    r"no habilita\b|documentar\b|documentacion\b|documentación\b|"
    r"vision futura\b|visión futura\b|arquitectura futura\b|pendiente\b|"
    r"en el futuro\b|como capacidad futura\b|como documentacion futura\b|"
    r"como documentación futura\b|estrategico\b|estratégico\b)",
    re.I,
)


def current_operational_claims(text: str) -> list[str]:
    claims = []
    for paragraph in re.split(r"\n\s*\n", text):
        for clause in CLAUSE_BOUNDARY.split(normalized(paragraph)):
            clause = clause.strip(" -*#>`\"")
            if CURRENT_CLAIM.search(clause) and not NON_CURRENT_CONTEXT.match(clause):
                claims.append(clause)
    return claims


def test_document_does_not_claim_future_capabilities_are_current():
    assert current_operational_claims(read(DOC)) == []


def test_claim_guard_detects_unsafe_affirmations_without_restriction_prefix():
    unsafe = [
        "IA_CORE actualmente ejecuta capacidades futuras.",
        "IA_CORE ya conecta integraciones reales.",
        "IA_CORE tiene Owner Console real.",
        "Financial Mirror es operativo.",
        "IA_CORE dispone de multi-tenant real.",
    ]
    for phrase in unsafe:
        assert current_operational_claims(phrase), phrase


def test_claim_guard_accepts_negations_future_and_documentary_scope():
    safe = [
        "No afirmar que IA_CORE actualmente ejecuta capacidades futuras.",
        "IA_CORE no conecta integraciones reales.",
        "Documentacion estrategica: Owner Console real pendiente de implementacion.",
        "Vision futura: Financial Mirror real requiere contrato propio.",
        "No habilita multi-tenant real como capacidad actual.",
    ]
    for phrase in safe:
        assert current_operational_claims(phrase) == [], phrase


def test_diff_is_limited_to_prompt_allowed_files():
    assert changed_paths() <= ALLOWED_DIFF
