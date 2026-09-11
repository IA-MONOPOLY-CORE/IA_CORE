"""Focused guards for hermetic collection and external-provider containment."""

from __future__ import annotations

import importlib
import os
import socket
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_default_network_guard_fails_closed_before_provider_calls():
    with pytest.raises(RuntimeError, match="IA_CORE_EXTERNAL_NETWORK_BLOCKED"):
        socket.create_connection(("203.0.113.10", 443), timeout=0.01)


def test_provider_import_is_collection_safe_and_does_not_instantiate_client():
    module = importlib.import_module("providers.nvidia_provider")
    assert module.NvidiaProvider
    assert not hasattr(module, "p")


def test_external_probes_are_explicitly_skipped_by_default():
    env = os.environ.copy()
    env.pop("IA_CORE_ALLOW_EXTERNAL_TESTS", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "test_respuesta.py",
            "tests/test_ollama_integration.py",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "skipped" in result.stdout


def test_legacy_root_scripts_are_safe_to_collect():
    env = os.environ.copy()
    env.pop("IA_CORE_ALLOW_EXTERNAL_TESTS", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "test_debate.py",
            "test_respuesta.py",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR" not in result.stdout
    assert "ERROR" not in result.stderr


def test_legacy_external_source_reads_credentials_only_inside_opt_in_test():
    response_source = (ROOT / "test_respuesta.py").read_text(encoding="utf-8")
    assert "NVIDIA_API_KEY" in response_source
    assert "NvidiaProvider(api_key=NVIDIA_API_KEY)" in response_source
    assert "if not _external_tests_enabled()" in response_source
    assert "Generando respuesta..." not in response_source
