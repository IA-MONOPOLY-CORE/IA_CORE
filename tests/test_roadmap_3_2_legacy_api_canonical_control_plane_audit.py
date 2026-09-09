"""Static, side-effect-free guards for the Roadmap 3.2 audit artifacts."""

from __future__ import annotations

import ast
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_EVIDENCE.json"
AUDIT_PATH = ROOT / "docs" / "ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_AUDIT.md"
CHECKPOINT_PATH = ROOT / "docs" / "ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_CHECKPOINT.md"
API_PATH = ROOT / "api.py"
ROADMAP_3_1_MANIFEST_PATH = ROOT / "docs" / "ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_EVIDENCE.json"
BASELINE = "2255295f5ffe4f7348476acfca606a84aa12af35"
MISSION_ID = "roadmap_3_2_legacy_api_canonical_control_plane_coverage_read_only_audit"

ALLOWED_MISSION_FILES = {
    "docs/ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_AUDIT.md",
    "docs/ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_EVIDENCE.json",
    "tests/test_roadmap_3_2_legacy_api_canonical_control_plane_audit.py",
    "docs/ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_CHECKPOINT.md",
}

COVERAGE_VALUES = {
    "CANONICAL_CONTROL_PLANE_COVERED",
    "PARTIALLY_COVERED",
    "LEGACY_BYPASS_DEMONSTRATED",
    "COVERAGE_NOT_DEMONSTRATED",
    "NOT_APPLICABLE",
}

READINESS_VALUES = {
    "REMEDIATION_SEMANTICS_DERIVABLE_FROM_EXISTING_CONTRACT",
    "MORE_READ_ONLY_TRUTH_REQUIRED",
    "REQUIRES_DIRECTION_POLICY_DECISION",
    "REQUIRES_EXTERNAL_EVIDENCE",
    "REQUIRES_RUNTIME_EVIDENCE",
    "ALREADY_COMPLIANT",
    "FUTURE_NOT_NOW",
}

REQUIRED_ROUTE_KEYS = {
    "route_id",
    "method",
    "path",
    "registration",
    "handler",
    "legacy_current_classification",
    "coverage_classification",
    "contract_exists_for_relevant_surface",
    "route_uses_contract",
    "auth",
    "authz",
    "permission_contract",
    "capability_contract",
    "request_validation",
    "request_envelope",
    "confirmation_gate",
    "activation_gate",
    "runtime_gate",
    "executor",
    "write_store_guard",
    "secret_policy",
    "ownership_resource_policy",
    "lifecycle_validator",
    "response_contract",
    "audit_evidence_path",
    "canonical_control_plane_entrypoint",
    "coverage_evidence",
    "bypass_evidence",
    "confidence",
    "unknowns",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def test_manifest_identifies_mission_and_baseline():
    manifest = _read_json(MANIFEST_PATH)
    assert manifest["mission_id"] == MISSION_ID
    assert manifest["baseline_head"] == BASELINE
    assert manifest["generated_from_commit"] == BASELINE
    assert manifest["mode"] == "READ_ONLY_PRODUCT_AUDIT"
    assert manifest["source_constraints"]["historical_zip"].startswith("IA_CORE_clean(1).zip")
    assert manifest["source_constraints"]["secret_values_read"] is False


def test_manifest_matches_exact_static_route_census():
    manifest = _read_json(MANIFEST_PATH)
    expected = _static_routes()
    actual = manifest["routes"]

    assert len(expected) == 36
    assert len(actual) == manifest["route_count"] == 36
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

    expected_keys = {(route["method"], route["path"]) for route in expected}
    actual_keys = {(route["method"], route["path"]) for route in actual}
    assert actual_keys == expected_keys
    assert len(actual_keys) == len(actual)

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


def test_every_route_has_full_coverage_contract_and_evidence_fields():
    manifest = _read_json(MANIFEST_PATH)
    for route in manifest["routes"]:
        assert REQUIRED_ROUTE_KEYS <= route.keys(), route["route_id"]
        assert route["legacy_current_classification"] == "LEGACY"
        assert route["coverage_classification"] in COVERAGE_VALUES
        assert isinstance(route["contract_exists_for_relevant_surface"], bool)
        assert isinstance(route["route_uses_contract"], bool)
        assert route["contract_exists_for_relevant_surface"] is True
        assert route["route_uses_contract"] is False
        assert route["coverage_evidence"], route["route_id"]
        assert route["unknowns"], route["route_id"]
        assert route["confidence"] in {"HIGH", "MEDIUM", "LOW"}
        assert route["auth"] == "NOT_DEMONSTRATED"
        assert route["authz"] == "NOT_DEMONSTRATED"

    assert manifest["coverage_counts"] == dict(
        CANONICAL_CONTROL_PLANE_COVERED=0,
        PARTIALLY_COVERED=1,
        LEGACY_BYPASS_DEMONSTRATED=2,
        COVERAGE_NOT_DEMONSTRATED=33,
        NOT_APPLICABLE=0,
    )
    assert Counter(route["coverage_classification"] for route in manifest["routes"]) == Counter(
        manifest["coverage_counts"]
    )


def test_mutative_and_high_risk_routes_are_reconciled():
    manifest = _read_json(MANIFEST_PATH)
    routes = {(route["method"], route["path"]): route for route in manifest["routes"]}
    mutative = [route for route in manifest["routes"] if route["method"] != "GET"]
    assert len(mutative) == 14

    chat = routes[("POST", "/api/chat")]
    assert chat["coverage_classification"] == "LEGACY_BYPASS_DEMONSTRATED"
    assert chat["route_uses_contract"] is False
    assert any("supervisor" in item.lower() or "provider" in item.lower() for item in chat["coverage_evidence"])
    assert chat["bypass_evidence"]

    settings = routes[("POST", "/api/settings")]
    assert settings["coverage_classification"] == "LEGACY_BYPASS_DEMONSTRATED"
    assert "api_key" in settings["secret_policy"]
    assert "config.py" in settings["write_store_guard"]
    assert settings["bypass_evidence"]

    domain_create = routes[("POST", "/api/domains/create")]
    assert domain_create["coverage_classification"] == "PARTIALLY_COVERED"
    assert "core.domain_registry.create_domain" in domain_create["executor"]

    findings = {finding["finding_id"]: finding for finding in manifest["findings"]}
    assert set(findings) == {
        "F-3.1-001",
        "F-3.1-002",
        "F-3.1-003",
        "F-3.1-004",
        "F-3.1-005",
        "F-3.1-006",
        "F-3.1-007",
    }
    assert all(findings[key]["provenance_preserved"] is True for key in findings)
    assert all(findings[key]["remediation_readiness"] in READINESS_VALUES for key in findings)


def test_canonical_census_is_nonempty_and_provenance_backed():
    manifest = _read_json(MANIFEST_PATH)
    census = manifest["canonical_control_plane_census"]
    assert len(census) >= 10
    assert len({item["control_id"] for item in census}) == len(census)
    for item in census:
        assert item["control_id"]
        assert item["files"]
        assert item["symbols"]
        assert item["purpose"]
        assert item["state"]
        assert item["test_evidence"]
        assert item["provenance"]
        for evidence_path in item["test_evidence"]:
            assert (ROOT / evidence_path).exists(), evidence_path


def test_contract_existence_is_distinct_from_route_usage():
    manifest = _read_json(MANIFEST_PATH)
    relationships = {
        (route["contract_exists_for_relevant_surface"], route["route_uses_contract"])
        for route in manifest["routes"]
    }
    assert (True, False) in relationships
    assert all(route["contract_exists_for_relevant_surface"] != route["route_uses_contract"] for route in manifest["routes"])
    assert "canonical contract" in manifest["coverage_matrix_semantics"]["contract_exists"]
    assert "canonical entrypoint" in manifest["coverage_matrix_semantics"]["route_uses_contract"]


def test_gokv_state_and_frontier_are_conservative():
    manifest = _read_json(MANIFEST_PATH)
    gokv = manifest["gokv_oci_dool"]
    assert gokv["oci_mode"] == "PROMOTED_ONLY"
    assert gokv["conflict_policy"] == "CURRENT_CONTRACT_WINS"
    assert gokv["conditioned_autonomy"] == "VALIDATED"
    assert gokv["conditioned_autonomy_promoted"] is False
    assert manifest["frontiers"]["hard_frontier_crossed"] is False
    assert manifest["new_findings"] == []


def test_docs_contain_all_routes_and_required_read_only_claims():
    manifest = _read_json(MANIFEST_PATH)
    doc = AUDIT_PATH.read_text(encoding="utf-8")
    rows = re.findall(r"^\| `([^`]+)` \| (GET|POST|PUT|DELETE) \| (\d+) \|", doc, re.MULTILINE)
    assert len(rows) == 36
    documented = {(method, path, int(line)) for path, method, line in rows}
    expected = {
        (route["method"], route["path"], route["registration"]["line"])
        for route in manifest["routes"]
    }
    assert documented == expected
    for marker in (
        "READ_ONLY_PRODUCT_AUDIT",
        "COVERAGE_NOT_DEMONSTRATED",
        "LEGACY_BYPASS_DEMONSTRATED",
        "CONTRACT_EXISTS",
        "ROUTE_USES_CONTRACT",
        "True hard frontiers",
        "No fix, bridge or policy was written.",
        "IA_CORE_clean(1).zip",
    ):
        assert marker in doc


def test_no_secret_values_or_unsupported_runtime_deployment_claims():
    raw = MANIFEST_PATH.read_text(encoding="utf-8")
    doc = AUDIT_PATH.read_text(encoding="utf-8")
    combined = f"{raw}\n{doc}"
    assert not re.search(r"(?:nvapi-|sk-[A-Za-z0-9]|gh[pousr]_[A-Za-z0-9]|Bearer\s+[A-Za-z0-9._-]{20,})", combined)
    assert "actual invocation" in combined
    assert "deployment edge" in combined
    assert "No provider, network, runtime" in combined
    assert "REMEDIATION_SEMANTICS_DERIVABLE_FROM_EXISTING_CONTRACT" in combined
    assert "TRUE_HARD_FRONTIER" not in raw


def test_api_has_no_demonstrated_canonical_bridge_import_or_call():
    api = API_PATH.read_text(encoding="utf-8")
    for marker in (
        "backend_internal_",
        "agent_permission_contract",
        "secrets_policy",
        "runtime_activation_gate",
        "dispatch_internal_request",
        "validate_internal_request_envelope",
        "validate_confirmation_gate",
    ):
        assert marker not in api


def test_checkpoint_exists_and_declares_final_boundary():
    text = CHECKPOINT_PATH.read_text(encoding="utf-8")
    assert "ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_COVERAGE_READ_ONLY_AUDIT_PASSED" in text
    assert "No product code, remediation or bridge was written" in text
    assert "POST-MISSION ARCHITECTURAL RECALCULATION" in text


def test_product_and_governance_diff_are_outside_mission_scope():
    tracked = set(_git_lines("diff", "--name-only", f"{BASELINE}..HEAD"))
    status = _git_lines("status", "--porcelain=v1", "-uall")
    working = {
        line[3:]
        for line in status
        if len(line) >= 4 and line[0:2] in {"??", " M", "M ", "A ", "AM", "MM"}
    }
    changed = tracked | working
    assert changed <= ALLOWED_MISSION_FILES, sorted(changed - ALLOWED_MISSION_FILES)
    assert "api.py" not in changed
    assert not any(path.startswith("knowledge/") for path in changed)
    assert not any(path.startswith("providers/") for path in changed)
    assert not any(path.startswith("core/") for path in changed)
    assert not any(path.startswith("agents/") for path in changed)
    assert not any(path.startswith("domains/") for path in changed)
