# Auditoria De Equipo Sandbox

Estado: `SANDBOX_TEAM_AUDIT_PASSED`

Veredicto: `SANDBOX_TEAM_DECLARATIVE_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_5_3_internal_team_listing`

## 1. Proposito

PROMPT 5.2 audita el equipo sandbox materializado en PROMPT 5.1 para confirmar que no sea solo un JSON decorativo. La auditoria verifica coherencia, trazabilidad, no-operatividad, manifest, miembros, permisos, politica de ejecucion, dependencies y preparacion para listado interno futuro.

Esta auditoria no ejecuta equipos, no crea agentes, no activa runtime, no toca UI y no abre integraciones.

## 2. Estado Actual De Fase 5

Fase 5 - Equipos reales sandbox queda en etapa de auditoria declarativa.

Cadena cerrada:

- PROMPT 5.0: schema de equipo sandbox real.
- PROMPT 5.1: materializacion declarativa desde `team_template`.
- PROMPT 5.2: auditoria del equipo sandbox materializado.

El siguiente paso permitido es `PROMPT 5.3 - Biblioteca interna/listado de equipos sandbox para futura UI`.

## 3. Que Creo 5.0

PROMPT 5.0 reconcilio `core/sandbox_team_schema.py` como contrato canonico. El schema exige:

- identidad propia (`team_id`, `artifact_id`, `materialization_id`);
- dominio sandbox (`domain_id`);
- diferencia entre `team_template` y equipo sandbox real;
- `source_team_template`;
- `created_from`;
- `members`;
- `permissions`;
- `execution_policy`;
- `validation`;
- estados no activos;
- compatibilidad con `artifact_manifest`.

El schema no escribe archivos ni ejecuta nada.

## 4. Que Creo 5.1

PROMPT 5.1 extendio `core/sandbox_team_materializer.py` con `materialize_sandbox_team_from_template()`.

La ruta materializa solo dentro de un dominio sandbox temporal/controlado:

- `sandbox_teams/<team_id>.json`;
- `sandbox_teams/<team_id>.manifest.json`;
- `manifests/artifact_manifest.json`;
- extension de `materialization_manifest.json`.

No crea `catalogs/team_templates.json`, no crea agentes, no crea runtime, no ejecuta modelos, no llama tools y no abre integraciones.

## 5. Coherencia Schema/Materializador

Veredicto: coherente.

El materializador construye el equipo mediante `build_sandbox_team_schema()` y vuelve a pasar por `validate_sandbox_team_schema()` antes de escribir. Luego `validate_materialized_sandbox_team()` valida post-materializacion:

- `team.json`;
- manifest especifico de equipo;
- `artifact_manifest`;
- policy default-deny;
- permisos sensibles;
- dependencies;
- lineage.

Correccion aplicada en 5.2: la validacion post-materializacion ahora audita con mayor precision el `artifact_manifest` contra el equipo:

- `artifact_manifest.domain_id`;
- `artifact_id`;
- `artifact_type: team`;
- `created_from.artifact_kind: sandbox_team`;
- `created_from.domain_id`;
- `created_from.team_id`;
- `created_from.source_team_template`;
- `created_from.materialization_id` en la ruta desde template;
- `operational=false`;
- `passed=false`.

## 6. Auditoria De No-Operatividad

Veredicto: no-operativo confirmado.

El equipo materializado mantiene bloqueados:

- runtime;
- execution;
- dry-run real;
- tools;
- model invocation;
- context injection;
- output delivery;
- writes/stores/memory operativos;
- network/browser;
- filesystem fuera del sandbox temporal/controlado;
- env/secrets;
- API/UI/UI-device;
- integrations;
- Market Catalog runtime;
- Business Composition Layer runtime;
- OBLITERATUS.

La materializacion no crea `runtime/`, `outputs/`, `execution_outputs/`, `stores/`, `memory/` ni `sandbox_agents/` cuando viene de `team_template` con `agent_reference=null`.

## 7. Auditoria De Artifact Manifest

Veredicto: compatible y trazable.

El equipo se registra en `manifests/artifact_manifest.json` como artefacto `team`. El registro conserva:

- `artifact_id`;
- `artifact_type: team`;
- `status=materialized`;
- `created_from`;
- `created_by`;
- `dependencies`;
- `rollback_info`;
- `operational=false`;
- `passed=false`.

La validacion 5.2 confirma que el manifest global pertenece al mismo `domain_id` que el equipo y que el registro apunta al mismo `team_id`, `artifact_id` y lineage.

## 8. Decision Artifact Type: Team Vs Artifact Kind

Decision confirmada:

```txt
artifact_type: team
artifact_kind: sandbox_team
```

`artifact_type: team` se mantiene por compatibilidad con `core/artifact_manifest_schema.py`, que acepta `team` como tipo global. `artifact_kind: sandbox_team` desambigua la semantica especifica del equipo sandbox real.

No hay evidencia de problema real que justifique cambiar la convencion en 5.2. Normalizar `artifact_type` a `sandbox_team` requeriria subprompt quirurgico futuro porque impactaria schema, tests y manifiestos historicos.

## 9. Auditoria De Members

Veredicto: declarativos y utiles.

Cada member exige:

- `member_id`;
- `role_id`;
- `role_name`;
- `agent_reference`;
- `responsibilities`;
- `inputs`;
- `outputs`;
- `status`;
- `artifact_state`.

`agent_reference` puede ser `null`. Eso preserva rol y responsabilidad sin forzar creacion de agente ni resolver contra runtime.

Los members no pueden estar `active`, no pueden declarar runtime y no pueden habilitar execution/tools/modelos/integraciones.

## 10. Auditoria De Permissions

Veredicto: permisos sensibles bloqueados.

El equipo exige `false` en:

- `can_execute`;
- `can_call_tools`;
- `can_call_models`;
- `can_write_outputs`;
- `can_access_network`;
- `can_use_integrations`.

Los tests de auditoria mutan cada permiso a `true` y confirman fallo.

## 11. Auditoria De Execution Policy

Veredicto: default-deny confirmado.

El equipo exige:

- `execution_enabled=false`;
- `runtime_enabled=false`;
- `tool_execution_enabled=false`;
- `model_invocation_enabled=false`;
- `external_integrations_enabled=false`;
- `human_approval_required=true`.

Los tests de auditoria mutan cada flag operativo a `true` y confirman fallo.

## 12. Auditoria De Lineage/Dependencies

Veredicto: trazabilidad suficiente.

Lineage validado:

```txt
team_template derivado
-> materialize_sandbox_team_from_template
-> sandbox_team schema 5.0
-> sandbox_teams/<team_id>.json
-> sandbox_teams/<team_id>.manifest.json
-> manifests/artifact_manifest.json
```

`source_team_template`, `created_from`, `team_template_id`, `domain_id`, `team_id`, `artifact_id` y `materialization_id` quedan trazados.

Cuando `agent_reference=null`, `dependencies=[]` es valido porque no hay agente sandbox materializado que depender. En fases futuras, si un member referencia agente, `dependencies` debe apuntar a `agent_reference.artifact_id`.

## 13. Riesgos Encontrados

Riesgos auditados:

- tratar una lista decorativa como equipo real;
- confundir `team_template` con equipo sandbox materializado;
- perder ambiguedad entre `artifact_type: team` y `sandbox_team`;
- dejar pasar `artifact_manifest` inconsistente;
- interpretar `agent_reference=null` como agente faltante;
- abrir execution/runtime por flags anidados.

Riesgo corregido en 5.2: se endurecio la validacion de `artifact_manifest` contra el equipo materializado.

No quedan riesgos bloqueantes para avanzar a 5.3.

## 14. Correcciones Aplicadas

Correccion aplicada:

- `validate_materialized_sandbox_team()` ahora valida `artifact_manifest.domain_id`, `artifact_id`, `artifact_kind`, `team_id`, `source_team_template`, `materialization_id` en ruta template y flags operativos del registro.

No se aplicaron refactors mayores.

## 15. Deudas Futuras

Deudas no bloqueantes:

- listar equipos sandbox de forma interna y read-only en PROMPT 5.3;
- definir si una fase futura acepta `artifact_type: sandbox_team` en el manifest global;
- auditar referencias reales a agentes sandbox cuando `agent_reference` deje de ser `null`;
- mantener UI fuera de Fase 5 hasta que exista contrato interno de listado.

## 16. Veredicto

`SANDBOX_TEAM_AUDIT_PASSED`

`SANDBOX_TEAM_DECLARATIVE_NO_OPERATIONAL_CONFIRMED`

El equipo sandbox materializado es coherente, trazable, no operativo, no decorativo, compatible con schema 5.0, compatible con materializacion 5.1 y compatible con `artifact_manifest`.

## 17. Readiness

`ready_for_phase_5_3_internal_team_listing`

Proximo prompt recomendado:

`PROMPT 5.3 - Biblioteca interna/listado de equipos sandbox para futura UI`

No avanzar a 5.3 dentro de este prompt.

## Confirmaciones Explicitas

- No crea agentes.
- No activa runtime.
- No ejecuta equipos.
- No invoca modelos.
- No llama tools.
- No toca UI.
- No abre integraciones.
- No habilita Market Catalog runtime.
- No habilita Business Composition Layer runtime.
- No incorpora OBLITERATUS.
