# Lineage de agentes sandbox

## Proposito

`agent_lineage` registra por que existe un agente sandbox, de donde nace y como evoluciona.

No reemplaza al contrato de agente. Lo complementa:

- `sandbox_agent_schema` describe identidad y contrato del agente.
- `agent_lineage_schema` describe origen, historia, reemplazos y artefactos relacionados.

## Cadena de origen

La cadena obligatoria es:

```txt
profile_catalog_main
  -> agent_presets_main
    -> paper_seed_main
      -> agent_identity
        -> agent
```

El origen registra:

- `profile_catalog_artifact_id`;
- `source_profile_id`;
- `agent_presets_artifact_id`;
- `preset_id`;
- `paper_seed_artifact_id`;
- `paper_seed_id`.

## Identidad estable

Estrategia:

- `agent_id` sobrevive a regeneraciones y actualizaciones menores;
- `current_version` cambia cuando evoluciona la misma identidad;
- `history` conserva eventos de creacion, regeneracion, actualizacion, archivo o rollback;
- si la identidad ya no representa al mismo agente, se crea otro `agent_id`;
- el reemplazo se registra con `replaced_by`.

Esto permite evolucionar sin perder nacimiento ni contexto.

## Artifact Manifest

`artifact_manifest` alcanza como inventario de artefactos y dependencias.

`agent_lineage` no duplica el manifest; aporta metadata de historia:

- origen humano/tecnico;
- eventos evolutivos;
- reemplazos;
- artefactos relacionados.

El futuro artefacto `agent` podra embeber metadata de lineage en `created_from.lineage`.

## Memoria futura

La memoria no pertenece a lineage.

Lineage puede registrar que una memoria fue creada o reemplazada, pero la memoria persistente debe ser artefacto propio si existe:

- memoria propia del agente;
- memoria compartida del dominio;
- indice vectorial;
- herramientas con estado;
- evolucion aprendida.

En ese caso debe aparecer como `artifact_type: memory` y declarar dependencias.

## Relacion con PASSED

Lineage no vuelve operativo a un agente.

Un agente PASSED futuro requiere:

- contrato de agente valido;
- lineage valido;
- config materializada;
- paper operativo o conocimiento aprobado;
- modelo/policy validado;
- rollback;
- controles de memoria y herramientas;
- revision humana si aplica.

## Auditoria final

- Un agente futuro podra explicar por que existe.
- El nacimiento queda rastreado desde perfil, preset y paper seed.
- Los reemplazos no pisan historial.
- La arquitectura soporta evolucion con `history` y `current_version`.
- No se crean agentes ni memoria operativa en esta fase.
