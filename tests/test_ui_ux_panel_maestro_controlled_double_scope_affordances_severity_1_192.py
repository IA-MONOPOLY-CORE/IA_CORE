"""Gate 1 scope, historical continuity and regression checks for UI/UX 1.192."""

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import unicodedata

import ast
import pytest

import ui_ux_1_192_scope as scope


ROOT = Path(__file__).resolve().parents[1]
BASE = "82dd100"
DOC = "docs/UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_AFFORDANCES_SEVERITY_1_192.md"
TEST = "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py"
MARKER = "/* UI/UX 1.192 Gate 1: existing administrative controls remain non-executable. */"
SELECTOR = 'body .console-utilities[data-interaction-scope="existing-management"] > :is(#settings-fab, #add-fab, #domain-fab)[data-contract-blocked="true"]:disabled[aria-disabled="true"]'
CONTROL_IDS = {"settings-fab": "CFG", "add-fab": "+", "domain-fab": "DOMAIN"}
ALLOWED = scope.ALLOWED | {
    "docs/ROADMAP_3_X_MACRO_02_2_FAILURE_ACCOUNTABILITY_LEDGER.md",
    "tests/test_roadmap_3_x_macro_02_2_failure_ledger.py",
    "tests/historical_test_context.py",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def normalized(text):
    return " ".join("".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)).casefold().split())


def test_gate_1_css_is_append_only_and_scoped_to_disabled_controls():
    before = git("show", f"{BASE}:ui/web/styles.css")
    after = git("show", "055e70e:ui/web/styles.css")
    scope.assert_css(before, after)
    assert after.startswith(before + scope.GATE_1_CSS)
    addition = scope.GATE_1_CSS.strip()
    assert addition.startswith(MARKER)
    rule = addition[len(MARKER):].strip()
    assert rule.startswith(SELECTOR + " {")
    assert rule.count("{") == rule.count("}") == 1
    declarations = dict(re.findall(r"([a-z-]+)\s*:\s*([^;{}]+);", rule[len(SELECTOR):]))
    assert declarations == {
        "background": "rgba(148, 163, 184, 0.05)",
        "border": "1px dashed rgba(148, 163, 184, 0.4)",
        "color": "#b4bdc9", "opacity": "1", "cursor": "not-allowed",
        "box-shadow": "none", "transform": "none", "transition": "none",
        "animation": "none", "letter-spacing": "0",
    }


def test_existing_controls_remain_disabled_and_html_is_identical():
    html = (ROOT / "ui/web/index.html").read_text(encoding="utf-8")
    assert html == git("show", f"{BASE}:ui/web/index.html")

    class Controls(HTMLParser):
        def __init__(self):
            super().__init__()
            self.found = {}
            self.current = None

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "button" and attrs.get("id") in CONTROL_IDS:
                self.current = attrs["id"]
                self.found[self.current] = {"attrs": attrs, "text": ""}

        def handle_data(self, data):
            if self.current:
                self.found[self.current]["text"] += data

        def handle_endtag(self, tag):
            if tag == "button":
                self.current = None

    parser = Controls()
    parser.feed(html)
    assert set(parser.found) == set(CONTROL_IDS)
    for control_id, text in CONTROL_IDS.items():
        item = parser.found[control_id]
        attrs = item["attrs"]
        assert item["text"] == text
        assert "disabled" in attrs and attrs["aria-disabled"] == "true"
        assert attrs["type"] == "button" and attrs["data-contract-blocked"] == "true"
        assert attrs["data-no-runtime"] == attrs["data-no-execution"] == attrs["data-no-mutation"] == "true"


def test_gate_2_only_adds_the_existing_administrative_boundary_style():
    before = git("show", "055e70e:ui/web/styles.css")
    after = git("show", "6ae13f4:ui/web/styles.css")
    assert after.startswith(before + scope.GATE_2_CSS)
    assert after in (
        {
            git("show", "6ae13f4:ui/web/styles.css"),
        }
        | scope.authorized_1_194_css_snapshots(ROOT)
        | scope.authorized_1_196_css_snapshots(ROOT)
        | scope.authorized_1_200_css_snapshots(ROOT)
    )
    html = (ROOT / "ui/web/index.html").read_text(encoding="utf-8")
    assert html == git("show", f"{BASE}:ui/web/index.html")
    assert html.count('<span class="admin-status" data-contract-blocked="true">') == 1


@pytest.mark.parametrize("addition", [
    scope.GATE_2_CSS.replace('body .console-utilities[data-interaction-scope="existing-management"] > ', ''),
    scope.GATE_2_CSS.replace('[data-contract-blocked="true"]', ''),
    scope.GATE_2_CSS.replace('.admin-status', '#request-contract-status'),
    scope.GATE_2_CSS.replace('cursor: default', 'cursor: pointer'),
    scope.GATE_2_CSS.replace('color: var(--amber);', 'color: green;'),
    scope.GATE_2_CSS.replace('line-height: 1.5;', 'display: none;'),
    scope.GATE_2_CSS.replace('line-height: 1.5;', 'opacity: 0;'),
    scope.GATE_2_CSS.replace('cursor: default;', 'cursor: pointer; cursor: default;'),
    scope.GATE_2_CSS + '\nbody { color: red; }\n',
    scope.GATE_2_CSS + '\n/* backend_internal_ui_payload.v2 */\n',
])
def test_gate_2_cannot_expand_severity_scope_or_hide_the_boundary(addition):
    with pytest.raises(AssertionError, match="exact Gate 1/Gate 2"):
        scope.assert_css("existing\n", "existing\n" + scope.GATE_1_CSS + addition)


def test_only_proposal_and_reporting_files_change():
    historical_head = "6ae13f4"
    scope.assert_current_scope(ROOT, head=historical_head, baseline=BASE, allowed_paths=ALLOWED)
    paths = set(git("diff", "--name-only", BASE, historical_head).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    assert paths <= ALLOWED, sorted(paths - ALLOWED)
    assert git("diff", "--name-only", BASE, historical_head, "--", "ui/web/index.html", "ui/web/*.js", "ui/web/i18n_es.json", "core", "api.py", "domains", "providers", "tools", "scripts", "integrations", "runtime", "execution", ".github").strip() == ""


def test_report_records_final_double_scope_completion_without_claiming_193_execution():
    doc = normalized((ROOT / DOC).read_text(encoding="utf-8"))
    for token in (
        "UI/UX Panel Maestro Controlled Double Scope Affordances Severity 1.192",
        BASE, "Candidato I", "gates internos", "commits internos", "no triple",
        "GATE_1_AFFORDANCES_BLOCKED_PASSED", "GATE_2_SEVERITY_VISUAL_PASSED",
        "HISTORICAL_GUARDS_1_192_RESOLVED", "DOUBLE_SCOPE_FULLY_IMPLEMENTED",
        "NO_CORRECTIVE_NEEDED", "UI_UX_CONTROLLED_DOUBLE_SCOPE_AFFORDANCES_SEVERITY_PASSED",
        "ready_for_ui_ux_1_193_controlled_double_scope_affordances_severity_checkpoint",
        "PROMPT UI/UX 1.193", "055e70e", "6ae13f4",
        "clientWidth", "scrollWidth", "modelo usado", "nivel de esfuerzo",
        "consumo", "calidad percibida", "recomendacion armonica",
    ):
        assert normalized(token) in doc, token
    assert "prompt ui/ux 1.193" in doc
    assert "gate 2 no ejecutado" in doc
    assert "ui/ux 1.192 bloqueado" in doc


@pytest.mark.parametrize("path", [
    "ui/web/index.html", "ui/web/backend-contract-widgets.js", "ui/web/i18n_es.json",
    "ui/web/admin-panels.js", "ui/web/console-interactions.js", "ui/web/domains.js",
    "api.py", "core/backend_internal_ui_payloads.py", "core/new.py", "runtime/new.py",
    "execution/new.py", "endpoints/new.py", "integrations/new.py", "providers/new.py",
    "domains/new.py", "tools/new.py", "scripts/new.py", ".github/workflows/new.yml",
    ".env", "package.json", "payloads/backend_internal_ui_payload.v2.json",
    "docs/unapproved.md", "tests/unapproved.py",
])
def test_forbidden_paths_are_rejected_even_with_all_continuity_artifacts(path):
    changes = {DOC: b"report", TEST: b"test", scope.HELPER: b"helper", path: b"change"}
    with pytest.raises(AssertionError, match="Forbidden paths"):
        scope.assert_snapshot(changes, {})


@pytest.mark.parametrize("addition", [
    scope.GATE_1_CSS.replace(':disabled', ''),
    scope.GATE_1_CSS.replace('[aria-disabled="true"]', ''),
    scope.GATE_1_CSS.replace('#settings-fab, #add-fab, #domain-fab', '*'),
    scope.GATE_1_CSS.replace('cursor: not-allowed', 'cursor: pointer'),
    scope.GATE_1_CSS.replace('opacity: 1;', 'opacity: 0; opacity: 1;'),
    scope.GATE_1_CSS + '\nbody { display: none; }\n',
    scope.GATE_1_CSS + '\n#request-draft-panel { opacity: 0; }\n',
    scope.GATE_1_CSS + '\n.closure-matrix-row { display: none; }\n',
    scope.GATE_1_CSS + '\n#functional-widgets { display: none; }\n',
    scope.GATE_1_CSS + '\n.p0-command-summary { display: none; }\n',
    scope.GATE_1_CSS + '\n.final-screen-contracts-rehousing { display: none; }\n',
    scope.GATE_1_CSS + '\n/* backend_internal_ui_payload.v2 */\n',
])
def test_css_cannot_expand_scope_or_enable_controls(addition):
    with pytest.raises(AssertionError, match="exact Gate 1"):
        scope.assert_css("existing\n", "existing\n" + addition)


def test_old_css_and_file_deletions_remain_prohibited():
    with pytest.raises(AssertionError):
        scope.assert_css("existing\n", "changed\n" + scope.GATE_1_CSS)
    with pytest.raises(AssertionError, match="Deletion forbidden"):
        scope.assert_snapshot({scope.CSS: None}, {scope.CSS: b"existing\n"})


def test_readmes_allow_only_append_only_1_192_notes():
    scope.assert_snapshot({"README.md": b"history\n\n## UI/UX 1.192\nnote"},
                          {"README.md": b"history\n"})
    for value in (b"rewritten\n## UI/UX 1.192", b"history\n\n## UI/UX 1.193"):
        with pytest.raises(AssertionError):
            scope.assert_snapshot({"README.md": value}, {"README.md": b"history\n"})


@pytest.mark.parametrize("path", sorted(scope.CHECKPOINTS))
def test_historical_assertions_and_allowlists_are_preserved_structurally(path):
    original = git("show", f"{BASE}:{path}")
    actual = (ROOT / path).read_text(encoding="utf-8")
    scope.assert_historical_adaptation(original, actual, scope.CHECKPOINTS[path])
    before = ast.parse(original)
    after = ast.parse(actual)
    assert sum(isinstance(n, ast.Assert) for n in ast.walk(before)) == sum(
        isinstance(n, ast.Assert) for n in ast.walk(after)
    )


@pytest.mark.parametrize("mutation", ["remove_assert", "allow_html", "skip", "wrong_checkpoint"])
def test_historical_guard_weakening_is_rejected(mutation):
    path = "tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py"
    original = git("show", f"{BASE}:{path}")
    tree = scope.expected_historical_tree(original, scope.CHECKPOINTS[path])
    if mutation == "remove_assert":
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                node.test = ast.Constant(value=True)
                break
    elif mutation == "allow_html":
        tree.body.append(ast.parse('ALLOWED_DIFF.add("ui/web/index.html")').body[0])
    elif mutation == "skip":
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                node.body.insert(0, ast.Return(value=None))
                break
    else:
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "HISTORICAL_COMMIT" for t in node.targets):
                node.value = ast.Constant(value="HEAD")
    with pytest.raises(AssertionError, match="Historical change exceeds"):
        scope.assert_historical_adaptation(original, ast.unparse(tree), scope.CHECKPOINTS[path])


@pytest.mark.parametrize("staged", [False, True])
def test_current_guard_inspects_worktree_and_index_independently(monkeypatch, staged):
    calls = []

    def fake_git(root, *args):
        calls.append(args)
        if "--name-only" in args and ("--cached" in args) == staged:
            return b"ui/web/index.html\n"
        return b""

    monkeypatch.setattr(scope, "git", fake_git)
    monkeypatch.setattr(scope.subprocess, "run", lambda *args, **kwargs: None)
    with pytest.raises(AssertionError, match="Forbidden"):
        scope.assert_current_scope(ROOT)
    assert any("--name-only" in c and ("--cached" in c) == staged for c in calls)
