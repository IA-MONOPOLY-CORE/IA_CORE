from __future__ import annotations

import ast
import builtins
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import scripts.closure_assurance_v2_2_4_a as successor
from scripts.closure_assurance_v2_2_4_a import (
    AuthorityEntry,
    AuthorityResolutionFailure,
    GovernedComponentResolver,
    ValidatedAuthoritySet,
    build_authoritative_resolver,
    canonical_bytes,
    derive_canonical_repository_root,
    sha256_bytes,
)
from scripts.run_mission_closure_v2_2_4_a import authorize_component
from scripts.closure_assurance_v2_2_3 import (
    ComponentEntry as HistoricalComponentEntry,
    GovernedComponentResolver as HistoricalResolver,
)


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_mission_closure_v2_2_4_a.py"
AUTHORITY = ROOT / successor.AUTHORITY_RELATIVE_PATH
BASELINE = "c920d3545c6862e4d6a4f8e88aed443ad6f8d071"
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


def run_runner(*args: str, cwd: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env is not None:
        merged.update(env)
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=cwd,
        env=merged,
        capture_output=True,
        text=True,
    )


def error_code(callable_object, *args, **kwargs) -> str:
    with pytest.raises(AuthorityResolutionFailure) as caught:
        callable_object(*args, **kwargs)
    return caught.value.code


def test_preflight_baseline_and_historical_bytes_are_preserved():
    assert subprocess.run(["git", "cat-file", "-e", f"{BASELINE}^{{commit}}"], cwd=ROOT, capture_output=True).returncode == 0
    for relative, expected in HISTORICAL_HASHES.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_historical_missing_authority_bypass_is_reproduced():
    raw = b"historical component bytes\n"
    resolver = HistoricalResolver([HistoricalComponentEntry("known", "implementation", raw, "implementation")])
    assert resolver.resolve("known", "implementation") == raw


def test_successor_real_entrypoint_authorizes_exact_bytes():
    result = run_runner("resolve", "successor-resolver", "implementation")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["result"] == "AUTHORIZED_BYTES_RELEASED"
    assert payload["released_sha256"] == hashlib.sha256((ROOT / successor.RESOLVER_RELATIVE_PATH).read_bytes()).hexdigest()
    assert payload["authorization_trace"]["authority_only"] is True
    event = payload["authorization_trace"]["events"][0]
    assert event["recomputed_component_sha256"] == payload["released_sha256"]
    assert event["authorized_entry_sha256"] == payload["released_sha256"]
    assert "execution_success" not in event
    assert "validation_success" not in event
    assert "component_pass" not in event


def test_r1_a_successor_missing_authority_rejects(monkeypatch):
    def missing(_root):
        raise AuthorityResolutionFailure("REJECTED_MISSING_AUTHORITY", "no binding exists")

    monkeypatch.setattr(successor, "_load_validated_authority_set", missing)
    assert error_code(successor.build_authoritative_resolver) == "REJECTED_MISSING_AUTHORITY"


def test_no_authority_or_empty_authority_cannot_construct():
    assert error_code(GovernedComponentResolver) == "REJECTED_MISSING_AUTHORITY_SET"
    empty = ValidatedAuthoritySet(ROOT, AUTHORITY, "a" * 64, (), successor._VALIDATION_TOKEN)
    assert error_code(GovernedComponentResolver, empty) == "REJECTED_EMPTY_AUTHORITY_SET"
    assert error_code(GovernedComponentResolver, {"known": b"substitute"}) == "REJECTED_INVALID_AUTHORITY_SET"


def test_r1_b_unknown_component_rejects_from_real_entrypoint():
    result = run_runner("resolve", "unknown-component", "implementation")
    assert result.returncode != 0
    assert json.loads(result.stderr)["result"] == "REJECTED_UNKNOWN_COMPONENT"


def test_r1_c_wrong_hash_rejects_and_does_not_release_bytes():
    authority = successor._load_validated_authority_set(ROOT)
    original = authority.entries[0]
    wrong = AuthorityEntry(original.logical_artifact_id, original.semantic_role, original.relative_path, original.byte_length, "0" * 64, original.content_role)
    forged = ValidatedAuthoritySet(ROOT, authority.manifest_path, authority.manifest_sha256, (wrong, *authority.entries[1:]), successor._VALIDATION_TOKEN)
    resolver = GovernedComponentResolver(forged)
    assert error_code(resolver.resolve, original.logical_artifact_id, original.semantic_role) == "REJECTED_COMPONENT_HASH_MISMATCH"
    assert resolver.authorization_trace()["events"] == []


def test_r1_d_wrong_role_rejects():
    resolver = build_authoritative_resolver()
    assert error_code(resolver.resolve, "successor-resolver", "entrypoint") == "REJECTED_SEMANTIC_ROLE_MISMATCH"
    assert resolver.authorization_trace()["events"] == []


def test_r1_e_caller_component_substitute_rejects():
    resolver = build_authoritative_resolver()
    assert error_code(resolver.resolve, "successor-resolver", "implementation", b"substitute") == "REJECTED_CALLER_COMPONENT_SUBSTITUTE"
    assert error_code(resolver.resolve, "successor-resolver", "implementation", raw_bytes=b"substitute") == "REJECTED_CALLER_COMPONENT_SUBSTITUTE"
    assert error_code(GovernedComponentResolver, ["caller entry"]) == "REJECTED_INVALID_AUTHORITY_SET"
    result = run_runner("resolve", "successor-resolver", "implementation", "--component-path", "C:\\temp")
    assert result.returncode != 0
    assert json.loads(result.stderr)["result"] == "REJECTED_CALLER_COMPONENT_SUBSTITUTE"


def test_r1_f_caller_selected_authority_set_rejects(monkeypatch):
    monkeypatch.setenv("IA_CORE_AUTHORITY_SET_PATH", str(ROOT / "docs" / "anything.json"))
    assert error_code(build_authoritative_resolver) == "REJECTED_CALLER_AUTHORITY_SET_SELECTION"
    result = run_runner("resolve", "successor-resolver", "implementation", env={"IA_CORE_AUTHORITY_MANIFEST": "C:\\temp\\authority.json"})
    assert result.returncode != 0
    assert json.loads(result.stderr)["result"] == "REJECTED_CALLER_AUTHORITY_SET_SELECTION"


def test_r1_g_caller_selected_repository_root_rejects(monkeypatch):
    monkeypatch.setenv("IA_CORE_REPOSITORY_ROOT", str(ROOT))
    assert error_code(derive_canonical_repository_root) == "REJECTED_CALLER_REPOSITORY_ROOT_SELECTION"
    result = run_runner("resolve", "successor-resolver", "implementation", "--repo-root", "C:\\temp")
    assert result.returncode != 0
    assert json.loads(result.stderr)["result"] == "REJECTED_CALLER_REPOSITORY_ROOT_SELECTION"
    result = run_runner("resolve", "successor-resolver", "implementation", env={"GIT_DIR": "C:\\temp\\.git"})
    assert result.returncode != 0
    assert json.loads(result.stderr)["result"] == "REJECTED_CALLER_REPOSITORY_ROOT_SELECTION"


def test_r1_h_current_working_directory_does_not_change_authority_location():
    first = run_runner("resolve", "successor-resolver", "implementation", cwd=ROOT)
    second = run_runner("resolve", "successor-resolver", "implementation", cwd=Path(r"C:\Windows"))
    assert first.returncode == second.returncode == 0
    first_payload = json.loads(first.stdout)
    second_payload = json.loads(second.stdout)
    first_event = first_payload["authorization_trace"]["events"][0]
    second_event = second_payload["authorization_trace"]["events"][0]
    assert first_event["authority_set_identity"] == second_event["authority_set_identity"]
    assert first_event["canonical_repository_root_identity"] == second_event["canonical_repository_root_identity"]
    assert first_payload["released_sha256"] == second_payload["released_sha256"]


def test_r1_i_exact_authorized_bytes_are_released_and_trace_is_resolver_owned():
    resolver = build_authoritative_resolver()
    raw = resolver.resolve("successor-entrypoint", "entrypoint")
    event = resolver.authorization_trace()["events"][0]
    assert sha256_bytes(raw) == event["recomputed_component_sha256"] == event["authorized_entry_sha256"]
    assert event["byte_length"] == len(raw)
    assert event["bytes_released"] is True
    assert event["authorization_result"] == "AUTHORIZED_BYTES_RELEASED"
    assert event["semantic_role"] == "entrypoint"
    assert event["logical_artifact_id"] == "successor-entrypoint"


def test_same_byte_single_read_is_proven(monkeypatch):
    resolver = build_authoritative_resolver()
    entry = resolver._by_id["successor-resolver"]
    target = (ROOT / entry.relative_path).resolve()
    real_open = builtins.open
    reads = []

    def counted_open(file, mode="r", *args, **kwargs):
        if Path(file).resolve() == target and "rb" in mode:
            reads.append(file)
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", counted_open)
    raw = resolver.resolve("successor-resolver", "implementation")
    assert len(reads) == 1
    event = resolver.authorization_trace()["events"][0]
    assert raw is not None
    assert sha256_bytes(raw) == event["recomputed_component_sha256"] == event["authorized_entry_sha256"]


def test_no_component_bytes_reach_loader_before_authorization(monkeypatch):
    calls = []
    original = successor._read_exact_authorized_component

    def observed(*args, **kwargs):
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(successor, "_read_exact_authorized_component", observed)
    resolver = build_authoritative_resolver()
    assert error_code(resolver.resolve, "unknown-component", "implementation") == "REJECTED_UNKNOWN_COMPONENT"
    assert error_code(resolver.resolve, "successor-resolver", "entrypoint") == "REJECTED_SEMANTIC_ROLE_MISMATCH"
    assert calls == []
    resolver.resolve("successor-resolver", "implementation")
    assert calls == [True]


def test_fake_trace_cannot_create_authority():
    fake_trace = {"authorization_result": "AUTHORIZED_BYTES_RELEASED", "bytes_released": True}
    assert "authority_set_identity" not in fake_trace
    resolver = build_authoritative_resolver()
    assert resolver.authorization_trace()["events"] == []
    assert error_code(resolver.resolve, "unknown-component", "implementation") == "REJECTED_UNKNOWN_COMPONENT"
    assert resolver.authorization_trace()["events"] == []


def test_fixed_authority_location_and_root_are_internal():
    assert successor.AUTHORITY_RELATIVE_PATH == "docs/ROADMAP_4X_MACRO_06_2_4_A_AUTHORIZED_VALIDATION_INPUT_SET.json"
    assert derive_canonical_repository_root() == ROOT.resolve()
    signature = inspect.signature(authorize_component)
    assert list(signature.parameters) == ["logical_artifact_id", "semantic_role"]
    assert Path(__file__).resolve().parents[1] == ROOT.resolve()


def test_authority_set_is_strict_and_exact():
    manifest = json.loads(AUTHORITY.read_bytes())
    assert set(manifest) == {"authority_relative_path", "entries", "manifest_sha256", "mission_id", "set_version"}
    assert len(manifest["entries"]) == 3
    assert {entry["logical_artifact_id"] for entry in manifest["entries"]} == set(successor.EXPECTED_COMPONENTS)
    assert successor._load_validated_authority_set(ROOT).manifest_sha256 == manifest["manifest_sha256"]
    duplicate = b'{"entries":[],"entries":[]}'
    assert error_code(successor._strict_json, duplicate, "duplicate") == "REJECTED_INVALID_AUTHORITY_SET"


def test_successor_loader_bypass_guard_is_executable_ast_check():
    source = (ROOT / successor.RESOLVER_RELATIVE_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    direct_file_reads: list[tuple[str, int]] = []

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.function = "<module>"

        def visit_FunctionDef(self, node):
            previous = self.function
            self.function = node.name
            self.generic_visit(node)
            self.function = previous

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id == "open" and self.function != "_read_exact_authorized_component":
                direct_file_reads.append((self.function, node.lineno))
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"read_bytes", "read_text"} and self.function not in {"_load_validated_authority_set"}:
                direct_file_reads.append((self.function, node.lineno))
            self.generic_visit(node)

    Visitor().visit(tree)
    assert direct_file_reads == []


def test_historical_impact_and_product_boundaries_are_clean():
    for relative, expected in HISTORICAL_HASHES.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    changed = set(subprocess.check_output(["git", "diff", "--name-only", BASELINE], cwd=ROOT, text=True).splitlines())
    forbidden = {path for path in changed if "v2_2_3" in path or path.startswith(("backend/", "frontend/", "src/"))}
    assert forbidden == set()


def test_py_compile_and_new_json_are_valid():
    completed = subprocess.run([sys.executable, "-m", "py_compile", str(ROOT / "scripts" / "closure_assurance_v2_2_4_a.py"), str(RUNNER)], cwd=ROOT, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    manifest = json.loads(AUTHORITY.read_bytes())
    assert manifest["manifest_sha256"] == sha256_bytes(canonical_bytes(manifest, exclude={"manifest_sha256"}))
