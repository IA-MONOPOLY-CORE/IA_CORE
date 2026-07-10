# Biblioteca Profesional Global Multi-Área / Multi-Nicho / Hardware-Aware

**Estado**: Diseño propuesto (Prompt 16)
**Fecha**: 2026-07-10
**HEAD**: 4ca5b7b

## Propósito

IA_CORE debe pasar de "crear agentes por dominio" a "crear equipos profesionales por dominio". La biblioteca profesional es GLOBAL, no pertenece a un dominio específico. Los perfiles profesionales se definen primero en modo empresa digital y luego se asignan a áreas, nichos, dominios, equipos, presets, papers y modelos recomendados.

## Estado Actual Auditado

### Catálogos Globales Existentes

- **Áreas**: 26 (catalogs/areas.json)
- **Nichos**: 94 (catalogs/niches.json)
- **Roles**: 20 (catalogs/roles.json)
- **Especializaciones**: 80 (catalogs/specializations.json)

### Combinaciones Posibles

- **Combinaciones rol + especialización posibles**: 80 (cada especialización pertenece a un rol)
- **Combinaciones rol + especialización usadas en Lotería**: 30 (domains/loteria/profile_catalog.json)

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

1. **Nichos insuficientes para empresa digital completa**: Los 94 nichos actuales cubren muchas áreas tradicionales pero faltan nichos específicos para:
   - Automatización de procesos
   - Growth hacking
   - Product management
   - Data engineering
   - DevOps
   - Community management
   - Customer success
   - Business intelligence avanzado

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
- **Plantillasde equipos**: 20-30 para configuraciones comunes
- **Políticas de modelo**: 10-15 para cubrir patrones de workload/reasoning
