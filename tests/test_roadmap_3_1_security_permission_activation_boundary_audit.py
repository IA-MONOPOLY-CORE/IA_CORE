"""Static, side-effect-free guards for the Roadmap 3.1 audit artifacts."""

from __future__ import annotations

import ast
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_EVIDENCE.json"
AUDIT_PATH = ROOT / "docs" / "ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_AUDIT.md"
API_PATH = ROOT / "api.py"
BASELINE = "4c898eae74c0a6c59cda4e659ec6a1e2d2d3641a"
MISSION_ID = "roadmap_3_1_security_permission_activation_boundary_read_only_audit"
ALLOWED_MISSION_FILES = {
    "docs/ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_AUDIT.md",
    "docs/ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_EVIDENCE.json",
    "tests/test_roadmap_3_1_security_permission_activation_boundary_audit.py",
    "docs/ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_CHECKPOINT.md",
}
AUTH_VALUES = {
    "DEMONSTRATED",
    "NOT_DEMONSTRATED",
    "DOCUMENTED_ONLY",
    "CONFIG_DEPENDENT",
    "HOSTING_EDGE_UNKNOWN",
    "LEGACY_BYPASS_CANDIDATE",
    "NOT_APPLICABLE",
}
PROVIDER_VALUES = {
    "LEXICAL_REFERENCE",
    "IMPORTED_OR_REGISTERED",
    "SOURCE_CALLABLE",
    "CONFIG_GATED",
    "ACTIVATION_GATED",
    "PERMISSION_GATED",
    "CREDENTIAL_GATED",
    "RUNTIME_REACHABLE_NOT_EXECUTED",
    "DEPLOYMENT_REACHABILITY_UNKNOWN",
    "BLOCKED_BY_CURRENT_CONTRACT",
    "NOT_REACHABLE_FROM_ROUTE",
    "UNKNOWN",
}
WRITE_VALUES = {
    "NO_WRITE_PATH_DEMONSTRATED",
    "WRITE_CODE_PRESENT_NOT_ROUTE_REACHABLE",
    "SOURCE_CALLABLE_WRITE",
    "CONFIG_GATED_WRITE",
    "ACTIVATION_GATED_WRITE",
    "PERMISSION_GATED_WRITE",
    "ROUTE_REACHABLE_WRITE_CANDIDATE",
    "PRODUCTIVE_REACHABILITY_UNKNOWN",
    "BLOCKED_BY_CURRENT_CONTRACT",
}
REQUIRED_ROUTE_KEYS = {
    "route_id",
    "method",
    "path",
    "registration",
    "handler",
    "entrypoint_chain",
    "surface_status",
    "exposure",
    "deployment",
    "authentication",
    "authorization",
    "cors",
    "sensitive_inputs",
    "activation_gates",
    "provider_reachability",
    "network_reachability",
    "write_reachability",
    "stores",
    "subprocess_shell",
    "agent_orchestrator",
    "trust_boundaries",
    "controls",
    "bypass_candidates",
    "evidence_positive",
    "evidence_negative_limited",
    "confidence",
    "unknowns",
    "severity",
}


def _read_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _static_routes() -> list[dict[str, object]]:
    tree = ast.parse(API_PATH.read_text(encoding="utf-8"), filename=str(API_PATH))
    routes: list[dict[str, object]] = []
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
                and isinstance(decorator.args[0].value, str)
            ):
                continue
            routes.append(
                {
                    "method": decorator.func.attr.upper(),
                    "path": decorator.args[0].value,
                    "registration_line": decorator.lineno,
                    "handler": node.name,
                    "handler_line": node.lineno,
                }
            )
    return sorted(routes, key=lambda route: int(route["registration_line"]))


def _git_lines(*args: str) -> list[str]:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).splitlines()


def test_manifest_is_valid_and_identifies_the_mission():
    manifest = _read_manifest()
    assert manifest["schema_version"].startswith("roadmap_3_1_")
    assert manifest["mission_id"] == MISSION_ID
    assert manifest["baseline_head"] == BASELINE
    assert manifest["generated_from_commit"] == BASELINE


def test_manifest_matches_static_api_route_census():
    manifest = _read_manifest()
    expected = _static_routes()
    actual = manifest["routes"]

    assert len(expected) == 36
    assert len(actual) == manifest["route_count"] == 36
    expected_keys = {(route["method"], route["path"]) for route in expected}
    actual_keys = {(route["method"], route["path"]) for route in actual}
    assert actual_keys == expected_keys
    assert len(actual_keys) == len(actual)
    assert Counter(route["method"] for route in expected) == {
        "GET": 22,
        "POST": 12,
        "PUT": 1,
        "DELETE": 1,
    }
    assert manifest["method_counts"] == {
        "GET": 22,
        "POST": 12,
        "PUT": 1,
        "DELETE": 1,
        "mutative_total": 14,
    }

    for source, recorded in zip(expected, sorted(actual, key=lambda route: route["registration"]["line"])):
        assert recorded["method"] == source["method"]
        assert recorded["path"] == source["path"]
        assert recorded["registration"] == {
            "file": "api.py",
            "line": source["registration_line"],
            "symbol": f"app.{source['method'].lower()}",
        }
        assert recorded["handler"] == {
            "file": "api.py",
            "line": source["handler_line"],
            "symbol": source["handler"],
        }


def test_every_route_has_security_and_reachability_classifications():
    manifest = _read_manifest()
    for route in manifest["routes"]:
        assert REQUIRED_ROUTE_KEYS <= route.keys(), route["route_id"]
        assert route["authentication"] in AUTH_VALUES
        assert route["authorization"] in AUTH_VALUES
        assert route["cors"] == "WILDCARD_GLOBAL_MIDDLEWARE"
        assert route["provider_reachability"] in PROVIDER_VALUES
        assert route["write_reachability"] in WRITE_VALUES
        assert route["deployment"] == "HOSTING_EDGE_UNKNOWN"
        assert route["exposure"] == "ROUTE_REGISTERED_NOT_DEPLOYMENT_PROVEN"
        assert route["activation_gates"]
        assert route["trust_boundaries"]
        assert route["evidence_positive"]
        assert route["evidence_negative_limited"]
        assert route["unknowns"]
        assert route["confidence"] in {"HIGH", "MEDIUM", "LOW"}
        assert route["severity"] in {"P0", "P1", "P2", "P3"}


def test_mutative_routes_and_required_sensitive_surfaces_are_present():
    manifest = _read_manifest()
    routes = {(route["method"], route["path"]): route for route in manifest["routes"]}
    mutative = [route for route in manifest["routes"] if route["method"] != "GET"]
    assert len(mutative) == 14
    assert all(route["write_reachability"] in WRITE_VALUES for route in mutative)
    assert ("POST", "/api/chat") in routes
    assert ("POST", "/api/settings") in routes
    assert routes[("POST", "/api/chat")]["provider_reachability"] == "SOURCE_CALLABLE"
    assert routes[("POST", "/api/settings")]["sensitive_inputs"] == [
        "api_key (name only)",
        "provider",
        "model",
        "selected_agents",
    ]
    assert routes[("POST", "/api/settings")]["write_reachability"] == "ROUTE_REACHABLE_WRITE_CANDIDATE"


def test_manifest_contains_boundary_and_gate_evidence():
    manifest = _read_manifest()
    assert len(manifest["trust_boundaries"]) >= 8
    assert len(manifest["activation_gates"]) >= 6
    assert len(manifest["provider_paths"]) >= 4
    assert len(manifest["write_paths"]) >= 6
    assert manifest["secret_flows"]
    assert {flow["flow_id"] for flow in manifest["secret_flows"]} == {"settings_api_key"}
    assert all(flow["value_read_by_audit"] is False for flow in manifest["secret_flows"])
    assert all(flow["value_included_in_evidence"] is False for flow in manifest["secret_flows"])
    assert manifest["unknowns"]
    assert all("UNKNOWN" in item["status"] or "PRESERVED" in item["status"] for item in manifest["unknowns"])


def test_documentation_has_all_route_rows_and_matches_manifest():
    manifest = _read_manifest()
    doc = AUDIT_PATH.read_text(encoding="utf-8")
    rows = re.findall(r"^\| `([^`]+)` \| (GET|POST|PUT|DELETE) \| (\d+) \|", doc, re.MULTILINE)
    assert len(rows) == 36
    documented = {(method, path, int(line)) for path, method, line in rows}
    expected = {
        (route["method"], route["path"], route["registration"]["line"])
        for route in manifest["routes"]
    }
    assert documented == expected
    assert "REMEDIATION_NOT_DESIGNED_OUT_OF_SCOPE" in doc
    assert "HOSTING_EDGE_UNKNOWN" in doc
    assert "IA_CORE_clean(1).zip" in doc


def test_manifest_does_not_contain_secret_values_or_unsupported_reachability_claims():
    raw = MANIFEST_PATH.read_text(encoding="utf-8")
    assert not re.search(r"(?:nvapi-|sk-[A-Za-z0-9]|gh[pousr]_[A-Za-z0-9]|Bearer\s+[A-Za-z0-9._-]{20,})", raw)
    manifest = _read_manifest()
    for route in manifest["routes"]:
        assert "DEPLOYMENT_REACHABLE" not in route["exposure"]
        assert route["deployment"] == "HOSTING_EDGE_UNKNOWN"
    assert all(path["network_invoked"] is False for path in manifest["provider_paths"])


def test_product_and_governance_diff_are_outside_the_mission_scope():
    tracked = set(_git_lines("diff", "--name-only", f"{BASELINE}..HEAD"))
    status = _git_lines("status", "--porcelain=v1", "-uall")
    working = {line[3:] for line in status if len(line) >= 4 and line[0:2] in {"??", " M", "M ", "A ", "AM", "MM"}}
    changed = tracked | working
    assert changed <= ALLOWED_MISSION_FILES, sorted(changed - ALLOWED_MISSION_FILES)
    assert "api.py" not in changed
    assert not any(path.startswith("knowledge/") for path in changed)
    assert not any(path.startswith("providers/") for path in changed)
    assert not any(path.startswith("core/") for path in changed)


def test_static_sources_show_the_expected_boundary_markers_without_importing_them():
    api = API_PATH.read_text(encoding="utf-8")
    runtime_gate = (ROOT / "core" / "runtime_activation_gate.py").read_text(encoding="utf-8")
    attempt_factory = (ROOT / "core" / "attempt_factory.py").read_text(encoding="utf-8")
    confirmation_gate = (ROOT / "core" / "backend_internal_confirmation_gate.py").read_text(encoding="utf-8")
    assert 'allow_origins=["*"]' in api
    assert 'allow_methods=["*"]' in api
    assert 'allow_headers=["*"]' in api
    assert "api_key: Optional[str] = Form(None)" in api
    assert "RUNTIME_NETWORK_ENABLED = False" in runtime_gate
    assert "RUNTIME_SECRET_ACCESS_ENABLED = False" in runtime_gate
    assert "ATTEMPT_FACTORY_ENABLED = False" in attempt_factory
    assert "ATTEMPT_FACTORY_EXTERNAL_ACCESS_ENABLED = False" in attempt_factory
    assert '"allow_runtime": False' in confirmation_gate
    assert '"allow_execution": False' in confirmation_gate
