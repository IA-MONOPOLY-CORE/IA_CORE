"""Núcleo del sistema: ensambla y arranca los gestores de forma asíncrona con optimización cuántica definitiva."""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, Type

import config as app_config

from agents.manager import AgentManager
from core.debate import (
    DebateTurn,
    build_pipeline,
    build_previous_outputs_async,
    collect_contradictions,
    compute_consensus_scores,
    detect_contradiction,
    extract_text,
    make_step_id,
    synthesize_final_response,
)
from core.evolution_base import EvolutionManagerBase
from core.orchestration import (
    AgentStepResult,
    DebateResult,
    ExecutionMode,
    OrchestrationResult,
    iso,
    new_execution_id,
    utc_now,
)
from memory.manager import MemoryManager
from core.hybrid.router import HybridRouter
from providers.registry import ProviderRegistry
from tools.manager import ToolManager

logger = logging.getLogger(__name__)

MEMORY_HISTORY_KEY = "orchestration_history"
MEMORY_RESULT_PREFIX = "orchestration:"
MEMORY_SCORES_KEY = "orchestration_scores"
MEMORY_DEBATE_PREFIX = "debate:"


class Supervisor:
    """Punto central de orquestación asíncrona de alto rendimiento."""

    def __init__(
        self,
        log_dir: str | Path = "logs",
        *,
        expert_mapping: Optional[dict[str, str]] = None,
        debate_pipeline: Optional[list[tuple[str, str]]] = None,
        default_debate_agents: Optional[list[str]] = None,
        evolution_manager_class: Optional[Type[EvolutionManagerBase]] = None,
        score_response_fn: Optional[Callable] = None,
        build_scores_summary_fn: Optional[Callable] = None
    ) -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._running = False

        # Domain-specific configuration (with lotería defaults for backwards compatibility)
        self._expert_mapping = expert_mapping or self._get_default_expert_mapping()
        self._debate_pipeline = debate_pipeline
        self._default_debate_agents = default_debate_agents or self._get_default_debate_agents()
        self._evolution_manager_class = evolution_manager_class or self._get_default_evolution_manager_class()
        self._score_response_fn = score_response_fn or self._get_default_score_response_fn()
        self._build_scores_summary_fn = build_scores_summary_fn or self._get_default_build_scores_summary_fn()

        self.providers = ProviderRegistry()
        self.memory = MemoryManager()
        self.tools = ToolManager()
        self.agents = AgentManager(
            memory=self.memory,
            tools=self.tools,
            providers=self.providers,
        )
        self.hybrid_router: HybridRouter | None = None
        self.evolution = self._evolution_manager_class()

    # ========================================================================
    # Helper methods to get default lotería config for backwards compatibility
    # ========================================================================
    @staticmethod
    def _get_default_expert_mapping() -> dict[str, str]:
        try:
            from domains.loteria.config_loteria import BUNKER_EXPERT_MAPPING
            return BUNKER_EXPERT_MAPPING
        except ImportError:
            return {}

    @staticmethod
    def _get_default_debate_agents() -> list[str]:
        try:
            from domains.loteria.config_loteria import DEBATE_AGENTS
            return DEBATE_AGENTS
        except ImportError:
            return []

    @staticmethod
    def _get_default_evolution_manager_class() -> Type[EvolutionManagerBase]:
        try:
            from domains.loteria.evolution_loteria import EvolutionManagerLoteria
            return EvolutionManagerLoteria
        except ImportError:
            from core.evolution_base import EvolutionManagerBase
            return EvolutionManagerBase

    @staticmethod
    def _get_default_score_response_fn() -> Callable:
        try:
            from domains.loteria.scoring import score_response
            return score_response
        except ImportError:
            def dummy_score(*args, **kwargs):
                from dataclasses import dataclass
                @dataclass
                class DummyScore:
                    total: float = 0.0
                    detalles: dict = None
                return DummyScore()
            return dummy_score

    @staticmethod
    def _get_default_build_scores_summary_fn() -> Callable:
        try:
            from domains.loteria.scoring import build_scores_summary
            return build_scores_summary
        except ImportError:
            def dummy_summary(*args, **kwargs):
                return "Sin puntuación disponible"
            return dummy_summary

    @property
    def running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self._running:
            logger.warning("Supervisor ya en ejecución")
            return

        logger.info("Iniciando sistema IA_CORE")
        self.providers.load_builtin_providers()
        if app_config.PROVIDER_FALLBACK_CHAIN:
            self.providers.set_fallback_chain(app_config.PROVIDER_FALLBACK_CHAIN)
        self.memory.start()
        self.tools.start()
        self.agents.start()
        if app_config.HYBRID_MODE:
            self.hybrid_router = HybridRouter(self.providers)
            logger.info("HybridRouter activo")
        self._preload_ollama_chat_model()
        self._running = True
        logger.info("Supervisor activo")

    def _preload_ollama_chat_model(self) -> None:
        if not getattr(app_config, "OLLAMA_PRELOAD_MODEL", False):
            return
        ollama = self.providers.get("ollama")
        if ollama is None or not hasattr(ollama, "preload_model"):
            return
        model = getattr(app_config, "DEFAULT_LOCAL_MODEL", "phi3:mini")
        if ollama.preload_model(model):
            logger.info("Modelo de chat precargado: %s", model)

    def stop(self) -> None:
        if not self._running:
            return

        logger.info("Deteniendo sistema")
        self.agents.stop()
        self.tools.stop()
        self.memory.stop()
        self._running = False
        logger.info("Supervisor detenido")

    def shutdown(self) -> None:
        self.stop()

    def orchestrate(
        self,
        task: str,
        agent_names: list[str] | None = None,
        *,
        mode: ExecutionMode = ExecutionMode.SEQUENTIAL,
    ) -> OrchestrationResult:
        """Wrapper sincrónico para orchestrate_async()."""
        return asyncio.run(
            self.orchestrate_async(task, agent_names, mode=mode)
        )

    async def orchestrate_async(
        self,
        task: str,
        agent_names: list[str] | None = None,
        *,
        mode: ExecutionMode = ExecutionMode.SEQUENTIAL,
    ) -> OrchestrationResult:
        """Punto de entrada asíncrono para orquestar debates y ejecuciones sin bloqueo."""
        if not self._running:
            raise RuntimeError("El supervisor debe estar en ejecución (llama a start())")

        execution_id = new_execution_id()
        started = utc_now()

        # CORRECCIÓN: Respetar los agentes pasados por parámetro
        if mode is ExecutionMode.DEBATE:
            # Si se pasaron agentes específicos, usarlos. Si no, usar los 6 del sistema.
            if agent_names:
                targets = agent_names
                logger.info(f"Usando agentes seleccionados por el usuario: {targets}")
            else:
                targets = self._resolve_debate_agents()
                logger.info(f"Usando agentes por defecto (sistema): {targets}")
        else:
            targets = self._resolve_agents(agent_names)

        logger.info(
            "Orquestación Asíncrona %s iniciada | modo=%s | agentes=%s",
            execution_id,
            mode.value,
            targets,
        )

        result = OrchestrationResult(
            execution_id=execution_id,
            task=task,
            mode=mode.value,
            agents=targets,
            started_at=iso(started),
        )

        orch_deadline = time.perf_counter() + app_config.ORCHESTRATION_TIMEOUT_S

        if mode is ExecutionMode.SEQUENTIAL:
            if not targets:
                result.success = False
                result.scores_summary = self._build_scores_summary_fn([])
            else:
                result.steps = await asyncio.to_thread(
                    self._run_sequential, execution_id, task, targets, deadline=orch_deadline
                )
                result.success = all(step.success for step in result.steps)
                result.scores_summary = self._build_scores_summary_fn(result.steps)

        elif mode is ExecutionMode.DEBATE:
            debate = await self._run_debate_async(execution_id, task, targets, deadline=orch_deadline)
            result.debate = debate
            result.steps = debate.steps
            
            continue_on_failure = getattr(app_config, "SEQUENTIAL_CONTINUE_ON_FAILURE", True)
            result.success = any(step.success for step in debate.steps) if continue_on_failure else all(step.success for step in debate.steps)
            result.scores_summary = self._build_scores_summary_fn(debate.steps)
            
            # Registrar aprendizaje post-ejecución
            await self._registrar_aprendizaje_post_debate(debate)

        else:
            raise NotImplementedError(f"Modo no implementado: {mode.value}")

        finished = utc_now()
        result.finished_at = iso(finished)
        result.duration_ms = (finished - started).total_seconds() * 1000

        await asyncio.to_thread(self._persist_orchestration, result)
        return result

    async def _run_debate_async(
        self, execution_id: str, task: str, agent_ids: list[str], *, deadline: float | None = None
    ) -> DebateResult:
        """
        NUEVO MOTOR RECURSIVO CUÁNTICO CON MEMORIA SEMÁNTICA COMPLETA
        Implementa timeouts granulares por agente, resúmenes automáticos por ronda
        y persistencia robusta por checkpoints sugerida por DeepSeek.
        
        AHORA RESPETA LOS AGENTES SELECCIONADOS POR EL USUARIO.
        """
        debate_id = new_execution_id()
        debate = DebateResult(debate_id=debate_id, task=task)
        steps: list[AgentStepResult] = []
        
        # Usar los agentes que se pasaron como parámetro
        agent_roles = []
        for agent_id in agent_ids:
            # Buscar el rol correspondiente a cada agente
            found_role = None
            for role, mapped_id in self._expert_mapping.items():
                if mapped_id == agent_id:
                    found_role = role
                    break
            if not found_role:
                found_role = agent_id  # Si no está mapeado, usar el ID como rol
            agent_roles.append((agent_id, found_role))
        
        historial_por_ronda: list[dict[str, str]] = []
        
        TOTAL_RECURSIVE_ROUNDS = 5
        agent_timeout = getattr(app_config, "AGENT_TIMEOUT_S", 30.0)
        
        for round_idx in range(1, TOTAL_RECURSIVE_ROUNDS + 1):
            if deadline is not None and time.perf_counter() > deadline:
                logger.error("Debate %s abortado por timeout global en ronda %d", debate_id, round_idx)
                break
                
            logger.info(f"🔄 [Mesa Redonda Cuántica - Ronda {round_idx}/{TOTAL_RECURSIVE_ROUNDS}] Lanzando {len(agent_roles)} agentes en paralelo...")
            round_start_time = time.perf_counter()
            
            if round_idx == 1:
                contexto_acumulado = f"TAREA/PATRÓN INICIAL DE ANÁLISIS: {task}"
            else:
                resumenes_previos = [f"● Resumen Ronda {i+1}: {r['summary']}" for i, r in enumerate(historial_por_ronda)]
                bloque_resumenes = "\n".join(resumenes_previos)
                ultimo_raw = historial_por_ronda[-1]["raw"] if historial_por_ronda else ""
                
                contexto_acumulado = (
                    f"🎯 TAREA PRINCIPAL INALTERABLE: {task}\n\n"
                    f"📋 SÍNTESIS HISTÓRICA DEL PROGRESO (RONDAS PREVIAS):\n"
                    f"{bloque_resumenes}\n\n"
                    f"🚨 COLISIÓN INMEDIATA DE LA ÚLTIMA RONDA:\n"
                    f"{ultimo_raw}\n\n"
                    f"INSTRUCCIÓN RECURSIVA: Re-evalúen sus métricas estadísticas basándose en la colisión anterior. "
                    f"Busquen contradicciones en los números de los demás, refuercen o rompan la hipótesis predictiva."
                )

            corrutinas = []
            info_agentes_ronda = []
            
            for agent_id, role_name in agent_roles:
                step_id = f"{debate_id}-q{round_idx}-{agent_id}"
                
                info_agentes_ronda.append((role_name, agent_id, step_id))
                
                corrutinas.append(
                    asyncio.wait_for(
                        self._execute_single_quantum_agent_async(
                            execution_id=execution_id,
                            debate_id=debate_id,
                            task=task,
                            round_number=round_idx,
                            role_name=role_name,
                            agent_id_to_use=agent_id,
                            step_id=step_id,
                            contexto_debate=contexto_acumulado
                        ),
                        timeout=agent_timeout
                    )
                )
            
            try:
                resultados_paralelos = await asyncio.gather(*corrutinas, return_exceptions=True)
            except asyncio.TimeoutError:
                logger.error(f"⚠️ Alerta: Uno o más agentes superaron el timeout de {agent_timeout}s en la ronda {round_idx}")
                resultados_paralelos = [None] * len(agent_roles)
            
            bloque_respuestas_ronda = []
            for idx, res in enumerate(resultados_paralelos):
                role_name, real_agent_id, step_id = info_agentes_ronda[idx]
                
                if isinstance(res, asyncio.TimeoutError) or res is None:
                    logger.warning(f"⏳ TIMEOUT AGENTE: {real_agent_id} (rol: {role_name}) en ronda {round_idx}/{TOTAL_RECURSIVE_ROUNDS} - superó {agent_timeout}s")
                    continue
                if isinstance(res, Exception) or not res.success:
                    logger.error(f"Fallo crítico en agente {real_agent_id} durante ronda {round_idx}: {res}")
                    if isinstance(res, AgentStepResult):
                        steps.append(res)
                    continue
                
                steps.append(res)
                text_clean = extract_text(res.result)
                bloque_respuestas_ronda.append(f"  ▶️ [{role_name.upper()} - {real_agent_id}]: {text_clean}")
            
            registro_ronda = f"=== [HISTORIAL DE LA RONDA {round_idx}] ===\n" + "\n".join(bloque_respuestas_ronda)
            
            logger.info(f"🧠 Optimizando memoria semántica: Resumiendo colisiones de la ronda {round_idx}...")
            resumen_ronda = await self._resumir_bloque_async(registro_ronda, round_idx)
            
            historial_por_ronda.append({
                "raw": registro_ronda,
                "summary": resumen_ronda
            })
            
            checkpoint_data = {
                "round": round_idx,
                "historial": historial_por_ronda,
                "steps": [s.to_dict() if hasattr(s, "to_dict") else str(s) for s in steps]
            }
            await asyncio.to_thread(
                self.memory.set,
                f"{MEMORY_DEBATE_PREFIX}{debate_id}_round_{round_idx}",
                checkpoint_data
            )
            logger.info(f"🗄️ Checkpoint guardado de forma segura para la ronda {round_idx}")
            
            round_duration_ms = (time.perf_counter() - round_start_time) * 1000
            logger.info(f"✅ Ronda {round_idx} completada en {round_duration_ms:.0f}ms")

            # Verificar criterio de parada temprana por consenso alto (mínimo 2 rondas)
            if round_idx >= 2:
                contradictions = collect_contradictions(steps)
                agreement, contradiction = compute_consensus_scores(steps, contradictions)
                threshold_fraction = getattr(app_config, "AGREEMENT_EARLY_STOP_THRESHOLD", 0.85)
                threshold_percent = threshold_fraction * 100  # convertir a 0-100 para comparar con agreement_score

                if agreement >= threshold_percent:
                    logger.info(
                        f"🎯 PARADA TEMPRANA ACTIVADA: Ronda {round_idx}/{TOTAL_RECURSIVE_ROUNDS} "
                        f"con agreement_score={agreement:.2f}% (umbral: {threshold_percent:.2f}%). "
                        f"Saltando {TOTAL_RECURSIVE_ROUNDS - round_idx} rondas restantes."
                    )
                    break

            await asyncio.sleep(0.001)

        logger.info("🛡️ Fase de Colisión Terminada. Iniciando Pipeline de Cierre y Auditoría...")
        
        resumenes_totales = [f"● Ronda {i+1}: {r['summary']}" for i, r in enumerate(historial_por_ronda)]
        contexto_final_auditoria = (
            f"TAREA ORIGINAL: {task}\n\n"
            f"SÍNTESIS COMPLETA DE TODAS LAS RONDAS RECURSIVAS:\n" + "\n".join(resumenes_totales) + "\n\n"
            f"ÚLTIMA COLISIÓN DETALLADA (RAW):\n{historial_por_ronda[-1]['raw'] if historial_por_ronda else ''}"
        )
        
        pipeline_secuencial = build_pipeline(self._debate_pipeline)
        last_step_id = steps[-1].step_id if steps else None

        for turn in pipeline_secuencial:
            if deadline is not None and time.perf_counter() > deadline:
                break
                
            step_id = make_step_id(debate_id, turn.round_number + 10, turn.agent_name)
            parent_id = turn.parent_step_id or last_step_id
            real_agent_id = self._expert_mapping.get(turn.agent_name, turn.agent_name)
            
            prompt_auditoria = (
                f"Fase de Cierre Analítico: {turn.phase}.\n"
                f"Todo el búnker ya debatió fuertemente en las rondas cuánticas previas.\n"
                f"A continuación tenés el mapa acumulado de la discusión:\n\n{contexto_final_auditoria}\n\n"
                f"Ejecutá tu rol de forma ultra-robusta y detallada basándote en este ecosistema."
            )
            
            step = await self._execute_debate_turn_async(
                execution_id=execution_id,
                debate_id=debate_id,
                task=prompt_auditoria,
                turn=turn,
                agent_id_to_use=real_agent_id,
                parent_id=parent_id,
                step_id=step_id,
                current_steps=steps
            )
            steps.append(step)
            last_step_id = step_id
            await asyncio.sleep(0.001)

        contradictions = collect_contradictions(steps)
        agreement, contradiction = compute_consensus_scores(steps, contradictions)
        
        debate.steps = steps
        debate.agreement_score = agreement
        debate.contradiction_score = contradiction
        debate.final_response = synthesize_final_response(task, steps)
        
        logger.info(f"🎯 Consenso Cuántico Finalizado Estructurado -> Acuerdo: {agreement}% | Contradicciones: {contradiction}%")
        return debate

    async def _resumir_bloque_async(self, texto_ronda: str, round_idx: int) -> str:
        """Usa el árbitro del dominio configurado de manera asíncrona para sintetizar las colisiones sin bloquear."""
        arbitro_id = self._expert_mapping.get("orchestrator", self._expert_mapping.get("optimizer"))
        if not arbitro_id and self._default_debate_agents:
            arbitro_id = self._default_debate_agents[-1]
        agent = self.agents.get(arbitro_id)
        if not agent:
            return f"[Resumen automático] Finalizada ronda {round_idx} de debate."
            
        prompt_resumen = (
            f"Extraé únicamente las tesis principales, los números clave y los puntos de desacuerdo "
            f"de la siguiente ronda de debate. Sé ultra-breve y ejecutivo. Máximo 2 o 3 líneas totales.\n\n{texto_ronda}"
        )
        try:
            # Pass arguments based on agent type
            if hasattr(agent, "system_prompt"):
                response = await asyncio.to_thread(
                    agent.run, 
                    prompt_resumen, 
                    system_prompt="Sos un extractor de datos semánticos y clusters de información de alta precisión."
                )
            else:
                response = await asyncio.to_thread(agent.run, prompt_resumen)
            return extract_text(response)
        except Exception as e:
            logger.error(f"No se pudo generar el resumen de la ronda {round_idx}: {e}")
            return f"[Error en síntesis] Ronda {round_idx} procesada de forma parcial."

    async def _execute_single_quantum_agent_async(
        self, execution_id: str, debate_id: str, task: str, round_number: int,
        role_name: str, agent_id_to_use: str, step_id: str, contexto_debate: str
    ) -> AgentStepResult:
        """Helper asíncrono aislado para resolver un solo agente dentro del pool del gather."""
        start_time = time.perf_counter()
        agent = self.agents.get(agent_id_to_use)

        if not agent:
            return AgentStepResult(step_id=step_id, agent_name=agent_id_to_use, success=False, error=f"No agent found for ID {agent_id_to_use}")

        try:
            fast_mode_rules = (
                "\n\n[DIRECTRICE CRÍTICA - FAST THINKING]\n"
                "Sé directo, ultra-conciso y técnico. NO metas introducciones amables. "
                "Ve directo al grano escribiendo tus datos, fórmulas y clusters estadísticos. "
                "Máximo 3 a 5 líneas por argumento técnico."
            )
            
            contexto_evolutivo = self.evolution.get_contexto_para_prompt(role=role_name)
            contexto_str = "".join(
                f"\n- {k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v}"
                for k, v in contexto_evolutivo.items()
            )
            
            prompt_final = (
                f"{contexto_debate}\n\n"
                f"CONTEXTO EVOLUTIVO DINÁMICO:{contexto_str}\n\n"
                f"{fast_mode_rules}"
            )
            
            system_prompt = getattr(agent, "system_prompt", None)
            if system_prompt:
                for key, value in contexto_evolutivo.items():
                    placeholder = "{" + key + "}"
                    if placeholder in system_prompt:
                        system_prompt = system_prompt.replace(placeholder, str(value))
            
            # Pass arguments based on agent type
            if hasattr(agent, "system_prompt"):
                response = await asyncio.to_thread(agent.run, prompt_final, system_prompt=system_prompt)
            else:
                response = await asyncio.to_thread(agent.run, prompt_final)
            text_response = extract_text(response)
            duration = (time.perf_counter() - start_time) * 1000
            
            numeros_encontrados = re.findall(r'\b([0-4]?[0-9]|50)\b', text_response)
            combinacion = [int(n) for n in numeros_encontrados[:6]] if len(numeros_encontrados) >= 6 else None
            
            score_data = self._score_response_fn(
                agent_name=agent_id_to_use,
                role=getattr(agent, "role", role_name),
                result={"output": text_response},
                success=True,
                duration_ms=duration,
                combinacion=combinacion
            )

            return AgentStepResult(
                step_id=step_id,
                agent_name=agent_id_to_use,
                role=getattr(agent, "role", role_name),
                round_number=round_number,
                success=True,
                result={"output": text_response, "llm": response.get("llm", {}) if isinstance(response, dict) else {}},
                duration_ms=duration,
                score=score_data,
                contradiction=detect_contradiction(text_response),
                refinement=False
            )
        except Exception as e:
            return AgentStepResult(step_id=step_id, agent_name=agent_id_to_use, success=False, error=str(e), duration_ms=(time.perf_counter() - start_time) * 1000)

    async def _execute_debate_turn_async(
        self, execution_id: str, debate_id: str, task: str, turn: DebateTurn, 
        agent_id_to_use: str, parent_id: str | None, step_id: str, current_steps: list[AgentStepResult]
    ) -> AgentStepResult:
        """Ejecuta un turno asíncronamente eliminando bloqueos del event loop."""
        start_time = time.perf_counter()
        agent = self.agents.get(agent_id_to_use)
        
        logger.info(f"🔍 Buscando agente de cierre: {agent_id_to_use} | Parent ID vinculado: {parent_id}")

        if not agent:
            logger.error(f"❌ Agente no encontrado en AgentManager: {agent_id_to_use}")
            return AgentStepResult(
                step_id=step_id, agent_name=agent_id_to_use, success=False, 
                error=f"Mente experta '{agent_id_to_use}' (titular) no se encuentra registrada."
            )

        provider_name = agent.llm_provider.provider_name() if (hasattr(agent, "llm_provider") and agent.llm_provider) else "Unknown"
        logger.info(f"✅ Agente encontrado: {agent.id} | role: {getattr(agent, 'role', 'Unknown')} | provider: {provider_name}")

        try:
            history = await build_previous_outputs_async(current_steps)
            
            fast_mode_rules = (
                "\n\n[DIRECTRICE CRÍTICA S.A.A.O.P.]\n"
                "Sé directo, ultra-conciso y técnico. NO incluyas introducciones amables. "
                "Ve al grano escribiendo directamente tus datos, fórmulas o bullets de impacto numérico. "
                "Máximo 3 a 5 líneas por argumento técnico."
            )
            
            contexto = self.evolution.get_contexto_para_prompt(role=turn.agent_name)
            contexto_str = ""
            for key, value in contexto.items():
                if isinstance(value, (dict, list)):
                    contexto_str += f"\n- {key}: {json.dumps(value, ensure_ascii=False)}"
                else:
                    contexto_str += f"\n- {key}: {value}"
            
            prompt_base = f"Tarea: {task}\nFase de Debate: {turn.phase}\nHistorial del Circuito:\n{history}\n\nCONTEXTO EVOLUTIVO:\n{contexto_str}\n\n{fast_mode_rules}"
            
            system_prompt = getattr(agent, "system_prompt", None)
            if system_prompt:
                for key, value in contexto.items():
                    placeholder = "{" + key + "}"
                    if placeholder in system_prompt:
                        system_prompt = system_prompt.replace(placeholder, str(value))
            
            logger.info(f"🚀 Ejecutando agente de cierre: {agent.id}")
            
            if not agent.llm_provider and hasattr(agent, "system_prompt"):
                logger.error(f"❌ Agente {agent.id} no tiene llm_provider asignado")
                return AgentStepResult(
                    step_id=step_id, agent_name=agent_id_to_use, success=False,
                    error=f"Agente {agent.id} sin llm_provider."
                )
            
            if hasattr(agent, "llm_provider") and agent.llm_provider:
                logger.info(f"📡 Usando proveedor: {agent.llm_provider.provider_name()}")

            # Buscar lecciones útiles para este rol antes de ejecutar
            lecciones_externas = []
            try:
                lecciones_externas = buscar_lecciones_utiles(turn.agent_name, top_k=2)
                if lecciones_externas:
                    logger.info(f"💡 {agent.id}: {len(lecciones_externas)} lecciones útiles inyectadas al prompt")
            except Exception as e:
                logger.warning(f"Error buscando lecciones útiles: {e}")

            context = {"lecciones_externas": lecciones_externas}
            # Pass arguments based on agent type
            if hasattr(agent, "system_prompt"):
                response = await asyncio.to_thread(agent.run, prompt_base, system_prompt=system_prompt, context=context)
            else:
                response = await asyncio.to_thread(agent.run, prompt_base, context=context)
            text_response = extract_text(response)
            
            logger.info(f"✅ Respuesta recibida de {agent.id} | longitud: {len(text_response)} chars")
            
            duration = (time.perf_counter() - start_time) * 1000
            
            numeros_encontrados = re.findall(r'\b([0-4]?[0-9]|50)\b', text_response)
            combinacion = [int(n) for n in numeros_encontrados[:6]] if len(numeros_encontrados) >= 6 else None
            
            score_data = self._score_response_fn(
                agent_name=agent_id_to_use,
                role=getattr(agent, "role", turn.agent_name),
                result={"output": text_response},
                success=True,
                duration_ms=duration,
                combinacion=combinacion
            )

            return AgentStepResult(
                step_id=step_id,
                agent_name=agent_id_to_use,
                role=getattr(agent, "role", turn.agent_name),
                round_number=turn.round_number,
                success=True,
                result={"output": text_response, "llm": response.get("llm", {}) if isinstance(response, dict) else {}},
                duration_ms=duration,
                score=score_data,
                contradiction=detect_contradiction(text_response),
                refinement=(turn.phase in ("refine", "reformulate"))
            )
        except Exception as e:
            logger.exception(f"❌ Error ejecutando agente {agent_id_to_use}: {e}")
            return AgentStepResult(
                step_id=step_id, agent_name=agent_id_to_use, success=False, 
                error=str(e), duration_ms=(time.perf_counter() - start_time) * 1000
            )

    def _run_sequential(self, execution_id: str, task: str, targets: list[str], deadline: float) -> list[AgentStepResult]:
        """Ejecuta agentes secuenciales delegando de forma segura sin colgar el event loop."""
        steps = []
        for index, name in enumerate(targets, start=1):
            if time.perf_counter() > deadline:
                break
            step_id = f"{execution_id}-s{index}-{name}"
            agent = self.agents.get(name)
            if agent:
                start = time.perf_counter()
                try:
                    res = agent.run(task)
                    steps.append(AgentStepResult(
                        step_id=step_id, agent_name=name, success=True, 
                        result=res, duration_ms=(time.perf_counter() - start) * 1000
                    ))
                except Exception as e:
                    steps.append(AgentStepResult(step_id=step_id, agent_name=name, success=False, error=str(e)))
        return steps

    def _persist_orchestration(self, result: OrchestrationResult) -> None:
        """Persiste los resultados de la ejecución en el MemoryManager."""
        try:
            key = f"{MEMORY_RESULT_PREFIX}{result.execution_id}"
            self.memory.set(key, result.to_dict() if hasattr(result, "to_dict") else str(result))
            logger.info("Resultado de orquestación %s guardado en memoria", result.execution_id)
        except Exception as e:
            logger.error("No se pudo persistir la orquestación: %s", e)

    def get_orchestration(self, execution_id: str) -> Any | None:
        key = f"{MEMORY_RESULT_PREFIX}{execution_id}"
        return self.memory.get(key)
        
    def get_debate(self, debate_id: str) -> Any | None:
        key = f"{MEMORY_DEBATE_PREFIX}{debate_id}"
        return self.memory.get(key)

    def _resolve_debate_agents(self) -> list[str]:
        """Devuelve los agentes por defecto del dominio configurado."""
        return self._default_debate_agents

    def _resolve_agents(self, agent_names: list[str] | None) -> list[str]:
        available = self.agents.list_ids()
        if agent_names is None:
            return available
        return [name for name in agent_names if name in available]

    # ========================================================================
    # APRENDIZAJE POST-EJECUCIÓN Y MEMORIA COMPARTIDA
    # ========================================================================
    async def _registrar_aprendizaje_post_debate(self, debate_result: DebateResult) -> None:
        """
        Registra lecciones aprendidas para cada agente.
        También guarda contradicciones resueltas en memoria compartida.
        """
        logger.info("🔵 ENTRO A _registrar_aprendizaje_post_debate")
        
        if not debate_result or not debate_result.steps:
            logger.warning("⚠️ debate_result o steps vacío")
            return
        
        logger.info(f"🔵 contradiction_score={debate_result.contradiction_score}, agreement_score={debate_result.agreement_score}, final_response existe={bool(debate_result.final_response)}")
        
        try:
            from core.memoria_perpetua import cargar_memoria, guardar_memoria
            from core.herramientas import extraer_herramientas_de_respuesta, registrar_herramienta, buscar_lecciones_utiles
            
            # Encontrar el mejor agente del debate
            best_agent = None
            best_score = 0
            
            for step in debate_result.steps:
                if step.success and step.score and step.score.total > best_score:
                    best_score = step.score.total
                    best_agent = step.agent_name
            
            # ========== MEMORIA COMPARTIDA: REGISTRAR CONTRADICCIONES RESUELTAS ==========
            if debate_result.contradiction_score > 0 and debate_result.final_response:
                logger.info("🔵 CONDICIÓN CUMPLIDA: Registrando contradicción resuelta")
                # Obtener la síntesis del final_response si existe
                synthesis_text = ""
                if isinstance(debate_result.final_response, dict):
                    synthesis_text = debate_result.final_response.get("synthesis", "")
                elif isinstance(debate_result.final_response, str):
                    synthesis_text = debate_result.final_response
                
                leccion_compartida = {
                    "timestamp": datetime.now().isoformat(),
                    "debate_id": debate_result.debate_id,
                    "contradiccion_inicial": debate_result.contradiction_score,
                    "consenso_final": debate_result.agreement_score,
                    "mejor_agente": best_agent,
                    "mejor_score": best_score,
                    "leccion": synthesis_text[:500] if synthesis_text else "Sin síntesis disponible",
                    "agentes_participantes": [step.agent_name for step in debate_result.steps if step.success]
                }
                
                compartida_path = Path("memory/herramientas_compartidas.json")
                compartida_path.parent.mkdir(parents=True, exist_ok=True)
                
                if compartida_path.exists():
                    with open(compartida_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = {
                        "herramientas": [],
                        "contradicciones_resueltas": [],
                        "lecciones_compartidas": [],
                        "ultima_actualizacion": None,
                        "versiones_por_agente": {},
                        "metricas_globales": {
                            "total_contradicciones": 0,
                            "total_consensos": 0,
                            "total_herramientas_registradas": 0
                        }
                    }
                
                data["contradicciones_resueltas"].append(leccion_compartida)
                data["metricas_globales"]["total_contradicciones"] += 1
                data["ultima_actualizacion"] = datetime.now().isoformat()
                
                # Mantener solo las últimas 100 contradicciones para no saturar
                if len(data["contradicciones_resueltas"]) > 100:
                    data["contradicciones_resueltas"] = data["contradicciones_resueltas"][-100:]
                
                with open(compartida_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                logger.info(f"📝 Contradicción resuelta registrada en memoria compartida (contradicción: {debate_result.contradiction_score}% → acuerdo: {debate_result.agreement_score}%)")
            else:
                logger.info("🔵 CONDICIÓN NO CUMPLIDA: No se registró contradicción")
            
            # ========== APRENDIZAJE POR AGENTE ==========
            for step in debate_result.steps:
                if not step.success:
                    continue
                
                agente_id = step.agent_name
                texto_respuesta = extract_text(step.result)
                score = step.score.total if step.score else 0
                
                memoria = cargar_memoria(agente_id)
                
                fue_acierto = score >= 60
                leccion = texto_respuesta[:300] if texto_respuesta else ""
                
                if not leccion:
                    continue
                
                if fue_acierto:
                    if "patrones_aprendidos" not in memoria:
                        memoria["patrones_aprendidos"] = []
                    memoria["patrones_aprendidos"].append({
                        "patron": leccion,
                        "score": score,
                        "timestamp": datetime.now().isoformat(),
                        "debate_id": debate_result.debate_id
                    })
                    if len(memoria["patrones_aprendidos"]) > 50:
                        memoria["patrones_aprendidos"] = memoria["patrones_aprendidos"][-50:]
                    logger.info(f"📚 {agente_id}: Nuevo patrón aprendido (score: {score})")
                    
                    # Extraer herramientas de respuestas exitosas
                    if score >= 70:
                        herramientas = extraer_herramientas_de_respuesta(
                            respuesta=texto_respuesta,
                            score=score,
                            agente_id=agente_id,
                            rol=step.role or "unknown"
                        )
                        
                        for herramienta in herramientas:
                            registrar_herramienta(
                                nombre=herramienta["nombre"],
                                descripcion=herramienta["descripcion"],
                                agente_creador=agente_id,
                                rol_asociado=herramienta["rol"],
                                contexto_exito=herramienta["contexto"],
                                score=score
                            )
                            logger.info(f"🔧 {agente_id}: Herramienta '{herramienta['nombre']}' registrada (score: {score})")
                    
                else:
                    if "errores_cometidos" not in memoria:
                        memoria["errores_cometidos"] = []
                    memoria["errores_cometidos"].append({
                        "error": leccion,
                        "score": score,
                        "timestamp": datetime.now().isoformat(),
                        "debate_id": debate_result.debate_id
                    })
                    if len(memoria["errores_cometidos"]) > 50:
                        memoria["errores_cometidos"] = memoria["errores_cometidos"][-50:]
                    logger.info(f"📚 {agente_id}: Nuevo error registrado (score: {score})")
                
                guardar_memoria(agente_id, memoria)
            
            # ========== REGENERAR PAPER DEL MEJOR AGENTE ==========
            if best_agent and best_score >= 70:
                try:
                    from mejorar_papers import mejorar_paper
                    import threading
                    threading.Thread(target=mejorar_paper, args=(best_agent,), kwargs={'usar_llm': False}).start()
                    logger.info(f"🔄 Regeneración automática de paper iniciada para {best_agent} (best score: {best_score})")
                except Exception as e:
                    logger.warning(f"Error iniciando regeneración de paper: {e}")
            
            # ========== BUSCAR LECCIONES ÚTILES PARA OTROS AGENTES ==========
            for step in debate_result.steps:
                if step.success and step.role:
                    try:
                        lecciones_utiles = buscar_lecciones_utiles(step.role, top_k=2)
                        if lecciones_utiles:
                            logger.info(f"💡 {step.agent_name}: {len(lecciones_utiles)} lecciones útiles disponibles de otros agentes")
                    except Exception as e:
                        logger.warning(f"Error buscando lecciones útiles: {e}")
                
        except Exception as e:
            logger.error(f"Error registrando aprendizaje post-debate: {e}")
