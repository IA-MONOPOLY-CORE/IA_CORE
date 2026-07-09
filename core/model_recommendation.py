"""Recomendador inteligente de provider/model por perfil de agente.

Este módulo provee recomendaciones de proveedor y modelo basadas en:
- Dominio del agente
- Rol y especialización
- Carga cognitiva esperada
- Requerimientos de razonamiento
- Hardware local disponible
"""

from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class HardwareProfile:
    """Perfil de hardware local para decisiones de routing."""
    cpu: str
    ram_gb: int
    gpu: bool
    gpu_name: str | None = None
    local_mode: str = "limited"  # "limited", "capable", "high_end"
    source: str = "unknown"  # "manual_config", "autodetect", "fallback"


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
    compatibility: str = "unknown"  # "compatible", "warning", "blocked", "cloud_available"
    hardware_reason: str = ""


def get_hardware_profile() -> HardwareProfile:
    """Retorna el perfil de hardware local del usuario.
    
    Prioridad:
    1. config/hardware_profile.json si existe
    2. Autodetección básica
    3. Fallback seguro
    """
    # 1. Intentar cargar desde config
    config_profile = _load_hardware_profile_from_config()
    if config_profile:
        return config_profile
    
    # 2. Intentar autodetectar
    autodetect_profile = _autodetect_hardware_profile()
    if autodetect_profile:
        return autodetect_profile
    
    # 3. Fallback seguro
    return _get_fallback_hardware_profile()


def _load_hardware_profile_from_config() -> HardwareProfile | None:
    """Carga el perfil de hardware desde config/hardware_profile.json."""
    try:
        config_path = Path("config/hardware_profile.json")
        if not config_path.exists():
            return None
        
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return HardwareProfile(
            cpu=data.get("cpu", "unknown"),
            ram_gb=data.get("ram_gb", 8),
            gpu=data.get("gpu", False),
            gpu_name=data.get("gpu_name"),
            local_mode=data.get("local_mode", "limited"),
            source=data.get("source", "manual_config"),
        )
    except Exception:
        return None


def _autodetect_hardware_profile() -> HardwareProfile | None:
    """Autodetecta el perfil de hardware básico."""
    try:
        cpu = platform.processor() or "unknown"
        
        # Detectar RAM
        ram_gb = 8  # Default
        try:
            ram_bytes = os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")
            ram_gb = int(ram_bytes / (1024 ** 3))
        except Exception:
            pass
        
        # GPU detection básica (sin dependencias pesadas)
        gpu = False
        gpu_name = None
        try:
            # Intento simple de detectar NVIDIA en Windows
            if platform.system() == "Windows":
                try:
                    import subprocess
                    result = subprocess.run(
                        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                        capture_output=True,
                        text=True,
                        timeout=2,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        gpu = True
                        gpu_name = result.stdout.strip().split("\n")[0]
                except Exception:
                    pass
        except Exception:
            pass
        
        # Determinar local_mode basado en RAM y GPU
        if gpu and ram_gb >= 32:
            local_mode = "high_end"
        elif gpu and ram_gb >= 16:
            local_mode = "capable"
        else:
            local_mode = "limited"
        
        return HardwareProfile(
            cpu=cpu,
            ram_gb=ram_gb,
            gpu=gpu,
            gpu_name=gpu_name,
            local_mode=local_mode,
            source="autodetect",
        )
    except Exception:
        return None


def _get_fallback_hardware_profile() -> HardwareProfile:
    """Retorna un perfil de hardware seguro como fallback."""
    return HardwareProfile(
        cpu="unknown",
        ram_gb=8,
        gpu=False,
        gpu_name=None,
        local_mode="limited",
        source="fallback",
    )


def get_default_hardware_profile() -> HardwareProfile:
    """Retorna el perfil de hardware local del usuario (legacy).
    
    Esta función mantiene compatibilidad con código existente.
    Usa get_hardware_profile() internamente.
    """
    return get_hardware_profile()


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
    
    # Evaluar compatibilidad del modelo recomendado
    compatibility = "unknown"
    hardware_reason = ""
    if provider and model:
        compat_result = evaluate_model_compatibility(provider, model, hardware_profile)
        compatibility = compat_result.get("compatibility", "unknown")
        hardware_reason = compat_result.get("hardware_reason", "")
    
    return ModelRecommendation(
        recommended=provider is not None and model is not None,
        provider=provider,
        model=model,
        workload=classification.workload,
        recommended_execution=classification.recommended_execution,
        reasoning_need=classification.reasoning_need,
        reason=reason,
        fallback=fallback,
        compatibility=compatibility,
        hardware_reason=hardware_reason,
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
            if hardware_profile.local_mode == "limited":
                reason = f"Workload {workload} requiere razonamiento profundo; el perfil de hardware local está marcado como limited/sin GPU, se recomienda cloud."
            else:
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


def evaluate_model_compatibility(
    provider: str,
    model: str,
    hardware_profile: HardwareProfile,
) -> dict[str, str]:
    """Evalúa la compatibilidad de un modelo con el hardware local.
    
    Args:
        provider: Nombre del provider (ej. "nvidia", "ollama")
        model: Nombre del modelo (ej. "phi3:mini", "meta/llama-3.3-70b-instruct")
        hardware_profile: Perfil de hardware local
    
    Returns:
        Dict con compatibility, hardware_reason
    """
    # A. Provider cloud: siempre cloud_available
    if _is_cloud_provider(provider):
        return {
            "provider": provider,
            "model": model,
            "compatibility": "cloud_available",
            "hardware_reason": "La inferencia corre en cloud; no depende del hardware local.",
        }
    
    # B. Provider local: evaluar según hardware y tamaño del modelo
    if not _is_local_provider(provider):
        # Provider desconocido
        return {
            "provider": provider,
            "model": model,
            "compatibility": "unknown",
            "hardware_reason": "Provider no clasificado como cloud ni local.",
        }
    
    # Clasificar tamaño del modelo
    model_size = _classify_model_size(model)
    local_mode = hardware_profile.local_mode
    
    # Reglas según hardware y tamaño
    if local_mode == "limited":
        if model_size == "small":
            return {
                "provider": provider,
                "model": model,
                "compatibility": "compatible",
                "hardware_reason": "Modelo liviano compatible con hardware local limitado.",
            }
        elif model_size == "medium":
            return {
                "provider": provider,
                "model": model,
                "compatibility": "warning",
                "hardware_reason": "Modelo mediano puede ser lento en hardware limitado; se recomienda cloud.",
            }
        else:  # large
            return {
                "provider": provider,
                "model": model,
                "compatibility": "blocked",
                "hardware_reason": "Modelo pesado no recomendado para hardware limitado; se requiere cloud.",
            }
    
    elif local_mode == "capable":
        if model_size == "small":
            return {
                "provider": provider,
                "model": model,
                "compatibility": "compatible",
                "hardware_reason": "Modelo liviano compatible con hardware capaz.",
            }
        elif model_size == "medium":
            return {
                "provider": provider,
                "model": model,
                "compatibility": "compatible",
                "hardware_reason": "Modelo mediano compatible con hardware capaz.",
            }
        else:  # large
            return {
                "provider": provider,
                "model": model,
                "compatibility": "warning",
                "hardware_reason": "Modelo pesado puede ser lento incluso en hardware capaz; cloud puede ser mejor.",
            }
    
    elif local_mode == "high_end":
        if model_size == "small":
            return {
                "provider": provider,
                "model": model,
                "compatibility": "compatible",
                "hardware_reason": "Modelo liviano compatible con hardware high-end.",
            }
        elif model_size == "medium":
            return {
                "provider": provider,
                "model": model,
                "compatibility": "compatible",
                "hardware_reason": "Modelo mediano compatible con hardware high-end.",
            }
        else:  # large
            return {
                "provider": provider,
                "model": model,
                "compatibility": "compatible",
                "hardware_reason": "Modelo pesado compatible con hardware high-end.",
            }
    
    else:  # unknown local_mode
        return {
            "provider": provider,
            "model": model,
            "compatibility": "unknown",
            "hardware_reason": "Modo de hardware local desconocido.",
        }


def _classify_model_size(model: str) -> str:
    """Clasifica el tamaño de un modelo según su nombre.
    
    Returns:
        "small", "medium", "large"
    """
    model_lower = model.lower()
    
    # Patrones para modelos grandes
    large_patterns = ["70b", "100b", "120b", "130b", "180b", "200b", "300b", "400b"]
    for pattern in large_patterns:
        if pattern in model_lower:
            return "large"
    
    # Patrones para modelos medianos
    medium_patterns = ["7b", "8b", "13b", "14b", "30b", "34b", "40b"]
    for pattern in medium_patterns:
        if pattern in model_lower:
            return "medium"
    
    # Patrones para modelos pequeños
    small_patterns = ["0.5b", "1b", "2b", "3b", "4b", "mini", "tiny", "nano"]
    for pattern in small_patterns:
        if pattern in model_lower:
            return "small"
    
    # Default: asumir mediano si no se puede clasificar
    return "medium"
