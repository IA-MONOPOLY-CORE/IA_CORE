"""Benchmark largo de la cadena sandbox 200/200.

Este runner materializa dominios sandbox temporales y nunca escribe en
`domains/` operativo, `agents/` runtime ni catalogos globales.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.agent_preset_materializer import materialize_agent_presets, rollback_agent_presets
from core.artifact_manifest_schema import validate_artifact_manifest_file
from core.domain_materialization_rollback import rollback_domain_materialization
from core.domain_materializer import materialize_sandbox_domain, validate_materialized_sandbox_domain
from core.paper_seed_materializer import materialize_paper_seed, rollback_paper_seed
from core.profile_catalog_materializer import materialize_profile_catalog, rollback_profile_catalog
from core.sandbox_agent_materializer import (
    materialize_sandbox_agent,
    rollback_sandbox_agent,
    validate_materialized_sandbox_agent,
)


CATALOGS = ROOT / "catalogs"
DOMAINS = ROOT / "domains"
AGENTS = ROOT / "agents"
FIXTURE = ROOT / "tests" / "fixtures" / "sandbox_domain" / "domain.json"
DEFAULT_OUTPUT = ROOT / "docs" / "benchmarks" / "sandbox_full_200_benchmark.json"
BENCHMARK_ID = "sandbox_full_200_v1"
FULL_DOMAIN_TARGET = 200
SELECTIVE_ROLLBACK_DOMAINS = 5


def run_benchmark(
    *,
    output_path: str | Path | None = DEFAULT_OUTPUT,
    domain_limit: int | None = None,
    write_metrics: bool = True,
) -> dict[str, Any]:
    started = time.perf_counter()
    started_at = datetime.now().isoformat()
    before_domains = _tree_hash(DOMAINS)
    before_agents = _tree_hash(AGENTS)
    before_catalogs = _tree_hash(CATALOGS)
    before_papers = _papers_hash()

    areas = [area for area in _load_catalog("areas.json") if area.get("activo", True)]
    niches = [niche for niche in _load_catalog("niches.json") if niche.get("activo", True)]
    pairs = sorted((niche["area_id"], niche["id"]) for niche in niches)
    selected_pairs = pairs[: domain_limit or len(pairs)]

    metrics = _empty_metrics(
        created_at=started_at,
        head=_git_head(),
        areas=len(areas),
        niches=len(niches),
        combinations=len(pairs),
    )
    metrics["domains_attempted"] = len(selected_pairs)

    sandbox_root = Path(tempfile.mkdtemp(prefix="ia_core_sandbox_full_")).resolve()
    materializations: list[dict[str, Any]] = []

    try:
        for index, (area_id, niche_id) in enumerate(selected_pairs, start=1):
            try:
                materialization = _materialize_chain(
                    sandbox_root=sandbox_root,
                    index=index,
                    area_id=area_id,
                    niche_id=niche_id,
                    metrics=metrics,
                )
                materializations.append(materialization)
            except Exception as exc:  # noqa: BLE001 - benchmark must preserve all failures.
                metrics["domains_failed"] += 1
                metrics["failures"].append(
                    {
                        "stage": "materialization",
                        "index": index,
                        "area_id": area_id,
                        "niche_id": niche_id,
                        "error_type": type(exc).__name__,
                        "message": str(exc),
                    }
                )

        _run_representative_regeneration(materializations, metrics)
        _run_rollbacks(materializations, metrics)
        metrics["sandbox_root_clean"] = not list(sandbox_root.glob("*/domain.json"))
        if not metrics["sandbox_root_clean"]:
            metrics["legacy_isolation_failures"] += 1
            metrics["failures"].append(
                {
                    "stage": "cleanup",
                    "error_type": "SandboxResidue",
                    "message": "Quedaron domain.json dentro del sandbox temporal.",
                }
            )
    finally:
        shutil.rmtree(sandbox_root, ignore_errors=True)

    if (
        _tree_hash(DOMAINS) != before_domains
        or _tree_hash(AGENTS) != before_agents
        or _tree_hash(CATALOGS) != before_catalogs
        or _papers_hash() != before_papers
    ):
        metrics["legacy_isolation_failures"] += 1
        metrics["failures"].append(
            {
                "stage": "legacy_isolation",
                "error_type": "RepositoryMutation",
                "message": "Cambio detectado en domains/, agents/, catalogs/ o papers globales.",
            }
        )

    metrics["duration_seconds"] = round(time.perf_counter() - started, 3)
    metrics["average_seconds_per_domain"] = round(
        metrics["duration_seconds"] / metrics["domains_attempted"],
        3,
    )
    metrics["result"] = _classify(metrics)

    if write_metrics and output_path is not None:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return metrics


def _materialize_chain(
    *,
    sandbox_root: Path,
    index: int,
    area_id: str,
    niche_id: str,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    schema = _schema_for_pair(index=index, area_id=area_id, niche_id=niche_id)
    domain = materialize_sandbox_domain(
        schema,
        sandbox_root=sandbox_root,
        execution_metadata={"benchmark_id": BENCHMARK_ID, "index": index},
    )
    domain_dir = Path(domain["domain_dir"])
    validate_materialized_sandbox_domain(domain_dir)
    metrics["domains_materialized"] += 1

    profile = materialize_profile_catalog(domain_dir)
    profile_payload = json.loads(Path(profile["profile_catalog_path"]).read_text(encoding="utf-8"))
    metrics["profile_catalogs_generated"] += 1
    metrics["profiles_generated"] += len(profile_payload.get("profiles", []))

    presets = materialize_agent_presets(domain_dir)
    presets_payload = json.loads(Path(presets["agent_presets_path"]).read_text(encoding="utf-8"))
    preset_items = presets_payload.get("presets", [])
    metrics["agent_presets_generated"] += len(preset_items)

    paper = materialize_paper_seed(domain_dir)
    paper_payload = json.loads(Path(paper["paper_seed_path"]).read_text(encoding="utf-8"))
    metrics["paper_seed_generated"] += len(paper_payload.get("paper_seeds", []))

    agents = []
    for preset in preset_items:
        agent = materialize_sandbox_agent(domain_dir, preset_id=preset["preset_id"])
        validate_materialized_sandbox_agent(domain_dir, agent_id=agent["agent_id"])
        agents.append(agent)
        metrics["sandbox_agents_generated"] += 1
        _validate_agent_boundary(agent, metrics)

    manifest = validate_artifact_manifest_file(Path(domain["domain_dir"]) / "manifests" / "artifact_manifest.json")
    if any(artifact.get("status") == "active" for artifact in manifest.get("artifacts", [])):
        metrics["runtime_boundary_failures"] += 1
    if not agents:
        metrics["lineage_failures"] += 1

    return {
        "domain": domain,
        "domain_dir": domain_dir,
        "profile": profile,
        "presets": presets,
        "paper": paper,
        "agents": agents,
        "first_preset_id": preset_items[0]["preset_id"] if preset_items else None,
    }


def _run_representative_regeneration(
    materializations: list[dict[str, Any]],
    metrics: dict[str, Any],
) -> None:
    if not materializations:
        return
    target = materializations[0]
    domain_dir = target["domain_dir"]
    first_preset_id = target["first_preset_id"]
    steps = [
        ("profile_catalog", lambda: materialize_profile_catalog(domain_dir, regenerate=True)),
        ("agent_presets", lambda: materialize_agent_presets(domain_dir, regenerate=True)),
        ("paper_seed", lambda: materialize_paper_seed(domain_dir, regenerate=True)),
        (
            "sandbox_agent",
            lambda: materialize_sandbox_agent(domain_dir, preset_id=first_preset_id, regenerate=True),
        ),
    ]
    for stage, action in steps:
        metrics["regeneration_attempted"] += 1
        try:
            result = action()
            if result.get("regenerated") is not True:
                raise ValueError(f"{stage} no quedo marcado como regenerado")
            metrics["regeneration_passed"] += 1
        except Exception as exc:  # noqa: BLE001 - benchmark records failure taxonomy.
            metrics["failures"].append(
                {
                    "stage": f"regeneration:{stage}",
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )


def _run_rollbacks(materializations: list[dict[str, Any]], metrics: dict[str, Any]) -> None:
    selective = materializations[:SELECTIVE_ROLLBACK_DOMAINS]
    for materialization in reversed(selective):
        domain_dir = materialization["domain_dir"]
        try:
            for agent in reversed(materialization["agents"]):
                metrics["rollback_selective_attempted"] += 1
                rollback_sandbox_agent(domain_dir, agent_id=agent["agent_id"])
                metrics["rollback_selective_passed"] += 1
            for rollback in (rollback_paper_seed, rollback_agent_presets, rollback_profile_catalog):
                metrics["rollback_selective_attempted"] += 1
                rollback(domain_dir)
                metrics["rollback_selective_passed"] += 1
        except Exception as exc:  # noqa: BLE001
            metrics["failures"].append(
                {
                    "stage": "selective_rollback",
                    "domain_id": materialization["domain"]["domain_id"],
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )

    for materialization in reversed(materializations):
        metrics["rollback_total_attempted"] += 1
        try:
            result = rollback_domain_materialization(
                manifest_path=materialization["domain"]["manifest_path"],
            )
            if result.get("status") != "rolled_back":
                raise ValueError("rollback total no devolvio status rolled_back")
            metrics["rollback_total_passed"] += 1
        except Exception as exc:  # noqa: BLE001
            metrics["failures"].append(
                {
                    "stage": "total_rollback",
                    "domain_id": materialization["domain"]["domain_id"],
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )


def _validate_agent_boundary(agent: dict[str, Any], metrics: dict[str, Any]) -> None:
    payload = agent["agent"]
    if payload.get("status") == "active" or payload.get("active") is True:
        metrics["runtime_boundary_failures"] += 1
    if payload.get("sandbox_config", {}).get("runtime_enabled") is not False:
        metrics["runtime_boundary_failures"] += 1
    if payload.get("metadata", {}).get("creates_runtime_agent") is not False:
        metrics["runtime_boundary_failures"] += 1
    lineage = agent.get("lineage") or {}
    if not lineage.get("origin") or not lineage.get("history"):
        metrics["lineage_failures"] += 1


def _schema_for_pair(*, index: int, area_id: str, niche_id: str) -> dict[str, Any]:
    schema = json.loads(FIXTURE.read_text(encoding="utf-8"))
    domain_id = f"sandbox_full_{index:03d}_domain"
    schema["domain_id"] = domain_id
    schema["name"] = f"Sandbox Full Benchmark {index:03d}"
    schema["description"] = f"Dominio sandbox sintetico para benchmark full #{index:03d}."
    schema["source_request"] = {
        "domain_id": domain_id,
        "area_id": area_id,
        "niche_id": niche_id,
        "niche_ids": [niche_id],
        "objective": "benchmark largo sandbox 200/200",
        "business_scale": "pyme",
        "complexity_level": "media",
    }
    schema["created_from"] = {
        "type": "manual_request",
        "source": "scripts/run_sandbox_full_benchmark.py",
        "benchmark_id": BENCHMARK_ID,
    }
    schema["metadata"] = {
        **schema.get("metadata", {}),
        "book_prompt": "2.4.2",
        "benchmark_id": BENCHMARK_ID,
        "benchmark_area_id": area_id,
        "benchmark_niche_id": niche_id,
        "operational": False,
    }
    return schema


def _empty_metrics(
    *,
    created_at: str,
    head: str,
    areas: int,
    niches: int,
    combinations: int,
) -> dict[str, Any]:
    return {
        "benchmark_id": BENCHMARK_ID,
        "created_at": created_at,
        "head": head,
        "total_areas_detected": areas,
        "total_niches_detected": niches,
        "total_domain_combinations_detected": combinations,
        "domains_attempted": 0,
        "domains_materialized": 0,
        "domains_failed": 0,
        "profile_catalogs_generated": 0,
        "profiles_generated": 0,
        "agent_presets_generated": 0,
        "paper_seed_generated": 0,
        "sandbox_agents_generated": 0,
        "artifact_manifest_failures": 0,
        "lineage_failures": 0,
        "runtime_boundary_failures": 0,
        "legacy_isolation_failures": 0,
        "rollback_selective_attempted": 0,
        "rollback_selective_passed": 0,
        "rollback_total_attempted": 0,
        "rollback_total_passed": 0,
        "regeneration_attempted": 0,
        "regeneration_passed": 0,
        "duration_seconds": 0,
        "average_seconds_per_domain": 0,
        "result": "",
        "sandbox_root_clean": False,
        "failures": [],
    }


def _classify(metrics: dict[str, Any]) -> str:
    if metrics["runtime_boundary_failures"]:
        return "FAILED_RUNTIME_BOUNDARY"
    if metrics["legacy_isolation_failures"]:
        return "FAILED_ISOLATION"
    if (
        metrics["artifact_manifest_failures"]
        or metrics["lineage_failures"]
        or metrics["domains_failed"]
        or metrics["rollback_total_passed"] != metrics["domains_materialized"]
        or metrics["regeneration_passed"] != metrics["regeneration_attempted"]
    ):
        return "FAILED_ARCHITECTURE"
    if (
        metrics["total_domain_combinations_detected"] == FULL_DOMAIN_TARGET
        and metrics["domains_attempted"] == FULL_DOMAIN_TARGET
        and metrics["domains_materialized"] == FULL_DOMAIN_TARGET
    ):
        return "PASSED_FULL_200"
    return "PARTIAL_SCALE_LIMIT"


def _load_catalog(name: str) -> list[dict[str, Any]]:
    data = json.loads((CATALOGS / name).read_text(encoding="utf-8"))
    return data["profiles"] if isinstance(data, dict) and "profiles" in data else data


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _papers_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted(DOMAINS.glob("*/agents/papers/*.json")):
        digest.update(path.relative_to(DOMAINS).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ejecuta benchmark sandbox full 200/200.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Ruta de metricas JSON.")
    parser.add_argument("--domain-limit", type=int, default=None, help="Limite diagnostico opcional.")
    args = parser.parse_args()

    metrics = run_benchmark(
        output_path=args.output,
        domain_limit=args.domain_limit,
        write_metrics=True,
    )
    print(
        json.dumps(
            {
                "result": metrics["result"],
                "domains_attempted": metrics["domains_attempted"],
                "domains_materialized": metrics["domains_materialized"],
                "domains_failed": metrics["domains_failed"],
                "duration_seconds": metrics["duration_seconds"],
                "output": str(Path(args.output).resolve()),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if metrics["result"] == "PASSED_FULL_200" else 1


if __name__ == "__main__":
    raise SystemExit(main())
