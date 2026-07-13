import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
POLICIES_PATH = ROOT / "catalogs" / "profile_model_policies.json"
PROFILES_PATH = ROOT / "catalogs" / "professional_profiles.json"

REQUIRED_POLICY_FIELDS = {
    "id",
    "nombre",
    "descripcion",
    "use_cases",
    "preferred_execution",
    "cognitive_requirement",
    "latency_requirement",
    "cost_sensitivity",
    "privacy_requirement",
    "context_requirement",
    "reliability_requirement",
    "human_review_required",
    "local_viable",
    "cloud_recommended",
    "fallback_policy",
    "recommended_provider_tier",
    "notes",
    "status",
    "activo",
}
EXPECTED_POLICIES = {
    "local_light",
    "local_standard",
    "local_heavy",
    "cloud_reasoning",
    "cloud_low_latency",
    "hybrid",
    "privacy_sensitive",
    "long_context",
    "multimodal",
    "batch_analysis",
    "cost_sensitive",
    "high_reliability",
    "fast_iteration",
    "offline_capable",
    "human_review_required",
}
VALID_EXECUTIONS = {"local", "cloud", "hybrid"}


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_profile_model_policies_catalog_exists_and_has_expected_policies():
    assert POLICIES_PATH.exists()
    policies = _load_json(POLICIES_PATH)
    ids = [policy["id"] for policy in policies]

    assert len(policies) == 15
    assert set(ids) == EXPECTED_POLICIES
    assert len(ids) == len(set(ids))


def test_all_profile_model_policies_are_active_complete_and_operational():
    invalid = []

    for policy in _load_json(POLICIES_PATH):
        missing = REQUIRED_POLICY_FIELDS - set(policy)
        if missing:
            invalid.append((policy["id"], "missing", sorted(missing)))
        if policy["status"] != "active":
            invalid.append((policy["id"], "status", policy["status"]))
        if policy["activo"] is not True:
            invalid.append((policy["id"], "activo", policy["activo"]))
        if policy["preferred_execution"] not in VALID_EXECUTIONS:
            invalid.append((policy["id"], "preferred_execution", policy["preferred_execution"]))
        if not policy["use_cases"]:
            invalid.append((policy["id"], "use_cases"))
        if not policy["fallback_policy"]:
            invalid.append((policy["id"], "fallback_policy"))
        if not isinstance(policy["local_viable"], bool):
            invalid.append((policy["id"], "local_viable"))
        if not isinstance(policy["cloud_recommended"], bool):
            invalid.append((policy["id"], "cloud_recommended"))

    assert invalid == []


def test_all_profile_model_policy_fallbacks_exist():
    policies = _load_json(POLICIES_PATH)
    policy_ids = {policy["id"] for policy in policies}
    invalid = [
        (policy["id"], policy["fallback_policy"])
        for policy in policies
        if policy["fallback_policy"] not in policy_ids
    ]

    assert invalid == []


def test_all_professional_profile_model_policies_exist():
    policies = {policy["id"] for policy in _load_json(POLICIES_PATH)}
    profiles = _load_json(PROFILES_PATH)["profiles"]
    invalid = [
        (profile["id"], profile["default_model_policy"])
        for profile in profiles
        if profile["default_model_policy"] not in policies
    ]

    assert invalid == []


def test_profile_model_policies_define_local_and_cloud_behavior():
    invalid = []

    for policy in _load_json(POLICIES_PATH):
        if policy["preferred_execution"] == "local" and not policy["local_viable"]:
            invalid.append((policy["id"], "local_without_local_viable"))
        if policy["preferred_execution"] == "cloud" and not policy["cloud_recommended"]:
            invalid.append((policy["id"], "cloud_without_cloud_recommended"))
        if policy["recommended_provider_tier"] == "":
            invalid.append((policy["id"], "recommended_provider_tier"))

    assert invalid == []
