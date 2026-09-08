import json
from pathlib import Path
import subprocess
import sys

from gokv.storage import default_paths


ROOT = Path(__file__).resolve().parents[1]


def _run_cli(*args: str, repo_root: Path | None = None) -> dict:
    command = [sys.executable, "-m", "gokv"]
    if repo_root is not None:
        command.extend(["--repo-root", str(repo_root)])
    command.extend(args)
    completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def test_cli_validates_canonical_vault_and_compiles_explicit_pack():
    validation = _run_cli("validate")
    assert validation["valid"] is True
    assert validation["item_count"] == 23

    shown = _run_cli("show-item", "internal_gates")
    assert shown["knowledge_id"] == "internal_gates"

    fixture = ROOT / "tests" / "fixtures" / "gokv" / "fixture_c_tag_filter.json"
    pack = _run_cli("compile-pack", str(fixture))
    assert pack["mode"] == "DEVELOPMENT_VALIDATED"
    assert pack["applicable_knowledge_ids"] == [
        "controlled_assembled_block_execution",
        "internal_gates",
    ]


def test_cli_add_candidate_rebuilds_isolated_registry():
    import tempfile

    source = ROOT / "knowledge" / "global_operational" / "items" / "model_sufficiency_over_maximum_model.json"
    with tempfile.TemporaryDirectory() as directory:
        repo_root = Path(directory)
        item_path = repo_root / "candidate.json"
        item_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        result = _run_cli("add-candidate", str(item_path), repo_root=repo_root)
        assert result["knowledge_id"] == "model_sufficiency_over_maximum_model"
        validation = _run_cli("validate", repo_root=repo_root)
        assert validation["item_count"] == 1


def test_checkpoint_and_protocol_document_exact_readiness_and_scope():
    checkpoint = (ROOT / "docs" / "GOKV_BOOTSTRAP_CHECKPOINT_0_1.md").read_text(encoding="utf-8")
    protocol = (ROOT / "docs" / "GOKV_CONTINUOUS_DEVELOPMENT_CAPTURE_PROTOCOL_V1.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "N8_GOKV_BOOTSTRAP_CHECKPOINT_PASSED" in checkpoint
    assert "IA_CORE_GLOBAL_OPERATIONAL_KNOWLEDGE_VAULT_BOOTSTRAP_0_1_PASSED" in checkpoint
    assert "ready_for_continuous_development_knowledge_capture_v1" in checkpoint
    assert "python -m gokv add-candidate" in protocol
    assert "python -m gokv compile-pack" in protocol
    assert "UI/UX 1.200 no fue ejecutado" in readme


def test_protocol_does_not_mark_product_integration_as_ready():
    checkpoint = (ROOT / "docs" / "GOKV_BOOTSTRAP_CHECKPOINT_0_1.md").read_text(encoding="utf-8")

    assert "Runtime integration | not implemented" in checkpoint
    assert "Agent consumption | not implemented" in checkpoint
    assert "Autonomous promotion | not implemented" in checkpoint
    assert "Embeddings/vector DB/RAG | not implemented" in checkpoint
