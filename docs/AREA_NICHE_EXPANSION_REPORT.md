# Reporte de Expansión de Áreas y Nichos Profesionales

**Estado**: Propuesto (Prompt 17)
**Fecha**: 2026-07-10
**HEAD**: b421ff1

## Propósito del Reporte

Este reporte define el universo objetivo de áreas y nichos profesionales para IA_CORE, sin límites artificiales de cantidad por área, con trazabilidad explícita hacia perfiles profesionales, presets, paper seeds, políticas de modelo y equipos. El objetivo es preparar la estructura necesaria para que Prompt 18 pueda crear perfiles profesionales de forma sistemática y operativa.

## Estado Actual de Áreas/Nichos

### Auditoría Real

- **Áreas actuales**: 26 (catalogs/areas.json)
- **Nichos actuales**: 94 (catalogs/niches.json)
- **Promedio de nichos por área**: 3.6
- **Áreas con más nichos**: 8 áreas con 5 nichos cada una
- **Áreas con menos nichos**: 18 áreas con 3 nichos cada una

### Distribución por Área

**Áreas con 5 nichos (prioridades actuales)**:
- comercial_ventas_negocios: 5
- administracion_contabilidad_finanzas: 5
- tecnologia_sistemas_telecomunicaciones: 5
- atencion_cliente_call_center_telemarketing: 5
- gastronomia_turismo: 5
- marketing_publicidad: 5
- legales: 5
- educacion_docencia_investigacion: 5

**Áreas con 3 nichos**:
- produccion_manufactura: 3
- abastecimiento_logistica: 3
- oficios_otros: 3
- salud_medicina_farmacia: 3
- recursos_humanos_capacitacion: 3
- ingenierias: 3
- ingenieria_civil_construccion: 3
- departamento_tecnico: 3
- secretarias_recepcion: 3
- gerencia_direccion_general: 3
- diseno: 3
- mineria_petroleo_gas: 3
- aduana_comercio_exterior: 3
- seguros: 3
- comunicacion_relaciones_institucionales_publicas: 3
- sociologia_trabajo_social: 3
- enfermeria: 3
- naviero_maritimo_portuario: 3

### Nichos Específicos Detectados

- **Nichos específicos de Lotería**: 1 (analisis_loteria_juegos_azar en oficios_otros)
- **Nichos duplicados o parecidos**: No detectados
- **Nichos útiles para empresa digital**: Parcialmente cubiertos en tecnología, marketing, ventas, finanzas

### Diagnóstico de Cobertura Actual

**Áreas artificialmente incompletas**:
- tecnologia_sistemas_telecomunicaciones: Solo 5 nichos para un área que debería cubrir desarrollo, DevOps, seguridad, datos, automatización, integraciones, cloud, etc.
- marketing_publicidad: Solo 5 nichos para un área que debería cubrir growth, SEO, contenido, paid media, branding, analytics, etc.
- recursos_humanos_capacitacion: Solo 3 nichos para un área que debería cubrir talento, cultura, payroll, benefits, L&D, etc.
- gerencia_direccion_general: Solo 3 nichos para un área que debería cubrir estrategia, ejecutivos, board, transformación, etc.

**Nichos faltantes para empresa digital completa**:
- Automatización de procesos
- Growth hacking
- Product management
- Data engineering
- DevOps
- Community management
- Customer success
- Business intelligence avanzado
- Revenue operations
- Sales enablement
- Customer experience
- UX/UI design
- Product operations
- Technical writing
- Knowledge management
- AI/ML engineering
- Security operations
- Compliance automation
- Supply chain digital
- E-commerce operations

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

1. Cargar una primera expansión de 50 nichos con metadatos operativos completos
2. Marcar nichos como `proposed` o `draft` según su estado de preparación
3. Validar que cada nicho tenga `expected_profile_types` definidos
4. Validar que cada nicho tenga `model_policy_need` definido
5. Validar que cada nicho tenga `operationalization_contract` definido
6. Mantener compatibilidad con los 94 nichos existentes
7. Usar los nuevos tests para validar que la expansión no rompe el loader
