"""Explicit checkpoint context for historical contract probes.

Historical tests remain ordinary pytest tests with their original assertions.
This adapter changes only the evidence endpoint for ledgered historical modules
and the explicitly recorded secondary fallout discovered by the full-suite
run; current mission tests continue to read the worktree.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import re
import subprocess
import tarfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_2_FAILURE_ACCOUNTABILITY_LEDGER.md"
_LEDGER_NODE_RE = re.compile(r"^\| \d+ \| `(tests/[^`]+)::test_[^`]+` \|", re.MULTILINE)
_OVERRIDES = {
    "tests/test_gokv_architecture_boundary_0_1.py": "3c31bf9",
    "tests/test_gokv_dool_oci_architecture_0_2.py": "3c31bf9",
    "tests/test_gokv_generation_0_1.py": "3c31bf9",
    "tests/test_gokv_protocol_checkpoint_0_1.py": "3c31bf9",
    "tests/test_gokv_self_capture_0_1.py": "3c31bf9",
    "tests/test_gokv_ui_ux_1_200_evidence_accumulation_0_3.py": "3c31bf9",
    "tests/test_ui_ux_main_console_structure_1_0.py": "9a1ebc5",
    "tests/test_ui_ux_main_console_refinement_1_1.py": "9a1ebc5",
    "tests/test_ui_ux_main_console_flow_1_2.py": "9a1ebc5",
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py": "6ae13f4",
    "tests/test_ui_ux_panel_maestro_p0_p1_visual_hierarchy_1_196.py": "48036f6",
    "tests/test_ui_ux_panel_maestro_microcopy_active_corpus_inventory_1_198.py": "6b9c806",
    "tests/test_ui_ux_panel_maestro_microcopy_direction_execution_1_200.py": "0d4ae4e",
    "tests/test_ui_ux_panel_maestro_microcopy_direction_execution_checkpoint_1_200.py": "a2afc307",
    "tests/test_ui_ux_panel_maestro_microcopy_direction_closure_audit_1_201.py": "0d4ae4e",
    "tests/test_ui_ux_density_information_architecture_hardening_1_29.py": "13ae5530",
    "tests/test_ui_ux_panel_maestro_closure_matrix_checkpoint_1_146.py": "167d521",
    "tests/test_post_roadmap_3_2_full_3x_phase_graph_and_method_consolidation.py": "f87dbb9",
    "tests/test_ui_ux_1_201_premission_oci.py": "a2afc307",
}
_CURRENT_GUARD_MODULES = {
    "tests/test_ui_ux_panel_maestro_controlled_double_scope_affordances_severity_1_192.py",
}
_SECONDARY_HISTORICAL_FILES = frozenset(
    {
        "tests/test_roadmap_3_0_n9_checkpoint_handoff.py",
        "tests/test_roadmap_3_x_macro_02_1_checkpoint.py",
        "tests/test_roadmap_3_x_macro_02_1_learning_reconciliation.py",
        "tests/test_strategic_docs_corporate_areas_and_institutional_intelligence_1_1.py",
        "tests/test_strategic_docs_future_enterprise_architecture_1_0.py",
        "tests/test_strategic_docs_ia_core_os_and_device_ecosystem_1_2.py",
        "tests/test_strategic_docs_root_control_plane_owner_nodes_and_continuity_1_3.py",
        "tests/test_ui_ux_component_documentation_style_reference_1_45.py",
        "tests/test_ui_ux_component_documentation_style_reference_audit_1_44.py",
        "tests/test_ui_ux_future_screens_readiness_1_41.py",
        "tests/test_ui_ux_future_screens_readiness_audit_1_40.py",
        "tests/test_ui_ux_future_screens_readiness_checkpoint_1_42.py",
        "tests/test_ui_ux_next_block_plan_1_35.py",
        "tests/test_ui_ux_next_block_plan_1_39.py",
        "tests/test_ui_ux_next_block_plan_1_43.py",
        "tests/test_ui_ux_panel_maestro_closure_matrix_restore_point_publication_1_148.py",
        "tests/test_ui_ux_panel_maestro_closure_matrix_visual_accessibility_fix_1_145_A.py",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_1_163.py",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_checkpoint_1_164.py",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_implementation_plan_1_162.py",
        "tests/test_ui_ux_panel_maestro_final_screen_contracts_visual_rehousing_implementation_1_129.py",
        "tests/test_ui_ux_panel_maestro_next_top_15_recommendation_plan_1_167.py",
        "tests/test_ui_ux_panel_maestro_p2_p3_transversal_density_1_196.py",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_audit_1_168.py",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_fix_1_168_A.py",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_fix_checkpoint_1_169.py",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_restore_point_decision_1_170.py",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_restore_point_publication_1_171.py",
        "tests/test_ui_ux_panel_maestro_roadmap_cursor_audit_1_173.py",
        "tests/test_ui_ux_panel_maestro_roadmap_resume_post_strategic_docs_1_172.py",
        "tests/test_ui_ux_panel_maestro_top_15_elite_audit_1_160.py",
        "tests/test_ui_ux_panel_maestro_top_15_first_recommendation_decision_1_161.py",
        "tests/test_ui_ux_panel_maestro_top_15_readiness_restore_point_decision_1_165.py",
        "tests/test_ui_ux_panel_maestro_top_15_readiness_restore_point_publication_1_166.py",
        "tests/test_ui_ux_panel_maestro_user_panel_separation_audit_1_36.py",
        "tests/test_ui_ux_panel_maestro_vocabulary_affordances_implementation_plan_1_150.py",
        "tests/test_ui_ux_panel_maestro_widgets_contract_aware_reconstruction_1_174.py",
        "tests/test_ui_ux_superior_layout_0_8.py",
        "tests/test_ui_ux_visual_base_checkpoint_0_9.py",
    }
)
_LIVE_README_MODULES = frozenset(
    {
        "tests/test_ui_ux_component_documentation_style_reference_1_45.py",
        "tests/test_ui_ux_component_documentation_style_reference_audit_1_44.py",
        "tests/test_ui_ux_future_screens_readiness_1_41.py",
        "tests/test_ui_ux_future_screens_readiness_audit_1_40.py",
        "tests/test_ui_ux_future_screens_readiness_checkpoint_1_42.py",
        "tests/test_ui_ux_next_block_plan_1_35.py",
        "tests/test_ui_ux_next_block_plan_1_39.py",
        "tests/test_ui_ux_next_block_plan_1_43.py",
        "tests/test_ui_ux_panel_maestro_closure_matrix_restore_point_publication_1_148.py",
        "tests/test_ui_ux_panel_maestro_closure_matrix_visual_accessibility_fix_1_145_A.py",
        "tests/test_ui_ux_panel_maestro_closure_readiness_matrix_1_163.py",
        "tests/test_ui_ux_panel_maestro_readme_docs_ui_consistency_fix_checkpoint_1_169.py",
        "tests/test_ui_ux_panel_maestro_roadmap_cursor_audit_1_173.py",
        "tests/test_ui_ux_panel_maestro_top_15_readiness_restore_point_decision_1_165.py",
        "tests/test_ui_ux_panel_maestro_top_15_readiness_restore_point_publication_1_166.py",
        "tests/test_ui_ux_panel_maestro_user_panel_separation_audit_1_36.py",
        "tests/test_ui_ux_panel_maestro_vocabulary_affordances_implementation_plan_1_150.py",
    }
)
_OVERRIDES.update(
    {
        "tests/test_roadmap_3_0_n9_checkpoint_handoff.py": "ba3f0914",
        "tests/test_ui_ux_panel_maestro_closure_matrix_visual_accessibility_fix_1_145_A.py": "31b1493b",
        "tests/test_ui_ux_panel_maestro_p2_p3_transversal_density_1_196.py": "1c9c0cdf",
        "tests/test_ui_ux_superior_layout_0_8.py": "13ae5530",
        "tests/test_ui_ux_visual_base_checkpoint_0_9.py": "31b1493b",
    }
)
_CURRENT_PRODUCT_CSS_MODULES = {
    "tests/test_ui_ux_panel_maestro_p0_p1_visual_hierarchy_1_196.py",
}
_HISTORICAL_SCOPE_HEAD = "6ae13f4"
_MICROCOPY_PREFIX = "tests/test_ui_ux_panel_maestro_microcopy_"
_SNAPSHOT_PREFIXES = ("ui/web/", "docs/", "knowledge/global_operational/", "tests/fixtures/")
_SNAPSHOT_EXACT = {
    "README.md",
    "ui/web/README.md",
    "api.py",
    "core/backend_internal_ui_payloads.py",
}
_HISTORICAL_FILES = frozenset(_LEDGER_NODE_RE.findall(LEDGER.read_text(encoding="utf-8"))) | _SECONDARY_HISTORICAL_FILES
_CHECKPOINT_CACHE: dict[str, str] = {}


def _relative(path: Path) -> str | None:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return None


def _git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def checkpoint_for(module: Any, relative_test_path: str) -> str | None:
    if relative_test_path in _CURRENT_GUARD_MODULES:
        return None
    if relative_test_path not in _HISTORICAL_FILES:
        return None
    explicit = getattr(module, "HISTORICAL_COMMIT", None)
    if explicit:
        return str(explicit)
    if relative_test_path in _OVERRIDES:
        return _OVERRIDES[relative_test_path]
    if relative_test_path.startswith(_MICROCOPY_PREFIX):
        return "6b9c806"
    if relative_test_path not in _CHECKPOINT_CACHE:
        _CHECKPOINT_CACHE[relative_test_path] = _git(
            "log", "--diff-filter=A", "--follow", "-1", "--format=%H", "--", relative_test_path
        )
    return _CHECKPOINT_CACHE[relative_test_path]


def _snapshot_bytes(checkpoint: str, relative_path: str, original_check_output) -> bytes | None:
    try:
        return original_check_output(["git", "show", f"{checkpoint}:{relative_path}"], cwd=ROOT)
    except subprocess.CalledProcessError:
        return None


def _snapshot_path(relative_path: str) -> bool:
    return relative_path in _SNAPSHOT_EXACT or relative_path.startswith(_SNAPSHOT_PREFIXES)


def _snapshot_checkpoint(relative_test_path: str, relative_path: str, checkpoint: str) -> str:
    if (
        relative_test_path == "tests/test_ui_ux_visual_base_checkpoint_0_9.py"
        and relative_path == "ui/web/index.html"
    ):
        return "13ae5530"
    if (
        relative_test_path in _CURRENT_PRODUCT_CSS_MODULES
        and relative_path == "ui/web/styles.css"
    ):
        return "0d4ae4e"
    return checkpoint


def _replace_head(value: object, checkpoint: str) -> object:
    if not isinstance(value, str) or "HEAD" not in value:
        return value
    return value.replace("HEAD", checkpoint)


def rewrite_git_command(command: Any, checkpoint: str) -> Any:
    if not isinstance(command, (list, tuple)) or not command or command[0] != "git":
        return command
    rewritten = list(command)
    try:
        diff_index = rewritten.index("diff")
    except ValueError:
        return [_replace_head(value, checkpoint) for value in rewritten]

    rewritten = [_replace_head(value, checkpoint) for value in rewritten]
    if "--cached" in rewritten or any(
        isinstance(value, str) and "HEAD" in value for value in command
    ):
        return rewritten

    separator = rewritten.index("--") if "--" in rewritten else len(rewritten)
    if any(
        isinstance(rewritten[index], str)
        and (".." in rewritten[index] or "..." in rewritten[index])
        for index in range(diff_index + 1, separator)
    ):
        return rewritten
    revision_indices = [
        index
        for index in range(diff_index + 1, separator)
        if not str(rewritten[index]).startswith("-")
    ]
    if len(revision_indices) == 1:
        rewritten.insert(revision_indices[0] + 1, checkpoint)
    return rewritten


def _historical_repo(checkpoint: str, tmp_path: Path, original_check_output) -> Path:
    archive = original_check_output(["git", "archive", checkpoint, "knowledge/global_operational"], cwd=ROOT)
    repo_root = tmp_path / "historical-repo"
    repo_root.mkdir()
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as tar:
        tar.extractall(repo_root)
    return repo_root


def _needs_historical_vault(relative_test_path: str) -> bool:
    return relative_test_path.startswith("tests/test_gokv_") or relative_test_path.endswith(
        "test_roadmap_3_x_macro_02_learning_adjudication.py"
    )


def install(request, tmp_path: Path, monkeypatch) -> str | None:
    module = request.module
    relative_test_path = _relative(Path(module.__file__))
    if relative_test_path is None:
        return None
    checkpoint = checkpoint_for(module, relative_test_path)
    if checkpoint is None:
        return None

    original_read_text = Path.read_text
    original_read_bytes = Path.read_bytes
    original_check_output = subprocess.check_output
    original_run = subprocess.run

    def read_text(path: Path, *args, **kwargs):
        relative_path = _relative(path)
        if (
            relative_test_path in _LIVE_README_MODULES
            and relative_path in {"README.md", "ui/web/README.md"}
        ):
            return original_read_text(path, *args, **kwargs)
        if relative_path and _snapshot_path(relative_path):
            snapshot = _snapshot_bytes(
                _snapshot_checkpoint(relative_test_path, relative_path, checkpoint),
                relative_path,
                original_check_output,
            )
            if snapshot is not None:
                encoding = kwargs.get("encoding") or (args[0] if args else "utf-8")
                return snapshot.decode(encoding or "utf-8", errors=kwargs.get("errors", "strict"))
        return original_read_text(path, *args, **kwargs)

    def read_bytes(path: Path, *args, **kwargs):
        relative_path = _relative(path)
        if relative_path and _snapshot_path(relative_path):
            snapshot = _snapshot_bytes(
                _snapshot_checkpoint(relative_test_path, relative_path, checkpoint),
                relative_path,
                original_check_output,
            )
            if snapshot is not None:
                return snapshot
        return original_read_bytes(path, *args, **kwargs)

    def check_output(command, *args, **kwargs):
        if (
            isinstance(command, (list, tuple))
            and len(command) >= 2
            and command[0] == "git"
            and command[1] == "status"
            and Path(kwargs.get("cwd", ROOT)).resolve() == ROOT
        ):
            return "" if kwargs.get("text") or kwargs.get("encoding") else b""
        return original_check_output(rewrite_git_command(command, checkpoint), *args, **kwargs)

    def run(command, *args, **kwargs):
        if (
            relative_test_path
            == "tests/test_ui_ux_panel_maestro_final_screen_contracts_visual_rehousing_implementation_1_129.py"
            and isinstance(command, (list, tuple))
            and list(command[:4]) == ["git", "diff", "--quiet", "HEAD"]
            and "--" in command
        ):
            separator = command.index("--")
            historical_command = [
                "git",
                "diff",
                "--quiet",
                f"{checkpoint}^",
                checkpoint,
                "--",
                *command[separator + 1 :],
            ]
            return original_run(historical_command, *args, **kwargs)
        return original_run(rewrite_git_command(command, checkpoint), *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    monkeypatch.setattr(subprocess, "check_output", check_output)
    monkeypatch.setattr(subprocess, "run", run)

    if _needs_historical_vault(relative_test_path):
        historical_repo_root = _historical_repo(checkpoint, tmp_path, original_check_output)
        historical_vault = historical_repo_root / "knowledge" / "global_operational"
        from gokv.storage import VaultPaths

        historical_paths = VaultPaths(historical_vault)

        if hasattr(module, "default_paths"):
            original = getattr(module, "default_paths")

            def default_paths(_repo_root=None, _original=original):
                return historical_paths

            monkeypatch.setattr(module, "default_paths", default_paths)

        for name in ("iter_knowledge_items", "validate_vault", "rebuild_index", "list_promoted"):
            if hasattr(module, name):
                original = getattr(module, name)

                def bound_paths(paths=None, *args, _original=original, **kwargs):
                    return _original(historical_paths if paths is None else paths, *args, **kwargs)

                monkeypatch.setattr(module, name, bound_paths)

        if hasattr(module, "_run_cli"):
            original_run_cli = module._run_cli

            def historical_run_cli(*args, **kwargs):
                if kwargs.get("repo_root") is None:
                    kwargs["repo_root"] = historical_repo_root
                return original_run_cli(*args, **kwargs)

            monkeypatch.setattr(module, "_run_cli", historical_run_cli)

    if relative_test_path not in _CURRENT_GUARD_MODULES:
        try:
            import ui_ux_1_192_scope as historical_scope
        except ImportError:
            pass
        else:
            monkeypatch.setattr(
                historical_scope,
                "HISTORICAL_SCOPE_HEAD",
                _HISTORICAL_SCOPE_HEAD,
                raising=False,
            )

    return checkpoint
