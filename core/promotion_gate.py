"""Evaluador no mutante de promotion gate para artefactos sandbox."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

from core.agent_preset_materializer import (
    AGENT_PRESETS_ARTIFACT_ID,
    validate_materialized_agent_presets,
)
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.artifact_state import ArtifactState
from core.capability_policy_schema import validate_capability_policy
from core.domain_materializer import validate_materialized_sandbox_domain
from core.paper_seed_materializer import PAPER_SEED_ARTIFACT_ID, validate_materialized_paper_seed
from core.profile_catalog_materializer import (
    ARTIFACT_MANIFEST_RELATIVE_PATH,
    PROFILE_CATALOG_ARTIFACT_ID,
    validate_materialized_profile_catalog,
)
from core.promotion_gate_schema import build_promotion_gate_report
from core.sandbox_agent_materializer import validate_materialized_sandbox_agent
from core.sandbox_team_materializer import validate_materialized_sandbox_team


REQUESTED_STATUSES = {"validated", "candidate_for_activation"}
FORBIDDEN_STATUSES = {"active"}
BLOCKING_CURRENT_STATUSES = {"active", "archived", "broken", "legacy"}

TARGET_ARTIFACT_IDS = {
    "profile_catalog": PROFILE_CATALOG_ARTIFACT_ID,
    "agent_preset": AGENT_PRESETS_ARTIFACT_ID,
    "paper_seed": PAPER_SEED_ARTIFACT_ID,
}


def evaluate_promotion_gate(
    *,
    target_type: str,
    requested_status: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evalua si un target sandbox puede ser candidato, sin promoverlo."""
    evaluator = {
        "domain": evaluate_domain_promotion,
        "artifact": evaluate_artifact_promotion,
        "profile_catalog": evaluate_profile_catalog_promotion,
        "agent_preset": evaluate_agent_preset_promotion,
        "paper_seed": evaluate_paper_seed_promotion,
        "agent": evaluate_agent_promotion,
        "team": evaluate_team_promotion,
        "capability_policy": evaluate_capability_policy_promotion,
    }.get(target_type)
    if evaluator is None:
        return _report(
            domain_id=_domain_id_from_target(target) or "unknown_domain",
            target_type=target_type if target_type else "artifact",
            target_id=_normalize_id(target_id or target_type or "unknown_target"),
            current_status="unknown",
            requested_status=requested_status,
            checks=[],
            blockers=[f"target_type no soportado: {target_type}"],
            evidence={"promotion_gate": "target_type invalido"},
        )
    return evaluator(
        requested_status=requested_status,
        domain_dir=domain_dir,
        target_id=target_id,
        target=target,
    )


def evaluate_domain_promotion(
    *,
    requested_status: str,
    domain_dir: str | Path | None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    domain_id = target_id or "unknown_domain"
    current_status = "unknown"

    _check_requested_status(requested_status, checks, blockers)
    if domain_dir is None:
        blockers.append("domain_dir requerido para evaluar domain")
    else:
        try:
            validation = validate_materialized_sandbox_domain(domain_dir)
            domain = validation["domain"]
            domain_id = domain["domain_id"]
            current_status = domain["status"]
            evidence["domain_json_path"] = str(validation["domain_json_path"])
            _check_current_status(current_status, checks, blockers)
            _add_check(checks, "domain_schema", "passed", f"domain_id={domain_id}")
            manifest = _load_manifest(domain_dir, checks, blockers, evidence)
            _check_minimum_chain(manifest, checks, blockers)
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"domain invalid: {exc}")
            _add_check(checks, "domain_schema", "blocked", str(exc))

    return _report(
        domain_id=domain_id,
        target_type="domain",
        target_id=domain_id,
        current_status=current_status,
        requested_status=requested_status,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
    )


def evaluate_artifact_promotion(
    *,
    requested_status: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    domain_id = _domain_id_from_target(target) or "unknown_domain"
    current_status = str((target or {}).get("status") or "unknown")
    artifact_id = target_id or str((target or {}).get("artifact_id") or "unknown_artifact")

    _check_requested_status(requested_status, checks, blockers)
    try:
        artifact = target or _artifact_from_manifest(domain_dir, artifact_id)
        domain_id = _domain_id_from_domain_dir(domain_dir) or domain_id
        current_status = artifact["status"]
        _check_artifact_record(artifact, checks, blockers)
        if domain_dir is not None:
            manifest = _load_manifest(domain_dir, checks, blockers, evidence)
            _check_manifest_dependencies(manifest, checks, blockers)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"artifact invalid: {exc}")
        _add_check(checks, "artifact_record", "blocked", str(exc))

    return _report(
        domain_id=domain_id,
        target_type="artifact",
        target_id=_normalize_id(artifact_id),
        current_status=current_status,
        requested_status=requested_status,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
    )


def evaluate_profile_catalog_promotion(**kwargs: Any) -> dict[str, Any]:
    return _evaluate_materialized_target(
        target_type="profile_catalog",
        artifact_id=PROFILE_CATALOG_ARTIFACT_ID,
        validator=validate_materialized_profile_catalog,
        **kwargs,
    )


def evaluate_agent_preset_promotion(**kwargs: Any) -> dict[str, Any]:
    return _evaluate_materialized_target(
        target_type="agent_preset",
        artifact_id=AGENT_PRESETS_ARTIFACT_ID,
        validator=validate_materialized_agent_presets,
        **kwargs,
    )


def evaluate_paper_seed_promotion(**kwargs: Any) -> dict[str, Any]:
    return _evaluate_materialized_target(
        target_type="paper_seed",
        artifact_id=PAPER_SEED_ARTIFACT_ID,
        validator=validate_materialized_paper_seed,
        **kwargs,
    )


def evaluate_agent_promotion(
    *,
    requested_status: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    agent_id = _normalize_entity_id(target_id, prefix="agent")
    checks: list[dict[str, str]] = []
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    domain_id = _domain_id_from_domain_dir(domain_dir) or "unknown_domain"
    current_status = "unknown"
    _check_requested_status(requested_status, checks, blockers)

    try:
        if domain_dir is None or agent_id is None:
            raise ValueError("domain_dir y target_id son requeridos para agent")
        validation = validate_materialized_sandbox_agent(domain_dir, agent_id=agent_id)
        agent = validation["agent"]
        artifact = validation["artifact"]
        domain_id = agent["domain_id"]
        current_status = agent["status"]
        _check_artifact_record(artifact, checks, blockers)
        _check_current_status(current_status, checks, blockers)
        _require_false(agent.get("sandbox_config", {}), "runtime_enabled", checks, blockers)
        _require_false(agent.get("sandbox_config", {}), "operational", checks, blockers)
        if not agent.get("lineage"):
            raise ValueError("agent lineage requerido")
        _add_check(checks, "lineage", "passed", f"agent_id={agent_id}")
        _load_manifest(domain_dir, checks, blockers, evidence)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"agent invalid: {exc}")
        _add_check(checks, "agent_contract", "blocked", str(exc))

    return _report(
        domain_id=domain_id,
        target_type="agent",
        target_id=agent_id or "unknown_agent",
        current_status=current_status,
        requested_status=requested_status,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
    )


def evaluate_team_promotion(
    *,
    requested_status: str,
    domain_dir: str | Path | None,
    target_id: str | None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    team_id = _normalize_entity_id(target_id, prefix="team")
    checks: list[dict[str, str]] = []
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    domain_id = _domain_id_from_domain_dir(domain_dir) or "unknown_domain"
    current_status = "unknown"
    _check_requested_status(requested_status, checks, blockers)

    try:
        if domain_dir is None or team_id is None:
            raise ValueError("domain_dir y target_id son requeridos para team")
        validation = validate_materialized_sandbox_team(domain_dir, team_id=team_id)
        team = validation["team"]
        artifact = validation["artifact"]
        domain_id = team["domain_id"]
        current_status = team["status"]
        _check_artifact_record(artifact, checks, blockers)
        _check_current_status(current_status, checks, blockers)
        _require_false(team.get("metadata", {}), "runtime_enabled", checks, blockers)
        _require_false(team.get("metadata", {}), "execution_enabled", checks, blockers)
        _require_false(team.get("coordination_model", {}), "runtime_enabled", checks, blockers)
        _require_false(team.get("coordination_model", {}), "execution_enabled", checks, blockers)
        _add_check(checks, "team_members", "passed", f"members={len(team['member_agents'])}")
        _load_manifest(domain_dir, checks, blockers, evidence)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"team invalid: {exc}")
        _add_check(checks, "team_contract", "blocked", str(exc))

    return _report(
        domain_id=domain_id,
        target_type="team",
        target_id=team_id or "unknown_team",
        current_status=current_status,
        requested_status=requested_status,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
    )


def evaluate_capability_policy_promotion(
    *,
    requested_status: str,
    domain_dir: str | Path | None = None,
    target_id: str | None = None,
    target: dict[str, Any] | None,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    domain_id = _domain_id_from_target(target) or "unknown_domain"
    current_status = str((target or {}).get("policy_status") or "unknown")
    policy_id = target_id or str((target or {}).get("policy_id") or "unknown_policy")
    _check_requested_status(requested_status, checks, blockers)

    try:
        if target is None:
            raise ValueError("target capability_policy requerido")
        policy = validate_capability_policy(target)
        domain_id = policy["domain_id"]
        policy_id = policy["policy_id"]
        current_status = policy["policy_status"]
        _require_false(policy, "runtime_enabled", checks, blockers)
        _require_false(policy, "execution_allowed", checks, blockers)
        _require_false(policy, "external_access", checks, blockers)
        _add_check(checks, "capability_policy", "passed", f"policy_status={current_status}")
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"capability_policy invalid: {exc}")
        _add_check(checks, "capability_policy", "blocked", str(exc))

    return _report(
        domain_id=domain_id,
        target_type="capability_policy",
        target_id=_normalize_id(policy_id),
        current_status=current_status,
        requested_status=requested_status,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
    )


def _evaluate_materialized_target(
    *,
    target_type: str,
    artifact_id: str,
    validator: Callable[[str | Path], dict[str, Any]],
    requested_status: str,
    domain_dir: str | Path | None,
    target_id: str | None = None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    blockers: list[str] = []
    evidence: dict[str, Any] = {}
    domain_id = _domain_id_from_domain_dir(domain_dir) or "unknown_domain"
    current_status = "unknown"
    _check_requested_status(requested_status, checks, blockers)

    try:
        if domain_dir is None:
            raise ValueError("domain_dir requerido")
        validation = validator(domain_dir)
        artifact = validation["artifact"]
        current_status = artifact["status"]
        _check_artifact_record(artifact, checks, blockers)
        _load_manifest(domain_dir, checks, blockers, evidence)
        _add_check(checks, target_type, "passed", f"artifact_id={artifact['artifact_id']}")
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"{target_type} invalid: {exc}")
        _add_check(checks, target_type, "blocked", str(exc))

    return _report(
        domain_id=domain_id,
        target_type=target_type,
        target_id=artifact_id,
        current_status=current_status,
        requested_status=requested_status,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
    )


def _check_requested_status(
    requested_status: str,
    checks: list[dict[str, str]],
    blockers: list[str],
) -> None:
    if requested_status in FORBIDDEN_STATUSES:
        blockers.append("requested_status active bloqueado en esta fase")
        _add_check(checks, "requested_status", "blocked", "active requiere fase futura")
    elif requested_status in REQUESTED_STATUSES:
        _add_check(checks, "requested_status", "passed", f"requested_status={requested_status}")
    else:
        blockers.append(f"requested_status invalido: {requested_status}")
        _add_check(checks, "requested_status", "blocked", f"requested_status={requested_status}")


def _check_current_status(
    current_status: str,
    checks: list[dict[str, str]],
    blockers: list[str],
) -> None:
    if current_status in BLOCKING_CURRENT_STATUSES:
        blockers.append(f"current_status bloqueado: {current_status}")
        _add_check(checks, "current_status", "blocked", f"current_status={current_status}")
    elif current_status in {ArtifactState.MATERIALIZED.value, ArtifactState.READY_TO_MATERIALIZE.value}:
        _add_check(checks, "current_status", "passed", f"current_status={current_status}")
    else:
        _add_check(checks, "current_status", "passed", f"current_status={current_status}")


def _check_artifact_record(
    artifact: dict[str, Any],
    checks: list[dict[str, str]],
    blockers: list[str],
) -> None:
    current_status = str(artifact.get("status"))
    _check_current_status(current_status, checks, blockers)
    if artifact.get("operational") is True or artifact.get("passed") is True:
        blockers.append("artifact no debe estar operational/passed antes de promotion real")
        _add_check(checks, "artifact_operational", "blocked", "operational/passed=true")
    else:
        _add_check(checks, "artifact_operational", "passed", "operational=false passed=false")


def _load_manifest(
    domain_dir: str | Path,
    checks: list[dict[str, str]],
    blockers: list[str],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    manifest_path = Path(domain_dir).resolve() / ARTIFACT_MANIFEST_RELATIVE_PATH
    manifest = validate_artifact_manifest_file(manifest_path)
    evidence["artifact_manifest_path"] = str(manifest_path)
    _add_check(checks, "artifact_manifest", "passed", f"artifacts={len(manifest['artifacts'])}")
    _check_manifest_dependencies(manifest, checks, blockers)
    return manifest


def _check_manifest_dependencies(
    manifest: dict[str, Any],
    checks: list[dict[str, str]],
    blockers: list[str],
) -> None:
    artifact_ids = {artifact["artifact_id"] for artifact in manifest.get("artifacts", [])}
    missing = [
        dependency
        for artifact in manifest.get("artifacts", [])
        for dependency in artifact.get("dependencies", [])
        if dependency not in artifact_ids
    ]
    if missing:
        blockers.append(f"manifest dependencies rotas: {missing}")
        _add_check(checks, "dependencies", "blocked", f"missing={missing}")
    else:
        _add_check(checks, "dependencies", "passed", "todas las dependencias existen")


def _check_minimum_chain(
    manifest: dict[str, Any],
    checks: list[dict[str, str]],
    blockers: list[str],
) -> None:
    artifact_types = {artifact["artifact_type"] for artifact in manifest.get("artifacts", [])}
    missing = [
        artifact_type
        for artifact_type in ["profile_catalog", "agent_preset", "paper_seed"]
        if artifact_type not in artifact_types
    ]
    if missing:
        blockers.append(f"cadena minima incompleta: {missing}")
        _add_check(checks, "minimum_chain", "blocked", f"missing={missing}")
    else:
        _add_check(checks, "minimum_chain", "passed", "profile_catalog/agent_preset/paper_seed presentes")


def _artifact_from_manifest(domain_dir: str | Path | None, artifact_id: str) -> dict[str, Any]:
    if domain_dir is None:
        raise ValueError("domain_dir requerido para buscar artifact")
    manifest = validate_artifact_manifest_file(Path(domain_dir).resolve() / ARTIFACT_MANIFEST_RELATIVE_PATH)
    matches = [artifact for artifact in manifest["artifacts"] if artifact["artifact_id"] == artifact_id]
    if len(matches) != 1:
        raise ValueError(f"artifact_id no encontrado o ambiguo: {artifact_id}")
    return matches[0]


def _require_false(
    payload: dict[str, Any],
    field: str,
    checks: list[dict[str, str]],
    blockers: list[str],
) -> None:
    if payload.get(field) is not False:
        blockers.append(f"{field} debe ser false")
        _add_check(checks, field, "blocked", f"{field}={payload.get(field)}")
    else:
        _add_check(checks, field, "passed", f"{field}=false")


def _report(
    *,
    domain_id: str,
    target_type: str,
    target_id: str,
    current_status: str,
    requested_status: str,
    checks: list[dict[str, str]],
    blockers: list[str],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    gate_result = "blocked" if blockers or requested_status == "active" else "passed"
    return build_promotion_gate_report(
        gate_id=_normalize_id(f"gate_{target_type}_{target_id}_{requested_status}"),
        domain_id=_normalize_id(domain_id),
        target_type=target_type,
        target_id=_normalize_id(target_id),
        current_status=current_status,
        requested_status=requested_status,
        gate_result=gate_result,
        checks=checks,
        blockers=blockers,
        evidence=evidence,
        capability_policy_result=_summary_for(checks, "capability_policy"),
        runtime_boundary_result=_runtime_summary(checks),
        legacy_boundary_result="blocked" if current_status == "legacy" else "passed",
    )


def _summary_for(checks: list[dict[str, str]], prefix: str) -> str:
    matching = [check for check in checks if check["check"].startswith(prefix)]
    if not matching:
        return "not_applicable"
    return "blocked" if any(check["result"] == "blocked" for check in matching) else "passed"


def _runtime_summary(checks: list[dict[str, str]]) -> str:
    runtime_checks = [
        check
        for check in checks
        if check["check"] in {"runtime_enabled", "execution_enabled", "external_access", "operational"}
    ]
    if not runtime_checks:
        return "not_applicable"
    return "blocked" if any(check["result"] == "blocked" for check in runtime_checks) else "passed"


def _add_check(checks: list[dict[str, str]], check: str, result: str, evidence: str) -> None:
    checks.append({"check": check, "result": result, "evidence": evidence})


def _domain_id_from_domain_dir(domain_dir: str | Path | None) -> str | None:
    if domain_dir is None:
        return None
    try:
        return validate_materialized_sandbox_domain(domain_dir)["domain"]["domain_id"]
    except Exception:  # noqa: BLE001
        return None


def _domain_id_from_target(target: dict[str, Any] | None) -> str | None:
    if not target:
        return None
    return target.get("domain_id")


def _normalize_entity_id(value: str | None, *, prefix: str) -> str | None:
    if value is None:
        return None
    normalized = _normalize_id(value)
    prefix_text = f"{prefix}_"
    return normalized[len(prefix_text) :] if normalized.startswith(prefix_text) else normalized


def _normalize_id(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    normalized = re.sub(r"_+", "_", normalized)
    return normalized or "unknown"
