# Sandbox Team Schema

Estado: `SANDBOX_TEAM_SCHEMA_READY`

Veredicto: `SANDBOX_TEAM_SCHEMA_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_5_1_team_template_materialization`

## 1. Proposito

`core/sandbox_team_schema.py` define el schema minimo de un equipo real sandbox como estructura declarativa, trazable, validable y no operativa.

El contrato permite representar un equipo dentro de un dominio sandbox sin materializar equipos operativos, ejecutar agentes, abrir runtime multiagente, invocar modelos, llamar tools ni conectar integraciones.

## 2. Relacion Con Fase 5

PROMPT 5.0 inicia Fase 5 - Equipos reales sandbox. Esta fase empieza por schema porque un equipo no puede materializarse desde `team_template` si antes no existe una forma validable de identidad, miembros, lineage, permisos y politica de no ejecucion.

El siguiente paso permitido es `PROMPT 5.1 - Materializar equipo real desde team_template`.

## 3. Team Template Vs Equipo Sandbox Real

`team_template`:

- es derivado o reusable;
- no es operativo;
- no esta necesariamente asociado a un dominio materializado;
- no ejecuta agentes;
- puede alimentar una creacion futura.

Equipo real sandbox:

- pertenece a un `domain_id` sandbox;
- tiene `team_id` y `artifact_id` propios;
- tiene estado y `artifact_state`;
- declara miembros con roles, especializaciones y responsabilidades;
- conserva `created_from`, `source_team_template` y `materialization_id`;
- se prepara para `artifact_manifest`;
- mantiene runtime, tools, modelos, outputs e integraciones bloqueados.

## 4. Campos Obligatorios

- `schema_version`
- `team_id`
- `domain_id`
- `name`
- `description`
- `team_type`
- `status`
- `artifact_state`
- `created_from`
- `source_team_template`
- `materialization_id`
- `artifact_id`
- `members`
- `coordination_model`
- `permissions`
- `execution_policy`
- `validation`
- `warnings`
- `metadata`
- `created_at`
- `updated_at`

El builder mantiene `purpose`, `member_agents`, `version`, `dependencies`, `rollback_info` y `capabilities` como compatibilidad con contratos historicos no operativos.

## 5. Campos Opcionales

- `purpose`: alias historico de `description`.
- `member_agents`: alias historico para materializadores anteriores.
- `version`: version semver del artefacto.
- `capabilities`: memoria, tools y policies declarativas futuras.
- `dependencies`: dependencias calculadas desde `agent_reference.artifact_id`.
- `rollback_info`: rollback futuro declarativo.
- `history` y `materialization`: metadata historica si un materializador sandbox las agrega.

## 6. Schema Conceptual

```json
{
  "schema_version": "1.0",
  "team_id": "sandbox_growth_team",
  "domain_id": "sandbox_marketing_crm_automation",
  "name": "Sandbox Growth Team",
  "description": "Coordina analisis y revision sin ejecucion runtime.",
  "team_type": "sandbox",
  "status": "materialized",
  "artifact_state": "materialized",
  "created_from": {},
  "source_team_template": {},
  "materialization_id": "mat_sandbox_growth_team",
  "artifact_id": "team_sandbox_growth_team",
  "members": [],
  "coordination_model": {},
  "permissions": {},
  "execution_policy": {},
  "validation": {},
  "warnings": [],
  "metadata": {},
  "created_at": "2026-07-15T00:00:00",
  "updated_at": "2026-07-15T00:00:00"
}
```

## 7. Ejemplo Valido

```json
{
  "team_type": "sandbox",
  "status": "materialized",
  "artifact_state": "materialized",
  "members": [
    {
      "member_id": "sandbox_growth_strategist",
      "role_id": "estratega",
      "role_name": "Estratega",
      "specialization_id": "negocio_digital",
      "specialization_name": "Negocio Digital",
      "agent_reference": {
        "agent_id": "sandbox_growth_strategist",
        "artifact_id": "agent_sandbox_growth_strategist",
        "artifact_type": "agent"
      },
      "responsibilities": ["Define hipotesis y criterios de priorizacion."],
      "inputs": [],
      "outputs": [],
      "status": "materialized",
      "artifact_state": "materialized"
    }
  ],
  "execution_policy": {
    "execution_enabled": false,
    "runtime_enabled": false,
    "tool_execution_enabled": false,
    "model_invocation_enabled": false,
    "external_integrations_enabled": false,
    "human_approval_required": true
  },
  "permissions": {
    "can_execute": false,
    "can_call_tools": false,
    "can_call_models": false,
    "can_write_outputs": false,
    "can_access_network": false,
    "can_use_integrations": false
  }
}
```

## 8. Ejemplos Invalidos

- `team_type != "sandbox"`.
- `status = "active"` o `artifact_state = "active"`.
- `members = []`.
- miembro sin `role_id`.
- miembro sin `responsibilities`.
- `execution_policy.execution_enabled = true`.
- `execution_policy.runtime_enabled = true`.
- `execution_policy.tool_execution_enabled = true`.
- `execution_policy.model_invocation_enabled = true`.
- `execution_policy.external_integrations_enabled = true`.
- cualquier permiso sensible en `true`.
- `source_team_template`, `materialization_id`, `artifact_id` o `created_from` ausentes.
- payload no serializable como JSON.

## 9. Estados Permitidos

El equipo y sus miembros no pueden estar `active`.

Estados aceptados:

- `ready_to_materialize`
- `materialized`
- `validated`
- `candidate_for_activation`

`active` queda bloqueado hasta una fase posterior explicita con PASSED operativo.

## 10. Politica De No Ejecucion

`execution_policy` es obligatoria y default-deny:

- `execution_enabled=false`
- `runtime_enabled=false`
- `tool_execution_enabled=false`
- `model_invocation_enabled=false`
- `external_integrations_enabled=false`
- `human_approval_required=true`

El validador no escribe archivos, no registra equipos, no materializa agentes, no llama runtime, no invoca modelos, no llama tools y no abre integraciones.

## 11. Permisos Bloqueados

`permissions` debe mantener en `false`:

- `can_execute`
- `can_call_tools`
- `can_call_models`
- `can_write_outputs`
- `can_access_network`
- `can_use_integrations`

Tambien se rechazan flags anidados que intenten habilitar execution, runtime, tools, modelos, integraciones, external access o permisos operativos.

## 12. Relacion Con Artifact Manifest

El equipo real sandbox define `artifact_id` y `dependencies` para futuro registro en `artifact_manifest`.

Por compatibilidad con `core/artifact_manifest_schema.py`, el registro vigente usa:

```txt
artifact_type: team
artifact_id: team_<team_id>
created_from.artifact_kind: sandbox_team
```

No se escribe `artifact_manifest.json` en PROMPT 5.0. Solo se valida compatibilidad en memoria.

## 13. Relacion Futura Con Agentes Sandbox

Cada miembro puede declarar `agent_reference` o dejarlo en `null` si el agente todavia no existe.

Cuando existe referencia a agente, la dependency esperada sale de `agent_reference.artifact_id`. Cuando la referencia es `null`, el miembro sigue siendo declarativo y no ejecutable.

## 14. Que NO Hace Este Schema

- No materializa equipos reales.
- No crea agentes.
- No ejecuta agentes.
- No activa runtime multiagente.
- No crea scheduler, worker, queue, orchestrator, dispatcher ni event bus.
- No invoca modelos.
- No llama tools.
- No escribe outputs.
- No toca UI.
- No abre integraciones.
- No habilita Market Catalog runtime.
- No habilita Business Composition Layer runtime.
- No incorpora OBLITERATUS.

## 15. Criterios Para Avanzar A 5.1

- `core/sandbox_team_schema.py` valida el contrato canónico 5.0.
- La diferencia `team_template` vs equipo sandbox real esta documentada.
- `execution_policy` y `permissions` bloquean ejecucion real.
- `tests/test_sandbox_team_schema.py` pasa.
- Checkpoints 4.9 y 4.8 siguen verdes.
- No se crearon equipos operativos ni agentes nuevos.

Marca de cierre:

`SANDBOX_TEAM_SCHEMA_READY`

`SANDBOX_TEAM_SCHEMA_NO_OPERATIONAL_CONFIRMED`

`ready_for_phase_5_1_team_template_materialization`
