import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from core.active_contract import evaluate_active_contract
from core.active_executor import execute_active
from core.approval_workflow import build_approval_request_from_gate, record_approval_decision
from core.approval_workflow_schema import build_approval_decision
from core.capability_policy_schema import build_capability_policy
from core.profile_catalog_materializer import ARTIFACT_MANIFEST_RELATIVE_PATH
from core.promotion_executor import execute_promotion
from core.promotion_gate import evaluate_promotion_gate
from core.runtime_contract import evaluate_runtime_contract
from core.sandbox_agent_memory_contract import build_memory_contract
from core.sandbox_agent_tool_contract import build_tool_contract
from tests.test_promotion_gate import _build_chain


ROOT = Path(__file__).parent.parent
AGENTS = ROOT / "agents"
DOMAINS = ROOT / "domains"
CATALOGS = ROOT / "catalogs"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _tree_inventory(root: Path) -> tuple[tuple[str, int], ...]:
    if not root.exists():
        return (("__missing__", 0),)
    return tuple(
        (path.relative_to(root).as_posix(), path.stat().st_size)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    )


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        digest.update(b"missing")
        return digest.hexdigest()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _papers_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(DOMAINS.glob("*/agents/papers/*.json")):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(str(path.stat().st_size).encode("utf-8"))
    return digest.hexdigest()


def _operational_snapshot() -> dict[str, object]:
    return {
        "domains": _tree_inventory(DOMAINS),
        "agents": _tree_inventory(AGENTS),
        "catalogs": _tree_inventory(CATALOGS),
        "global_papers": _papers_hash(),
    }


def _manifest(chain: dict) -> dict:
    return _read_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH)


def _write_manifest(chain: dict, manifest: dict) -> None:
    _write_json(chain["domain_dir"] / ARTIFACT_MANIFEST_RELATIVE_PATH, manifest)


def _artifact(chain: dict, artifact_id: str) -> dict:
    matches = [artifact for artifact in _manifest(chain)["artifacts"] if artifact["artifact_id"] == artifact_id]
    assert len(matches) == 1
    return matches[0]


def _agent_path(chain: dict, agent_id: str) -> Path:
    return chain["domain_dir"] / "sandbox_agents" / f"{agent_id}.json"


def _team_path(chain: dict) -> Path:
    return chain["domain_dir"] / "sandbox_teams" / f"{chain['team']['team_id']}.json"


def _policy(*, domain_id: str, subject_type: str, subject_id: str, capability_id: str) -> dict:
    return build_capability_policy(
        policy_id=f"policy_runtime_contract_e2e_{subject_type}_{subject_id}",
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


def _memory(domain_id: str, owner_agent_id: str, *, memory_scope: str = "agent") -> dict:
    return build_memory_contract(
        memory_id=f"memory_runtime_contract_e2e_{memory_scope}_{owner_agent_id}",
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        memory_scope=memory_scope,
        memory_type="documentary",
        persistence="none",
        storage_backend="none",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )


def _tool(domain_id: str, owner_agent_id: str, *, tool_id: str) -> dict:
    return build_tool_contract(
        tool_id=tool_id,
        owner_agent_id=owner_agent_id,
        domain_id=domain_id,
        tool_name="Runtime Contract E2E Declared Tool",
        tool_category="internal_future",
        created_at="2026-07-17T00:00:00",
        updated_at="2026-07-17T00:00:00",
    )


def _enrich_capabilities(chain: dict) -> tuple[str, str]:
    domain_id = chain["domain"]["domain_id"]
    agent_id = chain["agent_ids"][0]
    team_id = chain["team"]["team_id"]
    agent_tool = _tool(domain_id, agent_id, tool_id="tool_runtime_contract_e2e_agent")
    team_tool = _tool(domain_id, agent_id, tool_id="tool_runtime_contract_e2e_team")

    agent = _read_json(_agent_path(chain, agent_id))
    agent["capabilities"] = {
        "memory": [_memory(domain_id, agent_id)],
        "tools": [agent_tool],
        "policies": [
            _policy(
                domain_id=domain_id,
                subject_type="agent",
                subject_id=agent_id,
                capability_id=agent_tool["tool_id"],
            )
        ],
    }
    _write_json(_agent_path(chain, agent_id), agent)

    team = _read_json(_team_path(chain))
    team["capabilities"] = {
        "memory": [_memory(domain_id, agent_id, memory_scope="team")],
        "tools": [team_tool],
        "policies": [
            _policy(
                domain_id=domain_id,
                subject_type="team",
                subject_id=team_id,
                capability_id=team_tool["tool_id"],
            )
        ],
    }
    _write_json(_team_path(chain), team)
    return agent_id, team_id


def _candidate_approval(gate: dict) -> tuple[dict, dict]:
    request = build_approval_request_from_gate(
        gate,
        requested_by=f"requester_runtime_contract_e2e_{gate['target_type']}",
    )
    decision = record_approval_decision(
        request,
        decision="approved_for_activation_candidate",
        decided_by=f"reviewer_runtime_contract_e2e_{gate['target_type']}",
        reason="Runtime contract E2E candidate evidence reviewed.",
    )
    return request, decision


def _promote_to_candidate(chain: dict, *, target_type: str, target_id: str) -> dict:
    gate = evaluate_promotion_gate(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        requested_status="candidate_for_activation",
    )
    assert gate["gate_result"] == "passed"
    request, decision = _candidate_approval(gate)
    execution = execute_promotion(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        requested_status="candidate_for_activation",
        promotion_gate_result=gate,
        approval_request=request,
        approval_decision=decision,
        executed_by="runtime_contract_e2e_promotion",
    )
    assert execution["execution_result"] == "applied"
    return execution


def _active_approval(target_type: str, target_id: str) -> dict:
    return build_approval_decision(
        approval_decision_id=f"approval_decision_runtime_contract_e2e_active_{target_type}_{target_id}",
        approval_request_id=f"approval_request_runtime_contract_e2e_active_{target_type}_{target_id}",
        decision="approved_for_activation_candidate",
        decided_by="reviewer_runtime_contract_e2e_active",
        reason="Runtime contract E2E active evidence reviewed.",
        evidence_reviewed={"target_type": target_type, "target_id": target_id},
    )


def _active_audit(target_type: str, target_id: str) -> dict:
    return {
        "audit_event_id": f"audit_event_runtime_contract_e2e_active_{target_type}_{target_id}",
        "event_type": "active_contract_reviewed",
        "target_type": target_type,
        "target_id": target_id,
    }


def _activate(chain: dict, *, target_type: str, target_id: str) -> dict:
    approval = _active_approval(target_type, target_id)
    audit = _active_audit(target_type, target_id)
    contract = evaluate_active_contract(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        approval_decision=approval,
        audit_events=[audit],
    )
    assert contract["contract_result"] == "passed"
    execution = execute_active(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        active_contract_result=contract,
        approval_decision=approval,
        audit_events=[audit],
        executed_by="runtime_contract_e2e_active",
    )
    assert execution["result_status"] == "passed"
    return execution


def _runtime(chain: dict, *, target_type: str, target_id: str, active_execution: dict | None, **overrides) -> dict:
    return evaluate_runtime_contract(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_id,
        active_execution_result=active_execution,
        required_approval=_active_approval(target_type, target_id),
        required_evidence=[_active_audit(target_type, target_id)],
        **overrides,
    )


def _assert_blocked(result: dict, expected: str) -> None:
    assert result["contract_result"] == "blocked"
    assert expected in " ".join(result["blockers"])


def _assert_boundaries(chain: dict, agent_id: str, team_id: str) -> None:
    agent = _read_json(_agent_path(chain, agent_id))
    team = _read_json(_team_path(chain))
    assert agent["sandbox_config"]["runtime_enabled"] is False
    assert agent["sandbox_config"]["operational"] is False
    assert agent["capabilities"]["tools"][0]["runtime_enabled"] is False
    assert agent["capabilities"]["tools"][0]["execution_allowed"] is False
    assert agent["capabilities"]["tools"][0]["external_access"] is False
    assert agent["capabilities"]["memory"][0]["runtime_enabled"] is False
    assert agent["capabilities"]["memory"][0]["persistence"] == "none"
    assert team["metadata"]["runtime_enabled"] is False
    assert team["metadata"]["execution_enabled"] is False
    assert team["coordination_model"]["runtime_enabled"] is False
    assert team["coordination_model"]["execution_enabled"] is False
    assert team["capabilities"]["tools"][0]["execution_allowed"] is False
    assert team["capabilities"]["tools"][0]["external_access"] is False
    assert team["capabilities"]["memory"][0]["runtime_enabled"] is False
    assert team["capabilities"]["memory"][0]["persistence"] == "none"
    assert _artifact(chain, f"agent_{agent_id}")["status"] == "active"
    assert _artifact(chain, f"team_{team_id}")["status"] == "active"


def _active_chain(tmp_path: Path) -> tuple[dict, str, str, dict, dict]:
    chain = _build_chain(tmp_path)
    agent_id, team_id = _enrich_capabilities(chain)
    _promote_to_candidate(chain, target_type="agent", target_id=agent_id)
    _promote_to_candidate(chain, target_type="team", target_id=team_id)
    agent_active = _activate(chain, target_type="agent", target_id=agent_id)
    team_active = _activate(chain, target_type="team", target_id=team_id)
    return chain, agent_id, team_id, agent_active, team_active


def test_runtime_contract_e2e_agent_and_team_pass_without_mutation_or_runtime(tmp_path):
    before_operational = _operational_snapshot()
    chain, agent_id, team_id, agent_active, team_active = _active_chain(tmp_path)
    before_sandbox_hash = _tree_hash(chain["domain_dir"])
    before_manifest = deepcopy(_manifest(chain))
    before_agent = deepcopy(_read_json(_agent_path(chain, agent_id)))
    before_team = deepcopy(_read_json(_team_path(chain)))

    agent_runtime = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    team_runtime = _runtime(chain, target_type="team", target_id=team_id, active_execution=team_active)

    assert agent_runtime["contract_result"] == "passed"
    assert team_runtime["contract_result"] == "passed"
    assert agent_runtime["runtime_mode"] == "declarative_runtime_contract"
    assert team_runtime["runtime_mode"] == "declarative_runtime_contract"
    assert agent_runtime["runtime_allowed"] is False
    assert team_runtime["runtime_allowed"] is False
    assert _tree_hash(chain["domain_dir"]) == before_sandbox_hash
    assert _manifest(chain) == before_manifest
    assert _read_json(_agent_path(chain, agent_id)) == before_agent
    assert _read_json(_team_path(chain)) == before_team
    _assert_boundaries(chain, agent_id, team_id)
    assert _operational_snapshot() == before_operational
    assert not (chain["domain_dir"] / "ui").exists()
    assert not (chain["domain_dir"] / "integrations").exists()


@pytest.mark.parametrize("target_type", ["agent", "team"])
@pytest.mark.parametrize("status", ["materialized", "validated", "candidate_for_activation", "archived", "broken", "legacy"])
def test_runtime_contract_e2e_blocks_non_active_statuses(tmp_path, target_type, status):
    chain, agent_id, team_id, agent_active, team_active = _active_chain(tmp_path)
    target_id = agent_id if target_type == "agent" else team_id
    active_execution = agent_active if target_type == "agent" else team_active
    path = _agent_path(chain, agent_id) if target_type == "agent" else _team_path(chain)
    payload = _read_json(path)
    payload["status"] = status
    _write_json(path, payload)

    result = _runtime(chain, target_type=target_type, target_id=target_id, active_execution=active_execution)

    _assert_blocked(result, "target debe estar active")


@pytest.mark.parametrize("runtime_mode", ["runtime_ready_future", "execution_ready_future", "external_access_future"])
def test_runtime_contract_e2e_blocks_future_runtime_modes(tmp_path, runtime_mode):
    chain, agent_id, _team_id, agent_active, _team_active = _active_chain(tmp_path)

    result = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active, runtime_mode=runtime_mode)

    _assert_blocked(result, f"runtime_mode bloqueado en esta fase: {runtime_mode}")


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
def test_runtime_contract_e2e_blocks_forbidden_flags(tmp_path, mutator, expected):
    chain, agent_id, _team_id, agent_active, _team_active = _active_chain(tmp_path)
    agent = _read_json(_agent_path(chain, agent_id))
    mutator(agent)
    _write_json(_agent_path(chain, agent_id), agent)

    result = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)

    _assert_blocked(result, expected)


def test_runtime_contract_e2e_blocks_missing_evidence_policy_contracts_lineage_and_dependencies(tmp_path):
    chain, agent_id, _team_id, agent_active, _team_active = _active_chain(tmp_path)

    missing_evidence = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=None)
    _assert_blocked(missing_evidence, "active_execution_result requerido")

    agent_path = _agent_path(chain, agent_id)
    agent = _read_json(agent_path)
    valid_agent = deepcopy(agent)

    agent["capabilities"]["policies"] = []
    _write_json(agent_path, agent)
    missing_policy = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    _assert_blocked(missing_policy, "capability_policy requerida")

    agent = deepcopy(valid_agent)
    agent["capabilities"]["policies"][0]["declared_only"] = False
    _write_json(agent_path, agent)
    invalid_policy = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    _assert_blocked(invalid_policy, "capability_policy debe tener declared_only=true")

    agent = deepcopy(valid_agent)
    agent["capabilities"]["memory"][0]["runtime_enabled"] = True
    _write_json(agent_path, agent)
    invalid_memory = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    _assert_blocked(invalid_memory, "runtime_enabled=true bloqueado")

    agent = deepcopy(valid_agent)
    agent["capabilities"]["tools"][0]["execution_allowed"] = True
    _write_json(agent_path, agent)
    invalid_tool = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    _assert_blocked(invalid_tool, "execution_allowed=true bloqueado")

    agent = deepcopy(valid_agent)
    agent.pop("lineage")
    _write_json(agent_path, agent)
    invalid_lineage = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    _assert_blocked(invalid_lineage, "lineage invalido")

    _write_json(agent_path, valid_agent)
    manifest = _manifest(chain)
    for artifact in manifest["artifacts"]:
        if artifact["artifact_id"] == f"agent_{agent_id}":
            artifact["dependencies"].append("missing_dependency")
    _write_manifest(chain, manifest)
    broken_dependencies = _runtime(chain, target_type="agent", target_id=agent_id, active_execution=agent_active)
    _assert_blocked(broken_dependencies, "dependencia inexistente: missing_dependency")


@pytest.mark.parametrize(
    "target_type",
    ["domain", "profile_catalog", "agent_preset", "paper_seed", "capability_policy", "tool_contract", "memory_contract"],
)
def test_runtime_contract_e2e_blocks_wrong_direct_runtime_target_types(tmp_path, target_type):
    chain, _agent_id, _team_id, _agent_active, _team_active = _active_chain(tmp_path)

    result = evaluate_runtime_contract(
        target_type=target_type,
        domain_dir=chain["domain_dir"],
        target_id=target_type,
        active_execution_result=None,
        required_evidence=[{"audit_event_id": "audit_event_wrong_target"}],
    )

    _assert_blocked(result, f"target_type sin runtime directo: {target_type}")
