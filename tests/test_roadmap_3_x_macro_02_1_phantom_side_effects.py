"""Guards proving that legacy test persistence is temporary and fail-closed."""

from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_protected_repository_persistence_write_fails_immediately():
    target = ROOT / "memory" / "macro_02_1_forbidden_write.json"
    with pytest.raises(RuntimeError, match="IA_CORE_TEST_WRITE_BLOCKED"):
        target.write_text("{}", encoding="utf-8")
    assert not target.exists()


def test_legacy_persistence_helpers_are_redirected_to_tmp_path(tmp_path):
    import config
    import core.herramientas as herramientas
    import core.memoria_perpetua as memoria_perpetua

    expected_root = tmp_path.resolve()
    assert config.MEMORY_STATE_FILE.resolve().is_relative_to(expected_root)
    assert herramientas.HERRAMIENTAS_PATH.resolve().is_relative_to(expected_root)
    assert memoria_perpetua.MEMORIA_BASE.resolve().is_relative_to(expected_root)
    assert memoria_perpetua.MEMORIA_VECTORIAL_BASE.resolve().is_relative_to(expected_root)


def test_test_writes_are_contained_to_temporary_root(tmp_path):
    path = tmp_path / "memory" / "contained.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    assert path.resolve().is_relative_to(tmp_path.resolve())


def test_side_effect_contract_is_documented():
    document = (
        ROOT / "docs" / "ROADMAP_3_X_MACRO_02_1_PHANTOM_SIDE_EFFECT_CONTAINMENT.md"
    ).read_text(encoding="utf-8")
    assert "REPOSITORY_TRACKED_STATE_UNCHANGED_AFTER_TESTS" in document
    assert "TEST_WRITES_CONTAINED_TO_TEMPORARY_ROOT" in document
    assert "IA_CORE_TEST_WRITE_BLOCKED" in document
