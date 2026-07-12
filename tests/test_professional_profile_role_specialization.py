import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
CATALOGS_DIR = ROOT / "catalogs"
PROFESSIONAL_PROFILES_PATH = CATALOGS_DIR / "professional_profiles.json"
PENDING_VALUES = {
    "",
    "pending",
    "required",
    "pendiente",
    "por_definir",
    "required_role",
    "required_specialization",
}


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _profiles():
    return _load_json(PROFESSIONAL_PROFILES_PATH)["profiles"]


def test_all_active_professional_profile_role_ids_exist_and_are_active():
    roles_by_id = {
        role["id"]: role
        for role in _load_json(CATALOGS_DIR / "roles.json")
    }
    invalid = []

    for profile in _profiles():
        if not profile["activo"]:
            continue
        role_id = profile["expected_role_id"]
        if role_id not in roles_by_id:
            invalid.append((profile["id"], role_id, "missing"))
        elif roles_by_id[role_id]["activo"] is not True:
            invalid.append((profile["id"], role_id, "inactive"))

    assert invalid == []


def test_all_active_professional_profile_specialization_ids_exist_and_are_active():
    specializations_by_id = {
        specialization["id"]: specialization
        for specialization in _load_json(CATALOGS_DIR / "specializations.json")
    }
    invalid = []

    for profile in _profiles():
        if not profile["activo"]:
            continue
        specialization_id = profile["expected_specialization_id"]
        if specialization_id not in specializations_by_id:
            invalid.append((profile["id"], specialization_id, "missing"))
        elif specializations_by_id[specialization_id]["activo"] is not True:
            invalid.append((profile["id"], specialization_id, "inactive"))

    assert invalid == []


def test_no_active_professional_profiles_keep_pending_role_or_specialization_values():
    offenders = []

    for profile in _profiles():
        if not profile["activo"]:
            continue
        role_id = profile["expected_role_id"]
        specialization_id = profile["expected_specialization_id"]
        if role_id in PENDING_VALUES:
            offenders.append((profile["id"], "expected_role_id", role_id))
        if specialization_id in PENDING_VALUES:
            offenders.append(
                (profile["id"], "expected_specialization_id", specialization_id)
            )

    assert offenders == []


def test_expected_specialization_belongs_to_expected_role():
    specializations_by_id = {
        specialization["id"]: specialization
        for specialization in _load_json(CATALOGS_DIR / "specializations.json")
    }
    mismatches = []

    for profile in _profiles():
        if not profile["activo"]:
            continue
        specialization = specializations_by_id[profile["expected_specialization_id"]]
        if specialization["role_id"] != profile["expected_role_id"]:
            mismatches.append(
                (
                    profile["id"],
                    profile["expected_role_id"],
                    profile["expected_specialization_id"],
                    specialization["role_id"],
                )
            )

    assert mismatches == []


def test_role_and_specialization_catalogs_have_unique_ids():
    roles = _load_json(CATALOGS_DIR / "roles.json")
    specializations = _load_json(CATALOGS_DIR / "specializations.json")
    role_ids = [role["id"] for role in roles]
    specialization_ids = [specialization["id"] for specialization in specializations]

    assert len(role_ids) == len(set(role_ids))
    assert len(specialization_ids) == len(set(specialization_ids))


def test_all_global_roles_are_used_by_professional_profiles():
    roles = _load_json(CATALOGS_DIR / "roles.json")
    used_role_ids = {
        profile["expected_role_id"]
        for profile in _profiles()
        if profile["activo"]
    }

    assert {role["id"] for role in roles if role["activo"]} <= used_role_ids
