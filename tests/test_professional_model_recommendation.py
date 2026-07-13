import json
from pathlib import Path

from core.model_recommendation import HardwareProfile
from core.professional_model_recommendation import (
    recommend_model_for_professional_profile,
    recommend_models_for_all_professional_profiles,
)


ROOT = Path(__file__).parent.parent
PROFILES_PATH = ROOT / "catalogs" / "professional_profiles.json"


def _profiles():
    return json.loads(PROFILES_PATH.read_text(encoding="utf-8"))["profiles"]


def _profile(profile_id: str):
    return next(profile for profile in _profiles() if profile["id"] == profile_id)


def _limited_hardware():
    return HardwareProfile(
        cpu="Ryzen 7 7730U",
        ram_gb=16,
        gpu=False,
        local_mode="limited",
        source="test",
    )


def _high_end_hardware():
    return HardwareProfile(
        cpu="Ryzen 9",
        ram_gb=64,
        gpu=True,
        gpu_name="RTX 4090",
        local_mode="high_end",
        source="test",
    )


def test_all_professional_profiles_receive_model_recommendation():
    recommendations = recommend_models_for_all_professional_profiles(
        _profiles(),
        hardware_profile=_limited_hardware(),
    )

    assert len(recommendations) == 106
    for recommendation in recommendations:
        assert recommendation["profile_id"]
        assert recommendation["model_policy"]
        assert recommendation["recommended_execution"] in {"local", "cloud", "hybrid"}
        assert recommendation["recommended_provider"]
        assert recommendation["recommended_model"]
        assert recommendation["fallback_provider"]
        assert recommendation["fallback_model"]
        assert recommendation["reason"]
        assert recommendation["hardware_note"]
        assert recommendation["compatibility"] in {
            "compatible",
            "warning",
            "blocked",
            "cloud_available",
            "unknown",
        }


def test_human_review_required_policy_is_respected():
    profile = _profile("analista_operaciones_mineria_energia")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "human_review_required"
    assert recommendation["requires_human_review"] is True
    assert recommendation["fallback_provider"]


def test_privacy_sensitive_policy_is_marked_correctly():
    profile = _profile("auditor_privacidad_datos")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "privacy_sensitive"
    assert recommendation["privacy_sensitive"] is True
    assert recommendation["requires_human_review"] is True
    assert recommendation["recommended_provider"] == "ollama"


def test_cloud_reasoning_recommends_cloud_or_hybrid():
    profile = _profile("estratega_negocio_digital")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "cloud_reasoning"
    assert recommendation["recommended_execution"] in {"cloud", "hybrid"}
    assert recommendation["recommended_provider"] == "nvidia"


def test_local_light_recommends_local_when_hardware_allows_it():
    profile = _profile("creador_contenido_negocio_local")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "local_light"
    assert recommendation["recommended_execution"] == "local"
    assert recommendation["recommended_provider"] == "ollama"
    assert recommendation["compatibility"] == "compatible"


def test_local_heavy_falls_back_to_cloud_when_hardware_is_limited():
    profile = _profile("especialista_bi_dashboards")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "local_heavy"
    assert recommendation["recommended_execution"] == "cloud"
    assert recommendation["recommended_provider"] == "nvidia"
    assert recommendation["fallback_provider"] == "ollama"
    assert "limitado" in recommendation["reason"].lower()


def test_local_heavy_can_use_local_on_high_end_hardware():
    profile = _profile("especialista_bi_dashboards")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_high_end_hardware(),
    )

    assert recommendation["recommended_execution"] == "local"
    assert recommendation["recommended_provider"] == "ollama"


def test_batch_analysis_has_coherent_hybrid_recommendation():
    profile = _profile("analista_datos_negocio")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "batch_analysis"
    assert recommendation["recommended_execution"] == "hybrid"
    assert recommendation["recommended_provider"] == "nvidia"


def test_long_context_uses_long_context_cloud_model():
    profile = _profile("especialista_base_conocimiento")
    recommendation = recommend_model_for_professional_profile(
        profile,
        hardware_profile=_limited_hardware(),
    )

    assert profile["default_model_policy"] == "long_context"
    assert recommendation["recommended_provider"] == "nvidia"
    assert "maverick" in recommendation["recommended_model"]


def test_professional_recommendation_does_not_touch_domain_catalogs():
    domain_profile_catalog = ROOT / "domains" / "loteria" / "profile_catalog.json"
    domain_agent_presets = ROOT / "domains" / "loteria" / "agent_presets.json"

    before = {
        "profile_catalog": domain_profile_catalog.read_text(encoding="utf-8"),
        "agent_presets": domain_agent_presets.read_text(encoding="utf-8"),
    }
    recommend_models_for_all_professional_profiles(
        _profiles(),
        hardware_profile=_limited_hardware(),
    )
    after = {
        "profile_catalog": domain_profile_catalog.read_text(encoding="utf-8"),
        "agent_presets": domain_agent_presets.read_text(encoding="utf-8"),
    }

    assert after == before
