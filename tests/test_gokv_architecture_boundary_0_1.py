"""N1 architectural boundary tests for GOKV 0.1."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "GLOBAL_OPERATIONAL_KNOWLEDGE_VAULT_ARCHITECTURE_0_1.md"
PROTECTED = (
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
)


def test_n1_architecture_document_has_explicit_boundaries():
    text = DOC.read_text(encoding="utf-8").casefold()
    for marker in (
        "N1_GOKV_ARCHITECTURAL_BOUNDARY_PASSED",
        "knowledge/global_operational/",
        "boundary table",
        "ownership table",
        "data classification table",
        "MEMORY",
        "CONTEXT",
        "EVIDENCE",
        "LOG",
        "PAPER",
        "PRESET",
        "OPERATIONAL_KNOWLEDGE",
        "OBSERVED -> CANDIDATE -> VALIDATED -> PROMOTED",
        "no se modifican las ocho decisiones",
    ):
        assert marker.casefold() in text, marker


def test_n1_canonical_location_is_separate_from_existing_surfaces():
    text = DOC.read_text(encoding="utf-8").casefold()
    assert "memory/" in text
    assert "core/context_boundary.py" in text
    assert "core/audit_store.py" in text
    assert "gokv/" in text
    assert "runtime integration" in text


def test_n1_protected_product_paths_are_not_in_new_artifacts():
    text = DOC.read_text(encoding="utf-8")
    for path in PROTECTED:
        assert path in text
    assert "api.py`" in text
    assert "No se modifican" in text
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "7cb7134", "HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ).splitlines()
    assert not set(changed) & set(PROTECTED)
