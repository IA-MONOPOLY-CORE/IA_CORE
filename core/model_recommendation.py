"""Recomendador inteligente de provider/model por perfil de agente.

Este módulo provee recomendaciones de proveedor y modelo basadas en:
- Dominio del agente
- Rol y especialización
- Carga cognitiva esperada
- Requerimientos de razonamiento
- Hardware local disponible
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class HardwareProfile:
    """Perfil de hardware local para decisiones de routing."""
    cpu: str
    ram_gb: int
    gpu: bool
    local_mode: str  # "limited", "capable", "high_end"


@dataclass
class AgentWorkloadClassification:
    """Clasificación de carga de trabajo de un agente."""
    workload: str  # "light", "medium", "heavy", "critical"
    recommended_execution: str  # "local", "cloud", "cloud_preferred"
    reasoning_need: str  # "low", "medium", "high"
    latency_sensitivity: str  # "low", "medium", "high"


@dataclass
class ModelRecommendation:
    """Recomendación completa de provider/model."""
    recommended: bool
    provider: str | None
    model: str | None
    workload: str
    recommended_execution: str
    reasoning_need: str
    reason: str
    fallback: dict[str, Any] | None = None


def get_default_hardware_profile() -> HardwareProfile:
    """Retorna el perfil de hardware local del usuario.
    
    Por ahora está hardcoded como perfil ajustable del usuario.
    Futuro: podría detectarse automáticamente o leerse de config.
    """
    return HardwareProfile(
        cpu="Ryzen 7 7730U",
        ram_gb=16,
        gpu=False,
        local_mode="limited",
    )


def classify_agent_model_need(
    domain_id: str,
    role_id: str,
    specialization_id: str | None = None,
    profile_preset_id: str | None = None,
) -> AgentWorkloadClassification:
    """Clasifica las necesidades de modelo de un agente.
    
    Usa reglas determinísticas basadas en rol/especialización.
    No usa LLM para clasificación.
    """
    # Reglas específicas por dominio
    if domain_id == "loteria":
        return _classify_loteria_agent(role_id, specialization_id)
    
    # Reglas genéricas para otros dominios
    return _classify_generic_agent(role_id, specialization_id)


def _classify_loteria_agent(
    role_id: str,
    specialization_id: str | None,
) -> AgentWorkloadClassification:
    """Clasificación específica para agentes de Lotería."""
    
    # A. Agentes pesados / cloud fuerte preferido
    heavy_roles = {
        "auditor",
        "simulador",
        "detector_anomalias",
        "gestor_riesgo",
        "integrador_central",
    }
    
    if role_id in heavy_roles:
        return AgentWorkloadClassification(
            workload="heavy",
            recommended_execution="cloud_preferred",
            reasoning_need="high",
            latency_sensitivity="medium",
        )
    
    # B. Agentes medios
    medium_roles = {
        "analista",
        "critico",
        "investigador",
    }
    
    if role_id in medium_roles:
        return AgentWorkloadClassification(
            workload="medium",
            recommended_execution="cloud_preferred",
            reasoning_need="medium",
            latency_sensitivity="medium",
        )
    
    # C. Agentes livianos
    light_roles = {
        "archivista",
        "comunicador",
    }
    
    if role_id in light_roles:
        return AgentWorkloadClassification(
            workload="light",
            recommended_execution="local",
            reasoning_need="low",
            latency_sensitivity="low",
        )
    
    # Default para roles no clasificados
    return AgentWorkloadClassification(
        workload="medium",
        recommended_execution="cloud_preferred",
        reasoning_need="medium",
        latency_sensitivity="medium",
    )


def _classify_generic_agent(
    role_id: str,
    specialization_id: str | None,
) -> AgentWorkloadClassification:
    """Clasificación genérica para dominios no específicos."""
    
    # Palabras clave que sugieren carga pesada
    heavy_keywords = ["auditor", "critico", "simulador", "evaluador", "validador"]
    if any(kw in role_id.lower() for kw in heavy_keywords):
        return AgentWorkloadClassification(
            workload="heavy",
            recommended_execution="cloud_preferred",
            reasoning_need="high",
            latency_sensitivity="medium",
        )
    
    # Palabras clave que sugieren carga liviana
    light_keywords = ["archivista", "comunicador", "reportero", "notificador"]
    if any(kw in role_id.lower() for kw in light_keywords):
        return AgentWorkloadClassification(
            workload="light",
            recommended_execution="local",
            reasoning_need="low",
            latency_sensitivity="low",
        )
    
    # Default genérico
    return AgentWorkloadClassification(
        workload="medium",
        recommended_execution="cloud_preferred",
        reasoning_need="medium",
        latency_sensitivity="medium",
    )


def recommend_provider_model(
    domain_id: str,
    role_id: str,
    specialization_id: str | None = None,
    profile_preset_id: str | None = None,
    current_provider: str | None = None,
    current_model: str | None = None,
    available_providers: list[dict[str, Any]] | None = None,
    hardware_profile: HardwareProfile | None = None,
) -> ModelRecommendation:
    """Recomienda provider y modelo para un agente.
    
    Args:
        domain_id: ID del dominio
        role_id: ID del rol
        specialization_id: ID de especialización (opcional)
        profile_preset_id: ID del preset de perfil (opcional)
        current_provider: Provider actual del agente (opcional)
        current_model: Modelo actual del agente (opcional)
        available_providers: Lista de providers disponibles con sus modelos
        hardware_profile: Perfil de hardware local (opcional, usa default)
    
    Returns:
        ModelRecommendation con la recomendación completa
    """
    if hardware_profile is None:
        hardware_profile = get_default_hardware_profile()
    
    # Clasificar carga de trabajo
    classification = classify_agent_model_need(
        domain_id=domain_id,
        role_id=role_id,
        specialization_id=specialization_id,
        profile_preset_id=profile_preset_id,
    )
    
    # Normalizar providers disponibles
    if available_providers is None:
        available_providers = []
    
    providers_dict = _normalize_providers(available_providers)
    
    # Seleccionar provider según clasificación y hardware
    provider, model, reason = _select_provider_model(
        classification=classification,
        providers_dict=providers_dict,
        hardware_profile=hardware_profile,
    )
    
    # Generar fallback si no hay cloud disponible
    fallback = None
    if provider is None or model is None:
        fallback = _generate_fallback(
            classification=classification,
            providers_dict=providers_dict,
            hardware_profile=hardware_profile,
        )
    
    return ModelRecommendation(
        recommended=provider is not None and model is not None,
        provider=provider,
        model=model,
        workload=classification.workload,
        recommended_execution=classification.recommended_execution,
        reasoning_need=classification.reasoning_need,
        reason=reason,
        fallback=fallback,
    )


def _normalize_providers(
    providers: list[dict[str, Any]],
) -> dict[str, list[str]]:
    """Normaliza la lista de providers a un diccionario {provider: [models]}."""
    result = {}
    for provider_info in providers:
        name = provider_info.get("name")
        models = provider_info.get("models", [])
        is_placeholder = provider_info.get("is_placeholder", False)
        healthy = provider_info.get("healthy", False)
        
        # Ignorar placeholders y providers no saludables
        if is_placeholder or not healthy:
            continue
        
        if name and models:
            result[name] = models
    
    return result


def _select_provider_model(
    classification: AgentWorkloadClassification,
    providers_dict: dict[str, list[str]],
    hardware_profile: HardwareProfile,
) -> tuple[str | None, str | None, str]:
    """Selecciona provider y modelo según clasificación."""
    
    workload = classification.workload
    recommended_exec = classification.recommended_execution
    
    # Si hardware es limitado y workload es heavy/critical, no recomendar local
    if hardware_profile.local_mode == "limited" and workload in ["heavy", "critical"]:
        if recommended_exec == "local":
            recommended_exec = "cloud_preferred"
    
    # Preferencia de provider según workload
    if workload in ["heavy", "critical"]:
        # Preferir cloud
        cloud_providers = [p for p in providers_dict.keys() if _is_cloud_provider(p)]
        if cloud_providers:
            # Preferir NVIDIA si está disponible
            if "nvidia" in cloud_providers:
                provider = "nvidia"
            else:
                provider = cloud_providers[0]
            
            models = providers_dict[provider]
            model = _select_best_model_for_workload(models, workload)
            reason = f"Workload {workload} requiere razonamiento profundo; se recomienda cloud para calidad."
            return provider, model, reason
        
        # Fallback a local con advertencia
        local_providers = [p for p in providers_dict.keys() if _is_local_provider(p)]
        if local_providers:
            provider = local_providers[0]
            models = providers_dict[provider]
            model = _select_best_model_for_workload(models, "light")  # Usar modelo liviano
            reason = f"Workload {workload} pero no hay cloud disponible; local como fallback limitado."
            return provider, model, reason
        
        return None, None, "No hay providers disponibles para este workload."
    
    elif workload == "medium":
        # Preferir cloud si disponible, sino local
        cloud_providers = [p for p in providers_dict.keys() if _is_cloud_provider(p)]
        if cloud_providers:
            provider = cloud_providers[0]
            models = providers_dict[provider]
            model = _select_best_model_for_workload(models, workload)
            reason = f"Workload medio; cloud disponible para mejor calidad."
            return provider, model, reason
        
        local_providers = [p for p in providers_dict.keys() if _is_local_provider(p)]
        if local_providers:
            provider = local_providers[0]
            models = providers_dict[provider]
            model = _select_best_model_for_workload(models, workload)
            reason = f"Workload medio; local como única opción disponible."
            return provider, model, reason
        
        return None, None, "No hay providers disponibles para workload medio."
    
    else:  # light
        # Preferir local
        local_providers = [p for p in providers_dict.keys() if _is_local_provider(p)]
        if local_providers:
            provider = local_providers[0]
            models = providers_dict[provider]
            model = _select_best_model_for_workload(models, workload)
            reason = f"Workload liviano; local es suficiente y económico."
            return provider, model, reason
        
        # Fallback a cloud económico
        cloud_providers = [p for p in providers_dict.keys() if _is_cloud_provider(p)]
        if cloud_providers:
            provider = cloud_providers[0]
            models = providers_dict[provider]
            model = _select_best_model_for_workload(models, workload)
            reason = f"Workload liviano; cloud como local no disponible."
            return provider, model, reason
        
        return None, None, "No hay providers disponibles para workload liviano."


def _select_best_model_for_workload(
    models: list[str],
    workload: str,
) -> str | None:
    """Selecciona el mejor modelo de una lista según el workload."""
    if not models:
        return None
    
    # Preferencias por nombre de modelo (heurísticas simples)
    # Para workload heavy/critical: preferir modelos más grandes
    if workload in ["heavy", "critical"]:
        # Preferir modelos con "70b", "8b", "7b" en ese orden
        for keyword in ["70b", "8b", "7b"]:
            for model in models:
                if keyword in model.lower():
                    return model
        # Si no, el primero
        return models[0]
    
    # Para workload medium: modelos medianos
    elif workload == "medium":
        for keyword in ["8b", "7b", "3b"]:
            for model in models:
                if keyword in model.lower():
                    return model
        return models[0]
    
    # Para workload light: modelos pequeños
    else:
        for keyword in ["0.5b", "1b", "2b", "3b", "mini"]:
            for model in models:
                if keyword in model.lower():
                    return model
        # Si no hay modelo pequeño, usar el primero
        return models[0]


def _generate_fallback(
    classification: AgentWorkloadClassification,
    providers_dict: dict[str, list[str]],
    hardware_profile: HardwareProfile,
) -> dict[str, Any]:
    """Genera una recomendación de fallback cuando no hay opción ideal."""
    fallback = {
        "provider": None,
        "model": None,
        "warning": "No se pudo generar recomendación automática.",
    }
    
    # Intentar usar cualquier provider disponible
    if providers_dict:
        for provider, models in providers_dict.items():
            if models:
                fallback["provider"] = provider
                fallback["model"] = models[0]
                fallback["warning"] = "Usando primer provider/model disponible como fallback."
                break
    
    return fallback


def _is_cloud_provider(provider_name: str) -> bool:
    """Determina si un provider es cloud."""
    cloud_providers = {"nvidia", "openai", "claude", "gemini", "deepseek", "groq", "openrouter"}
    return provider_name.lower() in cloud_providers


def _is_local_provider(provider_name: str) -> bool:
    """Determina si un provider es local."""
    local_providers = {"ollama", "lmstudio", "localai"}
    return provider_name.lower() in local_providers
