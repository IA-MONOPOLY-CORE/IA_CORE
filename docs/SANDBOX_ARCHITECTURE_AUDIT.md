# Auditoria de preparacion de arquitectura sandbox

## Estado actual

La Fase 1 deja implementado:

- preview no operativo en `core/domain_materialization_preview.py`;
- schema sandbox en `core/sandbox_domain_schema.py`;
- materializacion controlada en `core/domain_materializer.py`;
- rollback idempotente en `core/domain_materialization_rollback.py`;
- ciclo completo y regeneracion en `core/sandbox_lifecycle_validation.py`;
- estados de dominio y artefacto en `core/domain_state.py` y `core/artifact_state.py`;
- identidad/equivalencia en `core/domain_identity.py`;
- tests de schema, materializacion, rollback y ciclo completo.

No existen todavia `profile_catalog`, `agent_presets`, papers, agentes, equipos ni memoria materializados dentro del sandbox.

## Fortalezas

- La creacion directa sobre `domains/` operativo esta bloqueada.
- El sandbox se materializa solo en raiz controlada.
- `domain.json` tiene identidad, origen, estado, revision humana, rollback y validacion.
- `materialization_manifest.json` registra paths creados, version de generacion e historial.
- Rollback elimina solo paths declarados y conserva evidencia en `_rollback_records`.
- Regeneracion ejecuta rollback antes de recrear, evitando sobrescritura silenciosa.
- `materialized` no equivale a `active`.
- Los tests cubren ida, vuelta, idempotencia y no contaminacion de `domains/`.

## Riesgos

- El manifest actual registra paths, pero no un grafo de artefactos con dependencias internas.
- Rollback actual es completo por materializacion, no parcial por artefacto.
- `artifact_state` es generico; puede alcanzar para Fase 2, pero papers/agentes/equipos probablemente requieran estados o subestados mas especificos.
- La identidad de dominio esta bien para dominios, pero las futuras identidades de perfiles, presets, papers, agentes y equipos deben tener su propio contrato.
- La estructura fisica futura no esta fijada en codigo: hoy solo existen `domain.json` y `materialization_manifest.json`.

## Huecos Antes de Fase 2

Obligatorio antes de materializar `profile_catalog` y `agent_presets`:

- Definir manifest de artefactos dentro del sandbox, por ejemplo `manifests/artifacts_manifest.json`.
- Definir identificadores estables para artefactos: `artifact_id`, `artifact_type`, `source`, `depends_on`, `state`.
- Definir convencion de paths para:
  - `profile_catalog/`
  - `agent_presets/`
  - `manifests/`
- Definir validacion post-materializacion para artefactos derivados.
- Extender rollback para registrar artefactos creados, aunque el rollback siga siendo completo.

No bloquea Fase 2, pero debe resolverse antes de papers/agentes/equipos:

- Grafo de dependencias entre presets, papers, agentes, equipos y memoria.
- Rollback parcial o selectivo.
- Versionado por artefacto.
- Estados especificos para agentes/equipos si aparecen flujos propios.

## Recomendaciones

### Obligatorio antes de avanzar

- Crear subprompt 1.4.1 o abrir Fase 2.0 con una primera tarea de contrato de `artifact_manifest` sandbox antes de escribir `profile_catalog` y `agent_presets`.
- Mantener Fase 2 limitada a `profile_catalog` y `agent_presets`; no mezclar papers, agentes, equipos ni memoria.
- Exigir que cada artefacto materializado tenga `artifact_state`, `source_request`, `materialization_id`, `created_paths` y `depends_on`.

### Recomendable futuro

- Separar `artifact_state` generico de estados operativos especificos si agentes o equipos ganan ciclo propio.
- Agregar validaciones de capacidad para sandboxes grandes.
- Agregar reporte de dependencias por generacion.
- Agregar rollback parcial cuando existan modificaciones, backups y relaciones cruzadas.

### No necesario ahora

- Crear `agent_state` o `team_state` antes de tener agentes/equipos reales.
- Implementar migracion a productivo.
- Implementar UI.
- Implementar integraciones externas.

## Auditoria de identidad de dominio

La identidad actual soporta dominios complejos a nivel de nombre, slug, alias, area/nicho y equivalencias conceptuales, incluyendo el caso Loteria. Puede convivir con dominios internos porque `list_domains(include_internal=True)` alimenta validaciones y porque legacy/demo quedan ocultos del flujo activo.

Limitacion: la identidad distingue dominios, no versiones internas del mismo dominio. Las generaciones viven en manifest, no en `domain_identity.py`. Esto es correcto para evitar duplicados de dominio, pero Fase 2 debe definir identidad de artefactos dentro del dominio.

## Auditoria de estructura sandbox

La estructura actual:

```txt
domain/
  domain.json
  materialization_manifest.json
```

Puede crecer hacia:

```txt
domain/
  domain.json
  profile_catalog/
  agent_presets/
  papers/
  agents/
  teams/
  memory/
  manifests/
```

Recomendacion: antes de crear `profile_catalog` y `agent_presets`, agregar `manifests/` y un manifest de artefactos. No es necesario cambiar la raiz sandbox actual.

## Auditoria de manifest y trazabilidad

La trazabilidad actual alcanza para reconstruir la materializacion de la raiz del dominio: id, generacion, paths, rollback, historial y metadata de ejecucion.

No alcanza todavia para reconstruir una instancia completa con 100 perfiles, 200 presets, papers, agentes y equipos, porque no existe registro por artefacto ni dependencias entre artefactos.

## Auditoria de estados

`domain_state` alcanza para dominio. `artifact_state` alcanza para derivados y artefactos simples de Fase 2 si se usa de forma disciplinada.

No hace falta crear `agent_state` o `team_state` ahora. Si papers/agentes/equipos pasan a tener ejecucion, aprobacion, memoria o health checks propios, convendra crear estados especificos.

## Auditoria de rollback futuro

Rollback actual revierte paths creados por una materializacion sandbox completa. Para Fase 2, si `profile_catalog` y `agent_presets` se agregan como paths creados por la misma materializacion, el rollback completo alcanza.

No alcanza para rollback parcial, restaurar backups, o preservar referencias cruzadas entre agentes/papers/equipos. Eso debe tratarse antes de Fase 3 o Fase 4.

## Auditoria de regeneracion

`regenerate_sandbox_domain()` reconstruye la capa inicial del sandbox. Conserva `previous_materialization_id`, `generation_number` e `lifecycle_history`.

Para Fase 2 debe extenderse a regenerar artefactos derivados desde el mismo origen o desde un `artifact_manifest`. Sin ese manifest, regenerar perfiles/presets podria perder relaciones internas.

## Separacion Core / Dominio / Artefacto

La separacion actual es sana:

- Core: servicios de preview, schema, materializacion, rollback y lifecycle.
- Dominio: `domain.json` y manifest de materializacion.
- Artefactos: todavia no materializados.
- Patrimonio compartido: catalogos globales fuera del sandbox.
- Integraciones externas: fuera de alcance.

Riesgo futuro: agentes y memoria pueden contaminar core si escriben directo en carpetas sin manifest. La Fase 2 debe reforzar que todo artefacto entra por servicios centrales.

## Pruebas de Resistencia Conceptual

### Caso A: sandbox grande

100 perfiles, 200 presets, 50 papers, 30 agentes y 10 equipos no bloquean la raiz actual, pero exigen manifest de artefactos y dependencias. Sin eso, rollback/regeneracion serian demasiado gruesos.

### Caso B: multiples generaciones

La base soporta generaciones mediante `generation_number`, `previous_materialization_id` y `lifecycle_history`. Para muchos artefactos, el historial debe incluir resumen por artefacto.

### Caso C: rollback parcial

No soportado todavia. No es necesario para `profile_catalog`/`agent_presets` iniciales si el rollback es completo, pero sera necesario antes de agentes/equipos.

### Caso D: migracion a operativo

No esta lista y no debe implementarse ahora. Requerira contrato de activacion PASSED, aprobacion, visibilidad, bloqueo de duplicados y promocion de rutas.

### Caso E: dominio archivado con patrimonio historico

La arquitectura bloquea legacy activo y protege `domains/loteria`. Para patrimonio historico futuro hace falta manifest de lineage y reglas de recuperacion por artefacto.

## Veredicto final

Si con ajustes menores.

El sandbox actual esta preparado para empezar la materializacion de `profile_catalog` y `agent_presets` siempre que Fase 2 comience por definir un manifest de artefactos sandbox. No esta listo para papers, agentes, equipos ni memoria sin contratos adicionales de dependencias, estados y rollback parcial.

Resultado operativo:

```txt
LISTO PARA PROMPT 2.0 CON AJUSTE MENOR OBLIGATORIO: artifact_manifest sandbox antes de escribir artefactos.
```
