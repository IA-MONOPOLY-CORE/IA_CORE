import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.active_contract import evaluate_active_contract
from core.active_executor import execute_active
from core.approval_workflow_schema import build_approval_decision
from core.capability_policy_schema import build_capability_policy
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.runtime_contract import evaluate_runtime_contract
from core.sandbox_agent_memory_contract import build_memory_contract
from core.sandbox_agent_tool_contract import build_tool_contract
from tests.test_promotion_gate import _build_chain


ROOT = Path(__file__).parent.parent


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _approval() -> dict:
    return build_approval_decision(
        approval_decision_id="approval_decision_runtime_contract",
        approval_request_id="approval_request_runtime_contract",
        decision="approved_for_activation_candidate",
        decided_by="runtime_contract_reviewer",
        reason="Runtime contract evidence reviewed.",
        evidence_reviewed={"runtime_contract": "declarative_only"},
    )


def _audit_events() -> list[dict]:
    return [{"audit_event_id": "audit_event_runtime_contract", "event_type": "runtime_contract_reviewed"}]


def _manifest(chain: dict) -> dict:
    return _read_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH)


def _write_manifest(chain: dict, manifest: dict) -> None:
    _write_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH, manifest)


def _set_artifact_status(chain: dict, artifact_id: str, status: str) -> None:
    manifest = _manifest(chain)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == artifact_id:
            artifact["status"] = status
            _write_manifest(chain, manifest)
            return
    raise AssertionError(f"artifact not found: {artifact_id}")


def _agent_path(chain: dict, agent_id: str) -> Path:
    return chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"


def _team_path(chain: dict) -> Path:
    return chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"


def _policy(*, domain_id: str, subject_type: str, subject_id: str, capability_id: str = "tool_runtime_contract_declared") -> dict:
    return build_capability_policy(
        policy_id=f"policy_runtime_contract_{subject_type}_{subject_id}",
        domain_id=domain_id,
        subject_type=subject_type,
        subject_id=subject_id,
        capability_type="tool",
        capability_id=capability_id,
        capability_category="internal_future",
        policy_status="allowed_declared",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )


def _memory(domain_id: str, owner_agent_id: str, **overrides) -> dict:
    payload = build_memory_contract(
        memory_id=f"memory_runtime_contract_{owner_agent_id}",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        memory_scope="agent",
        memory_type="documentary",
        persistence="none",
        storage_backend="none",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )
    payload.update(overrides)
    return payload


def _tool(domain_id: str, owner_agent_id: str, **overrides) -> dict:
    payload = build_tool_contract(
        tool_id=f"tool_runtime_contract_{owner_agent_id}",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        tool_name="Runtime Contract Declared Tool",
        tool_category="internal_future",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )
    payload.update(overrides)
    return payload


def _prepare_agent_candidate(chain: dict, *, with_policy: bool = True, memory: dict | None = None, tool: dict | None = None) -> str:
    agent_id = chain["agent_ids"][0]
    path = _agent_path(chain, agent_id)
    agent = _read_json(path)
    agent["status"] = "candidate_for_activation"
    agent["capabilities"] = {
        "memory": [memory if memory is not None else _memory(chain["domain"]["domain_id"], agent_id)],
        "tools": [tool if tool is not None else _tool(chain["domain"]["domain_id"], agent_id)],
        "policies": [],
    }
    if with_policy:
        agent["capabilities"]["policies"].append(
            _policy(
                domain_id=chain["domain"]["domain_id"],
                subject_type="agent",
                subject_id=agent_id,
            )
        )
    _write_json(path, agent)
    _set_artifact_status(chain, f"agent_{agent_id}", "candidate_for_activation")
    return agent_id


def _prepare_team_candidate(chain: dict, *, with_policy: bool = True) -> str:
    team_id = chain["team"]["team_id"]
    path = _team_path(chain)
    team = _read_json(path)
    team["status"] = "candidate_for_activation"
    team["capabilities"]["policies"] = []
    if with_policy:
        team["capabilities"]["policies"].append(
            _policy(
                domain_id=chain["domain"]["domain_id"],
                subject_type="team",
                subject_id=team_id,
                capability_id="tool_team_runtime_contract_declared",
            )
        )
    _write_json(path, team)
    _set_artifact_status(chain, f"team_{team_id}", "candidate_for_activation")
    return team_id


def _active_contract(target_type: str, chain: dict, target_id: str) -> dict:
    return evaluate_active_contract(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        approval_decision=_approval(),
        audit_events=_audit_events(),
    )


def _activate_agent(chain: dict, **kwargs) -> tuple[str, dict]:
    agent_id = _prepare_agent_candidate(chain, **kwargs)
    report = execute_active(
        target_type="agent",
        domain_dir=chain["domain_dir"],
        target_id=agent_id,
        active_contract_result=_active_contract("agent", chain, agent_id),
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="runtime_contract_test",
    )
    assert report["result_status"] == "passed"
    return agent_id, report


def _activate_team(chain: dict, **kwargs) -> tuple[str, dict]:
    team_id = _prepare_team_candidate(chain, **kwargs)
    report = execute_active(
        target_type="team",
        domain_dir=chain["domain_dir"],
        target_id=team_id,
        active_contract_result=_active_contract("team", chain, team_id),
        approval_decision=_approval(),
        audit_events=_audit_events(),
        executed_by="runtime_contract_test",
    )
    assert report["result_status"] == "passed"
    return team_id, report


def _runtime(target_type: str, chain: dict, target_id: str, active_execution: dict | None, **overrides) -> dict:
    return evaluate_runtime_contract(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        active_execution_result=active_execution,
        required_approval=_approval(),
        required_evidence=_audit_events(),
        **overrides,
    )


def _assert_blocked(result: dict, expected: str) -> None:
    assert result["contract_result"] == "blocked"
    assert expected in " ".join(result["blockers"])


def test_runtime_contract_valid_for_active_agent_with_dependencies(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)

    result = _runtime("agent", chain, agent_id, active_execution)

    assert result["contract_result"] == "passed"
    assert result["target_type"] == "agent"
    assert result["runtime_allowed"] is False
    assert result["runtime_enabled"] is False
    assert result["execution_enabled"] is False
    assert result["external_access_enabled"] is False


def test_runtime_contract_valid_for_active_team_with_members_and_dependencies(tmp_path):
    chain = _build_chain(tmp_path)
    team_id, active_execution = _activate_team(chain)

    result = _runtime("team", chain, team_id, active_execution)

    assert result["contract_result"] == "passed"
    assert result["target_type"] == "team"
    assert result["required_capability_policy"]["status"] == "passed"
    assert result["required_tool_contract"]["status"] == "passed"


@pytest.mark.parametrize("status", ["candidate_for_activation", "validated", "materialized", "ready_to_materialize"])
def test_runtime_contract_fails_if_target_is_not_active(tmp_path, status):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["status"] = status
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, "target debe estar active")


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda agent: agent["sandbox_config"].__setitem__("runtime_enabled", True), "runtime_enabled=true bloqueado"),
        (lambda agent: agent["sandbox_config"].__setitem__("execution_enabled", True), "execution_enabled=true bloqueado"),
        (lambda agent: agent["capabilities"]["policies"][0].__setitem__("external_access", True), "external_access_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("tool_execution_enabled", True), "tool_execution_enabled=true bloqueado"),
        (lambda agent: agent.__setitem__("memory_persistence_enabled", True), "memory_persistence_enabled=true bloqueado"),
    ],
)
def test_runtime_contract_blocks_runtime_execution_external_tool_and_memory_flags(tmp_path, mutator, expected):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    mutator(agent)
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, expected)


@pytest.mark.parametrize("status", ["legacy", "broken", "archived"])
def test_runtime_contract_blocks_non_operational_states(tmp_path, status):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["status"] = status
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, f"current_status bloqueado: {status}")


def test_runtime_contract_blocks_direct_runtime_for_non_agent_team_targets(tmp_path):
    chain = _build_chain(tmp_path)

    result = evaluate_runtime_contract(
        target_type="domain",
        domain_dir=chain["domain_dir"],
        active_execution_result=None,
        required_evidence=_audit_events(),
    )

    _assert_blocked(result, "target_type sin runtime directo: domain")


def test_runtime_contract_requires_active_execution_evidence(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, _active_execution = _activate_agent(chain)

    result = _runtime("agent", chain, agent_id, None)

    _assert_blocked(result, "active_execution_result requerido")


def test_runtime_contract_requires_capability_policy(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["capabilities"]["policies"] = []
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, "capability_policy requerida")


def test_runtime_contract_blocks_invalid_memory_contract(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["capabilities"]["memory"][0]["runtime_enabled"] = True
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, "runtime_enabled=true bloqueado")


def test_runtime_contract_blocks_invalid_tool_contract(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    agent["capabilities"]["tools"][0]["execution_allowed"] = True
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, "execution_allowed=true bloqueado")


def test_runtime_contract_blocks_invalid_lineage(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    agent = _read_json(_agent_path(chain, agent_id))
    agent.pop("lineage")
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, "lineage invalido")


def test_runtime_contract_blocks_broken_dependencies(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    manifest = _manifest(chain)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == f"agent_{agent_id}":
            artifact["dependencies"].append("missing_dependency")
    _write_manifest(chain, manifest)

    result = _runtime("agent", chain, agent_id, active_execution)

    _assert_blocked(result, "dependencia inexistente: missing_dependency")


def test_declarative_runtime_mode_passes_and_future_modes_block(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)

    passed = _runtime("agent", chain, agent_id, active_execution, runtime_mode="declarative_runtime_contract")
    runtime_ready = _runtime("agent", chain, agent_id, active_execution, runtime_mode="runtime_ready_future")
    execution_ready = _runtime("agent", chain, agent_id, active_execution, runtime_mode="execution_ready_future")
    external_ready = _runtime("agent", chain, agent_id, active_execution, runtime_mode="external_access_future")

    assert passed["contract_result"] == "passed"
    _assert_blocked(runtime_ready, "runtime_mode bloqueado en esta fase: runtime_ready_future")
    _assert_blocked(execution_ready, "runtime_mode bloqueado en esta fase: execution_ready_future")
    _assert_blocked(external_ready, "runtime_mode bloqueado en esta fase: external_access_future")


def test_runtime_contract_does_not_mutate_state_or_enable_runtime_execution_external_ui_integrations(tmp_path):
    chain = _build_chain(tmp_path)
    agent_id, active_execution = _activate_agent(chain)
    before_domain = _tree_hash(chain["domain_dir"])
    before_root = _tree_hash(ROOT / "core")
    agent_before = deepcopy(_read_json(_agent_path(chain, agent_id)))

    result = _runtime("agent", chain, agent_id, active_execution)

    assert result["contract_result"] == "passed"
    assert _tree_hash(chain["domain_dir"]) == before_domain
    assert _tree_hash(ROOT / "core") == before_root
    agent_after = _read_json(_agent_path(chain, agent_id))
    assert agent_after == agent_before
    assert agent_after["sandbox_config"]["runtime_enabled"] is False
    assert agent_after["sandbox_config"]["operational"] is False
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()
