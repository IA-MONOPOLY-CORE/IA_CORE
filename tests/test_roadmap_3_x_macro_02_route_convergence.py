import ast
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api.py"
EVIDENCE = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_ROUTE_CONVERGENCE_EVIDENCE.json"
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_ROUTE_CONVERGENCE.md"


def _routes():
    tree = ast.parse(API.read_text(encoding="utf-8"), filename=str(API))
    found = []
    for node in ast.walk(tree):
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
            ):
                continue
            found.append((decorator.func.attr.upper(), decorator.args[0].value, node.name, node.lineno))
    return sorted(found, key=lambda value: (value[1], value[0]))


def test_route_convergence_covers_exactly_the_current_36_route_census():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    actual = _routes()
    recorded = [
        (route["method"], route["path"], route["function"], route["line"])
        for route in evidence["routes"]
    ]

    assert evidence["route_count"] == 36
    assert len(recorded) == 36
    assert recorded == actual


def test_route_convergence_preserves_unknown_without_false_coverage():
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    assert evidence["before_summary"] == {"UNKNOWN": 36}
    assert evidence["after_summary"] == {"UNKNOWN": 36}
    assert evidence["classification_changes"] == []
    assert evidence["route_use_of_canonical_contract_proven"] is False
    assert evidence["owner_upgrades"] == []
    assert evidence["product_or_runtime_changes"] is False
    assert Counter(route["frontier"] for route in evidence["routes"]) == {"F-004": 36}
    assert all(route["before"] == route["after"] == "UNKNOWN" for route in evidence["routes"])
    assert all(route["owner"] == "UNKNOWN_LEGACY_OWNER" for route in evidence["routes"])
    assert all(route["new_evidence"] == "B4/B5 static boundaries; no route trace" for route in evidence["routes"])


def test_route_convergence_document_records_non_upgrade_invariants():
    doc = DOC.read_text(encoding="utf-8")

    for marker in (
        "All 36 remain `UNKNOWN`",
        "canonical contract existence is not route adapter coverage",
        "source-capable provider code is not runtime readiness",
        "a probable owner is not a contractual owner",
        "a read-only method is not authorization",
        "sandbox rollback is not product persistence",
        "No bridge or migration is",
    ):
        assert marker in doc
