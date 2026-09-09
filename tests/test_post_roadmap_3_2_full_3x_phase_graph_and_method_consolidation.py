"""Static guards for the post-Roadmap 3.2 documentary 3.x graph."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "fd9cc6fcf2040d630a2dba2dee635d63e7c07ccb"
MISSION_ID = "post_roadmap_3_2_full_3x_phase_execution_graph_frontier_engineering_and_method_consolidation"
GRAPH_PATH = ROOT / "docs" / "ROADMAP_3_X_FULL_PHASE_EXECUTION_GRAPH.md"
MAP_PATH = ROOT / "docs" / "ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json"
ENTERPRISE_PATH = ROOT / "docs" / "IA_CORE_ENTERPRISE_READINESS_ARCHITECTURAL_RESERVATIONS.md"
METHOD_PATH = ROOT / "docs" / "METHOD_SANTI_3_0_VERIFIED_ADAPTIVE_PROJECT_DIRECTION_ENGINEERING.md"
CREATIVE_PATH = ROOT / "docs" / "METHOD_SANTI_CREATIVE_INTAKE_PLACEMENT_FRAMEWORK.md"
GENESIS_PATH = ROOT / "docs" / "PROJECT_GENESIS_PACK_CONCEPT.md"
CHECKPOINT_PATH = ROOT / "docs" / "POST_ROADMAP_3_2_FULL_3X_GRAPH_METHOD_CONSOLIDATION_CHECKPOINT.md"
HISTORICAL_3_1_TEST = ROOT / "tests" / "test_roadmap_3_1_security_permission_activation_boundary_audit.py"

ALLOWED_FILES = {
    "docs/ROADMAP_3_X_FULL_PHASE_EXECUTION_GRAPH.md",
    "docs/ROADMAP_3_X_FRONTIER_ENGINEERING_MAP.json",
    "docs/IA_CORE_ENTERPRISE_READINESS_ARCHITECTURAL_RESERVATIONS.md",
    "docs/METHOD_SANTI_3_0_VERIFIED_ADAPTIVE_PROJECT_DIRECTION_ENGINEERING.md",
    "docs/METHOD_SANTI_CREATIVE_INTAKE_PLACEMENT_FRAMEWORK.md",
    "docs/PROJECT_GENESIS_PACK_CONCEPT.md",
    "tests/test_post_roadmap_3_2_full_3x_phase_graph_and_method_consolidation.py",
    "docs/POST_ROADMAP_3_2_FULL_3X_GRAPH_METHOD_CONSOLIDATION_CHECKPOINT.md",
    "tests/test_roadmap_3_2_legacy_api_canonical_control_plane_audit.py",
}

REQUIRED_SURFACE_KEYS = {
    "surface_id",
    "title",
    "current_state",
    "source",
    "why_it_belongs_to_3x",
    "dependencies",
    "risk",
    "evidence_available",
    "unknown",
    "remediation_readiness",
    "external_evidence_required",
    "human_decision_required",
    "already_closed_by",
    "blocks_3x_exit",
}

REQUIRED_BLOCK_KEYS = {
    "block_id",
    "objective",
    "input_postconditions",
    "surfaces",
    "dependencies",
    "expected_stations",
    "dynamic_station_families",
    "test_policy",
    "rollback_model",
    "expected_output",
    "postconditions",
    "next_candidate_blocks",
}

REQUIRED_FRONTIER_KEYS = {
    "frontier_id",
    "from_block",
    "potential_next_block",
    "why_sensitive",
    "current_classification",
    "required_evidence",
    "dissolve_if",
    "apparent_if",
    "true_hard_if",
    "preauthorized_branches",
    "reconnaissance_branch",
    "safe_pause_condition",
    "route_recalculation_trigger",
    "next_frontier_if_dissolved",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _map() -> dict:
    return json.loads(_read(MAP_PATH))


def _git_lines(*args: str) -> list[str]:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).splitlines()


def test_identity_baseline_and_artifact_presence():
    data = _map()
    assert data["mission_id"] == MISSION_ID
    assert data["baseline_head"] == BASELINE
    assert data["mode"] == "READ_ONLY_PRODUCT_DOCUMENTATION_AND_PLANNING_ONLY"
    for path in (
        GRAPH_PATH,
        MAP_PATH,
        ENTERPRISE_PATH,
        METHOD_PATH,
        CREATIVE_PATH,
        GENESIS_PATH,
        CHECKPOINT_PATH,
    ):
        assert path.exists(), path


def test_completion_contract_defines_required_truths_and_exit_unknowns():
    contract = _map()["completion_contract"]
    assert contract["contract_id"] == "ROADMAP_3_X_COMPLETION_CONTRACT"
    for key in (
        "required_truths",
        "required_security_truths",
        "required_contract_truths",
        "required_lifecycle_truths",
        "required_provider_truths",
        "required_persistence_truths",
        "required_legacy_truths",
        "required_test_truths",
        "allowed_unknowns_at_3x_exit",
        "forbidden_unknowns_at_3x_exit",
        "entry_contract_for_next_phase",
    ):
        assert contract[key]
    assert "ROADMAP_3_X_CLOSED" in contract["entry_contract_for_next_phase"]


def test_full_terrain_has_provenance_and_exit_relevance():
    surfaces = _map()["surfaces"]
    assert len(surfaces) >= 15
    ids = {surface["surface_id"] for surface in surfaces}
    assert len(ids) == len(surfaces)
    for surface in surfaces:
        assert REQUIRED_SURFACE_KEYS <= surface.keys(), surface["surface_id"]
        assert surface["source"]
        assert surface["dependencies"] is not None
        assert isinstance(surface["blocks_3x_exit"], bool)


def test_blocks_have_dependencies_postconditions_and_dynamic_stations():
    blocks = _map()["blocks"]
    assert len(blocks) == 8
    ids = {block["block_id"] for block in blocks}
    assert ids == {f"B-{index}" for index in range(8)}
    for block in blocks:
        assert REQUIRED_BLOCK_KEYS <= block.keys(), block["block_id"]
        assert block["expected_stations"]
        assert block["dynamic_station_families"]
        assert block["postconditions"]
        assert block["rollback_model"]


def test_conditional_edges_are_bounded_and_do_not_amplify_authority():
    edges = _map()["conditional_edges"]
    assert edges
    for edge in edges:
        for key in ("continue_if", "recalculate_if", "stop_if", "reorder_if", "human_decision_if"):
            assert key in edge
        assert edge["route_reorder_authorized"] in {True, False}
        joined = " ".join(
            item
            for key in ("continue_if", "recalculate_if", "stop_if", "reorder_if", "human_decision_if")
            for item in edge[key]
        ).lower()
        assert "new authority" not in joined or "no new authority" in joined
        assert "same" in joined or edge["route_reorder_authorized"] is False


def test_frontiers_have_classification_and_safe_stop_dissolution_conditions():
    frontiers = _map()["frontiers"]
    assert len(frontiers) == 12
    allowed = {
        "APPARENT_FRONTIER",
        "RESOLVABLE_FRONTIER",
        "CONDITIONAL_FRONTIER",
        "EXTERNAL_EVIDENCE_FRONTIER",
        "TRUE_HARD_FRONTIER",
        "EMERGENT_ONLY_UNKNOWN",
    }
    for frontier in frontiers:
        assert REQUIRED_FRONTIER_KEYS <= frontier.keys(), frontier["frontier_id"]
        assert frontier["current_classification"] in allowed
        assert frontier["required_evidence"]
        assert frontier["safe_pause_condition"]
        assert frontier["route_recalculation_trigger"]
    assert sum(item["current_classification"] == "TRUE_HARD_FRONTIER" for item in frontiers) == 3
    assert sum(item["current_classification"] == "EXTERNAL_EVIDENCE_FRONTIER" for item in frontiers) == 2


def test_frontier_metrics_are_documentary_counts_not_readiness_claims():
    metrics = _map()["frontier_metrics"]
    assert metrics["raw_frontier_distance"]["value"] == 12
    assert metrics["effective_true_frontier_distance"]["value"] == 5
    assert "not a runtime distance" in metrics["not_claimed"].lower()
    assert _map()["gps_protocol"]["stop_execution_is_not_close_macro_mission"] is True


def test_roadmap_3_2_is_route_recalculation_evidence():
    text = _read(GRAPH_PATH)
    for marker in (
        "APPARENT_FRONTIER",
        "SAFE_PAUSE",
        "ROUTE_RECALCULATION",
        "CONTINUATION_DIRECTIVE",
        "SAME MACRO-MISSION",
        "Frontier Engineering",
        "ROADMAP_3_X_CLOSED",
    ):
        assert marker in text
    assert "does not select or execute it" in text


def test_enterprise_reservations_contain_exactly_the_18_future_surfaces():
    text = _read(ENTERPRISE_PATH)
    ids = re.findall(r"^### (ER-\d{3}) -", text, re.MULTILINE)
    assert ids == [f"ER-{index:03d}" for index in range(1, 19)]
    for marker in (
        "ARCHITECTURAL_RESERVATION",
        "FUTURE",
        "NO_CURRENT_IMPLEMENTATION_CLAIM",
        "No reservation creates an endpoint",
    ):
        assert marker in text
    for capability in (
        "Privacy and data protection",
        "Data sovereignty and residency",
        "Compliance and regulatory controls",
        "Advanced audit and traceability",
        "Advanced security",
        "IAM and Identity Access Management",
        "Segregation of duties",
        "Resilience",
        "Disaster recovery and business continuity",
        "SLA and service objectives",
        "Enterprise observability",
        "Support and service operations",
        "Incident management",
        "Procurement and acquisition lifecycle",
        "Contracts, responsibility and accountability",
        "Legacy integrations",
        "Certifications and sector requirements",
        "Enterprise deployment and operation",
    ):
        assert capability in text


def test_method_santi_3_preserves_prior_versions_and_is_direction_approved():
    text = _read(METHOD_PATH)
    for marker in (
        "METHOD_SANTI_1_0",
        "PRESERVED",
        "METHOD_SANTI_2_0",
        "METHOD_SANTI_3_0",
        "DIRECTION_APPROVED",
        "ACTIVE",
        "EVOLVING",
        "DESTINATION != CURRENT_ROUTE",
        "PHASE_COMPLETION_CONTRACT",
        "Frontier Engineering",
        "Frontier Dissolution Contract",
        "Effective Block Size",
        "Safe Operating Envelope Expansion",
        "STOP_EXECUTION != CLOSE_MACRO_MISSION",
        "SAFE_PAUSE",
        "ROUTE_RECALCULATION_CHECKPOINT",
        "CONTINUATION_DIRECTIVE",
        "Project Genesis Pack",
        "no automatic promotion",
    ):
        assert marker in text


def test_creative_intake_has_exact_eight_primary_boxes_and_idea_record():
    text = _read(CREATIVE_PATH)
    boxes = (
        "PRODUCT_NOW",
        "PRODUCT_FUTURE",
        "ARCHITECTURAL_RESERVATION",
        "METHOD_EVOLUTION",
        "OPERATIONAL_LEARNING",
        "BUSINESS_STRATEGY",
        "EXTERNAL_BENCHMARK",
        "NOT_RELEVANT_DISCARD",
    )
    for box in boxes:
        assert box in text
    for field in (
        "IDEA_ID",
        "DATE",
        "RAW_IDEA",
        "PRIMARY_CLASSIFICATION",
        "WHY_IT_MATTERS",
        "WHY_NOW",
        "WHY_NOT_NOW",
        "ARCHITECTURAL_HOME",
        "DEPENDENCIES",
        "TRIGGER_TO_REVISIT",
        "RISK_IF_FORGOTTEN",
        "STATUS",
        "SOURCE_PROVENANCE",
    ):
        assert field in text
    assert "BASE_DOCUMENT_RECOMMENDED_FOR_NEW_AND_EXISTING_PROJECTS" in text


def test_project_genesis_pack_is_defined_without_tooling_claim():
    text = _read(GENESIS_PATH)
    for field in (
        "METHOD",
        "AUTHORITY_MODEL",
        "SOURCE_OF_TRUTH",
        "PREFLIGHT",
        "MISSION_MODEL",
        "STATION_MODEL",
        "GATE_MODEL",
        "FRONTIER_MODEL",
        "TEST_POLICY",
        "GIT_CHECKPOINT_POLICY",
        "RECOVERY_MODEL",
        "REPORT_CONTRACT",
        "CREATIVE_INTAKE",
        "LEARNING_LIFECYCLE",
        "METRICS",
        "READINESS_MODEL",
    ):
        assert field in text
    assert "not automatic tooling" in text.lower()


def test_historical_guard_and_gokv_boundaries_are_preserved():
    historical = _read(HISTORICAL_3_1_TEST)
    assert "FINAL_CHECKPOINT" in historical
    assert 'f"{BASELINE}..HEAD"' not in historical
    data = _map()
    assert data["gokv_oci_dool"]["oci_mode"] == "PROMOTED_ONLY"
    assert data["gokv_oci_dool"]["conditioned_autonomy_promoted"] is False
    assert data["gokv_oci_dool"]["dool_learning_created"] is False


def test_checkpoint_declares_documentary_pass_and_no_next_execution():
    text = _read(CHECKPOINT_PATH)
    for marker in (
        "POST_ROADMAP_3_2_FULL_3X_PHASE_EXECUTION_GRAPH_AND_METHOD_CONSOLIDATION_PASSED",
        "DOCUMENTATION_AND_PLANNING_ONLY",
        "No product code",
        "Do not select or execute",
        "CHAT / ARCHITECT",
    ):
        assert marker in text


def test_no_secrets_product_changes_or_unauthorized_mission_files():
    combined = "\n".join(
        _read(path)
        for path in (
            GRAPH_PATH,
            MAP_PATH,
            ENTERPRISE_PATH,
            METHOD_PATH,
            CREATIVE_PATH,
            GENESIS_PATH,
            CHECKPOINT_PATH,
        )
    )
    assert not re.search(r"(?:nvapi-|sk-[A-Za-z0-9]|gh[pousr]_[A-Za-z0-9]|Bearer\s+[A-Za-z0-9._-]{20,})", combined)
    tracked = set(_git_lines("diff", "--name-only", f"{BASELINE}..HEAD"))
    status = _git_lines("status", "--porcelain=v1", "-uall")
    working = {
        line[3:]
        for line in status
        if len(line) >= 4 and line[0:2] in {"??", " M", "M ", "A ", "AM", "MM"}
    }
    changed = tracked | working
    assert changed <= ALLOWED_FILES, sorted(changed - ALLOWED_FILES)
    forbidden_prefixes = ("api.py", "core/", "agents/", "providers/", "domains/", "knowledge/", "memory/")
    assert not any(path == prefix or path.startswith(prefix) for path in changed for prefix in forbidden_prefixes)
