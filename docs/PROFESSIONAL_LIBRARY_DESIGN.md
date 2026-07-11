# Biblioteca Profesional Global Multi-Área / Multi-Nicho / Hardware-Aware

**Estado**: Diseño propuesto (Prompt 16)
**Fecha**: 2026-07-10
**HEAD**: 4ca5b7b

## Propósito

IA_CORE debe pasar de "crear agentes por dominio" a "crear equipos profesionales por dominio". La biblioteca profesional es GLOBAL, no pertenece a un dominio específico. Los perfiles profesionales se definen primero en modo empresa digital y luego se asignan a áreas, nichos, dominios, equipos, presets, papers y modelos recomendados.

## Estado Actual Auditado

### Catálogos Globales Existentes

- **Áreas**: 30 (catalogs/areas.json)
- **Nichos**: 200 (catalogs/niches.json)
- **Roles**: 20 (catalogs/roles.json)
- **Especializaciones**: 80 (catalogs/specializations.json)

### Combinaciones Posibles

- **Combinaciones rol + especialización posibles**: 80 (cada especialización pertenece a un rol)
- **Combinaciones rol + especialización usadas en Lotería**: 30 (domains/loteria/profile_catalog.json)

## Estado del catálogo global antes de perfiles profesionales

Después de Tanda 2B, el catálogo global queda en:

- **30 áreas profesionales activas/PASSED**.
- **200 nichos activos/PASSED**.
- **0 nichos operativos en `proposed`, `draft` o `deprecated`**.
- **0 áreas nuevas pendientes de justificar para el objetivo 30/200**.

Este estado deja el terreno listo para Prompt 18. Los 200 nichos serán la base para mapear 80-100 perfiles profesionales globales, sus compatibilidades por área/nicho, posibles team templates y futuras model policies. Los nichos ya existen como opciones de creación de dominio, pero todavía no crean perfiles, presets, agentes ni papers por sí mismos.

## Base 30/200 lista para perfiles profesionales

La etapa de áreas/nichos queda cerrada como base operativa:

- El catálogo global llegó a **30 áreas profesionales** y **200 nichos PASSED**.
- Ningún nicho operativo está en `proposed`, `draft` o `deprecated`.
- No se crearon perfiles profesionales globales en Prompt 17.5.1.
- No se crearon presets, agentes ni papers.
- Los nichos son opciones usables de creación de dominio, no perfiles ejecutables.

Prompt 18 debe usar esta base para inventariar **80-100 perfiles profesionales globales PASSED**. Cada perfil futuro deberá:

- Conectarse con áreas y nichos compatibles.
- Declarar su función profesional con lenguaje global, no dependiente de Lotería.
- Definir luego `preset_seed`, `paper_seed` y `default_model_policy` o una política de recomendación equivalente.
- Evitar perfiles fantasma: si un perfil no tiene ruta hacia preset, paper y modelo, no debe aparecer como usable.

La biblioteca profesional global debe avanzar desde estos 200 nichos hacia perfiles reutilizables por múltiples dominios, team templates y model policies, manteniendo la regla PASSED.

### Perfiles y Presets por Dominio

**Dominio Lotería**:
- **Perfiles en profile_catalog.json**: 9 roles con 30 especializaciones
- **Presets en agent_presets.json**: 11 presets
- **Agentes existentes**: 11 (auditor_hostil, cazador_anomalias, estadistico_integral, gemini_cuantico, gestor_exposicion, gpt_auditor, integrador_central, nuevo_deepseek_saaop, simulador_escenarios, viejo_deepseek, viejo_lobo_rey)
- **Papers existentes**: 11 (uno por agente)

### Gaps Detectados

- **Perfiles sin preset**: 19 combinaciones rol+especialización en profile_catalog.json sin preset correspondiente
- **Presets sin profile asociado**: 0 (todos los presets mapean a combinaciones válidas)
- **Profiles que apuntan a roles/especializaciones inexistentes**: 0
- **Presets que apuntan a profiles inexistentes**: 0

### Tests Existentes

- test_agent_config_schema.py (19 tests)
- test_model_recommendation.py (40 tests)
- test_mejorar_papers_domain.py (11 tests)
- test_api_regenerate_paper.py (7 tests)

## Diagnóstico de Limitaciones

### Limitaciones Actuales

1. **Catálogo de nichos listo para perfiles profesionales**: Los 200 nichos actuales ya cubren la base PASSED esperada para empresa digital, pymes, operaciones, datos, growth, finanzas, legal básico, gestión de proyectos y áreas profesionales sectoriales. Las brechas restantes pasan a ser refinamientos posteriores, no bloqueantes para Prompt 18:
   - Data engineering y analítica avanzada
   - Seguridad operativa avanzada
   - Community management y operaciones de comunidad
   - Compliance sectorial específico
   - Nichos por industria regulada
   - Escalas enterprise y PMO avanzada

2. **Perfiles heredados de semillas anteriores**: Los perfiles actuales están fuertemente influenciados por el dominio Lotería, con roles como "auditor_hostil", "cazador_anomalias" que son específicos de ese dominio.

3. **Faltan perfiles profesionales de empresa digital**:
   - Operaciones
   - Ventas
   - Marketing
   - Automatización
   - Datos
   - Producto
   - Finanzas
   - Legal
   - Soporte
   - Contenido
   - Liderazgo
   - Estrategia
   - Investigación
   - Documentación
   - Sistemas
   - Gestión de conocimiento
   - Creatividad/diseño
   - Comunidad
   - Educación/capacitación

4. **Falta estructura global reusable**: No existe una biblioteca profesional global que pueda ser heredada por múltiples dominios.

5. **Falta recomendación de modelo por perfil profesional**: Los presets actuales tienen `recommended_provider` y `recommended_model` en null.

6. **Hay perfiles seleccionables que no podrían crear agentes operativos**: 19 combinaciones en profile_catalog.json sin preset correspondiente.

7. **Combinaciones rol + especialización no usadas**: 50 combinaciones posibles no están siendo utilizadas en Lotería.

8. **Restricciones para escalar**: La estructura actual obliga a duplicar presets por dominio de forma innecesaria.

9. **El sistema actual permite técnicamente derivar profile_catalog y agent_presets desde una biblioteca global**: Sí, es técnicamente posible mediante scripts de generación.

## Diseño Futuro de Biblioteca Profesional Global

### Ubicación Propuesta

- `catalogs/professional_profiles.json` — Biblioteca global de perfiles profesionales
- `catalogs/professional_archetypes.json` — Arquetipos profesionales/psicológicos
- `catalogs/team_templates.json` — Plantillas de equipos profesionales
- `catalogs/profile_model_policies.json` — Políticas de modelo por perfil

### Estructura de professional_profiles.json

```json
{
  "schema_version": "1.0",
  "profiles": [
    {
      "professional_profile_id": "automation_architect",
      "name": "Arquitecto de automatizaciones",
      "description": "Diseña e implementa workflows automatizados, integraciones de APIs y pipelines de datos para mejorar eficiencia operativa.",
      "role_id": "arquitecto_sistemas",
      "specialization_id": "arquitectura_componentes",
      "archetype": "systematic_builder",
      "seniority": "senior",
      "capabilities": [
        "Diseño de workflows automatizados",
        "Integración de APIs REST/SOAP",
        "Orquestación de procesos",
        "Documentación técnica de automatizaciones"
      ],
      "limits": [
        "No reemplaza validación humana en decisiones críticas",
        "Requiere revisión de seguridad para integraciones sensibles"
      ],
      "compatible_area_ids": [
        "tecnologia_sistemas_telecomunicaciones",
        "administracion_contabilidad_finanzas",
        "comercial_ventas_negocios"
      ],
      "compatible_niche_ids": [
        "desarrollo_software",
        "datos_bi",
        "prospeccion_b2b"
      ],
      "workload": "heavy",
      "reasoning_need": "high",
      "default_model_policy": "cloud_preferred",
      "preset_seed": "automation_architect_preset",
      "paper_seed": "automation_architect_paper",
      "status": "active",
      "tags": ["automation", "integration", "workflows"],
      "version": "1.0",
      "created_from": "design",
      "domain_overrides": {},
      "recommended_team_roles": ["analista", "validador"],
      "validation_rules": [
        "Requiere revisión de seguridad antes de producción",
        "Debe documentar rollback manual"
      ],
      "visibility": "public",
      "requires_tools": ["api_client", "workflow_engine"],
      "requires_memory": true,
      "requires_human_confirmation": true
    }
  ]
}
```

### Estructura de professional_archetypes.json

```json
{
  "schema_version": "1.0",
  "archetypes": [
    {
      "archetype_id": "systematic_builder",
      "name": "Constructor sistemático",
      "description": "Enfoque metódico en construcción de sistemas robustos, escalables y mantenibles.",
      "cognitive_style": "estructurado",
      "strengths": ["planificación", "documentación", "escalabilidad"],
      "weaknesses": ["velocidad inicial", "flexibilidad ante cambios imprevistos"],
      "preferred_roles": ["arquitecto_sistemas", "planificador", "coordinador"]
    }
  ]
}
```

### Estructura de team_templates.json

```json
{
  "schema_version": "1.0",
  "templates": [
    {
      "template_id": "digital_transformation_team",
      "name": "Equipo de transformación digital",
      "description": "Equipo multidisciplinario para proyectos de automatización y optimización de procesos.",
      "compatible_area_ids": ["tecnologia_sistemas_telecomunicaciones"],
      "compatible_niche_ids": ["desarrollo_software"],
      "roles": [
        {
          "professional_profile_id": "automation_architect",
          "team_role": "lead",
          "required": true
        },
        {
          "professional_profile_id": "data_analyst",
          "team_role": "analyst",
          "required": true
        },
        {
          "professional_profile_id": "process_auditor",
          "team_role": "validator",
          "required": false
        }
      ]
    }
  ]
}
```

### Estructura de profile_model_policies.json

```json
{
  "schema_version": "1.0",
  "policies": [
    {
      "policy_id": "heavy_reasoning_cloud",
      "name": "Razonamiento pesado en cloud",
      "workload": "heavy",
      "reasoning_need": "high",
      "execution_preference": "cloud_preferred",
      "local_allowed": false,
      "cloud_allowed": true,
      "fallback_policy": "cloud_required_if_hardware_limited",
      "user_explanation": "Este perfil requiere razonamiento fuerte para workflows complejos y análisis profundos. Se recomienda ejecución en cloud para garantizar capacidad suficiente.",
      "default_provider": "openai",
      "default_model": "gpt-4o"
    }
  ]
}
```

## Regla de Presets Obligatorios

Todo perfil profesional seleccionable para crear agente debe tener:

- `preset_seed` — Referencia al preset en agent_presets.json
- `paper_seed` — Referencia al paper seed
- `role_id` — Rol válido del catálogo global
- `specialization_id` — Especialización válida del catálogo global
- `default_model_policy` — Política de modelo definida
- `status: active` — Estado activo

No puede haber perfiles visibles/usables sin preset. Si un perfil existe como borrador pero no tiene preset_seed o paper_seed, debe quedar como:

```json
"status": "draft"
```

o

```json
"status": "disabled"
```

y no debe aparecer como opción usable para crear agentes.

## Diseño de Política de Modelo por Perfil

### Campos de Política

- **workload**: `light` / `medium` / `heavy` / `critical`
- **reasoning_need**: `low` / `medium` / `high`
- **execution_preference**: `local_allowed` / `cloud_preferred` / `cloud_required` / `auto`
- **local_allowed**: boolean
- **cloud_allowed**: boolean
- **fallback_policy**: Estrategia si el hardware local es limited
- **user_explanation**: Explicación visible para el usuario
- **default_provider**: Provider recomendado por defecto
- **default_model**: Modelo recomendado por defecto
- **compatibilidad con hardware_profile**: Integración con el sistema hardware-aware existente
- **compatibilidad con model_recommendation**: Integración con el recomendador existente

### Regla Obligatoria

Si un perfil requiere razonamiento alto y el hardware local detectado es limited, debe recomendar cloud por defecto.

### Ejemplos Conceptuales

#### Arquitecto de automatizaciones

```json
{
  "workload": "heavy",
  "reasoning_need": "high",
  "execution_preference": "cloud_preferred",
  "local_allowed": false,
  "cloud_allowed": true,
  "fallback_policy": "cloud_required_if_hardware_limited",
  "user_explanation": "Requiere razonamiento fuerte para workflows, APIs e integración de datos complejos.",
  "default_provider": "openai",
  "default_model": "gpt-4o"
}
```

#### Documentador operativo

```json
{
  "workload": "light",
  "reasoning_need": "medium",
  "execution_preference": "auto",
  "local_allowed": true,
  "cloud_allowed": true,
  "fallback_policy": "local_if_available_else_cloud",
  "user_explanation": "Puede funcionar con modelo local si el hardware alcanza. Cloud como fallback.",
  "default_provider": "ollama",
  "default_model": "llama3.2"
}
```

#### Auditor de riesgo crítico

```json
{
  "workload": "critical",
  "reasoning_need": "high",
  "execution_preference": "cloud_required",
  "local_allowed": false,
  "cloud_allowed": true,
  "fallback_policy": "block_if_no_cloud",
  "user_explanation": "Requiere precisión, razonamiento fuerte y bajo margen de error. Solo cloud.",
  "default_provider": "openai",
  "default_model": "gpt-4o"
}
```

## Relación Core / Dominio / Agente / Patrimonio Compartido

### Clasificación

- **Biblioteca Profesional Global** (`catalogs/professional_profiles.json`): **Patrimonio compartido** — Definiciones globales reusables por todos los dominios
- **Arquetipos Profesionales** (`catalogs/professional_archetypes.json`): **Patrimonio compartido** — Modelos psicológicos/cognitivos reusables
- **Plantillas de Equipos** (`catalogs/team_templates.json`): **Patrimonio compartido** — Configuraciones de equipos reusables
- **Políticas de Modelo** (`catalogs/profile_model_policies.json`): **Patrimonio compartido** — Políticas de ejecución reusables
- **profile_catalog.json por dominio**: **Dominio** — Hereda y adapta perfiles globales al contexto específico
- **agent_presets.json por dominio**: **Dominio** — Hereda y adapta presets globales al contexto específico
- **Papers generados**: **Agente** — Identidad específica de cada agente operativo

### ADR Propuesta

**ADR-020 — La Biblioteca Profesional es patrimonio compartido global y los dominios heredan perfiles compatibles**

**Estado**: Propuesto

**Contexto**:
IA_CORE evolucionó desde un dominio específico (Lotería) a un framework multi-dominio. Los perfiles profesionales actuales están fuertemente influenciados por Lotería y no hay una estructura global reutilizable.

**Decisión**:
- Los perfiles profesionales no nacen dentro de un dominio puntual
- Se definen globalmente en `catalogs/professional_profiles.json`
- Los dominios seleccionan o heredan perfiles compatibles vía `profile_catalog.json`
- Todo perfil usable debe tener preset_seed y paper_seed
- Toda recomendación de modelo debe considerar carga cognitiva, tipo de tarea y hardware
- Los dominios pueden tener overrides, pero no deben duplicar la definición global sin necesidad

**Consecuencias**:
- Permite escalar a múltiples dominios sin duplicar definiciones
- Facilita la creación de nuevos dominios reusando perfiles existentes
- Mantiene consistencia en la definición de roles y especializaciones
- Permite evolucionar la biblioteca global sin impactar dominios existentes

## Áreas/Nichos Sin Límite Fijo

No hay límite fijo de nichos por área. Si la lista crece mucho, primero se mide y después se decide cómo agrupar, filtrar, paginar o versionar. No se imponen restricciones artificiales.

## Status Operativo de Áreas/Nichos

Las áreas y nichos pueden tener un campo `status` opcional con valores:

- **proposed**: Existe como parte del universo objetivo, no necesariamente usable
- **draft**: Tiene estructura parcial, todavía no usable
- **active**: Solo debe usarse para elementos compatibles con flujo operativo actual o heredados por compatibilidad
- **deprecated**: Existe pero no debe sugerirse para nuevos usos

Los catálogos actuales (areas.json, niches.json) no requieren migración. Si el campo `status` no está presente, se asume compatibilidad con el estado actual.

## Compatible Business Scales

Las áreas y nichos pueden tener un campo `compatible_business_scales` opcional con valores:

- micro
- local_business
- freelancer
- pyme
- company
- enterprise
- department
- research_team
- experimental_domain

Esta capa prepara una futura segunda capa de adaptación por tipo de negocio, pero no se implementa todavía.

## Contrato de Operacionalización

Los nichos pueden tener un campo `operationalization_contract` opcional que define:

- `needs_professional_profiles`: bool
- `needs_presets`: bool
- `needs_paper_seed`: bool
- `needs_model_policy`: bool
- `can_create_agent_when`: string
- `can_join_team_when`: string
- `blocked_by`: list[str]

Este contrato asegura que ningún nicho se marque como `active` si no tiene trazabilidad operativa completa hacia perfiles profesionales, presets, papers y políticas de modelo.

## Regla: Active No Debe Usarse Como Decoración

El status `active` no debe usarse como decoración. Un nicho solo puede marcarse como `active` si:

1. Tiene professional_profile_id válido
2. Tiene preset_seed válido
3. Tiene paper_seed válido
4. Tiene default_model_policy definido
5. Puede crear agente operativo sin errores

Si falta cualquiera de estos, el nicho debe quedar como `draft` o `proposed`.

## Qué Queda Fuera de Alcance

- Integración n8n
- Orquestador de equipos
- UI de regeneración de paper
- Semáforo/compatibilidad visual HUD
- Validación cross-platform
- Implementación masiva de perfiles
- Implementación masiva de presets

## Riesgos de Implementación Masiva

- **Complejidad de migración**: Migrar los perfiles actuales de Lotería a la estructura global puede requerir ajustes significativos
- **Validación de compatibilidad**: Asegurar que todos los dominios existentes puedan seguir operando con la nueva estructura
- **Performance**: Si la biblioteca crece significativamente, puede impactar el tiempo de carga y filtrado
- **Consistencia**: Mantener consistencia entre la biblioteca global y los overrides por dominio

## Roadmap de Prompts Siguientes

- **Prompt 16** — Auditoría y diseño de Biblioteca Profesional Global (actual)
- **Prompt 17** — Reporte y expansión de áreas/nichos sin límite fijo
- **Prompt 18** — Inventario de perfiles profesionales tipo empresa digital
- **Prompt 19** — Matriz Perfil Profesional → Áreas/Nichos compatibles
- **Prompt 20** — Recomendación provider/model por perfil profesional
- **Prompt 21** — Generador de profile_catalog por dominio desde biblioteca global
- **Prompt 22** — Generador de agent_presets por dominio desde biblioteca global
- **Prompt 23** — Plantillas de equipos profesionales por dominio/nicho
- **Prompt 24** — Validación end-to-end: dominio nuevo con profesionales, presets, papers y modelos por defecto
- **Prompt 25** — Cierre del libro: auditoría, tests, documentación y deudas futuras

## Decisiones Pendientes

- ¿Cómo manejar versionado de perfiles globales?
- ¿Cómo resolver conflictos entre overrides de dominio y biblioteca global?
- ¿Qué criterios usar para activar/desactivar perfiles en un dominio?
- ¿Cómo validar que un perfil es compatible con un nicho específico?
- ¿Cómo manejar la migración de los perfiles actuales de Lotería a la nueva estructura?

## Estimación de Escala

- **Perfiles profesionales objetivo**: 50-100 para cubrir áreas principales de empresa digital
- **Nichos objetivo**: 150-200 para cubrir especializaciones por área
- **Plantillas de equipos**: 20-30 para configuraciones comunes
- **Políticas de modelo**: 10-15 para cubrir patrones de workload/reasoning

## Recuperación Futura de Perfiles Históricos de Lotería

### Contexto

Durante la migración al sistema profesional global, algunos perfiles psicológicos/técnicos históricos del dominio Lotería no volvieron a existir formalmente como combinación seleccionable rol + especialización. Existe un listado histórico en formato docx con perfiles que se quiere recuperar más adelante en su debido momento.

### Perfiles Históricos Candidatos a Recuperación

Los siguientes perfiles del listado histórico deben considerarse para recuperación en Prompt 18.1 o subpasos posteriores:

**Ya existen formalmente como agentes/presets correctos:**
- Estadístico Integral → `analista` + `analisis_datos` (preset: loteria_analista_estadistico_integral)
- Visionario Matemático → `simulador` + `simulacion_escenarios` (preset: loteria_simulador_escenarios)
- Auditor Hostil → `auditor` + `auditoria_consistencia` (preset: loteria_auditor_hostil)
- Cazador de Anomalías → `detector_anomalias` + `deteccion_anomalias` (preset: loteria_detector_cazador_anomalias)
- Gestor de Bankroll → `gestor_riesgo` + `gestion_exposicion` (preset: loteria_gestor_exposicion)
- Integrador Central → `integrador_central` + `integracion_perspectivas` (preset: loteria_integrador_central)
- Archivista → `archivista` + `archivo_documental` (preset: loteria_archivista_trazabilidad)

**Faltan o requieren mapeo futuro:**
- Intuitivo Obsesivo
- Persistente Metódico
- Arquitecto de Sistemas
- Competidor Estratégico
- Místico / Simbólico
- Hipercontrolado
- Destructor
- Minimalista de Señal
- Psicología de Masas
- Intuitivo Caótico
- Antisistema
- Apostador Profesional
- Jugador Obsesivo
- Analista de Sesgos → Parcialmente cubierto por `critico` + `deteccion_sesgos`
- Escéptico Radical
- Detector de Patrones → Parcialmente cubierto por `analista` + `analisis_patrones` (inactivo)
- Observador Conductual → Existe como role global `observador_conductual`
- Experimentalista
- Analista Temporal → Existe como `analista` + `analisis_temporal` (inactivo)
- Historiador
- Geómetra
- Integrador Central → Ya existe

### Reglas de Recuperación

1. **No cargar como prompts viejos directos**: Los perfiles históricos no deben migrarse como prompts crudos del sistema anterior. Deben traducirse al nuevo formato profesional.

2. **Migración al nuevo formato**: Cada perfil recuperado deberá tener:
   - `role_id` válido del catálogo global
   - `specialization_id` válida del catálogo global
   - `professional_profile_id` único
   - `preset_seed` en agent_presets.json
   - `paper_seed` para generación de paper
   - `default_model_policy` definido
   - `status: active` o `draft` según completitud

3. **Perfiles sin información suficiente**: Si un perfil histórico no tiene suficiente información para mapearlo a role_id + specialization_id de forma confiable, debe quedar como `status: draft` hasta que se complete la definición.

4. **Este trabajo corresponde a Prompt 18.1**: La recuperación masiva de perfiles históricos no es parte de este prompt (17.1.1). Debe abordarse en un prompt específico dedicado a esa tarea.

### Agentes Legacy Existentes

Los siguientes agentes config existen en `domains/loteria/agents/config/` pero no tienen combinación formal role+specialization en el sistema nuevo. Deben considerarse legacy y no deben romperse, pero tampoco deben usarse como referencia para nuevos agentes:

- `gemini_cuantico` → Rol histórico "analyst_zones"
- `gpt_auditor` → Rol histórico "critic"
- `nuevo_deepseek_saaop` → Agente experimental
- `viejo_deepseek` → Agente experimental
- `viejo_lobo_rey` → Rol histórico "analyst_human"

Estos agentes deben documentarse como legacy y mantenerse operativos por compatibilidad, pero no deben expandirse ni usarse como base para nuevos desarrollos sin migración previa al formato profesional.

## Alineación de Datos Existentes (Prompt 17.1.1)

### Inconsistencias Detectadas y Resueltas

**Profiles sin preset (19 combinaciones):**
- Se marcaron como `activo: false` con nota explicativa en `profile_catalog.json`
- Estas especializaciones no son seleccionables hasta que se creen presets operativos
- No se eliminaron del catálogo para preservar el diseño estructural

**Presets sin provider/model (11 presets):**
- No es inconsistencia técnica: el diseño delega recomendación a `core/model_recommendation.py`
- El sistema calcula dinámicamente provider/model según hardware y workload
- No se requiere modificación en este prompt

**Agentes legacy sin preset (5 agentes):**
- Se documentan como legacy (gemini_cuantico, gpt_auditor, nuevo_deepseek_saaop, viejo_deepseek, viejo_lobo_rey)
- No tienen combinación formal role+specialization
- Se mantienen operativos por compatibilidad pero no se expanden

**Roles/Especializaciones:**
- Todos los IDs usados en profiles y presets son válidos
- No requiere corrección

### Regla Vigente

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

Si falta una pieza obligatoria, el elemento debe marcarse como `activo: false` o `draft` y no aparecer como opción usable.

### Elementos Draft/Legacy

- **19 especializaciones** en `profile_catalog.json` marcadas como `activo: false` por falta de preset
- **5 agentes legacy** sin combinación formal role+specialization (documentados, no eliminados)
- **11 papers** con naming mismatch (sufijo `_paper`) - deuda técnica menor, no bloquea operatividad

---

## Regla PASSED: No existen catálogos fantasma

### Contexto

IA_CORE puede documentar propuestas, borradores e ideas en reportes y documentos de diseño, pero los catálogos operativos deben exponer solo elementos PASSED/active con camino real hacia uso. Elementos incompletos deben clasificarse como recuperar_para_operar, legacy, baja/desactivado o backlog_documental, y no pueden aparecer como opciones usables.

### Universo Exploratorio vs Catálogo Operativo

IA_CORE distingue entre:

**A. Universo exploratorio / backlog documental:**
- Ideas, propuestas, borradores, perfiles históricos, nichos candidatos
- Viven en: `docs/`, reportes, backlog futuro, documentos de diseño, Prompt 18.1 o futuros subprompts
- No aparecen como opción usable

**B. Catálogo operativo:**
- Solo elementos PASSED
- Lo que está en catálogo operativo debe poder avanzar hacia uso real

### Semántica PASSED

**Para áreas/nichos:**
Un área o nicho puede estar PASSED solo si:
- Tiene id válido
- Tiene nombre
- Tiene descripción
- Está asociado correctamente
- No está duplicado
- No rompe loader
- Tiene sentido operativo
- Si es nicho, tiene expected_profile_types concretos o justificación clara
- Tiene model_policy_need si corresponde
- Tiene compatible_business_scales si corresponde
- Tiene operationalization_contract si corresponde
- No se presenta como usable si todavía no puede conectarse a perfiles/presets/papers/model policies

**Para perfiles/presets:**
Un perfil puede estar PASSED solo si:
- Tiene role_id válido
- Tiene specialization_id válida
- Tiene preset operativo
- Tiene paper_seed o paper asociado
- Tiene default_model_policy o recomendación dinámica válida
- Puede crear agente operativo
- Pasa tests de consistencia

### Equivalencia Técnica

- `activo: true` = PASSED operativo
- `activo: false` = baja/desactivado temporal
- `status: active` (si se usa en futuro) = PASSED operativo
- `status: proposed/draft` = estados de transición para clasificar y decidir, no usables
- En loaders operativos (`active_only=True`), `proposed`, `draft` y `deprecated` quedan fuera de las respuestas usables aunque `activo` sea `true`

### Regla No Negociable

Ningún perfil/nicho/preset puede estar visible como usable sin cumplir reglas de consistencia. El soporte técnico para proposed/draft NO existe para acumular ideas dormidas o catálogos fantasma. Existe para convertir lo que ya está creado en algo operativo, o para decidir formalmente que debe darse de baja, quedar legacy o pasar a recuperación posterior.

### Tabla de Decisión de Elementos Existentes

| Tipo de Elemento | Cantidad | Estado Actual | Categoría de Decisión | Motivo | Piezas Faltantes | Subprompt Sugerido | Aparece como Usable |
|---|---|---|---|---|---|---|---|
| Áreas existentes | 30 | activo: true | PASSED | Operativas, validadas | Ninguna | - | Sí |
| Nichos existentes | 200 | activo: true | PASSED | Operativos, validados | Ninguna | - | Sí |
| Profiles activos Lotería | 11 | activo: true | PASSED | Tienen preset operativo | Ninguna | - | Sí |
| Profiles inactivos Lotería | 19 | activo: false | baja/desactivado temporal | Sin preset operativo | Preset | Prompt 18.1 / Prompt 20 | No |
| Presets existentes | 11 | activo: true | PASSED | Tienen paper_seed y trazabilidad | Ninguna | - | Sí |
| Agentes config existentes | 11 | Config válido | - | Total agentes en domains/loteria/agents/config/ | - | - | - |
| Agentes PASSED para flujo nuevo | 6 | Config válido | PASSED | Tienen trazabilidad completa profile→preset→paper/model policy | Ninguna | - | Sí |
| Agentes legacy / recuperar_para_operar | 5 | Config válido | legacy / recuperar_para_operar | Ejecutables pero sin combinación formal role+specialization | Role+specialization formales | Prompt 18.1 | No |
| Papers existentes | 11 | JSON válido | PASSED | Corresponden a agentes | Ninguna | - | Sí |
| Perfiles históricos documentados | 22 | Solo en docs | backlog_documental | Listados para recuperación futura | Preset, paper, model policy | Prompt 18.1 | No |

**Nota**: Los 5 agentes legacy (gemini_cuantico, gpt_auditor, nuevo_deepseek_saaop, viejo_deepseek, viejo_lobo_rey) son subset de los 11 agentes config existentes. Son ejecutables por historia pero no tienen trazabilidad completa para el flujo nuevo.

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
