from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "eda265c15bed0aedce4a8bfb141f39905e03a61b"
STRATEGY = ROOT / "docs" / "FUTURE_IA_CORE_ENTERPRISE_FOUNDRY_AND_AGENT_LINEAGE.md"
ROUTE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json"
SENSITIVITY = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_SENSITIVITY_AUTHORITY_AND_VISIBILITY_CONTRACT.md"
COHERENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_FAMILY_COHERENCE_ADJUDICATION.md"
GATE_MATRIX = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_COMPATIBILITY_AND_GATE_MATRIX.json"
PLAN = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md"
GOKV = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_GOKV_DOOL_OCI_RECONCILIATION.md"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_EVIDENCE.json"
LEDGER = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_COMMIT_ACCOUNTABILITY_LEDGER.md"

EXPECTED_ROUTES = {
    "api_status_get": "GET /api/status",
    "api_memory_get": "GET /api/memory",
    "api_logs_get": "GET /api/logs",
    "api_metrics_dynamic_get": "GET /api/metrics/dynamic",
}

MISSION_FILES = {
    "README.md",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/FUTURE_IA_CORE_ENTERPRISE_FOUNDRY_AND_AGENT_LINEAGE.md",
    "docs/ROADMAP_4X_MACRO_04_P1_ROUTE_SOURCE_PAYLOAD_AND_CONSUMER_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_04_P1_SENSITIVITY_AUTHORITY_AND_VISIBILITY_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_P1_FAMILY_COHERENCE_ADJUDICATION.md",
    "docs/ROADMAP_4X_MACRO_04_P1_COMPATIBILITY_AND_GATE_MATRIX.json",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
    "docs/FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_2_execution_metric.json",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_NATIVE_G0_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_INGESTION_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_2_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_2_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/test_gokv_cognitive_kernel_0_2.py",
    "tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py",
    "docs/ROADMAP_4X_MACRO_04_P1_GOKV_DOOL_OCI_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_P1_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "tests/historical_test_context.py",
    "tests/test_roadmap_3_x_macro_04_true_completion.py",
    "tests/test_roadmap_3_x_macro_05_final_closure.py",
    "tests/test_roadmap_4x_macro_03_checkpoint.py",
    "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
    "tests/test_roadmap_3_x_macro_05_1_live_state_consistency.py",
    "tests/test_roadmap_4x_macro_04_p1_entry_review.py",
    "docs/ROADMAP_4X_MACRO_04_1_OWNER_DIRECTION_ACCEPTANCE.md",
    "docs/ROADMAP_4X_MACRO_04_1_COGNITIVE_KERNEL_G0_ARCHITECTURE.md",
    "docs/ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json",
    "docs/ROADMAP_4X_MACRO_04_1_DOOL_GENERATIONAL_LINEAGE_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_1_OCI_NECESSARY_AND_SUFFICIENT_INHERITANCE.md",
    "docs/ROADMAP_4X_MACRO_04_1_AGENT_MODEL_FIT_AND_FALLBACK_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_1_ECOSYSTEM_INHERITANCE_PRIVACY_AND_RECOVERY.md",
    "docs/ROADMAP_4X_MACRO_04_1_DOMAIN_MODULE_PARITY_AUDIT.md",
    "docs/ROADMAP_4X_MACRO_04_1_GOKV_DOOL_OCI_RECONCILIATION.md",
    "docs/ROADMAP_4X_MACRO_04_1_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "docs/ROADMAP_4X_MACRO_04_1_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_1_CHECKPOINT_EVIDENCE.json",
    "knowledge/global_operational/schema/cognitive_kernel_g0.schema.json",
    "gokv/kernel.py",
    "tests/test_gokv_cognitive_kernel_0_1.py",
    "tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py",
    "README.md",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/FUTURE_IA_CORE_ENTERPRISE_FOUNDRY_AND_AGENT_LINEAGE.md",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
}

PROTECTED_PREFIXES = (
    "core/",
    "domains/",
    "catalogs/",
    "stores/",
    "runtime/",
    "execution/",
    "providers/",
    "integrations/",
    "secrets/",
    "backend/",
    "ui/",
    "payload/",
)
PROTECTED_EXACT = {
    "api.py",
    "backend.py",
    "i18n.py",
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    value = json.loads(_text(path))
    assert isinstance(value, dict)
    return value


def _changed_from_baseline() -> set[str]:
    return set(
        subprocess.check_output(
            ["git", "diff", "--name-only", f"{BASELINE}..HEAD"],
            cwd=ROOT,
            text=True,
        ).splitlines()
    )


def test_required_macro_04_artifacts_exist_and_are_valid_json():
    for path in (
        STRATEGY,
        ROUTE_MATRIX,
        SENSITIVITY,
        COHERENCE,
        GATE_MATRIX,
        PLAN,
        GOKV,
        CHECKPOINT,
        EVIDENCE,
        LEDGER,
    ):
        assert path.exists(), path
    route_matrix = _json(ROUTE_MATRIX)
    gate_matrix = _json(GATE_MATRIX)
    evidence = _json(EVIDENCE)
    assert route_matrix["state"] == "ENTRY_REVIEW_ONLY_REMEDIATION_NOT_STARTED"
    assert gate_matrix["state"] == "PREPARED_NOT_STARTED"
    assert evidence["result"].startswith("ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_COMPLETE_")


def test_four_routes_are_exact_and_no_route_is_invented():
    route_matrix = _json(ROUTE_MATRIX)
    observed = {
        route["route_id"]: f'{route["method"]} {route["path"]}'
        for route in route_matrix["route_inventory"]
    }
    assert observed == EXPECTED_ROUTES
    assert route_matrix["integrity"]["exact_route_count"] == 4
    assert route_matrix["integrity"]["invented_routes"] == []
    assert route_matrix["integrity"]["route_execution_performed"] is False

    gate_matrix = _json(GATE_MATRIX)
    assert gate_matrix["integrity"]["route_count"] == 4
    assert gate_matrix["integrity"]["routes_exact"] == list(EXPECTED_ROUTES.values())
    assert gate_matrix["integrity"]["invented_routes"] == []
    assert {route["path"] for route in gate_matrix["routes"]} == {
        value.split(" ", 1)[1] for value in EXPECTED_ROUTES.values()
    }


def test_all_route_claims_have_a_classification_and_gates_remain_inactive():
    route_matrix = _json(ROUTE_MATRIX)
    classifications = {"OBSERVED", "INFERRED", "UNKNOWN", "EXTERNAL_EVIDENCE_REQUIRED", "UNKNOWN_DEFAULT_DENY"}
    for route in route_matrix["route_inventory"]:
        for section in ("source_chain", "sources_and_reads", "errors", "side_effects", "consumers"):
            for item in route[section]:
                assert item.get("classification") in classifications, (route["path"], section, item)

    gate_matrix = _json(GATE_MATRIX)
    for route in gate_matrix["routes"]:
        assert route["decision"] in {"CONTAIN_UNTIL_EVIDENCE", "BLOCK_UNTIL_EVIDENCE"}
        assert all(gate["state"] == "INACTIVE_EVIDENCE_REQUIRED" for gate in route["gates"])
    assert gate_matrix["external_exposure"] == "DEFAULT_DENIED"
    assert gate_matrix["remediation"] == "NOT_STARTED"


def test_family_split_and_future_plan_are_coherent():
    coherence = _text(COHERENCE)
    plan = _text(PLAN)
    assert "ROADMAP_4X_MACRO_04_P1_ENTRY_REVIEW_COMPLETE_SUBFAMILY_SPLIT_CONTRACTED" in coherence
    assert "P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED" in coherence
    assert "TRUE_HARD_FRONTIER_P1_FAMILY_BOUNDARY" in coherence
    assert "There is no `TRUE_HARD_FRONTIER_P1_FAMILY_BOUNDARY`" in coherence
    assert "PREPARED_NOT_STARTED" in plan
    assert "GET /api/status" in plan
    for excluded in ("GET /api/memory", "GET /api/logs", "GET /api/metrics/dynamic"):
        assert excluded in plan
    assert "Macro-Mission 05 is not started" in plan or "does not begin Macro-Mission 05" in plan


def test_enterprise_foundry_is_future_only_and_constitutionally_bounded():
    strategy = _text(STRATEGY)
    required = (
        "FUTURE_CONCEPT_PRESERVED_NOT_SCHEDULED_NOT_IMPLEMENTED",
        "OWNER_FINAL_AUTHORITY",
        "SUCCESS_NEVER_GRANTS_ROOT",
        "ENTERPRISE_LOCAL_REALITY_BOUNDARY",
        "PROMOTION_IS_EVIDENCE_BOUND_AND_REVERSIBLE",
        "FOUNDING_IS_A_GATED_CAPABILITY",
        "PROPOSAL_IS_NOT_APPROVAL",
        "APPROVAL_IS_NOT_EXECUTION",
        "AGENT_CAPABILITY_PASSPORT",
        "MATURITY_MIGRATES_RAW_TENANT_MEMORY_DOES_NOT",
        "FOUNDING_LEASE",
        "creation_scope",
        "creation_mode",
        "GLOBAL_CAPABILITY_KERNEL",
        "IA_CORE_ENTERPRISE_FOUNDRY",
    )
    for token in required:
        assert token in strategy
    assert "does not activate" in strategy
    assert "does not create" in strategy
    assert "No product component" in strategy
    assert "plaintext passwords" in strategy


def test_gokv_is_reconciled_without_new_candidate_or_promotion():
    gokv = _text(GOKV)
    assert "NO_NEW_CANDIDATE" in gokv
    assert "38" in gokv
    assert "New knowledge item | No" in gokv
    assert "Automatic promotion | No" in gokv
    assert "Vault write | No" in gokv
    assert "OCI_DEVELOPMENT_ONLY" in gokv


def test_macro_04_diff_is_documentary_and_protected_diff_is_empty():
    changed = _changed_from_baseline()
    assert changed
    assert changed <= MISSION_FILES
    assert not (changed & PROTECTED_EXACT)
    assert not [path for path in changed if path.startswith(PROTECTED_PREFIXES)]

    protected_diff = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            f"{BASELINE}..HEAD",
            "--",
            "api.py",
            "core",
            "domains",
            "catalogs",
            "stores",
            "runtime",
            "execution",
            "providers",
            "integrations",
            "secrets",
            "backend",
            "ui",
            "payload",
            "i18n.py",
            "backend.py",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert protected_diff == []


def test_no_product_activation_and_macro_05_remains_unstarted():
    corpus = "\n".join(_text(path) for path in (STRATEGY, SENSITIVITY, COHERENCE, PLAN, GOKV, CHECKPOINT, LEDGER))
    assert "Macro-Mission 05 is not started" in corpus or "does not begin Macro-Mission 05" in corpus
    assert "EXTERNAL_EXPOSURE_DEFAULT_DENIED" in corpus
    assert "P1 no" not in corpus
    assert "remediation_not_started" in corpus.lower() or "remediation not started" in corpus.lower()
    assert "Provider/runtime/network use | No" in corpus
