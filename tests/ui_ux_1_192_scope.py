"""Explicit historical revisions and deny-by-default continuity for UI/UX 1.192."""

import ast
from pathlib import Path
import subprocess

BASE = "82dd100"
CSS = "ui/web/styles.css"
DOC = "docs/UI_UX_PANEL_MAESTRO_CONTROLLED_DOUBLE_SCOPE_AFFORDANCES_SEVERITY_1_192.md"
TEST = "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py"
HELPER = "tests/ui_ux_1_192_scope.py"
CHECKPOINTS = {
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py": "8ed0c3e",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py": "e2d1653",
    "tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py": "82dd100",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py": "e9f5b94",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_185.py": "9f83c34",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py": "72b6f71",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py": "07367d5",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py": "66d73e3",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py": "cef7b11",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py": "4403489",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py": "3da91a8",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py": "82705e4",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py": "d960aeb",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py": "d1c2486",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py": "b8db98f",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py": "2ab27f9",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py": "aeb7607",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py": "fdc2b7d",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py": "d98e999",
}
READMES = {"README.md", "ui/web/README.md"}
ALLOWED = {CSS, DOC, TEST, HELPER} | READMES | CHECKPOINTS.keys()
PATH_HELPERS = {"changed_paths", "working_paths", "checkpoint_paths", "selection_paths"}
IMPORT = "from ui_ux_1_192_scope import historical_paths, assert_current_scope"
CURRENT_TEST = """def test_current_scope_is_strict_1_192():
    assert_current_scope(ROOT)
"""
GATE_1_CSS = """
/* UI/UX 1.192 Gate 1: existing administrative controls remain non-executable. */
body .console-utilities[data-interaction-scope="existing-management"] > :is(#settings-fab, #add-fab, #domain-fab)[data-contract-blocked="true"]:disabled[aria-disabled="true"] {
    background: rgba(148, 163, 184, 0.05);
    border: 1px dashed rgba(148, 163, 184, 0.4);
    color: #b4bdc9;
    opacity: 1;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
    transition: none;
    animation: none;
    letter-spacing: 0;
}
"""
GATE_2_CSS = """
/* UI/UX 1.192 Gate 2: emphasize the existing contractual boundary, not an action. */
body .console-utilities[data-interaction-scope="existing-management"] > .admin-status[data-contract-blocked="true"] {
    color: var(--amber);
    border-inline-start: 2px solid var(--amber);
    padding-inline-start: 10px;
    margin-block: 0;
    min-width: 0;
    max-width: 100%;
    overflow-wrap: anywhere;
    line-height: 1.5;
    letter-spacing: 0;
    cursor: default;
}
"""


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def text(blob):
    return blob.decode("utf-8").replace("\r\n", "\n")


def historical_paths(root, checkpoint):
    assert checkpoint in CHECKPOINTS.values(), "Unknown historical checkpoint"
    return set(text(git(root, "diff", "--name-only", "--no-renames",
                        checkpoint + "^", checkpoint)).splitlines())


def path_helper_source(name):
    return (f"def {name}() -> set[str]:\n"
            '    """Paths in this closed checkpoint, never the current worktree."""\n'
            "    return historical_paths(ROOT, HISTORICAL_COMMIT)\n")


class HistoricalEndpoints(ast.NodeTransformer):
    """Only make implicit Git diff endpoints explicit; retain every assertion."""

    def visit_FunctionDef(self, node):
        if node.name in PATH_HELPERS:
            return ast.parse(path_helper_source(node.name)).body[0]
        return self.generic_visit(node)

    def visit_Call(self, node):
        self.generic_visit(node)
        args = None
        if isinstance(node.func, ast.Name) and node.func.id in {"git", "git_lines"}:
            args = node.args
        elif (isinstance(node.func, ast.Attribute) and
              isinstance(node.func.value, ast.Name) and
              node.func.value.id == "subprocess" and node.func.attr == "run" and
              node.args and isinstance(node.args[0], ast.List)):
            args = node.args[0].elts
        if args is None:
            return node
        offset = 1 if args and isinstance(args[0], ast.Constant) and args[0].value == "git" else 0
        if len(args) <= offset or not isinstance(args[offset], ast.Constant) or args[offset].value != "diff":
            return node
        revised = []
        for arg in args:
            if isinstance(arg, ast.Constant) and arg.value == "HEAD":
                revised.extend([
                    ast.BinOp(left=ast.Name(id="HISTORICAL_COMMIT", ctx=ast.Load()),
                              op=ast.Add(), right=ast.Constant(value="^")),
                    ast.Name(id="HISTORICAL_COMMIT", ctx=ast.Load()),
                ])
            elif isinstance(arg, ast.Name) and arg.id == "BASE":
                revised.extend([arg, ast.Name(id="HISTORICAL_COMMIT", ctx=ast.Load())])
            else:
                revised.append(arg)
        args[:] = revised
        return node


def expected_historical_tree(original, checkpoint):
    tree = HistoricalEndpoints().visit(ast.parse(original))
    # Keep the docstring first, then the explicit continuity import and revision.
    tree.body[1:1] = ast.parse(
        IMPORT + "\n" + f'HISTORICAL_COMMIT = "{checkpoint}"\n'
    ).body
    tree.body.extend(ast.parse(CURRENT_TEST).body)
    return ast.fix_missing_locations(tree)


def assert_historical_adaptation(original, current, checkpoint):
    expected = expected_historical_tree(original, checkpoint)
    assert ast.dump(ast.parse(current)) == ast.dump(expected), (
        "Historical change exceeds explicit endpoint migration; assertions must remain intact"
    )


def assert_css(before, after):
    # Accept only the committed Gate 1 snapshot or both exact authorized additions.
    gate_1 = before + GATE_1_CSS
    assert after in (gate_1, gate_1 + GATE_2_CSS), "CSS exceeds the exact Gate 1/Gate 2 additions"


def assert_snapshot(changes, baselines):
    assert changes.keys() <= ALLOWED, f"Forbidden paths: {sorted(changes.keys() - ALLOWED)}"
    for path, blob in changes.items():
        assert blob is not None, f"Deletion forbidden: {path}"
        current = text(blob)
        if path == CSS:
            assert_css(text(baselines[path]), current)
        elif path in CHECKPOINTS:
            assert_historical_adaptation(text(baselines[path]), current, CHECKPOINTS[path])
        elif path in READMES:
            before = text(baselines[path])
            assert current.startswith(before), f"Historical README content changed: {path}"
            assert current[len(before):].lstrip().startswith("## UI/UX 1.192"), path


def assert_current_scope(root):
    """Check staged and working changes independently, including commits since BASE."""
    root = Path(root)
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=root, check=True)
    for staged in (False, True):
        options = ["--cached"] if staged else []
        names = set(text(git(root, "diff", *options, "--name-only", "--no-renames", BASE)).splitlines())
        if not staged:
            names.update(text(git(root, "ls-files", "--others", "--exclude-standard")).splitlines())
        assert names <= ALLOWED, f"Forbidden {'index' if staged else 'worktree'} paths: {sorted(names - ALLOWED)}"
        changes = {}
        baselines = {}
        for path in names:
            if staged:
                changes[path] = git(root, "show", ":" + path)
            else:
                file = root / path
                assert file.is_file() and not file.is_symlink(), f"Not a regular file: {path}"
                changes[path] = file.read_bytes()
            if path in READMES or path in CHECKPOINTS or path == CSS:
                baselines[path] = git(root, "show", f"{BASE}:{path}")
        assert_snapshot(changes, baselines)
        # Content checks must not let a symlink or executable-bit change through.
        summary = text(git(root, "diff", *options, "--summary", BASE))
        assert "mode change" not in summary and "120000" not in summary, summary
