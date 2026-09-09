"""Static and isolated guards for Roadmap 3.x Macro-Mission 01."""

from __future__ import annotations

import ast
import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_PATH = ROOT / "api.py"


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
