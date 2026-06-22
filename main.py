"""
S.A.A.O.P. CORE — Runtime de Orquestación y Convergencia de Agentes Cognitivos
Punto de Entrada Oficial con Tensión Lógica y Validación Ciega Asíncrona.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import uuid
from typing import Any

import config
from core.orchestration import ExecutionMode, OrchestrationResult
from core.supervisor import MEMORY_HISTORY_KEY, MEMORY_RESULT_PREFIX, Supervisor

# 🎛️ ARTILLERÍA EXPERTA: IDs exactos que creamos en agents/config/
SAAOOP_BUNKER_AGENTS = [
    "gpt_auditor",           # 1. CRITIC - destruye primero
    "gemini_cuantico",       # 2. ANALYST_ZONAS - densidad energética
    "viejo_lobo_rey",        # 3. ANALYST_HUMAN - cirugía de ruptura
    "estadistico_integral",  # 4. ANALYST_V19 - defiende e integra
    "viejo_deepseek"         # 5. OPTIMIZER - árbitro final
]

# 🧠 CONTEXTO TÁCTICO REAL EXTRAÍDO DE LAS BITÁCORAS EXPERIMENTALES DE I+D
SAAOOP_CRITICAL_TASK = (
    "OBJETIVO TÁCTICO: Evaluar la matriz combinatoria bajo las directrices del búnker.\n\n"
    "PARÁMETROS MATEMÁTICOS DE ENTRADA:\n"
    "- Estado de Régimen Activo: CAZADOR (Predominancia balanceada en zonas bajas Z1-Z4).\n"
    "- Regla de Peso Estructural V19: 3 números bajos, 2 medios, 1 alto. Suma objetivo combinatoria: [110 - 140].\n"
    "- Restricción de Incomodidad Visual: Excluir patrones simétricos, secuenciales o de calendario.\n"
    "- Límite de Fronteras: Forzar evaluación de zonas Z8 y Z9 (40 al 45) para mitigar licuación humana.\n"
    "- Criterio de Cobertura: Estimar eficiencia de Pool con garantía matemática defensiva '4 si 5'.\n"
    "- Límite de Control Epistemológico: Bloquear cualquier sobreajuste que supere el Azar Estructural crítico del 22.1%.\n\n"
    "FLUJO DE DEBATE MANDATORIO:\n"
    "1. GPT Auditor actuará como juez implacable destruyendo sesgos, validando el uScore v2.1 final y controlando el overfitting.\n"
    "2. Gemini Cuántico auditará la densidad energética en los quintetos espaciales vectoriales (ECCD).\n"
    "3. El Viejo Lobo aplicará la cirugía de ruptura (+/-1, +/-2) basándose en la fatiga física del bolillero.\n"
    "4. El Estadístico Integral proyectará la eficiencia del Pool y la optimización del VER (Valor Esperado Real).\n"
    "5. Viejo DeepSeek validará la consistencia del régimen Cazador y bloqueará saltos de distancia bruscos >= 10.\n"
    "El orden de intervención es CRITIC → ANALYST_ZONAS → ANALYST_HUMAN → ANALYST_V19 → OPTIMIZER."
)


def setup_logging() -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format=config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(config.LOG_DIR / "supervisor.log", encoding="utf-8"),
        ],
    )


def _line(char: str = "=", width: int = 72) -> str:
    return char * width


def _format_output(result: Any) -> str:
    if isinstance(result, dict):
        if "output" in result:
            text = str(result["output"])
            if len(text) > 600:
                return text[:600] + "..."
            return text
        return json.dumps(result, indent=2, ensure_ascii=False)[:800]
    return str(result)


def print_orchestration_report(result: OrchestrationResult) -> None:
    summary = result.scores_summary or {}
    debate = result.debate

    print()
    print(_line())
    print(" 🚀 S.A.A.O.P. CORE — Ciclo de Convergencia Multiagente Activado")
    print(_line())
    print()
    print(f"  Task Context   : {result.task[:120]}...")
    print(f"  Execution ID   : {result.execution_id}")
    print(f"  Mode           : {result.mode}")
    print(f"  Bunker Agents  : {', '.join(result.agents)}")
    print(f"  Success        : {result.success}")
    if debate:
        print(f"  Debate ID      : {debate.debate_id}")
        print(f"  Agreement      : {debate.agreement_score:.1f}")
        print(f"  Contradiction  : {debate.contradiction_score:.1f}")

    print()
    print(_line("-"))
    print(" Desarrollo del Debate por Rondas")
    print(_line("-"))

    for step in result.steps:
        status = "OK" if step.success else "ERROR"
        print()
        print(
            f"  [{step.agent_name}]  role={step.role or '-'}  "
            f"round={step.round_number or '-'}  status={status}"
        )
        print(f"    duration      : {step.duration_ms:.1f} ms")

        if isinstance(step.result, dict):
            llm = step.result.get("llm") or {}
            if llm:
                print(
                    f"    llm           : {llm.get('provider', '-')} / {llm.get('model', '-')}"
                    f" ({llm.get('latency_ms', '-')} ms)"
                )

        if step.score:
            print(f"    uScore        : {step.score.total:.1f}")

        if step.success:
            print(f"    argumentación : {_format_output(step.result)}")
        else:
            print(f"    error         : {step.error}")

    if debate and debate.final_response:
        print()
        print(_line("-"))
        print(" Convergencia y Síntesis Final de la Matriz")
        print(_line("-"))
        print()
        print(f"  {_format_output(debate.final_response.get('synthesis', ''))}")

    print()
    print(_line("-"))
    print(" Resumen de Métricas de Calidad (Scores)")
    print(_line("-"))
    print(f"  Average uScore : {summary.get('average_total', 0):.1f}")
    print(f"  Best Performer : {summary.get('best_agent', '-')}")

    print()
    print(_line("-"))
    print(" Trazabilidad y Persistencia")
    print(_line("-"))
    print(f"  Total Duration : {result.duration_ms:.1f} ms")
    print(f"  Steps Count    : {len(result.steps)}")
    print(f"  State File     : {config.MEMORY_STATE_FILE}")
    print()
    print(_line())
    print()


async def run_saaop_orchestration_async(supervisor: Supervisor) -> OrchestrationResult:
    # Verificar proveedores disponibles
    if supervisor.providers.get("nvidia") is None and supervisor.providers.get("ollama") is None:
        raise RuntimeError("No hay proveedores LLM disponibles (nvidia o ollama).")
    
    # Intentar con NVIDIA primero, si no con Ollama
    provider = supervisor.providers.get("nvidia") or supervisor.providers.get("ollama")
    
    if provider is None:
        raise RuntimeError("No se pudo encontrar un proveedor LLM válido.")

    # Invocar la orquestación asíncrona con los 5 agentes del búnker
    return await supervisor.orchestrate_async(
        SAAOOP_CRITICAL_TASK,
        agent_names=SAAOOP_BUNKER_AGENTS,
        mode=ExecutionMode.DEBATE,
    )


async def main_async() -> int:
    setup_logging()
    logger = logging.getLogger("main")

    supervisor = Supervisor(log_dir=config.LOG_DIR)
    await asyncio.to_thread(supervisor.start)

    try:
        logger.info("Iniciando Runtime de debate multi-agente asíncrono S.A.A.O.P.")
        result = await run_saaop_orchestration_async(supervisor)
        print_orchestration_report(result)

        if supervisor.get_orchestration(result.execution_id) is None:
            logger.error("Error crítico: El resultado del debate no se consolidó en la memoria local.")
            return 1

        logger.info("Ciclo táctico ejecutado con éxito.")
        return 0 if result.success else 2
    except Exception:
        logger.exception("Fallo crítico en la ejecución del ciclo cognitivo de S.A.A.O.P.")
        return 1
    finally:
        await asyncio.to_thread(supervisor.shutdown)


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))