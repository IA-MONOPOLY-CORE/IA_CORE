import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent
CATALOGS = ROOT / "catalogs"
DOCS = ROOT / "docs"
CORE = ROOT / "core"
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
DOMAINS = ROOT / "domains"

CLOSURE_REPORT = DOCS / "PROFESSIONAL_GLOBAL_LIBRARY_BOOK_CLOSURE.md"

CATALOG_FILES = [
    CATALOGS / "areas.json",
    CATALOGS / "niches.json",
    CATALOGS / "professional_profiles.json",
    CATALOGS / "profile_model_policies.json",
    CATALOGS / "roles.json",
    CATALOGS / "specializations.json",
]

HELPER_FILES = [
    CORE / "professional_model_recommendation.py",
    CORE / "professional_profile_catalog_generator.py",
    CORE / "professional_agent_preset_generator.py",
    CORE / "professional_team_template_generator.py",
    CORE / "professional_domain_end_to_end.py",
]

SCRIPT_FILES = [
    SCRIPTS / "generate_professional_profile_matrix.py",
    SCRIPTS / "generate_domain_profile_catalog.py",
    SCRIPTS / "generate_domain_agent_presets.py",
    SCRIPTS / "generate_professional_team_template.py",
    SCRIPTS / "run_professional_domain_end_to_end.py",
    SCRIPTS / "README.md",
]

DOC_FILES = [
    DOCS / "PROFESSIONAL_LIBRARY_DESIGN.md",
    DOCS / "PROFESSIONAL_PROFILES_INITIAL_INVENTORY_CLOSURE.md",
    DOCS / "PROFESSIONAL_PROFILE_AREA_NICHE_MATRIX.md",
    DOCS / "PROFESSIONAL_PROFILE_MODEL_RECOMMENDATION.md",
    DOCS / "GENERATED_DOMAIN_PROFILE_CATALOG.md",
    DOCS / "GENERATED_DOMAIN_AGENT_PRESETS.md",
    DOCS / "GENERATED_PROFESSIONAL_TEAM_TEMPLATES.md",
    DOCS / "PROFESSIONAL_DOMAIN_END_TO_END_VALIDATION.md",
    DOCS / "EXAMPLE_GENERATED_PROFILE_CATALOG.md",
    DOCS / "EXAMPLE_GENERATED_AGENT_PRESETS.md",
    DOCS / "EXAMPLE_GENERATED_TEAM_TEMPLATE.md",
    DOCS / "EXAMPLE_PROFESSIONAL_DOMAIN_END_TO_END.md",
    DOCS / "generated" / "example_professional_domain_end_to_end.json",
    DOCS / "AREA_NICHE_EXPANSION_REPORT.md",
    DOCS / "HISTORICAL_PROFILES_RECOVERY_REPORT.md",
    DOCS / "PROFESSIONAL_PROFILE_COVERAGE_AUDIT.md",
    DOCS / "PROFESSIONAL_PROFILE_ROLE_SPECIALIZATION_AUDIT.md",
    ROOT / "ARCHITECTURE_DECISIONS.md",
]

PREVIOUS_CLOSURE_TESTS = [
    TESTS / "test_professional_profiles.py",
    TESTS / "test_professional_profile_coverage.py",
    TESTS / "test_professional_profile_role_specialization.py",
    TESTS / "test_professional_profiles_inventory_closure.py",
    TESTS / "test_professional_profile_matrix.py",
    TESTS / "test_profile_model_policies.py",
    TESTS / "test_professional_model_recommendation.py",
    TESTS / "test_professional_profile_catalog_generator.py",
    TESTS / "test_generate_domain_profile_catalog_script.py",
    TESTS / "test_professional_agent_preset_generator.py",
    TESTS / "test_generate_domain_agent_presets_script.py",
    TESTS / "test_professional_team_template_generator.py",
    TESTS / "test_generate_professional_team_template_script.py",
    TESTS / "test_professional_domain_end_to_end.py",
    TESTS / "test_run_professional_domain_end_to_end_script.py",
    TESTS / "test_catalogs.py",
    TESTS / "test_profile_preset_consistency.py",
    TESTS / "test_agent_config_schema.py",
]


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _profiles():
    return _load_json(CATALOGS / "professional_profiles.json")["profiles"]


def test_book_closure_report_catalogs_helpers_scripts_docs_and_examples_exist():
    expected = [
        CLOSURE_REPORT,
        *CATALOG_FILES,
        *HELPER_FILES,
        *SCRIPT_FILES,
        *DOC_FILES,
        *PREVIOUS_CLOSURE_TESTS,
    ]

    assert [path for path in expected if not path.exists()] == []


def test_book_closure_final_catalog_metrics_are_stable():
    areas = _load_json(CATALOGS / "areas.json")
    niches = _load_json(CATALOGS / "niches.json")
    roles = _load_json(CATALOGS / "roles.json")
    specializations = _load_json(CATALOGS / "specializations.json")
    policies = _load_json(CATALOGS / "profile_model_policies.json")
    profiles = _profiles()

    covered_areas = {area for profile in profiles for area in profile["areas_compatibles"]}
    covered_niches = {niche for profile in profiles for niche in profile["nichos_compatibles"]}

    assert len(areas) == 30
    assert len(niches) == 200
    assert len(profiles) == 106
    assert len(roles) == 20
    assert len(specializations) == 80
    assert len(policies) == 15
    assert len(covered_areas) == 30
    assert len(covered_niches) >= 160


def test_book_closure_did_not_create_derived_operational_outputs_in_domains():
    forbidden_names = {
        "example_professional_domain",
        "example_domain_growth_pyme",
        "generated_profile_catalog.json",
        "generated_agent_presets.json",
        "generated_team_template.json",
        "professional_domain_end_to_end.json",
    }
    offenders = [
        path.relative_to(ROOT).as_posix()
        for path in DOMAINS.rglob("*")
        if any(name in path.name for name in forbidden_names)
    ]

    assert offenders == []


def test_book_closure_domains_are_not_modified_in_working_tree():
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "domains"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert result.stdout.strip() == ""


def test_book_closure_report_contains_required_key_phrases():
    report = CLOSURE_REPORT.read_text(encoding="utf-8").lower()
    required_phrases = [
        "fuente de verdad",
        "artefacto derivado",
        "no operativo",
        "no se crearon agentes reales",
        "no se crearon papers reales",
        "sin modificar dominios especificos",
    ]

    assert [phrase for phrase in required_phrases if phrase not in report] == []
