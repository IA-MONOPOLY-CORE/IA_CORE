import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
SCRIPT_PATH = ROOT / "scripts" / "generate_professional_team_template.py"
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generate_professional_team_template_script_exists_and_help_runs():
    assert SCRIPT_PATH.exists()

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Genera una plantilla de equipo profesional derivada" in result.stdout


def test_script_runs_for_valid_example_without_output():
    before = {path: _sha256(path) for path in DOMAIN_FILES}

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--area",
            "marketing_publicidad",
            "--niche",
            "contenidos_redes",
            "--business-scale",
            "pyme",
            "--objective",
            "growth",
            "--max-profiles",
            "5",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    after = {path: _sha256(path) for path in DOMAIN_FILES}
    assert "Generated derived professional team template" in result.stdout
    assert "profile_count: 5" in result.stdout
    assert "preset_count: 5" in result.stdout
    assert after == before


def test_script_writes_valid_json_output_when_requested(tmp_path):
    output_path = tmp_path / "example_team_template.json"
    before = {path: _sha256(path) for path in DOMAIN_FILES}

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--area",
            "marketing_publicidad",
            "--niche",
            "contenidos_redes",
            "--business-scale",
            "pyme",
            "--objective",
            "growth",
            "--max-profiles",
            "5",
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    after = {path: _sha256(path) for path in DOMAIN_FILES}
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert "output:" in result.stdout
    assert data["artifact_type"] == "derived_professional_team_template"
    assert data["metadata"]["area_id"] == "marketing_publicidad"
    assert data["team_template"]["recommended_profile_ids"]
    assert data["team_template"]["recommended_preset_ids"]
    assert data["team_template"]["model_policy_mix"]
    assert after == before


def test_script_rejects_output_inside_domains():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--area",
            "marketing_publicidad",
            "--niche",
            "contenidos_redes",
            "--output",
            "domains/loteria/team_template.generated.json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "no escribe dentro de domains" in result.stderr
