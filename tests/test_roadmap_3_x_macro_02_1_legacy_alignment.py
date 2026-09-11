"""Guards for legacy-test disposition and current-contract alignment."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_legacy_disposition_is_explicit_and_non_silent():
    document = (
        ROOT / "docs" / "ROADMAP_3_X_MACRO_02_1_LEGACY_TEST_ALIGNMENT.md"
    ).read_text(encoding="utf-8")
    for decision in (
        "ALIGN_WITH_CURRENT_CONTRACT",
        "ISOLATE_AS_EXPLICIT_LEGACY_TEST",
        "IA_CORE_ALLOW_EXTERNAL_TESTS=1",
        "No test is silently skipped",
    ):
        assert decision in document


def test_root_legacy_scripts_use_safe_import_boundaries():
    debate = (ROOT / "test_debate.py").read_text(encoding="utf-8")
    response = (ROOT / "test_respuesta.py").read_text(encoding="utf-8")
    assert "from supervisor import Supervisor" not in debate
    assert "from core.supervisor import Supervisor" in debate
    assert "if os.environ.get(\"IA_CORE_ALLOW_EXTERNAL_TESTS\") != \"1\":" in debate
    assert "@pytest.mark.external" in response
    assert "if not _external_tests_enabled():" in response


def test_admin_assertions_target_current_contract_evidence():
    tests = (ROOT / "tests" / "test_api_admin_panels.py").read_text(encoding="utf-8")
    html = (ROOT / "ui" / "web" / "index.html").read_text(encoding="utf-8")
    assert '"PANEL MAESTRO / DOCUMENTARY CONSOLE" in html' in tests
    assert "section === 'providers'" in tests
    assert "PANEL MAESTRO / DOCUMENTARY CONSOLE" in html
    assert "providersLoadPromise" in html
