# Recuperación controlada de perfiles históricos

Prompt 18.6 audita identidades y perfiles históricos de dominios específicos para separar valor profesional reutilizable de nombres, prompts o lógicas demasiado atadas a un dominio particular.

No se copiaron prompts históricos. No se migraron textos largos de identidad vieja. Las recuperaciones globales fueron neutralizadas, profesionalizadas y reescritas como perfiles PASSED reutilizables.

## Fuentes Revisadas

- `domains/loteria/profile_catalog.json`
- `domains/loteria/agent_presets.json`
- `domains/loteria/agents/config/*.json`
- `domains/loteria/agents/papers/*.json`
- `catalogs/README.md`
- `docs/PROFESSIONAL_LIBRARY_DESIGN.md`
- `core/cerebro.md`
- `ui/web/index.html`

## Resumen De Clasificación

| Categoría | Cantidad |
|---|---:|
| `recuperar_como_global` | 5 |
| `mantener_como_dominio_especifico` | 6 |
| `legacy_no_selectable` | 9 |
| `ya_cubierto` | 12 |
| `descartar` | 6 |
| `backlog_documental` | 4 |

## Perfiles Recuperados Como Globales

| histórico | perfil global neutral |
|---|---|
| Analista de sesgos | `analista_sesgos_decision` |
| Integrador central | `integrador_sintesis_decisiones` |
| Simulador de escenarios / Visionario matemático | `simulador_escenarios_negocio` |
| Minimalista de señal | `minimalista_senal_ruido` |
| Historiador | `historiador_contexto_negocio` |

## Clasificación Detallada

| historical_id_or_name | fuente | descripción breve | estado actual | categoría_recomendada | motivo | equivalente_global_existente | acción_recomendada |
|---|---|---|---|---|---|---|---|
| Estadístico integral | `domains/loteria/profile_catalog.json`, `agent_presets.json`, configs/papers | Lectura estadística de datos históricos | Activo en dominio | `mantener_como_dominio_especifico` | Su forma histórica está ligada al dominio, aunque la función global ya existe | `analista_datos_negocio`, `especialista_bi_dashboards`, `modelador_metricas_kpis` | Mantener dominio; no duplicar global |
| Comparador de coberturas | `agent_presets.json` | Comparación homogénea de alternativas | Activo en dominio | `mantener_como_dominio_especifico` | La noción de cobertura conserva semántica específica | `analista_experimentos_ab_testing`, `evaluador_herramientas_software` | Mantener dominio |
| Cazador de anomalías | `profile_catalog.json`, `agent_presets.json` | Detección de rarezas y desviaciones | Activo en dominio | `mantener_como_dominio_especifico` | Nombre histórico útil localmente, globalmente ya está cubierto por detección operativa | `auditor_errores_sistemas`, `especialista_monitoreo_alertas`, `detector_fugas_rentabilidad` | Mantener dominio |
| Gestor de bankroll / exposición | `profile_catalog.json`, `agent_presets.json` | Control prudente de exposición | Activo en dominio | `mantener_como_dominio_especifico` | La noción de bankroll es específica; el riesgo global ya está cubierto | `analista_riesgo_tecnico_operativo`, `analista_riesgo_legal_preventivo`, `especialista_continuidad_operativa` | Mantener dominio |
| Administrador prudente | `profile_catalog.json`, `agent_presets.json` | Administración cautelosa de recursos | Activo en dominio | `mantener_como_dominio_especifico` | Valor local, pero globalmente se reparte entre finanzas y riesgo | `planificador_financiero_operativo`, `controlador_presupuesto` | Mantener dominio |
| Archivista de trazabilidad | `profile_catalog.json`, `agent_presets.json`, papers | Archivo documental y trazabilidad | Activo en dominio | `mantener_como_dominio_especifico` | Trazabilidad histórica local; la función global ya existe | `especialista_base_conocimiento`, `gestor_documentacion_administrativa`, `historiador_contexto_negocio` | Mantener dominio |
| Analista de sesgos | `agent_presets.json`, `profile_catalog.json`, docs | Detección de sesgos de selección/decisión | Activo parcial en dominio | `recuperar_como_global` | Aporta capacidad transversal no suficientemente explícita como perfil global | `critico` + `deteccion_sesgos` | Recuperado como `analista_sesgos_decision` |
| Integrador central | `agent_presets.json`, `profile_catalog.json`, docs | Integración de criterios y cierre trazable | Activo en dominio | `recuperar_como_global` | La función de síntesis multicriterio aporta valor transversal | `integrador_central` + `sintesis_multicriterio` | Recuperado como `integrador_sintesis_decisiones` |
| Simulador de escenarios / Visionario matemático | `agent_presets.json`, configs/papers, docs | Exploración de escenarios bajo supuestos | Activo en dominio | `recuperar_como_global` | Simulación neutral de escenarios de negocio faltaba como perfil explícito | `simulador` + `simulacion_escenarios` | Recuperado como `simulador_escenarios_negocio` |
| Minimalista de señal | docs, `ui/web/index.html` | Separación señal/ruido y reducción de complejidad | Documental/no formal | `recuperar_como_global` | Aporta foco operativo transversal en reporting y decisión | Parcial en `especialista_reporting_operativo` | Recuperado como `minimalista_senal_ruido` |
| Historiador | docs | Recuperación de contexto y antecedentes | Documental/no formal | `recuperar_como_global` | Falta perfil explícito de memoria contextual de negocio | Parcial en archivistas existentes | Recuperado como `historiador_contexto_negocio` |
| Lectura de patrones | `profile_catalog.json` | Detección de recurrencias | Inactivo/no seleccionable | `legacy_no_selectable` | Sin preset operativo histórico; función cubierta por análisis de patrones | `analista_segmentacion_clientes`, `analista_satisfaccion_cliente` | Mantener inactivo local |
| Explorador de hipótesis | `profile_catalog.json` | Comparación de decisiones alternativas | Inactivo/no seleccionable | `legacy_no_selectable` | Sin preset operativo; cubierto por experimentación y validación | `analista_experimentos_ab_testing` | Mantener inactivo local |
| Modelador de cobertura | `profile_catalog.json` | Evaluación de límites de cobertura | Inactivo/no seleccionable | `legacy_no_selectable` | Semántica muy local | Parcial en `simulador_escenarios_negocio` | Mantener inactivo local |
| Auditor de exposición | `profile_catalog.json` | Riesgo de sobreinterpretar señales débiles | Inactivo/no seleccionable | `legacy_no_selectable` | Cubierto por riesgo y auditoría global | `analista_riesgo_legal_preventivo`, `analista_riesgo_tecnico_operativo` | Mantener inactivo local |
| Control de riesgo operativo | `profile_catalog.json` | Control de riesgo operativo | Inactivo/no seleccionable | `legacy_no_selectable` | Ya hay perfiles globales de riesgo/control | `especialista_continuidad_operativa`, `controlador_cumplimiento_sops` | Mantener inactivo local |
| Priorizador de riesgos | `profile_catalog.json` | Ordenamiento de riesgos | Inactivo/no seleccionable | `legacy_no_selectable` | Cubierto por perfiles de riesgo | `analista_riesgo_legal_preventivo` | Mantener inactivo local |
| Cierre de jugada | `profile_catalog.json` | Cierre de decisión local | Inactivo/no seleccionable | `legacy_no_selectable` | Nombre y función ligados a dominio | `integrador_sintesis_decisiones` | Mantener inactivo local |
| Validador de datos | `profile_catalog.json` | Validación de datos | Inactivo/no seleccionable | `legacy_no_selectable` | Cubierto ampliamente por data quality | `analista_calidad_datos` | Mantener inactivo local |
| Validador de aprendizaje | `profile_catalog.json` | Validación de aprendizaje posterior | Inactivo/no seleccionable | `legacy_no_selectable` | Falta madurez para global propio | `analista_experimentos_ab_testing` | Mantener inactivo local |
| Auditor hostil | `agent_presets.json`, configs/papers, docs | Auditoría crítica fuerte | Activo en dominio | `ya_cubierto` | La capacidad existe globalmente como auditoría y crítica | `auditor_procesos_negocio`, `auditor_dashboards_metricas`, `analista_sesgos_decision` | No duplicar |
| Destructor de hipótesis | `profile_catalog.json`, docs | Refutación agresiva de hipótesis | Inactivo/no seleccionable | `ya_cubierto` | La refutación útil ya está cubierta sin nombre agresivo | `analista_sesgos_decision`, `tester_funcional_negocio` | No recuperar nombre |
| Crítico de viabilidad | `profile_catalog.json` | Validación de viabilidad | Inactivo/no seleccionable | `ya_cubierto` | Cubierto por validación, riesgo y planificación | `consultor_modelo_negocio`, `especialista_continuidad_operativa` | No duplicar |
| Detector de patrones | docs | Lectura de patrones | Documental/no formal | `ya_cubierto` | Ya existen roles/especializaciones y perfiles de análisis | `analista_segmentacion_clientes`, `analista_satisfaccion_cliente` | No agregar |
| Observador conductual | docs, `catalogs/roles.json` | Observación de fricciones y conducta | Role global existente | `ya_cubierto` | Existe role global y perfiles de clientes cubren uso práctico | `analista_segmentacion_clientes`, `analista_satisfaccion_cliente` | No agregar |
| Experimentalista | docs | Prueba de hipótesis/experimentos | Documental/no formal | `ya_cubierto` | Ya cubierto por experimentación A/B | `analista_experimentos_ab_testing` | No agregar |
| Analista temporal | `agent_presets.json`, docs | Lectura de ventanas temporales | Activo en dominio | `ya_cubierto` | Globalmente cubierto por análisis temporal y caja/tendencias | `analista_flujo_caja`, `analista_experimentos_ab_testing` | No duplicar |
| Arquitecto de sistemas | docs, `catalogs/roles.json` | Arquitectura técnica | Role global existente | `ya_cubierto` | Ya hay perfiles técnicos específicos | `arquitecto_datos_negocio`, `especialista_integraciones_api`, `administrador_sistemas_internos` | No agregar |
| Visionario matemático | docs, presets | Simulación y escenarios | Activo en dominio | `ya_cubierto` | Recuperado mediante perfil neutral de simulación | `simulador_escenarios_negocio` | Mantener histórico local |
| Psicología de masas | docs, UI histórica | Conducta colectiva | Documental/no formal | `ya_cubierto` | Cubierto sin nombre especulativo por observación/segmentación | `analista_segmentacion_clientes`, `analista_satisfaccion_cliente` | No agregar |
| Integrador de criterios | `profile_catalog.json` | Integración de criterios | Inactivo/no seleccionable | `ya_cubierto` | Recuperado en síntesis de decisiones | `integrador_sintesis_decisiones` | No agregar separado |
| Síntesis multicriterio | `profile_catalog.json` | Síntesis de múltiples criterios | Inactivo/no seleccionable | `ya_cubierto` | Es la especialización usada por perfil recuperado | `integrador_sintesis_decisiones` | No agregar separado |
| Intuitivo obsesivo | docs | Intuición intensa/persistente | Documental/no formal | `backlog_documental` | Podría traducirse a exploración, pero falta utilidad operativa clara | Sin equivalente directo | Dejar para auditoría futura |
| Persistente metódico | docs | Persistencia de método | Documental/no formal | `backlog_documental` | Podría aportar disciplina de seguimiento, pero se solapa con operaciones | Parcial en coordinadores/planificadores | No activar ahora |
| Geómetra | docs, UI histórica | Lectura geométrica/espacial | Documental/no formal | `backlog_documental` | Demasiado específico sin área/nicho global claro por ahora | Sin equivalente directo | Mantener documental |
| Competidor estratégico | docs | Lectura competitiva | Documental/no formal | `backlog_documental` | Puede aportar, pero ya hay estrategia comercial y competidores | `analista_oportunidades_locales`, `estratega_negocio_digital` | Revisar en auditoría 18.7 |
| Místico / simbólico | docs | Lectura simbólica | Documental/no formal | `descartar` | Decorativo y sin utilidad económica verificable | No aplica | No recuperar |
| Intuitivo caótico | docs, UI histórica | Intuición no estructurada | Documental/no formal | `descartar` | Ambiguo y difícil de validar | No aplica | No recuperar |
| Antisistema | docs, UI histórica | Postura contraria al sistema | Documental/no formal | `descartar` | Nombre ideológico/decorativo; riesgo de sesgo | No aplica | No recuperar |
| Apostador profesional | docs | Gestión de apuesta | Documental/no formal | `descartar` | Demasiado atado a dominio y potencialmente riesgoso | `gestor_exposicion` local | No recuperar global |
| Jugador obsesivo | docs | Conducta obsesiva de juego | Documental/no formal | `descartar` | No debe convertirse en perfil operativo | No aplica | No recuperar |
| Hipercontrolado | docs | Control excesivo | Documental/no formal | `descartar` | Rasgo psicológico, no función profesional clara | No aplica | No recuperar |

## Decisión Final

Se recuperaron 5 perfiles globales porque aportan cobertura transversal no expresada con suficiente claridad en los 95 perfiles actuales. El resto queda cubierto por perfiles existentes, mantenido como dominio específico, legado no seleccionable, descartado o en backlog documental.

El catálogo global conserva neutralidad: no absorbe identidades crudas, no copia prompts viejos y no convierte un dominio específico en centro del sistema.
