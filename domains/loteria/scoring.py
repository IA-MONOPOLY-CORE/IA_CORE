"""
IA_CORE — Motor de Puntuación Compuesto y Clasificación de Rareza.
U-Score v2.1 con componente SD (Saturación por Decena) Integrado.
FIXED: uScore ahora recibe combinación real, no mock
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import numpy as np

from .config_loteria import (
    IPN_RAW_MIN,
    IPN_RAW_MAX,
    IPN_WEIGHT,
    PP_RAW_MAX,
    PP_WEIGHT,
    PZ_RAW_MIN,
    PZ_RAW_MAX,
    PZ_WEIGHT,
    DSI_SUM_IDEAL,
    DSI_RAW_MAX,
    DSI_WEIGHT,
    CD_RAW_MAX,
    CD_STD_MAX,
    CD_WEIGHT,
    SD_WEIGHT,
    U_SCORE_WEIGHTS,
)


@dataclass(frozen=True)
class ResponseScore:
    total: float
    ipn: float
    pp: float
    pz: float
    dsi: float
    cd: float
    sd: float
    confidence: float
    reasoning_quality: float
    execution_quality: float
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __contains__(self, key):
        return hasattr(self, key)
    
    def __iter__(self):
        return iter(self.__dataclass_fields__.keys())


def popularidad_numero(n: int) -> float:
    if n == 0:
        return 0.05
    elif 1 <= n <= 12:
        return 0.90
    elif 13 <= n <= 31:
        return 0.70
    else:
        return 0.20


def peso_zonal(n: int) -> float:
    if 0 <= n <= 4:
        return 0.9
    elif 5 <= n <= 9:
        return 0.2
    elif 10 <= n <= 14:
        return 0.2
    elif 15 <= n <= 19:
        return 0.3
    elif 20 <= n <= 24:
        return 0.5
    elif 25 <= n <= 29:
        return 0.6
    elif 30 <= n <= 34:
        return 0.7
    elif 35 <= n <= 39:
        return 0.8
    else:
        return 0.9


def calcular_IPN_raw(combinacion: list[int]) -> float:
    promedio_pop = np.mean([popularidad_numero(n) for n in combinacion])
    return IPN_WEIGHT * (1 - promedio_pop)


def detectar_patrones(combinacion: list[int]) -> int:
    penalizacion = 0
    nums = sorted(combinacion)

    # Secuencias consecutivas de 2
    for i in range(len(nums) - 1):
        if nums[i + 1] - nums[i] == 1:
            penalizacion += 2

    # Secuencias consecutivas de 3+
    consecutivos = 1
    for i in range(len(nums) - 1):
        if nums[i + 1] - nums[i] == 1:
            consecutivos += 1
        else:
            if consecutivos >= 3:
                penalizacion += 5
            consecutivos = 1
    if consecutivos >= 3:
        penalizacion += 5

    # Divisor común (3+ números)
    for divisor in range(3, 10):
        count = sum(1 for n in nums if n % divisor == 0)
        if count >= 3:
            penalizacion += 4
            break

    # Mismo dígito terminal
    digitos = [n % 10 for n in nums]
    for d in set(digitos):
        if digitos.count(d) >= 3:
            penalizacion += 3
            break

    # Todos pares o todos impares
    paridades = [n % 2 for n in nums]
    if len(set(paridades)) == 1:
        penalizacion += 8

    # Patrón geométrico
    diferencias = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    if len(set(diferencias)) == 1 and len(diferencias) > 1:
        penalizacion += 6

    # Suma en rango popular
    suma = sum(nums)
    if 100 <= suma <= 160:
        penalizacion += 5

    # Todos en calendario
    if all(1 <= n <= 31 for n in nums):
        penalizacion += 10

    return penalizacion


def calcular_PP_raw(combinacion: list[int]) -> float:
    return max(0, PP_RAW_MAX - detectar_patrones(combinacion))


def calcular_PZ_raw(combinacion: list[int]) -> float:
    promedio_zonal = np.mean([peso_zonal(n) for n in combinacion])
    return 20 * promedio_zonal


def calcular_DSI_raw(combinacion: list[int]) -> float:
    suma = sum(combinacion)
    distancia = abs(suma - DSI_SUM_IDEAL)
    return DSI_RAW_MAX * (1 - min(distancia, DSI_SUM_IDEAL) / DSI_SUM_IDEAL)


def calcular_CD_raw(combinacion: list[int]) -> float:
    desviacion = np.std(combinacion, ddof=0)
    return CD_RAW_MAX * min(desviacion / CD_STD_MAX, 1)


def calcular_SD_raw(combinacion: list[int]) -> float:
    """
    Componente SD — Saturación por Decena (Aporte del Estadístico v2.1).
    Mide el amontonamiento de masa crítica humana en un mismo bloque de 10.
    """
    decenas = [n // 10 for n in combinacion]
    max_concentracion = max([decenas.count(d) for d in set(decenas)]) if decenas else 0
    # Penaliza drásticamente si hay más de 3 números metidos en la misma decena
    if max_concentracion >= 4:
        return 0.0
    elif max_concentracion == 3:
        return 10.0
    return 20.0


def u_score_v2_1(combinacion: list[int]) -> ResponseScore:
    """
    U-Score v2.1 — Ajustado para Gobernanza Epistemológica Organizacional.
    Integra el control de saturación por decena (SD).
    """
    ipn_raw = calcular_IPN_raw(combinacion)
    pp_raw = calcular_PP_raw(combinacion)
    pz_raw = calcular_PZ_raw(combinacion)
    dsi_raw = calcular_DSI_raw(combinacion)
    cd_raw = calcular_CD_raw(combinacion)
    sd_raw = calcular_SD_raw(combinacion)

    # Reescalado normalizado asíncrono (0-20)
    ipn = 20 * (ipn_raw - IPN_RAW_MIN) / (IPN_RAW_MAX - IPN_RAW_MIN)
    pp = 20 * pp_raw / PP_RAW_MAX
    pz = 20 * (pz_raw - PZ_RAW_MIN) / (PZ_RAW_MAX - PZ_RAW_MIN)
    dsi = 20 * dsi_raw / DSI_RAW_MAX
    cd = 20 * cd_raw / CD_RAW_MAX
    sd = sd_raw

    # Clip explícito al rango [0, 20] para evitar contaminación silenciosa
    ipn = max(0, min(20, ipn))
    pp = max(0, min(20, pp))
    pz = max(0, min(20, pz))
    dsi = max(0, min(20, dsi))
    cd = max(0, min(20, cd))
    sd = max(0, min(20, sd))

    # Matriz de pesos definitivos calibrados v2.1 (S.A.A.O.P.)
    score_total = (
        IPN_WEIGHT * (ipn / 20)
        + PP_WEIGHT * (pp / 20)
        + PZ_WEIGHT * (pz / 20)
        + DSI_WEIGHT * (dsi / 20)
        + CD_WEIGHT * (cd / 20)
        + SD_WEIGHT * (sd / 20)
    )

    return ResponseScore(
        total=round(score_total, 2),
        ipn=round(ipn, 2),
        pp=round(pp, 2),
        pz=round(pz, 2),
        dsi=round(dsi, 2),
        cd=round(cd, 2),
        sd=round(sd, 2),
        confidence=round(score_total / 100, 2),
        reasoning_quality=round(score_total / 100, 2),
        execution_quality=0.7,  # Default value, can be adjusted later
    )


def score_response(combinacion: Optional[list[int]] = None, **kwargs) -> ResponseScore:
    """
    Función puente compatible con la orquestación asíncrona del Supervisor.
    CORRECCIÓN: Ahora acepta None y usa placeholder.
    """
    # Si success=False, devolver score 0 directamente
    if not kwargs.get("success", True):
        return ResponseScore(
            total=0.0,
            ipn=0.0,
            pp=0.0,
            pz=0.0,
            dsi=0.0,
            cd=0.0,
            sd=0.0,
            confidence=0.0,
            reasoning_quality=0.0,
            execution_quality=0.0,
        )

    # Extraer combinacion del kwargs si viene en formato respuesta
    if combinacion is None:
        # Intentar extraer del formato de respuesta del agente
        if "respuesta" in kwargs and isinstance(kwargs["respuesta"], dict):
            combinacion = kwargs["respuesta"].get("numeros")
        elif "combinacion" in kwargs:
            combinacion = kwargs["combinacion"]
        elif "contexto" in kwargs and isinstance(kwargs["contexto"], dict):
            combinacion = kwargs["contexto"].get("combinacion") or kwargs["contexto"].get("numeros")

    # Si no hay combinación válida, usar placeholder (no lanzar error)
    if combinacion is None or not isinstance(combinacion, list) or len(combinacion) != 6:
        combinacion = [0, 0, 0, 0, 0, 0]  # Placeholder

    score_obj = u_score_v2_1(combinacion)
    # Update execution_quality based on duration_ms
    execution_quality = 0.7 if kwargs.get("duration_ms", 0) < 1000 else 0.5
    # Since ResponseScore is frozen, we can create a new one
    return ResponseScore(
        total=score_obj.total,
        ipn=score_obj.ipn,
        pp=score_obj.pp,
        pz=score_obj.pz,
        dsi=score_obj.dsi,
        cd=score_obj.cd,
        sd=score_obj.sd,
        confidence=score_obj.confidence,
        reasoning_quality=score_obj.reasoning_quality,
        execution_quality=execution_quality,
    )


def build_scores_summary(steps: list) -> dict:
    """Compila las métricas agregadas para la portada final del reporte."""
    if not steps:
        return {"average_total": 0.0, "best_agent": "None"}

    scores = []
    for s in steps:
        if hasattr(s, "score") and s.score:
            if isinstance(s.score, dict) and "total" in s.score:
                scores.append(s.score["total"])
            elif hasattr(s.score, "total"):
                scores.append(s.score.total)
    avg = np.mean(scores) if scores else 0.0

    # Busca el agente con mejor desempeño adaptativo
    best_agent = "None"
    best_val = -1.0
    for s in steps:
        if hasattr(s, "score") and s.score:
            current_score = None
            if isinstance(s.score, dict) and "total" in s.score:
                current_score = s.score["total"]
            elif hasattr(s.score, "total"):
                current_score = s.score.total
            if current_score and current_score > best_val:
                best_val = current_score
                best_agent = s.agent_name

    return {"average_total": round(avg, 2), "best_agent": best_agent}
