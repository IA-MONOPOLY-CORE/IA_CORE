# Materializacion De Equipo Sandbox

Estado: `SANDBOX_TEAM_TEMPLATE_MATERIALIZATION_READY`

Veredicto: `SANDBOX_TEAM_TEMPLATE_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_5_2_sandbox_team_audit`

## 1. Proposito

`core/sandbox_team_materializer.py` materializa equipos sandbox como artefactos declarativos dentro de un dominio sandbox controlado.

PROMPT 5.1 agrega la ruta desde `team_template` derivado mediante `materialize_sandbox_team_from_template()`. Esta ruta no ejecuta equipos, agentes, modelos, tools ni integraciones.

## 2. Relacion Con Fase 5

Fase 5 - Equipos reales sandbox avanza en dos pasos seguros:

1. PROMPT 5.0 definio el schema de equipo sandbox real.
2. PROMPT 5.1 materializa declarativamente un equipo desde `team_template`.

El siguiente paso es auditoria, no runtime: `PROMPT 5.2 - Auditoria de equipo sandbox`.

## 3. Entrada Desde Team Template

La entrada puede ser el wrapper generado por `core.professional_team_template_generator`:

```txt
artifact_type: derived_professional_team_template
team_template: {...}
```

o el payload interno `team_template` equivalente.

El materializador valida:

- identidad `team_template_id`;
- nombre y descripcion;
- roles o perfiles recomendados suficientes;
- estado derivado/no operativo;
- ausencia de runtime, execution, tools, modelos, integraciones y permisos reales.

No se crea `catalogs/team_templates.json` y no se inventan catalogos.

## 4. Team Template Vs Equipo Materializado Sandbox

`team_template` es una plantilla derivada y reusable. No pertenece por si sola a un sandbox materializado, no tiene `artifact_id` de equipo real y no ejecuta.

El equipo materializado sandbox:

- pertenece a `domain_id`;
- tiene `team_id`, `artifact_id` y `materialization_id`;
- se escribe en sandbox controlado;
- conserva `source_team_template` y `created_from`;
- registra members declarativos;
- queda preparado para manifest y rollback;
- no es operativo ni `active`.

## 5. Estructura Creada

La ruta 5.1 crea dentro del sandbox temporal/controlado:

```txt
<sandbox>/<domain_id>/sandbox_teams/<team_id>.json
<sandbox>/<domain_id>/sandbox_teams/<team_id>.manifest.json
<sandbox>/<domain_id>/manifests/artifact_manifest.json
```

Tambien extiende `materialization_manifest.json` del dominio sandbox con los paths creados.

## 6. Manifest Del Equipo

El manifest especifico del equipo incluye:

- `schema_version`;
- `materialization_id`;
- `artifact_id`;
- `artifact_type`;
- `artifact_kind`;
- `domain_id`;
- `team_id`;
- `source_template_id`;
- `source_team_template`;
- `created_from`;
- `created_paths`;
- `dependencies`;
- `rollback_prepared`;
- flags de ejecucion/runtime/tools/modelos/integraciones en `false`;
- `created_at`;
- `validation`;
- `history`.

## 7. Lineage Y Dependencies

Lineage:

```txt
team_template derivado
-> materialize_sandbox_team_from_template
-> sandbox_team schema 5.0
-> team manifest
-> artifact_manifest
```

Si los miembros tienen `agent_reference=null`, `dependencies` puede quedar vacio. Si en una fase futura existen agentes sandbox trazados, las dependencies podran salir de `agent_reference.artifact_id`.

## 8. Decision Artifact Type: Team Vs Sandbox Team

Auditoria 5.1:

- `artifact_type: team` es una convencion generica valida del `artifact_manifest_schema.py` actual.
- `created_from.artifact_kind: sandbox_team` y `team_manifest.artifact_kind: sandbox_team` desambiguan que se trata de un equipo sandbox real.
- Normalizar ahora a `artifact_type: sandbox_team` romperia compatibilidad con `artifact_manifest_schema.py`, tests existentes y manifiestos historicos que esperan `team`.
- No hay ambiguedad real porque el lineage declara `artifact_kind`, `source_team_template`, `materialization_id`, `created_by` y flags no operativos.

Decision: mantener `artifact_type: team` por compatibilidad y declarar `artifact_kind: sandbox_team` para semantica especifica. Una normalizacion futura requeriria subprompt quirurgico si el manifest global decide aceptar `sandbox_team` como tipo propio.

## 9. Politica De No Ejecucion

La materializacion exige:

- `execution_enabled=false`;
- `runtime_enabled=false`;
- `tool_execution_enabled=false`;
- `model_invocation_enabled=false`;
- `external_integrations_enabled=false`;
- `human_approval_required=true`.

El materializador no ejecuta agentes, no invoca modelos, no llama tools, no abre runtime y no produce outputs operativos.

## 10. Permisos Bloqueados

Permisos sensibles deben permanecer en `false`:

- `can_execute`;
- `can_call_tools`;
- `can_call_models`;
- `can_write_outputs`;
- `can_access_network`;
- `can_use_integrations`.

Templates que intenten declarar permisos o flags operativos en `true` fallan antes de escribir.

## 11. Relacion Con Artifact Manifest

El equipo se registra en `manifests/artifact_manifest.json` como:

```txt
artifact_type: team
artifact_id: team_<team_id>
created_from.artifact_kind: sandbox_team
operational: false
passed: false
```

El registro se valida con `core/artifact_manifest_schema.py`. No existen writer/read model de artifact manifest en este prompt; no se inventan.

## 12. Relacion Futura Con Agentes Sandbox

La materializacion desde template permite miembros con:

```txt
agent_reference: null
```

Esto preserva roles y responsabilidades sin exigir agentes reales. Las referencias contra agentes sandbox materializados se validaran en fases posteriores.

## 13. Que NO Hace Esta Materializacion

- No crea agentes.
- No ejecuta agentes.
- No activa runtime multiagente.
- No crea scheduler, worker, queue, orchestrator, dispatcher ni event bus.
- No invoca modelos.
- No llama tools.
- No abre red, UI ni integraciones.
- No escribe en `domains/` operativo.
- No habilita Market Catalog runtime.
- No habilita Business Composition Layer runtime.
- No incorpora OBLITERATUS.

## 14. Criterios Para Avanzar A Auditoria 5.2

- `materialize_sandbox_team_from_template()` existe y pasa tests.
- `validate_materialized_sandbox_team()` detecta inconsistencias entre team, manifest y artifact manifest.
- `artifact_type: team` vs `sandbox_team` queda auditado y documentado.
- No se crean agentes ni runtime.
- No se escribe en `domains/` operativo.
- Tests focales y checkpoints previos siguen verdes.

Marcas:

`SANDBOX_TEAM_TEMPLATE_MATERIALIZATION_READY`

`SANDBOX_TEAM_TEMPLATE_MATERIALIZATION_NO_OPERATIONAL_CONFIRMED`

`ready_for_phase_5_2_sandbox_team_audit`

## 15. Auditoria 5.2

PROMPT 5.2 confirma que la materializacion 5.1 queda coherente y no-operativa.

Resultado:

`SANDBOX_TEAM_AUDIT_PASSED`

`SANDBOX_TEAM_DECLARATIVE_NO_OPERATIONAL_CONFIRMED`

`ready_for_phase_5_3_internal_team_listing`

La auditoria endurece la validacion de `artifact_manifest` contra el equipo materializado: `domain_id`, `artifact_id`, `artifact_kind`, `team_id`, `source_team_template`, `materialization_id` en la ruta desde template y flags `operational/passed=false`.
