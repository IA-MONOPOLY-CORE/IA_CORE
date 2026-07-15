# Contrato de agente sandbox

## Proposito

Un agente sandbox es el contrato previo a crear un agente operativo. Todavia no es una configuracion ejecutable ni debe aparecer como agente activo.

El contrato existe para que la futura materializacion de agentes nazca con identidad, trazabilidad, dependencias y rollback definidos.

## Diferencia con agente operativo

Agente sandbox:

- es un artefacto de contrato;
- no ejecuta tareas;
- no tiene runtime propio;
- no crea memoria;
- no tiene herramientas activas;
- no participa en equipos;
- no escribe configs en `agents/` ni en dominios operativos.

Agente operativo futuro:

- tendra configuracion ejecutable;
- podra tener memoria propia o compartida;
- podra usar herramientas aprobadas;
- dependera de paper operativo y validacion PASSED;
- podra llegar a `active` solo con trazabilidad completa.

## Campos requeridos

`core/sandbox_agent_schema.py` exige:

- `agent_id`;
- `domain_id`;
- `profile_reference`;
- `preset_reference`;
- `paper_reference`;
- `role`;
- `specialization`;
- `model_policy_reference`;
- `status`;
- `version`;
- `dependencies`;
- `rollback_info`;
- `created_at`;
- `updated_at`.

## Dependencias

Cadena obligatoria:

```txt
profile_catalog_main
  -> agent_presets_main
    -> paper_seed_main
      -> agent_<agent_id>
```

El agente sandbox no deberia existir si faltan:

- perfil derivado;
- preset materializado;
- seed documental.

## Estados

Se reutiliza `core/artifact_state.py`.

Estados aceptados para contrato:

- `ready_to_materialize`;
- `materialized`;
- `archived`;
- `broken`.

`active` esta bloqueado en esta fase.

## Artifact Manifest

El futuro registro sera:

```txt
artifact_type: agent
dependencies:
  - profile_catalog_main
  - agent_presets_main
  - paper_seed_main
```

El manifest debe conservar:

- identidad del agente;
- referencias a perfil, preset y paper seed;
- version;
- status;
- rollback;
- historial futuro.

## Rollback

El contrato define `rollback_info`, pero no implementa rollback de agentes.

Cuando se materialicen agentes reales, rollback debera poder eliminar:

- config del agente;
- referencias runtime;
- memoria propia creada;
- papers operativos derivados si corresponde.

No debera eliminar automaticamente `profile_catalog`, `agent_presets` ni `paper_seed`.

## Memoria futura

La memoria debe tratarse como artefacto separado si aparece cualquiera de estas condiciones:

- memoria propia persistente del agente;
- memoria compartida entre agentes;
- indices vectoriales;
- herramientas con estado;
- evolucion o aprendizaje versionado.

En ese caso, `memory` deberia registrarse como `artifact_type: memory` y depender del agente o del paper operativo segun corresponda.

## Evolucion futura

El contrato deja diferidos:

- creacion real de agente;
- paper operativo;
- herramientas;
- memoria;
- equipos;
- activacion PASSED;
- UI e integraciones.

El siguiente paso natural es un materializador de agentes sandbox que consuma este contrato y escriba configs solo dentro del sandbox.
