"""Fachada compatible del U-Score v2.1 oficial definido en ``scoring.py``.

La fórmula vive únicamente en :func:`domains.loteria.scoring.u_score_v2_1`.
Este módulo conserva la API histórica de ``UScoreCalculator`` y
``calcular_uscore`` para sus consumidores existentes.
"""

import json
import os
from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List

from .scoring import u_score_v2_1


@dataclass
class UScoreResult:
    """Resultado completo del cálculo U-Score"""

    total: float
    ipn: float
    pp: float
    pz: float
    dsi: float
    cd: float
    sd: float
    combinacion: List[int]
    es_estructural_optima: bool
    diagnostico: str


class UScoreCalculator:
    """
    Calculadora U-Score v2.1
    Métricas: IPN, PP, PZ, DSI, CD, SD
    Con histórico real de Loto Plus (0-45)
    """

    def __init__(self, historical_data_path: str = None):
        if historical_data_path is None:
            historical_data_path = os.path.join(
                os.path.dirname(__file__), "lotoplus_completo_3511_3885.json"
            )
        self.historical_data_path = historical_data_path
        self.historical_draws = self._load_historical_draws()

    def _load_historical_draws(self) -> List[List[int]]:
        """Cargar sorteos históricos reales del JSON"""
        if not os.path.exists(self.historical_data_path):
            print(f"⚠️ No se encontró {self.historical_data_path}")
            return []

        with open(self.historical_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        draws = []

        # La estructura es: {'metadata': {...}, 'sorteos': [...]}
        if isinstance(data, dict) and "sorteos" in data:
            sorteos = data["sorteos"]
        elif isinstance(data, list):
            sorteos = data
        else:
            sorteos = []

        for draw in sorteos:
            # Buscar números del Match dentro de resultados
            numeros = None
            if "resultados" in draw and "Match" in draw["resultados"]:
                numeros = draw["resultados"]["Match"].get("numeros")
            elif "match" in draw:
                numeros = draw["match"]
            elif "numeros" in draw:
                numeros = draw["numeros"]

            if numeros is None:
                continue

            # Convertir a lista de enteros
            if isinstance(numeros, str):
                numeros = [int(x) for x in numeros.split("-")]
            elif isinstance(numeros, list):
                numeros = [int(x) for x in numeros]

            if numeros and len(numeros) == 6:
                draws.append(sorted(numeros))

        print(f"✅ Cargados {len(draws)} sorteos históricos reales")
        return draws

    def calculate(self, combinacion: List[int]) -> UScoreResult:
        """Calcula mediante la implementación canónica y adapta el resultado."""
        if len(combinacion) != 6:
            raise ValueError("La combinación debe tener exactamente 6 números")
        if not all(0 <= n <= 45 for n in combinacion):
            raise ValueError("Todos los números deben estar entre 0 y 45")

        score = u_score_v2_1(combinacion)

        return UScoreResult(
            total=score.total,
            ipn=score.ipn,
            pp=score.pp,
            pz=score.pz,
            dsi=score.dsi,
            cd=score.cd,
            sd=score.sd,
            combinacion=sorted(combinacion),
            es_estructural_optima=score.total >= 66,
            diagnostico=self._generar_diagnostico(score.total),
        )

    def _generar_diagnostico(self, total: float) -> str:
        if total >= 80:
            return "EXCELENTE - Estructuralmente óptima"
        elif total >= 66:
            return "BUENA - Fuerte potencial estructural"
        elif total >= 50:
            return "ACEPTABLE - Requiere ajustes menores"
        elif total >= 35:
            return "DÉBIL - Pobre estructura combinatoria"
        else:
            return "RECHAZADA - Patrones humanos evidentes"

    def compare(self, combinaciones: List[List[int]]) -> List[UScoreResult]:
        results = [self.calculate(c) for c in combinaciones]
        return sorted(results, key=lambda x: x.total, reverse=True)

    def get_historical_stats(self) -> Dict[str, Any]:
        if not self.historical_draws:
            return {"error": "No hay datos históricos"}

        frecuencias = Counter()
        for draw in self.historical_draws:
            frecuencias.update(draw)

        return {
            "total_sorteos": len(self.historical_draws),
            "numeros_mas_frecuentes": frecuencias.most_common(10),
            "numeros_menos_frecuentes": frecuencias.most_common()[-10:],
            "frecuencia_promedio": sum(frecuencias.values()) / len(frecuencias),
        }


def calcular_uscore(combinacion: List[int], historical_path: str = None) -> Dict[str, Any]:
    if historical_path:
        calc = UScoreCalculator(historical_path)
    else:
        calc = UScoreCalculator()

    result = calc.calculate(combinacion)
    return {
        "combinacion": result.combinacion,
        "uscore_total": result.total,
        "metricas": {
            "ipn": result.ipn,
            "pp": result.pp,
            "pz": result.pz,
            "dsi": result.dsi,
            "cd": result.cd,
            "sd": result.sd,
        },
        "diagnostico": result.diagnostico,
        "es_optima": result.es_estructural_optima,
    }


def get_historical_stats() -> Dict[str, Any]:
    calc = UScoreCalculator()
    return calc.get_historical_stats()


if __name__ == "__main__":
    test = [2, 8, 13, 16, 25, 41]
    resultado = calcular_uscore(test)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
