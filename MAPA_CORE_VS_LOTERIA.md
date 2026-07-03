# MAPA: Motor de Debate Genérico vs Lógica Específica Lotería/S.A.A.O.P.

Este documento mapea qué partes del sistema son el "motor de debate genérico" y cuáles son específicas del caso de uso Lotería/S.A.A.O.P.

## Leyenda
- **NO**: Lógica 100% genérica, reusable en cualquier dominio
- **SÍ**: Lógica 100% específica de Lotería/S.A.A.O.P.
- **PARCIAL**: Mezcla de ambos - contiene bloques específicos que deben extraerse

---

## Tabla de Análisis

| Ruta del archivo | Específico Lotería | Detalles |
|------------------|-------------------|----------|
| **core/** | | |
| core/base.py | NO | Contrato ABC genérico para componentes del sistema |
| core/debate.py | PARCIAL | DEBATE_PIPELINE_6_AGENTS movido a domains/loteria/config_loteria.py, patrones de contradicción específicos de lotería ("cazador", "espejo", "zonas") movidos a domains/loteria/debate_loteria.py, detect_cross_agent_contradiction() ahora acepta patrones adicionales como parámetro opcional, funciones como synthesize_final_response() son genéricas |
| core/evolution.py | ELIMINADO | Reemplazado por core/evolution_base.py (genérico) y domains/loteria/evolution_loteria.py (específico) |
| core/evolution_base.py | NO | **NUEVO** - Clase base genérica EvolutionManagerBase para cualquier sistema evolutivo (fases configurables, historial de agentes, ranking de herramientas, persistencia JSON, hooks para subclases) |
| core/herramientas.py | NO | Sistema genérico de herramientas compartidas (docstring generalizado, patrones de extracción genéricos en español) |
| core/memoria_perpetua.py | NO | Sistema genérico de memoria con ChromaDB, búsqueda vectorial y filtros de metadata arbitrarios; toda referencia a `sorteo` fue extraída al adaptador de Lotería |
| core/orchestration.py | NO | Modelos de datos genéricos (AgentStepResult, DebateResult, OrchestrationResult) |
| core/scoring.py | MOVIDO | Movido a domains/loteria/scoring.py (100% específico de Lotería) |
| core/supervisor.py | PARCIAL | BUNKER_EXPERT_MAPPING movido a domains/loteria/config_loteria.py, lógica de orquestación genérica, pero _execute_single_quantum_agent_async() usa scoring específico de lotería |
| **agents/** | | |
| agents/base.py | NO | Contrato ABC genérico para agentes |
| agents/manager.py | NO | Gestión genérica de agentes (carga JSON, registro, lifecycle) |
| agents/prompts.py | NO | Estructura genérica de construcción de prompts (docstring generalizado), prompts específicos movidos a domains/loteria/prompts_loteria.py |
| agents/loader.py | NO | Descubrimiento genérico de módulos de agentes |
| agents/llm_runner.py | NO | Runner genérico de LLM |
| agents/runtime_json_agent.py | NO | Implementación genérica de agente desde JSON |
| agents/result.py | NO | Modelos de resultado genéricos |
| agents/role_agent.py | NO | Agente con rol genérico |
| agents/roles.py | NO | Enum de roles genérico |
| **providers/** | | |
| providers/base.py | NO | Contrato ABC genérico para proveedores LLM |
| providers/registry.py | NO | Registro genérico de proveedores |
| providers/claude_provider.py | NO | Implementación genérica de proveedor Claude |
| providers/deepseek_provider.py | NO | Implementación genérica de proveedor DeepSeek |
| providers/gemini_provider.py | NO | Implementación genérica de proveedor Gemini |
| providers/groq_provider.py | NO | Implementación genérica de proveedor Groq |
| providers/nvidia_provider.py | NO | Implementación genérica de proveedor NVIDIA |
| providers/ollama_provider.py | NO | Implementación genérica de proveedor Ollama |
| providers/openai_provider.py | NO | Implementación genérica de proveedor OpenAI |
| providers/openrouter_provider.py | NO | Implementación genérica de proveedor OpenRouter |
| providers/classification.py | NO | Clasificación genérica de proveedores |
| **tools/** | | |
| tools/manager.py | NO | Gestión genérica de herramientas |
| tools/loader.py | NO | Descubrimiento genérico de módulos de herramientas |
| tools/uscore_calculator.py | MOVIDO | Movido a domains/loteria/uscore_calculator.py (100% específico de Lotería) |
| tools/cargar_memoria_desde_chat.py | NO | Utilidad genérica de carga de memoria |
| **memoria_agentes/** | | |
| memoria_agentes/*/memoria.json | NO | Datos específicos por agente, pero formato JSON genérico |
| **memory/** | | |
| memory/cargar_sorteos.py | MOVIDO | Movido a domains/loteria/cargar_sorteos.py (100% específico de Lotería) |
| memory/database.py | MOVIDO | Movido a domains/loteria/database_loteria.py (debates, intervenciones, U-Score, acuerdo y persistencia por sorteo) |
| **raíz/** | | |
| backtest_ciego.py | MOVIDO | Movido a domains/loteria/backtest_ciego.py (100% específico de Lotería) |
| lotoplus_completo_3511_3885.json | MOVIDO | Movido a domains/loteria/lotoplus_completo_3511_3885.json (datos específicos de Lotería) |
| **config.py** | PARCIAL | Variables genéricas de configuración (rutas, timeouts, proveedores) PERO variables específicas movidas a domains/loteria/config_loteria.py: DEFAULT_DEBATE_TASK, DEBATE_AGENTS, TRAINING_END/BLIND_TEST_START/LIVE_TEST_START/LIVE_TEST_END |
| **api.py** | PARCIAL | Endpoints genéricos de API REST PERO VALIDATION_AGENTS movido a domains/loteria/config_loteria.py (alias), SAAOP_TASK específico, límites de sistema TRAINING_END/BLIND_TEST_START/etc importados desde config_loteria.py, endpoints específicos de validación ciega con lógica de sorteos |
| **domains/loteria/** | | |
| domains/loteria/config_loteria.py | SÍ | **NUEVO** - Configuración específica de Lotería: DEBATE_AGENTS, DEFAULT_DEBATE_TASK, TRAINING_END/BLIND_TEST_START/LIVE_TEST_START/LIVE_TEST_END, BUNKER_EXPERT_MAPPING, VALIDATION_AGENTS (alias), DEBATE_PIPELINE_6_AGENTS |
| domains/loteria/debate_loteria.py | SÍ | **NUEVO** - Función get_loteria_contradiction_patterns() con patrones específicos de contradicción de zonas (CAZADOR/ESPEJO/PUENTE) |
| domains/loteria/prompts_loteria.py | SÍ | **NUEVO** - Prompts específicos: _analyst_prompt(), _analyst_reformulate_prompt(), _critic_prompt(), _optimizer_prompt() |
| domains/loteria/evolution_loteria.py | SÍ | **NUEVO** - EvolutionManagerLoteria hereda de EvolutionManagerBase e implementa toda la lógica específica de Lotería (fases entrenamiento/validacion_ciega/prediccion_en_vivo/operacional_real, límites de sorteos TRAINING_END/BLIND_TEST_START/etc, métricas aciertos_4/5/6, ranking de herramientas uScore/VER/CAZADOR/ESPEJO/PUENTE/ECLIPSE, pesos zonales Z1-Z9) |
| domains/loteria/scoring.py | SÍ | **MOVIDO** desde core/scoring.py - U-Score v2.1, zonas Z1-Z9, pesos zonales, patrones específicos de lotería (secuencias, divisores comunes, dígitos terminales, calendario), cálculo de rareza humana |
| domains/loteria/uscore_calculator.py | SÍ | **MOVIDO** desde tools/uscore_calculator.py - Calculadora U-Score v2.1, zonas Z1-Z9, histórico de Loto Plus (3511-3885), métricas específicas (IPN, PP, PZ, DSI, CD, SD) |
| domains/loteria/backtest_ciego.py | SÍ | **MOVIDO** desde raíz - Backtesting ciego específico de Lotería |
| domains/loteria/cargar_sorteos.py | SÍ | **MOVIDO** desde memory/ - Carga de sorteos específica de Lotería |
| domains/loteria/database_loteria.py | SÍ | **MOVIDO** desde memory/database.py - Persistencia SQLite de sorteos, debates, intervenciones y métricas de Lotería |
| domains/loteria/memoria_loteria.py | SÍ | **NUEVO** - Adaptador que conserva la API de Lotería y traduce `sorteo` a metadata genérica `{"sorteo": valor}` |
| domains/loteria/lotoplus_completo_3511_3885.json | SÍ | **MOVIDO** desde raíz - Datos históricos específicos de Loto Plus (3511-3885) |
| domains/loteria/agents/config/*.json | SÍ | **MOVIDOS** desde agents/config/ - Todos los prompts de sistema son 100% específicos de S.A.A.O.P.: |
| domains/loteria/agents/config/estadistico_integral.json | SÍ | Prompt específico defendiendo V19, framework S.A.A.O.P., CAZADOR/ESPEJO/PUENTE |
| domains/loteria/agents/config/gpt_auditor.json | SÍ | Prompt específico como destructor de hipótesis V19, auditor de S.A.A.O.P. |
| domains/loteria/agents/config/gemini_cuantico.json | SÍ | Prompt específico de explorador de zonas y densidad energética |
| domains/loteria/agents/config/viejo_lobo_rey.json | SÍ | Prompt específico de integrador humano con métrica de incomodidad visual |
| domains/loteria/agents/config/viejo_deepseek.json | SÍ | Prompt específico de árbitro matemático de S.A.A.O.P. |
| domains/loteria/agents/config/nuevo_deepseek_saaop.json | SÍ | Prompt específico de orquestador metodológico de IA_CORE/S.A.A.O.P. |
| domains/loteria/agents/papers/*.json | SÍ | **MOVIDOS** desde agents/papers/ - Todos los papers (identidad de agentes) son 100% específicos de S.A.A.O.P.: contienen términos como U-Score, CAZADOR, ESPEJO, cobertura combinatoria, framework V19 |
| domains/loteria/agents/papers/estadistico_integral_paper.json | SÍ | Paper específico con identidad, reglas y lecciones aprendidas del estadístico integral |
| domains/loteria/agents/papers/gpt_auditor_paper.json | SÍ | Paper específico con identidad, reglas y lecciones aprendidas del auditor |
| domains/loteria/agents/papers/gemini_cuantico_paper.json | SÍ | Paper específico con identidad, reglas y lecciones aprendidas del gemini cuántico |
| domains/loteria/agents/papers/viejo_lobo_rey_paper.json | SÍ | Paper específico con identidad, reglas y lecciones aprendidas del viejo lobo rey |
| domains/loteria/agents/papers/viejo_deepseek_paper.json | SÍ | Paper específico con identidad, reglas y lecciones aprendidas del viejo deepseek |
| domains/loteria/agents/papers/nuevo_deepseek_saaop_paper.json | SÍ | Paper específico con identidad, reglas y lecciones aprendidas del nuevo deepseek S.A.A.O.P. |

---

## Resumen por Categoría

### 100% Genérico (Reusable en cualquier dominio)
- core/base.py
- core/evolution_base.py (**NUEVO** - clase base genérica para sistemas evolutivos)
- core/memoria_perpetua.py
- core/orchestration.py
- agents/base.py
- agents/manager.py
- agents/loader.py
- agents/llm_runner.py
- agents/runtime_json_agent.py
- agents/result.py
- agents/role_agent.py
- agents/roles.py
- providers/* (todos)
- tools/manager.py
- tools/loader.py
- tools/cargar_memoria_desde_chat.py
- memoria_agentes/* (formato, no contenido)

### 100% Específico Lotería/S.A.A.O.P. (Movidos a domains/loteria/)
- domains/loteria/evolution_loteria.py (**NUEVO** - implementación específica de Lotería)
- domains/loteria/scoring.py (**MOVIDO** desde core/scoring.py)
- domains/loteria/uscore_calculator.py (**MOVIDO** desde tools/uscore_calculator.py)
- domains/loteria/backtest_ciego.py (**MOVIDO** desde raíz)
- domains/loteria/cargar_sorteos.py (**MOVIDO** desde memory/)
- domains/loteria/database_loteria.py (**MOVIDO** desde memory/)
- domains/loteria/memoria_loteria.py (**NUEVO** - adaptador de memoria para `sorteo`)
- domains/loteria/lotoplus_completo_3511_3885.json (**MOVIDO** desde raíz)
- domains/loteria/agents/config/*.json (**MOVIDOS** desde agents/config/)

### Parcial (Mezcla - requiere separación)
- core/debate.py
  - **COMPLETADO** - DEBATE_PIPELINE_6_AGENTS movido a domains/loteria/config_loteria.py
  - **COMPLETADO** - Patrones de contradicción específicos movidos a domains/loteria/debate_loteria.py
  - **COMPLETADO** - detect_cross_agent_contradiction() ahora acepta patrones adicionales como parámetro opcional
  - Mantener: detect_contradiction(), synthesize_final_response(), build_pipeline()
- core/herramientas.py
  - **COMPLETADO** - Docstring generalizado (eliminado "S.A.A.O.P.")
  - Mantener: sistema de registro y traducción de herramientas (patrones de extracción genéricos en español)
- core/supervisor.py
  - **COMPLETADO** - BUNKER_EXPERT_MAPPING movido a domains/loteria/config_loteria.py
  - Pendiente: lógica de scoring específica en _execute_single_quantum_agent_async()
  - Mantener: orquestación asíncrona, gestión de timeouts, persistencia
- agents/prompts.py
  - **COMPLETADO** - _analyst_prompt(), _analyst_reformulate_prompt(), _critic_prompt(), _optimizer_prompt() movidos a domains/loteria/prompts_loteria.py
  - **COMPLETADO** - Docstring generalizado (eliminado "LOTO PLUS WALK-FORWARD")
  - Mantener: build_role_prompt(), _format_previous_block(), _assistant_prompt()
- config.py
  - **COMPLETADO** - DEFAULT_DEBATE_TASK, DEBATE_AGENTS, límites de sorteos movidos a domains/loteria/config_loteria.py
  - Mantener: rutas, timeouts, configuración de proveedores
- api.py
  - **COMPLETADO** - VALIDATION_AGENTS movido a domains/loteria/config_loteria.py (alias)
  - Pendiente: SAAOP_TASK, endpoints de validación ciega
  - Mantener: estructura de API, endpoints genéricos de chat/debate

---

## Bloques Específicos a Extraer (Detalle)

### 1. core/debate.py
- **COMPLETADO** - DEBATE_PIPELINE_6_AGENTS movido a domains/loteria/config_loteria.py
- **COMPLETADO** - Patrones de contradicción específicos movidos a domains/loteria/debate_loteria.py
- **COMPLETADO** - detect_cross_agent_contradiction() modificado para aceptar patrones adicionales

### 2. core/evolution.py
- **COMPLETADO** - Archivo reemplazado por core/evolution_base.py (genérico) y domains/loteria/evolution_loteria.py (específico)
- core/evolution.py ELIMINADO

### 3. core/scoring.py
- **COMPLETADO** - Movido a domains/loteria/scoring.py
- U-Score v2.1 completo
- Zonas Z1-Z9
- Pesos zonales
- Patrones específicos de lotería

### 4. core/supervisor.py
- **COMPLETADO** - BUNKER_EXPERT_MAPPING movido a domains/loteria/config_loteria.py
- Pendiente: Inyección de contexto evolutivo específico
- Pendiente: Scoring específico en execute_single_quantum_agent_async y execute_debate_turn_async

### 5. config.py
- **COMPLETADO** - DEBATE_AGENTS movido a domains/loteria/config_loteria.py
- **COMPLETADO** - DEFAULT_DEBATE_TASK movido a domains/loteria/config_loteria.py
- **COMPLETADO** - Límites de sorteos movidos a domains/loteria/config_loteria.py

### 6. api.py
- **COMPLETADO** - VALIDATION_AGENTS movido a domains/loteria/config_loteria.py (alias)
- Pendiente: SAAOP_TASK
- Pendiente: Límites de sorteos (ya importados desde config_loteria.py)
- Pendiente: _run_validation_debate (completo)
- Pendiente: reveal_validation_result (lógica específica)

### 7. agents/prompts.py
- **COMPLETADO** - _analyst_prompt movido a domains/loteria/prompts_loteria.py
- **COMPLETADO** - _analyst_reformulate_prompt movido a domains/loteria/prompts_loteria.py
- **COMPLETADO** - _critic_prompt movido a domains/loteria/prompts_loteria.py
- **COMPLETADO** - _optimizer_prompt movido a domains/loteria/prompts_loteria.py

### 8. tools/uscore_calculator.py
- **COMPLETADO** - Movido a domains/loteria/uscore_calculator.py

### 9. agents/config/*.json
- **COMPLETADO** - Movidos a domains/loteria/agents/config/

### 10. Archivos adicionales movidos
- backtest_ciego.py → domains/loteria/backtest_ciego.py
- memory/cargar_sorteos.py → domains/loteria/cargar_sorteos.py
- memory/database.py → domains/loteria/database_loteria.py
- lotoplus_completo_3511_3885.json → domains/loteria/lotoplus_completo_3511_3885.json

### 11. Memoria vectorial
- **COMPLETADO** - `core/memoria_perpetua.py` acepta metadata arbitraria y ya no conoce el concepto `sorteo`
- **COMPLETADO** - `domains/loteria/memoria_loteria.py` traduce los parámetros históricos de Lotería a `{"sorteo": valor}`
