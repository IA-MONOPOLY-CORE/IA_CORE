# Materializacion de agentes sandbox

## Proposito

`core/sandbox_agent_materializer.py` crea una configuracion de agente dentro de un dominio sandbox.

El agente sandbox no es un trabajador operativo. Es una instancia materializada, trazable y preparada para una futura capa de ejecucion.

## Dependencias

La materializacion requiere:

```txt
profile_catalog_main
  -> agent_presets_main
    -> paper_seed_main
      -> agent_<agent_id>
```

El materializador valida que existan:

- `profile_catalog`;
- `agent_presets`;
- `paper_seed`;
- `artifact_manifest`;
- lineage valido.

## Ubicacion

El agente se escribe dentro del sandbox:

```txt
<sandbox>/<domain_id>/sandbox_agents/<agent_id>.json
```

No escribe en:

- `agents/`;
- `domains/` operativo;
- runtime;
- memoria operativa.

## Contenido del agente

Cada config contiene:

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
- `lineage`;
- `dependencies`;
- `rollback_info`;
- `sandbox_config`.

`sandbox_config` conserva seeds tecnicas para futuro runtime, pero declara:

```txt
runtime_enabled: false
operational: false
```

## Artifact Manifest

El registro futuro se materializa como:

```txt
artifact_type: agent
artifact_id: agent_<agent_id>
status: materialized
dependencies:
  - profile_catalog_main
  - agent_presets_main
  - paper_seed_main
```

`created_from.lineage` embebe metadata de lineage sin duplicar el historial completo.

## Lineage

La primera materializacion agrega evento:

```txt
materialized
```

La regeneracion conserva `agent_id`, incrementa version y agrega:

```txt
regenerated
```

Si en una fase posterior se requiere reemplazo de identidad, debera usarse `replaced_by` con un nuevo `agent_id`.

## Rollback

`rollback_sandbox_agent()` elimina solo:

```txt
<sandbox>/<domain_id>/sandbox_agents/
```

Conserva:

- `profile_catalog`;
- `agent_presets`;
- `paper_seed`;
- artifact_manifest de dependencias base.

## Diferencia con agente operativo

Agente sandbox:

- no ejecuta;
- no carga modelos;
- no crea memoria;
- no expone herramientas;
- no se registra en loader runtime;
- no esta `active`.

Agente operativo futuro:

- podra tener config runtime;
- podra tener paper operativo;
- podra tener memoria propia o compartida;
- podra usar herramientas aprobadas;
- requerira PASSED especifico.

## Auditoria de cierre

- El agente nace con identidad completa.
- Las dependencias quedan trazadas.
- El lineage funciona como historia evolutiva.
- Core, sandbox y runtime quedan separados.
- La memoria y herramientas siguen fuera de alcance hasta que exista un prompt especifico.
