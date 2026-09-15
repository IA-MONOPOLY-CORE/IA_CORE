from __future__ import annotations

import subprocess
from pathlib import Path

from gokv.kernel import load_kernel_graph
from gokv.storage import default_paths, validate_vault


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "5bde1c10acfd98d436f961e91661a104c7667593"
GRAPH = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json"
CHECKPOINT = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_CHECKPOINT_EVIDENCE.json"
OCI = ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_OCI_NECESSARY_AND_SUFFICIENT_INHERITANCE.md"
P1_PLAN = ROOT / "docs" / "ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md"
FOUNDRY = ROOT / "docs" / "FUTURE_IA_CORE_ENTERPRISE_FOUNDRY_AND_AGENT_LINEAGE.md"

REQUIRED_FILES = {
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
    "docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
    "docs/FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_NATIVE_G0_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_SECURITY_INGESTION_CONTRACT.md",
    "docs/ROADMAP_4X_MACRO_04_2_TRUTH_MATRIX.md",
    "docs/ROADMAP_4X_MACRO_04_2_EXECUTION_METRICS_BASELINE.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT.md",
    "docs/ROADMAP_4X_MACRO_04_2_CHECKPOINT_EVIDENCE.json",
    "docs/ROADMAP_4X_MACRO_04_2_COMMIT_ACCOUNTABILITY_LEDGER.md",
    "knowledge/global_operational/metrics/roadmap_4_x_macro_04_2_execution_metric.json",
    "tests/test_gokv_cognitive_kernel_0_2.py",
    "tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py",
}

PROTECTED_PREFIXES = (
    "api.py",
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


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _changed_from_baseline() -> set[str]:
    committed = {
        path.replace("\\", "/")
        for path in subprocess.check_output(
            ["git", "diff", "--name-only", f"{BASELINE}..HEAD"], cwd=ROOT, text=True
        ).splitlines()
        if path.strip()
    }
    working = {
        path.replace("\\", "/")
        for path in subprocess.check_output(
            ["git", "ls-files", "--others", "--modified", "--exclude-standard"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        if path.strip()
    }
    return committed | working


def test_required_artifacts_and_graph_contract_exist():
    for relative in REQUIRED_FILES:
        assert (ROOT / relative).is_file(), relative
    graph = load_kernel_graph(GRAPH)
    assert len(graph["nodes"]) == 13
    assert len(graph["edges"]) == 10
    assert graph["kernel_mode"] == "INERT_DEVELOPMENT_FOUNDATION"
    assert "KERNEL" not in {family["family_id"] for family in graph["families"]}


def test_active_inheritance_literal_is_migrated_without_rewriting_history():
    active = _text(OCI)
    assert "NECESSARY_AND_SUFFICIENT_INHERITANCE" in active
    assert "MINIMUM_SUFFICIENT_INHERITANCE" not in active
    assert "closed" in active and "evidence" in active
    assert "P1-A_PLATFORM_STATUS_HEALTH_SELECTED_NOT_STARTED" in _text(P1_PLAN)
    assert "NEXT_SELECTED_NOT_STARTED" in _text(P1_PLAN)


def test_owner_native_domain_parity_and_no_activation_are_explicit():
    foundry = _text(FOUNDRY)
    parity = _text(ROOT / "docs" / "ROADMAP_4X_MACRO_04_1_DOMAIN_MODULE_PARITY_AUDIT.md")
    checkpoint = _text(CHECKPOINT)
    evidence = _text(EVIDENCE)
    for token in ("OWNER_NATIVE", "OWNER_CREATED", "AGENT_FOUNDED_UNDER_OWNER_CHARTER", "tenant isolation"):
        assert token in foundry
    for token in ("legacy singled-out domain status", "domain_module_status", "NO_DOMAIN_MODULE_HAS_INHERENT_PRIVILEGED_OR_FEATURED_STATUS"):
        assert token in parity
    for token in ("P1-A", "P1-B", "P1-C", "P1-D", "Enterprise Foundry", "Macro-Mission 05", "No runtime OCI"):
        assert token in checkpoint
    assert '"routes_modified": false' in evidence


def test_current_gokv_vault_remains_valid_and_unmodified():
    validation = validate_vault(default_paths(ROOT))
    assert validation["valid"] is True
    assert validation["item_count"] == 38
    changed = _changed_from_baseline()
    assert not {path for path in changed if path.startswith("knowledge/global_operational/items/")}
    assert "knowledge/global_operational/registry.json" not in changed


def test_macro_04_1_change_set_is_scoped_and_p1_is_untouched():
    changed = _changed_from_baseline()
    assert changed
    assert changed <= REQUIRED_FILES | {
        "tests/historical_test_context.py",
        "tests/test_roadmap_4x_macro_03_checkpoint.py",
        "tests/test_roadmap_4x_macro_01_1_p4_live_closure.py",
        "tests/test_roadmap_3_x_macro_05_1_live_state_consistency.py",
        "tests/test_roadmap_4x_macro_04_p1_entry_review.py",
        "tests/test_roadmap_3_x_macro_04_true_completion.py",
        "tests/test_roadmap_3_x_macro_05_final_closure.py",
    }
    assert not [path for path in changed if path.startswith(PROTECTED_PREFIXES)]
    assert "api.py" not in changed
    assert not {path for path in changed if path.startswith("knowledge/global_operational/items/")}
