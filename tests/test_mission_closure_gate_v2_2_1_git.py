from pathlib import Path

import pytest

from scripts import closure_assurance_v2_2_1 as gate


ROOT = Path(__file__).resolve().parents[1]


def test_archival_gate_rejects_dirty_worktree(tmp_path: Path):
    repo = tmp_path / "repo"
    import subprocess
    subprocess.run(["git", "init", str(repo)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    (repo / "README.md").write_text("initial\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "fixture"], check=True, stdout=subprocess.DEVNULL)
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    (repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    with pytest.raises(gate.AssuranceFailure, match="clean working tree"):
        gate.validate_archival_read_only(repo, archival_head=head, terminal_basis=head, allowlist=set(), protected_prefixes=())
