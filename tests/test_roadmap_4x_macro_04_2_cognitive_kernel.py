from __future__ import annotations

import json
from pathlib import Path
import subprocess

from gokv.kernel import load_kernel_graph
from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "01c45650ad8a5a3322a3326e7f6d4c5d90d796df"
GRAPH = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_2_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_2_CHECKPOINT_EVIDENCE.json"
P1_PLAN = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md"
OS_DOC = ROOT / "docs" / "FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md"
SECURITY_DOC = ROOT / "docs" / "FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md"

ALLOWED_FILES = {
    "README.md",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
    "docs/FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md",
    "docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md",
    "docs/ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json",
    "knowledge/global_operational/schema/cognitive_kernel_g0.schema.json",
    "gokv/kernel.py",
    "tests/test_gokv_cognitive_kernel_0_1.py",
    "tests/test_gokv_cognitive_kernel_0_2.py",
    "tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py",
    "tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py",
    "tests/test_roadmap_3_x_macro_04_true_completion.py",
    "tests/test_roadmap_3_x_macro_05_final_closure.py",
    "tests/test_roadmap_3_x_macro_05_1_live_state_consistency.py",
    "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
    "tests/test_roadmap_4x_macro_03_checkpoint.py",
    "tests/test_roadmap_4x_macro_04_p1_entry_review.py",
    "tests/historical_test_context.py",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_NATIVE_G0_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_INGESTION_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_2_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_2_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_2_execution_metric.json",
}
PROTECTED_PREFIXES = (
    "api.py", "core/", "domains/", "stores/", "runtime/", "execution/",
    "providers/", "integrations/", "secrets/", "backend/", "ui/", "payload/",
)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def changed_files() -> set[str]:
    checkpoint = "6dd040e0985da134f18f2bc85a338aa1bf770d3f"
    committed = set(subprocess.check_output(["git", "diff", "--name-only", f"{BASELINE}..{checkpoint}"], cwd=ROOT, text=True).splitlines())
    return {path.replace("\\", "/") for path in committed if path}


def test_checkpoint_and_security_contract_are_present():
    graph = load_kernel_graph(GRAPH)
    assert len(graph["nodes"]) == 13
    assert len(graph["edges"]) == 10
    assert CHECKPOINT.is_file() and EVIDENCE.is_file()
    evidence = json.loads(text(EVIDENCE))
    assert evidence["mission"] == "ROADMAP_4X_MACRO_04_2"
    assert evidence["result"].endswith("P1_A_RELEASED_AS_NEXT_SELECTED_NOT_STARTED")
    assert json.loads((ROOT / "knowledge/global_operational/schema/cognitive_kernel_g0.schema.json").read_text(encoding="utf-8"))["$id"] == "ia_core.cognitive_kernel.g0.v1"


def test_future_security_os_and_p1_boundaries_are_explicit():
    checkpoint = text(CHECKPOINT)
    p1 = text(P1_PLAN)
    os_doc = text(OS_DOC)
    security = text(SECURITY_DOC)
    for token in (
        "SECURITY_IS_A_NATIVE_OPERATING_PLANE",
        "SECURITY_STRENGTH_MUST_BE_MEASURED_NOT_MARKETED",
        "UNTRUSTED_SECURITY_REPOSITORIES_ARE_EVIDENCE_NOT_AUTHORITY",
        "FUTURE_CONCEPT_PRESERVED_NOT_SCHEDULED_NOT_IMPLEMENTED",
        "FUTURE_IA_CORE_OS_DIRECTION_PRESERVED_NOT_IMPLEMENTED",
        "NEXT_SELECTED_NOT_STARTED",
        "P1-B",
        "P1-C",
        "P1-D",
        "Macro-Mission 05",
    ):
        assert token in checkpoint
    assert "IA_CORE_OS_IS_A_DISTINCT_AI_NATIVE_OPERATING_SYSTEM_BUILT_ON_LINUX" in os_doc
    assert "SECURITY_BY_DESIGN_NOT_SECURITY_AS_AN_ADD_ON" in security
    assert "NEXT_SELECTED_NOT_STARTED" in p1
    assert "P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED" in p1


def test_gokv_remains_valid_without_vault_writes_or_promotion():
    validation = validate_vault(default_paths(ROOT))
    assert validation == {
        "valid": True,
        "schema_version": "gokv.knowledge_item.v1",
        "registry_schema_version": "gokv.registry.v1",
        "item_count": 38,
        "status_counts": {"VALIDATED": 9, "CANDIDATE": 22, "PROMOTED": 7},
    }
    changed = changed_files()
    assert "knowledge/global_operational/registry.json" not in changed
    assert not {path for path in changed if path.startswith("knowledge/global_operational/items/")}
    assert not {path for path in changed if path.startswith("knowledge/global_operational/events/")}
    assert not {path for path in changed if path.startswith("knowledge/global_operational/packs/")}


def test_json_census_and_protected_diff_are_deterministic():
    checkpoint = "6dd040e0985da134f18f2bc85a338aa1bf770d3f"
    tracked = [line for line in subprocess.check_output(["git", "ls-tree", "-r", "--name-only", checkpoint], cwd=ROOT, text=True).splitlines() if line.endswith(".json")]
    new_json = {
        "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT_EVIDENCE.json",
        "knowledge/global_operational/metrics/roadmap_4_x_macro_04_2_execution_metric.json",
    }
    census = set(tracked) | {path for path in new_json if (ROOT / path).is_file()}
    assert len(census) == 258 + 2
    for relative in census:
        json.loads((ROOT / relative).read_text(encoding="utf-8"))
    changed = changed_files()
    assert changed <= ALLOWED_FILES
    assert not [path for path in changed if path.startswith(PROTECTED_PREFIXES)]
    assert "ui/web/index.html" not in changed
    assert "api.py" not in changed
