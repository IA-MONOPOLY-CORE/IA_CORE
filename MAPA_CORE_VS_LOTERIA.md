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
| core/debate.py | PARCIAL | Pipeline DEBATE_PIPELINE_6_AGENTS específico (líneas 46-66), patrones de contradicción específicos de lotería (líneas 124-139: "cazador", "espejo", "zonas"), pero funciones como detect_contradiction(), synthesize_final_response() son genéricas |
| core/evolution.py | SÍ | 100% específico - fases de entrenamiento/validación (líneas 20-25), límites de sorteos (TRAINING_END=3799, BLIND_TEST_START=3800, etc.), métricas específicas (aciertos_4, aciertos_5, aciertos_6), ranking de herramientas específicas (CAZADOR, ESPEJO, PUENTE, ECLIPSE) |
| core/herramientas.py | PARCIAL | Sistema genérico de herramientas compartidas, pero usa términos del dominio en ejemplos y patrones de extracción |
| core/memoria_perpetua.py | NO | Sistema genérico de memoria con ChromaDB y búsqueda vectorial |
| core/orchestration.py | NO | Modelos de datos genéricos (AgentStepResult, DebateResult, OrchestrationResult) |
| core/scoring.py | SÍ | 100% específico - U-Score v2.1, zonas Z1-Z9, pesos zonales, patrones específicos de lotería (secuencias, divisores comunes, dígitos terminales, calendario), cálculo de rareza humana |
| core/supervisor.py | PARCIAL | BUNKER_EXPERT_MAPPING específico (líneas 54-61: mapeo de roles a agentes S.A.A.O.P.), lógica de orquestación genérica, pero _execute_single_quantum_agent_async() usa scoring específico de lotería |
| **agents/** | | |
| agents/base.py | NO | Contrato ABC genérico para agentes |
| agents/manager.py | NO | Gestión genérica de agentes (carga JSON, registro, lifecycle) |
| agents/prompts.py | PARCIAL | Estructura genérica de construcción de prompts, pero prompts _analyst_prompt(), _critic_prompt(), _optimizer_prompt() son específicos de V19/Lotería |
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
| tools/uscore_calculator.py | SÍ | 100% específico - Calculadora U-Score v2.1, zonas Z1-Z9, histórico de Loto Plus (3511-3885), métricas específicas (IPN, PP, PZ, DSI, CD, SD) |
| tools/cargar_memoria_desde_chat.py | NO | Utilidad genérica de carga de memoria |
| **memoria_agentes/** | | |
| memoria_agentes/*/memoria.json | NO | Datos específicos por agente, pero formato JSON genérico |
| **config.py** | PARCIAL | Variables genéricas de configuración (rutas, timeouts, proveedores) PERO variables específicas: DEFAULT_DEBATE_TASK (líneas 181-190: tarea específica de CAZADOR/V19), DEBATE_AGENTS (líneas 171-178: lista específica de 6 agentes), TRAINING_END/BLIND_TEST_START/LIVE_TEST_START/LIVE_TEST_END (líneas 199-203: límites específicos de sorteos) |
| **api.py** | PARCIAL | Endpoints genéricos de API REST PERO VALIDATION_AGENTS (líneas 98-105: lista específica de 6 agentes), SAAOP_TASK (líneas 107-116: tarea específica), límites de sistema TRAINING_END/BLIND_TEST_START/etc (líneas 119-123), endpoints específicos de validación ciega con lógica de sorteos |
| **agents/config/*.json** | SÍ | Todos los prompts de sistema son 100% específicos de S.A.A.O.P.: |
| agents/config/estadistico_integral.json | SÍ | Prompt específico defendiendo V19, framework S.A.A.O.P., CAZADOR/ESPEJO/PUENTE |
| agents/config/gpt_auditor.json | SÍ | Prompt específico como destructor de hipótesis V19, auditor de S.A.A.O.P. |
| agents/config/gemini_cuantico.json | SÍ | Prompt específico de explorador de zonas y densidad energética |
| agents/config/viejo_lobo_rey.json | SÍ | Prompt específico de integrador humano con métrica de incomodidad visual |
| agents/config/viejo_deepseek.json | SÍ | Prompt específico de árbitro matemático de S.A.A.O.P. |
| agents/config/nuevo_deepseek_saaop.json | SÍ | Prompt específico de orquestador metodológico de IA_CORE/S.A.A.O.P. |

---

## Resumen por Categoría

### 100% Genérico (Reusable en cualquier dominio)
- core/base.py
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

### 100% Específico Lotería/S.A.A.O.P. (Debe extraerse)
- core/evolution.py
- core/scoring.py
- tools/uscore_calculator.py
- agents/config/*.json (todos los prompts)

### Parcial (Mezcla - requiere separación)
- core/debate.py
  - Extraer: DEBATE_PIPELINE_6_AGENTS, patrones de contradicción específicos
  - Mantener: detect_contradiction(), synthesize_final_response(), build_pipeline()
- core/herramientas.py
  - Extraer: patrones de extracción específicos del dominio
  - Mantener: sistema de registro y traducción de herramientas
- core/supervisor.py
  - Extraer: BUNKER_EXPERT_MAPPING, lógica de scoring específica
  - Mantener: orquestación asíncrona, gestión de timeouts, persistencia
- agents/prompts.py
  - Extraer: _analyst_prompt(), _critic_prompt(), _optimizer_prompt()
  - Mantener: build_role_prompt(), _format_previous_block()
- config.py
  - Extraer: DEFAULT_DEBATE_TASK, DEBATE_AGENTS, límites de sorteos
  - Mantener: rutas, timeouts, configuración de proveedores
- api.py
  - Extraer: VALIDATION_AGENTS, SAAOP_TASK, endpoints de validación ciega
  - Mantener: estructura de API, endpoints genéricos de chat/debate

---

## Bloques Específicos a Extraer (Detalle)

### 1. core/debate.py
- Líneas 46-66: DEBATE_PIPELINE_6_AGENTS (pipeline específico)
- Líneas 124-139: Patrones de contradicción específicos ("cazador", "espejo", "zonas")

### 2. core/evolution.py
- Archivo completo - mover a domain/loteria/evolution.py
- Todas las constantes de fases (TRAINING_END, BLIND_TEST_START, etc.)
- Toda la lógica de gestión de ciclo de 50 sorteos
- Ranking de herramientas específicas (CAZADOR, ESPEJO, PUENTE, ECLIPSE)

### 3. core/scoring.py
- Archivo completo - mover a domain/loteria/scoring.py
- U-Score v2.1 completo
- Zonas Z1-Z9
- Pesos zonales
- Patrones específicos de lotería

### 4. core/supervisor.py
- Líneas 54-61: BUNKER_EXPERT_MAPPING
- Líneas 431-435, 510-516: Inyección de contexto evolutivo específico
- Líneas 456-463, 547-554: Scoring específico en execute_single_quantum_agent_async y execute_debate_turn_async

### 5. config.py
- Líneas 171-178: DEBATE_AGENTS
- Líneas 181-190: DEFAULT_DEBATE_TASK
- Líneas 199-203: Límites de sorteos

### 6. api.py
- Líneas 98-105: VALIDATION_AGENTS
- Líneas 107-116: SAAOP_TASK
- Líneas 119-123: Límites de sorteos
- Líneas 235-335: _run_validation_debate (completo)
- Líneas 530-624: reveal_validation_result (lógica específica)

### 7. agents/prompts.py
- Líneas 64-94: _analyst_prompt
- Líneas 97-120: _analyst_reformulate_prompt
- Líneas 123-156: _critic_prompt
- Líneas 159-187: _optimizer_prompt

### 8. tools/uscore_calculator.py
- Archivo completo - mover a domain/loteria/uscore_calculator.py

### 9. agents/config/*.json
- Todos los archivos - mover a domain/loteria/agents/config/
