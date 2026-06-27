#!/usr/bin/env python3
"""Prueba del debate genérico."""

import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Import domain config and supervisor
from domains.demo_generico import (
    DEBATE_AGENTS as GENERIC_DEBATE_AGENTS,
    DEFAULT_DEBATE_TASK,
    GENERIC_EXPERT_MAPPING,
    DEBATE_PIPELINE_4_AGENTS,
    ResponseScore,
    score_response,
    build_scores_summary,
    EvolutionManagerDemo
)
from core.supervisor import Supervisor
from core.orchestration import ExecutionMode


async def main():
    logger.info("=== Iniciando prueba del debate genérico ===")

    # Initialize supervisor with our demo_generico config!
    supervisor = Supervisor(
        expert_mapping=GENERIC_EXPERT_MAPPING,
        debate_pipeline=DEBATE_PIPELINE_4_AGENTS,
        default_debate_agents=GENERIC_DEBATE_AGENTS,
        evolution_manager_class=EvolutionManagerDemo,
        score_response_fn=score_response,
        build_scores_summary_fn=build_scores_summary
    )
    supervisor.start()

    # Define our example task (no lotería!)
    TASK = DEFAULT_DEBATE_TASK

    # List our generic agents
    GENERIC_AGENTS = GENERIC_DEBATE_AGENTS

    logger.info(f"Usando agentes: {GENERIC_AGENTS}")
    logger.info(f"Tarea: {TASK.strip()}")

    try:
        # Run the debate!
        result = await supervisor.orchestrate_async(
            task=TASK,
            agent_names=GENERIC_AGENTS,
            mode=ExecutionMode.DEBATE
        )

        logger.info("=== Debate completado ===")
        logger.info(f"Resultado exitoso: {result.success}")

        # Verify that the agents used were the generic ones!
        used_agent_ids = {step.agent_name for step in result.steps if step.success}
        logger.info(f"Agentes que participaron: {sorted(used_agent_ids)}")
        assert all(agent.startswith("generic_") for agent in used_agent_ids), "No se usaron agentes genéricos!"
        logger.info("✅ Verificación: Se usaron agentes genéricos correctamente!")

        if result.debate:
            logger.info(f"Acuerdo: {result.debate.agreement_score}%")
            logger.info(f"Contradicciones: {result.debate.contradiction_score}%")
            if result.debate.final_response:
                logger.info("Síntesis final:")
                print("\n" + "-"*80)
                print(result.debate.final_response.get("synthesis", ""))
                print("-"*80 + "\n")

    except Exception as e:
        logger.exception(f"Error durante el debate: {e}")
    finally:
        supervisor.stop()


if __name__ == "__main__":
    asyncio.run(main())
