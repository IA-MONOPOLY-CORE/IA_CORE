"""Validación ciega y revelación de resultados, específico del dominio Lotería/S.A.A.O.P."""

from __future__ import annotations

import asyncio
import logging
import re
from pathlib import Path
from typing import Any

from core.orchestration import ExecutionMode
from agents.result import (
    calcular_contradiccion_real,
    calcular_acuerdo_real,
    calcular_u_score,
    validar_consenso,
)
from domains.loteria.config_loteria import VALIDATION_AGENTS
from domains.loteria.database_loteria import (
    get_db,
    crear_debate,
    guardar_intervencion,
    actualizar_debate_con_consenso,
    actualizar_debate_con_resultado,
    desbloquear_siguiente_sorteo,
    get_sorteo_by_numero,
    guardar_metrica_acumulada,
)


logger = logging.getLogger(__name__)


def _extraer_numeros_de_respuesta(output: str) -> list[int]:
    numeros = re.findall(r"\b([0-4]?[0-9]|45)\b", output)
    numeros_int = [int(n) for n in numeros if 0 <= int(n) <= 45]
    numeros_unicos = []
    for n in numeros_int:
        if n not in numeros_unicos:
            numeros_unicos.append(n)
        if len(numeros_unicos) == 6:
            break
    return numeros_unicos if len(numeros_unicos) == 6 else []


async def run_validation_debate(
    validation_id: str,
    sorteo: int,
    task: str,
    supervisor: Any,
    evolution: Any,
    validation_store: dict[str, Any],
    record_event: Any,
    track_orchestration: Any,
    serialize_result: Any,
) -> None:
    validation_store[validation_id]["status"] = "running"
    validation_store[validation_id]["sorteo"] = sorteo
    validation_store[validation_id]["fase"] = (
        evolution.get_fase(sorteo) if evolution else "desconocida"
    )

    try:
        debate_id = crear_debate(sorteo, estado="activo")

        result = await supervisor.orchestrate_async(
            task,
            agent_names=VALIDATION_AGENTS,
            mode=ExecutionMode.DEBATE,
        )
        track_orchestration(result)
        record_event("orchestration", f"Validación {validation_id} completada")

        intervenciones = {}
        if hasattr(result, "steps"):
            for step in result.steps:
                agent_name = getattr(step, "agent_name", "")
                output = ""
                if hasattr(step, "result") and step.result:
                    if isinstance(step.result, dict):
                        output = step.result.get("output", str(step.result))
                    else:
                        output = str(step.result)
                if "gpt_auditor" in agent_name.lower():
                    intervenciones["CRITIC"] = output
                elif "gemini_cuantico" in agent_name.lower():
                    intervenciones["ANALYST_ZONES"] = output
                elif "viejo_lobo_rey" in agent_name.lower():
                    intervenciones["ANALYST_HUMAN"] = output
                elif "estadistico_integral" in agent_name.lower():
                    intervenciones["ANALYST_V19"] = output
                elif "viejo_deepseek" in agent_name.lower():
                    intervenciones["OPTIMIZER"] = output
                elif "nuevo_deepseek" in agent_name.lower():
                    intervenciones["ORCHESTRATOR"] = output

            for orden, (agente, contenido) in enumerate(intervenciones.items()):
                guardar_intervencion(debate_id, sorteo, agente, contenido, orden)

        contradiccion = calcular_contradiccion_real(intervenciones)

        prediccion = {}
        synthesis = ""
        if hasattr(result, "debate") and result.debate and hasattr(result.debate, "final_response"):
            fr = result.debate.final_response
            if isinstance(fr, dict):
                synthesis = fr.get("synthesis", "")
            else:
                synthesis = str(fr)

        numeros = _extraer_numeros_de_respuesta(synthesis)
        if len(numeros) >= 6:
            prediccion = {
                "n1": numeros[0],
                "n2": numeros[1],
                "n3": numeros[2],
                "n4": numeros[3],
                "n5": numeros[4],
                "plus": numeros[5] if len(numeros) > 5 else 0,
            }

        u_score_tentativo = 50.0
        if "OPTIMIZER" in intervenciones:
            confianza_match = re.search(
                r"confianza[:\s]*(\d+)", intervenciones["OPTIMIZER"], re.IGNORECASE
            )
            if confianza_match:
                u_score_tentativo = float(confianza_match.group(1))

        resultado_validacion = validar_consenso(intervenciones, contradiccion_minima=20.0)
        puede_avanzar = resultado_validacion["es_valido"]
        estado = "consenso" if puede_avanzar else "bloqueado"

        actualizar_debate_con_consenso(
            debate_id, prediccion, contradiccion, u_score_tentativo, estado
        )

        if puede_avanzar:
            siguiente = sorteo + 1
            if get_sorteo_by_numero(siguiente):
                desbloquear_siguiente_sorteo(sorteo)
                logger.info("Sorteo %s completado. Siguiente: %s desbloqueado", sorteo, siguiente)
            else:
                logger.info("SORTEO %s: Último sorteo de validación. Ciclo completado.", sorteo)
        else:
            logger.warning("Sorteo %s BLOQUEADO: %s", sorteo, resultado_validacion["razon"])

        validation_store[validation_id].update(
            {
                "status": "complete",
                "result": serialize_result(result),
                "prediccion": numeros,
                "contradiccion_real": contradiccion,
                "contradiccion_por_agente": resultado_validacion.get(
                    "contradiccion_por_agente", {}
                ),
                "consenso_valido": puede_avanzar,
                "resultado_revelado": False,
            }
        )

        logger.info(
            "Validación %s completada para sorteo %s (contradicción: %.1f%%)",
            validation_id,
            sorteo,
            contradiccion,
        )

    except Exception as e:
        validation_store[validation_id] = {
            "status": "error",
            "error": str(e),
        }
        record_event("error", f"Validación {validation_id}: {e}")
        logger.exception("Error en validación %s: %s", validation_id, e)


def reveal_validation_result(
    validation_id: str,
    result_data: Any,
    evolution: Any,
    validation_store: dict[str, Any],
) -> dict:
    validation = validation_store.get(validation_id)
    if validation is None:
        raise ValueError("Validación no encontrada")

    if validation.get("resultado_revelado"):
        raise ValueError("Resultado ya fue revelado anteriormente")

    if validation.get("status") != "complete":
        raise ValueError("La validación aún no ha completado la predicción")

    prediccion_numeros = validation.get("prediccion", [])
    sorteo = result_data.sorteo
    resultado_numeros = result_data.numeros_tradicional
    aciertos_declarados = result_data.aciertos

    prediccion_dict = {}
    if len(prediccion_numeros) >= 6:
        prediccion_dict = {
            "n1": prediccion_numeros[0],
            "n2": prediccion_numeros[1],
            "n3": prediccion_numeros[2],
            "n4": prediccion_numeros[3],
            "n5": prediccion_numeros[4],
            "plus": prediccion_numeros[5],
        }

    resultado_dict = {
        "n1": resultado_numeros[0],
        "n2": resultado_numeros[1],
        "n3": resultado_numeros[2],
        "n4": resultado_numeros[3],
        "n5": resultado_numeros[4],
        "plus": resultado_numeros[5] if len(resultado_numeros) > 5 else 0,
    }

    acuerdo_real = calcular_acuerdo_real(prediccion_dict, resultado_dict)
    u_score_real = calcular_u_score(
        prediccion_dict, resultado_dict, confianza_declarada=validation.get("confianza", None)
    )

    if acuerdo_real > 100:
        acuerdo_real = min(acuerdo_real, 100)

    evolution.registrar_juego(
        sorteo=result_data.sorteo,
        prediccion_analyst=prediccion_numeros,
        prediccion_optimizer=prediccion_numeros,
        consenso_final=prediccion_numeros,
        uscore_predicho=u_score_real,
        resultado_real={
            "numeros": resultado_numeros,
            "aciertos": aciertos_declarados,
            "categoria": aciertos_declarados,
        },
        lecciones=f"Validación ciega completada. Aciertos: {aciertos_declarados}, U-Score: {u_score_real}",
    )

    with get_db() as conn:
        cur = conn.execute(
            "SELECT id FROM debates WHERE sorteo_numero = ? ORDER BY id DESC LIMIT 1", (sorteo,)
        )
        row = cur.fetchone()
        if row:
            debate_id = row["id"]
            actualizar_debate_con_resultado(debate_id, resultado_dict, u_score_real, acuerdo_real)

            guardar_metrica_acumulada(
                sorteo,
                {
                    "u_score_acumulado": u_score_real,
                    "ver_acumulado": u_score_real * 0.6,
                    "evf_acumulado": u_score_real * 0.5,
                    "drawdown_actual": 0,
                    "regimen_detectado": validation.get("fase", "desconocido"),
                    "regimen_acertado": aciertos_declarados >= 3,
                    "error_absoluto": abs(acuerdo_real - (validation.get("confianza", 50))),
                    "v19_sigue_vivo": True,
                },
            )

    validation["resultado_revelado"] = True
    validation["resultado_real"] = {"numeros": resultado_numeros, "aciertos": aciertos_declarados}
    validation["aciertos"] = aciertos_declarados
    validation["acuerdo_real"] = acuerdo_real
    validation["u_score_real"] = u_score_real

    logger.info(
        "Resultado revelado para validación %s: %d aciertos, acuerdo real: %.1f%%, U-Score real: %.1f",
        validation_id,
        aciertos_declarados,
        acuerdo_real,
        u_score_real,
    )

    return {
        "validation_id": validation_id,
        "sorteo": result_data.sorteo,
        "aciertos": aciertos_declarados,
        "acuerdo_real": acuerdo_real,
        "u_score_real": u_score_real,
        "message": f"Resultado registrado. Aciertos: {aciertos_declarados}/6, U-Score: {u_score_real}",
    }
