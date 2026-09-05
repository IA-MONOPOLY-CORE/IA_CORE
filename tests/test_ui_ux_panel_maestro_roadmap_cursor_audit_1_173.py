from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_ROADMAP_CURSOR_AUDIT_1_173.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"

NEXT_PROMPT = (
    "PROMPT UI/UX 1.174 — Reconstruir widgets del Panel Maestro IA_CORE como "
    "indicadores contract-aware basados en datos documentales existentes sin "
    "runtime/no-execution"
)

ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_ROADMAP_CURSOR_AUDIT_1_173.md",
    "tests/test_ui_ux_panel_maestro_roadmap_cursor_audit_1_173.py",
}

PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/src",
    "ui/web/styles",
    "ui/web/i18n",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
    "backend",
    "core",
    "domains",
    "providers",
    "integrations",
    "tools",
]

FUTURE_CAPABILITIES = [
    "integraciones",
    "usuarios reales",
    "auth real",
    "Owner Console",
    "Client Edition",
    "Financial Mirror",
    "Tax Mirror",
    "Legal",
    "Security runtime",
    "chat interno",
    "modulos enterprise",
    "multi-tenant",
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


def test_cursor_audit_document_exists():
    assert DOC.is_file()


def test_cursor_audit_has_required_markers():
    text = read(DOC)
    for marker in [
        "UI/UX Panel Maestro IA_CORE",
        "Roadmap Cursor Audit 1.173",
        "c38a3d3",
        "81dc766",
        "5fc5d35",
        "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
        "STRATEGIC_FUTURE_ENTERPRISE_ARCHITECTURE_DOCUMENTED",
        "UI_UX_ROADMAP_RESUMED_POST_STRATEGIC_DOCS",
        "UI_UX_ROADMAP_CURSOR_AUDITED_NEXT_BLOCK_SELECTED",
        "contract-aware",
        "no-runtime",
        "no-execution",
        "UI ghost",
        "acciones falsas",
        "widgets decorativos",
        "datos falsos",
        "capacidades futuras como actuales",
    ]:
        assert marker in text


def test_strategic_docs_do_not_enable_current_capabilities():
    text = normalized(read(DOC))
    assert "no habilita como capacidades actuales" in text
    for capability in FUTURE_CAPABILITIES:
        assert normalized(capability) in text


def test_exactly_one_next_prompt_is_selected_without_execution():
    text = read(DOC)
    assert text.count(NEXT_PROMPT) == 1
    assert len(re.findall(r"PROMPT UI/UX 1\.174\b", text)) == 1
    assert "un unico proximo prompt, sin ejecutarlo" in normalized(text)


def test_recommended_scope_is_safe_and_contract_backed():
    text = read(DOC)
    for marker in [
        "Auditar los widgets y metricas existentes",
        "backend_internal_ui_payload.v1",
        "fuente documental o contractual existente",
        "Definir nombres, estados, textos, restricciones",
        "fallback",
        "transformacion visual minima",
        "sin consumir APIs nuevas",
        "sin inventar datos",
        "sin tocar backend",
    ]:
        assert normalized(marker) in normalized(text)


def test_readmes_record_cursor_and_selected_block():
    root_text = read(README)
    for marker in [
        "UI/UX 1.173",
        "cursor real del roadmap",
        "proximo bloque seleccionado",
        "no-runtime",
        "no-execution",
        "UI/UX 1.174",
        "widgets contract-aware",
    ]:
        assert marker in root_text

    web_text = read(WEB_README)
    for marker in [
        "UI/UX 1.173",
        "roadmap UI/UX",
        "contract-aware",
        "no-runtime/no-execution",
        "proximo bloque visual seguro",
    ]:
        assert marker in web_text


CLAUSE_BOUNDARY = re.compile(r"[.!?;]\s+|\bpero\b|\baunque\b|\bsin embargo\b", re.I)
CURRENT_CLAIM = re.compile(
    r"\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?"
    r"(?:ejecuta|opera|administra|factura|declara|paga|conecta|envia|envía|"
    r"responde|controla|recupera|instala|activa)\b"
    r"|\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?(?:tiene|dispone de|ofrece)\s+"
    r"(?:integraciones reales|usuarios reales|auth real|owner console|"
    r"client edition|financial mirror|tax mirror|security runtime|chat interno|"
    r"modulos enterprise|multi-tenant|runtime real|execution real)\b"
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


def test_claim_guard_detects_unsafe_affirmations():
    unsafe = [
        "IA_CORE actualmente ejecuta capacidades futuras.",
        "IA_CORE ya conecta integraciones reales.",
        "IA_CORE tiene Owner Console.",
        "Financial Mirror es operativo.",
        "IA_CORE dispone de multi-tenant.",
    ]
    for phrase in unsafe:
        assert current_operational_claims(phrase), phrase


def test_claim_guard_accepts_negated_future_and_documentary_scope():
    safe = [
        "No afirmar que IA_CORE actualmente ejecuta capacidades futuras.",
        "IA_CORE no conecta integraciones reales.",
        "Documentacion estrategica: Owner Console pendiente de implementacion.",
        "Vision futura: Financial Mirror requiere contrato propio.",
        "No habilita multi-tenant como capacidad actual.",
    ]
    for phrase in safe:
        assert current_operational_claims(phrase) == [], phrase


def test_diff_is_limited_and_protected_paths_are_untouched():
    assert changed_paths() <= ALLOWED_DIFF
    for path in PROTECTED_PATHS:
        assert git("diff", "--name-only", "HEAD", "--", path) == ""
