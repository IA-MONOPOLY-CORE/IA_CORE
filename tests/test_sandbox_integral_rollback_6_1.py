import hashlib
import json
from pathlib import Path

import pytest

from core.agent_preset_materializer import materialize_agent_presets
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.domain_materialization_preview import build_domain_materialization_preview
from core.domain_materialization_rollback import (
    build_sandbox_domain_integral_rollback_plan,
    rollback_sandbox_domain_integral,
    validate_sandbox_domain_integral_rollback_plan,
    validate_sandbox_domain_integral_rollback_result,
)
from core.domain_materializer import materialize_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog
from core.sandbox_agent_materializer import materialize_sandbox_agent
from core.sandbox_agent_tool_contract import build_tool_contract
from core.sandbox_domain_schema import validate_sandbox_domain_schema
from core.sandbox_team_materializer import materialize_sandbox_team
from core.sandbox_team_read_model import list_sandbox_teams


ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "domains"
AGENTS = ROOT / "agents"
CATALOGS = ROOT / "catalogs"
MEMORY = ROOT / "memoria_agentes"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"
CHECKPOINT_DOC = ROOT / "docs" / "SANDBOX_INTEGRAL_ROLLBACK_6_1.md"
PHASE_6_PLAN = ROOT / "docs" / "BACKEND_INTERNAL_PHASE_6_SANDBOX_E2E_ROLLBACK_REGENERATION_BLOCK_PLAN.md"
NEXT_ARCH = ROOT / "docs" / "NEXT_ARCHITECTURE_BLOCK_PLAN.md"
NEXT_OPERATIONAL = ROOT / "docs" / "NEXT_OPERATIONAL_BLOCK_PLAN.md"
BOOK = ROOT / "docs" / "BACKEND_INTERNAL_BOOK_DESIGN.md"


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _preview() -> dict:
    return build_domain_materialization_preview(
        domain_id="sandbox_marketing_crm_automation",
        area_id="marketing_publicidad",
        niche_ids=["contenidos_redes"],
        business_scale="pyme",
        objective="sandbox integral rollback checkpoint 6.1",
        complexity_level="media",
        max_profiles=2,
        max_presets=2,
    )


def _schema_from_preview(preview: dict) -> dict:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    schema["source_request"] = preview["domain_request"]
    schema["created_from"] = {
        "type": "preview",
        "preview_id": preview["preview_id"],
        "artifact_state": preview["artifact_state"],
    }
    return validate_sandbox_domain_schema(schema)


def _coordination(agent_ids: list[str]) -> dict:
    return {
        "coordination_type": "single_coordinator",
        "coordinator_agent_id": agent_ids[0],
        "declared_only": True,
        "runtime_enabled": False,
        "execution_enabled": False,
        "rules": ["Rollback integral declarativo; no ejecuta coordinacion."],
        "suggested_order": list(agent_ids),
        "restrictions": ["Sin runtime.", "Sin pipeline ejecutable."],
    }


def _capabilities(domain_id: str, owner_agent_id: str) -> dict:
    tool = build_tool_contract(
        tool_id="tool_sandbox_integral_rollback_declared",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        tool_name="Future Sandbox Integral Rollback Tool",
        tool_category="internal_future",
        created_at="2026-07-15T00:00:00",
        updated_at="2026-07-15T00:00:00",
    )
    return {
        "memory": [],
        "tools": [tool],
        "policies": [
            {
                "policy_id": "policy_sandbox_integral_rollback_declared",
                "status": "declared",
                "declared_only": True,
                "runtime_enabled": False,
                "execution_enabled": False,
                "external_access": False,
            }
        ],
    }


def _full_chain(tmp_path) -> dict:
    sandbox_root = tmp_path / "sandboxes"
    domain = materialize_sandbox_domain(_schema_from_preview(_preview()), sandbox_root=sandbox_root)
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
        team_id="integral_rollback_team_6_1",
        agent_ids=agent_ids,
        coordination_model=_coordination(agent_ids),
        capabilities=_capabilities(domain["domain_id"], agent_ids[0]),
    )
    artifact_manifest = validate_artifact_manifest_file(team["artifact_manifest_path"])
    return {
        "sandbox_root": sandbox_root,
        "domain": domain,
        "domain_dir": domain_dir,
        "agents": agents,
        "team": team,
        "artifact_manifest": artifact_manifest,
    }


def _write_json(path: str | Path, payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _temporal_state() -> dict[str, bool]:
    return {
        ".tmp": (ROOT / ".tmp").exists(),
        "test_agent": (MEMORY / "test_agent").exists(),
        "test_agent_context": (MEMORY / "test_agent_context").exists(),
    }


def _assert_temporal_state_unchanged(before: dict[str, bool]) -> None:
    assert _temporal_state() == before


def test_integral_rollback_removes_full_sandbox_chain_and_is_idempotent(tmp_path):
    before_temporals = _temporal_state()
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    chain = _full_chain(tmp_path)
    sandbox_root = chain["sandbox_root"]
    domain = chain["domain"]
    domain_dir = chain["domain_dir"]
    sentinel = sandbox_root / "preserved_outside_domain.txt"
    sentinel.write_text("preserve me\n", encoding="utf-8")

    plan = build_sandbox_domain_integral_rollback_plan(
        manifest_path=domain["manifest_path"],
        sandbox_root=sandbox_root,
    )
    validated_plan = validate_sandbox_domain_integral_rollback_plan(plan)

    assert validated_plan["rollback_scope"] == "sandbox_domain_integral"
    assert validated_plan["domain_id"] == domain["domain_id"]
    assert validated_plan["materialization_id"] == domain["materialization_id"]
    assert validated_plan["operational"] is False
    assert validated_plan["runtime_enabled"] is False
    assert validated_plan["execution_enabled"] is False
    assert validated_plan["blocked_paths"] == []
    assert any(path.endswith("artifact_manifest.json") for path in validated_plan["planned_paths"])
    assert any(path.endswith("sandbox_teams") or "sandbox_teams" in path for path in validated_plan["planned_paths"])
    assert str(sentinel.resolve()) not in validated_plan["planned_paths"]

    root = sandbox_root.resolve()
    forbidden_parts = {"core", "docs", "tests", ".git"}
    for raw_path in validated_plan["planned_paths"]:
        path = Path(raw_path).resolve()
        assert path == root or root in path.parents
        assert DOMAINS.resolve() not in [path, *path.parents]
        assert ROOT.resolve() not in [path, *path.parents]
        assert not (set(path.parts) & forbidden_parts)

    first = rollback_sandbox_domain_integral(
        manifest_path=domain["manifest_path"],
        sandbox_root=sandbox_root,
    )
    validated_result = validate_sandbox_domain_integral_rollback_result(first)

    assert validated_result["status"] == "rolled_back_integral"
    assert validated_result["success"] is True
    assert validated_result["removed_paths"]
    assert validated_result["blocked_paths"] == []
    assert Path(validated_result["rollback_record_path"]).is_file()
    assert not domain_dir.exists()
    assert sentinel.exists()
    assert list_sandbox_teams(domain_dir)["teams_count"] == 0

    second = rollback_sandbox_domain_integral(
        manifest_path=domain["manifest_path"],
        sandbox_root=sandbox_root,
    )
    assert second["status"] == "already_rolled_back_integral"
    assert second["idempotent"] is True
    assert second["removed_paths"] == []
    assert second["skipped_paths"]
    assert sentinel.exists()

    dumped = json.dumps(second, ensure_ascii=False, sort_keys=True).lower()
    for forbidden in ("api_key", "secret", "token", "password", "runtime_handle", "model_config", "tool_config"):
        assert forbidden not in dumped

    assert _tree_hash(DOMAINS) == before_domains
    assert _tree_hash(AGENTS) == before_agents
    assert _tree_hash(CATALOGS) == before_catalogs
    _assert_temporal_state_unchanged(before_temporals)


def test_integral_rollback_blocks_path_traversal_and_operational_paths(tmp_path):
    chain = _full_chain(tmp_path)
    manifest_path = Path(chain["domain"]["manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["created_paths"].append(str((chain["sandbox_root"] / ".." / "escape.txt")))
    _write_json(manifest_path, manifest)

    with pytest.raises(ValueError, match="fuera del sandbox"):
        build_sandbox_domain_integral_rollback_plan(
            manifest_path=manifest_path,
            sandbox_root=chain["sandbox_root"],
        )

    manifest["created_paths"] = [str(DOMAINS / "loteria")]
    _write_json(manifest_path, manifest)
    with pytest.raises(ValueError, match="fuera del sandbox|domains/ operativo"):
        build_sandbox_domain_integral_rollback_plan(
            manifest_path=manifest_path,
            sandbox_root=chain["sandbox_root"],
        )


def test_integral_rollback_blocks_manifest_inconsistency_and_missing_manifest(tmp_path):
    chain = _full_chain(tmp_path)
    artifact_manifest_path = Path(chain["team"]["artifact_manifest_path"])
    artifact_manifest = json.loads(artifact_manifest_path.read_text(encoding="utf-8"))
    artifact_manifest["domain_id"] = "other_domain"
    _write_json(artifact_manifest_path, artifact_manifest)

    with pytest.raises(ValueError, match="domain_id"):
        build_sandbox_domain_integral_rollback_plan(
            manifest_path=chain["domain"]["manifest_path"],
            sandbox_root=chain["sandbox_root"],
        )

    artifact_manifest_path.unlink()
    with pytest.raises(FileNotFoundError, match="artifact_manifest"):
        build_sandbox_domain_integral_rollback_plan(
            manifest_path=chain["domain"]["manifest_path"],
            sandbox_root=chain["sandbox_root"],
        )


def test_integral_rollback_blocks_empty_created_paths_and_undeclared_preserved_files(tmp_path):
    chain = _full_chain(tmp_path)
    sandbox_root = chain["sandbox_root"]
    sentinel = sandbox_root / "undeclared_file.txt"
    sentinel.write_text("not declared\n", encoding="utf-8")
    manifest_path = Path(chain["domain"]["manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["created_paths"] = []
    _write_json(manifest_path, manifest)

    with pytest.raises(ValueError, match="created_paths"):
        build_sandbox_domain_integral_rollback_plan(
            manifest_path=manifest_path,
            sandbox_root=sandbox_root,
        )
    assert sentinel.exists()


def test_integral_rollback_blocks_symlink_escape_when_supported(tmp_path):
    chain = _full_chain(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("outside\n", encoding="utf-8")
    link = chain["domain_dir"] / "escape_link.txt"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink no disponible en este entorno: {exc}")
    manifest_path = Path(chain["domain"]["manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["created_paths"].append(str(link))
    _write_json(manifest_path, manifest)

    with pytest.raises(ValueError, match="fuera del sandbox"):
        build_sandbox_domain_integral_rollback_plan(
            manifest_path=manifest_path,
            sandbox_root=chain["sandbox_root"],
        )
    assert outside.exists()


def test_prompt_6_1_checkpoint_documentation_and_plans_are_consistent():
    for path in (CHECKPOINT_DOC, PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK):
        assert path.exists()

    checkpoint = CHECKPOINT_DOC.read_text(encoding="utf-8")
    for token in (
        "SANDBOX_INTEGRAL_ROLLBACK_PASSED",
        "SANDBOX_ROLLBACK_IDEMPOTENT_CONFIRMED",
        "ready_for_phase_6_2_safe_regeneration",
        "PROMPT 6.2 - Regeneracion segura sandbox completa",
        "artifact_manifest",
        "created_paths",
        "rollback plan",
        "operational=false",
        "runtime_enabled=false",
        "execution_enabled=false",
    ):
        assert token in checkpoint

    combined = "\n".join(path.read_text(encoding="utf-8") for path in (PHASE_6_PLAN, NEXT_ARCH, NEXT_OPERATIONAL, BOOK))
    for token in (
        "PROMPT 6.1",
        "SANDBOX_INTEGRAL_ROLLBACK_PASSED",
        "SANDBOX_ROLLBACK_IDEMPOTENT_CONFIRMED",
        "ready_for_phase_6_2_safe_regeneration",
        "PROMPT 6.2 - Regeneracion segura sandbox completa",
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
