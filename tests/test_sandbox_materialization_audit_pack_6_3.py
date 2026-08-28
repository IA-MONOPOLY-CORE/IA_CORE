import json
from copy import deepcopy

import pytest

from core.sandbox_materialization_audit_pack import (
    AUDIT_PACK_READINESS,
    AUDIT_PACK_SCOPE,
    build_sandbox_materialization_audit_pack,
    summarize_sandbox_materialization_audit_pack,
    validate_sandbox_materialization_audit_pack,
)
from tests.test_sandbox_integral_rollback_6_1 import (
    AGENTS,
    BOOK,
    CATALOGS,
    DOMAINS,
    MEMORY,
    NEXT_ARCH,
    NEXT_OPERATIONAL,
    PHASE_6_PLAN,
    ROOT,
    _full_chain,
    _preview,
    _schema_from_preview,
    _tree_hash,
)
from tests.test_sandbox_safe_regeneration_6_2 import (
    _extend_chain_from_domain,
    _snapshot,
)
from core.domain_materialization_rollback import (
    compare_sandbox_domain_materializations,
    regenerate_sandbox_domain_after_integral_rollback,
)


CHECKPOINT_DOC = ROOT / "docs" / "SANDBOX_MATERIALIZATION_AUDIT_PACK_6_3.md"
ADR = ROOT / "ARCHITECTURE_DECISIONS.md"
AUDIT_PACK_MODULE = ROOT / "core" / "sandbox_materialization_audit_pack.py"


FORBIDDEN_NEW_OPERATIONAL_MODULES = (
    "core/sandbox_audit_pack_runner.py",
    "core/sandbox_execution_runner.py",
    "core/sandbox_runtime_runner.py",
    "core/team_runtime_executor.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_dispatcher.py",
    "core/runtime_event_bus.py",
    "core/tool_execution_runtime.py",
    "core/model_invocation_runtime.py",
    "core/context_injection_runtime.py",
    "core/output_delivery_runtime.py",
    "core/ui_runtime.py",
    "core/integration_runtime.py",
)


def _temporal_state() -> dict[str, bool]:
    return {
        ".tmp": (ROOT / ".tmp").exists(),
        "test_agent": (MEMORY / "test_agent").exists(),
        "test_agent_context": (MEMORY / "test_agent_context").exists(),
    }


def _audit_pack_cycle(tmp_path) -> dict:
    first_chain = _full_chain(tmp_path)
    first_snapshot = _snapshot(first_chain)
    regeneration = regenerate_sandbox_domain_after_integral_rollback(
        _schema_from_preview(_preview()),
        manifest_path=first_chain["domain"]["manifest_path"],
        sandbox_root=first_chain["sandbox_root"],
    )
    regenerated_chain = _extend_chain_from_domain(regeneration["materialization"])
    regenerated_snapshot = _snapshot(regenerated_chain)
    comparison = compare_sandbox_domain_materializations(
        first_snapshot,
        regenerated_snapshot,
        regeneration_result=regeneration,
    )
    pack = build_sandbox_materialization_audit_pack(
        first_snapshot=first_snapshot,
        rollback_report=regeneration["rollback"],
        regeneration_report=regeneration,
        structural_comparison=comparison,
    )
    return {
        "first_snapshot": first_snapshot,
        "regeneration": regeneration,
        "comparison": comparison,
        "pack": pack,
    }


def test_audit_pack_builds_from_full_sandbox_cycle_and_is_json_safe(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_temporals = _temporal_state()

    cycle = _audit_pack_cycle(tmp_path)
    pack = validate_sandbox_materialization_audit_pack(cycle["pack"])
    summary = summarize_sandbox_materialization_audit_pack(pack)

    assert pack["audit_pack_id"]
    assert pack["domain_id"] == cycle["first_snapshot"]["domain_id"]
    assert pack["audit_scope"] == AUDIT_PACK_SCOPE
    assert pack["readiness"] == AUDIT_PACK_READINESS
    for section in (
        "first_materialization",
        "end_to_end_checkpoint",
        "rollback",
        "regeneration",
        "structural_comparison",
        "artifact_manifest_summary",
        "lineage_summary",
        "created_paths_summary",
        "read_models_summary",
        "non_operational_summary",
        "blocked_capabilities",
    ):
        assert section in pack
        assert pack[section]

    assert pack["first_materialization"]["artifact_count"] == cycle["first_snapshot"]["artifact_count"]
    assert pack["end_to_end_checkpoint"]["verdict"] == "SANDBOX_CHAIN_NO_OPERATIONAL_CONFIRMED"
    assert pack["rollback"]["idempotent"] is True
    assert pack["rollback"]["removed_paths_count"] > 0
    assert pack["regeneration"]["lineage_preserved"] is True
    assert pack["regeneration"]["duplicate_artifacts_detected"] == []
    assert pack["regeneration"]["residual_paths_detected"] == []
    assert pack["structural_comparison"]["structural_match"] is True
    assert pack["artifact_manifest_summary"]["artifact_manifest_valid"] is True
    assert pack["lineage_summary"]["previous_materialization_id_preserved"] is True
    assert pack["created_paths_summary"]["absolute_paths_included"] is False
    assert pack["read_models_summary"]["read_model_validated"] is True
    assert pack["non_operational_summary"]["all_blocked"] is True

    assert pack["operational"] is False
    assert pack["passed"] is False
    assert pack["runtime_enabled"] is False
    assert pack["execution_enabled"] is False
    assert pack["tool_execution_enabled"] is False
    assert pack["model_invocation_enabled"] is False
    assert pack["external_integrations_enabled"] is False
    assert all(value is False for value in pack["blocked_capabilities"].values())
    assert summary["structural_match"] is True
    assert summary["lineage_preserved"] is True

    dumped = json.dumps(pack, ensure_ascii=False, sort_keys=True).lower()
    for forbidden in (
        "api_key",
        "access_token",
        "password",
        "secret",
        "runtime_handle",
        "model_config",
        "tool_config",
        "productive_data",
    ):
        assert forbidden not in dumped

    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _temporal_state() == before_temporals


@pytest.mark.parametrize(
    "mutator,match",
    [
        (lambda pack: pack.__setitem__("operational", True), "operational"),
        (lambda pack: pack.__setitem__("runtime_enabled", True), "runtime_enabled"),
        (lambda pack: pack.__setitem__("execution_enabled", True), "execution_enabled"),
        (lambda pack: pack.__setitem__("api_secret", "nope"), "sensible"),
        (lambda pack: pack.pop("rollback"), "rollback"),
        (lambda pack: pack.pop("regeneration"), "regeneration"),
        (lambda pack: pack["structural_comparison"].__setitem__("structural_match", False), "structural_match"),
        (lambda pack: pack["regeneration"].__setitem__("lineage_preserved", False), "lineage_preserved"),
    ],
)
def test_invalid_audit_pack_fails_controlled(tmp_path, mutator, match):
    pack = deepcopy(_audit_pack_cycle(tmp_path)["pack"])
    mutator(pack)

    with pytest.raises(ValueError, match=match):
        validate_sandbox_materialization_audit_pack(pack)


def test_audit_pack_rejects_duplicate_artifacts_and_residual_paths(tmp_path):
    base_pack = _audit_pack_cycle(tmp_path)["pack"]
    pack = deepcopy(base_pack)
    pack["regeneration"]["duplicate_artifacts_detected"] = ["artifact_duplicate"]
    with pytest.raises(ValueError, match="duplicate_artifacts_detected"):
        validate_sandbox_materialization_audit_pack(pack)

    pack = deepcopy(base_pack)
    pack["regeneration"]["residual_paths_detected"] = ["residual.txt"]
    with pytest.raises(ValueError, match="residual_paths_detected"):
        validate_sandbox_materialization_audit_pack(pack)


def test_prompt_6_3_documentation_and_plans_are_consistent():
    for path in (CHECKPOINT_DOC, PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK, ADR, AUDIT_PACK_MODULE):
        assert path.exists()

    checkpoint = CHECKPOINT_DOC.read_text(encoding="utf-8")
    for token in (
        "SANDBOX_MATERIALIZATION_AUDIT_PACK_READY",
        "SANDBOX_AUDIT_PACK_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_6_4_integral_checkpoint",
        "PROMPT 6.4 - Checkpoint integral Fase 6",
        "artifact_manifest",
        "created_paths",
        "lineage",
        "JSON-safe",
        "operational=false",
        "runtime_enabled=false",
        "execution_enabled=false",
    ):
        assert token in checkpoint

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "PROMPT 6.3",
        "SANDBOX_MATERIALIZATION_AUDIT_PACK_READY",
        "SANDBOX_AUDIT_PACK_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_6_4_integral_checkpoint",
        "PROMPT 6.4 - Checkpoint integral Fase 6",
        "runtime",
        "execution",
        "dry-run real",
        "tools",
        "modelos",
        "UI",
        "integraciones",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
        "OBLITERATUS",
    ):
        assert token in combined

    assert "ADR-049" in ADR.read_text(encoding="utf-8")


def test_prompt_6_3_does_not_create_operational_modules_or_temporals():
    for relative in FORBIDDEN_NEW_OPERATIONAL_MODULES:
        assert not (ROOT / relative).exists(), relative
