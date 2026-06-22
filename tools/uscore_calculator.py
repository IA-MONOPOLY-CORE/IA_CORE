"""
U-Score v2.1 Calculator - Herramienta independiente para evaluación en tiempo real
No depende del pipeline de debate. Evaluación instantánea de cualquier combinación.
USANDO HISTÓRICO REAL DE LOTO PLUS (3511-3885)
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from collections import Counter
import math
import json
import os


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
                os.path.dirname(os.path.dirname(__file__)), 
                "lotoplus_completo_3511_3885.json"
            )
        self.historical_data_path = historical_data_path
        self.historical_draws = self._load_historical_draws()
        self.zones = self._define_zones()
        
    def _load_historical_draws(self) -> List[List[int]]:
        """Cargar sorteos históricos reales del JSON"""
        if not os.path.exists(self.historical_data_path):
            print(f"⚠️ No se encontró {self.historical_data_path}")
            return []
        
        with open(self.historical_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        draws = []
        
        # La estructura es: {'metadata': {...}, 'sorteos': [...]}
        if isinstance(data, dict) and 'sorteos' in data:
            sorteos = data['sorteos']
        elif isinstance(data, list):
            sorteos = data
        else:
            sorteos = []
        
        for draw in sorteos:
            # Buscar números del Match dentro de resultados
            numeros = None
            if 'resultados' in draw and 'Match' in draw['resultados']:
                numeros = draw['resultados']['Match'].get('numeros')
            elif 'match' in draw:
                numeros = draw['match']
            elif 'numeros' in draw:
                numeros = draw['numeros']
            
            if numeros is None:
                continue
            
            # Convertir a lista de enteros
            if isinstance(numeros, str):
                numeros = [int(x) for x in numeros.split('-')]
            elif isinstance(numeros, list):
                numeros = [int(x) for x in numeros]
            
            if numeros and len(numeros) == 6:
                draws.append(sorted(numeros))
        
        print(f"✅ Cargados {len(draws)} sorteos históricos reales")
        return draws
    
    def _define_zones(self) -> Dict[str, Tuple[int, int]]:
        """9 zonas de 5 números (0-45, incluyendo el 00)"""
        return {
            'Z1': (0, 4),
            'Z2': (5, 9),
            'Z3': (10, 14),
            'Z4': (15, 19),
            'Z5': (20, 24),
            'Z6': (25, 29),
            'Z7': (30, 34),
            'Z8': (35, 39),
            'Z9': (40, 45),
        }
    
    def _get_zone(self, num: int) -> str:
        for zone, (low, high) in self.zones.items():
            if low <= num <= high:
                return zone
        return None
    
    def _popularidad_numero(self, n: int) -> float:
        if n == 0:
            return 0.05
        elif 1 <= n <= 12:
            return 0.90
        elif 13 <= n <= 31:
            return 0.70
        else:
            return 0.20
    
    def _calc_ipn(self, combinacion: List[int]) -> float:
        popularidades = [self._popularidad_numero(n) for n in combinacion]
        promedio_pop = sum(popularidades) / 6
        ipn_raw = 30 * (1 - promedio_pop)
        ipn = (ipn_raw - 0.75) / (28.5 - 0.75) * 100
        return max(0, min(100, ipn))
    
    def _detectar_patrones(self, combinacion: List[int]) -> int:
        penalizacion = 0
        nums = sorted(combinacion)
        
        for i in range(len(nums) - 1):
            if nums[i+1] - nums[i] == 1:
                penalizacion += 2
        
        consecutivos = 1
        for i in range(len(nums) - 1):
            if nums[i+1] - nums[i] == 1:
                consecutivos += 1
            else:
                if consecutivos >= 3:
                    penalizacion += 5
                consecutivos = 1
        if consecutivos >= 3:
            penalizacion += 5
        
        digitos = [n % 10 for n in nums]
        for d in set(digitos):
            if digitos.count(d) >= 3:
                penalizacion += 3
                break
        
        pares = sum(1 for n in nums if n % 2 == 0)
        if pares == 6 or pares == 0:
            penalizacion += 8
        
        suma = sum(nums)
        if 100 <= suma <= 160:
            penalizacion += 5
        
        return penalizacion
    
    def _calc_pp(self, combinacion: List[int]) -> float:
        penalizacion = self._detectar_patrones(combinacion)
        pp_raw = max(0, 25 - penalizacion)
        return min(100, pp_raw * 4)
    
    def _calc_pz(self, combinacion: List[int]) -> float:
        pesos_zona = {
            'Z1': 0.9, 'Z2': 0.2, 'Z3': 0.2, 'Z4': 0.3,
            'Z5': 0.5, 'Z6': 0.6, 'Z7': 0.7, 'Z8': 0.8, 'Z9': 0.9
        }
        pesos = [pesos_zona.get(self._get_zone(n), 0.5) for n in combinacion]
        promedio_zonal = sum(pesos) / 6
        return (promedio_zonal - 0.2) / 0.7 * 100
    
    def _calc_dsi(self, combinacion: List[int]) -> float:
        suma = sum(combinacion)
        ideal = 140
        tolerancia = 40
        desvio = abs(suma - ideal)
        if desvio <= tolerancia:
            return 100 * (1 - desvio / tolerancia)
        return 0
    
    def _calc_cd(self, combinacion: List[int]) -> float:
        nums = sorted(combinacion)
        gaps = [nums[i+1] - nums[i] for i in range(5)]
        desviacion = math.sqrt(sum((g - sum(gaps)/5)**2 for g in gaps) / 5) if gaps else 0
        if desviacion < 2:
            return 20
        elif desviacion > 12:
            return 30
        else:
            return min(100, 50 + (desviacion - 3) * 8)
    
    def _calc_sd(self, combinacion: List[int]) -> float:
        decenas = [n // 10 for n in combinacion]
        max_concentracion = max(Counter(decenas).values()) if decenas else 0
        if max_concentracion >= 4:
            return 0
        elif max_concentracion == 3:
            return 50
        return 100
    
    def calculate(self, combinacion: List[int]) -> UScoreResult:
        if len(combinacion) != 6:
            raise ValueError("La combinación debe tener exactamente 6 números")
        if not all(0 <= n <= 45 for n in combinacion):
            raise ValueError("Todos los números deben estar entre 0 y 45")
        
        ipn = self._calc_ipn(combinacion)
        pp = self._calc_pp(combinacion)
        pz = self._calc_pz(combinacion)
        dsi = self._calc_dsi(combinacion)
        cd = self._calc_cd(combinacion)
        sd = self._calc_sd(combinacion)
        
        total = (ipn * 0.35 + pp * 0.25 + pz * 0.20 + 
                 dsi * 0.12 + cd * 0.08 + sd * 0.10)
        
        es_estructural_optima = total >= 66
        diagnostico = self._generar_diagnostico(total)
        
        return UScoreResult(
            total=round(total, 2),
            ipn=round(ipn, 2),
            pp=round(pp, 2),
            pz=round(pz, 2),
            dsi=round(dsi, 2),
            cd=round(cd, 2),
            sd=round(sd, 2),
            combinacion=sorted(combinacion),
            es_estructural_optima=es_estructural_optima,
            diagnostico=diagnostico
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
            "frecuencia_promedio": sum(frecuencias.values()) / len(frecuencias)
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
            "sd": result.sd
        },
        "diagnostico": result.diagnostico,
        "es_optima": result.es_estructural_optima
    }


def get_historical_stats() -> Dict[str, Any]:
    calc = UScoreCalculator()
    return calc.get_historical_stats()


if __name__ == "__main__":
    test = [2, 8, 13, 16, 25, 41]
    resultado = calcular_uscore(test)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))