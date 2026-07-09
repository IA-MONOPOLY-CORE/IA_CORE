"""Tests para el módulo de recomendación de modelos."""

import pytest

from core.model_recommendation import (
    HardwareProfile,
    AgentWorkloadClassification,
    ModelRecommendation,
    get_hardware_profile,
    get_default_hardware_profile,
    classify_agent_model_need,
    recommend_provider_model,
    _is_cloud_provider,
    _is_local_provider,
    _select_best_model_for_workload,
)


class TestHardwareProfile:
    """Tests para el perfil de hardware."""

    def test_get_hardware_profile_from_config(self):
        """El perfil de hardware debe cargarse desde config si existe."""
        profile = get_hardware_profile()

        # Como existe config/hardware_profile.json, debe usar ese
        assert profile.cpu == "Ryzen 7 7730U"
        assert profile.ram_gb == 16
        assert profile.gpu is False
        assert profile.local_mode == "limited"
        assert profile.source == "manual_config"

    def test_get_default_hardware_profile_compatibility(self):
        """get_default_hardware_profile debe mantener compatibilidad."""
        profile = get_default_hardware_profile()

        # Debe usar el mismo perfil que get_hardware_profile
        assert profile.cpu == "Ryzen 7 7730U"
        assert profile.ram_gb == 16
        assert profile.gpu is False
        assert profile.local_mode == "limited"


class TestAgentClassification:
    """Tests para la clasificación de agentes."""
    
    def test_classify_loteria_auditor_heavy(self):
        """Auditor de Lotería debe ser workload heavy."""
        classification = classify_agent_model_need(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
        )
        
        assert classification.workload == "heavy"
        assert classification.recommended_execution == "cloud_preferred"
        assert classification.reasoning_need == "high"
    
    def test_classify_loteria_simulador_heavy(self):
        """Simulador de Lotería debe ser workload heavy."""
        classification = classify_agent_model_need(
            domain_id="loteria",
            role_id="simulador",
            specialization_id="simulacion_escenarios",
        )
        
        assert classification.workload == "heavy"
        assert classification.recommended_execution == "cloud_preferred"
        assert classification.reasoning_need == "high"
    
    def test_classify_loteria_integrador_central_heavy(self):
        """Integrador central debe ser workload heavy."""
        classification = classify_agent_model_need(
            domain_id="loteria",
            role_id="integrador_central",
            specialization_id="integracion_perspectivas",
        )
        
        assert classification.workload == "heavy"
        assert classification.recommended_execution == "cloud_preferred"
    
    def test_classify_loteria_analista_medium(self):
        """Analista de Lotería debe ser workload medium."""
        classification = classify_agent_model_need(
            domain_id="loteria",
            role_id="analista",
            specialization_id="analisis_datos",
        )
        
        assert classification.workload == "medium"
        assert classification.recommended_execution == "cloud_preferred"
        assert classification.reasoning_need == "medium"
    
    def test_classify_loteria_archivista_light(self):
        """Archivista debe ser workload light."""
        classification = classify_agent_model_need(
            domain_id="loteria",
            role_id="archivista",
            specialization_id="archivo_documental",
        )
        
        assert classification.workload == "light"
        assert classification.recommended_execution == "local"
        assert classification.reasoning_need == "low"
    
    def test_classify_generic_auditor_heavy(self):
        """Auditor genérico debe ser workload heavy."""
        classification = classify_agent_model_need(
            domain_id="generic",
            role_id="auditor",
            specialization_id=None,
        )
        
        assert classification.workload == "heavy"
        assert classification.recommended_execution == "cloud_preferred"
    
    def test_classify_generic_archivista_light(self):
        """Archivista genérico debe ser workload light."""
        classification = classify_agent_model_need(
            domain_id="generic",
            role_id="archivista",
            specialization_id=None,
        )
        
        assert classification.workload == "light"
        assert classification.recommended_execution == "local"


class TestProviderModelSelection:
    """Tests para la selección de provider/model."""
    
    def test_recommend_with_nvidia_available_heavy(self):
        """Con NVIDIA disponible, workload heavy debe recomendar NVIDIA."""
        available_providers = [
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct", "meta/llama-3.3-70b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
            {
                "name": "ollama",
                "models": ["phi3:mini", "llama3.2:3b"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]
        
        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
        )
        
        assert recommendation.recommended is True
        assert recommendation.provider == "nvidia"
        assert recommendation.model is not None
        assert recommendation.workload == "heavy"
        assert "cloud" in recommendation.reason.lower()
    
    def test_recommend_only_ollama_heavy_with_warning(self):
        """Solo Ollama disponible para workload heavy debe dar fallback."""
        available_providers = [
            {
                "name": "ollama",
                "models": ["phi3:mini", "llama3.2:3b"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]
        
        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
        )
        
        assert recommendation.recommended is True
        assert recommendation.provider == "ollama"
        assert recommendation.model is not None
        assert "fallback" in recommendation.reason.lower() or "limitado" in recommendation.reason.lower()
    
    def test_recommend_no_providers(self):
        """Sin providers disponibles debe retornar recomendación incompleta."""
        available_providers = []
        
        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
        )
        
        assert recommendation.recommended is False
        assert recommendation.provider is None
        assert recommendation.model is None
        assert recommendation.fallback is not None
    
    def test_recommend_ignores_placeholder_providers(self):
        """Providers placeholder deben ignorarse."""
        available_providers = [
            {
                "name": "claude",
                "models": ["claude-sonnet-4"],
                "healthy": False,
                "is_placeholder": True,
            },
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]
        
        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
        )
        
        assert recommendation.recommended is True
        assert recommendation.provider == "nvidia"
        assert recommendation.provider != "claude"
    
    def test_recommend_light_workload_local_preferred(self):
        """Workload light debe preferir local."""
        available_providers = [
            {
                "name": "ollama",
                "models": ["phi3:mini", "llama3.2:3b"],
                "healthy": True,
                "is_placeholder": False,
            },
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]
        
        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="archivista",
            specialization_id="archivo_documental",
            available_providers=available_providers,
        )
        
        assert recommendation.recommended is True
        assert recommendation.provider == "ollama"
        assert "local" in recommendation.reason.lower()


class TestModelSelectionHelpers:
    """Tests para helpers de selección de modelos."""
    
    def test_is_cloud_provider(self):
        """Identificación correcta de providers cloud."""
        assert _is_cloud_provider("nvidia") is True
        assert _is_cloud_provider("openai") is True
        assert _is_cloud_provider("claude") is True
        assert _is_cloud_provider("gemini") is True
        assert _is_cloud_provider("ollama") is False
        assert _is_cloud_provider("lmstudio") is False
    
    def test_is_local_provider(self):
        """Identificación correcta de providers local."""
        assert _is_local_provider("ollama") is True
        assert _is_local_provider("lmstudio") is True
        assert _is_local_provider("localai") is True
        assert _is_local_provider("nvidia") is False
        assert _is_local_provider("openai") is False
    
    def test_select_best_model_heavy(self):
        """Workload heavy debe preferir modelos grandes."""
        models = ["phi3:mini", "meta/llama-3.1-8b-instruct", "meta/llama-3.3-70b-instruct"]
        
        selected = _select_best_model_for_workload(models, "heavy")
        
        # Debe preferir 70b
        assert selected == "meta/llama-3.3-70b-instruct"
    
    def test_select_best_model_medium(self):
        """Workload medium debe preferir modelos medianos."""
        models = ["phi3:mini", "meta/llama-3.1-8b-instruct", "meta/llama-3.3-70b-instruct"]
        
        selected = _select_best_model_for_workload(models, "medium")
        
        # Debe preferir 8b
        assert selected == "meta/llama-3.1-8b-instruct"
    
    def test_select_best_model_light(self):
        """Workload light debe preferir modelos pequeños."""
        models = ["phi3:mini", "meta/llama-3.1-8b-instruct", "meta/llama-3.3-70b-instruct"]
        
        selected = _select_best_model_for_workload(models, "light")
        
        # Debe preferir mini
        assert selected == "phi3:mini"
    
    def test_select_best_model_empty_list(self):
        """Lista vacía debe retornar None."""
        selected = _select_best_model_for_workload([], "heavy")
        assert selected is None


class TestHardwareLimitations:
    """Tests para limitaciones de hardware."""

    def test_limited_hardware_no_local_for_heavy(self):
        """Hardware limitado no debe recomendar local para workload heavy."""
        hardware = HardwareProfile(
            cpu="Ryzen 7 7730U",
            ram_gb=16,
            gpu=False,
            local_mode="limited",
        )

        available_providers = [
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
            {
                "name": "ollama",
                "models": ["phi3:mini"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]

        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
            hardware_profile=hardware,
        )

        # Debe preferir cloud a pesar de que local está disponible
        assert recommendation.provider == "nvidia"
        assert "cloud" in recommendation.reason.lower()

    def test_limited_hardware_reason_mentions_limitation(self):
        """Hardware limitado debe mencionar limitación en reason."""
        hardware = HardwareProfile(
            cpu="Ryzen 7 7730U",
            ram_gb=16,
            gpu=False,
            local_mode="limited",
        )

        available_providers = [
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]

        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
            hardware_profile=hardware,
        )

        # Reason debe mencionar "limited" o "sin GPU"
        assert "limited" in recommendation.reason.lower() or "sin gpu" in recommendation.reason.lower()

    def test_limited_hardware_local_ok_for_light(self):
        """Hardware limitado permite local para workload light."""
        hardware = HardwareProfile(
            cpu="Ryzen 7 7730U",
            ram_gb=16,
            gpu=False,
            local_mode="limited",
        )

        available_providers = [
            {
                "name": "ollama",
                "models": ["phi3:mini"],
                "healthy": True,
                "is_placeholder": False,
            },
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]

        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="archivista",
            specialization_id="archivo_documental",
            available_providers=available_providers,
            hardware_profile=hardware,
        )

        # Debe permitir local para workload light
        assert recommendation.provider == "ollama"

    def test_capable_hardware_allows_local_for_medium(self):
        """Hardware capaz permite local para workload medium."""
        hardware = HardwareProfile(
            cpu="Intel i7-12700K",
            ram_gb=32,
            gpu=True,
            gpu_name="NVIDIA RTX 3080",
            local_mode="capable",
        )

        available_providers = [
            {
                "name": "ollama",
                "models": ["llama3.2:3b", "llama3.2:7b"],
                "healthy": True,
                "is_placeholder": False,
            },
            {
                "name": "nvidia",
                "models": ["meta/llama-3.1-8b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]

        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="analista",
            specialization_id="analisis_datos",
            available_providers=available_providers,
            hardware_profile=hardware,
        )

        # Con hardware capaz, puede preferir cloud pero local es aceptable
        assert recommendation.recommended is True

    def test_high_end_hardware_allows_local_for_heavy(self):
        """Hardware high-end permite local para workload heavy."""
        hardware = HardwareProfile(
            cpu="AMD Ryzen 9 5950X",
            ram_gb=64,
            gpu=True,
            gpu_name="NVIDIA RTX 4090",
            local_mode="high_end",
        )

        available_providers = [
            {
                "name": "ollama",
                "models": ["llama3.2:70b"],
                "healthy": True,
                "is_placeholder": False,
            },
            {
                "name": "nvidia",
                "models": ["meta/llama-3.3-70b-instruct"],
                "healthy": True,
                "is_placeholder": False,
            },
        ]

        recommendation = recommend_provider_model(
            domain_id="loteria",
            role_id="auditor",
            specialization_id="auditoria_consistencia",
            available_providers=available_providers,
            hardware_profile=hardware,
        )

        # Con hardware high-end, puede preferir cloud pero local es aceptable
        assert recommendation.recommended is True
