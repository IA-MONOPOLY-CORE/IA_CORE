import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
SCRIPT_PATH = ROOT / "scripts" / "generate_domain_profile_catalog.py"
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generate_domain_profile_catalog_script_exists():
    assert SCRIPT_PATH.exists()


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
            "--max-profiles",
            "5",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    after = {path: _sha256(path) for path in DOMAIN_FILES}
    assert "Generated derived profile catalog" in result.stdout
    assert "candidate_count: 5" in result.stdout
    assert after == before


def test_script_writes_valid_json_output_when_requested(tmp_path):
    output_path = tmp_path / "example_profile_catalog.json"
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
            "--model-policy",
            "cloud_low_latency",
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
    assert output_path.exists()
    assert "output:" in result.stdout
    assert data["artifact_type"] == "derived_domain_profile_catalog"
    assert data["metadata"]["area_id"] == "marketing_publicidad"
    assert data["generated_from"]["professional_profiles"] == "catalogs/professional_profiles.json"
    assert data["profiles"]
    assert data["profile_catalog"]["roles"]
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
            "domains/loteria/profile_catalog.generated.json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "no escribe dentro de domains" in result.stderr
