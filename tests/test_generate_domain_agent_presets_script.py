import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
SCRIPT_PATH = ROOT / "scripts" / "generate_domain_agent_presets.py"
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generate_domain_agent_presets_script_exists_and_help_runs():
    assert SCRIPT_PATH.exists()

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Genera agent_presets derivados" in result.stdout


def test_script_runs_for_valid_area_and_niche_without_output():
    before = {path: _sha256(path) for path in DOMAIN_FILES}

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--area",
            "marketing_publicidad",
            "--niche",
            "contenidos_redes",
            "--max-profiles",
            "5",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    after = {path: _sha256(path) for path in DOMAIN_FILES}
    assert "Generated derived agent presets" in result.stdout
    assert "preset_count: 5" in result.stdout
    assert after == before


def test_script_writes_valid_json_output_when_requested(tmp_path):
    output_path = tmp_path / "example_agent_presets.json"
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
            "--capability",
            "contenido",
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
    assert data["artifact_type"] == "derived_domain_agent_presets"
    assert data["metadata"]["source_artifact_type"] == "derived_domain_profile_catalog"
    assert data["presets"]
    assert data["agent_presets"]["presets"]
    assert data["presets"][0]["instructions_seed"]
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
            "domains/loteria/agent_presets.generated.json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "no escribe dentro de domains" in result.stderr
