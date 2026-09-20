from pathlib import Path

from scripts.run_mission_closure_v2_2_1 import LevelAPlugin


ROOT = Path(__file__).resolve().parents[1]


def test_level_a_plugin_records_collection_and_all_three_phases():
    plugin = LevelAPlugin()
    plugin.pytest_collection_finish(type("Session", (), {"items": [type("Item", (), {"nodeid": "fixture::test"})()]})())
    report = type("Report", (), {"nodeid": "fixture::test", "when": "setup", "outcome": "passed", "duration": 0.01})()
    plugin.pytest_runtest_logreport(report)
    for phase in ("call", "teardown"):
        report.when = phase
        plugin.pytest_runtest_logreport(report)
    result = plugin.results["fixture::test"]
    assert plugin.nodeids == ["fixture::test"]
    assert result["setup"] == result["call"] == result["teardown"] == "passed"


def test_level_a_command_is_the_full_repository_suite():
    source = (ROOT / "scripts" / "run_mission_closure_v2_2_1.py").read_text(encoding="utf-8")
    assert 'pytest.main(["tests/", "-q", "--disable-warnings"]' in source
