# MAPA: Motor de Debate Genérico vs Lógica Específica Lotería/S.A.A.O.P.

Este documento mapea qué partes del sistema son el "motor de debate genérico" y cuáles son específicas del caso de uso Lotería/S.A.A.O.P.

## Estado verificado al 4 de julio de 2026

- **Paso 5 — COMPLETADO:** los seis papers de identidad se movieron de `agents/papers/` a `domains/loteria/agents/papers/`. La resolución activa ya no depende de una constante global de Lotería: los flujos genéricos usan `core/domain_registry.py` para resolver `domains/<dominio>/agents/config/`, `papers/` y `memory_sources/` por `domain_id`. `config.AGENTS_PAPERS_DIR` queda solo como compatibilidad legacy/default Lotería.
- **Paso 6 — COMPLETADO:** la memoria vectorial genérica permanece en `core/memoria_perpetua.py` y almacena metadata arbitraria en `memoria_vectorial/`; `domains/loteria/memoria_loteria.py` adapta el concepto `sorteo`. La persistencia SQL específica quedó en `domains/loteria/database_loteria.py`, con la base `domains/loteria/loto_plus.db`; `memory/database.py` fue eliminado.
- **Paso 8 — COMPLETADO:** `SAAOP_TASK` se define en `domains/loteria/config_loteria.py` y la ejecución/revelación de validación ciega vive en `domains/loteria/validation_loteria.py`. `api.py` conserva únicamente los endpoints/fachada y carga el dominio de forma perezosa; si Lotería no está disponible responde `501`.
- **Paso 9 — COMPLETADO:** `analyst`, `assistant`, `critic` y `optimizer` se identifican con `AGENT_IS_GENERIC_BASELINE = True`; `AgentManager` conserva esa clasificación, `/api/agents/list` publica `is_generic_baseline` y `ui/web/index.html` muestra dos grupos: **Agentes base (demo) [4]** y **Agentes S.A.A.O.P. [6]**.
- **Interfaz — COMPLETADO:** `ui/web/`, servido por FastAPI, es la única interfaz de usuario del proyecto; la estructura auxiliar de la interfaz anterior ya no existe.

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
| core/domain_registry.py | NO | Registro y resolución genérica de dominios: lee `domain.json`, crea dominios, resuelve carpetas de agentes/config/papers/memory_sources por `domain_id`, carga/valida `domains/<domain_id>/profile_catalog.json` y detecta ambigüedad de IDs de agente entre dominios |
| core/orchestration.py | NO | Modelos de datos genéricos (AgentStepResult, DebateResult, OrchestrationResult) |
| core/scoring.py | MOVIDO | Movido a domains/loteria/scoring.py (100% específico de Lotería) |
| core/supervisor.py | PARCIAL | La evolución, el pipeline, el mapeo de expertos y las funciones de scoring se inyectan por constructor; ya no hay scoring rígido en los ejecutores. Conserva fallbacks perezosos hacia Lotería por compatibilidad, textos S.A.A.O.P. y extracción de combinaciones 0-50, por lo que aún no es 100% agnóstico |
| **agents/** | | |
| agents/base.py | NO | Contrato ABC genérico para agentes |
| agents/manager.py | NO | Gestión genérica de agentes (carga JSON, registro, lifecycle) y registro de IDs marcados como baseline genérico |
| agents/prompts.py | PARCIAL | Conserva helpers genéricos, pero todavía importa directamente los prompts de `domains/loteria/prompts_loteria.py` |
| agents/loader.py | NO | Descubrimiento genérico de módulos y lectura opcional de `AGENT_IS_GENERIC_BASELINE` |
| agents/modules/{analyst,assistant,critic,optimizer}.py | NO | Agentes base reutilizables, identificados con `AGENT_IS_GENERIC_BASELINE = True` para diferenciarlos de los agentes reales del dominio |
| agents/llm_runner.py | NO | Runner genérico de LLM |
| agents/runtime_json_agent.py | PARCIAL | Implementación de agente desde JSON y carga de papers por ruta configurable; la integración de memoria aún usa directamente `domains/loteria/memoria_loteria.py` |
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
| **api.py** | PARCIAL | API REST genérica con fachada opcional de Lotería: carga perezosamente `SAAOP_TASK`, límites y funciones de validación desde `domains/loteria/`, devuelve `501` sin ese dominio y publica `is_generic_baseline` en `/api/agents/list`. La lógica de negocio de validación ciega ya no reside aquí |
| **domains/loteria/** | | |
| domains/loteria/profile_catalog.json | SÍ | Catálogo de perfiles habilitados para Lotería: mapea perfiles profesionalizados de S.A.A.O.P. a roles y especializaciones globales, y declara `role_groups` para sus capas operativas sin convertirlas en default del Core |
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
| domains/loteria/loto_plus.db | SÍ | Base SQLite específica regenerada desde el histórico JSON y ubicada junto al dominio |
| domains/loteria/lotoplus_completo_3511_3885.json | SÍ | **MOVIDO** desde raíz - Datos históricos específicos de Loto Plus (3511-3885) |
| domains/loteria/validation_loteria.py | SÍ | **NUEVO** - Lógica específica de validación ciega y revelación de resultados: run_validation_debate(), reveal_validation_result() y _extraer_numeros_de_respuesta() |
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
| **ui/** | | |
| ui/web/ | PARCIAL | Única interfaz de usuario vigente: HUD HTML/CSS/JavaScript servido por FastAPI; combina paneles genéricos con presentación y agentes S.A.A.O.P. Crear Agente consume `GET /api/domains/{domain_id}/profile-catalog` para roles/especializaciones del dominio seleccionado, renderiza `role_groups` como grupos visuales cuando existen y usa fallback global/legacy si el dominio no tiene catálogo |
| ui/app.py e interfaz anterior | ELIMINADO | Sus paneles, componentes, estado, traducciones y dependencias específicas fueron retirados completamente |
| **tests/** | | |
| tests/test_no_hardcoded_agent_paths.py | NO | Test anti-regresión que escanea Core, agentes, proveedores, dominios, UI y archivos Python raíz para impedir que reaparezcan rutas hardcodeadas como `agents/config`, `ROOT / "domains" / "loteria"` o `domain_id == config.DEFAULT_DOMAIN_ID` en flujos genéricos; obliga a usar resolvers por dominio |

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
- domains/loteria/validation_loteria.py (**NUEVO** - ejecución y revelación de validación ciega)
- domains/loteria/lotoplus_completo_3511_3885.json (**MOVIDO** desde raíz)
- domains/loteria/loto_plus.db (SQLite específica del dominio)
- domains/loteria/agents/config/*.json (**MOVIDOS** desde agents/config/)
- domains/loteria/agents/papers/*.json (**MOVIDOS** desde agents/papers/)

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
  - **COMPLETADO** - EvolutionManager, pipeline, expertos y funciones de scoring se reciben por inyección
  - **RESIDUAL** - Fallbacks perezosos a Lotería, texto S.A.A.O.P. y extracción numérica 0-50 permanecen por compatibilidad
  - Mantener: orquestación asíncrona, gestión de timeouts, persistencia
- agents/prompts.py
  - **COMPLETADO** - _analyst_prompt(), _analyst_reformulate_prompt(), _critic_prompt(), _optimizer_prompt() movidos a domains/loteria/prompts_loteria.py
  - **COMPLETADO** - Docstring generalizado (eliminado "LOTO PLUS WALK-FORWARD")
  - **RESIDUAL** - `build_role_prompt()` todavía importa directamente los prompts del dominio Lotería
  - Mantener: _format_previous_block(), _assistant_prompt()
- agents/runtime_json_agent.py
  - **COMPLETADO** - Papers resueltos de forma relativa al JSON del agente (`domains/<dominio>/agents/papers/`), sin asumir Lotería
  - **RESIDUAL** - La memoria vectorial se obtiene directamente desde `domains/loteria/memoria_loteria.py`
- config.py
  - **COMPLETADO** - DEFAULT_DEBATE_TASK, DEBATE_AGENTS, límites de sorteos movidos a domains/loteria/config_loteria.py
  - Mantener: rutas, timeouts, configuración de proveedores
- api.py
  - **COMPLETADO** - VALIDATION_AGENTS movido a domains/loteria/config_loteria.py (alias)
  - **COMPLETADO** - SAAOP_TASK movido a domains/loteria/config_loteria.py (alias de DEFAULT_DEBATE_TASK)
  - **COMPLETADO** - Límites de sorteos (TRAINING_END, BLIND_TEST_START, etc.) importados desde config_loteria.py
  - **COMPLETADO** - _run_validation_debate y reveal_validation_result movidos a domains/loteria/validation_loteria.py
  - **COMPLETADO** - Lazy imports para funciones de validación, devolviendo 501 si el dominio lotería no está disponible
  - Mantener: estructura de API, endpoints genéricos de chat/debate y endpoints-fachada opcionales del dominio
- ui/web/
  - **COMPLETADO** - Absorbió las capacidades operativas de la interfaz anterior
  - **COMPLETADO** - Selector de agentes dividido en baseline genérico y agentes reales S.A.A.O.P.

---

## Estado de extracción por componente

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
- **COMPLETADO** - Contexto evolutivo desacoplado mediante `evolution_manager_class`
- **COMPLETADO** - Scoring desacoplado mediante `score_response_fn` y `build_scores_summary_fn`; ambos ejecutores usan las funciones inyectadas
- **RESIDUAL** - Los defaults perezosos siguen apuntando a Lotería para compatibilidad y quedan textos/formato numérico específicos dentro del supervisor

### 5. config.py
- **COMPLETADO** - DEBATE_AGENTS movido a domains/loteria/config_loteria.py
- **COMPLETADO** - DEFAULT_DEBATE_TASK movido a domains/loteria/config_loteria.py
- **COMPLETADO** - Límites de sorteos movidos a domains/loteria/config_loteria.py

### 6. api.py
- **COMPLETADO** - VALIDATION_AGENTS movido a domains/loteria/config_loteria.py (alias)
- **COMPLETADO** - SAAOP_TASK movido a domains/loteria/config_loteria.py (alias de DEFAULT_DEBATE_TASK)
- **COMPLETADO** - Límites de sorteos importados desde config_loteria.py
- **COMPLETADO** - _run_validation_debate movido a domains/loteria/validation_loteria.py
- **COMPLETADO** - reveal_validation_result movido a domains/loteria/validation_loteria.py
- **COMPLETADO** - Lazy imports para funciones de validación con fallback a 501 Not Implemented

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

### 12. Papers de agentes
- **COMPLETADO** - `agents/papers/` dejó de ser la ubicación activa
- **COMPLETADO** - Los seis papers S.A.A.O.P. residen en `domains/loteria/agents/papers/`
- **COMPLETADO** - Los flujos genéricos usan `core/domain_registry.py` para resolver `agents/config`, `agents/papers` y `agents/memory_sources` por dominio; `config.AGENTS_PAPERS_DIR` queda como compatibilidad legacy/default Lotería

### 13. Validación ciega y tarea por defecto
- **COMPLETADO** - `SAAOP_TASK` se define en `domains/loteria/config_loteria.py`
- **COMPLETADO** - `run_validation_debate()` y `reveal_validation_result()` residen en `domains/loteria/validation_loteria.py`
- **COMPLETADO** - `api.py` funciona como fachada con carga perezosa y respuesta `501` cuando el dominio no está instalado

### 14. Clasificación de agentes
- **COMPLETADO** - Los cuatro agentes base declaran `AGENT_IS_GENERIC_BASELINE = True`
- **COMPLETADO** - `agents/loader.py` y `agents/manager.py` propagan la clasificación hasta `/api/agents/list`
- **COMPLETADO** - El HUD conserva los diez agentes y los renderiza en grupos de 4 baseline/demo y 6 S.A.A.O.P.
- **COMPLETADO** - `tests/test_api_admin_panels.py` cubre el contrato del endpoint y evita que el frontend descarte el flag

### 15. Interfaz de usuario
- **COMPLETADO** - La interfaz anterior y toda su estructura auxiliar fueron eliminadas
- **COMPLETADO** - `ui/web/` es la única interfaz y concentra agentes, proveedores, memoria, logs, modo híbrido, orquestación y overview
