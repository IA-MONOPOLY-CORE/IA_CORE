"""Provider/model recommendation for global professional profiles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import config
from core.model_recommendation import (
    HardwareProfile,
    evaluate_model_compatibility,
    get_default_hardware_profile,
)


CATALOGS_DIR = config.ROOT_DIR / "catalogs"
MODEL_POLICIES_PATH = CATALOGS_DIR / "profile_model_policies.json"

LOCAL_LIGHT = ("ollama", "phi3:mini")
LOCAL_STANDARD = ("ollama", "llama3.2:3b")
LOCAL_HEAVY = ("ollama", "llama3.1:8b")
CLOUD_FAST = ("nvidia", "meta/llama-3.1-8b-instruct")
CLOUD_REASONING = ("nvidia", "meta/llama-3.3-70b-instruct")
CLOUD_LONG_CONTEXT = ("nvidia", "meta/llama-4-maverick-17b-128e-instruct")
CLOUD_MULTIMODAL = ("nvidia", "meta/llama-4-maverick-17b-128e-instruct")
CLOUD_RELIABLE = ("nvidia", "meta/llama-3.1-8b-instruct")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile_model_policies(
    policies_path: Path = MODEL_POLICIES_PATH,
) -> dict[str, dict[str, Any]]:
    policies = _load_json(policies_path)
    return {policy["id"]: policy for policy in policies}


def _policy_for_profile(profile: dict[str, Any]) -> dict[str, Any]:
    policies = load_profile_model_policies()
    policy_id = profile["default_model_policy"]
    if policy_id not in policies:
        raise ValueError(f"Policy inexistente para perfil {profile['id']}: {policy_id}")
    return policies[policy_id]


def _execution_for_policy(policy: dict[str, Any], hardware_profile: HardwareProfile) -> str:
    preferred = policy["preferred_execution"]
    if preferred == "local" and policy["id"] == "local_heavy" and hardware_profile.local_mode == "limited":
        return "cloud"
    if preferred == "local" and hardware_profile.local_mode == "limited" and not policy["local_viable"]:
        return "cloud"
    return preferred


def _primary_provider_model(
    policy: dict[str, Any],
    hardware_profile: HardwareProfile,
) -> tuple[str, str]:
    policy_id = policy["id"]

    if policy_id == "local_light":
        return LOCAL_LIGHT
    if policy_id == "local_standard":
        return LOCAL_STANDARD
    if policy_id == "local_heavy":
        return CLOUD_FAST if hardware_profile.local_mode == "limited" else LOCAL_HEAVY
    if policy_id == "cloud_reasoning":
        return CLOUD_REASONING
    if policy_id == "cloud_low_latency":
        return CLOUD_FAST
    if policy_id == "hybrid":
        return CLOUD_FAST if hardware_profile.local_mode == "limited" else LOCAL_STANDARD
    if policy_id == "privacy_sensitive":
        return LOCAL_STANDARD
    if policy_id == "long_context":
        return CLOUD_LONG_CONTEXT
    if policy_id == "multimodal":
        return CLOUD_MULTIMODAL
    if policy_id == "batch_analysis":
        return CLOUD_FAST if hardware_profile.local_mode == "limited" else LOCAL_HEAVY
    if policy_id == "cost_sensitive":
        return LOCAL_LIGHT
    if policy_id == "high_reliability":
        return CLOUD_RELIABLE
    if policy_id == "fast_iteration":
        return LOCAL_LIGHT
    if policy_id == "offline_capable":
        return LOCAL_LIGHT
    if policy_id == "human_review_required":
        return CLOUD_RELIABLE

    return CLOUD_FAST


def _fallback_provider_model(
    policy: dict[str, Any],
    hardware_profile: HardwareProfile,
) -> tuple[str, str]:
    policy_id = policy["id"]

    if policy_id in {"local_light", "local_standard", "cost_sensitive", "fast_iteration", "offline_capable"}:
        return CLOUD_FAST
    if policy_id in {"privacy_sensitive", "human_review_required"}:
        return LOCAL_STANDARD
    if policy_id == "long_context":
        return CLOUD_REASONING
    if policy_id == "multimodal":
        return CLOUD_REASONING
    if policy_id == "local_heavy" and hardware_profile.local_mode == "limited":
        return LOCAL_LIGHT
    if policy_id in {"cloud_reasoning", "cloud_low_latency", "high_reliability"}:
        return LOCAL_STANDARD
    if policy_id in {"hybrid", "batch_analysis"}:
        return LOCAL_STANDARD if hardware_profile.local_mode == "limited" else CLOUD_FAST

    return LOCAL_STANDARD


def _human_review_required(profile: dict[str, Any], policy: dict[str, Any]) -> bool:
    return bool(
        policy["human_review_required"]
        or profile["default_model_policy"] == "human_review_required"
        or profile["default_model_policy"] == "privacy_sensitive"
    )


def _is_privacy_sensitive(profile: dict[str, Any], policy: dict[str, Any]) -> bool:
    return bool(
        profile["default_model_policy"] == "privacy_sensitive"
        or policy["privacy_requirement"] == "high"
    )


def recommend_model_for_professional_profile(
    profile: dict[str, Any],
    hardware_profile: HardwareProfile | None = None,
) -> dict[str, Any]:
    """Return a deterministic provider/model recommendation for a professional profile."""
    hardware_profile = hardware_profile or get_default_hardware_profile()
    policy = _policy_for_profile(profile)
    recommended_execution = _execution_for_policy(policy, hardware_profile)
    provider, model = _primary_provider_model(policy, hardware_profile)
    fallback_provider, fallback_model = _fallback_provider_model(policy, hardware_profile)
    compatibility = evaluate_model_compatibility(provider, model, hardware_profile)

    reason = (
        f"Policy {policy['id']} usa ejecucion {recommended_execution}; "
        f"carga={profile['cognitive_load']}, razonamiento={profile['reasoning_style']}, "
        f"hardware={hardware_profile.local_mode}."
    )
    if policy["id"] == "local_heavy" and hardware_profile.local_mode == "limited":
        reason += " Hardware local limitado: se recomienda cloud y fallback local liviano."
    if policy["cloud_recommended"] and recommended_execution in {"cloud", "hybrid"}:
        reason += " Cloud recomendado por la policy."

    return {
        "profile_id": profile["id"],
        "model_policy": policy["id"],
        "recommended_execution": recommended_execution,
        "recommended_provider": provider,
        "recommended_model": model,
        "fallback_provider": fallback_provider,
        "fallback_model": fallback_model,
        "fallback_policy": policy["fallback_policy"],
        "reason": reason,
        "requires_human_review": _human_review_required(profile, policy),
        "privacy_sensitive": _is_privacy_sensitive(profile, policy),
        "hardware_note": compatibility["hardware_reason"],
        "compatibility": compatibility["compatibility"],
        "policy": {
            "preferred_execution": policy["preferred_execution"],
            "recommended_provider_tier": policy["recommended_provider_tier"],
            "local_viable": policy["local_viable"],
            "cloud_recommended": policy["cloud_recommended"],
        },
    }


def recommend_models_for_all_professional_profiles(
    profiles: list[dict[str, Any]],
    hardware_profile: HardwareProfile | None = None,
) -> list[dict[str, Any]]:
    hardware_profile = hardware_profile or get_default_hardware_profile()
    return [
        recommend_model_for_professional_profile(profile, hardware_profile=hardware_profile)
        for profile in profiles
    ]
