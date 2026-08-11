# Backend Interno Phase 5 Team Sandbox Block Plan

Estado: `PHASE_5_TEAM_SANDBOX_BLOCK_PLANNED`

Veredicto: `PHASE_5_TEAM_SANDBOX_SELECTED`

Readiness: `ready_for_phase_5_team_sandbox_schema`

Next: `PROMPT 5.0 — Schema de equipo real sandbox`

## Propósito

Fase 5 — Equipos reales sandbox define el próximo bloque arquitectónico después del cierre de Runtime Execution Preparation. Su propósito es preparar contratos y artefactos de equipo sandbox que agrupen agentes sandbox existentes de forma trazable, validable y no-operativa.

## Objetivo Del Bloque

Definir primero el schema de equipo real sandbox y luego, en prompts posteriores, materializar equipos declarativos desde `team_template` sin abrir ejecución multiagente real.

## PROMPT 5.0 - Schema De Equipo Real Sandbox

Estado esperado al cierre: `SANDBOX_TEAM_SCHEMA_READY`

Veredicto esperado: `SANDBOX_TEAM_SCHEMA_NO_OPERATIONAL_CONFIRMED`

Readiness esperada: `ready_for_phase_5_1_team_template_materialization`

PROMPT 5.0 reconcilia `core/sandbox_team_schema.py` como contrato canonico de equipo real sandbox. El contrato diferencia `team_template` derivado de equipo sandbox real, exige identidad propia, `domain_id`, `artifact_id`, `materialization_id`, `source_team_template`, `created_from`, `members`, `execution_policy`, `permissions`, estados no activos y compatibilidad futura con `artifact_manifest`.

El schema mantiene aliases historicos (`purpose`, `member_agents`, `artifact_type: team` en manifest) para no romper la cadena previa de equipos sandbox, pero la forma canonica de Fase 5 queda en `members`, `team_type=sandbox`, `artifact_state`, `execution_policy` y `permissions`.

Criterio de cierre de 5.0:

- existe validador claro para equipo sandbox real;
- `team_template` derivado no pasa como equipo real sandbox;
- `execution_policy` bloquea runtime, ejecucion, tools, modelos e integraciones;
- `permissions` mantiene permisos sensibles en false;
- `agent_reference` puede ser `null` sin ejecutar nada;
- no se crea equipo operativo;
- no se ejecutan agentes, runtime, tools ni modelos;
- la documentacion vive en `docs/SANDBOX_TEAM_SCHEMA.md`.

## Por Qué Viene Después De Runtime Execution Preparation

Runtime Execution Preparation cerró con `RUNTIME_EXECUTION_PREPARATION_BLOCK_INTEGRAL_CHECKPOINT_PASSED`, `RUNTIME_EXECUTION_PREPARATION_BLOCK_CHAIN_READY` y `ready_for_next_architecture_block_planning`. El libro Backend Interno ya identifica Fase 5 como “Equipos reales sandbox” después de agentes reales sandbox, y existen piezas históricas no-operativas relacionadas con equipos sandbox (`core/sandbox_team_schema.py`, `core/sandbox_team_materializer.py`) y plantillas derivadas (`core/professional_team_template_generator.py`).

## Alcance

- Schema contractual de equipo real sandbox.
- Relación entre equipo sandbox, agentes sandbox existentes y `team_template` derivado.
- Manifest trazable de equipo sandbox.
- Estados no-operativos de equipo.
- Validaciones de referencias cruzadas.
- Límites, riesgos y criterios de cierre.

## Fuera De Alcance

- Runtime multiagente real.
- Ejecución de equipos.
- Orquestador operativo.
- Scheduler, worker, queue, dispatcher o event bus operativo.
- Tool execution.
- Model invocation.
- UI/UX.
- Integraciones.
- Market Catalog runtime.
- Business Composition Layer runtime.
- OBLITERATUS.

## Dependencias Previas

- Runtime Execution Preparation Block cerrado en commit `61c4b15b`.
- `docs/RUNTIME_EXECUTION_PREPARATION_BLOCK_INTEGRAL_CHECKPOINT.md`.
- Contratos cerrados de preparation, package, read model y projection.
- Equipo sandbox histórico como contrato/materialización no-operativa.
- Plantillas profesionales derivadas desde `core/professional_team_template_generator.py`.

## Archivos Base

- `docs/SANDBOX_TEAM_CONTRACT.md`
- `docs/SANDBOX_TEAM_MATERIALIZATION.md`
- `docs/SANDBOX_TEAM_CHAIN_CHECKPOINT.md`
- `core/sandbox_team_schema.py`
- `core/sandbox_team_materializer.py`
- `core/professional_team_template_generator.py`
- `scripts/generate_professional_team_template.py`

Nota: `catalogs/team_templates.json` no existe actualmente en el working tree revisado. La planificación no lo crea ni lo simula; cualquier relación con `team_template` debe partir de plantillas derivadas o de una fuente futura explícitamente aprobada.

## Relación Con Team Templates

Fase 5 debe consumir o referenciar `team_template` como artefacto derivado, no como catálogo operativo inventado. Un equipo sandbox real debe preservar trazabilidad hacia perfiles, presets y agentes sandbox existentes.

## Relación Con Agentes Sandbox

Un equipo sandbox real solo puede referenciar agentes sandbox existentes, validados y no-operativos. No crea agentes nuevos y no ejecuta agentes.

## Relación Con Materialización Sandbox Previa

La materialización de equipos sandbox ya existe históricamente como artefacto declarativo. Fase 5 debe ordenar esa frontera dentro del Backend Interno actual, sin abrir runtime ni reescribir fases cerradas.

## Contratos No-Operativos Que Permanecen Bloqueados

Runtime, execution, dry-run real, tools, model invocation, context injection, output delivery, writes, stores, memory, network, browser, filesystem runtime, env, secrets, API runtime, UI runtime, UI-device control, integrations, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo a User Panel permanecen bloqueados.

## Riesgos

- Llamar “equipo” a una lista decorativa de agentes.
- Referenciar agentes inexistentes.
- Confundir `team_template` derivado con equipo sandbox real.
- Introducir ejecución multiagente real por accidente.
- Saltar a UI/UX o integraciones antes del contrato.

## Restricciones

Fase 5 debe seguir siendo sandbox, contractual, trazable y no-operativa. No habilita ejecución multiagente real.

## Prompts Sugeridos

1. `PROMPT 5.0 — Schema de equipo real sandbox`
2. `PROMPT 5.1 — Materializar equipo real desde team_template`
3. `PROMPT 5.2 — Auditoría de equipo sandbox`
4. `PROMPT 5.3 — Biblioteca interna/listado de equipos sandbox para futura UI`

## Criterio De Cierre De Fase 5

Fase 5 cierra cuando exista un schema de equipo sandbox real, materialización declarativa validada desde `team_template`, auditoría de equipo sandbox, listado interno para futura UI y pruebas que garanticen que no se abrió ejecución multiagente real.

## Readiness

`ready_for_phase_5_team_sandbox_schema`

## Próximo Prompt Exacto

`PROMPT 5.0 — Schema de equipo real sandbox`
