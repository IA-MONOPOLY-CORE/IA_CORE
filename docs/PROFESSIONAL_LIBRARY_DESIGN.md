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

## Modelo de Perfil Profesional Global PASSED

Un Perfil Profesional Global es una entidad reutilizable de IA_CORE que define un tipo de profesional antes de convertirse en agente. No es un prompt, no es un preset, no es un paper y no es una instancia ejecutable. Su tarea es ordenar identidad profesional, utilidad, cobertura, límites y trazabilidad para que después pueda mapearse a dominios, equipos, presets, papers, políticas de modelo y agentes operativos.

El perfil global existe para responder con claridad:

- Para qué sirve.
- Qué problema resuelve.
- A qué negocio, proyecto o dominio puede ayudar.
- Cómo genera, protege o mejora valor económico.
- Cómo puede volverse operativo sin inventar piezas fantasma.

### Diferencia entre conceptos

- **Área**: campo amplio de actividad profesional, por ejemplo tecnología, ventas, finanzas, salud o legal.
- **Nicho**: caso de uso, subcampo o necesidad operativa dentro de un área.
- **Perfil Profesional Global**: tipo de profesional reutilizable que puede aportar en varias áreas y nichos.
- **Rol**: función técnica u operativa que IA_CORE usa para clasificar agentes y capacidades cognitivas.
- **Especialización**: afinación concreta de un rol para una función más precisa.
- **Preset**: configuración operativa para crear o ejecutar un agente.
- **Paper seed**: base documental o marco de conocimiento que profesionaliza al agente.
- **Agente**: instancia ejecutable concreta, creada desde perfil, preset, paper y configuración.
- **Equipo**: conjunto coordinado de perfiles o agentes para lograr un objetivo.
- **Model policy**: política que orienta el tipo de modelo según carga cognitiva, razonamiento, hardware, privacidad, latencia y costo.

### Campos obligatorios del perfil global

Cada perfil futuro en `catalogs/professional_profiles.json` debe declarar estos campos:

- `id`: identificador estable, `snake_case`, global y no dependiente de un único dominio.
- `nombre`: nombre visible en español claro para usuarios no técnicos.
- `descripcion`: explicación concreta de qué hace el perfil y para qué sirve.
- `familia_profesional`: agrupador de alto nivel. Valores esperados iniciales: `estrategia_direccion`, `operaciones_procesos`, `producto_ux`, `marketing_growth`, `ventas_revenue`, `datos_analytics`, `automatizacion_tecnologia`, `finanzas_administracion`, `legal_compliance`, `rrhh_capacitacion`, `soporte_customer_success`, `investigacion_analisis`, `calidad_riesgo`, `industria_oficios`, `dominio_especializado`.
- `tipo_perfil`: clase funcional del perfil. Valores esperados iniciales: `estrategico`, `operativo`, `tecnico`, `analitico`, `creativo`, `comercial`, `administrativo`, `soporte`, `compliance`, `investigacion`, `coordinacion`, `mixto`.
- `areas_compatibles`: lista de `area_id` existentes en `catalogs/areas.json`.
- `nichos_compatibles`: lista de `niche_id` existentes en `catalogs/niches.json`; debe ser realista y no inflada para simular cobertura.
- `capacidades_principales`: lista concreta de capacidades que el perfil puede ejecutar o asistir.
- `limites`: lista de cosas que no debe hacer, condiciones donde no conviene usarlo o decisiones que requieren humano.
- `seniority`: `junior`, `semi_senior`, `senior`, `lead`, `principal` o `executive`.
- `compatible_business_scales`: `emprendedor`, `local_comercial`, `pyme`, `empresa_mediana`, `enterprise`, `investigacion` o `dominio_especializado`.
- `cognitive_load`: `baja`, `media`, `alta` o `muy_alta`.
- `reasoning_style`: `operativo`, `analitico`, `creativo`, `estrategico`, `critico`, `investigativo`, `coordinador`, `tecnico` o `mixto`.
- `economic_value`: explicación de cómo el perfil aumenta ventas, reduce costos, mejora margen, evita riesgos, ordena operaciones, acelera ejecución, mejora retención, mejora decisiones o convierte ideas en activos vendibles.
- `value_creation_paths`: lista de caminos concretos de valor, por ejemplo optimización de precios, campañas comerciales, automatización de tareas, reducción de errores, creación de activos digitales, mejora de conversión, análisis de rentabilidad o prevención de riesgos.
- `default_model_policy`: política esperada de modelo. No define todavía un modelo concreto.
- `expected_role_id`: `role_id` esperado si ya existe; si no existe, se debe declarar un tipo requerido antes de normalizar.
- `expected_specialization_id`: `specialization_id` esperada si ya existe; si no existe, se debe declarar un tipo requerido antes de normalizar.
- `required_role_type`: descripción obligatoria cuando el `role_id` aún no existe.
- `required_specialization_type`: descripción obligatoria cuando la `specialization_id` aún no existe.
- `preset_seed_expected`: nombre o idea del preset futuro; no crea el preset.
- `paper_seed_expected`: nombre o idea del paper seed futuro; no crea el paper.
- `team_roles`: forma de participar en equipos: `lider`, `especialista`, `auditor`, `ejecutor`, `soporte`, `integrador`, `validador` o `investigador`.
- `coverage_notes`: explica qué superficie cubre el perfil y cuándo debería dividirse en perfiles más específicos.
- `status`: `active` solo si el perfil está PASSED; estados transicionales no son usables.
- `activo`: booleano operativo.
- `notes`: observaciones útiles, sin texto decorativo.

### Regla PASSED para perfiles

Un Perfil Profesional Global PASSED debe cumplir:

- Tiene `id` único, estable y no ambiguo.
- Tiene `nombre` claro y `descripcion` útil.
- Pertenece a una `familia_profesional`.
- Tiene `tipo_perfil` válido.
- Declara áreas compatibles reales.
- Declara nichos compatibles reales.
- Tiene capacidades principales concretas.
- Tiene límites explícitos.
- Tiene seniority.
- Tiene escalas de negocio compatibles.
- Tiene carga cognitiva.
- Tiene estilo de razonamiento.
- Explica valor económico.
- Declara caminos concretos de creación de valor.
- Tiene `default_model_policy` esperada.
- Tiene `expected_role_id` o `required_role_type`.
- Tiene `expected_specialization_id` o `required_specialization_type`.
- Tiene `preset_seed_expected`.
- Tiene `paper_seed_expected`.
- Tiene `coverage_notes`.
- Puede mapearse luego a `role_id`, `specialization_id`, preset, paper y model policy.
- No es decorativo.
- No existe solo para completar un número.

Regla no negociable: si un perfil no puede avanzar hacia operación real, no debe entrar como PASSED.

### Masa crítica inicial y cobertura inteligente

La meta de 80-100 perfiles profesionales es masa crítica inicial, no techo. IA_CORE no debe crear perfiles para cumplir un número; debe crearlos para cubrir necesidades reales.

La auditoría de cobertura futura debe medir perfiles contra:

- 30 áreas.
- 200 nichos.
- Escalas de negocio.
- Tipos de usuario.
- Tipos de equipo.
- Complejidad operativa.
- Necesidades de modelo.
- Posibilidad real de preset, paper y agente.
- Valor económico real.

Si la cobertura queda corta, el sistema debe recomendar expansión a 120, 150, 200 o la cantidad razonable que resulte usable y mantenible. Si la cobertura queda demasiado genérica, algunos perfiles deben dividirse. Si hay demasiada superposición, algunos perfiles deben fusionarse. La auditoría manda sobre el número.

Criterios futuros de auditoría:

- Cobertura por área.
- Cobertura por nicho.
- Cobertura por escala de negocio.
- Cobertura por tipo de valor económico.
- Cobertura por tipo de tarea.
- Cobertura por model policy.
- Cobertura por equipo.
- Solapamiento entre perfiles.
- Huecos de cobertura.
- Recomendación de expansión, fusión o división.

### Ubicación recomendada del catálogo global

La ubicación recomendada para Prompt 18.1/18.2 es:

- `catalogs/professional_profiles.json`: catálogo global PASSED de perfiles profesionales reutilizables.

Archivos futuros relacionados:

- `catalogs/professional_profile_families.json`: normalización opcional de familias si el catálogo crece.
- `catalogs/profile_model_policies.json`: políticas de modelo formalizadas por Prompt 20.
- `catalogs/team_templates.json`: plantillas de equipos profesionales.

En Prompt 18.0 no se crea el catálogo masivo. El contrato vive en este documento hasta que Prompt 18.1/18.2 cargue perfiles reales.

### Relación con roles y especializaciones

La base actual contiene 20 roles globales y 80 especializaciones globales, todos activos. Esa base alcanza para iniciar una masa crítica, pero no debe forzar perfiles artificiales. Algunos perfiles futuros mapearán directo a `expected_role_id` y `expected_specialization_id`; otros necesitarán `required_role_type` o `required_specialization_type` hasta que Prompt 18.8 normalice los gaps.

La normalización de roles/especializaciones conviene hacer durante y después de cargar bloques de perfiles: primero se detectan huecos reales, luego se agregan roles o especializaciones si la cobertura lo justifica. Para evitar perfiles no seleccionables, ningún perfil PASSED debe quedar sin ruta futura a rol, especialización, preset seed, paper seed y model policy.

Los perfiles globales son patrimonio compartido. Los perfiles específicos de dominio viven en `domains/*/profile_catalog.json` y solo adaptan o restringen perfiles globales cuando corresponde. Ningún dominio específico debe volver a ser centro simbólico del sistema.

### Relación con model policies

Cada perfil futuro debe declarar una política de modelo esperada. Prompt 18 no fija modelos concretos, pero deja categorías preliminares:

- `local_light`
- `local_standard`
- `local_heavy`
- `cloud_reasoning`
- `cloud_low_latency`
- `hybrid`
- `privacy_sensitive`
- `long_context`
- `multimodal`
- `batch_analysis`
- `cost_sensitive`
- `high_reliability`
- `fast_iteration`
- `offline_capable`
- `human_review_required`

Prompt 20 debe formalizar estas políticas e integrarlas con recomendación hardware-aware, costo, privacidad, latencia y confiabilidad.

### Relación con dominios específicos e históricos

Todo dominio específico existente o futuro debe tratarse como un dominio más dentro del sistema global. Puede tener perfiles propios si corresponde, puede aportar perfiles recuperables al catálogo global si son reutilizables y debe mantenerse aislado del core salvo por referencias formales y controladas.

Los perfiles históricos de dominios específicos no se cargan en Prompt 18.0. Se recuperarán controladamente en un subprompt posterior, sin copiar prompts viejos. Cada recuperación debe convertirse a perfil formal PASSED, quedar legacy, quedar específica del dominio original o descartarse. Algunos perfiles históricos podrán transformarse en perfiles globales de análisis, auditoría, simulación, riesgo o integración; otros no.

Lenguaje recomendado: dominios específicos, dominios existentes, dominios especializados, separación Core/Dominios y sin contaminación entre dominios.

### Relación con producto terminado y generación de valor

IA_CORE debe tender a producir salidas útiles:

- Dominio recomendado.
- Equipo profesional recomendado.
- Perfiles compatibles.
- Modelo recomendado.
- Plan de acción.
- Activos a crear.
- Riesgos.
- Primeros pasos.

Un perfil profesional global solo tiene sentido si ayuda a generar esas salidas y a convertir una idea o necesidad en acción, activo, mejora, ingreso o reducción de riesgo.

### Árbol sugerido de Prompt 18

- 18.0 - Modelo de perfil profesional global.
- 18.1 - Inventario de familias profesionales.
- 18.2 - Primer bloque PASSED: empresa digital moderna.
- 18.3 - Segundo bloque PASSED: pyme/local/emprendedor.
- 18.4 - Tercer bloque PASSED: técnica/datos/automatización.
- 18.5 - Cuarto bloque PASSED: legal/finanzas/RRHH/soporte.
- 18.6 - Recuperación controlada de perfiles históricos de dominios específicos.
- 18.7 - Auditoría de cobertura perfiles vs áreas/nichos.
- 18.8 - Normalización role_id/specialization_id.
- 18.9 - Cierre del inventario inicial de perfiles globales.

Este árbol puede dividirse más si el trabajo real lo pide. El método sigue siendo capa por capa. Los números iniciales no son techo: la auditoría de cobertura manda.

## Familias profesionales globales

Prompt 18.1 ordena la superficie profesional antes de crear perfiles individuales. Las familias no son perfiles, presets ni agentes: son la capa de organizacion que permite decidir que perfiles PASSED cargar, que valor economico cubren y que huecos quedan antes de avanzar a Prompt 18.2.

No se crea todavia `catalogs/professional_profile_families.json`. La estructura queda documentada para convertirla en catalogo formal si la auditoria de perfiles lo justifica.

### Inventario inicial de familias

| family_id | Nombre y descripcion | Tipo de valor principal | Areas y nichos representativos | Tipos de perfil esperados | Escalas y model policy tendencial | Valor economico, salidas y notas de cobertura |
|---|---|---|---|---|---|---|
| `estrategia_direccion` | Estrategia y Direccion: objetivos, prioridades, modelos de negocio, vision y coordinacion ejecutiva. | `mejorar_decision`, `profesionalizar_negocio`, `validar_oportunidades`, `generar_ingresos` | Gerencia, comercial, producto, datos, finanzas. Nichos: `planificacion_estrategica`, `tablero_direccion`, `modelos_negocio`, `estrategia_comercial`, `validacion_ideas_negocio`. | estrategico, coordinacion, analitico, mixto | pyme, empresa_mediana, enterprise, emprendedor; `cloud_reasoning`, `hybrid`, `long_context` | Mejora foco, priorizacion y decisiones. Salidas: roadmap ejecutivo, matriz de prioridades, plan de accion, hipotesis de negocio. Es transversal y debe evitar volverse consultoria generica sin entregables. |
| `operaciones_procesos` | Operaciones y Procesos: ordenar, documentar, controlar y mejorar la ejecucion diaria. | `ordenar_operacion`, `reducir_costos`, `acelerar_ejecucion`, `profesionalizar_negocio` | Produccion, abastecimiento, secretarias, gastronomia, soporte, proyectos. Nichos: `mejora_continua_procesos`, `estandarizacion_procedimientos`, `agenda_coordinacion`, `planificacion_produccion`, `compras_proveedores`. | operativo, coordinacion, administrativo, mixto | local_comercial, pyme, empresa_mediana; `local_standard`, `hybrid`, `batch_analysis` | Reduce friccion y errores. Salidas: SOPs, checklist, tablero operativo, mapa de proceso. Requiere perfiles aterrizados para pyme/local y no solo operations manager generico. |
| `producto_ux` | Producto y UX: propuesta de valor, discovery, research, roadmap, experiencia y validacion. | `validar_oportunidades`, `crear_activos_digitales`, `mejorar_retencion`, `generar_ingresos` | Producto, diseno, customer success, marketing, tecnologia. Nichos: `gestion_producto_digital`, `research_usuarios`, `priorizacion_roadmap`, `ux_ui`, `experiencia_cliente_omnicanal`. | estrategico, creativo, analitico, investigacion | emprendedor, pyme, empresa_mediana, enterprise; `hybrid`, `cloud_reasoning`, `multimodal` | Convierte ideas en productos vendibles. Salidas: brief de producto, roadmap, journeys, experimentos de validacion. Necesita dividir product strategy, UX research, UX/UI y service design. |
| `marketing_growth` | Marketing y Growth: adquisicion, campanas, contenidos, embudos, canales y crecimiento. | `generar_ingresos`, `aumentar_ventas`, `crear_activos_digitales`, `mejorar_retencion` | Marketing, comercial, customer success, datos. Nichos: `performance_ads`, `contenidos_redes`, `crm_fidelizacion`, `growth_experimentos`, `investigacion_mercado`. | estrategico, creativo, analitico, comercial | emprendedor, local_comercial, pyme, empresa_mediana; `local_standard`, `hybrid`, `fast_iteration`, `cloud_low_latency` | Acelera adquisicion y conversion. Salidas: campanas, calendario editorial, experimentos, mensajes, analisis de canales. Debe separar estrategia, performance, contenido y lifecycle. |
| `ventas_revenue` | Ventas y Revenue: pipeline, objeciones, revenue operations, seguimiento comercial y monetizacion. | `generar_ingresos`, `aumentar_ventas`, `mejorar_margen`, `profesionalizar_negocio` | Comercial, atencion, marketing, seguros, aduana. Nichos: `prospeccion_b2b`, `gestion_cuentas_clave`, `ventas_retail`, `ecommerce_y_marketplaces`, `diseno_pipeline_comercial`. | comercial, operativo, analitico, coordinacion | emprendedor, local_comercial, pyme, empresa_mediana, enterprise; `local_standard`, `hybrid`, `cloud_low_latency` | Genera ingresos directos. Salidas: scripts, CRM, pipeline, playbooks, propuestas comerciales. Es una familia critica para monetizacion y no debe quedar absorbida por marketing. |
| `datos_analytics` | Datos, BI y Analytics: metricas, dashboards, BI, rentabilidad, segmentacion y decisiones basadas en datos. | `mejorar_decision`, `mejorar_margen`, `reducir_costos`, `validar_oportunidades` | Datos, finanzas, marketing, customer success, operaciones. Nichos: `dashboards_operativos`, `indicadores_negocio`, `auditoria_datos`, `inteligencia_comercial`, `rentabilidad_por_canal`. | analitico, tecnico, investigacion | pyme, empresa_mediana, enterprise, investigacion; `batch_analysis`, `long_context`, `cloud_reasoning`, `local_heavy` | Convierte datos en decisiones. Salidas: dashboards, metricas, modelos de margen, segmentacion. Debe separar analista de negocio, BI, data quality y analytics avanzado. |
| `automatizacion_tecnologia` | Automatizacion y Tecnologia: integraciones, APIs, no-code/low-code, sistemas internos, soporte IT y automatizacion. | `automatizar_trabajo`, `reducir_costos`, `acelerar_ejecucion`, `crear_activos_digitales` | Automatizacion, tecnologia, departamento tecnico, datos. Nichos: `automatizacion_procesos_internos`, `integraciones_herramientas`, `gestion_apis`, `arquitectura_sistemas_internos`, `soporte_it`. | tecnico, operativo, coordinacion, mixto | pyme, empresa_mediana, enterprise, dominio_especializado; `local_heavy`, `hybrid`, `cloud_reasoning`, `offline_capable` | Reduce trabajo manual y crea sistemas. Salidas: workflows, especificaciones, integraciones, base tecnica. Debe separar automation specialist, system architect, soporte tecnico y seguridad. |
| `finanzas_administracion` | Finanzas y Administracion: caja, costos, rentabilidad, presupuestos, pagos, compras y control financiero. | `mejorar_margen`, `proteger_valor`, `reducir_costos`, `mejorar_decision` | Administracion, abastecimiento, seguros, comercio exterior. Nichos: `tesoreria_cashflow`, `control_gestion`, `planeamiento_financiero`, `costos_importacion_exportacion`, `presupuestos_computos`. | administrativo, analitico, compliance, operativo | emprendedor, local_comercial, pyme, empresa_mediana; `local_standard`, `batch_analysis`, `privacy_sensitive` | Ordena dinero y evita fuga de margen. Salidas: cashflow, presupuesto, analisis de costos, control de gestion. Requiere perfiles separados para controller, tesoreria, costos y administracion. |
| `legal_compliance` | Legal y Compliance: contratos, politicas, privacidad, riesgos legales, cumplimiento y prevencion. | `reducir_riesgo`, `proteger_valor`, `profesionalizar_negocio` | Legales, RRHH, comercio exterior, seguros, salud, tecnologia. Nichos: `analisis_contratos`, `compliance_normativo`, `proteccion_datos`, `derecho_laboral`, `compliance_comercio_exterior`. | compliance, analitico, critico, investigacion | pyme, empresa_mediana, enterprise, dominio_especializado; `privacy_sensitive`, `human_review_required`, `high_reliability`, `cloud_reasoning` | Protege valor y reduce contingencias. Salidas: matriz de riesgos, checklist legal, borradores, politicas. Siempre requiere limites claros y revision humana. |
| `rrhh_capacitacion` | RRHH y Capacitacion: roles, seleccion, onboarding, cultura, desempeno, aprendizaje y procesos internos de personas. | `escalar_equipo`, `profesionalizar_negocio`, `acelerar_ejecucion`, `mejorar_retencion` | RRHH, educacion, gerencia, comunicacion interna. Nichos: `seleccion_talento`, `onboarding_empleados`, `capacitacion_desarrollo`, `evaluacion_desempeno`, `clima_cultura`. | operativo, coordinacion, soporte, investigacion | pyme, empresa_mediana, enterprise; `local_standard`, `hybrid`, `human_review_required` | Mejora equipos y aprendizaje. Salidas: perfiles de puesto, onboarding, planes de capacitacion, evaluaciones. Debe distinguir HR ops, recruiter, trainer y people partner. |
| `soporte_customer_success` | Soporte y Customer Success: atencion, reclamos, postventa, onboarding, fidelizacion y satisfaccion. | `mejorar_retencion`, `proteger_valor`, `aumentar_ventas`, `ordenar_operacion` | Customer success, atencion, soporte tecnico, salud, seguros. Nichos: `soporte_cliente`, `reclamos_postventa`, `onboarding_clientes`, `gestion_churn`, `mesa_ayuda`. | soporte, operativo, analitico, coordinacion | local_comercial, pyme, empresa_mediana, enterprise; `cloud_low_latency`, `local_standard`, `hybrid` | Retiene clientes y reduce friccion. Salidas: protocolos, macros, playbooks, analisis de churn. Requiere perfiles diferenciados para soporte, CX, CS ops y calidad. |
| `investigacion_analisis` | Investigacion y Analisis: mercado, competencia, hipotesis, tendencias, evidencia y oportunidades. | `validar_oportunidades`, `mejorar_decision`, `generar_ingresos`, `proteger_valor` | Marketing, producto, educacion, sociologia, gerencia. Nichos: `investigacion_mercado`, `analisis_competitivo`, `investigacion_academica`, `evaluacion_impacto_social`, `research_usuarios`. | investigacion, analitico, estrategico, critico | emprendedor, pyme, empresa_mediana, investigacion, enterprise; `long_context`, `cloud_reasoning`, `batch_analysis` | Reduce incertidumbre. Salidas: research brief, mapa competitivo, hipotesis validadas, oportunidades. Necesita perfiles con razonamiento alto y buena gestion de evidencia. |
| `calidad_riesgo` | Calidad y Riesgo: auditoria, validacion, control, robustez, sesgos, inconsistencias y prevencion. | `reducir_riesgo`, `proteger_valor`, `mejorar_decision`, `profesionalizar_negocio` | Produccion, legal, datos, seguros, salud, ingenieria. Nichos: `control_calidad`, `auditoria_datos`, `suscripcion_riesgos`, `auditoria_medica`, `seguridad_higiene_obra`. | compliance, critico, analitico, auditor | pyme, empresa_mediana, enterprise, dominio_especializado; `high_reliability`, `human_review_required`, `batch_analysis` | Evita errores caros. Salidas: auditorias, controles, pruebas, matriz de riesgos. Debe separar QA, auditor, risk analyst y safety/compliance por sector. |
| `contenido_comunicacion` | Contenido y Comunicacion: mensajes, storytelling, piezas, comunicacion institucional, documentacion comercial y canales. | `crear_activos_digitales`, `aumentar_ventas`, `profesionalizar_negocio`, `proteger_valor` | Marketing, comunicacion, diseno, ventas, soporte. Nichos: `estrategia_marca`, `contenidos_redes`, `comunicacion_institucional`, `prensa_medios`, `documentacion_tecnica`. | creativo, estrategico, soporte, comercial | emprendedor, local_comercial, pyme, empresa_mediana; `local_standard`, `multimodal`, `fast_iteration` | Convierte conocimiento en activos comunicables. Salidas: mensajes, piezas, docs, guiones, comunicados. Debe distinguir copy, contenido, comunicacion institucional y documentacion tecnica. |
| `industria_oficios` | Industria y Oficios: rubros, operaciones fisicas, campo, construccion, salud, logistica, produccion y servicios tecnicos. | `ordenar_operacion`, `reducir_costos`, `proteger_valor`, `profesionalizar_negocio` | Produccion, ingenierias, construccion, salud, mineria, naviero, gastronomia, oficios. Nichos: `direccion_obra`, `operaciones_portuarias`, `gestion_restaurantes`, `operaciones_mineras`, `servicios_tecnicos`. | operativo, tecnico, coordinacion, dominio_especializado | local_comercial, pyme, empresa_mediana, enterprise, dominio_especializado; `hybrid`, `offline_capable`, `human_review_required` | Baja la IA a operaciones reales. Salidas: procedimientos, presupuestos, controles, coordinacion de campo. Es sectorial y requiere perfiles especificos cuando el riesgo operativo sea alto. |
| `dominio_especializado` | Dominio Especializado: perfiles no universales que tienen valor en dominios concretos o altamente especializados. | `validar_oportunidades`, `proteger_valor`, `generar_ingresos`, `crear_activos_digitales` | Loteria/juegos de azar, seguros, salud, comercio exterior, mineria, naviero, sociologia. Nichos: `analisis_loteria_juegos_azar`, `gestion_siniestros`, `farmacia_clinica`, `clasificacion_arancelaria`, `documentacion_maritima`. | dominio_especializado, investigacion, analitico, tecnico | dominio_especializado, investigacion, enterprise; `cloud_reasoning`, `privacy_sensitive`, `human_review_required`, `long_context` | Permite recuperar o crear perfiles muy concretos sin contaminar el core. Salidas: criterios especializados, auditorias de dominio, simulaciones, papers base. Debe entrar solo cuando haya valor real y trazabilidad. |

### Familias por tipo de valor economico

- **Generacion directa de ingresos**: `ventas_revenue`, `marketing_growth`, `producto_ux`, `estrategia_direccion`, `contenido_comunicacion`, `finanzas_administracion`.
- **Proteccion de valor y riesgo**: `legal_compliance`, `calidad_riesgo`, `finanzas_administracion`, `datos_analytics`, `operaciones_procesos`, `industria_oficios`.
- **Aceleracion y reduccion de costos**: `operaciones_procesos`, `automatizacion_tecnologia`, `datos_analytics`, `soporte_customer_success`, `rrhh_capacitacion`.
- **Creacion de activos digitales**: `producto_ux`, `contenido_comunicacion`, `marketing_growth`, `automatizacion_tecnologia`, `investigacion_analisis`.
- **Profesionalizacion y escalabilidad**: `estrategia_direccion`, `operaciones_procesos`, `rrhh_capacitacion`, `finanzas_administracion`, `calidad_riesgo`.

Las familias mas directamente relacionadas con ingresos son `ventas_revenue`, `marketing_growth`, `producto_ux`, `estrategia_direccion` y `contenido_comunicacion`. `finanzas_administracion` no siempre genera ventas, pero protege margen y mejora monetizacion.

### Mapa inicial de cobertura

- **Familias mas transversales**: `estrategia_direccion`, `operaciones_procesos`, `datos_analytics`, `automatizacion_tecnologia`, `calidad_riesgo`, `contenido_comunicacion`.
- **Familias de soporte**: `finanzas_administracion`, `rrhh_capacitacion`, `soporte_customer_success`, `legal_compliance`, `contenido_comunicacion`.
- **Familias sectoriales**: `industria_oficios`, `dominio_especializado`, con apoyo de `calidad_riesgo`, `legal_compliance` y `automatizacion_tecnologia`.
- **Nichos criticos de negocio**: `prospeccion_b2b`, `performance_ads`, `gestion_producto_digital`, `pricing_packaging`, `indicadores_negocio`, `tesoreria_cashflow`, `gestion_churn`, `automatizacion_procesos_internos`, `analisis_contratos`.
- **Areas con alta demanda de cobertura**: administracion/finanzas, marketing, comercial, gerencia, datos, automatizacion, tecnologia, customer success y legales.
- **Areas con riesgo de cobertura debil si no hay perfiles especificos**: enfermeria, salud, mineria/petroleo/gas, naviero/portuario, aduana/comercio exterior, ingenieria civil/construccion, seguros, sociologia/trabajo social y oficios.
- **Nichos que probablemente necesitaran perfiles especializados**: `auditoria_medica`, `farmacia_clinica`, `seguridad_ambiental`, `permisos_reportes_ambientales`, `clasificacion_arancelaria`, `documentacion_maritima`, `suscripcion_riesgos`, `seguridad_higiene_obra`, `analisis_loteria_juegos_azar`.

### Masa critica inicial sugerida por familia

Estos rangos son punto de partida, no techo. La auditoria de cobertura de Prompt 18.7 puede ampliar, dividir o fusionar familias y perfiles.

| family_id | Perfiles iniciales sugeridos |
|---|---:|
| `estrategia_direccion` | 5-7 |
| `operaciones_procesos` | 7-9 |
| `producto_ux` | 5-7 |
| `marketing_growth` | 7-9 |
| `ventas_revenue` | 6-8 |
| `datos_analytics` | 6-8 |
| `automatizacion_tecnologia` | 6-8 |
| `finanzas_administracion` | 5-7 |
| `legal_compliance` | 4-6 |
| `rrhh_capacitacion` | 4-5 |
| `soporte_customer_success` | 5-6 |
| `investigacion_analisis` | 4-6 |
| `calidad_riesgo` | 4-5 |
| `contenido_comunicacion` | 4-6 |
| `industria_oficios` | 5-8 |
| `dominio_especializado` | 2-5 |

Rango total inicial orientativo: 79-110 perfiles. Para la primera masa critica conviene apuntar al tramo 80-100 y dejar el excedente como expansion justificada por huecos.

### Huecos probables antes de perfiles

- Las areas con 9-13 nichos requieren varios perfiles por familia para no depender de perfiles demasiado genericos.
- Marketing y ventas necesitan perfiles separados para estrategia, performance, contenido, CRM, pipeline y revenue operations.
- Datos no debe quedar reducido a "analista de datos": hacen falta BI, data quality, analisis de negocio, inteligencia comercial y rentabilidad.
- Tecnologia y automatizacion requieren separar soporte IT, integraciones, arquitectura, ciberseguridad y no-code/low-code.
- Legal, salud, seguros, comercio exterior y obra requieren perfiles con limites, revision humana y conocimiento sectorial.
- Pymes/locales necesitan perfiles aterrizados a ejecucion diaria, no solo perfiles enterprise.
- Investigacion y estrategia requieren perfiles de razonamiento alto, manejo de evidencia y capacidad de convertir hallazgos en decisiones.
- Dominios historicos o especializados deben recuperarse sin contaminar la biblioteca global.

### Estructura futura recomendada para `professional_profile_families.json`

Si Prompt 18.2 o una auditoria posterior decide formalizar familias como catalogo, la estructura recomendada es:

```json
{
  "family_id": "marketing_growth",
  "nombre": "Marketing y Growth",
  "descripcion": "Familia orientada a adquisicion, campanas, canales, embudos y crecimiento medible.",
  "tipo_valor_principal": ["generar_ingresos", "aumentar_ventas", "crear_activos_digitales"],
  "areas_compatibles": ["marketing_publicidad", "comercial_ventas_negocios", "customer_success_experiencia_cliente"],
  "nichos_representativos": ["performance_ads", "contenidos_redes", "crm_fidelizacion"],
  "tipos_perfil_esperados": ["estrategico", "creativo", "analitico", "comercial"],
  "escalas_negocio_compatibles": ["emprendedor", "local_comercial", "pyme", "empresa_mediana"],
  "model_policy_tendencia": ["local_standard", "hybrid", "cloud_reasoning"],
  "valor_economico": "Ayuda a generar demanda, mejorar conversion y convertir mensajes en activos comerciales.",
  "ejemplos_de_salidas": ["plan de campana", "calendario de contenido", "analisis de canal", "experimento growth"],
  "notas_de_cobertura": "Debe dividirse entre estrategia, performance, contenido y lifecycle si la cobertura queda generica.",
  "status": "active",
  "activo": true
}
```

No se crea este JSON en Prompt 18.1 porque todavia no hay perfiles individuales ni tests de contrato para familias. La documentacion queda como fuente de diseño para el siguiente paso.

## Primer bloque PASSED de perfiles profesionales - empresa digital moderna

Prompt 18.2 crea el primer catálogo global real en `catalogs/professional_profiles.json`. El bloque inicial contiene **25 perfiles profesionales PASSED** orientados a empresa digital moderna, transformación de ideas en operación, generación de ingresos y creación de activos reutilizables.

### Perfiles creados

- `estratega_negocio_digital`
- `director_operativo_digital`
- `consultor_modelo_negocio`
- `product_manager_digital`
- `investigador_usuarios`
- `estratega_propuesta_valor`
- `priorizador_roadmap`
- `estratega_growth`
- `especialista_performance_marketing`
- `estratega_contenidos`
- `copywriter_conversion`
- `gestor_calendario_comercial`
- `disenador_pipeline_comercial`
- `especialista_ventas_consultivas`
- `revenue_operations_manager`
- `analista_datos_negocio`
- `especialista_bi_dashboards`
- `analista_rentabilidad_margen`
- `arquitecto_automatizaciones`
- `integrador_herramientas_digitales`
- `especialista_crm_whatsapp`
- `coordinador_operaciones_digitales`
- `analista_finanzas_pyme`
- `especialista_customer_success`
- `auditor_calidad_operativa`

### Familias cubiertas

El bloque cubre 11 de las 16 familias profesionales iniciales:

- `estrategia_direccion`
- `operaciones_procesos`
- `producto_ux`
- `marketing_growth`
- `ventas_revenue`
- `datos_analytics`
- `automatizacion_tecnologia`
- `finanzas_administracion`
- `soporte_customer_success`
- `calidad_riesgo`
- `contenido_comunicacion`

Quedan para bloques posteriores: `legal_compliance`, `rrhh_capacitacion`, `investigacion_analisis`, `industria_oficios` y `dominio_especializado`.

### Criterio de selección

La selección prioriza perfiles que ayudan a:

- convertir ideas en modelos de negocio y producto;
- ordenar operaciones digitales;
- generar demanda, ventas y retención;
- crear activos de contenido, CRM, dashboards y automatización;
- proteger margen, calidad y ejecución.

No se eligieron perfiles por cantidad. Se eligieron porque cubren necesidades base de una empresa digital moderna y tienen ruta futura hacia preset, paper, equipos y model policy.

### Cobertura inicial

El bloque cubre 15 áreas y 64 nichos únicos de la superficie 30/200. Las áreas más representadas son comercial, marketing, producto, datos, automatización, tecnología, finanzas, customer success, gerencia, diseño y atención.

Nichos clave cubiertos:

- `planificacion_estrategica`, `modelos_negocio`, `objetivos_metricas_okrs`
- `gestion_producto_digital`, `research_usuarios`, `priorizacion_roadmap`, `pricing_packaging`
- `growth_marketing`, `performance_ads`, `embudos_conversion`, `calendario_comercial`
- `prospeccion_b2b`, `ventas_consultivas`, `revenue_operations`, `crm_comercial`
- `dashboards_operativos`, `indicadores_negocio`, `inteligencia_comercial`, `rentabilidad_por_canal`
- `automatizacion_procesos_internos`, `integraciones_herramientas`, `automatizacion_whatsapp_crm`, `gestion_apis`
- `tesoreria_cashflow`, `control_gestion`, `onboarding_clientes`, `gestion_churn`, `control_calidad`

### Valor económico del bloque

El bloque cubre cinco caminos de valor principales:

- generación de ingresos: growth, performance, ventas consultivas, pipeline, RevOps;
- mejora de margen: rentabilidad, pricing, finanzas pyme, performance;
- reducción de costos: automatización, operaciones digitales, dashboards, calidad;
- creación de activos digitales: producto, contenido, copy, CRM, BI, workflows;
- protección de valor: customer success, auditoría operativa, finanzas, calidad de datos.

### Relación con roles y especializaciones

Todos los perfiles del primer bloque usan `expected_role_id` y `expected_specialization_id` existentes en `catalogs/roles.json` y `catalogs/specializations.json`.

Gaps semánticos a revisar en Prompt 18.8:

- `especialista_bi_dashboards` usa `sintetizador` + `sintesis_ejecutiva`, pero podría requerir una especialización futura de BI/dashboarding.
- `analista_finanzas_pyme` usa `gestor_riesgo` + `administracion_recursos`, pero podría requerir una especialización financiera más directa.
- `especialista_crm_whatsapp` usa `coordinador` + `coordinacion_flujos`, pero podría requerir una especialización CRM/marketing ops.
- Algunos perfiles comerciales usan comunicación persuasiva como aproximación funcional; Prompt 18.8 puede decidir si ventas necesita especializaciones propias.

Estos gaps no bloquean el bloque PASSED porque cada perfil tiene rol/especialización existente, cobertura real y trazabilidad futura.

### Relación con model policies

Policies usadas en el bloque:

- `batch_analysis`
- `cloud_low_latency`
- `cloud_reasoning`
- `cost_sensitive`
- `fast_iteration`
- `high_reliability`
- `hybrid`
- `local_heavy`
- `local_standard`
- `long_context`
- `privacy_sensitive`

No se crea `catalogs/profile_model_policies.json` todavía. Prompt 20 debe formalizar estas políticas e integrarlas con recomendación hardware-aware.

### Alcance explícito

No se crearon presets reales, papers reales ni agentes reales. `preset_seed_expected` y `paper_seed_expected` son semillas esperadas para prompts posteriores. No se modificaron dominios específicos, `profile_catalog.json` ni `agent_presets.json`.

### Preparación para Prompt 18.3

Prompt 18.3 debería cargar el segundo bloque PASSED orientado a pyme, local comercial y emprendedor: perfiles de administración práctica, atención, operaciones de comercio, agenda, compras, inventario, servicios, RRHH inicial, soporte y gestión cotidiana. Ese bloque debe complementar el foco digital de 18.2 con perfiles más aterrizados a negocio real de baja y media escala.
