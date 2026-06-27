"""
core/evolution_base.py - Módulo base genérico para gestión de ciclos evolutivos.
Proporciona la infraestructura reutilizable para cualquier sistema que necesite:
- Gestión de un ciclo con fases configurables
- Registro de historial de desempeño por agente
- Ranking de herramientas/estrategias
- Persistencia a JSON
- Hooks para lógica específica del dominio
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class EvolutionManagerBase(ABC):
    """
    Gestor base genérico para ciclos evolutivos.
    Subclases deben implementar la lógica específica de su dominio.
    """

    def __init__(self, memory_path: str = None, state_key: str = "evolucion"):
        """
        Args:
            memory_path: Ruta al archivo JSON de estado
            state_key: Clave principal en el JSON para el estado evolutivo
        """
        self.memory_path = Path(memory_path) if memory_path else None
        self.state_key = state_key
        self._state = None
        self._ultima_regeneracion = 0

        if self.memory_path and self.memory_path.exists():
            self._load_state()
        else:
            self._state = {self.state_key: self._get_default_evolution()}
            if self.memory_path:
                self._save_state()

    def _load_state(self):
        """Carga el estado desde el archivo JSON"""
        with open(self.memory_path, "r", encoding="utf-8") as f:
            self._state = json.load(f)

        # Asegurar que existe la estructura evolutiva
        if self.state_key not in self._state:
            self._state[self.state_key] = self._get_default_evolution()
            self._save_state()
        else:
            # Rellenar campos faltantes en la estructura evolutiva usando el valor por defecto
            default_evolution = self._get_default_evolution()

            # Rellenar campos faltantes en ciclo_actual
            if "ciclo_actual" not in self._state[self.state_key]:
                self._state[self.state_key]["ciclo_actual"] = default_evolution["ciclo_actual"]
            else:
                for key, value in default_evolution["ciclo_actual"].items():
                    if key not in self._state[self.state_key]["ciclo_actual"]:
                        self._state[self.state_key]["ciclo_actual"][key] = value
                    # Si es un diccionario anidado (como metricas_acumuladas), también rellenar sus campos faltantes
                    if isinstance(value, dict) and isinstance(
                        self._state[self.state_key]["ciclo_actual"][key], dict
                    ):
                        for sub_key, sub_value in value.items():
                            if sub_key not in self._state[self.state_key]["ciclo_actual"][key]:
                                self._state[self.state_key]["ciclo_actual"][key][sub_key] = (
                                    sub_value
                                )

        # Asegurar que existe la estructura de ranking de herramientas
        if "ranking_herramientas" not in self._state[self.state_key]:
            self._state[self.state_key]["ranking_herramientas"] = self._get_default_ranking()
        else:
            # Rellenar campos faltantes en ranking_herramientas
            default_ranking = self._get_default_ranking()
            for key, value in default_ranking.items():
                if key not in self._state[self.state_key]["ranking_herramientas"]:
                    self._state[self.state_key]["ranking_herramientas"][key] = value

        self._save_state()

    def _save_state(self):
        """Guarda el estado al archivo JSON"""
        if self.memory_path:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(self._state, f, indent=2, ensure_ascii=False)

    def _get_default_evolution(self) -> dict:
        """
        Retorna la estructura por defecto para el estado evolutivo.
        Las subclases pueden sobrescribir esto para agregar campos específicos.
        """
        return {
            "ciclo_actual": {
                "evento_inicio": 0,
                "evento_actual": 0,
                "eventos_completados": 0,
                "objetivo": 50,
                "fase_actual": self._get_initial_phase(),
                "ultimos_n_juegos": [],
                "metricas_acumuladas": {
                    "total_aciertos": 0,
                    "total_fallos": 0,
                    "delta_promedio_vs_baseline": 0,
                    "ventaja_actual": 0,
                },
            },
            "parametros_evolutivos": {},
            "historial_agentes": {},
            "ultima_regeneracion_papers": 0,
            "frecuencia_regeneracion_papers": 10,
        }

    def _get_default_ranking(self) -> dict:
        """
        Retorna la estructura genérica para el ranking de herramientas.
        Las subclases pueden inicializar herramientas específicas aquí.
        """
        return {
            "herramientas": {},
            "hipotesis_eliminadas": [],
            "hipotesis_supervivientes": [],
            "ultima_actualizacion": None,
        }

    @abstractmethod
    def _get_initial_phase(self) -> str:
        """Retorna la fase inicial del sistema (implementado por subclase)"""
        pass

    @abstractmethod
    def get_fase(self, evento: int) -> str:
        """
        Determina la fase del sistema según el número de evento.
        Implementado por subclase según lógica del dominio.
        """
        pass

    @abstractmethod
    def get_resultados_visibles_hasta(self, evento_actual: int) -> int:
        """
        Retorna el número de evento HASTA el cual el sistema puede ver resultados.
        Implementado por subclase según reglas del dominio.
        """
        pass

    def get_contexto_para_prompt(self, role: str = "analyst", evento_actual: int = None) -> dict:
        """
        Retorna el contexto actual para inyectar en los prompts de los agentes.
        El formato varía según el rol del agente y la fase actual.
        Las subclases pueden extender este método para agregar contexto específico.
        """
        ciclo = self._state[self.state_key]["ciclo_actual"]
        params = self._state[self.state_key].get("parametros_evolutivos", {})
        historial = self._state[self.state_key].get("historial_agentes", {})

        if evento_actual is None:
            # Soporte para sorteo_actual (usado en lotería) si evento_actual no existe
            evento_actual = ciclo.get("evento_actual", ciclo.get("sorteo_actual", 0))

        fase = self.get_fase(evento_actual)

        # Resumen de últimos N resultados (solo visibles) - soporte para ultimos_50_juegos
        ultimos_n = ciclo.get("ultimos_n_juegos", ciclo.get("ultimos_50_juegos", []))
        resultados_visibles_hasta = self.get_resultados_visibles_hasta(evento_actual)

        # Filtrar juegos visibles (soporte para "sorteo" clave)
        juegos_visibles = [
            j for j in ultimos_n if j.get("evento", j.get("sorteo", 0)) <= resultados_visibles_hasta
        ]

        resumen_n = {
            "total_eventos": len(juegos_visibles),
            "aciertos": sum(
                1 for j in juegos_visibles if j.get("aciertos", 0) >= self._get_acierto_threshold()
            ),
            "delta_promedio": ciclo["metricas_acumuladas"].get("delta_promedio_vs_baseline", 0),
        }

        # Instrucción de fase
        instruccion_fase = self._get_instruccion_fase(fase)

        # Contexto base común
        contexto_base = {
            "evento_actual": evento_actual,
            "eventos_completados": ciclo.get(
                "eventos_completados", ciclo.get("sorteos_completados", 0)
            ),
            "objetivo_ciclo": ciclo.get("objetivo", 50),
            "fase_actual": fase,
            "instruccion_fase": instruccion_fase,
            "resultados_visibles_hasta": resultados_visibles_hasta,
            "ultimos_n_resumen": resumen_n,
            "parametros_evolutivos": params,
            # Métricas del ciclo
            "total_aciertos": ciclo["metricas_acumuladas"].get("total_aciertos", 0),
            "total_fallos": ciclo["metricas_acumuladas"].get("total_fallos", 0),
            "delta_promedio_vs_baseline": ciclo["metricas_acumuladas"].get(
                "delta_promedio_vs_baseline", 0
            ),
            "ventaja_actual": ciclo["metricas_acumuladas"].get("ventaja_actual", 0),
        }

        # Agregar información específica por rol (subclases pueden extender)
        contexto_base.update(self._get_contexto_por_rol(role, historial))

        # Agregar ranking de herramientas
        ranking = self._state[self.state_key].get("ranking_herramientas", {})
        contexto_base["ranking_herramientas"] = ranking.get("herramientas", {})

        return contexto_base

    def _get_acierto_threshold(self) -> int:
        """
        Retorna el umbral para considerar un acierto.
        Subclases pueden sobrescribir esto según su dominio.
        """
        return 1

    @abstractmethod
    def _get_instruccion_fase(self, fase: str) -> str:
        """
        Retorna instrucciones específicas según la fase del sistema.
        Implementado por subclase.
        """
        pass

    def _get_contexto_por_rol(self, role: str, historial: dict) -> dict:
        """
        Retorna contexto específico por rol.
        Las subclases pueden sobrescribir para agregar campos específicos.
        """
        return {}

    def registrar_juego(
        self,
        evento: int,
        prediccion_analyst: Any,
        prediccion_optimizer: Any,
        consenso_final: Any,
        metrica_predicha: float,
        resultado_real: Dict[str, Any],
        lecciones: str = "",
    ):
        """
        Registra un juego completado y actualiza todas las métricas evolutivas.
        Las subclases pueden extender este método para lógica específica.
        """
        fase = self.get_fase(evento)

        # Solo registrar en fases de test (subclases pueden ajustar)
        if self._should_skip_registration(fase):
            self._acumular_aprendizaje_entrenamiento(evento, resultado_real)
            return

        ciclo = self._state[self.state_key]["ciclo_actual"]
        historial = self._state[self.state_key].get("historial_agentes", {})

        aciertos = resultado_real.get("aciertos", 0)

        # Crear registro del juego
        juego = {
            "evento": evento,
            "fase": fase,
            "prediccion_analyst": prediccion_analyst,
            "prediccion_optimizer": prediccion_optimizer,
            "consenso_final": consenso_final,
            "metrica_predicha": metrica_predicha,
            "resultado_real": resultado_real,
            "aciertos": aciertos,
            "lecciones_aprendidas": lecciones,
            "timestamp": datetime.now().isoformat(),
        }

        # Actualizar ventana rodante de últimos N
        ventana_size = self._get_ventana_size()
        ultimos_n = ciclo.get("ultimos_n_juegos", [])
        ultimos_n.append(juego)
        if len(ultimos_n) > ventana_size:
            ultimos_n.pop(0)
        ciclo["ultimos_n_juegos"] = ultimos_n

        # Actualizar métricas acumuladas
        if aciertos >= self._get_acierto_threshold():
            ciclo["metricas_acumuladas"]["total_aciertos"] += 1
        else:
            ciclo["metricas_acumuladas"]["total_fallos"] += 1

        # Actualizar historial de agentes (subclases pueden extender)
        self._actualizar_historial_agentes(
            historial, evento, aciertos, lecciones, prediccion_analyst
        )

        # Incrementar contadores del ciclo
        ciclo["eventos_completados"] += 1
        ciclo["evento_actual"] = evento + 1
        ciclo["fase_actual"] = self.get_fase(evento + 1)

        # Recalcular ventaja actual (subclases pueden sobrescribir fórmula)
        self._recalcular_ventaja_actual(ciclo)

        # Regeneración automática de papers (si aplica)
        self._check_regeneracion_papers(evento)

        self._save_state()

    def _should_skip_registration(self, fase: str) -> bool:
        """
        Determina si se debe saltar el registro en esta fase.
        Subclases pueden sobrescribir.
        """
        return fase == self._get_initial_phase()

    def _acumular_aprendizaje_entrenamiento(self, evento: int, resultado_real: Dict[str, Any]):
        """
        En fase de entrenamiento, solo acumulamos aprendizaje sin registrar como juego.
        Subclases pueden extender.
        """
        ciclo = self._state[self.state_key]["ciclo_actual"]
        ciclo["evento_actual"] = evento + 1
        self._save_state()

    def _get_ventana_size(self) -> int:
        """
        Retorna el tamaño de la ventana rodante.
        Subclases pueden sobrescribir.
        """
        return 50

    def _actualizar_historial_agentes(
        self, historial: dict, evento: int, aciertos: int, lecciones: str, prediccion_analyst: Any
    ):
        """
        Actualiza el historial de agentes.
        Subclases deben implementar la lógica específica.
        """
        pass

    def _recalcular_ventaja_actual(self, ciclo: dict):
        """
        Recalcula la ventaja actual.
        Subclases pueden sobrescribir la fórmula.
        """
        if ciclo["metricas_acumuladas"]["total_aciertos"] > 0:
            baseline = self._get_baseline_precision()
            porcentaje_real = (
                ciclo["metricas_acumuladas"]["total_aciertos"] / ciclo["eventos_completados"]
            ) * 100
            ciclo["metricas_acumuladas"]["ventaja_actual"] = (
                round(porcentaje_real / baseline, 2) if baseline > 0 else 0
            )

    def _get_baseline_precision(self) -> float:
        """
        Retorna la precisión baseline del dominio.
        Subclases deben implementar.
        """
        return 22.1

    def _check_regeneracion_papers(self, evento_actual: int):
        """
        Verifica si debe regenerar papers automáticamente.
        Subclases pueden implementar o sobrescribir.
        """
        pass

    def actualizar_parametros(self, nuevos_parametros: Dict[str, Any]):
        """
        Actualiza los parámetros evolutivos después de un debate.
        Solo actualiza los campos que vienen en el diccionario.
        """
        params = self._state[self.state_key].get("parametros_evolutivos", {})
        params.update(nuevos_parametros)
        self._save_state()

    def registrar_herramienta(self, herramienta: str, fue_acertada: bool):
        """
        Registra el desempeño de una herramienta específica para el ranking.
        """
        ranking = self._state[self.state_key].get("ranking_herramientas", {})
        herramientas = ranking.get("herramientas", {})

        if herramienta not in herramientas:
            herramientas[herramienta] = {
                "aciertos": 0,
                "fallos": 0,
                "precision": 0,
                "historial": [],
            }

        if fue_acertada:
            herramientas[herramienta]["aciertos"] += 1
        else:
            herramientas[herramienta]["fallos"] += 1

        total = herramientas[herramienta]["aciertos"] + herramientas[herramienta]["fallos"]
        if total > 0:
            herramientas[herramienta]["precision"] = round(
                herramientas[herramienta]["aciertos"] / total * 100, 2
            )

        herramientas[herramienta]["historial"].append(
            {"evento": self._get_current_evento(), "acerto": fue_acertada}
        )

        ranking["herramientas"] = herramientas
        ranking["ultima_actualizacion"] = str(self._get_current_evento())
        self._state[self.state_key]["ranking_herramientas"] = ranking
        self._save_state()

    def _get_current_evento(self) -> int:
        """Retorna el número del evento actual"""
        return self._state[self.state_key]["ciclo_actual"]["evento_actual"]

    def get_ultimos_juegos(self, n: int = 10) -> List[dict]:
        """Retorna los últimos N juegos registrados"""
        ultimos = self._state[self.state_key]["ciclo_actual"].get("ultimos_n_juegos", [])
        return ultimos[-n:] if ultimos else []

    def get_estadisticas_ciclo(self) -> dict:
        """Retorna estadísticas resumidas del ciclo actual"""
        ciclo = self._state[self.state_key]["ciclo_actual"]
        return {
            "eventos_completados": ciclo["eventos_completados"],
            "restantes": ciclo["objetivo"] - ciclo["eventos_completados"],
            "fase_actual": ciclo["fase_actual"],
            "total_aciertos": ciclo["metricas_acumuladas"]["total_aciertos"],
            "total_fallos": ciclo["metricas_acumuladas"]["total_fallos"],
            "delta_promedio": ciclo["metricas_acumuladas"]["delta_promedio_vs_baseline"],
            "ventaja_actual": ciclo["metricas_acumuladas"]["ventaja_actual"],
        }

    def get_ranking_herramientas(self) -> dict:
        """Retorna el ranking actual de herramientas"""
        return self._state[self.state_key].get("ranking_herramientas", {})

    def reset_ciclo(self, nuevo_inicio: int = None):
        """
        Resetea el ciclo actual y comienza uno nuevo.
        Útil después de completar N eventos o para reiniciar.
        """
        nuevo_inicio = nuevo_inicio or self._get_current_evento()
        fase = self.get_fase(nuevo_inicio)

        self._state[self.state_key]["ciclo_actual"] = {
            "evento_inicio": nuevo_inicio,
            "evento_actual": nuevo_inicio,
            "eventos_completados": 0,
            "objetivo": 50,
            "fase_actual": fase,
            "ultimos_n_juegos": [],
            "metricas_acumuladas": {
                "total_aciertos": 0,
                "total_fallos": 0,
                "delta_promedio_vs_baseline": 0,
                "ventaja_actual": 0,
            },
        }
        self._save_state()

    def puede_ver_resultado(self, evento: int) -> bool:
        """
        Determina si el sistema puede ver el resultado de un evento.
        Subclases pueden sobrescribir según reglas del dominio.
        """
        fase = self.get_fase(evento)
        return fase == self._get_initial_phase()
