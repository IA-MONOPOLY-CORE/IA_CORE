import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
SCRIPT_PATH = ROOT / "scripts" / "generate_professional_profile_matrix.py"
MATRIX_PATH = ROOT / "docs" / "PROFESSIONAL_PROFILE_AREA_NICHE_MATRIX.md"
DOMAIN_FILES = [
    ROOT / "domains" / "loteria" / "profile_catalog.json",
    ROOT / "domains" / "loteria" / "agent_presets.json",
]


def _load_matrix_module():
    spec = importlib.util.spec_from_file_location(
        "generate_professional_profile_matrix",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_professional_profile_matrix_script_exists_and_runs_without_domain_changes():
    assert SCRIPT_PATH.exists()
    before = {path: _sha256(path) for path in DOMAIN_FILES}

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    after = {path: _sha256(path) for path in DOMAIN_FILES}
    assert result.stdout.strip() == "Generated docs\\PROFESSIONAL_PROFILE_AREA_NICHE_MATRIX.md"
    assert after == before


def test_professional_profile_matrix_markdown_is_current():
    module = _load_matrix_module()
    expected = module.render_markdown(module.build_matrix(ROOT))

    assert MATRIX_PATH.exists()
    assert MATRIX_PATH.read_text(encoding="utf-8") == expected


def test_professional_profile_matrix_summary_matches_catalogs():
    module = _load_matrix_module()
    matrix = module.build_matrix(ROOT)
    content = MATRIX_PATH.read_text(encoding="utf-8")

    assert len(matrix["profiles"]) == 106
    assert len(matrix["areas"]) == 30
    assert len(matrix["niches"]) == 200
    assert len(matrix["covered_areas"]) == 30
    assert len(matrix["uncovered_areas"]) == 0
    assert len(matrix["covered_niches"]) == 166
    assert len(matrix["uncovered_niches"]) == 34
    assert (
        "<!-- MATRIX_SUMMARY profiles=106 areas=30 niches=200 "
        "covered_areas=30 uncovered_areas=0 covered_niches=166 uncovered_niches=34 -->"
    ) in content


def test_professional_profile_matrix_references_existing_areas_and_niches():
    module = _load_matrix_module()
    matrix = module.build_matrix(ROOT)
    area_ids = set(matrix["areas_by_id"])
    niche_ids = set(matrix["niches_by_id"])

    invalid_areas = []
    invalid_niches = []
    for profile in matrix["profiles"]:
        invalid_areas.extend(
            (profile["id"], area_id)
            for area_id in profile["areas_compatibles"]
            if area_id not in area_ids
        )
        invalid_niches.extend(
            (profile["id"], niche_id)
            for niche_id in profile["nichos_compatibles"]
            if niche_id not in niche_ids
        )

    assert invalid_areas == []
    assert invalid_niches == []


def test_professional_profile_matrix_area_and_niche_coverage_matches_profiles():
    module = _load_matrix_module()
    matrix = module.build_matrix(ROOT)

    real_covered_areas = {
        area_id
        for profile in matrix["profiles"]
        for area_id in profile["areas_compatibles"]
        if area_id in matrix["areas_by_id"]
    }
    real_covered_niches = {
        niche_id
        for profile in matrix["profiles"]
        for niche_id in profile["nichos_compatibles"]
        if niche_id in matrix["niches_by_id"]
    }

    assert matrix["covered_areas"] == real_covered_areas
    assert matrix["covered_niches"] == real_covered_niches
    assert matrix["uncovered_areas"] == sorted(set(matrix["areas_by_id"]) - real_covered_areas)
    assert matrix["uncovered_niches"] == sorted(set(matrix["niches_by_id"]) - real_covered_niches)
