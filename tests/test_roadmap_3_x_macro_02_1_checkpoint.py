"""Integral checkpoint for Macro 02.1 without product-surface changes."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "ad7a3dcac1959aba086c1098b126e8c97b9e32b8"
CHECKPOINT = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_1_CHECKPOINT.md"
EVIDENCE = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_1_CHECKPOINT_EVIDENCE.json"


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def test_checkpoint_documents_integral_boundary_and_exact_evidence():
    document = CHECKPOINT.read_text(encoding="utf-8")
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert "CHECKPOINT_READY_FOR_CONTROLLED_PUBLICATION" in document
    assert evidence["macro_02_commit_count"] == 20
    assert evidence["gokv"]["item_count"] == 32
    assert evidence["gokv"]["status_counts"] == {
        "CANDIDATE": 16,
        "VALIDATED": 9,
        "PROMOTED": 7,
    }
    for marker in (
        "IA_CORE_EXTERNAL_NETWORK_BLOCKED",
        "IA_CORE_TEST_WRITE_BLOCKED",
        "REPOSITORY_TRACKED_STATE_UNCHANGED_AFTER_TESTS",
        "TEST_WRITES_CONTAINED_TO_TEMPORARY_ROOT",
        "No NVIDIA, Ollama, provider, DNS, socket, HTTP",
    ):
        assert marker in document or marker in json.dumps(evidence)


def test_macro_02_history_and_repairs_remain_explicit():
    assert len(_git("rev-list", "--reverse", "fbbc5372865467c4c5de3c09e580644971e2d163.." + BASE).splitlines()) == 20
    assert _git("merge-base", "--is-ancestor", BASE, "HEAD") == ""
    subjects = _git("log", "--format=%s", BASE + "..HEAD").splitlines()
    for subject in (
        "docs(roadmap): add Macro 02 commit accountability ledger",
        "test: enforce hermetic collection and external opt-in",
        "test: contain legacy phantom side effects",
        "test: align legacy probes with current contracts",
        "docs(gokv): reconcile Macro 02.1 learning",
        "docs(method): define Method Santi 3.2.1 hermetic validation",
        "test: repair phantom write isolation",
        "test: align hermetic historical probes",
        "test: make pytest collection deterministic",
        "docs: reconcile phantom isolation evidence",
    ):
        assert subjects.count(subject) == 1


def test_current_macro_02_1_diff_has_no_prohibited_product_surface():
    changed = set(_git("diff", "--name-only", BASE, "HEAD").splitlines())
    prohibited_exact = {
        "api.py",
        "config.py",
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/i18n_es.json",
        "ui/web/admin-panels.js",
        "ui/web/backend-contract-widgets.js",
        "core/backend_internal_ui_payloads.py",
    }
    prohibited_prefixes = (
        "providers/",
        "agents/",
        "domains/",
        "memory/",
        "memoria_agentes/",
        "memoria_vectorial/",
    )
    assert not (changed & prohibited_exact)
    assert not [path for path in changed if path.startswith(prohibited_prefixes)]
    assert all(not path.endswith((".html", ".js")) for path in changed)


def test_diff_has_no_secret_like_material_and_guards_are_fail_closed():
    diff = _git("diff", "--no-ext-diff", "--unified=0", BASE, "HEAD")
    assert not re.search(
        r"(?:nvapi-[A-Za-z0-9]{12,}|sk-[A-Za-z0-9]{12,}|gh[pousr]_[A-Za-z0-9]{12,}|Bearer\s+[A-Za-z0-9._-]{20,})",
        diff,
    )
    guard = (ROOT / "conftest.py").read_text(encoding="utf-8")
    assert "sys.addaudithook(_audit_test_write)" in guard
    assert "IA_CORE_EXTERNAL_NETWORK_BLOCKED" in guard
    assert "IA_CORE_TEST_WRITE_BLOCKED" in guard
