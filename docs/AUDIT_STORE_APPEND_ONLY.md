# Audit Store Append-Only

## 1. Que es audit store

Audit store es una caja negra local para persistir eventos `observability` de IA_CORE en modo append-only logico y verificable. El objetivo es guardar evidencia correlacionable sin activar runtime, sin ejecutar agentes y sin tocar UI ni integraciones.

## 2. Que garantiza

- Append-only logico: cada append crea un archivo nuevo en `events/`.
- Inmutabilidad verificable: los eventos existentes no se actualizan desde la API publica.
- Checksum por evento: cada record incluye `checksum` estable.
- Chain de checksums: cada evento apunta al checksum del evento anterior con `previous_event_checksum`.
- Lectura ordenada por `sequence_number`.
- Deteccion de tampering por `verify_audit_store`.

## 3. Que no garantiza

- No es WORM fisico.
- No protege contra un actor con acceso total al filesystem que pueda reescribir todos los archivos y recalcular hashes.
- No usa base de datos externa.
- No implementa runtime executor.
- No habilita execution, tools reales, memoria real, UI ni integraciones.

## 4. Estructura de archivos

```txt
audit_store/
  store_manifest.json
  events/
    00000001_<event_id>.json
    00000002_<event_id>.json
```

`store_manifest.json` contiene `audit_store_id`, `store_mode`, `append_only=true`, `immutable_records=true`, `event_count`, timestamps, `last_event_checksum` y un checksum de manifest.

Cada evento persistido contiene el evento observability validado mas `sequence_number`, `previous_event_checksum`, `checksum` y `created_at`.

## 5. Checksum policy

El checksum usa JSON canonico con `sort_keys=True`, `ensure_ascii=True` y separadores estables. El checksum del evento excluye el propio campo `checksum`. El checksum del manifest cubre `event_count` y `last_event_checksum`.

## 6. Verify policy

`verify_audit_store` falla si:

- `event_count` no coincide con la cantidad de archivos;
- un archivo no respeta la secuencia esperada;
- un evento declara un `sequence_number` incorrecto;
- `previous_event_checksum` no coincide con el checksum anterior;
- el contenido de un evento ya no coincide con su `checksum`;
- el evento persistido ya no valida como observability event;
- `last_event_checksum` o el checksum del manifest son inconsistentes.

## 7. Integracion con observability

Los eventos generados por `promotion_executor`, `active_executor` y `runtime_contract` pueden persistirse con:

```python
from core.audit_store import append_audit_event

append_audit_event(store_path, observability_event)
```

El evento se valida antes de escribir. Si el evento es invalido, no se crea archivo parcial ni se actualiza el manifest.

## 8. Futuro

- Store persistente por proyecto o workspace.
- Politica de rotacion/export.
- Reportes y dashboard interno.
- Integracion controlada con audit views.
- Runtime executor futuro, en un prompt posterior y con frontera explicita.
