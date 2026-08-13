import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import materialize_agent_presets
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.domain_materialization_rollback import (
    compare_sandbox_domain_materializations,
    regenerate_sandbox_domain_after_integral_rollback,
    validate_sandbox_domain_safe_regeneration_result,
)
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog
from core.sandbox_agent_materializer import materialize_sandbox_agent
from core.sandbox_team_materializer import materialize_sandbox_team, validate_materialized_sandbox_team
from core.sandbox_team_read_model import get_sandbox_team_summary, list_sandbox_teams
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
    _capabilities,
    _coordination,
    _full_chain,
    _preview,
    _schema_from_preview,
    _tree_hash,
)


CHECKPOINT_DOC = ROOT / "docs" / "SANDBOX_SAFE_REGENERATION_6_2.md"


def _extend_chain_from_domain(domain: dict) -> dict:
    domain_dir = Path(domain["domain_dir"])
    materialize_profile_catalog(domain_dir)
    presets = materialize_agent_presets(domain_dir)
    materialize_paper_seed(domain_dir)
    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    agents = [
        materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
        for preset in presets_payload["presets"]
    ]
    agent_ids = [agent["agent_id"] for agent in agents]
    team = materialize_sandbox_team(
        domain_dir,
        team_id="safe_regeneration_team_6_2",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )
    return {
        "domain": domain,
        "domain_dir": domain_dir,
        "agents": agents,
        "team": team,
        "artifact_manifest": validate_artifact_manifest_file(team["artifact_manifest_path"]),
    }


def _snapshot(chain: dict) -> dict:
    domain = chain["domain"]
    domain_dir = Path(domain["domain_dir"])
    manifest = validate_artifact_manifest_file(chain["team"]["artifact_manifest_path"])
    materialization_manifest = json.loads(Path(domain["manifest_path"]).read_text(encoding="utf-8"))
    listing = list_sandbox_teams(domain_dir)
    summary = get_sandbox_team_summary(domain_dir, team_id=chain["team"]["team_id"])
    validation = validate_materialized_sandbox_team(domain_dir, team_id=chain["team"]["team_id"])
    artifact_kinds = [
        artifact.get("created_from", {}).get("artifact_kind", artifact["artifact_type"])
        for artifact in manifest["artifacts"]
    ]
    non_operational_flags = {
        "manifest_operational": [artifact.get("operational") for artifact in manifest["artifacts"]],
        "manifest_passed": [artifact.get("passed") for artifact in manifest["artifacts"]],
        "team_runtime_enabled": validation["team"]["metadata"]["runtime_enabled"],
        "team_execution_enabled": validation["team"]["metadata"]["execution_enabled"],
        "read_model_operational": listing["operational"],
        "read_model_passed": listing["passed"],
        "tool_execution_enabled": summary["execution_policy_summary"]["tool_execution_enabled"],
        "model_invocation_enabled": summary["execution_policy_summary"]["model_invocation_enabled"],
        "external_integrations_enabled": summary["execution_policy_summary"]["external_integrations_enabled"],
    }
    return {
        "domain_id": domain["domain_id"],
        "materialization_id": domain["materialization_id"],
        "previous_materialization_id": materialization_manifest.get("previous_materialization_id"),
        "artifact_count": len(manifest["artifacts"]),
        "artifact_types": [artifact["artifact_type"] for artifact in manifest["artifacts"]],
        "artifact_kinds": artifact_kinds,
        "dependencies": [artifact["dependencies"] for artifact in manifest["artifacts"]],
        "read_model_shape": sorted(summary.keys()),
        "non_operational_flags": non_operational_flags,
        "artifact_ids": [artifact["artifact_id"] for artifact in manifest["artifacts"]],
        "created_paths": list(materialization_manifest["created_paths"]),
        "team_id": chain["team"]["team_id"],
    }


def _temporal_state() -> dict[str, bool]:
    return {
        ".tmp": (ROOT / ".tmp").exists(),
        "test_agent": (MEMORY / "test_agent").exists(),
        "test_agent_context": (MEMORY / "test_agent_context").exists(),
    }


def test_safe_regeneration_rebuilds_full_chain_after_integral_rollback(tmp_path):
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_temporals = _temporal_state()

    first_chain = _full_chain(tmp_path)
    first_snapshot = _snapshot(first_chain)
    first_domain_dir = first_chain["domain_dir"]
    schema = _schema_from_preview(_preview())

    regeneration = regenerate_sandbox_domain_after_integral_rollback(
        schema,
        manifest_path=first_chain["domain"]["manifest_path"],
        sandbox_root=first_chain["sandbox_root"],
    )
    assert regeneration["first_materialization_id"] == first_snapshot["materialization_id"]
    assert regeneration["regenerated_materialization_id"] != first_snapshot["materialization_id"]
    assert regeneration["rollback"]["status"] == "rolled_back_integral"
    assert regeneration["validation"]["post_rollback_clean"] is True
    assert Path(regeneration["materialization"]["domain_dir"]).is_dir()
    assert Path(regeneration["materialization"]["domain_dir"]) == first_domain_dir

    regenerated_chain = _extend_chain_from_domain(regeneration["materialization"])
    regenerated_snapshot = _snapshot(regenerated_chain)
    comparison = compare_sandbox_domain_materializations(
        first_snapshot,
        regenerated_snapshot,
        regeneration_result=regeneration,
    )
    validated = validate_sandbox_domain_safe_regeneration_result(comparison)

    assert validated["structural_match"] is True
    assert validated["lineage_preserved"] is True
    assert validated["new_materialization_created"] is True
    assert validated["residual_paths_detected"] == []
    assert validated["duplicate_artifacts_detected"] == []
    assert regenerated_snapshot["domain_id"] == first_snapshot["domain_id"]
    assert regenerated_snapshot["artifact_types"] == first_snapshot["artifact_types"]
    assert regenerated_snapshot["artifact_kinds"] == first_snapshot["artifact_kinds"]
    assert regenerated_snapshot["artifact_count"] == first_snapshot["artifact_count"]
    assert regenerated_snapshot["previous_materialization_id"] == first_snapshot["materialization_id"]
    assert regenerated_snapshot["materialization_id"] != first_snapshot["materialization_id"]

    for value in regenerated_snapshot["non_operational_flags"]["manifest_operational"]:
        assert value is False
    for value in regenerated_snapshot["non_operational_flags"]["manifest_passed"]:
        assert value is False
    assert regenerated_snapshot["non_operational_flags"]["team_runtime_enabled"] is False
    assert regenerated_snapshot["non_operational_flags"]["team_execution_enabled"] is False
    assert regenerated_snapshot["non_operational_flags"]["read_model_operational"] is False
    assert regenerated_snapshot["non_operational_flags"]["read_model_passed"] is False
    assert regenerated_snapshot["non_operational_flags"]["tool_execution_enabled"] is False
    assert regenerated_snapshot["non_operational_flags"]["model_invocation_enabled"] is False
    assert regenerated_snapshot["non_operational_flags"]["external_integrations_enabled"] is False

    dumped = json.dumps(validated, ensure_ascii=False, sort_keys=True).lower()
    for forbidden in ("api_key", "secret", "token", "password", "runtime_handle", "model_config", "tool_config"):
        assert forbidden not in dumped
    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    assert _temporal_state() == before_temporals


def test_second_materialization_without_rollback_is_blocked_to_avoid_duplicates(tmp_path):
    first_chain = _full_chain(tmp_path)
    schema = _schema_from_preview(_preview())

    with pytest.raises((FileExistsError, ValueError), match="Ya existe sandbox materializado|dominio equivalente"):
        materialize_sandbox_domain(schema, sandbox_root=first_chain["sandbox_root"])


def test_safe_regeneration_with_incomplete_rollback_fails_controlled(tmp_path):
    sandbox_root = tmp_path / "sandboxes"
    schema = _schema_from_preview(_preview())
    domain = materialize_sandbox_domain(schema, sandbox_root=sandbox_root)

    with pytest.raises(FileNotFoundError, match="artifact_manifest"):
        regenerate_sandbox_domain_after_integral_rollback(
            schema,
            manifest_path=domain["manifest_path"],
            sandbox_root=sandbox_root,
        )


def test_safe_regeneration_with_inconsistent_manifest_fails_controlled(tmp_path):
    first_chain = _full_chain(tmp_path)
    artifact_manifest_path = Path(first_chain["team"]["artifact_manifest_path"])
    artifact_manifest = json.loads(artifact_manifest_path.read_text(encoding="utf-8"))
    artifact_manifest["domain_id"] = "other_domain"
    artifact_manifest_path.write_text(
        json.dumps(artifact_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="domain_id"):
        regenerate_sandbox_domain_after_integral_rollback(
            _schema_from_preview(_preview()),
            manifest_path=first_chain["domain"]["manifest_path"],
            sandbox_root=first_chain["sandbox_root"],
        )


def test_safe_regeneration_with_undeclared_residual_fails_controlled(tmp_path):
    first_chain = _full_chain(tmp_path)
    residual = first_chain["domain_dir"] / "undeclared_residual.txt"
    residual.write_text("residue\n", encoding="utf-8")

    with pytest.raises(ValueError, match="residual_paths_detected"):
        regenerate_sandbox_domain_after_integral_rollback(
            _schema_from_preview(_preview()),
            manifest_path=first_chain["domain"]["manifest_path"],
            sandbox_root=first_chain["sandbox_root"],
        )
    assert residual.exists()


def test_compare_safe_regeneration_detects_duplicates_and_operational_flags(tmp_path):
    first_chain = _full_chain(tmp_path)
    first_snapshot = _snapshot(first_chain)
    regenerated_snapshot = dict(first_snapshot)
    regenerated_snapshot["previous_materialization_id"] = first_snapshot["materialization_id"]
    regenerated_snapshot["materialization_id"] = f"{first_snapshot['materialization_id']}_new"
    regenerated_snapshot["artifact_ids"] = [
        *first_snapshot["artifact_ids"],
        first_snapshot["artifact_ids"][0],
    ]

    with pytest.raises(ValueError, match="duplicate_artifacts_detected"):
        compare_sandbox_domain_materializations(first_snapshot, regenerated_snapshot)

    regenerated_snapshot = dict(first_snapshot)
    regenerated_snapshot["previous_materialization_id"] = first_snapshot["materialization_id"]
    regenerated_snapshot["materialization_id"] = f"{first_snapshot['materialization_id']}_new"
    regenerated_snapshot["non_operational_flags"] = dict(first_snapshot["non_operational_flags"])
    regenerated_snapshot["non_operational_flags"]["team_runtime_enabled"] = True

    with pytest.raises(ValueError, match="structural_match"):
        compare_sandbox_domain_materializations(first_snapshot, regenerated_snapshot)


def test_prompt_6_2_checkpoint_documentation_and_plans_are_consistent():
    for path in (CHECKPOINT_DOC, PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK):
        assert path.exists()

    checkpoint = CHECKPOINT_DOC.read_text(encoding="utf-8")
    for token in (
        "SANDBOX_SAFE_REGENERATION_PASSED",
        "SANDBOX_REGENERATION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_6_3_materialization_audit_pack",
        "PROMPT 6.3 - Audit pack y trazabilidad de materializacion sandbox",
        "materializar -> rollback integral -> regenerar",
        "artifact_manifest",
        "created_paths",
        "structural_match=true",
        "operational=false",
        "runtime_enabled=false",
        "execution_enabled=false",
    ):
        assert token in checkpoint

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "PROMPT 6.2",
        "SANDBOX_SAFE_REGENERATION_PASSED",
        "SANDBOX_REGENERATION_NO_OPERATIONAL_CONFIRMED",
        "ready_for_phase_6_3_materialization_audit_pack",
        "PROMPT 6.3 - Audit pack y trazabilidad de materializacion sandbox",
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
