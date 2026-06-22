"""
core/evolution.py - Módulo de gestión del ciclo evolutivo S.A.A.O.P.
Maneja la memoria de 50 sorteos, parámetros ajustables y estadísticas de agentes.
Incluye lógica de fases: entrenamiento, validación ciega, predicción en vivo, operacional real.
"""

from __future__ import annotations

import json
import logging
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# ============================================================
# LÍMITES DEL SISTEMA POR FASE
# ============================================================
TRAINING_END = 3799           # Último sorteo de entrenamiento (2022-2024)
BLIND_TEST_START = 3800       # Comienza validación ciega
BLIND_TEST_END = 3850         # Termina validación ciega (51 sorteos)
LIVE_TEST_START = 3851        # Comienza predicción en vivo
LIVE_TEST_END = 3885          # Último sorteo con resultado conocido pero oculto
REAL_OPERATION_START = 3886   # Sorteos futuros reales


class EvolutionManager:
    """
    Gestiona el ciclo evolutivo de 50 sorteos para S.A.A.O.P.
    - Mantiene ventana rodante de últimos 50 juegos
    - Almacena parámetros evolutivos (pesos zonales, umbrales, etc.)
    - Registra historial de aciertos/fallos por agente
    - Provee contexto para inyectar en prompts
    - Gestiona las fases del sistema (entrenamiento, validación ciega, etc.)
    """

    def __init__(self, memory_path: str = "C:\\IA_CORE\\memory\\state.json"):
        self.memory_path = Path(memory_path)
        self._state = None
        self._load_state()
        self._ultima_regeneracion = 0

    def _load_state(self):
        """Carga el estado desde el archivo JSON"""
        with open(self.memory_path, 'r', encoding='utf-8') as f:
            self._state = json.load(f)
        
        # Asegurar que existe la estructura evolutiva
        if "evolucion_lotoplus" not in self._state:
            self._state["evolucion_lotoplus"] = self._get_default_evolution()
            self._save_state()
        
        # Asegurar que existe la estructura de ranking de herramientas
        if "ranking_herramientas" not in self._state["evolucion_lotoplus"]:
            self._state["evolucion_lotoplus"]["ranking_herramientas"] = self._get_default_ranking()
            self._save_state()
        
        # Asegurar que existe el contador de regeneración
        if "ultima_regeneracion_papers" not in self._state["evolucion_lotoplus"]:
            self._state["evolucion_lotoplus"]["ultima_regeneracion_papers"] = 0
            self._state["evolucion_lotoplus"]["frecuencia_regeneracion_papers"] = 10
            self._save_state()

    def _save_state(self):
        """Guarda el estado al archivo JSON"""
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self._state, f, indent=2, ensure_ascii=False)

    def _get_default_evolution(self) -> dict:
        """Retorna la estructura por defecto para evolucion_lotoplus"""
        return {
            "ciclo_actual": {
                "sorteo_inicio": 3800,
                "sorteo_actual": 3800,
                "sorteos_completados": 0,
                "objetivo": 50,
                "fase_actual": "validacion_ciega",
                "ultimos_50_juegos": [],
                "metricas_acumuladas": {
                    "total_aciertos_4": 0,
                    "total_aciertos_5": 0,
                    "total_aciertos_6": 0,
                    "delta_promedio_vs_random": 0,
                    "ventaja_actual": 0
                }
            },
            "parametros_evolutivos": {
                "pesos_zonales": {
                    "Z1": 0.9, "Z2": 0.2, "Z3": 0.2, "Z4": 0.3,
                    "Z5": 0.5, "Z6": 0.6, "Z7": 0.7, "Z8": 0.8, "Z9": 0.9
                },
                "exposicion_actual": 80,
                "umbral_uscore": 66,
                "umbral_ver": 0.3,
                "filtros_activos": [],
                "patrones_validados": [],
                "patrones_descartados": []
            },
            "historial_agentes": {
                "estadistico_integral": {
                    "aciertos_4+": [],
                    "fallos_0-2": [],
                    "precision_ultimos_10": 0,
                    "patrones_aprendidos": [],
                    "errores_cometidos": [],
                    "aciertos_historicos": []
                },
                "gpt_auditor": {
                    "detectados_correctos": [],
                    "falsos_positivos": [],
                    "precision_auditor": 0,
                    "patrones_aprendidos": [],
                    "errores_cometidos": [],
                    "aciertos_historicos": []
                },
                "viejo_deepseek": {
                    "recomendaciones_acertadas": [],
                    "recomendaciones_fallidas": [],
                    "factor_mejora": 0,
                    "patrones_aprendidos": [],
                    "errores_cometidos": [],
                    "aciertos_historicos": []
                }
            },
            "ultima_regeneracion_papers": 0,
            "frecuencia_regeneracion_papers": 10
        }

    def _get_default_ranking(self) -> dict:
        """Retorna la estructura para el ranking de herramientas"""
        return {
            "herramientas": {
                "uScore": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                },
                "VER": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                },
                "CAZADOR": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                },
                "ESPEJO": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                },
                "PUENTE": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                },
                "ECLIPSE": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                },
                "co_ocurrencias": {
                    "aciertos": 0,
                    "fallos": 0,
                    "precision": 0,
                    "historial": []
                }
            },
            "hipotesis_eliminadas": [],
            "hipotesis_supervivientes": [],
            "ultima_actualizacion": None
        }

    def get_fase(self, sorteo: int) -> str:
        """
        Determina la fase del sistema según el número de sorteo.
        
        Retorna:
        - "entrenamiento": 2022-2024, los agentes ven todo
        - "validacion_ciega": 3800-3850, predicen sin ver resultado
        - "prediccion_en_vivo": 3851-3885, predicen en vivo (resultados existen pero ocultos)
        - "operacional_real": 3886+, predicen sorteos futuros reales
        """
        if sorteo <= TRAINING_END:
            return "entrenamiento"
        elif sorteo <= BLIND_TEST_END:
            return "validacion_ciega"
        elif sorteo <= LIVE_TEST_END:
            return "prediccion_en_vivo"
        else:
            return "operacional_real"

    def get_resultados_visibles_hasta(self, sorteo_actual: int) -> int:
        """
        Retorna el número de sorteo HASTA el cual el sistema puede ver resultados.
        
        Reglas:
        - En entrenamiento (<=3799): ve todo hasta 3799
        - En test ciego (3800-3850): ve solo sorteos ANTERIORES al actual
        - En predicción en vivo (3851-3885): ve solo hasta 3850
        - En operacional real (3886+): ve todo el histórico hasta 3885
        
        Args:
            sorteo_actual: El sorteo que se está procesando actualmente
            
        Returns:
            Número de sorteo hasta el cual se pueden ver resultados
        """
        fase = self.get_fase(sorteo_actual)
        
        if fase == "entrenamiento":
            return TRAINING_END
        elif fase == "validacion_ciega":
            if sorteo_actual <= BLIND_TEST_START:
                return TRAINING_END
            else:
                return sorteo_actual - 1
        elif fase == "prediccion_en_vivo":
            return BLIND_TEST_END
        else:  # operacional_real
            return LIVE_TEST_END

    def get_contexto_para_prompt(self, role: str = "analyst", sorteo_actual: int = None) -> dict:
        """
        Retorna el contexto actual para inyectar en los prompts de los agentes.
        El formato varía según el rol del agente y la fase actual.
        """
        ciclo = self._state["evolucion_lotoplus"]["ciclo_actual"]
        params = self._state["evolucion_lotoplus"]["parametros_evolutivos"]
        historial = self._state["evolucion_lotoplus"]["historial_agentes"]
        
        if sorteo_actual is None:
            sorteo_actual = ciclo["sorteo_actual"]

        fase = self.get_fase(sorteo_actual)

        # Resumen de últimos 50 resultados (solo visibles)
        ultimos_50 = ciclo.get("ultimos_50_juegos", [])
        resultados_visibles_hasta = self.get_resultados_visibles_hasta(sorteo_actual)
        
        # Filtrar juegos visibles
        juegos_visibles = [j for j in ultimos_50 if j.get("sorteo", 0) <= resultados_visibles_hasta]
        
        resumen_50 = {
            "total_sorteos": len(juegos_visibles),
            "aciertos_4": sum(1 for j in juegos_visibles if j.get("aciertos", 0) >= 4),
            "aciertos_5": sum(1 for j in juegos_visibles if j.get("aciertos", 0) >= 5),
            "aciertos_6": sum(1 for j in juegos_visibles if j.get("aciertos", 0) >= 6),
            "delta_promedio": ciclo["metricas_acumuladas"]["delta_promedio_vs_random"]
        }

        # Instrucción de fase
        instruccion_fase = self._get_instruccion_fase(fase)

        # Contexto base común
        contexto_base = {
            "sorteo_actual": sorteo_actual,
            "sorteos_completados": ciclo["sorteos_completados"],
            "objetivo_ciclo": ciclo["objetivo"],
            "fase_actual": fase,
            "instruccion_fase": instruccion_fase,
            "resultados_visibles_hasta": resultados_visibles_hasta,
            "ultimos_50_resumen": resumen_50,
            "pesos_zonales_actuales": params["pesos_zonales"],
            "exposicion_actual": params["exposicion_actual"],
            "umbral_uscore": params["umbral_uscore"],
            "umbral_ver": params["umbral_ver"],
            "filtros_activos": params["filtros_activos"],
            "patrones_validados": params["patrones_validados"],
            "patrones_descartados": params["patrones_descartados"],
            # Métricas del ciclo
            "total_aciertos_4": ciclo["metricas_acumuladas"]["total_aciertos_4"],
            "total_aciertos_5": ciclo["metricas_acumuladas"]["total_aciertos_5"],
            "total_aciertos_6": ciclo["metricas_acumuladas"]["total_aciertos_6"],
            "delta_promedio_vs_random": ciclo["metricas_acumuladas"]["delta_promedio_vs_random"],
            "ventaja_actual": ciclo["metricas_acumuladas"]["ventaja_actual"]
        }

        # Agregar información específica por rol
        if role == "analyst":
            contexto_base.update({
                "mis_aciertos": historial["estadistico_integral"]["aciertos_4+"][-10:],
                "mis_fallos": historial["estadistico_integral"]["fallos_0-2"][-10:],
                "mi_precision": historial["estadistico_integral"]["precision_ultimos_10"]
            })
        elif role == "critic":
            contexto_base.update({
                "detectados_correctos": historial["gpt_auditor"]["detectados_correctos"][-10:],
                "falsos_positivos": historial["gpt_auditor"]["falsos_positivos"][-10:],
                "precision_auditor": historial["gpt_auditor"]["precision_auditor"]
            })
        elif role == "optimizer":
            contexto_base.update({
                "mis_aciertos_opt": historial["viejo_deepseek"]["recomendaciones_acertadas"][-10:],
                "mis_fallos_opt": historial["viejo_deepseek"]["recomendaciones_fallidas"][-10:],
                "mi_factor_mejora": historial["viejo_deepseek"]["factor_mejora"]
            })

        # Agregar ranking de herramientas
        ranking = self._state["evolucion_lotoplus"].get("ranking_herramientas", {})
        contexto_base["ranking_herramientas"] = ranking.get("herramientas", {})

        return contexto_base

    def _get_instruccion_fase(self, fase: str) -> str:
        """Retorna instrucciones específicas según la fase del sistema"""
        if fase == "entrenamiento":
            return "FASE DE ENTRENAMIENTO: Estás analizando datos históricos (2022-2024). Tienes acceso completo a los resultados para aprender patrones, calibrar U-Score y VER, y validar hipótesis."
        elif fase == "validacion_ciega":
            return "FASE DE VALIDACIÓN CIEGA: NO conoces el resultado de este sorteo. Debes predecir basándote SOLO en el entrenamiento previo y los aprendizajes de sorteos anteriores de esta fase."
        elif fase == "prediccion_en_vivo":
            return "FASE DE PREDICCIÓN EN VIVO: NO conoces el resultado de este sorteo. Aunque el dato existe en el sistema, está OCULTO para ti. Predice basándote en entrenamiento + validaciones previas."
        else:
            return "FASE OPERACIONAL REAL: Este es un sorteo REAL futuro. No existe resultado conocido en ningún lado. Predice basándote en todo el aprendizaje acumulado."

    def registrar_juego(self,
                       sorteo: int,
                       prediccion_analyst: List[int],
                       prediccion_optimizer: List[int],
                       consenso_final: List[int],
                       uscore_predicho: float,
                       resultado_real: Dict[str, Any],
                       lecciones: str = ""):
        """
        Registra un juego completado y actualiza todas las métricas evolutivas.
        También actualiza los patrones aprendidos y errores cometidos de los agentes.
        """
        fase = self.get_fase(sorteo)
        
        # Solo registrar en fases de test
        if fase == "entrenamiento":
            self._acumular_aprendizaje_entrenamiento(sorteo, resultado_real)
            return

        ciclo = self._state["evolucion_lotoplus"]["ciclo_actual"]
        params = self._state["evolucion_lotoplus"]["parametros_evolutivos"]
        historial = self._state["evolucion_lotoplus"]["historial_agentes"]

        aciertos = resultado_real.get("aciertos", 0)

        # Crear registro del juego
        juego = {
            "sorteo": sorteo,
            "fase": fase,
            "prediccion_analyst": prediccion_analyst,
            "prediccion_optimizer": prediccion_optimizer,
            "consenso_final": consenso_final,
            "uscore_predicho": uscore_predicho,
            "resultado_real": resultado_real,
            "aciertos": aciertos,
            "lecciones_aprendidas": lecciones,
            "timestamp": datetime.now().isoformat()
        }

        # Actualizar ventana rodante de últimos 50
        ultimos_50 = ciclo.get("ultimos_50_juegos", [])
        ultimos_50.append(juego)
        if len(ultimos_50) > 50:
            ultimos_50.pop(0)
        ciclo["ultimos_50_juegos"] = ultimos_50

        # Actualizar métricas acumuladas
        if aciertos >= 4:
            ciclo["metricas_acumuladas"]["total_aciertos_4"] += 1
        if aciertos >= 5:
            ciclo["metricas_acumuladas"]["total_aciertos_5"] += 1
        if aciertos >= 6:
            ciclo["metricas_acumuladas"]["total_aciertos_6"] += 1

        # Actualizar historial del Estadístico
        if aciertos >= 4:
            historial["estadistico_integral"]["aciertos_4+"].append(sorteo)
            # Registrar como acierto histórico
            leccion = f"Sorteo {sorteo}: Predicción {prediccion_analyst} - {aciertos} aciertos"
            historial["estadistico_integral"]["aciertos_historicos"].append({
                "sorteo": sorteo,
                "descripcion": leccion,
                "fecha": datetime.now().isoformat()
            })
        else:
            historial["estadistico_integral"]["fallos_0-2"].append(sorteo)
            # Registrar como error
            if lecciones:
                historial["estadistico_integral"]["errores_cometidos"].append({
                    "sorteo": sorteo,
                    "error": lecciones[:300],
                    "fecha": datetime.now().isoformat()
                })

        # Limitar históricos a 50 elementos
        for key in ["aciertos_historicos", "errores_cometidos", "patrones_aprendidos"]:
            if key in historial["estadistico_integral"]:
                if len(historial["estadistico_integral"][key]) > 50:
                    historial["estadistico_integral"][key] = historial["estadistico_integral"][key][-50:]

        # Calcular precisión últimos 10 del Estadístico
        ultimos_10_ei = (historial["estadistico_integral"]["aciertos_4+"][-10:] +
                         historial["estadistico_integral"]["fallos_0-2"][-10:])
        if ultimos_10_ei:
            aciertos_10 = sum(1 for s in ultimos_10_ei 
                            if s in historial["estadistico_integral"]["aciertos_4+"])
            historial["estadistico_integral"]["precision_ultimos_10"] = round(aciertos_10 / len(ultimos_10_ei) * 100, 2)

        # Incrementar contadores del ciclo
        ciclo["sorteos_completados"] += 1
        ciclo["sorteo_actual"] = sorteo + 1
        ciclo["fase_actual"] = self.get_fase(sorteo + 1)

        # Recalcular ventaja actual
        if ciclo["metricas_acumuladas"]["total_aciertos_4"] > 0:
            porcentaje_real = (ciclo["metricas_acumuladas"]["total_aciertos_4"] / ciclo["sorteos_completados"]) * 100
            ciclo["metricas_acumuladas"]["ventaja_actual"] = round(porcentaje_real / 22.1, 2)

        # ========== REGENERACIÓN AUTOMÁTICA DE PAPERS ==========
        ultima_reg = self._state["evolucion_lotoplus"].get("ultima_regeneracion_papers", 0)
        frecuencia = self._state["evolucion_lotoplus"].get("frecuencia_regeneracion_papers", 10)
        
        if ciclo["sorteos_completados"] - ultima_reg >= frecuencia:
            self._regenerar_papers_mejor_agente(sorteo)
            self._state["evolucion_lotoplus"]["ultima_regeneracion_papers"] = ciclo["sorteos_completados"]
            self._save_state()

        self._save_state()

    def _acumular_aprendizaje_entrenamiento(self, sorteo: int, resultado_real: Dict[str, Any]):
        """
        En fase de entrenamiento, solo acumulamos aprendizaje sin registrar como juego.
        Los agentes usan esto para calibrar sus parámetros.
        """
        ciclo = self._state["evolucion_lotoplus"]["ciclo_actual"]
        ciclo["sorteo_actual"] = sorteo + 1
        self._save_state()

    def actualizar_parametros(self, nuevos_parametros: Dict[str, Any]):
        """
        Actualiza los parámetros evolutivos después de un debate.
        Solo actualiza los campos que vienen en el diccionario.
        """
        params = self._state["evolucion_lotoplus"]["parametros_evolutivos"]

        if "pesos_zonales" in nuevos_parametros:
            params["pesos_zonales"].update(nuevos_parametros["pesos_zonales"])
        if "exposicion_actual" in nuevos_parametros:
            params["exposicion_actual"] = nuevos_parametros["exposicion_actual"]
        if "umbral_uscore" in nuevos_parametros:
            params["umbral_uscore"] = nuevos_parametros["umbral_uscore"]
        if "umbral_ver" in nuevos_parametros:
            params["umbral_ver"] = nuevos_parametros["umbral_ver"]
        if "filtros_activos" in nuevos_parametros:
            params["filtros_activos"] = nuevos_parametros["filtros_activos"]
        if "patrones_validados" in nuevos_parametros:
            params["patrones_validados"] = nuevos_parametros["patrones_validados"]
        if "patrones_descartados" in nuevos_parametros:
            params["patrones_descartados"] = nuevos_parametros["patrones_descartados"]

        self._save_state()

    def registrar_auditoria(self, 
                           acierto_auditor: bool,
                           fue_falso_positivo: bool = False):
        """
        Registra el desempeño del GPT Auditor.
        """
        historial = self._state["evolucion_lotoplus"]["historial_agentes"]["gpt_auditor"]
        
        if acierto_auditor:
            historial["detectados_correctos"].append(self._get_current_sorteo())
        if fue_falso_positivo:
            historial["falsos_positivos"].append(self._get_current_sorteo())
        
        total = len(historial["detectados_correctos"]) + len(historial["falsos_positivos"])
        if total > 0:
            historial["precision_auditor"] = round(
                len(historial["detectados_correctos"]) / total * 100, 2
            )
        
        self._save_state()

    def registrar_optimizacion(self, 
                              fue_acertada: bool,
                              mejora_factor: float = 0):
        """
        Registra el desempeño del Viejo DeepSeek como optimizador.
        """
        historial = self._state["evolucion_lotoplus"]["historial_agentes"]["viejo_deepseek"]
        
        if fue_acertada:
            historial["recomendaciones_acertadas"].append(self._get_current_sorteo())
        else:
            historial["recomendaciones_fallidas"].append(self._get_current_sorteo())
        
        if mejora_factor > 0:
            old_factor = historial["factor_mejora"]
            historial["factor_mejora"] = round((old_factor + mejora_factor) / 2, 2) if old_factor > 0 else mejora_factor
        
        self._save_state()

    def registrar_herramienta(self, herramienta: str, fue_acertada: bool):
        """
        Registra el desempeño de una herramienta específica para el ranking.
        """
        ranking = self._state["evolucion_lotoplus"].get("ranking_herramientas", {})
        herramientas = ranking.get("herramientas", {})
        
        if herramienta not in herramientas:
            herramientas[herramienta] = {"aciertos": 0, "fallos": 0, "precision": 0, "historial": []}
        
        if fue_acertada:
            herramientas[herramienta]["aciertos"] += 1
        else:
            herramientas[herramienta]["fallos"] += 1
        
        total = herramientas[herramienta]["aciertos"] + herramientas[herramienta]["fallos"]
        if total > 0:
            herramientas[herramienta]["precision"] = round(herramientas[herramienta]["aciertos"] / total * 100, 2)
        
        herramientas[herramienta]["historial"].append({
            "sorteo": self._get_current_sorteo(),
            "acerto": fue_acertada
        })
        
        ranking["herramientas"] = herramientas
        ranking["ultima_actualizacion"] = str(self._get_current_sorteo())
        self._state["evolucion_lotoplus"]["ranking_herramientas"] = ranking
        self._save_state()

    def _get_current_sorteo(self) -> int:
        """Retorna el número del sorteo actual"""
        return self._state["evolucion_lotoplus"]["ciclo_actual"]["sorteo_actual"]

    def get_ultimos_juegos(self, n: int = 10) -> List[dict]:
        """Retorna los últimos N juegos registrados"""
        ultimos = self._state["evolucion_lotoplus"]["ciclo_actual"]["ultimos_50_juegos"]
        return ultimos[-n:] if ultimos else []

    def get_estadisticas_ciclo(self) -> dict:
        """Retorna estadísticas resumidas del ciclo actual"""
        ciclo = self._state["evolucion_lotoplus"]["ciclo_actual"]
        return {
            "sorteos_completados": ciclo["sorteos_completados"],
            "restantes": ciclo["objetivo"] - ciclo["sorteos_completados"],
            "fase_actual": ciclo["fase_actual"],
            "aciertos_4": ciclo["metricas_acumuladas"]["total_aciertos_4"],
            "aciertos_5": ciclo["metricas_acumuladas"]["total_aciertos_5"],
            "aciertos_6": ciclo["metricas_acumuladas"]["total_aciertos_6"],
            "delta_promedio": ciclo["metricas_acumuladas"]["delta_promedio_vs_random"],
            "ventaja_actual": ciclo["metricas_acumuladas"]["ventaja_actual"]
        }

    def get_ranking_herramientas(self) -> dict:
        """Retorna el ranking actual de herramientas"""
        return self._state["evolucion_lotoplus"].get("ranking_herramientas", {})

    def reset_ciclo(self, nuevo_inicio: int = None):
        """
        Resetea el ciclo actual y comienza uno nuevo.
        Útil después de completar 50 sorteos o para reiniciar.
        """
        nuevo_inicio = nuevo_inicio or self._get_current_sorteo()
        fase = self.get_fase(nuevo_inicio)
        
        self._state["evolucion_lotoplus"]["ciclo_actual"] = {
            "sorteo_inicio": nuevo_inicio,
            "sorteo_actual": nuevo_inicio,
            "sorteos_completados": 0,
            "objetivo": 50,
            "fase_actual": fase,
            "ultimos_50_juegos": [],
            "metricas_acumuladas": {
                "total_aciertos_4": 0,
                "total_aciertos_5": 0,
                "total_aciertos_6": 0,
                "delta_promedio_vs_random": 0,
                "ventaja_actual": 0
            }
        }
        self._save_state()

    def puede_ver_resultado(self, sorteo: int) -> bool:
        """
        Determina si el sistema puede ver el resultado de un sorteo.
        En entrenamiento: SÍ
        En validación ciega: NO (solo después de predecir)
        En predicción en vivo: NO (solo después de predecir)
        En operacional real: NO (no existe resultado)
        """
        fase = self.get_fase(sorteo)
        return fase == "entrenamiento"

    def _regenerar_papers_mejor_agente(self, sorteo_actual: int):
        """
        Regenera el paper del agente con mejor performance reciente.
        Se ejecuta automáticamente cada N sorteos.
        """
        try:
            from mejorar_papers import mejorar_paper
            
            # Obtener estadísticas de los últimos 10 sorteos
            ultimos = self.get_ultimos_juegos(10)
            if not ultimos:
                logger.info("No hay sorteos suficientes para regenerar papers")
                return
            
            # Determinar mejor agente basado en aciertos
            historial = self._state["evolucion_lotoplus"].get("historial_agentes", {})
            
            mejor_score = 0
            mejor_agente = None
            
            # Evaluar cada agente por sus aciertos recientes
            for agente_id in ["estadistico_integral", "gpt_auditor", "viejo_deepseek", "gemini_cuantico", "viejo_lobo_rey", "nuevo_deepseek_saaop"]:
                if agente_id in historial:
                    # Para los que tienen aciertos_4+
                    aciertos_recientes = len(historial[agente_id].get("aciertos_4+", [])) if "aciertos_4+" in historial[agente_id] else 0
                    if aciertos_recientes > mejor_score:
                        mejor_score = aciertos_recientes
                        mejor_agente = agente_id
            
            if mejor_agente and mejor_score > 0:
                import logging
                logging.getLogger(__name__).info(f"🔄 Regenerando paper para {mejor_agente} (aciertos recientes: {mejor_score})")
                mejorar_paper(mejor_agente, usar_llm=False)
            else:
                # Si no hay un claro ganador, regenerar solo el Estadístico como base
                import logging
                logging.getLogger(__name__).info("🔄 No hay ganador claro, regenerando paper del Estadístico Integral")
                mejorar_paper("estadistico_integral", usar_llm=False)
                    
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Error en regeneración automática de papers: {e}")
