"""Static and isolated guards for Roadmap 3.x Macro-Mission 01."""

from __future__ import annotations

import ast
import json
import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_PATH = ROOT / "api.py"
EVIDENCE_PATH = ROOT / "docs" / "ROADMAP_3_X_MACRO_01_EVIDENCE.json"
DISPOSITION_PATH = ROOT / "docs" / "ROADMAP_3_X_LEGACY_ROUTE_DISPOSITION.md"
CHECKPOINT_PATH = ROOT / "docs" / "ROADMAP_3_X_MACRO_01_CHECKPOINT.md"
RECONNAISSANCE_PATH = ROOT / "docs" / "ROADMAP_3_X_MACRO_01_ROUTE_RECONNAISSANCE.md"
B3_PATH = ROOT / "docs" / "ROADMAP_3_X_MACRO_01_B3_COVERAGE.md"


def _api_tree() -> ast.Module:
    return ast.parse(API_PATH.read_text(encoding="utf-8"), filename=str(API_PATH))


def _route_nodes() -> list[tuple[str, str, ast.AST]]:
    routes: list[tuple[str, str, ast.AST]] = []
    for node in ast.walk(_api_tree()):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and isinstance(decorator.func.value, ast.Name)
                and decorator.func.value.id == "app"
                and decorator.func.attr in {"get", "post", "put", "delete", "patch"}
                and decorator.args
                and isinstance(decorator.args[0], ast.Constant)
                and isinstance(decorator.args[0].value, str)
            ):
                continue
            routes.append((decorator.func.attr.upper(), decorator.args[0].value, node))
    return routes


def _function_source(name: str) -> str:
    node = next(node for node in _api_tree().body if getattr(node, "name", "") == name)
    return ast.get_source_segment(API_PATH.read_text(encoding="utf-8"), node) or ""


def test_current_api_route_census_remains_36_and_14_mutative():
    routes = _route_nodes()
    assert len(routes) == 36
    assert Counter(method for method, _path, _node in routes) == {
        "GET": 22,
        "POST": 12,
        "PUT": 1,
        "DELETE": 1,
    }
    assert sum(method != "GET" for method, _path, _node in routes) == 14


def test_cors_policy_is_explicit_allowlist_and_rejects_untrusted_configuration(monkeypatch):
    tree = _api_tree()
    function = next(node for node in tree.body if getattr(node, "name", "") == "_cors_allow_origins")
    namespace = {"os": os, "re": re}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(API_PATH), "exec"), namespace)
    resolve_origins = namespace["_cors_allow_origins"]

    monkeypatch.delenv("IA_CORE_CORS_ALLOW_ORIGINS", raising=False)
    assert resolve_origins() == ["http://localhost:8000"]

    monkeypatch.setenv("IA_CORE_CORS_ALLOW_ORIGINS", "https://trusted.example")
    assert resolve_origins() == ["https://trusted.example"]

    monkeypatch.setenv("IA_CORE_CORS_ALLOW_ORIGINS", "*")
    assert resolve_origins() == []

    monkeypatch.setenv("IA_CORE_CORS_ALLOW_ORIGINS", "javascript:bad")
    assert resolve_origins() == []


def test_cors_middleware_does_not_use_wildcards_or_enable_credentials():
    source = API_PATH.read_text(encoding="utf-8")
    assert "allow_origins=_cors_allow_origins()" in source
    assert 'allow_methods=["GET", "POST", "PUT", "DELETE"]' in source
    assert 'allow_headers=["Accept", "Content-Type"]' in source
    assert "allow_credentials=False" in source
    assert 'allow_origins=["*"]' not in source
    assert 'allow_methods=["*"]' not in source
    assert 'allow_headers=["*"]' not in source


def test_settings_secret_boundary_blocks_persistence_and_response_exposure():
    save_source = _function_source("save_settings")
    get_source = _function_source("get_settings")

    assert "if api_key:" in save_source
    assert "status_code=403" in save_source
    assert "api_key persistence is blocked" in save_source
    assert '"api_key": api_key' not in save_source
    assert "config_path" not in save_source
    assert 'settings.pop("api_key", None)' in get_source
    assert "api_key_configured" in get_source


def test_evidence_manifest_contains_complete_b2_disposition_and_hard_stop():
    manifest = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    routes = manifest["routes"]
    assert manifest["mission_id"] == "roadmap_3x_macro_01_security_legacy_canonical_alignment"
    assert len(routes) == 36
    assert len({route["route_id"] for route in routes}) == 36
    assert Counter(route["method"] for route in routes) == {
        "GET": 22,
        "POST": 12,
        "PUT": 1,
        "DELETE": 1,
    }
    assert {route["destination"] for route in routes} == {"UNKNOWN"}
    assert manifest["route_census"]["disposition_counts"]["UNKNOWN"] == 36
    assert manifest["coverage_before"] == manifest["coverage_after"]
    assert manifest["blocks"]["B-1"] == "PASS"
    assert manifest["blocks"]["B-2"] == "PASS_UNKNOWN_QUALITY_GATE"
    assert manifest["blocks"]["B-3"] == "PASS_EXPLICIT_CONTRACT_ONLY_UNALIGNED_LEGACY_SURFACE"
    assert manifest["route_recalculation"]["new_classification"] == "RECONNAISSANCE_REQUIRED_CONDITIONAL_FRONTIER"
    assert manifest["route_reconnaissance"]["routes_with_unknown_quality_records"] == 36
    assert manifest["b3_coverage"]["canonical_contracts_are_route_authority"] is False
    assert manifest["b3_coverage"]["coverage_changed"] is False


def test_route_reconnaissance_records_unknown_quality_gate_for_all_routes():
    reconnaissance = RECONNAISSANCE_PATH.read_text(encoding="utf-8")
    assert "B-2 result | `PASS_UNKNOWN_QUALITY_GATE`" in reconnaissance
    assert "UNKNOWN != NOT_INVESTIGATED" in reconnaissance
    assert reconnaissance.count("| `") >= 36
    for marker in (
        "Unknown reason",
        "Search surfaces checked",
        "Caller evidence checked",
        "Contract evidence checked",
        "Canonical owner checked",
        "Successor checked",
        "External consumer risk",
        "Evidence that would resolve it",
    ):
        assert marker in reconnaissance
    assert "POST /api/chat" in reconnaissance
    assert "GET /api/settings" in reconnaissance
    assert "POST /api/settings" in reconnaissance
    assert "CONTRACT_EXISTS_IS_NOT_ROUTE_ADAPTER" in reconnaissance


def test_b3_coverage_contract_keeps_canonical_contracts_distinct_from_routes():
    b3 = B3_PATH.read_text(encoding="utf-8")
    api_source = API_PATH.read_text(encoding="utf-8")
    assert "CONTROL_PLANE_COVERAGE_CONTRACT = PASS_EXPLICIT_CONTRACT_ONLY_UNALIGNED_LEGACY_SURFACE" in b3
    assert "Canonical internal modules contain no FastAPI route registration." in b3
    assert "NO_SAFE_ALIGNMENT; coverage remains unchanged" in b3
    assert "B-4, B-5, B-6 or B-7" in b3
    for forbidden_import in (
        "backend_internal_request_envelope",
        "backend_internal_dispatcher",
        "backend_internal_confirmation_gate",
        "backend_internal_response_adapter",
        "agent_permission_contract",
        "runtime_activation_gate",
    ):
        assert f"from core.{forbidden_import}" not in api_source
    assert "orchestrate_async" in _function_source("chat_endpoint")
    assert "dispatch_internal_request" not in _function_source("chat_endpoint")
    assert 'settings.pop("api_key", None)' in _function_source("get_settings")


def test_disposition_and_checkpoint_preserve_recalculated_frontier():
    disposition = DISPOSITION_PATH.read_text(encoding="utf-8")
    checkpoint = CHECKPOINT_PATH.read_text(encoding="utf-8")
    rows = re.findall(r"^\| `[^`]+` \| (GET|POST|PUT|DELETE) \|", disposition, re.MULTILINE)
    assert len(rows) == 36
    assert "F-004" in disposition
    assert "No route is marked `REMOVE`" in disposition
    assert "ROADMAP_3X_MACRO_01_SECURITY_LEGACY_CANONICAL_ALIGNMENT_PASSED" in checkpoint
    assert "B-3: PASS_EXPLICIT_CONTRACT_ONLY_UNALIGNED_LEGACY_SURFACE" in checkpoint
    assert "ROADMAP_3X_MACRO_01_SECURITY_LEGACY_CANONICAL_ALIGNMENT_PUBLISHED" not in checkpoint
