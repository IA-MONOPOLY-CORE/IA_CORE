from __future__ import annotations

import ast
import hashlib
import inspect
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

import pytest

import scripts.closure_assurance_v2_2_4_a as assurance
from scripts.run_mission_closure_v2_2_4_a import authorize_component
from scripts.closure_assurance_v2_2_3 import (
    ComponentEntry as HistoricalComponentEntry,
    GovernedComponentResolver as HistoricalResolver,
)


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_mission_closure_v2_2_4_a.py"
AUTHORITY = ROOT / assurance.AUTHORITY_RELATIVE_PATH
BASELINE = "41636ecd3d2806b8699a3c656afa8f947992125e"
HISTORICAL_HASHES = {
    "scripts/closure_assurance_v2_2_3.py": "eabd1a6327d51b8032b56c57c6181bbcc62e68e6de61b0637460bd5fedbef1b6",
    "scripts/run_mission_closure_v2_2_3.py": "84075336ba472884116fe3f83fb3a6347c6171e586fe3f17910091b4988a2498",
    "scripts/render_canonical_report_v2_2_3.py": "1fe77b3718ca3c1ab8b1ef194e3b74d5691b5c1dadbfd3e634c3b3ceca58e4e6",
    "scripts/validate_mission_closure_v2_2_3.py": "33f329217d5861574e5708375aae287f2f0b557fbc979c115ab71dcce44563e7",
    "scripts/run_mission_closure_v2_2_3_red_reproduction.py": "e85f01e0b69234f6be71c5411c2b53ec714d8731f671d902f40cdac23e200780",
    "tests/test_mission_closure_gate_v2_2_3.py": "796fae9618708daede2484c539a25419118ffbcc3cdb7e0e693dce53a8e7b09c",
    "tests/test_mission_closure_gate_v2_2_3_ci_contract.py": "eb245f86c9547d2ed8419f6c924f65149ed7a037dc70d36651caa03b51c74141",
    "docs/MISSION_CLOSURE_GATE_V2_2_3_CONTRACT.md": "57e348d3e0216250d4a57c0d08f158c8e37359c1c95c54ab231f7a4528cef289",
    "docs/MISSION_CLOSURE_POLICY_V2_2_3.json": "1c24f8aba68482325d5293a8e720f79240ba1ac73597e8a02a3bb113e7246090",
}


def _run(path: Path, *args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run([sys.executable, str(path), *args], cwd=cwd or path.parent.parent, env=merged, capture_output=True, text=True)


def _json_stderr(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stderr)


def _cleanup_readonly(function, path, _exc):
    os.chmod(path, stat.S_IWRITE)
    function(path)


def _commit(repo: Path, message: str) -> None:
    subprocess.run(["git", "-C", str(repo), "add", "--all"], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=Micro A Test", "-c", "user.email=micro-a-test@example.invalid", "commit", "-m", message], check=True, capture_output=True, text=True)


def _copy_candidate_surfaces(repo: Path) -> None:
    for relative in (
        assurance.RESOLVER_RELATIVE_PATH,
        assurance.ENTRYPOINT_RELATIVE_PATH,
        assurance.CONTRACT_RELATIVE_PATH,
        assurance.AUTHORITY_RELATIVE_PATH,
    ):
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def _candidate_clone(tmp_path: Path) -> Path:
    repo = tmp_path / "candidate"
    subprocess.run(["git", "clone", "--no-local", "--branch", "main", str(ROOT), str(repo)], check=True, capture_output=True, text=True)
    _copy_candidate_surfaces(repo)
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "add",
            assurance.RESOLVER_RELATIVE_PATH,
            assurance.ENTRYPOINT_RELATIVE_PATH,
            assurance.CONTRACT_RELATIVE_PATH,
            assurance.AUTHORITY_RELATIVE_PATH,
        ],
        check=True,
    )
    staged_diff = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--quiet"],
        capture_output=True,
    )
    if staged_diff.returncode != 0:
        _commit(repo, "test: create isolated Micro A candidate")
    return repo


def _remove_candidate(repo: Path) -> None:
    if repo.exists():
        shutil.rmtree(repo, onerror=_cleanup_readonly)


@pytest.fixture
def candidate_clone(tmp_path: Path):
    repo = _candidate_clone(tmp_path)
    try:
        yield repo
    finally:
        _remove_candidate(repo)


def _update_manifest_to_worktree(repo: Path) -> None:
    manifest_path = repo / assurance.AUTHORITY_RELATIVE_PATH
    manifest = json.loads(manifest_path.read_bytes())
    for entry in manifest["entries"]:
        raw = (repo / entry["repository_relative_path"]).read_bytes()
        entry["byte_length"] = len(raw)
        entry["sha256"] = hashlib.sha256(raw).hexdigest()
    payload = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    manifest["manifest_sha256"] = hashlib.sha256((json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    manifest_path.write_bytes((json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())


def test_baseline_exists_and_v2_2_3_is_byte_identical():
    assert subprocess.run(["git", "cat-file", "-e", f"{BASELINE}^{{commit}}"], cwd=ROOT, capture_output=True).returncode == 0
    for relative, expected in HISTORICAL_HASHES.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_r1_j_historical_externally_constructed_state_is_reproduced():
    raw = (ROOT / "README.md").read_bytes()
    entry = HistoricalComponentEntry("caller-readme", "implementation", raw, "implementation")
    resolver = HistoricalResolver([entry])
    released = resolver.resolve("caller-readme", "implementation")
    assert released == raw
    assert resolver.trace_document({"caller-readme"})["result"] == "PASS"


def test_r1_j_repaired_successor_has_no_externally_constructible_authority_surface(candidate_clone):
    assert not hasattr(assurance, "GovernedComponentResolver")
    assert not hasattr(assurance, "ValidatedAuthoritySet")
    assert not hasattr(assurance, "AuthorityEntry")
    assert not hasattr(assurance, "_VALIDATION_TOKEN")
    assert list(inspect.signature(authorize_component).parameters) == ["logical_artifact_id", "semantic_role"]
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "caller-readme", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_UNKNOWN_COMPONENT"


def test_r1_k_historical_self_consistent_local_state_was_reproduced_and_is_now_rejected(candidate_clone):
    resolver_path = candidate_clone / assurance.RESOLVER_RELATIVE_PATH
    resolver_path.write_bytes(resolver_path.read_bytes() + b"\n# uncommitted local mutation\n")
    _update_manifest_to_worktree(candidate_clone)
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT"


def test_positive_real_entrypoint_is_commit_bound(candidate_clone):
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    commit = subprocess.check_output(["git", "-C", str(candidate_clone), "rev-parse", "HEAD"], text=True).strip()
    expected = hashlib.sha256((candidate_clone / assurance.RESOLVER_RELATIVE_PATH).read_bytes()).hexdigest()
    event = payload["authorization_trace"]["events"][0]
    assert payload["result"] == "AUTHORIZED_BYTES_RELEASED"
    assert event["derived_commit_sha"] == commit
    assert payload["released_sha256"] == expected
    assert event["recomputed_component_sha256"] == event["authorized_entry_sha256"] == expected
    assert "execution_success" not in event
    assert "validation_success" not in event
    assert "component_pass" not in event


def test_r1_a_missing_governed_input_fails_closed(candidate_clone):
    manifest_path = candidate_clone / assurance.AUTHORITY_RELATIVE_PATH
    manifest = json.loads(manifest_path.read_bytes())
    manifest["entries"] = []
    payload = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    manifest["manifest_sha256"] = hashlib.sha256((json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    manifest_path.write_bytes((json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())
    _commit(candidate_clone, "test: commit empty authority fixture")
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_EMPTY_AUTHORITY_SET"


def test_r1_b_unknown_component(candidate_clone):
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "unknown-component", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_UNKNOWN_COMPONENT"


def test_r1_c_wrong_component_hash_is_rejected_from_same_commit(candidate_clone):
    manifest_path = candidate_clone / assurance.AUTHORITY_RELATIVE_PATH
    manifest = json.loads(manifest_path.read_bytes())
    for entry in manifest["entries"]:
        if entry["logical_artifact_id"] == "successor-resolver":
            entry["sha256"] = "0" * 64
    payload = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    manifest["manifest_sha256"] = hashlib.sha256((json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    manifest_path.write_bytes((json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())
    _commit(candidate_clone, "test: commit wrong component hash fixture")
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_COMPONENT_HASH_MISMATCH"


def test_r1_d_wrong_role(candidate_clone):
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "entrypoint")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_SEMANTIC_ROLE_MISMATCH"


def test_r1_e_caller_component_substitute(candidate_clone):
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", "--loader", "caller")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_CALLER_COMPONENT_SUBSTITUTE"


def test_r1_f_caller_authority_set(candidate_clone):
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", "--manifest", "README.md")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_CALLER_AUTHORITY_SET_SELECTION"
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", env={"IA_CORE_AUTHORITY_SET_PATH": "README.md"})
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_CALLER_AUTHORITY_SET_SELECTION"


def test_r1_g_caller_root_commit_and_branch(candidate_clone):
    for flag, expected in (("--repository-root", "REJECTED_CALLER_REPOSITORY_ROOT_SELECTION"), ("--commit", "REJECTED_CALLER_REPOSITORY_ROOT_SELECTION"), ("--branch", "REJECTED_CALLER_REPOSITORY_ROOT_SELECTION")):
        result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", flag, "other")
        assert result.returncode != 0
        assert _json_stderr(result)["result"] == expected
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", env={"IA_CORE_COMMIT": "0" * 40})
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_CALLER_COMMIT_SELECTION"


def test_r1_h_cwd_independence(candidate_clone):
    first = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", cwd=candidate_clone)
    second = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation", cwd=Path(r"C:\Windows"))
    assert first.returncode == second.returncode == 0
    first_payload = json.loads(first.stdout)
    second_payload = json.loads(second.stdout)
    assert first_payload["released_sha256"] == second_payload["released_sha256"]
    assert first_payload["authorization_trace"]["events"][0]["authority_set_identity"] == second_payload["authorization_trace"]["events"][0]["authority_set_identity"]


def test_r1_i_exact_authorized_bytes_and_trace_ceiling(candidate_clone):
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-entrypoint", "entrypoint")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    event = payload["authorization_trace"]["events"][0]
    assert event["resolution_state"] == "COMMIT_BOUND_AUTHORIZED"
    assert event["bytes_released"] is True
    assert event["recomputed_component_sha256"] == event["authorized_entry_sha256"] == payload["released_sha256"]
    assert event["derived_commit_sha"] == subprocess.check_output(["git", "-C", str(candidate_clone), "rev-parse", "HEAD"], text=True).strip()


def test_detached_head_rejected(candidate_clone):
    subprocess.run(["git", "-C", str(candidate_clone), "checkout", "--detach", "HEAD"], check=True, capture_output=True)
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_DETACHED_HEAD"


def test_wrong_branch_rejected(candidate_clone):
    subprocess.run(["git", "-C", str(candidate_clone), "checkout", "-b", "not-main"], check=True, capture_output=True)
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_BRANCH_NOT_MAIN"


def test_staged_relevant_change_rejected(candidate_clone):
    runner = candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH
    runner.write_bytes(runner.read_bytes() + b"\n# staged mutation\n")
    subprocess.run(["git", "-C", str(candidate_clone), "add", assurance.ENTRYPOINT_RELATIVE_PATH], check=True)
    result = _run(candidate_clone / assurance.ENTRYPOINT_RELATIVE_PATH, "resolve", "successor-resolver", "implementation")
    assert result.returncode != 0
    assert _json_stderr(result)["result"] == "REJECTED_RELEVANT_LOCAL_STATE_DIFFERS_FROM_COMMIT"


def test_public_api_has_one_supported_authority_surface(candidate_clone):
    assert assurance.__all__ == ()
    import scripts.run_mission_closure_v2_2_4_a as entrypoint

    assert entrypoint.__all__ == ("authorize_component",)
    assert list(inspect.signature(entrypoint.authorize_component).parameters) == ["logical_artifact_id", "semantic_role"]
    assert "**kwargs" not in str(inspect.signature(entrypoint.authorize_component))


def test_git_object_reads_are_binary_shell_false_and_path_is_fixed():
    source = (ROOT / assurance.RESOLVER_RELATIVE_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "cat-file" in source
    assert "ls-tree" in source
    run_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "run"]
    assert run_calls
    assert any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is False for call in run_calls for keyword in call.keywords)
    assert any(keyword.arg == "text" and isinstance(keyword.value, ast.Constant) and keyword.value.value is False for call in run_calls for keyword in call.keywords)
    assert assurance.AUTHORITY_RELATIVE_PATH == "docs/ROADMAP_4X_MACRO_06_2_4_A_AUTHORIZED_VALIDATION_INPUT_SET.json"


def test_relevant_paths_are_exactly_equal_to_head_on_candidate(candidate_clone):
    assert Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=candidate_clone, text=True).strip()).resolve() == candidate_clone.resolve()
    assert subprocess.check_output(["git", "branch", "--show-current"], cwd=candidate_clone, text=True).strip() == "main"
    assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", assurance.RESOLVER_RELATIVE_PATH, assurance.ENTRYPOINT_RELATIVE_PATH, assurance.AUTHORITY_RELATIVE_PATH, assurance.CONTRACT_RELATIVE_PATH], cwd=candidate_clone).returncode == 0


def test_historical_impact_and_product_boundaries_are_clean():
    for relative, expected in HISTORICAL_HASHES.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    changed = set(subprocess.check_output(["git", "diff", "--name-only", BASELINE], cwd=ROOT, text=True).splitlines())
    forbidden = {path for path in changed if "v2_2_3" in path or path.startswith(("backend/", "frontend/", "src/"))}
    assert forbidden == set()


def test_py_compile_and_authority_json():
    result = subprocess.run([sys.executable, "-m", "py_compile", str(ROOT / assurance.RESOLVER_RELATIVE_PATH), str(RUNNER)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    manifest = json.loads(AUTHORITY.read_bytes())
    canonical = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    assert manifest["manifest_sha256"] == hashlib.sha256((json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
