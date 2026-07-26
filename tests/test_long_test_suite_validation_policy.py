from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LONG_TEST_SUITE_VALIDATION_POLICY.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_long_test_suite_validation_policy_exists_and_is_ready():
    text = _text()

    assert DOC.exists()
    assert "LONG_TEST_SUITE_VALIDATION_POLICY_READY" in text


def test_policy_preserves_monolithic_suite_as_preferred_path():
    text = _text()

    assert "La suite monolítica filtrada sigue siendo la validación preferida" in text
    assert 'python -m pytest tests/ -q -k "not test_ollama_integration and not sandbox_chain_full_benchmark"' in text


def test_policy_allows_equivalent_blocks_after_operational_timeout():
    text = _text()

    assert "timeout operativo sin fallo visible" in text
    assert "validación equivalente por bloques" in text
    assert "todos los bloques deben pasar" in text
    assert "mismo universo filtrado" in text
    assert "total agregado" in text
    assert "git diff --check" in text
    assert "working tree limpio" in text


def test_policy_defines_repeatable_block_segmentation():
    text = _text()

    for phrase in [
        "Bloque 1",
        "Bloque 2",
        "Bloque 3",
        "Sort-Object Name",
        "Select-Object -First 50",
        "Select-Object -Skip 50 -First 50",
        "Select-Object -Skip 100",
        "test_ollama_integration.py",
        "test_sandbox_chain_full_benchmark.py",
    ]:
        assert phrase in text


def test_policy_declares_next_step():
    text = _text()

    assert "PROMPT 3.7 — Auditoría de integración result/history/read model" in text


def test_policy_does_not_modify_operational_boundaries():
    text = _text()

    for boundary in [
        "runtime",
        "stores",
        "lifecycle writes",
        "result store",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "memory persistence",
        "external access",
        "API",
        "UI",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
    ]:
        assert boundary in text


def test_policy_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "runtime_enabled = true",
        "store_writes_enabled = true",
        "lifecycle_writes_enabled = true",
        "result_store_enabled = true",
        "scheduler_enabled = true",
        "worker_enabled = true",
        "queue_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
    ]:
        assert forbidden not in text
