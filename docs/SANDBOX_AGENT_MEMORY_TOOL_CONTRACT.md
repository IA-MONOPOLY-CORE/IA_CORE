# Contrato de memoria y herramientas para agentes sandbox

## 1. Resumen

En esta fase, memoria y herramientas son capacidades declarativas de un agente sandbox.

No crean almacenamiento, no crean adapters, no llaman APIs, no ejecutan agentes y no convierten al agente en operativo.

Regla central:

```txt
capability declared != capability enabled != capability executed
```

Solo se permite `declared`.

## 2. Frontera

`declared` significa:

- la capacidad existe como intencion tecnica futura;
- esta serializada y validada;
- sirve para planificar memoria, herramientas, permisos y dependencias posteriores;
- no puede usarse en runtime.

`enabled` significa:

- la capacidad podria ser usada por runtime;
- requiere permisos, policy, auditoria y materializacion futura;
- esta bloqueada en este prompt.

`runtime` significa:

- hay ejecucion real, lectura/escritura externa o llamada de herramienta;
- pertenece a fases posteriores;
- esta prohibido en sandbox 2.5.

## 3. Memoria declarativa

El contrato vive en `core/sandbox_agent_memory_contract.py`.

Campos minimos:

- `memory_id`;
- `owner_agent_id`;
- `domain_id`;
- `memory_scope`;
- `memory_type`;
- `status`;
- `persistence`;
- `storage_backend`;
- `declared_only`;
- `runtime_enabled`;
- `dependencies`;
- `created_at`;
- `updated_at`.

Scopes permitidos:

- `agent`;
- `domain`;
- `team`;
- `global_future`.

Tipos permitidos:

- `none`;
- `ephemeral`;
- `documentary`;
- `vector_future`;
- `shared_future`.

Limites:

- `declared_only=true`;
- `runtime_enabled=false`;
- `status=declared`;
- sin vector DB;
- sin memoria persistente real;
- sin escritura en `memoria_agentes/`, `memory/`, `agents/` ni `domains/`.

La memoria persistente futura deberia ser artefacto separado si contiene estado propio, indices, aprendizaje, memoria compartida o rollback independiente.

## 4. Herramientas declarativas

El contrato vive en `core/sandbox_agent_tool_contract.py`.

Campos minimos:

- `tool_id`;
- `owner_agent_id`;
- `domain_id`;
- `tool_name`;
- `tool_category`;
- `status`;
- `declared_only`;
- `runtime_enabled`;
- `execution_allowed`;
- `external_access`;
- `dependencies`;
- `created_at`;
- `updated_at`.

Categorias permitidas:

- `internal_future`;
- `filesystem_future`;
- `api_future`;
- `browser_future`;
- `calendar_future`;
- `email_future`;
- `database_future`;
- `automation_future`.

Limites:

- `declared_only=true`;
- `runtime_enabled=false`;
- `execution_allowed=false`;
- `external_access=false`;
- `status=declared`;
- sin adapters;
- sin clients;
- sin llamadas externas;
- sin permisos runtime.

Las herramientas quedan como capability declarativa dentro del agente. En fases futuras podrian convertirse en artefactos separados si requieren estado, permisos, auditoria, versionado o rollback propio.

## 5. Seguridad

Bloqueos obligatorios:

- no runtime;
- no external access;
- no execution;
- no `active`;
- no legacy mutation;
- no escritura en `agents/`;
- no escritura en `domains/`;
- no modificacion de catalogos globales;
- no modificacion de papers globales.

`sandbox_agent_schema` acepta opcionalmente:

```json
{
  "capabilities": {
    "memory": [],
    "tools": []
  }
}
```

Si `capabilities` no existe, el agente sandbox sigue siendo valido.

Si existe, cada memoria y herramienta se valida como declarativa. Cualquier intento de `enabled=true`, `runtime_enabled=true`, `executable=true`, `execution_allowed=true`, `external_access=true` o `external_call=true` falla.

## 6. Futuro

Queda para fases posteriores:

- memoria persistente;
- vector store;
- tools reales;
- adapters;
- clients externos;
- permisos por usuario/rol/agente;
- capability policy;
- auditoria de ejecucion;
- equipos;
- UI;
- integraciones externas.

Recomendacion futura: crear una `capability_policy` antes de activar memoria o herramientas reales.
