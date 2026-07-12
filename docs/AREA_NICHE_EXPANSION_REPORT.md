# Reporte de Expansión de Áreas y Nichos Profesionales

**Estado**: Propuesto (Prompt 17)
**Fecha**: 2026-07-10
**HEAD**: b421ff1

## Propósito del Reporte

Este reporte define el universo objetivo de áreas y nichos profesionales para IA_CORE, sin límites artificiales de cantidad por área, con trazabilidad explícita hacia perfiles profesionales, presets, paper seeds, políticas de modelo y equipos. El objetivo es preparar la estructura necesaria para que Prompt 18 pueda crear perfiles profesionales de forma sistemática y operativa.

## Estado Actual de Áreas/Nichos

### Auditoría Real

- **Áreas actuales**: 30 (catalogs/areas.json)
- **Nichos actuales**: 200 (catalogs/niches.json)
- **Promedio de nichos por área**: 6.7
- **Áreas con más nichos**: 2 áreas con 13 nichos cada una
- **Área con menos nichos**: 1 área con 4 nichos

### Distribución por Área

**Áreas con mayor cobertura**:
- administracion_contabilidad_finanzas: 13
- marketing_publicidad: 13
- comercial_ventas_negocios: 12
- automatizacion_integraciones: 9
- customer_success_experiencia_cliente: 9
- datos_bi_analytics: 9
- gerencia_direccion_general: 9
- tecnologia_sistemas_telecomunicaciones: 9
- legales: 8

**Áreas con menor cobertura actual**:
- oficios_otros: 4
- salud_medicina_farmacia: 5
- ingenierias: 5
- ingenieria_civil_construccion: 5
- departamento_tecnico: 5
- secretarias_recepcion: 5
- diseno: 5
- mineria_petroleo_gas: 5
- aduana_comercio_exterior: 5
- seguros: 5
- comunicacion_relaciones_institucionales_publicas: 5
- sociologia_trabajo_social: 5
- enfermeria: 5
- naviero_maritimo_portuario: 5

### Nichos Específicos Detectados

- **Nichos específicos de Lotería**: 1 (analisis_loteria_juegos_azar en oficios_otros)
- **Nichos duplicados o parecidos**: No detectados
- **Nichos útiles para empresa digital**: Cubiertos progresivamente en tecnología, automatización, producto, datos, marketing, ventas, finanzas, customer success, legal básico y gestión operativa

### Diagnóstico de Cobertura Actual

**Estado post Tanda 2B**:
- El catálogo llegó al objetivo operativo de 30 áreas y 200 nichos PASSED.
- Todas las áreas tienen al menos 4 nichos activos y la mayoría tiene 5 o más.
- Las áreas transversales de empresa digital, pymes, operaciones, datos, marketing, ventas, finanzas, customer success, legal básico y gestión de proyectos ya tienen cobertura suficiente para iniciar Prompt 18.

**Brechas residuales para etapas posteriores**:
- Data engineering, seguridad avanzada, AI/ML engineering y compliance sectorial específico requieren perfiles/model policies más especializados.
- Nichos verticales por país, regulación o industria deben cargarse más adelante para evitar catálogos fantasma.
- PMO enterprise, gestión de portafolios y operaciones complejas pueden esperar hasta tener perfiles profesionales definidos.

## Criterio de Diseño

### Principios de Expansión

1. **Sin límite fijo por área**: Cada área tiene tantos nichos como necesite para cubrir su especialización real
2. **Trazabilidad operativa**: Todo nicho debe poder conectarse a perfiles profesionales, presets, papers y políticas de modelo
3. **Status explícito**: proposed/draft/active/deprecated para controlar el ciclo de vida
4. **Contrato de operacionalización**: Cada nicho define claramente qué necesita para volverse usable
5. **Priorización por valor de negocio**: Nichos críticos para empresa digital tienen prioridad alta
6. **Reutilización por dominio**: Nichos globales reusables por múltiples dominios
7. **Evolución incremental**: No se cargan cientos de nichos sin validación previa

### Regla No Negociable

Todo perfil profesional usable debe tener:
- preset_seed
- paper_seed
- default_model_policy
- role_id
- specialization_id
- status: active

Si no tiene eso, no puede ser usable ni seleccionable. Debe quedar como draft/disabled/proposed.

## Universo Objetivo Propuesto

### Áreas Propuestas (30 áreas objetivo)

**Áreas existentes a mantener**:
1. comercial_ventas_negocios
2. administracion_contabilidad_finanzas
3. tecnologia_sistemas_telecomunicaciones
4. atencion_cliente_call_center_telemarketing
5. marketing_publicidad
6. legales
7. educacion_docencia_investigacion
8. recursos_humanos_capacitacion
9. gerencia_direccion_general
10. diseno

**Áreas nuevas propuestas**:
11. estrategia_direccion_ejecutiva
12. producto_experiencia_usuario
13. operaciones_procesos
14. automatizacion_sistemas
15. datos_inteligencia_negocio
16. inversion_activos
17. contenido_comunicacion
18. comunidad_soporte
19. investigacion_innovacion
20. tecnologia_desarrollo
21. creatividad_diseno
22. gestion_conocimiento
23. calidad_mejora_continua
24. seguridad_informacion
25. integraciones_apis
26. inteligencia_artificial_aplicada
27. supply_logistica
28. gestion_comercial
29. administracion_backoffice
30. customer_success

### Nichos Propuestos por Área (200 nichos objetivo)

#### 1. estrategia_direccion_ejecutiva (12 nichos)

**Nichos propuestos**:
- estrategia_corporativa
- transformacion_digital
- gobierno_datos
- gestion_portafolio
- m_a_integraciones_post
- board_ejecutivo
- estrategia_riesgo
- planificacion_estrategica
- kpi_ejecutivos
- comunicacion_externa
- relaciones_inversores
- sucesion_liderazgo

**expected_profile_types**:
- executive_strategy_advisor
- transformation_lead
- portfolio_manager
- m_a_integrator
- board_advisor
- risk_strategist
- kpi_analyst
- communications_director
- investor_relations_specialist
- leadership_developer

**model_policy_need**: cloud_preferred (razonamiento alto, decisiones críticas)

**complexity**: high/critical

#### 2. producto_experiencia_usuario (10 nichos)

**Nichos propuestos**:
- product_management
- product_discovery
- product_growth
- ux_research
- ux_design
- product_analytics
- product_operations
- roadmap_strategy
- feature_prioritization
- user_journey_mapping

**expected_profile_types**:
- product_manager
- product_discovery_specialist
- growth_product_manager
- ux_researcher
- ux_designer
- product_analyst
- product_ops_specialist
- roadmap_strategist
- prioritization_framework_specialist
- journey_mapping_specialist

**model_policy_need**: cloud_preferred (análisis complejo, síntesis)

**complexity**: medium/high

#### 3. operaciones_procesos (8 nichos)

**Nichos propuestos**:
- process_optimization
- operations_management
- workflow_automation
- process_documentation
- quality_operations
- capacity_planning
- service_delivery
- sla_management

**expected_profile_types**:
- operations_manager
- process_optimization_specialist
- workflow_designer
- process_documenter
- quality_ops_analyst
- capacity_planner
- service_delivery_manager
- sla_specialist

**model_policy_need**: auto/local_ok (operativo, documental)

**complexity**: medium

#### 4. automatizacion_sistemas (10 nichos)

**Nichos propuestos**:
- automation_architecture
- rpa_automation
- api_automation
- workflow_orchestration
- integration_patterns
- automation_governance
- low_code_platforms
- script_development
- automation_testing
- monitoring_automation

**expected_profile_types**:
- automation_architect
- rpa_developer
- api_integration_specialist
- workflow_orchestrator
- integration_architect
- automation_governance_specialist
- low_code_developer
- script_developer
- automation_qa_engineer
- monitoring_automation_specialist

**model_policy_need**: cloud_preferred (razonamiento técnico complejo)

**complexity**: high

#### 5. datos_inteligencia_negocio (12 nichos)

**Nichos propuestos**:
- data_engineering
- data_warehouse
- data_lakes
- bi_analytics
- business_intelligence
- data_governance
- data_quality
- data_catalog
- forecasting_analytics
- predictive_analytics
- data_visualization
- self_service_bi

**expected_profile_types**:
- data_engineer
- data_warehouse_architect
- data_lake_specialist
- bi_analyst
- business_intelligence_developer
- data_governance_specialist
- data_quality_analyst
- data_catalog_manager
- forecasting_specialist
- predictive_modeler
- data_visualization_specialist
- self_service_bi_specialist

**model_policy_need**: cloud_preferred (procesamiento datos complejo)

**complexity**: high

#### 6. inversion_activos (6 nichos)

**Nichos propuestos**:
- portfolio_management
- asset_allocation
- risk_management
- performance_analytics
- investment_research
- compliance_investment

**expected_profile_types**:
- portfolio_manager
- asset_allocation_specialist
- investment_risk_analyst
- performance_analyst
- investment_researcher
- investment_compliance_specialist

**model_policy_need**: cloud_required (finanzas críticas, precisión)

**complexity**: critical

#### 7. contenido_comunicacion (8 nichos)

**Nichos propuestos**:
- content_strategy
- content_creation
- content_marketing
- copywriting
- editorial_calendar
- content_seo
- content_localization
- brand_storytelling

**expected_profile_types**:
- content_strategist
- content_creator
- content_marketing_specialist
- copywriter
- editorial_calendar_manager
- seo_content_specialist
- localization_specialist
- brand_storyteller

**model_policy_need**: auto (creatividad, generación texto)

**complexity**: medium

#### 8. comunidad_soporte (8 nichos)

**Nichos propuestos**:
- community_management
- customer_support
- technical_support
- support_automation
- community_engagement
- user_advocacy
- support_analytics
- knowledge_base

**expected_profile_types**:
- community_manager
- customer_support_lead
- technical_support_specialist
- support_automation_specialist
- community_engagement_specialist
- user_advocate
- support_analyst
- knowledge_base_manager

**model_policy_need**: auto/local_ok (interacción, documentación)

**complexity**: medium

#### 9. investigacion_innovacion (6 nichos)

**Nichos propuestos**:
- market_research
- competitive_intelligence
- innovation_strategy
- r_d_management
- patent_research
- trend_analysis

**expected_profile_types**:
- market_researcher
- competitive_intelligence_analyst
- innovation_strategist
- r_d_manager
- patent_researcher
- trend_analyst

**model_policy_need**: cloud_preferred (análisis profundo)

**complexity**: high

#### 10. tecnologia_desarrollo (12 nichos)

**Nichos propuestos**:
- software_architecture
- frontend_development
- backend_development
- fullstack_development
- mobile_development
- devops_engineering
- cloud_infrastructure
- database_administration
- api_development
- testing_qa
- security_engineering
- performance_optimization

**expected_profile_types**:
- software_architect
- frontend_developer
- backend_developer
- fullstack_developer
- mobile_developer
- devops_engineer
- cloud_infrastructure_specialist
- database_administrator
- api_developer
- qa_engineer
- security_engineer
- performance_engineer

**model_policy_need**: cloud_preferred (razonamiento técnico)

**complexity**: high

#### 11. creatividad_diseno (6 nichos)

**Nichos propuestos**:
- graphic_design
- ui_design
- motion_design
- brand_design
- design_systems
- creative_direction

**expected_profile_types**:
- graphic_designer
- ui_designer
- motion_designer
- brand_designer
- design_system_specialist
- creative_director

**model_policy_need**: auto (creatividad visual)

**complexity**: medium

#### 12. gestion_conocimiento (6 nichos)

**Nichos propuestos**:
- knowledge_architecture
- documentation_management
- learning_management
- knowledge_sharing
- taxonomy_design
- content_curation

**expected_profile_types**:
- knowledge_architect
- documentation_manager
- lms_specialist
- knowledge_sharing_specialist
- taxonomy_designer
- content_curator

**model_policy_need**: auto/local_ok (organización, documentación)

**complexity**: medium

#### 13. calidad_mejora_continua (6 nichos)

**Nichos propuestos**:
- quality_assurance
- continuous_improvement
- process_auditing
- six_sigma
- lean_management
- compliance_quality

**expected_profile_types**:
- qa_specialist
- continuous_improvement_specialist
- process_auditor
- six_sigma_black_belt
- lean_specialist
- quality_compliance_specialist

**model_policy_need**: auto (procesos, auditoría)

**complexity**: medium

#### 14. seguridad_informacion (8 nichos)

**Nichos propuestos**:
- information_security
- cybersecurity_operations
- security_architecture
- compliance_security
- incident_response
- vulnerability_management
- security_awareness
- identity_access_management

**expected_profile_types**:
- information_security_specialist
- cybersecurity_ops_specialist
- security_architect
- security_compliance_specialist
- incident_responder
- vulnerability_manager
- security_awareness_trainer
- iam_specialist

**model_policy_need**: cloud_required (seguridad crítica)

**complexity**: critical

#### 15. integraciones_apis (6 nichos)

**Nichos propuestos**:
- api_design
- api_development
- api_documentation
- api_testing
- api_governance
- api_marketplace

**expected_profile_types**:
- api_designer
- api_developer
- api_documenter
- api_tester
- api_governance_specialist
- api_marketplace_manager

**model_policy_need**: cloud_preferred (integración técnica)

**complexity**: high

#### 16. inteligencia_artificial_aplicada (8 nichos)

**Nichos propuestos**:
- ai_strategy
- ml_engineering
- prompt_engineering
- ai_governance
- ai_ethics
- ai_ops
- nlp_specialization
- computer_vision

**expected_profile_types**:
- ai_strategist
- ml_engineer
- prompt_engineer
- ai_governance_specialist
- ai_ethics_specialist
- ai_ops_specialist
- nlp_engineer
- computer_vision_engineer

**model_policy_need**: cloud_required (IA compleja)

**complexity**: critical

#### 17. supply_logistica (6 nichos)

**Nichos propuestos**:
- supply_chain_management
- logistics_optimization
- inventory_management
- demand_planning
- supplier_management
- warehouse_operations

**expected_profile_types**:
- supply_chain_manager
- logistics_optimizer
- inventory_manager
- demand_planner
- supplier_relationship_manager
- warehouse_operations_manager

**model_policy_need**: cloud_preferred (optimización compleja)

**complexity**: high

#### 18. gestion_comercial (6 nichos)

**Nichos propuestos**:
- sales_operations
- sales_enablement
- revenue_operations
- channel_management
- partner_management
- pricing_strategy

**expected_profile_types**:
- sales_ops_specialist
- sales_enablement_specialist
- revenue_ops_specialist
- channel_manager
- partner_manager
- pricing_strategist

**model_policy_need**: auto/local_ok (operaciones comerciales)

**complexity**: medium

#### 19. administracion_backoffice (4 nichos)

**Nichos propuestos**:
- backoffice_operations
- administrative_support
- document_management
- office_automation

**expected_profile_types**:
- backoffice_manager
- administrative_support_specialist
- document_management_specialist
- office_automation_specialist

**model_policy_need**: local_ok (operativo, simple)

**complexity**: low

#### 20. customer_success (6 nichos)

**Nichos propuestos**:
- customer_success_management
- onboarding_specialist
- customer_retention
- customer_health
- success_analytics
- advocacy_programs

**expected_profile_types**:
- customer_success_manager
- onboarding_specialist
- retention_specialist
- customer_health_analyst
- success_analyst
- advocacy_program_manager

**model_policy_need**: auto (relación cliente, análisis)

**complexity**: medium

## Trazabilidad Hacia Perfiles Profesionales

### Flujo Operativo Completo

```
Nicho
→ necesidades profesionales
→ expected_profile_types
→ professional_profile_id (Prompt 18)
→ role_id + specialization_id
→ preset_seed (Prompt 22)
→ paper_seed (Prompt 22)
→ default_model_policy (Prompt 20)
→ agente operativo
→ equipo profesional (Prompt 23)
```

### Ejemplo de Trazabilidad Completa

**Nicho**: automation_architecture
**expected_profile_types**: automation_architect
**Professional Profile** (Prompt 18):
- professional_profile_id: automation_architect
- role_id: arquitecto_sistemas
- specialization_id: arquitectura_componentes
- preset_seed: automation_architect_preset
- paper_seed: automation_architect_paper
- default_model_policy: cloud_preferred
- status: active

**Preset** (Prompt 22):
- id: automation_architect_preset
- system_prompt: "Actúa como arquitecto de automatizaciones..."
- paper_seed: {...}

**Paper** (Prompt 22):
- identity: "Arquitecto de automatizaciones..."
- operating_style: "Sistemático, trazable..."

**Model Policy** (Prompt 20):
- workload: heavy
- reasoning_need: high
- execution_preference: cloud_preferred

**Agente Operativo**:
- agent_id: automation_architect_01
- profile_preset_id: automation_architect_preset
- provider: openai
- model: gpt-4o

**Equipo Profesional** (Prompt 23):
- template_id: operations_automation_team
- roles: [automation_architect, process_designer, ops_documenter]

## Criterios de Status

### Status = proposed

- Existe como parte del universo objetivo
- Tiene descripción, necesidades, perfiles esperados
- Tiene contrato de operacionalización definido
- Todavía no tiene perfiles/presets/papers/model policies creados
- No aparece como opción usable en UI

### Status = draft

- Tiene estructura lista para implementación
- Puede estar cerca de ser usable
- Le falta al menos una pieza obligatoria (preset/paper/model_policy)
- No aparece como opción usable en UI

### Status = active

- Solo puede marcarse active si está completamente respaldado
- Tiene professional_profile_id válido
- Tiene preset_seed válido
- Tiene paper_seed válido
- Tiene default_model_policy definido
- Aparece como opción usable en UI
- Puede crear agente operativo sin errores

### Status = deprecated

- Fue active pero ya no se recomienda
- Puede mantenerse por compatibilidad
- No aparece como opción para nuevos agentes
- Puede migrarse a reemplazo

## Criterios para que un Nicho Pueda Volverse Operativo

Un nicho puede volverse operativo cuando:

1. **Tiene professional_profile_id**: Existe en catalogs/professional_profiles.json
2. **Tiene preset_seed**: Existe en domains/*/agent_presets.json
3. **Tiene paper_seed**: El preset tiene paper_seed definido
4. **Tiene default_model_policy**: El perfil tiene política de modelo
5. **Tiene role_id válido**: Referencia a catalogs/roles.json
6. **Tiene specialization_id válido**: Referencia a catalogs/specializations.json
7. **Status = active**: Marcado como activo en professional_profiles.json

Si falta cualquiera de estos, el nicho queda como proposed o draft.

## Contrato de Operacionalización por Nicho

### Formato Estándar

```json
{
  "niche_id": "automation_architecture",
  "operationalization_contract": {
    "needs_professional_profiles": true,
    "needs_presets": true,
    "needs_paper_seed": true,
    "needs_model_policy": true,
    "can_create_agent_when": "Professional profile exists with preset_seed, paper_seed and default_model_policy",
    "can_join_team_when": "Team template includes this professional_profile_id",
    "blocked_by": [
      "No professional_profile_id defined",
      "No preset_seed in professional profile",
      "No paper_seed in preset",
      "No default_model_policy in profile"
    ]
  }
}
```

### Regla

Ningún nicho debe declararse "operativamente completo" si todavía no tiene perfiles/presets/papers/model policies asociados.

## Riesgos de Escala

### Riesgos Identificados

1. **Performance**: Si la biblioteca crece a 200+ nichos, puede impactar tiempo de carga
2. **Usabilidad**: Lista larga sin filtros/tags/búsqueda puede ser inmanejable
3. **Mantenimiento**: Actualizar 200+ nichos con cambios de schema puede ser costoso
4. **Consistencia**: Mantener trazabilidad entre nichos, perfiles, presets, papers
5. **Validación**: Asegurar que cada nicho tenga todas las piezas obligatorias
6. **Adopción**: Usuarios pueden sentirse abrumados por cantidad de opciones

### Mitigaciones Propuestas

1. **Filtros y búsqueda**: Implementar búsqueda por área, tags, complexity, priority
2. **Paginación**: Mostrar nichos en grupos paginados por área
3. **Status filtering**: Por defecto mostrar solo active, proposed/draft en sección avanzada
4. **Validación automatizada**: Tests que verifiquen trazabilidad completa
5. **Documentación contextual**: Ayuda inline para cada nicho
6. **Adopción gradual**: Activar nichos en grupos, no todos de golpe

## Alcance Real Objetivo Estimado

### A. Áreas objetivo para empresa digital
- **30 áreas** (26 existentes + 4 nuevas)

### B. Nichos objetivo como universo
- **200 nichos** (94 actuales + 106 nuevos)

### C. Nichos active inicialmente
- **50 nichos** (prioridad alta para empresa digital)

### D. Nichos proposed/draft
- **150 nichos** (estructura lista, activación gradual)

### E. Perfiles profesionales necesarios (Prompt 18)
- **80-100 perfiles** para cubrir nichos objetivo

### F. Plantillas de equipo necesarias (Prompt 23)
- **25-30 plantillas** para configuraciones comunes

### G. Políticas de modelo necesarias (Prompt 20)
- **12-15 políticas** para cubrir patrones workload/reasoning

### H. Volumen cargable sin romper usabilidad
- **50-100 nichos** con filtros y búsqueda adecuados
- **Más de 150** requiere paginación y tags

### I. Volumen que requiere filtros/tags/búsqueda/paginación
- **Más de 100 nichos** requiere filtros por área
- **Más de 150 nichos** requiere búsqueda y tags
- **Más de 200 nichos** requiere paginación

### J. División en subpasos
- **Prompt 17.1**: Adaptar schema/catalog loader para soportar status, tags, complexity
- **Prompt 17.2**: Cargar primera expansión de 50 nichos active
- **Prompt 17.3**: Validar usabilidad con 50 nichos
- **Prompt 17.4**: Cargar segundo grupo de 50 nichos
- **Prompt 17.5**: Implementar filtros y búsqueda si necesario

## Relación con Perfiles Profesionales Futuros (Prompt 18)

### Mapeo Nicho → Perfiles

Cada nicho propuesto incluye `expected_profile_types` que guiará Prompt 18. Ejemplos:

- automation_architecture → automation_architect
- product_management → product_manager
- data_engineering → data_engineer
- sales_operations → sales_ops_specialist
- customer_success → customer_success_manager

### Tipos de Perfiles a Crear

Prompt 18 deberá crear perfiles para:
- Estrategia y dirección (12 tipos)
- Producto y UX (10 tipos)
- Operaciones y automatización (18 tipos)
- Datos e inteligencia (12 tipos)
- Ventas y crecimiento (8 tipos)
- Soporte y comunidad (8 tipos)
- Tecnología y desarrollo (12 tipos)
- Seguridad y compliance (8 tipos)
- Contenido y comunicación (8 tipos)
- Gestión y administración (10 tipos)

Total estimado: **80-100 perfiles profesionales**

## Relación con Equipos Futuros (Prompt 23)

### Plantillas de Equipo Propuestas

**growth_team**:
- growth_strategist
- paid_media_specialist
- seo_content_strategist
- data_analyst

**operations_automation_team**:
- automation_architect
- process_designer
- ops_documenter
- api_integration_specialist

**risk_compliance_team**:
- compliance_auditor
- legal_reviewer
- risk_analyst
- documentation_controller

**data_intelligence_team**:
- data_analyst
- bi_architect
- data_quality_analyst
- forecasting_specialist

**product_team**:
- product_manager
- ux_researcher
- product_analyst
- technical_writer

**customer_success_team**:
- customer_success_manager
- onboarding_specialist
- retention_specialist
- support_analyst

**security_team**:
- security_architect
- incident_responder
- vulnerability_manager
- security_compliance_specialist

Total estimado: **25-30 plantillas de equipo**

## Relación con Políticas de Modelo Futuras (Prompt 20)

### Mapeo Nicho → Model Policy

Cada nicho incluye `model_policy_need` que guiará Prompt 20. Ejemplos:

- documentación operativa: local_ok / auto
- automatización compleja: cloud_preferred
- auditoría legal/riesgo: cloud_required
- análisis de datos liviano: auto
- estrategia ejecutiva compleja: cloud_preferred
- seguridad crítica: cloud_required

### Patrones de Política Detectados

1. **local_ok**: Operativo simple, documental, sin razonamiento complejo
2. **auto**: Puede funcionar local o cloud según hardware
3. **cloud_preferred**: Razonamiento medio-alto, mejor en cloud
4. **cloud_required**: Crítico, precisa, razonamiento alto obligatorio

Total estimado: **12-15 políticas de modelo**

## Recomendación de Próximos Subpasos

### Prompt 17.1 (si necesario)

**Objetivo**: Adaptar schema/catalog loader para soportar nuevos campos

**Cambios**:
- Agregar campo `status` a areas.json y niches.json
- Agregar campo `tags` a niches.json
- Agregar campo `complexity` a niches.json
- Agregar campo `operational_priority` a niches.json
- Actualizar core/catalog_registry.py para validar nuevos campos
- Actualizar tests/test_catalogs.py para validar nuevos campos

**Criterio**: Si el catálogo actual no soporta bien status/metadata, ejecutar este subpaso antes de cargar expansión masiva.

### Prompt 17.2

**Objetivo**: Cargar primera expansión de 50 nichos active

**Cambios**:
- Agregar 4 áreas nuevas a catalogs/areas.json
- Agregar 50 nichos prioritarios a catalogs/niches.json
- Marcar status: active para nichos prioritarios
- Marcar status: proposed para nichos no prioritarios
- Validar con tests existentes
- Verificar compatibilidad con loaders

### Prompt 17.3

**Objetivo**: Validar usabilidad con 50 nichos

**Cambios**:
- Verificar tiempo de carga de catálogos
- Verificar usabilidad en UI de creación de dominio
- Verificar filtrado por área
- Recopilar feedback sobre usabilidad

### Prompt 17.4

**Objetivo**: Cargar segundo grupo de 50 nichos

**Cambios**:
- Agregar 50 nichos adicionales
- Activar filtros y búsqueda si necesario
- Validar escalabilidad

## Relación con Prompt 18, 19 y 20

### Prompt 18 — Inventario de Perfiles Profesionales

- Usa expected_profile_types de cada nicho
- Crea professional_profiles.json con 80-100 perfiles
- Define role_id y specialization_id por perfil
- Establece preset_seed y paper_seed por perfil
- Define default_model_policy por perfil

### Prompt 19 — Matriz Perfil → Áreas/Nichos

- Mapea cada professional_profile_id a compatible_area_ids
- Mapea cada professional_profile_id a compatible_niche_ids
- Valida que cada nicho tenga perfiles compatibles
- Documenta gaps donde faltan perfiles

### Prompt 20 — Recomendación Provider/Model por Perfil

- Usa model_policy_need de cada nicho
- Crea profile_model_policies.json con 12-15 políticas
- Define workload, reasoning_need, execution_preference
- Integra con hardware_profile existente
- Integra con model_recommendation existente

## Qué Queda Fuera de Alcance

- Integración n8n
- Orquestador de equipos
- UI de regeneración de paper
- Semáforo/compatibilidad visual HUD
- Validación cross-platform
- Implementación masiva de perfiles profesionales (Prompt 18)
- Implementación masiva de presets (Prompt 22)
- Implementación masiva de agentes
- Modificación de agentes existentes
- Modificación de papers existentes
- Modificación de presets existentes
- Avance a Prompt 18

## Decisiones Pendientes

- ¿Ejecutar Prompt 17.1 para adaptar schema antes de carga masiva?
- ¿Cuáles 50 nichos activar primero en Prompt 17.2?
- ¿Cómo manejar migración de nichos existentes a nuevo schema?
- ¿Qué criterios usar para priorizar activación de nichos?
- ¿Cómo validar que un nicho es realmente usable antes de marcarlo active?
- ¿Cómo manejar deprecación de nichos obsoletos?

## Estimación de Escala Final

- **Áreas objetivo**: 30 (26 existentes + 4 nuevas)
- **Nichos objetivo**: 200 (94 actuales + 106 nuevos)
- **Nichos active inicial**: 50 (prioridad alta)
- **Nichos proposed/draft**: 150 (activación gradual)
- **Perfiles profesionales**: 80-100 (Prompt 18)
- **Plantillas de equipo**: 25-30 (Prompt 23)
- **Políticas de modelo**: 12-15 (Prompt 20)

## Preparación Técnica del Catálogo

### Campos Nuevos Soportados

El catálogo ahora soporta metadatos operativos opcionales para áreas y nichos, manteniendo compatibilidad hacia atrás con los JSON existentes.

#### Campos para Áreas

**Campos operativos opcionales**:
- `status`: proposed / draft / active / deprecated
- `tags`: list[str]
- `business_value`: string
- `typical_domains`: list[str]
- `compatible_business_scales`: list[str]
- `operational_priority`: low / medium / high / critical
- `suggested_niche_count`: int
- `notes`: string

#### Campos para Nichos

**Campos operativos opcionales**:
- `status`: proposed / draft / active / deprecated
- `tags`: list[str]
- `typical_needs`: list[str]
- `expected_profile_types`: list[str]
- `likely_professional_profiles`: list[str]
- `required_capabilities`: list[str]
- `possible_team_templates`: list[str]
- `model_policy_need`: local_ok / auto / cloud_preferred / cloud_required / critical_reasoning_required
- `complexity`: low / medium / high / critical
- `operational_priority`: low / medium / high / critical
- `compatible_business_scales`: list[str]
- `activation_requirements`: list[str]
- `operationalization_contract`: object
- `notes`: string

#### Operationalization Contract

El campo `operationalization_contract` puede contener:
- `needs_professional_profiles`: bool
- `needs_presets`: bool
- `needs_paper_seed`: bool
- `needs_model_policy`: bool
- `can_create_agent_when`: string
- `can_join_team_when`: string
- `blocked_by`: list[str]

### Compatibilidad Hacia Atrás

- Los catálogos actuales (areas.json, niches.json) no requieren migración
- Los campos nuevos son opcionales
- Si un campo no está presente, el loader no lo valida ni lo requiere
- Los catálogos existentes siguen funcionando sin cambios
- Los tests existentes siguen pasando sin modificaciones

### Validaciones Implementadas

El loader `core/catalog_registry.py` ahora valida:

## Auditoría y Alineación de Datos Existentes (Prompt 17.1.1)

### Estado de la Base Antes de Expansión

Antes de proceder con la carga masiva de nuevos nichos en Prompt 17.2, se ejecutó una auditoría completa de la base existente para asegurar consistencia y trazabilidad operativa.

### Inconsistencias Detectadas y Resueltas

**Dominio Lotería:**
- **19 combinaciones role+specialization** sin preset operativo → Marcadas como `activo: false` en `profile_catalog.json`
- **11 presets** sin `recommended_provider`/`recommended_model` → No es inconsistencia: diseño delega recomendación a `core/model_recommendation.py`
- **5 agentes legacy** sin combinación formal role+specialization → Documentados como legacy (gemini_cuantico, gpt_auditor, nuevo_deepseek_saaop, viejo_deepseek, viejo_lobo_rey)
- **Todos los role_ids y specialization_ids** en profiles y presets son válidos → No requiere corrección

### Regla Vigente Post-Auditoría

Todo elemento seleccionable para crear agentes debe tener trazabilidad completa:

```
profile_catalog (activo: true)
→ role_id válido en catalogs/roles.json
→ specialization_id válida en catalogs/specializations.json
→ preset correspondiente en agent_presets.json
→ paper_seed definido
→ default_model_policy o recomendación dinámica
→ agent config capaz de ejecutarse
```

### Tests de Consistencia Agregados

Se creó `tests/test_profile_preset_consistency.py` con 10 tests para validar:
- Ningún profile usable sin preset
- Ningún preset usable sin profile
- Ningún preset usable sin paper_seed
- Todos los role_ids y specialization_ids son válidos
- Los 11 agentes, 11 papers y 11 presets de Lotería siguen existiendo

### Impacto en Prompt 17.2

Prompt 17.2 puede avanzar sobre una base saneada. La estructura existente cumple con las reglas de trazabilidad operativa. Los perfiles históricos de Lotería que no tienen combinación formal role+specialización quedan documentados para recuperación futura en Prompt 18.1.

- Si `status` aparece, debe ser uno de: proposed, draft, active, deprecated
- Si `complexity` aparece, debe ser uno de: low, medium, high, critical
- Si `operational_priority` aparece, debe ser uno de: low, medium, high, critical
- Si `model_policy_need` aparece, debe ser uno de: local_ok, auto, cloud_preferred, cloud_required, critical_reasoning_required
- Si `compatible_business_scales` aparece, debe ser una lista con valores válidos: micro, local_business, freelancer, pyme, company, enterprise, department, research_team, experimental_domain
- Si `operationalization_contract` aparece, debe tener la estructura esperada con tipos correctos
- Si campos de lista aparecen (tags, typical_needs, expected_profile_types, etc.), deben ser listas de strings no vacíos

### Por Qué No Se Cargan Todavía los 106 Nichos

Aunque el catálogo ahora soporta los metadatos operativos necesarios, no se cargan los 106 nichos nuevos en este prompt porque:

1. **Prioridad técnica**: Primero se prepara la infraestructura de validación y loader
2. **Validación gradual**: Es mejor cargar en grupos pequeños (Prompt 17.2) para validar usabilidad
3. **Dependencia de Prompt 18**: Los nichos nuevos requieren perfiles profesionales que aún no existen
4. **Trazabilidad operativa**: Los nichos nuevos no deben marcarse como `active` hasta que tengan preset_seed, paper_seed y default_model_policy

### Qué Queda Listo para Prompt 17.2

Prompt 17.2 podrá:

1. Cargar una primera expansión de nichos PASSED con metadatos operativos completos
2. Mantener candidatos `proposed` o `draft` en documentación/backlog hasta que puedan pasar a operativo
3. Validar que cada nicho tenga `expected_profile_types` definidos
4. Validar que cada nicho tenga `model_policy_need` definido
5. Validar que cada nicho tenga `operationalization_contract` definido
6. Mantener compatibilidad con los 94 nichos existentes
7. Usar los nuevos tests para validar que la expansión no rompe el loader

---

## Universo Objetivo vs Catálogo Operativo PASSED

### Regla PASSED

IA_CORE distingue entre:

**A. Universo exploratorio / backlog documental:**
- Ideas, propuestas, borradores, perfiles históricos, nichos candidatos
- Viven en: `docs/`, reportes, backlog futuro, documentos de diseño, Prompt 18.1 o futuros subprompts
- No aparecen como opción usable

**B. Catálogo operativo:**
- Solo elementos PASSED
- Lo que está en catálogo operativo debe poder avanzar hacia uso real

### Equivalencia Técnica

- `activo: true` = PASSED operativo
- `activo: false` = baja/desactivado temporal
- `status: active` (si se usa en futuro) = PASSED operativo
- `status: proposed/draft` = estados de transición para clasificar y decidir, no usables
- En loaders operativos (`active_only=True`), `proposed`, `draft` y `deprecated` quedan fuera de respuestas usables aunque `activo` sea `true`

### Impacto en Prompt 17.2

El universo objetivo puede tener 200 nichos, pero no se cargarán como opciones operativas hasta que estén PASSED. Prompt 17.2 debe cargar solo elementos PASSED o preparar bloques con trazabilidad suficiente. Lo no validado queda en reporte/backlog. Todo elemento propuesto debe tender a operación real o darse de baja.

### Clasificación de Decisiones

**A. Alta operativa / PASSED:**
- Elemento está completo, tiene trazabilidad y puede usarse
- Aparece como opción usable en UI

**B. Recuperar y volver operativo:**
- Elemento es valioso, pero le faltan piezas
- Debe quedar identificado con las piezas faltantes y el subprompt donde se completará
- No aparece como opción usable hasta completar

**C. Legacy:**
- Elemento existe por historia o compatibilidad
- Puede seguir ejecutándose si corresponde
- No pasa por el flujo nuevo hasta que sea recuperado formalmente
- No aparece como opción usable en flujo nuevo

**D. Baja / desactivar:**
- Elemento no debe usarse, no aporta o quedó obsoleto
- No se elimina necesariamente si hay riesgo histórico
- No aparece como opción usable

**E. Backlog documental:**
- Elemento es una idea o candidato futuro
- No entra todavía al catálogo operativo
- Vive en docs/ o reportes
- No aparece como opción usable

---

## Estrategia de expansión PASSED por tandas

### Objetivo final del libro

La Biblioteca Profesional Global debe avanzar progresivamente hacia:

- Aproximadamente 30 áreas profesionales activas/PASSED.
- Aproximadamente 200 nichos activos/PASSED.
- 80-100 perfiles profesionales conectables a dominios reales.
- 25-30 team templates para equipos profesionales frecuentes.
- 12-15 model policies o políticas de recomendación de modelo.

La expansión no busca inflar catálogos. Cada incorporación debe mejorar la utilidad real del sistema y conservar una ruta posterior hacia perfiles, presets, papers y model policies.

### Regla de carga

- No se cargan 200 nichos de golpe si no están bien definidos.
- No se cargan propuestas dormidas ni `draft` eternos.
- Cada tanda entra como PASSED o queda fuera del JSON operativo.
- Cada tanda debe dejar IA_CORE más usable que antes.
- `proposed`, `draft` y `deprecated` pueden vivir como discusión documental, pero no como opción usable.

### Tandas sugeridas

1. **Tanda 1 — Empresa digital moderna**: producto, automatización, datos/BI, customer success y nichos prácticos para ventas, marketing, finanzas, RRHH, tecnología y dirección.
2. **Tanda 2 — Automatización, datos, operaciones y crecimiento**: profundizar flujos internos, RevOps avanzado, operaciones digitales, analítica aplicada y crecimiento por canal.
3. **Tanda 3 — Escala de negocio**: nichos diferenciados para emprendedor, comercio local, pyme, empresa y enterprise.
4. **Tanda 4 — Investigación, estrategia avanzada, riesgo y compliance**: dominios de mayor complejidad, gobernanza, auditoría, riesgo y especializaciones sectoriales.
5. **Tanda 5 — Normalización final**: acercamiento al objetivo 30/200, deduplicación conceptual y ajuste de metadata operativa.

Cada tanda debe cerrar con tests, conteo actualizado, documentación, commit y working tree limpio.

## Prompt 17.2 — Tanda 1 PASSED cargada

### Conteo antes

- Áreas: 26.
- Nichos: 94.
- Estados transicionales en JSON operativo: 0.

### Conteo después

- Áreas: 30.
- Nichos: 134.
- Estados transicionales en JSON operativo: 0.

### Áreas nuevas agregadas

| Área | Motivo |
|---|---|
| `producto_gestion_producto` | Cubre discovery, roadmap, pricing y ciclo de producto completo, que no estaban resueltos por diseño UX o gerencia general. |
| `automatizacion_integraciones` | Separa automatización operativa transversal de tecnología genérica. |
| `datos_bi_analytics` | Convierte el nicho de datos/BI en un área global para métricas, tableros, calidad de datos y decisión. |
| `customer_success_experiencia_cliente` | Distingue adopción, retención y churn de soporte/call center tradicional. |

### Nichos nuevos agregados por área

| Área | Cantidad | Nichos |
|---|---:|---|
| `producto_gestion_producto` | 5 | `gestion_producto_digital`, `research_usuarios`, `validacion_ideas_negocio`, `priorizacion_roadmap`, `pricing_packaging` |
| `automatizacion_integraciones` | 5 | `automatizacion_procesos_internos`, `integraciones_herramientas`, `automatizacion_whatsapp_crm`, `gestion_apis`, `arquitectura_sistemas_internos` |
| `datos_bi_analytics` | 5 | `dashboards_operativos`, `indicadores_negocio`, `analisis_cohortes`, `inteligencia_comercial`, `auditoria_datos` |
| `customer_success_experiencia_cliente` | 5 | `onboarding_clientes`, `retencion_fidelizacion_clientes`, `voz_cliente_nps`, `gestion_churn`, `experiencia_cliente_omnicanal` |
| `tecnologia_sistemas_telecomunicaciones` | 4 | `devops_basico_pymes`, `seguridad_operativa_basica`, `soporte_tecnico_operativo`, `calidad_software_qa` |
| `marketing_publicidad` | 4 | `growth_marketing`, `estrategia_contenidos`, `embudos_conversion`, `campanas_comercios_locales` |
| `comercial_ventas_negocios` | 3 | `ventas_consultivas`, `revenue_operations`, `crm_comercial` |
| `administracion_contabilidad_finanzas` | 4 | `flujo_caja_pyme`, `control_gastos`, `rentabilidad_producto`, `punto_equilibrio` |
| `recursos_humanos_capacitacion` | 3 | `onboarding_empleados`, `evaluacion_desempeno`, `diseno_roles_internos` |
| `gerencia_direccion_general` | 2 | `objetivos_metricas_okrs`, `modelos_negocio` |

### Criterio de selección

La primera tanda prioriza dominios frecuentes en empresas digitales, pymes, comercios y servicios reales: producto, automatización, datos, customer success, crecimiento, ventas, finanzas, RRHH, tecnología operativa y dirección. Se agregaron áreas nuevas solo cuando el concepto no estaba suficientemente cubierto por áreas existentes.

### Nichos descartados o pospuestos

- Operaciones avanzadas, logística digital, compliance ampliado y riesgo sectorial quedan para tandas posteriores.
- Nichos de IA aplicada, data science avanzada y seguridad especializada quedan pospuestos hasta tener perfiles/model policies más específicos.
- Nichos verticales por industria quedan para la tanda de escala/sector, para evitar duplicar áreas existentes.

### Acercamiento al objetivo 30/200

La tanda deja el sistema en 30 áreas y 134 nichos. Faltan aproximadamente 66 nichos PASSED para llegar al objetivo de 200. La siguiente expansión debe priorizar profundidad operativa y deduplicación, no cantidad por sí misma.

### Próxima tanda sugerida

Prompt 17.3 debería validar usabilidad de esta tanda con creación de dominios y, si no hay regresiones, preparar la Tanda 2: automatización avanzada, operaciones digitales, datos aplicados y crecimiento por canal, manteniendo la regla PASSED.

## Validación de usabilidad de Tanda 1

### Qué se validó

Prompt 17.3 validó que la Tanda 1 no quedara solo como JSON cargado. La revisión cubrió:

- Carga de áreas activas con `load_areas(active_only=True)`.
- Carga de nichos activos con `load_niches(active_only=True)`.
- Agrupación de opciones para Crear Dominio mediante `get_domain_creation_catalog()`.
- Validación de selección `area_profesional_id` + `nicho_id` con `validate_domain_catalog_selection()`.
- Creación temporal de dominios desde nichos nuevos usando `nombre_dominio_sugerido`, `descripcion_sugerida` e `instrucciones_sugeridas`.
- Filtro de `proposed`, `draft`, `deprecated` y `activo:false` con `active_only=True`.
- Separación entre catálogo global y dominio Lotería.

### Muestra de nichos probados

La muestra de flujo de dominio cubrió las 4 áreas nuevas y áreas existentes enriquecidas:

| Área | Nicho validado |
|---|---|
| `producto_gestion_producto` | `gestion_producto_digital` |
| `automatizacion_integraciones` | `automatizacion_procesos_internos` |
| `datos_bi_analytics` | `dashboards_operativos` |
| `customer_success_experiencia_cliente` | `onboarding_clientes` |
| `tecnologia_sistemas_telecomunicaciones` | `devops_basico_pymes` |
| `marketing_publicidad` | `growth_marketing` |
| `comercial_ventas_negocios` | `ventas_consultivas` |
| `administracion_contabilidad_finanzas` | `flujo_caja_pyme` |
| `recursos_humanos_capacitacion` | `onboarding_empleados` |
| `gerencia_direccion_general` | `objetivos_metricas_okrs` |

Para cada nicho se validó que:

- Está activo/PASSED.
- Pertenece a un `area_id` válido.
- Aparece como opción usable en el catálogo de creación de dominios.
- Expone nombre, descripción e instrucciones sugeridas.
- Conserva metadata operativa mínima.
- No contiene dependencias de Lotería.
- No contiene prompts embebidos de agente ni IDs concretos de agentes/perfiles.
- Permite crear un dominio temporal sin crear agentes, presets ni papers permanentes.

### Resultado del flujo de dominio

El flujo global puede consumir Tanda 1 de punta a punta:

- La API `/api/catalogs/domain-creation` consume automáticamente las áreas y nichos nuevos porque usa el registry global.
- La UI de Crear Dominio carga áreas y nichos desde ese endpoint y rellena los campos editables con las sugerencias del nicho seleccionado.
- `create_domain()` acepta la selección área/nicho y persiste `area_profesional_id`, `nicho_id` y `nicho_sugerido` en `domain.json`.
- La creación probada se hizo en fixtures temporales, sin modificar `domains/` operativo.

### Separación de Lotería

La expansión global no contamina Lotería:

- Los 40 nichos nuevos no referencian `domains/loteria`.
- Los textos de Tanda 1 no contienen términos de lotería, sorteos, cartones, bankroll, apuestas ni promesas de azar.
- Lotería sigue siendo un dominio específico con su `domain.json`, `profile_catalog.json` y `agent_presets.json`.
- Los tests de Lotería siguen cubriendo perfil, presets y separación de agentes/papers por dominio.

### Catálogos fantasma

Se reforzó la prueba de estados no usables:

- `status: proposed` queda fuera con `active_only=True`.
- `status: draft` queda fuera con `active_only=True`.
- `status: deprecated` queda fuera con `active_only=True`.
- `activo:false` queda fuera con `active_only=True`.
- `activo:true` + `status: active` aparece correctamente.
- `activo:true` sin `status` aparece correctamente como PASSED por compatibilidad.

El JSON operativo real sigue sin estados `proposed`, `draft` ni `deprecated`.

### Problemas detectados y correcciones

No se detectaron problemas graves de UX en los 40 nichos nuevos:

- No hay nombres excesivamente largos.
- No hay `nombre_dominio_sugerido` excesivamente largo.
- No hay descripciones demasiado cortas o demasiado largas.
- No hay instrucciones sugeridas demasiado cortas o demasiado largas.
- No hay IDs duplicados ni nombres visibles duplicados.
- No hay referencias a Lotería ni prompts embebidos.

No se modificó `catalogs/areas.json` ni `catalogs/niches.json` en este prompt. La corrección realizada fue de cobertura: tests de flujo real y filtros PASSED.

### Estado final de Tanda 1

- Áreas totales: 30.
- Áreas activas/PASSED: 30.
- Nichos totales: 134.
- Nichos activos/PASSED: 134.
- Estados `proposed`/`draft`/`deprecated` en JSON operativo: 0.
- Nichos de Tanda 1 usables/PASSED: 40 de 40.
- Áreas nuevas usables/PASSED: 4 de 4.

Tanda 1 queda validada como usable para creación de dominios. El siguiente paso debe ampliar cobertura sin romper deduplicación ni la regla PASSED.

## Preparación histórica de Tanda 2 PASSED

Esta sección quedó como preparación documental previa a Prompt 17.4. Tanda 2A ya cargó una primera sub-tanda y dejó el catálogo en 169 nichos PASSED; el tramo restante queda preparado más abajo como Tanda 2B.

### Alcance sugerido

Tanda 2 debería priorizar nichos reales y entendibles para usuarios no técnicos en:

- Automatización avanzada.
- Operaciones digitales.
- Datos aplicados por negocio.
- Crecimiento por canal.
- Ventas y revenue operations.
- Customer success avanzado.
- Administración y finanzas para pymes.
- Legal/compliance básico.
- Gestión de proyectos.
- Investigación y estrategia avanzada.
- Perfiles por escala de negocio: emprendedor, local comercial, pyme, empresa y enterprise.

### Criterio de entrada

Cada nicho de Tanda 2 debe entrar solo si cumple:

- Caso de uso real y distinguible.
- `area_id` válido y sin duplicación conceptual grave.
- Nombre comprensible para usuario no técnico.
- `nombre_dominio_sugerido`, `descripcion_sugerida` e `instrucciones_sugeridas` accionables.
- Metadata operativa mínima completa.
- `activo:true` y, si usa `status`, `status: active`.
- Sin referencias a Lotería, agentes legacy, presets inexistentes, papers ni n8n.

Si una sub-tanda no puede cumplir esos criterios, debe quedar en backlog documental y no en JSON operativo.

## Tanda 2A PASSED

### Conteo antes

- Áreas: 30.
- Nichos: 134.
- Estados transicionales en JSON operativo: 0.

### Conteo después

- Áreas: 30.
- Nichos: 169.
- Estados transicionales en JSON operativo: 0.

### Nichos agregados

Tanda 2A agregó 35 nichos PASSED, todos en áreas existentes:

| Área | Cantidad | Nichos |
|---|---:|---|
| `automatizacion_integraciones` | 4 | `aprobaciones_internas`, `automatizacion_reportes_recurrentes`, `flujos_no_code_low_code`, `automatizacion_tareas_administrativas` |
| `datos_bi_analytics` | 4 | `rentabilidad_por_canal`, `analisis_clientes_recurrentes`, `tableros_margen_costos`, `segmentacion_comercial_avanzada` |
| `marketing_publicidad` | 4 | `crecimiento_whatsapp`, `crecimiento_instagram_tiktok`, `calendario_comercial`, `analisis_rendimiento_campanas` |
| `comercial_ventas_negocios` | 4 | `diseno_pipeline_comercial`, `seguimiento_oportunidades_comerciales`, `procesos_venta_pymes`, `scripts_objeciones_comerciales` |
| `customer_success_experiencia_cliente` | 4 | `recuperacion_clientes_inactivos`, `medicion_satisfaccion_cliente`, `programas_fidelizacion`, `experiencia_postventa` |
| `administracion_contabilidad_finanzas` | 4 | `rentabilidad_unidad_negocio`, `flujo_caja_semanal`, `control_deuda_pagos`, `presupuesto_por_area` |
| `legales` | 3 | `checklist_documental_basico`, `contratos_simples_pymes`, `politicas_internas_basicas` |
| `gerencia_direccion_general` | 4 | `planificacion_proyectos_internos`, `seguimiento_entregables`, `gestion_riesgos_proyecto`, `analisis_competidores` |
| `abastecimiento_logistica` | 2 | `planificacion_compras`, `seguimiento_proveedores` |
| `produccion_manufactura` | 2 | `mejora_continua_procesos`, `estandarizacion_procedimientos` |

### Criterio de selección

La tanda priorizó casos reales y frecuentes para empresa digital, pyme, local comercial y equipos internos:

- Automatización que reduce trabajo manual sin depender de n8n ni de agentes reales todavía.
- Datos aplicados a margen, canales, clientes recurrentes y segmentación comercial.
- Growth por canales concretos, calendario comercial y medición de campañas.
- Procesos de venta entendibles para pymes y equipos comerciales pequeños.
- Customer success avanzado sin duplicar soporte ni Lotería.
- Finanzas operativas de corto plazo y control de gestión.
- Legal/compliance básico con lenguaje práctico y sin prometer asesoramiento jurídico completo.
- Gestión de proyectos internos, entregables, riesgos y análisis competitivo.
- Operaciones de compras, proveedores, mejora continua y procedimientos.

### Nichos descartados o pospuestos

- IA aplicada, data science avanzada y data engineering quedan para una tanda posterior con model policies más específicas.
- Security operations avanzado queda fuera para no duplicar `ciberseguridad` y `seguridad_operativa_basica`.
- Compliance regulatorio sectorial se pospone para evitar cargar nichos legales que requieren especialización vertical.
- Gestión de proyectos enterprise, PMO avanzada y portafolios complejos se dejan para Tanda 2B o una tanda de escala.
- Nichos por industria específica se mantienen fuera para no contaminar áreas transversales con verticales prematuros.

### Confirmación PASSED

- No se cargó ningún `proposed`, `draft` ni `deprecated`.
- Todo nicho nuevo entra con `activo:true` y `status: active`.
- Todo nicho nuevo tiene campos mínimos completos y metadata operativa.
- Todo nicho nuevo conserva `operationalization_contract` hacia Prompt 18.
- No se agregaron áreas nuevas.
- No se tocaron profiles, presets, agentes, papers, HUD ni n8n.

### Acercamiento al objetivo 30/200

El catálogo queda en 30 áreas y 169 nichos PASSED. Faltan aproximadamente 31 nichos para llegar al objetivo orientativo de 200.

La cobertura de empresa digital queda mucho más completa en automatización, datos, growth, ventas, customer success, finanzas, legal básico, proyectos y operaciones. Las brechas restantes se concentran en áreas con baja cobertura, escala de negocio, investigación avanzada, compliance más específico y verticales operativos.

## Preparación histórica de Tanda 2B PASSED

Esta sección quedó como preparación documental previa a Prompt 17.5. Tanda 2B ya cargó el tramo restante y dejó el catálogo en 200 nichos PASSED.

### Enfoque recomendado

- Cerrar brechas en áreas con 3 nichos: salud, ingeniería, construcción, seguros, comunicación, sociología/trabajo social, enfermería, marítimo/portuario, minería/energía, diseño, secretaría/recepción y departamento técnico.
- Sumar nichos por escala de negocio: emprendedor, local comercial, pyme, empresa y enterprise.
- Reforzar investigación y estrategia sin duplicar `investigacion_mercado`, `research_usuarios` ni `analisis_competidores`.
- Agregar operaciones digitales pendientes: coordinación interna, mesa de operaciones, gestión de capacidad, documentación operacional y control de calidad de servicio.
- Ampliar legal/compliance solo con casos básicos y usables, evitando verticales regulados complejos hasta tener perfiles especializados.
- Mantener cada nuevo nicho con caso de uso real, nombre claro, metadata completa y ruta posterior hacia perfiles, team templates y model policies.

### Criterio de corte

Si Tanda 2B agrega aproximadamente 30-31 nichos PASSED, el catálogo llegaría a 199-200 nichos y quedaría listo para que Prompt 18 avance sobre perfiles profesionales sin sensación de base incompleta.

## Tanda 2B PASSED

### Conteo antes

- Áreas: 30.
- Nichos: 169.
- Estados transicionales en JSON operativo: 0.

### Conteo después

- Áreas: 30.
- Nichos: 200.
- Estados transicionales en JSON operativo: 0.

### Nichos agregados

Tanda 2B agregó 31 nichos PASSED, todos en áreas existentes:

| Área | Cantidad | Nichos |
|---|---:|---|
| `oficios_otros` | 1 | `gestion_servicios_oficios` |
| `salud_medicina_farmacia` | 2 | `agenda_consultorios_salud`, `seguimiento_pacientes_cronicos` |
| `ingenierias` | 2 | `validacion_requerimientos_tecnicos`, `gestion_cambios_ingenieria` |
| `ingenieria_civil_construccion` | 2 | `seguimiento_avance_obra`, `control_costos_obra` |
| `departamento_tecnico` | 2 | `gestion_garantias_tecnicas`, `base_conocimiento_tecnica` |
| `secretarias_recepcion` | 2 | `seguimiento_tramites`, `coordinacion_reuniones_eventos` |
| `diseno` | 2 | `sistemas_diseno_marca`, `investigacion_visual_usuarios` |
| `mineria_petroleo_gas` | 2 | `control_produccion_minera_energia`, `permisos_reportes_ambientales` |
| `aduana_comercio_exterior` | 2 | `seguimiento_embarques`, `costos_importacion_exportacion` |
| `seguros` | 2 | `renovacion_polizas`, `analisis_cartera_seguros` |
| `comunicacion_relaciones_institucionales_publicas` | 2 | `gestion_crisis_comunicacional`, `comunicacion_interna` |
| `sociologia_trabajo_social` | 2 | `evaluacion_impacto_social`, `gestion_casos_sociales` |
| `enfermeria` | 2 | `coordinacion_turnos_enfermeria`, `seguimiento_indicaciones_cuidado` |
| `naviero_maritimo_portuario` | 2 | `coordinacion_operaciones_embarque`, `control_documental_portuario` |
| `atencion_cliente_call_center_telemarketing` | 1 | `protocolos_respuesta_cliente` |
| `legales` | 1 | `proteccion_datos_basica` |
| `recursos_humanos_capacitacion` | 1 | `gestion_beneficios_compensaciones` |
| `educacion_docencia_investigacion` | 1 | `evaluacion_aprendizaje` |

### Criterio de selección

La tanda cerró brechas de áreas con baja cobertura y completó el objetivo 30/200 sin crear áreas nuevas. Se priorizaron:

- Áreas profesionales que seguían en 3 nichos y necesitaban casos de uso reales.
- Operación administrativa, técnica, social, salud, diseño, seguros, comercio exterior, comunicación y sectores industriales.
- Casos que un usuario no técnico puede elegir para crear un dominio útil.
- Nichos con ruta futura hacia perfiles profesionales, team templates y model policies.

### Nichos descartados o pospuestos

- Nichos regulatorios altamente especializados por país o industria quedan fuera hasta tener perfiles legales/sectoriales.
- Nichos clínicos de diagnóstico o tratamiento quedan fuera; salud y enfermería se mantuvieron en coordinación y gestión operativa.
- Nichos de ingeniería extremadamente técnicos quedan fuera para evitar prometer capacidades sin perfiles expertos.
- Nichos enterprise complejos de PMO, data engineering y seguridad avanzada quedan para después de Prompt 18.

### Confirmación PASSED

- No se cargó ningún `proposed`, `draft` ni `deprecated`.
- Todo nicho nuevo entra con `activo:true` y `status: active`.
- Todo nicho nuevo tiene campos mínimos completos y metadata operativa.
- Todo nicho nuevo conserva `operationalization_contract` hacia Prompt 18.
- No se agregaron áreas nuevas.
- No se tocaron profiles, presets, agentes, papers, HUD ni n8n.

### Acercamiento al objetivo 30/200

El catálogo queda exactamente en 30 áreas y 200 nichos PASSED. El objetivo de áreas/nichos del libro queda cubierto para iniciar la etapa de perfiles profesionales globales.

## Preparación de cierre de etapa áreas/nichos

Recomendación: ejecutar un micro-prompt 17.5.1 de auditoría final 30/200 antes de Prompt 18.

Ese cierre debería:

- Revisar deduplicación conceptual de los 200 nichos.
- Validar UX de nombres, descripciones e instrucciones sugeridas.
- Confirmar 0 `proposed`/`draft`/`deprecated`.
- Confirmar que Lotería sigue aislada como dominio específico.
- Congelar el catálogo de áreas/nichos como base de Prompt 18.
- Preparar el inventario de 80-100 perfiles profesionales sin cargar perfiles todavía.

Si esa auditoría final queda verde, el siguiente paso natural será Prompt 18: inventario de perfiles profesionales globales.

## Cierre de etapa áreas/nichos — 30 áreas / 200 nichos

### Conteo final

- Áreas totales: 30.
- Áreas activas/PASSED: 30.
- Nichos totales: 200.
- Nichos activos/PASSED: 200.
- Estados `proposed`/`draft`/`deprecated` en JSON operativo: 0.
- IDs duplicados: 0.
- Nichos con `area_id` inválido: 0.
- Áreas sin nichos: 0.
- Menor cobertura por área: 4 nichos.
- Mayor cobertura por área: 13 nichos.

### Distribución final por área

| Área | Nichos |
|---|---:|
| `administracion_contabilidad_finanzas` | 13 |
| `marketing_publicidad` | 13 |
| `comercial_ventas_negocios` | 12 |
| `automatizacion_integraciones` | 9 |
| `customer_success_experiencia_cliente` | 9 |
| `datos_bi_analytics` | 9 |
| `gerencia_direccion_general` | 9 |
| `tecnologia_sistemas_telecomunicaciones` | 9 |
| `legales` | 9 |
| `recursos_humanos_capacitacion` | 7 |
| `atencion_cliente_call_center_telemarketing` | 6 |
| `educacion_docencia_investigacion` | 6 |
| `abastecimiento_logistica` | 5 |
| `aduana_comercio_exterior` | 5 |
| `comunicacion_relaciones_institucionales_publicas` | 5 |
| `departamento_tecnico` | 5 |
| `diseno` | 5 |
| `enfermeria` | 5 |
| `gastronomia_turismo` | 5 |
| `ingenieria_civil_construccion` | 5 |
| `ingenierias` | 5 |
| `mineria_petroleo_gas` | 5 |
| `naviero_maritimo_portuario` | 5 |
| `produccion_manufactura` | 5 |
| `producto_gestion_producto` | 5 |
| `salud_medicina_farmacia` | 5 |
| `secretarias_recepcion` | 5 |
| `seguros` | 5 |
| `sociologia_trabajo_social` | 5 |
| `oficios_otros` | 4 |

### Resumen de tandas

- **Tanda 1 / Prompt 17.2**: llevó el catálogo a 30 áreas y 134 nichos, agregando producto, automatización, datos/BI y customer success como áreas nuevas.
- **Validación / Prompt 17.3**: confirmó que Tanda 1 funciona en creación de dominios y que `active_only=True` no expone elementos no usables.
- **Tanda 2A / Prompt 17.4**: agregó 35 nichos PASSED y llevó el catálogo de 134 a 169 nichos.
- **Tanda 2B / Prompt 17.5**: agregó 31 nichos PASSED y completó el objetivo exacto de 200 nichos.
- **Auditoría final / Prompt 17.5.1**: confirma que la etapa áreas/nichos queda lista para alimentar Prompt 18.

### Auditoría conceptual y UX

La muestra auditada incluyó nichos históricos, Tanda 1, Tanda 2A, Tanda 2B, Lotería, áreas nuevas, áreas técnicas, áreas de negocio, atención, operación y administración.

Resultado:

- Los nombres son entendibles para usuarios no técnicos.
- `nombre_dominio_sugerido` permite crear dominios reconocibles.
- `descripcion_sugerida` describe casos de uso reales.
- `instrucciones_sugeridas` orienta el comportamiento del dominio sin crear agentes.
- No se detectaron duplicados de nombre visible ni de nombre de dominio sugerido.
- No se detectaron placeholders reales como `por definir`, `tbd`, `placeholder` o textos vacíos.
- No se detectaron prompts/presets embebidos inválidos.
- Lotería sigue siendo un nicho y dominio específico, no un default global.

### Preparación para Prompt 18

El catálogo 30/200 ya puede guiar el inventario de perfiles profesionales globales:

- **Perfiles estratégicos**: gerencia, modelos de negocio, OKRs, análisis competitivo, planificación y transformación.
- **Perfiles operativos**: producción, logística, abastecimiento, secretaría, coordinación interna, proyectos y procedimientos.
- **Perfiles técnicos**: tecnología, soporte IT, departamento técnico, ingeniería, construcción, minería/energía y operaciones portuarias.
- **Perfiles de datos**: dashboards, indicadores, auditoría de datos, segmentación, cohortes, margen/costos y BI comercial.
- **Perfiles comerciales**: ventas, CRM, revenue operations, pipeline, scripts, e-commerce, prospección y cuentas clave.
- **Perfiles administrativos/financieros**: contabilidad, tesorería, cashflow, presupuestos, deuda, rentabilidad y control de gestión.
- **Perfiles legales/compliance**: contratos, compliance normativo, protección de datos, políticas internas y documentación básica.
- **Perfiles de atención/soporte**: atención al cliente, reclamos, mesa de ayuda, postventa, protocolos y customer success.
- **Perfiles de investigación**: research de usuarios, investigación de mercado, análisis de tendencias, competidores, impacto social y aprendizaje.

Muchos perfiles futuros podrán ser globales y reutilizables: analista de datos, operations manager, project manager, compliance analyst, customer success manager, marketing/growth strategist, financial controller, technical writer, service designer, support manager y business analyst.

### Decisión final

La etapa de áreas/nichos queda **lista para Prompt 18**.

No se recomienda cargar más nichos antes de perfiles. El próximo paso debe ser inventariar 80-100 perfiles profesionales globales PASSED, evitando perfiles fantasma y conectando cada perfil futuro con áreas/nichos, preset_seed, paper_seed y model policy.

### Transición a perfiles profesionales globales

Etapa 30/200 cerrada; siguiente etapa: perfiles profesionales globales. Prompt 18.0 define el modelo, la regla PASSED y la cobertura inteligente antes de cargar perfiles masivos.

Las 30 áreas y 200 nichos serán cubiertos primero por familias profesionales globales antes de crear perfiles individuales. Esta capa evita perfiles sueltos, ayuda a detectar huecos de cobertura y ordena la futura masa crítica de perfiles por valor económico, transversalidad, soporte, riesgo, tecnología y especialización sectorial.

Los primeros perfiles profesionales globales ya empiezan a cubrir la superficie 30/200: Prompt 18.2 crea 25 perfiles PASSED de empresa digital moderna, con cobertura inicial sobre estrategia, producto, marketing, ventas, datos, automatización, finanzas, customer success, contenido y calidad/riesgo.

El segundo bloque de perfiles globales amplía cobertura hacia pyme, local comercial y emprendedor. Prompt 18.3 suma perfiles de caja diaria, costos, compras, stock, turnos, WhatsApp, atención, promociones, reclamos, experiencia local y control de rentabilidad.
