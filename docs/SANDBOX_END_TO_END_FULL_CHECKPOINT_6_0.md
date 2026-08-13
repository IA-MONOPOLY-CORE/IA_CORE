# Sandbox End-to-End Full Checkpoint 6.0

Estado: `SANDBOX_END_TO_END_FULL_CHECKPOINT_PASSED`

Veredicto: `SANDBOX_CHAIN_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_6_1_integral_rollback`

Proximo prompt recomendado: `PROMPT 6.1 - Rollback integral de dominio sandbox completo`

Compatibilidad de nombre: `PROMPT 6.1 - Rollback integral de dominio sandbox completo`

## Proposito

Este checkpoint valida de punta a punta la cadena sandbox completa existente despues del cierre de Fase 5 y de la planificacion 5.4. La validacion confirma que IA_CORE puede encadenar artefactos sandbox declarativos hasta el read model interno de equipo sin abrir runtime, execution, dry-run real, UI ni integraciones.

## Estado Previo Fases 0-5

- Fases 0 a 3 establecieron contrato derivado vs operativo, preview, materializacion controlada, artifact state, sandbox, approval/gates, execution intent pre-operacional y Security Layer.
- Fase 4 cerro Runtime Execution Preparation como bloque no-operativo en `PROMPT 4.8`.
- Fase 4.9 selecciono Fase 5 como bloque de equipos reales sandbox.
- Fase 5 cerro schema, materializacion, auditoria y read model interno de equipos sandbox.
- Fase 5.4 selecciono Fase 6 como bloque de end-to-end sandbox, rollback y regeneracion.

## Piezas Reutilizadas

- `core/domain_materializer.py`
- `core/domain_materialization_rollback.py`
- `core/sandbox_domain_schema.py`
- `core/artifact_manifest_schema.py`
- `core/profile_catalog_materializer.py`
- `core/agent_preset_materializer.py`
- `core/paper_seed_materializer.py`
- `core/sandbox_agent_materializer.py`
- `core/sandbox_team_materializer.py`
- `core/sandbox_team_read_model.py`
- `tests/test_sandbox_chain_with_team_checkpoint.py`
- `tests/test_sandbox_team_read_model.py`
- `tests/test_domain_materialization_rollback.py`

## Piezas Parciales Extendidas

`tests/test_sandbox_end_to_end_full_checkpoint_6_0.py` extiende la cobertura del chain checkpoint vigente con validacion explicita del read model interno, flags no-operativas, limpieza temporal y documentacion de continuidad. No crea una segunda arquitectura `sandbox_chain`.

## Piezas No Usadas Y Motivo

- `tests/test_sandbox_chain_full_benchmark.py`: benchmark largo, no debe convertirse en requisito focal de cada prompt.
- UI, endpoints publicos e integraciones: fuera de alcance de 6.0.
- Runtime runner, scheduler, worker, queue, orchestrator, dispatcher y event bus: prohibidos para este checkpoint.

## Alcance Del E2E

La cadena validada es:

`domain sandbox -> artifact_manifest -> profile_catalog -> agent_presets -> paper_seed -> sandbox agents -> sandbox team -> team read model`

El E2E usa fixture controlada, `tmp_path` y rollback final. No usa dominios productivos ni `domains/` operativo.

## Fuera De Alcance

- runtime real;
- execution real;
- dry-run real operativo;
- tools runtime;
- model invocation;
- context injection operativo;
- output delivery;
- UI o UX;
- integraciones;
- stores/memory operativos;
- Market Catalog runtime;
- Business Composition Layer runtime;
- OBLITERATUS;
- raw Package directo a User Panel.

## Artifact Manifest Y Lineage

El checkpoint valida que el `artifact_manifest` contenga, en orden, `profile_catalog`, `agent_preset`, `paper_seed`, dos `agent` y `team`. Cada artifact conserva `artifact_id`, `artifact_type`, `created_from`, `dependencies`, `rollback_info.created_paths`, `safe_remove=true`, `operational=false` y `passed=false`.

Para equipo se mantiene la convencion vigente: `artifact_type=team` y `artifact_kind=sandbox_team`.

## No-Operatividad Confirmada

La cadena completa permanece con:

- `operational=false`
- `passed=false`
- `runtime_enabled=false`
- `execution_enabled=false`
- `tool_execution_enabled=false`
- `model_invocation_enabled=false`
- `external_integrations_enabled=false`

El read model tambien rechaza payloads alterados con permisos sensibles o execution policy en `true`.

## Read Models Validados

El read model interno de equipos sandbox queda validado como JSON-safe, read-only, sin secretos, sin runtime handles, sin raw prompts, sin tool/model configs y consumible por una futura UI sin obligar a inferir logica critica.

## Limpieza Y Side Effects

La prueba materializa todo bajo `tmp_path`, hace rollback del equipo, agentes, paper seed, presets, profile catalog y dominio, y comprueba hashes de `domains/`, `agents/`, `catalogs/` y papers globales. Tambien confirma que no quedan `.tmp/` ni `memoria_agentes/test_agent*`.

## Riesgos

- Confundir E2E sandbox completo con ejecucion operativa real.
- Convertir el benchmark largo en suite focal obligatoria.
- Duplicar la cadena `sandbox_chain` en lugar de extender checkpoints vigentes.
- Exponer raw Package directo a User Panel antes del contrato backend/UI.

## Deudas

- `PROMPT 6.1` debe enfocar rollback integral de dominio sandbox completo.
- `PROMPT 6.2` debe enfocar regeneracion segura integral.
- `PROMPT 6.3` debe consolidar audit pack/trazabilidad si el rollback y la regeneracion lo requieren.

## ADR

No se crea ADR nueva en 6.0. Este checkpoint valida decisiones ya tomadas en Fase 5.4 y en `ADR-046`; no introduce una decision arquitectonica nueva.

## Veredicto

`SANDBOX_END_TO_END_FULL_CHECKPOINT_PASSED`

`SANDBOX_CHAIN_NO_OPERATIONAL_CONFIRMED`

## Readiness

`ready_for_phase_6_1_integral_rollback`

## Proximo Prompt Recomendado

`PROMPT 6.1 - Rollback integral de dominio sandbox completo`
