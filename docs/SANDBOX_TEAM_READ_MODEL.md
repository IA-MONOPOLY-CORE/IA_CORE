# Sandbox Team Read Model

Estado: `SANDBOX_TEAM_READ_MODEL_READY`

Veredicto: `SANDBOX_TEAM_INTERNAL_LISTING_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_next_architecture_block_after_phase_5`

## 1. Proposito

`core/sandbox_team_read_model.py` define un listado interno, read-only y JSON-safe de equipos sandbox materializados.

El objetivo es permitir inspeccion interna y preparar una futura UI sin crear UI real, endpoints publicos, runtime, ejecucion, agentes, tools, modelos ni integraciones.

## 2. Relacion Con Fase 5

Fase 5 - Equipos reales sandbox cierra su bloque minimo con:

1. PROMPT 5.0 - schema de equipo sandbox real.
2. PROMPT 5.1 - materializacion declarativa desde `team_template`.
3. PROMPT 5.2 - auditoria de equipo sandbox.
4. PROMPT 5.3 - read model/listado interno para futura UI.

## 3. Relacion Con 5.0 Schema

El read model consume equipos que ya pasan `core.sandbox_team_schema.validate_sandbox_team_schema()`.

No reemplaza el schema. Solo proyecta una vista segura y compacta.

## 4. Relacion Con 5.1 Materializacion

El read model lee equipos creados por `materialize_sandbox_team_from_template()` y validados por `validate_materialized_sandbox_team()`.

No crea equipos, no regenera equipos y no modifica manifests.

## 5. Relacion Con 5.2 Auditoria

El read model se apoya en la auditoria 5.2:

- `artifact_manifest` endurecido;
- `artifact_type: team` confirmado;
- `artifact_kind: sandbox_team` confirmado;
- permissions bloqueadas;
- execution_policy bloqueada;
- members declarativos;
- no-operatividad confirmada.

## 6. Contrato De Listado Interno

Funciones publicas:

- `list_sandbox_teams(domain_dir)`;
- `get_sandbox_team_summary(domain_dir, team_id=...)`;
- `build_sandbox_team_read_model(validation)`;
- `validate_sandbox_team_read_model(payload)`.

El listado acepta un `domain_dir` sandbox explicito y bloquea `domains/` operativo y `agents/` runtime.

## 7. Payload Minimo

Cada equipo se proyecta como:

```json
{
  "team_id": "",
  "domain_id": "",
  "name": "",
  "description": "",
  "team_type": "sandbox",
  "status": "",
  "artifact_state": "",
  "artifact_id": "",
  "artifact_type": "team",
  "artifact_kind": "sandbox_team",
  "materialization_id": "",
  "source_team_template": {},
  "members_count": 0,
  "members_summary": [],
  "permissions_summary": {},
  "execution_policy_summary": {},
  "operational": false,
  "passed": false,
  "readiness": "sandbox_team_non_operational_confirmed",
  "warnings": [],
  "validation": {},
  "created_at": "",
  "updated_at": "",
  "metadata": {}
}
```

## 8. Members Summary

`members_summary` es declarativo y compacto:

```json
{
  "member_id": "",
  "role_id": "",
  "role_name": "",
  "specialization_id": "",
  "specialization_name": "",
  "has_agent_reference": false,
  "responsibilities_count": 0,
  "status": "",
  "artifact_state": ""
}
```

No expone `agent_reference`, `member_agents`, prompts, payloads internos, runtime handles ni configuraciones sensibles.

## 9. Permissions Summary

Debe contener permisos sensibles en `false`:

- `can_execute`;
- `can_call_tools`;
- `can_call_models`;
- `can_write_outputs`;
- `can_access_network`;
- `can_use_integrations`.

Si alguno aparece `true`, el read model falla con error controlado.

## 10. Execution Policy Summary

Debe contener:

- `execution_enabled=false`;
- `runtime_enabled=false`;
- `tool_execution_enabled=false`;
- `model_invocation_enabled=false`;
- `external_integrations_enabled=false`;
- `human_approval_required=true`.

Si algun flag operativo aparece `true`, el read model falla con error controlado.

## 11. Readiness

Readiness permitidas para el listado:

- `sandbox_team_non_operational_confirmed`;
- `sandbox_team_invalid`;
- `sandbox_team_requires_audit`;
- `sandbox_team_broken`;

Readiness de cierre del bloque:

`ready_for_next_architecture_block_after_phase_5`

No se permite readiness que sugiera runtime, execution, activacion, tools, modelos, integraciones o UI operativa.

## 12. Relacion Con Artifact Manifest

El read model conserva la decision:

```txt
artifact_type: team
artifact_kind: sandbox_team
```

`artifact_type: team` mantiene compatibilidad con `core/artifact_manifest_schema.py`.
`artifact_kind: sandbox_team` expresa semantica especifica sin ambiguedad.

## 13. Relacion Con Futura UI

Este read model prepara payload legible para futura UI.

La UI futura puede consumirlo como vista interna filtrada, no como fuente de reglas operativas.

## 14. Que Puede Mostrar La UI Futura

- equipo;
- dominio;
- estado;
- origen `team_template`;
- miembros resumidos;
- permisos bloqueados;
- execution policy bloqueada;
- warnings;
- readiness;
- acciones futuras sugeridas por otro contrato.

## 15. Que NO Puede Hacer La UI Futura

- activar equipo;
- ejecutar equipo;
- crear agentes;
- crear equipos;
- resolver permisos;
- corregir inconsistencias;
- materializar;
- mutar manifests;
- invocar modelos;
- llamar tools;
- abrir integraciones.

## 16. Reglas De No-Operatividad

El read model:

- es read-only;
- no escribe archivos;
- no crea stores;
- no crea API;
- no crea UI;
- no ejecuta runtime;
- no invoca modelos;
- no llama tools;
- no toca red;
- no lee env/secrets;
- no toca Market Catalog runtime;
- no toca Business Composition Layer runtime;
- no incorpora OBLITERATUS.

## 17. Errores Esperados

Errores controlados:

- `domains/` operativo usado como fuente;
- `artifact_manifest` ausente;
- manifest inconsistente;
- `artifact_kind` distinto de `sandbox_team`;
- `artifact_type` distinto de `team`;
- `operational=true`;
- `passed=true`;
- permiso sensible `true`;
- flag operativo `true`;
- payload no JSON-safe;
- presencia de campos sensibles como secrets/env/runtime handles/tool configs/model configs.

## 18. Criterios De Cierre De Fase 5 Minima

Fase 5 minima queda cerrada si:

- existe schema de equipo sandbox real;
- existe materializacion declarativa desde `team_template`;
- existe auditoria de equipo sandbox;
- existe read model/listado interno seguro;
- tests focales pasan;
- no se abrio runtime, execution, UI ni integraciones;
- queda readiness para planificar el siguiente bloque arquitectonico.

Marcas de cierre:

`SANDBOX_TEAM_READ_MODEL_READY`

`SANDBOX_TEAM_INTERNAL_LISTING_NO_OPERATIONAL_CONFIRMED`

`ready_for_next_architecture_block_after_phase_5`
