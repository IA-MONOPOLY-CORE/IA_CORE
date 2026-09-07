"""Documentation-only post-mortem guard for UI/UX 1.194."""

from pathlib import Path
import subprocess
import unicodedata

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "307067d"
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_ASSEMBLED_BLOCK_1_194_POSTMORTEM_1_195.md"
TEST = ROOT / "tests" / "test_ui_ux_panel_maestro_assembled_block_1_194_postmortem_1_195.py"
COMMIT_MESSAGE = "docs(ui): analizar postmortem bloque ensamblado 1.194"
PRODUCT_FILES = {
    "ui/web/index.html", "ui/web/styles.css", "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json", "ui/web/admin-panels.js", "ui/web/console-interactions.js",
    "ui/web/domains.js", "core/backend_internal_ui_payloads.py", "api.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def station_commit(message: str) -> str:
    matches = [line.split("\t", 1)[0] for line in git("log", "--all", "--format=%H%x09%s").splitlines() if "\t" in line and line.split("\t", 1)[1] == message]
    assert len(matches) == 1, message
    return matches[0]


def test_postmortem_has_required_operational_evidence():
    content = normalized(read(DOC))
    for marker in (
        "assembled_block_1_194_postmortem_passed", "307067d", "6/6", "intervenciones del operador: 0",
        "rollbacks: 0", "correctivos: 0", "322 tests passed", "0 failures", "0 skips",
        "preautorizaciones", "blockers", "retries", "validaciones redundantes",
        "presion de contexto", "luna muy alto", "infraestructura de tests",
        "resolved", "partially_resolved", "active_debt", "infrastructure_debt",
        "semantic_frontier", "architectural_frontier", "future_layer",
        "microcopy contractual", "no ejecuta ui/ux 1.196",
    ):
        assert normalized(marker) in content, marker


def test_postmortem_commit_is_documental_only():
    commit = station_commit(COMMIT_MESSAGE)
    files = set(filter(None, git("show", "--format=", "--name-only", commit).splitlines()))
    assert files <= {DOC.relative_to(ROOT).as_posix(), TEST.relative_to(ROOT).as_posix(), "tests/ui_ux_1_192_scope.py"}
    for path in PRODUCT_FILES:
        assert subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", path], cwd=ROOT, check=False).returncode == 0, path


def test_postmortem_does_not_execute_next_prompt_or_add_product_scope():
    content = normalized(read(DOC))
    assert "no implementa ui" in content
    assert "no modifica producto" in content
    assert "no ejecuta ui/ux 1.196" in content
    assert "payload v2" not in content or "no payload" in content
    assert "continuity_1_195" in normalized(read(ROOT / "tests" / "ui_ux_1_192_scope.py"))
