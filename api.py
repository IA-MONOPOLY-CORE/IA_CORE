"""
IA_CORE — Servidor FastAPI.

Expone el sistema multiagente como API REST.
Ejecutar: uvicorn api:app --host 0.0.0.0 --port 8000 --reload
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import shutil
import sys
import uuid
import time
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File, Form, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
from core.catalog_registry import (
    get_domain_creation_catalog,
    get_roles_catalog,
    get_specializations_catalog,
)
from core.domain_registry import (
    create_domain,
    find_agent_json,
    get_domain_agent_paths,
    get_domain_agent_preset,
    get_domain_agent_presets,
    get_domain_profile_catalog,
    get_theme_presets,
    iter_agent_config_dirs,
    list_domains,
    load_domain,
    resolve_agent_json,
)
from core.supervisor import MEMORY_HISTORY_KEY, Supervisor
from core.orchestration import ExecutionMode
from core.model_recommendation import recommend_provider_model


# ========================================================================
# Lazy imports for loteria-specific code (to keep API generic)
# ========================================================================
_loteria_cache = None


def _get_loteria():
    global _loteria_cache
    if _loteria_cache is not None:
        return _loteria_cache

    try:
        from domains.loteria.config_loteria import (
            VALIDATION_AGENTS,
            DEFAULT_VALIDATION_TASK,
            TRAINING_END,
            BLIND_TEST_START,
            BLIND_TEST_END,
            LIVE_TEST_START,
            LIVE_TEST_END,
        )
        from domains.loteria.evolution_loteria import EvolutionManagerLoteria
        from domains.loteria.database_loteria import (
            init_db as loteria_init_db,
            get_v19_status as loteria_get_v19_status,
            get_sorteo_by_numero as loteria_get_sorteo_by_numero,
        )
        from domains.loteria.validation_loteria import (
            run_validation_debate,
            reveal_validation_result,
        )

        _loteria_cache = {
            "VALIDATION_AGENTS": VALIDATION_AGENTS,
            "DEFAULT_VALIDATION_TASK": DEFAULT_VALIDATION_TASK,
            "TRAINING_END": TRAINING_END,
            "BLIND_TEST_START": BLIND_TEST_START,
            "BLIND_TEST_END": BLIND_TEST_END,
            "LIVE_TEST_START": LIVE_TEST_START,
            "LIVE_TEST_END": LIVE_TEST_END,
            "EvolutionManagerLoteria": EvolutionManagerLoteria,
            "init_db": loteria_init_db,
            "get_v19_status": loteria_get_v19_status,
            "get_sorteo_by_numero": loteria_get_sorteo_by_numero,
            "run_validation_debate": run_validation_debate,
            "reveal_validation_result": reveal_validation_result,
        }
        return _loteria_cache
    except ImportError:
        _loteria_cache = None
        return None


def _require_loteria():
    loteria = _get_loteria()
    if not loteria:
        raise HTTPException(
            status_code=501, detail="Funcionalidad no disponible (dominio lotería no instalado)"
        )
    return loteria


# ========================================================================
# Logging
# ========================================================================
config.LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format=config.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(config.LOG_DIR / "api.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


# ========================================================================
# Helper functions
# ========================================================================
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


# ========================================================================
# App setup
# ========================================================================
app = FastAPI(title="IA_CORE API", version="2.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================================================
# Global state
# ========================================================================
supervisor: Supervisor | None = None
evolution: Any = None  # Will be EvolutionManagerLoteria if loteria is available
debate_store: dict[str, dict[str, Any]] = {}
validation_store: dict[str, dict[str, Any]] = {}
conversation_history: dict[str, list[dict]] = {}
session_events: list[dict[str, Any]] = []
runtime_metrics: dict[str, float | int] = {
    "started_at": time.time(),
    "orchestrations": 0,
    "agent_dispatches": 0,
    "last_orchestration_ms": 0.0,
}


# ========================================================================
# Lifecycle
# ========================================================================
@app.on_event("startup")
async def startup() -> None:
    global supervisor, evolution
    supervisor = Supervisor(log_dir=config.LOG_DIR)

    loteria = _get_loteria()
    if loteria:
        evolution = loteria["EvolutionManagerLoteria"]()
        loteria["init_db"]()

    await asyncio.to_thread(supervisor.start)
    runtime_metrics.update(
        {
            "started_at": time.time(),
            "orchestrations": 0,
            "agent_dispatches": 0,
            "last_orchestration_ms": 0.0,
        }
    )
    session_events.clear()
    _record_event("system", "API y Supervisor iniciados")
    logger.info("IA_CORE API lista")


@app.on_event("shutdown")
async def shutdown() -> None:
    if supervisor:
        await asyncio.to_thread(supervisor.shutdown)
    _record_event("system", "API y Supervisor detenidos")
    logger.info("IA_CORE API detenida")


# ========================================================================
# Helper functions (generic, not loteria-specific)
# ========================================================================
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


def _record_event(kind: str, message: str) -> None:
    session_events.append(
        {
            "kind": kind,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
    )
    if len(session_events) > 200:
        del session_events[:-100]


def _track_orchestration(result: Any) -> None:
    steps = getattr(result, "steps", None) or []
    runtime_metrics["orchestrations"] = int(runtime_metrics["orchestrations"]) + 1
    runtime_metrics["agent_dispatches"] = int(runtime_metrics["agent_dispatches"]) + len(steps)
    runtime_metrics["last_orchestration_ms"] = round(
        float(getattr(result, "duration_ms", 0) or 0), 1
    )


def _memory_summary() -> dict[str, Any]:
    if not supervisor:
        return {
            "running": False,
            "path": str(config.MEMORY_STATE_FILE),
            "key_count": 0,
            "history_count": 0,
            "keys_preview": [],
        }

    memory = supervisor.memory
    keys = memory.list_keys()
    history = memory.get(MEMORY_HISTORY_KEY, [])
    if not isinstance(history, list):
        history = []
    return {
        "running": memory.running,
        "path": str(memory.state_path),
        "key_count": len(keys),
        "history_count": len(history),
        "keys_preview": keys[:12],
    }


def _history_summary(limit: int = 15) -> list[dict[str, Any]]:
    if not supervisor:
        return []
    history = supervisor.memory.get(MEMORY_HISTORY_KEY, [])
    if not isinstance(history, list):
        return []

    rows = []
    for entry in reversed(history[-limit:]):
        if not isinstance(entry, dict):
            continue
        rows.append(
            {
                "execution_id": entry.get("execution_id"),
                "mode": entry.get("mode"),
                "agents": entry.get("agents", []),
                "success": entry.get("success", False),
                "started_at": entry.get("started_at"),
                "duration_ms": entry.get("duration_ms", 0),
            }
        )
    return rows


def _tail_log(path: Path, lines: int) -> list[str]:
    if not path.exists():
        return []
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]
    except OSError:
        return []


def _provider_status(provider: Any) -> dict[str, Any]:
    """Aísla fallos de diagnóstico para no perder el catálogo completo."""
    try:
        name = provider.provider_name()
    except Exception as exc:
        name = type(provider).__name__
        logger.warning("No se pudo obtener el nombre del provider %s: %s", name, exc)

    is_placeholder = getattr(provider, "IS_PLACEHOLDER", False)
    healthy = False
    message = "Diagnóstico no disponible"
    models: list[str] = []

    try:
        health = provider.health_check()
        healthy = bool(health.healthy)
        message = health.message
    except Exception as exc:
        message = f"Health check falló: {exc}"
        logger.warning("Health check falló para %s: %s", name, exc)

    try:
        models = provider.available_models()
    except Exception as exc:
        logger.warning("No se pudieron listar modelos de %s: %s", name, exc)
        if message == "Diagnóstico no disponible":
            message = f"Listado de modelos falló: {exc}"

    return {
        "name": name,
        "is_placeholder": is_placeholder,
        "healthy": healthy,
        "message": message,
        "models": models,
    }


async def _run_debate(
    debate_id: str,
    task: str,
    mode: ExecutionMode = ExecutionMode.DEBATE,
    agent_names: list[str] | None = None,
) -> None:
    debate_store[debate_id]["status"] = "running"
    _record_event("orchestration", f"Ejecución {debate_id} iniciada en modo {mode.value}")
    try:
        result = await supervisor.orchestrate_async(
            task,
            agent_names=agent_names,
            mode=mode,
        )
        _track_orchestration(result)
        debate_store[debate_id] = {
            "status": "complete",
            "result": _serialize_result(result),
        }
        _record_event("orchestration", f"Ejecución {debate_id} completada")
        logger.info("Ejecución %s completada en modo %s", debate_id, mode.value)
    except Exception as e:
        debate_store[debate_id] = {
            "status": "error",
            "error": str(e),
        }
        _record_event("error", f"Ejecución {debate_id}: {e}")
        logger.exception("Error en ejecución %s: %s", debate_id, e)


# ========================================================================
# Pydantic models
# ========================================================================
class DebateRequest(BaseModel):
    task: str | None = None
    mode: str = "debate"
    agents: Optional[List[str]] = None


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


class DomainCreateRequest(BaseModel):
    nombre: str
    descripcion: str
    instrucciones: str
    tema_id: str
    nicho_sugerido: str | None = None
    area_profesional_id: str | None = None
    nicho_id: str | None = None


class CreateAgentRequest(BaseModel):
    id: str
    role: str
    provider: str = "nvidia"
    model: Optional[str] = None
    system_prompt: str
    temperature: float = 0.3


# ========================================================================
# Endpoints
# ========================================================================
@app.get("/api/status")
async def get_status(full: bool = False) -> dict:
    fase_actual = "desconocida"
    sorteo_actual = 3800
    limites_sistema = {
        "training_end": 3799,
        "blind_test_start": 3800,
        "blind_test_end": 3850,
        "live_test_start": 3851,
        "live_test_end": 3885,
    }

    loteria = _get_loteria()
    if loteria and evolution:
        stats = evolution.get_estadisticas_ciclo()
        fase_actual = stats.get("fase_actual", "desconocida")
        if hasattr(evolution, "_state"):
            sorteo_actual = evolution._state["evolucion_lotoplus"]["ciclo_actual"]["sorteo_actual"]
        limites_sistema = {
            "training_end": loteria["TRAINING_END"],
            "blind_test_start": loteria["BLIND_TEST_START"],
            "blind_test_end": loteria["BLIND_TEST_END"],
            "live_test_start": loteria["LIVE_TEST_START"],
            "live_test_end": loteria["LIVE_TEST_END"],
        }

    providers_info: list[dict[str, Any]] = []
    if supervisor:
        providers = supervisor.providers.list_providers()
        providers_info = list(
            await asyncio.gather(
                *(asyncio.to_thread(_provider_status, provider) for provider in providers)
            )
        )

    hybrid_status: dict[str, Any] | None = None
    if supervisor and supervisor.hybrid_router:
        hybrid_status = await asyncio.to_thread(
            supervisor.hybrid_router.get_ui_snapshot,
            full=full,
        )
    elif config.HYBRID_MODE:
        hybrid_status = {
            "hybrid_enabled": True,
            "execution_mode": "pending",
            "safe_mode": config.SAFE_MODE,
        }

    memory = _memory_summary()
    return {
        "running": supervisor is not None and supervisor.running,
        "providers_ready": bool(supervisor and supervisor.running and providers_info),
        "providers": providers_info,
        "agents": supervisor.agents.list_ids() if supervisor else [],
        "fase_actual": fase_actual,
        "sorteo_actual": sorteo_actual,
        "limites_sistema": limites_sistema,
        "hybrid": hybrid_status,
        "overview": {
            "uptime_s": round(time.time() - float(runtime_metrics["started_at"]), 1),
            "agent_count": len(supervisor.agents.list_ids()) if supervisor else 0,
            "provider_count": len(providers_info),
            "tool_count": len(supervisor.tools.list_names()) if supervisor else 0,
            "tools": supervisor.tools.list_names() if supervisor else [],
            "orchestrations": int(runtime_metrics["orchestrations"]),
            "agent_dispatches": int(runtime_metrics["agent_dispatches"]),
            "last_orchestration_ms": float(runtime_metrics["last_orchestration_ms"]),
            "memory": memory,
        },
    }


@app.get("/api/memory")
async def get_memory_snapshot(
    key: str | None = None,
    history_limit: int = 15,
) -> dict:
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor no disponible")

    history_limit = max(1, min(history_limit, 100))
    keys = supervisor.memory.list_keys()
    history = _history_summary(history_limit)
    latest = None
    if history:
        execution_id = history[0].get("execution_id")
        if execution_id:
            latest = {
                "summary": history[0],
                "detail": supervisor.get_orchestration(execution_id),
            }

    payload: dict[str, Any] = {
        "status": _memory_summary(),
        "keys": keys,
        "history": history,
        "latest": latest,
    }
    if key is not None:
        if key not in keys:
            raise HTTPException(status_code=404, detail=f"Clave de memoria no encontrada: {key}")
        payload["selected_key"] = key
        payload["value"] = supervisor.memory.get(key)
    return payload


@app.get("/api/logs")
async def get_logs(lines: int = 80) -> dict:
    lines = max(20, min(lines, 500))
    log_path = config.LOG_DIR / "api.log"
    content = _tail_log(log_path, lines)
    warnings = [line for line in content if "WARNING" in line]
    errors = [line for line in content if "ERROR" in line]
    return {
        "path": str(log_path),
        "requested_lines": lines,
        "lines": content,
        "warnings": warnings[-50:],
        "errors": errors[-50:],
        "events": session_events[-50:],
    }


@app.get("/api/metrics/dynamic")
async def get_dynamic_metrics() -> dict:
    loteria = _require_loteria()
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
        loteria["get_v19_status"]() if hasattr(evolution, "_state") else {"congelado": False, "razon": ""}
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

    try:
        mode = ExecutionMode(request.mode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Modo no soportado: {request.mode}") from exc

    debate_id = str(uuid.uuid4())

    loteria = _get_loteria()
    task = request.task or (loteria["DEFAULT_VALIDATION_TASK"] if loteria else "Debate genérico")

    debate_store[debate_id] = {
        "status": "queued",
        "result": None,
        "mode": mode.value,
        "agents": request.agents or [],
    }
    background_tasks.add_task(_run_debate, debate_id, task, mode, request.agents)

    _record_event("orchestration", f"Ejecución {debate_id} encolada en modo {mode.value}")
    logger.info("Ejecución %s encolada en modo %s", debate_id, mode.value)
    return {"debate_id": debate_id, "status": "queued", "mode": mode.value}


@app.post("/api/validation/start")
async def start_validation(
    request: DebateRequest,
    background_tasks: BackgroundTasks,
) -> dict:
    loteria = _require_loteria()

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
    task = request.task or loteria["DEFAULT_VALIDATION_TASK"]

    validation_store[validation_id] = {
        "status": "queued",
        "sorteo": sorteo_actual,
        "fase": fase,
        "resultado_revelado": False,
    }

    background_tasks.add_task(
        loteria["run_validation_debate"],
        validation_id,
        sorteo_actual,
        task,
        supervisor,
        evolution,
        validation_store,
        _record_event,
        _track_orchestration,
        _serialize_result,
    )

    logger.info(
        "Validación ciega %s iniciada para sorteo %s (fase: %s)", validation_id, sorteo_actual, fase
    )
    return {
        "validation_id": validation_id,
        "sorteo": sorteo_actual,
        "fase": fase,
        "status": "queued",
    }


@app.get("/api/validation/next")
async def get_next_validation_info() -> dict:
    loteria = _require_loteria()

    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    sorteo_actual = evolution._state["evolucion_lotoplus"]["ciclo_actual"]["sorteo_actual"]
    fase = evolution.get_fase(sorteo_actual)
    sorteo_info = loteria["get_sorteo_by_numero"](sorteo_actual)
    fecha_sorteo = sorteo_info.get("fecha") if sorteo_info else None

    if fase == "validacion_ciega":
        total_test = loteria["BLIND_TEST_END"] - loteria["BLIND_TEST_START"] + 1
        completados = evolution.get_estadisticas_ciclo().get("sorteos_completados", 0)
        restantes = total_test - completados
    elif fase == "prediccion_en_vivo":
        total_test = loteria["LIVE_TEST_END"] - loteria["LIVE_TEST_START"] + 1
        completados = evolution.get_estadisticas_ciclo().get("sorteos_completados", 0)
        restantes = total_test - completados
    else:
        completados = 0
        restantes = 0
        total_test = 0

    return {
        "sorteo_actual": sorteo_actual,
        "fecha": fecha_sorteo,
        "fase_actual": fase,
        "progreso": {"completados": completados, "restantes": restantes, "total_fase": total_test},
        "ranking_herramientas": evolution.get_ranking_herramientas() if evolution else {},
    }


@app.get("/api/validation/{validation_id}")
async def get_validation(validation_id: str) -> dict:
    data = validation_store.get(validation_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Validación no encontrada")
    return data


@app.post("/api/validation/{validation_id}/reveal")
async def reveal_validation(
    validation_id: str,
    result_data: ValidationResultRequest,
) -> dict:
    loteria = _require_loteria()

    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    try:
        return loteria["reveal_validation_result"](validation_id, result_data, evolution, validation_store)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/ranking")
async def get_ranking() -> dict:
    _require_loteria()
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")
    return evolution.get_ranking_herramientas()


@app.get("/api/evolucion/stats")
async def get_evolucion_stats() -> dict:
    _require_loteria()
    if not evolution:
        raise HTTPException(status_code=503, detail="EvolutionManager no disponible")

    return {
        "estadisticas_ciclo": evolution.get_estadisticas_ciclo(),
        "ranking_herramientas": evolution.get_ranking_herramientas(),
        "ultimos_juegos": evolution.get_ultimos_juegos(10),
    }


@app.post("/api/evolucion/reset")
async def reset_ciclo(nuevo_inicio: int | None = None) -> dict:
    _require_loteria()
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


# ========================================================================
# Chat libre (genérico)
# ========================================================================
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not supervisor or not supervisor.running:
        raise HTTPException(status_code=503, detail="Supervisor no disponible")

    loteria = _get_loteria()
    agent_ids = request.agent_ids or (loteria["VALIDATION_AGENTS"] if loteria else [])

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
        _track_orchestration(result)
        _record_event("orchestration", f"Chat {conv_id} completado")

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
        _record_event("error", f"Chat {conv_id}: {e}")
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


# ========================================================================
# Dominios (genéricos)
# ========================================================================
@app.get("/api/catalogs/domain-creation")
async def get_domain_creation_catalog_endpoint() -> dict:
    """Devuelve catálogos compartidos para asistir la creación de dominios."""
    try:
        return {"success": True, **get_domain_creation_catalog()}
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/catalogs/roles")
async def get_roles_catalog_endpoint() -> dict:
    """Devuelve roles/arquetipos profesionales globales."""
    try:
        return {"success": True, **get_roles_catalog()}
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/catalogs/specializations")
async def get_specializations_catalog_endpoint(role_id: str | None = None) -> dict:
    """Devuelve especializaciones profesionales globales agrupadas por rol."""
    try:
        return {"success": True, **get_specializations_catalog(role_id=role_id)}
    except ValueError as exc:
        message = str(exc)
        status_code = 400 if "Rol inexistente" in message or "role_id" in message else 500
        raise HTTPException(status_code=status_code, detail=message) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/domains/list")
async def get_domains() -> dict:
    domains = list_domains()
    return {
        "success": True,
        "domains": domains,
        "themes": get_theme_presets(),
        "total": len(domains),
    }


@app.get("/api/domains/{domain_id}/profile-catalog")
async def get_domain_profile_catalog_endpoint(domain_id: str) -> dict:
    """Devuelve el catálogo read-only de perfiles habilitados para un dominio."""
    try:
        return {"success": True, **get_domain_profile_catalog(domain_id)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        message = str(exc)
        status_code = 400 if "inválid" in message.lower() else 500
        raise HTTPException(status_code=status_code, detail=message) from exc


@app.get("/api/domains/{domain_id}/agent-presets")
async def get_domain_agent_presets_endpoint(domain_id: str) -> dict:
    """Devuelve presets read-only de agentes para un dominio."""
    try:
        return {"success": True, **get_domain_agent_presets(domain_id)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        message = str(exc)
        lowered = message.lower()
        if "dominio no encontrado" in lowered:
            status_code = 404
        elif "inv" in lowered or "inexistente" in lowered or "no existe" in lowered:
            status_code = 400
        else:
            status_code = 500
        raise HTTPException(status_code=status_code, detail=message) from exc


@app.get("/api/domains/{domain_id}/agent-presets/match")
async def get_domain_agent_preset_match_endpoint(
    domain_id: str,
    role_id: str,
    specialization_id: str,
) -> dict:
    """Devuelve un preset exacto por role_id + specialization_id."""
    try:
        preset = get_domain_agent_preset(
            domain_id,
            role_id=role_id,
            specialization_id=specialization_id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        message = str(exc)
        lowered = message.lower()
        if "dominio no encontrado" in lowered:
            status_code = 404
        elif "inv" in lowered or "inexistente" in lowered or "no existe" in lowered:
            status_code = 400
        else:
            status_code = 500
        raise HTTPException(status_code=status_code, detail=message) from exc

    if preset is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No existe preset activo para role_id={role_id} "
                f"y specialization_id={specialization_id} en dominio {domain_id}"
            ),
        )
    return {"success": True, "domain_id": domain_id, "preset": preset}


@app.post("/api/domains/create")
async def create_domain_endpoint(request: DomainCreateRequest) -> dict:
    try:
        domain = create_domain(
            name=request.nombre,
            description=request.descripcion,
            instructions=request.instrucciones,
            theme_id=request.tema_id,
            suggested_niche=request.nicho_sugerido,
            area_profesional_id=request.area_profesional_id,
            nicho_id=request.nicho_id,
        )
        logger.info("Dominio creado: %s", domain["id"])
        return {"success": True, "domain": domain}
    except FileExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# ========================================================================
# Agentes (genéricos)
# ========================================================================
def _validate_agent_profile_selection(
    *,
    domain_id: str,
    role: str | None,
    specialization_id: str | None = None,
) -> dict[str, Any]:
    """Valida rol/especialización contra profile_catalog si el dominio lo declara."""
    try:
        profile_catalog = get_domain_profile_catalog(domain_id)
    except FileNotFoundError:
        # Fallback temporal para dominios que todavía no tienen profile_catalog.json.
        return {"success": True, "profile_catalog": None}
    except ValueError as exc:
        return {"success": False, "error": str(exc)}

    roles = profile_catalog.get("roles", [])
    role_entry = next((item for item in roles if item.get("role_id") == role), None)
    if role_entry is None:
        return {
            "success": False,
            "error": f"Rol '{role}' no está habilitado para el dominio '{domain_id}'",
        }

    normalized_specialization_id = (
        specialization_id.strip() if isinstance(specialization_id, str) else None
    )
    if not normalized_specialization_id:
        return {"success": True, "profile_catalog": profile_catalog}

    specialization_entry = next(
        (
            item
            for item in role_entry.get("specializations", [])
            if item.get("specialization_id") == normalized_specialization_id
        ),
        None,
    )
    if specialization_entry is None:
        return {
            "success": False,
            "error": (
                f"Especialización '{normalized_specialization_id}' no está habilitada "
                f"para el rol '{role}' en el dominio '{domain_id}'"
            ),
        }

    return {
        "success": True,
        "profile_catalog": profile_catalog,
        "specialization_name": specialization_entry.get("nombre_visible"),
    }


@app.post("/api/agents/create")
async def create_agent_endpoint(
    id: str = Form(...),
    role: str = Form(...),
    specialization_id: Optional[str] = Form(None),
    profile_preset_id: Optional[str] = Form(None),
    provider: str = Form("nvidia"),
    model: Optional[str] = Form(None),
    system_prompt: str = Form(...),
    temperature: float = Form(0.3),
    memory_file: Optional[UploadFile] = File(None),
    domain_id: str = Form(...),
):
    """
    Crea un nuevo agente en el sistema.
    - Genera el JSON en domains/{domain_id}/agents/config/{id}.json
    - Si hay archivo de memoria, lo indexa en ChromaDB
    - Genera el paper automáticamente
    """
    if not id or not id.strip():
        return {"success": False, "error": "ID del agente es obligatorio"}

    if not system_prompt or not system_prompt.strip():
        return {"success": False, "error": "System Prompt es obligatorio"}

    if not isinstance(specialization_id, str) or not specialization_id.strip():
        specialization_id = None
    if not isinstance(profile_preset_id, str) or not profile_preset_id.strip():
        profile_preset_id = None

    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", id)
    if safe_id != id:
        logger.warning(f"ID sanitizado: {id} -> {safe_id}")
        id = safe_id

    domain = load_domain(domain_id)
    if domain is None:
        return {"success": False, "error": f"Dominio '{domain_id}' no encontrado"}

    profile_validation = _validate_agent_profile_selection(
        domain_id=domain_id,
        role=role,
        specialization_id=specialization_id,
    )
    if profile_validation.get("success") is False:
        return profile_validation

    profile_preset = None
    if profile_preset_id:
        if not specialization_id:
            return {
                "success": False,
                "error": "profile_preset_id requiere specialization_id",
            }
        try:
            presets_catalog = get_domain_agent_presets(domain_id)
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"El dominio '{domain_id}' no tiene presets de agentes",
            }
        except ValueError as exc:
            return {"success": False, "error": str(exc)}
        profile_preset = next(
            (
                preset
                for preset in presets_catalog.get("presets", [])
                if preset.get("id") == profile_preset_id
            ),
            None,
        )
        if profile_preset is None:
            return {
                "success": False,
                "error": f"profile_preset_id '{profile_preset_id}' no existe en el dominio '{domain_id}'",
            }
        if (
            profile_preset.get("role_id") != role
            or profile_preset.get("specialization_id") != specialization_id
        ):
            return {
                "success": False,
                "error": (
                    f"profile_preset_id '{profile_preset_id}' no corresponde a "
                    f"role='{role}' y specialization_id='{specialization_id}'"
                ),
            }

    config_dir, papers_dir = get_domain_agent_paths(domain_id, ensure=True)

    final_model = model
    if not final_model:
        if provider == "ollama":
            final_model = "phi3:mini"
        else:
            final_model = "meta/llama-3.1-8b-instruct"

    from core.agent_config_schema import build_agent_config
    from core.agent_paper_schema import build_initial_paper_from_preset, write_initial_agent_paper

    # Preparar variables para paper
    paper_created = False
    paper_source = None
    paper_path = None
    agent_config = None
    memory_source = None
    paper_enriched = False
    paper_enrichment_applied_at = None
    paper_enrichment_reason = None

    # Read memory file content early if available
    contenido_memoria = None
    if memory_file and memory_file.filename:
        try:
            contenido = await memory_file.read()
            contenido_memoria = contenido.decode("utf-8", errors="replace")
            memory_source = {
                "content": contenido_memoria,
                "filename": memory_file.filename,
            }
        except Exception as e:
            return {"success": False, "error": f"Error leyendo archivo de memoria: {e}"}

    # Primero verificar si paper ya existe para evitar basura
    if profile_preset:
        _, papers_dir_check = get_domain_agent_paths(domain_id, ensure=False)
        paper_path_check = papers_dir_check / f"{id}_paper.json"
        if paper_path_check.exists():
            return {"success": False, "error": f"Ya existe un paper para el agente con ID '{id}'"}

    # Crear config de agente con paper info inicial
    agent_config = build_agent_config(
        id=id,
        role=role,
        domain_id=domain_id,
        domain_instructions=domain.get("instrucciones", ""),
        provider=provider,
        model=final_model,
        temperature=temperature,
        system_prompt=system_prompt,
        instructions=[],
        specialization_id=specialization_id,
        specialization_name=profile_validation.get("specialization_name") if specialization_id else None,
        profile_preset_id=profile_preset["id"] if profile_preset else None,
        profile_preset_name=profile_preset.get("nombre_visible") if profile_preset else None,
        preset_applied_at=datetime.now().isoformat() if profile_preset else None,
        memory_uploaded=bool(memory_file and memory_file.filename),
        memory_filename=memory_file.filename if memory_file and memory_file.filename else None,
        memory_indexed=False,  # Se actualizará después de indexar
        paper_enriched=False,  # Will update if we enrich
        paper_enrichment_applied_at=None,
        paper_enrichment_reason=None,
        created_via="hud_create_agent",
        preset_source="domain_agent_presets" if profile_preset else None,
        paper_created=False,  # Se actualizará después de crear paper
        paper_source=None,
    )

    json_path = config_dir / f"{id}.json"

    if find_agent_json(id) is not None:
        return {"success": False, "error": f"Ya existe un agente con ID '{id}'"}

    # Generar paper primero si hay preset, para evitar basura si falla
    if profile_preset:
        try:
            domain_metadata = {
                "nombre": domain.get("nombre"),
                "descripcion": domain.get("descripcion"),
                "instrucciones": domain.get("instrucciones"),
            }
            paper = build_initial_paper_from_preset(
                agent_config=agent_config,
                profile_preset=profile_preset,
                domain_metadata=domain_metadata,
                memory_source=memory_source,
            )
            paper_path = write_initial_agent_paper(domain_id, id, paper, overwrite=False)
            paper_created = True
            paper_source = "preset_initial_paper"
            logger.info(f"✅ Paper inicial generado para {id} desde preset")
            # Check if paper was enriched with memory
            if paper.get("memory_enrichment", {}).get("applied"):
                paper_enriched = True
                paper_enrichment_applied_at = paper["memory_enrichment"]["applied_at"]
        except Exception as e:
            return {"success": False, "error": f"Error generando paper desde preset: {e}"}
    else:
        if memory_file and memory_file.filename:
            paper_enrichment_reason = "no_profile_preset"

    # Ahora guardar JSON del agente (con paper info actualizada si aplica)
    if paper_created:
        agent_config["paper"]["created"] = True
        agent_config["paper"]["source"] = paper_source
    # Update memory block with enrichment info
    agent_config["memory"]["paper_enriched"] = paper_enriched
    agent_config["memory"]["paper_enrichment_applied_at"] = paper_enrichment_applied_at
    agent_config["memory"]["paper_enrichment_reason"] = paper_enrichment_reason

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Agente JSON creado: {json_path}")
    except Exception as e:
        # Si falla guardar JSON y ya habíamos guardado paper, intentar eliminar paper
        if paper_created and paper_path:
            try:
                paper_path.unlink(missing_ok=True)
                logger.warning(f"⚠️ Eliminado paper por fallo en guardar JSON del agente {id}")
            except Exception:
                pass
        return {"success": False, "error": f"Error guardando JSON: {e}"}

    memoria_indexada = False
    if memory_file and memory_file.filename and contenido_memoria:
        try:
            from core.memoria_perpetua import sincronizar_memoria_vectorial

            fragmentos = sincronizar_memoria_vectorial(id, contenido_memoria)
            if fragmentos:
                memoria_indexada = True
                logger.info(f"✅ Memoria vectorial indexada para {id}: {fragmentos} fragmentos")

                # Actualizar el JSON del agente para reflejar que la memoria fue indexada
                agent_config["memory"]["indexed"] = True
                agent_config["metadata"]["updated_at"] = datetime.now().isoformat()
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(agent_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Error indexando memoria para {id}: {e}")

    # Si no hay preset, generar paper básico para compatibilidad hacia atrás
    if not profile_preset:
        paper_basico = {
            "agente_id": id,
            "dominio_id": domain_id,
            "rol": role,
            "identidad": system_prompt[:500],
            "instrucciones_dominio": domain.get("instrucciones", ""),
            "reglas_clave": [],
            "lecciones_aprendidas": [],
            "errores_a_evitar": [],
            "estilo_respuesta": "Técnico, directo",
            "fecha_creacion": datetime.now().isoformat(),
        }
        paper_path = papers_dir / f"{id}_paper.json"
        with open(paper_path, "w", encoding="utf-8") as f:
            json.dump(paper_basico, f, indent=2, ensure_ascii=False)
        paper_created = True
        paper_source = "basic_compatibility"
        # Actualizar la config del agente para reflejar que se creó el paper
        agent_config["paper"]["created"] = True
        agent_config["paper"]["source"] = paper_source
        agent_config["metadata"]["updated_at"] = datetime.now().isoformat()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Paper básico creado para {id} en dominio {domain_id}")

    return {
        "success": True,
        "agent_id": id,
        "config_path": str(json_path),
        "memoria_indexada": memoria_indexada,
        "paper_generado": paper_created,
        "message": f"Agente '{id}' creado exitosamente",
    }


@app.post("/api/settings")
async def save_settings(
    provider: str = Form("nvidia"),
    api_key: Optional[str] = Form(None),
    model: str = Form("meta/llama-3.1-8b-instruct"),
    selected_agents: str = Form(""),
):
    loteria = _get_loteria()

    try:
        if selected_agents:
            if selected_agents.startswith("["):
                selected_list = json.loads(selected_agents)
            else:
                selected_list = [a.strip() for a in selected_agents.split(",") if a.strip()]
        else:
            selected_list = loteria["VALIDATION_AGENTS"] if loteria else []

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
    loteria = _get_loteria()
    settings_path = ROOT / "memory" / "user_settings.json"
    if not settings_path.exists():
        return {
            "success": True,
            "provider": "nvidia",
            "model": "meta/llama-3.1-8b-instruct",
            "selected_agents": loteria["VALIDATION_AGENTS"] if loteria else [],
            "api_key_configured": bool(config.NVIDIA_API_KEY),
        }

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        return {"success": True, **settings, "api_key_configured": bool(config.NVIDIA_API_KEY)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/agents/model-recommendation")
async def get_model_recommendation(
    domain_id: str = Form(...),
    role_id: str = Form(...),
    specialization_id: Optional[str] = Form(None),
    profile_preset_id: Optional[str] = Form(None),
    current_provider: Optional[str] = Form(None),
    current_model: Optional[str] = Form(None),
):
    """
    Obtiene una recomendación de provider/model para un perfil de agente.
    
    La recomendación se basa en:
    - Dominio, rol y especialización
    - Carga cognitiva esperada
    - Hardware local disponible
    - Providers realmente disponibles
    
    Es una sugerencia editable, NO una imposición.
    """
    try:
        # Obtener providers disponibles desde supervisor
        available_providers = []
        if supervisor:
            providers = supervisor.providers.list_providers()
            for provider in providers:
                try:
                    name = provider.provider_name()
                    models = provider.available_models()
                    health = provider.health_check()
                    is_placeholder = getattr(provider, "IS_PLACEHOLDER", False)
                    
                    available_providers.append({
                        "name": name,
                        "models": models,
                        "healthy": health.healthy,
                        "is_placeholder": is_placeholder,
                        "message": health.message,
                    })
                except Exception as e:
                    logger.warning(f"Error obteniendo info de provider: {e}")
        
        # Generar recomendación
        recommendation = recommend_provider_model(
            domain_id=domain_id,
            role_id=role_id,
            specialization_id=specialization_id,
            profile_preset_id=profile_preset_id,
            current_provider=current_provider,
            current_model=current_model,
            available_providers=available_providers,
        )
        
        return {
            "success": True,
            "recommendation": {
                "recommended": recommendation.recommended,
                "provider": recommendation.provider,
                "model": recommendation.model,
                "workload": recommendation.workload,
                "recommended_execution": recommendation.recommended_execution,
                "reasoning_need": recommendation.reasoning_need,
                "reason": recommendation.reason,
                "fallback": recommendation.fallback,
                "compatibility": recommendation.compatibility,
                "hardware_reason": recommendation.hardware_reason,
            },
            "available_providers": available_providers,
        }
    except Exception as e:
        logger.exception("Error generando recomendación de modelo")
        return {
            "success": False,
            "error": str(e),
        }


@app.get("/api/system/hardware-profile")
async def get_hardware_profile():
    from core.model_recommendation import get_hardware_profile

    try:
        profile = get_hardware_profile()
        return {
            "success": True,
            "profile": {
                "cpu": profile.cpu,
                "ram_gb": profile.ram_gb,
                "gpu": profile.gpu,
                "gpu_name": profile.gpu_name,
                "local_mode": profile.local_mode,
                "source": profile.source,
            },
        }
    except Exception as e:
        logger.exception("Error obteniendo perfil de hardware")
        return {
            "success": False,
            "error": str(e),
        }


@app.post("/api/system/model-compatibility")
async def get_model_compatibility(provider: str = Form(...), model: str = Form(...)):
    from core.model_recommendation import evaluate_model_compatibility, get_hardware_profile

    try:
        hardware_profile = get_hardware_profile()
        compatibility = evaluate_model_compatibility(provider, model, hardware_profile)
        return {
            "success": True,
            "compatibility": compatibility,
        }
    except Exception as e:
        logger.exception("Error evaluando compatibilidad del modelo")
        return {
            "success": False,
            "error": str(e),
        }


@app.get("/api/agents/list")
async def list_agents():
    if not supervisor:
        return {"success": False, "error": "Supervisor no disponible"}

    agentes = []
    agentes_ids = set()

    # Fuente 1: Agentes JSON de todos los dominios registrados.
    for domain_id, config_dir in iter_agent_config_dirs():
        if not config_dir.exists():
            continue
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
                            "is_generic_baseline": False,
                            "domain_id": data.get("domain_id", domain_id),
                            "specialization_id": data.get("specialization_id"),
                            "specialization_name": data.get("specialization_name"),
                            "profile_preset_id": data.get("profile_preset_id"),
                            "profile_preset_name": data.get("profile_preset_name"),
                            "memory": data.get("memory"),
                            "metadata": data.get("metadata"),
                            "system_prompt": data.get("system_prompt"),
                        }
                    )
            except Exception as e:
                logger.warning(f"Error leyendo {json_file}: {e}")

    # Fuente 2: Agentes desde AgentManager (solo los que no tenemos ya)
    for agent_id in supervisor.agents.list_ids():
        if agent_id not in agentes_ids:
            role = supervisor.agents.get_role(agent_id)
            found = find_agent_json(agent_id)
            source = "json" if found else "python"
            is_generic = supervisor.agents.is_generic_baseline(agent_id)
            provider = "nvidia" if source == "json" else "python_module"
            model = "builtin" if source == "python" else "unknown"

            agentes.append(
                {
                    "id": agent_id,
                    "role": role or "unknown",
                    "provider": provider,
                    "model": model,
                    "source": source,
                    "is_generic_baseline": is_generic,
                    "domain_id": found[0]
                    if found
                    else getattr(supervisor.agents, "get_domain_id", lambda _id: None)(agent_id),
                }
            )
            agentes_ids.add(agent_id)

    return {"success": True, "agents": agentes, "total": len(agentes)}


# ========================================================================
# Modificar y eliminar agentes (genéricos)
# ========================================================================
@app.put("/api/agents/{agent_id}")
async def update_agent(agent_id: str, request: Request, domain_id: str | None = None):
    """Actualiza un agente existente (rol, provider, modelo, system_prompt)."""
    try:
        data = await request.json()
        role = data.get("role")
        provider = data.get("provider")
        model = data.get("model")
        system_prompt = data.get("system_prompt")
        specialization_id = data.get("specialization_id")

        resolved_domain_id, json_path = resolve_agent_json(agent_id, domain_id)

        with open(json_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        effective_domain_id = config_data.get("domain_id") or resolved_domain_id
        effective_role = role or config_data.get("role")
        # Solo validar role/specialization si el usuario está cambiando esos campos explícitamente
        # Esto permite edición operativa (provider/model/system_prompt) de agentes legacy
        role_changed = role is not None and role != config_data.get("role")
        specialization_changed = "specialization_id" in data and specialization_id != config_data.get("specialization_id")
        if role_changed or specialization_changed:
            profile_validation = _validate_agent_profile_selection(
                domain_id=effective_domain_id,
                role=effective_role,
                specialization_id=specialization_id,
            )
            if profile_validation.get("success") is False:
                return profile_validation

        if role:
            config_data["role"] = role
        if provider:
            config_data["provider"] = provider
        if model:
            config_data["model"] = model
        # Solo actualizar system_prompt si no está vacío (preservar existente)
        if system_prompt and system_prompt.strip():
            config_data["system_prompt"] = system_prompt
        if "specialization_id" in data:
            if specialization_id:
                config_data["specialization_id"] = specialization_id
                if profile_validation.get("specialization_name"):
                    config_data["specialization_name"] = profile_validation[
                        "specialization_name"
                    ]
            else:
                config_data.pop("specialization_id", None)
                config_data.pop("specialization_name", None)

        # Preservar campos nuevos y actualizar metadata
        if "metadata" not in config_data:
            config_data["metadata"] = {
                "schema_version": "1.0",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "created_via": "legacy_import",
            }
        else:
            config_data["metadata"]["updated_at"] = datetime.now().isoformat()

        if "memory" not in config_data:
            config_data["memory"] = {
                "source_uploaded": False,
                "source_filename": None,
                "indexed": False,
            }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Agente {agent_id} actualizado")
        return {"success": True, "message": f"Agente {agent_id} actualizado"}

    except (FileNotFoundError, ValueError) as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Error actualizando agente {agent_id}: {e}")
        return {"success": False, "error": str(e)}


@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: str, domain_id: str | None = None):
    """Elimina un agente (JSON, paper y memorias asociadas)."""
    try:
        if re.sub(r"[^a-zA-Z0-9_-]", "", agent_id) != agent_id:
            return {"success": False, "error": "ID de agente inválido"}

        _, json_path = resolve_agent_json(agent_id, domain_id)
        paper_path = json_path.parent.parent / "papers" / f"{agent_id}_paper.json"
        memory_path = ROOT / "memoria_agentes" / agent_id
        vector_path = ROOT / "memoria_vectorial" / agent_id

        json_path.unlink()
        logger.info(f"🗑️ Eliminado JSON de {agent_id}")

        if paper_path.exists():
            paper_path.unlink()
            logger.info(f"🗑️ Eliminado paper de {agent_id}")

        _delete_agent_directory(memory_path, agent_id, "memoria JSON")

        _release_agent_vector_memory(agent_id)

        _delete_agent_directory(vector_path, agent_id, "memoria vectorial")

        return {"success": True, "message": f"Agente {agent_id} eliminado exitosamente"}

    except (FileNotFoundError, ValueError) as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.exception(f"Error eliminando agente {agent_id}: {e}")
        return {"success": False, "error": str(e)}


@app.post("/api/agents/{agent_id}/regenerate-paper")
async def regenerate_agent_paper(agent_id: str, request: Request):
    """
    Regenera el paper de un agente existente usando mejorar_papers.py.

    Request body:
    {
        "domain_id": "loteria",
        "usar_llm": false
    }

    Response:
    {
        "success": true,
        "agent_id": "auditor_hostil",
        "domain_id": "loteria",
        "paper_path": "domains/loteria/agents/papers/auditor_hostil_paper.json",
        "changed": true,
        "message": "Paper regenerado correctamente.",
        "paper": {...}
    }
    """
    try:
        # Validar agent_id
        if not agent_id or not agent_id.strip():
            return {"success": False, "error": "ID del agente es obligatorio"}

        safe_agent_id = re.sub(r"[^a-zA-Z0-9_-]", "", agent_id)
        if safe_agent_id != agent_id:
            return {"success": False, "error": "ID de agente inválido"}

        # Extraer parámetros del request
        body = await request.json()
        domain_id = body.get("domain_id")
        usar_llm = body.get("usar_llm", False)

        # Validar domain_id
        if not domain_id or not domain_id.strip():
            return {"success": False, "error": "domain_id es obligatorio"}

        # Validar que el dominio existe
        domain = load_domain(domain_id)
        if domain is None:
            return {"success": False, "error": f"Dominio '{domain_id}' no encontrado"}

        # Validar que el agente existe (config JSON)
        try:
            _, agent_config_path = resolve_agent_json(safe_agent_id, domain_id)
        except (FileNotFoundError, ValueError) as e:
            return {"success": False, "error": f"Agente '{safe_agent_id}' no encontrado en dominio '{domain_id}': {e}"}

        # Validar usar_llm
        if not isinstance(usar_llm, bool):
            return {"success": False, "error": "usar_llm debe ser un valor booleano"}

        # Importar mejorar_papers
        import mejorar_papers

        # Llamar a mejorar_paper
        paper_result = mejorar_papers.mejorar_paper(
            safe_agent_id,
            usar_llm=usar_llm,
            domain_id=domain_id,
        )

        # Obtener ruta relativa del paper
        paper_path = mejorar_papers.resolver_paper_path(safe_agent_id, domain_id=domain_id)
        try:
            relative_paper_path = str(paper_path.relative_to(ROOT)) if paper_path.is_absolute() else str(paper_path)
        except ValueError:
            # Si paper_path no está dentro de ROOT (ej. en tmp_path durante tests), usar el nombre del archivo
            relative_paper_path = f"domains/{domain_id}/agents/papers/{safe_agent_id}_paper.json"

        # Devolver respuesta
        return {
            "success": True,
            "agent_id": safe_agent_id,
            "domain_id": domain_id,
            "paper_path": relative_paper_path,
            "changed": True,
            "message": "Paper regenerado correctamente.",
            "paper": paper_result,
        }

    except Exception as e:
        logger.exception(f"Error regenerando paper para agente {agent_id}: {e}")
        return {"success": False, "error": str(e)}


# ========================================================================
# Servir frontend
# ========================================================================
WEB_DIR = ROOT / "ui" / "web"

if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="static")
else:

    @app.get("/")
    async def root() -> dict:
        return {"message": "IA_CORE API activa. Coloca index.html en ui/web/"}


# ========================================================================
# Entry point
# ========================================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
