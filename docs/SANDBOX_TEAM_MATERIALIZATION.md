# Materializacion de equipos sandbox

## 1. Que se materializa

`core/sandbox_team_materializer.py` materializa un equipo sandbox como artefacto declarativo dentro de un dominio sandbox existente.

El archivo se escribe en:

```txt
<sandbox>/<domain_id>/sandbox_teams/<team_id>.json
```

El equipo contiene:

- `team_id`;
- `domain_id`;
- `name`;
- `purpose`;
- `status`;
- `version`;
- `member_agents`;
- `coordination_model`;
- `capabilities`;
- `dependencies`;
- `rollback_info`;
- `history`.

## 2. Diferencia con runtime

```txt
team materialized != team active != team runtime
```

`team materialized` significa que existe un artefacto trazable dentro del sandbox.

No significa:

- ejecucion;
- coordinacion real;
- debate real;
- pipeline real;
- activacion de agentes;
- llamadas externas;
- memoria real;
- herramientas reales.

## 3. Miembros

Relacion:

```txt
sandbox_agents
  -> sandbox_team
```

El materializador requiere agentes sandbox existentes en:

```txt
<sandbox>/<domain_id>/sandbox_agents/
```

Cada miembro conserva:

- `agent_id`;
- rol;
- especializacion;
- responsabilidad;
- referencia al artefacto `agent_<agent_id>`;
- estado `materialized`.

El equipo no puede referenciar agentes inexistentes, duplicados, `active` o con `runtime_enabled=true`.

## 4. Coordinacion declarativa

La coordinacion permitida es declarativa.

Tipos:

- `none`;
- `single_coordinator`;
- `parallel_review`;
- `sequential_pipeline`;
- `debate_future`;
- `approval_future`.

Bloqueos:

- no `execute=true`;
- no `runtime_enabled=true`;
- no `execution_enabled=true`;
- no `pipeline_enabled=true`;
- no `debate_enabled=true`.

## 5. Capabilities

El equipo puede declarar:

- memoria futura;
- herramientas futuras;
- policies futuras.

Todas las capacidades siguen siendo declarativas:

- `declared_only=true`;
- `runtime_enabled=false`;
- `execution_allowed=false`;
- `external_access=false`.

No se implementa `capability_policy` en este prompt.

## 6. Rollback y regeneracion

`rollback_sandbox_team()` elimina solo el equipo sandbox materializado.

Conserva:

- sandbox agents;
- paper_seed;
- agent_presets;
- profile_catalog;
- dominio sandbox.

`regenerate_sandbox_team()` mantiene `team_id`, incrementa version patch, archiva la version anterior en `sandbox_teams/history/` y conserva miembros/dependencias.

## 7. Seguridad

El materializador:

- registra `artifact_type: team`;
- mantiene `status: materialized`;
- bloquea runtime;
- bloquea ejecucion;
- bloquea external access;
- no escribe en `agents/`;
- no escribe en `domains/` operativo;
- no modifica catalogos globales;
- no modifica papers globales.

## 8. Artifact manifest

El equipo se registra como:

```txt
artifact_type: team
artifact_id: team_<team_id>
dependencies:
  - profile_catalog_main
  - agent_presets_main
  - paper_seed_main
  - agent_<agent_id>
```

El manifest conserva rollback y versionado, pero no ejecuta coordinacion.
