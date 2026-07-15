from pathlib import Path

from scripts.run_sandbox_full_benchmark import FULL_DOMAIN_TARGET, run_benchmark


def test_full_200_sandbox_chain_benchmark(tmp_path):
    output = tmp_path / "sandbox_full_200_benchmark.json"

    metrics = run_benchmark(output_path=output, write_metrics=True)

    assert output.is_file()
    assert metrics["total_areas_detected"] == 30
    assert metrics["total_niches_detected"] == 200
    assert metrics["total_domain_combinations_detected"] == FULL_DOMAIN_TARGET
    assert metrics["domains_attempted"] == FULL_DOMAIN_TARGET
    assert metrics["domains_materialized"] == FULL_DOMAIN_TARGET
    assert metrics["domains_failed"] == 0
    assert metrics["profile_catalogs_generated"] == FULL_DOMAIN_TARGET
    assert metrics["profiles_generated"] > 0
    assert metrics["agent_presets_generated"] == metrics["paper_seed_generated"]
    assert metrics["paper_seed_generated"] == metrics["sandbox_agents_generated"]
    assert metrics["artifact_manifest_failures"] == 0
    assert metrics["lineage_failures"] == 0
    assert metrics["runtime_boundary_failures"] == 0
    assert metrics["legacy_isolation_failures"] == 0
    assert metrics["rollback_selective_attempted"] == metrics["rollback_selective_passed"]
    assert metrics["rollback_total_attempted"] == FULL_DOMAIN_TARGET
    assert metrics["rollback_total_passed"] == FULL_DOMAIN_TARGET
    assert metrics["regeneration_attempted"] == 4
    assert metrics["regeneration_passed"] == 4
    assert metrics["sandbox_root_clean"] is True
    assert metrics["result"] == "PASSED_FULL_200"
    assert not list(Path("domains").glob("sandbox_full_*/domain.json"))
