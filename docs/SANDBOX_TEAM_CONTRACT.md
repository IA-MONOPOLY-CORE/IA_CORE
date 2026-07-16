# Contrato de equipo sandbox

## 1. Que es un equipo sandbox

Un equipo sandbox es un contrato de coordinacion entre agentes sandbox.

No es una lista decorativa de agentes y tampoco es un runtime. Declara miembros, objetivo, dependencias, reglas de coordinacion y capacidades futuras sin ejecutar nada.

Diferencias:

- `team contract`: estructura validable en memoria, sin filesystem operativo.
- `team materialized`: fase futura que podra escribir un artefacto sandbox trazable.
- `team runtime`: fase futura, no implementada, donde podria existir coordinacion real.

PROMPT 2.6 solo define `team contract`.

## 2. Relacion con agentes

Relacion conceptual:

```txt
sandbox_agent
  -> sandbox_team
```

El equipo depende de agentes sandbox, no de presets directamente.

Los presets, perfiles y paper_seed son dependencias indirectas de cada agente. El equipo se apoya en artefactos `agent_<agent_id>` porque la unidad coordinable es el agente sandbox ya definido.

## 3. Miembros

Cada miembro declara:

- `agent_id`;
- `role`;
- `specialization`;
- `responsibility`;
- `required`;
- `source_reference`;
- `status`.

Reglas:

- no hay equipo sin miembros;
- no hay miembro sin `agent_id`;
- no hay miembro sin `responsibility`;
- no hay agentes duplicados;
- no hay miembros `active`;
- no hay miembros con `runtime_enabled=true`;
- no hay miembros con `execution_enabled=true`.

`required=true` indica que el miembro es necesario para que el equipo futuro tenga sentido, pero no ejecuta nada.

## 4. Coordinacion declarativa

`coordination_model` declara estructura, no orquestacion real.

Tipos permitidos:

- `none`;
- `single_coordinator`;
- `parallel_review`;
- `sequential_pipeline`;
- `debate_future`;
- `approval_future`.

El modelo puede declarar:

- `coordinator_agent_id`;
- reglas declarativas;
- orden sugerido;
- restricciones.

Bloqueos:

- `declared_only=true`;
- `runtime_enabled=false`;
- `execution_enabled=false`;
- sin debate real;
- sin pipeline real;
- sin orquestador runtime.

## 5. Capacidades futuras

El equipo puede declarar:

```json
{
  "memory": [],
  "tools": [],
  "policies": []
}
```

La memoria y herramientas reutilizan los criterios de contratos declarativos de agentes sandbox:

- memoria: `declared_only=true`, `runtime_enabled=false`;
- herramientas: `declared_only=true`, `runtime_enabled=false`, `execution_allowed=false`, `external_access=false`;
- policies: `declared_only=true`, `runtime_enabled=false`, `execution_enabled=false`, `external_access=false`.

Esto no crea memoria real, herramientas reales, permisos reales ni integraciones.

## 6. Seguridad

Bloqueos obligatorios:

- no `active`;
- no runtime;
- no execution;
- no external access;
- no legacy mutation;
- no escritura en `agents/`;
- no escritura en `domains/` operativo;
- no modificacion de catalogos globales;
- no modificacion de papers globales.

## 7. Artifact manifest futuro

`artifact_manifest_schema.py` ya contempla:

```txt
artifact_type: team
```

Cuando una fase futura materialice equipos, el registro esperado sera:

```txt
artifact_id: team_<team_id>
artifact_type: team
dependencies:
  - agent_<agent_id>
```

El contrato actual valida compatibilidad futura, pero no escribe el manifest.

## 8. Futuro

Queda para fases posteriores:

- materializador de equipos sandbox;
- rollback real de equipos materializados;
- memoria propia de equipo;
- herramientas propias de equipo;
- capability_policy;
- permisos;
- auditoria de coordinacion;
- runtime de equipos;
- UI e integraciones.

Recomendacion: antes de ejecutar equipos reales, cerrar una `capability_policy` comun para agentes y equipos.
