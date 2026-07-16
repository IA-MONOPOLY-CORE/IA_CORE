# Checkpoint end-to-end con equipos sandbox

## 1. Resumen ejecutivo

La cadena completa con `sandbox_team` esta lista para avanzar a `capability_policy`.

El checkpoint valida materializacion, manifest, lineage, dependencias, runtime boundary, rollback, regeneracion e isolation legacy en sandbox temporal.

Veredicto: `PASSED_TEAM_CHAIN`.

## 2. Flujo validado

```txt
domain -> profile_catalog -> presets -> paper_seed -> agents -> team
```

Todo ocurre dentro de `tmp_path` y no toca dominios operativos.

## 3. Resultado por capa

| Capa | Estado | Evidencia | Riesgo |
|---|---|---|---|
| Dominio sandbox | PASSED | `materialize_sandbox_domain` y rollback total | bajo |
| Profile catalog | PASSED | artefacto `profile_catalog_main` materialized | bajo |
| Agent presets | PASSED | artefacto `agent_presets_main` materialized | bajo |
| Paper seed | PASSED | artefacto `paper_seed_main` materialized | bajo |
| Sandbox agents | PASSED | agentes materialized con lineage y runtime false | bajo |
| Sandbox team | PASSED | `artifact_type: team` materialized | bajo |
| Capacidades declarativas | PASSED | tools/policies declarativas sin ejecucion | medio futuro |
| Coordinacion declarativa | PASSED | `execution_enabled=false` | medio futuro |

## 4. Manifest y dependencias

El manifest contiene:

```txt
profile_catalog
agent_preset
paper_seed
agent
agent
team
```

El equipo se registra como:

```txt
artifact_type: team
artifact_id: team_checkpoint_team
```

Dependencias registradas:

```txt
profile_catalog_main
agent_presets_main
paper_seed_main
agent_<agent_id>
```

El contrato interno del team depende de agentes sandbox. Las dependencias base quedan en el registro de manifest para trazabilidad de la cadena completa.

## 5. Runtime boundary

Confirmado:

- no `active`;
- no runtime;
- no execution;
- no external access;
- agentes con `runtime_enabled=false`;
- equipo con `runtime_enabled=false`;
- coordinacion con `execution_enabled=false`;
- tools/policies declarativas sin ejecucion.

## 6. Rollback y regeneracion

Rollback selectivo validado:

```txt
rollback sandbox_team
rollback sandbox_agents
rollback paper_seed
rollback agent_presets
rollback profile_catalog
rollback sandbox domain
```

Resultados:

- rollback de equipo elimina solo el equipo;
- rollback de equipo conserva agentes;
- rollback de agentes conserva `paper_seed`, `agent_presets` y `profile_catalog`;
- rollback total deja sandbox temporal sin dominios materializados;
- no quedan archivos huerfanos del equipo;
- manifest queda consistente.

Regeneracion:

- `team_id` conservado;
- version incrementada de `1.0.0` a `1.0.1`;
- historial conserva `materialized` y `regenerated`;
- miembros y dependencias conservadas;
- runtime sigue bloqueado.

## 7. Veredicto

`PASSED_TEAM_CHAIN`

## 8. Recomendacion

Listo para capability_policy.
