"""
S.A.A.O.P. — Servidor FastAPI
Expone el sistema multiagente como API REST.
Ejecutar: uvicorn api:app --host 0.0.0.0 --port 8000 --reload
"""

from __future__ import annotations

import asyncio
import json
import logging
import shutil
import sys
import uuid
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
from domains.loteria.config_loteria import VALIDATION_AGENTS
from core.supervisor import Supervisor
from core.orchestration import ExecutionMode
from domains.loteria.evolution_loteria import EvolutionManagerLoteria as EvolutionManager
from memory.database import (
    init_db,
    get_db,
    crear_debate,
    guardar_intervencion,
    actualizar_debate_con_consenso,
    actualizar_debate_con_resultado,
    get_v19_status,
    get_sorteo_by_numero,
    desbloquear_siguiente_sorteo,
    guardar_metrica_acumulada,
)
from agents.result import (
    calcular_contradiccion_real,
    calcular_acuerdo_real,
    calcular_u_score,
    validar_consenso,
)

# ─── Logging ────────────────────────────────────────────────────────────────
config.LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format=config.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(config.LOG_DIR / "api.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("api")


def _release_agent_vector_memory(agent_id: str) -> None:
    memoria_module = sys.modules.get("core.memoria_perpetua")
    memoria_vectorial = getattr(memoria_module, "MemoriaVectorial", None)
    instances = getattr(memoria_vectorial, "_instances", None)
    if not isinstance(instances, dict):
        return

    instance = instances.pop(agent_id, None)
    if instance is None:
        return

    client = getattr(instance, "client", None)
    if client is not None and hasattr(client, "close"):
        try:
            client.close()
        except Exception as e:
            logger.warning(f"No se pudo cerrar ChromaDB para {agent_id}: {e}")

    instance.collection = None
    instance.client = None


def _delete_agent_directory(path: Path, agent_id: str, label: str) -> None:
    try:
        shutil.rmtree(path)
        logger.info(f"🗑️ Eliminada {label} de {agent_id}")
    except FileNotFoundError:
        return


# ─── App ────────────────────────────────────────────────────────────────────
app = FastAPI(title="S.A.A.O.P. API", version="2.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Estado global ──────────────────────────────────────────────────────────
supervisor: Supervisor | None = None
evolution: EvolutionManager | None = None
debate_store: dict[str, dict[str, Any]] = {}
validation_store: dict[str, dict[str, Any]] = {}
conversation_history: dict[str, list[dict]] = {}

# VALIDATION_AGENTS movido a domains/loteria/config_loteria.py

SAAOP_TASK = (
    "OBJETIVO TÁCTICO: Evaluar la matriz combinatoria bajo las directrices del búnker.\n\n"
    "PARÁMETROS:\n"
    "- Régimen activo: CAZADOR (zonas bajas Z1-Z4)\n"
    "- Regla V19: 3 números bajos, 2 medios, 1 alto. Suma 110-140\n"
    "- Excluir patrones simétricos, secuenciales o de calendario\n"
    "- Evaluar zonas Z8/Z9 (40-45) para mitigar licuación humana\n"
    "- Garantía matemática defensiva '4 si 5'\n"
    "- Bloquear sobreajuste > 22.1% (azar estructural baseline)"
)

# ─── Límites del sistema ─────────────────────────────────────────────────────
TRAINING_END = 3799
BLIND_TEST_START = 3800
BLIND_TEST_END = 3850
LIVE_TEST_START = 3851
LIVE_TEST_END = 3885


# ─── Lifecycle ──────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup() -> None:
    global supervisor, evolution
    supervisor = Supervisor(log_dir=config.LOG_DIR)
    evolution = EvolutionManager()
    await asyncio.to_thread(supervisor.start)
    init_db()
    logger.info("S.A.A.O.P. API lista")


@app.on_event("shutdown")
async def shutdown() -> None:
    if supervisor:
        await asyncio.to_thread(supervisor.shutdown)
    logger.info("S.A.A.O.P. API detenida")


# ─── Helpers ────────────────────────────────────────────────────────────────
def _serialize_result(result: Any) -> dict:
    try:
        steps_data = []
        if hasattr(result, "steps") and result.steps:
            for step in result.steps:
                score_value = None
                if hasattr(step, "score") and step.score is not None:
                    if hasattr(step.score, "total"):
                        score_value = step.score.total
                    elif isinstance(step.score, (int, float)):
                        score_value = step.score
                    elif isinstance(step.score, dict) and "total" in step.score:
                        score_value = step.score["total"]

                output_value = None
                if hasattr(step, "result") and step.result is not None:
                    if isinstance(step.result, dict):
                        output_value = str(step.result.get("output", step.result))
                    elif isinstance(step.result, str):
                        output_value = step.result
                    else:
                        output_value = str(step.result)

                steps_data.append(
                    {
                        "agent_name": getattr(step, "agent_name", "unknown"),
                        "role": getattr(step, "role", None),
                        "round_number": getattr(step, "round_number", None),
                        "success": getattr(step, "success", False),
                        "error": getattr(step, "error", None),
                        "duration_ms": round(getattr(step, "duration_ms", 0) or 0, 1),
                        "score": score_value,
                        "output": output_value,
                    }
                )

        debate_data = None
        if hasattr(result, "debate") and result.debate is not None:
            debate = result.debate
            synthesis = ""
            if hasattr(debate, "final_response") and debate.final_response:
                if isinstance(debate.final_response, dict):
                    synthesis = debate.final_response.get("synthesis", "")
                else:
                    synthesis = str(debate.final_response)
            debate_data = {
                "debate_id": getattr(debate, "debate_id", None),
                "agreement_score": getattr(debate, "agreement_score", 0),
                "contradiction_score": getattr(debate, "contradiction_score", 0),
                "synthesis": synthesis,
            }

        return {
            "execution_id": getattr(result, "execution_id", None),
            "mode": getattr(result, "mode", None),
            "agents": getattr(result, "agents", []),
            "success": getattr(result, "success", False),
            "duration_ms": round(getattr(result, "duration_ms", 0) or 0, 1),
            "started_at": getattr(result, "started_at", None),
            "finished_at": getattr(result, "finished_at", None),
            "steps": steps_data,
            "scores_summary": getattr(result, "scores_summary", {}) or {},
            "debate": debate_data,
        }
    except Exception as e:
        logger.exception("Error serializando resultado: %s", e)
        return {
            "execution_id": getattr(result, "execution_id", "error"),
            "success": False,
            "error": f"Serialization error: {str(e)}",
            "duration_ms": 0,
            "started_at": None,
            "finished_at": None,
            "agents": [],
            "steps": [],
            "debate": None,
            "scores_summary": {},
        }


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


async def _run_validation_debate(validation_id: str, sorteo: int, task: str) -> None:
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
                    intervenciones["ANALYST_ZONAS"] = output
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
                "result": _serialize_result(result),
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
        logger.exception("Error en validación %s: %s", validation_id, e)


async def _run_debate(debate_id: str, task: str) -> None:
    debate_store[debate_id]["status"] = "running"
    try:
        result = await supervisor.orchestrate_async(
            task,
            mode=ExecutionMode.DEBATE,
        )
        debate_store[debate_id] = {
            "status": "complete",
            "result": _serialize_result(result),
        }
        logger.info("Debate %s completado", debate_id)
    except Exception as e:
        debate_store[debate_id] = {
            "status": "error",
            "error": str(e),
        }
        logger.exception("Error en debate %s: %s", debate_id, e)


# ─── Modelos ────────────────────────────────────────────────────────────────
class DebateRequest(BaseModel):
    task: str | None = None


class ValidationResultRequest(BaseModel):
    sorteo: int
    numeros_tradicional: list[int]
    aciertos: int


class ChatRequest(BaseModel):
    message: str
    agent_ids: Optional[List[str]] = None
    conversation_id: Optional[str] = None


class LearnRequest(BaseModel):
    content: str
    agent_id: str
    source: str = "user_input"


class CreateAgentRequest(BaseModel):
    id: str
    role: str
    provider: str = "nvidia"
    model: Optional[str] = None
    system_prompt: str
    temperature: float = 0.3


# ─── Endpoints ──────────────────────────────────────────────────────────────
@app.get("/api/status")
async def get_status() -> dict:
    fase_actual = "desconocida"
    sorteo_actual = 3800
    if evolution:
        stats = evolution.get_estadisticas_ciclo()
        fase_actual = stats.get("fase_actual", "desconocida")
        if hasattr(evolution, "_state"):
            sorteo_actual = evolution._state["evolucion_lotoplus"]["ciclo_actual"]["sorteo_actual"]

    providers_info = []
    if supervisor:
        for provider in supervisor.providers.list_providers():
            name = provider.provider_name()
            is_placeholder = getattr(provider, "IS_PLACEHOLDER", False)
            health = provider.health_check()
            providers_info.append({
                "name": name,
                "is_placeholder": is_placeholder,
                "healthy": health.healthy,
                "message": health.message,
                "models": provider.available_models()
            })

    return {
        "running": supervisor is not None and supervisor.running,
        "providers": providers_info,
        "agents": supervisor.agents.list_ids() if supervisor else [],
        "fase_actual": fase_actual,
        "sorteo_actual": sorteo_actual,
        "limites_sistema": {
            "training_end": TRAINING_END,
            "blind_test_start": BLIND_TEST_START,
            "blind_test_end": BLIND_TEST_END,
            "live_test_start": LIVE_TEST_START,
            "live_test_end": LIVE_TEST_END,
        },
    }


@app.get("/api/metrics/dynamic")
async def get_dynamic_metrics() -> dict:
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    stats = evolution.get_estadisticas_ciclo()
    azar_estructural = 22.1
    aciertos_4 = stats.get("aciertos_4", 0)
    sorteos_completados = stats.get("sorteos_completados", 0)

    if sorteos_completados > 0:
        porcentaje_real = (aciertos_4 / sorteos_completados) * 100
        ventaja_actual = round(porcentaje_real / azar_estructural, 2) if azar_estructural > 0 else 0
    else:
        porcentaje_real = 0
        ventaja_actual = 0

    # CORRECCIÓN: get_v19_status() puede devolver bool o dict
    v19_status_raw = (
        get_v19_status() if hasattr(evolution, "_state") else {"congelado": False, "razon": ""}
    )
    if isinstance(v19_status_raw, bool):
        v19_status = {"congelado": v19_status_raw, "razon": "V19 congelado por sistema"}
    else:
        v19_status = v19_status_raw

    return {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "forward_test": {
            "sorteos_completados": sorteos_completados,
            "aciertos_4": aciertos_4,
            "aciertos_5": stats.get("aciertos_5", 0),
            "aciertos_6": stats.get("aciertos_6", 0),
            "porcentaje_4_real": round(porcentaje_real, 1),
            "azar_estructural": azar_estructural,
            "ventaja_actual": ventaja_actual,
            "ventaja_formateada": f"×{ventaja_actual}" if ventaja_actual > 0 else "×0",
        },
        "v19": {
            "congelado": v19_status.get("congelado", False),
            "razon": v19_status.get("razon", ""),
            "version": "V19",
        },
        "fase_actual": stats.get("fase_actual", "desconocido"),
    }


@app.post("/api/debate/start")
async def start_debate(
    request: DebateRequest,
    background_tasks: BackgroundTasks,
) -> dict:
    if not supervisor or not supervisor.running:
        raise HTTPException(status_code=503, detail="Supervisor no disponible")

    debate_id = str(uuid.uuid4())
    task = request.task or SAAOP_TASK

    debate_store[debate_id] = {"status": "queued", "result": None}
    background_tasks.add_task(_run_debate, debate_id, task)

    logger.info("Debate %s encolado", debate_id)
    return {"debate_id": debate_id, "status": "queued"}


@app.post("/api/validation/start")
async def start_validation(
    request: DebateRequest,
    background_tasks: BackgroundTasks,
) -> dict:
    if not supervisor or not supervisor.running:
        raise HTTPException(status_code=503, detail="Supervisor no disponible")

    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    sorteo_actual = evolution._state["evolucion_lotoplus"]["ciclo_actual"]["sorteo_actual"]
    fase = evolution.get_fase(sorteo_actual)

    if fase not in ["validacion_ciega", "prediccion_en_vivo"]:
        raise HTTPException(
            status_code=400,
            detail=f"Fase actual: {fase}. Solo se permite validación ciega en fases de test.",
        )

    validation_id = str(uuid.uuid4())
    task = request.task or SAAOP_TASK

    validation_store[validation_id] = {
        "status": "queued",
        "sorteo": sorteo_actual,
        "fase": fase,
        "resultado_revelado": False,
    }

    background_tasks.add_task(_run_validation_debate, validation_id, sorteo_actual, task)

    logger.info(
        "Validación ciega %s iniciada para sorteo %s (fase: %s)", validation_id, sorteo_actual, fase
    )
    return {
        "validation_id": validation_id,
        "sorteo": sorteo_actual,
        "fase": fase,
        "status": "queued",
    }


@app.get("/api/validation/{validation_id}")
async def get_validation(validation_id: str) -> dict:
    data = validation_store.get(validation_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Validación no encontrada")
    return data


@app.post("/api/validation/{validation_id}/reveal")
async def reveal_validation_result(
    validation_id: str,
    result_data: ValidationResultRequest,
) -> dict:
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    validation = validation_store.get(validation_id)
    if validation is None:
        raise HTTPException(status_code=404, detail="Validación no encontrada")

    if validation.get("resultado_revelado"):
        raise HTTPException(status_code=400, detail="Resultado ya fue revelado anteriormente")

    if validation.get("status") != "complete":
        raise HTTPException(
            status_code=400, detail="La validación aún no ha completado la predicción"
        )

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


@app.get("/api/validation/next")
async def get_next_validation_info() -> dict:
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    sorteo_actual = evolution._state["evolucion_lotoplus"]["ciclo_actual"]["sorteo_actual"]
    fase = evolution.get_fase(sorteo_actual)

    if fase == "validacion_ciega":
        total_test = BLIND_TEST_END - BLIND_TEST_START + 1
        completados = evolution.get_estadisticas_ciclo().get("sorteos_completados", 0)
        restantes = total_test - completados
    elif fase == "prediccion_en_vivo":
        total_test = LIVE_TEST_END - LIVE_TEST_START + 1
        completados = evolution.get_estadisticas_ciclo().get("sorteos_completados", 0)
        restantes = total_test - completados
    else:
        completados = 0
        restantes = 0
        total_test = 0

    return {
        "sorteo_actual": sorteo_actual,
        "fase_actual": fase,
        "progreso": {"completados": completados, "restantes": restantes, "total_fase": total_test},
        "ranking_herramientas": evolution.get_ranking_herramientas() if evolution else {},
    }


@app.get("/api/ranking")
async def get_ranking() -> dict:
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")
    return evolution.get_ranking_herramientas()


@app.get("/api/evolucion/stats")
async def get_evolucion_stats() -> dict:
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    return {
        "estadisticas_ciclo": evolution.get_estadisticas_ciclo(),
        "ranking_herramientas": evolution.get_ranking_herramientas(),
        "ultimos_juegos": evolution.get_ultimos_juegos(10),
    }


@app.post("/api/evolucion/reset")
async def reset_ciclo(nuevo_inicio: int | None = None) -> dict:
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    evolution.reset_ciclo(nuevo_inicio)
    logger.info("Ciclo evolutivo reseteado. Nuevo inicio: %s", nuevo_inicio or "default")
    return {"message": "Ciclo resetado exitosamente", "nuevo_inicio": nuevo_inicio or 3800}


@app.get("/api/debate/{debate_id}")
async def get_debate(debate_id: str) -> dict:
    data = debate_store.get(debate_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Debate no encontrado")
    return data


@app.get("/api/debates")
async def list_debates() -> dict:
    return {
        "debates": [{"debate_id": k, "status": v.get("status")} for k, v in debate_store.items()]
    }


# ─── CHAT LIBRE ────────────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not supervisor or not supervisor.running:
        raise HTTPException(status_code=503, detail="Supervisor no disponible")

    agent_ids = request.agent_ids or VALIDATION_AGENTS

    conv_id = request.conversation_id or f"conv_{int(time.time())}"
    if conv_id not in conversation_history:
        conversation_history[conv_id] = []

    conversation_history[conv_id].append(
        {"role": "user", "content": request.message, "timestamp": time.time()}
    )

    history_context = ""
    for msg in conversation_history[conv_id][-10:]:
        role = "Usuario" if msg["role"] == "user" else "Asistente"
        history_context += f"{role}: {msg['content']}\n"

    task = f"""CHAT LIBRE - RESPUESTA GENERAL

HISTORIAL RECIENTE:
{history_context}

INSTRUCCIÓN: Respondé como un asistente versátil. No estás limitado a lotería.
Podés ayudar con programación, explicaciones, ideas, o cualquier consulta general.

CONSULTA ACTUAL: {request.message}

Respondé de forma clara, directa y útil."""

    try:
        result = await supervisor.orchestrate_async(
            task=task, agent_names=agent_ids, mode=ExecutionMode.DEBATE
        )

        if result.debate and result.debate.synthesis:
            response_text = result.debate.synthesis
        elif result.steps:
            best_name = result.scores_summary.get("best_agent", "")
            for step in result.steps:
                if step.agent_name == best_name and step.success:
                    response_text = (
                        step.result.get("output", str(step.result))
                        if isinstance(step.result, dict)
                        else str(step.result)
                    )
                    break
            else:
                response_text = "No se pudo generar respuesta"
        else:
            response_text = "No se pudo generar respuesta"

        conversation_history[conv_id].append(
            {"role": "assistant", "content": response_text, "timestamp": time.time()}
        )

        return {
            "success": True,
            "conversation_id": conv_id,
            "response": response_text,
            "agent_used": result.scores_summary.get("best_agent", "unknown")
            if hasattr(result, "scores_summary")
            else "unknown",
        }

    except Exception as e:
        logger.exception(f"Error en chat: {e}")
        return {"success": False, "error": str(e)}


@app.post("/api/learn")
async def learn_endpoint(request: LearnRequest):
    from core.memoria_perpetua import actualizar_memoria, sincronizar_memoria_vectorial

    try:
        actualizar_memoria(
            agente_id=request.agent_id, nueva_info=request.content, tipo="conocimiento_base"
        )

        sincronizar_memoria_vectorial(request.agent_id, request.content)

        logger.info(f"Aprendizaje guardado para {request.agent_id}")

        return {
            "success": True,
            "message": f"Información aprendida y guardada en memoria de {request.agent_id}",
            "source": request.source,
        }
    except Exception as e:
        logger.exception(f"Error en learn: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    if conversation_id in conversation_history:
        return {
            "success": True,
            "conversation_id": conversation_id,
            "messages": conversation_history[conversation_id],
        }
    return {"success": False, "error": "Conversación no encontrada"}


# ─── CREACIÓN DE AGENTES ────────────────────────────────────────────────────
@app.post("/api/agents/create")
async def create_agent_endpoint(
    id: str = Form(...),
    role: str = Form(...),
    provider: str = Form("nvidia"),
    model: Optional[str] = Form(None),
    system_prompt: str = Form(...),
    temperature: float = Form(0.3),
    memory_file: Optional[UploadFile] = File(None),
):
    """
    Crea un nuevo agente en el sistema.
    - Genera el JSON en agents/config/{id}.json
    - Si hay archivo de memoria, lo indexa en ChromaDB
    - Genera el paper automáticamente
    """
    if not id or not id.strip():
        return {"success": False, "error": "ID del agente es obligatorio"}

    if not system_prompt or not system_prompt.strip():
        return {"success": False, "error": "System Prompt es obligatorio"}

    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", id)
    if safe_id != id:
        logger.warning(f"ID sanitizado: {id} -> {safe_id}")
        id = safe_id

    config_dir = config.AGENTS_CONFIG_DIR
    papers_dir = ROOT / "agents" / "papers"
    config_dir.mkdir(parents=True, exist_ok=True)
    papers_dir.mkdir(parents=True, exist_ok=True)

    final_model = model
    if not final_model:
        if provider == "ollama":
            final_model = "phi3:mini"
        else:
            final_model = "meta/llama-3.1-8b-instruct"

    agent_config = {
        "id": id,
        "role": role,
        "provider": provider,
        "model": final_model,
        "temperature": temperature,
        "system_prompt": system_prompt,
        "instructions": [],
    }

    json_path = config_dir / f"{id}.json"

    if json_path.exists():
        return {"success": False, "error": f"Ya existe un agente con ID '{id}'"}

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Agente JSON creado: {json_path}")
    except Exception as e:
        return {"success": False, "error": f"Error guardando JSON: {e}"}

    memoria_indexada = False
    if memory_file and memory_file.filename:
        try:
            contenido = await memory_file.read()
            contenido_memoria = contenido.decode("utf-8", errors="replace")

            from core.memoria_perpetua import sincronizar_memoria_vectorial

            fragmentos = sincronizar_memoria_vectorial(id, contenido_memoria)
            if fragmentos:
                memoria_indexada = True
                logger.info(f"✅ Memoria vectorial indexada para {id}: {fragmentos} fragmentos")
        except Exception as e:
            logger.warning(f"Error indexando memoria para {id}: {e}")

    paper_generado = False
    try:
        from mejorar_papers import mejorar_paper

        mejorar_paper(id, usar_llm=False)
        paper_generado = True
        logger.info(f"✅ Paper generado automáticamente para {id}")
    except ImportError as e:
        logger.warning(f"No se pudo importar mejorar_papers: {e}")
        paper_basico = {
            "agente_id": id,
            "rol": role,
            "identidad": system_prompt[:500],
            "reglas_clave": [],
            "lecciones_aprendidas": [],
            "errores_a_evitar": [],
            "estilo_respuesta": "Técnico, directo",
            "fecha_creacion": datetime.now().isoformat(),
        }
        paper_path = papers_dir / f"{id}_paper.json"
        with open(paper_path, "w", encoding="utf-8") as f:
            json.dump(paper_basico, f, indent=2, ensure_ascii=False)
        paper_generado = True
        logger.info(f"✅ Paper básico creado para {id}")
    except Exception as e:
        logger.error(f"Error generando paper para {id}: {e}")

    return {
        "success": True,
        "agent_id": id,
        "config_path": str(json_path),
        "memoria_indexada": memoria_indexada,
        "paper_generado": paper_generado,
        "message": f"Agente '{id}' creado exitosamente",
    }


@app.post("/api/settings")
async def save_settings(
    provider: str = Form("nvidia"),
    api_key: Optional[str] = Form(None),
    model: str = Form("meta/llama-3.1-8b-instruct"),
    selected_agents: str = Form(""),
):
    try:
        if selected_agents:
            if selected_agents.startswith("["):
                selected_list = json.loads(selected_agents)
            else:
                selected_list = [a.strip() for a in selected_agents.split(",") if a.strip()]
        else:
            selected_list = VALIDATION_AGENTS

        settings_path = ROOT / "memory" / "user_settings.json"
        settings = {
            "provider": provider,
            "api_key": api_key if api_key else "",
            "model": model,
            "selected_agents": selected_list,
            "updated_at": datetime.now().isoformat(),
        }

        settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

        if api_key:
            config_path = ROOT / "config.py"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = re.sub(
                    r'NVIDIA_API_KEY = "[^"]*"', f'NVIDIA_API_KEY = "{api_key}"', content
                )
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                logger.info("API Key actualizada en config.py")

        logger.info(f"Configuración guardada: provider={provider}, agentes={len(selected_list)}")

        return {
            "success": True,
            "message": "Configuración guardada exitosamente",
            "settings": settings,
        }

    except Exception as e:
        logger.error(f"Error guardando configuración: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/settings")
async def get_settings():
    settings_path = ROOT / "memory" / "user_settings.json"
    if not settings_path.exists():
        return {
            "success": True,
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
            "selected_agents": VALIDATION_AGENTS,
            "api_key_configured": bool(config.NVIDIA_API_KEY),
        }

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        return {"success": True, **settings, "api_key_configured": bool(config.NVIDIA_API_KEY)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/agents/list")
async def list_agents():
    if not supervisor:
        return {"success": False, "error": "Supervisor no disponible"}

    agentes = []
    agentes_ids = set()

    # Fuente 1: Agentes desde JSON (leer directorio directamente)
    config_dir = config.AGENTS_CONFIG_DIR
    if config_dir.exists():
        for json_file in config_dir.glob("*.json"):
            if json_file.name.endswith(".bak"):
                continue
            try:
                with open(json_file, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                agent_id = data.get("id", json_file.stem)
                if agent_id not in agentes_ids:
                    agentes_ids.add(agent_id)
                    agentes.append(
                        {
                            "id": agent_id,
                            "role": data.get("role", "unknown"),
                            "provider": data.get("provider", "nvidia"),
                            "model": data.get("model", "unknown"),
                            "source": "json",
                        }
                    )
            except Exception as e:
                logger.warning(f"Error leyendo {json_file}: {e}")

    # Fuente 2: Agentes desde AgentManager (solo los que no tenemos ya)
    for agent_id in supervisor.agents.list_ids():
        if agent_id not in agentes_ids:
            role = supervisor.agents.get_role(agent_id)
            # Verificar si existe el JSON
            json_path = config_dir / f"{agent_id}.json"
            source = "json" if json_path.exists() else "python"
            provider = "nvidia" if source == "json" else "python_module"
            model = "builtin" if source == "python" else "unknown"

            agentes.append(
                {
                    "id": agent_id,
                    "role": role or "unknown",
                    "provider": provider,
                    "model": model,
                    "source": source,
                }
            )
            agentes_ids.add(agent_id)

    return {"success": True, "agents": agentes, "total": len(agentes)}


# ─── MODIFICAR Y ELIMINAR AGENTES ────────────────────────────────────────────


@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: str, request: Request):
    """Actualiza un agente existente (rol, provider, modelo, system_prompt)."""
    try:
        data = await request.json()
        role = data.get("role")
        provider = data.get("provider")
        model = data.get("model")
        system_prompt = data.get("system_prompt")

        json_path = config.AGENTS_CONFIG_DIR / f"{agent_id}.json"
        if not json_path.exists():
            return {"success": False, "error": f"Agente {agent_id} no encontrado"}

        with open(json_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        if role:
            config_data["role"] = role
        if provider:
            config_data["provider"] = provider
        if model:
            config_data["model"] = model
        if system_prompt:
            config_data["system_prompt"] = system_prompt

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Agente {agent_id} actualizado")
        return {"success": True, "message": f"Agente {agent_id} actualizado"}

    except Exception as e:
        logger.error(f"Error actualizando agente {agent_id}: {e}")
        return {"success": False, "error": str(e)}


@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Elimina un agente (JSON, paper y memorias asociadas)."""
    try:
        if re.sub(r"[^a-zA-Z0-9_-]", "", agent_id) != agent_id:
            return {"success": False, "error": "ID de agente inválido"}

        json_path = config.AGENTS_CONFIG_DIR / f"{agent_id}.json"
        paper_path = ROOT / "agents" / "papers" / f"{agent_id}_paper.json"
        memory_path = ROOT / "memoria_agentes" / agent_id
        vector_path = ROOT / "memoria_vectorial" / agent_id

        if not json_path.exists():
            return {"success": False, "error": f"Agente {agent_id} no encontrado"}

        json_path.unlink()
        logger.info(f"🗑️ Eliminado JSON de {agent_id}")

        if paper_path.exists():
            paper_path.unlink()
            logger.info(f"🗑️ Eliminado paper de {agent_id}")

        _delete_agent_directory(memory_path, agent_id, "memoria JSON")

        _release_agent_vector_memory(agent_id)
        _delete_agent_directory(vector_path, agent_id, "memoria vectorial")

        return {"success": True, "message": f"Agente {agent_id} eliminado"}

    except Exception as e:
        logger.error(f"Error eliminando agente {agent_id}: {e}")
        return {"success": False, "error": str(e)}


# ─── Servir frontend ────────────────────────────────────────────────────────
WEB_DIR = ROOT / "ui" / "web"

if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="static")
else:

    @app.get("/")
    async def root() -> dict:
        return {"message": "S.A.A.O.P. API activa. Coloca index.html en ui/web/"}


# ─── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
