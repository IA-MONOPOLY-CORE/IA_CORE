# Audit Store Internal Flows E2E Checkpoint

## 1. Resumen ejecutivo

Audit store esta listo como caja negra opcional para flujos internos antes de runtime. Promotion, active y runtime contract pueden enviar eventos observability al store append-only cuando `observability_context.persist_events=true` y existe `audit_store_path`.

Veredicto: `PASSED_AUDIT_STORE_INTERNAL_FLOWS_E2E`.

## 2. Flujo probado

```txt
promotion_executor -> observability events -> audit_store
active_executor -> observability events -> audit_store
runtime_contract -> observability events -> audit_store
```

El test usa cadena sandbox temporal y audit store en `tmp_path / "audit_store"`.

## 3. Eventos persistidos

| Event type | Module | Persisted | Sequence | Checksum | Correlation | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `promotion_executed` | `core.promotion_executor` | si | 1 | si | compartida | `applied` |
| `active_executed` | `core.active_executor` | si | 2 | si | compartida | `applied` |
| `runtime_contract_evaluated` | `core.runtime_contract` | si | 3 | si | compartida | `passed` |
| `mutation_scope_verified` | `core.active_executor` | si | 4 | si | compartida | `blocked` |
| `runtime_contract_blocked` | `core.runtime_contract` | si | 5 | si | compartida | `blocked` |
| `runtime_contract_blocked` | `core.runtime_contract` | si | 6 | si | compartida | `blocked` |
| `runtime_boundary_violation` | `core.runtime_contract` | si | 7 | si | compartida | `blocked` |
| `active_rollback_recorded` | `core.active_executor` | si | 8 | si | compartida | `rolled_back` |
| `promotion_rollback_recorded` | `core.promotion_executor` | si | 9 | si | compartida | `rolled_back` |

`snapshot_recorded` no se emite como evento independiente en esta fase; los snapshots quedan persistidos dentro de `snapshot_refs` de los eventos existentes.

## 4. Append-only

Cada evento se escribe como archivo nuevo bajo `events/` con secuencia incremental. La escritura usa create exclusivo y no hay helper publico de update/delete.

## 5. Verify chain

`verify_audit_store` valida:

- cantidad de archivos contra `event_count`;
- prefijo y `sequence_number`;
- `previous_event_checksum`;
- checksum del contenido;
- `last_event_checksum`;
- checksum del manifest.

## 6. Compatibilidad

Se valido:

- sin `observability_context`: los flujos siguen funcionando y no emiten eventos;
- con context sin store: los flujos siguen funcionando y reportan `audit_store_path_missing`;
- con context y store: los flujos persisten eventos append-only y verificables.

## 7. Failure handling

Politica real:

- los eventos se validan antes de persistir, por lo que un evento invalido no escribe parcial;
- si el store no existe, el helper devuelve `audit_store_error` sin crear store implicito;
- si el store esta tampered, `verify_audit_store` falla y la respuesta de persistencia reporta error controlado;
- la escritura opcional no habilita runtime ni execution;
- si la falla de persistencia ocurre despues de una mutacion funcional ya aplicada por el executor, el resultado reporta el error en `audit_store_result`. No se promete rollback automatico de target en esta fase.

## 8. No runtime

Los eventos persistidos mantienen:

- `runtime_allowed=false`;
- `execution_allowed=false`;
- `tool_execution_enabled=false`;
- `memory_persistence_enabled=false`.

Los flujos siguen siendo internos y declarativos; no se ejecutan agentes, equipos ni tools reales.

## 9. No contaminacion

Se tomaron snapshots antes/despues de:

```txt
domains/
agents/
catalogs/
papers/
```

No hubo cambios globales. La cadena modificada fue temporal en `tmp_path`.

## 10. Veredicto

`PASSED_AUDIT_STORE_INTERNAL_FLOWS_E2E`

Los flujos internos persisten eventos observability en audit store append-only sin romper compatibilidad ni habilitar runtime.

## 11. Recomendacion

Listo para disenar execution contract antes de runtime executor.

Motivo: audit store y observability ya pueden registrar flujos internos de forma opcional; antes de runtime conviene definir el contrato de execution para mantener la frontera runtime/execution explicita.
