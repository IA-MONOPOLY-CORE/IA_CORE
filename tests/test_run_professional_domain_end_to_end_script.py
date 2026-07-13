import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "run_professional_domain_end_to_end.py"
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]
AGENTS_DIR = ROOT / "domains" / "loteria" / "agents"


def _hashes():
    return {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in DOMAIN_FILES}


def _agent_files():
    return sorted(path.relative_to(AGENTS_DIR) for path in AGENTS_DIR.rglob("*") if path.is_file())


def _command():
    return [sys.executable, str(SCRIPT), "--area", "marketing_publicidad", "--niche", "contenidos_redes", "--business-scale", "pyme", "--objective", "growth", "--max-profiles", "5", "--max-presets", "5", "--domain-id", "example_domain_growth_pyme"]


def test_script_exists_and_help_runs():
    assert SCRIPT.exists()
    result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=ROOT, text=True, capture_output=True, check=True)
    assert "Valida la cadena profesional end-to-end" in result.stdout


def test_script_runs_valid_example_without_touching_domains():
    before = _hashes()
    agents_before = _agent_files()
    result = subprocess.run(_command(), cwd=ROOT, text=True, capture_output=True, check=True)
    assert "Professional domain end-to-end validation completed" in result.stdout
    assert "profile_count: 5" in result.stdout
    assert "preset_count: 5" in result.stdout
    assert _hashes() == before
    assert _agent_files() == agents_before


def test_script_writes_valid_json_to_safe_path(tmp_path):
    output = tmp_path / "end_to_end.json"
    before = _hashes()
    result = subprocess.run(_command() + ["--output", str(output)], cwd=ROOT, text=True, capture_output=True, check=True)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert "output:" in result.stdout
    assert data["metadata"]["operational"] is False
    assert data["profile_catalog"]["profiles"]
    assert data["agent_presets"]["presets"]
    assert data["team_template"]["recommended_preset_ids"]
    assert data["activation_plan"]
    assert _hashes() == before


def test_script_rejects_domains_output():
    result = subprocess.run(_command() + ["--output", "domains/loteria/end_to_end.json"], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode != 0
    assert "no escribe dentro de domains" in result.stderr
