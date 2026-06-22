"""Backtesting ciego sorteo por sorteo - Mide aciertos en 4/5/6."""

import sys
import json
import time
import asyncio
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.evolution import EvolutionManager
from core.supervisor import Supervisor
from core.orchestration import ExecutionMode


def cargar_sorteos_reales():
    ruta = Path("lotoplus_completo_3511_3885.json")
    if not ruta.exists():
        print(f"❌ No se encuentra {ruta}")
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    sorteos = data.get("sorteos", [])
    sorteos_filtrados = [s for s in sorteos if s.get("sorteo", 0) >= 3800]
    print(f"📊 Cargados {len(sorteos_filtrados)} sorteos (desde 3800)")
    return sorted(sorteos_filtrados, key=lambda x: x["sorteo"])


def extraer_numeros_de_texto(texto: str):
    """Extrae 6 números (0-45) del texto de un agente."""
    if not texto:
        return []
    numeros = list(map(int, re.findall(r'\b([0-4]?[0-9]|45)\b', texto)))
    return list(dict.fromkeys(numeros))[:6]


def calcular_mejores_aciertos(numeros_jugados, resultados_reales):
    """Devuelve max_aciertos, mejor_modalidad, flags 4/5/6."""
    if not numeros_jugados:
        return 0, "N/A", False, False, False
    set_jugados = set(numeros_jugados)
    modalidades = ["Match", "Tradicional", "Desquite", "Sale o Sale"]
    max_aciertos = 0
    mejor_modalidad = "Ninguna"
    for modalidad in modalidades:
        numeros_ganadores = set(resultados_reales.get(modalidad, {}).get("numeros", []))
        aciertos = len(set_jugados.intersection(numeros_ganadores)) if numeros_ganadores else 0
        if aciertos > max_aciertos:
            max_aciertos = aciertos
            mejor_modalidad = modalidad
    es_4 = max_aciertos >= 4
    es_5 = max_aciertos >= 5
    es_6 = max_aciertos >= 6
    return max_aciertos, mejor_modalidad, es_4, es_5, es_6


def extraer_resultados_reales(sorteo_data):
    resultados = sorteo_data.get("resultados", {})
    return {
        "Match": {"numeros": resultados.get("Match", {}).get("numeros", [])},
        "Tradicional": {"numeros": resultados.get("Tradicional", {}).get("numeros", [])},
        "Desquite": {"numeros": resultados.get("Desquite", {}).get("numeros", [])},
        "Sale o Sale": {"numeros": resultados.get("Sale o Sale", {}).get("numeros", [])},
        "Plus": int(resultados.get("Plus", {}).get("numero", sorteo_data.get("numero_plus", 0)))
    }


def extraer_jugada_mejor_agente(resultado, mejor_agente_nombre):
    for step in resultado.steps:
        if step.agent_name == mejor_agente_nombre and step.success:
            texto = step.result.get("output", "") if isinstance(step.result, dict) else str(step.result)
            return extraer_numeros_de_texto(texto)
    return []


async def ejecutar_backtest_ciego():
    print("=" * 70)
    print("🔬 BACKTESTING CIEGO S.A.A.O.P. (MIDE ACIERTOS 4, 5 Y 6)")
    print("=" * 70)

    sorteos_reales = cargar_sorteos_reales()
    if not sorteos_reales:
        return

    supervisor = Supervisor()
    supervisor.start()
    evolution = EvolutionManager()

    total_4 = 0
    total_5 = 0
    total_6 = 0
    resultados_por_sorteo = []

    for idx, sorteo_data in enumerate(sorteos_reales):
        sorteo_num = sorteo_data.get("sorteo")
        print(f"\n{'='*70}")
        print(f"📅 PROCESANDO SORTEO {sorteo_num} ({idx+1}/{len(sorteos_reales)})")
        print(f"{'='*70}")

        fase = evolution.get_fase(sorteo_num)
        print(f"   Fase: {fase}")

        resultados_reales = extraer_resultados_reales(sorteo_data)
        print(f"   🎲 Resultados reales:")
        for m in ["Match", "Tradicional", "Desquite", "Sale o Sale"]:
            print(f"      {m}: {resultados_reales[m]['numeros']}")
        print(f"      Plus: {resultados_reales['Plus']}")

        task = f"""OBJETIVO: Evaluar la matriz combinatoria bajo las directrices del búnker.
Parámetros: CAZADOR, V19 (3 bajos, 2 medios, 1 alto), suma 110-140, evitar patrones humanos.
FASE: {fase.upper()} | SORTEO ACTUAL: {sorteo_num}
Generá tu análisis y tu combinación de 6 números en formato técnico directo."""

        start_time = time.time()
        resultado = await supervisor.orchestrate_async(task=task, mode=ExecutionMode.DEBATE)
        duration = time.time() - start_time

        mejor_agente = resultado.scores_summary.get('best_agent', 'N/A') if hasattr(resultado, 'scores_summary') else 'N/A'
        jugada_agente = extraer_jugada_mejor_agente(resultado, mejor_agente)

        max_aciertos, mejor_modalidad, es_4, es_5, es_6 = calcular_mejores_aciertos(jugada_agente, resultados_reales)

        if es_4:
            total_4 += 1
        if es_5:
            total_5 += 1
        if es_6:
            total_6 += 1

        resultados_por_sorteo.append({
            "sorteo": sorteo_num,
            "mejor_agente": mejor_agente,
            "jugada": jugada_agente,
            "max_aciertos": max_aciertos,
            "mejor_modalidad": mejor_modalidad,
            "es_4": es_4,
            "es_5": es_5,
            "es_6": es_6
        })

        print(f"\n   🤖 Mejor agente: {mejor_agente}")
        print(f"   🎯 Jugada evaluada: {jugada_agente}")
        print(f"   🏆 Máximos aciertos en una modalidad: {max_aciertos} ({mejor_modalidad})")
        print(f"   ✅ ¿4+ aciertos? {'SÍ' if es_4 else 'NO'} | ¿5+ aciertos? {'SÍ' if es_5 else 'NO'} | ¿6 aciertos? {'SÍ 🎉' if es_6 else 'NO'}")
        print(f"   ⏱️  Duración: {duration:.2f}s")

        evolution.registrar_juego(
            sorteo=sorteo_num,
            prediccion_analyst=jugada_agente,
            prediccion_optimizer=[],
            consenso_final=[],
            uscore_predicho=0,
            resultado_real={"aciertos": max_aciertos}
        )

        await asyncio.sleep(1)

    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL (4, 5 y 6 aciertos)")
    print("=" * 70)
    print(f"   Sorteos analizados: {len(resultados_por_sorteo)}")
    print(f"   Sorteos con al menos 4 aciertos: {total_4}")
    print(f"   Sorteos con al menos 5 aciertos: {total_5}")
    print(f"   Sorteos con 6 aciertos: {total_6}")

    if total_5 > 0 or total_6 > 0:
        print("\n   🎯 Desglose de sorteos con 5+ aciertos:")
        for r in resultados_por_sorteo:
            if r["es_5"] or r["es_6"]:
                print(f"      - Sorteo {r['sorteo']}: {r['max_aciertos']} aciertos ({r['mejor_modalidad']}) - {r['mejor_agente']}")

    supervisor.stop()
    print("\n🏁 Backtesting finalizado.")

if __name__ == "__main__":
    asyncio.run(ejecutar_backtest_ciego())