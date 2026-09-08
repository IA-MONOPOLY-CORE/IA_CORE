"""S6 documentation/test-only checkpoint for the assembled UI/UX 1.194 block."""

from pathlib import Path
import subprocess
import unicodedata

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "f5ddde4"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_RESPONSIVE_VISUAL_COHERENCE_ASSEMBLED_BLOCK_1_194.md"
TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_responsive_visual_coherence_assembled_block_1_194.py"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
S6_MESSAGE = "docs(ui): checkpoint bloque ensamblado responsive coherencia visual"
STATIONS = {
    "feat(ui): corregir containment responsive panel maestro": "7196ad5",
    "feat(ui): consolidar severidad visual existente": "88824b8",
    "feat(ui): unificar coherencia visual widgets badges blockers": "6e4adaf",
    "feat(ui): optimizar densidad visual p2 p3": "a29a26f",
    "feat(ui): mejorar accesibilidad y legibilidad panel maestro": "d7321d2",
}
PRODUCT_FILES = {
    "ui/web/index.html",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
}
ALLOWED_FILES = {
    "ui/web/styles.css",
    "tests/ui_ux_1_192_scope.py",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_checkpoint_1_193.py",
    "tests/test_ui_ux_panel_maestro_assembled_block_scale_audit_1_193.py",
    "README.md",
    "ui/web/README.md",
    DOC.relative_to(ROOT).as_posix(),
    TEST.relative_to(ROOT).as_posix(),
} | scope.CONTINUITY_1_194 | scope.CONTINUITY_1_195
ALLOWED_FILES |= scope.CONTINUITY_1_196
ALLOWED_FILES |= scope.CONTINUITY_1_197
ALLOWED_FILES |= scope.CONTINUITY_1_198


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return " ".join("".join(c for c in decomposed if not unicodedata.combining(c)).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def commit_for(message: str) -> str:
    matches = [
        line.split("\t", 1)[0]
        for line in git("log", "--all", "--format=%H%x09%s").splitlines()
        if "\t" in line and line.split("\t", 1)[1] == message
    ]
    assert len(matches) == 1, f"expected one station commit: {message}"
    return matches[0]


def changed_paths(base: str, head: str = "HEAD") -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "--no-renames", base, head).splitlines()))
    untracked = set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return tracked | untracked


def test_checkpoint_document_contains_complete_assembled_block_contract():
    assert DOC.is_file()
    content = normalized(read(DOC))
    markers = [
        "UI/UX Panel Maestro - Bloque ensamblado responsive y coherencia visual 1.194",
        "f5ddde4", "auditoria 1.193", "GPT-5.6 Luna Muy Alto", "muy alto",
        "inicio observable", "cierre documental s6", "estaciones planificadas",
        "s1", "s2", "s3", "s4", "s5", "s6", "commits independientes",
        "no existe commit globo", "tests focales", "suite integral", "desktop",
        "mobile", "clientwidth", "scrollwidth", "consola", "p0 preservado",
        "p1 preservado", "matriz p3 preservada", "widgets contract-aware",
        "request draft panel", "backend_internal_ui_payload.v1", "payload v2 ausente",
        "no runtime", "no execution", "no endpoints", "no integrations",
        "autonomia condicionada", "bloqueos previsibles", "intervenciones manuales",
        "retries", "estaciones completadas", "microcopy transversal",
        "motion", "audiovisual", "ui_ux_responsive_visual_coherence_assembled_block_passed",
        "ready_for_ui_ux_1_195_post_assembled_block_direction_review",
        "no se ejecuta ui/ux 1.195", "ui/ux 1.194 cerrado",
    ]
    missing = [marker for marker in markers if normalized(marker) not in content]
    assert not missing, missing


def test_each_station_has_one_independent_commit_and_s6_is_documental():
    for message, prefix in STATIONS.items():
        assert commit_for(message).startswith(prefix), message
    s6 = commit_for(S6_MESSAGE)
    files = set(filter(None, git("show", "--format=", "--name-only", s6).splitlines()))
    assert files <= {"README.md", "ui/web/README.md", DOC.relative_to(ROOT).as_posix(), TEST.relative_to(ROOT).as_posix()}


def test_assembled_block_scope_keeps_product_contract_closed():
    assert changed_paths(BASE) <= ALLOWED_FILES
    for path in PRODUCT_FILES:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path
    current_css = read(ROOT / "ui" / "web" / "styles.css")
    scope.assert_css(scope.text(scope.git(ROOT, "show", f"{scope.BASE}:{scope.CSS}")), current_css, ROOT)
    assert "backend_internal_ui_payload.v1" in normalized(read(ROOT / "ui" / "web" / "index.html") + read(ROOT / "ui" / "web" / "backend-contract-widgets.js"))
    active = "\n".join(read(ROOT / path) for path in ("ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js", "core/backend_internal_ui_payloads.py")).casefold()
    for forbidden in ("backend_internal_ui_payload.v2", "payload.v2", 'schema_version": "v2"'):
        assert forbidden not in active, forbidden


def test_readmes_record_assembled_block_without_operational_scope():
    for path in (README, WEB_README):
        content = normalized(read(path))
        for marker in ("ui/ux 1.194", "bloque ensamblado", "no runtime", "no execution", "payload v2"):
            assert marker in content, (path, marker)


def test_s6_guard_rejects_unapproved_product_or_operational_changes():
    helper = read(ROOT / "tests" / "ui_ux_1_192_scope.py")
    assert "CONTINUITY_1_194" in helper
    assert "AUTHORIZED_1_194_STATION_MESSAGES" in helper
    assert "payload v2 ausente" in normalized(read(DOC))
    assert "no acciones nuevas" in normalized(read(DOC))
